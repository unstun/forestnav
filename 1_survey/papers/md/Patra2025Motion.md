---
citation_key: Patra2025Motion
arxiv_id: 2502.05462
arxiv_url: "https://arxiv.org/abs/2502.05462"
title: "Motion Planning of Cooperative Nonholonomic Mobile Manipulators"
authors_short: "Keshab Patra et al."
year: 2025
direction_tag: N_path_repair;P_nonholonomic_constraints
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:11:37Z
origin: ai+web
reviewed: false
---

# <sub>M</sub>otion <sub>P</sub>lanning of <sub>C</sub>ooperative <sub>N</sub>onholonomic <sub>M</sub>obile <sub>M</sub>anipulators

Keshab Patra <sup>ID</sup> <sup>1∗</sup>, Arpita Sinha <sup>ID</sup> <sup>2</sup>, and Anirban Guha<sup>1</sup>

<sup>1</sup>Department of Mechanical Engineering, Indian Institute of Technology Bombay, Mumbai, Maharashtra, India <sup>2</sup>Center for Systems and Control, Indian Institute of Technology Bombay, Mumbai, Maharashtra, India

## <sub>A</sub>bstract

We propose a real-time implementable motion planning framework for cooperative object transportation by nonholonomic mobile manipulator robots (MMRs) in dynamic environments. Our global planner finds a path from start to goal through the static, obstacle-free regions in the environment and generates a set of convex, static, obstacle-free regions around the path using a novel, fast, and computationally lightweight ellipse-based technique. We introduce a nonlinear Model Predictive Control (NMPC) based real-time implementable planning technique that jointly plans feasible motion for the mobile base and the manipulator’s arm and generates a kinodynamic feasible, collision-free trajectory for cooperative object transportation. Simulation and hardware experiments validate the eficiency of our proposed planning framework.

## <sub>1 I</sub>ntroduction

Robotic systems became integral to automation in manufacturing, remote exploration, warehouse management, and other areas. Cooperative multiple MMRs garner attention due to their low cost, small size, redundancy in heavy or oversized object transportation, and fixture-less multipart assembly requiring more Degrees of Freedom (DoF). A cooperative MMR system extends workspace coverage, flexibility, and redundancy with added complexity in robot coordination, communication, and motion planning. Multiple MMRs leverage the mobile bases’ locomotion ability and the arms’ manipulation ability for object transportation and manipulation in a large workspace.

Nonholonomic mobile bases are widespread in robotic applications because of their advantages in a reduced number of actuators, simplified wheels, and better load-carrying capacity. Nonholonomic MMRs can work better than their holonomic counterparts on uneven ground surfaces as they restrict sideways motion, which leads to increased stability, traction, and controllability on uneven surfaces. The nonholonomic mobile base of the MMRs restricts sideways motion, including non-integrable kinematic constraints. Hence, there are more intricacies in cooperative motion planning and trajectory generation than in the holonomic counterpart.

The study on collaborative manipulators started with a virtual linkage model [1] representing the collaborative manipulation systems to generate closed-chain constraints [2] between the object and the MMRs for motion synchronization and coordination. The dual arm cooperative control problem has been addressed by NMPC [3]. The coordination scheme for multi-MMR cooperative manipulation and transportation comprises of centralized [4], decentralized [5, 6] and distributed [7, 8, 9] control framework. Task allocation [10, 11] algorithm ensures eficient utilization of the capabilities of the cooperative manipulators. The collision-free navigation started with a variational-based method [12] that demonstrated static obstacle avoidance for a two MMR system with poor scalability. Dipolar inverse Lyapunov functions fused with the potential field-based navigation function [13] plan collision-free motion in static environments to transport deformable material by multiple MMRs with a little scope of formation control.

Optimization-based motion planning technique [14] for holonomic MMRs in dynamic environments uses obstacle-free convex polygons around the formation in the position-time space. It optimizes the holonomic MMRs’ pose to retain the cooperative MMR system inside the obstacle-free polygon. A geometric path planning approach [15, 16] for multiple MMRs transport an object avoiding static obstacles. A rectangular passagewaybased approach [15] finds the optimal system width and moving direction in the static obstacle-free area for navigation. These methods do not include motion constraints to provide guaranteed feasible motion for nonholonomic MMRs.

A kinematic motion planning technique [17] plans for spatial collaborative payload manipulation using a hierarchical approach. The technique’s conservative approximation of the obstacles as uniform cylinders highly restricts navigation in tight spaces with high aspect ratios polygonal obstacles. MPC-based motion planning techniques for static obstacle avoidance have been presented in [18, 19]. An alternating direction method of multipliers-based distributed trajectory planning algorithm [20] plans trajectory in a static environment. A distributed formation control technique [21] utilizes constrained optimization for object transportation in a static environment. Motion Planning for deformable object transportation [22, 23] in a static environment uses optimization techniques. A reciprocal collision avoidance algorithm [24] combined with MPC doesn’t maintain any formation. These generic planning algorithms cannot be used as they do not maintain the rigid formation required for collaborative MMRs. An NMPC-based kinodynamic motion planning technique [25] plans motion for object transportation by multiple MMRs in dynamic environments. The proposed planning technique is limited to holonomic MMRs and environments with convex static obstacles.

We propose an end-to-end trajectory planning framework for collaborative object transportation by nonholonomic MMRs. Our proposed algorithm plans the trajectory in two steps: offline path planning and online motion planning. To the best of our knowledge, the end-to-end planning for nonholonomic MMRs has not been done before. The ofline planning algorithm computes a linear, piecewise path from start to goal using the visibility vertices algorithm [26] and defines the static, obstaclefree region for motion planning optimization. Motivated by [27], we have developed a novel, fast, ellipse-based optimizationfree convex polygon computation algorithm to define the static obstacle-free region around the piecewise linear path. Starting from computing a polygon around the path segments using its visibility vertices, we convexify it by eliminating the concave vertices using the tangents of ellipses. We compute the ellipse, aligning its major axis along the path segment that touches the nearest concave vertex, and inflate it to eliminate subsequent concave vertices in the same polygon. The proposed planning technique eliminates the restriction of convex obstacles of IRISbased planning algorithms [27, 14, 25] and convex optimization, guaranteeing the path segment will remain within it.

The major contributions of this article are as follows.

1. We propose a fast ellipse-based optimization-free convex polygon computation algorithm to define the static obstacle-free region around the linear piece-wise path using its visible vertices. The convex obstacle-free region is regarded as inequality constraints in the NMPC for motion planning.

2. We introduce an NMPC-based, real-time implementable online motion planner that jointly plans for the nonholonomic MMR’s base and the manipulator. The planner computes a kinodynamic feasible collisionfree motion plan for the multiple MMRs in a dynamic environment.

## <sub>2 P</sub>roblem <sub>F</sub>ormulation

A system of n nonholonomic MMRs grasps a rigid object at its periphery as shown in Fig. 1 to collaboratively transport the object without any collision.

![](Patra2025Motion_figs/546dc559ecc32ffd80bf90c63700d050020c61e346cf51b4f10d4de87fc5c6a4.jpg)  
Figure 1: Formation of five non-holonomic MMRs holding an object. The MMRs grasped the object to transport collaboratively without any collision.

{w} defines the world fixed reference frame. An object coordinate frame {o} is attached to the object center of mass (CoM), and each MMR has its own body coordinates $\{ { \pmb b } _ { i } \}$ attached to the center of its mobile base. Without specific mention, all the quantities are defined in {w}. The collaborative manipulation system is defined in the following subsections.

## 2.1 Mobile Manipulator and Collaborative Formation

The mobile base of i-th MMR is defined with pose $q _ { m , i } =$ $[ p _ { i } ^ { T } , \phi _ { i } ] ^ { T }$ where $p _ { i } \in \mathbb { R } ^ { 2 }$ and $\phi _ { i } \in \mathbb { R }$ <sup>,</sup>are the position and orien-<sup>,</sup> <sup>ϕ ϕ</sup>tation of the mobile base. The manipulator of i-th MMR has $n _ { i }$ number of joints and it’s displacement is defined as $q _ { a , i } =$ $[ q _ { \underline { { { a } } } , i 1 } , q _ { \underline { { { a } } } , i 2 } , \cdot \cdot \cdot , q _ { { a } , i n _ { i } } ] ^ { T }$ The whole MMR is defined by $q _ { i } \ =$ $[ q _ { m , i } ^ { T } , q _ { a , i } ^ { T } ] ^ { T }$ <sup>, ,</sup>. The i-th EE’s position and orientation is defined in <sup>,</sup>{w} as $p _ { e e , i } \in \mathbb { R } ^ { 3 }$ and $\phi _ { e e , i } \in \mathbb { R } ^ { 3 }$ . The i-th non-holonomic MMR’s <sup>, ϕ</sup>first-order dynamics is $\dot { q } _ { i } = [ \nu _ { i } \cos ( \phi _ { i } ) , \nu _ { i } \sin ( \phi _ { i } ) , \omega _ { i } , \dot { q } _ { a , i } ] ^ { T }$ where <sup>ϕ , ϕ ,</sup> <sup>ω , ,</sup>the control inputs are mobile base’s linear and angular velocities $\nu _ { i } , \omega _ { i }$ respectively and the manipulator’s joint velocities $\dot { q } _ { a , i } ,$ <sup>ω</sup>therefore, $u _ { i } = [ \nu _ { i } , \omega _ { i } , \dot { q } _ { a , i } ]$

