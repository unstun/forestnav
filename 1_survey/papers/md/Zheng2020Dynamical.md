---
citation_key: Zheng2020Dynamical
arxiv_id: 2012.14576
arxiv_url: "https://arxiv.org/abs/2012.14576"
title: "Dynamical Systems based Obstacle Avoidance with Workspace Constraint for Manipulators"
authors_short: "Dake Zheng et al."
year: 2020
direction_tag: C_elastic_band
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:48:26Z
origin: ai+web
reviewed: false
---

# Dynamical Systems based Obstacle Avoidance with Workspace Constraint for Manipulators

Dake Zheng<sup>1,</sup> <sup>2</sup>, Xinyu Wu<sup>1</sup>, and Jianxin Pang<sup>2</sup>

(dake.zheng@ubtrobot.com, xy.wu@siat.ac.cn, and walton@ubtrobot.com)

Abstract— In this paper, based on Dynamical Systems (DS), we present an obstacle avoidance method that take into account workspace constraint for serial manipulators. Two modulation matrices that consider the effect of an obstacle and the workspace of a manipulator are determined when the obstacle does not intersect the workspace boundary and when the obstacle intersects the workspace boundary respectively. Using the modulation matrices, an original DS is deformed. The proposed approach can ensure that the trajectory of the manipulator computed according to the deformed DS neither penetrate the obstacle nor go out of the workspace. We validate the effectiveness of the approach in the simulations and experiments on the left arm of the UBTECH humanoid robot.

## I. INTRODUCTION

It is well known that each serial manipulator has a corresponding workspace, therefore the given trajectory of its end-effector must be within the workspace. In practice, manipulators often work with other agents and objects, e.g. bottles, human workers and other manipulators. The agents and objects can be referred to as obstacles. When an obstacle appears on the given trajectory, the manipulator can not track the original trajectory anymore. A new trajectory needs to be computed to avoid the obstacle. In addition, the newly computed trajectory must be in the workspace.

Obstacle avoidance has been studied for a long time in robotics, and many methods have been proposed. Generally, those methods can be divided into two categories, i.e. the global approaches and the local approaches. Local approaches such as the vector field histogram [1] and the curvaturevelocity method [2] can avoid the obstacles rapidly. However, those methods are usually locally optimal, they may fail to get a feasible path.

Global approaches such as the probabilistic roadmaps method [3] and the rapidly exploring random tree method [4] avoid obstacles by using path planning algorithms. Those methods can always find a collision-free path even in very complex scenarios. Although it is possible to parallelise the algorithms, the computational costs of the global path searches for those methods are still very heavy. Therefore, those methods cannot be applied to real-time obstacle avoidance [5].

In order to achieve real-time obstacle avoidance, several methods have been proposed. In the presence of obstacles, the elastic band approach [6, 7] deforms the original path by applying repulsive forces to get a new collision-free path. A reactive motion planning approach is proposed in [8], during the execution of a task, this approach avoids obstacles by re-planning and deforming the original path.

Khatib [9] proposes the artificial potential field method. Based on this method, Park et al. [10] propose the dynamic potential field methods, Iossifidis and Schöner [11] propose the attractor dynamics approach, Sprunk et al. [12] propose a kinodynamic trajectory generation method, etc. The artificial potential field method models each obstacle with a repulsive force to avoid collision between the robot and the obstacle. The repulsive force should be well defined to avoid local minima. To overcome the limitations of the potential field methods, the harmonic potential methods [13, 14] are proposed and widely used [15]. This approach is inspired by the description of the dynamics of fluids around impenetrable obstacles.

Similar to the harmonic potential functions method, Khansari Zadeh et al. [16] propose the dynamical systems (DS) based method recently. A trajectory can be computed according to an original DS. In the presence of obstacles, the original DS is deformed by a modulation matrix of the obstacles, then, a new trajectory that can avoid the obstacles is computed according the deformed DS. Compared to the harmonic potential functions method, the DS based method does not have to follow harmonic functions so it can be applied more widely. Huber et al. [17] extend out the DS based approach and propose an approach to avoid multiple concave obstacles. However, the approach is proposed under the assumption that the original DS is linear, therefore, the application of the approach is limited.

Since manipulators usually require real-time obstacle avoidance, hence the DS based method is a good choice for the obstacle avoidance of manipulators. As stated above, a manipulator must work in its workspace, however, few current obstacle avoidance methods take into account the workspace constraint. Therefore, the trajectories computed by the current methods may tend to go out of the workspace, then the manipulators will not work properly. For a serial manipulator, in order to get obstacle avoidance in the workspace of the manipulator, we extend out the work in [16] and propose a DS based approach.

## II. PROBLEM FORMULATION

Fig.1(a) illustrates the left arm of the UBTECH humanoid robot tracks a trajectory computed from a modulated DS proposed in [16]. The DS is obtained by applying an obstacle modulation matrix to an original DS, and is used to avoid the obstacle. Suppose the original trajectory computed from the original DS is in the workspace of the arm. The blue point cloud represents the workspace. When the obstacle is placed in the current position, the trajectory computed from the modulated DS goes out of the workspace, although it avoids the obstacle. Since part of the trajectory is out of the workspace, hence, the arm will fail to track the trajectory and will cause some damage.

![](Zheng2020Dynamical_figs/c6c5a984681c5aede67aa76fc054f8f5632575ce9771374aa097d9fe91ac70f7.jpg)  
(a)

![](Zheng2020Dynamical_figs/e1bc6f158fd30f4af2181d29246f8ad2ad406f3e462c76a7ee6a28fdc365eec3.jpg)  
(b)  
Figure 1. A manipulator tracking a DS based trajectory.

For the above problem, a method will be proposed to ensure that the DS based trajectory neither go out of the workspace nor penetrate the obstacle. Fig.1(b) shows a simplified model of the problem. For simplicity, a spherical workspace and a convex obstacle are considered in this paper.

## III. OBSTACLE-AVOIDANCE ALGORITHM

Consider a serial manipulator in Fig.1(b), we denote a state variable $\xi$ as the translational position of the end-effector of the manipulator. A DS based trajectory for the end-effector can be computed according to:

$$
\dot {\xi} = f (\xi), f: \mathfrak {R} ^ {3} \mapsto \mathfrak {R} ^ {3}\tag{1}
$$

where $f ( \cdot )$ is a continuous function. Given a start position $\{ \xi \} _ { 0 }$ , the trajectory of the end-effector can be computed along time according to:

$$
\{\xi \} _ {t} = \{\xi \} _ {t - 1} + f (\{\xi \} _ {t - 1}) \Delta t\tag{2}
$$

where is a positive integer and is the integration time step.

