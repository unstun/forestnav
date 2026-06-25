---
citation_key: GonzlezCalvin2024SingularityFree
arxiv_id: 2412.13033
arxiv_url: "https://arxiv.org/abs/2412.13033"
title: "Singularity-Free Guiding Vector Field over Bézier's Curves Applied to Rovers Path Planning and Path Following"
authors_short: "Alfredo González-Calvin et al."
year: 2024
direction_tag: P_nonholonomic_constraints
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:26:55Z
origin: ai+web
reviewed: false
---

# Singularity-Free Guiding Vector Field over Bézier’s Curves applied to Rovers Path Planning and Path following.

Alfredo González-Calvin Dept. Arquitectura de Computadores y Automática Facultad de Ciencias Físicas. Universidad Complutense Madrid, Spain alfredgo@ucm.es

Lía García-Pérez Dept. Arquitectura de Computadores y Automática Facultad de Ciencias Físicas. Universidad Complutense Madrid, Spain liagar05@ucm.es

Juan F. Jiménez Dept. Arquitectura de Computadores y Automática Facultad de Ciencias Físicas. Universidad Complutense Madrid, Spain juan.jimenez@fis.ucm.es

## Abstract

This paper presents a guidance algorithm for solving the problem of following parametric paths, as well as a curvature-varying speed setpoint for land-based car-type wheeled mobile robots (WMRs). The guidance algorithm relies on Singularity-Free Guiding Vector Fields SF-GVF. This novel GVF approach expands the desired robot path and the Guiding vector field to a higher dimensional space, in which an angular control function can be found to ensure global asymptotic convergence to the desired parametric path while avoiding field singularities. In SF-GVF, paths should follow a parametric definition. This feature makes using Bezier’s curves attractive to define the robot’s desired path. The curvaturevarying speed setpoint, combined with the guidance algorithm, eases the convergence to the path when physical restrictions exist, such as minimal turning radius or maximal lateral acceleration. We provide theoretical results, simulations, and outdoor experiments using a WMR platform assembled with of-the-shelf components. The small Rover (WMR) selected provides an easy-to-use non-holonomic platform for the experiments. The results could be extrapolated to full-scale or more complex vehicles, providing the necessary vehicle control system adaptations, while the GVF algorithm would remain the same.

Keywords Wheeled Mobile Robots, Guiding Vector Fields, Parametric Paths, Path following, Speed controller, curvature changing speed setpoint, Rover.

## 1 Introduction

Autonomous Mobile Robots (AMRs) have become a broad research area with applications in many fields; from automatic storage systems in warehouses, environment monitoring, post-catastrophe inspection, and emergency rescue to planetary exploration, the presence of AMRs is ubiquitous. A review of the categories and applications of AMRs can be found in (Rubio et al., 2019).

Following a classical scheme, (Siegwart et al., 2011, page 10), the mobility control of the AMR could be divided into two main tasks: perception and motion control. We are interested in motion control since it makes the AMR follow a planned path(s) (path following).

There are certain types of AMR applications in which the robots are required to pass through specified points that an expert user defines. For example, environmental monitoring robots (Hitz et al., 2017) that take samples or measurements at points of interest, surveillance robots that need to visit specific locations (Thakur et al., 2013), agricultural robots that must apply treatments at designated locations (Bechar and Vigneault, 2016; Bechar and Vigneault, 2017), or delivery robots (Mathew et al., 2015) that have to deliver products to defined locations. Usually, the robot’s human operators have prior knowledge of the mission. They can plan the robot’s path by breaking it into feasible trajectories. This can be done using maps or photographs of the terrain the robots will traverse and defining a set of waypoints that the Rover should visit or at least pass close to. The robot, in turn, must generate and follow a trajectory that ensures these points are reached. In some cases, it is helpful for the user to define, in addition to the waypoints, an area within which the trajectory is restricted, for example, for safety reasons. Think, for instance, about rovers for outdoor exploration or patrol. They should be able to cope with unstructured environments where slopes, terrain irregularities, and obstacles could hamper the Rover’s performance.

However, for a robot to be able to follow a path visiting specific waypoints autonomously, it is not enough to define the trajectory between them. To make it an autonomous system, an AMR must be able to drive itself, be aware of its state, avoid obstacles, etc., and ultimately reach its predetermined goals. For this purpose, once a suitable trajectory has been defined for the AMR, it is essential to provide a motion control algorithm that allows it to follow the trajectory correctly. The control algorithm can be divided into Guidance and Navigation.

The guidance controller provides the desired setpoints (e.g., position, heading and speed) to take the robot from its current state (i.e., position, attitude and speed) to the desired trajectory. When planning a trajectory, we may consider the mission the robot has to accomplish as the starting point. This planning process must take into account the kinematic and dynamic constraints. Our robot is a typical nonholonomic system, a (four) Wheeled Mobile Robot, WMR, with a minimum turning radius and maximum acceleration limits to avoid wheel slippage, lateral skidding or robot overturning. The latter two could be estimated using an Inertial Unit on board (Nourizadeh et al., 2023).

In some cases, the upper and lower speed limits are mission-dependent, while in others, the speed limit is fixed during the whole mission. Using the first approach, we can facilitate the operator’s search for feasible trajectories by linking the speed control to the curvature of the trajectory, thus connecting it to the guidance controllers. Therefore, it is suficient to define waypoints to design a reasonable path, avoiding significant obstacles and sharp turns, and leave it to the guidance system to adjust the speed to follow the resulting trajectory.

The AMR navigation comprises headings and speed control to allow the robot to follow the desired trajectory. It is linked to the mechanical characteristics of the robot and the specific onboard actuators and sensors.

This paper outlines the development, simulation, and field experimentation of a navigation system based on waypoints. This system is implemented and tested on a small, land-based, four-wheeled mobile robot (WMR) with a low-cost onboard electronic system. We give this particular type of WMR the generic name

of Rover because it can move over rough terrain.

The Rover has to pass through the waypoints determined by the user. These waypoints are connected by Bézier curves, whose first and last points are the waypoints, while the rest of them (control points) allow the route to remain within safe navigation zones. The Rover’s task is to follow the trajectory calculated using the Bézier curves. The user can modify waypoints and control points during the mission and send them to the Rover. When the Rover receives them, a new trajectory is generated. The path-following system, consisting of guidance and speed control, computes the appropriate commands to enable the Rover to follow the trajectory through the waypoints. We use Guidance Vector Fields (GVF), in particular, the novel Singular Free Parametric GVF (SF-GVF) methodology (Yao, 2021), to set the heading and the curvature of the trajectory to set the speed. A non-linear control strategy for the heading ensures mathematical convergence to the path. In addition, we use a linear controller for the speed.

As we shall describe later in the paper, SF-GVF requires defining parametric curves to determine the robot’s path. However, this can be challenging in real-world applications, especially when the robot moves in nonstructured environments. To address this issue, we propose using Bezier curves, which are parametric curves well-suited for defining the robot’s path in SF-GVF. This approach can make it easier to apply SF-GVF to real-world scenarios. The user only needs to specify the control points for the Bezier curve and then check whether the resulting path meets their requirements.

Results of the guidance and navigation controllers are presented first in simulation and after with a real Rover in a natural environment. In both cases, the Paparazzi environment was used (Gati and Balazs, 2013). Paparazzi autopilot has been used together with GVF for UAVs (Kapitanyuk et al., 2017),(De Marina et al., 2017).

In the following sections of the paper, we will progressively develop our proposal according to the following sequence: Section 2 describes a simple Rover model that will be employed later to build the guidance control system. Section 3 deals with the SF-GVF guidance approach, the Rover steering control description and its stability properties. Section 4 explains the use of Bézier curves in path planning and discusses their main advantages and disadvantages. Section 5 presents the speed controller used in our Rover and the curvature-varying setpoint. Section 6 is devoted to simulated and experimental results, briefly introducing the Paparazzi ecosystem, an open-source software platform we use to develop Rover onboard code and simulate and monitor experiments with a team of small Rovers. Eventually, we close the work in section 7, drawing some conclusions.

## 2 Rover model

Our Rover is a four-wheeled WMR with a spring suspension system to ensure maximum contact between the wheels and the ground. Two fixed rear wheels on a joint axle and two front steering wheels, a car-like or type (1,1) according to (Siciliano and Khatib, 2008) robot classification.

## 2.1 Basic model assumptions

Figure 1 depicted an outline of a four-wheeled vehicle. As it is known, a four-wheeled car will not skid if the longitudinal axis of each wheel is aligned with the circumferences they trace around to the center of rotation. For this purpose, an Ackermann steering linkage can be employed, in which each wheel turns a diferent angle when tracing a curve, according to well-known equations (Siciliano and Khatib, 2008). However, when conditions are ideal (i.e., no skid), the two wheels of an Ackerman drive can be replaced by a virtual single wheel situated at the center of the front axis, that is, in the direction of motion of the Rover. Therefore, in figure 1, the angle θ represents the Rover’s heading in an inertial frame $W ( p ) , p = ( p _ { x } , p _ { y } ) \in \mathbb { R } ^ { 2 }$ attached to the earth and the angle ϕ is the angle between the longitudinal axis of the car (i.e., its direction of motion)

![](GonzlezCalvin2024SingularityFree_figs/02a8e23f75197d259e84750a967af666293af958eabb8039191db4147f573bdc.jpg)  
Figure 1: Representation of a simple four-wheeled car with wheelbase l. The car is shown in light blue, while the virtual front wheel is shown in red. The direction of motion is shown with a blue line, and the direction of the virtual wheel is shown in red.

and the virtual single wheel (shown in red). Then, the velocity can be computed as:

