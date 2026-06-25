---
citation_key: Wang2020Searchbased
arxiv_id: 2011.00806
arxiv_url: "https://arxiv.org/abs/2011.00806"
title: "Search-based Kinodynamic Motion Planning for Omnidirectional Quadruped Robots"
authors_short: "Pei Wang et al."
year: 2020
direction_tag: C_elastic_band
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:48:01Z
origin: ai+web
reviewed: false
---

# Search-based Kinodynamic Motion Planning for Omnidirectional Quadruped Robots

Pei Wang, Xiaoyu Zhou, Qingteng Zhao, Jun Wu, Qiuguo Zhu<sup>1</sup>

Abstract—Autonomous navigation has played an increasingly significant role in quadruped robot system. However, most existing works on quadruped robots navigation using traditional search-based or sample-based methods do not consider the kinodynamic characteristics of quadruped robots, generating kinodynamically infeasible parts, that are difficult to track. In this paper, we introduce a complete navigation system considering the omnidirectional abilities of quadruped robots. First, we use kinodynamic path finding method to obtain smooth, dynamically feasible, time-optimal initial paths and add collision cost as a soft constraint to ensure safety. Then the trajectory is refined by the timed elastic band (TEB) method based on the omnidirectional model of quadruped robots. The superior performance of our work is demonstrated through simulating and real-world experiments on our quadruped robot Jueying Mini.

## I. INTRODUCTION

Legged robots have better mobility and versatility than wheeled or tracked vehicles in complex environments such as rough terrains, [1], [2], [3]. Thus, some research groups make use of the strong omnidirectional and flexible locomotive capabilities of legged robots to realize autonomous navigation. However, this is still a challenging task because of difficulties in modeling and motion planning.

Current approaches to motion planning and navigation on legged robots often focus on foothold planning [4], [5], [6], and torso-based planning [7], [8], [9], [10]. Foothold planning considers the selection of foot-placements according to dynamics model of legged robot, while torso-based planning avoids complex dynamic modeling of legged robot with a virtual body model, which separates planning and control problems, and works well with fast gait-based locomotion.

Recent work has shown the advantage of torso-based planning on real robots. In [4], quadruped StarlETH uses the RRT\* algorithm to find a global path and considered the whole robot footprint, instead of the foothold. And the method carries out footprint planning many times, which is time consuming. Big Dog uses a variation of the $\mathbf { A } ^ { * }$ algorithm for the whole body path planning and a spline algorithm for path smoothing [5]. ANYmal features the $\mathbf { A } ^ { * }$ algorithm for pose graph planning and the RRT\* algorithm for traversability planning [6]. The quadruped robot in [7] uses the Dijkstra algorithm for global planning and the equivalent virtual body model for obstacle avoidance. The torso-based planning methods mentioned above use position-only methods to plan rough global paths which are not precise or energy efficient enough, also uneasily tracked. In order to solve these problems, kinodynamic path finding method [11], [12] can be applied on quadruped robots for energy efficient, easily tracked and kinodynamic feasible prior trajectories while maintaining self-stabilization property of gait-based locomotion. In [13], a data driven approach is used to learn the kinodynamic model of the quadruped robot, and then apply it on path finding for energy efficient navigation. The method is verified in the 2d flat ground simulation only, but not in real world. Similar to [13], we use kinodynamic path finding instead of position-only methods, but we use ‘two-stage’ planning, the front-end and the back-end, to simplify the complex modeling problems. And we incorporate footprint planning into global planning with the use of costmap by soft constraints to avoid multiple planning. Finally, we test our method in the simulation as well as the quadruped robot platform Jueying Mini, with consideration of its omnidirectional motion ability. The main contribution of this paper can be concluded as

1) A kinodynamic path finding method is used in the front-end, instead of geometric graph searching, for energy efficient, collision-free, kinodynamic feasible, and time-optimal trajectories. These trajectories are easily tracked and can reduce the burden of back-end for trajectory optimization. Hard and soft constraints with costmap are introduced to ensure safe front-end searching.

2) We use the timed elastic band (TEB) method under omnidirectional locomotion model in the back-end for further trajectory optimization and add constraints according to actual physical parameters and different locomotive abilities (in the forward-backward and lateral directions of our quadruped robot).

The rest part of this paper is organized in the following way. Section II describes the navigation system’s structure and formulates the navigation problem. Section III introduces the Kinodynamic $\mathbf { A } ^ { * }$ algorithm and describes hard and soft constraints applied to the motion uncertainty optimization problem. In Section IV, we combine TEB and omnidirectional methods for quadruped robots to refine the front-end path planning. Section V describes the experiments that we used to verify the robot’s performance and presents results. In Section VI, we summarize our work.