In this paper, we suppose the original DS given by Eq.(1) is a three-dimensional globally asymptotically stable and converges to a point $\xi ^ { * }$ , i.e. $f ( \xi ^ { * } ) = 0$ , in the workspace.

![](Zheng2020Dynamical_figs/66b614f455d885eb71d91bbc8d899cc08863111c644d997578e263d4086f5b0f.jpg)  
Figure 2. Illustration of the workspace boundary.

## A. Convex Obstacle and Workspace

As shown in Fig.1(b), the workspace boundary and the obstacle surface are convex. $\xi _ { o } ^ { c }$ and $\xi _ { w } ^ { c }$ represent the obstacle center and the workspace boundary center, respectively. Define $\widetilde { \pmb { \xi } } _ { o } = \pmb { \xi } - \pmb { \xi } _ { o } ^ { c }$ and $\widetilde { \pmb { \xi } } _ { w } = \pmb { \xi } - \pmb { \xi } _ { w } ^ { c }$ , then, the obstacle surface and the workspace boundary can be described by the two three-dimensional ellipsoids, respectively, as follows:

$$
\Gamma_ {o} (\widetilde {\xi} _ {o}) \colon \sum_ {i = 1} ^ {3} ((\widetilde {\xi} _ {o}) _ {i} / a _ {i} ^ {o}) ^ {2 p _ {o}} = 1\tag{3}
$$

$$
\Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}): \sum_ {i = 1} ^ {3} ((\widetilde {\boldsymbol {\xi}} _ {w}) _ {i} / a _ {i} ^ {w}) ^ {2 p _ {w}} = 1\tag{4}
$$

where functions $T _ { o } ( \tilde { \xi } _ { o } )$ and $T _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ are continuous distance functions and have first order partial derivatives and increases monotonically with $\left\| \widetilde { \xi } _ { o } \right\|$ and $\left\| \tilde { \xi } _ { w } \right\|$ , respectively. () represents the element value of a vector $\mathbf { ( \cdot ) } ~ . ~ a _ { i } ^ { o }$ and $a _ { i } ^ { w }$ are the axis lengths of the obstacle and the workspace boundary, respectively. $p _ { o }$ and $p _ { w }$ are positive integers.

As in [16], the functions $T _ { o } ( \tilde { \xi } _ { o } )$ and $T _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ can divide the obstacle and the workspace into exterior, boundary and interior regions, respectively, according to:

$$
\left\{ \begin{array}{l} \boldsymbol {\chi} _ {o} ^ {e} = \{\boldsymbol {\xi} \in \Re^ {3}: \Gamma_ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) > 1 \} \\ \boldsymbol {\chi} _ {o} ^ {b} = \{\boldsymbol {\xi} \in \Re^ {3}: \Gamma_ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) = 1 \}, \\ \boldsymbol {\chi} _ {o} ^ {i} = \{\boldsymbol {\xi} \in \Re^ {3}: \Gamma_ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) <   1 \} \end{array} \right. \left\{ \begin{array}{l} \boldsymbol {\chi} _ {w} ^ {e} = \{\boldsymbol {\xi} \in \Re^ {3}: \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) > 1 \} \\ \boldsymbol {\chi} _ {w} ^ {b} = \{\boldsymbol {\xi} \in \Re^ {3}: \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) = 1 \} \\ \boldsymbol {\chi} _ {w} ^ {i} = \{\boldsymbol {\xi} \in \Re^ {3}: \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) <   1 \} \end{array} \right.\tag{5}
$$

where $\chi _ { o } ^ { e } , \chi _ { o } ^ { b }$ and $\chi _ { o } ^ { i }$ are points in exterior, boundary and interior regions of the obstacle, respectively. $\chi _ { w } ^ { e } , \chi _ { w } ^ { b }$ and $\chi _ { w } ^ { i }$ are points in exterior, boundary and interior regions of the workspace, respectively.

## B. DS based Trajectory in the Workspace

The DS based obstacle avoidance approach in [16] is proposed to ensure the impenetrability of the obstacles, i.e. the DS is always in the exterior region of an obstacle. However, as described above, the DS in Fig.1(b) should never go out of the workspace.

At each point $\pmb { \zeta } _ { w } ^ { b } \in \pmb { \chi } _ { w } ^ { b }$ on the inner surface of the workspace boundary in Fig.2, define $\tilde { \pmb { \xi } } _ { w } ^ { b } = \pmb { \xi } - \pmb { \xi } _ { w } ^ { c }$ , we can get a tangential plane defined by its norm vector ${ \pmb n } _ { w } ( { \pmb \xi } _ { w } ^ { b } )$ :

$$
\boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}) = \left[ - \frac {\partial \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})}{\partial (\boldsymbol {\xi} _ {w} ^ {b}) _ {1}} - \frac {\partial \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})}{\partial (\boldsymbol {\xi} _ {w} ^ {b}) _ {2}} - \frac {\partial \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})}{\partial (\boldsymbol {\xi} _ {w} ^ {b}) _ {3}} \right] ^ {T}\tag{6}
$$

By extension, a deflection plane at each point $\pmb { \xi } \in \pmb { \chi } _ { w } ^ { i }$ in the interior region of the workspace can be computed with normal vector:

$$
\boldsymbol {n} _ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w}\right) = \left[ - \frac {\partial \Gamma_ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w}\right)}{\partial (\boldsymbol {\xi}) _ {1}} - \frac {\partial \Gamma_ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w}\right)}{\partial (\boldsymbol {\xi}) _ {2}} - \frac {\partial \Gamma_ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w}\right)}{\partial (\boldsymbol {\xi}) _ {3}} \right] ^ {T}\tag{7}
$$

A linear combination of a set of two linearly independent vectors that form a basis of the deflection plane, can describe every point on the deflection plane. Here, a set of vectors consists of $e _ { w } ^ { 1 } ( { \widetilde { \xi } } _ { w } )$ and $e _ { w } ^ { 2 } ( { \widetilde { \xi } } _ { w } )$ is chosen as:

$$
\left\{ \begin{array}{l} \boldsymbol {e} _ {w} ^ {1} (\widetilde {\xi} _ {w}) = \left[ \left(\boldsymbol {n} _ {w} (\widetilde {\xi} _ {w})\right) _ {2} - \left(\boldsymbol {n} _ {w} (\widetilde {\xi} _ {w})\right) _ {1} 0 \right] ^ {T} \\ \boldsymbol {e} _ {w} ^ {2} (\widetilde {\xi} _ {w}) = \left[ \left(\boldsymbol {n} _ {w} (\widetilde {\xi} _ {w})\right) _ {3} 0 - \left(\boldsymbol {n} _ {w} (\widetilde {\xi} _ {w})\right) _ {1} \right] ^ {T} \end{array} \right.\tag{8}
$$

Similarly to the modulation matrix of a spherical obstacle determined in [16], the modulation matrix $M _ { w } ( \widetilde { \xi } _ { w } )$ of the workspace is given by:

$$
\pmb {M} _ {w} (\widetilde {\pmb {\xi}} _ {w}) = \pmb {E} _ {w} (\widetilde {\pmb {\xi}} _ {w}) \pmb {D} _ {w} (\widetilde {\pmb {\xi}} _ {w}) \pmb {E} _ {w} (\widetilde {\pmb {\xi}} _ {w}) ^ {(- 1)}\tag{9}
$$

with a basis matrix $\pmb { { \cal E } } _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ and an associated eigenvalue matrix $\pmb { { \cal D } } _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ as:

$$
\boldsymbol {E} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) = \left[ \begin{array}{c c c} \boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) & \boldsymbol {e} _ {w} ^ {1} (\widetilde {\boldsymbol {\xi}} _ {w}) & \boldsymbol {e} _ {w} ^ {2} (\widetilde {\boldsymbol {\xi}} _ {w}) \end{array} \right]\tag{10}
$$

$$
\boldsymbol {D} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) = \operatorname{diag} \left(\lambda_ {w} ^ {1} (\widetilde {\boldsymbol {\xi}} _ {w}), \lambda_ {w} ^ {2} (\widetilde {\boldsymbol {\xi}} _ {w}), \lambda_ {w} ^ {3} (\widetilde {\boldsymbol {\xi}} _ {w})\right)\tag{11}
$$

where

$$
\lambda_ {w} ^ {1} (\widetilde {\boldsymbol {\xi}} _ {w}) = \left\{ \begin{array}{l l} 1 - \left| \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) \right| & \left| \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) \right| > \lambda_ {w} \\ 1 & \left| \Gamma_ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) \right| \leq \lambda_ {w} \end{array} \right.
$$

$$
\lambda_ {w} ^ {2} (\widetilde {\xi} _ {w}) = \lambda_ {w} ^ {3} (\widetilde {\xi} _ {w}) = \left\{ \begin{array}{l l} 1 + \left| \Gamma_ {w} (\widetilde {\xi} _ {w}) \right| & \left| \Gamma_ {w} (\widetilde {\xi} _ {w}) \right| > \lambda_ {w} \\ 1 & \left| \Gamma_ {w} (\widetilde {\xi} _ {w}) \right| \leq \lambda_ {w} \end{array} , 0 <   \lambda_ {w} <   1. \right.
$$

Since $T _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ monotonically increases with $\left\| \tilde { \xi } _ { w } \right\|$ , when $\lambda _ { \scriptscriptstyle W } = 0$ , the matrices $\pmb { { \cal D } } _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ and $M _ { w } ( \widetilde { \xi } _ { w } )$ converge to the identity matrix as the distance to the workspace center decreases. Therefore, the effect of the modulation matrix is maximum at the inner boundary of the workspace, and vanishes at the points near the workspace center.

In practice, the original DS should not be deformed by the modulation matrix except in the region near the inner workspace boundary. This can be achieved by choosing a proper value for $\lambda _ { w }$ in Eq.(11). The effect of the modulation matrix disappears in more region of the workspace around the workspace center as $\lambda _ { w }$ increases.

Similar to the obstacle avoidance method in [16], we can apply the workspace boundary modulation given by Eq.(9) to the original DS given by Eq.(1), then we have:

$$
\dot {\boldsymbol {\xi}} = \boldsymbol {M} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w}) \boldsymbol {f} (\boldsymbol {\xi})\tag{12}
$$

Theorem 1 Consider a three-dimensional convex workspace with boundary $T _ { \scriptscriptstyle w } ( \widetilde { \xi } _ { \scriptscriptstyle w } ) = 1$ with respect to a reference point $\xi _ { w } ^ { c }$ in the workspace. And the original DS given by Eq.(1) converges to a target point in the workspace. A trajectory $\{ \xi \} _ { t }$ that starts in the workspace, i.e. ${ \varGamma } _ { w } ( \left\{ \xi \right\} _ { 0 } - \xi _ { w } ^ { c } ) \leq 1$ ,and evolves according to Eq.(12), will never go out of the workspace, i.e. ${ \varGamma } _ { w } ( \left\{ \xi \right\} _ { t } - \xi _ { w } ^ { c } ) \leq 1 , t = 0 . . . \infty$ . Proof: see Appendix A.

## C. Obstacle does not Intersect the Workspace Boundary

So far we have shown how the workspace modulation matrix $M _ { w } ( \widetilde { \xi } _ { w } )$ can be used to deform a DS such that it never go out of the workspace of a manipulator. In a case that there is an obstacle in the workspace and does not intersect the workspace boundary as shown in Fig.3(a), the original DS should be deformed by a proper dynamic modulation matrix such that it neither penetrate the obstacle nor go out of the workspace. This is a problem similar to the multi-obstacle avoidance problem described in [16].

When the obstacle does not intersect with the workspace boundary in Fig.3(a), as in [16], we can compute a dynamic modulation ${ \pmb { M } } _ { o } ( { \pmb { \tilde { \xi } } } _ { o } )$ of the obstacle as:

$$
\boldsymbol {M} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) = \boldsymbol {E} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) \boldsymbol {D} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) \boldsymbol {E} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) ^ {(- 1)}\tag{13}
$$

with a basis matrix $\pmb { { \cal E } } _ { o } ( \tilde { \pmb { \xi } } _ { o } )$ and an associated eigenvalue matrix $\pmb { { \cal D } } _ { o } ( \widetilde { \pmb { \xi } } _ { o } )$ as:

$$
\boldsymbol {E} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) = \left[ \begin{array}{c c c} \boldsymbol {n} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) & \boldsymbol {e} _ {o} ^ {1} (\widetilde {\boldsymbol {\xi}} _ {o}) & \boldsymbol {e} _ {o} ^ {2} (\widetilde {\boldsymbol {\xi}} _ {o}) \end{array} \right]\tag{14}
$$

$$
\boldsymbol {D} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o}) = \operatorname{diag} \left(\lambda_ {o} ^ {1} (\widetilde {\boldsymbol {\xi}} _ {o}), \lambda_ {o} ^ {2} (\widetilde {\boldsymbol {\xi}} _ {o}), \lambda_ {o} ^ {3} (\widetilde {\boldsymbol {\xi}} _ {o})\right)\tag{15}
$$

