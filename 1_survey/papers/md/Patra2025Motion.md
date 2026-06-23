---
citation_key: Patra2025Motion
arxiv_id: 2502.05462
arxiv_url: "https://arxiv.org/abs/2502.05462"
title: "Motion Planning of Cooperative Nonholonomic Mobile Manipulators"
authors_short: "Keshab Patra et al."
year: 2025
direction_tag: N_path_repair;P_nonholonomic_constraints
source: pymupdf4llm
converted_at: 2026-06-23T18:07:56Z
origin: ai+web
reviewed: false
---

## Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

**Keshab Patra ID** 1[∗] **, Arpita Sinha ID** 2 **, and Anirban Guha** 1 

1Department of Mechanical Engineering, Indian Institute of Technology Bombay, Mumbai, Maharashtra, India 

2Center for Systems and Control, Indian Institute of Technology Bombay, Mumbai, Maharashtra, India 

## **A** bstract 

We propose a real-time implementable motion planning framework for cooperative object transportation by nonholonomic mobile manipulator robots (MMRs) in dynamic environments. Our global planner finds a path from start to goal through the static, obstacle-free regions in the environment and generates a set of convex, static, obstacle-free regions around the path using a novel, fast, and computationally lightweight ellipse-based technique. We introduce a nonlinear Model Predictive Control (NMPC) based real-time implementable planning technique that jointly plans feasible motion for the mobile base and the manipulator’s arm and generates a kinodynamic feasible, collision-free trajectory for cooperative object transportation. Simulation and hardware experiments validate the efficiency of our proposed planning framework. 

## 1 Introduction 

Robotic systems became integral to automation in manufacturing, remote exploration, warehouse management, and other areas. Cooperative multiple MMRs garner attention due to their low cost, small size, redundancy in heavy or oversized object transportation, and fixture-less multipart assembly requiring more Degrees of Freedom (DoF). A cooperative MMR system extends workspace coverage, flexibility, and redundancy with added complexity in robot coordination, communication, and motion planning. Multiple MMRs leverage the mobile bases’ locomotion ability and the arms’ manipulation ability for object transportation and manipulation in a large workspace. 

Nonholonomic mobile bases are widespread in robotic applications because of their advantages in a reduced number of actuators, simplified wheels, and better load-carrying capacity. Nonholonomic MMRs can work better than their holonomic counterparts on uneven ground surfaces as they restrict sideways motion, which leads to increased stability, traction, and controllability on uneven surfaces. The nonholonomic mobile base of the MMRs restricts sideways motion, including non-integrable kinematic constraints. Hence, there are more intricacies in cooperative motion planning and trajectory generation than in the holonomic counterpart. 

The study on collaborative manipulators started with a virtual linkage model [1] representing the collaborative manipulation systems to generate closed-chain constraints [2] between the object and the MMRs for motion synchronization and coordination. The dual arm cooperative control problem has been addressed by NMPC [3]. The coordination scheme for multi-MMR cooperative manipulation and transportation comprises of centralized [4], decentralized [5, 6] and distributed [7, 8, 9] control framework. Task allocation [10, 11] algorithm ensures efficient utilization of the capabilities of the cooperative manipulators. The collision-free navigation started with a variational-based method [12] that demonstrated static obstacle avoidance for a two MMR system with poor scalability. Dipolar inverse Lyapunov functions fused with the potential field-based navigation function [13] plan collision-free motion in static environments to transport deformable material by multiple MMRs with a little scope of formation control. 

Optimization-based motion planning technique [14] for holonomic MMRs in dynamic environments uses obstacle-free convex polygons around the formation in the position-time space. It optimizes the holonomic MMRs’ pose to retain the cooperative MMR system inside the obstacle-free polygon. A geometric path planning approach [15, 16] for multiple MMRs transport an object avoiding static obstacles. A rectangular passagewaybased approach [15] finds the optimal system width and moving direction in the static obstacle-free area for navigation. These methods do not include motion constraints to provide guaranteed feasible motion for nonholonomic MMRs. 

A kinematic motion planning technique [17] plans for spatial collaborative payload manipulation using a hierarchical approach. The technique’s conservative approximation of the obstacles as uniform cylinders highly restricts navigation in tight spaces with high aspect ratios polygonal obstacles. MPC-based motion planning techniques for static obstacle avoidance have been presented in [18, 19]. An alternating direction method of multipliers-based distributed trajectory planning algorithm [20] plans trajectory in a static environment. A distributed formation control technique [21] utilizes constrained optimization for object transportation in a static environment. Motion Planning for deformable object transportation [22, 23] in a static environment uses optimization techniques. A reciprocal collision avoidance algorithm [24] combined with MPC doesn’t maintain any formation. These generic planning algorithms cannot be used as they do not maintain the rigid formation required for collaborative MMRs. An NMPC-based kinodynamic motion planning technique [25] plans motion for object transportation by multiple MMRs in dynamic environments. The proposed planning technique is limited to holonomic MMRs and environments with convex static obstacles. 

We propose an end-to-end trajectory planning framework for collaborative object transportation by nonholonomic MMRs. Our proposed algorithm plans the trajectory in two steps: offline path planning and online motion planning. To the best of our knowledge, the end-to-end planning for nonholonomic MMRs has not been done before. The offline planning algorithm computes a linear, piecewise path from start to goal using the visibility vertices algorithm [26] and defines the static, obstaclefree region for motion planning optimization. Motivated by [27], 

***correspondence:** `keshabpatra19@gmail.com` 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

2 

we have developed a novel, fast, ellipse-based optimizationfree convex polygon computation algorithm to define the static obstacle-free region around the piecewise linear path. Starting from computing a polygon around the path segments using its visibility vertices, we convexify it by eliminating the concave vertices using the tangents of ellipses. We compute the ellipse, aligning its major axis along the path segment that touches the nearest concave vertex, and inflate it to eliminate subsequent concave vertices in the same polygon. The proposed planning technique eliminates the restriction of convex obstacles of IRISbased planning algorithms [27, 14, 25] and convex optimization, guaranteeing the path segment will remain within it. 

The major contributions of this article are as follows. 

1. We propose a fast ellipse-based optimization-free convex polygon computation algorithm to define the static obstacle-free region around the linear piece-wise path using its visible vertices. The convex obstacle-free region is regarded as inequality constraints in the NMPC for motion planning. 

2. We introduce an NMPC-based, real-time implementable online motion planner that jointly plans for the nonholonomic MMR’s base and the manipulator. The planner computes a kinodynamic feasible collisionfree motion plan for the multiple MMRs in a dynamic environment. 

## 2 Problem Formulation 

A system of _n_ nonholonomic MMRs grasps a rigid object at its periphery as shown in Fig. 1 to collaboratively transport the object without any collision. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0002-08.png)


Figure 1: Formation of five non-holonomic MMRs holding an object. The MMRs grasped the object to transport collaboratively without any collision. 

{ _**w**_ } defines the world fixed reference frame. An object coordinate frame { _**o**_ } is attached to the object center of mass (CoM), and each MMR has its own body coordinates { _**b** i_ } attached to the center of its mobile base. Without specific mention, all the quantities are defined in { _**w**_ }. The collaborative manipulation system is defined in the following subsections. 