We represent the coupled first order system dynamics for i-th MMR by a discrete-time non-linear system as

$$
q _ {i} ^ {k + 1} = f (q _ {i} ^ {k}, u _ {i} ^ {k})\tag{1}
$$

where $k$ is the discrete time step. The admissible states and control inputs are defined by Eqn. 2

$$
\underline {{q}} _ {a, i} \leq q _ {a, i} \leq \overline {{q}} _ {a, i}, \underline {{u}} _ {i} \leq u _ {i} \leq \overline {{u}} _ {i}, \forall i \in [ 1, n ]\tag{2}
$$

where $\underline { { q } } _ { a . i } , \overline { { q } } _ { a , i }$ represents the manipulator’s joint position limit <sup>,</sup>vector and $\underline { { u } } _ { i } , \overline { { u } } _ { i }$ are the admissible control limits. The set of admissible states $Q _ { i }$ and control inputs $\mathcal { U } _ { i }$ are indicated by joint position and velocity vectors’ limit (Eqn. (2)), $Q _ { i } = [ \underline { { { q } } } _ { a . i } , \overline { { { q } } } _ { a , i } ] ,$ $\mathcal { U } _ { i } = [ \underline { { u } } _ { i } , \overline { { u } } _ { i } ]$

The EE of the i-th MMR of the multi-MMR formation $\mathcal { F }$ (Fig 1) grasps the object at $^ o r _ { i }$ defined in object frame o, where the superscript o indicates it’s reference frame {o}. The formation configuration is defined by $\boldsymbol { X } = [ p ^ { T } , o ^ { T } , Q ^ { \dot { T } } ] ^ { \dot { T } }$ , where $p \in \mathbb { R } ^ { 3 }$ is the position and o $\in \mathbb { R } ^ { 3 }$ <sup>, ,</sup>is the orientation of the object CoM, $Q = \dot { [ } q _ { 1 } ^ { T } , q _ { 2 } ^ { T } , \cdots , q _ { n } ^ { T } ] ^ { T }$ is the configuration of n MMRs. The <sup>, , ,</sup>space occupied by the formation is defined as B(X).

## 2.2 Environments

A structured and bounded environment having both static and dynamic obstacles is defined as W. O represents the set of static obstacles in W. The static obstacle-free workspace is defined by $W _ { f r e e } = W \setminus O \in \mathbb { R } ^ { 2 }$ . The set of dynamic obstacles in the environment is defined as $O _ { d y n }$ . The start position $p _ { s }$ and the goal position $p _ { g }$ of the object CoM are in the obstacle-free space $W _ { f r e e } .$

The planning objective is to design a motion planning framework such that 1) the MMRs can cooperatively transport the object without any collision. 2) the generated trajectory is kinodynamically feasible and within the admissible limits of the MMRs minimizing the control input of MMRs. 3) the planner can handle any rigid object, grasping configuration and static concave obstacles directly.

## <sub>3 M</sub>otion <sub>P</sub>lanning

We solve the motion planning problem for cooperative multi-MMRs in two steps: ofline path planning and online motion planning shown in Fig. 2. In the ofline path planning step, we compute a static obstacle-free linear piece-wise shortest distance path (S ) between the start and the goal location using ofline path planner in Section 3.1. Then we compute a set of connected convex region around the path using our proposed convex polygon computation algorithm in 3.1.2.

![](Patra2025Motion_figs/c4840005ef5f0bed647f58666ca8e80e7cd6c12e49783bf65ce7b6230b166e91.jpg)  
Figure 2: Two step motion planning process: ofline path planning and online motion planning.

In the next step, an online motion planner (Section 3.2) computes a feasible motion plan for the collaborative MMRs in receding horizons. The planner generates a kinodynamically feasible trajectory in the dynamic environment using $p _ { r } ( c _ { t } )$ as an initial guess. The generated trajectory is free from collision with the static and dynamic obstacles and collision among the MMRs and with the object.

![](Patra2025Motion_figs/bd65c4b1009d7ef08b75fec93970469d67faa094f1d97fa0d55ea38371c573b4.jpg)  
Figure 3: Ofline path planning and convex polygon computation process around S .

## 3.1 Global Path Planner

The global path planner computes a static obstacle-free path S for the MMRs’ between the start and goal in ofline employing visibility vertices finding algorithm [26]. Then it computes a set of connected convex obstacle-free polygon around S . Fig. 3 shows the outline of the path planning process.

## 3.1.1 Path Computation

The global path planner dilates O by a distance $r _ { f }$ so that we consider the formation F at any point p,the CoM of the grasped object. The dilation distance $r _ { f }$ is the radius of a circle located at $p ,$ inside which the formation could always be enclosed. The planner substitutes the mutually intersecting dilated obstacles $O _ { d i l }$ with their union. A visibility vertices finding algorithm [26] creates a visibility map considering $O _ { d i l }$ and the start and goal point. The vertices from the visibility map are added as node V to a graph $\mathcal { G } ( \mathcal { V } , \mathcal { E } , \mathcal { W } )$ . An edge E is added between two mu-<sup>, ,</sup>tually visible nodes using the visibility map with the Euclidean distance between them as weight W. A graph search algorithm computes the shortest linear piece-wise path S between the start $p _ { s }$ and the goal $p _ { g }$ location. Fig. 4 shows the computed path S with linear segments $\bar { S } _ { 1 } , \bar { S _ { 2 } } , \bar { S _ { 3 } } , \bar { S _ { 4 } }$ and vertices $w _ { 1 } , w _ { 2 } , w _ { 3 } , w _ { 4 } , w _ { 5 }$

![](Patra2025Motion_figs/6a22799028503f2da4bc796ceb4a4a7562b1c837b72105c9532069c9a8601367.jpg)  
Figure 4: Path Polygon for $S _ { 2 }$ computed using the visible ver tices of $W _ { 2 }$ and $W _ { 3 }$ .

## 3.1.2 Convex Polygon Computation

We compute a static obstacle-free polygon around a path segments $S _ { i } \in S$ and convexify. We consider O and the vertices w of the path to obtain the set of vertices $\mathrm { V } _ { s }$ present in the static environment and visible from $w _ { i }$ ∀i (Fig. 4). A simple polygon is defined for each vertex $w _ { i } ,$ <sup>,</sup>∀i by cyclically connecting its visible <sup>,</sup>vertices. The polygon remains in $W _ { f r e e } .$ . The union of polygons obtained for $w _ { i }$ and $w _ { i + 1 }$ of a path segment $S _ { i }$ defines a static obstacle-free simple polygon $\mathrm { P } _ { c c , i }$ around $S _ { i } \in S$ . Fig. 4 shows <sup>,</sup>the computed polygons for the path segment $S _ { 2 }$ using the polygons around $w _ { 2 }$ and $w _ { 3 }$ . The union of the two polygons (green and blue) in red boundary defined around $w _ { 2 }$ and w provides a static obstacle-free polygon $\mathrm { P } _ { c c , 2 }$ around $S _ { 2 }$ . A set of polygon $\mathcal { P } _ { c c }$ <sup>,</sup>for S is computed similarly. The computed polygons are generally concave. Convexification is needed for the static obstacle avoidance constraints in motion planning optimizations. We compute a set of convex polygons $\mathcal { P } _ { S }$ analytically as a subset of their original concave polygons in $\mathcal { P } _ { c c }$ . To eliminate the concave vertices of $\mathrm { P } _ { c c , i }$ we use tangents of ellipses at concave vertices, <sup>,</sup>whose major axis aligned with $S _ { i }$ . The convexification steps are illustrated in the Algo. 1.

We define an ellipse in the ground plane as

$$
\kappa (\mathrm{C}, \mathrm{d}) = \{x = \mathrm{C} \overline {{x}} + \mathrm{d}: \| \overline {{x}} \| \leq 1, x \in \mathbb {R} ^ {2} \}\tag{3}
$$

where C is a $. 2 \times 2$ symmetric positive definite matrix that maps the deformation of a unit radius circle $( \left\| { \overline { { x } } } \right\| \leq 1 )$ to an ellipse. C is decomposed as $\mathbf { C } = R ^ { T } \Lambda R .$ , where R is a rotation matrix that aligns the ellipse axes to the world reference frame axes and $\boldsymbol { \Lambda } = d i a g ( a , b )$ is a diagonal scale matrix. The diagonal elements <sup>,</sup>a and b of Λ refer to the length of the ellipse semi-major and minor axes. d defines the center of the ellipse.