where $\begin{array} { r } { \lambda _ { o } ^ { 1 } ( \widetilde { \xi } _ { o } ) = 1 - \frac { \omega _ { o } ( \widetilde { \xi } _ { o } ) } { \big | T _ { o } ( \widetilde { \xi } _ { o } ) \big | } , \ : \lambda _ { o } ^ { 2 } ( \widetilde { \xi } _ { o } ) = \lambda _ { o } ^ { 3 } ( \widetilde { \xi } _ { o } ) = 1 + \frac { \omega _ { o } ( \widetilde { \xi } _ { o } ) } { \big | T _ { o } ( \widetilde { \xi } _ { o } ) \big | } } \end{array}$ , and

$\omega _ { o } ( \tilde { \xi } _ { o } )$ is a weighting coefficient of the obstacle that can be computed according to [16]:

$$
\omega_ {o} (\widetilde {\xi} _ {o}) = \frac {(1 - \Gamma_ {w} (\widetilde {\xi} _ {w}))}{(\Gamma_ {o} (\widetilde {\xi} _ {o}) - 1) + (1 - \Gamma_ {w} (\widetilde {\xi} _ {w}))}\tag{16}
$$

and a corresponding weighting coefficient $\omega _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ of the workspace is computed as:

$$
\omega_ {w} (\widetilde {\xi} _ {w}) = \frac {(\Gamma_ {o} (\widetilde {\xi} _ {o}) - 1)}{(\Gamma_ {o} (\widetilde {\xi} _ {o}) - 1) + (1 - \Gamma_ {w} (\widetilde {\xi} _ {w}))}\tag{17}
$$

Then, the modulation matrix $M _ { w } ( \widetilde { \xi } _ { w } )$ of the workspace given by Eq.(9) can be modified as:

$$
{ } ^ { w } \boldsymbol { M } _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) = \boldsymbol { E } _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) ^ { w } \boldsymbol { D } _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \boldsymbol { E } _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) ^ { ( - 1 ) }\tag{18}
$$

with a modified eigenvalues matrix ${ } ^ { w } { \pmb { D } } _ { w } ( { \pmb { \tilde { \xi } } } _ { w } )$ as

$$
{ } ^ { w } \boldsymbol { D } _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) = \operatorname{diag} ( { } ^ { w } \lambda _ { w } ^ { 1 } ( \widetilde { \boldsymbol { \xi } } _ { w } ) , { } ^ { w } \lambda _ { w } ^ { 2 } ( \widetilde { \boldsymbol { \xi } } _ { w } ) , { } ^ { w } \lambda _ { w } ^ { 3 } ( \widetilde { \boldsymbol { \xi } } _ { w } ) )\tag{19}
$$

where

$$
{ } ^ { w } \lambda _ { w } ^ { 1 } ( \widetilde { \boldsymbol { \xi } } _ { w } ) = \left\{ \begin{array} { l l } 1 - \omega _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | \Gamma _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | & \Big | \Gamma _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | > \lambda _ { w } \\ 1 & \Big | \Gamma _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | \leq \lambda _ { w } \end{array} \right.
$$

$$
{ } ^ { w } \lambda _ { w } ^ { 2 } ( \widetilde { \boldsymbol { \xi } } _ { w } ) = { } ^ { w } \lambda _ { w } ^ { 3 } ( \widetilde { \boldsymbol { \xi } } _ { w } ) = \left\{ \begin{array} { l l } 1 + \omega _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | \Gamma _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | & \Big | \Gamma _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | > \lambda _ { w } \\ 1 & \Big | \Gamma _ { w } ( \widetilde { \boldsymbol { \xi } } _ { w } ) \Big | \leq \lambda _ { w } \end{array} . \right.
$$

![](Zheng2020Dynamical_figs/141771a97499597b514cd2df8398284e6a6f95ed2918fd6613dc95effdc5930e.jpg)  
(a)

![](Zheng2020Dynamical_figs/f61df9db2c7fa9d98fecfdd25dc07fa30495f37c4a9d2d056781341d6e8f4a8c.jpg)  
(b)  
Figure 3. Illustration of the workspace boundary with a convex obstacle.

According to Eq.(16) and Eq.(17), we observe that $\omega _ { o } ( \widetilde { \xi } _ { o } ) + \omega _ { w } ( \widetilde { \xi } _ { w } ) = 1 , 0 \leq \omega _ { o } ( \widetilde { \xi } _ { o } ) \leq 1$ and $0 \leq \omega _ { w } ( \widetilde { \pmb { \xi } } _ { w } ) \leq 1$ . At the obstacle boundary, we have $\omega _ { o } ( \widetilde { \xi } _ { o } ) = 1$ and $\omega _ { w } ( \widetilde { \pmb { \xi } } _ { w } ) = 0$ and vice versa. With the obstacle modulation matrix ${ \pmb { M } } _ { o } ( { \pmb { \tilde { \xi } } } _ { o } )$ given by Eq.(13) and the workspace modulation matrix $^ w M _ { w } ( { \widetilde \xi } _ { w } )$ given by Eq.(18), we can compute a combined modulation matrix that consider the net effect of the obstacle and the workspace as:

$$
\overline {{M}} (\widetilde {\xi}) = M _ {o} (\widetilde {\xi} _ {o}) ^ {w} M _ {w} (\widetilde {\xi} _ {w})\tag{20}
$$

We can apply the combined modulation matrix $\overline { { { \pmb { M } } } } ( \widetilde { \pmb { \xi } } )$ given by Eq.(20) to the original DS given by Eq.(1), then we have:

$$
\dot {\boldsymbol {\xi}} = \overline {{\boldsymbol {M}}} (\widetilde {\boldsymbol {\xi}}) \boldsymbol {f} (\boldsymbol {\xi})\tag{21}
$$

According to [16] and Theorem 1, a trajectory $\{ \xi \} _ { t }$ , that starts in the workspace, and evolves according to Eq.(21), will neither go out of the workspace nor penetrate the obstacle.

## D. Obstacle Intersects the Workspace Boundary

In a case that an obstacle intersects the workspace boundary as shown in Fig.3(b), the modulation matrix $\overline { { { \pmb { M } } } } ( \widetilde { \pmb { \xi } } )$ may lose efficacy, since $T _ { o } ( \widetilde { \xi } _ { o } ) = T _ { w } ( \widetilde { \xi } _ { w } ) = 1$ at the points on the intersection line between the obstacle and workspace boundary, then $\omega _ { o } ( \tilde { \xi } _ { o } )$ and $\omega _ { w } ( \widetilde { \pmb { \xi } } _ { w } )$ are not numbers. Besides, this is a concave problem, and the original DS is always nonlinear, hence, current methods cannot deal with it [16, 17].

To solve the problem, consider a motion $\{ \xi \} _ { t }$ , that starts in the workspace and outside the obstacle. When the motion $\{ \xi \} _ { t }$ does not reach any point on the intersection line, in order to ensure that the motion $\{ \xi \} _ { t }$ neither ${ \bf g 0 }$ out of the workspace nor penetrate the obstacle, according to [16] and Section C, the motion can evolve according to Eq.(21). When the motion $\{ \xi \} _ { t }$ reaches a point $\xi _ { o w } ^ { b }$ on the intersection line between the obstacle and the workspace boundary, i.e. ${ \cal T } _ { w } ( \{ \xi \} _ { t } - \xi _ { w } ^ { c } ) = 1$ and ${ \cal T } _ { o } ( \big \{ \pmb { \xi } \big \} _ { t } - \pmb { \xi } _ { o } ^ { c } ) = 1$ define $\widetilde { \pmb { \xi } } _ { w } ^ { b } = \pmb { \xi } _ { o w } ^ { b } - \pmb { \xi } _ { w } ^ { c }$ and $\widetilde { \pmb { \xi } } _ { o } ^ { b } = \pmb { \xi } _ { o w } ^ { b } - \pmb { \xi } _ { o } ^ { c }$ , we can compute the normal vector ${ \pmb n } _ { w } ( { \pmb \xi } _ { w } ^ { b } )$ of the workspace boundary and the normal vector ${ \pmb n } _ { o } ( { \pmb \xi } _ { o } ^ { b } )$ of the obstacle surface at the point $\boldsymbol { \xi } _ { o w } ^ { b }$ as follows:

$$
\boldsymbol {n} _ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right) = \left[ - \frac {\partial \Gamma_ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right)}{\partial (\boldsymbol {\xi}) _ {1}} - \frac {\partial \Gamma_ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right)}{\partial (\boldsymbol {\xi}) _ {2}} - \frac {\partial \Gamma_ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right)}{\partial (\boldsymbol {\xi}) _ {3}} \right] ^ {T}\tag{22}
$$

