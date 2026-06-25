---
citation_key: Kulathunga2024Resilient
arxiv_id: 2412.03174
arxiv_url: "https://arxiv.org/abs/2412.03174"
title: "Resilient Timed Elastic Band Planner for Collision-Free Navigation in Unknown Environments"
authors_short: "Geesara Kulathunga et al."
year: 2024
direction_tag: C_elastic_band
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:27:15Z
origin: ai+web
reviewed: false
---

# Resilient Timed Elastic Band Planner for Collision-Free Navigation in Unknown Environments

Geesara Kulathunga<sup>1</sup>, Abdurrahman Yilmaz<sup>1</sup>, Zhuoling Huang<sup>1</sup>,

Ibrahim Hroob<sup>1</sup>, Hariharan Arunachalam<sup>1</sup>, Leonardo Guevara<sup>1</sup>, Alexandr Klimchik<sup>1</sup>, Grzegorz Cielniak<sup>1</sup>, and Marc Hanheide<sup>1∗†</sup>

## Abstract

In autonomous navigation, trajectory replanning, refinement, and control command generation are essential for efective motion planning. This paper presents a resilient approach to trajectory replanning addressing scenarios where the initial planner’s solution becomes infeasible. The proposed method incorporates a hybrid A\* algorithm to generate feasible trajectories when the primary planner fails and applies a soft constraints-based smoothing technique to refine these trajectories, ensuring continuity, obstacle avoidance, and kinematic feasibility. Obstacle constraints are modelled using a dynamic Voronoi map to improve navigation through narrow passages. This approach enhances the consistency of trajectory planning, speeds up convergence, and meets real-time computational requirements. In environments with around 30% or higher obstacle density, the ratio of free space before and after placing new obstacles, the Resilient Timed Elastic Band (RTEB) planner achieves approximately 20% reduction in traverse distance, traverse time, and control efort compared to the Timed Elastic Band (TEB) planner and Nonlinear Model Predictive Control (NMPC) planner. These improvements demonstrate the RTEB planner’s potential for application in field robotics, particularly in agricultural and industrial environments, where navigating unstructured terrain is crucial for ensuring eficiency and operational resilience.

## 1 Introduction

Motion planning is essential for autonomous navigation, allowing robots to move through complex environments. This process involves determining optimal trajectories that robots can follow while ensuring safety and eficiency. With advancements in robotics and artificial intelligence, there has been a shift towards online trajectory replanning, refining, and control command generation, crucial components methods that allow robots to adapt to real-time changes in their surroundings, incorporating feedback from their sensors [Kulathunga et al., 2022b]. Unlike ofline planning, which relies on pre-defined paths, online methods facilitate dynamic adjustments, making them essential for applications in environments with unpredictable obstacles. However, achieving the balance between computational eficiency and the generation of kine matically and dynamically feasible trajectories remains a significant challenge in the field. Researchers are continuously exploring innovative strategies to enhance motion planning algorithms, focusing on real-time optimisation and the integration of various planning components to improve the overall robustness and adaptability of autonomous systems [Xiao et al., 2022]. However, formulating motion planning that ensures kinematic and dynamic feasibility while generating smooth control commands is computationally demanding [Meng et al., 2024].

The challenge in motion planning for autonomous robots stems from the need to integrate global and local planning components efectively. While global planning generates an initial path, it often overlooks the kinematic feasibility [Allozi et al., 2022], resulting in trajectories that the robot cannot physically follow. This limitation requires local planners to refine these paths, ensuring that the control commands respect both dynamic and kinematic constraints. Additionally, local planners must navigate a complex environment filled with both static obstacles, such as walls and trees, and dynamic ones like moving vehicles and pedestrians. This complexity demands rapid decision-making based on potentially noisy sensor data, mak ing real-time optimisation a critical yet challenging task. Furthermore, local planners must balance safety and eficiency, optimising paths in real-time while accounting for the various constraints imposed by the environment [Nair et al., 2024].

This research investigates resilient trajectory replanning in autonomous navigation frameworks. In general, many navigation frameworks comprise two primary planning modules: global and local planners. Resilient trajectory replanning is particularly essential for local planners when the planning visibility range is constrained, as it enables the system to adapt to environmental changes and prevents the planner from becoming infeasible.

The contributions of this paper are as follows:

Resilient trajectory generation: A hybrid A\* algorithm with a novel heuristic cost is proposed to generate such trajectories to handle cases where the TEB planner produces infeasible solutions. In such instances, the hybrid A\* generates a new kinematically feasible trajectory, which is then used to reinitialise the TEB planner. This approach accelerates the convergence of the TEB planner and improves the consistency of trajectory planning, particularly in cluttered environments. It provides smoother control commands and reduces sudden directional changes, focusing on car-like vehicles. This is especially relevant for field applications where diferential drive may not be feasible or desirable.

Resilient trajectory refinement procedure: This procedure is framed as a soft constraint-based optimization to refine trajectories generated by the proposed hybrid A\* algorithm. The refinement process incorporates considerations for trajectory continuity, obstacle avoidance, and kinematic feasibility. Obstacle constraints are defined using dynamic Voronoi maps, enabling smooth navigation through the constraint environments and reducing the need for replanning. As a result, the refined trajectories are both feasible and optimised for safety and eficiency in confined spaces.

Evaluating Resilient Planning in Obstacle-Constrained Scenarios: a comprehensive evaluation of the proposed approach through real-world experiments that validate various components of the proposed approach under diverse obstacle constraints.

The primary practical advantage of RTEB lies in its recovery behaviour, which is triggered mainly in obstacle dense environments, thereby reducing computational time. This approach leverages the strengths of the TEB planner along with the proposed recovery strategy, all while maintaining a moderate computational load.

## 2 Related work

Trajectory planning has evolved significantly, with various approaches developed to address the challenges posed by real-time, kinematic, and temporal constraints. Early methods like the Elastic Band (EB) approach [Quinlan, 1995] were initially introduced as a novel method that deforms the generated path while preserving the vehicle’s distance from obstacles by defi ning obstacle cost as a set of artificial forces. However, traditional trajectory planning methods generally do not incorporate kinematics and temporal constraints.

Subsequently, In [Delsart and Fraichard, 2008], they proposed a reactive trajectory deformation method that, instead of path deformation, includes temporal constraints to predict the future behaviours of obstacles. Given the computational demands of the methods mentioned, various sampling-based techniques like DWA [Fox et al., 1997] and MPPI [Kim et al., 2022] are well-suited for real-time trajectory planning in holonomic robots. However, sampling-based methods are not well-suited for trajectory planning in non-holonomic robots, such as car-like robots.

To meet the temporal, real-time, and kinematic constraints, the TEB [R¨osmann et al., 2015] planner was developed. This planner mimics a predictive controller behaviour through variable-length receding horizon trajectory planning. The trajectory planning problem is formulated as a hyper-graph [R¨osmann et al., 2013] and addressed as a sparse optimisation problem using the g2o [K¨ummerle et al., 2011] to ensure real-time computational eficiency. The Levenberg-Marquardt (LM) method [Ranganathan, 2004] is utilised for solving the trajectory planning problem due to its robustness and eficiency. Since g2o implements a sparse variant of LM, where nonlinear constraint terms influence only a subset of parameters, it eficiently balances the underlying Hessian calculation, ensuring real-time performance with minimal constraint settings.

Conversely, Model predictive control (MPC)-based trajectory planning [Qie et al., 2022] for autonomous ground vehicles (AUV) has gained popularity over the past decade, owing to advances in computational embedded systems and control schemes for robotics. MPC can be formulated in two ways: convex and nonconvex [Kulathunga and Klimchik, 2023]. When system dynamics and constraints are non-linear or nonconvex, it is necessary to use NMPC [Kulathunga et al., 2022a]. This may involve linearisation, applying Sequential Quadratic Programming (SQP) variations [Torrisi et al., 2016], or directly solving the non-linear formulation. Solving MPC non-linearly typically involves multiple shooting and direct collocation methods [Kulathunga et al., 2022a]. Many MPCs aim to minimise a cost function that penalises a combination of control error and other specified costs [R¨osmann et al., 2015] subject to provided hard and soft constraints. Time-optimal, point-to-point transitions [Van den Broeck et al., 2011] are generally not well-developed for real-time applications. In [R¨osmann et al., 2015], TEB was extended into MPC to achieve time-optimal point-to-point transitions. While MPC usually has a fixed receding horizon length, this work formulated MPC using TEB, retaining a discrete variable time interval between consecutive optimisation parameters. The MPC formulation becomes highly non-linear in cluttered environments, leading to high computational demands. Unless system dynamics are highly non-linear, TEB is an optimal choice as a local planner for autonomous navigation.

The TEB planner is not specifically designed for horizon-based planning methods like MPC. Instead, it utilises a variable horizon length approach, which focuses on point-to-point trajectory planning [Stefanini et al., 2024]. Intermediate goals are derived from a global path, enabling a quasi-pathfollowing strategy through waypoint navigation. However, the TEB planner’s computation time increases as the number of feasible points grows, due to the need to verify kinematic feasibility[Wullt et al., 2024]. While this approach converges more quickly in obstacle-free environments, it takes longer to reach a final consistent feasible trajectory in environments with many obstacles. In such cases, waypoint navigation with many fea sible points is less practical, as intermediate poses may end up within obstacle zones, leading to significantly higher computational costs. Moreover, if the global planner does not specify the orientations of the poses, the TEB planner defaults to a forward-oriented planning approach, aligning each pose’s orientation with the direction of the next pose in the path. This is less eficient when the robot can navigate in both forward and backward directions[Huajian et al., 2024]. The following timeline illustrates the evaluation of the timed elastic band planner and its variations in the recent past.

