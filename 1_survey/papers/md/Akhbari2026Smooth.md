---
citation_key: Akhbari2026Smooth
arxiv_id: 2602.16758
arxiv_url: "https://arxiv.org/abs/2602.16758"
title: "Smooth trajectory generation and hybrid B-splines-Quaternions based tool path interpolation for a 3T1R parallel kinematic milling robot"
authors_short: "Sina Akhbari et al."
year: 2026
direction_tag: B_trajectory_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:15:05Z
origin: ai+web
reviewed: false
---

# Smooth trajectory generation and hybrid B-splines-Quaternions based tool path interpolation for a 3T1R parallel kinematic milling robot

Sina Akhbari, Mehran Mahboubkhah

Sina Akhbari<sup>1</sup>: Intelligent Automation Centre, Wolfson School of Mechanical, Electrical & Manufacturing Engineering, Loughborough University, Loughborough, UK. email: s.akhbari@lboro.ac.uk, ORCID ID: (https://orcid.org/0000-0002-9063-2882).

Mehran Mahboubkhah: Department of Mechanical Engineering, University of Tabriz, 51666-16471, Tabriz, Iran.

Corresponding Author: Sina Akhbari

## Abstract

This paper presents a smooth trajectory generation method for a four-degree-of-freedom parallel kinematic milling robot. The proposed approach integrates B-spline and Quaternion interpolation techniques to manage decoupled position and orientation data points. The synchronization of orientation and arc-length-parameterized position data is achieved through the fitting of smooth piece-wise Bezier curves, which describe the non-linear relationship between path length and tool orientation, solved via sequential quadratic programming. By leveraging the convex hull properties of Bezier curves, the method ensures spatial and temporal separation constraints for multi-agent trajectory generation. Unit quaternions are employed for orientation interpolation, providing a robust and efficient representation that avoids gimbal lock and facilitates smooth, continuous rotation. Modifier polynomials are used for position interpolation. Temporal trajectories are optimized using minimum jerk, time-optimal piecewise Bezier curves in two stages: task space followed by joint space, implemented on a low-cost microcontroller. Experimental results demonstrate that the proposed method offers enhanced accuracy, reduced velocity fluctuations, and computational efficiency compared to conventional interpolation methods.

## Keywords

Smooth trajectory generation; tool path interpolation; parallel kinematic robots; minimum jerk optimization; B-spline unit quaternions; piece-wise Beziers.

## Introduction

Over the last few decades, much attention has been given to the problems of tool path and trajectory generation of for generating freeform curves. More recently, parallel kinematic robots have emerged as trending topics in fields of additive [1] and subtractive manufacturing [2]. Parallel kinematic machine tools are significantly different from serial counterparts, since their multi degree of freedom are obtained from closed loop kinematic chains. This parallel formation offers superior rigidity, less mass, thus enabling the requirements for high-speed and high-precision machining [3].

Toolpath and trajectory generation are essential components of robotics and CNC machine automation. Toolpath generation must ensure high conformity and geometric smoothness of the defined path, while trajectory generation aims to produce optimal reference inputs for the control system and achieve smooth motion. The performance of planned trajectories is crucial for motion control since it exerts a significant and direct influence on the stability, reliability and productivity of the machinery [4].

In order to obtain a continuous tool path, many researches have been dedicated on implementation of parametric curves for multi axis tool path generation. Fleisig and Spence [5] used fifth-order polynomials for position splines and spherical Bezier splines for orientation, achieving coordinated motion through chord-length reparameterization.. Liu et al. [6] improved this by relating the orientation parameter to the interpolation arc length. In a different format, Langeron et al. [7] employed double Bsplines for tool position and orientation,. While, Yen et al. [8] decoupled position and orientation using fifth-order B-splines and solved a nonlinear optimization problem for parameter scheduling.

The nonlinear relationship between B-spline parameters and arc length necessitates numerical solutions. Various methods have been developed to address this. The proportional interpolation method was first proposed by Bedi and augmented in [5, 9], where the spline parameter is scheduled proportionally to the arc length. However, this straightforward method is only applicable to linear paths with constant speed. Taylor’s series approximation is the most commonly used among the above-mentioned methods [10-13]. However, Taylor Expansion (TE) cannot produce smooth geometry in case of sudden steep curvature changes. To avoid this drawback, others, [14, 15] used predictor-corrector methods, though these are computationally intensive and may not converge. Erkorkmaz and Altintas [16] introduced polynomials to relate B-spline parameters to arc length. This method reduces feed-rate fluctuations and minimizes real-time computation by preprocessing coefficients, making it widely adopted [8, 17-19].

Trajectory generation for robotic machine tools typically involve mathematical formulations optimized for objectives like minimum time or jerk, subject to kinematic and geometric constraints. These problems are often solved using analytical methods (e.g., quadratic programming) or heuristic approaches (e.g., genetic algorithms, particle swarm optimization). The S-shape velocity with trapezoidal acceleration is widely used [20-22] for jerk-limited motion but fails to control sudden jerk changes, which can excite system resonances. Higher order polynomials [23, 24] and trigonometric velocity scheduling [25, 26] have been proposed to address this, though its computational cost of trigonomic equations limits practicality.

Time-optimal velocity profiles, optimized under kinematic and geometric constraints, are another focus. Sencer et al. [27] used cubic B-splines and sequential quadratic programming to simplify constraints, while others, [28, 29] approximated constraints with linear programming, though results were often overly conservative. Subsequently, Erkorkmaz et al. [30] combined linear programming with a windowing scheme to reduce computational load for long toolpaths. In an alternative approach, Gasparetto and Zanotto [31] proposed a hybrid time-jerk optimization method using sequential quadratic programming. Heuristic algorithms, such as genetic algorithms [32] and particle swarm optimization [33], have also been applied for near-optimal trajectory generation. However, their high computational cost and lower accuracy compared to classical methods make them less suitable for lowcost embedded systems, with a higher risk of constraint violations.

While toolpath interpolation and feed-rate scheduling have been extensively studied, their application to parallel kinematic machines (PKMs) with more than three degrees of freedom remains underexplored. This work implements a proposed trajectory generation method on a 3T1R parallel mechanism previously developed by the authors[34, 35]. A decoupled approach is used for toolpath parameterization, with quintic B-splines globally interpolating discrete tool pose data to ensure C³ continuity. Spatial tool orientation is mapped to quaternion space to avoid gimbal lock and interpolated using quintic B-splines, guaranteeing at least third-order continuous rotations. For parameter interpolation, piecewise ninth-order polynomials approximate the position spline parameter as a function of arc length, ensuring C³ continuity and accurate velocity profiles. The nonlinear relationship between quaternion spline parameters and arc length is approximated using seventh-order piecewise Bezier splines, minimizing geometric jerk. Bezier curves are used because of their geometric and numerical superiority to power basis polynomials, and also retaining most of the B-spline properties such as convex hull, without its differential complexity. Convex hull properties of Bezier curves can be used to satisfy spatial and temporal separation constraints for multi-agent trajectory generation.

A dual-stage trajectory generation method is proposed to address the nonlinear kinematic mapping of parallel robots. While dual-stage trajectory generation is underexplored, previous studies by the authors [35] highlight its importance in maintaining trajectory functions of the same order and degree in both workspace and joint space to minimize nonlinearity. Consequently, first, a jerk-time optimal trajectory in the workspace generates coarse interpolation data, which is transformed into joint space vertices. Second, a jerk-optimal trajectory is computed for real-time interpolation of drive commands within the microcontroller. This approach distinguishes itself by leveraging unit quaternions for orientation and combining Bezier splines with polynomial fitting, offering a computationally efficient and smooth trajectory generation method for PKMs. The subsequent sections of this research paper are structured as follows. Section 2 provides a concise description of the mechanism and presents its kinematics. In Section 3, the hybrid quaternion-B-spline multi-axis tool path interpolation model for the parallel robot machine tool is established. The smooth trajectory generation problem is addressed in Section 4, where the minimum jerk time optimal piece-wise Bezier curves are utilized. Section 5 begins by illustrating the developed firmware and experimental setup, followed by an in-depth discussion of the obtained results. The paper is concluded in Section 6.

## 2. Brief Mechanism Description and Kinematics

## 2.1. Four DOF parallel kinematic milling robot

The Euclidean geometric group has a subset called Schönfels motion, which describes the motion of a rigid body based on three longitudinal motions and one rotation around a fixed axis independent of each other, which is represented by the 3T1R index in robotics. Based on this concept, the mechanism in this paper was designed and developed by the authors and fully presented in detail [35]. The mechanism depicted in Figure 1(a) consists of four kinematic chains connected to an end-effector. As shown in Figure 1(b), the ball screw system of rails is coupled to stepper motors which act as actuators for the kinematic chains while linear encoders are coupled to the saddles for motion tracking. Motion generated by the stepper motors actuates the prismatic joints and desired motion is transferred to the end-effector and tool tip.

![](Akhbari2026Smooth_figs/b0898508b2afe73fe3bb0581b2fd35370f96f0d1e414a0d3da69eba965b3d0c4.jpg)  
Fig.1. (a) CAD model of the manipulator under study, (b) Real-world 4DOF parallel robot milling robot.

## 2.2. Kinematics

Kinematics is a fundamental component in the generation of trajectories and tool paths for parallel robots. To achieve the desired tool motion, the temporal motion information of the tool resulting from interpolation must be translated into the corresponding movement of actuators each interpolation period through the use of inverse kinematics.

Figure 2 illustrates the kinematic configuration of the mechanism. The global frame origin {O} is defined as the center of a spatial rectangle. The vector connecting the global origin to local origin of the ith prismatic joint is denoted as $\mathbf { a } _ { i } ,$ and the vector denoted as $d _ { i } \hat { \mathbf { d } } _ { i }$ represents the distance of the ith prismatic joint with respect to its local reference. The vector $\mathbf { L } _ { i }$ represents the spatial directions and lengths of the ith limb. Each connector on the end effector has the vector $\mathbf { c } _ { i }$ , beginning from the midpoint of the universal joints and ending at the revolute axis of the connector. Additionally, ${ \mathrm { \bf ~ P } } _ { { \mathrm { \bf ~ b } } _ { i } }$ is defined as the vector representing the end joint of ith parallelogram relative to the local frame, {??} of the end-effector.

![](Akhbari2026Smooth_figs/fbf5f28c31bc16033c3485cca7fdac9b6d83885bbbd6e5056523b18382be16a1.jpg)  
Fig.2. Free body diagram of two representative kinematic chains (identical pairs are omitted).

A comprehensive study of the kinematics is provided in the author’s previous publication [35]. Consequently, this paper presents only the final matrix form of the equations. According to Figure 2(a) closed form solution can be found for the inverse kinematics of position in the following vector form:

$$
d _ {i} = - c _ {i} + \hat {\mathbf {d}} _ {i} ^ {T} (\mathbf {p} _ {i} + \mathbf {b} _ {i} - \mathbf {a} _ {i}) - \left(l _ {i} ^ {2} - (\mathbf {p} _ {i} + \mathbf {b} _ {i} - \mathbf {a} _ {i}) ^ {T} \left(\mathbf {I} _ {3 \times 3} - \hat {\mathbf {d}} _ {i} \hat {\mathbf {d}} _ {i} ^ {T}\right) (\mathbf {p} _ {i} + \mathbf {b} _ {i} - \mathbf {a} _ {i})\right) ^ {1 / 2}\tag{1}
$$

If R<sub>x</sub> represents the rotation matrix around x axis, then in equation (1), $\mathbf { b } _ { i } = \mathbf { R } _ { x } ^ { \mathrm { ~ \tiny ~ P ~ } } \mathbf { b } _ { i }$ , and $\mathbf { I } _ { 3 \times 3 }$ is the identity matrix.

According to [35] by differentiating the kinematic chain from equation (1) against time, velocity equilibrium can be written as:

$$
{[ \mathbf {L} _ {i} ^ {T}} {\left(\mathbf {b} _ {i} \times \mathbf {L} _ {i}\right) \cdot \hat {\mathbf {i}} ] _ {4 \times 4} \left[ \dot {\pmb {\mathbf {p}}} \atop \dot {\alpha} \right] _ {4 \times 1} = \left[ \mathrm{diag} \big (\hat {\mathbf {d}} _ {i} \cdot \mathbf {L} _ {i} \big) \right] _ {4 \times 4} [ \dot {d} _ {1} \quad \dots \quad \dot {d} _ {4} ] _ {4 \times 1} ^ {T} \Rightarrow \mathbf {J} _ {p} \dot {\mathbf {P}} = \mathbf {J} _ {d} \dot {\mathbf {d}} _ {i},}\tag{2}
$$

In this context, $\mathbf { J } _ { p }$ and ${ \mathbf { J } } _ { d }$ represent the Jacobian matrices of end-effector and joint space, respectively. As expounded in [35], Higher-order kinematics can be derived by taking successive time derivatives of the kinematic equation (2). The Leibniz rule can be used to organize the higher-order kinematics in a recursive form, as shown in equations (3) and (4).

$$
\mathbf {P} ^ {(n + 1)} = \mathbf {J} _ {p} ^ {- 1} \left(\sum_ {k = 0} ^ {n} \binom {n} {k} \mathbf {J} _ {d} ^ {(n - k)} \mathbf {d} ^ {(k + 1)} + (\delta (n) - 1) \left(\sum_ {k = 0} ^ {n - 1} \binom {n} {k} \mathbf {J} _ {p} ^ {(n - k)} \mathbf {P} ^ {(k + 1)}\right)\right),\tag{3}
$$

$$
\mathbf {d} ^ {(n + 1)} = \mathbf {J} _ {d} ^ {- 1} \left(\sum_ {k = 0} ^ {n} {\binom {n} {k}} \mathbf {J} _ {P} ^ {(n - k)} \mathbf {P} ^ {(k + 1)} + (\delta (n) - 1) \left(\sum_ {k = 0} ^ {n - 1} {\binom {n} {k}} \mathbf {J} _ {d} ^ {(n - k)} \mathbf {d} ^ {(k + 1)}\right)\right),\tag{4}
$$

The $( n { + } 1 ) t h \left( \mathrm { n { \ge } 0 } \right)$ derivative with respect to time $t ,$ is denoted as superscript $( { \mathrm { e . g . } } \partial d ^ { 3 } / \partial t ^ { 3 } , { \mathrm { n } } { = } 2 )$ , where k represents the order of the derivative with respect to time. The notation $\binom { n } { k }$ refers to the binomial coefficient. P is a 4×1 vector containing end effector pose, and d is the 4×1 vector for joints displacement. And $\delta ( \cdot )$ represents the Dirac delta function. For example, given the end-effector pose, velocity, acceleration, and jerk vectors $( \mathbf { P } , \mathbf { P } ^ { ( 1 ) } , \mathbf { P } ^ { ( 2 ) } , \mathbf { P } ^ { ( 3 ) } )$ one can calculate the corresponding joint jerk vector, d <sup>(3)</sup> using Equation (4) by iterating over $n = 0 , \cdots 2$ . Also, the reader is referred to the authors previous work [35] for further details on the procedure of extracting the derivatives of Jacobian matrices $( \mathbf { J } ^ { ( \mathrm { n + 1 } ) } )$ .

## 3. Hybrid B-splines-Quaternions based tool path interpolation

This section explores parametric interpolation for the parallel robot’s toolpath. As shown in Figure 3, the process begins by extracting input data from a pre-defined path, separating tooltip position and orientation into respective vectors. B-spline curves are fitted to this data to define the toolpath. To reduce interpolation computation time, the toolpath length is pre-calculated using numerical integration and stored in a look-up table. The nonlinear relationship between curve length and parameter is approximated using piecewise ninth-degree polynomials, ensuring C³ continuity. Modifier polynomials estimate the next curve parameter during interpolation, providing the tooltip position via the B-spline curve. For orientation, Euler angles are converted to unit quaternions, and quintic B-splines are fitted. The arc-length-to-parameter relationship is modeled using seventh-degree piecewise Bezier curves through nonlinear optimization. After computing position and derivatives via inverse kinematics, a second trajectory optimization layer generates actuator motion profiles, which are sent to an Arduino Due microcontroller for real-time pulse generation. The decoupled approach fits discrete tool pose data using two distinct curves: C(u) for tooltip position and $\mathbf { O } ( w )$ for tool rotation. $\mathbf { O } ( w )$ is first mapped to quaternion space, Q(w), before being converted back to Euler angles for inverse kinematics.

Unlike the double spline method, C(u) and Q(w) are independent functions of different geometric parameters. This approach allows independent adjustment of orientation or position. Since position and rotation depend on different geometric parameters, re-parameterization functions ensure proper curve synchronization. Modifier polynomials u(s) and piecewise Bezier curves w(s) are used for position and rotation, respectively, where s is the toolpath displacement. These functions synchronize position and rotation while preserving geometric smoothness, and motion continuity.

![](Akhbari2026Smooth_figs/e6bc4b84b3d5375326e7099168c5080011a624076bc6b69f9c590a875288dbcd.jpg)  
Fig.3. An overview of the proposed interpolation process.

## 3.1. B-Spline formulation

Rather than Cox-Deboor recursive formula, B-splines can be represented in matrix form using a basis function matrix. A general matrix notation for B-spline curves of an arbitrary degree can be presented by means of a Toeplitz matrix, which results in an explicitly recursive matrix formula. The matrix algorithm has less time complexity than the Cox-de Boor, when used for conversion and computation of B-spline curves and surfaces [36]. Let $\mathbf { U } = \{ u _ { i } \} _ { j = 1 } ^ { n + p + 1 }$ be a knot vector for a B-spline curve of degree $p ,$ then matrix notation is given, as follows:

$$
\pmb {C} (u) = \pmb {N} _ {p} (u) \pmb {c}\tag{5}
$$

Where $\pmb { c } = \left[ c _ { i - p } , c _ { i - p + 1 } , \hdots c _ { i } \right] ^ { T }$ is the control point vector and the set of blending matrices of degree p is $N _ { p } ( u )$ is a $p \times ( p + 1 )$ sparse matrix with two nonzero elements on each row. The element wise construction of the matrix is, as follows:

$$
\left(N _ {p}\right) _ {k, l} = \left(1 - v _ {d, i - p + 1}\right) \delta_ {k, l} + v _ {d, i - p + k} \delta_ {k + 1, l}\tag{6}
$$

Where $\delta _ { k , l }$ is the Kronecker delta, $v _ { p , i } ( u ) = ( u - u _ { i } ) ( u _ { i + p } - u _ { i } ) ^ { - 1 } \cdot \left[ u _ { i } \leq u < u _ { i + p } \right]$ is the scaling function defined using the Iverson bracket [∙].

## 3.2. Tool position interpolation

The goal of B-spline curve fitting is to select the degree $p ,$ knot vector U and control points $\pmb { c } _ { i }$ for the parametric curve $C ( u )$ , so that the curve passes through every tool position vector $\mathbf { p } _ { k } = [ p _ { x , k } , \ p _ { y , k } ,$ $p _ { z , k } ] ^ { T } , k = 0 , 1 , \ldots , N$ with the desired continuity. To maintain at least jerk continuity, a B-spline curve of the fifth degree is required, so $p { = } 5$ is set. To determine the knot vector U, first parametric values ${ { \bar { u } } _ { k } }$ are assigned to each position vector using the centripetal method.

$$
\bar {u} _ {k} = \bar {u} _ {k - 1} + \frac {\sqrt {\| \mathbf {p} _ {k} - \mathbf {p} _ {k - 1} \|}}{\sum_ {k = 1} ^ {N} \sqrt {\| \mathbf {p} _ {k} - \mathbf {p} _ {k - 1} \|}}, k = 1, \dots , N - 1, \bar {u} _ {0} = 0, \bar {u} _ {1} = 1\tag{7}
$$

As can be seen from equation (7), the parameter values are selected based on the distribution of the position vector along the tool path. By using the centripetal method, the oscillating behavior of the curve between the waypoints is minimized. The elements of knot vector are then obtained by averaging (9) as follows:

$$
\left\{ \begin{array}{l} u _ {0} = u _ {1} = \dots u _ {k} = 0; u _ {N + 1} = u _ {N + 2} = \dots = u _ {N + p + 1} = 1 \\ u _ {j + p} = \frac {1}{p} \sum_ {k = j} ^ {j + p - 1} \bar {u} _ {k}, j = 1, 2, \dots , N - p \end{array} \right.\tag{8}
$$

The knot vector will have a similar characteristic to the assigned parameters since they are obtained based on their distribution. The number of basic functions and control points in equation (5) are set equal to the number of position points of the tool tip p<sub>k</sub> so that it is possible to extract and solve the system of $( N + 1 ) \times ( N + 1 )$ ) linear equations. Since the knot vector U is known from equation (10), the basis functions $N _ { i , p } ( u )$ for each parameter u are obtained from equations (7) and (8). Furthermore, because a parameter value $\overline { { u } } _ { k }$ is assigned for each position vector $\mathbf { P } _ { k } ,$ the vector of control points, c<sub>i</sub> is determined by solving the following system of linear equations by inverse method:

$$
\underbrace {\left[ \begin{array}{c c c} N _ {0 , p} (\overline {{u}} _ {0}) & \cdots & N _ {N , p} (\overline {{u}} _ {0}) \\ \vdots & \ddots & \vdots \\ N _ {0 , p} (\overline {{u}} _ {N}) & \cdots & N _ {\mathrm{N} , p} (\overline {{u}} _ {N}) \end{array} \right]} _ {\boldsymbol {\Phi} _ {1}} \underbrace {\left[ \begin{array}{c} \boldsymbol {c} _ {0} ^ {T} \\ \vdots \\ \boldsymbol {c} _ {N} ^ {T} \end{array} \right]} _ {\boldsymbol {\Gamma} _ {1}} = \underbrace {\left[ \begin{array}{c} \boldsymbol {p} _ {0} ^ {T} \\ \vdots \\ \boldsymbol {p} _ {N} ^ {T} \end{array} \right]} _ {\boldsymbol {\Psi} _ {1}} \to \boldsymbol {\Phi} _ {1} = \boldsymbol {\Gamma} _ {1} ^ {- 1} \boldsymbol {\Psi} _ {1}\tag{9}
$$

After calculating the knot vector U and control points, the tool position data is fitted by the B-spline curve C(u) of equation (5).

## 3.2.1. Modifier Polynomials

For the purpose of interpolating the position of the B-spline curve parameter, it is necessary to formulate the nonlinear relationship between u and s. The arc length of a parametric curve within a given parameter interval can generally be determined through the use of an integral as follows:

$$
s (b) - s (a) = \int_ {a} ^ {b} \| \partial \pmb {C} (u) / \partial s \| d u, 0 \leq a \leq b \leq 1\tag{10}
$$

Adaptive quadrature Simson’s rule, the result is series of parametric intervals with corresponding displacements. The displacements between intervals are successively summed resulting in a set of cumulative displacements $\pmb { s } _ { j } = [ 0 \quad s _ { 1 } \quad s _ { 2 } \quad \cdots \quad s _ { M } = S _ { \Sigma } ] ^ { T }$ at corresponding geometric parameter $\pmb { u _ { j } } ^ { * } = [ 0 \quad u ^ { * } { } _ { 1 } \quad u ^ { * } { } _ { 2 } \quad \cdots \quad u ^ { * } { } _ { M } = 1 ] ^ { T }$ , with $S _ { \Sigma }$ being the total length of the tool path.

Then series of ninth order, piece-wise modifier-polynomials are fitted through the data. To avoid ill conditioning, the modifier-polynomials are constructed with normalized arc lengths as follows:

$$
\left\{ \begin{array}{l} \hat {u} (\sigma_ {k}) = \sum_ {i = 0} ^ {9} a _ {i} \sigma_ {k} ^ {i}, j = 1, \dots , M, k = 1, \dots , n \\ 0 \leq {\pmb {\sigma}} \leq 1, {\pmb {\sigma}} _ {k} = [ 0, \sigma_ {1}, \dots , \sigma_ {M - 1}, 1 ], \sigma_ {k j} = \frac {s _ {k j} - s _ {k 0}}{S _ {\Sigma} - S _ {k 0}} \end{array} \right.\tag{11}
$$

In order to formulate constraints on the endpoints of a polynomial segment, and to ensure continuity of at least third order, derivative of u with respect to s from equation (10), and derivatives of ??̂ with respect to s in equation (11) are required. These derivatives are obtained using the chain rule for equation (10) and (11) respectively as follows:

$$
\hat {u} ^ {(r)} (s) = \frac {\partial^ {r} \hat {u}}{\partial s ^ {r}} = \Big (\frac {\partial \sigma}{\partial s} \Big) ^ {r} \sum_ {i = r} ^ {N} \big (\prod_ {j = 0} ^ {r - 1} (i - j) \big) a _ {i} \sigma^ {i - r}, r = 0, \dots , n\tag{12}
$$

Subsequently, an optimization problem is formulated to estimate the polynomial coefficients. The objective function is constructed based on the least squares of the actual parameters $u ^ { * }$ and the estimated ones from equation (11). The boundary conditions are imposed as a linear function of the coefficients via (12) at the endpoints $u { = } 0$ and $u { = } 1$ . The optimization problem then can be expressed in a general form as follows:

$$
\min _ {\boldsymbol {\alpha}} \frac {1}{2} (\mathbf {u} ^ {*} - \boldsymbol {\Phi} \boldsymbol {\alpha}) ^ {T} (\mathbf {u} ^ {*} - \boldsymbol {\Phi} \boldsymbol {\alpha})\tag{13}
$$

$$
\text { s.t. } \quad \Omega \alpha - \eta = 0\tag{14}
$$

In this context,?? denotes the matrix whose elements are the normalized arc lengths, $\sigma _ { j } ,$ , where $j =$ $1 , \cdots , M$ substituted in equation (14). α represents the vector of corresponding unknown coefficients $a _ { i } ,$ where $i = 0 , \cdots , 9$ . Additionally, ?? signifies the matrix of constants and eta is the vector of fixed boundary conditions obtained from equation (12) at the endpoints, in the following form:

$$
\Omega_ {0 _ {r n}} = \left\{ \begin{array}{l l} \prod_ {m} ^ {r - 1} (r - m) & \text {if} r = n \\ 0 & \text {if} r \neq n \end{array} \right.\tag{15}
$$

$$
\eta_ {0 _ {r}} = u ^ {(r)} (s = 0)\tag{16}
$$

$$
\Omega_ {(\sigma_ {M}) _ {r n}} = \left\{ \begin{array}{l l} (\prod_ {m = 0} ^ {r - 1} (r - m)) \sigma_ {M} ^ {n - r} & \text {if} n \geq r \\ 0 & \text {if} n <   r \end{array} \right.\tag{17}
$$

$$
\eta_ {(\sigma_ {M}) r} = u ^ {(r)} (\sigma_ {M} = 1)\tag{18}
$$

Which leads to a linear, constrained quadratic minimization problem. This problem can be solved through any linear programming method in a straightforward manner namely, the elimination method or Lagrange multipliers. Introduction of a vector of Lagrange multipliers ?? to objective function results in the following system of linear equations:

$$
\left[ \begin{array}{c c} \boldsymbol {\Phi} ^ {T} \boldsymbol {\Phi} & \boldsymbol {\Omega} ^ {T} \\ \boldsymbol {\Omega} & 0 \end{array} \right] \left[ \begin{array}{c} \boldsymbol {\alpha} \\ \boldsymbol {\Lambda} \end{array} \right] = \left[ \begin{array}{c} \boldsymbol {\Phi} ^ {T} \mathbf {u} ^ {*} \\ \boldsymbol {\eta} \end{array} \right]\tag{19}
$$

Given that all segments of arc length are non-zero, it follows that the matrix in equation (19) possesses full rank and is thus invertible. Consequently, the normalized coefficients α may be readily derived via the application of the Cholesky decomposition method. To minimize the estimation of the curve parameter, a recursive adaptive step is incorporated, segmenting the polynomial into several piecewise polynomials until the mean squared error between the actual and estimated parameters falls below a specified tolerance. Should this tolerance be exceeded, the data set ${ \pmb u } _ { j } ^ { * }$ is divided into two equal subsets, with a polynomial fitted to each group of points using the proposed method. This iterative process of splitting and fitting terminates when all modifier polynomials meet the specified condition or when the amount of data in a subset equals the degree of the polynomial. Upon convergence, the nonlinear relationship between s and u is represented by a series of piecewise ninth-order C3 continuous polynomials.

## 3.3. Tool orientation interpolation

As depicted in the flowchart presented in Figure 4, the tool orientation B-spline is not directly fitted to the raw tool orientation data, in contrast to the tool tip position. To ensure that the magnitude of the orientation vectors remains equal to unity, the tool orientation data is initially mapped into quaternion space. Given the absence of an explicit relationship between the path length parameter and the B-spline parameter of quaternions, a non-linear relationship between the arc length parameter and the quaternion parameter is established through the use of Bezier curves and non-linear optimization. Ultimately, through inverse mapping of the quaternions, the Euler angles denoting the spatial orientation of the tool during the corresponding interpolation period are derived.

![](Akhbari2026Smooth_figs/c0def28a46510d9cb856e587f88bd3c5bfae89cfbd98b58a8c88fa5d0b2db224.jpg)  
Fig.4. A flowchart describing the process of spatial interpolation of tool orientation. All computationally intensive steps (quaternion conversion, B-spline fitting, and nonlinear optimization for interpolation between B-Spline curve parameter and quaternions) occur offline in approximately 1.5 second for \~300 waypoints in optimized C++.

While the rotation matrix provides a convenient means of expressing the spatial orientation of a rigid body, this approach is not without its limitations. One notable issue pertains to the order of matrix multiplication; for a given set of Euler angles, different multiplication sequences can yield disparate results. Another challenge associated with the use of rotation matrices is the phenomenon of gimbal lock, which arises due to singularities in the matrix. This can result in the loss of one degree of rotational freedom for certain angular configurations of the rigid body. The aforementioned challenges, render the parametric fitting and interpolation of rotation matrices a complex task. Consequently, smooth interpolation is facilitated through the conversion of Euler angles into unit quaternions.

A unit quaternion, which is a type of hyper-complex number and satisfy the condition $\| \mathbf { Q } \| _ { 2 } = 1$ , can be utilized to provide a unique description of an object’s orientation. It is expressed in the following manner:

$$
\mathbf {Q} = [ q _ {0} \quad q _ {1} \quad q _ {2} \quad q _ {3} ] ^ {T} = q _ {0} + q _ {1} i + q _ {2} j + q _ {3} k\tag{20}
$$

Wherein $q _ { r } , \ r \in \{ 0 , \ldots , 3 \}$ are real numbers, while $i , j ,$ and k are imaginary units and satisfy $i ^ { 2 } = j ^ { 2 } =$ $k ^ { 2 } = i j k = - 1$ . This subset of quaternions constitutes the group of unit quaternions.

In order to streamline the notation, the vector representation comprising the real component $q _ { 0 }$ and the imaginary vector component q is employed, resulting in:

$$
\mathbf {Q} = [ q _ {0}, \mathbf {q} ] ^ {T}, \mathbf {q} = [ q _ {1} q _ {2} q _ {3} ] \in \mathbb {R} ^ {3}\tag{21}
$$

The multiplication of two quaternions yields a resultant quaternion, which is derived through the subsequent relationship:

$$
\mathbf {Q} = \mathbf {Q _ {1}} \mathbf {Q _ {2}} = [ q _ {1 0}, \mathbf {q _ {1}} ] ^ {T} [ q _ {2 0}, \mathbf {q _ {2}} ] ^ {T} = [ q _ {1 0} q _ {2 0} - \mathbf {q _ {1} ^ {T}} \mathbf {q _ {2}}, q _ {1 0} \mathbf {q _ {2}} + q _ {2 0} \mathbf {q _ {1}} + \mathbf {q _ {1}} \times \mathbf {q _ {2}} ] ^ {T}\tag{22}
$$

Quaternion multiplication is non-commutative, meaning $\mathbf { Q } _ { 1 } \mathbf { Q } _ { 2 } \neq \mathbf { Q } _ { 2 } \mathbf { Q } _ { 1 }$ . The conjugate of a quaternion Q is denoted as $\mathbf { Q } ^ { * }$ and is defined as ${ \bf Q } ^ { * } = [ q _ { 0 } , \mathbf { \Pi } - { \bf q } ] ^ { T }$

A unit quaternion can be represented as a point on the unit hypersphere in S3 space. Quaternions can represent rotations in three-dimensional Euclidean space using their trigonometric form. Rotation of an arbitrary vector $\mathbf { p } = [ x \quad y \quad z ] ^ { T } \in \mathbb { R } ^ { 3 }$ about the unit vector ${ \bf n } = n _ { 1 } i + n _ { 2 } j + n _ { 3 } k$ by an angle of φ can be represented in the form of unit quaternions as follows:

$$
\mathbf {p} ^ {\prime} = \mathbf {Q p Q} ^ {*}\tag{23}
$$

This implies that the result of two consecutive rotations can be obtained by multiplying pair of unit quaternions, which is equivalent to the overall rotation matrix. Using this reasoning, the relationships for converting between Euler angles and quaternions have been derived. Cayley’s method is the most efficient approach for directly calculating the components of quaternions using the following equations:

$$
\begin{array}{r l} & {q _ {\mathrm{i}} = \frac {1}{4} \Big (\big (1 + \mathrm{r} _ {\mathrm{ii}} - \mathrm{tr} (\boldsymbol {R}) \big) ^ {2} + \big (\mathrm{r} _ {3 2} - (- 1) ^ {\mathrm{i}} \mathrm{r} _ {2 3} \big) ^ {2} + \big (\mathrm{r} _ {1 3} - (- 1) ^ {\mathrm{i}} \mathrm{r} _ {3 1} \big) ^ {2} + \big (r _ {2 1} - (- 1) ^ {\mathrm{i}} r _ {1 2} \big) ^ {2}} \\ & {(- 1) ^ {i} r _ {1 2} \Big) ^ {2} \Big) ^ {1 / 2}, \mathrm{tr} (\boldsymbol {R}) = r _ {1 1} + r _ {2 2} + r _ {3 3}} \end{array}\tag{24}
$$

Similar to the position of the tool tip, the vector of tool orientations along the path, $\mathbf { 0 } _ { k } =$ $[ \alpha _ { k } , \beta _ { k } , \gamma _ { k } ] ^ { T }$ must be fitted to a parametric B-spline. Similar to curve fitting for tool tip position, the purpose of curve fitting for tool orientation is to select the degree, the knot vector W, and the control points. But, since the length of the tool remains constant, the magnitude of the orientation vector must always be equal to unity. Therefore, in contrast to fitting on the tool tip position data, the tool orientation B-spline is not directly fitted on the raw tool orientation data. Rather, to ensure that the magnitude of the orientation vectors is always equal to unity, and avoid gimbal lock, the tool orientation curve is fitted in quaternion space. According to this, by using equation (24), the spatial orientation of the tool expressed by the Euler angles are converted into their equivalent unit quaternions $\mathbf { Q } _ { k } = [ q _ { o k } , \ \mathbf { q } _ { k } ]$

A basic form of quaternion interpolation involves leveraging the spherical linear interpolation (SLERP) method. This approach interpolates along the geodesic of two quaternions, thus following the shortest distance between them. Specifically, the exponential-logarithmic representation of SLERP is provided as follows:

$$
\mathbf {Q} (w) = \mathbf {Q} _ {1} \exp (\log (\mathbf {Q} _ {1} ^ {*} \mathbf {Q} _ {2}) w), w \in [ 0, 1 ]\tag{25}
$$

Within the domain of B-Spline interpolation in three-dimensional space, a parametrization approach that involves an angle?? ∈ ℝ and an axis ?? $\in \mathbb { R } ^ { 3 }$ with $\| \mathbf { n } \| _ { 2 } = 1$ has proven to be beneficial. This leads to the adoption of the quaternion representation, which can be expressed as:

$$
\mathbf {Q} = [ \cos (\varphi / 2) \sin (\varphi / 2) \mathbf {n} ] ^ {T} = \exp \boldsymbol {\psi}, \quad \boldsymbol {\psi} = [ 0 (\varphi / 2) \mathbf {n} ] ^ {T}\tag{26}
$$

Wherein ${ \bf n } = n _ { 1 } i + n _ { 2 } j + n _ { 3 } k$ , denotes a unit pure quaternion. The exponential mapping procedure produces a unit quaternion that represents a rotation, which corresponds to the pure quaternion vector ??. The scaled rotation axis is subsequently denoted as $\boldsymbol { \psi } = ( \varphi / 2 ) \mathbf { n }$ . The inverse of equation (26), namely the logarithmic form of a quaternion, can be defined as follows:

$$
\pmb {\Psi} = [ 0 \quad \psi ] ^ {T} = \log \mathbf {Q} = \log ([ \cos (\varphi / 2) \quad \sin (\varphi / 2) \mathbf {n} ] ^ {T})\tag{27}
$$

The SLERP interpolation method enables rotations with a constant angular derivative, resulting in a zero second derivative. However, this technique is not ideal for generating a path that passes through more than two quaternions or connects multiple segments. The resulting path will be discontinuous. Consequently, a novel method, derived from the SLERP approach, has been introduced for generating a parametric path that considers all input quaternion data simultaneously. To ensure that the quaternions remain unit quaternions, a mapping technique is employed, which is expressed as follows:

$$
\mathbf {Q} (w) = \mathbf {Q} _ {1} \exp \left(\left[ 0 \quad \frac {\varphi (w)}{2} \mathbf {n} (w) \right] ^ {T}\right) = \mathbf {Q} _ {1} \left[ \cos \left(\frac {\varphi (w)}{2}\right) \quad \sin \left(\frac {\varphi (w)}{2}\right) \mathbf {n} (w) \right] ^ {T}\tag{28}
$$

Equation (28) exhibits similarity to Equation (25), with the primary difference being that in Equation (38), the angle $\varphi$ and the unit rotation axis n are both functions of the parameter w. It is noteworthy that $\mathbf { Q } _ { 1 }$ represents the initial orientation. By suitably adjusting ??(??) and $\varphi ( w )$ , the desired path in quaternions can be obtained. The local rotational vector $\Psi ( w ) = [ 0 , \ \psi ^ { T } ( w ) ] ^ { T }$ is formulated, taking into account that $| | \mathbf { n } | | _ { 2 } = 1$ , and this vector is utilized for path generation. Thus, Equation (28) can be represented as follows:

$$
\mathbf {Q} (w) = \mathbf {Q} _ {1} \mathrm{exp} \big (\boldsymbol {\Psi} (w) \big)\tag{29}
$$

The local orientation vector $\Psi ( w )$ is represented as a pure quaternion. Equation (29) allows interpolation of a B-spline curve through the imaginary component of the quaternion. The extraction of the imaginary vector $\psi ( w )$ from the quaternions $\mathbf { Q } _ { k } , \ k = 1 , \ldots , N + 1$ , is achieved using the following expression:

$$
{ [ 0 } { \psi ( w _ { k } ) ] ^ { T } = \log ( \mathbf { Q } _ { 1 } ^ { * } \mathbf { Q } _ { k } ) }\tag{30}
$$

In which the subsequent equations hold:

$$
\left\{ \begin{array}{l} \varphi_ {k} (w) = 2 \| \boldsymbol {\Psi} _ {k} (w) \| \\ \mathbf {n} _ {k} (w) = \frac {2 \mathrm{Im} (\boldsymbol {\Psi} _ {k} (w))}{\psi_ {k} (w)} \end{array} \right.\tag{31}
$$

Finally, the imaginary vectors obtained from equation (30), similar to the position data, can be interpolated by B-spline curves. Assuming a knot vector W and control points Θ consisting of pure imaginary quaternions, the B-spline curve is expressed in matrix form similar to (5) as follows:

$$
\psi (w) = \mathbf {N} _ {p} (w) \Theta\tag{32}
$$

The control points can be obtained by solving a system of linear equations, using a method identical to that employed in generating position tool paths. The difference lies in the knot vector estimation, where the geodesic angular distance is utilized instead of the Euclidean distance. Upon calculating $\varphi _ { k } ( w )$ through (32), the quaternion path is attained using equations (29) through (31). In Figure 5, the B-spline curves obtained for a sample quaternion data set utilizing the two SLERP and the B-spline method introduced in this article are shown. As is evident from Figure 5, the presented approach enables highorder continuity and results in a smoother curve.

Similar to the tooltip position parameter $u ,$ the tool orientation parameter w must also be interpolated as a function of the toolpath length s. However, unlike the position spline, there is no direct relationship between s and the parameter $w ,$ , as tool orientation does not affect tooltip displacement. Hence, from the available $( s _ { k } , ~ \overline { { w } } _ { k } )$ data, a parametric curve can be fitted to represent this non-linear relationship. However, due to scarcity of data, curves with optimized internal energy functional can be employed to ensure uniformity, at least third-order continuity, and minimal oscillations. The shape-preserving property of piecewise Bezier curves makes it suitable for the task. The definition of the nth order Bezier curve is as follows:

$$
w _ {k} (\sigma) = \sum_ {i = 0} ^ {n} {\binom {n} {i}} (1 - \sigma) ^ {n - i} \sigma^ {i} \rho_ {i, k}, \sigma = \frac {s - s _ {k - 1}}{s _ {k} - s _ {k - 1}} \in [ 0, 1 ]\tag{33}
$$

(a)  
![](Akhbari2026Smooth_figs/a06ee47355dee83d87847eea1ada8017e09b42229806806e3fb029331de18f96.jpg)

(b)  
![](Akhbari2026Smooth_figs/da14a928e76ddcd7bb83025e2f79bb842a32e944e462f6dc43234606608ffbf5.jpg)  
Fig.5. Curves obtained from the interpolation of the quaternion data using: a) SLERP, b) cubic Bspline.

In accordance with equation (33), Bezier curves are fitted to each interval $\left[ s _ { k - 1 } , \ s _ { k } \right]$ . The control coefficients $\rho _ { i , k }$ are not known a priori, where the subscript i denotes the numerator of the coefficients within the kth curve segment.

The constraints are delineated based on three distinct criteria, namely, the monotonicity of curves, the requirement that curves pass through all data points $( s _ { k } , \overline { { w } } _ { k } )$ , and the need for rth order continuity at segment junctions. These constraints are mathematically expressed in equations (34) through (36) as follows:

$$
\rho_ {0, k} \leq \rho_ {1, k} \leq \dots \leq \rho_ {n - 1, k} \leq \rho_ {n, k}, k = 1, \ldots , N\tag{34}
$$

$$
[ \rho_ {0, k} \quad \rho_ {n, k} ] ^ {T} = [ \overline {{w}} _ {k - 1} \quad \overline {{w}} _ {k} ] ^ {T}, k = 1, \dots , N\tag{35}
$$

$$
\frac {\Delta^ {r} \rho_ {n - 1 , k}}{(s _ {k} - s _ {k - 1}) ^ {r}} = \frac {\Delta^ {r} \rho_ {1 , k + 1}}{(s _ {k + 1} - s _ {k}) ^ {r}}, \quad \Delta^ {r} \bar {\rho} _ {n} = \sum_ {j = 0} ^ {r} {\binom {r} {j}} (- 1) ^ {2 r - j} \bar {\rho} _ {n + j}\tag{36}
$$

Wherein the forward difference operator, denoted by $\Delta ^ { r }$ , which adheres to Pascal's triangle law.

To determine the optimal control points for piece-wise Bezier curves that interpolate the tool orientations, a nonlinear optimization problem with linear constraints may be formulated. The objective function for this problem is defined as the integral square of the rth derivative, subject to the constraints specified in equations (42) through (44). Specifically, for the case of $r = 3$ , also known as minimized jerk, the objective function can be expressed as follows:

$$
\min _ {\rho_ {i, k}} J _ {\rho} = \sum_ {k = 1} ^ {N} \int_ {0} ^ {1} \frac {w ^ {\prime \prime \prime} {} _ {k} ^ {2}}{(s _ {k} - s _ {k - 1}) ^ {5}} \mathrm{d} \sigma\tag{37}
$$

Any nonlinear optimization method, such as interior point or active-set methods, can be employed to solve the minimization problem. Nevertheless, a straightforward time efficient method is presented in the subsequent section, given that minimum jerk trajectories are formulated in a similar manner. The solution of (37) produces the optimal control points of orientation interpolation function.

## 4. Minimum jerk time optimal Trajectory generation

Minimum-jerk Bezier splines have proven very effective as robot trajectories, since the motor commands and orientation accelerations of the mechanism are proportional to the jerk, or forth derivative of the tool path. Convex hull properties of Bezier curves can be exploited to satisfy spatial and temporal separation constraints for multi-agent trajectory generation.

This article presents a two-step optimization approach for generating minimum jerk and time optimal trajectories. The approach involves first optimizing the time allocation along each segment, followed by a feasibility-based total time optimization that takes into account drive constraints.

## 4.1 Minimum Jerk Objective function

The trajectories are generated using piece-wise Bezier curves, with arc length parameterized against time. Composite Bezier curves are formed by connecting multiple Bezier curves at their beginning and end points, while ensuring continuity of the desired degree between adjacent curves. These composite curves are defined as following:

$$
\rho (t) = \left\{ \begin{array}{l l} \sum_ {n = 0} ^ {N} \bar {\rho} _ {0, N} b _ {n} ^ {N} \left(\frac {t - t _ {0}}{t _ {1} - t _ {0}}\right) & t _ {0} \leq t \leq t _ {1} \\ \sum_ {n = 0} ^ {N} \bar {\rho} _ {1, N} b _ {n} ^ {N} \left(\frac {t - t _ {1}}{t _ {2} - t _ {1}}\right) & t _ {1} \leq t \leq t _ {2} \\ \vdots \\ \sum_ {n = 0} ^ {N} \bar {\rho} _ {m - 1, N} b _ {n} ^ {N} \left(\frac {t - t _ {m - 1}}{t _ {m} - t _ {m - 1}}\right) & t _ {m - 1} \leq t \leq t _ {m} \end{array} \right.\tag{38}
$$

Where in $b _ { n } ^ { N } ( \zeta ) = \binom { N } { n } ( 1 - \zeta ) ^ { N - n } \zeta ^ { n }$ is the Bernstein basis function.

Any Bezier curve that is part of a composite curve can be defined individually with normalized time, as follows:

$$
\rho_ {k} (\zeta) = \sum_ {n = 0} ^ {N} \bar {\rho} _ {n} b _ {n} ^ {N} (\zeta) \qquad \zeta = \frac {t - t _ {k - 1}}{\tau}, \tau = t _ {k} - t _ {k - 1}\tag{39}
$$

Then, integral squared norm of the rth derivative is introduced as the objective function of each segment in the following form:

$$
J (\tau) = \min _ {\tau} \frac {1}{\tau^ {2 r - 1}} \int_ {0} ^ {1} \left(\frac {d ^ {r}}{d \zeta^ {r}} \rho (\zeta)\right) ^ {2} \mathrm{d} \zeta\tag{40}
$$

It should be emphasized that the time allocation variable is positioned outside the integral, indicating that the control points determining the minimum jerk trajectory for a given segment are not dependent on the time allocated for that segment.

By formulating the derivative of the Bezier curve in a matrix format, the following expression is derived:

$$
\frac {d ^ {r}}{d \zeta^ {r}} \rho (\zeta) = \left(\frac {N !}{(N - r) !}\right) \mathbf {B} _ {r} (\zeta) ^ {T} \mathbf {D} _ {r} \overline {{\mathbf {P}}},\tag{41}
$$

Wherein the Bernstein matrix, the matrix of control points and the matrix containing the forward difference operators, are respectively defined as follows:

$$
\begin{array}{l} \mathbf {B} _ {r} (\zeta) = [ b _ {0} ^ {N - 1} (\zeta) \quad b _ {1} ^ {N - 1} (\zeta) \quad \dots \quad b _ {N - 1} ^ {N - 1} (\zeta) ] ^ {T} \\ \overline {{\mathbf {P}}} = [ \bar {\rho} _ {0} \quad \bar {\rho} _ {1} \quad \dots \quad \bar {\rho} _ {N} ] ^ {T} \end{array}\tag{42}
$$

(43)

Furthermore, as indicated in equation (41), the matrix D<sub>r</sub> is a (N-r) by N matrix consisting of a forward difference operator, with non-zero elements.

The matrix relationships derived and the independence of the control points and the forward difference operator from time changes allow for the removal of these matrices from within the integral. As a result, the objective function expressed in equation (40) can be reformulated in matrix form as follows:

$$
J (\tau) = \min _ {\tau} \frac {1}{\tau^ {2 r - 1}} \Bigl (\frac {N !}{(N - r) !} \Bigr) ^ {2} \overline {{\mathbf {P}}} ^ {T} \mathbf {D} _ {r} ^ {T} \left(\int_ {0} ^ {1} (\mathbf {B} _ {r} (\zeta) \mathbf {B} _ {r} (\zeta) ^ {T}) \mathrm{d} \zeta\right) \mathbf {D} _ {r} \overline {{\mathbf {P}}}\tag{44}
$$

As can be seen, the expression inside the integral represents the matrix symmetric square of Bernstein polynomials. This integral can be evaluated element-wise. The integration of $F _ { r }$ on an element-wise basis requires the utilization of the Beta and Gamma function integral theorems. Upon the completion of the integration, the objective function (44) can be represented solely as the following matrix product:

$$
J (\tau) = \min _ {\tau} (\prod_ {k = 0} ^ {r - 1} (N - k)) ^ {2} \tau^ {1 - 2 r} \overline {{\mathbf {P}}} ^ {T} \mathbf {D} _ {r} ^ {T} \mathbf {F} _ {r} \mathbf {D} _ {r} \overline {{\mathbf {P}}}.\tag{45}
$$

The objective function of m Bezier curve segments can be evaluated by concatenating them through the Kronecker tensor multiplication rule as:

$$
\begin{array}{r l} & {\overbrace {J (\tau_ {0} , \ldots , \tau_ {m - 1})} ^ {\textbf {J}} =} \\ & {\underset {(\tau_ {0}, \ldots , \tau_ {m - 1})} {\min} \overbrace {[ \bar {\rho} _ {0} \quad \cdots \quad \bar {\rho} _ {m - 1} ]} ^ {\overline {{\mathbf {P}}}} \mathrm{diag} (\overbrace {[ \frac {1}{\tau_ {0} ^ {2 r - 1}} \mathbf {D} _ {r} ^ {T} \mathbf {F} _ {r} \mathbf {D} _ {r} \quad \cdots \quad \frac {1}{\tau_ {m - 1} ^ {2 r - 1}} \mathbf {D} _ {r} ^ {T} \mathbf {F} _ {r} \mathbf {D} _ {r} ]} ^ {\mathbf {Q} _ {r}}) \overbrace {[ \bar {\rho} _ {0} \quad \cdots \quad \bar {\rho} _ {m - 1} ]} ^ {\overline {{\mathbf {P}}}}} \end{array}\tag{46}
$$

The cost function for the entire trajectory can be expressed using a quadratic programming approach as follows:

$$
\mathbf {J} = \min _ {\boldsymbol {\tau}} \overline {{\mathbf {P}}} ^ {T} \mathbf {Q} _ {r} \overline {{\mathbf {P}}}\tag{47}
$$

Wherein the associated segment-wise time allocation variable $\tau = \left[ \tau _ { 0 } , \tau _ { 1 } , \dots , \tau _ { m - 1 } \right]$ is incorporated in the expression.

## 4.2. Constraints

The optimization of the piecewise Bezier curves requires the satisfaction of certain constraints, including the fixed junction points, fixed derivatives at the initial and final location based on the required initial and final states, and matched derivatives at all intermediate junction points up to the rth derivative to ensure the $\mathbf { C } ^ { r }$ continuity of the curve. These constraints can be expressed in matrix form as follows:

$$
A = [ A _ {0} \quad A _ {1} ] ^ {T} = [ \mathbf {B} _ {0} ^ {T} (0) \mathbf {D} _ {0} \quad \dots \quad \mathbf {B} _ {r} ^ {T} (0) \mathbf {D} _ {r} \quad \mathbf {B} _ {0} ^ {T} (1) \mathbf {D} _ {0} \quad \dots \quad \mathbf {B} _ {r} ^ {T} (1) \mathbf {D} _ {r} ] ^ {T},\tag{48}
$$

In the given context, where A represents the Bernstein component of each derivative at the fixed control points, and

$$
d = [ d _ {0} \quad d _ {1} ] ^ {T} = \left[ \frac {\partial^ {0}}{\partial t ^ {0}} \rho (0) \quad \dots \quad \frac {\partial^ {r}}{\partial t ^ {r}} \rho (0) \quad \frac {\partial^ {0}}{\partial t ^ {0}} \rho (1) \quad \dots \quad \frac {\partial^ {r}}{\partial t ^ {r}} \rho (1) \right] ^ {T},\tag{49}
$$

The vectors in (48) and (49) comprises the values corresponding to the fixed or matched derivatives at the fixed control points. It is important to note that the aforementioned constraints apply to each individual Bezier segment. To represent the constraints for the entire trajectory, the entries are populated in a block-diagonal manner as follows:

$$
\overbrace {\left[ \begin{array}{c c c c c} A _ {0} & & & & \\ A _ {1} & & & & \\ A _ {1} & & - A _ {0} & & \\ & & A _ {1} & & \\ & & \vdots & \ddots & \\ & & & & A _ {1} \end{array} \right]} ^ {\mathbf {A}} \overbrace {\left[ \begin{array}{c} \bar {\rho} _ {0} \\ \bar {\rho} _ {1} \\ \vdots \\ \vdots \\ \vdots \\ \bar {\rho} _ {m - 1} \end{array} \right]} ^ {\overline {{\mathbf {P}}}} = \overbrace {\left[ \begin{array}{c} b _ {0 , 0} \\ b _ {0 , 1} \\ 0 \\ b _ {1 , 1} \\ \vdots \\ b _ {m - 1 , 1} \end{array} \right]} ^ {\mathbf {b}},\tag{50}
$$

## 4.3. Unconstrained QP Solution

To prevent the occurrence of singular or poorly conditioned matrices during the nonlinear optimization process, which is commonly challenging due to the large sparse matrices defining the constraint equations, a strategy can be employed. This strategy involves incorporating the constraints directly into the cost function using matrix inversion. By adopting this approach, the optimization process becomes more efficient, allowing for the direct extraction of the optimal control points based on the given time allocation. Hence, the cost function of the unconstrained formulation can be represented as follows:

$$
\mathbf {J} = \min _ {\boldsymbol {\tau}} \mathbf {d} ^ {T} \mathbf {A} ^ {- T} \mathbf {Q} _ {r} \mathbf {A} ^ {T} \mathbf {d}\tag{51}
$$

The newly formulated quadratic cost function now involves the endpoint derivatives of the segments as decision variables. These variables are re-arranged such that the fixed or specified derivatives are grouped together (denoted as ${ \bf d } _ { k } )$ , while the free or unspecified derivatives are grouped together (denoted as $\mathbf { d } _ { u } )$ . To achieve this re-ordering, a sparse permutation matrix (M) is constructed. Thus, the revised expression is as follows:

$$
\mathbf {J} = \min _ {\boldsymbol {\tau}} \left[ \begin{array}{c} \mathbf {d} _ {k} \\ \mathbf {d} _ {u} \end{array} \right] ^ {T} \overbrace {\mathbf {M A} ^ {- T} \mathbf {Q} _ {r} \mathbf {A} ^ {- 1} \mathbf {M} ^ {T}} ^ {\mathbf {R}} \left[ \begin{array}{c} \mathbf {d} _ {k} \\ \mathbf {d} _ {u} \end{array} \right] = \min _ {\boldsymbol {\tau}} \left[ \begin{array}{c} \mathbf {d} _ {k} \\ \mathbf {d} _ {u} \end{array} \right] ^ {T} \left[ \begin{array}{c c} \mathbf {R} _ {k k} & \mathbf {R} _ {k u} \\ \mathbf {R} _ {u k} & \mathbf {R} _ {u u} \end{array} \right] \left[ \begin{array}{c} \mathbf {d} _ {k} \\ \mathbf {d} _ {u} \end{array} \right]\tag{52}
$$

The augmented cost matrix is subsequently partitioned based on the indices of the fixed and free derivatives.

By differentiating J and setting it to zero, the vector of optimal values for the free derivatives can be obtained in terms of the fixed or specified derivatives and the cost matrix. The equation representing this relationship is as follows:

$$
\mathbf {d} _ {u} ^ {*} = - (\mathbf {R} _ {u u} ^ {T} + \mathbf {R} _ {u u}) ^ {- 1} \big (\mathbf {R} _ {k u} ^ {T} + \mathbf {R} _ {u k} \big) \mathbf {d} _ {k}\tag{53}
$$

Subsequently, the optimal control points for a specific time allocation can be computed using the following equation:

$$
\overline {{\pmb {\rho}}} ^ {*} = \mathbf {A} ^ {- 1} \mathbf {M} ^ {T} \left[ \begin{array}{c} \mathbf {d} _ {k} \\ \mathbf {d} _ {u} ^ {*} \end{array} \right]\tag{54}
$$

The configuration of the control points remains unaltered irrespective of the scaling in the time allocation since the time variable does not contribute to the integral cost for an independent Bezier segment. To determine the optimal arrangement of control points, the total sum of allocated times is constrained to unity, represented as $\begin{array} { r } { \tau _ { n } = ( \tau _ { 0 } , \tau _ { 1 } , \dots , \tau _ { m - 2 } , 1 - \sum _ { k = 0 } ^ { m - 2 } \tau _ { k } ) } \end{array}$ ensuring that every time allocation value is consistently positive. This procedure is repeated in the actuator space

## 4.4. Optimal Time Trajectory

Since the optimized trajectory is parametrized within the range of t [0, 1], regardless of the scale of the solution, the resulting trajectories may not always be feasible. To address this, a secondary optimization is conducted to determine the optimal total flight time that adheres to the actuator constraints imposed by the mechanism. The cost function $\mathbf { J } _ { \mathrm { T } } ,$ representing the total flight time, can be formulated as a constrained optimization problem, subjected to tangential and axial kinematic constraints as shown below:

$$
\begin{array}{l} \mathbf {J} _ {T} = \underset {k} {\min} \quad \mathbf {J} (k \tau), \\ \text {s.t} \quad \left\{ \begin{array}{l l} | \ddot {s} | <   a _ {\max}, & | \ddot {s} | <   j _ {\max} \\ | \ddot {d} | <   a _ {d _ {\max}} & | \dddot {d} | <   j _ {d _ {\max}} \end{array} \right. \end{array}\tag{55}
$$

The optimization problem can be solved using nonlinear optimization methods such as interior point or active set methods. In this particular study, the open source NLopt C++ library is utilized to solve equation (55).

## 4.5. Actuator space layer interpolation

In order to determine the spatial position of the tool during each interpolation period and the corresponding length of the traversed path, a series of calculations are performed. Initially, the B-spline curve parameter is computed, which allows for the determination of the B-spline curve position. If there are changes in the spatial orientation of the tool, the imaginary part of the unit quaternions is calculated, and subsequently, the quaternion path is derived. Finally, the obtained quaternions are transformed back to Euler angles, providing the position and spatial orientation of the tool relative to the vector P, at time t. The inverse kinematics is then employed to obtain the displacement vector for the actuators.

Subsequently, the minimum snap/jerk trajectory generation method, previously discussed for the task space, is further extended to the actuator space. This entails determining the coefficients of the polynomials that describe the motion of the actuators. Once the coefficients are obtained, they are transmitted to the microprocessor during each interpolation interval, facilitating the generation of the requisite pulses for the accurate movement of the motors.

The proposed trajectory-generation framework consists of two main computational stages: (1) offline preprocessing, which includes numerical integration for position interpolation, nonlinear optimization for orientation interpolation, and time-optimal trajectory generation; and (2) real-time execution, where precomputed coefficients are used for efficient interpolation.

The offline preprocessing stage, which is executed once per trajectory, requires a total computation time of approximately 5 seconds for a trajectory consisting of 300 waypoints, broken down as follows: position interpolation via numerical integration (\~3.3 sec), orientation interpolation via nonlinear optimization (\~0.4 sec), and minimum jerk time optimal trajectory generation (\~0.4 sec).

The real-time execution stage is computationally efficient due to precomputed coefficients. The total time per real-time interpolation step is approximately 65 µs, making the proposed method highly suitable for real-time industrial robotic applications.

## 5. Results and Discussion

Figure 6 presents the motion unit’s configuration, which comprises four distinct components: a graphical user interface (GUI), microprocessors, motors, and linear encoders. Within the computer system, intensive calculations such as the parametric interpolation of the tool path and motion planning in Cartesian space are executed using object-oriented C++ programming. The system ultimately produces a set of polynomial coefficients that define the motion equations in actuator space. In addition, a Qt-based user interface has been developed to enable seamless hardware interaction, allowing users to perform operations such as referencing, issuing movement commands, and executing stop commands with ease.

A 32-bit ARM-based microprocessor (Arduino Due) is responsible for generating movement pulses and transmitting them to the motor drives. Furthermore, four AVR-based Arduino Mega 2560 microprocessors are deployed to receive signals from the encoders, process the data, and relay the results to the GUI. Once the digital pulses for motion and direction are received, the drivers amplify the voltage and perform the necessary processing to ensure that the motion signals are accurately transmitted to the motors, thereby enabling precise rotational movement.

The optimized C code running on the Arduino Due has achieved an interpolation loop time of 55 microseconds, approaching real-time performance. All tool path generation and trajectory optimization are carried out on a PC (ASUS N43sn laptop, 2nd generation 2.2 GHz CPU). The piecewise trajectory polynomial coefficients for all joint space segments are stored in a lookup table and transmitted to the microcontroller via UDP communication; the only online operation is the calculation of the next step at each timer interrupt to drive the motor to its desired pose at the corresponding time.

The system continuously monitors incoming data from network communications and stores the received data in buffers. It then generates and transmits precise digital pulses to the motor driver. To achieve this, an internal timer within the central processor, operating at a frequency of 84 MHz, is employed. This timer triggers system interrupts for brief durations during which all computations related to pulse generation and transmission are executed within a dedicated function. Rigorous benchmarking determined that the total time required to calculate the displacement of four motors using eighth-degree polynomials is at least 55 microseconds. To accommodate additional processor tasks between interrupts, a slight temporal buffer of a few extra microseconds is incorporated. Consequently, the interrupt timer is set to 65 microseconds, yielding 0.4 MHz in algorithm frequency.

![](Akhbari2026Smooth_figs/01114167db32c9728aad7f917bd735b883622c725e01f81949748927b51f9f98.jpg)  
Fig.6. Motion generation unit: (a) schematic overview (b) real-world implementation.

The initial test involved a fan-shaped tool path comprising 89 data points, which were subsequently scaled to an approximate size of 125 (mm) by 125 (mm). As depicted in part (a) of Figure 7, a 5th degree B-spline curve was fitted to these data points using the methodology outlined in the preceding section. The resulting tool path exhibited a total length of 568.268 (mm). Examination of the curvature graph plotted against the curve parameter, as presented in part (b) of Figure 7, revealed the presence of four sharp corners within the tool path. Subsequently, a comparative analysis was conducted to assess the performance of the interpolation and trajectory generation method proposed in this research. In this study, two distinct performance indices related to trajectory smoothness and accuracy are explicitly defined and analyzed. First, feed-rate fluctuation explicitly refers to sudden or rapid variations of instantaneous feed-rate over short periods. Such fluctuations are quantitatively characterized by peak jerk values, Root Mean Square (RMS), and standard deviation of higher-order derivatives (such as jerk). Large fluctuations represent abrupt and frequent feed-rate changes, which cause mechanical vibrations, increased actuator stress, and reduced motion precision. Second, the term feed-rate deviation (tracking error) explicitly indicates the instantaneous absolute difference between actual feed-rate values measured experimentally through encoder data and direct kinematics, and analytically calculated ideal feed-rates. This second metric primarily reflects how accurately the trajectory execution adheres to the ideal planned trajectory.

To facilitate this analysis, motion planning was conducted employing the minimum jerk approach and a maximum speed of 20 (mm/s), with a maximum acceleration of 300 (mm/s<sup>2</sup>).

![](Akhbari2026Smooth_figs/965c667aa5af72db5dd9dd8b90747e1c05e294c4c2a3aa6195ae7480c742705f.jpg)

![](Akhbari2026Smooth_figs/5687bc76a5530381e8a29bd214581ad6ebea71f3b8370a3ee76bc69a29a48796.jpg)  
Fig.7. (a) Fan-shaped B-spline path, (b) curvature variation against curve parameter.

In order to quantitatively demonstrate the effectiveness of the proposed optimal trajectory generation method, Figure 8 presents a comparison between the optimized time-optimal minimum-jerk trajectory and a conventional piecewise polynomial trajectory of identical polynomial degree (7th degree). The comparisons are shown through three key motion metrics: feed-rate, acceleration, and jerk. As observed from Figure 8(a) and further supported by statistical analysis, the optimized trajectory significantly reduces feed-rate fluctuations, with peak feed-rate decreasing by approximately 73.4% (from 70.70 mm/s to 18.84 mm/s) compared to the non-optimal trajectory. Furthermore, the optimized method yields a 79.7% reduction in feed-rate standard deviation (from 13.55 mm/s to 2.76 mm/s), indicating a consistently smoother speed profile throughout the trajectory.

Acceleration profiles, shown in Figure 8(b), illustrate even greater improvements. The optimized trajectory achieves an 88.6% reduction in peak acceleration (from 260.16 mm/s² down to 29.65 mm/s²) and an 89.8% reduction in both RMS and standard deviation values (from 51.71 mm/s² to 5.30 mm/s²). Such considerable reductions directly translate to diminished mechanical stress, reduced vibrations, and increased trajectory tracking precision. Figure 8(c) emphasizes jerk, a critical indicator of motion smoothness, illustrating the most substantial improvement. Peak jerk is reduced by 95.7% (from 1793.82 mm/s³ to 77.84 mm/s³) in the optimized method. Additionally, jerk RMS and standard deviation both show reductions of approximately 95.0% (from 311.04 mm/s³ to 15.61 mm/s³), confirming drastically smoother acceleration transitions.

Collectively, these statistical outcomes clearly substantiate the practical superiority of the optimized trajectory generation approach. By achieving substantially lower peak values, RMS magnitudes, and variations in jerk, acceleration, and feed-rate, the proposed method effectively balances fast execution with minimal dynamic disturbances. This leads to improved mechanical stability, enhanced surface finish quality, decreased machine wear, and potentially reduced energy consumption in manufacturing and robotic machining processes.

Regarding computational efficiency, the proposed optimal trajectory-generation approach, demonstrates highly favorable computational complexity. Traditional dense polynomial trajectory optimization algorithms exhibit cubic complexity $( O ( n ^ { 3 } )$ . However, by adopting a sparse unconstrained quadratic-programming formulation with optimized sparse linear algebra routines, the proposed method significantly reduces practical complexity to approximately quadratic $( O ( n ^ { 3 } )$ . For example, benchmarks clearly illustrate solution times of approximately 0.34 ms for a 3-segment trajectory using C++/Eigen dense solvers. Extending these benchmarks explicitly to a larger scenario involving, for instance, 300 waypoints (\~100 polynomial segments), would naively lead to approximately a 100-fold increase in complexity. This would yield an estimated computational time of around 340 ms, maintaining excellent scalability and feasibility for robotic applications. Furthermore, due to the offline calculation and storage of polynomial coefficients, the real-time computational overhead per interpolation step is minimal (on the order of 65 µs per step on the micro-controller side), explicitly reinforcing the real-time suitability of this method.

To evaluate the effectiveness of the proposed interpolation method presented in this article, an assessment was conducted by comparing the obtained results with the direct kinematic output from encoders. Table.1 lists the feed-rate, acceleration, and jerk values derived from the analytical relations, juxtaposed with the corresponding experimental values obtained from application of direct kinematics to encoder data. In the respective sections of this table, the outcomes obtained from natural interpolation methods, Taylor expansion of first-order and second-order, as well as modifier polynomials with varying tolerances of least square error (specifically, 1e-8, 1e-10, and 1e-12), have been listed. This comparison provides insights into the performance of the proposed interpolation method in relation to these alternative approaches.

(a)  
![](Akhbari2026Smooth_figs/0218cfd8a447482d8e683e405104408e5a103c8a07d5a151ac7dc0eab4eea068.jpg)  
(c)

![](Akhbari2026Smooth_figs/0a23cb6a24bfbfee42f2e6794bd11671c18f4535f7661bf9a5b067a87696d428.jpg)

![](Akhbari2026Smooth_figs/2a14ed7253b1366dd086c78ae0fa6168e9e7d3e2178c49bf35b64b7990fd4812.jpg)  
Fig.8. comparison of presented optimum and general piece-wise non-optimal trajectory for 7th degree

Bezier Curves: (a) Feed-rate, (b) Acceleration, (c) Jerk.

Based on Table 1, it is evident that the natural interpolation method exhibits significant feed-rate fluctuations. Consequently, the maximum feed-rate during path travel exceeds the predetermined limit, reaching approximately 30 (mm/s). Moreover, the maximum deviation from the ideal feed-rate is approximately 12 (mm/s), with an average fluctuation of 4.6 (mm/s) during motion. This behavior arises due to the assumption of a linear relationship between the curve parameter and a fraction of the path length in the natural interpolation method, which fails to account for the non-linear relationship between the path length and the parameter of the B-spline curve. As discussed in Section 3, achieving a perfectly linear relationship between displacement and curve parameter is only possible for straight lines without any curvature. Consequently, part (b) of Figure 7 demonstrates that the presence of curvature and significant changes in curvature renders the natural interpolation method inaccurate for free-form curves. Furthermore, the actual acceleration and jerk using the natural interpolation method deviates significantly from the ideal state. The observed large sudden changes in acceleration and jerk can be attributed to the assumption of a linear relationship between the curve parameter and the path length in the natural interpolation method, which fails to capture the higher-order continuity of the curve parameter with respect to the path length.

Table.1. Comparative analysis of interpolation methods based on motion indices. The table summarizes the absolute deviations of feed-rate, acceleration, and jerk from their ideal values, as well as the computation time for each interpolation method.

<table><tr><td rowspan="2">Interpolation Method</td><td colspan="2">Feed-rate deviation (mm/sec)</td><td colspan="2">Acceleration deviation (mm/sec $^2$ )</td><td colspan="2">Jerk deviation (mm/sec $^3$ )</td></tr><tr><td>max</td><td>mean</td><td>max</td><td>mean</td><td>max</td><td>mean</td></tr><tr><td>Natural</td><td>11.852</td><td>4.467</td><td>38.047</td><td>8.808</td><td>115.554</td><td>30.930</td></tr><tr><td>1st Taylor&#x27;s</td><td>2.755</td><td>0.568</td><td>14.955</td><td>2.065</td><td>91.953</td><td>9.722</td></tr><tr><td>2nd Taylor&#x27;s</td><td>1.648</td><td>0.137</td><td>4.490</td><td>0.630</td><td>41.477</td><td>4.230</td></tr><tr><td>Modifier polys  $ε_{MSE}=1e-8$ </td><td>0.809</td><td>0.064</td><td>3.300</td><td>0.387</td><td>37.582</td><td>2.833</td></tr><tr><td>Modifier polys  $ε_{MSE}=1e-10$ </td><td>0.676</td><td>0.047</td><td>3.277</td><td>0.300</td><td>35.134</td><td>2.514</td></tr><tr><td>Modifier polys  $ε_{MSE}=1e-12$ </td><td>0.642</td><td>0.037</td><td>2.932</td><td>0.236</td><td>20.791</td><td>1.867</td></tr></table>

Regarding the first-order Taylor expansion interpolation method, referring to the results listed in Table 1 show a notable improvement compared to the natural interpolation method in terms of reducing the deviation of feed-rate from the ideal values. Fluctuations in feed-rate are observed primarily in four regions characterized by sharp corners, attributed to the high curvature of the curve within these zones. The impact of curvature on the fluctuations is expected, as the curve's slope varies significantly in high curvature points, resulting in inaccurate approximation of the curve parameter with respect to the path length. In the first-order Taylor expansion method, the curve parameter is assumed to have a linear relationship with the first-order derivative of the path length function, disregarding higher-order derivatives. Consequently, round-off errors, as well as substantial errors in approximating the curve parameter in regions with large second derivatives (i.e., higher curvature), lead to feed-rate fluctuations. An additional drawback of the first-order Taylor expansion method is its time-consuming nature, as it requires analytical calculations of the first-order derivative of the B-spline curve in each interpolation cycle. Results from the second-order Taylor expansion method, listed in Table 1, exhibits significant improvement in the proximity of the actual feed-rate to the ideal value. However, the lack of high-order continuity boundary conditions between the segments and cumulative rounding errors leads to feed-rate fluctuations. Despite the improved smoothness and proximity to the ideal state compared to the firstorder expansion method, the computation time for the second-order Taylor expansion method is high due to the requirement of calculating the first and second-order derivatives of the curve during interpolation.

The modifier polynomial method, consistently yields superior outcomes compared to other interpolation methods. As expounded upon in Section 3, this technique leverages the analytical relationship between the path length and the integral of the first-order derivative of the underlying B-spline curve. It formulates a linear optimization problem aimed at minimizing the least squared error between the estimated curve parameters and their ideal values, while incorporating continuity boundary conditions of at least third order. The resulting algorithm generates coefficients for multiple ninth-degree polynomials, each approximating the curve parameter within a specific interval during each interpolation period, based on the known path length. The number of polynomials utilized depends on the specified tolerance for the least squares error. As the approximate curve parameter aligns more closely with the ideal value, variations in the path length, calculated via motion relationships derived from minimized jerk, increasingly match the patterns of motion curves, resulting in minimal feed-rate oscillations along the path. As the tolerance for the least squares error tightens the actual motion curves follow the desired trend more closely. The modifier polynomial interpolation method, employing a tolerance of $\varepsilon _ { M S E } = 1 e - 8$ using 1655 path length data obtained from Simpson's integral, 31 piecewise polynomials are obtained. even with a tolerance of $1 \mathrm { e } { \cdot } 8 .$ , this interpolation method exhibits smoother motion than the second-order Taylor expansion method. Further reduction in the least squares error tolerance leads to enhanced quality and smoothness of the motion curves. The corresponding number of polynomials for these tolerances is 33 and 63, respectively. Another advantageous aspect of the modifier polynomial method, compared to Taylor expansion approaches, lies in computation time. Since the modifier polynomial coefficients are preprocessed and stored in tables, the interpolation process experiences significant reduction in calculation time, estimated to be around 65 us for Atmel SAM3X8E ARM Cortex-M3.

![](Akhbari2026Smooth_figs/2f615f8b6ac7ffe404c2d63a372a7728637c78ce7da3afd34f8ba528cd1cbc78.jpg)

![](Akhbari2026Smooth_figs/be9ccc049e21e4132e9e1c857bb6885faad804a4a9e54a1552e5aaf64a8f6d11.jpg)

![](Akhbari2026Smooth_figs/6ff3df57276cd4f5d8e3d95b3af1195fe59b7ee5119cc793ec3e02c462d5a860.jpg)

![](Akhbari2026Smooth_figs/c8ebe215dc2d3d9580478ada75ae9c163f3f8187e7c0cea62791e7d90418239d.jpg)

(e)  
![](Akhbari2026Smooth_figs/ea99265f6c9927a4ac63c791ea869f01f4c79d41cb2cfeead9c03a9b4f4d8cef.jpg)

![](Akhbari2026Smooth_figs/41e78492991abd013e06df901dcc926d6860a3fb5b24af33332806fdb7bedcee.jpg)  
Fig.9. comparison of ideal and actual motion profiles for end-effector in cartesian space: (a) x axis feed-rate, (b) y axis feed-rate, (c) x axis acceleration, (d) y axis acceleration, (e) x axis jerk, (f) y axis jerk.

Figure 9 presents a comparison between the desired (planned) trajectories and actual (measured) trajectories obtained via direct kinematic calculations using encoder data. It can be clearly observed that the actual trajectories closely follow the desired profiles, confirming the high accuracy and reliability of the proposed interpolation method. However, subtle deviations occur, especially in regions associated with sharp directional changes or significant curvature variations. These slight deviations between planned and actual paths arise primarily from inherent numerical approximations and limited dynamic response of the robotic system in real-time execution.

![](Akhbari2026Smooth_figs/9a76fc3d8bbd7a7e9c6c8f6576cfad1d9cca0843d886cd99142f0eda29d64435.jpg)

![](Akhbari2026Smooth_figs/1cc383ddf87507ef04a7fa66c3cad81a52336c9b469a1e4a6282bc3df42e239c.jpg)

![](Akhbari2026Smooth_figs/1e97728900c1f63db5c95c9759de33ba0128815fd0b8c5d1085864daab5e5f6c.jpg)  
Fig.10. Resultant actual motion profiles for joint space via the presented optimal time minimum jerk trajectory generation: (a) velocity, (b) acceleration, (c) jerk.

To further investigate these deviations, Figure 10 explicitly depicts the corresponding joint-space profiles, including velocity, acceleration, and jerk, for each joint. Although the Cartesian-space trajectories appear generally smooth and close to the desired trajectory, the joint-space results illustrate clear dynamic complexities. Specifically, joints frequently change directions, driven by the nonlinear mapping of Cartesian-space paths to joint angles through inverse kinematics. As the robot end-effector moves smoothly along the planned Cartesian path, individual joints must continually alter their velocities and directions to precisely follow toll path, inherently resulting in notable acceleration and jerk spikes. These joint-level dynamic variations are primarily a consequence of nonlinear mapping from Cartesian to joint space, as joint axes constantly reorient and accelerate to accommodate smooth end-effector movements.

The presence of these acceleration and jerk spikes at the joint level clearly underscores the necessity of explicitly constraining joint-level dynamics during trajectory planning, particularly for parallel robotic mechanisms. Nonetheless, these peaks remain within acceptable actuator and mechanical limits, validating the effectiveness of the proposed trajectory-generation method in managing axis-level dynamics explicitly.

Moreover, the machined part is illustrated in part (a) of Figure 11. Data points from the machined curve were extracted using a profile projector device, as depicted in part (b) of Figure 11. By selecting a reference point, 200 points were extracted from both the outer and inner edges of the machined curve. To reconstruct the path, a B-spline curve was fitted to these data points by taking the median, following the procedure described in Section 3. The results, as shown in parts (a) and (b) of Figure 12, indicate that despite compensating for the movement error of the sliders, errors of approximately hundredths of a millimeter were still observed in the x and y directions. These discrepancies may be attributed to various factors, including errors caused by the expansion coefficient of rails, joints, arms, and clearance between the arms.

(a)  
![](Akhbari2026Smooth_figs/b703b8b5ace2e1d98c7713df4d3d92d175e2255032a2d8e2a078696240c803e2.jpg)

(b)  
![](Akhbari2026Smooth_figs/485c3bdc29de26ceeb6e0f2f554340afc959277771fccd89d816a24a57c5fd7a.jpg)  
Fig.11. (a) A visual representation of the machined freeform fan-shaped tool path, and (b) An illustration of the curve profile measurement setup using the projector profile device.

![](Akhbari2026Smooth_figs/629d3b3c519b98f8eca79c049a170e71dff7fa72670618d904a996d1fddac544.jpg)

![](Akhbari2026Smooth_figs/4f15c48c6b90e251a3c2aa2e577b443c88be3b3bc2536bf57af7db6c146ed2a8.jpg)  
Fig.12. The error arising from the disparity between experimental and simulation data for the fanshaped machined part: (a) along the x-axis, and (b) along the y-axis.

To validate the tool path orientation, a curved path was derived from 18 data points representing a spherical section in the y-z plane. Following the procedure detailed in Section 3, a fifth-degree B-spline curve was fitted to these data points. The resulting curve, illustrated in Figure 13, defines the tool path. Tool orientation was established by ensuring that the tool axis remained perpendicular to the path. This perpendicular vector was computed as the second derivative of the B-spline curve with respect to the geometric parameter, following the derivation presented in Equation 8. Euler angles were determined by calculating the angle between the tool's initial orientation vector and vectors perpendicular to the fitted curve. Using the improved Simpson integration method, the curve was discretized into 103 segments, resulting in a total path length of 63.511 mm. Position interpolation for the tool tip was executed using 14 piecewise-modified ninth-degree polynomials, with the interpolation tolerance set to $\varepsilon _ { M S E } = 1 e - 1 2$ , ensuring high accuracy in the approximation of the curve parameter along the path.

The tool's spatial orientation was represented by converting Euler angles into unit quaternions within a four-dimensional quaternion space. This conversion employed a fifth-degree B-spline fitting technique, as described in Subsection 3.3. Subsequently, spatial orientation was parameterized through the optimization of piecewise Bezier curves relative to arc length. To achieve smooth temporal parameterization of the path length, the trajectory generation approach described in Section 4 was utilized. Given an offline interpolation interval of 10 ms, actuator displacements were calculated via inverse kinematics. Each displacement segment underwent trajectory generation within actuator space, following the same procedure.

Upon trajectory calculation, segment data was transmitted to the microcontroller, which executed motion generation at a 65 µs interpolation cycle. After motion completion, linear and angular positions, velocities, accelerations, and jerk values of the tool were computed using direct kinematics, with encoder feedback ensuring accuracy.

![](Akhbari2026Smooth_figs/08a22f4a42352e41415a553eb291193732e4879c36fa94a1baf7ffe0cc7db787.jpg)  
Fig.13. B-spline toolpath reconstructed from point cloud, where the tool axis maintains a consistent perpendicular orientation to the path.

Figure 14 illustrates the velocity, acceleration, and jerk resulting from the motion along the tool path. The curves for velocity, acceleration, and jerk exhibit minimal deviations from their ideal counterparts due to the low curvature and small changes in curvature along the path. The maximum feed-rate deviation, as shown in part (a) of Figure 19, is 0.009 (mm/s) with an average of 0.001 (mm/s) along the path. This demonstrates the high performance of the interpolation method with modified polynomials in curved paths with low curvature. The trajectory generation with minimum jerk ensures minimal acceleration changes while satisfying continuity constraints. Consequently, a nearly uniform acceleration is achieved after the initial acceleration phase, resulting in a smooth and continuous motion. Part (b) of Figure 19 shows the maximum deviation from the ideal acceleration, which is 0.1904 (mm/s<sup>2</sup>) with an average deviation of 0.0165 (mm/s<sup>2</sup>) along the route. The acceleration curve exhibits smooth variations without sharp fluctuations, reflecting the influence of the minimum jerk trajectory profile defined by third-order continuity. Part (c) of Figure 19 displays the jerk curve obtained from the encoder feedback and direct kinematics compared to the ideal state. The maximum jerk deviation is reported as $7 . 1 2 3 ( \mathrm { m m } / \mathrm { s } ^ { 3 } )$ with an average deviation of $0 . 4 ( \mathrm { m m } / \mathrm { s } ^ { 3 } )$ along the route. The observed variations in jerk are predominantly present in areas where the curvature changes abruptly. Based on these findings and the comparison with figures 8 and 9, it is evident that the curvature of the path significantly impacts the accuracy of interpolation, with smoother motion observed for paths with lower curvature and minimal changes in curvature.

![](Akhbari2026Smooth_figs/2accd78a45dc19df78c45424116006fe4ad9895907b086626f4b89bb21b06535.jpg)

![](Akhbari2026Smooth_figs/6d54ebb811474332276e82cf2dd4db7460aa8759060de8856b08ca1a420ed378.jpg)

![](Akhbari2026Smooth_figs/62d848f6ada127baec8c13765d57e17229b56510c9407eec51722c99461299d2.jpg)  
Fig.14. comparative analysis of motion profiles for the B-spline path displayed in Figure 17, between the ideal and actual states. The depicted curves represent: (a) velocity, (b) acceleration, and (c) jerk.

By utilizing the method described in subsection 3.3, the spatial orientation of the tool was represented using quaternions. These quaternions were fitted to the B-spline curve and parameterized with the parameter w. The parameter w was further reparametrized using Bezier curves, which aimed to minimize changes in curvature compared to the path length parameter, s. Additionally, the path length was parameterized using trajectory generation method from section 4. Consequently, in each interpolation period, the quaternions representing the spatial orientation of the tool were obtained. Figure 15, part (a), illustrates these quaternions after omitting one dimension on the unit sphere. Part (b) of Figure 15 presents the variations of the real and imaginary components of the quaternions in relation to the curve parameter w. It can be observed that due to the mechanism's rotational degree of freedom around x-axis, the changes in the imaginary parts j and k are zero. Furthermore, the shape of the curve representing the variations in the quaternions closely resembles the graph (refer to Figure 8) depicting the feed-rate of the path length with respect to time. The accuracy of parametrizing the nonlinear relationship between s and w is evident in part (b) of Figure 15. Also, Figure 16 demonstrates how the curve parameter w is effectively fitted using piece-wise continuous Bezier curves with high precision.

![](Akhbari2026Smooth_figs/d7cb0766123197f9e6f2e2161da41c35acd6870249bc727dc17fdc94a51cdf2e.jpg)

![](Akhbari2026Smooth_figs/d3790ceb460dc4b6ba2bcca79c9d056aa1ee278bcb52795a5894f8a717dacd98.jpg)  
Fig.15. Visualization of tool's angular orientation quaternions: (a) Representation of the curve on the unit sphere, derived from fitting B-spline curves on the purely imaginary quaternions. (b) Variation of both imaginary and real components of the unit quaternions with respect to the curve parameter, w.

![](Akhbari2026Smooth_figs/cfffab963be4930fc5fda262f76c65c78ec1a96833ebcda98f8d0668c9ae1e52.jpg)  
Fig.16. Correlation between path length and curve parameter of tool orientation quaternions achieved through piece-wise Bezier curves optimization algorithm.

Furthermore, Figure 17 illustrates the angular velocity, angular acceleration, and angular jerk graphs resulting from encoder feedback in comparison to their ideal counterparts. The minimal deviations between the values obtained from direct kinematics and the ideal values are evident in all three parts of the figure. Specifically, from part (a) of Figure 22, the maximum deviation of angular velocity is 1.2198e-5 (deg/s) with an average of 2.3606e-7 (deg/s) along the path; from part (b) of Figure 22, the maximum deviation of angular acceleration is 8.969e-4 (deg/s<sup>2</sup>) with an average of 1.688e-5 (deg/s<sup>2</sup>) along the path; and from part (c) of Figure 17, the maximum angular jerk deviation is 0.05 (deg/s<sup>3</sup>) with an average of 0.001 (deg/s<sup>3</sup>) along the path.

An interesting observation from Figure 17 is the striking resemblance between the motion curves of the angular orientation of the tool and the tool position depicted in Figures 8 and 9. As previously mentioned in section 3, considering the absence of an analytical relationship between tool orientation and path length, the close correspondence of the motion curves obtained from direct kinematics with the ideal values highlights the success of the parametric interpolation method for the tool's spatial orientation, as described in this article. The results obtained through this method prove to be favorable and reliable.

![](Akhbari2026Smooth_figs/b4c9d3579e252efe9ba09dc9eeba9331a30812cf77625bf11d50897b5c9d2790.jpg)

![](Akhbari2026Smooth_figs/fac4afa405758c1df283dedd3d129c0f2dd6fdce9e7047b91decc5a94f0e8edf.jpg)

![](Akhbari2026Smooth_figs/9f8f76c68513c6c05938d97fa310f644d74c9313620fdd9aed9193fc02f4dda8.jpg)  
Fig.17. Comparison of angular motion curves in the ideal state and the results of encoder data and direct kinematics: (a) Depicts angular velocity, (b) shows angular acceleration, and (c) presents angular jerk.

## 6. Conclusion

This study introduced and implemented a dual-stage smooth trajectory and hybrid B-spline-Quaternion interpolation method for freeform paths in a four-degree-of-freedom multi-axis parallel kinematic milling robot. The research commenced by presenting the mechanical structure and establishing kinematic relations between the actuator and task space. Subsequently, trajectory interpolation and generation for B-spline tool paths were outlined, and a comprehensive comparison with existing interpolation methods from the literature was conducted. Moreover, position interpolation utilized modifier polynomials, while angular orientation interpolation employed unit quaternions. The synchronization of path length and spatial orientation was achieved through an optimization process employing piece-wise Bezier curves, minimizing the integral norm of geometric jerk. Further, motion planning involved solving an optimization problem for minimum jerk and time-optimal Bezier curve minimization, with the two-layer approach encompassing both task and actuator spaces, and implemented within an arm-based embedded system. Experimental validation entailed writing and executing all interpolation and motion planning steps within a C++ object-oriented programming environment, with GUI development facilitated by the Qt framework and multithreaded Ethernet communication with hardware.

In this research, several key conclusions have been drawn. Natural interpolation methods are unsuitable for highly curved or rapidly changing paths, leading to undesirable velocity oscillations, pronounced acceleration fluctuations, and uncontrollable jerk. The first-order Taylor expansion method accumulates rounding errors and struggles with sharp corners, contributing to computational inefficiency. The second-order Taylor expansion method, while better in approximating velocity, is sensitive to cumulative rounding errors and less practical for real-time applications. In contrast, modifier polynomials provide high-quality interpolation with reduced velocity fluctuations, enhanced smoothness, and computational advantages. A novel synchronization method for path length and tool orientation quaternions ensures accurate results. Overall, the developed methodology demonstrates remarkable efficiency and performance improvements in multi-axis tool path interpolation for robotic systems. By reducing velocity fluctuations and enhancing smoothness through modifier polynomials, it ensures more precise and controlled movements, particularly beneficial in applications requiring high accuracy, such as milling machines. Moreover, the synchronization method for path length and tool orientation quaternions enhances overall performance, resulting in close correspondence between actual and ideal values for velocity, acceleration, and angular jerk. This methodology's versatility and adaptability make it a valuable asset for subtractive and additive manufacturing with robots, offering potential applications across machining processes, where precise and efficient motion planning is paramount.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that

could have appeared to influence the work reported in this paper.

## Acknowledgments

None to report.

## References

[1] M.A. Isa, I. Lazoglu, Five-axis additive manufacturing of freeform models through buildup of transition layers, Journal of Manufacturing Systems, 50 (2019) 69-80

[2] S. Sun, P. Zhao, T. Zhang, B. Li, D. Yu, Smoothing interpolation of five-axis tool path with less feed-rate fluctuation and higher computation efficiency, Journal of Manufacturing Processes, 109 (2024) 669- 693.https://doi.org/10.1016/j.jmapro.2023.12.012

[3] M. Mahboubkhah, A. Barari, Design and development of a novel 4-DOF parallel kinematic coordinate measuring machine (CMM), International Journal of Computer Integrated Manufacturing, (2019) 1- 11.10.1080/0951192X.2019.1610576

[4] E. Ghanbary Kalajahi, M. Mahboubkhah, A. Barari, On detailed deviation zone evaluation of scanned surfaces for automatic detection of defected regions, Measurement, 221 (2023) 113462.https://doi.org/10.1016/j.measurement.2023.113462

[5] R.V. Fleisig, A.D. Spence, A constant feed and reduced angular acceleration interpolation algorithm for multi-axis machining, Computer-Aided Design, 33 (2001) 1-15.http://dx.doi.org/10.1016/S0010- 4485(00)00049-X

[6] Y. Liu, H. Li, Y. Wang, Realization of a 5-axis NURBS Interpolation with Controlled Angular Velocity, Chinese Journal of Aeronautics, 25 (2012) 124-130.https://doi.org/10.1016/S1000-9361(11)60370-1

[7] J.M. Langeron, E. Duc, C. Lartigue, P. Bourdet, A new format for 5-axis tool path computation, using Bspline curves, Computer-Aided Design, 36 (2004) 1219-1229.http://dx.doi.org/10.1016/j.cad.2003.12.002

[8] A. Yuen, K. Zhang, Y. Altintas, Smooth trajectory generation for five-axis machine tools, International Journal of Machine Tools and Manufacture, 71 (2013) 11-19

[9] F.C. Wang, P.K. Wright, B.A. Barsky, D.C.H. Yang, Approximately Arc-Length Parametrized C3 Quintic Interpolatory Splines, Journal of Mechanical Design, 121 (1999) 430-439.10.1115/1.2829479

[10] S.-S. Yeh, P.-L. Hsu, Adaptive-feed-rate interpolation for parametric curves with a confined chord error, Computer-Aided Design, 34 (2002) 229-237.http://dx.doi.org/10.1016/S0010-4485(01)00082-3

[11] M.C. Tsai, C.W. Cheng, M.Y. Cheng, A real-time NURBS surface interpolator for precision three-axis CNC machining, International Journal of Machine Tools and Manufacture, 43 (2003) 1217- 1227.http://dx.doi.org/10.1016/S0890-6955(03)00154-8

[12] W. Zhong, X. Luo, W. Chang, F. Ding, Y. Cai, A real-time interpolator for parametric curves, International Journal of Machine Tools and Manufacture, 125 (2018) 133- 145.https://doi.org/10.1016/j.ijmachtools.2017.11.010

[13] F. Liang, G. Yan, F. Fang, Global time-optimal B-spline feed-rate scheduling for a two-turret multi-axis NC machine tool based on optimization with genetic algorithm, Robotics and Computer-Integrated Manufacturing, 75 (2022) 102308.https://doi.org/10.1016/j.rcim.2021.102308

[14] S. Ji, L. Lei, J. Zhao, X. Lu, H. Gao, An adaptive real-time NURBS curve interpolation for 4-axis polishing machine tool, Robotics and Computer-Integrated Manufacturing, 67 (2021) 102025.https://doi.org/10.1016/j.rcim.2020.102025

[15] M. Chen, W.-S. Zhao, X.-C. Xi, Augmented Taylor's expansion method for B-spline curve interpolation for CNC machine tools, International Journal of Machine Tools and Manufacture, 94 (2015) 109-

119.http://dx.doi.org/10.1016/j.ijmachtools.2015.04.013

[16] K. Erkorkmaz, Y. Altintas, Quintic spline interpolation with minimal feed fluctuation, Journal of manufacturing science and engineering, 127 (2005) 339-349

[17] M. Liu, Y. Huang, L. Yin, J. Guo, X. Shao, G. Zhang, Development and implementation of a NURBS interpolator with smooth feed-rate scheduling for CNC machine tools, International Journal of Machine Tools and Manufacture, 87 (2014) 1-15.http://dx.doi.org/10.1016/j.ijmachtools.2014.07.002

parallel kinematic machines, Robotics and Computer-Integrated Manufacturing, 57 (2019) 347- 356.https://doi.org/10.1016/j.rcim.2018.12.013

[19] J. Yang, Y. Chen, Y. Chen, D. Zhang, A tool path generation and contour error estimation method for fouraxis serial machines, Mechatronics, (2015).http://dx.doi.org/10.1016/j.mechatronics.2015.03.001

[20] S. Zhang, Z. Shi, Y. Ding, Toolpath smoothing with reduced curvature and synchronized motion for hybrid robots, Journal of Manufacturing Processes, 109 (2024) 181-197.https://doi.org/10.1016/j.jmapro.2023.12.002

[21] E. Kelekci, S. Kizir, A novel tool path planning and feed-rate scheduling algorithm for point to point linear and circular motions of CNC-milling machines, Journal of Manufacturing Processes, 95 (2023) 53- 67.https://doi.org/10.1016/j.jmapro.2023.04.003

[22] L. Hua, Y. Zhao, J. Zhou, Y. Zhang, N. Huang, L. Zhu, Five-axis toolpath interpolation method with kinematic corner smoothing and time synchronization, Journal of Manufacturing Processes, 105 (2023) 338- 358.https://doi.org/10.1016/j.jmapro.2023.09.048

[23] R.A. Osornio-Rios, R. de Jesus Romero-Troncoso, G. Herrera-Ruiz, R. Castañeda-Miranda, Computationally efficient parametric analysis of discrete-time polynomial based acceleration–deceleration profile generation for industrial robotics and CNC machinery, Mechatronics, 17 (2007) 511- 523.http://dx.doi.org/10.1016/j.mechatronics.2007.05.004

[24] Z. Shen, Y. Wu, P. Guo, H. Zhang, P. Zhang, H. Li, F. Lou, Convolution synchronous smoothing for tool position and posture of continuous line-segment path in 5-axis machining, Journal of Manufacturing Processes, 112 (2024) 136-149.https://doi.org/10.1016/j.jmapro.2024.01.012

[25] J. Huang, L.-M. Zhu, Feed-rate scheduling for interpolation of parametric tool path using the sine series representation of jerk profile, Proceedings of the Institution of Mechanical Engineers, Part B: Journal of Engineering Manufacture, 231 (2017) 2359-2371.10.1177/0954405416629588

[26] Y. Wang, D. Yang, R. Gai, S. Wang, S. Sun, Design of trigonometric velocity scheduling algorithm based on pre-interpolation and look-ahead interpolation, International Journal of Machine Tools and Manufacture, 96 (2015) 94-105.http://dx.doi.org/10.1016/j.ijmachtools.2015.06.009

[27] S. Tajima, B. Sencer, Online interpolation of 5-axis machining toolpaths with global blending, Internationa Journal of Machine Tools and Manufacture, 175 (2022)

103862.https://doi.org/10.1016/j.ijmachtools.2022.103862

[28] W. Fan, X.-S. Gao, C.-H. Lee, K. Zhang, Q. Zhang, Time-optimal interpolation for five-axis CNC machining along parametric tool path based on linear programming, The International Journal of Advanced Manufacturing Technology, 69 (2013) 1373-1388.10.1007/s00170-013-5083-x

[29] D.-N. Song, D.-W. Zheng, Y.-G. Zhong, J.-W. Ma, J.-S. Li, Non-isometric dual-spline interpolation for five-axis machine tools by FIR filtering-based feed-rate scheduling using pseudo curvature under axial drive constraint, Journal of Manufacturing Processes, 79 (2022) 827-843.https://doi.org/10.1016/j.jmapro.2022.05.023

[30] K. Erkorkmaz, Q.-G. Chen, M.-Y. Zhao, X. Beudaert, X.-S. Gao, Linear programming and windowing based feed-rate optimization for spline toolpaths, CIRP Annals, 66 (2017) 393-

396.https://doi.org/10.1016/j.cirp.2017.04.058

[31] A. Gasparetto, V. Zanotto, A technique for time-jerk optimal planning of robot trajectories, Robotics and Computer-Integrated Manufacturing, 24 (2008) 415-426.http://dx.doi.org/10.1016/j.rcim.2007.04.001

[32] J. Huang, P. Hu, K. Wu, M. Zeng, Optimal time-jerk trajectory planning for industrial robots, Mechanism and Machine Theory, 121 (2018) 530-544.https://doi.org/10.1016/j.mechmachtheory.2017.11.006

[33] J. Xiao, S. Liu, H. Liu, M. Wang, G. Li, Y. Wang, A jerk-limited heuristic feed-rate scheduling method based on particle swarm optimization for a 5-DOF hybrid robot, Robotics and Computer-Integrated Manufacturing, 78 (2022) 102396.https://doi.org/10.1016/j.rcim.2022.102396

[34] S. Akhbari, M. Mahboubkhah, A. Gadimzadeh, Linear motion analysis for a novel 4-DOF parallel kinematic machine, Journal of the Brazilian Society of Mechanical Sciences and Engineering, 41 (2019) 428.10.1007/s40430-019-1927-0

[35] S. Akhbari, M. Mahboubkhah, D. Karimi, A. Barari, Experimental and analytical evaluation of tool path error using computer integrated nonlinear kinematical modeling for a 4DOF parallel milling machine, International Journal of Computer Integrated Manufacturing, (2021) 1-29.10.1080/0951192X.2021.1925968 [36] K. Qin, General matrix representations for B-splines, Visual Comp, 16 (2000) 177- 186.10.1007/s003710050206