$$
\boldsymbol {n} _ {o} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right) = \left[ \begin{array}{c c c} \frac {\partial \Gamma_ {o} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right)}{\partial (\boldsymbol {\xi}) _ {1}} & \frac {\partial \Gamma_ {o} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right)}{\partial (\boldsymbol {\xi}) _ {2}} & \frac {\partial \Gamma_ {o} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right)}{\partial (\boldsymbol {\xi}) _ {3}} \end{array} \right] ^ {T}\tag{23}
$$

Then, a vector $\pmb { e } _ { o w } ( \pmb { \xi } _ { o w } ^ { b } )$ that is perpendicular to the vector ${ \pmb n } _ { w } ( { \pmb \xi } _ { w } ^ { b } )$ and the vector ${ \pmb n } _ { o } ( \widetilde { \pmb \xi } _ { o } ^ { b } )$ is given by:

$$
\boldsymbol {e} _ {o w} (\boldsymbol {\xi} _ {o w} ^ {b}) = \boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}) \times \boldsymbol {n} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})\tag{24}
$$

Similarly to the modulation matrix given by Eq.(13), a modulation matrix $M _ { o w } ( \widetilde { \xi } _ { o } ^ { b } )$ of the point $\boldsymbol { \xi } _ { o w } ^ { b }$ on the intersection line between the obstacle and the workspace boundary is given by:

$$
\boldsymbol {M} _ {o w} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right) = \boldsymbol {E} _ {o w} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right) \boldsymbol {D} _ {o w} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right) \operatorname{pinv} \left(\boldsymbol {E} _ {o w} \left(\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}\right)\right)\tag{25}
$$

with a basis matrix $E _ { o w } ( \widetilde { \xi } _ { o } ^ { b } )$ and an associated eigenvalue matrix $D _ { o w } ( \tilde { \xi } _ { o } ^ { b } )$ as:

$$
\pmb {E} _ {o w} (\widetilde {\pmb {\xi}} _ {o} ^ {b}) = \left[ \begin{array}{c c} \pmb {n} _ {o} (\widetilde {\pmb {\xi}} _ {o} ^ {b}) & \pmb {e} _ {o w} (\pmb {\xi} _ {o w} ^ {b}) \end{array} \right]\tag{26}
$$

$$
\pmb {D} _ {o w} (\widetilde {\pmb {\xi}} _ {o} ^ {b}) = \mathrm{diag} (\lambda_ {o} ^ {1} (\widetilde {\pmb {\xi}} _ {o} ^ {b}), \lambda_ {o} ^ {2} (\widetilde {\pmb {\xi}} _ {o} ^ {b}))\tag{27}
$$

where $\begin{array} { r } { \lambda _ { o } ^ { 1 } ( \widetilde { \xi } _ { o } ^ { b } ) = 1 - \frac { 1 } { \left| T _ { o } ( \widetilde { \xi } _ { o } ^ { b } ) \right| } , \lambda _ { o } ^ { 2 } ( \widetilde { \xi } _ { o } ^ { b } ) = 1 + \frac { 1 } { \left| T _ { o } ( \widetilde { \xi } _ { o } ^ { b } ) \right| } } \end{array}$ , is the pseudo inverse of () .

We can apply the modulation matrix $M _ { o w } ( \widetilde { \xi } _ { o } ^ { b } )$ of the intersection line given by Eq.(25) to the original DS given by Eq.(1), then we have:

$$
\dot {\boldsymbol {\xi}} = \boldsymbol {M} _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}) \boldsymbol {f} (\boldsymbol {\xi})\tag{28}
$$

Theorem 2 Consider a three-dimensional convex workspace with boundary $T _ { \scriptscriptstyle w } ( \widetilde { \xi } _ { \scriptscriptstyle w } ) = 1$ with respect to a reference point $\xi _ { w } ^ { c }$ in the workspace and a three-dimensional convex obstacle with boundary $T _ { o } ( \widetilde { \xi } _ { o } ) = 1$ with respect to a reference point $\xi _ { o } ^ { c }$ inside the obstacle. The obstacle intersects with the workspace boundary. A trajectory $\{ \xi \} _ { t }$ , that starts in the workspace and outside the obstacle, i.e. ${ \varGamma } _ { w } ( \left\{ \xi \right\} _ { 0 } - \xi _ { w } ^ { c } ) \leq 1$ and ${ \varGamma } _ { o } ( \left\{ \xi \right\} _ { 0 } - \xi _ { o } ^ { c } ) \geq 1$ , and evolves according to Eq.(21). When the trajectory $\{ \xi \} _ { t }$ reaches a point on the intersection line between the obstacle and the workspace boundary, i.e. ${ \cal T } _ { w } ( \{ \xi \} _ { t } - \xi _ { w } ^ { c } ) = 1$ and ${ \cal T } _ { o } ( \left\{ \xi \right\} _ { t } - \xi _ { o } ^ { c } ) = 1$ , then the trajectory $\{ \xi \} _ { t }$ evolves according to Eq.(28) and vice versa, will neither go out of the workspace nor penetrate the obstacle, i.e. ${ \cal T } _ { w } ( \{ \xi \} _ { t } - \xi _ { w } ^ { c } ) \le 1$ and ${ \varGamma _ { o } } ( \left\{ \xi \right\} _ { t } - \xi _ { o } ^ { c } ) \geq 1 , t = 0 . . \infty$ . Proof: see Appendix B.