$$
\left\{ \begin{array}{l l} \dot {p} _ {x} & = v \cos (\theta) \\ \dot {p} _ {y} & = v \sin (\theta) \end{array} \right.\tag{1}
$$

where v is the speed in the direction of motion. Now let r be the distance travelled by the car (by its rear axis), and let R be the instantaneous radius of rotation. An infinitesimal displacement in the distance implies $d r = R d \theta$ , and it can be seen that $\begin{array} { r } { R = \frac { l } { \tan \left( \phi \right) } } \end{array}$ . Then $\begin{array} { r } { \dot { r } = v = \frac { l } { \tan ( \phi ) } \dot { \theta } . } \end{array}$ , where l represents the wheelbase of the vehicle. Finally, assume that the control input is the angular rotation of the virtual front wheel $\dot { \phi } = u _ { \phi }$ then the model can be represented a

$$
\left\{ \begin{array}{l l} \dot {p} _ {x} & = v \cos (\theta) \\ \dot {p} _ {y} & = v \sin (\theta) \\ \dot {\theta} & = v \frac {\tan \phi}{l} \\ \dot {\phi} & = u _ {\phi} \end{array} \right.\tag{2}
$$

with the condition that $\begin{array} { r } { - \frac { \pi } { 2 } < \phi < \frac { \pi } { 2 } } \end{array}$ to stay in the approximation of no skid. We may consider $- \phi _ { m a x } <$ $\phi < \phi _ { m a x }$ , with $\phi _ { m a x }$ , the maximum turn angle the wheels can rotate around their vertical axis. Usually, ϕ<sub>max</sub> $\approx \frac { \pi } { 6 }$

## 2.2 Rover kinematic equations

If the control signal $u _ { \phi }$ can modify the value of ϕ practically instantaneously $\displaystyle ( \mathrm { i . e . , ~ } \phi = u _ { \phi } )$ , then we can consider for the Rover the following non-holonomic model,

$$
\left\{ \begin{array}{l l} \dot {p} _ {x} & = v \cos (\theta) \\ \dot {p} _ {y} & = v \sin (\theta) \\ \dot {\theta} & = u _ {\theta} \end{array} \right.\tag{3}
$$

and the angle of the virtual front wheel can be computed as $\begin{array} { r } { \phi = \arctan \left( \frac { l u _ { \theta } } { v } \right) } \end{array}$

Eventually, we arrive at a simple unicycle model. Besides, we conducted experiments using small RC Rovers propelled by electrical motors, so we can take $v = u _ { v } ,$ , acting directly on the Rover’s speed, disregarding inertial and resistance to advance.

![](GonzlezCalvin2024SingularityFree_figs/27d26775de494b0c8e1e5dbc5b5ffd7a3d6bbc80d5113777e79dd76b4ed33354.jpg)  
Figure 2: Illustration of the relationship among $\mathcal { P } , { } ^ { a u g } \mathcal { P } , \phi _ { 1 } ( \xi )$ and $\phi _ { 2 } ( \xi )$ . P is a Bézier’s curve of degree 4, with control points $\mathcal { C } = \{ ( 1 , 1 ) , ( 3 , - 4 ) , ( 1 , 0 ) , ( 3 , 4 ) , ( 1 , - 1 ) \}$

## 3 Parametric GVF for Rover guidance and path following

Many algorithms for path following can be found in the literature. Among them, some of the most common are carrot chasing (Safwat et al., 2018), line-of-sight (Gu et al., 2022), or pure pursuit (Samuel et al., 2016) A complete survey and comparison can be found in (Sujit et al., 2014), where authors show using simulations that Vector Field (VF) is the technique that more accurately follows the path. We use the Guiding Vector fields methodology to guide the Rovers. At each point in space, the GVF provides a suitable heading direction for the Rover to converge towards the target path or remain on it when reached. This work is based on a novel methodology, Singularity Free parametric GVF (SF-GVF), (Yao et al., 2021), which extends GVF to deal with self-intersecting paths and singularities (i.e. points at which the vector field is null) by defining parametric curves in an augmented space, where all singular points are removed.

Parametric GVF was designed to work with paths described by generic parametric equations in $\mathbb { R } ^ { 3 }$ and $\mathbb { R } ^ { 2 }$ . In this last case:

$$
\mathcal {P} := \{p _ {x} = f _ {1} (w), p _ {y} = f _ {2} (w) \},\tag{4}
$$

where w is the parameter of the path, $p _ { x } , p _ { y } \in \mathbb { R } ^ { 2 }$ and $f _ { 1 } , f _ { 2 } \in C ^ { 2 }$ . Therefore, even though we are working with Bézier curves, any parametric curve could be used.

## 3.1 Guidance problem

The guiding vector field should be designed so that their integral curves converge to the desired path. Thus, if the vehicle aligns with the vector field, it will converge to the desired path. This approach is known as the vector-field guided path-following navigation problem; it can be briefly described as follows (Yao et al., 2021):

Problem 1 (The vector-field guided path-following navigation problem). Given a desired path $\mathcal { P } \subset \mathbb { R } ^ { n }$ , to design a continuous diferentiable vector field $\chi : \mathbb { R } ^ { n } \to \mathbb { R } ^ { n }$ such that the dynamical system $\dot { \xi } ( t ) = \chi ( \xi ( t ) )$ fulfills the following two conditions:

1. There is a neighborhood of $\mathcal { D } \subseteq \mathbb { R } ^ { n }$ such that for all $\xi ( 0 ) \in { \mathcal { D } }$ the distance between ξ(t) and P

approaches to zero as $t \to \infty$

2. If a trajectory starts on the desired path, it remains in the desired path. $\xi ( 0 ) \in \mathcal { P } \Rightarrow \xi ( t ) \in \mathcal { P } , \forall t \geq 0$

To design an appropriate SF-GVF, we first define the following surfaces, departing from the definition of the desired path $\mathcal { P }$ in (4),

$$
\phi_ {1} (\xi) = p _ {x} - f _ {1} (w), \phi_ {2} (\xi) = p _ {y} - f _ {2} (w),\tag{5}
$$

where $\xi = ( p _ { x } , p _ { y } , w ) \in \mathbb { R } ^ { 3 }$ represents a vector on an ‘augmented’ space (i.e., the augmented space consists of the Rover position $( p _ { x } , p _ { y } )$ and the curve parameter w). We then define an ‘augmented path’ as,

$$
{ } ^ { a u g } \mathcal { P } : = \{ \xi = ( p _ { x } , p _ { y } , w ) \in \mathbb { R } ^ { 3 } : \phi _ { i } = 0 , i = 1 , 2 \} .\tag{6}
$$

Figure 2 shows an example for a path $\mathcal { P }$ defined using a Bézier curve. Notice that $a u g \mathcal { P }$ is the intersection of the surfaces $\phi _ { 1 } ( \xi )$ and $\phi _ { 2 } ( \xi )$ and $\mathcal { P }$ is just the projection of $a u g \mathcal { P }$ onto $( p _ { x } , p _ { y } )$ . The figure shows one of the main features of SF-GVF. The actual desired path $\mathcal { P }$ for the Rover (blue line) has a crossing point, and it is impossible to define a single vector for the Rover to follow to stay on the path at such a point. The augmented path <sup>aug</sup>P instead unfolds $\mathcal { P }$ using the parameter $w .$ Thus, there is a single 3D vector for every point of the 3D unfolded curve. The Rover can now be guided using its 2D projection onto the plane $p _ { x } , p _ { y } .$

We consider the function $e ( \xi ) = ( \phi _ { 1 } ( \xi ) , \phi _ { 2 } ( \xi ) ) ^ { T } : \mathbb { R } ^ { 3 } \to \mathbb { R } ^ { 2 }$ an error function, which gives a measurement of the splitting between a point $\xi$ and the path $\mathcal { P } , \| e ( \xi ) \| = 0 \Rightarrow \xi \in \mathcal { P }$ , (where || · || is the Euclidean norm). We can now obtain a guiding vector field on the ‘augmented’ space, departing from $\phi _ { 1 } ( \xi )$ and $\phi _ { 2 } ( \xi )$

$$
^ {a u g} \chi = \nabla \phi_ {1} \times \nabla \phi_ {2} - \sum_ {i = 1} ^ {2} k _ {i} \phi_ {i} \nabla \phi_ {i}.\tag{7}
$$

The first addend of equation (7) is perpendicular to $\nabla \phi _ { 1 }$ and $\nabla \phi _ { 2 } . ~ \mathrm { S o }$ , it is a vector tangential to the surfaces $\phi _ { 1 } ( \xi ) = 0$ and $\phi _ { 2 } ( \xi ) = 0$ , pointing along $a u g \mathcal { P }$ . It is called in (Yao et al., 2021) the propagation term. The sense of this propagation term can be changed just by swapping the gradients in the cross-product. The second addend points towards that surface $( { \mathrm { i . e . } }$ , it is the normal component of the vector field) and, therefore, towards <sup>aug</sup>P. This term is called the converging term, where $k _ { i } > 0$ are adjustable gains to fit the normal component of the field.

The gradients $\nabla \phi _ { 1 } = ( 1 , 0 , - f _ { 1 } ^ { \prime } ( w ) ) ^ { T }$ and $\nabla \phi _ { 2 } = ( 0 , 1 , - f _ { 2 } ^ { \prime } ( w ) ) ^ { T }$ can be straightforwardly obtained, where $f _ { i } ^ { \prime } ( w ) : = \frac { d f _ { i } ( w ) } { d w }$ . Besides,

$$
\nabla \phi_ {1} \times \nabla \phi_ {2} = (f _ {1} ^ {\prime} (w), f _ {2} ^ {\prime} (w), 1).\tag{8}
$$

Thus, our ‘augmented vector field’ is,

$$
{ } ^ { a u g } \chi ( \xi ) = \left( \begin{array} { c } f _ { 1 } ^ { \prime } ( w ) - k _ { 1 } \phi _ { 1 } \\ f _ { 2 } ^ { \prime } ( w ) - k _ { 2 } \phi _ { 2 } \\ 1 + k _ { 1 } \phi _ { 1 } f _ { 1 } ^ { \prime } ( w ) + k _ { 2 } \phi _ { 2 } f _ { 2 } ^ { \prime } ( w ) \end{array} \right) .\tag{9}
$$

Note that the third component of the vector in equation (8) is always constant and equal to 1, regardless of the path’s parametrization. Moreover, the terms $\nabla \phi _ { 1 } \times \nabla \phi _ { 2 }$ and $\begin{array} { r } { \sum _ { i = 1 } ^ { 2 } k _ { i } \phi _ { i } \nabla \phi _ { i } } \end{array}$ in equation (7) are orthogonal to each other and are linearly independent. As a result, the third component of $^ { a u g } \chi ( \xi )$ is always non-zero. Therefore, $^ { a u g } \chi ( \xi ) \neq 0$ for all $\xi \in \mathbb { R } ^ { 3 }$ . Thus, there are no singular points in the augmented field.

In summary, we have added a fictitious third coordinate to the dimensions of our problem, including the path parameter w as a new variable. This has several advantages (Yao et al., 2021). First, it constructs a guiding vector field that leads the vehicle towards the path. Besides, the augmented path is not self-intersecting, although the path could be, see figure 2, and the augmented GVF does not have singular points.

The vector field <sup>aug</sup>χ defined in equation (7) is an efective solution to Problem 1, i.e. $\dot { \xi } ( t ) = { } ^ { a u g } \chi$ approaches the augmented path <sup>aug</sup>P if $\xi ( 0 ) \not \in { } ^ { a u g } { \mathcal { P } }$ or remains in <sup>aug</sup>P if $\xi ( 0 ) \in { } ^ { \mathrm { a u g } } { \mathcal { P } }$ . Formal proofs can be found in (Yao et al., 2018, Theorem 3) and (Yao and Cao, 2020, Proposition 2, Theorem 2). Finally, in (Yao et al., 2021, Theorem 2) is proved that if P is parameterized as in equation (4), ϕ<sub>1</sub> and $\phi _ { 2 }$ are chosen like in (5) and there are no singular points in $\operatorname { a u g } _ { \chi } .$ the projected trajectory $\xi ^ { p } = ( p _ { x } , p _ { y } )$ globally converges to the path $\mathcal { P } _ { \cdot }$

We will ofer here a proof sketch of the exponential convergence of $^ { a u g } \chi ( \xi )$ to $a u g \mathcal { P }$ , according to the following proposition,

Proposition 1. Let $\xi ( t )$ be the solution to $\dot { \xi } ( t ) = { } ^ { a u g } \chi ( \xi ( t ) )$ with $^ { a u g } \chi ( \xi ( t ) )$ ) as defined in equation (9), then $\xi ( t )$ will converge to the augmented path $a u g \mathcal { P }$ , defined in equation $( \boldsymbol { \theta } )$ as $t \to \infty$

Proof. The distance from the solution to the path at any time is defined as,

$$
\operatorname{dist} (\xi (t), \mathcal {P}) = \inf \left\{\| \xi (t) - p \|: p \in {} ^ {\text { aug }} \mathcal {P} \right\}\tag{10}
$$

This distance can be approximated by $\| e ( \xi ( t ) ) \|$ because the norm of $e ( \xi ) = ( \phi _ { 1 } ( \xi ) , \phi _ { 2 } ( \xi ) ) ^ { T }$ is bounded and there are not singular points in $a u g \mathcal { P }$ . Taking the $e ( \xi )$ time derivative,

$$
\dot {e} (\xi (t)) = N ^ {T} (\xi (t)) \cdot \dot {\xi} (t) = N ^ {T} (\xi (t)) \cdot \chi (\xi (t)) = - N ^ {T} (\xi (t)) \cdot N (\xi (t)) \cdot K \cdot e (\xi (t)),\tag{11}
$$

where $K = \mathrm { d i a g } ( k _ { 1 } , k _ { 2 } ) , N = ( \nabla \phi _ { 1 } , \nabla \phi _ { 2 } )$ and $N ^ { T } \cdot ( \nabla \phi _ { 1 } \times \nabla \phi _ { 2 } ) = 0$

Now we define the following Lyapunov’s function candidate:

$$
V (\xi (t)) = \frac {1}{2} e ^ {T} (\xi (t)) \cdot K \cdot e (\xi (t)).\tag{12}
$$

One important property of $V ( \xi ( t ) )$ and the error vector norm $\| e ( \xi ( t ) ) \|$ is,

$$
2 \frac {V}{k _ {m}} \geq \| e \| ^ {2} \geq 2 \frac {V}{k _ {M}},\tag{13}
$$

where $k _ { m } = \operatorname* { m i n } \{ k _ { 1 } , k _ { 2 } \}$ and $k _ { M } = \operatorname* { m a x } \{ k _ { 1 } , k _ { 2 } \}$ . We will omit ξ(t) dependence for clarity. Taking the time derivative of the Lyapunov function,

$$
\dot {V} = \frac {1}{2} \left(\dot {e} ^ {T} K e + e K \dot {e}\right) = - \frac {1}{2} \left(e ^ {T} K N ^ {T} N K e + e ^ {T} K N ^ {T} N K e\right) = - e ^ {T} Q e = - \| N K e \| ^ {2}\tag{14}
$$

Notice that $Q = K N ^ { T } N K \succ 0$ , det $( Q ) = k _ { 1 } ^ { 2 } k _ { 2 } ^ { 2 } \lVert \nabla \phi _ { 1 } \times \nabla \phi _ { 2 } \rVert ^ { 2 } \ge 0$ . (Recall equation (9)). Thus $\dot { V } = 0 \Rightarrow$ $e ( \xi ) = 0$ . Let $\lambda _ { m i n } > 0$ be the minimum eigenvalue of $Q$ . Then,

$$
\dot {V} \leq - \lambda_ {m i n} \| e \| ^ {2} \leq - 2 \lambda_ {m i n} \frac {V}{k _ {M}}\tag{15}
$$

Thus,

$$
\frac {k _ {m}}{2} \| e \| ^ {2} \leq V \leq V (e _ {0}) \exp \left(- \frac {2 \lambda_ {\text { min }} t}{k _ {M}}\right) \leq \frac {k _ {M}}{2} \| e _ {0} \| ^ {2}\tag{16}
$$

With $e _ { 0 } = e ( \xi ( 0 )$ the initial error. Eventually,

$$
\| e \| \leq \sqrt {\frac {k _ {M}}{k _ {m}}} \| e _ {0} \| \exp \left(- \frac {\lambda_ {m i n} t}{k _ {M}}\right)\tag{17}
$$

![](GonzlezCalvin2024SingularityFree_figs/28dccf9a29b30cddb89fc612a0a0baa01b7a5f289e08a81a36a23e72aa2115b5.jpg)  
Figure 3: Illustration of the relationship between $^ { a u g } \chi$ and $\chi ^ { p } ,$ . The vector field $\chi ^ { p }$ (shown as black arrows) is the projection of $^ { a u g } \chi$ (shown as red arrows) onto the plane $( p _ { x } , p _ { y } )$ of constant w (shown as a black dot in the red plane). The solid orange line represents the augmented path, while the dashed blue line represents the augmented trajectory ξ.

## 3.2 Path following

Once a dynamic model for the Rover, a desired path, and its GVF associated have been defined, we need to find a control law that makes the Rover trajectory converge to the desired path. First, we extend the dynamic model described in section 2, equation (3), adding an equation for the new variable w:

$$
\dot {w} = v \frac {\chi_ {3}}{\sqrt {\chi_ {1} ^ {2} + \chi_ {2} ^ {2}}},\tag{18}
$$

where ${ } ^ { a u g } \chi = ( \chi _ { 1 } , \chi _ { 2 } , \chi _ { 3 } ) ^ { T }$ are the components of the ‘augmented’ guiding field. The path parameter must adapt accordingly to the Rover’s speed because the Rover will follow the guiding vector field evaluated at a specific w. As discussed in (Yao, 2021, page 194), the GVF path following process could also be considered as a special trajectory tracking algorithm (Siciliano et al., 2010, page 506), in which the tracking parameter is state-dependent, closing a control loop.

Therefore, the objective should be to align the Rover augmented velocity $\dot { \xi } = ( \dot { p } _ { x } , \dot { p } _ { y } , \dot { w } ) ^ { T }$ with the GVF, making it head in the direction of the field. Assuming the disturbances to the system can be neglected, we approximate the Rover velocity direction with its heading vector, $\hat { \dot { p } } \approx \hat { h } = ( \cos ( \theta ) , \sin ( \theta ) ) ^ { T }$ , where ˆ represents the normalization operator, and define $\chi ^ { p }$ as the projection of the guiding field $^ { a u g } \chi$ onto the plane $( p _ { x } , p _ { y } )$ ,

$$
\hat {\chi} ^ {p} := (\hat {\chi} _ {1}, \hat {\chi} _ {2}) ^ {T} = \frac {1}{\sqrt {\chi_ {1} ^ {2} + \chi_ {2} ^ {2}}} \binom{\chi_ {1}}{\chi_ {2}}.\tag{19}
$$

Figure 3 shows the concepts relating to the augmented and projected vector field and trajectories. It is interesting to notice how the projected vector field changes following the parameter w.

Hence, let us consider the following error function between the Rover’s orientation and ${ \hat { \chi } } ^ { p } ;$ :

$$
e _ {*} = \binom{\hat {h} - \hat {\chi} ^ {p}}{\dot {w} - v \frac {\chi_ {3}}{| | \chi^ {p} | |}} = \binom{\hat {h} - \hat {\chi} ^ {p}}{0},\tag{20}
$$

which is 0 if and only if $\hat { h } ^ { T } \hat { \chi } ^ { p } = 1 ;$ ; therefore, the orientation is aligned with the vector field. It is clear that thanks to the election made of w˙ we only have to find a control law that makes $\hat { h } - \hat { \chi } ^ { p }  0 , \mathrm { i . e . }$ ., a control law that asymptotically aligns the Rover with the projection of the augmented guiding field, $\chi ^ { p } ,$ . The variation of $\chi ^ { p }$ orientation as the Rover moves can be obtained as,

$$
\frac {d}{d t} \hat {\chi} ^ {p} = \frac {1}{\| \chi^ {P} \|} \left(I - \hat {\chi} ^ {p} \hat {\chi} ^ {p T}\right) \frac {d \chi^ {p}}{d t} = \frac {1}{\| \chi^ {P} \|} \left(I - \hat {\chi} ^ {p} \hat {\chi} ^ {p T}\right) J (\chi^ {p}) v
$$

Where $I \in \mathbb { R } ^ { 2 }$ is the identity matrix and $\boldsymbol { J } ( \boldsymbol { \chi } ^ { p } )$ is the Jacobian matrix of the field $\chi ^ { p } = ( \chi _ { 1 } , \chi _ { 2 } )$ with respect to $\boldsymbol { p } = \left( p _ { x } , p _ { y } \right)$ . Notice also that $\big ( I - \hat { \chi ^ { p } } \hat { \chi } ^ { p } T \big ) = E \hat { \chi } ^ { p } ( E \hat { \chi } ^ { p } ) ^ { T }$ is a projector in the direction orthogonal to $\hat { \chi ^ { p } }$ $\mathrm { S o }$

$$
\frac {d}{d t} \hat {\chi} ^ {p} = - \left(\frac {\hat {\chi} ^ {p T}}{| | \chi^ {p} | |} E J (\chi^ {p}) v\right) E \hat {\chi} ^ {p} = \dot {\theta} _ {d} E \hat {\chi} ^ {p}.
$$

Where E is the 90 degree counter-clock rotation matrix $\begin{array} { r } { E = \left( \begin{array} { l l } { 0 \ { - } 1 } \\ { 1 } & { 0 } \end{array} \right) } \end{array}$ and we define:

$$
\dot {\theta} _ {d} := - \left(\frac {\hat {\chi} ^ {p T}}{| | \chi^ {p} | |} E J (\chi^ {p}) v\right).\tag{21}
$$

Notice that $\dot { \theta } _ { d }$ is a scalar quantity, and it can be considered as the rotation rate of $\hat { \chi } ^ { p }$ , since $E \hat { \chi } ^ { p } \perp \hat { \chi } ^ { p }$ Then, if the angular velocity of the Rover $\dot { \theta }$ converges to $\dot { \theta } _ { d }$ while $\hat { h }  \chi ^ { p }$ , the Rover will follow the GVF and, eventually, will connect to the desired path. A suitable Lyapunov function can be found in (Yao et al., 2021) as $\begin{array} { r } { V = \frac { 1 } { 2 } | | e _ { * } | | ^ { 2 } } \end{array}$ , whose time derivative is:

$$
\begin{array}{r l} & {\dot {V} = \left(\dot {\hat {h}} - \dot {\hat {\chi}} ^ {p}\right) ^ {T} (h - \hat {\chi} ^ {p}),} \\ & {\dot {V} = \left(- \dot {\theta} \hat {h} ^ {T} E + \dot {\theta} _ {d} \chi^ {p T} E\right) (h - \hat {\chi} ^ {p}),} \\ & {\dot {V} = (\dot {\theta} - \dot {\theta} _ {d}) (\hat {h} ^ {T} E \hat {\chi} ^ {p}).} \end{array}
$$

Where $\dot { \hat { h } } = \dot { \theta } E \hat { h }$ . Therefore, by choosing the control function

$$
\dot {\theta} = u _ {\theta} = \dot {\theta} _ {d} - k _ {\theta} \hat {h} ^ {T} E \hat {\chi} ^ {p}: k _ {\theta} \in \mathbb {R} ^ {+},\tag{22}
$$

then $\dot { V } = - k _ { \theta } ( \hat { h } ^ { T } E \hat { \chi } ^ { p } ) ^ { 2 } \leq 0$ . This means that $\hat { h }  \hat { \chi } ^ { p }$ and $\dot { \theta }  \dot { \theta } _ { d }$ as desired. Notice that $k _ { \theta }$ is an adjustable gain to modulate the control action.

We use spline segments with $C ^ { 4 }$ continuity, while the endpoints connecting two curves have $C ^ { 2 }$ continuity. This guarantees convergence, justifying using at least fifth-order Bézier curves.

## 3.3 A note on field perturbation.

We now add a perturbation to the vector field,

$$
\dot {\xi} = \chi (\xi (t)) + d (t)\tag{23}
$$

Where $d : \mathbb { R } _ { \geq 0 } \to \mathbb { R } ^ { 2 }$ is a bounded function of time $t , \forall t \geq 0$ . Then, the dynamics of the path-following error, equation (11), changes,

$$
\dot {e} (t) = N ^ {T} (\xi (t)) \left(\chi (\xi (t) + d (t)) \right.\tag{24}
$$

Using again equation (12) as Lyapunov’s candidate function, its time derivative is,

$$
\dot {V} = \frac {1}{2} \left(\dot {e} ^ {T} K e + e K \dot {e}\right) = - \frac {1}{2} \left((\chi + d) ^ {T} N K e + e ^ {T} K N ^ {T} (\chi + d)\right) = - \| N K e \| ^ {2} + d ^ {T} N K e\tag{25}
$$

and using Young’s inequality, $d ^ { T } N k e \leq \| N K e \| ^ { 2 } / 2 + \| d \| ^ { 2 } / 2$

$$
\dot {V} \leq - \frac {1}{2} \| N K e \| ^ {2} + \frac {1}{2} \| d \| ^ {2}\tag{26}
$$

Following an identical reasoning as in proposition 1 proof, we arrive to,

$$
\dot {V} \leq - \frac {1}{2} \lambda_ {m i n} \| e \| ^ {2} + \frac {1}{2} \| d \| ^ {2}\tag{27}
$$

If d(t) is bounded, ∥e∥ will be bounded by $\begin{array} { r } { \operatorname* { s u p } _ { t \in [ 0 , \infty ) } \| d ( t ) \| / \sqrt { \lambda _ { m i n } } } \end{array}$ , while if $d ( t )$ vanishes as $t \to \infty$ , then $| | e ( t ) | |  0$ as $t \to \infty$

## 4 Bézier’s curves for path planning

Whatever mission a final user wants to assign to an AMR involves the explicit or implicit definition of trajectories the vehicle should cover to fulfil its objectives. Probably the broadest extended method is the generation of Dubins’ splines based on Dubins’ curves (Dubins, 1957; Lavalle, 2006, page 880). For constant speed and predefined waypoints, a Dubins’ spline is built by combining circle arcs and straight lines that minimize the time to cover the path. The method used a circle arc with the minimum radius allowed by the vehicle’s speed. Another common approach is the use of N-splines. These are defined as $3 ^ { \mathrm { r d } }$ degree polynomials, which interpolate two consecutive waypoints of the desired path. The polynomial coeficients become entirely determined by imposing continuity for the splines and their first derivatives on the common waypoints.

Even if SF-GVFs ensure a convergence to any $C ^ { 2 }$ continuous parametric curve, not all parametric curves are suitable for an AMR mission. While the previously mentioned curves are quite common in literature, they lack several desired properties that ease the path creation and/or that allow to fit the parametric curve to a real restricted area. That is, they usually lack: 1) an intuitive adjustment of the waypoints by the operator, 2) analytical knowledge of the area in which the curve is contained by a simple look at its waypoints, 3) ease of computation, and 4) ease of implementation in real hardware. The first property allows for fast path creation, while the second for an a-priori known area in which the curve will be contained. The last two properties are related to hardware implementations, allowing the use of embedded memory and computationally restricted systems. Bézier’s curves meet all this requirements, since 1) they are straightforward to adjust, 2) once we know the waypoints of the Bézier curve, it is contained within its convex hull, so by joining the points of the Bézier curve with straight lines, we have the area in which the Bézier curve is contained; 3) they are easy to compute since they are well-known and defined polynomials called Bernstein polynomials, and 4) for its implementation only its waypoints are needed, and no previous computations must be carried since its waypoints completely determine Bézier curves, as they are the coeficients of the polynomials. Thus, they are very suitable for AMR path following, as they can be easily defined and fit in tight areas, and are computationally friendly for embedded systems.