Algo. 1 initializes a polygon P with the concave polygon $\mathrm { P } _ { c c , i }$ It finds the concave vertices $\boldsymbol { \gamma } _ { c c }$ of P. If $\boldsymbol { \gamma } _ { c c }$ <sup>,</sup>is not empty, then it convexifies P in line $4 - 1 7$ . The algorithm computes the half-plane representation of P in line 19. In the polygon

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Polygon Convexification
Input: Concave Polygon  $P_{cc,i}$ , Path segment  $S_{i}$ 
Output: Convex Polygon P

1:  $P \leftarrow P_{cc,i}$ ;  $j \leftarrow 0$ 

2:  $V_{cc} \leftarrow$  ConcaveVertices(P)

3: if  $V_{cc} \neq \phi$  then

4: d  $\leftarrow$  Midpoint( $S_{i}$ ); R: major axis along  $S_{i}$ 

5:  $a \leftarrow 0.5\text{length}(S_{i}) + r_{f}$ 

6:  $x_{j}^{*} \leftarrow$  NearestVertex( $V_{cc}$ , d)

7:  $C_{j}, d \leftarrow$  FindEllipse( $R, a, d, x_{j}^{*}$ )  $\triangleright$  Use  $\|x_{j}^{*}\| = 1$ 

8:  $\kappa_{j} \leftarrow (C_{j}, d)$ 

9:  $a_{j} \leftarrow 2C_{j}^{-T}C_{j}^{-1}(x_{j}^{*} - d)$ ;  $b_{j} \leftarrow a_{j}^{T}x_{j}^{*} \triangleright$  Tangent of ellipse  $\kappa_{j}$  at  $x_{j}^{*}$ 

10: P,  $V_{cc} \leftarrow$  DiscardVertices( $a_{j}, b_{j}, P, V_{cc}$ )

11: while  $V_{cc} \neq \phi$  do

12: j = j + 1

13:  $x_{j}^{*} =$  NearestVertex( $V_{cc}$ , d)

14:  $\kappa_{j} \leftarrow$  DilateEllipse( $\kappa_{0}, R, x_{j}^{*}$ )

15: repeat line 9 - 10

16: end while

17: P : A  $\leftarrow [a_{0}^{T}, a_{1}^{T}, \cdots]^{T}$ , b  $\leftarrow [b_{0}, b_{1}, \cdots]^{T}$ 

18: else

19: P : (A, b)  $\leftarrow$  HalfPlanes(P)

20: end if

21: return P(A, b)
</div>

convexification process, the algorithm fits an ellipse $\kappa _ { 0 }$ center d at the midpoint of the path segment $S _ { i } \in S$ <sup>κ</sup>. The major axis is aligned with the path segment $S _ { i } ,$ the semi-major axis length $a = 0 . 5 l e n g t h ( S _ { i } ) + r _ { f }$ . The ellipse is inflated in the minor-axis <sup>.</sup>direction till it touches the nearest concave points $x _ { 0 } ^ { * }$ to d and an ellipse $\kappa _ { 0 }$ is computed in line $4 - 8 .$ The tangent to the ellipse <sup>κ</sup><sub>0</sub> at point $x _ { 0 } ^ { * }$ defines the inequality $H _ { 0 } = \{ x : \mathbf { a } _ { 0 } ^ { T } x \leq b _ { 0 } \}$ . After <sup>κ</sup>obtaining $H _ { 0 } ^ { \mathrm { { ^ { \circ } } } }$ in line $9 _ { ; }$ , we cut the polygon with $H _ { 0 }$ and keep the polygon that contains $S _ { i }$ and keep it as P (Fig. 5a). We discard the concave vertices outside the new polygon P from $\boldsymbol { \gamma } _ { c c }$ . If there is any concave vertices left $\mathcal { V } _ { c c } \neq \phi$ the ellipse $\kappa _ { 0 }$ is dilated to form an ellipse $\kappa _ { 1 }$ <sup>ϕ</sup>in line 14 keeping the aspect <sup>κ κ</sup>ratio same till it touches the nearest concave vertices $x _ { i } ^ { * } \in \mathcal { V } _ { c c }$ to d. The tangent to the ellipse at point $x _ { 1 } ^ { * }$ defines the inequality $H _ { 1 } = \{ x : \mathbf { a } _ { 1 } ^ { T } x \leq b _ { 1 } \}$ . After obtaining $H _ { 1 }$ in line 9, we cut the polygon with $H _ { 1 }$ and keep the polygon that contains $S _ { i }$ and keep it as ${ \mathrm { P } } ,$ as shown in Fig. 5b. The convexification process in line $1 1 - 1 6$ is repeated until no concave vertex left in the polygon $\mathcal { N } _ { c c } \neq$ (Fig. 5b-5d). After eliminating all the concave vertices, <sup>ϕ</sup>the polygon P becomes convex (Fig. 5d), and the half-plane representation of P is returned in line 17.

![](Patra2025Motion_figs/1172864ba7f55c37b5ba410d911ca87bb742401ddfa965d0285d93f447fda678.jpg)

![](Patra2025Motion_figs/38cf2b7c75a331484bd060667846e1eeaa08a1341b32b6ab2f69efa096c35cb9.jpg)

(a)  
![](Patra2025Motion_figs/cfea9b66351e8931555803da637ea9a59ec6e95fcae96c1a10787b901482fd45.jpg)  
(c)

(b)  
![](Patra2025Motion_figs/02a4040ede1d655ecfe622b3475946ac078a1ade5538d4f0368914bd56b50ad4.jpg)  
(d)

![](Patra2025Motion_figs/3cc246c0f0a5b558af97d02d33f7e901569135c9e7089f371ef337e5a83f4ee8.jpg)  
(e) Convex polygons (light green) around S  
Figure 5: Fig. $5 \mathrm { a } - 5 \mathrm { d }$ shows the steps of polygon convexification process for $S _ { 2 }$ . A tangent of an ellipse touching the nearest concave vertex (red line) of the polygon eliminates its concavity by cutting the polygon (black edges). The polygon (sky blue) containing the path segment has been kept. A convex polygon is formed (green polygon in Fig. 5d.)

The Fig. 5 shows the polygon convexification process of $\mathrm { P } _ { c c , 2 }$ defined for $S _ { 2 }$ <sup>,</sup>. An ellipse touching its nearest concave vertex to $S _ { 2 }$ , has been obtained and a tangent (red line) to the ellipse at this point has been drawn in Fig. 5a. The tangent cuts the polygon into two. The polygon (sky blue) containing the path segment has been kept. The ellipse has been dilated keeping the aspect ratio same in Fig 5b till it touches the nearest concave vertex (to $S _ { 2 } )$ of the new polygon. Here a very small portion of the polygon is cut by the tangent to the ellipse at this concave vertex. The process continues till any concave vertex remains and a convex polygon is formed (green polygon in Fig. 5d.)

Fig. 5e shows a set of convex polygons $\mathcal { P } _ { S }$ in light green around the path segment S computed using the Algo. 1. Every segment of S remains inside any convex polygon $\boldsymbol { \mathrm { P } } \in \mathcal { S } _ { S }$ defined in $W _ { f r e e } .$ We add additional intermediate control points in red dots in Fig. 5e on S . The control points are used to generate time-normalized smooth trajectory $p _ { r } ( c _ { t } )$ from the S using a Bézier curve with normalized time parameter $c _ { t } \in [ 0 , 1 ]$ . These <sup>,</sup>intermediate control points are inserted when a new convex polygon appears along the path S from the start point. A control point is added for the last path segment while exiting the intersection area of the last two polygons. The generated quadratic Bézier curve would remain in $W _ { f r e e }$ as any three consecutive control points remain within a single convex polygon. The timenormalized reference trajectory $p _ { r } ( c _ { t } )$ is used as an initial guess for the online motion planner.

## 3.2 Online Motion Planner

The global path planner in Section 3.1 computes a static obstaclefree path S . It does not delve into the motion constraints of the MMRs, dynamic obstacle avoidance, and the collision among the MMRs but provide the global references. We propose an online motion planner as a constrained nonlinear optimization problem incorporating kinodynamic constraints. It uses the smoothed global reference trajectory $p _ { r } ( c _ { t } )$ as an initial guess to eliminate the local stuck. The online motion planning optimization is given as

$$
\mathcal {X} _ {*} ^ {0: N _ {h}}, \mathbf {u} ^ {0: N _ {h}} = \arg \min \sum_ {k = 0} ^ {N _ {h} - 1} J (\mathcal {X} ^ {k}, u ^ {k}) + J _ {N _ {h}}\tag{4a}
$$

$$
\mathrm{s.t.} \quad q ^ {k + 1} = f (q ^ {k}, u ^ {k})\tag{4b}
$$

$$
\mathcal {B} (\mathcal {X}) \subset \mathcal {W} _ {f r e e}\tag{4c}
$$

$$
\mathcal {B} (\mathcal {X}) \cap \mathcal {O} _ {d y n} = \emptyset\tag{4d}
$$

$$
H _ {i} \mathrm{v} _ {<   x, y >} \leq h _ {i},\tag{4e}
$$

$$
H _ {(i + 1) \% n} \mathrm{V} _ {<   x, y >} \geq h _ {(i + 1) \% n},\tag{4f}
$$