Similarly to the safety margin given in [16], in practice, the condition, i.e. ${ \cal T } _ { w } ( \left\{ \xi \right\} _ { t } - \xi _ { w } ^ { c } ) = 1$ and ${ \cal T } _ { o } ( \left\{ \xi \right\} _ { t } - \xi _ { o } ^ { c } ) = 1$ , given in Theorem 2 can be relaxed to $\beta _ { 1 } \le T _ { w } ( \left\{ \xi \right\} _ { t } - \xi _ { w } ^ { c } ) \le 1$ and $1 \leq T _ { o } ( \left\{ \xi \right\} _ { t } - \xi _ { o } ^ { c } ) \leq \beta _ { 2 }$ , where $0 < \beta _ { 1 } \leq 1 , \ \beta _ { 2 } \geq 1 . \ \beta _ { 1 }$ and $\beta _ { 2 }$ should be chosen as close to 1 as possible.

![](Zheng2020Dynamical_figs/c3f43e3693e2bbb8b67c17884233288eb4b2c246ce9587c9d681f53e558448fc.jpg)  
(a)

![](Zheng2020Dynamical_figs/b8fe930f476ee9eb12fb1ec3d4b61ca385928651ca0eb0c1717257c2a1a519cd.jpg)  
(b)

![](Zheng2020Dynamical_figs/f3099fda674f6ebe3f60b2f5acba87b1f68d9fd5073097661cc30c4c721055a1.jpg)  
(c)  
Figure 4. Illustration of the effectiveness of the proposed method.

Fig.4 illustrates the effectiveness of the proposed method. The red curve is DS based trajectory, the purple surface is the workspace boundary, the cyan cuboid is the obstacle, the cross mark is the start point of the trajectory and the star mark is the end point. Fig.4(a) shows an original DS given by Eq.(1), which is learned according to the method given in [18]. Fig.4(b) shows a DS deformed by the obstacle modulation matrix given in [16] that can avoid the obstacle. However, part of the trajectory is outside the workspace. Fig.4(c) shows a DS deformed by the proposed approach. We observe the DS neither penetrate the obstacle nor go out of the workspace, hence, the effectiveness of the approach is validated.

![](Zheng2020Dynamical_figs/afeb15cb556853d8e36be8dae30ba73d11a7b774dad843355e97f2ce546f0609.jpg)  
(a)

![](Zheng2020Dynamical_figs/9e1c1dc4668ec20e90a848a1e45d026fcc18e3930452dad1cdc11664afe5431d.jpg)  
(b)

![](Zheng2020Dynamical_figs/3e857720286b8e2120ca16cc713f2b89add3acc87888a039e33da7e8b334e308.jpg)  
(c)  
Figure 5. Illustration of a local minim point of the DS.

## E. Local Minima and Direction

According to [16], since the modulation matrix $M _ { o w } ( \widetilde { \xi } _ { o } ^ { b } )$ loses one rank, the modulated DS given by Eq.(28) may has some other equilibrium points besides the target point that could be local minima and/or saddle points, then, the DS will get stuck at those points [16]. To avoid the DS getting stuck into the local minima, when the norm of the velocity $\dot { \xi }$ given by Eq.(28) is less than a threshold value $\nu _ { t h }$ , then, we replace $\dot { \boldsymbol { \xi } }$ with $\nu _ { t h } \frac { \dot { \xi } } { \| \dot { \xi } \| }$ . Fig.5(a) shows a local minima point , and the corresponding velocities of deformed DS vanish at the point S as shown in Fig.5(b) .

According to Theorem 2, the velocity $\dot { \boldsymbol { \xi } }$ given by Eq.(28) is parallel to the vector $e _ { o w } ( \xi _ { o w } ^ { b } )$ given by Eq.(24). However the direction of $\dot { \xi }$ is uncertain. We can set the direction of $\dot { \xi }$ to be the same as the direction of $\pmb { e } _ { o w } ( \widetilde { \pmb { \xi } } _ { o w } ^ { b } )$ by replacing $\dot { \xi }$ with sign $( \dot { \xi } ^ { T } \pmb { e } _ { o w } ( \pmb { \xi } _ { o w } ^ { b } ) ) \dot { \xi }$ . In addition, we can set the direction of $\dot { \boldsymbol { \xi } }$ to be opposite to the direction of $\pmb { e } _ { o w } ( \pmb { \xi } _ { o w } ^ { b } )$ by replacing $\dot { \xi } \mathrm { w i t h } \ - \mathrm { s i g n } ( \dot { \xi } ^ { T } { \pmb e } _ { o w } ( { \pmb \xi } _ { o w } ^ { b } ) ) \dot { \xi }$

![](Zheng2020Dynamical_figs/8c0e1bbe2445aa627e1dea344f1d914522957018516ccf16f12fe66aa12fdb8f.jpg)  
(a)

![](Zheng2020Dynamical_figs/730c61f9c55bdfa2b38f22520165bad9641aafb3c6388ba4185a9928e6ecfb17.jpg)  
(b)  
Figure 6. Illustration of two kinds of DS with different directions.

Fig.6(a) shows a DS with the direction of its velocity $\dot { \xi }$ given by Eq.(28) is set to be the same as the direction of $\pmb { e } _ { o w } ( \pmb { \xi } _ { o w } ^ { b } )$ . Fig.6(b) shows a DS with the direction of its velocity $\dot { \xi }$ given by Eq.(28) is set to be the opposite to the direction of $\pmb { e } _ { o w } ( \pmb { \xi } _ { o w } ^ { b } )$ . In both cases, the locations of the obstacle relative to the workspace are the same.

## IV. EXPERIMENT VALIDATION

To further verify the proposed method, we implement the proposed approach and the method presented in [16] on the 7-DOF arm of the UBTECH humanoid robot and carry out a set of comparative experiments. The arm as illustrated in Fig.7 is controlled at a rate of 100 Hz. The actual positions and the desired positions of the end-effector are converted to joint velocities using the task space controller given in [19] and the inverted kinematics of the arm. Since we don’t have a visual detection system at present, we only consider stationary obstacles and assume that the positions and orientations of the obstacles are known. Since the obstacle avoidance methods can only ensure that a point will not penetrate the obstacle, a safety margin [16] is added to each obstacle.

