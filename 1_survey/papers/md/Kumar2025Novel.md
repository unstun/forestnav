---
citation_key: Kumar2025Novel
arxiv_id: 2509.24143
arxiv_url: "https://arxiv.org/abs/2509.24143"
title: "A Novel Model for 3D Motion Planning for a Generalized Dubins Vehicle with Pitch and Yaw Rate Constraints"
authors_short: "Deepak Prakash Kumar et al."
year: 2025
direction_tag: K_dubins_reeds_shepp
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:17:07Z
origin: ai+web
reviewed: false
---

# A Novel Model for 3D Motion Planning for a Generalized Dubins Vehicle with Pitch and Yaw Rate Constraints

Deepak Prakash Kumar, Member, IEEE, Swaroop Darbha, Fellow, IEEE, Satyanarayana Gupta Manyam, Senior Member, IEEE, David W. Casbeer, Senior Member, IEEE

Abstract—In this paper, we propose a new modeling approach and a fast algorithm for 3D motion planning, applicable for fixedwing unmanned aerial vehicles. The goal is to construct the shortest path connecting given initial and final configurations subject to motion constraints. Our work differs from existing literature in two ways. First, we consider full vehicle orientation using a body-attached frame, which includes roll, pitch, and yaw angles. However, existing work uses only pitch and/or heading angle, which is insufficient to uniquely determine orientation. Second, we use two control inputs to represent bounded pitch and yaw rates, reflecting control by two separate actuators. In contrast, most previous methods rely on a single input, such as path curvature, which is insufficient for accurately modeling the vehicle’s kinematics in 3D. We use a rotation minimizing frame to describe the vehicle’s configuration and its evolution, and construct paths by concatenating optimal Dubins paths on spherical, cylindrical, or planar surfaces. Numerical simulations show our approach generates feasible paths within 10 seconds on average and yields shorter paths than existing methods in most cases.

Index Terms—Aerial systems: applications, 3D motion and path planning, Dubins vehicle.

## I. INTRODUCTION

HE use of Unmanned Aerial Vehicles (UAVs) is rapidly growing in civilian and military applications, including search and rescue and surveillance. Fixed-wing UAVs are of particular interest due to longer flight times, larger payload capacity, and the ability to fly at higher altitudes [1], [2]. However, they are persistently in motion, i.e., cannot stop or hover mid-air, and cannot change their heading angle instantaneously. Hence, they have a bound on the rate of change of their heading/orientation, which manifests itself as curvature constraints on the path. Motion planning is important for these vehicles, in which the goal is to plan the optimal path to travel from one configuration (i.e., position and orientation together) to another. The objective of interest in this paper is to obtain the minimum-time (or distance) path(s). We seek a finite set of candidate paths that includes the optimal path for any boundary condition. These candidate paths are suitable for constructing paths for fixed-wing aircraft or yaw rateconstrained vehicles.

Motion planning for yaw rate-constrained vehicles is typically addressed by considering a simplified kinematic model, called the Dubins model. This models a vehicle traveling at a constant speed and has a minimum turning radius constraint, which is suitable for UAVs traveling at constant altitude (in 2D). Dubins [3] solved the problem of the shortest path between a pair of configurations on a plane. It was shown that the optimal path is of type CSC, CCC, or a degenerate path of the same, where $C = L ,$ R denotes a left or a right turn of minimum turning radius, and S denotes a straight line segment. Although Dubins showed this result using geometric techniques, the same result was later derived using Pontryagin’s Minimum Principle ( [4]) in [5] using simpler proofs. Various variants of the planar path planning problem have been explored with variations in the model and/or the objective, such as in [6], where different left and right turning radius was considered.

Motion planning for such vehicles in 3D has also been an area of interest, where the shortest path to travel from one configuration to another, considering their motion constraints, is sought. The 3D problem applies not only to fixed-wing UAVs but also to underwater gliders and robots [7], [8]. Although specifying the heading angle alone uniquely defines the orientation of the vehicle in the 2D problem, the 3D problem requires both the heading angle and the plane in which the UAV lies. The UAV’s plane can be uniquely described using two additional angles (pitch and roll) or by a vector along its lateral or normal direction.

Simple kinematic models have also been used to tackle the 3D problem, where, similar to the 2D problem, the generated path can be tracked using a lower-level controller [9]. Because these paths can be computed very quickly, they can be combined with algorithms such as Rapidly Exploring Random Tree (RRT) to find feasible, obstacle-avoiding routes [10]. This method has also been experimentally demonstrated using an ARDrone in [11].

To our knowledge, the first exploration of the 3D problem was by Sussman [12]. The author showed that the optimal path is of type CSC, CCC, or a degenerate<sup>1</sup> version of these paths, or a helicoidal arc to connect a given location and heading direction<sup>2</sup>. Unlike the 2D problem, there are infinitely many $C$ segments since the plane containing the segment can be arbitrarily picked; due to the tangential S segment, many (finite) solutions may exist. Conditions exist for which infinitely many CSC paths exist, such as those shown in [13]. Hence, efficient construction of CSC paths has been explored in the literature. In [14], a CSC path was constructed for instances where the initial and final locations are spaced sufficiently far apart using geometric and numerical approaches. In a later work [15], the authors adopted this path as an initial guess for a nonlinear optimization problem that was solved using a multiple-shooting method to improve the solution. The CSC path construction was addressed in [13] as an inverse kinematics problem for a five degrees-of-freedom robotic manipulator. Analytical solutions were obtained for the path parameters to improve computational efficiency. CSC path construction was also recently addressed in [16]. In that work, the authors parametrized the path in terms of two variables and performed a numerical search, utilizing off-theshelf solvers assisted by derived gradients to construct the path.

In [17], the 3D problem was addressed with a model that has two controllable inputs - one for yaw rate, and another for the rate of change of the altitude. In this work, a “Dubins airplane model” was proposed, and it was shown that the optimal trajectory comprises segments with arcs of minimum turning radius, straight lines, or a Dubins path of a certain length. Depending on the altitude difference between the initial and final locations, feasible solutions were generated by introducing additional segments to attain the desired altitude. This model was modified in [18], wherein a pitch angle constraint was introduced. Contrary to [17], this paper generates trajectories by incorporating helicoidal segments to attain the desired altitude when necessary. Additionally, the constructed paths were validated by simulations using a six-degree-of-freedom model (given in [19]) and a vector-field-based guidance law, inspired by [20], for tracking.

The 3D motion planning problem has also been addressed using the 2D Dubins result in [21]. The authors consider a total curvature constraint and a bounded pitch angle for the vehicle. They decouple the CSC path to connect the given initial and final locations and heading vector into horizontal and vertical components. In this regard, they use the horizontal projection of the configurations to connect the locations and heading angles. The obtained path length is utilized as the x coordinate in the vertical plane, with the desired altitude difference to be attained serving as the z coordinate. Using iterative optimization of the horizontal and vertical turning radii, a feasible solution is constructed such that the total curvature bound and pitch angle bounds are satisfied. The authors used this solution to provide an initial guess to a nonlinear optimization problem to further refine the path in [22].

In the existing literature, we observe that the complete orientation of the vehicle has not been considered for 3D motion planning. This is because the description of the pitch and heading angles alone does not uniquely describe its orientation. For example, Fig. 1 shows two orientations for the same vehicle moving along a straight line trajectory with a pitch angle of $0 ^ { \circ }$ and a heading angle of $4 5 ^ { \circ }$ : one where the roll angle is $0 ^ { \circ }$ and another where the roll angle is $4 5 ^ { \circ }$ . Infinitely many orientations exist for the same trajectory. However, from these figures, we can observe that prescribing the longitudinal direction and the lateral or normal direction of the vehicle would uniquely describe the orientation.<sup>3</sup> While the study in [23] models the complete configuration of a general robot, it is unclear how their model relates to the kinematics of a fixed-wing UAV.

![](Kumar2025Novel_figs/0c3f0d05aec4b48d0cbafb0aff7e9d339289491220db43a14a82503157f29cde.jpg)

![](Kumar2025Novel_figs/5319388ce6ff7f601bcf06edd71b725c131885d1f5e86031515d2596751e9978.jpg)  
(a) Roll angle $\qquad = \quad 0 ^ { \circ }$ (animation (b) Roll $\mathsf { a n g l e } = \ 4 5 ^ { \circ }$ (animation provided on our GitHub page) provided on our GitHub page)  
Fig. 1. Depiction of two orientations corresponding to the same heading and pitch angle

The literature on path planning for aerial robots has primarily focused on models with a single control input, such as yaw rate, or a single constraint on the path’s curvature. In the 3D generalization of path planning, a single control input alone cannot capture the range of motions. This is because there are two elementary motions of interest for the motion planning of aerial vehicles: pitch and yaw. For fixed-wing UAVs, pitch motion is achieved using elevators, and yaw motion is achieved with rudder and/or aileron<sup>4</sup> [19]. Since yaw and pitch motion are controlled by separate actuators, considering a single control is not sufficient. Hence, it is crucial to consider two control inputs: a bounded pitch rate and a bounded yaw rate. These constraints correspond to the minimum turning radii, $R _ { p i t c h }$ and $R _ { y a w } ,$ of the path’s curvature. The bounds on the pitch and yaw rates manifest as locally inaccessible spherical regions of radii $R _ { p i t c h }$ and $R _ { y a w } ,$ , respectively.<sup>5</sup> Though two control inputs are considered in [17], the second control input is the rate of change of the altitude of the vehicle; furthermore, the pitch angle is not considered in this model, which makes it more appropriate for a quadcopter.

A demonstration of the limitations of state-of-the-art approaches that rely on a single control input is presented in Fig. 2 for two instances. In both of these cases, paths were generated using the method from [21] - for which the code is publicly available. The minimum turning radius for this model was set to 40 meters to enforce the curvature constraint. In the following, we analyze these examples to explain why this path planning method is either infeasible or inefficient for the proposed (3D) model.

1) Our proposed model incorporates two independent control inputs for the yaw and pitch rates. We set the minimum pitch turning radius, $R _ { p i t c h }$ , to 40 meters<sup>6</sup> for the first example. This choice is consistent with the parameter used in [21]. Since the yaw turning radius, $R _ { y a w } ,$ can be chosen independently, we set it to 50 meters. The solution generated by [21], shown in Fig. 2a, violates the yaw rate constraint by entering the yaw motion sphere. Such a maneuver is infeasible as the vehicle must travel a sufficient distance outside the sphere before entering it. This behavior is analogous to the infeasibility of entering the left or right turning circles in the 2D Dubins problem [3].

2) In the second example, we alternately pick $R _ { y a w }$ in our model to be the same as the parameter in [21], which is 40 meters. Since $R _ { p i t c h }$ is free to choose, we set $R _ { p i t c h }$ to be equal to 60 meters. The path obtained using the algorithm from [21] is shown in Fig. 2b. We observe that the path enters one of the pitch motion spheres (which lies at the top of the vehicle), and hence violates the pitch rate constraint.

Alternatively, one could argue that the maximum of $R _ { y a w }$ and $R _ { p i t c h }$ can be chosen as the minimum turning radius in [21]. However, this would lead to inefficient motion planning, since the vehicle would take larger-than-necessary turns in some instances.

The presented issues were addressed in our previous work in [24], where a special case of motion planning on the surface of a sphere was studied. This paper provided insights for the 3D motion planning by considering a vehicle model with bounded yaw rate and pitch rate. Furthermore, the spherical motion planning problem was shown to arise as an intermediary problem to be solved for the 3D problem.

Having identified two major issues in the literature, the contributions of this paper are as follows:

1) We present a novel model using a rotation minimizing frame, also called the Bishop frame, to obtain the shortest path for a vehicle subject to pitch rate and yaw rate constraints. We build on the insights provided in [24] for the 3D problem.

2) We prove that the pitch rate and yaw rate constraints manifest as four spheres around the vehicle that represent temporarily inaccessible regions, thereby appropriately generalizing the 2D Dubins model to 3D.

![](Kumar2025Novel_figs/e94b688f2f0c0c8e94ee3104107c9eb8875afe739b645ca92913f04ddec0547b.jpg)

![](Kumar2025Novel_figs/e95199c00ddf05437a2bf48938778ec1e98619d84d9bdf4d6d32a5f34ff166ce.jpg)  
(a) Yaw rate violation for (b) Pitch rate violation for $R _ { \mathit { p i t c h } } = 4 0 ~ \mathsf { m }$ $R _ { y a w } = 5 0 \ R _ { y a w } = 4 0$ m. $R _ { p i t c h } = 6 0$ m. m.  
Fig. 2. Issue with single control input

3) We propose a path construction algorithm that consists of three classes of paths. The main idea is to build path segments on spherical surfaces that are tangent to the initial and final configurations, and these segments are connected by an intermediary surface. This surface could be a cylindrical envelope, a cross-tangent plane, or another spherical surface.

4) We pose and solve a Dubins-type path planning problem subject to curvature constraints on a cylindrical surface. To the best of our knowledge, the cylindrical motion planning problem has not been addressed in the literature. The proposed solution method involves unwrapping the surface to a two-dimensional plane, computing the optimal Dubins path, and then mapping back onto the cylindrical surface.

5) We present extensive numerical results on several instances. We show the effect of (i) model that defines the complete configuration of the vehicle, (i.e., heading and lateral orientation) and (ii) the impact of minimum turning radii on the best feasible path. We also observe that our algorithm can produce a high-quality feasible solution within 10 seconds. Additionally, we provide the code in a publicly available repository.<sup>7</sup>

## II. MODELING AND GEOMETRIC PRELIMINARIES

Let t and s denote the time and arc length, respectively, and X(s) denote the instantaneous location of the vehicle. We consider a Rotation-Minimizing frame, also called a Bishop frame [25], attached to the center of mass of the UAV. Let T, Y, U denote the unit vectors of the Bishop frame with T, Y directed along the longitudinal and lateral directions of the vehicle, respectively. The vector $\mathbf { U } : = \mathbf { T } \times \mathbf { Y }$ is along the normal direction of the vehicle. Fig. 3 shows the vehicle configuration with the vectors T, Y and U.<sup>8</sup>

![](Kumar2025Novel_figs/798d82cb44236878e7987531dc2bd274c8c6abca10bc9774ebf242168affa292.jpg)  
Fig. 3. The configuration of the vehicle defined by the three vectors T, Y and U

The instantaneous angular velocity of the frame can be written as

$$
\omega (t) = \omega_ {x} (t) \mathbf {T} (t) + \omega_ {y} (t) \mathbf {Y} (t) + \omega_ {z} (t) \mathbf {U} (t),
$$

with $\omega _ { x } , \omega _ { y } , \omega _ { z }$ denoting the components in the T, Y, and U directions, respectively. One may think of them as the roll, pitch, and yaw rates of the body, respectively. Notably, the Rotation Minimizing Frame (RMF) is constructed so that $\omega _ { x } ( t ) = 0 \colon$ : there is no rotation about the tangent, minimizing frame twisting (essentially, the roll rate is set to zero).<sup>9</sup> The kinematics of the frame then satisfy:

$$
\begin{array}{r l} & {\frac {d \mathbf {T}}{d t} = \omega (t) \times \mathbf {T} (t) = \omega_ {z} (t) \mathbf {Y} (t) - \omega_ {y} (t) \mathbf {U} (t),} \\ & {\frac {d \mathbf {Y}}{d t} = \omega (t) \times \mathbf {Y} (t) = - \omega_ {z} (t) \mathbf {T} (t),} \\ & {\frac {d \mathbf {U}}{d t} = \omega (t) \times \mathbf {U} (t) = \omega_ {y} (t) \mathbf {T} (t).} \end{array}
$$

A key property of an RMF is that Y(t) and U(t) change only in the direction of T(t).

Assume that the vehicle moves at a constant, nonzero longitudinal speed $V _ { 0 }$ . Defining

$$
\kappa_ {g} (s) := \frac {\omega_ {z} (s)}{V _ {0}}, \qquad \kappa_ {n} (s) := - \frac {\omega_ {y} (s)}{V _ {0}},\tag{1}
$$

the kinematic equations parameterized in terms of s become