Bézier curves have occasionally been used in robotics (Han et al., 2010; Hilario et al., 2011; Jolly et al., 2009; Kawabata et al., 2015), but no examples of their use have been found in the literature for the design of safe trajectories in uncrewed vehicles except for berthing (Yuan et al., 2023). Bézier curves allow the creation of a trajectory simply and intuitively (Simba et al., 2016; Hwang et al., 2003). In addition, they are quite suitable for working in combination with GVFs, as we will see later on. A brief description of them is given to expose their main characteristics.

We focus on two-dimensional Bézier curves, $f ( w ) \in \mathbb { R } ^ { 2 }$ , of degree n. They are polynomials defined by a set of points, whose basis are the Bernstein polynomials $\begin{array} { r } { b _ { k , n } ( w ) = \binom { n } { k } w ^ { k } ( 1 - w ) ^ { n - k } : w \in [ 0 , 1 ] } \end{array}$ where $\binom { n } { k }$ is the binomial coeficient. A degree n Bézier curve is defined as:

$$
f (w) = \left(f _ {1} (w), f _ {2} (w)\right) = \sum_ {k = 0} ^ {n} \beta_ {k} b _ {k, n} (w),\tag{28}
$$

where $\beta _ { k } \in \mathbb { R } ^ { 2 } : k \in [ 0 , n ]$ are the $n + 1$ points that define the Bézier curve. Thus, as shown in equation (28), there is no need to compute polynomial coeficients from the control points as, for instance, in standard basis cubic polynomials. This allows for less computations in the AMR vehicle, liberating resources for other tasks. Moreover, the points completely determine the shape of the curve, making it easier to adjust it manually, as in (Han et al., 2010).