## _2.1 Mobile Manipulator and Collaborative Formation_ 

The mobile base of _i_ -th MMR is defined with pose _qm_ , _i_ = [ _p[T] i_[, ϕ] _[i]_[]] _[T]_[where] _[p][i]_[∈][R][2][and][ ϕ] _[i]_[∈][R][ are the position and orien-] tation of the mobile base. The manipulator of _i_ -th MMR has _ni_ number of joints and it’s displacement is defined as _qa_ , _i_ = [ _qa_ , _i_ 1, _qa_ , _i_ 2, · · · , _qa_ , _ini_ ] _[T]_ . The whole MMR is defined by _qi_ = [ _q[T] m_ , _i_[,] _[ q][T] a_ , _i_[]] _[T]_[.][The] _[ i]_[-th EE’s position and orientation is defined in] { _w_ } as _pee_ , _i_ ∈ R[3] and ϕ _ee_ , _i_ ∈ R[3] . The _i_ -th non-holonomic MMR’s first-order dynamics is _q_ ˙ _i_ = [ _vi_ cos(ϕ _i_ ), _vi_ sin(ϕ _i_ ), ω _i_ , ˙ _qa_ , _i_ ] _[T]_ where the control inputs are mobile base’s linear and angular velocities _vi_ , ω _i_ respectively and the manipulator’s joint velocities _q_ ˙ _a_ , _i_ , therefore, _ui_ = [ _vi_ , ω _i_ , ˙ _qa_ , _i_ ]. 

We represent the coupled first order system dynamics for _i_ -th MMR by a discrete-time non-linear system as 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0002-14.png)


where _k_ is the discrete time step. The admissible states and control inputs are defined by Eqn. 2 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0002-16.png)


where _qa_ , _i_[,] _qa_ , _i_ represents the manipulator’s joint position limit vector and _ui_[,] _ui_ are the admissible control limits. The set of admissible states Q _i_ and control inputs U _i_ are indicated by joint position and velocity vectors’ limit (Eqn. (2)), Q _i_ = [ _q_ ~~_a_~~ , _i_[,] _qa_ , _i_ ], U _i_ = [ _u_ ~~_i_~~[,] _ui_ ] 

The EE of the _i_ -th MMR of the multi-MMR formation F (Fig 1) grasps the object at _[o] ri_ defined in object frame _**o**_ , where the superscript _**o**_ indicates it’s reference frame { _**o**_ }. The formation configuration is defined by X = [ _p[T]_ , _o[T]_ , _Q[T]_ ] _[T]_ , where _p_ ∈ R[3] is the position and _o_ ∈ R[3] is the orientation of the object CoM, _Q_ = [ _q[T]_ 1[,] _[ q][T]_ 2[,][ · · ·][,] _[ q][T] n_[]] _[T]_[is][the][configuration][of] _[n]_[MMRs.][The] space occupied by the formation is defined as B(X). 

## _2.2 Environments_ 

A structured and bounded environment having both static and dynamic obstacles is defined as _W_ . O represents the set of static obstacles in _W_ . The static obstacle-free workspace is defined by _W free_ = _W_ \ O ∈ R[2] . The set of dynamic obstacles in the environment is defined as O _dyn_ . The start position _ps_ and the goal position _pg_ of the object CoM are in the obstacle-free space _W free_ . 

The planning objective is to design a motion planning framework such that 1) the MMRs can cooperatively transport the object without any collision. 2) the generated trajectory is kinodynamically feasible and within the admissible limits of the MMRs minimizing the control input of MMRs. 3) the planner can handle any rigid object, grasping configuration and static concave obstacles directly. 

## 3 Motion Planning 

We solve the motion planning problem for cooperative multiMMRs in two steps: offline path planning and online motion planning shown in Fig. 2. In the offline path planning step, we compute a static obstacle-free linear piece-wise shortest 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

3 

distance path ( _S_ ) between the start and the goal location using offline path planner in Section 3.1. Then we compute a set of connected convex region around the path using our proposed convex polygon computation algorithm in 3.1.2. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0003-03.png)


**----- Start of picture text -----**<br>
MMR with<br>the object<br>Offline Path Online  Motion<br>Planner  Planner<br>**----- End of picture text -----**<br>


Figure 2: Two step motion planning process: offline path planning and online motion planning. 

In the next step, an online motion planner (Section 3.2) computes a feasible motion plan for the collaborative MMRs in receding horizons. The planner generates a kinodynamically feasible trajectory in the dynamic environment using _pr_ ( _ct_ ) as an initial guess. The generated trajectory is free from collision with the static and dynamic obstacles and collision among the MMRs and with the object. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0003-06.png)


**----- Start of picture text -----**<br>
Obstacle Dilation &  Visibility Graph  Compute<br>Post Processing Generation  Path<br>Path  Visibility  Compute  Ref. Trajectory<br>Vertices Computation Convex Polygon Generation<br>**----- End of picture text -----**<br>


Figure 3: Offline path planning and convex polygon computation process around _S_ . 

## _3.1 Global Path Planner_ 

The global path planner computes a static obstacle-free path _S_ for the MMRs’ between the start and goal in offline employing visibility vertices finding algorithm [26]. Then it computes a set of connected convex obstacle-free polygon around _S_ . Fig. 3 shows the outline of the path planning process. 

## _3.1.1 Path Computation_ 

The global path planner dilates O by a distance _r f_ so that we consider the formation F at any point _p_ ,the CoM of the grasped object. The dilation distance _r f_ is the radius of a circle located at _p_ , inside which the formation could always be enclosed. The planner substitutes the mutually intersecting dilated obstacles O _dil_ with their union. A visibility vertices finding algorithm [26] creates a visibility map considering O _dil_ and the start and goal point. The vertices from the visibility map are added as node V to a graph G(V, E, W). An edge E is added between two mutually visible nodes using the visibility map with the Euclidean distance between them as weight W. A graph search algorithm computes the shortest linear piece-wise path _S_ between the start _ps_ and the goal _pg_ location. Fig. 4 shows the computed path _S_ with linear segments _S_ 1, _S_ 2, _S_ 3, _S_ 4 and vertices _w_ 1, _w_ 2, _w_ 3, _w_ 4, _w_ 5. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0003-12.png)


Figure 4: Path Polygon for _S_ 2 computed using the visible vertices of _W_ 2 and _W_ 3. 

## _3.1.2 Convex Polygon Computation_ 

We compute a static obstacle-free polygon around a path segments _S i_ ∈ _S_ and convexify. We consider O and the vertices _wi_ of the path to obtain the set of vertices V _s_ present in the static environment and visible from _wi_ , ∀ _i_ (Fig. 4). A simple polygon is defined for each vertex _wi_ , ∀ _i_ by cyclically connecting its visible vertices. The polygon remains in _W free_ . The union of polygons obtained for _wi_ and _wi_ +1 of a path segment _S i_ defines a static obstacle-free simple polygon P _cc_ , _i_ around _S i_ ∈ _S_ . Fig. 4 shows the computed polygons for the path segment _S_ 2 using the polygons around _w_ 2 and _w_ 3. The union of the two polygons (green and blue) in red boundary defined around _w_ 2 and _w_ 3 provides a static obstacle-free polygon P _cc_ ,2 around _S_ 2. A set of polygon P _cc_ for _S_ is computed similarly. The computed polygons are generally concave. Convexification is needed for the static obstacle avoidance constraints in motion planning optimizations. We compute a set of convex polygons P _S_ analytically as a subset of their original concave polygons in P _cc_ . To eliminate the concave vertices of P _cc_ , _i_ we use tangents of ellipses at concave vertices, whose major axis aligned with _S i_ . The convexification steps are illustrated in the Algo. 1. 