$$
\frac {d \mathbf {X} (s)}{d s} = \frac {1}{V _ {0}} \frac {d \mathbf {X}}{d t} = \mathbf {T} (s),\tag{2}
$$

$$
\frac {d \mathbf {T} (s)}{d s} = \kappa_ {g} (s) \mathbf {Y} (s) + \kappa_ {n} (s) \mathbf {U} (s),\tag{3}
$$

$$
\frac {d \mathbf {Y} (s)}{d s} = - \kappa_ {g} (s) \mathbf {T} (s),\tag{4}
$$

$$
\frac {d \mathbf {U} (s)}{d s} = - \kappa_ {n} (s) \mathbf {T} (s).\tag{5}
$$

<sup>8</sup>We also denote T, Y, and U as tangent, tangent normal, and surface normal vectors, respectively.

<sup>9</sup>Since $\omega _ { x } = 0 ,$ , the generated paths do not allow for unbounded roll. The paths constructed remain feasible for a model with non-zero roll rate assumption, however, the paths may be suboptimal when additional constraints, such as bounded roll angles or rates, are imposed. Extending our model and method to enforce bounds on the roll angle would be valuable, and can be considered an important direction for future work.

The bounds for control inputs $\kappa _ { g }$ and $\kappa _ { n }$ , which we refer to as geodesic curvature and normal curvature, respectively, are stated as shown below,<sup>10</sup>

$$
| \kappa_ {n} | \leq \frac {1}{R _ {p i t c h}}, \quad | \kappa_ {g} | \leq \frac {1}{R _ {y a w}}.\tag{6}
$$

We shall later show that $R _ { p i t c h }$ is the minimum turning radius corresponding to pitch motion and $R _ { y a w }$ is the minimum turning radius corresponding to the yaw motion. The objective is to compute the minimum distance trajectory from the initial to final configuration, defined by X, T, Y, and U. Hence, the cost to minimize is $J = \int 1 d s$

Remark 1 (Model). Three angles (roll, pitch, and yaw), or equivalently, T, Y, and U, are required to specify the UAV’s orientation in 3D, but only two (pitch and yaw) are directly controlled by the primary actuators on a fixedwing UAV (aileron, rudder, and elevator). The roll angle evolves naturally as a consequence of coordinated turning [19], wherein ailerons, which cause roll, allows the vehicle to turn. From a planning perspective, the two control inputs are sufficient to reach any orientation; this is analogous to rigid-body kinematics, wherein a z-y-z rotation can be used to reach any orientation. The Bishop frame is used to separate vehicle orientation from path geometry, enabling continuous and physically feasible orientation profiles while capturing the aircraft’s kinematics.

Geometrically, the path planning problem can be depicted as shown in Fig. 4. A detailed description of this figure follows.

![](Kumar2025Novel_figs/7c5f61ee176dd99300e6fd7400f8851d62b467f2c4aef8d497987964611f017f.jpg)  
Fig. 4. Depiction of spheres corresponding to pitch motion (in orange and magenta) and yaw motion (in blue and green) at the initial and final configuration

In Fig. 4, it can be observed that four spheres are constructed, which are tangential to the vehicle configuration. To understand how they appear, we need to understand the geometric impact of the curvatures, $\kappa _ { n }$ and $\kappa _ { g }$ . To this end, we derive the closed-form expression for X, T, Y, and U over an interval wherein $\kappa _ { g }$ and $\kappa _ { n }$ are constants. The obtained expressions are shown in Appendix A.

We remark here that since the control inputs appear linearly in the differential equations (3)-(5), and a minimum time problem is considered, the optimal control actions are expected to be bang-bang from Pontryagin’s minimum principle $[ 4 ] . ^ { 1 1 }$ Therefore, it is sufficient to consider intervals in which $\kappa _ { g }$ and $\kappa _ { n }$ are constant. Furthermore, it suffices to consider $\begin{array} { r } { \kappa _ { g } \in \{ - \frac { 1 } { R _ { u a w } } , 0 , \frac { 1 } { R _ { u a w } } \} } \end{array}$ and $\begin{array} { r } { \kappa _ { n } \in \{ - \frac { 1 } { R _ { p i t c h } } , 0 , \frac { 1 } { R _ { p i t c h } } \} } \end{array}$ Using the closed-form expressions derived in Appendix A, we state and prove the following two lemmas.

Lemma 1. When $\begin{array} { r } { \kappa _ { n } = \frac { 1 } { R _ { p i t c h } } ~ o r - \frac { 1 } { R _ { p i t c h } } } \end{array}$ the corresponding segment lies on spheres with radius $\dot { R _ { p i t c h } }$ whose center lies along U $o r \mathrm { ~ - ~ } \mathbf { U }$ , respectively. Furthermore, such segments correspond to a maximum ascent or descent motion of the vehicle with a turning radius of $\frac { 1 } { \sqrt { \kappa _ { g } ^ { 2 } + \frac { 1 } { R _ { p i t c h } ^ { 2 } } } } .$

Proof. The proof is provided in Appendix B.

The following lemma states a similar result in a different axis, and the proof follows the same reasoning.

Lemma 2. When $\begin{array} { r } { \kappa _ { g } = \pm \frac { 1 } { R _ { u a w } } } \end{array}$ , the corresponding segment lies on spheres with radius $\tilde { R } _ { y a w }$ whose center lies along Y $o r - \mathbf { Y }$ . Furthermore, such segments correspond to maximum turn (left or right) motion of the vehicle with a turning radius $\begin{array} { r } { o f \frac { 1 } { \sqrt { \frac { 1 } { R _ { y a w } ^ { 2 } } + \kappa _ { n } ^ { 2 } } } } \end{array}$

From these two lemmas, we see that the normal curvature $\kappa _ { n }$ governs the pitch motion, while the geodesic curvature $\kappa _ { g }$ governs the yaw motion. In fact, these curvatures directly correspond to the vehicle’s pitch rate and yaw rate, respectively (which is expected based on the Bishop frame setup and the definitions in (1)). When the vehicle moves with its maximum pitch rate and zero yaw rate, it follows a great circle of radius $R _ { p i t c h }$ on the orange or purple sphere shown in Fig. 4. This result comes from Lemma 1. Since the vehicle travels at unit speed, the time to complete the circle is $t _ { p i t c h } = 2 \pi R _ { p i t c h }$ Over this time, the pitch angle changes by 2π, so the pitch rate is $\begin{array} { r } { \frac { 2 \pi } { t _ { p i t c h } } = \frac { 1 } { R _ { p i t c h } } } \end{array}$ . A similar argument holds for the yaw rate, giving a maximum value of $\frac { 1 } { R _ { u a w } }$ . Therefore, $\kappa _ { n }$ and $\kappa _ { g }$ represent the vehicle’s pitch and yaw rates, respectively.

By varying $\begin{array} { r l r } { \kappa _ { n } } & { { } \in } & { \left\{ - \frac { 1 } { R _ { p i t c h } } , 0 , \frac { 1 } { R _ { p i t c h } } \right\} } \end{array}$ and $\kappa _ { g } \in$ $\begin{array} { r } { \left\{ - \frac { 1 } { R _ { u a w } } , 0 , \frac { 1 } { R _ { u a w } } \right\} } \end{array}$ , we obtain nine distinct motion primitives, shown in $\mathrm { F i g . } \ 5$ . These were generated using the closed-form expressions, presented in Appendix A. Using Lemma 1, we find that the segments $L _ { s i } , R _ { s i } , L _ { s o } ,$ and $R _ { s o }$ have radius $\frac { 1 } { \sqrt { \frac { 1 } { R _ { y a w } ^ { 2 } } + \frac { 1 } { R _ { p i t c h } ^ { 2 } } } }$ , corresponding to motion with maximum ab-

solute pitch and yaw rates. Here, L and R denote a left turn and right turn, respectively, which correspond to $\begin{array} { r } { \kappa _ { g } = \frac { 1 } { R _ { y a w } } } \end{array}$ and $\begin{array} { r } { \kappa _ { g } = - \frac { 1 } { R _ { y a w } } } \end{array}$ , respectively. Additionally, subscripts $^ { \ast } s i ^ { \prime }$ and $" s o ^ { \prime \prime }$ are used to refer to the segments that lie on the “inner” sphere and “outer” sphere, respectively; the inner sphere corresponds to $\begin{array} { r } { \kappa _ { n } ~ = ~ \frac { 1 } { R _ { p i t c h } } } \end{array}$ , and the outer sphere corresponds to $\begin{array} { r } { \kappa _ { n } = - \frac { 1 } { R _ { p i t c h } } } \end{array}$ . The segments $G _ { s i }$ and $G _ { s o }$ result from pure pitch motion $( \kappa _ { g } \ = \ 0 )$ , while $L _ { p }$ and $R _ { p }$ result from pure yaw motion. When both curvatures are zero $( \kappa _ { n } = \kappa _ { g } = 0 )$ , the vehicle moves in a straight line segment S.

Using the obtained motion primitives and the observation that $\kappa _ { n }$ and $\kappa _ { g }$ attaining values of $\pm \frac { 1 } { R _ { p i t c h } }$ and $\pm \frac { 1 } { R _ { u a w } }$ yields two spheres each (a pair along U and a pair along Y), we can observe that at both the initial and final configuration, four spheres exist around the vehicle. Additionally, portions of the optimal path will lie on one of the four spheres at the initial configuration and one of the four spheres at the final configuration<sup>12</sup>. Hence, we propose three classes of paths to construct a feasible path connecting one of the initial spheres with one of the final spheres. We construct the path using three types of intermediary surfaces (or classes): a cylindrical envelope, a planar surface, or a spherical surface. These three classes of paths are a generalization of the classical CSC and CCC paths for the planar Dubins problems. In our algorithm, we consider a sphere at the initial or final configuration to serve as a generalization of the turn segment (C) in a plane; furthermore, we consider the cylindrical envelope and planar surface to generalize the S segment. In the following section, we describe the three classes of paths in more detail.

![](Kumar2025Novel_figs/958edd27d296e8f7738f168c179767593ca00504d037bd619da382f928cedd0b.jpg)

![](Kumar2025Novel_figs/48f6d26391938a76f6bb4d4dd8b00708cd1dfa9eff2d5f0b7c0ada2f9daa761d.jpg)  
(b) Segments on spheres corresponding to max. yaw rate (and straight line segment)  
Fig. 5. Visualization of segments [24]. We note that $L _ { s i } , R _ { s i } , L _ { s o } ,$ and $R _ { s o }$ are shown in both subfigures, since each of these segments lies on two spheres.

Remark 2. In general, the yaw and pitch rates for different UAVs may vary and can be coupled. The problem posed here is still of significant interest in obtaining lower and upper bounds for the shortest path length. One such case is illustrated by the region within the boundaries, shown in brown, in Fig. 6. However, by replacing the boundary with a rectangular region inscribed within this area, one can derive an upper bound that is a feasible solution. Similarly, by outer approximating the allowable region with a larger rectangular region, shown in green in Fig. 6, a lower bound for the optimal path length can be obtained.

![](Kumar2025Novel_figs/35c200a6efb57b1891649f04279fcd319e6c913aaaa8a505b118ef46e96009fe.jpg)  
Fig. 6. Generic control inputs region and obtaining bounds for rectangular control input region considered in this paper

## III. SHORTEST PATH CONSTRUCTION

The constructed paths start and end on a spherical surface at the initial and final configurations. Three distinct classes of paths are presented, each using a different intermediary surface for the sub-path between the spheres, which can be cylindrical, planar, or spherical. We refer to the spheres centered along the U-axis as the inner (orange, along U) and outer (purple, along −U) spheres, as shown in Fig. 4. Similarly, the spheres centered along the Y-axis are called the left (green, along Y) and right (blue, along −Y) spheres.

The intermediary sub-paths considered are as follows:

1) In the first class, the sub-path is constructed using a cylindrical envelope. In this case, we connect the pair of spheres of the same type at the initial and final configurations. There are four such pairs: inner-to-inner, outer-to-outer, left-to-left, and right-to-right. Fig. 7a illustrates the cylindrical envelope between inner and outer spheres. We will later show that these paths satisfy the curvature constraints in (6). The full construction is detailed in Section IV.

2) In the second class of paths, a sub-path between a pair of spheres is constructed on a cross-tangent plane. For spheres of opposite type, such as inner-to-outer, outerto-inner, left-to-right, or right-to-left, a path through a cylindrical envelope is not feasible. This is because the normal vector of the cylindrical surface, U for pitch spheres and Y for yaw spheres, remains constant along the envelope and does not support a continuous feasible orientation between opposing directions. Hence, such spheres are connected using a cross-tangent plane. An example for the inner-to-outer case is shown in Fig. 7b. Details of this construction are provided in Section V.

3) In the third class of paths, we construct sub-paths between pairs of spheres of the same type using an intermediary sphere. There are four such configurations: inner–outer–inner, outer–inner–outer, left–right–left, and right–left–right. These paths are designed for initial and final locations that are close to each other. An example of this type is illustrated in Fig. 7c, and the full construction is described in Section VI.

Remark 3. Note that only the listed classes are possible using a single intermediary surface. For example, connecting an inner sphere at the initial configuration with a left sphere at the final configuration is not possible. A cylindrical surface cannot be used because the outward normal directions differ: −U for the inner sphere and −Y for the left sphere. Since the normal vector remains constant across cylindrical, spherical, and frustum surfaces, none of these can bridge the two spheres. A planar surface also doesn’t work, as there is no common tangent plane between the two. For instance, the T − Y plane is tangent to the inner sphere but not to the left sphere (see Fig. 4). Therefore, using a single intermediary surface, we can only connect either a pair of pitch spheres or a pair of yaw spheres, not a mix of both. The underlying reason is that X, T, Y, and U must be continuous. The same argument applies for using an intermediary sphere as the tangential sphere to the initial and final spheres, i.e., only a right sphere can be used to connect two left spheres.

Remark 4. Although it is possible to connect a pair of spheres of the same type (e.g., inner–inner) using a plane, we do not consider such paths in this paper. This is because the planar connection is a special case of the cylindrical connection. This is because a plane can be wrapped into a cylinder without changing the path length or violating the curvature constraints. We discuss this preservation property in more detail when introducing the cylindrical path construction in the next section.

Remark 5. In Sections IV, V, and VI, we present the methodology for constructing three types of paths by introducing parameters that describe each path, which are subsequently discretized. Whenever we refer to the “shortest” path, we mean the least-length path obtained by our construction methodology under the chosen discretization; global optimality is not claimed. However, we note that the subpath constructed on each individual surface (cylinders, spheres, and planes) is optimal for that surface. Our methodology will always yield a feasible path, as at least the first class of path (through the cylindrical envelope) always exists.

## IV. PATH SYNTHESIS ON CYLINDRICAL ENVELOPE

To generate a feasible path connecting two spheres of the same radius and type via a cylindrical envelope (as shown in Fig. 7a), the vehicle follows this sequence:

• Step 1: The path starts on the initial sphere and transitions to the cylindrical surface. The transition point, ${ \bf { X } } _ { i c } ,$ lies on the boundary circle formed by the intersection of the sphere and the cylindrical envelope. At this point, its longitudinal direction aligns with $\mathbf { T } _ { i c } ,$ as illustrated in Fig. 8.

• Step 2: The path exits the cylindrical envelope at $\mathbf { X } _ { o c } ,$ with longitudinal direction $\mathbf { T } _ { o c }$

• Step 3: Finally, the path continues on the final sphere to reach the desired final configuration.

Note that the entry and exit points on the cylinder, along with their corresponding tangent directions, are not fixed and can be freely chosen. We parameterize these directions using four angles: ${ \theta } _ { i c } , \ { \phi } _ { i c } , \ { \theta } _ { o c } ,$ and $\phi _ { o c }$ . The following section describes how the path on the spheres and the cylinder is constructed based on these four parameters.

![](Kumar2025Novel_figs/2eb28e1e8d0350ad00f5f146fda8d0873655e3823534da05c29f67ed03429cff.jpg)  
Fig. 7. Depiction of surfaces used to connect spheres at the initial and final configurations

