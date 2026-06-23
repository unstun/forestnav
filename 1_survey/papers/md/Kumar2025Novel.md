---
citation_key: Kumar2025Novel
arxiv_id: 2509.24143
arxiv_url: "https://arxiv.org/abs/2509.24143"
title: "A Novel Model for 3D Motion Planning for a Generalized Dubins Vehicle with Pitch and Yaw Rate Constraints"
authors_short: "Deepak Prakash Kumar et al."
year: 2025
direction_tag: K_dubins_reeds_shepp
source: pymupdf4llm
converted_at: 2026-06-23T19:47:56Z
origin: ai+web
reviewed: false
---

IEEE TRANSACTIONS ON ROBOTICS 

1 

# A Novel Model for 3D Motion Planning for a Generalized Dubins Vehicle with Pitch and Yaw Rate Constraints 

Deepak Prakash Kumar, _Member, IEEE_ , Swaroop Darbha, _Fellow, IEEE_ , Satyanarayana Gupta Manyam, _Senior Member, IEEE_ , David W. Casbeer, _Senior Member, IEEE_ 

_**Abstract**_ **—In this paper, we propose a new modeling approach and a fast algorithm for 3D motion planning, applicable for fixedwing unmanned aerial vehicles. The goal is to construct the shortest path connecting given initial and final configurations subject to motion constraints. Our work differs from existing literature in two ways. First, we consider full vehicle orientation using a body-attached frame, which includes roll, pitch, and yaw angles. However, existing work uses only pitch and/or heading angle, which is insufficient to uniquely determine orientation. Second, we use two control inputs to represent bounded pitch and yaw rates, reflecting control by two separate actuators. In contrast, most previous methods rely on a single input, such as path curvature, which is insufficient for accurately modeling the vehicle’s kinematics in 3D. We use a rotation minimizing frame to describe the vehicle’s configuration and its evolution, and construct paths by concatenating optimal Dubins paths on spherical, cylindrical, or planar surfaces. Numerical simulations show our approach generates feasible paths within 10 seconds on average and yields shorter paths than existing methods in most cases.** 

_**Index Terms**_ **—Aerial systems: applications, 3D motion and path planning, Dubins vehicle.** 

## I. INTRODUCTION 

HE use of Unmanned Aerial Vehicles (UAVs) is rapidly **T** growing in civilian and military applications, including search and rescue and surveillance. Fixed-wing UAVs are of particular interest due to longer flight times, larger payload capacity, and the ability to fly at higher altitudes [1], [2]. However, they are persistently in motion, i.e., cannot stop or hover mid-air, and cannot change their heading angle instantaneously. Hence, they have a bound on the rate of change of their heading/orientation, which manifests itself as curvature constraints on the path. Motion planning is important for these vehicles, in which the goal is to plan the optimal path to travel from one configuration (i.e., position and orientation together) to another. The objective of interest in this paper is 

Received 24 September 2025; revised 2 March 2026; accepted 13 April 2026. Recommended by Editor Rafael Murrieta-Cid. ( _Corresponding author: Deepak Prakash Kumar_ ). 

Deepak Prakash Kumar is with the Department of Electrical Engineering and Computer Science, University of California, Irvine, CA 92697, USA (email: deepakprakash1997@gmail.com). 

Swaroop Darbha is with the Department of Mechanical Engineering, Texas A&M University, College Station, TX 77843, USA (e-mail: dswaroop@tamu.edu). 

Satyanarayana Gupta Manyam is with the DCS Corporation, 4027 Col Glenn Hwy, Dayton, OH 45431, USA (e-mail: msngupta@gmail.com). David Casbeer is with the Control Science Center, Air Force Research Laboratory, Wright-Patterson Air Force Base, OH 45433 USA (e-mail: david.casbeer@us.af.mil). 

to obtain the minimum-time (or distance) path(s). We seek a finite set of candidate paths that includes the optimal path for any boundary condition. These candidate paths are suitable for constructing paths for fixed-wing aircraft or yaw rateconstrained vehicles. 

Motion planning for yaw rate-constrained vehicles is typically addressed by considering a simplified kinematic model, called the Dubins model. This models a vehicle traveling at a constant speed and has a minimum turning radius constraint, which is suitable for UAVs traveling at constant altitude (in 2D). Dubins [3] solved the problem of the shortest path between a pair of configurations on a plane. It was shown that the optimal path is of type _CSC, CCC,_ or a degenerate path of the same, where _C_ = _L, R_ denotes a left or a right turn of minimum turning radius, and _S_ denotes a straight line segment. Although Dubins showed this result using geometric techniques, the same result was later derived using Pontryagin’s Minimum Principle ( [4]) in [5] using simpler proofs. Various variants of the planar path planning problem have been explored with variations in the model and/or the objective, such as in [6], where different left and right turning radius was considered. 

Motion planning for such vehicles in 3D has also been an area of interest, where the shortest path to travel from one configuration to another, considering their motion constraints, is sought. The 3D problem applies not only to fixed-wing UAVs but also to underwater gliders and robots [7], [8]. Although specifying the heading angle alone uniquely defines the orientation of the vehicle in the 2D problem, the 3D problem requires both the heading angle and the plane in which the UAV lies. The UAV’s plane can be uniquely described using two additional angles (pitch and roll) or by a vector along its lateral or normal direction. 

Simple kinematic models have also been used to tackle the 3D problem, where, similar to the 2D problem, the generated path can be tracked using a lower-level controller [9]. Because these paths can be computed very quickly, they can be combined with algorithms such as Rapidly Exploring Random Tree (RRT) to find feasible, obstacle-avoiding routes [10]. This method has also been experimentally demonstrated using an ARDrone in [11]. 

To our knowledge, the first exploration of the 3D problem was by Sussman [12]. The author showed that the optimal path is of type _CSC, CCC,_ or a degenerate[1] version of these paths, or a helicoidal arc to connect a given location 

DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited. AFRL-2025-3035; Cleared 06/17/2025. 

> 1Degenerate paths of _CSC_ and _CCC_ paths are _CS, SC, CC, C,_ and _S_ . 

2 

IEEE TRANSACTIONS ON ROBOTICS 

and heading direction[2] . Unlike the 2D problem, there are infinitely many _C_ segments since the plane containing the segment can be arbitrarily picked; due to the tangential _S_ segment, many (finite) solutions may exist. Conditions exist for which infinitely many _CSC_ paths exist, such as those shown in [13]. Hence, efficient construction of _CSC_ paths has been explored in the literature. In [14], a _CSC_ path was constructed for instances where the initial and final locations are spaced sufficiently far apart using geometric and numerical approaches. In a later work [15], the authors adopted this path as an initial guess for a nonlinear optimization problem that was solved using a multiple-shooting method to improve the solution. The _CSC_ path construction was addressed in [13] as an inverse kinematics problem for a five degrees-of-freedom robotic manipulator. Analytical solutions were obtained for the path parameters to improve computational efficiency. _CSC_ path construction was also recently addressed in [16]. In that work, the authors parametrized the path in terms of two variables and performed a numerical search, utilizing off-theshelf solvers assisted by derived gradients to construct the path. 

In [17], the 3D problem was addressed with a model that has two controllable inputs - one for yaw rate, and another for the rate of change of the altitude. In this work, a “Dubins airplane model” was proposed, and it was shown that the optimal trajectory comprises segments with arcs of minimum turning radius, straight lines, or a Dubins path of a certain length. Depending on the altitude difference between the initial and final locations, feasible solutions were generated by introducing additional segments to attain the desired altitude. This model was modified in [18], wherein a pitch angle constraint was introduced. Contrary to [17], this paper generates trajectories by incorporating helicoidal segments to attain the desired altitude when necessary. Additionally, the constructed paths were validated by simulations using a six-degree-of-freedom model (given in [19]) and a vector-field-based guidance law, inspired by [20], for tracking. 

The 3D motion planning problem has also been addressed using the 2D Dubins result in [21]. The authors consider a _total_ curvature constraint and a bounded pitch angle for the vehicle. They decouple the _CSC_ path to connect the given initial and final locations and heading vector into horizontal and vertical components. In this regard, they use the horizontal projection of the configurations to connect the locations and heading angles. The obtained path length is utilized as the _x_ coordinate in the vertical plane, with the desired altitude difference to be attained serving as the _z_ coordinate. Using iterative optimization of the horizontal and vertical turning radii, a feasible solution is constructed such that the total curvature bound and pitch angle bounds are satisfied. The authors used this solution to provide an initial guess to a nonlinear optimization problem to further refine the path in [22]. In the existing literature, we observe that the _complete ori-_ 

> 2We note that in 3D, specifying only the location and heading direction does not fully determine the vehicle’s configuration, since the orientation of the plane containing the vehicle is not uniquely defined. In contrast, for 2D motion planning, location and heading are sufficient to uniquely specify the configuration. 

_entation of the vehicle_ has not been considered for 3D motion planning. This is because the description of the pitch and heading angles alone does not uniquely describe its orientation. For example, Fig. 1 shows two orientations for the same vehicle moving along a straight line trajectory with a pitch angle of 0 _[◦]_ and a heading angle of 45 _[◦]_ : one where the roll angle is 0 _[◦]_ and another where the roll angle is 45 _[◦] ._ Infinitely many orientations exist for the same trajectory. However, from these figures, we can observe that prescribing the longitudinal direction and the lateral or normal direction of the vehicle would uniquely describe the orientation.[3] While the study in [23] models the complete configuration of a general robot, it is unclear how their model relates to the kinematics of a fixed-wing UAV. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0002-07.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0002-08.png)


(a) Roll angle = 0 _[◦]_ (animation (b) Roll angle = 45 _[◦]_ (animation provided on our GitHub page) provided on our GitHub page) 

Fig. 1. Depiction of two orientations corresponding to the same heading and pitch angle 

The literature on path planning for aerial robots has primarily focused on models with a single control input, such as yaw rate, or a single constraint on the path’s curvature. In the 3D generalization of path planning, a single control input alone cannot capture the range of motions. This is because there are two elementary motions of interest for the motion planning of aerial vehicles: pitch and yaw. For fixed-wing UAVs, pitch motion is achieved using elevators, and yaw motion is achieved with rudder and/or aileron[4] [19]. Since yaw and pitch motion are controlled by separate actuators, considering a single control is not sufficient. Hence, it is crucial to consider two control inputs: a bounded pitch rate and a bounded yaw rate. These constraints correspond to the minimum turning radii, _Rpitch_ and _Ryaw_ , of the path’s curvature. The bounds on the pitch and yaw rates manifest as locally inaccessible spherical regions of radii _Rpitch_ and _Ryaw_ , respectively.[5] Though two control inputs are considered in [17], the second control input 

> 3We remark here that in Fig. 1, unit vectors along the longitudinal, lateral, and normal directions are referred to as tangent, tangent normal, and surface normal vectors, respectively. The latter notation would be used later in the paper to describe the rotation minimizing frame model. 

> 4Ailerons control the roll of the UAV, and this roll motion leads to a corresponding yaw motion for the vehicle. 

5Imagine a vehicle moving in 3D space with a maximum allowable yaw rate (i.e., how quickly it can turn left or right). Due to this constraint, the vehicle cannot immediately change direction; it needs a certain minimum turning radius to execute a yaw maneuver. A yaw motion sphere is a spherical region around the vehicle that it cannot enter directly unless it has traveled a sufficient distance to allow for the required turning maneuver. This is analogous to the turning circles on the left and right in the 2D Dubins path problem. Similar to the yaw motion spheres that define inaccessible regions in the horizontal plane, pitch constraints define vertical maneuverability limits. 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

3 

is the rate of change of the altitude of the vehicle; furthermore, the pitch angle is not considered in this model, which makes it more appropriate for a quadcopter. 

A demonstration of the limitations of state-of-the-art approaches that rely on a single control input is presented in Fig. 2 for two instances. In both of these cases, paths were generated using the method from [21] - for which the code is publicly available. The minimum turning radius for this model was set to 40 meters to enforce the curvature constraint. In the following, we analyze these examples to explain why this path planning method is either infeasible or inefficient for the proposed (3D) model. 

- 1) Our proposed model incorporates two independent control inputs for the yaw and pitch rates. We set the minimum pitch turning radius, _Rpitch_ , to 40 meters[6] for the first example. This choice is consistent with the parameter used in [21]. Since the yaw turning radius, _Ryaw_ , can be chosen independently, we set it to 50 meters. The solution generated by [21], shown in Fig. 2a, violates the yaw rate constraint by entering the yaw motion sphere. Such a maneuver is infeasible as the vehicle must travel a sufficient distance outside the sphere before entering it. This behavior is analogous to the infeasibility of entering the left or right turning circles in the 2D Dubins problem [3]. 

- 2) In the second example, we alternately pick _Ryaw_ in our model to be the same as the parameter in [21], which is 40 meters. Since _Rpitch_ is free to choose, we set _Rpitch_ to be equal to 60 meters. The path obtained using the algorithm from [21] is shown in Fig. 2b. We observe that the path enters one of the pitch motion spheres (which lies at the top of the vehicle), and hence violates the pitch rate constraint. 

Alternatively, one could argue that the maximum of _Ryaw_ and _Rpitch_ can be chosen as the minimum turning radius in [21]. However, this would lead to inefficient motion planning, since the vehicle would take larger-than-necessary turns in some instances. 