## II. PROBLEM FORMULATION

## A. System Overview

The planning system framework is shown in Fig. 1. The framework has three important components: Costmap, Global planner, and Local planner. Costmap takes the sensor input of the real environment and inflates costs on a 2D occupancy grid map. Global planner generates an initial trajectory, containing kinodynamic information, from the current position to goal position. Local planner obtains the robot’s real-time location from the state estimator, provides a controller that connects path to robot, generates a trajectory using TEB, and sends motion commands to robot control system.

![](Wang2020Searchbased_figs/8c0f30c04d6e77071990a00ce191de8844ca2f8ae3331c870e7c34eb060a6d35.jpg)  
Figure 1. The structure of navigation system

## B. Problem Formulation and Assumptions

Jueying Mini [14] is a quadruped robot that has the ability to move in a wide variety of complex environments. The control system guarantees the stability, and provides omnidirectional mobility to the robot. Since motion planning is in two dimensional regions, and roll and pitch can be ignored while their values remain small, only forward-backward, lateral, and yaw motions are considered in our framework. This allows translation and rotation to be defined independently of one other and simplifies the planning problem.

## III. KINODYNAMIC A\* PATH FINDING METHOD

## A. Motion Primitives Generation

Based on the assumption in Section II.B, each axis component of trajectory can be described independently. For saving computing resources to support online planning, we only focus on the $[ x , y ]$ in the front end. Let $\boldsymbol { x } \left( t \right) \in \boldsymbol { \chi } \subset \mathsf { R } ^ { 4 }$ be a system state, consisting of position $p \big ( t \big )$ and its derivatives. Thus,

$$
\begin{array}{c} x (t) := \left[ \begin{array}{l l} p ^ {\mathrm{T}} (t) & \dot {p} ^ {\mathrm{T}} (t) \end{array} \right] ^ {\mathrm{T}} \\ p (t) := \left[ \begin{array}{l l} p _ {x} (t) & p _ {y} (t) \end{array} \right] ^ {\mathrm{T}}, p _ {d} (t) = \sum_ {k = 0} ^ {K} a _ {k} \frac {t ^ {k}}{k !}, d \in \{x, y \} \end{array} \tag {1}
$$

where $a _ { k }$ represents polynomial coefficients. The velocity is denoted by $\nu \big ( t \big ) : = \dot { p } \big ( t \big )$ , and also acceleration is denoted by $a \mathopen { } \mathclose \bgroup \left( t \aftergroup \egroup \right) : = \ddot { p } \mathopen { } \mathclose \bgroup \left( t \aftergroup \egroup \right) \qquad ,$ and the control input $u \left( t \right) = a \left( t \right) \in U : = \left[ - u _ { m a x } , u _ { m a x } \right] ^ { 2 } \subset \mathsf { R } ^ { 2 }$ . The state space model can be described as

$$
\dot {x} = A x + B u,
$$

$$
A = \left[ \begin{array}{c c} 0 & I _ {2} \\ 0 & 0 \end{array} \right], B = \left[ \begin{array}{c} 0 \\ I _ {2} \end{array} \right]\tag{2}
$$

The solution for the equation is expressed as

$$
x (t) = e ^ {A t} x (0) + \int_ {0} ^ {t} e ^ {A (t - \tau)} B u (\tau) d \tau\tag{3}
$$

To generate trajectories that consider more than the shortest geometric distance considered by the traditional $\mathbf { A } ^ { * }$ algorithm, i.e., that are also smooth, collision-free, dynamically feasible, and optimal (in time and control), the qualities of the trajectory can be expressed as

$$
J (\phi) = \int_ {0} ^ {T} u ^ {2} (t) d t = \int_ {0} ^ {T} a ^ {2} (t) d t\tag{4}
$$

where $\phi$ denotes the trajectory. By taking time into consideration, the cost function is refined to

$$
J (T) = J (\phi) + \rho T = \int_ {0} ^ {T} u ^ {2} (t) d t + \rho T\tag{5}
$$

where $\rho$ is the parameter which determines the relative importance of the duration versus its smoothness.