![](Kumar2025Novel_figs/7de1bd37cd14a3bd7a7133a67a3096fe8fe4d7a207c7c02d3fcf401bd5230895.jpg)  
Fig. 8. Notation for discretization of position and headings on a cylinder connecting two spheres

Remark 6. Since cylinders connect spheres of the same type, the cylinder always has the same radius as the spheres and thus does not expand or shrink.

## A. Origins of the Spheres and Axes of the Cylinders

We begin by deriving expressions for the centers of the spheres at the initial and final configurations, denoted by $\mathbf { r } _ { i }$ and $\mathbf { r } _ { f } .$ , respectively. These vectors are given by

$$
\mathbf {r} _ {i} = \mathbf {X} _ {i} + \delta_ {i, o} ^ {i n i t i a l} R _ {p i t c h} \mathbf {U} _ {i} + \delta_ {l, r} ^ {i n i t i a l} R _ {y a w} \mathbf {Y} _ {i},\tag{7}
$$

$$
\mathbf {r} _ {f} = \mathbf {X} _ {f} + \delta_ {i, o} ^ {f i n a l} R _ {p i t c h} \mathbf {U} _ {f} + \delta_ {l, r} ^ {f i n a l} R _ {y a w} \mathbf {Y} _ {f}.\tag{8}
$$

Here, $\delta _ { i , o } ^ { i n i t i a l } = 1 , - 1$ or 0 depending on whether the inner sphere, outer sphere, or one of the left/right spheres is selected at the initial configuration, respectively. Similarly, $\delta _ { l , r } ^ { i n i t i a l } =$ $1 , - 1 , 0$ if the left sphere, right sphere, or one of the inner/outer spheres is chosen. The same interpretation applies for $\delta _ { i , o } ^ { f i \ i }$ nal and $\delta _ { l , r } ^ { f i n a l }$ . For cylindrical envelope constructions, we require that $\delta _ { i , o } ^ { \ ' i n i t i a l } = \delta _ { i , o } ^ { f i n a l }$ and $\delta _ { l , r } ^ { i n i t i a l } = \delta _ { l , r } ^ { f i n a l }$

We can obtain the axis of the cylinder that connects the selected pair of spheres as (refer to Fig. 7a)

$$
\mathbf {k} = \frac {\mathbf {r} _ {f} - \mathbf {r} _ {i}}{\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}}.\tag{9}
$$

Furthermore, the length of the cylinder is given by $h = \| \mathbf { r } _ { f } -$ $\mathbf { r } _ { i } \lVert _ { 2 }$ . Since the radius of the cylinder is the same as the radius of the selected pair of spheres, the cylinder’s radius is $R _ { p i t c h }$ if $\delta _ { i , o } ^ { i n n e r } \neq 0$ and $R _ { y a w }$ if $\delta _ { l , r } ^ { i n n e r } \neq 0$

We now derive expressions for the entry and exit points on the cylinder $( \mathbf { X } _ { i c }$ and $\mathbf { X } _ { o c } )$ as well as their corresponding tangent directions $( \mathbf { T } _ { i c }$ and $\mathbf { T } _ { o c } )$ .

B. Parameters for the location and tangent vector on the cylinder

On the cylindrical envelope, we parameterize the entry point $\mathbf { X } _ { i c }$ and the tangent $\mathbf { T } _ { i c }$ by two angles, $\theta _ { i c }$ and $\phi _ { i c }$ (see Fig. 8). Likewise, $\theta _ { o c }$ and $\phi _ { o c }$ parameterize the exit point $\mathbf { X } _ { o c }$ and the corresponding tangent $\mathbf { T } _ { o c }$ . To derive these expressions, we introduce a body frame $B ( O _ { B } , x , y , z )$ centered at the cylinder’s base point $\mathbf { r } _ { i } ,$ with its z-axis aligned along the cylinder axis (also shown in Fig. 8).<sup>13</sup>

The expressions for $\mathbf { X } _ { i c }$ and $\mathbf { X } _ { o c }$ can be derived in the body frame B to be

$$
\mathbf {X} _ {i c} ^ {\mathcal {B}} = \left( \begin{array}{c} \overline {{R}} \cos \theta_ {i c} \\ \overline {{R}} \sin \theta_ {i c} \\ 0 \end{array} \right), \quad \mathbf {X} _ {o c} ^ {\mathcal {B}} = \left( \begin{array}{c} \overline {{R}} \cos \theta_ {o c} \\ \overline {{R}} \sin \theta_ {o c} \\ h \end{array} \right),\tag{10}
$$

where $\overline { { R } }$ is the radius of the cylinder, and is given by

$$
\overline {{R}} = R _ {p i t c h} | \delta_ {i, o} ^ {i n i t i a l} | + R _ {y a w} | \delta_ {l, r} ^ {i n i t i a l} |.\tag{11}
$$

We can derive the direction cosines of the tangent vector when it enters and exits the cylinder as (refer to Fig. 8)

$$
\begin{array}{l} \mathbf {T} _ {i c} ^ {\mathcal {B}} = \mathbf {R} _ {z} (\theta_ {i c}) \mathbf {R} _ {x} (\phi_ {i c}) \left( \begin{array}{c} 0 \\ 1 \\ 0 \end{array} \right) = \left( \begin{array}{c} - \sin \theta_ {i c} \cos \phi_ {i c} \\ \cos \theta_ {i c} \cos \phi_ {i c} \\ \sin \phi_ {i c} \end{array} \right), \\ \mathbf {T} _ {o c} ^ {\mathcal {B}} = \mathbf {R} _ {z} (\theta_ {o c}) \mathbf {R} _ {x} (\phi_ {o c}) \left( \begin{array}{c} 0 \\ 1 \\ 0 \end{array} \right) = \left( \begin{array}{c} - \sin \theta_ {o c} \cos \phi_ {o c} \\ \cos \theta_ {o c} \cos \phi_ {o c} \\ \sin \phi_ {o c} \end{array} \right). \end{array}
$$

Here, $\mathbf { R } _ { z }$ and $\mathbf { R } _ { x }$ are standard elementary rotation matrices for rotation about the z and x axis, respectively.

The entry position $\mathbf { X } _ { i c }$ and tangent direction $\mathbf { T } _ { i c }$ in the global frame ${ \mathcal { G } } ( O , X , Y , Z )$ can be expressed as

$$
\mathbf {X} _ {i c} ^ {\mathcal {G}} = \left( \begin{array}{c c c} \mathbf {x} & \mathbf {y} & \mathbf {z} \end{array} \right) \mathbf {X} _ {i c} ^ {\mathcal {B}} + \left( \begin{array}{c} X _ {O _ {\mathcal {B}}} \\ Y _ {O _ {\mathcal {B}}} \\ Z _ {O _ {\mathcal {B}}} \end{array} \right),\tag{12}
$$

$$
\mathbf {T} _ {i c} ^ {\mathcal {G}} = \left( \begin{array}{c c c} \mathbf {x} & \mathbf {y} & \mathbf {z} \end{array} \right) \mathbf {T} _ {i c} ^ {\mathcal {B}},\tag{13}
$$

where $\mathbf { x } , \mathbf { y } .$ , and z are unit vectors along the $x , y , z$ axes of the body frame $B ,$ and $X _ { O _ { B } } , Y _ { O _ { B } } , Z _ { O _ { B } }$ is the location of the body frame’s origin. Analogous expressions hold for $\mathbf { X } _ { o c }$ and $\mathbf { T } _ { o c } .$

With the expressions for the entry and exit locations and their corresponding tangent vectors on the cylindrical envelope now established, we proceed to construct the optimal path on the initial and final spheres, as well as on the cylindrical envelope.

## C. Generation of paths on initial and final spheres

Consider the chosen sphere at the initial configuration. We need to obtain the optimal path connecting the initial configuration to the location $\mathbf { X } _ { i c } ^ { g }$ with heading direction given by $\mathbf { T } _ { i c } ^ { \overline { { \mathcal { G } } } }$ to enter the cylindrical envelope (as shown in Fig. 8). We simplify this problem by translating the sphere’s center to the origin. This allows us to analyze the motion using a Sabban frame [24], [26]. The task becomes finding the optimal path on the sphere’s surface that connects an initial location $\mathbf { X } _ { s p , 0 }$ and tangent $\mathbf { T } _ { s p , 0 }$ to a final location and tangent.

In [24], [26], the Sabban frame model was used to study motion planning on a unit sphere. The configuration of the vehicle was specified by a location $\hat { \mathbf { X } } _ { s p }$ (which is a unit vector pointing radially outwards), a tangent vector $\mathbf { T } _ { s p }$ along the longitudinal direction of the vehicle, and a normal vector $\mathbf { N } _ { s p }$ along the lateral direction. Additionally, the path was parametrized in terms of arc length s. ˆ The evolution equations for these vectors are given by

$$
\begin{array}{l} \frac {d \hat {\mathbf {X}} _ {s p}}{d \hat {s}} (\hat {s}) = \mathbf {T} _ {s p} (\hat {s}), \quad \frac {d \mathbf {T} _ {s p}}{d \hat {s}} (\hat {s}) = - \hat {\mathbf {X}} _ {s p} (\hat {s}) + \hat {u} _ {g} \mathbf {N} _ {s p} (\hat {s}), \\ \frac {d \mathbf {N} _ {s p}}{d \hat {s}} (\hat {s}) = - \hat {u} _ {g} \mathbf {T} _ {s p} (\hat {s}), \end{array} \tag {14}\tag{14}
$$

where $\hat { u } _ { g } ~ \in ~ [ - \hat { U } _ { m a x } , \hat { U } _ { m a x } ]$ is the geodesic curvature on the unit sphere and serves as the control input. It relates to the minimum turning radius $\hat { r }$ on the unit sphere by $\begin{array} { r } { \hat { r } = \frac { 1 } { \sqrt { 1 + \hat { U } _ { m a r } ^ { 2 } } } } \end{array}$

We can adapt the previous results for motion planning on a sphere of any radius (R) by scaling the problem to a unit sphere problem.<sup>14</sup> First, we compute the normal vector $\begin{array} { r } { \mathbf { N } _ { s p } : = \frac { 1 } { R } \mathbf { X } _ { s p } \times \mathbf { T } _ { s p } } \end{array}$ . While scaling does not affect the tangent vector $\mathbf { T } _ { s p } ^ { * }$ or the normal vector $\mathbf { N } _ { s p } .$ , other parameters change. The location on the unit sphere becomes $\begin{array} { r } { \hat { \mathbf { X } } _ { s p } : = \frac { 1 } { \overline { { R } } } { \mathbf { X } } _ { s p } , } \end{array}$ , and the corresponding minimum turning radius becomes $\begin{array} { r } { \hat { r } = \frac { 1 } { \overline { { R } } } r . } \end{array}$ A detailed derivation of this scaling is available in Appendix C.

![](Kumar2025Novel_figs/7569c77e6f600a35f64b39cc1c391ff97ed7ebe985b717bfe1b3d1b52ffbdfa6.jpg)  
Fig. 9. Motion planning on sphere with radius $\overline { { R } }$ and on a unit sphere

From [24], the candidate optimal paths on a unit sphere are of type CGC, CCC for $\begin{array} { r } { \hat { r } \le \frac { 1 } { 2 } } \end{array}$ , CGC, CCCC, or a degenerate path for $\textstyle { \frac { 1 } { 2 } } < { \hat { r } } \leq { \frac { 1 } { \sqrt { 2 } } }$ , and CGC, CCCCC, or $C C _ { \pi } C ^ { 1 5 }$ for $\textstyle { \frac { 1 } { \sqrt { 2 } } } < { \hat { r } } \leq { \frac { \sqrt { 3 } } { 2 } } . { ^ { 1 6 } }$ The analytical computation of the arc angles for each path is provided in [27]. We note here that the arc angles of the segments of a path on the unit sphere and the corresponding path on the sphere with radius $\bar { \overline { { { R } } } } \bar { { } }$ would be the same. Hence, we can obtain the arc angles of the segments for each candidate path on the sphere with radius R using [27].

Remark 7. The arc angle ϕ is related to the segment length l by $l = \hat { r } \phi$ for L and R segments, and $l = \phi$ for a $G$ segment on a unit sphere.

Finally, we want to obtain the expressions for $\mathbf { X } _ { s p } , \ \mathbf { T } _ { s p } .$ and $\mathbf { N } _ { s p }$ along the path to describe the instantaneous configuration of the vehicle along the sphere. We can obtain these expressions by solving the Sabban frame equations, derived in Appendix C, using the Euler-Rodriguez formula. Therefore, the configuration of the vehicle on the sphere along the path can be obtained.

The last step to be performed is to obtain the configuration of the vehicle in 3D (which utilizes the rotation minimizing frame). Since we had shifted the origin of the sphere to

frame chosen

coincide with the origin of the global frame ${ \mathcal { G } } ,$ the location (X) and longitudinal direction (T) can be easily obtained as

$$
\mathbf {X} (s) = \mathbf {X} _ {s p} (s) + \mathbf {r} _ {i}, \quad \mathbf {T} (s) = \mathbf {T} _ {s p} (s).
$$

Furthermore, depending on the type of sphere chosen at the initial configuration, Y and U can be computed (refer to Fig. 9). If $\delta _ { i , o } ^ { \bar { i } n i t i a l } \neq 0$ or $\delta _ { l , r } ^ { i n i t i a l } \neq 0$ , the expressions for U (the surface normal) and Y (the tangent normal) are obtained, respectively, as (refer to Figs. 4 and 9)

$$
\begin{array}{r l} & {\mathbf {U} (s) = - \delta_ {i, o} ^ {i n i t i a l} \frac {1}{R} \mathbf {X} _ {s p} (s), \quad \delta_ {i, o} ^ {i n i t i a l} \neq 0,} \\ & {\mathbf {Y} (s) = - \delta_ {l, r} ^ {i n i t i a l} \frac {1}{R} \mathbf {X} _ {s p} (s), \quad \delta_ {l, r} ^ {i n i t i a l} \neq 0.} \end{array}
$$

When $\delta _ { i , o } ^ { i n i t i a l } \neq 0 , { \bf Y } = { \bf U } \times { \bf T } ;$ ; when $\delta _ { l , r } ^ { i n i t i a l } \neq 0$ , U = $\mathbf { T } \times \mathbf { Y }$ . The path on the sphere at the final configuration is constructed similarly.

## D. Generation of path on cylinder

In this section, we describe the construction of the optimal Dubins path on a cylindrical surface. This path connects an initial and final configuration on the cylinder, which we had previously parameterized in terms of ${ \theta } _ { i c } , \ \phi _ { i c } , \ { \theta } _ { o c } ,$ , and $\phi _ { o c } .$ . The path we construct on the cylinder must obey the geodesic curvature (yaw rate) and normal curvature (pitch rate) constraints for the 3D model. We note that the radius of the cylinder is ${ \overline { { R } } } ,$ whose definition is given in (11). We choose the bound on the geodesic curvature for motion over the cylinder to be

$$
| \kappa_ {g, c y c} | \leq \left\{ \begin{array}{l l} \frac {1}{R _ {p i t c h}}, & \delta_ {i, o} ^ {i n i t i a l} = 0, \\ \frac {1}{R _ {y a w}}, & \delta_ {l, r} ^ {i n i t i a l} = 0. \end{array} \right.\tag{15}
$$

We claim that the considered radius for the cylinder and the geodesic curvature bounds satisfy the geodesic curvature and normal curvature constraints for the 3D problem.

Lemma 3. The optimal path on a cylinder of radius ${ \overline { { R } } } ,$ defined in (11), with geodesic curvature bounds given by (15) satisfies the geodesic curvature and normal curvature bounds for the proposed rotation minimizing frame model.

Proof. The proof is provided in Appendix D.

□

We present the construction of the optimal path on the cylinder. Note that geodesic curvature is bending invariant [28]. Hence, we can unwrap the cylinder onto a plane, as shown in Fig. 10, and construct the optimal path on the plane. Finally, the constructed path on the plane can be wrapped back onto the cylinder.

1) Unwrapping frame for cylinder: For unwrapping the cylinder, we consider a frame $u ,$ referred to as the unwrapping frame, with axes $x _ { \mathit { U } } , \mathit { y } _ { \mathit { U } }$ , and $z _ { M }$ . The origin for U is at the point of entry of the cylinder $( \mathbf { X } _ { i c } )$ . Furthermore, $z _ { M }$ is parallel to z and $y u$ points radially inwards to the cylinder. We will use the unwrapping frame for constructing the path on the plane. Once we construct such a path, we will represent it in the body frame $B ,$ and finally obtain the vehicle’s configuration in the global frame G for the 3D problem.