We define an ellipse in the ground plane as 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0003-17.png)


where C is a 2 × 2 symmetric positive definite matrix that maps the deformation of a unit radius circle (|| _x_ || ≤ 1) to an ellipse. C is decomposed as C = _R[T]_ Λ _R_ , where _R_ is a rotation matrix that aligns the ellipse axes to the world reference frame axes and Λ = _diag_ ( _a_ , _b_ ) is a diagonal scale matrix. The diagonal elements _a_ and _b_ of Λ refer to the length of the ellipse semi-major and minor axes. d defines the center of the ellipse. 

Algo. 1 initializes a polygon P with the concave polygon P _cc_ , _i_ . It finds the concave vertices V _cc_ of P. If V _cc_ is not empty, then it convexifies P in line 4 − 17. The algorithm computes the half-plane representation of P in line 19. In the polygon 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

4 

**Algorithm 1** Polygon Convexification 

**Input:** Concave Polygon P _cc_ , _i_ , Path segment _S i_ **Output:** Convex Polygon P 1: P ← P _cc_ , _i_ ; _j_ ← 0 2: V _cc_ ← ConcaveVertices(P) 3: **if** V _cc_ � ϕ **then** 4: d ← Midpoint( _S i_ ); _R_ : major axis along _S i_ 5: _a_ ← 0.5 _length_ ( _S i_ ) + _r f_ 6: _x_[∗] _j_[←][NearestVertex(][V] _[cc]_[,][ d)] 7: C _j_ , _d_ ← FindEllipse( _R_ , _a_ , d, _x_[∗] _j_[)] ▷ Use || _x_[∗] _j_[||][ =][ 1] 8: κ _j_ ← (C _j_ , d) 9: a _j_ ← 2C[−] _j[T]_[C][−] _j_[1][(] _[x]_[∗] _j_[−][d);] _[ b][j]_[←][a] _[T] j[x]_[∗] _j_[▷][Tangent of ellipse] κ _j_ at _x_[∗] _j_ 10: P, V _cc_ ← DiscardVertices(a _j_ , _b j_ , P, V _cc_ ) 11: **while** V _cc_ � ϕ **do** 12: _j_ = _j_ + 1 13: _x_[∗] _j_[=][ NearestVertex(][V] _[cc]_[,][ d)] 14: κ _j_ ← DilateEllipse(κ0, _R_ , _x_[∗] _j_[)] 15: repeat line 9 − 10 16: **end while** 17: P : **A** ← [a _[T]_ 0[,][ a] 1 _[T]_[,][ · · ·][ ]] _[T]_[,] **[ b]**[ ←][[] _[b]_[0][,] _[ b]_[1][,][ · · ·][ ]] _[T]_ 18: **else** 19: P : ( **A** , **b** ) ← HalfPlanes(P) 20: **end if** 21: **return** P( **A** , **b** ) 

convexification process, the algorithm fits an ellipse κ0 center d at the midpoint of the path segment _S i_ ∈ _S_ . The major axis is aligned with the path segment _S i_ , the semi-major axis length _a_ = 0.5 _length_ ( _S i_ ) + _r f_ . The ellipse is inflated in the minor-axis direction till it touches the nearest concave points _x_ 0[∗][to] _[ d]_[ and an] ellipse κ0 is computed in line 4 − 8. The tangent to the ellipse κ0 at point _x_ 0[∗][defines the inequality] _[ H]_[0][=][ {] _[x]_[ : a] _[T]_ 0 _[x]_[ ≤] _[b]_[0][}][.][After] obtaining _H_ 0 in line 9, we cut the polygon with _H_ 0 and keep the polygon that contains _S i_ and keep it as P (Fig. 5a). We discard the concave vertices outside the new polygon P from V _cc_ . If there is any concave vertices left V _cc_ � ϕ the ellipse κ0 is dilated to form an ellipse κ1 in line 14 keeping the aspect ratio same till it touches the nearest concave vertices _xi_[∗][∈V] _[cc]_ to d. The tangent to the ellipse at point _x_ 1[∗][defines the inequality] _H_ 1 = { _x_ : a _[T]_ 1 _[x]_[≤] _[b]_[1][}][.][After obtaining] _[H]_[1][in line 9, we cut the] polygon with _H_ 1 and keep the polygon that contains _S i_ and keep it as P, as shown in Fig. 5b. The convexification process in line 11 − 16 is repeated until no concave vertex left in the polygon V _cc_ � ϕ (Fig. 5b-5d). After eliminating all the concave vertices, the polygon P becomes convex (Fig. 5d), and the half-plane representation of P is returned in line 17. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0004-05.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0004-06.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0004-07.png)


**----- Start of picture text -----**<br>
(a) (b)<br>(c) (d)<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0004-08.png)


(e) Convex polygons (light green) around _S_ . 

Figure 5: Fig. 5a - 5d shows the steps of polygon convexification process for _S_ 2. A tangent of an ellipse touching the nearest concave vertex (red line) of the polygon eliminates its concavity by cutting the polygon (black edges). The polygon (sky blue) containing the path segment has been kept. A convex polygon is formed (green polygon in Fig. 5d.) 

The Fig. 5 shows the polygon convexification process of P _cc_ ,2 defined for _S_ 2. An ellipse touching its nearest concave vertex to _S_ 2, has been obtained and a tangent (red line) to the ellipse at this point has been drawn in Fig. 5a. The tangent cuts the polygon into two. The polygon (sky blue) containing the path segment has been kept. The ellipse has been dilated keeping the aspect ratio same in Fig 5b till it touches the nearest concave vertex (to _S_ 2) of the new polygon. Here a very small portion of the polygon is cut by the tangent to the ellipse at this concave 

5 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

vertex. The process continues till any concave vertex remains and a convex polygon is formed (green polygon in Fig. 5d.) 

Fig. 5e shows a set of convex polygons P _S_ in light green around the path segment _S_ computed using the Algo. 1. Every segment of _S_ remains inside any convex polygon P ∈P _S_ defined in _W free_ . We add additional intermediate control points in red dots in Fig. 5e on _S_ . The control points are used to generate time-normalized smooth trajectory _pr_ ( _ct_ ) from the _S_ using a Bézier curve with normalized time parameter _ct_ ∈ [0, 1]. These intermediate control points are inserted when a new convex polygon appears along the path _S_ from the start point. A control point is added for the last path segment while exiting the intersection area of the last two polygons. The generated quadratic Bézier curve would remain in _W free_ as any three consecutive control points remain within a single convex polygon. The timenormalized reference trajectory _pr_ ( _ct_ ) is used as an initial guess for the online motion planner. 

## _3.2 Online Motion Planner_ 