The presented issues were addressed in our previous work in [24], where a special case of motion planning on the surface of a sphere was studied. This paper provided insights for the 3D motion planning by considering a vehicle model with bounded yaw rate and pitch rate. Furthermore, the spherical motion planning problem was shown to arise as an intermediary problem to be solved for the 3D problem. 

Having identified two major issues in the literature, the contributions of this paper are as follows: 

- 1) We present a novel model using a rotation minimizing frame, also called the Bishop frame, to obtain the shortest path for a vehicle subject to pitch rate and yaw rate constraints. We build on the insights provided in [24] for the 3D problem. 

- 2) We prove that the pitch rate and yaw rate constraints manifest as four spheres around the vehicle that represent temporarily inaccessible regions, thereby appropriately generalizing the 2D Dubins model to 3D. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0003-11.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0003-12.png)


(a) Yaw rate violation for (b) Pitch rate violation for _Rpitch_ = 40 m. _Ryaw_ = 50 _Ryaw_ = 40 m. _Rpitch_ = 60 m. m. 

Fig. 2. Issue with single control input 

- 3) We propose a path construction algorithm that consists of three classes of paths. The main idea is to build path segments on spherical surfaces that are tangent to the initial and final configurations, and these segments are connected by an intermediary surface. This surface could be a cylindrical envelope, a cross-tangent plane, or another spherical surface. 

- 4) We pose and solve a Dubins-type path planning problem subject to curvature constraints on a cylindrical surface. To the best of our knowledge, the cylindrical motion planning problem has not been addressed in the literature. The proposed solution method involves unwrapping the surface to a two-dimensional plane, computing the optimal Dubins path, and then mapping back onto the cylindrical surface. 

- 5) We present extensive numerical results on several instances. We show the effect of ( _i_ ) model that defines the complete configuration of the vehicle, ( _i.e., heading and lateral orientation_ ) and ( _ii_ ) the impact of minimum turning radii on the best feasible path. We also observe that our algorithm can produce a high-quality feasible solution within 10 seconds. Additionally, we provide the code in a publicly available repository.[7] 

## II. MODELING AND GEOMETRIC PRELIMINARIES 

Let _t_ and _s_ denote the time and arc length, respectively, and **X** ( _s_ ) denote the instantaneous location of the vehicle. We consider a Rotation-Minimizing frame, also called a Bishop frame [25], attached to the center of mass of the UAV. Let **T** _,_ **Y** _,_ **U** denote the unit vectors of the Bishop frame with **T** _,_ **Y** directed along the longitudinal and lateral directions of the vehicle, respectively. The vector **U** := **T** _×_ **Y** is along 

> 7The code for our algorithm is available at https://github.com/DeepakPrakashKumar/ 3D-Motion-Planning-for-Generalized-Dubins-with-Pitch-Yaw-constraints. git. 

> 6In the paper, we will interchangeably use “m” to denote “meters”. 

4 

IEEE TRANSACTIONS ON ROBOTICS 

the normal direction of the vehicle. Fig. 3 shows the vehicle configuration with the vectors **T** _,_ **Y** and **U** .[8] 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-03.png)


Fig. 3. The configuration of the vehicle defined by the three vectors **T** _,_ **Y** and **U** 

The instantaneous angular velocity of the frame can be written as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-06.png)


with _ωx, ωy, ωz_ denoting the components in the **T** _,_ **Y** , and **U** directions, respectively. One may think of them as the roll, pitch, and yaw rates of the body, respectively. Notably, the Rotation Minimizing Frame (RMF) is constructed so that _ωx_ ( _t_ ) = 0: there is no rotation about the tangent, minimizing frame twisting (essentially, the roll rate is set to zero).[9] The kinematics of the frame then satisfy: 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-08.png)


A key property of an RMF is that **Y** ( _t_ ) and **U** ( _t_ ) change only in the direction of **T** ( _t_ ). 

Assume that the vehicle moves at a constant, nonzero longitudinal speed _V_ 0. Defining 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-11.png)


the kinematic equations parameterized in terms of _s_ become 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-13.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-14.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-15.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-16.png)


> 8We also denote **T** _,_ **Y** _,_ and **U** as tangent, tangent normal, and surface normal vectors, respectively. 

> 9Since _ωx_ = 0 _,_ the generated paths do not allow for unbounded roll. The paths constructed remain feasible for a model with non-zero roll rate assumption, however, the paths may be suboptimal when additional constraints, such as bounded roll angles or rates, are imposed. Extending our model and method to enforce bounds on the roll angle would be valuable, and can be considered an important direction for future work. 

The bounds for control inputs _κg_ and _κn_ , which we refer to as geodesic curvature and normal curvature, respectively, are stated as shown below,[10] 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-20.png)


We shall later show that _Rpitch_ is the minimum turning radius corresponding to pitch motion and _Ryaw_ is the minimum turning radius corresponding to the yaw motion. The objective is to compute the minimum distance trajectory from the initial to final configuration, defined by **X** _,_ **T** _,_ **Y** _,_ and **U** . Hence, the cost to minimize is _J_ = � 1 _ds._ 

**Remark 1** ( **Model** ) **.** Three angles (roll, pitch, and yaw), or equivalently, **T** _,_ **Y** _,_ and **U** _,_ are required to specify the UAV’s orientation in 3D, but only two (pitch and yaw) are directly controlled by the primary actuators on a fixedwing UAV (aileron, rudder, and elevator). The roll angle evolves naturally as a consequence of coordinated turning [19], wherein ailerons, which cause roll, allows the vehicle to turn. From a planning perspective, the two control inputs are sufficient to reach any orientation; this is analogous to rigid-body kinematics, wherein a z-y-z rotation can be used to reach any orientation. The Bishop frame is used to separate vehicle orientation from path geometry, enabling continuous and physically feasible orientation profiles while capturing the aircraft’s kinematics. 

Geometrically, the path planning problem can be depicted as shown in Fig. 4. A detailed description of this figure follows. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-24.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-25.png)


**----- Start of picture text -----**<br>
Z<br>Xi Xf<br>Y<br>X<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-26.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-27.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-28.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-29.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-30.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-31.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-32.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-33.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0004-34.png)


Fig. 4. Depiction of spheres corresponding to pitch motion (in orange and magenta) and yaw motion (in blue and green) at the initial and final configuration 

In Fig. 4, it can be observed that four spheres are constructed, which are tangential to the vehicle configuration. To understand how they appear, we need to understand the geometric impact of the curvatures, _κn_ and _κg._ To this end, we derive the closed-form expression for **X** _,_ **T** _,_ **Y** _,_ and **U** over an interval wherein _κg_ and _κn_ are constants. The obtained expressions are shown in Appendix A. 

We remark here that since the control inputs appear linearly in the differential equations (3)-(5), and a minimum time 

> 10We use the notation _κg_ and _κn_ , since they have the same form as that of the geodesic and normal curvatures in the Darboux frame model, a differential geometric model. 

5 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

problem is considered, the optimal control actions are expected to be bang-bang from Pontryagin’s minimum principle [4].[11] Therefore, it is sufficient to consider intervals in which _κg_ and _κn_ are constant. Furthermore, it suffices to consider _κg ∈{− Ryaw_ 1 _[,]_[ 0] _[,] Ryaw_ 1 _[}]_[and] _[κ][n][∈{−] Rpitch_ 1 _[,]_[ 0] _[,] Rpitch_ 1 _[}]_[.] Using the closed-form expressions derived in Appendix A, we state and prove the following two lemmas. 

**Lemma 1.** _When κn_ = _Rpitch_ 1 _[or][−] Rpitch_ 1 _[the][corresponding] segment lies on spheres with radius Rpitch whose center lies along_ **U** _or −_ **U** _, respectively. Furthermore, such segments correspond to a maximum ascent or descent motion of the_ 1 _vehicle with a turning radius of κ_[2] _g_ + _R_[2] 1 _._ � _pitch_ 

## _Proof._ The proof is provided in Appendix B. 

The following lemma states a similar result in a different axis, and the proof follows the same reasoning. 

**Lemma 2.** _When κg_ = _± Ryaw_ 1 _[,][the][corresponding][segment] lies on spheres with radius Ryaw whose center lies along_ **Y** _or −_ **Y** _. Furthermore, such segments correspond to maximum turn (left or right) motion of the vehicle with a turning radius_ 1 _of_ 1 _._ � _Ryaw_[2][+] _[κ]_[2] _[n]_ 

From these two lemmas, we see that the normal curvature _κn_ governs the pitch motion, while the geodesic curvature _κg_ governs the yaw motion. In fact, these curvatures directly correspond to the vehicle’s pitch rate and yaw rate, respectively (which is expected based on the Bishop frame setup and the definitions in (1)). When the vehicle moves with its maximum pitch rate and zero yaw rate, it follows a great circle of radius _Rpitch_ on the orange or purple sphere shown in Fig. 4. This result comes from Lemma 1. Since the vehicle travels at unit speed, the time to complete the circle is _tpitch_ = 2 _πRpitch._ Over this time, the pitch angle changes by 2 _π_ , so the pitch rate is 2 _π_ 1[A][similar][argument][holds][for][the][yaw] _tpitch_[=] _Rpitch[.]_ rate, giving a maximum value of _Ryaw_ 1[.][Therefore,] _[κ][n]_[and] _[κ][g]_ represent the vehicle’s pitch and yaw rates, respectively. By varying _κn ∈ {− Rpitch_ 1 _[,]_[ 0] _[,] Rpitch_ 1 _[}]_ and _κg ∈_ 1 1 _{− Ryaw[,]_[ 0] _[,] Ryaw[}]_[,][we][obtain][nine][distinct][motion][primitives,] shown in Fig. 5. These were generated using the closed-form expressions, presented in Appendix A. Using Lemma 1, we find that the segments _Lsi, Rsi, Lso,_ and _Rso_ have radius 1 1 1 , corresponding to motion with maximum ab� _Ryaw_[2][+] _Rpitch_[2] solute pitch and yaw rates. Here, _L_ and _R_ denote a left turn and right turn, respectively, which correspond to _κg_ = _Ryaw_ 1 andand _κ_ “ _sog_ =” are _− Ryaw_ used1 _[,]_[respectively.] to refer to the[Additionally,] segments that[subscripts] lie on[“] _[si]_ the[”] “inner” sphere and “outer” sphere, respectively; the inner sphere corresponds to _κn_ = _Rpitch_ 1 _[,]_[and][the][outer][sphere] corresponds to _κn_ = _− Rpitch_ 1 _[.]_[The][segments] _[G][si]_[and] _[G][so]_ 

> 11We remark here that in general, minimizing path length and minimizing time are not equivalent. However, we assume the speed of the vehicle to be constant, which can be set to be a unit speed without loss of generality; if not, the optimal time and optimal path length will differ by a scalar value (which is the speed). 

result from pure pitch motion ( _κg_ = 0), while _Lp_ and _Rp_ result from pure yaw motion. When both curvatures are zero ( _κn_ = _κg_ = 0), the vehicle moves in a straight line segment _S_ . 

Using the obtained motion primitives and the observation that _κn_ and _κg_ attaining values of _± Rpitch_ 1[and] _[±] Ryaw_ 1[yields] two spheres each (a pair along **U** and a pair along **Y** ), we can observe that at both the initial and final configuration, four spheres exist around the vehicle. Additionally, portions of the optimal path will lie on one of the four spheres at the initial configuration and one of the four spheres at the final configuration[12] . Hence, we propose three classes of paths to construct a feasible path connecting one of the initial spheres with one of the final spheres. We construct the path using three types of intermediary surfaces (or classes): a cylindrical envelope, a planar surface, or a spherical surface. These three classes of paths are a generalization of the classical _CSC_ and _CCC_ paths for the planar Dubins problems. In our algorithm, we consider a sphere at the initial or final configuration to serve as a generalization of the turn segment ( _C_ ) in a plane; furthermore, we consider the cylindrical envelope and planar surface to generalize the _S_ segment. In the following section, we describe the three classes of paths in more detail. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0005-11.png)


**----- Start of picture text -----**<br>
Gsi<br>Lsi U 0 Rsi Lsi U 0 Rsi S<br>Y 0 T 0 Lp Y 0 T 0 Rp<br>Lso Rso Lso Rso<br>Z X 0 Z X 0<br>Y Gso Y<br>X X<br>(a) Segments (b) Segments on spheres<br>on spheres corresponding to max. yaw<br>corresponding to rate (and straight line seg-<br>max. pitch rate ment)<br>**----- End of picture text -----**<br>


Fig. 5. Visualization of segments [24]. We note that _Lsi, Rsi, Lso,_ and _Rso_ are shown in both subfigures, since each of these segments lies on two spheres. 

**Remark 2.** In general, the yaw and pitch rates for different UAVs may vary and can be coupled. The problem posed here is still of significant interest in obtaining lower and upper bounds for the shortest path length. One such case is illustrated by the region within the boundaries, shown in brown, in Fig. 6. However, by replacing the boundary with a rectangular region inscribed within this area, one can derive an upper bound that is a feasible solution. Similarly, by outer approximating the allowable region with a larger rectangular region, shown in 