Consider a point $Q$ on the cylinder. The relationship between its location in the unwrapping frame $( \mathbf { X } _ { Q } ^ { \mathcal { U } } )$ and the body frame $( \mathbf { X } _ { Q } ^ { B } )$ is given by<sup>17</sup>

$$
\mathbf {X} _ {Q} ^ {\mathcal {B}} = \left( \begin{array}{c c c} - \sin \theta_ {i c} & - \cos \theta_ {i c} & 0 \\ \cos \theta_ {i c} & - \sin \theta_ {i c} & 0 \\ 0 & 0 & 1 \end{array} \right) \mathbf {X} _ {Q} ^ {\mathcal {U}} + \left( \begin{array}{c} \overline {{R}} \cos \theta_ {i c} \\ \overline {{R}} \sin \theta_ {i c} \\ 0 \end{array} \right).\tag{16}
$$

![](Kumar2025Novel_figs/b6bcbf99b04f3074b4e4c8e96bddddf0c85dd9de6f419911601c1eee5108d713.jpg)

![](Kumar2025Novel_figs/67c487762996b60a11afa3cff19db5bd3390020fd09dc1431092fb745f272696.jpg)  
(b) Unwrapping plane chosen  
Fig. 10. Frames on the cylinder and the unwrapping plane chosen for the cylinder

Using (16), we can represent the entry location $\mathbf { X } _ { i c }$ and the exit location $\mathbf { X } _ { o c }$ in the unwrapping frame U as ${ \bf X } _ { i c } ^ { U } = { \bf \Psi }$ $( 0 , 0 , 0 ) ^ { T }$ and $\mathbf { X } _ { o c } ^ { \mathcal { U } } = ( \overline { { R } }$ sin $( \delta \theta ) , \overline { { R } } ( 1 - \overline { { \cos { ( \delta \theta ) } } } ) , h ) ^ { T }$ . Here, the expression for $\mathbf { X } _ { o c } ^ { B }$ from (10) was used, and $\delta \theta : = \theta _ { o c } - \theta _ { i c } .$

We now aim to unwrap the cylindrical surface onto a plane, selecting the tangent plane at $\mathbf { X } _ { i c }$ as reference. Therefore, the unwrapping plane is defined by $x _ { \mathcal { U } }$ and $z _ { \mathcal { U } }$ axes, as shown in Fig. 10b. We will now describe the mapping of the initial and final configurations of the cylinder to the unwrapping plane.

2) Configurations after unwrapping cylinder: Consider unwrapping a point on the cylinder as shown in Fig. 11. A point $P ,$ whose coordinates are (R sin (δθ), R(1 − cos (δθ)), δd) in $u ,$ gets mapped to two points on the plane due to periodicity of the angle $\bar { \delta \theta } \in ( - \pi , \pi ] ^ { \bar { 1 } 8 }$ . Hence, the two images of $P$ obtained on the plane, shown in Fig. 11, are given by $P _ { 1 } ( \overline { { R } } \theta _ { 1 } , \delta d )$ and $P _ { 2 } ( \overline { { R } } \theta _ { 2 } , \delta d )$ , where

$$
\theta_ {1} = \left\{ \begin{array}{l l} \delta \theta , & \delta \theta \geq 0 \\ \delta \theta + 2 \pi , & \delta \theta <   0 \end{array} , \quad \theta_ {2} = \left\{ \begin{array}{l l} \delta \theta - 2 \pi , & \delta \theta > 0 \\ \delta \theta , & \delta \theta \leq 0 \end{array} . \right. \right.\tag{17}
$$

The two images corresponding to the final configuration, which is the exit location of the cylinder, obtained on the unwrapping plane, are shown in Fig. 12. It can be observed that the heading angles for the entry and exit locations are $\phi _ { i c }$ and $\phi _ { o c }$ on the plane, respectively (compare with Fig. 10).

![](Kumar2025Novel_figs/4f99cac933e9ba263d746962c91c46e2510c027c18167b6d1bfe449a82c7b3ab.jpg)  
Fig. 11. Unwrapping point lying on the cylinder

![](Kumar2025Novel_figs/91a05226b07ec27f446577d4c3824ba5339bc2b8545080cbb18cb48530158006.jpg)  
Fig. 12. Initial configuration and two images of the final configuration obtained on the unwrapping plane

We can now plan the optimal path to each image of the final configuration on the plane. To this end, we generate the six 2D Dubins candidate paths (CSC and CCC) using the analytical expressions provided in [29] to each image, and pick the shortest path. Let this shortest path be

$$
\mathbf {X} _ {p l a n e} (s) = \left(u (s), v (s)\right) ^ {T},\tag{18}
$$

where s is the arc length. Additionally, let the instantaneous heading angle on the plane be $\psi ( s )$ , which is the angle made with respect to $x _ { \mathcal { U } }$

3) Wrapping path onto cylinder: After the path is generated on the unwrapped plane, the corresponding path on the cylinder is retrieved by inverse mapping. To this end, consider a point given by $( \overline { { R } } \theta , d )$ on the unwrapping plane. The corresponding image of this point on the cylinder will be (R sin $\theta , \overline { { R } } ( 1 - \cos \theta ) , d )$ in U using the previously established procedure (refer to Fig. 11).

Now, consider the curve on the plane given by (18). Using the previous argument, the corresponding curve obtained on the cylinder in the unwrapping frame U is given by

$$
\mathbf {X} _ {c y l} ^ {\mathcal {U}} (s) = \left(\overline {{R}} \sin \left(\frac {u (s)}{\overline {{R}}}\right), \overline {{R}} \left(1 - \cos \left(\frac {u (s)}{\overline {{R}}}\right)\right), v (s)\right) ^ {T}.\tag{19}
$$

We now prove that the proposed mapping preserves the length of the curve.

Lemma 4. The proposed mapping between a planar curve and the wrapped curve on the cylindrical surface preserves the length of the curve.

Proof. The proof is provided in Appendix E.

Using (16), the equation of the considered curve in (19) can be obtained in the body frame B as

$$
\mathbf {X} ^ {\mathcal {B}} (s) = \left( \begin{array}{c} \overline {{R}} \cos \left(\theta_ {i c} + \frac {u (s)}{\overline {{R}}}\right) \\ \overline {{R}} \sin \left(\theta_ {i c} + \frac {u (s)}{\overline {{R}}}\right) \\ v (s) \end{array} \right).\tag{20}
$$

We compute the tangent vector along the path using the instantaneous heading angle $\psi ( s )$ obtained from the 2D Dubins path on the $x _ { U } z _ { U }$ plane. Hence, the angle made by T in the unwrapped plane with respect to $x _ { \mathcal { U } }$ , which is the heading angle, is known (refer to Fig. 12). From Fig. 10a, the direction cosines of T expressed in the body frame can be obtained as

$$
\mathbf {T} ^ {\mathcal {B}} (s) = \left( \begin{array}{c} - \sin \left(\theta_ {i c} + \frac {u (s)}{\overline {{R}}}\right) \cos \left(\psi (s)\right) \\ \cos \left(\theta_ {i c} + \frac {u (s)}{\overline {{R}}}\right) \cos \left(\psi (s)\right) \\ \sin \left(\psi (s)\right) \end{array} \right).
$$

If the inner or outer sphere was chosen at the initial configuration, the expression for U in B can be obtained by noting that it is radially outwards or inwards to the cylinder, as (refer to Fig. 7a)

$$
\mathbf {U} ^ {\mathcal {B}} = - \delta_ {i, o} ^ {i n i t i a l} \left(\cos \left(\theta_ {i c} + \frac {u (s)}{\overline {{R}}}\right), \sin \left(\theta_ {i c} + \frac {u (s)}{\overline {{R}}}\right), 0\right) ^ {T}.
$$

Alternatively, if the left or right spheres were chosen, the same expression for $\mathbf { Y } ^ { B }$ is obtained with $\delta _ { i . o } ^ { i n i t i a l }$ replaced with $\delta _ { l , r } ^ { i n i t i a l }$ . The expression for Y when $\delta _ { i . o } ^ { i n i t i a l } \neq 0$ and U when $\delta _ { l . r } ^ { i n i t i a l } \neq 0$ can be obtained as $\mathbf { Y } ^ { B } = \mathbf { U } ^ { B } \times \mathbf { T } ^ { B }$ and $\mathbf { U } ^ { B } = \mathbf { T } ^ { B ^ { \prime \prime } } \times \mathbf { Y } ^ { B }$ , respectively.

Finally, the expressions for X, T, Y, and U can be obtained in the global frame $\mathcal { G }$ using (12) and (13) (refer to Fig. $8 ) ^ { 1 9 }$ Hence, we have obtained the configuration of the vehicle along the shortest path on the cylinder for chosen ${ \theta } _ { i c } , { \phi } _ { i c } , { \theta } _ { o c } ,$ and $\phi _ { o c }$ values; this path satisfies the pitch and yaw rate constraints of the vehicle.

Remark 8. Though four parameters were introduced for path construction using a cylindrical envelope in the beginning of Section IV, the initial and final sphere computations depend only on two parameters each $( \theta _ { i c }$ and $\phi _ { i c } ,$ or $\theta _ { o c }$ and $\phi _ { o c } )$ Furthermore, the motion planning on the cylinder depends on $\phi _ { i c } , \phi _ { o c }$ , and the difference between $\theta _ { i c }$ and $\theta _ { o c }$

To compute the best feasible path for a selected pair of spheres at the initial and final configuration, we discretize $\theta _ { i c }$ and $\theta _ { o c }$ in [0, 2π). We discretize $\phi _ { i c }$ and $\phi _ { o c }$ over the interval $[ 0 , \pi ]$ , representing the feasible interval of heading angles that allow the path to enter the cylinder at $\mathbf { X } _ { i c }$ and exit at $\mathbf { X } _ { o c }$ (refer to Fig. 8). The number of discretizations of $\theta _ { i c }$ and $\theta _ { o c }$ are determined by a parameter $\theta _ { d i s c } .$ , whereas $\phi _ { d i s c }$ dictates the number of discretizations for $\phi _ { i c }$ and $\phi _ { o c }$ . We choose the combination that yields the shortest feasible path.

## V. CONSTRUCTING FEASIBLE SOLUTION USING CROSS-TANGENT PLANE

In this section, we describe the second class of paths where the sub-path between the initial and final spheres is constructed on a cross-tangent plane. There exist infinitely many crosstangent planes between these two spheres; the locus of the point of intersection of these cross-tangent planes with the initial/final sphere will be a circle, as shown in Fig. 13. To uniquely define a cross-tangent plane, we use angle θ as a parameter (see Fig. 13).

![](Kumar2025Novel_figs/0fa28da0b44ed986dbb908e63d234e53a00a151e2fce92fc3679dbc8abc62c57.jpg)  
Fig. 13. Parameterization of family of planes and configurations at entry and exit from cross-tangent plane

Remark 9. From Fig. 13, we can observe that the considered cross-tangent plane exists when $\| \mathbf { r } _ { f } - \mathbf { r } _ { i } \| _ { 2 } \geq 2 \overline { { R } }$ , i.e., when the spheres at the initial and final configurations do not intersect.

We denote the center of the locus at the initial and final spheres by A and B, respectively, as shown in Fig. 13. The location of A and B can be obtained as

$$
\mathbf {A} = \mathbf {r} _ {i} + \overline {{R}} \cos \alpha \left(\frac {\mathbf {r} _ {f} - \mathbf {r} _ {i}}{\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}}\right),\tag{21}
$$

$$
\mathbf {B} = \mathbf {r} _ {f} - \overline {{R}} \cos \alpha \left(\frac {\mathbf {r} _ {f} - \mathbf {r} _ {i}}{\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}}\right),\tag{22}
$$

where $\begin{array} { r } { \alpha : = \cos ^ { - 1 } \bigg ( \frac { 2 \overline { { R } } } { \| \mathbf { r } _ { f } - \mathbf { r } _ { i } \| _ { 2 } } \bigg ) } \end{array}$ . Here, the expressions for $\mathbf { r } _ { i }$ and $\mathbf { r } _ { f }$ are given in (7) and (8), respectively, and $\overline { { R } }$ is given in (11). The cross-tangent plane between the initial and final spheres is needed for inner-outer, outer-inner, left-right, and right-left pairings. It follows that $\delta _ { i , o } ^ { i n i t i a l } ~ = ~ - \delta _ { i , o } ^ { f i n a l }$ and $\delta _ { l , r } ^ { i n i t i a l } = - \delta _ { l , r } ^ { f i n a l }$

To define the parameter $\theta ,$ we first designate a unit vector x perpendicular to $\mathbf { r } _ { f } \ - \ \mathbf { r } _ { i } ,$ , as shown in Fig. 13.<sup>20</sup> The angle θ specifies the point of tangency on the initial sphere, with respect $\operatorname { t o } \ \mathbf { x } .$ In other words, θ describes the point of intersection of the cross-tangent plane with the circular locus of cross-tangent planes (shown in green) on the initial sphere; since the point of tangency is on the circular locus and x lies on the circular locus, θ, which is measured as the angle from x, uniquely describes the point. We then define another unit vector $\begin{array} { r } { \mathbf { y } : = \left( \frac { \mathbf { r } _ { f } - \mathbf { r } _ { i } } { \| \mathbf { r } _ { f } - \mathbf { r } _ { i } \| _ { 2 } } \right) \times \mathbf { x } } \end{array}$ , which is orthogonal to both x and the axis (k, defined in (9)) between the spheres. Using x and $\mathbf { y } ,$ we now express the entry and exit points $\mathbf { X } _ { i c }$ and $\mathbf { X } _ { o c } ,$ which are the points of tangency (see Fig. 13).

$$
\begin{array}{r l} & {\mathbf {X} _ {i c} (\theta) = \mathbf {A} + \overline {{R}} \sin \alpha \cos \theta \mathbf {x} + \overline {{R}} \sin \alpha \sin \theta \mathbf {y},} \\ & {\mathbf {X} _ {o c} (\theta) = \mathbf {B} + \overline {{R}} \sin \alpha \cos (\theta + \pi) \mathbf {x} + \overline {{R}} \sin \alpha \sin (\theta + \pi) \mathbf {y}.} \end{array}
$$

Next, we parameterize the tangent vectors at the entry and exit points using angles $\phi _ { i c }$ and $\phi _ { o c } .$ defined relative to the axis t, where t is a unit vector pointing from $\mathbf { X } _ { i c } ( \theta )$ to $\mathbf { X } _ { o c } ( \theta )$ (see Fig. 13). The tangent vectors $\mathbf { T } _ { i c }$ and $\mathbf { T } _ { o c }$ at the entry and exit points are derived as below:

$$
\begin{array}{l} \mathbf {T} _ {i c} (\phi_ {i c}) = \cos \phi_ {i c} \mathbf {t} (\theta) + \sin \phi_ {i c} \left(\frac {\mathbf {X} _ {i c} (\theta) - \mathbf {r} _ {i}}{\overline {{R}}} \times \mathbf {t} (\theta)\right), \\ \mathbf {T} _ {o c} (\phi_ {o c}) = \cos \phi_ {o c} \mathbf {t} (\theta) + \sin \phi_ {o c} \left(\frac {\mathbf {X} _ {i c} (\theta) - \mathbf {r} _ {i}}{\overline {{R}}} \times \mathbf {t} (\theta)\right). \end{array}
$$

Given the location and tangent vectors at the exit point from the initial sphere and the entry point of the final sphere, we can construct the optimal path over each sphere using the approach in Section IV-C. We can also construct the path on the crosstangent plane using the 2D Dubins result [3], [29], illustrated in Fig. 14. In this figure, the minimum turning radius $R _ { p l a n e }$ is dictated by the type of spheres considered at the initial and final configurations. If we are considering inner-outer or outerinner connections, $R _ { p l a n e } = R _ { y a w }$ since the vehicle moves in the T − Y plane (as observed from Fig. 13). Alternatively, $R _ { p l a n e } = R _ { p i t c h }$ if left-right or right-left sphere connections are considered.