The curve begins at point $\beta _ { 0 }$ and ends at point $\beta _ { n }$ , called end points, while $\beta _ { k } : 1 \le k \le n - 1$ , called control points, are used to define the shape of the trajectory. For instance, two control points can shape the trajectory if a degree $n = 3$ Bézier curve is used. It’s important to note that the Bézier curve is contained within the convex hull created by its points. This is useful when restricting the curve to a specific area. Hence, Bézier curves allow for an easy and intuitive way to fit the curve into a desired or particular shape or area by a) fixing the starting and end points and b) moving the control points to create a safe trajectory, knowing that it will be contained in its convex hull. Finally, since Bézier curves are polynomials, an n degree curve implies $C ^ { n - 1 }$ continuity, meaning that when $n \geq 3 .$ the acceleration, velocity and position are continuous. This property is necessary if curvature continuity is desired since it depends on the first and second derivatives of the parametric curve. Bézier curves have many other properties that make them useful for various applications; for a complete description, we refer to (Hansford, 2002).

Nevertheless, when generating paths, a single Bézier curve with many control points may be cumbersome for creating a desired shaped trajectory. Thus, a Bézier spline is designed for that purpose. When connecting two Bézier curves, the minimum requirement is to have $C ^ { 0 }$ continuity in the ending point $\beta _ { n } ^ { i }$ of the curve i and the starting point $\beta _ { 0 } ^ { i + 1 }$ of the curve $i + 1$ (except for the ending point of the last curve), that is, $\beta _ { n } ^ { i } = \beta _ { 0 } ^ { i + 1 }$ for every $i \in \{ 0 , \overset { \cdot } { 1 } , \dots , N - 2 \}$ , where N is the number of Bézier curves that compose the spline Moreover, if $C ^ { 1 }$ and $C ^ { 2 }$ continuity are desired, the following relationship between control points must hold

$$
\left\{ \begin{array}{l} f ^ {i ^ {\prime}} (1) = f ^ {i + 1 ^ {\prime}} (0) \Rightarrow \beta_ {n} ^ {i} - \beta_ {n - 1} ^ {i} = \beta_ {1} ^ {i + 1} - \beta_ {0} ^ {i + 1} \Rightarrow \\ \beta_ {1} ^ {i + 1} \underset {C ^ {1} \text {cont.}} {=} 2 \beta_ {n} ^ {i} - \beta_ {n - 1} ^ {i} \\ f ^ {i ^ {\prime \prime}} (1) = f ^ {i + 1 ^ {\prime \prime}} (0) \Rightarrow \beta_ {n} ^ {i} - 2 \beta_ {n - 1} ^ {i} + \beta_ {n - 2} ^ {i} = \beta_ {2} ^ {i + 1} - 2 \beta_ {1} ^ {i + 1} + \beta_ {0} ^ {i + 1} \Rightarrow \\ \beta_ {2} ^ {i + 1} \underset {C ^ {1}, C ^ {2} \text {cont.}} {=} 4 \beta_ {n} ^ {i} - 4 \beta_ {n - 1} ^ {i} + \beta_ {n - 2} ^ {i} \end{array} \right.
$$

where $\begin{array} { r } { { f ^ { i } } ^ { \prime } = \frac { d f ^ { i } } { d w } , f ^ { i } ( \cdot ) = ( f _ { 1 } ^ { i } ( \cdot ) , f _ { 2 } ^ { i } ( \cdot ) ) = \sum _ { k = 0 } ^ { n } \beta _ { k } ^ { i } b _ { k , n } ( \cdot ) } \end{array}$ is the ith segment of the spline. This means that the first and second control points of the $i + 1$ curve $( \beta _ { 1 } ^ { i + 1 } , \beta _ { 2 } ^ { i + 1 } )$ are also fixed and cannot be used to shape the trajectory. It can be shown that if $C ^ { p }$ continuity is desired for a Bézier spline of degree $n > p$ , it implies that p control points will be fixed, and only $n - 1 - p$ control points can be used to shape each segment of the spline. In our application, $C ^ { 2 }$ is necessary, and two control points would be enough. Therefore, $n = 5$ degree Bézier curves are selected.

A spline with N segments and $C ^ { 2 }$ continuity can be expressed as

$$
f _ {s} (w) = \left\{ \begin{array}{l l} f ^ {0} (w), & 0 \leq w \leq 1 \\ f ^ {1} (w - 1), & 1 \leq w \leq 2 \\ \vdots & \vdots \\ f ^ {N - 1} (w - (N - 1)), & N - 1 \leq w \leq N \end{array} \right..
$$

where the continuity relations above hold for each Bézier curve. Note that $( w - i ) \in [ 0 , 1 ]$ , as required in the definition of Bézier curves.

Thus, since we will work with N Bézier curves of degree $n = 5 ,$ each curve $( { \mathrm { i . e . } }$ , each segment of the spline) has $C ^ { 4 }$ continuity and, at the points in which two curves connect there is $C ^ { 2 }$ continuity. The following reasons justify the usage of this type of spline. First, the guidance algorithm requires that the complete trajectory is a path with at least $C ^ { 2 }$ continuity. Second, if lower degree curves were used $( \mathrm { i . e . , } n = 3 , n = 4 )$ and $C ^ { 2 }$ continuity is required, this would imply that less than two control points could be used to shape each segment of the spline, losing the ease of creating Bézier curves. Finally, only one segment and a higher degree Bézier curve could be used for the complete trajectory. However, in contrast to fixing ending points and only changing the i and i + 1 segment when moving a control point, creating a single polynomial leads not only to a complex adjustment of the curve to the desired area but to a higher-order polynomial computation, which could lead to lack of numerical stability (Faraway et al., 2007).

## 5 Speed Control Problem

Several works can be found in the literature on adapting guidance controllers to the curvature, like in (Leng and Minor, 2017), for guidance algorithms to achieve better convergence. A speed controller for an AMR vehicle is helpful when following curvature-changing paths. This allows us to reach a constant speed setpoint and adapt the speed to path characteristics. The non-varying setpoint provides for constant speed pathfollowing while changing the setpoint depending on some information about the desired path (e.g., curvature) should speed up the convergence of the guidance controller. This approach is simple because only the desired reference speed changes; thus, whatever speed controller can be used, for example, in (Cao et al., 2019), a finite time double sliding surface guidance algorithm is used for Subway’s speed curve tracking.

In recent years, there has been increased attention towards determining trajectory-dependent speed profiles for guidance due to the rise of autonomous road vehicles (Gámez Serna and Ruichek, 2017). Most works use a-priori information about the desired trajectory to compute the path curvature and use this information to adapt vehicle speed, preventing slipping and rollover. Trajectory information can be extracted from maps, like (Villagra et al., 2012) that used a closed-form speed profiler combined with the path planner, providing a continuous velocity reference. Or (Li et al., 2012) that obtains the curvature using the Geographic Information Systems (GIS) roadmaps. In other cases, certain assumptions are made about the curvature of roads to adapt the vehicle’s speed, as in (Park et al., 2015).

## 5.1 Speed controller

To control the Rover speed, we use as a control signal $u _ { v } \ \mathrm { ( i . e . }$ , the throttle) the output of a feedforward + PID controller:

$$
u _ {v} = k _ {f} v _ {r e f} + k _ {p} e _ {v} (t) + k _ {d} \dot {e} _ {v} (t) + k _ {i} \int_ {0} ^ {t} e _ {v} (\tau) d \tau ,\tag{29}
$$

where $v _ { r e f } \in \mathbb { R } _ { \geq 0 }$ is the desired speed, $e _ { v } ( t ) = v _ { r e f } - v ( t )$ is the error between this one and the actual speed of the Rover, and $k _ { f } , k _ { p } , k _ { d } , k _ { i } \in \mathbb { R } _ { \geq 0 }$ are, respectively, the feedforward, proportional, derivative and integral control constants. The feedforward controller allows reaching a constant speed depending on $v _ { r e f }$ , while the PID controller acts in the presence of error, allowing the desired speed to be reached without steady-state error.

Recall that, as was pointed out in section 2, we have ignored the dynamic of the Rover. Thus $v \sim \propto u _ { v }$ and we can consider,

$$
v = k _ {f} v _ {r e f} + k _ {p} (v _ {r e f} - v) + k _ {d} (\dot {v} _ {r e f} - \dot {v}) + k _ {i} \int_ {0} ^ {t} (v _ {r e f} - v) d t\tag{30}
$$

Taking time derivatives, considering a constant $v _ { r e f }$ and regrouping terms, we get a linear system,

$$
\binom{\ddot {v}}{\dot {v}} = \left( \begin{array}{c c} - \frac {1 + k _ {p}}{k _ {d}} & - \frac {k _ {i}}{k _ {d}} \\ 1 & 0 \end{array} \right) \binom{\dot {v}}{v} + \binom{1}{0} \frac {k _ {i}}{k _ {d}} v _ {r e f}.\tag{31}
$$

It is immediate to see that the system matrix always has negative spectral abscissa, i.e. the system is stable and $v \to v _ { r e f } ~ \mathrm { a s } ~ t \to \infty$ , due to the control integral term.

Note that if the setpoint change is slower than the controller’s time constant, then the vehicle will follow the desired time-changing speed setpoint. This plays a crucial role in the next section since we will use a smooth (i.e., diferentiable) and variable setpoint that depends on curvature.

In our case, the Rover measures its position directly from the GPS, discarding data from inertial sensors. Our Rovers are small outdoor vehicles subject to bumpy and stony terrain and several other factors. This bounciness afects the accelerometers of the IMU, adding a significant amount of noise, almost equal to or larger than the actual acceleration of the Rover due to displacement. Besides, the Rover’s acceleration transient time is faster than the noise perturbations (due to its relatively small mass). Therefore, the acceleration due to an actual increase or decrease in speed could not be diferentiated from the noise signal. In addition, a proper measure of the noise process variance is complex since it depends on the terrain.

Thus, the GPS speed is critical, but this signal is also noisy. Filtering is needed to allow for the operation of a speed controller (especially the derivative controller). For this purpose, we use a simple moving average filter. Therefore, our Rovers measure the speed using only the GPS signal filtered with a moving average filter, and they use this filtered speed measurement v as an input to the speed controller in equation (29).

## 5.2 Changing speed setpoint

Typically, path-following algorithms consider a constant speed when following a specific curve. This speed is chosen so that the vehicle can follow the trajectory with suficiently small (guidance) control inputs. Moreover, their heading cannot change instantly when dealing with non-holonomic vehicles like the model in equation (1). This means that the radius of curvature that it can trace increases (respectively decreases) as speed increases (decreases). Therefore, if the speed is held constant, it must be restricted to the maximum value that ensures the Rover can follow the trajectory. That is, the speed of the Rover must allow its guidance controller to converge to the trajectory, regardless of high curvature segments. That is because guidance control signals (i.e., inputs to the steering angle) at relatively high speeds can cause a rollover. Moreover, the saturation of the steering angle creates the same problems explained above.

Besides, there are applications in which a constant speed is not desirable or interesting. For example, if the trajectory must be completed below a certain time stamp, an interesting approach is that the vehicle accelerates where the curvature is low or zero (i.e., straight lines) and reduces its speed when curvature increases. For this purpose, we propose that the speed setpoint can be changed according to the path’s curvature, following the next equation,

$$
v _ {r e f} (\kappa) = (v _ {m a x} - v _ {m i n}) \exp (- c _ {\kappa} \kappa^ {2}) + v _ {m i n},\tag{32}
$$

where $v _ { m a x }$ and $v _ { m i n } \in \mathbb { R } _ { \geq 0 }$ are the maximal and minimal Rover speed $( v _ { m a x } \geq v _ { m i n } ) , \kappa \in \mathbb { R }$ is the curvature and $c _ { \kappa } \in \mathbb { R } _ { \geq 0 }$ is a constant used to penalize the speed as curvature increases. Since we are dealing with parametric curves, the curvature formula is well known (Dubrovin et al., 1984) and is defined as

$$
\kappa (w) = \frac {f _ {1} ^ {\prime} (w) f _ {2} ^ {\prime \prime} (w) - f _ {1} ^ {\prime \prime} (w) f _ {2} ^ {\prime} (w)}{(f _ {1} ^ {\prime} (w) ^ {2} + f _ {2} ^ {\prime} (w) ^ {2}) ^ {3 / 2}}.\tag{33}
$$

Thus, the curvature is computed using the parameter of the path w, that is, equation (33) calculates the curvature of the point at which the vector field is pointing to (see figure 7).

Assuming that $c _ { \kappa }$ is greater than zero in equation (32), we can observe that the speed setpoint, which will be utilized in the controller (29), is limited by $v _ { r e f } \in [ v _ { m i n } , v _ { m a x } ]$ . The maximum value of the setpoint is achieved when $\kappa  0$ , while the minimum value is obtained when $\kappa  \infty$ . By adjusting $c _ { \kappa }$ appropriately, the speed of the Rover can be slowed down when it approaches areas with relatively high curvature. It’s interesting to note that the exponential argument is quadratic. This solves two problems: 1) κ can take negative values depending on the sign of the curvature, and 2) taking $\kappa ^ { 2 }$ instead of $| \kappa |$ makes the setpoint diferentiable, providing the curve has at least $C ^ { 3 }$ continuity to have a diferentiable curvature, which is a fine property if, for example, a derivative or nonlinear controller is desired.