$$
0 \leq \mathrm{v} _ {z} \leq Z _ {h}, \forall \mathrm{v} \in \mathcal {V} _ {i} (q _ {i}), \forall i \in [ 1, n ]\tag{4g}
$$

$$
q _ {a, i} ^ {k} \in \mathcal {Q} _ {i}, u _ {i} ^ {k} \in \mathcal {U} _ {i}, \forall i \in [ 1, n ]\tag{4h}
$$

$$
g _ {i} (\mathcal {X}) = 0, \forall i \in [ 1, n ]\tag{4i}
$$

$$
\mathcal {X} ^ {0} = \mathcal {X} (0)\tag{4j}
$$

where the superscript k refers to the discrete time step. Section 3.2.1 illustrates the cost function in Eqn. (4a). Eqn. (4b) represents the state transition function (Eqn. (1)) of the system. Eqn. (4c) and (4d) account for the static and dynamic obstacles avoidance constraints detailed in Section 3.2.2 and Section 3.2.3. The self collision avoidance described in Section 3.2.4 is ensured by the constraints in the Eqn. (4e)-(4g). The set of admissible states and control inputs are defined in Eqn. (4h) and elaborated in Eqn. 2. The grasp constraints described in Section 3.2.5) are maintained by Eqn. (4i). Eqn. (4j) defines the initial state of the formation in a planning horizon $N _ { h }$

The online motion planner computes the optimal motion plan for the MMRs by solving the optimization problem in Eqn. 4 in receding horizons for $N _ { h }$ horizon segment with time $T _ { h }$ to reduce the computational burden. The horizon length should be long enough to capture the sharp turning behavior. The MMRs execute the computed motion plan of a horizon for an execution time $T _ { e } ( T _ { e } < \bar { T _ { h } } )$ ). We choose the execution time $T _ { e }$ so that the <sup><</sup>computation time for a horizon is guaranteed to be less than $T _ { e } ,$ and the MMRs can start the next plan once it finishes executing the current plan. In case of failure to get a motion plan the MMRs would stop motion and the planner would try to re-plan from the stopping position.

## 3.2.1 Cost Function

The cost function of the optimization in Eqn. (4) described in Eqn. (5) minimizes the control inputs and the tracking error with respect to the initial guess trajectory. The diagonal weightage matrix $\mathbf { W _ { u } }$ for control efort minimization is provided with higher value than the weight-age matrix ${ \bf W _ { e } }$ to the tracking error $e ^ { k }$ of the object CoM. The higher weight-age to control inputs prioritize input minimization. The lower weight values to the tracking error provides global guidance to the trajectory with flexibility to deform for dynamic obstacle avoidance and kinodynamic motion compliance.

$$
J (\mathcal {X} _ {k}, u _ {k}) = u ^ {k T} \mathbf {W _ {u}} u ^ {k} + e ^ {k T} \mathbf {W _ {e}} e ^ {k}\tag{5}
$$

We discretize the reference path $p _ { r } ( c _ { t } )$ into Λ path segment. The expected and reference position for the CoM of the object is denoted as $p ^ { k }$ and $p _ { r } ^ { \lambda + k } = [ x , y ] _ { r } ^ { \lambda + k }$ for the future time step k and <sup>,</sup>is the index of the nearest reference path segment to $\bar { p ^ { 0 } }$ . The discretized path should hold the relation $\begin{array} { r } { \sum _ { k = 0 } ^ { N _ { h } - 1 } \vert \vert p _ { r } ^ { \lambda + k + 1 } - \dot { p } _ { r } ^ { \lambda + k } \vert \vert \leq } \end{array}$ $\nu _ { o p } T _ { h } ,$ , where $\nu _ { o p }$ is the operational velocity of the formation. The tracking error vector $e ^ { k }$ is defined as

$$
e ^ {k} = p ^ {k} - p _ {r} ^ {\lambda + k}\tag{6}
$$

The terminal cost $J _ { N _ { h } }$ is defined in Eqn. (7) similar to the tracking error with a higher weighting ${ \bf W } _ { n _ { h } }$

$$
J _ {N _ {h}} = e ^ {N _ {h} T} \mathbf {W} _ {\mathbf {N _ {h}}} e ^ {N _ {h}}\tag{7}
$$

## 3.2.2 Static Obstacles Avoidance

The formation F must remain within $W _ { f r e e } \left( { \mathcal { B } } ( X ) \subset { \mathcal { W } } _ { f r e e } \right)$ to avoid collision with static obstacles. $W _ { f r e e }$ is represented by a set of convex polygons $\mathcal { P } _ { S }$ computed by the ofline path planner in Section 3.1.2. The inequality representation of the polygon $\mathbf { P } \in \mathcal { P }$ is in Eqn. (8).

$$
\mathbf {P} = \left\{\mathrm{x} \in \mathbb {R} ^ {2}: \mathbf {A x} \leq \boldsymbol {b}, \mathbf {A} \in \mathbb {R} ^ {n _ {f} \times 2}, \boldsymbol {b} \in \mathbb {R} ^ {n _ {f}} \right\}\tag{8}
$$

where $n _ { f }$ is the number of the sides of P and x is an interior point of P. The set of vertices of the bounding polygons of the object and the n MMRs are represented by $\mathcal { V } ( \bar { \boldsymbol { X } } )$ . The projection of ${ \mathcal { V } } ( X )$ at the ground plane $( z = 0 )$ must remain within any polygon $\boldsymbol { \mathrm { P } } \in \mathcal { P } _ { S }$ . The constraints are represented as follows

$$
\mathbf {A} \mathrm{v} _ {<   x, y >} \leq \boldsymbol {b} - d _ {\text { safe }}, \forall \mathrm{v} \in \mathcal {V} (\mathcal {X}), \mathrm{P}: (\mathbf {A}, \boldsymbol {b})\tag{9}
$$

where $\mathbf { V } _ { < x , y > }$ is the $x - y$ projection of the vertex $\mathbf { v } \in \mathcal { V } ( \boldsymbol { X } )$ <sup>< , ></sup>defined in {w}. $d _ { s a f e }$ is the safety distance. The number of constraints in Eqn. (9) increases the computational complexity significantly. The problem can be simplified further by considering the bounding circles of the projected vertices of the

MMR base, manipulators, and the object. This collision geometry reduces the number of constraints and the computational complexity. We have implemented circumscribing bounding circles for each MMR base, manipulator, and object in the ground plane. The center of the circles for the i-th MMR base, manipulator, and the object in the ground are located at $p _ { b a s e , i } , p _ { a r m , i }$ and $p _ { o b j , i }$ with radius $r _ { b a s e , i } , r _ { a r m , i }$ and $r _ { o b j , i }$ <sup>, , ,</sup>. The cyan, purple, <sup>, , , , ,</sup>and gray area in Fig. 6 shows the circumscribing circles for the $i - t h$ MMR base, manipulator, and object. The reduced static collision avoidance constraints are in the Eqn. (10)

$$
\begin{array}{c} \mathbf {A} p _ {m, i} ^ {k} \leq \boldsymbol {b} - d _ {s a f e} - r _ {m, i}, \mathrm{P}: (\mathbf {A}, \boldsymbol {b}) \\ \forall m \in \{b a s e, o b j, a r m \}, \forall i \in [ 1, n ], \forall k \in [ 1, N _ {h} ] \end{array}\tag{10}
$$

where $d _ { s a f e } \in$ <sup>R</sup> is the safety distance.

## 3.2.3 Dynamic Obstacle Avoidance

The formation $\mathcal { F }$ must not collide with any of the dynamic obstacles $O _ { d y n }$ . The space occupied by the formation $\dot { \mathcal { B } ( X ) }$ should not overlap with the dynamic obstacles i.e. $\mathcal { B } ( \boldsymbol { \chi } ) \cap O _ { d y n } = \boldsymbol { \emptyset }$ We implement the dynamic obstacle avoidance by introducing a nonlinear constraint between the collision geometries of the formations and the dynamic obstacles. The collision geometry of the dynamic obstacles are considered as circles with radius $r _ { d y n , d } , \forall d \in [ 1 , n _ { d y n } ]$ located at $p _ { d y n , d } ^ { k } , \forall k \in [ 1 , N _ { h } ]$ in the ground plane, where $d \in [ 1 , n _ { d y n } ]$ <sup>,</sup>represents the $n _ { d y n }$ number dynamic obstacles’ $( O _ { d y n } )$ <sup>,</sup> index and represents the number of dynamic obstacle present at the beginning of planning horizon. The position $p _ { d y n , d } ^ { k } ~ = ~ p _ { d y n , d } + \nu _ { d y n , d } k T _ { c }$ ∀d $\forall k \in [ 1 , N _ { h } ]$ is <sup>,</sup>predicted with the position $p _ { d y n , d }$ and velocity $\nu _ { d y n , d }$ measured <sup>, ,</sup>at the beginning of each planning horizon using camera, Li-DAR based perception system or a motion capture system. Any other dynamic obstacle state estimation model would work with the proposed motion planning algorithm. The accuracy of the estimation model impacts the collision avoidance behavior.