The global path planner in Section 3.1 computes a static obstaclefree path _S_ . It does not delve into the motion constraints of the MMRs, dynamic obstacle avoidance, and the collision among the MMRs but provide the global references. We propose an online motion planner as a constrained nonlinear optimization problem incorporating kinodynamic constraints. It uses the smoothed global reference trajectory _pr_ ( _ct_ ) as an initial guess to eliminate the local stuck. The online motion planning optimization is given as 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-06.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-07.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-08.png)


long enough to capture the sharp turning behavior. The MMRs execute the computed motion plan of a horizon for an execution time _Te_ ( _Te_ < _Th_ ). We choose the execution time _Te_ so that the computation time for a horizon is guaranteed to be less than _Te_ , and the MMRs can start the next plan once it finishes executing the current plan. In case of failure to get a motion plan the MMRs would stop motion and the planner would try to re-plan from the stopping position. 

## _3.2.1 Cost Function_ 

The cost function of the optimization in Eqn. (4) described in Eqn. (5) minimizes the control inputs and the tracking error with respect to the initial guess trajectory. The diagonal weightage matrix **Wu** for control effort minimization is provided with higher value than the weight-age matrix **We** to the tracking error _e[k]_ of the object CoM. The higher weight-age to control inputs prioritize input minimization. The lower weight values to the tracking error provides global guidance to the trajectory with flexibility to deform for dynamic obstacle avoidance and kinodynamic motion compliance. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-12.png)


We discretize the reference path _pr_ ( _ct_ ) into Λ path segment. The expected and reference position for the CoM of the object is denoted as _p[k]_ and _p_[λ] _r_[+] _[k]_ = [ _x_ , _y_ ][λ] _r_[+] _[k]_ for the future time step _k_ and λ is the index of the nearest reference path segment to _p_[0] . The discretized path should hold the relation[�] _k[N]_ = _[h]_ 0[−][1][||] _[p] r_[λ][+] _[k]_[+][1] − _p_[λ] _r_[+] _[k]_ || ≤ _vopTh_ , where _vop_ is the operational velocity of the formation. The tracking error vector _e[k]_ is defined as 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-14.png)


The terminal cost _JNh_ is defined in Eqn. (7) similar to the tracking error with a higher weighting **W** _nh_ . 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-16.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-17.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-18.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-19.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-20.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-21.png)


where the superscript _k_ refers to the discrete time step. Section 3.2.1 illustrates the cost function in Eqn. (4a). Eqn. (4b) represents the state transition function (Eqn. (1)) of the system. Eqn. (4c) and (4d) account for the static and dynamic obstacles avoidance constraints detailed in Section 3.2.2 and Section 3.2.3. The self collision avoidance described in Section 3.2.4 is ensured by the constraints in the Eqn. (4e)-(4g). The set of admissible states and control inputs are defined in Eqn. (4h) and elaborated in Eqn. 2. The grasp constraints described in Section 3.2.5) are maintained by Eqn. (4i). Eqn. (4j) defines the initial state of the formation in a planning horizon _Nh_ . 

The online motion planner computes the optimal motion plan for the MMRs by solving the optimization problem in Eqn. 4 in receding horizons for _Nh_ horizon segment with time _Th_ to reduce the computational burden. The horizon length should be 

## _3.2.2 Static Obstacles Avoidance_ 

The formation F must remain within _W free_ (B(X) ⊂W _free_ ) to avoid collision with static obstacles. _W free_ is represented by a set of convex polygons P _S_ computed by the offline path planner in Section 3.1.2. The inequality representation of the polygon P ∈P is in Eqn. (8). 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-26.png)


where _n f_ is the number of the sides of P and x is an interior point of P. The set of vertices of the bounding polygons of the object and the _n_ MMRs are represented by _V_ (X). The projection of _V_ (X) at the ground plane ( _z_ = 0) must remain within any polygon P ∈P _S_ . The constraints are represented as follows 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0005-28.png)


where v< _x_ , _y_ > is the _x_ − _y_ projection of the vertex v ∈ _V_ (X) defined in { _w_ }. _dsa fe_ is the safety distance. The number of constraints in Eqn. (9) increases the computational complexity significantly. The problem can be simplified further by considering the bounding circles of the projected vertices of the 

6 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

MMR base, manipulators, and the object. This collision geometry reduces the number of constraints and the computational complexity. We have implemented circumscribing bounding circles for each MMR base, manipulator, and object in the ground plane. The center of the circles for the _i_ -th MMR base, manipulator, and the object in the ground are located at _pbase_ , _i_ , _parm_ , _i_ and _pob j_ , _i_ with radius _rbase_ , _i_ , _rarm_ , _i_ and _robj_ , _i_ . The cyan, purple, and gray area in Fig. 6 shows the circumscribing circles for the _i_ − _th_ MMR base, manipulator, and object. The reduced static collision avoidance constraints are in the Eqn. (10) 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0006-03.png)


## _3.2.3 Dynamic Obstacle Avoidance_ 

The formation F must not collide with any of the dynamic obstacles O _dyn_ . The space occupied by the formation B(X) should not overlap with the dynamic obstacles i.e. B(X) ∩O _dyn_ = ∅. We implement the dynamic obstacle avoidance by introducing a nonlinear constraint between the collision geometries of the formations and the dynamic obstacles. The collision geometry of the dynamic obstacles are considered as circles with radius _rdyn_ , _d_ , ∀ _d_ ∈ [1, _ndyn_ ] located at _p[k] dyn_ , _d_[,][ ∀] _[k]_[ ∈][[1][,] _[ N][h]_[] in the] ground plane, where _d_ ∈ [1, _ndyn_ ] represents the _ndyn_ number dynamic obstacles’ (O _dyn_ ) index and represents the number of dynamic obstacle present at the beginning of planning horizon. The position _p[k] dyn_ , _d_[=] _[p][dyn]_[,] _[d]_[+] _[ v][dyn]_[,] _[d][kT][c]_[,][∀] _[d]_[,][∀] _[k]_[∈][[1][,] _[ N][h]_[]][is] predicted with the position _pdyn_ , _d_ and velocity _vdyn_ , _d_ measured at the beginning of each planning horizon using camera, LiDAR based perception system or a motion capture system. Any other dynamic obstacle state estimation model would work with the proposed motion planning algorithm. The accuracy of the estimation model impacts the collision avoidance behavior. 

The same collision geometry defined for the static obstacle avoidance in Section 3.2.2 for the base, manipulator of the MMRs, and the object are utilized here. The constraints in Eqn. (11) ensure that the obstacle does not intersect with the formation. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0006-07.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0006-08.png)


Figure 6: The infinite convex wedge for _i_ − _th_ MMR is defined by the half plane H _i_ , H( _i_ +1)% _n_ , _z_ = 0 and _z_ = ∞. The enclosing circles for MMRs’ mobile base and manipulator are blue and violet, respectively, and the object is gray. 

The self-collision avoidance for the _i[th]_ MMR is defined in the following 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0006-11.png)


where _Vi_ ( _qi_ ) is the set of vertices of the _i_ -th MMR. 

## _3.2.5 Grasp Constraints_ 