![](GonzlezCalvin2024SingularityFree_figs/2db1d393dc547ed25df394eae3b4c92a4d946582954ca1313507338f31d1892d.jpg)  
(a) View of the team of Rovers.

![](GonzlezCalvin2024SingularityFree_figs/e6d967d0d718d0da0ef7e3d30b117ad24dd8d390de6b9f948764c1344f15295d.jpg)  
(b) Overview of the mechanical system of the Rovers.  
Figure 4: Rovers

In summary, the Rover will reach its maximum speed whenever it is following a straight path, $\kappa = 0 ;$ it will get a stable speed $v _ { m a x } > v \ge v _ { m i n }$ if it is following a curve of constant κ, i.e. a circle or circle section and it will accelerate o decelerate if κ is decreasing or increasing. Parameters in equation 32 allow us to tune the WMR behaviour to the path and terrain features.

## 6 Results

## 6.1 Experimental Platform

We use the same software for simulations and experiments. In this way, the algorithms implemented for the simulation can also be used in the experiments without any further change. This section briefly describes the hardware and software platforms used for simulations and experiments.

## 6.1.1 Rover’s Hardware

Figure 4 shows several of our Rovers. These Rovers are commercial RC electric cars modified to provide a robust mechanical structure for their use as a testing platform, not only for algorithms designed for these vehicles but also for more complex systems, such as Unmanned Surface Vehicles (e.g., a boat whose direction is controlled by a rudder or a diferential drive vessel) or fixed wing planes. The dimensions of the Rover are collected in table 1. We have removed the commercial radio receiver from the Rovers and mounted on top of it a PVC foam board and a potting box as shown in figure 5. These Rovers have a front-wheel Ackerman-type steering, which mechanically coordinates the angle of the two front wheels mounted on a standard axle for steering. Moreover, they are all-wheel drive and equipped with diferential gears in both axes, reducing the skidding when turning since it allows each wheel (in each axis) to rotate at a diferent speed. The Rovers’ movement is controlled by two motors: (1) an HPI Racing Saturn brushed DC motor that provides thrust to all wheels and (2) a servo motor that drives the steering. The onboard autopilot is a Matek f765-Wing flight controller whose Microcontroller Unit (MCU) is the STM32F765VIT6 from ST Microelectronics. Althoug it has been designed to control fixed-wing drones, the autopilot suits our purposes well, supplying a common platform for diferent types of autonomous vehicles. In addition to a built-in Inertial Measurement Unit (IMU) in the flight controller, the Rovers have several devices connected to it: 1) an ublox GPS (SAM-M8Q) receiver with a built-in compass, 2) a Digi Xbee S2C RF transceiver that allows both monitoring the Rovers parameters and sending control signals to them from a ground station (see below) and 3) a Futaba RC receiver with SBus protocol, that allows the Rovers to be remotely controlled using a RC Futaba radio and transfer the control to and from the autopilot. These devices also grant access to the necessary states: the position $( p _ { x } , p _ { y } )$ and attitude θ, relative to the inertial frame $W ( p )$ , needed for the guidance controller shown in equation (22), as well as access to the speed v, used (after filtering) by the speed controller in equation (29). A 7.4 V Li-Po Battery powers the complete system with a capacity of 3000 mAh.

![](GonzlezCalvin2024SingularityFree_figs/ed904a3a236d32d7233d9a55b63e80ff6f4afee977dc251e9a0b9986bae53992.jpg)

Figure 5: Rover’s electronics hardware setup in an outdoors experiment.

<table><tr><td>Wheelbase</td><td>Axle Track</td><td>Length</td><td>Width</td><td>Height</td><td>M.S.A outer wheel</td><td>M.S.A inner wheel</td></tr><tr><td>25 cm</td><td>23 cm</td><td>40 cm</td><td>30 cm</td><td>29 cm</td><td>15 degrees</td><td>10 degrees</td></tr></table>

Table 1: Rover’s physical measurements. MSA stands for Maximal Steering Angle.

## 6.1.2 Paparazzi UAV environment

As noted in section 1, we use Paparazzi as a development environment to program autonomous vehicles. Paparazzi is a free and open-source hardware and software project intended to create a flexible autopilot system. Although it was initially designed to deal with unmanned aerial vehicles (UAVs), researchers from diferent universities have extended its applications to other autonomous vehicles. Moreover, Paparazzi supports multiple hardware designs. To do so, it includes 1) a cross compiler, allowing the user to compile code for any supported flight controller board, 2) an uploader tool to upload the implemented code to the flight controller, and 3) support for several sensors and devices. The reader interested may address to

<table><tr><td>Brushed DC motor</td><td>HPI Racing Saturn</td><td>Provides thrust to all wheels</td></tr><tr><td>Servo motor</td><td></td><td>Drives the steering</td></tr><tr><td>Microcontroller unit</td><td>STM32F765VIT6 (ST Microcontrollers)</td><td>Onboard Matek f765-Wing autopilot</td></tr><tr><td>Inertial Measurement Unit</td><td>MPU-6000 and ICM20602 (InvenSense)</td><td>Onboard Matek f765-Wing autopilot</td></tr><tr><td>GPS</td><td>ublox GPS (SAM-M8Q)</td><td>Provides speed and positioning</td></tr><tr><td>RF transceiver</td><td>Digi Xbee S2C RF</td><td>Provides communication to ground station</td></tr><tr><td>Radio receiver controller</td><td>RC Futaba with Sbus protocol</td><td>Allows to remote control the rover</td></tr><tr><td>Battery</td><td>7.4 V Li-Po 3000 mAh</td><td>Rover power</td></tr></table>

Table 2: Rover’s hardware components

![](GonzlezCalvin2024SingularityFree_figs/0eead4360662a488c42f35ba6db7d5cc7263f21e1d6d1001b7a7a7f67ad39eff.jpg)

![](GonzlezCalvin2024SingularityFree_figs/10c37ee0338cf6fbba68ad0410eae57ccad59951ff9307c2d32d368d533f9a9b.jpg)  
Figure 6: Screenshot from the Paparazzi’s GCS in simulation. Bézier points are represented as blue diamonds, while the desired trajectory is represented as a green line. The actual trajectory traced by the Rover is shown in blue.  
Figure 7: Screenshot from the same simulation as figure 6 but forwarded in time and showing the vector field $\hat { \chi } ^ { p }$ as red arrows.

## Paparazzi wiki pages: https://wiki.paparazziuav.org/wiki/Main\_Page.

Paparazzi also provides a simulator with diferent simulation vehicle models (e.g., the Rover’s model, fixedwing aircraft models and rotorcraft models) as well as sensor models. Besides, it is possible to modify the models or add new ones to fit the model to a specific AMR. The simulator is intended to test the performance of new algorithms before implementing them in the actual vehicles, saving time and resources.

The third and last component of Paparazzi is a Ground Control Station (GCS), shown in figures 6 and 7, where agents’ positions are visualised, and diferent sensor and internal variables can be monitored. The Paparazzi GCS is coded in C++ and can be customised to include new properties. For instance, we have added the code to define, show, and modify the Bézier curves used for path planning on the fly. To ofer maximum flexibility and openness, the Paparazzi ecosystem was designed from the start as a modular one (Gati and Balazs, 2013). The user can specify the type of vehicle and sensors used, the flight plan, and the desired telemetry data using Extensible Markup Language (XML) files. This allows the user to choose between several XML modules without developing any C-Code. Therefore, thanks to the modular software architecture, generating the basic navigation code for the Rovers has been accelerated by using the diferent modules available in the paparazzi framework, such as GPS, radio control, wireless communication and others.

Figure 8 shows a block diagram with the system’s main features. Using the Paparazzi GCS, the user can give real-time commands as inputs to the Rover’s autopilot. Examples of inputs include path following commands of a desired curve –waypoints, speed setpoints, and guidance and speed controller constants. The rest of the system runs in the Rover’s flight controller, allowing for a fully autonomous mode. Concerning the autonomous mode, states $( p _ { x } , p _ { y } )$ and speed v are obtained from GPS data and sent to the SF-GVF module. This module computes the desired trajectory f(w), the vector field $\hat { \chi } ^ { p }$ and the term $\dot { \theta } _ { d }$ needed for $u _ { \theta } .$ , as well as w and $\kappa ( w )$ required in the speed controller. The heading and speed controllers generate the control signals $u _ { \theta } \to \phi$ and $u _ { v }$ by using the states, guidance information from the SF-GVF, and controller constants given by the user via Paparazzi GCS. Moreover, the states are fed to the Navigation Plan block to show these variables in real-time in paparazzi GCS. Finally, the control signals are sent to the lowest level of the Paparazzi UAV (not shown in the figure; it maps the values of $\phi$ and $u _ { v }$ to PWM signals) to turn the Rover’s steering servo and spin the DC motor.