The problem defined by (5) is a linear quadratic minimum-time problem [15]. To convert the optimization problem into a graph searching problem [12], we used lattice discretization $U _ { \scriptscriptstyle M } : = \left\{ u _ { \scriptscriptstyle 1 } , u _ { \scriptscriptstyle 2 } , . . . , u _ { \scriptscriptstyle M } \right\}$ , and each control input $u _ { { \scriptscriptstyle m } } \in \mathsf { R } ^ { 2 }$ is a vector in the x-y plane, which is applied for a short duration  . A discretization step $d _ { \mu }$ was introduced to get $\mu = u _ { m a x } / d _ { \mu }$ samples along each axis $\left[ 0 , { u _ { m a x } } \right]$ . Then, the discretized set of $\left( 2 \mu + 1 \right) ^ { 2 }$ primitives was $\left\{ - u _ { { \scriptscriptstyle m a x } } , - \frac { \mu - 1 } { \mu } u _ { { \scriptscriptstyle m a x } } , . . . , 0 , . . . , \frac { \mu - 1 } { \mu } u _ { { \scriptscriptstyle m a x } } , u _ { { \scriptscriptstyle m a x } } \right\}$ . Since is short, we treat the control input as a constant vector $u _ { m }$ . Using the initial state $\boldsymbol { x } _ { 0 } : = \left[ \boldsymbol { p } _ { 0 } ^ { \mathrm { ~ T ~ } } \quad \boldsymbol { \nu } _ { 0 } ^ { \mathrm { ~ T ~ } } \right] ^ { \mathrm { T } }$ , another form of $p _ { d } \left( t \right)$ is written as

$$
p _ {d} (t) = u _ {m} \frac {t ^ {2}}{2} + v _ {0} t + p _ {0}\tag{6}
$$

With both duration and control input are known and fixed, we calculate the actual cost of a motion primitive as $\left( \left\| u _ { m } \right\| ^ { 2 } + \rho \right) \tau$ Similar to traditional $\mathbf { A } ^ { * }$ , the formulation of Kinodynamic $\mathbf { A } ^ { * }$ algorithm has two parts, the actual cost and heuristic cost. Thus, the evaluation function f is as followed

$$
f = g + h\tag{7}
$$

where $g$ represents the actual cost from start state to current state, and h represents the heuristic cost. Thus, the actual cost g from the start state to the current state is accumulated as followed.

$$
g = \sum \left(\left\| u _ {m} \right\| ^ {2} + \rho\right) \tau\tag{8}
$$

## B. Heuristic Function

A suitable heuristic function reduces unnecessary expansion and results in faster searching. The distance between the current state and the goal state is heuristic for the traditional $\mathbf { A } ^ { * }$ algorithm. Since the evaluation of $g$ has changed, and the complexity of the Kinodynamic $\mathbf { A } ^ { * }$ algorithm is higher than that of ${ \mathrm {  ~ \bar { ~ } A ^ { * } , } }$ , it is essential to design an admissible and tight heuristic function to speed up node expansion. By minimizing $J ( T )$ from the current state to the goal state, using the Pontryagins minimum principle [16], we get

$$
\begin{array}{c} p _ {d} ^ {*} (t) = \frac {1}{6} \alpha_ {d} t ^ {3} + \frac {1}{2} \beta_ {d} t ^ {2} + v _ {d c} t + p _ {d c} \\ \left[ \begin{array}{l} \alpha_ {d} \\ \beta_ {d} \end{array} \right] = \frac {1}{T ^ {3}} \left[ \begin{array}{c c} - 1 2 & 6 T \\ 6 T & - 2 T ^ {2} \end{array} \right] \left[ \begin{array}{c} p _ {d g} - p _ {d c} - v _ {d c} T \\ v _ {d g} - v _ {d c} \end{array} \right] \\ J ^ {*} (T) = \sum_ {d \circ \{x, y \}} \left(\frac {1}{3} \alpha_ {d} ^ {2} T ^ {3} + \alpha_ {d} \beta_ {d} T ^ {2} + \beta_ {d} ^ {2} T\right) \end{array}\tag{9}
$$

where $p _ { d c } , \nu _ { d c } , p _ { d g } , \nu _ { d g }$ are the position and velocity of the current state and position and velocity of the goal state, respectively. And the heuristic function $\dot { h }$ can be described as

$$
h = J ^ {*} (T)\tag{10}
$$

The heuristic function h is only related to $T$ . To minimize $\boldsymbol { J } ^ { * } ( \boldsymbol { T } )$ for the optimal $T ,$ we need to obtain its extremum by making $\partial J ^ { * } \left( T \right) / \partial T = 0$ . Denoting the root as $T _ { h }$ , we get

$$
h = J ^ {*} \left(T _ {h}\right)\tag{11}
$$

Thus, the complete form of the evaluation function $f$ is expressed as

$$
f = g + h = \sum \left(\left\| u _ {m} \right\| ^ {2} + \rho\right) \tau + J ^ {*} \left(T _ {h}\right)\tag{12}
$$

## C. Collision and Dynamic Feasible Check