> 12The only motion primitive that does not lie on a sphere is a straight line segment _S._ However, even in this case, a portion of the optimal path can be modeled to lie on one of the four spheres; however, the path will be trivial, i.e., of zero length. 

6 

IEEE TRANSACTIONS ON ROBOTICS 

green in Fig. 6, a lower bound for the optimal path length can be obtained. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0006-03.png)


**----- Start of picture text -----**<br>
Upper κn Lower<br>bound Kn bound<br>κg<br>−K [l] −K [u] K [u] K [l]<br>g g g g<br>−Kn Generic<br>curvature<br>constraints<br>**----- End of picture text -----**<br>


Fig. 6. Generic control inputs region and obtaining bounds for rectangular control input region considered in this paper 

## III. SHORTEST PATH CONSTRUCTION 

The constructed paths start and end on a spherical surface at the initial and final configurations. Three distinct classes of paths are presented, each using a different intermediary surface for the sub-path between the spheres, which can be cylindrical, planar, or spherical. We refer to the spheres centered along the **U** -axis as the inner (orange, along **U** ) and outer (purple, along _−_ **U** ) spheres, as shown in Fig. 4. Similarly, the spheres centered along the **Y** -axis are called the left (green, along **Y** ) and right (blue, along _−_ **Y** ) spheres. 

The intermediary sub-paths considered are as follows: 

- 1) In the first class, the sub-path is constructed using a cylindrical envelope. In this case, we connect the pair of spheres of the same type at the initial and final configurations. There are four such pairs: inner-to-inner, outer-to-outer, left-to-left, and right-to-right. Fig. 7a illustrates the cylindrical envelope between inner and outer spheres. We will later show that these paths satisfy the curvature constraints in (6). The full construction is detailed in Section IV. 

- 2) In the second class of paths, a sub-path between a pair of spheres is constructed on a cross-tangent plane. For spheres of opposite type, such as inner-to-outer, outerto-inner, left-to-right, or right-to-left, a path through a cylindrical envelope is not feasible. This is because the normal vector of the cylindrical surface, **U** for pitch spheres and **Y** for yaw spheres, remains constant along the envelope and does not support a continuous feasible orientation between opposing directions. Hence, such spheres are connected using a cross-tangent plane. An example for the inner-to-outer case is shown in Fig. 7b. Details of this construction are provided in Section V. 

- 3) In the third class of paths, we construct sub-paths between pairs of spheres of the same type using an intermediary sphere. There are four such configurations: inner–outer–inner, outer–inner–outer, left–right–left, and right–left–right. These paths are designed for initial and final locations that are close to each other. An example of this type is illustrated in Fig. 7c, and the full construction is described in Section VI. 

**Remark 3.** Note that only the listed classes are possible using a single intermediary surface. For example, connecting an inner sphere at the initial configuration with a left sphere at the final configuration is not possible. A cylindrical surface cannot be used because the outward normal directions differ: _−_ **U** for the inner sphere and _−_ **Y** for the left sphere. Since the normal vector remains constant across cylindrical, spherical, and frustum surfaces, none of these can bridge the two spheres. A planar surface also doesn’t work, as there is no common tangent plane between the two. For instance, the **T** _−_ **Y** plane is tangent to the inner sphere but not to the left sphere (see Fig. 4). Therefore, using a single intermediary surface, we can only connect either a pair of pitch spheres or a pair of yaw spheres, not a mix of both. The underlying reason is that **X** _,_ **T** _,_ **Y** _,_ and **U** must be continuous. The same argument applies for using an intermediary sphere as the tangential sphere to the initial and final spheres, i.e., only a right sphere can be used to connect two left spheres. 

**Remark 4.** Although it is possible to connect a pair of spheres of the same type (e.g., inner–inner) using a plane, we do not consider such paths in this paper. This is because the planar connection is a special case of the cylindrical connection. This is because a plane can be wrapped into a cylinder without changing the path length or violating the curvature constraints. We discuss this preservation property in more detail when introducing the cylindrical path construction in the next section. 

**Remark 5.** In Sections IV, V, and VI, we present the methodology for constructing three types of paths by introducing parameters that describe each path, which are subsequently discretized. Whenever we refer to the “shortest” path, we mean the least-length path obtained by our construction methodology under the chosen discretization; global optimality is not claimed. However, we note that the subpath constructed on each individual surface (cylinders, spheres, and planes) is optimal for that surface. Our methodology will always yield a feasible path, as at least the first class of path (through the cylindrical envelope) always exists. 

## IV. PATH SYNTHESIS ON CYLINDRICAL ENVELOPE 

To generate a feasible path connecting two spheres of the same radius and type via a cylindrical envelope (as shown in Fig. 7a), the vehicle follows this sequence: 

- Step 1: The path starts on the initial sphere and transitions to the cylindrical surface. The transition point, **X** _ic_ , lies on the boundary circle formed by the intersection of the sphere and the cylindrical envelope. At this point, its longitudinal direction aligns with **T** _ic,_ as illustrated in Fig. 8. 

- Step 2: The path exits the cylindrical envelope at **X** _oc_ , with longitudinal direction **T** _oc_ . 

- Step 3: Finally, the path continues on the final sphere to reach the desired final configuration. 

Note that the entry and exit points on the cylinder, along with their corresponding tangent directions, are not fixed and can be freely chosen. We parameterize these directions using 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

7 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-02.png)


**----- Start of picture text -----**<br>
Cross-tangent<br>Yi plane Uf Yi Uf<br>Z Xi Yf Z Xi Ti Yf Z Xi Ti Tf Yf<br>Xf<br>Xf Xf<br>Y Y Y<br>X X X<br>(a) Cylindrical envelope (b) Sample cross-tangent plane (c) Connection through an inter-<br>mediary sphere<br>**----- End of picture text -----**<br>


Fig. 7. Depiction of surfaces used to connect spheres at the initial and final configurations 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-04.png)


**----- Start of picture text -----**<br>
Center of a sphere<br>at final configuration Toc θoc<br>φoc<br>Center of a sphere x z<br>at initial configuration<br>Z OB θicTφicic h<br>Xoc ri y<br>Xic<br>O<br>Y<br>X<br>**----- End of picture text -----**<br>


Fig. 8. Notation for discretization of position and headings on a cylinder connecting two spheres 

We can obtain the axis of the cylinder that connects the selected pair of spheres as (refer to Fig. 7a) 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-07.png)


Furthermore, the length of the cylinder is given by _h_ = _∥_ **r** _f −_ **r** _i∥_ 2 _._ Since the radius of the cylinder is the same as the radius of the selected pair of spheres, the cylinder’s radius is _Rpitch_ if _δi,o[inner]_ = 0 and _Ryaw_ if _δl,r[inner]_ = 0 _._ 

We now derive expressions for the entry and exit points on the cylinder ( **X** _ic_ and **X** _oc_ ) as well as their corresponding tangent directions ( **T** _ic_ and **T** _oc_ ). 

four angles: _θic, ϕic, θoc,_ and _ϕoc._ The following section describes how the path on the spheres and the cylinder is constructed based on these four parameters. 

**Remark 6.** Since cylinders connect spheres of the same type, the cylinder always has the same radius as the spheres and thus does not expand or shrink. 

## _A. Origins of the Spheres and Axes of the Cylinders_ 

We begin by deriving expressions for the centers of the spheres at the initial and final configurations, denoted by **r** _i_ and **r** _f ,_ respectively. These vectors are given by 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-14.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-15.png)


## _B. Parameters for the location and tangent vector on the cylinder_ 

On the cylindrical envelope, we parameterize the entry point **X** _ic_ and the tangent **T** _ic_ by two angles, _θic_ and _ϕic_ (see Fig. 8). Likewise, _θoc_ and _ϕoc_ parameterize the exit point **X** _oc_ and the corresponding tangent **T** _oc_ . To derive these expressions, we introduce a body frame _B_ ( _OB, x, y, z_ ) centered at the cylinder’s base point **r** _i_ , with its _z_ -axis aligned along the cylinder axis (also shown in Fig. 8).[13] 

The expressions for **X** _ic_ and **X** _oc_ can be derived in the body frame _B_ to be 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-19.png)


where _R_ is the radius of the cylinder, and is given by 

Here, _δi,o[initial]_ = 1 _, −_ 1 or 0 depending on whether the inner sphere, outer sphere, or one of the left/right spheres is selected at the initial configuration, respectively. Similarly, _δl,r[initial]_ = 1 _, −_ 1 _,_ 0 if the left sphere, right sphere, or one of the inner/outer spheres is chosen. The same interpretation applies for _δi,o[final]_ and _δl,r[final] ._ For cylindrical envelope constructions, we require that _δ[initial]_ = _δ[final]_ and _δ[initial]_ = _δ[final]_ . _i,o i,o l,r l,r_ 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0007-22.png)


> 13Since the cylinder’s _z_ -axis is known, but the _x_ - and _y_ -axes of the body frame are not, we begin by aligning the _x_ -axis with the global _X_ -axis. We then apply Gram–Schmidt orthogonalization to compute a unit vector perpendicular to the _z_ -axis. If the dot product between the global _X_ -axis and the cylinder’s _z_ -axis is close to one (i.e., they are nearly aligned), we instead use the global _Y_ -axis to initialize the process. 

8 

IEEE TRANSACTIONS ON ROBOTICS 

We can derive the direction cosines of the tangent vector when it enters and exits the cylinder as (refer to Fig. 8) 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0008-03.png)


Here, **R** _z_ and **R** _x_ are standard _elementary rotation matrices_ for rotation about the _z_ and _x_ axis, respectively. 

The entry position **X** _ic_ and tangent direction **T** _ic_ in the global frame _G_ ( _O, X, Y, Z_ ) can be expressed as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0008-06.png)


where **x** _,_ **y** _,_ and **z** are unit vectors along the _x, y, z_ axes of the body frame _B,_ and _XOB , YOB , ZOB_ is the location of the body frame’s origin. Analogous expressions hold for **X** _oc_ and **T** _oc_ . 

With the expressions for the entry and exit locations and their corresponding tangent vectors on the cylindrical envelope now established, we proceed to construct the optimal path on the initial and final spheres, as well as on the cylindrical envelope. 

## _C. Generation of paths on initial and final spheres_ 

Consider the chosen sphere at the initial configuration. We need to obtain the optimal path connecting the initial configuration to the location **X** _[G] ic_[with][heading][direction][given] by **T** _[G] ic_[to][enter][the][cylindrical][envelope][(as][shown][in][Fig.][8).] We simplify this problem by translating the sphere’s center to the origin. This allows us to analyze the motion using a Sabban frame [24], [26]. The task becomes finding the optimal path on the sphere’s surface that connects an initial location **X** _sp,_ 0 and tangent **T** _sp,_ 0 to a final location and tangent. 

In [24], [26], the Sabban frame model was used to study motion planning on a _unit_ sphere. The configuration of the vehicle was specified by a location **X**[ˆ] _sp_ (which is a unit vector pointing radially outwards), a tangent vector **T** _sp_ along the longitudinal direction of the vehicle, and a normal vector **N** _sp_ along the lateral direction. Additionally, the path was parametrized in terms of arc length _s._ ˆ The evolution equations for these vectors are given by 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0008-12.png)


ˆ where _ug ∈_ [ _−U_[ˆ] _max, U_[ˆ] _max_ ] is the geodesic curvature on the unit sphere and serves as the control input. It relates to the minimum turning radius _r_ ˆ on the unit sphere by _r_ ˆ = 1 _._ ~~_√_~~ 1+ _U_[ˆ] _max_[2] We can adapt the previous results for motion planning on a sphere of any radius ( _R_ ) by scaling the problem to a 

unit sphere problem.[14] First, we compute the normal vector **N** _sp_ := _R_[1] **[X]** _[sp][×]_ **[T]** _[sp][.]_[ While scaling does not affect the tangent] vector **T** _sp_ or the normal vector **N** _sp_ , other parameters change. The location on the unit sphere becomes **X**[ˆ] _sp_ := _R_[1] **[X]** ˆ _[sp]_[,][and] the corresponding minimum turning radius becomes _r_ = _R_[1] _[r.]_ A detailed derivation of this scaling is available in Appendix C. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0008-15.png)


**----- Start of picture text -----**<br>
L segment (radius r )<br>L segment (radius r ˆ)<br>N sp, 0 N sp, 0 XZ Y G segment<br>X sp, 0 [T] [sp,] [0] X ˆ sp, 0 T sp, 0 G segment (radius R )<br>R segment (radius r ˆ)<br>R segment (radius r )<br>**----- End of picture text -----**<br>


Fig. 9. Motion planning on sphere with radius _R_ and on a unit sphere 

From [24], the candidate optimal paths on a unit sphere are of type _CGC, CCC_ for ˆ _r ≤_[1] 2 _[, CGC, CCCC,]_[ or a degenerate] path for[1] 2 _[<][r]_[ˆ] _[≤]_ ~~_√_~~ 12 _[,]_[and] _[CGC,][CCCCC,]_[or] _[CC][π][C]_[15][for] 1 ~~_√_~~ 3 _[r]_[ˆ] _[≤]_[The][analytical][computation][of][the][arc][angles] ~~_√_~~ 2 _[<]_ 2 _[.]_[16] for each path is provided in [27]. We note here that the arc angles of the segments of a path on the unit sphere and the corresponding path on the sphere with radius _R_ would be the same. Hence, we can obtain the arc angles of the segments for each candidate path on the sphere with radius _R_ using [27]. **Remark 7.** The arc angle _ϕ_ is related to the segment length _l_ ˆ by _l_ = _rϕ_ for _L_ and _R_ segments, and _l_ = _ϕ_ for a _G_ segment on a unit sphere. 