The same collision geometry defined for the static obstacle avoidance in Section 3.2.2 for the base, manipulator of the MMRs, and the object are utilized here. The constraints in Eqn. (11) ensure that the obstacle does not intersect with the formation.

$$
\begin{array}{c} \| p _ {d y n, d} ^ {k} - p _ {m} ^ {k} \| \geq r _ {d y n, d} + r _ {m} + d _ {s a f e, d y n} \\ \forall m \in \{b a s e, o b j, a r m \}, \forall d \in [ 1, n _ {d y n} ], \forall k \in [ 1, N _ {h} ] \end{array}\tag{11}
$$

## 3.2.4 Self Collision Avoidance

For collision avoidance with the object and the other MMRs, the i-th MMR needs to be within the convex wedge shown in Fig. 6 defined by two infinite vertical planes $\mathcal { H } _ { i }$ and $\mathcal { H } _ { ( i + 1 ) \% n }$ as shown in Fig. 6. The convex wedge specifies the workspace for the i-th MMR free from movements of the neighboring MMRs. The planes $\mathcal { H } _ { i }$ and $\mathcal { H } _ { ( i + 1 ) } \ L _ { \% n } \mathrm { i s }$ define considering the workspace of MMRs. Here, we have equally divided the space around the periphery of the object, starting at the CoM of the object for each MMR, as the grasping point is equispaced. The vertical plane $\mathcal { H } _ { i }$ is defined as follows.

$$
\mathcal {H} _ {i} = \{\mathrm{x} \in \mathbb {R} ^ {2}: H _ {i} \mathrm{x} \leq h _ {i}, H _ {i} \in \mathbb {R} ^ {1 \times 2} \}, 0 \leq z \leq + \infty\tag{12}
$$

![](Patra2025Motion_figs/e2de1634f85f0cdd2858e45e906003513ca1384073bdbe8608e6b0b7203972a6.jpg)  
Figure 6: The infinite convex wedge for $i - t h$ MMR is defined by the half plane H , $\mathcal { H } _ { ( i + 1 ) \% n } , z = 0$ and $z = \infty$ . The enclosing <sup>,</sup>circles for MMRs’ mobile base and manipulator are blue and violet, respectively, and the object is gray.

The self-collision avoidance for the $i ^ { t h }$ MMR is defined in the following

$$
H _ {i} \mathrm{v} _ {<   x, y >} \leq h _ {i}, H _ {(i + 1) \% n} \mathrm{v} _ {<   x, y >} \geq h _ {(i + 1) \% n}, \forall \mathrm{v} \in \mathcal {V} _ {i} (q _ {i})\tag{13}
$$

where $\mathscr { V } _ { i } ( q _ { i } )$ is the set of vertices of the i-th MMR.

## 3.2.5 Grasp Constraints

The MMRs grasp the object at its periphery at equal spacing from each other to have equal workspace among them and for optimal wrench interaction with the object. There should be no relative movement between the EE and the grasped object throughout the task to ensure stable formation as the object is rigid. The grasp constraint for i-th MMR is

$$
p _ {e e, i} = p + \mathbf {\Phi} _ {o} ^ {w} \mathrm{R} (\psi) ^ {o} r _ {i}, \phi_ {e e, i} = \psi\tag{14}
$$

where $p _ { e e , i }$ is i-th MMR’s EE position, <sup>w</sup>R is the rotation matrix <sup>,</sup>between o and w. We represent Eqn. (14) by $g _ { i } ( X ) = 0$

## <sub>4 O</sub>bject <sub>T</sub>ransportation

We validate the proposed motion planning algorithm in simulation and hardware experiments with the nonholonomic MMRs that accept velocity as a control input. The system dynamics for the MMRs are approximated using the fourth-order Runge-Kutta method as mentioned in Eqn. (1). The NMPC problem of the local motion planning is solved using the CasADi package [28] with an Interior point optimization (Ipopt) method.

## 4.1 Simulation

The MMRs with a diferential drive mobile base have the same forwarding and reversing capabilities. The Denavit-Hartenberg (DH) parameters are mentioned in Table 1.

Table 1: DH Parameters Value for the manipulators

<table><tr><td>Joint</td><td>d (m)</td><td>a (m)</td><td>α (rad)</td><td>θ (rad)</td></tr><tr><td>Joint 1</td><td>0.070</td><td>0</td><td>0</td><td> $q_{a,1}$ </td></tr><tr><td>Joint 2</td><td>0</td><td>0</td><td>0.5 π</td><td> $q_{a,2}$ </td></tr><tr><td>Joint 3</td><td>0.100</td><td>0</td><td>-π</td><td> $q_{a,3}$ </td></tr><tr><td>Joint 4</td><td>0.125</td><td>0</td><td>π</td><td> $q_{a,4}$ </td></tr><tr><td>Joint 5</td><td>0</td><td>0.120</td><td>-0.5 π</td><td> $q_{a,5}$ </td></tr><tr><td>Gripper</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

We select the operational velocity of the formation $\nu _ { o p } =$ 0 15 $m / s$ and use prediction horizon time $T _ { h } = 9 ~ s ,$ trajectory <sup>. /</sup>execution time $T _ { e } = 3 ~ s$ and the discretization time step $T _ { c } =$ 0 25 s. The safety margins $d _ { s a f e } = 0 . 0 5$ m and $d _ { s a f e , d y n } = 0 . 1$ m <sup>. . , .</sup>for static and dynamic obstacle avoidance to keep the formation safe during object transportation. A higher margin restricts the formation from nearing the obstacles and hence reduces the obstacle-free space. The tuned optimization weights are $\mathbf { W _ { u } } ~ = ~ d i a g ( r e p e a t ( [ 0 . 0 5 $ 0 25 2 5 2 5 2 5 5 2 5] 5)), ${ \bf W _ { e } } = { \bf \Psi }$ $d i a g ( [ 0 . 0 1 , 0 . 0 1 ] )$ <sup>.</sup>and $\mathbf { W _ { N _ { h } } } = 1 0 ^ { 5 }$ <sup>, . , . , , . ,</sup>. We assign a lower weight <sup>. , .</sup>to the base, prioritize the use of the mobile base motion over the arm, and avoid joint limits when reaching for the arm. The base angular motion is assigned a relatively higher weight than linear to reduce rotation and hence improve ground trajectory smoothness. One of the manipulator joints is assigned a higher weight to reduce the more frequent motion in the ±z direction. The lower weight to the global reference tracking error ensures flexibility for a smooth trajectory with better dynamic obstacle avoidance behavior.

The five MMRs (the mobile base in deep green rectangle and manipulator’s arm in red line) start transporting (Fig. 7a) the object while grasping at its periphery through a narrow corridor of 1 9m in an environment of size 10m × 10m . While the MMRs <sup>.</sup>come out of the corridor, it encounters dynamic obstacles in Fig. 7b, while taking a sharp left turn. The generated motion plan successfully navigates the formation, avoiding dynamic obstacles, and turns toward (Fig. 7c) the goal. The MMRs successfully transport the object through the narrow doors and complete the task without any collision (Fig. 7d). Fig. 7e plots the shortest distance $d _ { m a r g i n }$ from the formation to any static and dynamic obstacles. The $d _ { m a r g i n }$ in Fig 7e for the static and the dynamic obstacles being always positive indicates successful collision avoidance behavior.

## 4.2 Hardware Experiments

We perform experiments with our in-house developed ROSenabled MMRs to evaluate the motion planning algorithm in Section 3.2 in an environment (4 m × 4 m) with static and dynamic obstacles. We have defined a specific path for the dynamic obstacles (turtle bot). However, the path of the obstacle is not known to the mobile manipulators. The nonholonomic MMR bases are made of two disc wheels each separately driven by geared motor with an encoder. Fig. 8 shows two MMRs both grasped an object to transport it in an indoor environment shown in Fig. 9a.

The manipulator of the MMRs shown in Fig. 8 is same as the manipulator used for the simulation, described in Table 1, except for the joint 5. We have removed and fixed the joint 5 because of the joint 2 torque limitations. The adjusted DH parameters of the gripper are $d = 0 . 1 2 0 m , a = 0 , \alpha = 0 .$ and $\theta = 0$ . The <sup>. , ,</sup> <sup>α θ</sup>planned trajectory and the control input for the MMRs by the online motion planner (Section 3.2) are sent to the respective MMRs. The trajectory tracking controllers for the mobile base and manipulator uses online motion planner’s computed control input as feed forward and PID feedback controller to ensure desired trajectory tracking. It uses external motion capture system data and joints encoder data for the mobile base and manipulator feedback.

![](Patra2025Motion_figs/ccefcdc145f1f29194d28981222f7a292ae0a58764e2c1bc1942b86132a1314d.jpg)

![](Patra2025Motion_figs/706ace8e2f6e090594845198d697575acb7441f788ae7fce29f791a54c355b73.jpg)  
(b) $t = 3 2 . 5 s$

(a) $t = 0 ~ s$  
![](Patra2025Motion_figs/35855981616857bb37ee41e3483f22706d06f45526d1e0a1abb04b2dc2d8a5d9.jpg)