We aim to find a collision-free and dynamic feasible trajectory from the start state to the goal state. Hence, it is necessary to verify collision and dynamic constraints during the search process.

The environment is described with a two-dimensional occupancy grid map. The costmap, in which each grid has a value describing the probability of collision, can be generated based on the occupancy grid map. A set of positions that the system can traverse along the trajectory can be sampled using the cost map. We define a lethal cost, related to the size of robot, that represent the collision boundary as a hard constraint. For the duration , we need to ensure that the cost of each grid, corresponding to positions $p \left( t _ { i } \right)$ for all $i \in \{ 0 , . . . , I \}$ $t _ { i } \in \left[ 0 , \tau \right]$ , is no more than the lethal cost. The selection of I should guarantee that the maximum distance between two adjacent sampling points does not exceed costmap resolution R by setting the condition $\tau { \nu _ { _ { m a x } } } / I \geq R$

![](Wang2020Searchbased_figs/d58ea2bb7dc240e9644e750c71b48c4105cbe8cea99b4a1c98f5ebd554236849.jpg)  
Figure 2. Trend of cost value in the costmap.

The way to determine that the primitive satisfied the dynamic constraints, is to find the maximum and minimum derivatives, such as velocity and acceleration, during  . Because the derivatives are polynomial function of time, we can easily obtain their extrema and check if they are within the constraints.

## D. Soft Constraint for Safety

Although we obtain a collision-free trajectory with hard constraints, considering motion uncertainty, we prefer a trajectory that is as far away from obstacles as possible. Artificial Potential Field (APF) [17] is an efficient and commonly used method to maintain a path away from obstacles. However, it ignores dynamic constraints during re-optimization, and the resulting trajectory is often easily trapped in undesired local minima. Liu [18] models motion uncertainty as a soft constraint through the collision cost with an expression form of APF, but it requires a prior trajectory, from which the resulting trajectory is constrained to be within a tunnel.

A collision cost $J _ { c } ( \phi )$ was added to (5) to become $M \left( \phi , T \right)$ as a soft constraint during the searching process:

$$
M (\phi , T) = J (\phi) + \rho T + \rho_ {c} J _ {c} (\phi)\tag{13}
$$

where $\rho _ { c }$ is the weight coefficient about collision description and $J _ { c } ( \phi )$ is defined according to the trajectory

$$
J _ {c} (\phi) = \int_ {\phi} F (s) d s, s \in \mathsf {R} ^ {2}\tag{14}
$$

$F \left( s \right)$ is the cost in position, and it depends on the costmap value