Finally, we want to obtain the expressions for **X** _sp,_ **T** _sp,_ and **N** _sp_ along the path to describe the instantaneous configuration of the vehicle along the sphere. We can obtain these expressions by solving the Sabban frame equations, derived in Appendix C, using the Euler-Rodriguez formula. Therefore, the configuration of the vehicle on the sphere along the path can be obtained. 

The last step to be performed is to obtain the configuration of the vehicle in 3D (which utilizes the rotation minimizing frame). Since we had shifted the origin of the sphere to 

> 14We note here that we perform this scaling since **X** _sp,_ **T** _sp,_ and **N** _sp_ do not form a rotation matrix as **X** _sp_ is not a unit vector. However, when the problem is scaled to motion planning on a unit sphere, these vectors form a rotation matrix; therefore, the path can be constructed easily. 

> 15 _Cπ_ refers to a _C_ segment (i.e., a left turn or right turn of minimum turning radius) with an arc angle of exactly _π_ radians. 

> 16The optimal path candidates for spherical motion planning with _r_ ˆ _> √_ 23 remain an open problem. It has been hypothesized that, as _r_ ˆ _→_ 1, an increasing number of path concatenations is required due to the progressively limited maneuverability of the vehicle, with the number of concatenations tending to infinity. 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

9 

coincide with the origin of the global frame _G,_ the location ( **X** ) and longitudinal direction ( **T** ) can be easily obtained as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0009-03.png)


Furthermore, depending on the type of sphere chosen at the initial configuration, **Y** and **U** can be computed (refer to Fig. 9). If _δi,o[initial]_ = 0 or _δl,r[initial]_ = 0 _,_ the expressions for **U** (the surface normal) and **Y** (the tangent normal) are obtained, respectively, as (refer to Figs. 4 and 9) 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0009-05.png)


When _δi,o[initial]_ = 0 _,_ **Y** = **U** _×_ **T** ; when _δl,r[initial]_ = 0 _,_ **U** = **T** _×_ **Y** _._ The path on the sphere at the final configuration is constructed similarly. 

## _D. Generation of path on cylinder_ 

In this section, we describe the construction of the optimal Dubins path on a cylindrical surface. This path connects an initial and final configuration on the cylinder, which we had previously parameterized in terms of _θic, ϕic, θoc,_ and _ϕoc._ The path we construct on the cylinder must obey the geodesic curvature (yaw rate) and normal curvature (pitch rate) constraints for the 3D model. We note that the radius of the cylinder is _R,_ whose definition is given in (11). We choose the bound on the geodesic curvature for motion over the cylinder to be 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0009-09.png)


We claim that the considered radius for the cylinder and the geodesic curvature bounds satisfy the geodesic curvature and normal curvature constraints for the 3D problem. 

**Lemma 3.** _The optimal path on a cylinder of radius R, defined in_ (11) _, with geodesic curvature bounds given by_ (15) _satisfies the geodesic curvature and normal curvature bounds for the proposed rotation minimizing frame model._ 

## _Proof._ The proof is provided in Appendix D. 

We present the construction of the optimal path on the cylinder. Note that geodesic curvature is bending invariant [28]. Hence, we can unwrap the cylinder onto a plane, as shown in Fig. 10, and construct the optimal path on the plane. Finally, the constructed path on the plane can be wrapped back onto the cylinder. 

_1) Unwrapping frame for cylinder:_ For unwrapping the cylinder, we consider a frame _U,_ referred to as the unwrapping frame, with axes _xU , yU ,_ and _zU_ . The origin for _U_ is at the point of entry of the cylinder ( **X** _ic_ ). Furthermore, _zU_ is parallel to _z_ and _yU_ points radially inwards to the cylinder. We will use the unwrapping frame for constructing the path on the plane. Once we construct such a path, we will represent it in the body frame _B,_ and finally obtain the vehicle’s configuration in the global frame _G_ for the 3D problem. 

Consider a point _Q_ on the cylinder. The relationship between its location in the unwrapping frame ( **X** _[U] Q_[) and the body] frame ( **X** _[B] Q_[)][is][given][by][17] 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0009-16.png)


**----- Start of picture text -----**<br>
− sin  θic − cos  θic 0 R  cos  θic<br>X [B] Q [=]  cos  θic − sin  θic 0 X [U] Q [+]  R  sin  θic  .<br> 0 0 1  0 <br>(16)<br>Toc z Toc z Unwrappingplane (tan-<br>φoc gent plane<br>θoc at entry<br>location)<br>zU Tic zU Tic<br>φic<br>yU y yU y<br>xU xU<br>θic<br>x x<br>(a) Unwrapping (b) Unwrapping plane chosen<br>frame chosen<br>**----- End of picture text -----**<br>


Fig. 10. Frames on the cylinder and the unwrapping plane chosen for the cylinder 

Using (16), we can represent the entry location **X** _ic_ and the exit location **X** _oc_ in the unwrapping frame _U_ as **X** _[U] ic_[=] (0 _,_ 0 _,_ 0) _[T]_ and **X** _[U] oc_[= (] _R_ sin ( _δθ_ ) _, R_ (1 _−_ cos ( _δθ_ )) _, h_ ) _[T] ._ Here, the expression for **X** _[B] oc_[from (10) was used, and] _[ δθ]_[:=] _[ θ][oc][−][θ][ic][.]_ 

We now aim to unwrap the cylindrical surface onto a plane, selecting the tangent plane at **X** _ic_ as reference. Therefore, the unwrapping plane is defined by _xU_ and _zU_ axes, as shown in Fig. 10b. We will now describe the mapping of the initial and final configurations of the cylinder to the unwrapping plane. 

_2) Configurations after unwrapping cylinder:_ Consider unwrapping a point on the cylinder as shown in Fig. 11. A point _P,_ whose coordinates are ( _R_ sin ( _δθ_ ) _, R_ (1 _−_ cos ( _δθ_ )) _, δd_ ) in _U,_ gets mapped to two points on the plane due to periodicity of the angle _δθ ∈_ ( _−π, π_ ][18] . Hence, the two images of _P_ obtained on the plane, shown in Fig. 11, are given by _P_ 1( _Rθ_ 1 _, δd_ ) and _P_ 2( _Rθ_ 2 _, δd_ ) _,_ where 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0009-21.png)


The two images corresponding to the final configuration, which is the exit location of the cylinder, obtained on the unwrapping plane, are shown in Fig. 12. It can be observed that the heading angles for the entry and exit locations are _ϕic_ and _ϕoc_ on the plane, respectively (compare with Fig. 10). 

> 17For motion planning on a cylinder where the initial location (equivalent to the origin of _U_ ) is not in the _xy_ plane, the last term in (16) can be replaced with ( _R_ cos _θic, R_ sin _θic, dic_ ) _[T] ._ Here, _dic_ is the distance from the _xy_ plane. 

> 18In principle, there are infinitely many images due to the periodicity of the angle _δθ._ However, we consider only two images for simplicity. 

10 

IEEE TRANSACTIONS ON ROBOTICS 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0010-02.png)


**----- Start of picture text -----**<br>
yU<br>P (R sin δθ, R(1 − cos δθ), δd)<br>δθ − 2π<br>δθ<br>P1(Rθ1, δd)<br>xU<br>P2(Rθ2, δd) x y<br>11. Unwrapping point lying on the cylinder<br>z<br>Toc<br>Toc,unwrapped<br>φoc<br>φoc<br>zU Tic<br>φic<br>yU y<br>xU<br>x<br>**----- End of picture text -----**<br>


Fig. 11. Unwrapping point lying on the cylinder 

Fig. 12. Initial configuration and two images of the final configuration obtained on the unwrapping plane 

We can now plan the optimal path to each image of the final configuration on the plane. To this end, we generate the six 2D Dubins candidate paths ( _CSC_ and _CCC_ ) using the analytical expressions provided in [29] to each image, and pick the shortest path. Let this shortest path be 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0010-06.png)


where _s_ is the arc length. Additionally, let the instantaneous heading angle on the plane be _ψ_ ( _s_ ) _,_ which is the angle made with respect to _xU ._ 

_3) Wrapping path onto cylinder:_ After the path is generated on the unwrapped plane, the corresponding path on the cylinder is retrieved by inverse mapping. To this end, consider a point given by ( _Rθ, d_ ) on the unwrapping plane. The corresponding image of this point on the cylinder will be ( _R_ sin _θ, R_ (1 _−_ cos _θ_ ) _, d_ ) in _U_ using the previously established procedure (refer to Fig. 11). 

Now, consider the curve on the plane given by (18). Using the previous argument, the corresponding curve obtained on the cylinder in the unwrapping frame _U_ is given by 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0010-10.png)


We now prove that the proposed mapping preserves the length of the curve. 

**Lemma 4.** _The proposed mapping between a planar curve and the wrapped curve on the cylindrical surface preserves the length of the curve._ 

_Proof._ The proof is provided in Appendix E. 

Using (16), the equation of the considered curve in (19) can be obtained in the body frame _B_ as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0010-15.png)


We compute the tangent vector along the path using the instantaneous heading angle _ψ_ ( _s_ ) obtained from the 2D Dubins path on the _xU zU_ plane. Hence, the angle made by **T** in the unwrapped plane with respect to _xU_ , which is the heading angle, is known (refer to Fig. 12). From Fig. 10a, the direction cosines of **T** expressed in the body frame can be obtained as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0010-17.png)


If the inner or outer sphere was chosen at the initial configuration, the expression for **U** in _B_ can be obtained by noting that it is radially outwards or inwards to the cylinder, as (refer to Fig. 7a) 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0010-19.png)


Alternatively, if the left or right spheres were chosen, the same expression for **Y** _[B]_ is obtained with _δi,o[initial]_ replaced with _δl,r[initial] ._ The expression for **Y** when _δi,o[initial]_ = 0 and **U** when _δ[initial]_ = 0 can be obtained as **Y** _[B]_ = **U** _[B] ×_ **T** _[B]_ and _l,r_ **U** _[B]_ = **T** _[B] ×_ **Y** _[B] ,_ respectively. 

Finally, the expressions for **X** _,_ **T** _,_ **Y** _,_ and **U** can be obtained in the global frame _G_ using (12) and (13) (refer to Fig. 8)[19] . Hence, we have obtained the configuration of the vehicle along the shortest path on the cylinder for chosen _θic, ϕic, θoc,_ and _ϕoc_ values; this path satisfies the pitch and yaw rate constraints of the vehicle. 

**Remark 8.** Though four parameters were introduced for path construction using a cylindrical envelope in the beginning of Section IV, the initial and final sphere computations depend only on two parameters each ( _θic_ and _ϕic,_ or _θoc_ and _ϕoc_ ). Furthermore, the motion planning on the cylinder depends on _ϕic, ϕoc,_ and the difference between _θic_ and _θoc._ 

To compute the best feasible path for a selected pair of spheres at the initial and final configuration, we discretize _θic_ and _θoc_ in [0 _,_ 2 _π_ ) _._ We discretize _ϕic_ and _ϕoc_ over the interval [0 _, π_ ], representing the feasible interval of heading angles that allow the path to enter the cylinder at **X** _ic_ and exit at **X** _oc_ (refer to Fig. 8). The number of discretizations of _θic_ and _θoc_ are determined by a parameter _θdisc,_ whereas _ϕdisc_ dictates the number of discretizations for _ϕic_ and _ϕoc_ . We choose the combination that yields the shortest feasible path. 

> 19Similar to the transformation for the tangent vector in (13) between the body and global frames, equations for the tangent-normal and surface-normal vectors can be obtained. 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

11 

## V. CONSTRUCTING FEASIBLE SOLUTION USING CROSS-TANGENT PLANE 

In this section, we describe the second class of paths where the sub-path between the initial and final spheres is constructed on a cross-tangent plane. There exist infinitely many crosstangent planes between these two spheres; the locus of the point of intersection of these cross-tangent planes with the initial/final sphere will be a circle, as shown in Fig. 13. To uniquely define a cross-tangent plane, we use angle _θ_ as a parameter (see Fig. 13). 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-04.png)


**----- Start of picture text -----**<br>
Rpitch<br>t Ticφic Cross-tangent<br>plane<br>Yi Uf<br>Z ri Xic Ti Yf<br>Xi<br>Xf<br>rf<br>Y Xoc<br>X Toc<br>φoc<br>**----- End of picture text -----**<br>


Fig. 13. Parameterization of family of planes and configurations at entry and exit from cross-tangent plane 

**Remark 9.** From Fig. 13, we can observe that the considered cross-tangent plane exists when _∥_ **r** _f −_ **r** _i∥_ 2 _≥_ 2 _R,_ i.e., when the spheres at the initial and final configurations do not intersect. 