![](Kumar2025Novel_figs/29315035d7efc4d5ed9592bd2dc66e0733555cac88464fde564940ad5b28f0fe.jpg)  
Fig. 14. Configurations on cross-tangent plane

After the path on the plane is constructed, the vehicle’s coordinates (u and v) and the heading angle (ψ) are defined. We can reconstruct the configuration of the vehicle along the path in 3D. First, we compute the location and the tangent vector along the plane as

$$
\begin{array}{l} \mathbf {X} (s) = \mathbf {X} _ {i c} + u (s) \mathbf {t} (\theta) + v (s) \left(\frac {\mathbf {X} _ {i c} (\theta) - \mathbf {r} _ {i}}{\overline {{R}}} \times \mathbf {t} (\theta)\right), \\ \mathbf {T} (s) = \cos \left(\psi (s)\right) \mathbf {t} (\theta) \\ \qquad + \sin \left(\psi (s)\right) \left(\frac {\mathbf {X} _ {i c} (\theta) - \mathbf {r} _ {i}}{\overline {{R}}} \times \mathbf {t} (\theta)\right). \end{array}
$$

The vectors U and Y are computed depending on $\delta _ { i , o } ^ { i n i t i a l } \neq 0$ or $\delta _ { l , r } ^ { i n i t i a l } \neq 0$ , as shown below:

$$
\begin{array}{r l} & {\mathbf {U} (s) = - \delta_ {i, o} ^ {i n i t i a l} \frac {\mathbf {X} _ {i c} (\theta) - \mathbf {r} _ {i}}{\overline {{R}}}, \quad \delta_ {i, o} ^ {i n i t i a l} \neq 0,} \\ & {\mathbf {Y} (s) = - \delta_ {l, r} ^ {i n i t i a l} \frac {\mathbf {X} _ {i c} (\theta) - \mathbf {r} _ {i}}{\overline {{R}}}, \quad \delta_ {l, r} ^ {i n i t i a l} \neq 0.} \end{array}
$$

Further, we can compute these vectors as $\mathbf { Y } = \mathbf { U } \times \mathbf { T }$ when $\delta _ { i , o } ^ { i n i t i a l } \neq 0 .$ , and $\mathbf { U } = \mathbf { T } \times \mathbf { Y }$ when $\delta _ { l , r } ^ { i n i t i a l } \neq 0$ . Thus, the vehicle’s configuration in 3D is completely described on the initial sphere, cross-tangent plane, and final sphere.

Note that the path construction for this class is a function of the three parameters: θ, $\phi _ { i c } .$ , and $\phi _ { o c }$ . However, motion planning on each of the surfaces depends only on two parameters. We optimize on these parameters by discretizing $\theta \in [ 0 , 2 \pi )$ , and $\phi _ { i c }$ and $\phi _ { o c }$ in $[ - \frac { \pi } { 2 } , \frac { \pi } { 2 } ]$ (refer to Fig. 13). The number of discretizations of θ is dictated by $\theta _ { d i s c } ,$ whereas $\phi _ { d i s c }$ represents the number of discretizations for $\phi _ { i c }$ and $\phi _ { o c } .$ We choose the parameter set that yields the shortest path length for each pairing of the initial and final spheres.

## VI. CONSTRUCTING FEASIBLE SOLUTION USING INTERMEDIARY SPHERE

In this section, we present the construction of the third class of paths. When the initial and the final positions are sufficiently close, we construct a path that goes through an intermediary spherical surface. We consider the four possible combinations in this regard, as outlined in Section III. This class of paths exists only when the Euclidean distance between the initial and final position satisfies $\| \mathbf { r } _ { f } - \mathbf { r } _ { i } \| _ { 2 } \leq 4 \overline { { R } }$ , as illustrated in Fig. 7c.

We parameterize the center of the intermediary sphere using a parameter $\alpha .$ The locus of the center of the intermediary sphere is a circle, as shown in Fig. 15. The value of $\alpha$ is related to the radius of this circular locus, and can be derived to be

$$
\alpha = \cos^ {- 1} \left(\frac {\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}}{4 \overline {{R}}}\right),
$$

and the radius of the circular locus is $2 \overline { { R } }$ sin α.

To parameterize the center of the intermediary sphere, we generate a unit vector x perpendicular to $\mathbf { r } _ { f } - \mathbf { r } _ { i }$ (similar to the one in Section IV). We define $\theta \in [ 0 , { \overset { \cdot } { 2 } } \pi )$ as the angle made by the center of the intermediary sphere on the circular locus with respect to x, similar to the definition for the crosstangent plane case. This parameter specifies the location of the intermediary sphere. Hence, we can define the center of the intermediary sphere as (refer to Fig. 15)

$$
\begin{array}{l} \mathbf {X} _ {c} (\theta) = \mathbf {r} _ {i} + \frac {1}{2} (\mathbf {r} _ {f} - \mathbf {r} _ {i}) \\ \qquad + 2 \overline {{R}} \sin \alpha \left(\cos \theta \mathbf {x} + \sin \theta \left(\frac {\mathbf {r} _ {f} - \mathbf {r} _ {i}}{\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}} \times \mathbf {x}\right)\right). \end{array}
$$

Given $\mathbf { X } _ { c } ,$ entry point $( \mathbf { X } _ { i c } )$ and exit point $( \mathbf { X } _ { o c } )$ for the intermediary sphere are derived as shown below,

$$
\mathbf {X} _ {i c} (\theta) = \frac {1}{2} \left(\mathbf {r} _ {i} + \mathbf {X} _ {c} (\theta)\right), \quad \mathbf {X} _ {o c} (\theta) = \frac {1}{2} \left(\mathbf {r} _ {f} + \mathbf {X} _ {c} (\theta)\right).
$$

![](Kumar2025Novel_figs/d1156871821d96cb534fc5a94839f4a4af401a9cc14c9308d766d8de1239ea3b.jpg)  
Fig. 15. Parameterization of the locus of intermediary spheres and the configurations at entry and exit from the intermediary sphere. (Note that, instead of the vectors $\mathbf { x } _ { i c }$ and $\mathbf { x } _ { o c } ,$ , we show the same vectors scaled by R tan(α).)

Finally, to parameterize the tangent vectors at $\mathbf { X } _ { i c }$ and $\mathbf { X } _ { o c } ,$ we define the unit vectors $\mathbf { x } _ { i c }$ and $\mathbf { x } _ { f c } .$ . These vectors are perpendicular to $\mathbf { X } _ { i c } - \mathbf { r } _ { i }$ and ${ \bf X } _ { o c } - { \bf r } _ { f }$ , as illustrated in Fig. 15, and are derived as follows:

$$
\begin{array}{r l} & {\mathbf {x} _ {i c} = \frac {\frac {\overline {{R}}}{\cos \alpha} \frac {\mathbf {r} _ {f} - \mathbf {r} _ {i}}{\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}} - (\mathbf {X} _ {i c} - \mathbf {r} _ {i})}{\overline {{R}} \tan \alpha},} \\ & {\mathbf {x} _ {o c} = \frac {- \frac {\overline {{R}}}{\cos \alpha} \frac {\mathbf {r} _ {f} - \mathbf {r} _ {i}}{\| \mathbf {r} _ {f} - \mathbf {r} _ {i} \| _ {2}} - (\mathbf {X} _ {o c} - \mathbf {r} _ {f})}{\overline {{R}} \tan \alpha}.} \end{array}
$$

We parameterize the tangent vectors at $\mathbf { X } _ { i c }$ and $\mathbf { X } _ { o c }$ denoted by $\mathbf { T } _ { i c }$ and $\mathbf { T } _ { o c }$ respectively, using the parameters $\phi _ { i c }$ and $\phi _ { o c }$ , as shown below:

$$
\begin{array}{l} \mathbf {T} _ {i c} (\phi_ {i c}) = \cos {(\phi_ {i c})} \mathbf {x} _ {i c} + \sin {(\phi_ {i c})} \frac {\left((\mathbf {X} _ {i c} - \mathbf {r} _ {i}) \times \mathbf {x} _ {i c}\right)}{\overline {{R}}}, \\ \mathbf {T} _ {o c} (\phi_ {o c}) = \cos {(\phi_ {o c})} \mathbf {x} _ {o c} + \sin {(\phi_ {o c})} \frac {\left((\mathbf {X} _ {o c} - \mathbf {r} _ {f}) \times \mathbf {x} _ {o c}\right)}{\overline {{R}}}. \end{array}
$$

We optimize the path length over the parameters $\theta \in [ 0 , 2 \pi )$ $\phi _ { i c } \in [ 0 , 2 \pi )$ , and $\phi _ { o c } \in [ 0 , 2 \pi )$ . For a given set of parameters, we can compute $\mathbf { X } _ { i c } , \ \mathbf { X } _ { o c } , \ \mathbf { T } _ { i c } .$ and $\mathbf { T } _ { o c } .$ . Similar to the methodology in Section IV-C, we generate the optimal path on the initial sphere, intermediary sphere, and the final sphere. Note that motion planning on each of the surfaces depends only on two parameters. For instance, in the case of the intermediary sphere, the path length depends only on $\phi _ { i c }$ and $\phi _ { o c } .$ . Similar to the path construction using an intermediary plane, $\theta _ { d i s c }$ dictates the number of discretizations of θ and $\phi _ { d i s c }$ represents the number of discretizations for $\phi _ { i c }$ and $\phi _ { o c } .$ Finally, among all the combinations of the discretized parameter values, we select the path with the minimal total length.

## VII. SUMMARY OF PATH CONSTRUCTION ALGORITHM

In this section, we summarize the path construction comprising the three classes of paths, presented in Sections IV, V, and VI as a pseudocode in Algorithm 1.

The initial configuration and final configuration, each of which is defined by the four vectors X, T, Y, and U, are the inputs to the algorithm. We compactly represent them by the homogeneous transformation matrices $\mathbf { H } _ { 0 }$ and $\mathbf { H } _ { f } .$ respectively.<sup>21</sup> The other inputs to the algorithm include the pitch rate (captured by $R _ { p i t c h } )$ , yaw rate (captured by $R _ { y a w } )$ and the discretization parameters, $( \theta _ { d i s c }$ and $\phi _ { d i s c } )$ . Recall that $\theta _ { d i s c }$ and $\phi _ { d i s c }$ are the discretization parameters corresponding to the position and the heading, respectively (which were discussed in Sections IV, V, and VI).

In line 1 of the algorithm, the minimum cylinder path is computed, which constructs the shortest path through an intermediary cylindrical envelope (described in Section IV). The function returns the length of the shortest path and the configuration of the vehicle along the path. Similarly, paths through a cross-tangent plane (described in Section V) and through an intermediary sphere (described in Section VI), are constructed in lines 2 and 3, respectively. Finally, the shortest of all the three classes of paths is determined in line 4, and the configuration of the vehicle along the shortest path is returned by the algorithm.

```c
Algorithm 1 Path construction algorithm for 3D Dubins
Input: H₀, H_f, R_pitch, R_yaw, θ_disc, φ_disc
/* Computing the shortest path through cylindrical envelope */
1: l_SCS, H_SCS ← MinimumCylinderPath(H₀, H_f, R_pitch, R_yaw, θ_disc, φ_disc)
/* Computing the shortest path through cross-tangent plane */
2: l_SPS, H_SPS ← MinimumPlanePath(H₀, H_f, R_pitch, R_yaw, θ_disc, φ_disc)
/* Computing the shortest path through intermediary spherical envelope */
3: l_SSS, H_SSS ← MinimumSpherePath(H₀, H_f, R_pitch, R_yaw, θ_disc, φ_disc)
/* Computing the shortest overall path */
4: l*, H* ← MinimumLength (H_SCS, H_SPS, H_SSS)
5: return l*, H*
```

Remark 10. If an existence condition is violated for a candidate path (such as an inner sphere – plane – outer sphere connection), its path length is returned as NaN. The functions MinimumPlanePath and MinimumSpherePath select the shortest path among those with finite length for each path type. Notably, SCS paths always exist. If no valid path exists for a particular connection type $( \mathbf { e . g . } , S P S )$ , the corresponding function (such as MinimumPlanePath) returns NaN. Since the MinimumLength function considers only paths with finite length, any non-existent paths are automatically ignored.

## VIII. RESULTS

In this section, we present computational results to study the performance of Algorithm 1 and the effect of the vehicle’s configuration and the motion constraints on the path. To this end, we consider the scenarios provided in [21], where five $^ { \mathrm { \tiny ~ 6 6 } } \mathrm { L o n g } ^ { \mathrm { \tiny ~ , } }$ and five “Short” instances were considered depending on the distance between the initial and final configurations. The minimum turning radius was chosen to be 40 m in [21], and correspondingly, we consider $R _ { p i t c h } = 4 0 ~ \mathrm { m }$ . In [21], the orientation is defined by only the pitch and heading angles. To describe the complete orientation, we additionally specify the roll angle at the initial and final positions to be one of the values from the set $\{ - 1 5 ^ { \circ } , 0 ^ { \circ } , 1 5 ^ { \circ } \} ^ { \bar { 2 } 2 }$ . To study the effect of the motion constraints, we run the experiments for different values of $R _ { y a w } \in \{ 3 0 \mathrm { m } , 4 0 \mathrm { m } , 5 0 \mathrm { m } \}$

Furthermore, we consider two sets of scenarios referred to as “Additional $1 ^ { \circ }$ and “Additional $2 ^ { \circ }$ described shortly, based on Figs. 2a and 2b, respectively. In the first set of scenarios, the vehicle needs to perform a turn maneuver with a marginal altitude change. The initial location is (120, 40, 20) with initial heading and pitch angles of $9 0 °$ and $- 5 ^ { \circ }$ , and the final location is (300, 40, 15) with heading and pitch angles of $- 9 0 ^ { \circ }$ and $- 5 ^ { \circ }$ . In “Additional $2 ^ { \circ }$ , the vehicle needs to perform an ascent maneuver from an initial location of (120, 40, 20) with initial heading and pitch angles of $9 0 °$ and $- 1 5 ^ { \circ }$ to a final location of (130, 120, 41) with heading and pitch angles of $8 5 ^ { \circ }$ and 20<sup>◦</sup>.<sup>23</sup>

In addition to considering the algorithm from [21], we also use the path construction methodologies described in [13] and [30]; the latter implementation utilizes the model proposed in [18]. The implementation for the former algorithm is available on the GitHub page of the authors (link in [13]). For the algorithm from [13], since only a single turning radius parameter is used, we set $R \ : = \ : R _ { p i t c h } \ : = \ : 4 0 \ : \mathrm { m } . ^ { 2 4 }$ For the implementation in [30], we select the maximum roll rate so that the turning radius matches 40 m (which is our $R _ { p i t c h } ) _ { \ }$ , and retain the default bounds for the maximum flight path angle of ±0.5 radians. We note that the model considered in [30], which implements [18], utilizes the initial and final heading angles, rather than the full heading vector.

For Algorithm 1, to optimize the path length with respect to the parameters, we consider 15 discretizations for all parameters that describe the positions and tangent vectors for entry and exit between the intermediary surfaces. We implemented the algorithms in Python 3.8 on a computer with AMD Ryzen 9 5900HS CPU running at 3.30 GHz with 16 GB RAM. For all the classes of the paths constructed, we parallelized the functions that compute the sub-paths on each individual surface. The computational results of the algorithm are summarized in Table I. <sup>25</sup>

In Table I, we show the length of the path obtained using the three benchmarking algorithms under the instance name. For the implementation in [21], we consider the same parameter values used by the authors, which are a minimum turning radius of 40 m and a bounded pitch angle in $[ - 1 5 ^ { \circ } , 2 0 ^ { \circ } ]$

From this table, we can observe that