![](Patra2025Motion_figs/d222094dc684eb00349fdf54fcb9777459cb720cc0c921a2bcf7dbb3a4843f08.jpg)

(c) $t = 4 0 . 5 ~ s$ 4  
(d) $t = 7 9 ~ s$  
![](Patra2025Motion_figs/69a750563e56ad1c7e1bb38fe53997b8c4250fda7226bba6767c76df0e339394.jpg)  
(e) Safety margins.  
Figure 7: The snapshots of object transportation from a start (Fig. 7a) to a goal (Fig. 7d) by five MMRs in 10m × 10m environment. The red circle indicates dynamic obstacle is in its current state. The horizontal lines in Fig. 7e plots static and dynamic safety threshold $d _ { s a f e } = 0 . 0 5$ m and $d _ { s a f e , d y n } = 0 . 1 m$

![](Patra2025Motion_figs/efbfbbdcbe702f6d3a1f129e2df65af04329019a24ae975544c90b00fd06173c.jpg)  
Figure 8: Experimental Setup of two in-house developed nonholonomic MMRs.

![](Patra2025Motion_figs/1b76efa2682b753fb71db0dbb231bb8467d4c93b6705c882ca936110340174f3.jpg)

![](Patra2025Motion_figs/719e3d5e786ce1b2beec96ad92983dee80ad3d7070938f5ca2e886b0121ddf33.jpg)

(a) t = 0 s  
![](Patra2025Motion_figs/ac309e8dff5b32b20910e7f9698fb4c3556f26b9541ac30f0d8fbc753f06eae2.jpg)  
(c) $t = 2 0 ~ s$

(b) t = 15 10 s  
![](Patra2025Motion_figs/41d1ad82831a73955c1e1352407004363cdf97e9c5aecb9e2884c3c81b02b918.jpg)  
(d) $t = 4 7 ~ s$  
Figure 9: Two MMRs transport the rectangular object. The MMRs encounter a dynamic obstacle and started avoidance maneuver (Fig. 9b). It successfully avoids the dynamic obstacle 9c) and reaches the goal point 9d)

Fig. 9 shows the snap of the object transport from the start (Fig. 9a) to the goal (Fig. 9d). It encounters a dynamic obstacle and start avoidance maneuver. Fig. 9b shows when the formation approaches the dynamic obstacle and finally avoids (Fig. 9c) the obstacle to reach the goal (Fig. 9d).

![](Patra2025Motion_figs/c1b06ee972554d37b7a8f6c0fc9976883936b11a4435a0541130220272bd8475.jpg)

![](Patra2025Motion_figs/b821ffcfe8696e782b78b0c3e5efbf01ee581e9b2439372690748bddbaf3dd52.jpg)

![](Patra2025Motion_figs/f43f8e9812984926189273001e784d1aeb066ad156332cd721e0188e8fadac6d.jpg)

![](Patra2025Motion_figs/6c59aa8255708b0091c6cf3b0e1dac98f08397a868852c46f7e102e8ef9fda68.jpg)  
Figure 10: Trajectory of the CoM of the object. The subscript d and m of the legend represents the planned and actual values.

Fig. 10 shows the planned and the actual trajectory of the CoM of the transported object. The position error remains within

![](Patra2025Motion_figs/97eb9c4bdb52c07ba1ecbbbeae0c53d529ef7b3bd242430ba68a3aedf3d35a50.jpg)  
Figure 11: The distance between the two EE during the object transportation.

0 05 m, and the orientation error remains within 0 15 rad. The z <sup>.</sup>height increases near $t = 1 0$ <sup>.</sup>s and t = 28 s before taking sharp turn to reduce the inter robot distance and turning radius. The error in fixed distance between the $\mathrm { E E s } ^ { \prime }$ grasping point in Fig. 11 shows that the coordination between the MMRs has been maintained.

## 4.3 Comparison

We present a comparison of performances of our proposed path planning algorithm for the environment shown in Fig. 5e and motion planning algorithms for a simplified environment where all the three algorithm (proposed, [14, 25]) works. We have run all the algorithms in Python on a Laptop equipped with an AMD Ryzen 5800H CPU and 16 GB RAM. The comparison results are presented as follows.

Path Planner: We compare our proposed path planning algorithm with the IRIS-based algorithms $[ 1 4 , \bar { 2 } 5 ]$ and a RRT Connect like technique [29] (computes only path) for the environ ment shown in Fig. 5e. Table 2 shows the comparison of path length and the computation time for ten runs of each algorithm.

Table 2: Path Planner Comparison.

<table><tr><td></td><td>Path Lengthmean ± sd (m)</td><td>Computation Timemean ± sd (s)</td></tr><tr><td>Proposed</td><td>9.22 ± 0</td><td>0.09 ± 0.03</td></tr><tr><td>Keshab et al.[25]</td><td>9.87 ± 0</td><td>3.74 ± 1.60</td></tr><tr><td>Alonso-Mora et al.[14]</td><td>12.09 ± 3.88</td><td>8.36 ± 6.28</td></tr><tr><td>Zhang et al.[29]</td><td>12.61 ± 4.20</td><td>35.01 ± 14.02</td></tr></table>

The convex optimization-based path planning approaches in [27, 14] rely on randomly generated seed points to compute the path and its corresponding obstacle-free convex region. Such random seeding coupled with convex optimization incurs high computational cost. The targeted seeding strategy proposed in [25] shows improved performance relative to fully samplingbased techniques [14, 29]. Our method deterministically generates the shortest feasible path and analytically computes the associated obstacle-free convex region thereby reduces the computational time.

Motion Planner: We compare the computational time and control efort of our proposed online motion planning technique with the holonomic MMRs’ planning algorithm proposed by Keshab et al. [25] and Alonso-Mora et al. [14]. All algorithms plan the motion of two MMRs in a dynamic environment with a dynamic obstacle with environment details mentioned in Section 3.1 of the attached file. We compare our nonholonomic planning framework against holonomic baseline, as to the best of our knowledge there exist no other nonholonomic multi-robot collaborative motion planners that address dynamic obstacle avoidance. The MMRs are the same except for the base motion constraints: nonholonomic and holonomic. Computational time is measured for each local planning horizon. The control efort is computed for a complete trajectory. As shown in the Table 3, the computation time and the control eforts of our method are lower than the algorithm in [14] and slightly higher than the algorithm proposed in [25]. The nonholonomic constraint for the mobile base reduces the solution space compared to its holonomic counterpart, resulting in increased computation time and control eforts. The proposed method achieves real-time operation in Python and we anticipate substantially faster runtime with C++ implementation.

Table 3: Motion Planner Comparison.

<table><tr><td></td><td colspan="3">Computation Time (s)</td></tr><tr><td></td><td>min</td><td>mean ± sd</td><td>max</td></tr><tr><td>Proposed</td><td>0.199</td><td>0.580 ± 0.231</td><td>1.855</td></tr><tr><td>Keshab et al.[25]</td><td>0.227</td><td>0.272 ± 0.035</td><td>0.346</td></tr><tr><td>Alonso-Mora et al.[14]</td><td>0.46</td><td>0.857 ± 0.256</td><td>1.26</td></tr><tr><td></td><td colspan="3">Control Effort</td></tr><tr><td></td><td> $\sum ||\boldsymbol{u}||_2$ </td><td colspan="2"> $||\boldsymbol{u}||_2$  mean ± sd</td></tr><tr><td>Proposed</td><td>64.869</td><td colspan="2">0.676 ± 0.468</td></tr><tr><td>Keshab et al.[25]</td><td>36.136</td><td colspan="2">0.435 ± 0.183</td></tr><tr><td>Alonso-Mora et al.[14]</td><td>78.754</td><td colspan="2">0.984 ± 0.759</td></tr></table>

## <sub>5 C</sub>onclusion

The optimization-free ellipse based polygon computation algorithm is a trade-of, where the polygon suboptimality significantly reduces the computational time. This trade-of does not afect the subsequent NMPC-based planning stage, as the ellipses are aligned with the piece-wise reference path segments and adaptively inflated to ensure adequate obstacle free space for kinodynamic constrained motion and dynamic obstacle avoidance. The proposed path planning technique computes both the path and its associated convex region within 120 ms indicating that the path can be recomputed online during the task execution.

The simulation and experimental results demonstrate that the motion planner generates kinodynamically feasible, collisionfree trajectories in dynamic environments in real time, indicating the strong potential for deployment in factory and warehouse like settings. Motion planning for cooperative MMRs during object transportation remains particularly challenging, especially for nonholonomic MMRs due to the kinodynamic constraints and the rigid object-manipulator coupling that must be respected during task executions.

Our simulations and hardware experiments indicate that the trajectory may exhibits non-smooth transitions at the intersection of the obstacle-free convex polygon. However, this did not adversely afect the experiments as planner ensures the controls constraints and the low-level tracking controller efectively managed traction loss in the mobile base. In the future, we will address the trajectory smoothness at the transitions.

## <sub>R</sub>eferences