$$
F (s) = \left\{ \begin{array}{c c} 0, & l (s) \geq l _ {2} \\ C (l (s)), & l _ {2} > l (s) \geq l _ {1} \\ C _ {\max} & l (s) <   l _ {1} \end{array} \right.\tag{15}
$$

where $l ( s )$ is the distance between the position s and the nearest obstacle, and $C _ { m a x }$ is the maximum value of $C ( l )$ . The inflation radius $l _ { 2 }$ can be affected by the environment and safety demands. Points outside the inflation radius are considered safe. The inscribed radius of the robot is $l _ { 1 }$ . For the points between $l _ { 1 }$ and $l _ { 2 }$ , the cost is defined by

$$
C (l) = C _ {\max} e ^ {- \lambda_ {c} (l - l _ {1})}\tag{16}
$$

where $\lambda _ { c }$ determines the decreasing rate of cost value while $l \in \left[ l _ { 1 } , l _ { 2 } \right]$ . Different from previous works [17], [18], gradient of cost function is not continuous and the range and trend can be adjusted by the inflation radius and the parameter $\lambda _ { c }$ which may result in sharp decreases at the boundary (Fig. 2).

In practice, we can calculate the accumulated cost of each primitive by sampling. Similar to the process of collision checks, we obtain a set of $I _ { c }$ dense points along primitives during time $\tau . \ I _ { c }$ is determined by

$$
I _ {c} = \frac {\nu_ {m a x} \tau}{R}\tag{17}
$$

where $R$ is the resolution of the costmap. Start and end points of a primitive are included, so that the time step $d t : = \tau / \left( I _ { c } - 1 \right)$ . And the integral can be discretized as

$$
\int_ {\phi} F (s) d s \approx \sum_ {i = 0} ^ {I _ {c} - 1} F \left(p _ {i _ {c}}\right) \| v _ {i _ {c}} \| d t\tag{18}
$$

where $p _ { i _ { c } }$ and $\nu _ { i _ { c } }$ are the position and velocity at time $i _ { c } \cdot d t$ Therefore, the evaluation function that produces a trajectory away from obstacles, ensuring safety of robots, is updated to

$$
\begin{array}{c} f = g + h + \rho_ {c} c _ {\text { collision }} \\ c _ {\text { collision }} = \sum_ {i = 0} ^ {I _ {c} - 1} F \left(p _ {i _ {c}}\right) \left\| v _ {i _ {c}} \right\| d t \end{array}\tag{19}
$$

and the influence of collision cost can be adjusted by adjusting the weight $\rho _ { c }$

## IV. TIMED ELASTIC BAND TRAJECTORY OPTIMIZATION

The trajectory generated by Kinodynamic $\mathbf { A } ^ { * }$ provides not only a collision-free path but also time information, with which we can refine the prior path for a smoother and safer trajectory and take yaw into account using the TEB approach. TEB is based on elastic band approach, defined by $B : { \mathbf { a } }$ sequence of n robot poses $S _ { i } = \left[ x _ { i } , y _ { i } , \theta _ { i } \right] ^ { T } \in \mathsf { R } ^ { 2 } \times S ^ { 1 }$ and $n - 1$ time intervals $\Delta T _ { i }$ . And $x _ { i } , y _ { i }$ is the position, while $\theta _ { i }$ is the orientation of the robot in global frame. These can be written as

$$
\begin{array}{c} Q = \left\{s _ {i} \right\} _ {i = 0 \dots n} n \in \mathsf {N} ^ {\prime}, \tau = \left\{\Delta T _ {i} \right\} _ {i = 0 \dots n - 1} \\ B := (Q, \tau) \end{array}\tag{20}
$$

Because of the robot’s omnidirectional properties, we obtain expressions for dynamic constraints that differ from those in [19]:

$$
\Delta s _ {i} = \left( \begin{array}{c} \Delta x _ {i} \\ \Delta y _ {i} \\ \Delta \theta_ {i} \end{array} \right) = \left( \begin{array}{c} x _ {i + 1} - x _ {i} \\ y _ {i + 1} - y _ {i} \\ \theta_ {i + 1} - \theta_ {i} \end{array} \right)\tag{21}
$$

where $\Delta { s _ { i } }$ contains the distance between consecutive positions and the angular change between the two position vectors. We convert $\Delta { s _ { i } }$ in time $\Delta T _ { i }$ from the world coordinate system to the robot coordinate system using

$$
\begin{array}{c} d x _ {i} = \Delta x _ {i} \cos \theta_ {i} + \Delta y _ {i} \sin \theta_ {i} \\ d y _ {i} = - \Delta x _ {i} \sin \theta_ {i} + \Delta y _ {i} \cos \theta_ {i} \end{array}\tag{22}
$$

after which, linear and angular velocity and acceleration can then be obtained as

$$
v _ {i x} = \frac {d x _ {i}}{\Delta T _ {i}}, v _ {i x} \in \left[ - v _ {x \min}, v _ {x \max} \right] v _ {i y} = \frac {d y _ {i}}{\Delta T _ {i}}, v _ {i y} \in \left[ - v _ {y \max}, v _ {y \max} \right]
$$

$$
a _ {i x} = \frac {v _ {(i + 1) x} - v _ {i x}}{\left(\Delta T _ {i} + \Delta T _ {i + 1}\right) / 2}, a _ {i x} \in \left[ - a _ {x \max}, a _ {x \max} \right]
$$

$$
a _ {i y} = \frac {v _ {(i + 1) y} - v _ {i y}}{(\Delta T _ {i} + \Delta T _ {i + 1}) / 2}, a _ {i y} \in \left[ - a _ {y \max}, a _ {y \max} \right]
$$

$$
\omega_ {i} = \frac {\Delta \theta_ {i}}{\Delta T _ {i}}, \omega_ {i} \in \left[ - \omega_ {\max}, \omega_ {\max} \right]
$$

$$
\alpha_ {i} = \frac {\omega_ {i + 1} - \omega_ {i}}{(\Delta T _ {i} + \Delta T _ {i + 1}) / 2}, \alpha_ {i} \in [ - \alpha_ {\max}, \alpha_ {\max} ]\tag{23}
$$

A total objective function

$$
\begin{array}{l} R (B) = \sum_ {k} \gamma_ {k} R _ {k} (B) \\ B ^ {*} = \underset {B} {\operatorname{argmin}} R (B) \end{array}\tag{24}
$$

where $B ^ { * }$ represents the optimal TEB. And component objective functions $R _ { k } \left( B \right)$ contain constraints about the minimum time, attraction of global path, repulsion of obstacles with respect to trajectory, and dynamic limits, such as velocity and acceleration [20]. What’s more, the different locomotion capabilities of quadruped robots in forward, backward and lateral directions decide the weight $\gamma _ { _ { k } }$ of the corresponding $R _ { k } \left( B \right)$ . And a new constraint about yaw is added to the total objective function to minimize the change of yaw in order to save energy. Finally, TEB algorithm adopts the g2o-framework to optimize and get solutions.

## V. EXPERIMENTAL RESULTS

## A. Platform Details

Jueying Mini has four legs with 12 actuators, and each leg has 3 degrees of freedom and each joint has an expanded range of motion. (Fig. 3) The kinodynamic constraints in navigation of Jueying Mini are shown in Table I. Jueying Mini is equipped with Velodyne VLP-16 LiDAR and IMU for sensing and state estimation. All software modules, including state estimation, mapping, and planning, run on a four-core 2.80 GHz processor with a 256 GB hard disk and a 8 GB RAM.

![](Wang2020Searchbased_figs/2cdbb27ac415bebd78427cc127f149acfcde46d73833e42809c5f998c9f3a236.jpg)  
Figure 3. The Jueying Mini quadruped robot.

TABLE I. KINODYNAMIC CONSTRAINTS IN EXPERIMENTS

<table><tr><td>Name</td><td>Value</td><td>Unit</td></tr><tr><td> $v_{x\ max}$ </td><td>0.75</td><td rowspan="3">m/s</td></tr><tr><td> $v_{x\ min}$ </td><td>0.10</td></tr><tr><td> $v_{y\ max}$ </td><td>0.20</td></tr><tr><td> $\omega_{max}$ </td><td>0.70</td><td>rad/s</td></tr><tr><td> $a_{x\ max}$ </td><td>1.00</td><td rowspan="2"> $m/s^2$ </td></tr><tr><td> $a_{y\ max}$ </td><td>0.17</td></tr><tr><td> $\alpha_{max}$ </td><td>0.52</td><td> $rad/s^2$ </td></tr></table>

## B. Simulations

1) Search-Based Planning Performance: To evaluate the Kinodynamic $\mathbf { A } ^ { * }$ algorithm, we compare its performance with that of the traditional $\mathbf { A } ^ { * }$ path planning algorithm. The results cannot be obtained directly, since the path generated by traditional $\mathbf { A } ^ { * }$ does not contain any kinodynamic information. Instead, we test the generated trajectories in real execution. With the only difference between experiments lying in the front-end, we can verify the performance between Kinodynamic $\mathbf { A } ^ { * }$ and traditional $\mathbf { A } ^ { * }$