The heading and speed controllers have been implemented in Paparazzi (C-code), allowing us to use them in simulation and in the experimental platform. First, the algorithm in section 3 has been modified to be used with Rover vehicles since it was already implemented in Paparazzi for fixed-wing aircraft. Moreover, the capability of following Bézier curves has been added. Thus, the user can not only create a desired Bézier curve in the Paparazzi GCS but modify it when desired $( \mathrm { e . g . }$ , during an experiment) since it is the flight controller in the Rover that automatically computes the Bézier curve control points for continuity conditions.

![](GonzlezCalvin2024SingularityFree_figs/00ef9892246a51fb5a413a5aec70ec1fb156da081a44308d6a59995a5391f00a.jpg)  
Figure 8: Schematic representation of the system. Once the code has been uploaded to the AMR from Paparazzi, GCS commands can be given to the Rover via telemetry. Then, the Rover follows the trajectory and speed setpoint according to the modules shown in the figure.

Second, the speed controller of equation (29) has been implemented using the modules Paparazzi provides. Third, the changing speed setpoint of section 5 and a moving average filter for the measured speed have been implemented.

Finally, to see in real-time the desired parametric curve $f ( w )$ , the authors have implemented the code to show the trajectory and also the varying vector field $\hat { \chi } ^ { p }$ , as shown in figures 6 and 7 (where a fifth order Bézier curve with $C ^ { 2 }$ continuity is shown). This allows us to adjust the guidance constants $( \mathrm { i . e . , } k _ { 1 } , k _ { 2 }$ and $k _ { \theta } )$ by visualising the deviations from the desired trajectory and the point the vector field is pointing to.

It is important to note that waypoints can be adjusted to fit the trajectory into the desired area. By simply moving the desired control or endpoints, the user can shape the path as they wish. Onboard software recalculates the trajectory whenever a point has changed. This allows for considerable flexibility in experimental environments where uncertainties in position may arise.

The main code for following third-order Bézier curves is under the central paparazzi repository: https: //github.com/paparazzi/paparazzi, for following both third-order and fifth-order Bézier curves is under the repository https://github.com/alfredoFBW/paparazzi\_alfredoFBW, while the code to visualise both Bézier curves and the vector field in paparazzi GCS is under https://github.com/alfredoFBW/PprzGCS.

## 6.2 Simulation results

A trajectory is created to test the SF-GVF and heading controller in simulation using $N = 3$ fifth order $( n = 5 )$ Bézier curves. As explained in section 4, a degree fifth Bézier curve is defined by $n + 1 = 6$ points: the starting and end points and four control points, which can be used to shape the curve. Since the spline has $C ^ { 2 }$ continuity, the endpoint of the segment i is the starting point of segment $i + 1 , i \in [ 0 , N - 2 ]$ and the two control points $\beta _ { 1 } ^ { i } , \beta _ { 2 } ^ { i }$ of segment i came defined by the values of the second and third to last points of the previous segment $\beta _ { 4 } ^ { \bar { i } - 1 } , \beta _ { 3 } ^ { i - 1 }$ , giving us two control points to shape each spline segment. Thus, we have $3 ( N + 1 ) = 1 2$ configurable points for the complete spline, which we define as $\beta _ { k } ^ { s }$ . In particular, $\beta _ { k } ^ { s } : k \in \{ 0 , 5 , 8 , 1 1 \}$ define each segment’s starting and end points, while the rest are used as control points to modify each segment’s shape independently. Therefore, the curve starts at $\beta _ { 0 } ^ { s }$ and ends at $\beta _ { 3 N - 2 } ^ { s } = \beta _ { 1 1 }$ An example of a curve is created and shown in figure 9, where the trajectory intersects with itself and has a changing curvature, necessary conditions to test our controllers. After launching the simulation using the model from equation (3), it can be seen how the path traced by the Rover converges to the desired parametric curve and errors ϕ , ϕ are in the order of centimetres. Moreover, it can be seen how the speed setpoint (speedsp) and Rover’s speed (speed measured) change according to the path’s curvature. Note that the algorithm is restarted when reaching the ending point $\beta _ { 1 1 }$ by resetting the path parameter w to the initial value $w = 0$

![](GonzlezCalvin2024SingularityFree_figs/dcf57b1d53f1580741ae9779ef13b2e7f8accf95f770a27c478c1e2c62d7ca9f.jpg)  
Figure 9: Screenshot from the Paparazzi’s GCS in simulation. Upper right graphic shows the distance errors in meters $( \phi _ { 1 } , \phi _ { 2 } )$ to the desired path P (as phi[0] and phi[1]) respectively) versus time. The bottom right graphic shows the time evolution of $v _ { r e f }$ and v as red and blue lines in $\mathrm { m } / \mathrm { s }$ . Constants $k _ { 1 } = k _ { 2 } = 0 . 5 ~ \mathrm { m } , k _ { \theta } = 3$ for the guidance controller and $v _ { m i n } = 1 . 7 ~ \mathrm { m / s } , v _ { m a x } = 2 . 7 ~ \mathrm { m / s } , c _ { \kappa } = 1 0 ~ \mathrm { m ^ { 2 } }$ for the speed controller were used.

## 6.3 Real Rover Results

This subsection is divided into two parts. The first deals with the actual experiments on the guidance algorithm, while the second deals with the speed control problem. It is also important to note that the following experiments can be reproduced by compiling and downloading the code to the vehicle (provided they have the same or compatible hardware) using the repositories presented above.

Two self-intersecting curves are chosen for the SF-GVF and heading controller experimental tests. The first one is an experimental setup with fair environmental conditions, i.e., a clear sky for the GPS receiver and an obstacle-free football field. The second one represents a worse-case scenario, where the area in which the Rover can move is tighter, and the GPS is not providing the best possible resolution. Now, the speed setpoint is the same for both experiments and is implemented as in equation (32) using: $v _ { m i n } = 1 . 4 ~ \mathrm { m / s } , v _ { m a x } = 2 . 4 ~ \mathrm { m / s } , c _ { \kappa } = 1 5 \mathrm { m ^ { 2 } }$ . Using the Paparazzi replay utility, real data results from both experiments are reproduced in figure 10 for the first case and figure 11 for the second one.

Paparazzi replay utility tool allows us to select time intervals of interest to extract data for their analysis. Besides, Paparazzi logs the vehicle’s status with the Zigbee telemetry radio. Hence, data from the experiments can be extracted for its posterior analysis. Thus, data from the logs were extracted for both curves to determine the magnitude of the errors. This data are displayed for a complete set of trajectories traced by the Rover for the first experiment curve in figure 12, and for the second one in figures 13 and 14.

Figure 13 shows a particular trajectory of the second experiment, while figure 14 shows a set of trajectories made during the same experiment.

For the first experiment, in figure 12, the left graphic represents the actual trajectory as a blue line and the desired trajectory as a black line where the origin of coordinates is centred on the HOME point shown in figure 10. Thus, the Rover position $( p _ { x } , p _ { y } )$ is measured relative to the HOME origin attached to the earth and fixed throughout the whole experiment. Home location is determined by the first geographical position

![](GonzlezCalvin2024SingularityFree_figs/601dfa89af872829480e6dc22ec92c45484927e8c2d0c2ef3c9b14bcadeb70fd.jpg)  
Figure 10: Screenshot from the Paparazzi’s GCS in the first real experiment. The representations and meanings are the same as in the simulation. The same constants were used as in the simulation.

![](GonzlezCalvin2024SingularityFree_figs/60a780a65e6bbe6e41d98bbd3fe2cfcd8358e96c80f889663638c215a90d691b.jpg)  
Figure 11: Screenshot from the Paparazzi’s GCS in the second real experiment. The same constants were used as in the simulation.

## the GPS measures.

The Rover begins 25 meters away from the intended path (as shown on the left side graphic of figure 12). The algorithm then guides the Rover towards the path until it reaches it. Once the final segment of the path is reached, the trajectory begins again, the algorithm restarts and w is reset to 0. This is indicated by the Rover converging back to the starting point of the path. The upper right graphic shows the evolution of the errors $\phi _ { 1 }$ and $\phi _ { 2 }$ (on the left y-axis) and the parameter w (on the right y-axis) over time. The bottom left graphic displays the error to the path, $e _ { \mathcal { P } } = \operatorname* { i n f } \{ | | p - p _ { d } | | \mid p _ { d } \in \mathcal { P } \}$ , as well as the GPS position accuracy.

Once the Rover has converged to the trajectory, the distance to the path $e _ { \mathcal { P } }$ is close to zero and well below the GPS position accuracy throughout the experiment. Note, however, that the errors $\phi _ { 1 } , \phi _ { 2 }$ , and thus the previously mentioned error ||e(ξ)|| with $e ( \xi ) = ( \phi _ { 1 } ( \xi ) , \phi _ { 2 } ( \xi ) )$ , are bigger, and in certain time instants they can reach errors of 10 meters. This behaviour is due to oscillations in the parameter w, whose dynamics were specified in equation (18).

As can be seen in the upper right graphic, the time instants in which w oscillates match those times when the errors $\phi _ { 1 } , \phi _ { 2 }$ oscillate and separate from zero. Recall that $\phi _ { 1 } = p _ { x } - f _ { 1 } ( w )$ and $\phi _ { 1 } = p _ { y } - f _ { 2 } ( w )$ and, for a three segment Bézier spline, $w \in [ 0 , 3 ]$ . Thus, even if the Rover has converged to the trajectory, a fast oscillation of w creates fast oscillations of $f _ { 1 } ( w )$ and $f _ { 2 } ( w )$ , which in turn creates fast oscillations of $\phi _ { 1 }$ and $\phi _ { 2 }$ . Moreover, since $w \in [ 0 , 3 ]$ and the dimensions of the Bézier spline are in the order of tens of meters, a fast and small variation of w can create a big variation in $f ( w )$ and a big and fast transient in $\phi _ { 1 }$ and $\phi _ { 2 } .$ Nevertheless, the distance to the path, $e _ { \mathcal { P } }$ , is not directly afected by $w ,$ and from the left graphic and the bottom right graphic, it can be seen that it converges towards zero and remains below the GPS accuracy.

For the second experiment, figure 14 represents the same information as figure 13 but for a set of trajectories. Note that, compared to figure 12, the area in which the Rover must remain is tighter, as can be seen from the dimensions of the trajectory. Moreover, the mean GPS accuracy is close to the one in figure 12, allowing for a similar error if the GPS accuracy is considered as the bound of the d term of equation (24). As explained above, the algorithm restarts when reaching the end point of the spline, which means that the trajectories shown in figure 14 are done sequentially, that is, in the same experiment and one after another.

In this more extensive set of experiments, similar to the previous one, the error is bounded from above throughout the entire experiment by the GPS position accuracy; as it is reflected in the comparison between the desired and actual trajectory. Moreover, at the starting points, it can be seen that a transient loop occurs. This is due to the asymptotic stability of the closed loop system; when the curve is restarted, it shall converge to the trajectory again. Moreover, comparing with figure 12, this experiment did not show any fast

![](GonzlezCalvin2024SingularityFree_figs/4e9f973c53f7e5bcc01c9718449f37a50f2f0cde6ea3282860e10004adf18782.jpg)

![](GonzlezCalvin2024SingularityFree_figs/cefb3b57bd568c11a31feaabb9a278b42a0adafefde0c067650e1438d758f209.jpg)