We denote the center of the locus at the initial and final spheres by **A** and **B** , respectively, as shown in Fig. 13. The location of **A** and **B** can be obtained as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-08.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-09.png)


2 _R_ where _α_ := cos _[−]_[1][ �] _∥_ **r** _f −_ **r** _i∥_ 2 �. Here, the expressions for **r** _i_ and **r** _f_ are given in (7) and (8), respectively, and _R_ is given in (11). The cross-tangent plane between the initial and final spheres is needed for inner-outer, outer-inner, left-right, and right-left pairings. It follows that _δi,o[initial]_ = _−δi,o[final]_ and _δ[initial]_ = _−δ[final] . l,r l,r_ 

To define the parameter _θ_ , we first designate a unit vector **x** perpendicular to **r** _f −_ **r** _i_ , as shown in Fig. 13.[20] The angle _θ_ specifies the point of tangency on the initial sphere, with respect to **x** . In other words, _θ_ describes the point of intersection of the cross-tangent plane with the circular locus of cross-tangent planes (shown in green) on the initial sphere; since the point of tangency is on the circular locus and **x** lies 

> 20The generation of **x** is similar to the procedure described for the cylindrical envelope. 

on the circular locus, _θ,_ which is measured as the angle from **x** _,_ uniquely describes the point. We then define another unit vector **y** := � _∥_ **rr** _ff −−_ **rr** _ii∥_ 2 � _×_ **x** , which is orthogonal to both **x** and the axis ( **k** , defined in (9)) between the spheres. Using **x** and **y** , we now express the entry and exit points **X** _ic_ and **X** _oc_ , which are the points of tangency (see Fig. 13). 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-14.png)


Next, we parameterize the tangent vectors at the entry and exit points using angles _ϕic_ and _ϕoc_ , defined relative to the axis **t** , where **t** is a unit vector pointing from **X** _ic_ ( _θ_ ) to **X** _oc_ ( _θ_ ) (see Fig. 13). The tangent vectors **T** _ic_ and **T** _oc_ at the entry and exit points are derived as below: 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-16.png)


Given the location and tangent vectors at the exit point from the initial sphere and the entry point of the final sphere, we can construct the optimal path over each sphere using the approach in Section IV-C. We can also construct the path on the crosstangent plane using the 2D Dubins result [3], [29], illustrated in Fig. 14. In this figure, the minimum turning radius _Rplane_ is dictated by the type of spheres considered at the initial and final configurations. If we are considering inner-outer or outerinner connections, _Rplane_ = _Ryaw_ since the vehicle moves in the **T** _−_ **Y** plane (as observed from Fig. 13). Alternatively, _Rplane_ = _Rpitch_ if left-right or right-left sphere connections are considered. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-18.png)


**----- Start of picture text -----**<br>
Cross-tangent plane<br>−1<br>�R�  (Xic − ri) × t<br>φoc<br>φic<br>(0, 0) t<br>Rplane ∥rf − ri∥ [2] − 4R 2 , 0<br>�� �<br>**----- End of picture text -----**<br>


Fig. 14. Configurations on cross-tangent plane 

After the path on the plane is constructed, the vehicle’s coordinates ( _u_ and _v_ ) and the heading angle ( _ψ_ ) are defined. We can reconstruct the configuration of the vehicle along the path in 3D. First, we compute the location and the tangent vector along the plane as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-21.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0011-22.png)


12 

IEEE TRANSACTIONS ON ROBOTICS 

The vectors **U** and **Y** are computed depending on _δi,o[initial]_ = 0 or _δl,r[initial]_ = 0 _,_ as shown below: 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-03.png)


Further, we can compute these vectors as **Y** = **U** _×_ **T** when _δi,o[initial]_ = 0 _,_ and **U** = **T** _×_ **Y** when _δl,r[initial]_ = 0. Thus, the vehicle’s configuration in 3D is completely described on the initial sphere, cross-tangent plane, and final sphere. Note that the path construction for this class is a function of the three parameters: _θ, ϕic,_ and _ϕoc_ . However, motion planning on each of the surfaces depends only on two parameters. We optimize on these parameters by discretizing _θ ∈_ [0 _,_ 2 _π_ ) _,_ and _ϕic_ and _ϕoc_ in � _−[π]_ 2 _[,][π]_ 2 � (refer to Fig. 13). The number of discretizations of _θ_ is dictated by _θdisc,_ whereas _ϕdisc_ represents the number of discretizations for _ϕic_ and _ϕoc_ . We choose the parameter set that yields the shortest path length for each pairing of the initial and final spheres. 

## VI. CONSTRUCTING FEASIBLE SOLUTION USING INTERMEDIARY SPHERE 

In this section, we present the construction of the third class of paths. When the initial and the final positions are sufficiently close, we construct a path that goes through an intermediary spherical surface. We consider the four possible combinations in this regard, as outlined in Section III. This class of paths exists only when the Euclidean distance between the initial and final position satisfies _∥_ **r** _f −_ **r** _i∥_ 2 _≤_ 4 _R_ , as illustrated in Fig. 7c. 

We parameterize the center of the intermediary sphere using a parameter _α_ . The locus of the center of the intermediary sphere is a circle, as shown in Fig. 15. The value of _α_ is related to the radius of this circular locus, and can be derived to be 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-08.png)


and the radius of the circular locus is 2 _R_ sin _α._ 

To parameterize the center of the intermediary sphere, we generate a unit vector **x** perpendicular to **r** _f −_ **r** _i_ (similar to the one in Section IV). We define _θ ∈_ [0 _,_ 2 _π_ ) as the angle made by the center of the intermediary sphere on the circular locus with respect to **x** _,_ similar to the definition for the crosstangent plane case. This parameter specifies the location of the intermediary sphere. Hence, we can define the center of the intermediary sphere as (refer to Fig. 15) 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-11.png)


Given **X** _c_ , entry point ( **X** _ic_ ) and exit point ( **X** _oc_ ) for the intermediary sphere are derived as shown below, 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-13.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-14.png)


**----- Start of picture text -----**<br>
Xic − ri Xoc − rf<br>R α tan (α)xoc<br>R rf −ri R<br>cos (α) ∥rf −ri∥2<br>Z<br>ri Xc rf<br>Xi<br>Xf<br>Y<br>X<br>**----- End of picture text -----**<br>


Fig. 15. Parameterization of the locus of intermediary spheres and the configurations at entry and exit from the intermediary sphere. (Note that, instead of the vectors **x** _ic_ and **x** _oc_ , we show the same vectors scaled by _R_ tan( _α_ ).) 

Finally, to parameterize the tangent vectors at **X** _ic_ and **X** _oc_ , we define the unit vectors **x** _ic_ and **x** _fc_ . These vectors are perpendicular to **X** _ic−_ **r** _i_ and **X** _oc−_ **r** _f ,_ as illustrated in Fig. 15, and are derived as follows: 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-17.png)


We parameterize the tangent vectors at **X** _ic_ and **X** _oc_ denoted by **T** _ic_ and **T** _oc_ respectively, using the parameters _ϕic_ and _ϕoc,_ as shown below: 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0012-19.png)


We optimize the path length over the parameters _θ ∈_ [0 _,_ 2 _π_ ) _, ϕic ∈_ [0 _,_ 2 _π_ ) _,_ and _ϕoc ∈_ [0 _,_ 2 _π_ ). For a given set of parameters, we can compute **X** _ic,_ **X** _oc,_ **T** _ic,_ and **T** _oc_ . Similar to the methodology in Section IV-C, we generate the optimal path on the initial sphere, intermediary sphere, and the final sphere. Note that motion planning on each of the surfaces depends only on two parameters. For instance, in the case of the intermediary sphere, the path length depends only on _ϕic_ and _ϕoc_ . Similar to the path construction using an intermediary plane, _θdisc_ dictates the number of discretizations of _θ_ and _ϕdisc_ represents the number of discretizations for _ϕic_ and _ϕoc_ . Finally, among all the combinations of the discretized parameter values, we select the path with the minimal total length. 

## VII. SUMMARY OF PATH CONSTRUCTION ALGORITHM 

In this section, we summarize the path construction comprising the three classes of paths, presented in Sections IV, V, and VI as a pseudocode in Algorithm 1. 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

13 

The initial configuration and final configuration, each of which is defined by the four vectors **X** _,_ **T** _,_ **Y** _,_ and **U** _,_ are the inputs to the algorithm. We compactly represent them by the homogeneous transformation matrices **H** 0 and **H** _f ,_ respectively.[21] The other inputs to the algorithm include the pitch rate (captured by _Rpitch_ ), yaw rate (captured by _Ryaw_ ), and the discretization parameters, ( _θdisc_ and _ϕdisc_ ). Recall that _θdisc_ and _ϕdisc_ are the discretization parameters corresponding to the position and the heading, respectively (which were discussed in Sections IV, V, and VI). 

In line 1 of the algorithm, the minimum cylinder path is computed, which constructs the shortest path through an intermediary cylindrical envelope (described in Section IV). The function returns the length of the shortest path and the configuration of the vehicle along the path. Similarly, paths through a cross-tangent plane (described in Section V) and through an intermediary sphere (described in Section VI), are constructed in lines 2 and 3, respectively. Finally, the shortest of all the three classes of paths is determined in line 4, and the configuration of the vehicle along the shortest path is returned by the algorithm. 

## **Algorithm 1** Path construction algorithm for 3D Dubins 

**Input: H** 0 _,_ **H** _f , Rpitch, Ryaw, θdisc, ϕdisc_ 

   - _/* Computing the shortest path through cylindrical envelope */_ 

- 1: _lSCS,_ **H** _SCS ←_ MinimumCylinderPath( **H** 0 _,_ **H** _f , Rpitch, Ryaw, θdisc, ϕdisc_ ) _/* Computing the shortest path through cross-tangent plane */_ 

- 2: _lSP S_ , **H** _SP S ←_ MinimumPlanePath( **H** 0 _,_ **H** _f , Rpitch, Ryaw, θdisc, ϕdisc_ ) _/* Computing the shortest path through intermediary spherical envelope */_ 

- 3: _lSSS_ , **H** _SSS ←_ MinimumSpherePath( **H** 0 _,_ **H** _f , Rpitch, Ryaw, θdisc, ϕdisc_ ) 

   - _/* Computing the shortest overall path */_ 

- 4: _l[∗] ,_ **H** _[∗] ←_ MinimumLength ( **H** _SCS_ , **H** _SP S_ , **H** _SSS_ ) 5: **return** _l[∗]_ , **H** _[∗]_ 

**Remark 10.** If an existence condition is violated for a candidate path (such as an inner sphere – plane – outer sphere connection), its path length is returned as NaN. The functions MinimumPlanePath and MinimumSpherePath select the shortest path among those with finite length for each path type. Notably, _SCS_ paths always exist. If no valid path exists for a particular connection type (e.g., _SPS_ ), the corresponding function (such as MinimumPlanePath) returns NaN. Since the MinimumLength function considers only paths with finite length, any non-existent paths are automatically ignored. 

configuration and the motion constraints on the path. To this end, we consider the scenarios provided in [21], where five “Long” and five “Short” instances were considered depending on the distance between the initial and final configurations. The minimum turning radius was chosen to be 40 m in [21], and correspondingly, we consider _Rpitch_ = 40 m. In [21], the orientation is defined by only the pitch and heading angles. To describe the complete orientation, we additionally specify the roll angle at the initial and final positions to be one of the values from the set _{−_ 15 _[◦] ,_ 0 _[◦] ,_ 15 _[◦] }_[22] . To study the effect of the motion constraints, we run the experiments for different values of _Ryaw ∈{_ 30 m _,_ 40 m _,_ 50 m _}_ . 

Furthermore, we consider two sets of scenarios referred to as “Additional 1” and “Additional 2” described shortly, based on Figs. 2a and 2b, respectively. In the first set of scenarios, the vehicle needs to perform a turn maneuver with a marginal altitude change. The initial location is (120 _,_ 40 _,_ 20) with initial heading and pitch angles of 90 _[◦]_ and _−_ 5 _[◦] ,_ and the final location is (300 _,_ 40 _,_ 15) with heading and pitch angles of _−_ 90 _[◦]_ and _−_ 5 _[◦]_ . In “Additional 2”, the vehicle needs to perform an ascent maneuver from an initial location of (120 _,_ 40 _,_ 20) with initial heading and pitch angles of 90 _[◦]_ and _−_ 15 _[◦]_ to a final location of (130 _,_ 120 _,_ 41) with heading and pitch angles of 85 _[◦]_ and 20 _[◦]_ .[23] 

In addition to considering the algorithm from [21], we also use the path construction methodologies described in [13] and [30]; the latter implementation utilizes the model proposed in [18]. The implementation for the former algorithm is available on the GitHub page of the authors (link in [13]). For the algorithm from [13], since only a single turning radius parameter is used, we set _R_ = _Rpitch_ = 40 m.[24] For the implementation in [30], we select the maximum roll rate so that the turning radius matches 40 m (which is our _Rpitch_ ), and retain the default bounds for the maximum flight path angle of _±_ 0 _._ 5 radians. We note that the model considered in [30], which implements [18], utilizes the initial and final heading angles, rather than the full heading vector. 