The MMRs grasp the object at its periphery at equal spacing from each other to have equal workspace among them and for optimal wrench interaction with the object. There should be no relative movement between the EE and the grasped object throughout the task to ensure stable formation as the object is rigid. The grasp constraint for _i_ -th MMR is 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0006-15.png)


where _pee_ , _i_ is _i_ -th MMR’s EE position, _[w] o_[R][ is the rotation matrix] between _**o**_ and _**w**_ . We represent Eqn. (14) by _gi_ (X) = 0. 

## 4 Object Transportation 

## _3.2.4 Self Collision Avoidance_ 

For collision avoidance with the object and the other MMRs, the _i_ -th MMR needs to be within the convex wedge shown in Fig. 6 defined by two infinite vertical planes H _i_ and H( _i_ +1)% _n_ as shown in Fig. 6. The convex wedge specifies the workspace for the _i_ -th MMR free from movements of the neighboring MMRs. The planes H _i_ and H( _i_ +1)% _n_ is define considering the workspace of MMRs. Here, we have equally divided the space around the periphery of the object, starting at the CoM of the object for each MMR, as the grasping point is equispaced. The vertical plane H _i_ is defined as follows. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0006-20.png)


We validate the proposed motion planning algorithm in simulation and hardware experiments with the nonholonomic MMRs that accept velocity as a control input. The system dynamics for the MMRs are approximated using the fourth-order Runge-Kutta method as mentioned in Eqn. (1). The NMPC problem of the local motion planning is solved using the CasADi package [28] with an Interior point optimization (Ipopt) method. 

## _4.1 Simulation_ 

The MMRs with a differential drive mobile base have the same forwarding and reversing capabilities. The Denavit-Hartenberg (DH) parameters are mentioned in Table 1. 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

7 

Table 1: DH Parameters Value for the manipulators 

|**Joint**|_d_ (_m_)|_a_ (_m_)|α (_rad_)|θ (_rad_)|
|---|---|---|---|---|
|Joint 1|0.070|0|0|_qa_,1|
|Joint 2|0|0|0.5π|_qa_,2|
|Joint 3|0.100|0|−π|_qa_,3|
|Joint 4|0.125|0|π|_qa_,4|
|Joint 5|0|0.120|−0.5π|_qa_,5|
|Gripper|0|0|0|0|



We select the operational velocity of the formation _vop_ = 0.15 _m_ / _s_ and use prediction horizon time _Th_ = 9 _s_ , trajectory execution time _Te_ = 3 _s_ and the discretization time step _Tc_ = 0.25 _s_ . The safety margins _dsafe_ = 0.05 _m_ and _dsafe_ , _dyn_ = 0.1 _m_ for static and dynamic obstacle avoidance to keep the formation safe during object transportation. A higher margin restricts the formation from nearing the obstacles and hence reduces the obstacle-free space. The tuned optimization weights are **Wu** = _diag_ ( _repeat_ ([0.05, 0.25, 2.5, 2.5, 2.5, 5, 2.5], 5)), **We** = _diag_ ([0.01, 0.01]) and **WNh** = 10[5] . We assign a lower weight to the base, prioritize the use of the mobile base motion over the arm, and avoid joint limits when reaching for the arm. The base angular motion is assigned a relatively higher weight than linear to reduce rotation and hence improve ground trajectory smoothness. One of the manipulator joints is assigned a higher weight to reduce the more frequent motion in the ± _z_ direction. The lower weight to the global reference tracking error ensures flexibility for a smooth trajectory with better dynamic obstacle avoidance behavior. 

The five MMRs (the mobile base in deep green rectangle and manipulator’s arm in red line) start transporting (Fig. 7a) the object while grasping at its periphery through a narrow corridor of 1.9 _m_ in an environment of size 10 _m_ × 10 _m_ . While the MMRs come out of the corridor, it encounters dynamic obstacles in Fig. 7b, while taking a sharp left turn. The generated motion plan successfully navigates the formation, avoiding dynamic obstacles, and turns toward (Fig. 7c) the goal. The MMRs successfully transport the object through the narrow doors and complete the task without any collision (Fig. 7d). Fig. 7e plots the shortest distance _dmargin_ from the formation to any static and dynamic obstacles. The _dmargin_ in Fig 7e for the static and the dynamic obstacles being always positive indicates successful collision avoidance behavior. 

## _4.2 Hardware Experiments_ 

We perform experiments with our in-house developed ROSenabled MMRs to evaluate the motion planning algorithm in Section 3.2 in an environment (4 _m_ × 4 _m_ ) with static and dynamic obstacles. We have defined a specific path for the dynamic obstacles (turtle bot). However, the path of the obstacle is not known to the mobile manipulators. The nonholonomic MMR bases are made of two disc wheels each separately driven by geared motor with an encoder. Fig. 8 shows two MMRs both grasped an object to transport it in an indoor environment shown in Fig. 9a. 

The manipulator of the MMRs shown in Fig. 8 is same as the manipulator used for the simulation, described in Table 1, except for the joint 5. We have removed and fixed the joint 5 because 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0007-09.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0007-10.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0007-11.png)


**----- Start of picture text -----**<br>
(a) t  = 0  s (b) t  = 32.5 s<br>(c) t  = 40.5  s (d) t  = 79  s<br>(e) Safety margins.<br>**----- End of picture text -----**<br>


Figure 7: The snapshots of object transportation from a start (Fig. 7a) to a goal (Fig. 7d) by five MMRs in 10 _m_ × 10 _m_ environment. The red circle indicates dynamic obstacle is in its current state. The horizontal lines in Fig. 7e plots static and dynamic safety threshold _dsa fe_ = 0.05 _m_ and _dsa fe_ , _dyn_ = 0.1 _m_ . 

of the joint 2 torque limitations. The adjusted DH parameters of the gripper are _d_ = 0.120 _m_ , _a_ = 0, α = 0, and θ = 0. The planned trajectory and the control input for the MMRs by the online motion planner (Section 3.2) are sent to the respective MMRs. The trajectory tracking controllers for the mobile base and manipulator uses online motion planner’s computed control 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0007-14.png)


Figure 8: Experimental Setup of two in-house developed nonholonomic MMRs. 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

8 

input as feed forward and PID feedback controller to ensure desired trajectory tracking. It uses external motion capture system data and joints encoder data for the mobile base and manipulator feedback. 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0008-03.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0008-04.png)



![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0008-05.png)


**----- Start of picture text -----**<br>
(a) t  = 0  s (b) t  = 15.10 s<br>(c) t  = 20  s (d) t  = 47 s<br>**----- End of picture text -----**<br>


Figure 9: Two MMRs transport the rectangular object. The MMRs encounter a dynamic obstacle and started avoidance maneuver (Fig. 9b). It successfully avoids the dynamic obstacle 9c) and reaches the goal point 9d) 

Fig. 9 shows the snap of the object transport from the start (Fig. 9a) to the goal (Fig. 9d). It encounters a dynamic obstacle and start avoidance maneuver. Fig. 9b shows when the formation approaches the dynamic obstacle and finally avoids (Fig. 9c) the obstacle to reach the goal (Fig. 9d). 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0008-08.png)


Figure 10: Trajectory of the CoM of the object. The subscript d and m of the legend represents the planned and actual values. 