![](GonzlezCalvin2024SingularityFree_figs/220c72c4b38701cddf1fd98639f01c2bbd351b9d70a482777a47a9dfb2a42e45.jpg)  
Figure 12: Experimental data obtained from the logs for a complete set of trajectories traced by the Rover. The left subfigure shows the actual traced trajectory in blue, the desired one in black, the initial point in red, and the curve points $\beta _ { 0 } , \beta _ { 5 } , \beta _ { 8 } , \beta _ { 1 1 }$ in magenta. The upper right subfigure shows the errors $\phi _ { 1 } , \phi _ { 2 }$ in the left y-axis and the parameter w in the right y-axis. The bottom right subfigure shows the distance to the path $e _ { \mathcal { P } } = \operatorname* { i n f } \{ | | p - p _ { d } | | \mid p _ { d } \in \mathcal { P } \}$ and the accuracy of the GPS position.

![](GonzlezCalvin2024SingularityFree_figs/62058a72e2617aba5aa5acb1ed2a3653ea73bd9db4fd81e737555c31fb14fa92.jpg)

![](GonzlezCalvin2024SingularityFree_figs/618504985ef5ab0cf903c5ca230de0cea3d5865801f5778782bf6546629ccb5b.jpg)  
Figure 13: Experimental data obtained from the logs. The left subfigure shows a set of actual trajectories and the desired one, the initial point in red, and the curve points $\beta _ { 0 } , \beta _ { 5 } , \beta _ { 8 } , \beta _ { 1 1 }$ in magenta, the upper right subfigure shows in the left y-axis the errors $\phi _ { 1 } , \phi _ { 2 }$ , and in the right y-axis the parameter $w .$ The bottom right subfigure shows the distance to the path $e _ { \mathcal { P } } = \operatorname* { i n f } \{ | p - p _ { d } | \ |$ $p _ { d } \in \mathcal { P } \}$

, and the GPS position accuracy.

![](GonzlezCalvin2024SingularityFree_figs/ce0efc6111fc56814de5a04129fdf39bcd24cc3e2d540b4fa0074407944cbff9.jpg)

![](GonzlezCalvin2024SingularityFree_figs/6b924e6b9e9a0c382e3fedc01ca040de331459fd637b894024d40bbb2f5413f3.jpg)  
Figure 14: Experimental data obtained from the logs of the same experiment, but or a complete set of trajectories. The left subfigure shows a set of actual trajectories and the desired one, the initial point in red, and the curve points $\beta _ { 0 } , \beta _ { 5 } , \beta _ { 8 } , \beta _ { 1 1 }$ in magenta, the upper right sub figure shows in the left y-axis the errors $\phi _ { 1 } , \phi _ { 2 }$ 2 and in the right y-axis the parameter w. The bottom right subfigure shows the distance to the path $e _ { \mathcal { P } } = \operatorname* { i n f } \{ | p - p _ { d } | | p _ { d } \in \mathcal { P } \}$ , and the GPS position accuracy.

oscillations of the parameter w, and in turn no fast oscillations of the errors $\phi _ { 1 }$ and $\phi _ { 2 }$ .

For completeness, let us use the results of equation 27, where we arrived at the result that $| | e ( \xi ) | | \leq$ $\begin{array} { r } { \operatorname* { s u p } _ { t \in [ 0 , \infty ) } \frac { | | d ( t ) | | } { \sqrt { \lambda _ { m i n } } } } \end{array}$ . The $Q$ matrix can be expressed as

$$
Q = \left[ \begin{array}{c c} q _ {1 1} & q _ {1 2} \\ q _ {1 2} & q _ {2 2} \end{array} \right] = \left[ \begin{array}{c c} (f _ {1} ^ {\prime} (w) ^ {2} + 1) k _ {1} ^ {2} & f _ {1} ^ {\prime} (w) f _ {2} ^ {\prime} (w) k _ {1} k _ {2} \\ f _ {1} ^ {\prime} (w) f _ {2} ^ {\prime} (w) k _ {1} k _ {2} & (f _ {2} ^ {\prime} (w) ^ {2} + 1) k _ {2} ^ {2} \end{array} \right] \succ 0.
$$

The eigenvalues can be computed to obtain $\begin{array} { r } { \lambda = \frac { q _ { 1 1 } + q _ { 2 2 } \pm \sqrt { ( q _ { 1 1 } + q _ { 2 2 } ) ^ { 2 } - 4 ( q _ { 1 1 } q _ { 2 2 } - q _ { 1 2 } ^ { 2 } ) } } { \Omega } } \end{array}$ . Moreover, note that in both experiments, we have used the same values of $k _ { 1 }$ and $k _ { 2 } , { \mathrm { i . e . , } } ^ { z } k _ { 1 } = k _ { 2 } = 0 . 5 .$ , so plugin in this condition on the eigenvalues and the values of the $Q$ matrix, we arrive at

$$
\lambda = \frac {k _ {1} ^ {2} (f _ {1} ^ {\prime} (w) ^ {2} + f _ {2} ^ {\prime} (w) ^ {2} + 2) \pm \sqrt {k _ {1} ^ {4} (f _ {1} ^ {\prime} (w) ^ {2} + f _ {2} ^ {\prime} (w) ^ {2}) ^ {2}}}{2} = \frac {k _ {1} ^ {2} (f _ {1} ^ {\prime} (w) ^ {2} + f _ {2} ^ {\prime} (w) ^ {2} + 2) \pm k _ {1} ^ {2} (f _ {1} ^ {\prime} (w) ^ {2} + f _ {2} ^ {\prime} (w) ^ {2})}{2}.
$$

Thus, it can be easily seen that $\lambda _ { m i n } = k _ { 1 } ^ { 2 } , \lambda _ { m a x } = k _ { 1 } ^ { 2 } ( | | f ^ { \prime } ( w ) | | ^ { 2 } + 1 )$ . So the error can now be bounded, $\begin{array} { r } { | | e ( \xi ) | | \leq \operatorname* { s u p } _ { t \in [ 0 , \infty ) } \frac { | | d ( t ) | | } { \sqrt { \lambda _ { m i n } } } = \operatorname* { s u p } _ { t \in [ 0 , \infty ) } \frac { | | d ( t ) | | } { \sqrt { k _ { 1 } ^ { 2 } } } , \mathrm { ~ s o ~ } | | e ( \xi ) | | \leq 2 \operatorname* { s u p } _ { t \in [ 0 , \infty ) } | | d ( t ) | | } \end{array}$ . For the first experiment sup $| | d ( t ) | | = 7 . 6 $ while for the second sup $| | d ( t ) | | = 5 . 3$ , so for the first experiment $| | e ( \xi ) | | \le 1 5 . 2 \mathrm { m } .$ while for the second $| | e ( \xi ) | | \le 1 0 . 6 \mathrm { ~ m ~ }$ This holds true in both experiments when computing $| | e ( \xi ) | | =$ $\sqrt { \phi _ { 1 } ( \xi ) ^ { 2 } + \phi _ { 2 } ( \xi ) ^ { 2 } }$ , which connect theoretical and experimental results. Note that in the first experiment, the supremum of the disturbance is larger (i.e., there are instants in which the GPS uncertainty is larger), while the average GPS position error is lower than in the second experiment, as can be seen by comparing figure 12 with figures 13 or 14.

Before commenting on the results of the speed controller, it is worth noting that in the Paparazzi platform, the throttle control actions $u _ { v }$ are bounded by $u _ { v } \in [ - 9 6 0 0 , 9 6 0 0 ]$ , and those values are converted to PWM signals as explained above.

Speed controller data from the second set of experiments is shown in figure 15. The top left graphic shows the speed setpoint $v _ { r e f }$ and the GPS speed v filtered with a moving average filter (a low pass filter) of $M = 2 0 0$ samples. Vertical black dotted lines represent the timestamps in which the Rover passes through the corresponding Bézier points $\beta _ { i } ^ { s }$ . The top right graphic depicts the curvature of the Bézier spline. As it can be seen from both top graphics, the speed setpoint $v _ { r e f }$ changes accordingly to the computed curvature $\kappa ,$ reducing the setpoint when $\kappa ^ { 2 }$ increases and vice versa. The bottom left graphic shows the speed control signal $u _ { v }$ and its PID components, and the bottom right graphic represents the speed accuracy given by the GPS.

The time delay that can be seen in the top left graphic, where the actual speed v is behind the setpoint, is due to the speed controller settling time and the filter’s efect. However, the delay in some way is not an undesired property. At any given time t, the vector field points towards a point of the Bézier curve ahead of the Rover, as shown in figures 10 and 11. The speed setpoint changes based on the curvature of the function $f ( w )$ ; however, assuming the Rover has already reached the trajectory at time t, it will be at a point $f ( w - w ^ { * } )$ where $w - w ^ { \ast } < w$ . This indicates that the Rover will reach the point $f ( w )$ , for which the setpoint was originally calculated after some delay. Thus, the trade-of between noise and time delay can be adjusted with the speed controller constants and the number of samples M. In particular, the constants we used are shown in table 4. Finally, for completeness, tables 3 and 4 show the Bézier points and constant values used in the first and second set of experiments, respectively. Note that except for the first segment (segment i = 0), the points $\beta _ { 1 } ^ { i } , \beta _ { 2 } ^ { i }$ for $i \in \{ 1 , 2 \}$ are computed using the $C ^ { 2 }$ continuity conditions shown in section 4. Thus, the user only needs to specify the points in figure 10.

![](GonzlezCalvin2024SingularityFree_figs/4f167b3d7585f13907e417ea362695e49f2c68222ed5e1d8a4a71530b34b94fc.jpg)

Figure 15: Rover’s speed data obtained from the same experiment as in figure 13. The top left graphic shows the desired speed setpoint as a blue line, the Rover’s measured speed as a red line and as vertical black dotted lines the timestamps in which the Rover passes through the corresponding Bézier points $\beta _ { i } ^ { s }$ The top right graphic represents the curvature as a function of time κ(w(t)). The bottom left graphic represents the proportional, integral and derivative control actions and the total speed control action $u _ { v } .$ The bottom right graphic represents the speed accuracy given by the GPS. Constant used for this experiment: v<sub>min</sub> = 1.4 m/s, v<sub>max</sub> = 2.4 m/s, c<sub>κ</sub> = 15m<sup>2</sup>, k<sub>f</sub> = 1000, k<sub>p</sub> = 3000, k<sub>i</sub> = 300 and $k _ { d } = 2 0 0 0$

<table><tr><td colspan="4">Bézier points used for the first experiment</td><td colspan="2">Controller constants</td></tr><tr><td>Bézier points (w.r.t HOME)</td><td>Segment 0 (m)</td><td>Segment 1 (m)</td><td>Segment 2 (m)</td><td>Constant used</td><td>Values</td></tr><tr><td> $\beta_0^i$ </td><td>(-11.62, 36.58)</td><td>(59.53, 49.69)</td><td>(30.12, 40.59)</td><td> $k_1, k_2$ </td><td>0.5</td></tr><tr><td> $\beta_1^i$ </td><td>(14.93, 64.67)</td><td>(40.45, 65.78)</td><td>(20.78, 31.71)</td><td> $k_\theta$ </td><td>1</td></tr><tr><td> $\beta_2^i$ </td><td>(16.02, -8.84)</td><td>(-16.64, 65.54)</td><td>(10.78, 4.84)</td><td> $k_f$ </td><td>1000</td></tr><tr><td> $\beta_3^i$ </td><td>(59.72, 1.15)</td><td>(47.74, 40.36)</td><td>(20.00, 26.13)</td><td> $(k_p, k_i, k_d)$ </td><td>(3000, 300, 2000)</td></tr><tr><td> $\beta_4^i$ </td><td>(78.63, 33.59)</td><td>(39.26, 49.47)</td><td>(0.07, 14.38)</td><td> $c_\kappa$ </td><td>15</td></tr><tr><td> $\beta_5^i$ </td><td>(59.54, 49.69)</td><td>(30.02, 40.59)</td><td>(-11.63, 34.13)</td><td>M</td><td>200</td></tr></table>

Table 3: Bézier control points measured from HOME position and constants used for the first experiment.