The experiment was performed on a simulated irregular polygon map approximately $3 0 \mathrm { m } \times 3 0 \mathrm { m } .$ , with data recorded during navigation to evaluate the performance of two methods. As shown in Table II, the start and goal positions of four groups were randomly selected. For Kinodynamic $\mathbf { A } ^ { * }$ , the effort of trajectory and the total running time for each experiment was better than those of the traditional $\mathbf { A } ^ { * }$ Kinodynamic $\mathbf { A } ^ { * }$ resulted in a smoother and more easily tracked prior path, while the path of traditional $\mathbf { A } ^ { * }$ had many dynamically infeasible parts, which required more energy and time for the local planner to optimize and adjust. Therefore, we demonstrate that Kinodynamic $\mathbf { A } ^ { * }$ algorithm can finally lead to a smooth and fast trajectory to execute.

![](Wang2020Searchbased_figs/134ec6a135d48531f29009c35a65876374e50f62c99598ac4abd19b3b63c4986.jpg)

![](Wang2020Searchbased_figs/00031038d4ee3356d26ef89c28ffa29e67f1e0e29a6d6a3190f4233e33945389.jpg)  
(a) Traditional A\*  
(b) Kinodynamic $\mathbf { A } ^ { * }$

Figure 4. Dynamic feasibility performance. The yellow rectangle represents the outline, the yellow line represents the path, and the red arrow represents the position vector of the robot.  
![](Wang2020Searchbased_figs/04694bb84624e3dbd445122b74a8b336b3a903149963251e121e723002bf5da9.jpg)

![](Wang2020Searchbased_figs/f1c4dc017c2556ca8258a7cc40127012ea2b2ddca91c5d2efead710156e37b3c.jpg)  
(a) Kinodynamic $\mathbf { A } ^ { * } ,$ ${ \rho _ { c } } \mathrm { { = } } 0$  
(b) Kinodynamic $\mathbf { A } ^ { * } ,$ ${ \rho } _ { c } { = } 5$  
Figure 5. Performace after adding a collision cost. The collision cost can be achieved by adjusting $\rho _ { c }$ . The yellow rectangle represents the outline, the yellow line represents the path, and the red arrow represents the position vector of the robot.