Fig. 10 shows the planned and the actual trajectory of the CoM of the transported object. The position error remains within 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0008-11.png)


Figure 11: The distance between the two EE during the object transportation. 

0.05 _m_ , and the orientation error remains within 0.15 _rad_ . The _z_ height increases near _t_ = 10 _s_ and _t_ = 28 _s_ before taking sharp turn to reduce the inter robot distance and turning radius. The error in fixed distance between the EEs’ grasping point in Fig. 11 shows that the coordination between the MMRs has been maintained. 

## _4.3 Comparison_ 

We present a comparison of performances of our proposed path planning algorithm for the environment shown in Fig. 5e and motion planning algorithms for a simplified environment where all the three algorithm (proposed, [14, 25]) works. We have run all the algorithms in Python on a Laptop equipped with an AMD Ryzen 5800H CPU and 16 GB RAM. The comparison results are presented as follows. 

_Path Planner:_ We compare our proposed path planning algorithm with the IRIS-based algorithms [14, 25] and a RRT Connect like technique [29] (computes only path) for the environment shown in Fig. 5e. Table 2 shows the comparison of path length and the computation time for ten runs of each algorithm. 

Table 2: Path Planner Comparison. 

|||Path Length<br>mean±sd(_m_)|Computation Time<br>mean±sd(_s_)|
|---|---|---|---|
||Proposed|9.22±0|0.09±0.03|
||_Keshab et al._[25]|9.87±0|3.74±1.60|
||_Alonso-Mora et al._[14]|12.09±3.88|8.36±6.28|
||_Zhang et al._[29]|12.61±4.20|35.01±14.02|



The convex optimization-based path planning approaches in [27, 14] rely on randomly generated seed points to compute the path and its corresponding obstacle-free convex region. Such random seeding coupled with convex optimization incurs high computational cost. The targeted seeding strategy proposed in [25] shows improved performance relative to fully samplingbased techniques [14, 29]. Our method deterministically generates the shortest feasible path and analytically computes the associated obstacle-free convex region thereby reduces the computational time. 

_Motion Planner:_ We compare the computational time and control effort of our proposed online motion planning technique with the holonomic MMRs’ planning algorithm proposed by _Keshab et al._ [25] and _Alonso-Mora et al._ [14]. All algorithms plan the motion of two MMRs in a dynamic environment with 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

9 

a dynamic obstacle with environment details mentioned in Section 3.1 of the attached file. We compare our nonholonomic planning framework against holonomic baseline, as to the best of our knowledge there exist no other nonholonomic multi-robot collaborative motion planners that address dynamic obstacle avoidance. The MMRs are the same except for the base motion constraints: nonholonomic and holonomic. Computational time is measured for each local planning horizon. The control effort is computed for a complete trajectory. As shown in the Table 3, the computation time and the control efforts of our method are lower than the algorithm in [14] and slightly higher than the algorithm proposed in [25]. The nonholonomic constraint for the mobile base reduces the solution space compared to its holonomic counterpart, resulting in increased computation time and control efforts. The proposed method achieves real-time operation in Python and we anticipate substantially faster runtime with C++ implementation. 

Table 3: Motion Planner Comparison. 

||Computation Time(s)|Computation Time(s)|
|---|---|---|
||min|mean±sd<br>max|
|Proposed<br>_Keshab et al._[25]<br>_Alonso-Mora et al._[14]<br>Proposed<br>_Keshab et al._[25]<br>_Alonso-Mora et al._[14]|0.199<br>0.227<br>0.46<br>�||**_u_**||2<br>64.869<br>36.136<br>78.754|0.580±0.231<br>1.855<br>0.272±0.035<br>0.346<br>0.857±0.256<br>1.26<br>Control Efort<br>||**_u_**||2 mean±sd<br>0.676±0.468<br>0.435±0.183<br>0.984±0.759|



## 5 Conclusion 

The optimization-free ellipse based polygon computation algorithm is a trade-off, where the polygon suboptimality significantly reduces the computational time. This trade-off does not affect the subsequent NMPC-based planning stage, as the ellipses are aligned with the piece-wise reference path segments and adaptively inflated to ensure adequate obstacle free space for kinodynamic constrained motion and dynamic obstacle avoidance. The proposed path planning technique computes both the path and its associated convex region within 120 _ms_ indicating that the path can be recomputed online during the task execution. 

The simulation and experimental results demonstrate that the motion planner generates kinodynamically feasible, collisionfree trajectories in dynamic environments in real time, indicating the strong potential for deployment in factory and warehouse like settings. Motion planning for cooperative MMRs during object transportation remains particularly challenging, especially for nonholonomic MMRs due to the kinodynamic constraints and the rigid object-manipulator coupling that must be respected during task executions. 

Our simulations and hardware experiments indicate that the trajectory may exhibits non-smooth transitions at the intersection of the obstacle-free convex polygon. However, this did not adversely affect the experiments as planner ensures the controls constraints and the low-level tracking controller effectively managed traction loss in the mobile base. In the future, we will address the trajectory smoothness at the transitions. 

## References 

- [1] O. Khatib, K. Yokoi, K. Chang, D. Ruspini, R. Holmberg, and A. Casal, “Coordination and decentralized cooperation of multiple mobile manipulators,” _Journal of Robotic Systems_ , vol. 13, no. 11, pp. 755–764, 1996. 

- [2] P. Xu, J. Zhang, Y. Cui, K. Zhang, and Q. Tang, “Modeling and coordinated control of multiple mobile manipulators with closed-chain constraints,” _International Journal of Control, Automation and Systems_ , vol. 21, pp. 1296–1308, 4 2023. 

- [3] X. Zhao, Y. Zhang, W. Ding, B. Tao, and H. Ding, “A dualarm robot cooperation framework based on a nonlinear model predictive cooperative control,” _IEEE_ / _ASME Transactions on Mechatronics_ , vol. 29, no. 5, pp. 3993–4005, 2024. 

- [4] S. Erhart and S. Hirche, “Adaptive force/velocity control for multi-robot cooperative manipulation under uncertain kinematic parameters,” in _2013 IEEE_ / _RSJ International Conference on Intelligent Robots and Systems_ , 2013, pp. 307–314. 

- [5] P. Culbertson and M. Schwager, “Decentralized adaptive control for collaborative manipulation,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , 2018, pp. 278–285. 

- [6] C. K. Verginis, A. Nikou, and D. V. Dimarogonas, “Communication-based decentralized cooperative object transportation using nonlinear model predictive control,” in _2018 European Control Conference (ECC)_ , 2018, pp. 733–738. 

- [7] G.-B. Dai and Y.-C. Liu, “Distributed coordination and cooperation control for networked mobile manipulators,” _IEEE Transactions on Industrial Electronics_ , vol. 64, no. 6, pp. 5065–5074, 2017. 

- [8] A. Marino, “Distributed adaptive control of networked cooperative mobile manipulators,” _IEEE Transactions on Control Systems Technology_ , vol. 26, no. 5, pp. 1646–1660, 2018. 

- [9] Y. Ren, S. Sosnowski, and S. Hirche, “Fully distributed cooperation for networked uncertain mobile manipulators,” _IEEE Transactions on Robotics_ , vol. 36, no. 4, pp. 984– 1003, 2020. 