[1] O. Khatib, K. Yokoi, K. Chang, D. Ruspini, R. Holmberg, and A. Casal, “Coordination and decentralized cooperation of multiple mobile manipulators,” Journal of Robotic Systems, vol. 13, no. 11, pp. 755–764, 1996.

[2] P. Xu, J. Zhang, Y. Cui, K. Zhang, and Q. Tang, “Modeling and coordinated control of multiple mobile manipulators with closed-chain constraints,” International Journal of Control, Automation and Systems, vol. 21, pp. 1296–1308, 4 2023.

[3] X. Zhao, Y. Zhang, W. Ding, B. Tao, and H. Ding, “A dualarm robot cooperation framework based on a nonlinear model predictive cooperative control,” IEEE/ASME Transactions on Mechatronics, vol. 29, no. 5, pp. 3993–4005, 2024.

[4] S. Erhart and S. Hirche, “Adaptive force/velocity control for multi-robot cooperative manipulation under uncertain kinematic parameters,” in 2013 IEEE/RSJ International Conference on Intelligent Robots and Systems, 2013, pp. 307–314.

[5] P. Culbertson and M. Schwager, “Decentralized adaptive control for collaborative manipulation,” in 2018 IEEE International Conference on Robotics and Automation (ICRA), 2018, pp. 278–285.

[6] C. K. Verginis, A. Nikou, and D. V. Dimarogonas, “Communication-based decentralized cooperative object transportation using nonlinear model predictive control,” in 2018 European Control Conference (ECC), 2018, pp. 733–738.

[7] G.-B. Dai and Y.-C. Liu, “Distributed coordination and cooperation control for networked mobile manipulators,” IEEE Transactions on Industrial Electronics, vol. 64, no. 6, pp. 5065–5074, 2017.

[8] A. Marino, “Distributed adaptive control of networked cooperative mobile manipulators,” IEEE Transactions on Control Systems Technology, vol. 26, no. 5, pp. 1646–1660, 2018.

[9] Y. Ren, S. Sosnowski, and S. Hirche, “Fully distributed cooperation for networked uncertain mobile manipulators,” IEEE Transactions on Robotics, vol. 36, no. 4, pp. 984– 1003, 2020.

[10] K. Patra, A. Sinha, and A. Guha, “Online capability based task allocation of cooperative manipulators,” Journal of Intelligent & Robotic Systems, vol. 110, p. 23, 3 2024.

[11] J. Du, Y. Liang, H. Tao, Y. Xu, L. Zhu, and H. Ding, “Load sharing in distributed collaborative manipulation,” IEEE Robotics and Automation Letters, vol. 10, no. 4, pp. 3390–3397, 2025.

[12] J. Desai and V. Kumar, “Nonholonomic motion planning for multiple mobile manipulators,” in Proceedings of International Conference on Robotics and Automation, vol. 4, 1997, pp. 3409–3414 vol.4.

[13] H. Tanner, S. Loizou, and K. Kyriakopoulos, “Nonholonomic navigation and control of cooperating mobile manipulators,” IEEE Transactions on Robotics and Automation, vol. 19, no. 1, pp. 53–64, 2003.

[14] J. Alonso-Mora, S. Baker, and D. Rus, “Multi-robot formation control and object transport in dynamic environments via constrained optimization,” The International Journal of Robotics Research, vol. 36, no. 9, pp. 1000–1021, 2017.

[15] Z. Cao, N. Gu, J. Jiao, S. Nahavandi, C. Zhou, and M. Tan, “A novel geometric transportation approach for multiple mobile manipulators in unknown environments,” IEEE Systems Journal, vol. 12, no. 2, pp. 1447–1455, 2018.

[16] J. Jiao, Z. Cao, N. Gu, S. Nahavandi, Y. Yang, and M. Tan, “Transportation by multiple mobile manipulators in unknown environments with obstacles,” IEEE Systems Journal, vol. 11, no. 4, pp. 2894–2904, 2017.

[17] R. Tallamraju, D. H. Salunkhe, S. Rajappa, A. Ahmad, K. Karlapalem, and S. V. Shah, “Motion planning for multimobile-manipulator payload transport systems,” in 2019 IEEE 15th International Conference on Automation Science and Engineering (CASE), 2019, pp. 1469–1474.

[18] A. Nikou, C. Verginis, S. Heshmati-alamdari, and D. V. Dimarogonas, “A nonlinear model predictive control scheme for cooperative manipulation with singularity and collision avoidance,” in 2017 25th Mediterranean Conference on Control and Automation (MED), 2017, pp. 707–712.

[19] F. Kennel-Maushart and S. Coros, “Payload-aware trajectory optimisation for non-holonomic mobile multi-robot manipulation with tip-over avoidance,” IEEE Robotics and Automation Letters, vol. 9, no. 9, pp. 7669–7676, 2024.

[20] O. Shorinwa and M. Schwager, “Scalable collaborative manipulation with distributed trajectory planning,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020, pp. 9108–9115.

[21] C. Wu, H. Fang, Q. Yang, X. Zeng, Y. Wei, and J. Chen, “Distributed cooperative control of redundant mobile manipulators with safety constraints,” IEEE Transactions on Cybernetics, pp. 1–13, 2021.

[22] J. Hu, W. Liu, H. Zhang, J. Yi, and Z. Xiong, “Multi-robot object transport motion planning with a deformable sheet,” IEEE Robotics and Automation Letters, vol. 7, no. 4, pp. 9350–9357, 2022.

[23] L. Pei, J. Lin, Z. Han, L. Quan, Y. Cao, C. Xu, and F. Gao, “Collaborative planning for catching and transporting objects in unstructured environments,” IEEE Robotics and Automation Letters, vol. 9, no. 2, pp. 1098–1105, 2024.

[24] R. Mao, H. Gao, and L. Guo, “A novel collision-free navigation approach for multiple nonholonomic robots based on orca and linear mpc,” Mathematical Problems in Engineering, vol. 2020, pp. 1–16, 6 2020.

[25] K. Patra, A. Sinha, and A. Guha, “Kinodynamic motion planning for collaborative object transportation by multiple mobile manipulators,” Journal of Mechanisms and Robotics, vol. 17, no. 12, p. 121003, 09 2025.

[26] H. Choset, K. Lynch, S. Hutchinson, G. Kantor, and W. Burgard, Principles of Robot Motion: Theory, Algorithms, and Implementations, ser. Intelligent Robotics and Autonomous Agents series. MIT Press, 2005.

[27] R. Deits and R. Tedrake, “Computing large convex regions of obstacle-free space through semidefinite programming,” in WAFR, 2014.

[28] J. A. E. Andersson, J. Gillis, G. Horn, J. B. Rawlings, and M. Diehl, “CasADi – A software framework for nonlinear optimization and optimal control,” Mathematical Programming Computation, vol. 11, no. 1, pp. 1–36, 2019.

[29] H. Zhang, H. Song, W. Liu, X. Sheng, Z. Xiong, and X. Zhu, “Hierarchical motion planning framework for cooperative transportation of multiple mobile manipulators,” 2022. [Online]. Available: https://arxiv.org/abs/2208.08054

## <sub>A</sub>ppendix <sub>I:</sub> <sub>A</sub>dditional <sub>D</sub>etails of <sub>A</sub>lgorithm

We present some additional implementation details of our proposed Algorithms in Section 5, List of Symbols in Section 5. The analytical ellipse computation technique is described in detail in Section 5, and the dilation of the ellipse is described in Section 5. We add a tabulated list for symbols used in the manuscript in Section 5.

Algorithm 1 illustrated convexify simple concave polygon. Here we explain the FindEllipse function in details in Algorithm 2 and DilateEllipse in Algorithm 3.

Ellipse Computation

![](Patra2025Motion_figs/c4f03e77f2b0f762f97d7e90b60845bec75678400795be07cc6fafc2f3976c77.jpg)  
Figure 12: Ellipse fitting at the center d of the path segment $S _ { 2 }$ .

This section describe the ellipse computation method with mathematical details, used in the Polygon Convexification Algorithm 1. We find the Rotation matrix R putting a local frame origin at the center (d) of the ellipse and x-axis along the path segment $S _ { 2 }$ as shown in Fig. 12. The ellipse computation method has been described in Algorithm 2.

Once we have $x ^ { * } ,$ , the nearest concave vertex to $d ,$ the distance of $x ^ { * }$ from the origin d of the ellipse should be less than the semimajor axis a, otherwise one cannot fit the ellipse with $R , a , \mathrm { d } , x _ { i } ^ { * } .$ <sup>, , ,</sup>We check the degeneracy in lines 1-2 and modify a if required. Then we compute the semi-minor axis b using the fundamental ellipse equation for Cartesian coordinates.

## Ellipse Dilation

We describe the ellipse dilation method in Algorithm 3. We dilate the base ellipse computed in the first step of the polygon convexification technique to eliminate the remaining concave vertices. The dilation step length is computed analytically based on the nearest concave vertices of the base ellipse and is described in the Algorithm 3 step-wise.