TABLE II. COMPARISON OF PATH PLANNING ALGORITHMS

<table><tr><td rowspan="2"></td><td colspan="2">Total Running Time (s)</td><td colspan="2">Effort J</td></tr><tr><td>Kinodynamic A*</td><td>Traditional A*</td><td>Kinodynamic A*</td><td>Traditional A*</td></tr><tr><td>1</td><td>27.362</td><td>31.794</td><td>4.7630</td><td>5.5047</td></tr><tr><td>2</td><td>16.298</td><td>25.395</td><td>5.1730</td><td>6.8421</td></tr><tr><td>3</td><td>25.338</td><td>31.000</td><td>5.1201</td><td>5.8651</td></tr><tr><td>4</td><td>25.975</td><td>25.594</td><td>4.1946</td><td>7.4720</td></tr></table>

![](Wang2020Searchbased_figs/a8f01ccf2a7f8054e2817582566668080b7be6581e187b434a3e23397b2a871c.jpg)

![](Wang2020Searchbased_figs/5fa94a1c9879931e1b23555553da4e3abaa4bd132ca5a8378a0dfa0ff650fb91.jpg)  
(a) Traditional $\mathbf { A } ^ { * }$  
(b) Kinodynamic A\*  
Figure 6. The actual trajectories of the robot. The yellow line represents the actual trajectory of the robot and the red arrow represents the position vector of the robot.

![](Wang2020Searchbased_figs/624ed9f2f9b361f5cbb58aafa6f8b8be0e990fbf9dd15555901b2f81cff0142d.jpg)

Figure 7. Three parallel points are set up to simulate a situation where the robot is performing actual tasks. The robot needs to face toward the object and stay for 2s. The upper pictures shows the performance of the omnidirectional method, and the lower one shows the performance of the non-omnidirectional method.  
![](Wang2020Searchbased_figs/267044da366533d1e38bb7a6ea7a90663284f057a9413ba5f4739121e207e21e.jpg)  
Figure 8. Dynamic obstacle avoidance performance.

Another advantage of Kinodynamic $\mathbf { A } ^ { * }$ is that it takes kinodynamic characteristics into consideration. As shown in Fig.4, the global planner using $\mathbf { A } ^ { * }$ contains no motion information, it ignores the initial state, especially in re-planning. This may result in trajectories that are unsuitable. However, Kinodynamic $\mathbf { A } ^ { * }$ considers the robot’s initial state and avoids the unnecessary cost of turning around.

2) Collision Cost Performance: We verified the contribution of soft collision constraints. Fig. 5(a) shows results of the method without soft constraints, in which the robot may hit the obstacle inside the circle region. Fig. 5(b) shows the results of the method with collision costs, in which the robot avoids the obstacles by walking a safer path.

## C. Experiments

1) Search-Based Planning Performance: We conducted the experiment in an incompletely known environment with unexpected obstacles, unknown in the initial costmap. Fig. 6 shows the actual trajectories of the robot. The Kinodynamic $\mathbf { A } ^ { * }$ algorithm provided an easily tracked prior trajectory which led to a better final trajectory, while the trajectory produced by the traditional $\mathbf { A } ^ { * }$ algorithm had many dynamically infeasible parts that made tracking difficult for the local planner.

2) Omnidirectional Method Performance: We compared the performance of TEB under omnidirectional model assumption the non-omnidirectional model assumption in an indoor environment as shown in Fig. 7. The overall running time of each experiment was compared. Because of the difference in forward and lateral locomotion abilities, we set a greater weight for the forward direction. As shown in Table III and Fig. 7, the omnidirectional method was flexible and fast. Because the omnidirectional motion characteristics of the quadruped robot were considered, our method enabled robot to transfer flexibly between the parallel points by side shifting.

TABLE III. COMPARISON OF OMNIDIRECTIONAL AND NONOMINIDIRECTIONAL METHODS

<table><tr><td rowspan="2"></td><td colspan="2">Time(s)</td></tr><tr><td>Omnidirectional method</td><td>Non-omnidirectional method</td></tr><tr><td>To first via point</td><td>11</td><td>11</td></tr><tr><td>To second via point</td><td>10</td><td>20</td></tr><tr><td>To third via point</td><td>11</td><td>23</td></tr><tr><td>Total time</td><td>32</td><td>54</td></tr></table>