Refer to Fig.4, in the experiments, an original trajectory is given for the end-effector. First, in the presence of the obstacle, i.e. a ball, the original trajectory is deformed by the modulation matrix of the ball in real-time according to the method in [16] to avoid the ball. However, because the method does not consider the workspace constraint of the arm, the deformed trajectory goes out of the workspace even though it avoids the ball. Hence, the end-effector will fail to track the trajectory and cannot reach the desired target.

![](Zheng2020Dynamical_figs/eb070c8b396401de8a40ba705ef3717b8ef6cdc64bdeeb952c95120aa1245214.jpg)  
Figure 7. The experiment set-up.

Furthermore, in the presence of the ball, the original trajectory is deformed by the modulation matrix of the ball in real-time according to the proposed method to avoid the ball, while the end-effector tracks the deformed trajectory. The experiment results show that the end-effector tracking the deformed trajectory can avoid the ball and finally reach the desired target. In the experiment, the deformed trajectory neither penetrate the ball nor go out of the workspace. Therefore the experiment results indicate the effectiveness of the proposed approach.

According to [20], it is easy to apply the DS based obstacle avoidance approaches to the obstacle avoidance of moving obstacles and multiple obstacles. In the future, the extensions of the proposed method to moving obstacle avoidance and multi-obstacle avoidance will be presented. In addition, in practice, because the workspace boundaries are often more complex than spheres, we will further extend out the method for obstacle avoidance with complex workspace boundary constraints.

## V. CONCLUSION

In this paper, we presented a DS based obstacle avoidance approach for serial manipulators with limited workspace. The method works primarily by guiding the trajectory of the manipulator to evolve along an intersection line between the workspace boundary and the three-dimensional obstacle when the trajectory reaches a point on the intersection line. Besides, the trajectory can evolve along the intersection line in two opposite directions. We proved that the proposed approach can ensure that the trajectory neither penetrate the obstacle nor go out of the workspace without being stuck into local minima. The effectiveness of the approach was validated in several sets of comparative simulations. In addition, we implemented the method on the 7-DOF arm of the UBTECH humanoid robot. The experimental results show the effectiveness of the method. In the future, we will apply the approach to other problems such as concave obstacle avoidance and other robotic systems such as drones, underwater robots.

## A. Proof of Theorem 1

To ensure that the trajectory $\{ \xi \} _ { t }$ never exceed the workspace boundary, the normal velocity at the boundary points $\pmb { \zeta } _ { w } ^ { b } \in \pmb { \chi } _ { w } ^ { b }$ vanishes:

$$
(\pmb {n} _ {w} (\widetilde {\pmb {\xi}} _ {w} ^ {b})) ^ {T} \dot {\pmb {\xi}} _ {w} ^ {b} = 0\tag{29}
$$

With Eq.(9) and Eq.(12), Eq.(29) can be rewritten as:

$$
\left(\boldsymbol {n} _ {w} \left(\tilde {\xi} _ {w} ^ {b}\right)\right) ^ {T} \dot {\xi} _ {w} ^ {b} = \left(\boldsymbol {n} _ {w} \left(\tilde {\xi} _ {w} ^ {b}\right)\right) ^ {T} E _ {w} \left(\tilde {\xi} _ {w} ^ {b}\right) D _ {w} \left(\tilde {\xi} _ {w} ^ {b}\right) E _ {w} \left(\tilde {\xi} _ {w} ^ {b}\right) ^ {(- 1)} f (\cdot)\tag{30}
$$

Since ${ \pmb n } _ { w } ( { \pmb \xi } _ { w } ^ { b } )$ is perpendicular to the vectors $e _ { w } ^ { 1 } ( \widetilde { \xi } _ { w } ^ { b } )$ and $e _ { w } ^ { 2 } ( \widetilde { \pmb { \xi } } _ { w } ^ { b } )$ , then Eq.(30) reduces to:

$$
\left(\boldsymbol {n} _ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right)\right) ^ {T} \dot {\boldsymbol {\xi}} _ {w} ^ {b} = \left[ \begin{array}{l l l} a & 0 & 0 \end{array} \right] D _ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right) E _ {w} \left(\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}\right) ^ {(- 1)} \boldsymbol {f} (\cdot)\tag{31}
$$

where is a positive value. For each point on the workspace boundary, the eigenvalue $\lambda _ { w } ^ { 1 } ( \widetilde { \pmb { \xi } } _ { w } ^ { b } )$ is zero. Therefore, we get:

$$
(\boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})) ^ {T} \dot {\boldsymbol {\xi}} _ {w} ^ {b} = \left[ \begin{array}{c c c} 0 & 0 & 0 \end{array} \right] E _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b}) ^ {(- 1)} \boldsymbol {f} (\cdot) = 0\tag{32}
$$

## B. Proof of Theorem 2

To ensure that the trajectory $\{ \xi \} _ { t }$ neither go out of the workspace nor penetrate the obstacle, when the trajectory $\{ \xi \} _ { t }$ does not reach any point on the intersection line between the obstacle and the workspace boundary, the aforementioned performance is ensured according to [16] and Theorem 1.

When the trajectory $\{ \xi \} _ { t }$ reaches a point on the intersection line between the obstacle and the workspace boundary, the normal velocity of the obstacle boundary and the normal velocity of the workspace boundary at the points $\xi _ { o w } ^ { b } \in \chi _ { w } ^ { b } \cap \chi _ { o } ^ { b }$ on the intersection line vanish:

$$
(\pmb {n} _ {o} (\widetilde {\pmb {\xi}} _ {o} ^ {b})) ^ {T} \dot {\pmb {\xi}} _ {o w} ^ {b} = 0\tag{33}
$$

$$
(\pmb {n} _ {w} (\widetilde {\pmb {\xi}} _ {w} ^ {b})) ^ {T} \dot {\pmb {\xi}} _ {o w} ^ {b} = 0\tag{34}
$$

With Eq.(25) and Eq.(28), Eq.(33) and Eq.(34) can be rewritten as:

$$
\begin{array}{c} (\boldsymbol {n} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) ^ {T} \dot {\boldsymbol {\xi}} _ {o w} ^ {b} = (\boldsymbol {n} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) ^ {T} E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}) \\ D _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}) \mathrm{pinv} (E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) \boldsymbol {f} (\cdot) \\ (\boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})) ^ {T} \dot {\boldsymbol {\xi}} _ {o w} ^ {b} = (\boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})) ^ {T} E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}) \\ D _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}) \mathrm{pinv} (E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) \boldsymbol {f} (\cdot) \end{array}\tag{35}
$$

(36)