For Algorithm 1, to optimize the path length with respect to the parameters, we consider 15 discretizations for all parameters that describe the positions and tangent vectors for entry and exit between the intermediary surfaces. We implemented the algorithms in Python 3 _._ 8 on a computer with AMD Ryzen 9 5900HS CPU running at 3 _._ 30 GHz with 16 GB RAM. For all the classes of the paths constructed, we parallelized the functions that compute the sub-paths on each 

> 22It should be noted that the orientation of the vehicle can be uniquely prescribed by the vectors **T** _,_ **Y** _,_ and **U** _,_ or by specifying the yaw (rotation about _z_ ), pitch (rotation about _y_ ), and roll (rotation about _x_ ) angles. Fixing a _ZY X_ rotation sequence, one can uniquely compute the expressions for **T** _,_ **Y** _,_ and **U** for given angles. It should be noted that positive pitch angle is considered to be about _−y_ axis since geometrically, when the vehicle has its nose pointing up, the pitch angle is desired to be considered to be positive. 

> 23All coordinates specified in this paragraph are in meters. 

## VIII. RESULTS 

In this section, we present computational results to study the performance of Algorithm 1 and the effect of the vehicle’s 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0013-21.png)


> 24In this implementation, the turning radius is assumed to be 1, and the initial heading vector is aligned with the _z_ -axis. Thus, for all of our instances, we scale down the problem and use coordinate transforms to align the initial location with the origin and the initial heading vector with the + _z_ -axis. With this scaled instance, the code provided by the authors can be used to construct the _CSC_ paths. In our implementation, we supply the code for scaling down the problem, and for recovering the _CSC_ path for the original problem instance using the authors’ parameters. 

14 

IEEE TRANSACTIONS ON ROBOTICS 

individual surface. The computational results of the algorithm are summarized in Table I.[25] 

In Table I, we show the length of the path obtained using the three benchmarking algorithms under the instance name. For the implementation in [21], we consider the same parameter values used by the authors, which are a minimum turning radius of 40 m and a bounded pitch angle in [ _−_ 15 _[◦] ,_ 20 _[◦]_ ]. From this table, we can observe that 

- The path lengths obtained from our model are comparable to those from [21], [13], and [30] for all “Long” maneuvers. In particular, our path length is shorter for a majority of “Long 2”, “Long 3”, “Long 4”, and “Long 5” instances. The generated paths satisfy both pitch and yaw rate constraints while connecting the initial and final configurations, which include the vehicle’s roll angle. 

- For “Short” maneuvers, the length of the paths generated by the proposed algorithm is two to three times shorter than the path obtained from [21], while remaining comparable to the paths from [13] and [30]. On a few of the maneuvers, [30] yields larger path lengths due to constraints on the flight path angle. 

- The computation time is around 10 seconds for most of the instances. 

These results show the impact of the model and the control inputs on the resulting trajectory. We further expand upon these results to showcase the effect of the motion constraints and the configurations in the following subsections, along with additional examples. 

## _A. Effect of motion constraints_ 

From Table I, we can observe that increasing _Ryaw_ changes the path length and also the best feasible path type. For instance, consider the “Short 4” instance with initial and final roll angles of 15 _[◦]_ and _−_ 15 _[◦] ,_ respectively. The path generated for _Ryaw_ = 30 m, 40 m, and 50 m is illustrated in Fig. 16. We can observe that increasing _Ryaw_ from 40 m to 50 m changes the path obtained from our algorithm from a cross-tangent connection to a path through the left spheres at the initial and final configurations connected by a cylinder. Additionally, while increasing _Ryaw_ from 30 m to 40 m retains the same path type as the best path, the points of departure and arrival at the initial and final spheres have changed significantly. This is because _Ryaw_ particularly affects the turning capability of the vehicle on the cross-tangent plane, as can be observed from Figs. 16a and 16b. 

For an instance of the “Short 4” case where the path length is around 400 m, the change in path length is around 50 to 70 m when _Ryaw_ is varied. The effect of _Ryaw_ is more pronounced for “Additional 2”, where the vehicle needs to perform an ascent motion. For this instance, the path length may vary from 100 m to as high as 280 m depending on _Ryaw._ An illustration of the paths for increasing _Ryaw_ from 30 m to 50 m is shown in Fig. 17. 

> 25The first instance of running each function takes a higher time than the reported times in Table I, due to the overheads associated with spawning different processes to implement the functions in a parallel manner. To circumvent this issue, we “warm start” our algorithm using a dummy instance. 

These effects may not be captured by the existing models, including [21], [13], and [30], due to the single control input considered in these models. Illustrations of the paths obtained using the results from [21], [13], and [30] for the scenarios “Short 4” and “Additional 2” are shown in Figs. 18 and 19, respectively. We note that the path obtained from [30] utilizes a helical segment followed by a left turn, straight line segment, and another left turn to construct the path for “Short 4” in Fig. 18. Additionally, since the full heading vector is not considered in [30], it yields a starkly different path, which enters the pitch sphere and hence violates the pitch rate constraint, unlike the other two algorithms for “Additional 2”. 

## _B. Effect of considering complete configuration_ 

From Table I, we can observe that the roll angle at the initial and final locations impacts the path length and the path type as well. For instance, consider “Long 1” with _Ryaw_ = 40 m. We illustrate the change in the path type with changing roll angles across the three subfigures in Fig. 20. We observe that for initial and final roll angles of _−_ 15 _[◦]_ and 0 _[◦] ,_ the vehicle travels on the outer sphere, followed by traveling on the cross-tangent plane and an inner sphere. However, changing the initial and final roll angles changes the minimum cost path from our algorithm to travel along a cylindrical envelope connecting the left spheres for initial and final roll angles of 0 _[◦]_ and 15 _[◦] ._ For initial and final roll angles of 15 _[◦]_ and _−_ 15 _[◦] ,_ the best feasible path is a cylindrical envelope connecting inner spheres. 

In contrast, the paths obtained from [21], [13], and [30] are shown in Fig. 21. All three algorithms will produce the same path for any values of _Ryaw_ and for any of the three combinations of initial and final roll angles we considered in this subsection. This is due to the fact that the generated path does not account for the complete orientation of the vehicle at the initial and final locations; this highlights the novelty of our approach considering the full orientation of the vehicle. 

We also note here that all the paths satisfy the pitch and yaw rate constraints close to the initial configuration when _Ryaw_ = 40 m. However, the paths from [21] and [30] violate the yaw rate constraints at the initial configuration for _Ryaw_ = 50 m, while the path from [13] violates for _Ryaw_ = 53 m, since they enter the left sphere (similar to Fig. 2a). These results reaffirm the importance of the model and control inputs presented in the current paper. 

## _C. Additional examples_ 

In addition to the previous instances, we consider two additional instances. First, we consider an instance where the final location is inside the “inner” sphere of the vehicle, i.e., one of the pitch spheres. In this instance, the vehicle needs to depart from the origin with a heading, pitch, and yaw angle of 30 _[◦] ,_ 10 _[◦] ,_ and 15 _[◦] ,_ respectively. The desired final location is (5 _,_ 10 _,_ 15) with a desired heading, pitch, and yaw angle of 190 _[◦] ,_ 10 _[◦] ,_ and _−_ 15 _[◦] ,_ respectively. Furthermore, we chose _Rpitch_ and _Ryaw_ to be 40 m and 50 m, respectively. The minimum cost path obtained using Algorithm 1 and from the three benchmarking algorithms are shown in Figs. 22a and 22b, respectively. From our algorithm, the vehicle leverages 

15 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

TABLE I 

SUMMARY OF BEST FEASIBLE PATH AND COMPUTATION TIME FOR DIFFERENT INSTANCES WITH VARYING INITIAL ROLL ANGLE, FINAL ROLL ANGLE, AND _Ryaw._ PATH LENGTH OBTAINED USING ALGORITHMS FROM [21], [13], AND [30] ARE SHOWN UNDER THE INSTANCE NAME. IN THE TABLE, _S_ DENOTES A SPHERE, _C_ DENOTES A CYLINDER, AND _P_ DENOTES A PLANE. FOR SPHERES, SUBSCRIPTS _i, o, l,_ AND _r_ REPRESENT THE INNER SPHERE, OUTER SPHERE, LEFT SPHERE, AND RIGHT SPHERE, RESPECTIVELY. 

|**Inst.**|**Roll**~~_∗_~~<br>**(**_◦_**,**_◦_**)**|_Ryaw_<br>**(m)**|**Length**<br>**(m)**|**Path**<br>**type**|**Time**<br>**(s)**||**Inst.**|**Roll**~~_∗_~~<br>**(**_◦_**,**_◦_**)**|_Ryaw_<br>**(m)**|**Length**<br>**(m)**|**Path**<br>**type**|**Time**<br>**(s)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Long 1<br>446.04 [21]<br>437.86 [13]<br>445.10 [30]|(_−_15_,_0)|30|478.06|_SrPSl_|9.91||Short 2<br>668.17 [21]<br>281.96 [13]<br>506.05 [30]|(_−_15_,_0)|30|302.02|_SoPSi_|9.54|
|||40|510.64|_SoPSi_|9.60||||40|323.47||9.34|
|||50|533.24||9.77||||50|356.72||9.50|
||(0_,_15)|30|475.98|_SrPSl_|9.87|||(0_,_15)|30|298.45||9.59|
|||40|412.17|_SlCSl_|10.17||||40|313.69||9.33|
|||50|545.09|_SrPSl_|10.46||||50|335.89||9.51|
||(15_, −_15)|30|447.36|_SiCSi_|9.68|||(15_, −_15)|30|313.70||9.44|
|||40|470.08||9.53||||40|336.86||9.79|
|||50|473.59||9.87||||50|349.95||10.14|
|Long 2<br>638.45 [21]<br>631.73 [13]<br>637.22 [30]|(_−_15_,_0)|30|587.86|_SrCSr_|9.72||Short 3<br>976.79 [21]<br>342.52 [13]<br>521.46 [30]|(_−_15_,_0)|30|364.92|_SoPSi_|9.83|
|||40|606.64||9.66||||40|386.80||9.37|
|||50|614.57||9.90||||50|400.55||9.62|
||(0_,_15)|30|590.12||12.03|||(0_,_15)|30|356.75||9.49|
|||40|601.87||10.29||||40|368.52||9.37|
|||50|620.67||10.87||||50|384.82||10.03|
||(15_, −_15)|30|583.47||10.18|||(15_, −_15)|30|349.90||10.84|
|||40|603.90||10.29||||40|416.92|_SrCSr_|10.29|
|||50|612.32||10.83||||50|408.28||9.79|
|Long 3<br>1068.34 [21]<br>1059.20 [13]<br>1054.19 [30]|(_−_15_,_0)|30|1032.72|_SiCSi_|10.97||Short 4<br>1169.80 [21]<br>422.26 [13]<br>625.75 [30]|(_−_15_,_0)|30|425.17|_SlCSl_|9.77|
|||40|1141.58||10.90||||40|425.65||9.53|
|||50|1161.82|_SlCSl_|11.23||||50|421.25||9.75|
||(0_,_15)|30|1026.87|_SiCSi_|11.30|||(0_,_15)|30|420.89||9.94|
|||40|1045.90||11.14||||40|422.72||9.47|
|||50|1048.38||11.30||||50|447.19||9.68|
||(15_, −_15)|30|1037.06||11.06|||(15_, −_15)|30|445.42|_SoPSi_|9.62|
|||40|1040.40||10.91||||40|493.81||9.55|
|||50|1058.79||12.67||||50|512.31|_SlCSl_|9.84|
|Long 4<br>1788.80 [21]<br>1784.85 [13]<br>1787.15 [30]|(_−_15_,_0)|30|1744.87|_SlCSl_|11.52||Short 5<br>1362.91 [21]<br>437.46 [13]<br>730.04 [30]|(_−_15_,_0)|30|444.24|_SoPSi_|9.62|
|||40|1758.23||12.05||||40|463.42||9.53|
|||50|1773.09||11.29||||50|477.80||9.66|
||(0_,_15)|30|1747.76||10.65|||(0_,_15)|30|440.33||9.60|
|||40|1759.44||10.60||||40|446.09||9.33|
|||50|1776.86||10.65||||50|520.75|_SlCSl_|9.77|
||(15_, −_15)|30|1744.13||10.87|||(15_, −_15)|30|453.28|_SrCSr_|9.66|
|||40|1763.51||10.86||||40|447.54||9.52|
|||50|1768.64||10.61||||50|467.20||9.88|
|Long 5<br>2214.54 [21]<br>2213.70 [13]<br>2208.70 [30]|(_−_15_,_0)|30|2187.58|_SrCSr_|10.91||Add. 1<br>225.89 [21]<br>225.67 [13]<br>225.72 [30]|(_−_15_,_0)|30|212.63|_SrCSr_|9.43|
|||40|2201.98||10.79||||40|223.18||9.83|
|||50|2211.11||11.00||||50|233.88||10.26|
||(0_,_15)|30|2189.22||11.17|||(0_,_15)|30|213.34||9.58|
|||40|2201.75||10.79||||40|223.83||10.00|
|||50|2212.44||11.14||||50|234.02||10.11|
||(15_, −_15)|30|2192.96||10.86|||(15_, −_15)|30|211.93||9.48|
|||40|2209.89||10.59||||40|222.00||9.85|
|||50|2225.56||11.04||||50|232.53||10.10|
|Short 1<br>580.79 [21]<br>299.34 [13]<br>312.87 [30]|(_−_15_,_0)|30|289.67|_SrCSr_|9.75||Add. 2<br>84.55 [21]<br>84.54 [13]<br>83.33 [30]|(_−_15_,_0)|30|107.59|_SlSrSl_|11.86|
|||40|376.88|_SoCSo_|9.47||||40|91.54||11.63|
|||50|394.71||9.72||||50|274.51|_SiCSi_|11.95|
||(0_,_15)|30|355.38|_SoPSi_|9.58|||(0_,_15)|30|87.17|_SiSoSi_|12.00|
|||40|375.31|_SrCSr_|9.54||||40|250.06|_SrSlSr_|11.52|
|||50|389.47||9.54||||50|280.35|_SiCSi_|12.07|
||(15_, −_15)|30|352.59|_SoCSo_|9.58|||(15_, −_15)|30|95.39|_SrSlSr_|11.82|
|||40|380.83|_SrCSr_|9.44||||40|259.63|_SiCSi_|11.61|
|||50|360.12|_SrSlSr_|10.18||||50|280.38|_SiPSo_|12.13|