• The path lengths obtained from our model are comparable to those from [21], [13], and [30] for all $^ { \mathrm { \tiny ~ 6 6 } } \mathrm { L o n g } ^ { \mathrm { \tiny ~ , } }$ maneuvers. In particular, our path length is shorter for a majority of “Long $2 " ,$ , “Long 3”, “Long $4 ^ { \circ } ,$ , and “Long $5 ^ { \circ }$ instances. The generated paths satisfy both pitch and yaw rate constraints while connecting the initial and final configurations, which include the vehicle’s roll angle.

• For “Short” maneuvers, the length of the paths generated by the proposed algorithm is two to three times shorter than the path obtained from [21], while remaining comparable to the paths from [13] and [30]. On a few of the maneuvers, [30] yields larger path lengths due to constraints on the flight path angle.

• The computation time is around 10 seconds for most of the instances.

These results show the impact of the model and the control inputs on the resulting trajectory. We further expand upon these results to showcase the effect of the motion constraints and the configurations in the following subsections, along with additional examples.

## A. Effect of motion constraints

From Table I, we can observe that increasing $R _ { y a w }$ changes the path length and also the best feasible path type. For instance, consider the “Short $4 ^ { \circ }$ instance with initial and final roll angles of $1 5 ^ { \circ }$ and $- 1 5 ^ { \circ }$ , respectively. The path generated for $R _ { y a w } = 3 0$ m, 40 m, and 50 m is illustrated in Fig. 16. We can observe that increasing $R _ { y a w }$ from 40 m to 50 m changes the path obtained from our algorithm from a cross-tangent connection to a path through the left spheres at the initial and final configurations connected by a cylinder. Additionally, while increasing $R _ { y a w }$ from 30 m to 40 m retains the same path type as the best path, the points of departure and arrival at the initial and final spheres have changed significantly. This is because $R _ { y a w }$ particularly affects the turning capability of the vehicle on the cross-tangent plane, as can be observed from Figs. 16a and 16b.

For an instance of the “Short $4 ^ { \dag }$ case where the path length is around 400 m, the change in path length is around 50 to 70 m when $R _ { y a w }$ is varied. The effect of $R _ { y a w }$ is more pronounced for “Additional $2 ^ { \circ }$ , where the vehicle needs to perform an ascent motion. For this instance, the path length may vary from 100 m to as high as 280 m depending on $R _ { y a w } .$ An illustration of the paths for increasing $R _ { y a w }$ from 30 m to 50 m is shown in Fig. 17.

These effects may not be captured by the existing models, including [21], [13], and [30], due to the single control input considered in these models. Illustrations of the paths obtained using the results from [21], [13], and [30] for the scenarios “Short $4 ^ { \circ }$ and “Additional $2 ^ { \circ }$ are shown in Figs. 18 and 19, respectively. We note that the path obtained from [30] utilizes a helical segment followed by a left turn, straight line segment, and another left turn to construct the path for “Short $4 ^ { \dag }$ in Fig. 18. Additionally, since the full heading vector is not considered in [30], it yields a starkly different path, which enters the pitch sphere and hence violates the pitch rate constraint, unlike the other two algorithms for “Additional 2”.

## B. Effect of considering complete configuration

From Table I, we can observe that the roll angle at the initial and final locations impacts the path length and the path type as well. For instance, consider “Long $1 ^ { \circ }$ with $R _ { y a w } = 4 0 \mathrm { ~ m ~ }$ . We illustrate the change in the path type with changing roll angles across the three subfigures in Fig. 20. We observe that for initial and final roll angles of $- 1 5 ^ { \circ }$ and $0 ^ { \circ }$ , the vehicle travels on the outer sphere, followed by traveling on the cross-tangent plane and an inner sphere. However, changing the initial and final roll angles changes the minimum cost path from our algorithm to travel along a cylindrical envelope connecting the left spheres for initial and final roll angles of $0 ^ { \circ }$ and $1 5 ^ { \circ }$ . For initial and final roll angles of $1 5 ^ { \circ }$ and $- 1 5 ^ { \circ }$ , the best feasible path is a cylindrical envelope connecting inner spheres.

In contrast, the paths obtained from [21], [13], and [30] are shown in Fig. 21. All three algorithms will produce the same path for any values of $R _ { y a w }$ and for any of the three combinations of initial and final roll angles we considered in this subsection. This is due to the fact that the generated path does not account for the complete orientation of the vehicle at the initial and final locations; this highlights the novelty of our approach considering the full orientation of the vehicle.

We also note here that all the paths satisfy the pitch and yaw rate constraints close to the initial configuration when $R _ { y a w } =$ 40 m. However, the paths from [21] and [30] violate the yaw rate constraints at the initial configuration for $R _ { y a w } = 5 0$ m, while the path from [13] violates for $R _ { y a w } = 5 3$ m, since they enter the left sphere (similar to Fig. 2a). These results reaffirm the importance of the model and control inputs presented in the current paper.

## C. Additional examples

In addition to the previous instances, we consider two additional instances. First, we consider an instance where the final location is inside the “inner” sphere of the vehicle, i.e., one of the pitch spheres. In this instance, the vehicle needs to depart from the origin with a heading, pitch, and yaw angle of $3 0 ^ { \circ } , 1 0 ^ { \circ }$ , and $1 5 ^ { \circ }$ , respectively. The desired final location is (5, 10, 15) with a desired heading, pitch, and yaw angle of 190<sup>◦</sup>, 10<sup>◦</sup>, and $- 1 5 ^ { \circ }$ , respectively. Furthermore, we chose $R _ { p i t c h }$ and $R _ { y a w }$ to be 40 m and 50 m, respectively. The minimum cost path obtained using Algorithm 1 and from the three benchmarking algorithms are shown in Figs. 22a and 22b, respectively. From our algorithm, the vehicle leverages the pitch and yaw rate bounds to make a sharper turn, leading to a path with a length of 253.36 m, which traverses through an intermediary sphere. On the other hand, due to the pitch angle bounds in [21], the vehicle takes a longer path of length 290.57 m. The algorithm [30] provides a comparable path length of 289.23 m, whereas [13] provides a much longer path with a length of 419.03 m.

TABLE I  
SUMMARY OF BEST FEASIBLE PATH AND COMPUTATION TIME FOR DIFFERENT INSTANCES WITH VARYING INITIAL ROLL ANGLE, FINAL ROLL ANGLE, AND $R _ { y a w } .$ . PATH LENGTH OBTAINED USING ALGORITHMS FROM [21], [13], AND [30] ARE SHOWN UNDER THE INSTANCE NAME. IN THE TABLE, S DENOTES A SPHERE, C DENOTES A CYLINDER, AND P DENOTES A PLANE. FOR SPHERES, SUBSCRIPTS $i , o , l ,$ AND r REPRESENT THE INNER SPHERE, OUTER SPHERE, LEFT SPHERE, AND RIGHT SPHERE, RESPECTIVELY.

<table><tr><td>Inst.</td><td>Roll*(°,°)</td><td> $R_{yaw}$ (m)</td><td>Length(m)</td><td>Path type</td><td>Time(s)</td></tr><tr><td rowspan="9">Long 1446.04 [21]437.86 [13]445.10 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>478.06</td><td> $S_rPS_l$ </td><td>9.91</td></tr><tr><td>40</td><td>510.64</td><td rowspan="2"> $S_oPS_i$ </td><td>9.60</td></tr><tr><td>50</td><td>533.24</td><td>9.77</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>475.98</td><td> $S_rPS_l$ </td><td>9.87</td></tr><tr><td>40</td><td>412.17</td><td> $S_lCS_l$ </td><td>10.17</td></tr><tr><td>50</td><td>545.09</td><td> $S_rPS_l$ </td><td>10.46</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>447.36</td><td rowspan="3"> $S_iCS_i$ </td><td>9.68</td></tr><tr><td>40</td><td>470.08</td><td>9.53</td></tr><tr><td>50</td><td>473.59</td><td>9.87</td></tr><tr><td rowspan="9">Long 2638.45 [21]631.73 [13]637.22 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>587.86</td><td rowspan="9"> $S_rCS_r$ </td><td>9.72</td></tr><tr><td>40</td><td>606.64</td><td>9.66</td></tr><tr><td>50</td><td>614.57</td><td>9.90</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>590.12</td><td>12.03</td></tr><tr><td>40</td><td>601.87</td><td>10.29</td></tr><tr><td>50</td><td>620.67</td><td>10.87</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>583.47</td><td>10.18</td></tr><tr><td>40</td><td>603.90</td><td>10.29</td></tr><tr><td>50</td><td>612.32</td><td>10.83</td></tr><tr><td rowspan="9">Long 31068.34 [21]1059.20 [13]1054.19 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>1032.72</td><td rowspan="2"> $S_iCS_i$ </td><td>10.97</td></tr><tr><td>40</td><td>1141.58</td><td>10.90</td></tr><tr><td>50</td><td>1161.82</td><td> $S_lCS_l$ </td><td>11.23</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>1026.87</td><td rowspan="6"> $S_iCS_i$ </td><td>11.30</td></tr><tr><td>40</td><td>1045.90</td><td>11.14</td></tr><tr><td>50</td><td>1048.38</td><td>11.30</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>1037.06</td><td>11.06</td></tr><tr><td>40</td><td>1040.40</td><td>10.91</td></tr><tr><td>50</td><td>1058.79</td><td>12.67</td></tr><tr><td rowspan="9">Long 41788.80 [21]1784.85 [13]1787.15 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>1744.87</td><td rowspan="9"> $S_lCS_l$ </td><td>11.52</td></tr><tr><td>40</td><td>1758.23</td><td>12.05</td></tr><tr><td>50</td><td>1773.09</td><td>11.29</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>1747.76</td><td>10.65</td></tr><tr><td>40</td><td>1759.44</td><td>10.60</td></tr><tr><td>50</td><td>1776.86</td><td>10.65</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>1744.13</td><td>10.87</td></tr><tr><td>40</td><td>1763.51</td><td>10.86</td></tr><tr><td>50</td><td>1768.64</td><td>10.61</td></tr><tr><td rowspan="9">Long 52214.54 [21]2213.70 [13]2208.70 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>2187.58</td><td rowspan="9"> $S_rCS_r$ </td><td>10.91</td></tr><tr><td>40</td><td>2201.98</td><td>10.79</td></tr><tr><td>50</td><td>2211.11</td><td>11.00</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>2189.22</td><td>11.17</td></tr><tr><td>40</td><td>2201.75</td><td>10.79</td></tr><tr><td>50</td><td>2212.44</td><td>11.14</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>2192.96</td><td>10.86</td></tr><tr><td>40</td><td>2209.89</td><td>10.59</td></tr><tr><td>50</td><td>2225.56</td><td>11.04</td></tr><tr><td rowspan="9">Short 1580.79 [21]299.34 [13]312.87 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>289.67</td><td> $S_rCS_r$ </td><td>9.75</td></tr><tr><td>40</td><td>376.88</td><td rowspan="2"> $S_oCS_o$ </td><td>9.47</td></tr><tr><td>50</td><td>394.71</td><td>9.72</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>355.38</td><td> $S_oPS_i$ </td><td>9.58</td></tr><tr><td>40</td><td>375.31</td><td rowspan="2"> $S_rCS_r$ </td><td>9.54</td></tr><tr><td>50</td><td>389.47</td><td>9.54</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>352.59</td><td> $S_oCS_o$ </td><td>9.58</td></tr><tr><td>40</td><td>380.83</td><td> $S_rCS_r$ </td><td>9.44</td></tr><tr><td>50</td><td>360.12</td><td> $S_rS_lS_r$ </td><td>10.18</td></tr></table>

∗ – Initial and final roll angles are specified as an ordered pair.

A similar result was obtained in the second instance, where the final location was chosen inside the right sphere (one of the yaw spheres). The initial configuration and vehicle parameters were chosen to be the same as the first instance, the final location is chosen to be (0, −30, 5), and the desired final heading, pitch, and roll angles are 190<sup>◦</sup>, 10<sup>◦</sup>, and −15<sup>◦</sup>, respectively. The path length from our algorithm was 257.27 m, whereas the path length with the algorithms from [21], [13], and [30] were 293.03 m, 391.13 m, and 290.63 m, respectively.

<table><tr><td>Inst.</td><td>Roll*(°,°)</td><td> $R_{yaw}$ (m)</td><td>Length(m)</td><td>Path type</td><td>Time(s)</td></tr><tr><td rowspan="9">Short 2668.17 [21]281.96 [13]506.05 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>302.02</td><td rowspan="9"> $S_oPS_i$ </td><td>9.54</td></tr><tr><td>40</td><td>323.47</td><td>9.34</td></tr><tr><td>50</td><td>356.72</td><td>9.50</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>298.45</td><td>9.59</td></tr><tr><td>40</td><td>313.69</td><td>9.33</td></tr><tr><td>50</td><td>335.89</td><td>9.51</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>313.70</td><td>9.44</td></tr><tr><td>40</td><td>336.86</td><td>9.79</td></tr><tr><td>50</td><td>349.95</td><td>10.14</td></tr><tr><td rowspan="9">Short 3976.79 [21]342.52 [13]521.46 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>364.92</td><td rowspan="7"> $S_oPS_i$ </td><td>9.83</td></tr><tr><td>40</td><td>386.80</td><td>9.37</td></tr><tr><td>50</td><td>400.55</td><td>9.62</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>356.75</td><td>9.49</td></tr><tr><td>40</td><td>368.52</td><td>9.37</td></tr><tr><td>50</td><td>384.82</td><td>10.03</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>349.90</td><td>10.84</td></tr><tr><td>40</td><td>416.92</td><td rowspan="2"> $S_rCS_r$ </td><td>10.29</td></tr><tr><td>50</td><td>408.28</td><td>9.79</td></tr><tr><td rowspan="9">Short 41169.80 [21]422.26 [13]625.75 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>425.17</td><td rowspan="6"> $S_lCS_l$ </td><td>9.77</td></tr><tr><td>40</td><td>425.65</td><td>9.53</td></tr><tr><td>50</td><td>421.25</td><td>9.75</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>420.89</td><td>9.94</td></tr><tr><td>40</td><td>422.72</td><td>9.47</td></tr><tr><td>50</td><td>447.19</td><td>9.68</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>445.42</td><td rowspan="2"> $S_oPS_i$ </td><td>9.62</td></tr><tr><td>40</td><td>493.81</td><td>9.55</td></tr><tr><td>50</td><td>512.31</td><td> $S_lCS_l$ </td><td>9.84</td></tr><tr><td rowspan="9">Short 51362.91 [21]437.46 [13]730.04 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>444.24</td><td rowspan="5"> $S_oPS_i$ </td><td>9.62</td></tr><tr><td>40</td><td>463.42</td><td>9.53</td></tr><tr><td>50</td><td>477.80</td><td>9.66</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>440.33</td><td>9.60</td></tr><tr><td>40</td><td>446.09</td><td>9.33</td></tr><tr><td>50</td><td>520.75</td><td> $S_lCS_l$ </td><td>9.77</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>453.28</td><td rowspan="3"> $S_rCS_r$ </td><td>9.66</td></tr><tr><td>40</td><td>447.54</td><td>9.52</td></tr><tr><td>50</td><td>467.20</td><td>9.88</td></tr><tr><td rowspan="9">Add. 1225.89 [21]225.67 [13]225.72 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>212.63</td><td rowspan="9"> $S_rCS_r$ </td><td>9.43</td></tr><tr><td>40</td><td>223.18</td><td>9.83</td></tr><tr><td>50</td><td>233.88</td><td>10.26</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>213.34</td><td>9.58</td></tr><tr><td>40</td><td>223.83</td><td>10.00</td></tr><tr><td>50</td><td>234.02</td><td>10.11</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>211.93</td><td>9.48</td></tr><tr><td>40</td><td>222.00</td><td>9.85</td></tr><tr><td>50</td><td>232.53</td><td>10.10</td></tr><tr><td rowspan="9">Add. 284.55 [21]84.54 [13]83.33 [30]</td><td rowspan="3">(-15,0)</td><td>30</td><td>107.59</td><td rowspan="2"> $S_lS_rS_l$ </td><td>11.86</td></tr><tr><td>40</td><td>91.54</td><td>11.63</td></tr><tr><td>50</td><td>274.51</td><td> $S_iCS_i$ </td><td>11.95</td></tr><tr><td rowspan="3">(0,15)</td><td>30</td><td>87.17</td><td> $S_iS_oS_i$ </td><td>12.00</td></tr><tr><td>40</td><td>250.06</td><td> $S_rS_lS_r$ </td><td>11.52</td></tr><tr><td>50</td><td>280.35</td><td> $S_iCS_i$ </td><td>12.07</td></tr><tr><td rowspan="3">(15,-15)</td><td>30</td><td>95.39</td><td> $S_rS_lS_r$ </td><td>11.82</td></tr><tr><td>40</td><td>259.63</td><td> $S_iCS_i$ </td><td>11.61</td></tr><tr><td>50</td><td>280.38</td><td> $S_iPS_o$ </td><td>12.13</td></tr></table>