```txt
Algorithm 2 FindEllipse(R, a, d, x*)  
Input: Rotation Matrix R, Semi-major axis a  
Center of Ellipse d, The nearest concave point x*  
Output: Ellipse κ(C, d)  
1: dist_x* = Euclidean Distance of x* from d  
2: if dist_x* > (a - ε) then ▷ ε = 0.001, when x* is distant eliminates degeneracy  
3: a = max(1.5 * dist_x*, 2 * a) ▷ Modify a with parameter 1.5, 2 so x* can used for ellipse fitting  
4: end if  
5: x*(x, y) = R(x* - d) ▷ Converting to local ellipse frame  
6: b = |x_y^*/√(1 - (x_x^)/a)^2| ▷ Find the minor axis of the ellipse touching x*(x, y) using (x_x^)/a^2 + (x_y^)/b^2 = 1  
7: Λ = diag(a, b)  
8: C = R^T ΛR  
9: return C, d
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 DilateEllipse( $\kappa_{0}(C_{0},d_{0}),R,x_{j}^{*}$ )

Input: Base Ellipse  $\kappa_{0}$ , The nearest concave point  $x_{j}^{*}$ 

Output: Ellipse  $\kappa_{j}$ 

1:  $a,b\leftarrow\kappa_{0}\quad\triangleright$  Extract semi-major and semi-minor axis from  $\kappa_{0}$ 

2:  $x^{*}(x,y)=R(x_{j}^{*}-d)\quad\triangleright$  Converting to local ellipse frame

3:  $angle=\tan^{-1}(\frac{x_{y}^{*}a}{x_{x}^{*}b})\quad\triangleright$  Finding the ellipse angle of vector from d to  $x_{j}^{*}$  with the semi major axis

4:  $\alpha=x_{y}^{*}/(b\cdot\sin(angle))\quad\triangleright$  Computing the scaling  $\alpha$  from projection of  $x_{y}^{*}$  to the minor axis

5:  $C=\alpha\cdot C_{0},d=d_{0}$ 

6:  $\kappa_{j}\leftarrow C,d$ 

7: return  $\kappa_{j}$
</div>

<sub>L</sub>ist of $\mathbf { S } \mathbf { \Psi }$ ymbols

Table 4: Description of Symbols

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td>n</td><td>Number of mobile manipulator robots (MMRs)</td></tr><tr><td>{w}</td><td>The world fixed reference frame</td></tr><tr><td>{o}</td><td>Object coordinate frame attached to the object center of mass</td></tr><tr><td>{bi}</td><td>Body coordinates attached to the center of i-th mobile base</td></tr><tr><td>qm,i</td><td>Pose of the mobile base of i-th MMR</td></tr><tr><td>pi</td><td>Position of the mobile base in  $\mathbb{R}^2$  of i-th MMR</td></tr><tr><td>φi</td><td>Orientation of the mobile base in R of i-th MMR</td></tr><tr><td>ni</td><td>Number of joint of i-th MMR</td></tr><tr><td>qa,i</td><td>Joint displacement of i-th MMR</td></tr><tr><td>qi</td><td>Combined pose (mobile base) and manipulator joint displacement of i-th MMR</td></tr><tr><td>q̇i</td><td>Combined pose (mobile base) and manipulator joint of i-th MMR</td></tr><tr><td>pee,i</td><td>Position of the i-th end effector in  $\mathbb{R}^3$ </td></tr><tr><td>φee,i</td><td>Orientation of the i-th end effector in  $\mathbb{R}^3$ </td></tr><tr><td>vi</td><td>Linear velocity of the mobile base of i-th MMR</td></tr><tr><td>ωi</td><td>Angular velocity of the mobile base of i-th MMR</td></tr><tr><td>q̇a,i</td><td>Joint velocity of the manipulator of the i-th MMR</td></tr><tr><td>ui</td><td>Combined velocity of mobile base and the manipulator arm of i-th MMR</td></tr><tr><td>k</td><td>Discrete time step</td></tr><tr><td>q̄a,i</td><td>i-th manipulator&#x27;s joint position lower limit vector</td></tr><tr><td> $\overline{q}_{a,i}$ </td><td>i-th manipulator&#x27;s joint position upper limit vector</td></tr><tr><td>ūi</td><td>The admissible control lower limits of i-th MMR</td></tr><tr><td> $\overline{u}_{i}$ </td><td>The admissible control upper limits i-th MMR</td></tr><tr><td>Qi</td><td>Admissible displacement of i-th MMR</td></tr><tr><td>Ui</td><td>Admissible control of i-th MMR</td></tr><tr><td>F</td><td>Multi-MMR formation</td></tr><tr><td>o ri</td><td>Grasp pose of i-th EE from the object CoM measured in {o}</td></tr><tr><td>p</td><td>The position of the object CoM in  $\mathbb{R}^3$ </td></tr><tr><td>o</td><td>The orientation of the object CoM in  $\mathbb{R}^3$ </td></tr><tr><td>Q</td><td>The configuration of n MMRs</td></tr><tr><td>X</td><td>The formation configuration</td></tr><tr><td>B(X)</td><td>The space occupied by the formation</td></tr><tr><td>W</td><td>A structured and bounded environment having both static and dynamic obstacles</td></tr><tr><td>O</td><td>The set of static obstacles in W</td></tr><tr><td>Odil</td><td>The set of dilated statics obstacles</td></tr><tr><td>Wfree</td><td>Static obstacle-free region W\ O ∈  $\mathbb{R}^2$ </td></tr><tr><td>Odyn</td><td>The dynamic obstacles in the environment W</td></tr><tr><td>ps</td><td>The start position</td></tr><tr><td>pg</td><td>The goal position</td></tr><tr><td>S</td><td>Linear piece-wise static obstacle-free shortest path</td></tr><tr><td>Si</td><td>Path segment of S</td></tr><tr><td>rf</td><td>The radius of the circle enclosing the formation F</td></tr><tr><td>V</td><td>Nodes of the graph</td></tr><tr><td>E</td><td>Edges of the graph</td></tr><tr><td>W</td><td>Weight of E of the graph</td></tr><tr><td>G(V,E,W)</td><td>Graph</td></tr><tr><td>wi</td><td>Vertices of the path S</td></tr><tr><td>Vs</td><td>Set of visible vertices of the statics obstacles from wi, ∀i</td></tr><tr><td>Pcc,i</td><td>Static obstacle-free simple polygon around Si</td></tr><tr><td>Pcc</td><td>Set of all simple polygon Pcc,i around S</td></tr><tr><td>C</td><td>A 2 × 2 symmetric positive definite matrix to maps a unit radius circle to an ellipse</td></tr><tr><td>R</td><td>Rotation matrix that aligns the ellipse axes to the world reference frame axes</td></tr><tr><td>Λ = diag(a,b)</td><td>A diagonal scale matrix</td></tr><tr><td>a, b</td><td>The length of the ellipse semi-major and minor axes</td></tr><tr><td>d</td><td>Defines the center of the ellipse.</td></tr><tr><td>κ(C,d)</td><td>Ellipse in the ground plane</td></tr></table>

<sub>P</sub>reprint <sub>–</sub> <sub>M</sub>otion <sub>P</sub>lanning of <sub>C</sub>ooperative <sub>N</sub>onholonomic <sub>M</sub>obile <sub>M</sub>anipulators

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $\mathcal{V}_{cc}$ </td><td>Set of concave vertices of a simple polygon</td></tr><tr><td> $x^{*}$ </td><td>Nearest concave vertices to d</td></tr><tr><td>H</td><td>Hyperplane</td></tr><tr><td> $\mathcal{P}_{S}$ </td><td>Set of convex polygon around S</td></tr><tr><td> $p_{r}(c_{t})$ </td><td>Time-normalized smooth trajectory guess</td></tr><tr><td> $c_{t}$ </td><td>Normalized time parameter ∈ [0, 1]</td></tr><tr><td> $N_{h}$ </td><td>Planning horizon segment</td></tr><tr><td> $T_{h}$ </td><td>Planning horizon time</td></tr><tr><td> $T_{e}$ </td><td>Execution time</td></tr><tr><td> $T_{c}$ </td><td>Discretization time-step</td></tr><tr><td> $\mathbf{W}_{\mathbf{u}}$ </td><td>Diagonal weight-age matrix for control effort</td></tr><tr><td> $\mathbf{W}_{\mathbf{e}}$ </td><td>Diagonal weight-age matrix for the trajectory error</td></tr><tr><td> $e^{k}$ </td><td>Tracking error</td></tr><tr><td> $\lambda$ </td><td>The index of the nearest reference path segment</td></tr><tr><td> $J(\mathcal{X}_{k}, u_{k})$ </td><td>The Running cost</td></tr><tr><td> $J_{N_{h}}$ </td><td>The terminal cost</td></tr><tr><td> $v_{op}$ </td><td>Operational velocity of the formation</td></tr><tr><td> $\mathcal{V}(\mathcal{X})$ </td><td>Set of vertices of the bounding polygons of the object and the n MMRs</td></tr><tr><td> $d_{safe}$ </td><td>The safety distance for static obstacle avoidance</td></tr><tr><td> $d_{safe,dyn}$ </td><td>The safety distance for dynamic obstacle avoidance</td></tr></table>