> ~~_∗_~~ – Initial and final roll angles are specified as an ordered pair. 

the pitch and yaw rate bounds to make a sharper turn, leading to a path with a length of 253 _._ 36 m, which traverses through an intermediary sphere. On the other hand, due to the pitch angle bounds in [21], the vehicle takes a longer path of length 290 _._ 57 m. The algorithm [30] provides a comparable path length of 289 _._ 23 m, whereas [13] provides a much longer path with a length of 419 _._ 03 m. 

A similar result was obtained in the second instance, where 

the final location was chosen inside the right sphere (one of the yaw spheres). The initial configuration and vehicle parameters were chosen to be the same as the first instance, the final location is chosen to be (0 _, −_ 30 _,_ 5), and the desired final heading, pitch, and roll angles are 190 _[◦] ,_ 10 _[◦] ,_ and _−_ 15 _[◦] ,_ respectively. The path length from our algorithm was 257 _._ 27 m, whereas the path length with the algorithms from [21], [13], and [30] were 293 _._ 03 m, 391 _._ 13 m, and 290 _._ 63 m, respectively. 

16 

IEEE TRANSACTIONS ON ROBOTICS 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0016-02.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0016-03.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0016-04.png)


(a) _Ryaw_ = 30 m (path through inter(b) _Ryaw_ = 40 m (path through inter(c) _Ryaw_ = 50 m (path through intermediary cross-tangent plane) mediary cross-tangent plane) mediary cylindrical envelope) 

Fig. 16. Depiction of varying paths with _Ryaw_ for “Short 4” with initial roll angle of 15 _[◦]_ and final roll angle of _−_ 15 _[◦]_ and instantaneous configuration of the vehicle. Animations of a vehicle moving along these paths are available on our GitHub page. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0016-07.png)


(a) _Ryaw_ = 30 m (path through intermediary sphere envelope) 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0016-09.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0016-10.png)


(b) _Ryaw_ = 40 m (path through inter(c) _Ryaw_ = 50 m (path through intermediary cylindrical envelope) mediary cross-tangent plane) 

Fig. 17. Depiction of varying paths with _Ryaw_ for “Additional 2” with initial roll angle of 15 _[◦]_ and final roll angle of _−_ 15 _[◦]_ and instantaneous configuration of the vehicle. Animations of a vehicle moving along these paths are available on our GitHub page. 

**Remark 11.** We identified two key issues with state-of-the-art methods: (i) the generated path does not change with changing roll angle, and (ii) the use of a single turning radius constraint can lead to violations of one of the curvature constraints in our model. While we have illustrated these issues with a few examples, they are expected to persist across a broader range of scenarios. 

## _D. Impact of discretization of parameters_ 

Noting that the number of discretizations of the path parameters can be freely chosen, we performed a sensitivity study by varying them across 5, 10, 15, 20, and 25 values. For each setting, we obtained the best path using our algorithm for all instances and variations in _Ryaw_ and initial and final roll angles, as outlined in Table I. The results are summarized in Fig. 24, which shows both the change in shortest path lengths 

and the computation times across the 12 considered instances. For each instance, the nine variations ( _R_ yaw, initial, and final roll angles) are condensed into a box plot. 

From these figures, we observe that a smaller number of discretizations yields faster computation time, but typically at the expense of solution quality. This trend is consistent across all instances, and is especially apparent in “Additional 2.” From Fig. 24, 15 discretizations represent a good tradeoff between computation time and path length. Alternatively, using 10 discretizations provides solutions in approximately 5 seconds, compared to 10 seconds for 15 discretizations, albeit with some compromise in path quality. 

## IX. CONCLUSION 

In this paper, we propose a novel model for 3D motion planning and a methodology for generating high-quality feasible 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

17 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0017-02.png)


Fig. 18. Solutions from [21], [13], and [30] for “Short 4” 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0017-04.png)


Fig. 19. Solutions from [21], [13], and [30] for “Additional 2” 

trajectories. The proposed model and the approach address two key limitations of the existing methods: the incomplete representation of vehicle configuration, and inadequate modeling of the motion constraints. We highlight these issues using illustrative examples. To address these, we proposed a model using a rotation-minimizing frame to uniquely represent the vehicle’s configuration, and the model includes two control inputs corresponding to the pitch rate and yaw rate of the vehicle. We proved that the pitch rate and yaw rate bounds yield a total of four distinct spheres tangential to the vehicle’s configuration, _viz._ inner, outer, left and right, which represent temporarily inaccessible regions. 

We proposed three classes of curvature-constrained paths beginning and ending on the surface of the spheres, tangential to the initial and final configurations. The three classes differ in the transition mechanism from the initial to the final sphere. These transitions involve a path on the surface of a cylindrical envelope, a cross-tangent plane, or another spherical surface. 

Finally, we presented extensive computational experiments to evaluate the impact of the motion constraints and the vehicle’s configuration on the path length and the path classification. Additionally, a comparison of the proposed methodology with the algorithms in [21], [13], and [30] underscored the advantages of modeling with complete orientation. The proposed model and path generation methodology offer a novel perspective on the 3D motion planning problem. 

## REFERENCES 

- [1] Fixed Wing Drone: The Complete Guide for Professionals (Accessed Apr 2025). [Online]. Available: https://quantum-systems.com/blog/2025/02/05/fixed-wing-drone-guide/ #: _[∼]_ :text=Superior%20Range%20%26%20Coverage%3A%20The% 20design,to%20survey%20extensive%20landscapes%20quickly. 

- [2] What Is A Fixed Wing Drone? — Advantages And Uses Of Fixed Wing Drones (Accessed Apr 2025). [Online]. Available: https://uavsystemsinternational.com/blogs/drone-guides/ what-is-a-fixed-wing-drone-advantages-and-uses-of-fixed-wing-drones? srsltid=AfmBOorCTIkSZHuUP3N4YbgcjBHHJoqQUL wTsxMGUmw4nzJpJ1lvfb 

- [3] L. E. Dubins, “On curves of minimal length with a constraint on average curvature, and with prescribed initial and terminal positions and tangents,” _American Journal of Mathematics_ , vol. 79, 1957. 

- [4] L. S. Pontryagin, V. G. Boltyanskii, R. V. Gamkrelidze, and E. F. Mishchenko, _The mathematical theory of optimal processes_ . Interscience Publishers, 1962. 

- [5] X.-N. Bui, J.-D. Boissonnat, P. Soueres, and J.-P. Laumond, “Shortest path synthesis for dubins non-holonomic robot,” in _Proceedings of the 1994 IEEE International Conference on Robotics and Automation_ , 1994, pp. 2–7. 

- [6] E. Bakolas and P. Tsiotras, “The asymmetric sinistral/dextral markovdubins problem,” in _Proceedings of the 48h IEEE Conference on Decision and Control (CDC)_ , 2009, pp. 5649–5654. 

- [7] Y. Wang and Y. R. Zheng, “3-dimensional path planning for autonomous underwater vehicle,” in _OCEANS 2018 MTS/IEEE Charleston_ , 2018, pp. 1–6. 

- [8] H. Marino, M. Bonizzato, R. Bartalucci, P. Salaris, and L. Pallottino, “Motion planning for two 3D-Dubins vehicles with distance constraint,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2012, pp. 4702–4707. 

- [9] G. Ambrosino, M. Ariola, U. Ciniglio, F. Corraro, E. De Lellis, and A. Pironti, “Path generation and tracking in 3-d for uavs,” _IEEE Transactions on Control Systems Technology_ , vol. 17, no. 4, pp. 980– 988, 2009. 

- [10] R. Hurley, R. Lind, and J. Kehoe, “A mixed local-global solution to motion planning within 3-d environments,” in _AIAA Guidance, Navigation, and Control Conference_ , 2009. [Online]. Available: https://arc.aiaa.org/doi/abs/10.2514/6.2009-6297 

- [11] Y. Lin and S. Saripalli, “Path planning using 3D Dubins curve for unmanned aerial vehicles,” in _2014 International Conference on Unmanned Aircraft Systems (ICUAS)_ , 2014, pp. 296–304. 

- [12] H. Sussmann, “Shortest 3-dimensional paths with a prescribed curvature bound,” in _IEEE Conference on Decision and Control_ , 1995, pp. 3306– 3312. 

- [13] V. M. Baez, N. Navkar, and A. T. Becker, “An analytic solution to the 3D csc Dubins path problem,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 7157–7163. 

- [14] S. Hota and D. Ghose, “Optimal geometrical path in 3D with curvature constraint,” in _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2010, pp. 113–118. 

- [15] S. Hota and D. Ghose, “Optimal path planning for an aerial vehicle in 3D space,” in _49th IEEE Conference on Decision and Control (CDC)_ , 2010, pp. 4902–4907. 

- [16] L. Xu, Y. Baryshnikov, and C. Sung, “Reparametrization of 3D csc Dubins paths enabling 2d search,” in _Algorithmic Foundations of Robotics XVI_ , 2024. 

- [17] H. Chitsaz and S. M. LaValle, “Time-optimal paths for a Dubins airplane,” in _2007 46th IEEE Conference on Decision and Control_ , 2007, pp. 2379–2384. 

- [18] M. Owen, R. W. Beard, and T. W. McLain, _Implementing Dubins Airplane Paths on Fixed-Wing UAVs*_ . Dordrecht: Springer Netherlands, 2015, pp. 1677–1701. [Online]. Available: https://doi.org/ 10.1007/978-90-481-9707-1 120 

18 

IEEE TRANSACTIONS ON ROBOTICS 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0018-02.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0018-03.png)



![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0018-04.png)


(a) Initial roll = _−_ 15 _[◦] ,_ final roll = 0 _[◦]_ (b) Initial roll = 0 _[◦] ,_ final roll = 15 _[◦]_ (path (c) Initial roll = 15 _[◦] ,_ final roll _−_ 15 _[◦]_ (path (path through cross-tangent plane) through cylindrical envelope) through cylindrical envelope) 

Fig. 20. Depiction of varying paths with initial and final roll angles for “Long 1” with _Ryaw_ = 40 m and instantaneous configuration of the vehicle. Animations of a vehicle moving along these paths are available on our GitHub page. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0018-07.png)


and S. G. Manyam, “Optimal geodesic curvature constrained dubins’ paths on a sphere,” _Journal of Optimization Theory and Applications_ , vol. 197, pp. 966–992, 2023. 

- [27] D. P. Kumar, S. Darbha, S. G. Manyam, and D. Casbeer, “Generation of paths for motion planning for a dubins vehicle on sphere,” 2025. [Online]. Available: https://arxiv.org/abs/2504.11832 

- [28] D. J. Struik, _Lectures on Classical Differential Geometry_ , 2nd ed. Dover, 1988, ch. 4. 

- [29] A. M. Shkel and V. Lumelsky, “Classification of the dubins set,” _Robotics and Autonomous Systems_ , vol. 34, pp. 179–202, 2001. 

- [30] MathWorks, “uavDubinsConnection: Dubins path connection for UAV,” 2019, MATLAB Documentation (accessed March 1, 2026). [Online]. Available: https://www.mathworks.com/help/uav/ref/ uavdubinsconnection.connect.html 

- [31] M. P. D. Carmo, _Differential Geometry of Curves & Surfaces_ , 2nd ed. Dover, 2016, ch. 3. 

## APPENDIX 

Fig. 21. Feasible path from [21], [13], and [30] for “Long 1” 

## _A. Construction of segments_ 

- [19] R. W. Beard and T. W. McLain, _Small Unmanned Aircraft: Theory and Practice_ . Princeton University Press, 2012. 

- [20] V. M. Goncalves, L. C. A. Pimenta, C. A. Maia, B. C. O. Dutra, and G. A. S. Pereira, “Vector fields for robot navigation along time-varying curves in _n_ -dimensions,” _IEEE Transactions on Robotics_ , vol. 26, no. 4, pp. 647–659, 2010. 

- [21] P. V´aˇna, A. Alves Neto, J. Faigl, and D. G. Macharet, “Minimal 3D Dubins path with bounded curvature and pitch angle,” in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , 2020, pp. 8497–8503. 