Social Elastic Band: predictive path optimisation for socially aware robot navigation[P´erez et al., 2024]

A nonlinear proportional function of tracking error recalibrates the robot control quantity [Liu and Liu, 2023]

DTEB Planner: Trajectory Sharing and Collision Prediction for Multi-Robot Systems 2022 ● [Chung et al., 2022]

Real-time motion planning utilising nonlinear model predictive control in conjunction with 2021 ó non-Euclidean rotation groups [Rsmann et al., 2021]

Dynamic obstacle-aware model predictive control for collaborative manipula-2020 ó tors [Kr¨amer et al., 2020]

Time-optimal nonlinear model predictive control [R¨osmann, 2019]2019

Timed Elastic Bands for eficient online motion planning of car-like robots [R¨osmann et al., 2017]

TEB for time-optimal point-to-point nonlinear model predictive control [R¨osmann et al., 2015]

“g2o” for solving “timed elastic band” problems [R¨osmann et al., 2013]2013

The ”timed elastic band” problem is expressed within a framework of weighted multiobjective optimisation [R¨osmann et al., 2012]

Conversely, a substantial body of prior research has introduced learning-based approaches for trajectory plan ning, with many utilising simulated environments to collect data for training purposes [Kadian et al., 2020, Chaplot et al., 2020, Tan et al., 2019, Chen et al., 2019]. Subsequently, various methods have employed real-world experiments to learn policies that generate control commands [Fang et al., 2023, Khazatsky et al., 2021, Shah et al., 2021]. These policies are primarily trained using reinforcement learning techniques. However, due to the inherent stochastic nature of these algorithms, they often struggle to generalise efectively to previously unseen environments [Kadian et al., 2020, Gervet et al., 2023]. To address these limitations, recent work has proposed the use of hierarchical reinforcement learning and generative models combined with high-level global planning [Faust et al., 2018, Li et al., 2020, Shah et al., 2023]. While these approaches ofer improvements, they also introduce additional computational complexity, rendering them unsuitable for real-time trajectory planning tasks. As a result, learning-based trajectory planning remains in its early stages and is not yet mature enough for practical real-world applications. In contrast, analytical methods continue to outperform these learning-based approaches, providing deterministic estimations of control commands, which ofer higher confidence and reliability for deployment in real-world scenarios.

In this work, the ROS2 navigation stack was selected to validate the proposed RTEB planner. Commonly used planners within ROS2 include TEB [R¨osmann et al., 2017b], NMPC [R¨osmann et al., 2021], the Dynamic Window Approach (DWA), and Model Predictive Path Integral (MPPI), among others [Houshyari and Sezer, 2022, Yucel et al., 2021]. Among the available options, TEB and NMPC are the most optimal for generating control commands, particularly for car-like robots, which is one of the main objectives, each utilising distinct techniques [R¨osmann et al., 2015, R¨osmann et al., 2021]. Table 2 lists the characteristics, pros, and cons of the aforementioned planners, including the proposed approach.

The primary drawback of the TEB and NMPC planners is that their computation time increases exponentially with the number of feasible points in TEB and the receding horizon length in NMPC, both of which require kinematic feasibility checks. In environments with fewer obstacles, such drawbacks can be alleviated by reducing the number of feasibility-checking points or shortening the planning horizon. However, substantial computational resources and time are required to generate feasible control commands. To tackle this issue, we introduced a resilient trajectory generation method followed by a smoothing technique for the TEB planner. Thus, the proposed approach is designed to regain functionality when the trajectory generated by the initial planner does not meet kinematic feasibility requirements to introduce resilient planning that enables recovery while managing moderate computational demands.

Table 1: The characteristics, pros, and cons of RTEB, TEB, NMPC, and MPPI trajectory planning methods.

<table><tr><td>Method</td><td>Pros</td><td>Cons</td></tr><tr><td>RTEB</td><td>- High success rate in complex environments- Moderate computation time- Bidirectional orientation flexibility (Hybrid A*)</td><td>- Higher computational cost compared to TEB when activating resilient planning- More complex implementation</td></tr><tr><td>TEB</td><td>- Moderate success rate- Efficient in environments with moderate complexity[Rahmani and et al., 2020]- Low computation time[Li and et al., 2019]</td><td>- Lower success rate in challenging environments [Wu et al., 2021]- Forward-oriented, limited orientation flexibility- Poor handling of narrow gaps [Wu et al., 2021]</td></tr><tr><td>NMPC</td><td>- High path efficiency [Ge et al., 2023]- Capable of handling dynamic and constrained systems</td><td>- Very high computational cost [Astudillo et al., 2024]- Low efficient in complex environments- High computation time [Astudillo et al., 2024]</td></tr><tr><td>MPPI</td><td>- Good balance between computation time and path efficiency [Kazim et al., 2024]- Due to its stochastic behaviour, performance depends on the implementation</td><td>- Less success rate in complex environments [Kazim et al., 2024]- Moderately high computational cost- Requires fine-tuning of parameters [Kazim et al., 2024]</td></tr></table>

## 3 Methodology

Building upon the advancements and limitations identified in previous methods, the proposed RTEB planner introduces several key innovative resilient (recovery) plans (Fig.1) to enhance the TEB planner [R¨osmann et al., 2017a]. First, it implements variable-length feasible global path generation, improving the eficiency of waypoint navigation. Second, during each planning iteration, the trajectory’s kinematic feasibility is assessed. If deemed infeasible, a hybrid A\* planner is employed, followed by a smoothing process to reinitialise the TEB planner’s current poses and update its optimisation (see Fig.2). This approach allows for rapid convergence to a feasible trajectory, bypassing the TEB planner’s slower and independent optimi sation process. Additionally, the hybrid A\* planner generates each intermediate pose with its orientation, independent of the global plan’s orientation, ensuring proper orientation adjustments when refining the TEB planner’s poses. This orientation estimation enables the robot to navigate eficiently in both forward and backward directions. Additionally, the RTEB supports precise goal alignment operations; for example, the robot’s orientation must closely match the desired alignment at the specific target location.

The following subsections highlight the key advancements introduced in the RTEB planner. Section 3.1 provides a mathematical formulation of the RTEB planner. In Section 3.1.1, a hybrid $\mathrm { A } ^ { * }$ algorithm with a novel heuristic cost is integrated to generate kinematically feasible trajectories when TEB trajectory generation fails, enabling seamless reinitialization of the TEB planner. Section 3.1.2 discusses the trajectory refinement process, which pushes the path into free space to minimize the need for frequent replanning. Finally, Section 3.1.3 introduces an accurate goal alignment procedure to ensure precise robot orientation at the target goal.

![](Kulathunga2024Resilient_figs/b406fd4763bc06a8d6c3c64d2ca53815a18d29a1ae1bfe3bf0a09c522d527085.jpg)  
Figure 1: Resilient Timed Elastic Band (RTEB) Planner Architecture: The resilient planning module extends the standard TEB planner by introducing enhanced recovery capabilities.

## 3.1 Resilient Timed Elastic Band planner: problem statement

The RTEB planner is formulated as a trajectory optimisation problem for a mobile robot, where each state $\mathbf { x } = [ x , y , \theta ] ^ { \top }$ denotes the robot’s position $( x , y )$ and orientation θ. The goal is to gBuilding upon the advancements and limitations identified in previous methods, tnerate a collision-free, smooth, and kinematically feasible trajectory $\mathcal { T } = \{ \mathbf { x } _ { t } \} _ { t = 0 } ^ { T }$ over a finite planning horizon T . Control inputs $\mathbf { u } = [ \phi , s ] ^ { \top }$ consist of the steering angle ϕ and motion arc length s, constrained to ensure the vehicle’s manoeuvrability. To meet trajectory refinement objectives, we minimise a cost function $J _ { t o t a l } .$ , which combines weighted sub-costs: obstacle avoidance $J _ { o b s }$ , curvature smoothness ${ { J } _ { c u r } } ,$ and path eficiency $J _ { p a t h }$ . Obstacle avoidance leverages a dynamic Voronoi field, penalising proximity to obstacles, while curvature and path length costs promote smoothness and directness of the trajectory. Additionally, goal alignment is achieved by ensuring that the trajectory approaches an intermediate pose near the target, with specific orientation $\theta _ { g }$ , to refine accuracy. This mathematical framework will guide the notation and conversion methods used in the subsequent sections of the paper.

## 3.1.1 Hybrid A\* with novel heuristic cost: recovery trajectory generation

Since we focus on car-like vehicles, the discrete-time state transition is expressed in the following way:

$$
\mathbf {x} _ {t + 1} = \mathbf {x} _ {t} + \left\{ \begin{array}{l l} \left( \begin{array}{c} k (\sin (\theta_ {t} + \frac {s}{k}) - \sin (\theta_ {t})) \\ - k (\cos (\theta_ {t} + \frac {s}{k}) - \cos (\theta_ {t})) \\ \frac {s}{k} \end{array} \right), & \text {if} \phi \neq 0 \\ \left( \begin{array}{c} s \cos (\theta_ {t}) \\ s \sin (\theta_ {t}) \\ 0 \end{array} \right), & \text {if} \phi = 0 \end{array} \right.
$$

![](Kulathunga2024Resilient_figs/7b7f24930abfc9c7ace5bb82ebed21024aff78e40088958dd39fd8c45d744dad.jpg)  
Figure 2: Trajectory planning using the RTEB planner – (a) The TEB planner initially fails to find a solution. (b) The dynamic Voronoi graph-based Voronoi field in (3) aids in pushing the hybrid $\mathrm { A } ^ { * }$ planned trajectory further away from obstacles. (c) Employing the proposed hybrid $\mathrm { A ^ { * } }$ planner followed by smoothing yields a feasible trajectory. (d) Reinitialisation of the TEB planner according to the planned path by Hybrid $\mathrm { A ^ { * } }$ and the newly planned feasible path. The global path was generated as a set of straight lines without considering obstacle avoidance to prevent any bias in the local planning.

where term $k = L / \tan ( \phi )$ and robot wheelbase is denoted by L. To define the initialisation of state propagation in hybrid $\mathrm { A ^ { * } }$ planning, let $\phi _ { \mathrm { m a x } }$ be the maximum steering angle and the term $r _ { s }$ be the resolution parameter for arc length division. Control input U set is defined for forward $( v _ { t } \ge 0 )$ and backward motions $( v _ { t } < 0 )$ as follows:

$$
\mathcal {U} = \left\{ \begin{array}{l} \big \{(\delta , a) \mid - \delta_ {\max} \leq \delta \leq \delta_ {\max}, \delta = r _ {s} \cdot \delta_ {\max}, r _ {s} \in \mathbb {R}, \\ \text {and} a = r _ {a} \cdot s _ {m a x}, r _ {a} \in \mathbb {R}, \left\{ \begin{array}{l} s _ {m a x} \leq a \leq 2 \cdot s _ {m a x}, \text {if} v _ {t} \geq 0 \\ - 2 \cdot s _ {m a x} \leq a \leq - s _ {m a x}, \text {if} v _ {t} <   0 \end{array} \right. \end{array} \right\}
$$

where steering angle δ is constrained to $[ - \delta _ { \mathrm { m a x } } , \delta _ { \mathrm { m a x } } ]$ and given by $\delta = r _ { s } \cdot \delta _ { \operatorname* { m a x } }$ . For non-negative velocity $v _ { t } \geq 0$ , the arc length a ranges from $s _ { \mathrm { m a x } }$ to $2 \cdot s _ { \mathrm { m a x } }$ and is scaled as $a = r _ { a } \cdot s _ { \operatorname* { m a x } } ,$ with $r _ { a } \in \mathbb { R }$ . For negative velocity $v _ { t } < 0 ,$ , a ranges from $- 2 \cdot s _ { \mathrm { m a x } }$ $\mathrm { t o } - s _ { \mathrm { m a x } } ,$ similarly scaled by $s _ { \mathrm { m a x } }$ . When the velocity $v _ { t }$ is non-negative, the inputs include positive accelerations; otherwise, they account for negative accelerations. The parameters used in the experiments, $r _ { s } = 0 . 3 , r _ { a } = 0 . 5$ , and $s _ { m a x } = 1 . 0$ , were determined through unbiased testing.

In the hybrid $\mathrm { A } ^ { * }$ planner, the heuristic $g _ { s c o r e } ^ { p }$ and $f _ { s c o r e } ^ { p }$ are calculated as follows:

$$
\begin{array}{r l} & g _ {s c o r e} ^ {p} = g _ {s c o r e} ^ {c} + \left\{ \begin{array}{l l} \lambda_ {f} \cdot | a | & \text {if} \zeta > 0 \\ \lambda_ {b} \cdot | a | & \text {if} \zeta \leq 0 \end{array} + \lambda_ {s} \cdot | \delta | \cdot | a | + \lambda_ {s c} \cdot | \delta - \phi_ {t} |, \zeta = \left\{ \begin{array}{l l} 1 & \text {if} a > 0, \\ - 1 & \text {if} a \leq 0. \end{array} \right. \right. \\ & f _ {s c o r e} ^ {p} = g _ {s c o r e} ^ {p} + \lambda_ {h e u} \cdot \eta \cdot \| \mathbf {x} _ {t} - \mathbf {x} _ {g} \| _ {2} \end{array}
$$

In this formulation, $g _ { s c o r e } ^ { p }$ represents the cost associated with transitioning from the current node to a specific node, where each node includes the robot’s desired state and control inputs during graph search.

It incorporates several components: $g _ { s c o r e } ^ { c }$ is the base cost from the current node, while $\lambda _ { f }$ and $\lambda _ { b }$ are penalties for forward and backward arc length changes, respectively. The term $\lambda _ { s } \cdot | \delta | \cdot | a |$ accounts for the penalty associated with steering, and $\lambda _ { s c } \cdot | \delta - \phi _ { t } |$ penalises changes in the steering angle. The cost to goal $f _ { s c o r e } ^ { p }$ is obtained by adding a heuristic component to $g _ { s c o r e } ^ { p }$ . This heuristic component, $\lambda _ { h e u } \cdot \eta \cdot \| \mathbf { x } _ { t } - \mathbf { x } _ { g } \| _ { 2 } .$ uses the Euclidean distance between the current state $\mathbf { x } _ { t }$ and the goal state $\mathbf { x } _ { g } .$ , scaled by the heuristic weight $\lambda _ { h e u }$ and a tie-breaking [Horne and Cole Smith, 2005] factor $\eta .$ The parameters that were used in experiments are $\lambda _ { f } = \lambda _ { b } = 1 . 0 , \lambda _ { s } = 0 . 5 , \lambda _ { s c } = 0 . 0 1 , \lambda _ { h e u } = 5 . 0 , \eta = 1 . 0 0 0 1$ , were estimated empirical testing. These parameters are integrated into the RTEB planner to balance smoothness, acceleration, and speed constraints, ensuring the generation of feasible and dynamically consistent trajectories that adhere to the robot’s physical limitations.

## 3.1.2 Trajectory refinement: enhancing free space navigation to minimise replanning

The hybrid $\mathrm { A ^ { * } }$ planned trajectory will be further refined using the proposed smoothing technique as outlined below. Smoothing helps push the planned trajectory away from obstacles that help to RTEB planner generate consistent control commands. The overall objective function for smoothing is expressed as:

$$
J _ {t o t a l} = \lambda_ {o b s} J _ {o b s} + \lambda_ {c u r} J _ {c u r} + \lambda_ {p a t h} J _ {p a t h},\tag{1}
$$

where $J _ { o b s } , J _ { c u r }$ , and $J _ { p a t h }$ are the costs associated with obstacles, path curvature, and path length improvement, respectively. The weights $\lambda _ { o b s } = 0 . 5 , \lambda _ { c u r } = 0 . 3$ , and $\lambda _ { p a t h } = 0 . 2$ were set based on empirical testing, prioritising obstacle cost over the other costs.

The obstacle cost, $J _ { o b s }$ , is evaluated using the Voronoi field approach [Lau et al., 2010], which improves upon the Artificial Potential Fields (APF) method. The APF method can create high-potential areas near narrow passages that obstruct robot movement, whereas the Voronoi field adjusts the potential based on the configuration space’s geometry, facilitating better navigation through tight spaces [Dolgov et al., 2008]. The obstacle cost is defined by:

$$
J _ {o b s} = \sum_ {p = 0} ^ {Q} F _ {v} (x _ {p}, y _ {p}),\tag{2}
$$

where $Q$ is the number of points along the planned trajectory. The Voronoi field value $F _ { v } ( x _ { p } , y _ { p } )$ is expressed as:

$$
F _ {v} (x _ {p}, y _ {p}) = A (x _ {p}, y _ {p}) \cdot S (x _ {p}, y _ {p}) \cdot R (x _ {p}, y _ {p})\tag{3}
$$

where:

$$
A (x _ {p}, y _ {p}) = 1 - \left(\frac {d _ {o b s} (x _ {p} , y _ {p})}{d _ {o b s} ^ {m a x}}\right) ^ {2}, S (x _ {p}, y _ {p}) = \frac {\lambda_ {v}}{\lambda_ {v} + d _ {o b s} (x _ {p} , y _ {p})}, R (x _ {p}, y _ {p}) = \frac {d _ {v o r} (x _ {p} , y _ {p})}{d _ {o b s} (x _ {p} , y _ {p}) + d _ {v o r} (x _ {p} , y _ {p})}.
$$

Here, $\lambda _ { v } > 0 \in \mathbb { R }$ governs the decay of influence for the Voronoi field [Lau et al., 2013], and $d _ { o b s } ^ { m a x } > 0 \in \mathbb { R }$ is the maximum allowable distance between the robot and closest obstacle pose. The function $d _ { o b s } ( \cdot )$ indicates the distance to the nearest obstacle, while $d _ { v o r } ( . )$ indicates the distance to the nearest Voronoi diagram edge.

The curvature penalty $J _ { c u r }$ measures how much the instantaneous curvature $k _ { p }$ deviates from a predefined maximum curvature $k _ { m a x }$ . This penalty is computed by summing the squared diferences between $k _ { p }$ and $k _ { m a x }$ . Here, $k _ { m a x }$ is the reciprocal of the minimum radius of curvature $\rho _ { m i n }$ , and it applies uniformly regardless of the curvature’s sign. The instantaneous curvature $k _ { p }$ is derived from the ratio of the angle change $\delta \theta _ { p }$ to the positional change $\delta x _ { p }$

$$
\begin{array}{l} {J _ {k} = \sum_ {p = 0} ^ {Q - 1} \left(k _ {p} - \left\{ \begin{array}{l l} 1 & \mathrm{if} k _ {p} > 0 \\ 0 & \mathrm{if} k _ {p} = 0 \\ - 1 & \mathrm{if} k _ {p} <   0 \end{array} \right\} \cdot k _ {m a x}\right) ^ {2},} \\ {k _ {p} = \Big (\mathrm{atan2} (\Delta y _ {p + 1}, \Delta x _ {p + 1}) - \mathrm{atan2} (\Delta y _ {p}, \Delta x _ {p}) \Big) / \Delta {\bf x} _ {p},} \end{array}\tag{4}
$$

where $\Delta x _ { p } = x _ { p } - x _ { p + 1 }$ <sub>1</sub> and $\Delta y _ { p } = y _ { p } - y _ { p + 1 }$ <sub>1</sub> represent the diferences in x and y coordinates between consecutive waypoints at the p-th index. The cost function for improving path length is defined by:

$$
J _ {p a t h} = \sum_ {p = 0} ^ {Q - 1} \| (\Delta x _ {p + 1}, \Delta y _ {p + 1}) - (\Delta x _ {p}, \Delta y _ {p}) \| ^ {2}\tag{5}
$$

The $J _ { p a t h }$ measures the deviation in path length by penalising changes in displacement between successive waypoints, encouraging a smoother trajectory with fewer abrupt changes in direction. This trajectory refinement process not only enhances trajectory feasibility by minimizing abrupt changes but also ensures safer navigation through complex environments, significantly improving the RTEB planner’s robustness and consistency.

## 3.1.3 Precise goal alignment

When the RTEB planner gets closer to the final goal, the proposed precise goal alignment procedure is activated as illustrated in Fig. 3. Following this, the RTEB planner calculates an intermediate pose $( x _ { i } , y _ { i } , \phi _ { g } )$ that is displaced by a distance $d _ { i } \in C , e . g .$ , 1.0m, from the goal pose $( x _ { g } , y _ { g } , \phi _ { g } )$ . The intermediate pose coordinates are determined by:

$$
x _ {i} = x _ {g} - d _ {i} \cos (\phi_ {g}), y _ {i} = y _ {g} - d _ {i} \sin (\phi_ {g}),
$$

where $( x _ { i } , y _ { i } )$ represents the intermediate position, and $\phi _ { g }$ denotes the goal orientation. The robot will start moving towards the goal pose as long as the distance between its current pose $( x _ { s } , y _ { s } , \phi )$ and the intermediate pose $( x _ { i } , y _ { i } )$ is within a threshold $d _ { r } \in C , i . e . , 0 . 1 m \colon$ $\sqrt { ( x _ { s } - x _ { i } ) ^ { 2 } + ( y _ { s } - y _ { i } ) ^ { 2 } } \leq d _ { r }$ . This method ensures that the robot is aligned with the desired goal orientation before reaching the goal pose, thereby enhancing the precision of the final orientation at the goal.

![](Kulathunga2024Resilient_figs/772a8ec8988febc7b2f2764ba79e5a69b6298e1dfcebec817925e7d01571c47c.jpg)  
Figure 3: The goal alignment behaviour of the RTEB planner is particularly crucial at the start of inrow navigation. This behaviour ensures that the vehicle aligns its orientation with the desired direction, facilitating a smoother and more accurate path following within the row.

By incorporating this precise alignment method, the RTEB planner ensures not only accurate goal-reaching behavior but also smooth and consistent orientation adjustments. This capability significantly improves the reliability and efectiveness of the planner in scenarios requiring high-precision navigation.

## 3.2 Integration of the RTEB with the ROS2 navigation stack

To validate the performance of the RTEB planner, we integrated it with the ROS2 navigation stack. The ROS2 navigation stack splits planning into two stages: global and local. In our setup, the proposed RTEB planner was employed as the local planner, while a custom global planner was developed to simplify the process. This global planner bypasses obstacle avoidance, generating a straight-line path between intermediate poses from the robot’s current position to the goal. Its primary function is to provide a consistent global path for the RTEB planner, whose evaluation takes place during the local planning stage.

## 3.2.1 Global planning with topological map manager

For localisation, we utilised RTK-GPS, and the mapping is handled through a spatiotemporal voxel mapper, as detailed in the following subsections. To generate global planning, we developed a Topological Map Manager (TMM)<sup>1</sup> (see Fig. 4), which functions as a high-level planning utility that guides robot behaviour across the provided environment. The TMM represents a high-level traversability graph as a set of nodes and edges, where each node attaches to a specific navigation action within the environment. Initially, the TMM performs root planning by navigating along the edges of the topological map, based on the robot’s current and target poses. Subsequently, the TMM generates an action message, which is processed by the nav through poses action server [Ghzouli et al., 2023] ROS2 navigation behaviour server. The TMM’s backend interfaces with the ROS2 navigation behaviour server, relaying responses to the TMM’s GOTO action server (Fig. 4), which serves as an intermediary between the ROS2 navigation behaviour server and front-end applications such as RViz. The ROS2 global planner then receives the initial path from the TMM and regenerates the global path as a series of straight lines. If the robot’s pose approaches the path’s edge, for example within 2 m (a configurable threshold), the planner will skip that close edge and connect to the subsequent one. The regenerated global path is shown as red dashed lines in Fig. 2. This global planning is performed without obstacle avoidance, primarily to ensure that the local planner receives the same global path, preventing any bias in its performance caused by the global plan. However, the proposed framework can also accommodate other global planning techniques.

![](Kulathunga2024Resilient_figs/a44b96e3afe4019999a5275e04ffb39901fd9f94318321344a9d465d13039dfa.jpg)  
Figure 4: The proposed navigation stack is built on the ROS2 navigation stack. It has specific ROS2- compatible plugins for global and local planning as well as local and global mapping. Topological map manager helps to generate an initial high-level root plan that subscribes by nav through poses action server along with a specific behaviour tree that depends on the action type that topological map manager provides.

## 3.3 Localisation and mapping

For localisation, we utilise RTK-GPS, which is particularly well-suited for outdoor navigation scenarios. On the other hand, for mapping, we implement a spatiotemporal voxel mapper, serving as the local cost map [Macenski et al., 2020]. Given the project’s focus on utilising low-cost sensors, we employ Livox LiDAR [Lin and Zhang, 2020], which, while cost-efective, tends to produce a significant amount of false positive data. Additionally, outdoor environments, in general, are characterised by uneven surfaces, further complicating the accurate interpretation of sensor data.

Consequently, it is crucial to address the challenge of distinguishing between ground and non-ground points in the input point clouds before integrating the data into the spatiotemporal voxel mapper. For this reason, the rough ground itself may sometimes be mistakenly perceived as an obstacle. In contrast, at other times, false positive measurements caused by the robot’s vertical oscillatory movements due to ground roughness can lead to incorrect detections. This preprocessing step is essential for mitigating the impact of false positives and ensuring the reliability of the mapping process. For a given set of point clouds, such as those obtained from LiDAR or depth cameras, the mapping utility processes the data to estimate the optimal spatial-temporal voxel clusters representing the environment. The processing workflow begins with ground removal, a critical step to isolate the relevant points from those representing the ground surface. For this task, Patchwork++ [Lim et al., 2021] is utilised, efectively removing the ground points from the initial point clouds.

## 4 Experimental procedure and results

In our study, we aimed to rigorously evaluate the performance of our proposed RTEB planner, specifically against two established planners, TEB and NMPC. These planners were implemented as local planners within the ROS2 navigation stack to support a consistent comparison framework. Our experiments were structured into two primary evaluations. The first experiment focused on goal alignment, comparing RTEB and TEB across various scenarios to assess each planner’s accuracy in maintaining goal-oriented navigation. The second experiment extended this evaluation to real-world and simulated environments with diverse obstacle densities, enabling a detailed comparison of RTEB’s robustness and adaptability compared to TEB and NMPC.

## 4.1 Experimental environment

The experimental environment for both simulation and real-world trials was based on a section of a strawberry farm located at the University of Lincoln, UK. As shown in Fig. 5, this environment provided a realistic and challenging setting for testing the proposed approach. To maintain consistency, the same environment was replicated in the Gazebo simulator, allowing for extensive testing and refinement of the navigation strategies in a controlled virtual setting. This approach facilitated iterative development, reducing the need for frequent field trials while ensuring the software’s readiness for real-world deployment. All simulated experiments took place in Gazebo, where the farm environment was modelled to match the physical setup closely. Using this simulated environment allowed for a safe and cost-efective method to try diferent navigation algorithms, especially under various controlled conditions that would be dificult to replicate outdoors. By fine-tuning the system within the simulator, we were able to ensure a higher level of robustness before conducting tests in the actual field.

## 4.2 Real-world platform: hardware and software stack overview

For the real-world experiments, we used the Agilex Hunter 2.0 platform<sup>2</sup>, a versatile and durable robotic platform optimised for outdoor environments. The robot was outfitted with several critical hardware components, including a Trimble RTK-GPS<sup>3</sup> for high-precision localization, essential for maintaining accurate navigation in agricultural settings. An Intel NUC i7-10710U<sup>4</sup> served as the onboard computer, managing the complex processing tasks associated with navigation, sensor integration, and control. Fig. 5 illustrates the complete hardware configuration.

![](Kulathunga2024Resilient_figs/db870582267f0044b464fc740bb2f10a5a5260b795d932984998e71f4ec9a20d.jpg)  
Figure 5: Real-world testing environment and robot equipped with sensors

The navigation stack was implemented in C++ within the ROS2 framework, adhering to ROS2’s pluginbased architecture. Each navigation plugin was designed to align with ROS2’s standards, allowing seamless integration with other ROS2 components and supporting future updates or adaptations. This modular approach enabled us to develop a flexible and eficient navigation solution suitable for both simulation and real-world testing, facilitating smooth transitions between the two environments.

## 4.3 Performance evaluation of the proposed RTEB planner

In the first experiment, we assessed the goal alignment capabilities of the RTEB planner in comparison with TEB across several defined scenarios. This experiment involved a controlled setup where the start and target orientations were maintained constant, while the displacement between them varied, simulating a parallel parking task (as depicted in Fig. 6). Displacement values ranged from 2 m to 4 m, increasing in 0.5 m steps, with each scenario corresponding to specific displacement values (e.g., scenario 1 is set to 2 m, and scenario 5 to 4 m), as shown in Table 2. We established a tolerance threshold of 0.2 m for XY positioning and 0.1 rad for yaw to ensure meaningful comparisons of goal alignment accuracy. To evaluate performance, we measured three main criteria: the traverse distance, the traversal time (T ), and control efort $\begin{array} { r } { \left( \int _ { 0 } ^ { T } \| \mathbf { u } ( t ) \| ^ { 2 } d t \right) } \end{array}$ , where the control input vector u comprises linear velocity v and angular velocity ω values over time. Each scenario was repeated ten times to account for variability, and we present the averaged results with standard deviations in Table 2.

The results in Table 2 demonstrate a significant improvement in RTEB’s performance over TEB across three key metrics: traverse distance, traverse time, and control efort. Paired t-tests [Hsu and Lachenbruch, 2014] were used to assess the statistical significance of the diferences between RTEB and TEB for each metric. For the traverse time, the p-value was $p = 0 . 0 0 2$ , indicating a statistically significant diference, suggesting that RTEB consistently reaches the target faster than TEB. This time eficiency could be advantageous in applications where rapid task completion is essential. Similarly, the control efort metric showed a significant diference, with a p-value of $p = 0 . 0 0 5$ . Control efort, calculated as the integral of squared control inputs, reflects the smoothness and energy expenditure of the robot’s movement. This result implies that RTEB and TEB difer in terms of motion smoothness and energy eficiency, with RTEB ofering a more refined control strategy. In contrast, for traverse distance, the p-value was $p = 0 . 2 0 9$ , indicating no significant diference in the total distance travelled. This suggests that RTEB and TEB are equally efective in minimizing the path length required to reach the goal.

![](Kulathunga2024Resilient_figs/04f4e38e2f0ace54a11daf77c76f3f538131346e44ca1bdaaa5e9f0ae8464cf8.jpg)  
(a)

![](Kulathunga2024Resilient_figs/f565698137235b9fd8d3b4c4114df79a6c1b8f303d0992bf93f1397803c5cbb4.jpg)  
Figure 6: The comparison of planning performance evaluates the goal alignment estimation of RTEB in relation to TEB. In this scenario (the second scenario in Table2, which involves a 2.5m displacement between the starting and target poses), the starting and target poses remain constant. The robot is planned and navigated twice using each method. RTEB generates more consistent trajectories, while TEB exhibits variability over time.

Table 2: Comparison of goal alignment performance improvement in RTEB compared to TEB (values are given as $\mu \pm \sigma )$

<table><tr><td rowspan="2">Scenario</td><td colspan="2">Traverse Distance (m)</td><td colspan="2">Traverse Time (s)</td><td colspan="2">Control Effort</td></tr><tr><td>TEB</td><td>RTEB</td><td>TEB</td><td>RTEB</td><td>TEB</td><td>RTEB</td></tr><tr><td>1</td><td>3.00 ± 1.15</td><td>2.86 ± 0.87</td><td>21.52 ± 3.95</td><td>18.00 ± 2.88</td><td>4.78 ± 1.25</td><td>3.82 ± 1.21</td></tr><tr><td>2</td><td>4.78 ± 1.32</td><td>4.51 ± 1.25</td><td>33.00 ± 1.25</td><td>26.00 ± 2.12</td><td>10.36 ± 1.55</td><td>6.41 ± 1.38</td></tr><tr><td>3</td><td>5.41 ± 1.36</td><td>5.95 ± 1.28</td><td>37.54 ± 2.10</td><td>32.00 ± 3.00</td><td>18.12 ± 2.48</td><td>13.00 ± 1.32</td></tr><tr><td>4</td><td>8.54 ± 1.30</td><td>6.55 ± 0.74</td><td>49.61 ± 4.20</td><td>41.00 ± 1.05</td><td>24.77 ± 1.65</td><td>18.79 ± 1.50</td></tr><tr><td>5</td><td>11.17 ± 1.41</td><td>8.97 ± 0.81</td><td>55.21 ± 1.50</td><td>48.00 ± 2.45</td><td>27.58 ± 2.72</td><td>8.96 ± 1.60</td></tr></table>

Overall, while both algorithms perform similarly in traverse distance, RTEB and TEB display significant diferences in traverse time and control efort, which could impact their suitability for specific applications. Additionally, RTEB consistently demonstrates lower mean values and standard deviations across all metrics, indicating improved eficiency and reduced variability in goal alignment scenarios. For example, in Scenario 1, RTEB reduced the traverse time by an average of 16.4%, alongside a notable decrease in control efort. This trend is consistent across various displacement scenarios, with RTEB achieving shorter distances, times, and more eficient control inputs, particularly in Scenarios 4 and 5. As shown in Fig. 6, RTEB provides superior goal alignment, resulting in more consistent and reliable trajectories. These findings support RTEB as a robust approach for applications demanding precise and eficient goal alignment.

![](Kulathunga2024Resilient_figs/1b422de50a340ee1034b5d06f2c5d64c5f47cee8b4fa3996601f28258469a18d.jpg)

![](Kulathunga2024Resilient_figs/eccf091cd036b21b9f9314c4258ff2e6579e009847ff70b3e58488c39dca7636.jpg)

![](Kulathunga2024Resilient_figs/3d6b9f7c019da6e053e728da15d3dee72a096920a9ce8f2460eecb10d964ee00.jpg)

![](Kulathunga2024Resilient_figs/675d614c58984f1479f671b851dd46694deab7201e9fd5b071731e39c42a05cd.jpg)

![](Kulathunga2024Resilient_figs/e5874b3421d1da7d0bcfc65ed34165211a3e4cac2f45bba5272d7959536a14fe.jpg)

(a)  
![](Kulathunga2024Resilient_figs/a256f270bbf40584fb3fd269b8a003da71a2cd12538d67873679492d0485d11b.jpg)  
(b)

![](Kulathunga2024Resilient_figs/427d7d392ac15066d8d055a75feefa79af9d6667bf6151ca5527ee31333493b5.jpg)

![](Kulathunga2024Resilient_figs/21a40de077f2dde74f240f605dc1bf5c3a1408ca47fbfa78baa5f0383a766b9b.jpg)  
Figure 7: Performance evaluation of RTEB, TEB, NMPC, and MPPI in randomised dense obstacle simulated environments

In this second experiment, we evaluated the performance of RTEB, TEB, NMPC, and MPPI in randomised dense obstacle scenarios across five simulated environments (see Fig. 7 for examples). Each environment featured four distinct start and goal position pairs, with twenty trials conducted per pair. These environments comprised static obstacles randomly arranged in a confined 3D space, creating narrow gaps and challenging navigation conditions. The goal was to assess each planner’s eficiency in traversing narrow gaps while minimizing collisions and path deviations. To quantify environmental complexity, we used the average width of the two narrowest gaps as a benchmark. This metric was computed by measuring gap widths between adjacent obstacles, sorting them in ascending order, and averaging the two smallest values. The resulting narrow gap widths ranged from 1.5 m to 2.5 m, highlighting the most dificult passages for navigation. By focusing on these critical gaps, the complexity metric ensures a representative assessment of each algorithm’s performance under challenging conditions. The results of this experiment are summarised in Table 3.

Table 3: Performance comparison of trajectory planning methods in scenarios involving narrow gaps within the environment

<table><tr><td>Metric</td><td>RTEB</td><td>TEB</td><td>NMPC</td><td>MPPI</td></tr><tr><td>Success Rate (%)</td><td>90</td><td>80</td><td>75</td><td>70</td></tr><tr><td>Path Efficiency (Path Ratio)</td><td>0.91</td><td>0.72</td><td>0.68</td><td>0.62</td></tr><tr><td>Maximum Planning Frequency (Hz)</td><td>17</td><td>13</td><td>12</td><td>20</td></tr><tr><td>Handling Narrow Gaps</td><td>Good</td><td>Moderate</td><td>Moderate</td><td>Moderate</td></tr><tr><td>Orientation Flexibility</td><td>Bidirectional (Hybrid A*)</td><td>Forward-Oriented</td><td>Bidirectional</td><td>Bidirectional</td></tr><tr><td>Adaptability to Complexity</td><td>High</td><td>Medium</td><td>Medium</td><td>Medium</td></tr></table>

Across several key metrics, RTEB consistently outperformed the other methods, demonstrating its robustness and eficiency in complex navigation scenarios. In terms of success rate, the percentage of trials in which the planner completed the task without collisions or failures, RTEB achieved 90%, significantly higher than TEB (80%), NMPC (75%), and MPPI (70%). This indicates that RTEB is more reliable in successfully navigating dense obstacle environments with narrow gaps. Such a high success rate underscores its ability to efectively plan and execute feasible trajectories even under challenging conditions. Path eficiency, the ratio of the actual path length taken by the planner to the shortest possible path length, further reinforces RTEB’s superiority. It achieved a ratio of 0.91, closely approximating the feasible path, while TEB (0.72), NMPC (0.68), and MPPI (0.62) displayed lower eficiency. This demonstrates that RTEB generates shorter, smoother trajectories, minimizing deviations from the ideal path while navigating narrow gaps.

The maximum planning frequency, the highest rate at which the planner can generate updated trajectories, reflects the computational performance of each method. RTEB operated at 17 Hz, outperforming TEB (13 Hz) and NMPC (12 Hz), though MPPI achieved the highest frequency (20 Hz). However, while MPPI’s higher frequency may enable rapid re-planning, its lower path eficiency and success rate suggest it struggles with the complexities of narrow gaps, making RTEB a more balanced choice for such environments. In terms of handling narrow gaps, a qualitative assessment of the planner’s ability to navigate through tight spaces or obstacles with minimal clearance: ”Good,” and ”Moderate” indicates the relative efectiveness in such scenarios, RTEB is rated ”Good,” while the other planners are rated ”Moderate.” Orientation flexibility highlights RTEB and MPPI as bidirectional planners, with RTEB leveraging Hybrid A\* for enhanced flexibility, whereas TEB is constrained to forward-oriented planning. Finally, adaptability to complexity, which evaluates how well the planner performs in environments with high levels of obstacle density, shows RTEB rated ”High,” while the others are ”Medium,” underscoring RTEB’s superior robustness when increasing obstacle density.

The goal of the final experiment is to comprehensively compare the trajectory planning performance of three diferent planners: TEB planner, RTEB (the proposed planner), and NMPC [R¨osmann et al., 2021]. This comparison was conducted in both simulated and real environments with obstacle densities of 20%, 30%, 40%, and 50% (Fig.8), complemented by maintaining a minimum distance of 2.5 m between obstacles. Obstacle density was estimated as the ratio of free space before placing obstacles to the free space after placing new obstacles, expressed as a percentage. A common reference path is used for all test cases to ensure comparability of results across diferent obstacle densities and environments. The Gazebo provides a controlled setting in the simulated environment where obstacle densities are systematically varied. The same environmental configurations and obstacle densities are replicated in the real-world setup to validate the simulation results. Performance is assessed based on traverse distance, traverse time (T ), control efort $\begin{array} { r } { ( \int _ { 0 } ^ { T } | \mathbf { u } ( t ) | ^ { 2 } d t ) } \end{array}$ , speed range (minimum and maximum speeds), and maximum planning frequency (the average time taken per planning iteration). Each experiment was conducted five times, and the average values are presented in Table 4.

![](Kulathunga2024Resilient_figs/2f9a2850d95c40174c60019cda9da454411f47c587a45dc7021af63b4881ec77.jpg)  
Figure 8: Left: example of the simulated experiment setup in Gazebo, showcasing the environment with varying obstacle densities used to validate TEB versus RTEB performance. Right: The final trajectories for TEB and RTEB methods illustrate the paths navigated through the obstacle-laden environment.

Table 4 reveals that RTEB consistently outperforms TEB, particularly in environments with increasing obstacle density, where RTEB’s stability is reflected by its lower standard deviation values across traverse distance, time, and control efort metrics. This stability is crucial for applications in dynamic and densely populated environments, as it implies that RTEB provides more predictable and reliable trajectory outcomes under challenging conditions. Additionally, RTEB’s ability to maintain a comparable or slightly higher planning frequency than TEB across most scenarios indicates its computational eficiency despite handling complex path adjustments. For example, all planners perform similarly at a low obstacle density of 20%, with TEB and RTEB achieving nearly identical distances of around 63 m, while NMPC covers a slightly longer distance of 71.82 m. As the obstacle density increases, NMPC tends to cover longer distances, particularly at 40% density, where it records 97.21 m compared to RTEB’s 77.11 m, which is the shortest distance among the planners. In real environments, the planners show similar trends, with NMPC consistently covering the longest distance, particularly at 40% density (100.64 m), suggesting a potential trade-of between distance and obstacle avoidance. Therefore, NMPC, while occasionally producing smoother trajectories (noted by tighter control efort and speed variation), experiences a decline in planning frequency and robustness, especially at higher obstacle densities. This decrease suggests that NMPC, although useful in smoother, less complex setups, may not be as suited for dynamic environments requiring rapid, adaptive path adjustments.

Table 4: Comparison of trajectory planning performance across various environmental settings in real and simulated setups

<table><tr><td colspan="2">Attempt</td><td colspan="3">Traverse Distance [m]</td><td colspan="3">Traverse Time [s]</td><td colspan="3">Control Effort</td></tr><tr><td rowspan="5">Simulation</td><td>obstacle density</td><td>TEB</td><td>RTEB</td><td>NMPC</td><td>TEB</td><td>RTEB</td><td>NMPC</td><td>TEB</td><td>RTEB</td><td>NMPC</td></tr><tr><td>20%</td><td>65.32</td><td>65.33</td><td>71.82</td><td>167.00</td><td>171.00</td><td>191.00</td><td>70.70</td><td>69.20</td><td>78.31</td></tr><tr><td>30%</td><td>76.59</td><td>69.21</td><td>79.29</td><td>230.00</td><td>178.00</td><td>218.00</td><td>83.39</td><td>77.45</td><td>93.21</td></tr><tr><td>40%</td><td>115.54</td><td>77.11</td><td>97.21</td><td>352.00</td><td>216.00</td><td>249.00</td><td>140.77</td><td>79.13</td><td>168.34</td></tr><tr><td>50%</td><td>145.54</td><td>120.11</td><td>NaN</td><td>432.02</td><td>257.00</td><td>NaN</td><td>196.40</td><td>100.11</td><td>NaN</td></tr><tr><td rowspan="4">Real-world</td><td>20%</td><td>65.89</td><td>66.40</td><td>73.12</td><td>168.10</td><td>170.00</td><td>196.00</td><td>67.82</td><td>68.87</td><td>70.78</td></tr><tr><td>30%</td><td>78.9</td><td>70.39</td><td>81.29</td><td>239.00</td><td>181.00</td><td>226.00</td><td>85.21</td><td>78.29</td><td>95.69</td></tr><tr><td>40%</td><td>112.16</td><td>78.28</td><td>100.64</td><td>347.00</td><td>220.00</td><td>256.00</td><td>135.28</td><td>81.37</td><td>173.25</td></tr><tr><td>50%</td><td>162.54</td><td>138.11</td><td>NaN</td><td>448.02</td><td>269.00</td><td>NaN</td><td>212.40</td><td>114.11</td><td>NaN</td></tr><tr><td colspan="2">Attempt</td><td colspan="3">Speed (min, max) [m/s]</td><td colspan="3">MaximumPlanningFrequency [Hz]</td><td></td><td></td><td></td></tr><tr><td rowspan="5">Simulation</td><td>obstacle density</td><td>TEB</td><td>RTEB</td><td>NMPC</td><td>TEB</td><td>RTEB</td><td>NMPC</td><td></td><td></td><td></td></tr><tr><td>20%</td><td>±0.51</td><td>±0.53</td><td>0.52</td><td>20±3</td><td>20±2</td><td>17±5</td><td></td><td></td><td></td></tr><tr><td>30%</td><td>±0.81</td><td>±0.76</td><td>±0.76</td><td>19±3</td><td>17±5</td><td>12±5</td><td></td><td></td><td></td></tr><tr><td>40%</td><td>±0.54</td><td>±0.54</td><td>±0.78</td><td>17±4</td><td>16±4</td><td>9±5</td><td></td><td></td><td></td></tr><tr><td>50%</td><td>±0.52</td><td>NaN</td><td>NaN</td><td>15±3</td><td>14±5</td><td>NaN</td><td></td><td></td><td></td></tr><tr><td rowspan="4">Real-world</td><td>20%</td><td>±0.55</td><td>±0.55</td><td>±0.54</td><td>19±3</td><td>19±5</td><td>15±5</td><td></td><td></td><td></td></tr><tr><td>30%</td><td>±0.55</td><td>±0.55</td><td>±0.55</td><td>17±3</td><td>14±5</td><td>11±5</td><td></td><td></td><td></td></tr><tr><td>40%</td><td>±0.53</td><td>±0.54</td><td>±0.58</td><td>15±4</td><td>11±5</td><td>7±5</td><td></td><td></td><td></td></tr><tr><td>50%</td><td>±0.83</td><td>±0.52</td><td>NaN</td><td>15±3</td><td>14±5</td><td>NaN</td><td></td><td></td><td></td></tr></table>

NaN: the planner is unable to reach the target location and continues to loop around.

For a traverse time, the analysis reveals that the time required increases significantly with obstacle density across all planners. However, RTEB generally results in shorter traverse times compared to TEB and NMPC, particularly in denser environments. For instance, at 40% obstacle density in simulated environments, RTEB and TEB take the average of 216 s and 352 s. This pattern holds in real environments, where RTEB consistently shows shorter times, with a notable gap at higher densities, such as 220 s for RTEB versus 347 s for TEB at 40% density. When considering control efort, which reflects the intensity of manoeuvres required to avoid obstacles, it is observed that control efort increases with obstacle density across all planners. NMPC generally demands the highest control efort, especially at high densities, reflecting its more aggressive obstacle avoidance strategy. In simulated environments, NMPC’s control efort reaches 168.34 at 40% density, while RTEB shows relatively stable and lower control eforts. Similar trends are observed in real environments, with NMPC again requiring the highest control efort (173.25 at 40% density), indicating its resource-intensive nature compared to TEB and RTEB, which demonstrate more eficiency.

This suggests that the modifications in RTEB enhance its ability to handle dense environments more eficiently. Overall, RTEB’s balance of eficiency and adaptability makes it a strong candidate for real-world applications where reliability and computational load are both critical factors, particularly in more complex environments with higher obstacle densities. In obstacle-free environments, there is no notable diference between TEB and RTEB, as the recovery mechanism is unnecessary. As a result, within the RTEB planner, the recovery mechanism remains inactive, and planning proceeds without it, which is advantageous in terms of computational cost.

## 5 Conclusion

This paper introduces RTEB, an enhanced version of the Timed Elastic Band (TEB) planner, designed to outperform both TEB and Nonlinear Model Predictive Control (NMPC) in terms of traverse time and control efort, particularly in complex and dense environments. One of the key innovations of RTEB is the incorporation of a resilient trajectory generation method, which leverages a hybrid A\* algorithm to reinitialise the TEB planner when it encounters failure situations. This capability significantly enhances the planner’s consistency and speed, particularly in environments with high clutter and dynamic obstacles, where traditional planning methods often struggle to maintain eficient and feasible solutions.

Additionally, RTEB integrates a soft constraints-based smoothing utility that further refines the generated trajectories. This utility ensures that the resulting paths are not only eficient but also safe, smooth, and feasible. The soft constraints allow for the inclusion of dynamic and environmental factors that afect the robot’s motion, such as changes in velocity or unforeseen obstacle movements. This refinement ensures that the robot can navigate through complex, cluttered spaces with minimal control efort, while also adhering to safety constraints. These features collectively contribute to the robust and flexible nature of RTEB, making it an ideal choice for autonomous navigation in unknown, dynamically changing environments.

For the validation of the proposed RTEB planner, we utilised the ROS2 navigation stack, exploiting the available local planners, specifically TEB and NMPC. While several recent trajectory planning approaches, such as the Spatial-Temporal Trajectory Planner [Han et al., 2023], OBTPAP [Li et al., 2021], and DL-IAPS+PJSO [Zhou et al., 2020], have demonstrated strong performance in ROS1 environments, their adaptation to ROS2 has proven to be time-consuming due to various system constraints. Consequently, we opted to validate our RTEB approach against the more widely adopted TEB and NMPC planners. In future work, we aim to validate RTEB against these recent methods once their ROS2 implementations are available, expanding the comparison to understand better RTEB’s performance in relation to these state-of-the-art planners.

Furthermore, the resilient trajectory generation approach introduced in this paper is highly adaptable and can be integrated with any local planning method, ofering flexibility for various robot configurations and environments. Looking ahead, we plan to integrate RTEB with Nonlinear Model Predictive Control (NMPC), further enhancing its capabilities. However, the integration of RTEB with NMPC presents certain challenges. Unlike TEB, which utilises a variable receding horizon for planning, NMPC relies on a fixed receding horizon, which may afect the implementation of the resilient planning strategy. To address this, we foresee the need for a cascade planning approach that harmonises soft and hard constraints within the NMPC framework, enabling real-time performance without compromising trajectory quality. This research direction will be a focus of future work, aiming to bridge the gap between these two powerful planning methods and enhance the robustness and eficiency of autonomous navigation systems.

## Acknowledgements

This work was supported by the Innovate UK-funded project Agri-OpenCore [grant number 10041179].

## References

[Allozi et al., 2022] Allozi, E., Yilmaz, A., Ervan, O., and Temeltas, H. (2022). Feasibility analysis of path planning algorithms. In 2022 International Conference on INnovations in Intelligent SysTems and Applications (INISTA), pages 1–6. IEEE.

[Astudillo et al., 2024] Astudillo, A., Florez, A., Decr´e, W., and Swevers, J. (2024). Rapid deployment of model predictive control for robotic systems: From impact to ros 2 through code generation. In 2024 IEEE 18th International Conference on Advanced Motion Control (AMC), pages 1–6. IEEE.

[Chaplot et al., 2020] Chaplot, D. S., Jiang, H., Gupta, S., and Gupta, A. (2020). Semantic curiosity for active visual learning. In Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part VI 16, pages 309–326. Springer.

[Chen et al., 2019] Chen, T., Gupta, S., and Gupta, A. (2019). Learning exploration policies for navigation. arXiv preprint arXiv:1903.01959.

[Chung et al., 2022] Chung, Y. M., Youssef, H., and Roidl, M. (2022). Distributed timed elastic band (dteb) planner: Trajectory sharing and collision prediction for multi-robot systems. In 2022 International Conference on Robotics and Automation (ICRA), pages 10702–10708. IEEE.

[Delsart and Fraichard, 2008] Delsart, V. and Fraichard, T. (2008). Reactive trajectory deformation to navigate dynamic environments. In European Robotics Symposium 2008, pages 233–241. Springer.

[Dolgov et al., 2008] Dolgov, D., Thrun, S., Montemerlo, M., and Diebel, J. (2008). Practical search techniques in path planning for autonomous driving. Ann Arbor, 1001(48105):18–80.

[Fang et al., 2023] Fang, K., Yin, P., Nair, A., Walke, H. R., Yan, G., and Levine, S. (2023). Generalization with lossy afordances: Leveraging broad ofline data for learning visuomotor tasks. In Conference on Robot Learning, pages 106–117. PMLR.

[Faust et al., 2018] Faust, A., Oslund, K., Ramirez, O., Francis, A., Tapia, L., Fiser, M., and Davidson, J. (2018). Prm-rl: Long-range robotic navigation tasks by combining reinforcement learning and sampling based planning. In 2018 IEEE international conference on robotics and automation (ICRA), pages 5113– 5120. IEEE.

[Fox et al., 1997] Fox, D., Burgard, W., and Thrun, S. (1997). The dynamic window approach to collision avoidance. IEEE Robotics & Automation Magazine, 4(1):23–33.

[Ge et al., 2023] Ge, L., Zhao, Y., Zhong, S., Shan, Z., and Guo, K. (2023). Eficient nonlinear model predictive motion controller for autonomous vehicles from standstill to extreme conditions based on split integration method. Control Engineering Practice, 141:105720.

[Gervet et al., 2023] Gervet, T., Chintala, S., Batra, D., Malik, J., and Chaplot, D. S. (2023). Navigating to objects in the real world. Science Robotics, 8(79):eadf6991.

[Ghzouli et al., 2023] Ghzouli, R., Berger, T., Johnsen, E. B., Wasowski, A., and Dragule, S. (2023). Behavior trees and state machines in robotics applications. IEEE Transactions on Software Engineering, 49(9):4243–4267.

[Han et al., 2023] Han, Z., Wu, Y., Li, T., Zhang, L., Pei, L., Xu, L., Li, C., Ma, C., Xu, C., Shen, S., et al. (2023). An eficient spatial-temporal trajectory planner for autonomous vehicles in unstructured environments. IEEE Transactions on Intelligent Transportation Systems.

[Horne and Cole Smith, 2005] Horne, J. A. and Cole Smith, J. (2005). Dynamic programming algorithms for the conditional covering problem on path and extended star graphs. Networks: An International Journal, 46(4):177–185.

[Houshyari and Sezer, 2022] Houshyari, H. and Sezer, V. (2022). A new gap-based obstacle avoidance approach: follow the obstacle circle method. Robotica, 40(7):2231–2254.

[Hsu and Lachenbruch, 2014] Hsu, H. and Lachenbruch, P. A. (2014). Paired t test. Wiley StatsRef: statistics reference online.

[Huajian et al., 2024] Huajian, L., Wei, D., Shouren, M., Chao, W., and Yongzhuo, G. (2024). Sampleeficient learning-based dynamic environment navigation with transferring experience from optimizationbased planner. IEEE Robotics and Automation Letters.

[Kadian et al., 2020] Kadian, A., Truong, J., Gokaslan, A., Clegg, A., Wijmans, E., Lee, S., Savva, M., Chernova, S., and Batra, D. (2020). Sim2real predictivity: Does evaluation in simulation predict realworld performance? IEEE Robotics and Automation Letters, 5(4):6670–6677.

[Kazim et al., 2024] Kazim, M., Hong, J., Kim, M.-G., and Kim, K.-K. K. (2024). Recent advances in path integral control for trajectory optimization: An overview in theoretical and algorithmic perspectives. Annual Reviews in Control, 57:100931.

[Khazatsky et al., 2021] Khazatsky, A., Nair, A., Jing, D., and Levine, S. (2021). What can i do here? learning new skills by imagining visual afordances. In 2021 IEEE International Conference on Robotics and Automation (ICRA), pages 14291–14297. IEEE.

[Kim et al., 2022] Kim, T., Park, G., Kwak, K., Bae, J., and Lee, W. (2022). Smooth model predictive path integral control without smoothing. IEEE Robotics and Automation Letters, 7(4):10406–10413.

[Kr¨amer et al., 2020] Kr¨amer, M., R¨osmann, C., Hofmann, F., and Bertram, T. (2020). Model predictive control of a collaborative manipulator considering dynamic obstacles. Optimal Control Applications and Methods, 41(4):1211–1232.

[Kulathunga et al., 2022a] Kulathunga, G., Devitt, D., and Klimchik, A. (2022a). Trajectory tracking for quadrotors: An optimization-based planning followed by controlling approach. Journal of Field Robotics, 39(7):1001–1011.

[Kulathunga et al., 2022b] Kulathunga, G., Hamed, H., Devitt, D., and Klimchik, A. (2022b). Optimizationbased trajectory tracking approach for multi-rotor aerial vehicles in unknown environments. IEEE Robotics and Automation Letters, 7(2):4598–4605.

[Kulathunga and Klimchik, 2023] Kulathunga, G. and Klimchik, A. (2023). Survey on motion planning for multirotor aerial vehicles in plan-based control paradigm. Remote Sensing, 15(21):5237.

[K¨ummerle et al., 2011] K¨ummerle, R., Grisetti, G., Strasdat, H., Konolige, K., and Burgard, W. (2011). g 2 o: A general framework for graph optimization. In 2011 IEEE international conference on robotics and automation, pages 3607–3613. IEEE.

[Lau et al., 2010] Lau, B., Sprunk, C., and Burgard, W. (2010). Improved updating of euclidean distance maps and voronoi diagrams. In 2010 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 281–286. IEEE.

[Lau et al., 2013] Lau, B., Sprunk, C., and Burgard, W. (2013). Eficient grid-based spatial representations for robot navigation in dynamic environments. Robotics and Autonomous Systems, 61(10):1116–1130.

[Li et al., 2021] Li, B., Acarman, T., Zhang, Y., Ouyang, Y., Yaman, C., Kong, Q., Zhong, X., and Peng, X. (2021). Optimization-based trajectory planning for autonomous parking with irregularly placed obstacles: A lightweight iterative framework. IEEE Transactions on Intelligent Transportation Systems, 23(8):11970– 11981.

[Li et al., 2020] Li, C., Xia, F., Martin-Martin, R., and Savarese, S. (2020). Hrl4in: Hierarchical reinforcement learning for interactive navigation with mobile manipulators. In Conference on Robot Learning, pages 603–616. PMLR.

[Li and et al., 2019] Li, W. and et al. (2019). Teb combined with neural networks for obstacle handling in robotics. Artificial Intelligence Review, 52(4):1873–1888.

[Lim et al., 2021] Lim, H., Minho, O., and Myung, H. (2021). Patchwork: Concentric zone-based regionwise ground segmentation with ground likelihood estimation using a 3d lidar sensor. IEEE Robotics and Automation Letters.

[Lin and Zhang, 2020] Lin, J. and Zhang, F. (2020). Loam livox: A fast, robust, high-precision lidar odometry and mapping package for lidars of small fov. In 2020 IEEE international conference on robotics and automation (ICRA), pages 3126–3131. IEEE.

[Liu and Liu, 2023] Liu, C. and Liu, Y. (2023). Robot planning and control method based on improved time elastic band algorithm. In 2023 4th International Conference on Computer Engineering and Application (ICCEA), pages 911–915.

[Macenski et al., 2020] Macenski, S., Tsai, D., and Feinberg, M. (2020). Spatio-temporal voxel layer: A view on robot perception for the dynamic world. International Journal of Advanced Robotic Systems, 17(2).

[Meng et al., 2024] Meng, D., Chu, H., Tian, M., Gao, B., and Chen, H. (2024). Real-time high-precision nonlinear tracking control of autonomous vehicles using fast iterative model predictive control. IEEE Transactions on Intelligent Vehicles.

[Nair et al., 2024] Nair, S. H., Lee, H., Joa, E., Wang, Y., Tseng, H. E., and Borrelli, F. (2024). Predictive control for autonomous driving with uncertain, multimodal predictions. IEEE Transactions on Control Systems Technology.

[P´erez et al., 2024] P´erez, G., Zapata-Cornejo, N., Bustos, P., and N´u˜nez, P. (2024). Social elastic band with prediction and anticipation: Enhancing real-time path trajectory optimization for socially aware robot navigation. International Journal of Social Robotics, pages 1–23.

[Qie et al., 2022] Qie, T., Wang, W., Yang, C., Li, Y., Zhang, Y., Liu, W., and Xiang, C. (2022). An improved model predictive control-based trajectory planning method for automated driving vehicles under uncertainty environments. IEEE Transactions on Intelligent Transportation Systems, 24(4):3999–4015.

[Quinlan, 1995] Quinlan, S. (1995). Real-time modification of collision-free paths. Stanford University.

[Rahmani and et al., 2020] Rahmani, K. and et al. (2020). Adaptation of teb for uavs and swarm robotics in complex terrain. In 2020 IEEE International Conference on Robotics and Automation, pages 2341–2346.

[Ranganathan, 2004] Ranganathan, A. (2004). The levenberg-marquardt algorithm. Tutoral on LM algorithm, 11(1):101–110.

[R¨osmann, 2019] R¨osmann, C. (2019). Time-Optimal Nonlinear Model Predictive Control. PhD thesis, Faculty of Electrical Engineering and Information Technology at Technische Universit¨at Dortmund.

[R¨osmann et al., 2012] R¨osmann, C., Feiten, W., W¨osch, T., Hofmann, F., and Bertram, T. (2012). Trajectory modification considering dynamic constraints of autonomous robots. In ROBOTIK 2012; 7th German Conference on Robotics, pages 1–6. VDE.

[R¨osmann et al., 2013] R¨osmann, C., Feiten, W., W¨osch, T., Hofmann, F., and Bertram, T. (2013). Eficient trajectory optimization using a sparse model. In 2013 European Conference on Mobile Robots, pages 138– 143. IEEE.

[R¨osmann et al., 2015] R¨osmann, C., Hofmann, F., and Bertram, T. (2015). Timed-elastic-bands for time optimal point-to-point nonlinear model predictive control. In 2015 european control conference (ECC), pages 3352–3357. IEEE.

[R¨osmann et al., 2017a] R¨osmann, C., Hofmann, F., and Bertram, T. (2017a). Integrated online trajectory planning and optimization in distinctive topologies. Robotics and Autonomous Systems, 88:142–153.

[R¨osmann et al., 2017b] R¨osmann, C., Hofmann, F., and Bertram, T. (2017b). Kinodynamic trajectory optimization and control for car-like robots. In 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 5681–5686. IEEE.

[R¨osmann et al., 2021] R¨osmann, C., Makarow, A., and Bertram, T. (2021). Online motion planning based on nonlinear model predictive control with non-euclidean rotation groups. In 2021 European Control Conference (ECC), pages 1583–1590. IEEE.

[Rsmann et al., 2021] Rsmann, C., Makarow, A., and Bertram, T. (2021). Online motion planning based on nonlinear model predictive control with non-euclidean rotation groups. In 2021 European Control Conference (ECC), pages 1583–1590.

[R¨osmann et al., 2013] R¨osmann, C., Feiten, W., W¨osch, T., Hofmann, F., and Bertram, T. (2013). Eficient trajectory optimization using a sparse model. In 2013 European Conference on Mobile Robots, pages 138– 143.

[R¨osmann et al., 2017] R¨osmann, C., Hofmann, F., and Bertram, T. (2017). Kinodynamic trajectory optimization and control for car-like robots. In 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 5681–5686.

[Shah et al., 2021] Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., and Levine, S. (2021). Rapid exploration for open-world navigation with latent goal models. arXiv preprint arXiv:2104.05859.

[Shah et al., 2023] Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., and Levine, S. (2023). Vint: A foundation model for visual navigation. arXiv preprint arXiv:2306.14846.

[Stefanini et al., 2024] Stefanini, E., Palmieri, L., Rudenko, A., Hielscher, T., Linder, T., and Pallottino, L. (2024). Eficient context-aware model predictive control for human-aware navigation. IEEE Robotics and Automation Letters.

[Tan et al., 2019] Tan, H., Yu, L., and Bansal, M. (2019). Learning to navigate unseen environments: Back translation with environmental dropout. arXiv preprint arXiv:1904.04195.

[Torrisi et al., 2016] Torrisi, G., Grammatico, S., Smith, R. S., and Morari, M. (2016). A variant to sequential quadratic programming for nonlinear model predictive control. In 2016 IEEE 55th Conference on Decision and Control (CDC), pages 2814–2819. IEEE.

[Van den Broeck et al., 2011] Van den Broeck, L., Diehl, M., and Swevers, J. (2011). A model predictive control approach for time optimal point-to-point motion control. Mechatronics, 21(7):1203–1212.

[Wu et al., 2021] Wu, J., Ma, X., Peng, T., and Wang, H. (2021). An improved timed elastic band (teb) algorithm of autonomous ground vehicle (agv) in complex environment. Sensors, 21(24):8312.

[Wullt et al., 2024] Wullt, B., Mattsson, P., Sch¨on, T. B., and Norrl¨of, M. (2024). A model predictive control approach to motion planning in dynamic environments. In 2024 European Control Conference (ECC), pages 3247–3254. IEEE.

[Xiao et al., 2022] Xiao, X., Liu, B., Warnell, G., and Stone, P. (2022). Motion planning and control for mobile robot navigation using machine learning: a survey. Autonomous Robots, 46(5):569–597.

[Yucel et al., 2021] Yucel, B., Yilmaz, A., Ervan, O., and Temeltas, H. (2021). Fuzzy controlled adaptive follow the gap obstacle avoidance algorithm. In Proceedings of the 7th International Conference on Robotics and Artificial Intelligence, pages 93–98.

[Zhou et al., 2020] Zhou, J., He, R., Wang, Y., Jiang, S., Zhu, Z., Hu, J., Miao, J., and Luo, Q. (2020). Autonomous driving trajectory optimization with dual-loop iterative anchoring path smoothing and piecewise-jerk speed optimization. IEEE Robotics and Automation Letters, 6(2):439–446.