3) Dynamic Obstacle Avoidance: We test the robot using Kinodynamic $\mathbf { A } ^ { * }$ and TEB with the omnidirectional model in a dynamic and completely unknown environment as shown is Fig.8. Perception range limits prevented some obstacles from being considered in the initial global plan, which was a challenge to planning, requiring continuous and rapid re-planning to avoid sudden dangers. As shown in Fig. 8, our method can generate feasible trajectories and allow the robot to flexibly react. Additional details can be seen in our accompanying video.

## VI. CONCLUSION

In this paper, we describe the design of a complete autonomous navigation system for quadruped robots that takes into account their ability for flexible, powerful, and stable omnidirectional locomotion. We use a framework with a global planner and a local planner, to find a path from start to goal and calculate velocity commands for robot to execute. The global planner uses Kinodynamic $\mathbf { A } ^ { * }$ to find a smooth, safe, kinodynamically feasible, and minimum-time prior path, which contains hard and soft constraints to guarantee the clearance and dynamic feasibility. The initial path is refined by local planner using TEB method with an omnidirectional model. Finally, we verify the effectiveness and feasibility of our method through experiments and prove that our quadruped robot can perform more flexible movements and react rapidly to changes in complex environments.

## REFERENCES

[1] Hutter M, Marco C,Lauber A, et al. "Anymal-toward legged robots for harsh environments." Advanced Robotics 31.17 (2017): 918-931.

[2] Raibert M, Blankespoor K, Nelson G, et al. "Bigdog, the rough-terrain quadruped robot." IFAC Proceedings Volumes 41.2 (2008): 10822-10825.

[3] Park H W, Wensing P M, and Kim S. "High-speed bounding with the MIT Cheetah 2: Control design and experiments." The International Journal of Robotics Research 36.2 (2017): 167-192.

[4] Cheah, Wei, et al. "Grid-based motion planning using advanced motions for hexapod robots." 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2018.

[5] Winkler, Alexander W., et al. "Planning and execution of dynamic whole-body locomotion for a hydraulic quadruped on challenging terrain." 2015 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2015.

[6] <sub>Č</sub>ížek, Petr, Diar Masri, and Jan Faigl. "Foothold placement planning with a hexapod crawling robot." 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2017.

[7] Wermelinger, Martin, et al. "Navigation planning for legged robots in challenging terrain." 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2016.

[8] Wooden D, Malchano M, Blankespoor K, et al. "Autonomous navigation for BigDog." 2010 IEEE International Conference on Robotics and Automation. IEEE, 2010.

[9] Bellicoso C D, Bjelonic M, Wellhausen L, et al. "Advances in realworld applications for legged robots." Journal of Field Robotics 35.8 (2018): 1311-1326.

[10] Liu, Yufei, et al. "Research on path planning of quadruped robot based on globally mapping localization." 2020 3rd International Conference on Unmanned Systems (ICUS). IEEE, 2020.

[11] Dolgov D, Thrun S, Montemerlo M, et al. "Path planning for autonomous vehicles in unknown semi-structured environments." The International Journal of Robotics Research 29.5 (2010): 485-501.

[12] Liu S, Atanasov N, Mohta K, et al. "Search-based motion planning for quadrotors using linear quadratic minimum time control." 2017 IEEE/RSJ international conference on intelligent robots and systems (IROS). IEEE, (2017):2872-2879.

[13] Harper, Mario Y., et al. "Energy efficient navigation for running legged robots." 2019 International Conference on Robotics and Automation (ICRA). IEEE, 2019.

[14] http://www.deeprobotics.cn/

[15] Verriest, E. I., and F. L. Lewis. "On the linear quadratic minimum-time problem." IEEE transactions on automatic control 36.7 (1991): 859-863.

[16] Mueller M W, Hehn M,and D'Andrea R. "A computationally efficient motion primitive for quadrocopter trajectory generation." IEEE Transactions on Robotics 31.6 (2015): 1294-1310.

[17] Li G, Tamura Y, Yamashita A, et al. "Effective improved artificial potential field-based regression search method for autonomous mobile robot path planning." International Journal of Mechatronics and Automation 3.3 (2013): 141-170.

[18] Liu S, Mohta K, Atanasov N, et al. "Towards search-based motion planning for micro aerial vehicles." arXiv preprint arXiv:1810.03071 (2018).

[19] Rösmann C, Feiten W, Wösch T, et al. "Trajectory modification considering dynamic constraints of autonomous robots." ROBOTIK 2012; 7th German Conference on Robotics. VDE, 2012.

[20] Rösmann C, Feiten W, Wösch T, et al. "Efficient trajectory optimization using a sparse model." 2013 European Conference on Mobile Robots. IEEE, 2013.