![](Kumar2025Novel_figs/1812b224bc55e8880c7d6e783793bb58fe44fa7b0a43f6b40df63712a48fbd88.jpg)

![](Kumar2025Novel_figs/2021dc656b0023057b572f1309e05e803c9a91043c621ec72a6a0af71a63f6a9.jpg)

![](Kumar2025Novel_figs/78b2599d66f154b8e8fb4c95454a10877d54b4284370d852e0b71b21c376ab78.jpg)  
(a) $R _ { y a w } = 3 0 ~ \mathsf { m }$ (path through inter- (b) $R _ { y a w } = 4 0 $ m (path through inter- (c) $R _ { y a w } = 5 0 ~ \mathsf { m }$ (path through intermediary cross-tangent plane) mediary cross-tangent plane) mediary cylindrical envelope)

Fig. 16. Depiction of varying paths with $R _ { y a w }$ for “Short $4 ^ { \dag }$ with initial roll angle of $1 5 ^ { \circ }$ and final roll angle of − $\boldsymbol { \cdot } 1 5 ^ { \circ }$ and instantaneous configuration of the vehicle. Animations of a vehicle moving along these paths are available on our GitHub page.  
![](Kumar2025Novel_figs/0b967f1cdbc9ee26c54aa03a4821a911905c5617fd230349ff53daebde90576e.jpg)  
(a) $R _ { y a w } = 3 0$ m (path through intermediary sphere envelope)

![](Kumar2025Novel_figs/a8249c75f6fd114513bd21ceaaa1a6a4342963eae4de48fee262c6ebedd22adc.jpg)  
(b) $R _ { y a w } = 4 0 \mathsf { n }$ (path through intermediary cylindrical envelope)

![](Kumar2025Novel_figs/ff468e7813d3425f47b4596bb17ee109a56baa2b608ad8e735b36e540161efd7.jpg)  
(c) $R _ { y a w } = 5 0 \mathrm { m }$ (path through intermediary cross-tangent plane)  
Fig. 17. Depiction of varying paths with $R _ { y a w }$ for “Additional $2 ^ { \ast }$ with initial roll angle of $1 5 ^ { \circ }$ and final roll angle o $\mathrm { \Delta - 1 5 ^ { \circ } }$ and instantaneous configuration of the vehicle. Animations of a vehicle moving along these paths are available on our GitHub page.

Remark 11. We identified two key issues with state-of-the-art methods: (i) the generated path does not change with changing roll angle, and (ii) the use of a single turning radius constraint can lead to violations of one of the curvature constraints in our model. While we have illustrated these issues with a few examples, they are expected to persist across a broader range of scenarios.

## D. Impact of discretization of parameters

Noting that the number of discretizations of the path parameters can be freely chosen, we performed a sensitivity study by varying them across 5, 10, 15, 20, and 25 values. For each setting, we obtained the best path using our algorithm for all instances and variations in $R _ { y a w }$ and initial and final roll angles, as outlined in Table I. The results are summarized in Fig. 24, which shows both the change in shortest path lengths and the computation times across the 12 considered instances. For each instance, the nine variations $( R _ { \mathrm { y a w } }$ , initial, and final roll angles) are condensed into a box plot.

From these figures, we observe that a smaller number of discretizations yields faster computation time, but typically at the expense of solution quality. This trend is consistent across all instances, and is especially apparent in “Additional 2.” From Fig. 24, 15 discretizations represent a good tradeoff between computation time and path length. Alternatively, using 10 discretizations provides solutions in approximately 5 seconds, compared to 10 seconds for 15 discretizations, albeit with some compromise in path quality.

## IX. CONCLUSION

In this paper, we propose a novel model for 3D motion planning and a methodology for generating high-quality feasible trajectories. The proposed model and the approach address two key limitations of the existing methods: the incomplete representation of vehicle configuration, and inadequate modeling of the motion constraints. We highlight these issues using illustrative examples. To address these, we proposed a model using a rotation-minimizing frame to uniquely represent the vehicle’s configuration, and the model includes two control inputs corresponding to the pitch rate and yaw rate of the vehicle. We proved that the pitch rate and yaw rate bounds yield a total of four distinct spheres tangential to the vehicle’s configuration, viz. inner, outer, left and right, which represent temporarily inaccessible regions.

![](Kumar2025Novel_figs/fc9c82c9f5638a83cb083eee06dc18483083503aac091877dbbfd2845f8c1d45.jpg)

Fig. 18. Solutions from [21], [13], and [30] for “Short 4”  
![](Kumar2025Novel_figs/b86a30cd2b4a04e12464e2bebade38561a58e13b65deee58364a3c1b7c5a17bd.jpg)  
Fig. 19. Solutions from [21], [13], and [30] for “Additional 2”

We proposed three classes of curvature-constrained paths beginning and ending on the surface of the spheres, tangential to the initial and final configurations. The three classes differ in the transition mechanism from the initial to the final sphere. These transitions involve a path on the surface of a cylindrical envelope, a cross-tangent plane, or another spherical surface.

Finally, we presented extensive computational experiments to evaluate the impact of the motion constraints and the vehicle’s configuration on the path length and the path classification. Additionally, a comparison of the proposed methodology with the algorithms in [21], [13], and [30] underscored the advantages of modeling with complete orientation. The proposed model and path generation methodology offer a novel perspective on the 3D motion planning problem.

## REFERENCES

[1] Fixed Wing Drone: The Complete Guide for Professionals (Accessed Apr 2025). [Online]. Available: https://quantum-systems.com/blog/2025/02/05/fixed-wing-drone-guide/ #:<sup>∼</sup>:text=Superior%20Range%20%26%20Coverage%3A%20The% 20design,to%20survey%20extensive%20landscapes%20quickly.

[2] What Is A Fixed Wing Drone? — Advantages And Uses Of Fixed Wing Drones (Accessed Apr 2025). [Online]. Available: https://uavsystemsinternational.com/blogs/drone-guides/ what-is-a-fixed-wing-drone-advantages-and-uses-of-fixed-wing-drones? srsltid=AfmBOorCTIkSZHuUP3N4YbgcjBHHJoqQUL wTsxMGUmw4nzJpJ1lvfb

[3] L. E. Dubins, “On curves of minimal length with a constraint on average curvature, and with prescribed initial and terminal positions and tangents,” American Journal of Mathematics, vol. 79, 1957.

[4] L. S. Pontryagin, V. G. Boltyanskii, R. V. Gamkrelidze, and E. F. Mishchenko, The mathematical theory of optimal processes. Interscience Publishers, 1962.

[5] X.-N. Bui, J.-D. Boissonnat, P. Soueres, and J.-P. Laumond, “Shortest path synthesis for dubins non-holonomic robot,” in Proceedings of the 1994 IEEE International Conference on Robotics and Automation, 1994, pp. 2–7.

[6] E. Bakolas and P. Tsiotras, “The asymmetric sinistral/dextral markovdubins problem,” in Proceedings of the 48h IEEE Conference on Decision and Control (CDC), 2009, pp. 5649–5654.

[7] Y. Wang and Y. R. Zheng, “3-dimensional path planning for autonomous underwater vehicle,” in OCEANS 2018 MTS/IEEE Charleston, 2018, pp. 1–6.

[8] H. Marino, M. Bonizzato, R. Bartalucci, P. Salaris, and L. Pallottino, “Motion planning for two 3D-Dubins vehicles with distance constraint,” in 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, 2012, pp. 4702–4707.

[9] G. Ambrosino, M. Ariola, U. Ciniglio, F. Corraro, E. De Lellis, and A. Pironti, “Path generation and tracking in 3-d for uavs,” IEEE Transactions on Control Systems Technology, vol. 17, no. 4, pp. 980– 988, 2009.

[10] R. Hurley, R. Lind, and J. Kehoe, “A mixed local-global solution to motion planning within 3-d environments,” in AIAA Guidance, Navigation, and Control Conference, 2009. [Online]. Available: https://arc.aiaa.org/doi/abs/10.2514/6.2009-6297

[11] Y. Lin and S. Saripalli, “Path planning using 3D Dubins curve for unmanned aerial vehicles,” in 2014 International Conference on Unmanned Aircraft Systems (ICUAS), 2014, pp. 296–304.

[12] H. Sussmann, “Shortest 3-dimensional paths with a prescribed curvature bound,” in IEEE Conference on Decision and Control, 1995, pp. 3306– 3312.

[13] V. M. Baez, N. Navkar, and A. T. Becker, “An analytic solution to the 3D csc Dubins path problem,” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 7157–7163.

[14] S. Hota and D. Ghose, “Optimal geometrical path in 3D with curvature constraint,” in 2010 IEEE/RSJ International Conference on Intelligent Robots and Systems, 2010, pp. 113–118.

[15] S. Hota and D. Ghose, “Optimal path planning for an aerial vehicle in 3D space,” in 49th IEEE Conference on Decision and Control (CDC), 2010, pp. 4902–4907.

[16] L. Xu, Y. Baryshnikov, and C. Sung, “Reparametrization of 3D csc Dubins paths enabling 2d search,” in Algorithmic Foundations of Robotics XVI, 2024.

[17] H. Chitsaz and S. M. LaValle, “Time-optimal paths for a Dubins airplane,” in 2007 46th IEEE Conference on Decision and Control, 2007, pp. 2379–2384.

[18] M. Owen, R. W. Beard, and T. W. McLain, Implementing Dubins Airplane Paths on Fixed-Wing UAVs\*. Dordrecht: Springer Netherlands, 2015, pp. 1677–1701. [Online]. Available: https://doi.org/ 10.1007/978-90-481-9707-1 120

![](Kumar2025Novel_figs/5c1de22509b256de1a065371a878415b9ae78ee7a8ab21e3119a5fab03c632a2.jpg)

![](Kumar2025Novel_figs/bffd8930eaa9d5f3ca432d0941006df1d30474a422df4f76242e39a469a87652.jpg)

![](Kumar2025Novel_figs/ecfd52d1a942c36ba6ff21bf25bf9442aaa575bcc5c0cc1871e47dde9046a03c.jpg)  
(a) Initial roll $= \ - 1 5 ^ { \circ }$ , final roll $= ~ 0 ^ { \circ }$ (b) Initial $\mathsf { r o l l } = 0 ^ { \circ }$ , final roll $= 1 5 ^ { \circ }$ (path (c) Initial roll $= 1 5 ^ { \circ }$ , final roll $- 1 5 ^ { \circ }$ (path (path through cross-tangent plane) through cylindrical envelope) through cylindrical envelope)

Fig. 20. Depiction of varying paths with initial and final roll angles for “Long 1” with $R _ { y a w } = 4 0$ m and instantaneous configuration of the vehicle. Animations of a vehicle moving along these paths are available on our GitHub page.

![](Kumar2025Novel_figs/54a5b8704bf3925e53c81d5287099f5f24a52c154e6205205d422c75b5502b96.jpg)  
Fig. 21. Feasible path from [21], [13], and [30] for “Long 1”

[19] R. W. Beard and T. W. McLain, Small Unmanned Aircraft: Theory and Practice. Princeton University Press, 2012.

[20] V. M. Goncalves, L. C. A. Pimenta, C. A. Maia, B. C. O. Dutra, and G. A. S. Pereira, “Vector fields for robot navigation along time-varying curves in n -dimensions,” IEEE Transactions on Robotics, vol. 26, no. 4, pp. 647–659, 2010.

[21] P. Va´na, A. Alves Neto, J. Faigl, and D. G. Macharet, “Minimal 3Dˇ Dubins path with bounded curvature and pitch angle,” in 2020 IEEE International Conference on Robotics and Automation (ICRA), 2020, pp. 8497–8503.

[22] J. Herynek, P. Va´na, and J. Faigl, “Finding 3D Dubins paths withˇ pitch angle constraint using non-linear optimization,” in 2021 European Conference on Mobile Robots (ECMR), 2021, pp. 1–6.

[23] W. Wang and P. Li, “Towards finding the shortest-paths for 3D rigid bodies,” in Robotics: Science and Systems 2021, 2021.

[24] D. P. Kumar, S. Darbha, S. G. Manyam, and D. W. Casbeer, “A new approach to motion planning in 3d for a dubins vehicle: Special case on a sphere,” IEEE Transactions on Robotics, pp. 1–18, 2026.

[25] R. L. Bishop, “There is more than one way to frame a curve,” The American Mathematical Monthly, vol. 82, no. 3, pp. 246–251, 1975.

[26] S. Darbha, A. Pavan, R. Kumbakonam, S. Rathinam, D. W. Casbeer,

and S. G. Manyam, “Optimal geodesic curvature constrained dubins’ paths on a sphere,” Journal of Optimization Theory and Applications, vol. 197, pp. 966–992, 2023.

[27] D. P. Kumar, S. Darbha, S. G. Manyam, and D. Casbeer, “Generation of paths for motion planning for a dubins vehicle on sphere,” 2025. [Online]. Available: https://arxiv.org/abs/2504.11832

[28] D. J. Struik, Lectures on Classical Differential Geometry, 2nd ed. Dover, 1988, ch. 4.

[29] A. M. Shkel and V. Lumelsky, “Classification of the dubins set,” Robotics and Autonomous Systems, vol. 34, pp. 179–202, 2001.

[30] MathWorks, “uavDubinsConnection: Dubins path connection for UAV,” 2019, MATLAB Documentation (accessed March 1, 2026). [Online]. Available: https://www.mathworks.com/help/uav/ref/ uavdubinsconnection.connect.html

[31] M. P. D. Carmo, Differential Geometry of Curves & Surfaces, 2nd ed. Dover, 2016, ch. 3.

## APPENDIX

## A. Construction of segments

Consider an interval $\begin{array} { r l r } { s } & { { } \in } & { \left[ s _ { 0 } , s _ { 1 } \right] } \end{array}$ in which $\kappa _ { g }$ and $\kappa _ { n }$ are constants. In this case, noting that $\begin{array} { r l } { \mathbf { R } ( s ) } & { { } : = } \end{array}$ $\begin{array} { r l r } { \lceil \mathbf { T } ( s ) } & { { } \mathbf { Y } ( s ) } & { \mathbf { U } ( s ) \rceil } \end{array}$ is a rotation matrix, (3), (4), and (5) can be rewritten as

$$
\mathbf {R} ^ {\prime} (s) = \mathbf {R} (s) \underbrace {\left( \begin{array}{c c c} 0 & - \kappa_ {g} & - \kappa_ {n} \\ \kappa_ {g} & 0 & 0 \\ \kappa_ {n} & 0 & 0 \end{array} \right)} _ {\Omega}.\tag{23}
$$

Suppose at least one of $\kappa _ { g }$ and $\kappa _ { n }$ is non-zero. The solution for the above differential equation is given by $\begin{array} { r l } { \mathbf { R } ( s ) } & { { } = } \end{array}$ $\mathbf { R } ( s _ { 0 } ) e ^ { \Omega ( s - s _ { 0 } ) }$ , where the expression for the exponential of the skew-symmetric matrix can be obtained using the Euler-Rodriguez formula. Furthermore, using the obtained expression for $\mathbf { T } ( s )$ , the solution for $\mathbf { X } ( s )$ can be obtained by integrating $\mathbf { X } ^ { \prime } ( s )$ from (2). Hence, the solution for the evolution of the four vectors can be written as