- [10] K. Patra, A. Sinha, and A. Guha, “Online capability based task allocation of cooperative manipulators,” _Journal of Intelligent_ & _Robotic Systems_ , vol. 110, p. 23, 3 2024. 

- [11] J. Du, Y. Liang, H. Tao, Y. Xu, L. Zhu, and H. Ding, “Load sharing in distributed collaborative manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 4, pp. 3390–3397, 2025. 

- [12] J. Desai and V. Kumar, “Nonholonomic motion planning for multiple mobile manipulators,” in _Proceedings of International Conference on Robotics and Automation_ , vol. 4, 1997, pp. 3409–3414 vol.4. 

- [13] H. Tanner, S. Loizou, and K. Kyriakopoulos, “Nonholonomic navigation and control of cooperating mobile manipulators,” _IEEE Transactions on Robotics and Automation_ , vol. 19, no. 1, pp. 53–64, 2003. 

10 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

- [14] J. Alonso-Mora, S. Baker, and D. Rus, “Multi-robot formation control and object transport in dynamic environments via constrained optimization,” _The International Journal of Robotics Research_ , vol. 36, no. 9, pp. 1000–1021, 2017. 

- [15] Z. Cao, N. Gu, J. Jiao, S. Nahavandi, C. Zhou, and M. Tan, “A novel geometric transportation approach for multiple mobile manipulators in unknown environments,” _IEEE Systems Journal_ , vol. 12, no. 2, pp. 1447–1455, 2018. 

- [16] J. Jiao, Z. Cao, N. Gu, S. Nahavandi, Y. Yang, and M. Tan, “Transportation by multiple mobile manipulators in unknown environments with obstacles,” _IEEE Systems Journal_ , vol. 11, no. 4, pp. 2894–2904, 2017. 

- [17] R. Tallamraju, D. H. Salunkhe, S. Rajappa, A. Ahmad, K. Karlapalem, and S. V. Shah, “Motion planning for multimobile-manipulator payload transport systems,” in _2019 IEEE 15th International Conference on Automation Science and Engineering (CASE)_ , 2019, pp. 1469–1474. 

- [18] A. Nikou, C. Verginis, S. Heshmati-alamdari, and D. V. Dimarogonas, “A nonlinear model predictive control scheme for cooperative manipulation with singularity and collision avoidance,” in _2017 25th Mediterranean Conference on Control and Automation (MED)_ , 2017, pp. 707–712. 

- [19] F. Kennel-Maushart and S. Coros, “Payload-aware trajectory optimisation for non-holonomic mobile multi-robot manipulation with tip-over avoidance,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 9, pp. 7669–7676, 2024. 

- [20] O. Shorinwa and M. Schwager, “Scalable collaborative manipulation with distributed trajectory planning,” in _2020 IEEE_ / _RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2020, pp. 9108–9115. 

- [21] C. Wu, H. Fang, Q. Yang, X. Zeng, Y. Wei, and J. Chen, “Distributed cooperative control of redundant mobile manipulators with safety constraints,” _IEEE Transactions on Cybernetics_ , pp. 1–13, 2021. 

- [22] J. Hu, W. Liu, H. Zhang, J. Yi, and Z. Xiong, “Multi-robot object transport motion planning with a deformable sheet,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 9350–9357, 2022. 

- [23] L. Pei, J. Lin, Z. Han, L. Quan, Y. Cao, C. Xu, and F. Gao, “Collaborative planning for catching and transporting objects in unstructured environments,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 2, pp. 1098–1105, 2024. 

- [24] R. Mao, H. Gao, and L. Guo, “A novel collision-free navigation approach for multiple nonholonomic robots based on orca and linear mpc,” _Mathematical Problems in Engineering_ , vol. 2020, pp. 1–16, 6 2020. 

- [25] K. Patra, A. Sinha, and A. Guha, “Kinodynamic motion planning for collaborative object transportation by multiple mobile manipulators,” _Journal of Mechanisms and Robotics_ , vol. 17, no. 12, p. 121003, 09 2025. 

- [26] H. Choset, K. Lynch, S. Hutchinson, G. Kantor, and W. Burgard, _Principles of Robot Motion: Theory, Algorithms, and Implementations_ , ser. Intelligent Robotics and Autonomous Agents series. MIT Press, 2005. 

- [27] R. Deits and R. Tedrake, “Computing large convex regions of obstacle-free space through semidefinite programming,” in _WAFR_ , 2014. 

- [28] J. A. E. Andersson, J. Gillis, G. Horn, J. B. Rawlings, and M. Diehl, “CasADi – A software framework for nonlinear optimization and optimal control,” _Mathematical Programming Computation_ , vol. 11, no. 1, pp. 1–36, 2019. 

- [29] H. Zhang, H. Song, W. Liu, X. Sheng, Z. Xiong, and X. Zhu, “Hierarchical motion planning framework for cooperative transportation of multiple mobile manipulators,” 2022. [Online]. Available: https://arxiv.org/abs/2208.08054 

## Appendix I: Additional Details of Algorithm 

We present some additional implementation details of our proposed Algorithms in Section 5, List of Symbols in Section 5. The analytical ellipse computation technique is described in detail in Section 5, and the dilation of the ellipse is described in Section 5. We add a tabulated list for symbols used in the manuscript in Section 5. 

Algorithm 1 illustrated convexify simple concave polygon. Here we explain the FindEllipse function in details in Algorithm 2 and DilateEllipse in Algorithm 3. 

## _Ellipse Computation_ 


![](1_survey/papers/md/Patra2025Motion_figs/Patra2025Motion.pdf-0010-22.png)


Figure 12: Ellipse fitting at the center _d_ of the path segment _S_ 2. 

This section describe the ellipse computation method with mathematical details, used in the Polygon Convexification Algorithm 1. We find the Rotation matrix _R_ putting a local frame origin at the center ( _d_ ) of the ellipse and _x_ -axis along the path segment _S_ 2 as shown in Fig. 12. The ellipse computation method has been described in Algorithm 2. 

Once we have _x_[∗] , the nearest concave vertex to _d_ , the distance of _x_[∗] from the origin _d_ of the ellipse should be less than the semimajor axis _a_ , otherwise one cannot fit the ellipse with _R_ , _a_ , d, _x_[∗] _j_[.] We check the degeneracy in lines 1-2 and modify _a_ if required. Then we compute the semi-minor axis _b_ using the fundamental ellipse equation for Cartesian coordinates. 

## _Ellipse Dilation_ 

We describe the ellipse dilation method in Algorithm 3. We dilate the base ellipse computed in the first step of the polygon 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

11 