Since $e _ { o w } ( \xi _ { o w } ^ { b } )$ is perpendicular to the vectors ${ \pmb n } _ { o } ( \widetilde { \pmb \xi } _ { o } ^ { b } )$ and ${ n } _ { w } ( \widetilde { \xi } _ { w } ^ { b } )$ , then Eq.(35) and Eq.(36) reduce to:

$$
\left(\boldsymbol {n} _ {o} \left(\tilde {\boldsymbol {\xi}} _ {o} ^ {b}\right)\right) ^ {T} \dot {\boldsymbol {\xi}} _ {o w} ^ {b} = \left[ a _ {o} \quad 0 \right] D _ {o w} \left(\tilde {\boldsymbol {\xi}} _ {o} ^ {b}\right) \operatorname{pinv} \left(E _ {o w} \left(\tilde {\boldsymbol {\xi}} _ {o} ^ {b}\right)\right) \boldsymbol {f} (\cdot)\tag{37}
$$

$$
(\boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})) ^ {T} \dot {\boldsymbol {\xi}} _ {o w} ^ {b} = \left[ a _ {w} \quad 0 \right] D _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b}) \mathrm{pinv} (E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) \boldsymbol {f} (\cdot)\tag{38}
$$

where $a _ { o }$ and $a _ { w }$ are real values. For each point on the intersection line, the eigenvalue $\lambda _ { o } ^ { 1 } ( \widetilde { \xi } _ { o } ^ { b } )$ is zero. Therefore, we get:

$$
(\boldsymbol {n} _ {o} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) ^ {T} \dot {\boldsymbol {\xi}} _ {o w} ^ {b} = \left[ \begin{array}{c c} 0 & 0 \end{array} \right] \mathrm{pinv} (E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) \boldsymbol {f} (\cdot) = 0\tag{39}
$$

$$
(\boldsymbol {n} _ {w} (\widetilde {\boldsymbol {\xi}} _ {w} ^ {b})) ^ {T} \dot {\boldsymbol {\xi}} _ {o w} ^ {b} = \left[ \begin{array}{c c} 0 & 0 \end{array} \right] \mathrm{pinv} (E _ {o w} (\widetilde {\boldsymbol {\xi}} _ {o} ^ {b})) \boldsymbol {f} (\cdot) = 0\tag{40}
$$

As stated above, according to [16] and Theorem 1, with Eq.(39) and Eq.(40), Theorem 2 is proved.

[1] J. Borenstein, and Y. Koren, “The vector field histogram-fast obstacle avoidance for mobile robots,” IEEE Transactions on Robotics and Automation, vol. 7, no. 3, pp. 278–288, June 1991.

[2] R. Simmons, “The curvature-velocity method for local obstacle avoidance,” In Proc. of the IEEE int. conf. on robotics and automation, Minnesota, 1996, pp. 3375–3382.

[3] L. E. Kavraki, P. Svestka, J. -C. Latombe, and M. H. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” IEEE Transactions on Robotics and Automation, vol. 12, no. 4, pp. 566–580, August 1996.

[4] J. J. Kuffner, and S. M. LaValle, “RRT-connect: An efficient approach to single-query path planning,” In Proc. of the IEEE int. conf. on robotics and automation, San Francisco, 2000, pp. 995–1001.

[5] Diankov, R., & Kuffner, J., “Randomized statistical path planning”. In Proc. of IEEE/RSJ int. conf. on robots and systems, 2007, pp. 1–6.

[6] O. Brock, and O. Khatib, “Elastic strips: A framework for motion generation in human environments,” The International Journal of Robotics Research, vol. 21, no. 12, pp. 1031–1052, December 2002.

[7] S. Quinlan, and O. Khatib, “Elastic bands: connecting path planning and contro,” In Proc. of the IEEE int. conf. on robotics and automation, 1993, pp. 802–807.

[8] Yoshida, E., & Kanehiro, F., “Reactive robot motion using path replanning and deformation,” In Proc. IEEE int. conf. on robotics and automation, 2011, pp. 5457–5462.

[9] O. Khatib, “Real-time obstacle avoidance for manipulators and mobile robots,” The International Journal of Robotics Research, vol. 5, no. 1, pp. 90–98, Spring 1986.

[10] D.-H. Park, H. Hoffmann, P. Pastor, and S. Schaal, “Movement reproduction and obstacle avoidance with dynamic movement primitives and potential fields,” In Proc. of the IEEE-RAS int. conf. on humanoid robotics, Daejeon, 2008, pp. 91–98.

[11] I. Iossifidis, and G. Schöner, “Dynamical systems approach for the autonomous avoidance of obstacles and joint-limits for a redundant robot arm,” In Proc. of the IEEE/RSJ int. conf. on intelligent robots and systems, Beijing, 2006, pp. 580–585.

[12] Ch. Sprunk, B. Lau, P. Pfaffz, and W. Burgard, “ Online generation of kinodynamic trajectories for non-circular omnidirectional robots,” In Proc. of IEEE int. conf. on robotics and automation, Shanghai, 2011, pp. 72–77.

[13] H. J. S. Feder, and J.-J. E. Slotine, “Real-time path planning using harmonic potentials in dynamic environments,” In Proc. of IEEE int. conf. on robotics and automation, Albuquerque, 1997, pp. 874–881.

[14] J.-O. Kim, and P. K. Khosla, “Real-time obstacle avoidance using harmonic potential functions,” IEEE Transactions on Robotics and Automation, vol. 8, no. 3, pp. 338–349, June 1992.

[15] S. Waydo, and R. M. Murray, “Vehicle motion planning using stream functions,” In Proc. of IEEE int. conf. on robotics and automation, Taipei, 2003, pp. 2484–2491.

[16] S. M. Khansari Zadeh, and A. Billard, “A Dynamical System Approach to Realtime Obstacle Avoidance,” Autonomous Robots, vol. 32, no. 4, pp. 433–454, March 2012.

[17] L. Huber, A. Billard and J.-J. Slotine, “Avoidance of Convex and Concave Obstacles with Convergence ensured through Contraction,” IEEE Robotics and Automation Letters, vol. 4, no. 2, pp. 1462–1469, April 2019.

[18] S. M. Khansari Zadeh, and A. Billard, “Learning stable nonlinear dynamical systems with gaussian mixture models,” IEEE Transactions on Robotics, vol. 27, no. 5, pp. 943–957, October 2011.

[19] T. Petrič, L. Žajpah, “Smooth continuous transition between tasks on a kinematic control level: obstacle avoidance as a control problem,” Robotics and Autonomous Systems, vol. 61, no. 9, pp. 948–959, May 2013.

[20] S. M. Khansari Zadeh, “A dynamical system-based approach to modeling stable robot control policies via imitation learning,” Ph.D. dissertation, School of Engineering, Ecole Polytechnique Federale de Lausanne, Lausanne, Switzerland, 2012.