![](Kumar2025Novel_figs/366c7fb02ca6752fc6d78c39a6b1d9d8355f530ff0e0349396ba65b7569702e3.jpg)  
(a) Best path for final location inside pitch sphere from Algorithm 1 (best feasible path is left sphere – right sphere – left sphere). Animation of a vehicle moving along this path is available on our GitHub page.

![](Kumar2025Novel_figs/89fee2907030ef15f4b999b2ad3902cdc7bc49c6fd9a49f8f0712e4ed8e3b447.jpg)  
(b) Best path for same configuration using algorithms from [21], [13], and [30]  
Fig. 22. Depiction of path for final location lying inside pitch sphere (specifications given in Section VIII-C)

$$
\left[ \begin{array}{c c} \mathbf {R} (\phi) & \mathbf {X} (\phi) \\ \mathbf {0} _ {3 \times 1} & 1 \end{array} \right] = \left[ \begin{array}{c c} \mathbf {R} (0) & \mathbf {X} (0) \\ \mathbf {0} _ {3 \times 1} & 1 \end{array} \right] \mathbf {H} (\phi).\tag{24}
$$

Here, $\phi : = ( s - s _ { 0 } ) \sqrt { \kappa _ { n } ^ { 2 } + \kappa _ { g } ^ { 2 } }$ and denotes the arc angle of the considered segment, and H(ϕ) is given by

$$
\mathbf {H} = \left( \begin{array}{c c c c} c \phi & \frac {- \kappa_ {g} s \phi}{K} & \frac {- \kappa_ {n} s \phi}{K} & \frac {s \phi}{K} \\ \frac {\kappa_ {g} s \phi}{K} & \frac {\kappa_ {n} ^ {2} + c \phi \kappa_ {g} ^ {2}}{K ^ {2}} & \frac {- \kappa_ {g} \kappa_ {n} (1 - c \phi)}{K ^ {2}} & \frac {\kappa_ {g} (1 - c \phi)}{K ^ {2}} \\ \frac {\kappa_ {n} s \phi}{K} & \frac {- \kappa_ {g} \kappa_ {n} (1 - c \phi)}{K ^ {2}} & \frac {\kappa_ {g} ^ {2} + \kappa_ {n} ^ {2} c \phi}{K ^ {2}} & \frac {\kappa_ {n} (1 - c \phi)}{K ^ {2}} \\ 0 & 0 & 0 & 1 \end{array} \right),\tag{25}
$$

where $K : = \sqrt { \kappa _ { n } ^ { 2 } + \kappa _ { g } ^ { 2 } }$ and $c \phi : = \cos \phi , s \phi : = \sin \phi$ . We can observe that the solution is periodic with a period of 2π.

In the case of $\kappa _ { g } = \kappa _ { n } = 0 , \mathbf { T } , \mathbf { Y }$ , and U remain constant (from (2)); furthermore, $\mathbf { X } ( s ) = \mathbf { X } ( 0 ) + s \mathbf { T } ( 0 )$ is obtained.

![](Kumar2025Novel_figs/244360a1b7259ff7445b6b8f5e4550a13805bb776efcffdef344431bf2dd1c33.jpg)  
(a) Best path for final location inside yaw sphere from Algorithm 1 (best feasible path is right sphere – left sphere – right sphere). Animation of a vehicle moving along this path is available on our GitHub page.

![](Kumar2025Novel_figs/37f7e8f307d62e6196b2e591669f95361ddf0f794ee2e18793fbef4e13c97db4.jpg)  
(b) Best path for same configuration using algorithms from [21], [13], and [30]  
Fig. 23. Depiction of path for final location lying inside yaw sphere (specifications given in Section VIII-C)

## B. Proof for Lemma 1

Without loss of generality, consider the initial rotation matrix R(0) to be the identity matrix and the initial location $\mathbf { X } ( 0 )$ to coincide with the origin. Hence, using the closed-form expressions in Appendix A, the position is given by

$$
\mathbf {X} (\phi) = \left( \begin{array}{c c c} \frac {s \phi}{K} & \frac {\kappa_ {g} (1 - c \phi)}{K ^ {2}} & \frac {\kappa_ {n} (1 - c \phi)}{K ^ {2}} \end{array} \right) ^ {T},\tag{26}
$$

where $K = \sqrt { \kappa _ { n } ^ { 2 } + \kappa _ { g } ^ { 2 } } .$ . Consider $\begin{array} { r } { \kappa _ { n } ~ = ~ \frac { 1 } { R _ { p i t c h } } } \end{array}$ . We claim that the obtained position $\mathbf { X } ( \phi )$ lies on a sphere centered at $( 0 , 0 , R _ { p i t c h } ) ^ { T }$ , which is along U, with radius $R _ { p i t c h }$ . To this end, we can show that $\| \mathbf { X } ( \phi ) - ( 0 , 0 , R _ { p i t c h } ) ^ { T } \| _ { 2 } ^ { 2 } = R _ { p i t c h } ^ { 2 }$ , for all $\begin{array} { r } { \kappa _ { g } \in \left[ - \frac { 1 } { R _ { y a w } } , \frac { 1 } { R _ { y a w } } \right] } \end{array}$ . Hence, all segments corresponding to $\kappa _ { n } = \sum _ { \textit { R } _ { p i t c h } }$ lie on a sphere centered at $( 0 , 0 , R _ { p i t c h } ) ^ { T }$ with radius $R _ { p i t c h }$ . A similar argument can be made for $\begin{array} { r } { \kappa _ { n } = - \frac { 1 } { R _ { p i t c h } } . } \end{array}$ , where all segments lie on a sphere centered at $( 0 , 0 , - \overset { \vartriangle } { R _ { p i t c h } } ) ^ { T }$ with radius of $R _ { p i t c h }$ . Therefore, we can observe that $\kappa _ { n }$ controls the pitch motion of the vehicle; furthermore, $\begin{array} { r } { \kappa _ { n } = \pm \frac { 1 } { R _ { p i t c h } } } \end{array}$ yield maximum ascent or descent motion for the vehicle.

![](Kumar2025Novel_figs/64394406c078b88288ba2b117e1a889835e5035480c9cdebbdf5e42eba78537b.jpg)  
(a) Percentage change in shortest path’s length

![](Kumar2025Novel_figs/1eede5286ece6f26067113cd7de171be0f90c7bfed8d143e1f13c5eccb02a7af.jpg)  
(b) Varying computation time of Algorithm 1 (discretizations shown with a colored marker as well)  
Fig. 24. Impact of varying the discretization of parameters on path length and computation time for each instance (shown with a box plot)

The radius of a segment corresponding to when $\kappa _ { g }$ is constant in $\begin{array} { r } { \left\lceil - \frac { 1 } { R _ { y a w } } , \frac { 1 } { R _ { y a w } } \right\rceil } \end{array}$ can be obtained using the expression for $\mathbf { X } ( \phi )$ as $\begin{array} { r } { { \frac { 1 } { 2 } } \| \mathbf { X } ( \pi ) - \mathbf { \bar { X } } ( 0 ) \| _ { 2 } } \end{array}$ . Using the expression for $\mathbf { X } ( \phi )$ given in (26), it follows that $\begin{array} { r } { \frac { 1 } { 2 } \| \mathbf { X } ( \pi ) - \mathbf { X } ( 0 ) \| _ { 2 } = \frac { 1 } { \sqrt { \kappa _ { g } ^ { 2 } + \frac { 1 } { R _ { p i t c h } ^ { 2 } } } } } \end{array}$

C. Sabban frame equations for sphere with radius $\overline { { R } }$ and path obtained in 3D

The evolution equations for the Sabban frame on a unit sphere, described in Section IV-C, can be generalized to a sphere with radius R. To this end, the arc length s on the sphere with radius R is defined to be $s : = { \overline { { R } } } { \widehat { s } } .$ where sˆ is the arc length on the unit sphere. Furthermore, $\mathbf { X } _ { s p } : = \overline { { R } } \hat { \mathbf { X } } _ { s p }$ depicts the location on the new sphere; here, $\hat { \mathbf { X } } _ { s p }$ denotes the location on the unit sphere (refer to Fig. 9). Additionally, the bound for the control input from the unit sphere $( = \hat { U } _ { m a x } )$ is scaled to obtain $U _ { m a x } : = \left( \overline { { { R } } } \right) ^ { - 1 } \hat { U } _ { m a x }$ . Following a similar process as Lemma 3.2 in [26], we can show that the minimum turning radius r on the sphere of radius R is given by $r = \overline { { R } } \hat { r }$ A depiction of the scaling for the initial configuration is shown in Fig. 9.

The evolution equations for the sphere with radius $\overline { { R } }$ can therefore be obtained as

$$
\begin{array}{r l} & {\frac {d \mathbf {X} _ {s p}}{d s} (s) = \mathbf {T} _ {s p} (s), \quad \frac {d \mathbf {T} _ {s p}}{d s} (s) = - \frac {1}{\overline {{R}} ^ {2}} \mathbf {X} _ {s p} (s) + u _ {g} \mathbf {N} _ {s p} (s),} \\ & {\frac {d \mathbf {N} _ {s p}}{d s} (s) = - u _ {g} \mathbf {T} _ {s p} (s),} \end{array}\tag{27}
$$

where $u _ { g } \in [ - U _ { m a x } , U _ { m a x } ]$ is the geodesic curvature on the sphere of radius R and relates to the minimum turning radius r on the sphere by $\begin{array} { r } { r = \frac { \overline { { R } } } { \sqrt { 1 + U _ { -- } ^ { 2 } \overline { { R } } ^ { 2 } } } } \end{array}$ . The evolution of these three vectors for $u _ { g } \equiv U _ { m a x } ^ { \mathrm { ~ v ~ } } , 0 , 0 ^ { m a x } - U _ { m a x }$ , which correspond to left turn, great circular arc, and right turns on the sphere, can be obtained using the Euler-Rodriguez formula.

## D. Proof for Lemma 3

Consider cylinders connecting a pair of inner or outer spheres, which are shown in Fig. 7a. The tangent plane for these cylinders is the T−Y plane. Consider the bound chosen for the geodesic curvature on the cylinder $( \kappa _ { g , c y c } )$ from (15), which is $\frac { 1 } { R _ { y a w } }$ . We note that $\kappa _ { g , c y c }$ denotes the magnitude of the projection of the curvature vector on the tangent plane [28]. Since the tangent plane of this cylinder is the T − Y plane, $\kappa _ { g , c y c }$ also represents the geodesic curvature for the rotation minimizing frame model. This is because geodesic curvature for the minimizing frame model $( \kappa _ { g } )$ controls the yaw motion (in the T − Y plane) for the vehicle. Hence, the geodesic curvature bound for the rotation minimizing frame model is automatically satisfied for the chosen bound for $\kappa _ { g , c y c } .$

On the other hand, the normal curvature of a cylinder depends on the direction of traversal along the cylinder. If the curve is along a direction parallel to the axis of the cylinder, $\kappa _ { n , c y c } = 0 ;$ however, if the curve is perpendicular to the axis, $\begin{array} { r } { \kappa _ { n , c y c } = \frac { 1 } { \overline { { R } } } } \end{array}$ , since the curve is along the circular cross-section [31]. Since these curvatures of 0 and $\textstyle { \frac { 1 } { \overline { { R } } } }$ are the principal curvatures, the normal curvature for any intermediary direction of motion lies between the two through Euler’s theorem [28]. Noting that the normal curvature is along the surface normal for the cylinder, which is along U for the rotation minimizing frame model, the normal curvature bounds for the rotation minimizing frame model are automatically satisfied. A similar argument applies for the selected bound for $\kappa _ { g , c y c }$ for the left and right cylinders, with the only difference arising in considering T−U as the tangent plane and the surface normal for the cylinders being Y.

## E. Proof for Lemma 4

Consider a cylinder that is parameterized in terms of u and v through (19). It suffices to show that the first fundamental form for the cylinder is the same as that for the plane, parameterized using u and v as given in (18). The first fundamental form coefficients are given by ( [28]) $\begin{array} { r } { E _ { c y l } = \frac { \partial \mathbf { X } _ { c y l } ^ { \mathcal { U } } ( s ) } { \partial u } \cdot \frac { \partial \mathbf { X } _ { c y l } ^ { \mathcal { U } } ( s ) } { \partial u } = } \end{array}$ $\begin{array} { r } { 1 , \ F _ { c y l } \ = \ \frac { \partial { \bf X } _ { c y l } ^ { \mathcal { U } } ( s ) } { \partial u } \ \cdot \ \frac { \partial { \bf X } _ { c y l } ^ { \mathcal { U } } ( s ) } { \partial v } \ = \ 0 } \end{array}$ , and $\begin{array} { r } { G _ { c y l } = \frac { \partial \mathcal { U } } { \partial v } } \end{array}$ $\begin{array} { r } { \frac { \partial \mathbf { X } _ { c y l } ^ { \mathcal { U } } ( s ) } { \partial v } = 1 } \end{array}$ . Similarly, $E _ { p l a n e } , F _ { p l a n e } ,$ , and $G _ { p l a n e }$ can be obtained to be 1, 0, and 1. Since the first fundamental form coefficients of the cylinder and the plane are equal, the length of the curve is preserved. This is because the distance between two closely spaced points on the curve on the cylinder that are initially separated by du and dv on the plane is given by $d s _ { c y l } ^ { 2 } = E _ { c y l } d u ^ { 2 } + 2 F _ { c y l } d u d v + G _ { c y l } d v ^ { 2 } = d s _ { p l a n e } ^ { 2 } .$

![](Kumar2025Novel_figs/8e70ee416322b47449d13185b6f6e5e1d66f5b0f2d159549308f202fea06f3bd.jpg)

Deepak Prakash Kumar (Member, IEEE) received his Ph.D. degree in Mechanical Engineering from Texas A&M University in 2025. He received his B.Tech in Engineering Design and M.Tech in Automotive Engineering from the Engineering Design department at IIT Madras in 2020. He is currently a Postdoctoral Scholar with the Center for Resilient Autonomous Systems, Department of Electrical Engineering and Computer Science, University of California, Irvine. His research interests include safe physical AI algorithms for multi-agent collaboration, physical AI for human–robot teaming, motion planning and control for autonomous vehicles, and vehicle routing algorithms.

![](Kumar2025Novel_figs/bdf28dc9d5f97079379d5cef089b57a2fc093212dd3b2496eac522c1779833b7.jpg)  
Systems and Unmanned Vehicles.  
Swaroop Darbha (Fellow, IEEE), received the Ph.D. degree from the University of California at Berkeley, Berkeley, CA, USA, in 1994. He is currently the Gulf Oil/Thomas A Dietz Professor of mechanical engineering with Texas A&M University, College Station, TX, USA. His research interests include dynamics, control, and diagnostics of connected and autonomous ground vehicles, routing of unmanned aerial vehicles, and decision-making under uncertainty. He is a fellow of ASME and IEEE for his contributions to Intelligent Transportation

![](Kumar2025Novel_figs/108d5e00de17a5b1fa588ad486a679840372058fc14b6f6f7977163411269a33.jpg)

Satyanarayana Gupta Manyam (Senior Member, IEEE), Satyanarayana Gupta Manyam received the Ph.D. degree in Mechanical Engineering from Texas A & M University, College Station, Texas, in 2015. He is currently a Research Scientist at DCS Corporation, where he works as a contractor for the Control Science Center of the U.S. Air Force Research Laboratory (AFRL) at Wright-Patterson Air Force Base, OH, USA. His primary research interest include cooperative path planning for multivehicle systems, trajectory and motion planning for autonomous vehicles. His interests also include combinatorial optimization and bounding algorithms for discrete optimization problems.

![](Kumar2025Novel_figs/5b30d3869a2cc003b588af01b92f2e7556cc134db68963cf01a810fd5108d042.jpg)  
Information Systems.

David W. Casbeer (Senior Member, IEEE) is the technical area lead for UAV Cooperative and Intelligent Control at the Air Force Research Laboratory’s Control Science Center, where he leads research to enable autonomous UAVs in future Air Force missions. He received the BS (2003) and PhD (2009) degrees from Brigham Young University, where he focused on decentralized estimation techniques. He is a Senior Member of the IEEE and an Associate Fellow in the AIAA. He currently serves as an associate editor for the AIAA Journal of Aerospace