- [22] J. Herynek, P. V´aˇna, and J. Faigl, “Finding 3D Dubins paths with pitch angle constraint using non-linear optimization,” in _2021 European Conference on Mobile Robots (ECMR)_ , 2021, pp. 1–6. 

- [23] W. Wang and P. Li, “Towards finding the shortest-paths for 3D rigid bodies,” in _Robotics: Science and Systems 2021_ , 2021. 

- [24] D. P. Kumar, S. Darbha, S. G. Manyam, and D. W. Casbeer, “A new approach to motion planning in 3d for a dubins vehicle: Special case on a sphere,” _IEEE Transactions on Robotics_ , pp. 1–18, 2026. 

- [25] R. L. Bishop, “There is more than one way to frame a curve,” _The American Mathematical Monthly_ , vol. 82, no. 3, pp. 246–251, 1975. 

- [26] S. Darbha, A. Pavan, R. Kumbakonam, S. Rathinam, D. W. Casbeer, 

Consider an interval _s ∈_ [ _s_ 0 _, s_ 1] in which _κg_ and _κn_ are constants. In this case, noting that **R** ( _s_ ) := � **T** ( _s_ ) **Y** ( _s_ ) **U** ( _s_ )[�] is a rotation matrix, (3), (4), and (5) can be rewritten as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0018-26.png)


Suppose at least one of _κg_ and _κn_ is non-zero. The solution for the above differential equation is given by **R** ( _s_ ) = **R** ( _s_ 0) _e_[Ω(] _[s][−][s]_[0][)] _,_ where the expression for the exponential of the skew-symmetric matrix can be obtained using the EulerRodriguez formula. Furthermore, using the obtained expression for **T** ( _s_ ) _,_ the solution for **X** ( _s_ ) can be obtained by inte- 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

19 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-02.png)


(a) Best path for final location inside pitch sphere from Algorithm 1 (best feasible path is left sphere – right sphere – left sphere). Animation of a vehicle moving along this path is available on our GitHub page. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-04.png)


(b) Best path for same configuration using algorithms from [21], [13], and [30] 

Fig. 22. Depiction of path for final location lying inside pitch sphere (specifications given in Section VIII-C) 

grating **X** _[′]_ ( _s_ ) from (2). Hence, the solution for the evolution of the four vectors can be written as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-08.png)


Here, _ϕ_ := ( _s − s_ 0)� _κ_[2] _n_ + _κ_[2] _g_ and denotes the arc angle of the considered segment, and **H** ( _ϕ_ ) is given by 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-10.png)


where _K_ := � _κ_[2] _n_ + _κ_[2] _g_ and _cϕ_ := cos _ϕ, sϕ_ := sin _ϕ._ We can observe that the solution is periodic with a period of 2 _π._ 

In the case of _κg_ = _κn_ = 0 _,_ **T** _,_ **Y** _,_ and **U** remain constant (from (2)); furthermore, **X** ( _s_ ) = **X** (0) + _s_ **T** (0) is obtained. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-13.png)


(a) Best path for final location inside yaw sphere from Algorithm 1 (best feasible path is right sphere – left sphere – right sphere). Animation of a vehicle moving along this path is available on our GitHub page. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-15.png)


(b) Best path for same configuration using algorithms from [21], [13], and [30] 

Fig. 23. Depiction of path for final location lying inside yaw sphere (specifications given in Section VIII-C) 

## _B. Proof for Lemma 1_ 

Without loss of generality, consider the initial rotation matrix **R** (0) to be the identity matrix and the initial location **X** (0) to coincide with the origin. Hence, using the closed-form expressions in Appendix A, the position is given by 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0019-20.png)


where _K_ = � _κ_[2] _n_ + _κ_[2] _g._ Consider _κn_ = _Rpitch_ 1 _[.]_[We][claim] that the obtained position **X** ( _ϕ_ ) lies on a sphere centered at (0 _,_ 0 _, Rpitch_ ) _[T] ,_ which is along **U** _,_ with radius _Rpitch._ To this end, we can show that _∥_ **X** ( _ϕ_ ) _−_ (0 _,_ 0 _, Rpitch_ ) _[T] ∥_ 2[2][=] _[ R] pitch_[2] _[,]_[ for] all _κg ∈_ � _− Ryaw_ 1 _[,] Ryaw_ 1 � _._ Hence, all segments corresponding to _κn_ = _Rpitch_ 1[lie][on][a][sphere][centered][at][(0] _[,]_[ 0] _[, R][pitch]_[)] _[T][ ,]_ with radius _Rpitch._ A similar argument can be made for _κn_ = _− Rpitch_ 1 _[,]_[where][all][segments][lie][on][a][sphere][centered] at (0 _,_ 0 _, −Rpitch_ ) _[T]_ with radius of _Rpitch._ Therefore, we can 

20 

IEEE TRANSACTIONS ON ROBOTICS 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0020-02.png)


(a) Percentage change in shortest path’s length 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0020-04.png)


(b) Varying computation time of Algorithm 1 (discretizations shown with a colored marker as well) 

Fig. 24. Impact of varying the discretization of parameters on path length and computation time for each instance (shown with a box plot) 

observe that _κn_ controls the pitch motion of the vehicle; furthermore, _κn_ = _± Rpitch_ 1[yield][maximum][ascent][or][descent] motion for the vehicle. 

The radius of a segment corresponding to when _κg_ is constant in � _− Ryaw_ 1 _[,] Ryaw_ 1 � can be obtained using the expression for **X** ( _ϕ_ ) as[1] 2 _[∥]_ **[X]**[(] _[π]_[)] _[−]_ **[X]**[(0)] _[∥]_[2] _[.]_[ Using the expression for] **[ X]**[(] _[ϕ]_[)] given in (26), it follows that[1] 2 _[∥]_ **[X]**[(] _[π]_[)] _[−]_ **[X]**[(0)] _[∥]_[2][=] _κ_[2] _g_[+] 1 _R_[2] 1 _._ � _pitch_ 

## _C. Sabban frame equations for sphere with radius R and path obtained in 3D_ 

The evolution equations for the Sabban frame on a unit sphere, described in Section IV-C, can be generalized to a sphere with radius _R._ To this end, the arc length _s_ on the sphere with radius _R_ is defined to be _s_ := _Rs,_ ˆ where _s_ ˆ is the arc length on the unit sphere. Furthermore, **X** _sp_ := _R_ **X**[ˆ] _sp_ depicts the location on the new sphere; here, **X**[ˆ] _sp_ denotes the location on the unit sphere (refer to Fig. 9). Additionally, the bound for the control input from _−_ 1theˆ unit sphere (= _U_[ˆ] _max_ ) is scaled to obtain _Umax_ := � _R_ � _Umax._ Following a similar process as Lemma 3.2 in [26], we can show that the minimum ˆ turning radius _r_ on the sphere of radius _R_ is given by _r_ = _Rr._ A depiction of the scaling for the initial configuration is shown in Fig. 9. 

The evolution equations for the sphere with radius _R_ can therefore be obtained as 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0020-12.png)


where _ug ∈_ [ _−Umax, Umax_ ] is the geodesic curvature on the sphere of radius _R_ and relates to the minimum turning radius _r_ on the sphere by _r_ = ~~_√_~~ 1+ _URmax_[2] _R_ ~~2~~ _[.]_[The][evolution][of][these] three vectors for _ug ≡ Umax,_ 0 _,_ or _−Umax,_ which correspond to left turn, great circular arc, and right turns on the sphere, can be obtained using the Euler-Rodriguez formula. 

## _D. Proof for Lemma 3_ 

Consider cylinders connecting a pair of inner or outer spheres, which are shown in Fig. 7a. The tangent plane for these cylinders is the **T** _−_ **Y** plane. Consider the bound chosen for the geodesic curvature on the cylinder ( _κg,cyc_ ) from (15), which is _Ryaw_ 1 _[.]_[We][note][that] _[κ][g,cyc]_[denotes][the][magnitude][of] the projection of the curvature vector on the tangent plane [28]. Since the tangent plane of this cylinder is the **T** _−_ **Y** plane, _κg,cyc_ also represents the geodesic curvature for the rotation minimizing frame model. This is because geodesic curvature for the minimizing frame model ( _κg_ ) controls the yaw motion (in the **T** _−_ **Y** plane) for the vehicle. Hence, the geodesic curvature bound for the rotation minimizing frame model is automatically satisfied for the chosen bound for _κg,cyc._ . 

On the other hand, the normal curvature of a cylinder depends on the direction of traversal along the cylinder. If the curve is along a direction parallel to the axis of the cylinder, _κn,cyc_ = 0; however, if the curve is perpendicular to the axis, _κn,cyc_ = _R_[1] _[,]_[ since the curve is along the circular cross-section] [31]. Since these curvatures of 0 and _R_ 1[are][the][principal] curvatures, the normal curvature for any intermediary direction of motion lies between the two through Euler’s theorem [28]. Noting that the normal curvature is along the surface normal for the cylinder, which is along **U** for the rotation minimizing frame model, the normal curvature bounds for the rotation minimizing frame model are automatically satisfied. A similar argument applies for the selected bound for _κg,cyc_ for the left and right cylinders, with the only difference arising in considering **T** _−_ **U** as the tangent plane and the surface normal for the cylinders being **Y** . 

## _E. Proof for Lemma 4_ 

Consider a cylinder that is parameterized in terms of _u_ and _v_ through (19). It suffices to show that the first fundamental form for the cylinder is the same as that for the plane, parameterized using _u_ and _v_ as given in (18). The first fundamental form coefficients are given by ( [28]) _Ecyl_ = _∂_ **X** _∂u[U] cyl_[(] _[s]_[)] _· ∂_ **X** _∂u[U] cyl_[(] _[s]_[)] = 1 _, Fcyl_ = _∂_ **X** _∂u[U] cyl_[(] _[s]_[)] _· ∂_ **X** _∂v[U] cyl_[(] _[s]_[)] = 0 _,_ and _Gcyl_ = _∂_ **X** _∂v[U] cyl_[(] _[s]_[)] _· ∂_ **X** _∂v[U] cyl_[(] _[s]_[)] = 1. Similarly, _Eplane, Fplane,_ and _Gplane_ can be obtained to be 1 _,_ 0 _,_ and 1 _._ Since the first fundamental form coefficients of the cylinder and the plane are equal, the length 

KUMAR _et al._ : MODEL FOR 3D MOTION PLANNING FOR A DUBINS VEHICLE WITH PITCH AND YAW RATE CONSTRAINTS 

21 

of the curve is preserved. This is because the distance between two closely spaced points on the curve on the cylinder that are initially separated by _du_ and _dv_ on the plane is given by _ds_[2] _cyl_[=] _[ E][cyl][du]_[2][ + 2] _[F][cyl][dudv]_[ +] _[ G][cyl][dv]_[2][=] _[ ds]_[2] _plane[.]_ 

**Deepak Prakash Kumar** (Member, IEEE) received his Ph.D. degree in Mechanical Engineering from Texas A&M University in 2025. He received his B.Tech in Engineering Design and M.Tech in Automotive Engineering from the Engineering Design department at IIT Madras in 2020. He is currently a Postdoctoral Scholar with the Center for Resilient Autonomous Systems, Department of Electrical Engineering and Computer Science, University of California, Irvine. His research interests include safe physical AI algorithms for multi-agent collaboration, physical AI for human–robot teaming, motion planning and control for autonomous vehicles, and vehicle routing algorithms. 

**Swaroop Darbha** (Fellow, IEEE), received the Ph.D. degree from the University of California at Berkeley, Berkeley, CA, USA, in 1994. He is currently the Gulf Oil/Thomas A Dietz Professor of mechanical engineering with Texas A&M University, College Station, TX, USA. His research interests include dynamics, control, and diagnostics of connected and autonomous ground vehicles, routing of unmanned aerial vehicles, and decision-making under uncertainty. He is a fellow of ASME and IEEE for his contributions to Intelligent Transportation Systems and Unmanned Vehicles. 

**Satyanarayana Gupta Manyam** (Senior Member, IEEE), Satyanarayana Gupta Manyam received the Ph.D. degree in Mechanical Engineering from Texas A & M University, College Station, Texas, in 2015. He is currently a Research Scientist at DCS Corporation, where he works as a contractor for the Control Science Center of the U.S. Air Force Research Laboratory (AFRL) at Wright-Patterson Air Force Base, OH, USA. His primary research interest include cooperative path planning for multivehicle systems, trajectory and motion planning for autonomous vehicles. His interests also include combinatorial optimization and bounding algorithms for discrete optimization problems. 


![](1_survey/papers/md/Kumar2025Novel_figs/Kumar2025Novel.pdf-0021-06.png)


**David W. Casbeer** (Senior Member, IEEE) is the technical area lead for UAV Cooperative and Intelligent Control at the Air Force Research Laboratory’s Control Science Center, where he leads research to enable autonomous UAVs in future Air Force missions. He received the BS (2003) and PhD (2009) degrees from Brigham Young University, where he focused on decentralized estimation techniques. He is a Senior Member of the IEEE and an Associate Fellow in the AIAA. He currently serves as an associate editor for the AIAA Journal of Aerospace 

Information Systems. 