|**Algorithm 2**FindEllipse(_R_,_a_,d,_x_∗)<br>**Input:** Rotation Matrix_R_, Semi-major axis_a_<br>Center of Ellipse d, The nearest concave point _x_∗<br>**Output:** Ellipseκ(C,_d_)<br>1: _dist_x_∗=Euclidean Distance of _x_∗from_d_<br>2: **if** _dist_x_∗>(_a_−ϵ)**then**<br>▷ϵ =0.001, when _x_∗is distant<br>eliminates degeneracy<br>3:<br>_a_=_max_(1.5∗_dist_x_∗,2∗_a_)<br>▷Modify_a_with<br>parameter 1.5,2 so _x_∗can used for ellipse ftting<br>4: **end if**<br>5: _x_∗(_x_,_y_)=_R_(_x_∗−_d_)<br>▷Converting to local ellipse frame<br>6: _b_=|_x_∗<br>_y_/<br>~~�~~<br>1−( _x_∗_x_<br>_a_ )2|<br>▷Find the minor axis of the ellipse<br>touching_x_∗(_x_,_y_) using ( _x_∗<br>_x_<br>_a_ )2+(<br>_x_∗<br>_y_<br>_b_ )2 =1<br>7: Λ =_diag_(_a_,_b_)<br>8: _C_ =_RT_Λ_R_<br>9: **return**C,_d_<br>convexifcation technique to eliminate the remaining concave<br>vertices. The dilation step length is computed analytically based<br>on the nearest concave vertices of the base ellipse and is de-<br>scribed in the Algorithm3step-wise.<br>**Algorithm 3**DilateEllipse(κ0(_C_0,_d_0),_R_,_x_∗<br>_j_)<br>**Input:** Base Ellipseκ0, The nearest concave point_x_∗<br>_j_<br>**Output:** Ellipseκ_j_<br>1: _a_,_b_←κ0 ▷Extract semi-major and semi-minor axis from<br>κ0<br>2: _x_∗(_x_,_y_)=_R_(_x_∗<br>_j_ −_d_)<br>▷Converting to local ellipse frame<br>3: _angle_=tan−1(<br>_x_∗<br>_y_·_a_<br>_x_∗_x_·_b_)<br>▷Finding the ellipse angle of vector<br>from_d_to_x_∗<br>_j_ with the semi major axis<br>4: α= _x_∗<br>_y_/(_b_·sin(_angle_))<br>▷Computing the scalingαfrom<br>projection of_x_∗<br>_y_ to the minor axis<br>5: _C_ =α·_C_0,_d_ =_d_0<br>6: κ_j_ ←_C_,_d_<br>7: **return**κ_j_<br>List ofSymbols<br>We list the symbols used in the manuscript in the following<br>tables with descriptions.|Table 4: Description of Symbols|
|---|---|
||Symbol<br>Description|
||_n_<br>Number of mobile manipulator robots (MMRs)<br>{**_w_**}<br>The world fxed reference frame<br>{**_o_**}<br>Object coordinate frame attached to the object<br>center of mass<br>{**_b_**_i_}<br>Body coordinates attached to the center of_i_-th<br>mobile base<br>_qm_,_i_<br>Pose of the mobile base of_i_-th MMR<br>_pi_<br>Position of the mobile base inR2 of_i_-th MMR<br>ϕ_i_<br>Orientation of the mobile base inRof_i_-th MMR<br>_ni_<br>Number of joint of_i_-th MMR<br>_qa_,_i_<br>Joint displacement of_i_-th MMR<br>_qi_<br>Combined pose (mobile base) and manipulator<br>joint displacement of_i_-th MMR<br>˙_qi_<br>Combined pose (mobile base) and manipulator<br>joint of_i_-th MMR<br>_pee_,_i_<br>Position of the_i_-th end efector inR3<br>ϕ_ee_,_i_<br>Orientation of the_i_-th end efector inR3<br>_vi_<br>Linear velocity of the mobile base of_i_-th MMR<br>ω_i_<br>Angular velocity of the mobile base of_i_-th MMR<br>˙_qa_,_i_<br>Joint velocity of the manipulator of the_i_-th MMR<br>_ui_<br>Combined velocity of mobile base and the<br>manipulator arm of_i_-th MMR<br>_k_<br>Discrete time step<br>_q_<br>_a_,_i_<br>_i_-th manipulator’s joint position lower limit vector<br>_qa_,_i_<br>_i_-th manipulator’s joint position upper limit vector<br>_u_<br>~~_i_~~<br>The admissible control lower limits of_i_-th MMR<br>_ui_<br>The admissible control upper limits_i_-th MMR<br>Q_i_<br>Admissible displacement of_i_-th MMR<br>U_i_<br>Admissible control of_i_-th MMR<br>F<br>Multi-MMR formation<br>_ori_<br>Grasp pose of_i_-th EE from the object CoM<br>measured in{**_o_**}<br>_p_<br>The position of the object CoM inR3<br>_o_<br>The orientation of the object CoM inR3<br>_Q_<br>The confguration of_n_MMRs<br>X<br>The formation confguration<br>B(X)<br>The space occupied by the formation<br>_W_<br>A structured and bounded environment having<br>both static and dynamic obstacles<br>O<br>The set of static obstacles in_W_<br>O_dil_<br>The set of dilated statics obstacles<br>_W free_<br>Static obstacle-free region_W_\ O ∈R2<br>O_dyn_<br>The dynamic obstacles in the environment_W_<br>_ps_<br>The start position<br>_pg_<br>The goal position<br>_S_<br>Linear piece-wise static obstacle-free shortest path<br>_S i_<br>Path segment of_S_<br>_rf_<br>The radius of the circle enclosing the formationF<br>V<br>Nodes of the graph<br>E<br>Edges of the graph<br>W<br>Weight ofEof the graph<br>G(V,E,W)<br>Graph<br>_wi_<br>Vertices of the path_S_<br>V_s_<br>Set of visible vertices of the statics obstacles<br>from_wi_, ∀_i_<br>P_cc_,_i_<br>Static obstacle-free simple polygon around_S i_<br>P_cc_<br>Set of all simple polygon P_cc_,_i_ around_S_<br>C<br>A 2×2 symmetric positive defnite matrix to<br>maps a unit radius circle to an ellipse<br>_R_<br>Rotation matrix that aligns the ellipse axes to<br>the world reference frame axes<br>Λ =_diag_(_a_,_b_)<br>A diagonal scale matrix<br>_a_,_b_<br>The length of the ellipse semi-major and minor axes<br>d<br>Defnes the center of the ellipse.<br>κ(C,d)<br>Ellipse in thegroundplane|



12 

Preprint – Motion Planning of Cooperative Nonholonomic Mobile Manipulators 

|Symbol|Description|
|---|---|
|V_cc_|Set of concave vertices of a simple polygon|
|_x_∗|Nearest concave vertices to d|
|_H_|Hyperplane|
|P_S_|Set of convex polygon around_S_|
|_pr_(_ct_)|Time-normalized smooth trajectory guess|
|_ct_|Normalized time parameter∈[0,1]|
|_Nh_|Planning horizon segment|
|_Th_|Planning horizon time|
|_Te_|Execution time|
|_Tc_|Discretization time-step|
|**Wu**|Diagonal weight-age matrix for control efort|
|**We**|Diagonal weight-age matrix for the trajectory error|
|_ek_|Tracking error|
|λ|The index of the nearest reference path segment|
|_J_(X_k_,_uk_)|The Running cost|
|_JNh_|The terminal cost|
|_vop_|Operational velocity of the formation|
|_V_(X)|Set of vertices of the bounding polygons of the object and the_n_MMRs|
|_dsa fe_|The safety distance for static obstacle avoidance|
|_dsafe_,_dyn_|The safetydistance for dynamic obstacle avoidance|