<table><tr><td colspan="4">Bézier points used for the second experiment</td><td colspan="2">Controller constants</td></tr><tr><td>Bézier points (w.r.t HOME)</td><td>Segment 0 (m)</td><td>Segment 1 (m)</td><td>Segment 2 (m)</td><td>Constant used</td><td>Values</td></tr><tr><td> $\beta_{0}^{i}$ </td><td>(-6.61, -28.20)</td><td>(-5.08, -2.34)</td><td>(-11.95, -12.10)</td><td> $k_{1}, k_{2}$ </td><td>0.5</td></tr><tr><td> $\beta_{1}^{i}$ </td><td>(-6.85, -20.01)</td><td>(-7.20, 0.55)</td><td>(-8.89, -16.75)</td><td> $k_{\theta}$ </td><td>1</td></tr><tr><td> $\beta_{2}^{i}$ </td><td>(-6.86, -17.00)</td><td>(-12.26, -1.49)</td><td>(-2.00, -19.81)</td><td> $k_{f}$ </td><td>1000</td></tr><tr><td> $\beta_{3}^{i}$ </td><td>(-3.80, -10.11)</td><td>(-14.25, -1.25)</td><td>(-6.86, -22.65)</td><td> $(k_{p}, k_{i}, k_{d})$ </td><td>(3000, 300, 2000)</td></tr><tr><td> $\beta_{4}^{i}$ </td><td>(-2.97, -5.25)</td><td>(-15.01, -7.46)</td><td>(-5.51, -23.45)</td><td> $c_{\kappa}$ </td><td>15</td></tr><tr><td> $\beta_{5}^{i}$ </td><td>(-5.08, -2.34)</td><td>(-11.95, -12.10)</td><td>(-4.73, -27.78)</td><td>M</td><td>200</td></tr></table>

Table 4: Bézier control points measured from HOME position and constants used for the second experiment.

## 7 Conclusions

In this paper, a guidance system based on GVFs is designed for path-following in AMR vehicles, and a curvature-dependent speed controller is used for faster convergence of the guidance algorithm. The definition of the desired path as parametric curves allows for a straightforward computation of the curve’s curvature for the speed setpoint. In addition to presenting theoretical work involving these two controllers, simulations of the complete system are made using the Paparazzi UAV platform. Finally, we introduce our AMR platform, for which exhaustive experiments are made to show the approach’s efectiveness. The main contributions of this work are:

• Generate a waypoint trajectory using Bézier curves, allowing the human user to easily set the waypoints and control points on the map and change them on the fly if necessary. Bézier curves allow smooth trajectories to be generated within the defined bounding box, formally called a convex hull.

• Once the trajectory is established, GVF is employed to define a vector field that allows us to know, at any point in space, the desired velocity direction of the rover that will allow it to converge to the target path. The vector field can be applied to derive a control law for the convergence property. GVF algorithms show exemplary performance. To the authors’ knowledge, no results of this Singularity Free GVF (SF-GVF) applied to the Rover path-following problem exist.

• Using SF-GVF and the Rover kinematic model, a controller is derived using a Lyapunov function, assuring stability.

• Path following is improved by speed control based on path curvature.

• Results of the guidance and speed controllers are presented in simulation and with a real Rover in a natural environment. For this purpose, the Paparazzi environment is used (Gati and Balazs, 2013).

The ease and adaptability of Bézier polynomials make them very attractive to extend their use to other autonomous vehicles. For instance, we are currently testing the same approach to control Autonomous Surface Vehicles for water quality monitoring in inland reservoirs. imulation results are presented in (González-Calvin et al., 2023), using a planner and a guidance and control algorithm to traverse the planned trajectory. The results presented in this paper: generation of trajectories from measurement points using Bezier curves, tracking of these trajectories using SF-GVF and velocity control based on the curvature of the path are being tested on a USV with measurement probes for the detection of cyanobacterial blooms. The results are promising and will be the object of future publications.

Besides, we are also interested in extending our algorithm for obstacle avoidance, using data from proximity sensors to modify the shape of the Beziérs curves on the fly. So, the vehicle will replan its path, maintaining the prescribed waypoints wherever possible.

## Acknowledgments

This work is partially supported by IA-GES-BLOOM-CM (Y2020/TCS-6420) of the Synergic Projects program of the Autonomous Community of Madrid and INSERTION (PID2021-27648OB-C33) of the Knowledge Generation program of the Ministry of Science and Innovation.

## References

Bechar, A. and Vigneault, C. (2016). Agricultural robots for field operations: Concepts and components. Biosystems Engineering, 149:94–111.

Bechar, A. and Vigneault, C. (2017). Agricultural robots for field operations. part 2: Operations and systems. Biosystems engineering, 153:110–128.

Cao, Y., Wang, Z.-C., Liu, F., Li, P., and Xie, G. (2019). Bio-inspired speed curve optimization and sliding mode tracking control for subway trains. IEEE Transactions on Vehicular Technology, 68(7):6331–6342.

De Marina, H. G., Sun, Z., Bronz, M., and Hattenberger, G. (2017). Circular formation control of fixedwing uavs with constant speeds. In 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 5298–5303. IEEE.

Dubins, L. E. (1957). On curves of minimal length with a constraint on average curvature, and with prescribed initial and terminal positions and tangents. American Journal of Mathematics, 79(3):497–516.

Dubrovin, B. A., Fomenko, A. T., and Novikov, S. P. (1984). Modern Geometry - Methods and Applications, volume Part I. The Geometry of Surfaces, Transformation Groups, and Fields of Graduate Texts in Mathematics (GTM, volume 93). Springer.

Faraway, J. J., Reed, M. P., and Wang, J. (2007). Modelling Three-Dimensional Trajectories by Using Bézier Curves with Application to Hand Motion. Journal of the Royal Statistical Society Series C: Applied Statistics, 56(5):571–585.

Gámez Serna, C. and Ruichek, Y. (2017). Dynamic speed adaptation for path tracking based on curvature information and speed limits. Sensors, 17(6):1383.

Gati and Balazs (2013). Open source autopilot for academic research-the paparazzi system. In 2013 American Control Conference, pages 1478–1481. IEEE.

González-Calvin, A., García-Perez, L., Risco-Martín, J. L., and Besada-Portas, E. (2023). Simulation, optimization and control of trajectories of asvs performing hacbs monitoring missions in lentic waters. In 2023 Winter Simulation Conference (WSC), pages 910–921.

Gu, N., Wang, D., Peng, Z., Wang, J., and Han, Q.-L. (2022). Advances in line-of-sight guidance for path following of autonomous marine vehicles: An overview. IEEE Transactions on Systems, Man, and Cybernetics: Systems, 53(1):12–28.

Han, L., Yashiro, H., Nejad, H. T. N., Do, Q. H., and Mita, S. (2010). Bezier curve based path planning for autonomous vehicle in urban environment. In 2010 IEEE intelligent vehicles symposium, pages 1036–1042. IEEE.

Hansford, D. (2002). Chapter 4 - bézier techniques. In Farin, G., Hoschek, J., and Kim, M.-S., editors, Handbook of Computer Aided Geometric Design, pages 75–109. North-Holland, Amsterdam.

Hilario, L., Montés, N., Mora, M. C., and Falcó, A. (2011). Real-time bézier trajectory deformation for potential fields planning methods. In 2011 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 1567–1572. IEEE.

Hitz, G., Galceran, E., Garneau, M.-È., Pomerleau, F., and Siegwart, R. (2017). Adaptive continuous-space informative path planning for online environmental monitoring. Journal of Field Robotics, 34(8):1427– 1449.

Hwang, J.-H., Arkin, R. C., and Kwon, D.-S. (2003). Mobile robots at your fingertip: Bezier curve on-line trajectory generation for supervisory control. In Proceedings 2003 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2003)(Cat. No. 03CH37453), volume 2, pages 1444–1449. IEEE.

Jolly, K., Kumar, R. S., and Vijayakumar, R. (2009). A bezier curve based path planning in a multiagent robot soccer system without violating the acceleration limits. Robotics and Autonomous Systems, 57(1):23–33.

Kapitanyuk, Y. A., de Marina, H. G., Proskurnikov, A. V., and Cao, M. (2017). Guiding vector field algorithm for a moving path following problem\*\*the work was supported in part by the european research council (erc-stg-307207), the netherlands organization for scientific research (nwo-vidi-14134) and rfbr, grants 17-08-01728, 17-08-00715 and 17-08-01266. IFAC-PapersOnLine, 50(1):6983–6988. 20th IFAC World Congress.

Kawabata, K., Ma, L., Xue, J., Zhu, C., and Zheng, N. (2015). A path generation for automated vehicle based on bezier curve and via-points. Robotics and Autonomous Systems, 74:243–252.

Lavalle, S. M. (2006). Planning Algorithms. Cambridge University Press.

Leng, Z. and Minor, M. A. (2017). Curvature-based ground vehicle control of trailer path following considering sideslip and limited steering actuation. IEEE Transactions on Intelligent Transportation Systems, 18(2):332–348.

Li, Z., Chitturi, M. V., Bill, A. R., and Noyce, D. A. (2012). Automated identification and extraction of horizontal curve information from geographic information system roadway maps. Transportation Research Record, 2291:80 – 92.

Mathew, N., Smith, S. L., and Waslander, S. L. (2015). Planning paths for package delivery in heterogeneous multirobot teams. IEEE Transactions on Automation Science and Engineering, 12(4):1298–1308.

Nourizadeh, P., Stevens McFadden, F. J., and Browne, W. N. (2023). In situ slip estimation for mobile robots in outdoor environments. Journal of Field Robotics, 40(3):467–482.

Park, M., Lee, S., and Han, W. (2015). Development of steering control system for autonomous vehicle using geometry-based path tracking algorithm. Etri Journal, 37(3):617–625.

Rubio, F., Valero, F., and Llopis-Albert, C. (2019). A review of mobile robots: Concepts, methods, theoretical framework, and applications. International Journal of Advanced Robotic Systems, 16(2):1729881419839596.

Safwat, E., Zhang, W., Wu, M., Lyu, Y., and Jia, Q. (2018). Robust path following controller for unmanned aerial vehicle based on carrot chasing guidance law using dynamic inversion. In 2018 18th International Conference on Control, Automation and Systems (ICCAS), pages 1444–1450. IEEE.

Samuel, M., Hussein, M., and Mohamad, M. B. (2016). A review of some pure-pursuit based path tracking techniques for control of autonomous vehicle. International Journal of Computer Applications, 135(1):35–38.

Siciliano, B. and Khatib, O. (2008). Springer Handbook of Robotics. Springer Handbook of Robotics. Springer Berlin Heidelberg.

Siciliano, B., Sciavicco, L., Villani, L., and Oriolo, G. (2010). Robotics: Modelling, Planning and Control. Springer Publishing Company, Incorporated.

Siegwart, R., Nourbakhsh, I. R., and Scaramuzza, D. (2011). Introduction to Autonomous Mobile Robots. The MIT Press, 2nd edition.

Simba, K. R., Uchiyama, N., and Sano, S. (2016). Real-time smooth trajectory generation for nonholonomic mobile robots using bézier curves. Robotics and Computer-Integrated Manufacturing, 41:31–42.

Sujit, P. B., Saripalli, S., and Sousa, J. B. (2014). Unmanned aerial vehicle path following: A survey and analysis of algorithms for fixed-wing unmanned aerial vehicless. IEEE Control Systems, 34:42–59.

Thakur, D., Likhachev, M., Keller, J., Kumar, V., Dobrokhodov, V., Jones, K., Wurz, J., and Kaminer, I. (2013). Planning for opportunistic surveillance with multiple robots. In 2013 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 5750–5757.

Villagra, J., Milanés, V., Pérez, J., and Godoy, J. (2012). Smooth path and speed planning for an automated public transport vehicle. Robotics and Autonomous Systems, 60(2):252–265.

Yao, W. (2021). Guiding Vector Fields for Robot Motion Control. PhD thesis, University of Groningen.

Yao, W. and Cao, M. (2020). Path following control in 3d using a vector field. Automatica, 117:108957.

Yao, W., de Marina, H. G., Lin, B., and Cao, M. (2021). Singularity-free guiding vector field for robot navigation. IEEE Transactions on Robotics, 37(4):1206–1221.

Yao, W., Kapitanyuk, Y. A., and Cao, M. (2018). Robotic path following in 3d using a guiding vector field. In 2018 IEEE Conference on Decision and Control (CDC), pages 4475–4480.

Yuan, S., Liu, Z., Sun, Y., Wang, Z., and Zheng, L. (2023). An event-triggered trajectory planning and tracking scheme for automatic berthing of unmanned surface vessel. Ocean Engineering, 273:113964.