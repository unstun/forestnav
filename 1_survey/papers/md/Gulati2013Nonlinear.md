---
citation_key: Gulati2013Nonlinear
arxiv_id: 1305.5024
arxiv_url: "https://arxiv.org/abs/1305.5024"
title: "A Nonlinear Constrained Optimization Framework for Comfortable and Customizable Motion Planning of Nonholonomic Mobile Robots - Part I"
authors_short: "Shilpa Gulati et al."
year: 2013
direction_tag: P_nonholonomic_constraints
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T10:01:58Z
origin: ai+web
reviewed: false
---

# A Nonlinear Constrained Optimization Framework for Comfortable and Customizable Motion Planning of Nonholonomic Mobile Robots – Part I

Shilpa Gulati<sup>∗</sup>

Chetan Jhurani<sup>†</sup>

Benjamin Kuipers<sup>‡</sup>

## Abstract

In this series of papers, we present a motion planning framework for planning comfortable and customizable motion of nonholonomic mobile robots such as intelligent wheelchairs and autonomous cars. In this first one we present the mathematical foundation of our framework.

The motion of a mobile robot that transports a human should be comfortable and customizable. We identify several properties that a trajectory must have for comfort. We model motion discomfort as a weighted cost functional and define comfortable motion planning as a nonlinear constrained optimization problem of computing trajectories that minimize this discomfort given the appropriate boundary conditions and constraints. The optimization problem is infinite-dimensional and we discretize it using conforming finite elements. We also outline a method by which diferent users may customize the motion to achieve personal comfort.

There exists significant past work in kinodynamic motion planning, to the best of our knowledge, our work is the first comprehensive formulation of kinodynamic motion planning for a nonholonomic mobile robot as a nonlinear optimization problem that includes all of the following – a careful analysis of boundary conditions, continuity requirements on trajectory, dynamic constraints, obstacle avoidance constraints, and a robust numerical implementation.

In this paper, we present the mathematical foundation of the motion planning framework and formulate the full nonlinear constrained optimization problem. We describe, in brief, the discretization method using finite elements and the process of computing initial guesses for the optimization problem. Details of the above two are presented in Part II (Gulati et al., 2013) of the series.

## 1 Introduction

Autonomous mobile robots such as intelligent wheelchairs and autonomous cars have the potential to improve the quality of life of many demographic groups. Recent surveys have concluded that many users with mobility impairments find it dificult or impossible to operate existing power wheelchairs because they lack the necessary motor skills or cognitive abilities (Fehr et al., 2000; Simpson et al., 2008). Assistive mobile robots such as smart wheelchairs and scooters that can navigate autonomously benefit such users by increasing thei mobility (Fehr et al., 2000). Autonomous cars have the potential to increase the mobility of a significan proportion of the elderly whose driving ability is reduced due to age-related problems (Silberg et al., 2012).

The motion of an autonomous mobile robot should be comfortable to be acceptable to human users. Moreover, since the feeling of comfort is subjective, diferent users should be able to customize the motion according to their comfort. Motion planning is a challenging problem and has received significant attention. See (Latombe, 1991; Hwang and Ahuja, 1992; Choset et al., 2005; LaValle, 2006, 2011a,b). However, most of the existing motion planning methods have been developed for robots that do not transport a human user and issues such as comfort and customization have not been explicitly addressed.

In this paper we focus on planning comfortable motion for nonholonomic mobile robots such that the motion can be customized by diferent users. Our key contributions are as follows:

• We model user discomfort as a weighted cost functional. This is informed by studies of human comfort in road and railway vehicle literature that indicate that human discomfort increases with the magnitude of acceleration and jerk and that comfortable levels of these quantities have diferent magnitudes in the direction of motion and perpendicular to the direction of motion (Suzuki, 1998). Thus, our cost functional is a weighted sum of the following three physical quantities: total travel time, tangential jerk, and normal jerk.

Minimum jerk cost functionals have previously been used in literature (Zefran, 1996; Arechavaleta<sup>ˇ</sup> et al., 2008) for optimal motion planning. What is new here is the separation of tangential and normal components, and computing the weights using the technique of dimensional analysis (Langhaar, 1951) that allows us to develop a straightforward procedure for varying the weights for customization.

• We develop a framework for planning comfortable and customizable motion. Here, we present a precise mathematical formulation of kinodynamic motion planning of a nonholonomic mobile robot moving on a plane as a nonlinear constrained optimization problem. This includes an in-depth analysis of conditions under which the cost-functional is mathematically meaningful, analysis of boundary conditions, and precise formulation of constraints necessary for motion comfort and for obstacle avoidance. To the best of our knowledge, such a formulation is absent from the literature.

The idea of computing optimal trajectories that minimize a cost functional is not new and has been used for planning optimal trajectories for wheeled robots (Dubins, 1957; Reeds and Shepp, 1990; Balkcom and Mason, 2002; Bianco and Romano, 2005) and manipulators (Fernandes et al., 1991; Shiller, 1994; Zefran, 1996; Arechavaleta et al., 2008). All of these formulations make several limiting<sup>ˇ</sup> assumptions, such as known travel time, or known path, or boundary conditions on configuration but not its derivatives. None of these approaches consider obstacles. The closest existing work to ours in terms of problem formulation and numerical solution method is (Zefran, 1996), but obstacle<sup>ˇ</sup> avoidance constraints are not part of this formulation.

The trajectories planned by our framework have several useful properties – they exactly satisfy boundary conditions on position, orientation, curvature, speed and tangential acceleration, satisfy kinematic and dynamic constraints, and avoid obstacles while minimizing discomfort. Further, our framework is capable of planning a family of trajectories between a given pair of boundary conditions and can be customized by diferent users to obtain a trajectory that satisfies their comfort requirements.

• We represent obstacles as star-shaped domains with piecewise C<sup>2</sup> boundary. This choice allows treatment of non-convex obstacles without subdividing them into a union of convex shapes. This reduces the number of constraints imposed due to obstacles and leads to a faster optimization process. Such a representation of obstacles is not very common in robotics where most collisiondetection algorithms assume polygonal obstacles, and detect collisions between non-convex polygons by subdividing them into convex polygons (Quinlan, 1994; Mirtich, 1998; Lin and Manocha, 2004).

• We use the Finite Element Method to discretize the above infinite-dimensional problem into a finite dimensional problem. The finite element method is not unknown in trajectory planning but it is not very common. However, it is a natural choice for problems like ours and we strongly believe that using it provides us insight, flexibility, and reliability that is not easily obtained by choosing other discretization methods.

• Our method can be used independently for motion planning of nonholomic mobile robots. It can also be a used as local planner in sampling-based methods (LaValle, 2006) since the trajectories computed by our method exactly satisfy boundary conditions, kinodynamic constraints, continuity requirements, and avoid obstacles.

## 2 Background and related work

In this section, we characterize motion comfort by analyzing studies in ground vehicles, elevator design, and robotics. We then review existing motion planning methods and identify their strengths and limitations in planning comfortable motion.

## 2.1 Comfort

Comfort - What is it? Comfort has both psychological and physiological components, but it involves a sense of subjective well-being and the absence of discomfort, stress or pain (Richards, 1980).

Studies to characterize comfort in ground vehicles such as automobiles and trains have shown that the feeling of comfort in a vehicle is afected by various characteristics of the vehicle environment including dynamic factors (such as acceleration and jerk), ambient factors (such as temperature and air quality), and spatial factors (such as seat quality and leg room) (Richards, 1980). In this work we focus on comfort due to dynamic factors alone.

Passenger discomfort increases as the magnitude of acceleration increases (Suzuki, 1998; Jacobson et al., 1980; Pepler et al., 1980; F¨orstberg, 2000; Chakroborty and Das, 2004). This is because an increase in magnitude of acceleration implies increase in magnitude of force experienced by a passenger. Two separate components of acceleration efect discomfort – tangential component along the direction of motion and normal component perpendicular to the direction of motion (Jacobson et al., 1980; Pepler et al., 1980; F¨orstberg, 2000). The normal component is zero in a straight line motion but becomes important when traversing curves. The actual values of comfortable bounds of the two components may be diferent (Suzuki, 1998), may vary across people, may depend on the mode of transportation, and may depend on the passenger’s position (Pepler et al., 1980; F¨orstberg, 2000). Hence, guidelines for ground transportation design prescribe maximum values of accelerations (Suzuki, 1998; Chakroborty and Das, 2004; Iwnicki, 2006), or maximum values of comfort indices that are functions of accelerations (ISO, 1997; CEN, 1999).

Discomfort also increases as the magnitude of jerk increases (Pepler et al., 1980; F¨orstberg, 2000). This is because a high rate of change of jerk implies a high rate of change of magnitude or direction or both of the forces acting on the passenger. Upper bounds on jerk for comfort have been proposed for road (Chakroborty and Das, 2004) and railway vehicles (Suzuki, 1998). In elevator design, motion profiles are designed for user comfort by choosing profiles with smooth accelerations and low jerk (Hall et al., 1970; Krapek and Bittar, 1993; Spielbauer and Peters, 1995).

From a geometric standpoint, it has been known for more than a century that sharp changes in curvature of roads and railway tracks can be dangerous and can cause passenger discomfort (Laundhart, 1887; Glover, 1900; Lamm et al., 1999). For a point mass moving on a path, the normal acceleration at a point is given by $\kappa v ^ { 2 }$ where κ is the curvature of the path and v is the speed at that point. If curvature is not continuous, then normal acceleration cannot be continuous unless the speed goes to zero at the point of discontinuity.

This is clearly undesirable for comfort. In robotics, the desire to drive a robot with non-zero speed from start to goal has led to the development of methods for planning continuous curvature paths (Lamiraux and Laumond, 2001; Fraichard and Scheuer, 2004; Bianco and Romano, 2004, 2005; Piazzi et al., 2007).

To summarize, in a motion planning context, a trajectory should have the following properties for comfort. First, the acceleration should be continuous and bounded. Second, jerk should be bounded. Third, the geometric path should have curvature continuity so that is is possible to travel from start to end without stopping. Fourth, a trajectory should exactly satisfy appropriate end point boundary conditions boundary conditions on position, orientation, curvature, speed, and acceleration since many tasks require precise these (for example, positioning at a desk for an intelligent wheelchair, parking in a tight parking space for a car). Fifth, it should be possible to join multiple trajectories such that the combined trajectory has the above properties. This means that a trajectory should satisfy the above described boundary conditions on both ends.

## 2.2 Motion planning

There exists a large body of work on motion planning. Before reviewing this work, we define some terms. The space of all possible positions and orientations of a robot is called configuration space. The space of all possible configurations and their first derivatives is called state space. A trajectory is a time-parameterized function of configuration. A control trajectory is a time-parameterized function of control inputs.

Motion planning is the problem of finding either a trajectory, or a control trajectory, or both, given the initial and final configuration, and possibly their first and higher derivatives, such that the geometric path does not intersect any obstacles, and the trajectory satisfies kinematic and dynamic constraints. Kinematic constraints refer to constraints on configuration and dynamic constraints refer to constraints on velocity and its higher derivatives. These constraints arise from physics, engineering limitations, or comfort requirements.

A variety of methods have been used to solve various aspects of the motion planning problem. Path Planning methods focus on the purely geometric problem of finding a collision-free path. Another set of methods, stemming from diferential geometric control theory, focus on computing control inputs that steer a robot to a specified position and orientation or that make a robot follow a specified path. Kinodynamic motion planning methods, consider both dynamics and obstacles and focus on computing collision-free trajectories that satisfy kinematic and dynamic constraints. See (Hwang and Ahuja, 1992; Latombe, 1991; Choset et al., 2005; LaValle, 2006) for excellent presentation of all three kinds of methods, (Laumond et al., 1998) for diferential geometric control methods, and (Donald et al., 1993; Fraichard, 1996; LaValle and Kufner, 2001a; Hsu et al., 2002) for kinodynamic planning. In this work, we use motion planning in the sense of (Donald et al., 1993), that is, we speak of kinodynamic motion planning, consistent with the informal definition presented above.

## Sampling-based methods

Sampling-based methods have found widespread acceptance and practical use for motion planning. These methods are used for both path planning (LaValle, 1998; Kavraki et al., 1996; LaValle and Kufner, 2001b) and for motion planning (Canny, 1988; Barraquand and Latombe, 1989; Donald et al., 1993; Fraichard, 1996; LaValle and Kufner, 2001b,a; Hsu et al., 2002). See (LaValle, 2006) for an in-depth discussion. The main idea in all sampling-based methods is to sample the state space (Donald et al., 1993; LaValle and Kufner, 2001a) or state-time space (Erdman and Lozano-P´erez, 1987; Barraquand and Latombe, 1990; Fraichard, 1996; Hsu et al., 2002) to construct a directed graph called a roadmap from the start state to the goal region. The vertices of this graph are points in the obstacle free region of the appropriate space (state space or state-time space) and the edges are trajectory segments that satisfy kinodynamic constraints. The sequence of control inputs associated with the edges of the roadmap is the control trajectory. Among the most computationally eficient methods here are the ones that add vertices to the graph by randomized

sampling.

Randomized sampling-based algorithms follow two paradigms – multiple-query and single-query. In the multiple-query paradigm, a roadmap is constructed once and used to answer multiple path planning queries. These algorithms are particularly computationally eficient in an unchanging environment since a single roadmap can be used to answer multiple queries. Some of the most well-known algorithms that follow this paradigm are Probabilistic Roadmaps (PRMs) and its variants (Kavraki et al., 1996).

In the single-query paradigm, a roadmap is constructed for each query. Some of the most well-known algorithms that follow this paradigm are Randomly Exploring Dense Trees (RDT) (LaValle, 2006) and its variants (Hsu et al., 2002; Karaman and Frazzoli, 2011). These methods start with a roadmap rooted at the start state and iteratively add vertices by randomized sampling of the appropriate space. Diferent variants difer in the way they add a new vertex to the roadmap. We describe RDT in some detail here. A new vertex is added as follows (i) a sample point $q _ { n e w }$ is chosen from a randomized sequence (ii) a vertex $q _ { c u r r }$ in the graph that is closest to the sample point, according to a distance metric, is selected (iii) all controls from a set of discretized controls are applied to $q _ { c u r r }$ and the system is allowed to evolve for a fixed time $\Delta t \ \mathrm { ( i v ) }$ out of all the new points that can be reached via collision-free trajectories satisfying diferential constraints, the point nearest $q _ { c u r r }$ is chosen and added to the graph. This process is continued till a vertex in the goal region is added to the graph.

The closeness of the end point of the trajectory to the goal state increases as the resolution increases, but in general, it is not possible to find a trajectory that exactly reaches the goal state. If it is desired to reach a goal state exactly, then a boundary value problem has to be solved between the end state of the solution trajectory and the goal state. This is a non-trivial problem since the solution must avoid obstacles and satisfy kinodynamic constraints. Some sampling-based methods are bidirectional, that is, they simultaneously grow roadmaps from the start state as well as the goal state. In this case, a solution trajectory exactly satisfies the boundary conditions. However, like before, a boundary value problem has to be solved to connect the two roadmaps.

Since a fixed value of control input is applied for a finite length of time at each step, the planned path lacks curvature continuity and has to be smoothed in a post-processing step. Curvature continuity can be attained at the cost of increasing the dimensionality of the state space, and has been demonstrated only for a path planning problem (Scheuer and Laugier, 1998). Similarly, for achieving acceleration continuity the dimensionality of the state space has to be increased resulting in increased computational complexity.

Recently, sampling-based algorithms described above have been shown to almost always converge to solu tion that has non-optimal cost (Karaman and Frazzoli, 2011) and a new algorithm, RRT\* was proposed for planning asymptotically optimal paths. Results in a two dimensional configuration space showed that algorithm is computationally eficient. While promising, these results are very recent, and extending this work to kinodynamic motion planning is yet to be carried out.

Another set of sampling-based methods can compute optimal trajectories by constructing a grid over the state space or state-time space and searching this discrete grid using graph-search algorithms such as $\mathrm { A } ^ { * }$ (Canny, 1988; Barraquand and Latombe, 1989; Fraichard, 1996). This grid is called the state-lattice. Each pair of neighboring vertices of the grid are connected to each other by a trajectory that satisfies kinodynamic constraints. Three key choices efect the solution quality. First, the choice of discretization determines the closeness of the solution to the true optimum and the speed of computing the solution. Second, the choice of a neighborhood (e.g. k-nearest) for a vertex determines the connectivity of the space. Third, the choice of a method for computing trajectory segments between vertices determines the quality of the solution trajectory. Computing trajectory segments between adjacent states involve solving a non-trivial boundary value problem. For continuity of curvature, velocity and acceleration between connected trajectory segments, the state space should include curvature, and the first and second derivative of configuration. This results in increase in dimensionality of the search space and hence increase in computational time. For this reason, lattice-based methods have been shown to plan trajectories, with some but not all of the properties necessary for comfort (Section 2.1) in autonomous driving applications. Continuous curvature trajectories are demonstrated in (Pivtoraiko et al., 2009), continuous velocity but not continuous curvature trajectories are demonstrated in (Likhachev and Ferguson, 2009). Trajectories with continuous curvature, speed, and acceleration are demonstrated in (McNaughton et al., 2011) Here the problem is tractable because the sampling can be restricted to the road on which the vehicle drives. Eficiently planning trajectories that satisfy all properties of comfort as described in Section 2.1 in less structured environments very much remains an open problem.

## Optimal-control based methods

The problem of planning trajectories that are optimal with respect to some performance measure and also avoid obstacles has been shown to very hard (Canny and Reif, 1987), even in relatively simple cases. However, for many applications, we do require that a solution trajectory be optimal with respect to some performance measure such as time, path length, energy etc.

Optimal control methods (Bryson and Ho, 1975; Troutman, 1995) have traditionally been used for computing optimal trajectories for systems subject to dynamic constraints in the absence of obstacles and have been widely applied in aerospace engineering and control-systems engineering. The formulation consists of constructing a cost functional representing the cumulative cost over the duration of motion and minimizing the cost functional to find a desired state trajectory or control trajectory or both. A functional is an operator that maps a function to a real or complex number.

Suficient conditions for a solution of the minimization problem are given by the Hamilton-Jacobi-Bellman (HJB) equation. HJB is a second-order partial diferential equation with end-point boundary conditions. Analytic solutions of the HJB equation for linear systems with quadratic cost have long been known (Bryson and Ho, 1975). For general nonlinear systems, the HJB equation has to be solved numerically.

Necessary conditions for optimality are derived using Pontryagin’s principle and consist of a set of first-order ordinary diferential equations. These diferential equations convert the optimization problem into a twopoint boundary value problem. The system of diferential equations can either be solved analytically (where possible) or numerically using methods such as the shooting method or finite-diference methods.

Analytical solution to the problem of finding minimum length paths for Dubins (Dubins, 1957) car and Reeds and Shepp (Reeds and Shepp, 1990) car (see (Sou\`eres and Boissonnat, 1998)) was found using such an approach. Dubins car is only allowed to move forward while Reeds and Shepp car is also allowed to move backward. These paths are comprised of straight line and arc segments and minimize the distance traveled by the mid-point of the rear axle. Each path segment is traversed at a fixed speed, so the trajectories corresponding to these paths are also time-optimal for a given speed. More recently, shortest paths for a diferential drive wheeled robot were developed by including a rotation cost in the cost functional (Balkcom and Mason, 2002) (since a diferential drive robot can turn in place). Such minimum-time paths lack curvature continuity and require frequent stopping and reorienting of wheels.

More complex problems generally require a numerical solution. One frequently used numerical method is the shooting method where the two point boundary value problem is converted into an initial value problem. Shooting methods have been used for trajectory planning for nonholonomic mobile robots (Howard and Kelly, 2007; Ferguson et al., 2008). However, in shooting methods, it is challenging to specify a good initial guess of the unknown parameters that produces a final state reasonably close to the specified state. In general, the trajectories computed do not exactly satisfy end point boundary conditions.

Instead of solving the diferential equations representing necessary conditions, approximation methods that discretize the infinite-dimensional problem into a finite-dimensional one and optimize the cost functional directly in this finite-dimensional space can be used. Such methods have been used for planning optimal trajectories of robots. In (Fernandes et al., 1991), control inputs that minimize total control energy to travel between a given pair of boundary states are computed. Here Fourier basis functions are used for discretization. In (Zefran, 1996), trajectories that minimize the integral of square of<sup>ˇ</sup> $L ^ { 2 }$ norm of end-efector jerk and the square of $L ^ { 2 }$ norm of time derivatives of joint torque vector, subject to torque constraints, are computed. Here a finite-element discretization is used. Other discretizations are also possible, such as B-spline (Bobrow et al., 2001) and spectral (Strizzi et al., 2002) discretization.

Very few of the existing optimal control approaches include obstacle-avoidance. Not only do obstacle avoid ance constraints make the optimal control problem highly nonlinear, but also each obstacle divides the set of feasible solutions into disjoint regions. One of the earliest methods that included dynamic constraints and obstacle-avoidance for motion planning of autonomous vehicles used a two step approach – first an obstacle free path was found and then an optimal speed on this path was computed (Shiller and Dubowsky, 1991; Shiller and Gwo, 1991). Because of path-velocity decomposition, the resulting trajectory is, in general, not optimal. Obstacles were included as hard constraints for a two-dimensional translating robot in (Tominaga and Bavarian, 1990).

## Learning methods

Optimal control methods require an accurate model of the kinematics and dynamics of the robot as well as models of the robot’s interactions with the world. Such models are not always available. Further, it is not straightforward to develop an appropriate cost functional for a given task. Even if such models and cost functionals are available, searching through the high dimensional configuration space of the robot (e.g. in the case of humanoid robots) for an optimal trajectory can be computationally expensive. One set of learningbased methods use the key observation that, in practice, robot trajectories are restricted to a manifold by the task and by the kinodynamic constraints. The dimension of this manifold is, in general, lower than the dimension of the configuration space. These methods aim to learn the structure of this manifold from observed data of the robot’s movement (Ramamoorthy and Kuipers, 2008). Another set of methods aim to learn motion primitives for a specific task using observed data from human movements (Schaal et al., 2003). A detailed discussion of these methods is beyond the scope of this work and the interested reader is referred to the following works for more details: (Full and Koditschek, 1999; Schaal et al., 2003; Calinon and Billard, 2009; Ramamoorthy and Kuipers, 2008; Havoutis, 2012).

## Summary

Trajectories computed by sampling-based methods, in general, lack continuity of curvature and acceleration. While these problems can be solved by increasing the dimensionality of state space at the cost of increased computational complexity, the problems of lack of optimality and not satisfying the goal boundary conditions exactly still remain.

Optimal control methods have primarily been demonstrated for trajectory planning in the absence of obstacles. Further, a comprehensive formulation of kinodynamic motion planning problem for nonholonomic mobile robots that includes obstacle avoidance is absent. Thus, none of the existing methods can be directly applied to planning comfortable and trajectories. To this end, we develop a motion planning framework to compute trajectories that result in comfortable motion.

## 3 Overview of the approach

At the root of our framework is the assumption that user discomfort can be quantified as a cost functional, and that trajectories that minimize this discomfort and avoid obstacles will result in user-acceptable motion. We outline the main steps of our approach below.

• Formulate user discomfort as a mathematically meaningful cost functional. Based on existing literature, and making the assumption that a user would like to travel as fast as is consistent with comfort, we define a measure of discomfort as a weighted sum of the following three terms: total travel time, time integrals of squared tangential jerk and squared normal jerk.

Each weight used in the discomfort measure to add diferent quantities is the product of two factors. The first factor has physical units so that the physical quantities with diferent dimensions can be added together. It is a fixed function of known length and velocity scales. The second factor is a dimensionless parameter that can be varied according to user preferences. The dimensional part is derived using the standard technique of dimensional analysis (Langhaar, 1951).

• Define the problem. We formulate our motion planning problem as follows: “Given the appropriate boundary conditions, kinodynamic constraints, the weights in the cost functional, and a representation of obstacles, find a trajectory that minimizes the cost functional, satisfies boundary conditions, respects constraints, and avoids obstacles”. This description is transformed into a precise mathematical problem statement using a general nonlinear constrained optimization approach.

• Choose a parameterization of the trajectory. Mathematically, one can use diferent functions to fully describe a trajectory. We express the trajectory by an orientation and a velocity as functions of a scaled arc-length parameter where the scaling factor is an additional scalar unknown to be solved for. This leads to a relatively simple expression for discomfort. We use a scaled arc-length parameterization Thus, we do not assume that the path length is known until the problem is solved.

• Analyze the boundary conditions. A complete analysis of boundary conditions shows that for the optimization problem to be well-posed, we need to impose boundary conditions on position, orientation, curvature, speed, and tangential acceleration on each end. Further, we find that three diferent types of boundary conditions on speed and tangential acceleration on each end describe all types of motion tasks of interest such as starting/ending at rest or not.

• Choose a representation of obstacles. To incorporate obstacle avoidance, we make the assumption that each obstacle can be modeled as a star-shaped domain with a boundary that is a piecewise smooth curve with continuous second order derivative. If an obstacle is not star-shaped, our framework can still handle it if it can be expressed as a finite union of piecewise smooth star-shaped domains. It is assumed that a representation of each obstacle is known in polar coordinates where the origin lies in the interior of the kernel of the star-shaped domain. Since each obstacle is assumed star-shaped, the constraint that the trajectory stay outside obstacles can be easily cast as an inequality.

To eficiently incorporate obstacle avoidance constraints, we have to introduce position on the path as an additional unknown. This leads to a sparse Hessian of constraint inequalities, which otherwise would be dense. The position as an unknown is redundant in that it can be computed from the two primary unknowns (orientation and speed). Hence that relation is included as an extra equality constraint.

• Discretize the problem. We use finite elements to convert the infinite-dimensional minimization problem to a finite dimensional one. For discomfort to be mathematically meaningful and bounded, both speed and orientation must have square-integrable second derivatives. We use a uniform mesh and cubic Hermite polynomial shape functions on each element for speed and orientation. Starting or stopping with zero speed is a special case that requires that speed have an infinite derivative (with respect to scaled arc-length) with a known strength on the corresponding boundary point. In this case we use singular shape functions for speed only on elements adjacent to the corresponding boundary.

In the non-discretized version of the optimization problem the obstacle avoidance constraint can be expressed as the condition that each point on the trajectory should be outside each obstacle. We discretize this into a finite dimensional set of inequalities by requiring that some fixed number of points on the trajectory be outside each obstacle.

• Compute an appropriate initial guess. A good initial guess is necessary for eficiently solving any nonlinear optimization problem. In general, there exist infinitely many trajectories between any given pair of boundary conditions. Based on our analysis of this non-uniqueness, we compute a set of four good quality initial guesses by solving another, simpler, optimization problem. These initial guesses do not incorporate obstacle-avoidance constraints. Four discomfort minimization problems, corresponding to these four initial guesses, are solved to find four trajectories. The lowest cost trajectory can be chosen as the final solution.

• Implement and solve. We use Ipopt, a robust large-scale nonlinear constrained optimization library (W¨achter and Biegler, 2006) to solve the discretized problem.

## 4 Organization of this paper

This paper is organized as follows. Section 5 presents some preliminary material on the motion of nonholonomic mobile robot on a plane and on parametric curves. Section 6 lays out the mathematical foundation of our framework, and is followed by the numerical solution method in Section 7 and computing an initial guess in Section 8. Evaluation of the framework and results are presented in Section 9, followed by concluding remarks and direction for future work in Section 10.

## 5 Preliminary material

In this section, we present the notation and some preliminary material that is relevant to our formulation. We begin by an analysis of motion of a nonholonomic mobile robot moving on a plane. We then provide a brief introduction to parametric curves and arc-length parameterization of curves.

## 5.1 Motion of a nonholonomic mobile robot moving on a plane

The configuration of a rigid body moving on a plane at any time t can be completely specified by specifying the position vector $\mathbf { r } ( t ) = \{ x ( t ) , y ( t ) \}$ and orientation $\theta ( t )$ of a body-fixed frame with respect to a fixed reference frame. Suppose the rigid body starts from an initial configuration at time $t = 0$ and reaches a final configuration at time $t = \tau$ . To fully specify the motion of the body it is necessary to specify the functions $x ( t ) , y ( t )$ and $\theta ( t )$ on $I = [ 0 , \tau ]$ . If this body is a physical system, it cannot change its position instantaneously. Further, since forces of infinite magnitude cannot be applied in the real world, the acceleration of the body must be finite. Hence $x ( t ) , y ( t )$ , and $\theta ( t )$ must be at least $C ^ { 1 }$ on I.

If this rigid body has directional wheels, its motion should obey the following nonholonomic constraint

$$
\dot {x} \sin \theta - \dot {y} \cos \theta = 0.\tag{1}
$$

Here dot, (˙), represents derivative with respect to t. For motion planning, it is common to model a mobile robot as a wheeled rigid body subject to above nonholonomic constraint, and we will do the same. A motion of such a body can be specified by specifying a travel time τ and a trajectory $\mathbf { r } ( t )$ for $t \in [ 0 , \tau ]$ . The orientation $\theta ( t )$ can be computed from Equation (1). Essentially, $\theta ( t ) = \arctan 2 ( \dot { { \mathbf r } } ( t ) )$ . If $\dot { \mathbf { r } } ( t )$ is zero, which means the velocity is zero, then this equation cannot be used. If the instantaneous velocity is zero at $t = t _ { 0 }$ and non-zero in a neighborhood of $t _ { 0 } .$ , then $\theta ( t _ { 0 } )$ can be defined as a $\operatorname* { l i m } _ { t \to t _ { 0 } }$ arctan2(r˙ (t)).

## 5.2 Parametric curves and the arc-length parameterization

We present a brief introduction to parametric curves and the arc-length parameterization. The reader can refer to any book on diferential geometry of curves for more details.

Let $q _ { a } < q _ { b }$ and $I = [ q _ { a } , q _ { b } ] \subset \mathbb { R }$ . A planar parametric curve is a mapping $\mathbf { r } : I \mapsto \mathbb { R } ^ { 2 }$ . If components of r are of class $C ^ { 1 }$ , the vector space of functions with continuous first derivatives, the tangent vector at $\mathbf { r } ( q )$ for $q \in [ q _ { a } , q _ { b } ]$ is $\mathbf { r } ^ { \prime } ( q )$ . In this section, we denote derivatives with respect to the parameter q by a prime ( <sup>0</sup>).

Let the length of a curve be denoted by λ, where

$$
\lambda = \int_ {q _ {a}} ^ {q _ {b}} | | \mathbf {r} ^ {\prime} (q) | | d q.\tag{2}
$$

Define a function $s = s ( q )$ , which is the length of the curve between $[ q _ { a } , q ]$ . Then,

$$
s (q) = \int_ {q _ {a}} ^ {q} | | \mathbf {r} ^ {\prime} (q) | | d q.\tag{3}
$$

Note that the integrand $\left| \left| \mathbf { r } ^ { \prime } ( q ) \right| \right|$ is non-negative throughout I. We make an assumption that it is zero only at a finite number of $q \mathrm { { ^ { * } s } }$ in I. If q represented time, the physical interpretation is that the velocity is equal to zero only at a finite number of discrete instants in time. This assumption implies that s is an increasing function of $q .$ That is, $\mathrm { i f } \ q _ { 2 } > q _ { 1 }$ , then $s ( q _ { 2 } ) > s ( q _ { 1 } )$ . This, in turn, means that for any given $s \in [ 0 , \lambda ]$ , a unique $q = q ( s )$ can be found that corresponds to that s. If components of r are of class $C ^ { 1 }$ , then $\left| \left| \mathbf { r } ^ { \prime } ( q ) \right| \right|$ is continuous, and thus $s = s ( q )$ is also in $C ^ { 1 }$ . Thus, $\textstyle { \frac { d s } { d q } }$ is defined and is a continuous function. Obviously, $\begin{array} { r } { \frac { d s } { d q } = | | \mathbf { r } ^ { \prime } ( q ) | | } \end{array}$

With the assumption above that $\left| \left| \mathbf { r } ^ { \prime } ( q ) \right| \right|$ can be zero only at a finite number of $q \mathrm { ^ s }$ , it is possible to introduce the arc-length parameterization. For $s \in [ 0 , \lambda ]$ define

$$
\widehat {\mathbf {r}} (s) = \mathbf {r} (q) \text {   where   } s = s (q).\tag{4}
$$

The function $\widehat { \mathbf { r } }$ is well-defined because for each $s \in [ 0 , \lambda ]$ a unique q can be found. Using the chain-rule for diferentiation,

$$
\frac {d \widehat {\mathbf {r}}}{d s} = \frac {d \mathbf {r}}{d q} \frac {d q}{d s}.
$$

Now $\textstyle { \frac { d \mathbf { r } } { d q } }$ exists and is continuous and $\begin{array} { r } { \frac { d q } { d s } = \frac { 1 } { \frac { d s } { d q } } = \frac { 1 } { | | \mathbf { r } ^ { \prime } ( q ) | | } } \end{array}$ also exists (and is continuous) if $\left| \left| \mathbf { r } ^ { \prime } ( q ) \right| \right|$ is not zero. Thus, at points where $| | \mathbf { r } ^ { \prime } ( q ) | | > 0$

$$
\left| \left| \frac {d \widehat {\mathbf {r}}}{d s} \right| \right| = | | \mathbf {r} ^ {\prime} (q) | | / | | \mathbf {r} ^ {\prime} (q) | | = 1.
$$

On points where $\begin{array} { r } { | | \mathbf { r } ^ { \prime } ( q ) | | = 0 , \ | | \frac { d \widehat { \mathbf { r } } } { d s } | | } \end{array}$ cannot be computed by the expression above. However, the choice that makes it continuous for all s is 1. This is analogous to computing the limiting value of the orientation when velocity is zero as shown earlier in this section.

Symbolically, the curve has been parameterized by the arc-length. Since $\textstyle \left| \left| { \frac { d { \widehat { \mathbf { r } } } } { d s } } \right| \right| = 1$ , the tangent vector computed in the new parameterization is a unit vector. The tangent vector is $\mathbf { \dot { T } } ( s )$ and the unit normal vector is $\mathbf { N } ( s )$ , where

$$
\begin{array}{r} \mathbf {T} (s) = \frac {d \widehat {\mathbf {r}}}{d s} \\ \mathbf {N} (s) = \frac {\frac {d \mathbf {T}}{d s}}{\left| \left| \frac {d \mathbf {T}}{d s} \right| \right|} \end{array}\tag{5}
$$

See Figure 1. The signed curvature $\kappa ( s )$ is defined as

$$
\kappa (s) = \frac {d \theta}{d s}\tag{6}
$$

![](Gulati2013Nonlinear_figs/ec632788dc42f45834f760803f1632e563840f7e1238616cefb31a6fa1ac74e0.jpg)  
Figure 1: Tangent and Normal to a curve

where $\theta ( s )$ is the tangent angle.

## 6 Formulating motion planning as a constrained optimization problem

This section presents the mathematical formulation of our framework for planning comfortable and customizable motion of a planar nonholonomic mobile robot.

The steps involved are: (1) formulating a discomfort cost functional (Section 6.1) (2) dimensional analysis of cost functional (Section 6.2) (3) formulating an informal problem statement (Section 6.3) (4) choosing an appropriate parameterization of the trajectory (Section 6.4), (5) choosing the function space to which the trajectory should belong for the cost functional to be well-defined (Section 6.5), (6) analysis of boundary conditions to determine the boundary conditions that should be imposed for the problem to be well-posed (Section 6.6), (7) choosing a representation of obstacles and imposing constraints for obstacle avoidance (Section 6.7), and finally, (8) formulating the full infinite-dimensional constrained optimization problem (Section 6.8).

## 6.1 The discomfort cost functional

In Section 2.1, we saw that for motion comfort, it is necessary to have continuous and bounded acceleration along the tangential and normal directions. It is possible that the actual values of the bounds on the tangential and normal components are diferent. It is also desirable to keep jerk small and bounded. We model user discomfort as a weighted sum of the following three terms: total travel time, time integral of squared tangential jerk and time integral of squared normal jerk. Travel time is included because we make the justifiable assumption that a user would prefer to reach a goal as fast as is consistent with comfort. Thus, longer travel time implies greater discomfort. We will see later in Section 6.5 that this cost functional is mathematically meaningful only when both tangential and normal acceleration are continuous. Thus, we get continuous accelerations by construction. To keep accelerations within comfortable bounds, we impose explicit constraints on the maximum and minimum values.

We construct a cost functional J as follows:

$$
J = \tau + w _ {T} \int_ {0} ^ {\tau} (\dddot {\mathbf {r}} \cdot \mathbf {T}) ^ {2} d t + w _ {N} \int_ {0} ^ {\tau} (\dddot {\mathbf {r}} \cdot \mathbf {N}) ^ {2} d t.\tag{7}
$$

Here τ is the total travel time and r is the position of robot at time $t \in [ 0 , \tau ]$ . r represents the jerk. r ·T and $\ddot { \mathbf { r } } \cdot \mathbf { N }$ are the tangential and normal components of jerk respectively. We assume that $\mathbf { r } ( t )$ is smooth enough for the cost functional to be well-defined. This means (at least) that the acceleration vector is continuous and normal and tangential components of jerk are square integrable.

The term $\tau$ is necessary. If it is not included in the functional, the optimal solution is to reach the destination at $\tau = \infty$ traveling at essentially zero speed in the limit (except perhaps at the end-points where the speed is already specified). Thus, minimizing just the integral terms will not lead to a good solution.

The weights $( w _ { T }$ and $w _ { N } )$ are non-negative known real numbers. We separate tangential and normal jerk to allow a choice of diferent weights $( w _ { T }$ and $w _ { N } )$

The weights serve two purposes. First, they act as scaling factors for dimensionally diferent terms. Second, they determine the relative importance of the terms and provide a way to adjust the robot’s performance according to user preferences. For example, for a wheelchair, some users may not tolerate high jerk and prefer traveling slowly while others could tolerate relatively high jerks if they reach their destination quickly. The typical values of weights will be chosen using dimensional analysis.

## 6.2 Dimensional analysis of cost functional and determination of characteristic weights

Choosing the weights in an ad hoc manner does not provide weights that lead to similar comfort levels independent of the input (the boundary conditions). Moreover, since the diferent components of the total discomfort are diferent physical quantities, choice of weights should reflect this. In other words, for the total discomfort to make physical sense, the weights cannot be dimensionless numbers but should have physical units. We determine the weights using dimensional analysis (Langhaar, 1951). If the weights are chosen without the dimensional analysis step, the optimal trajectory will be diferent just by specifying the input in diferent physical units. In addition, using the same numerical weights for diferent tasks will not lead to similar quantitative discomfort level.

All the physical quantities in the cost functional (time, jerk) depend on only two units − length L and time T . From Equation (7) we see that J has dimensions $L ^ { 0 } T ^ { 1 }$ due to the first term $( \tau )$ . Thus $w _ { T }$ should have dimensions $T ^ { 6 } / L ^ { 2 }$ . Similarly, the dimensions of $w _ { N }$ $T ^ { 6 } / L ^ { 2 }$ . Alternatively, since $T = L / V , w _ { T }$ and $w _ { N }$ has dimensions $L ^ { 4 } / V ^ { 6 }$

We now determine the base values of weights analytically. The main idea behind determining the base values is that the correct base values should keep the maximum speed below the maximum allowable speed. A user can then customize the weights by multiplying the base values by a dimensionless constant that indicates user preference.

## Weight for tangential and normal jerk

We first determine $w _ { T }$ . Consider a one dimensional motion with a trajectory that starts from origin and travels a distance $L > 0$ in an unknown time $\tau > 0$ . The starting and ending speeds and accelerations are zero. We choose the exact form of the trajectory to be a quintic polynomial in time $t \in [ 0 , \tau ]$ . This choice uniquely determines the trajectory. The reason we have chosen a quintic is that it minimizes integral of squared jerk (a third derivative), just like a cubic spline minimizes integral of squared second derivative. Additionally, we choose the quintic to satisfy the boundary conditions.

Let $s ( t )$ be the distance traveled in time t. It is easily seen that the quintic

$$
s (t) = \frac {L t ^ {3}}{\tau^ {5}} \left(6 t ^ {2} - 1 5 t \tau + 1 0 \tau^ {2}\right)
$$

satisfies all the boundary conditions. For such a trajectory, the discomfort functional is

$$
J = \tau + w _ {T} \int_ {0} ^ {\tau} \dddot {s} (t) ^ {2} d t = \tau + \frac {7 2 0 L ^ {2} w _ {T}}{\tau^ {5}}.
$$

We do not know $\tau$ and $w _ { T }$ yet. We first choose $\mathrm { ~ a ~ } \tau$ that minimizes J for all $w _ { T }$ . This means

$$
\tau = \left(3 6 0 0 L ^ {2} w _ {T}\right) ^ {1 / 6}.
$$

Obviously, choosing a large value of $w _ { T }$ will increase $\tau ,$ which is natural because doing so penalizes jerk and would slow down the motion. We now choose a $w _ { T }$ so that the maximum speed during the motion is $V .$ , a dimensional velocity scale. It can be seen that the maximum speed occurs at $t = \tau / 2$ and it is

$$
\left(\frac {2 2 5}{2 0 4 8}\right) ^ {1 / 3} \left(\frac {L ^ {4}}{w _ {T}}\right) ^ {1 / 6}.
$$

Hence we choose

$$
w _ {T} = \left(\frac {2 2 5}{2 0 4 8}\right) ^ {2} \frac {L ^ {4}}{V ^ {6}}.\tag{8}
$$

The base value for the weight corresponding to the normal jerk $( w _ { N } )$ is chosen to be the same. We emphasize that both $w _ { T }$ and $w _ { N }$ will be present in a real problem and the maximum speed constraint is imposed explicitly rather than relying on weights. The analysis done here is to get dimensional dependencies of the base weight and reasonable proportionality constants using a simple problem that can be treated analytically. If a diferent problem is chosen, these base values will change.

## Factoring the weights for customization

In the preceding discussion, we determined the base values of weights using simple analytical problems. We will refer to these base values as $\widehat { w } _ { T }$ and $\widehat { w } _ { N }$ . Let $R _ { * }$ be the minimum turning radius of the robot. For any given input, we determine the characteristic length $L _ { * }$ as max $( \Delta L , \pi R _ { * } )$ where $\Delta L$ is the straight line distance between the start and end points. The characteristic speed $V _ { * }$ is the maximum allowable speed of the robot. The base values of weights are then computed as

$$
\widehat {w} _ {T} = \widehat {w} _ {N} = \left(\frac {2 2 5}{2 0 4 8}\right) ^ {2} \frac {L _ {*} ^ {4}}{V _ {*} ^ {6}}.\tag{9}
$$

The weights for the actual problem are chosen as a multiple of these base weights where the multiplying factors $f _ { T }$ and $f _ { N }$ are chosen by a user.

$$
\begin{array}{l} {w _ {T} = f _ {T} \widehat {w} _ {T},} \\ {w _ {N} = f _ {N} \widehat {w} _ {N}.} \end{array}\tag{10}
$$

## 6.3 Problem statement

We formulate motion planning as a constrained optimization problem as follows: Given the appropriate boundary conditions on position, orientation, and derivatives of position and orientation, bounds on curvature, speed, tangential and normal accelerations, the weight factors $f _ { T }$ and $f _ { N }$ (Equation (9)), and a representation of obstacles, find a trajectory that minimizes the cost functional representing user discomfort Equation (7) such that the trajectory satisfies boundary conditions, respects bounds, and avoids obstacles

We model the robot as a rigid body moving on a plane, subject to the nonholonomic constraint of Equation (1), and assume that the robot moves with non-zero speed except at a finite number of points. Let the robot start from $\mathbf { r } _ { 0 }$ at $t = 0$ and reach $\mathbf { r } _ { \tau }$ in time $\tau \ ( \mathrm { F i g u r e \ 2 } )$ ). From the discussion in Section 5.1, we see that to fully specify the motion of the robot, we need only to specify a curve $\mathbf { r } ( t )$ on $t \in [ 0 , \tau ]$ such that the curve is at least $C ^ { 1 }$ continuous. Henceforth, in this chapter, we will use trajectory to refer to a function of robot position with respect to time.

![](Gulati2013Nonlinear_figs/217812b303921bb6c5fca74aaf1f4d696c9f2c5299937987f6f50823b345ef20.jpg)  
Figure 2: Illustration of the optimization problem.  
(a) The initial configuration of the robot at time $t = 0$ is given by the position $\mathbf { r } _ { 0 }$ and orientation $\theta _ { 0 }$ . The final configuration at time $t = \tau$ is given by the position $\mathbf { r } _ { \tau }$ and orientation $\theta _ { \tau }$ . The speed at an end point, when non-zero, is necessarily along the vector q. (b) There exist infinitely many trajectories that satisfy boundary conditions and respect constraints, illustrated by the solid and dotted curves. Infinitely many of such trajectories will not result in comfortable motion, illustrated by the dotted curves. Our objective is to find a trajectory $\mathbf { r } ( t )$ that additionally minimizes the cost functional of Equation (7) and results in comfortable motion. Such a trajectory is illustrated by the solid curve.

We now transform the above problem description into a precise mathematical problem statement using a general nonlinear constrained optimization approach.

## 6.4 Parameterization of the trajectory

Mathematically, one can use diferent primary variables to describe a trajectory. For example, assuming the trajectory starts at zero time, one way to describe a trajectory is to provide the final time and the position vector as a function of time in between. Another way is to provide the final time and specify the orientation and velocity as functions of time. Another way is to represent the geometric path separately, using either position vector or orientation as a function of arc-length. The velocity at each point on the path is provided separately in this case.

We have found that making the assumption that speed be non-zero except at boundaries and expressing the trajectory solely in terms of speed and orientation as functions of a scaled arc-length parameter leads to relatively simple expressions for all the remaining physical quantities (such as accelerations and jerks). We shall see below, that with this parameterization, the primary variables (speed and orientation) and their derivatives enter the cost functional polynomially. This would not have been the case if everything were expressed in terms of r as a function of time as we did in our previous work (Gulati et al., 2009).

In the following discussion, we implicitly assume that all the quantities have suficient smoothness for expressions to be mathematically meaningful. In some cases, the derivatives appear not as point-wise values but inside an integral sign. In such a case we will assume that the integrands belong to an appropriate space of functions so that the integrals are well-defined. We explicitly state the requirements on the regularity when posing the optimization problem later in Section 6.5.

## Scaled arc-length parameterization

Let $u \in [ 0 , 1 ]$ . The trajectory is parameterized by u. The starting point is given by $u = 0$ and the ending point is given by $u = 1$ . Let $\mathbf { r } = \mathbf { r } ( u )$ denote the position vector of the robot in the plane. Let $v = v ( u )$ be the speed. Both r and v are functions of u. Let λ denote the length of the trajectory. Since only the start and end positions are known, λ cannot be specified in advance. It has to be an unknown that will be found by the optimization process.

Let $s \in [ 0 , \lambda ]$ be the arc-length parameter. We choose u to be a scaled arc-length parameter where $\begin{array} { r } { u = \frac { s } { \lambda } } \end{array}$ so that the unknown constant λ is not used in defining an unknown sized interval (as would be the case if u was chosen as the arc-length parameter).

In the following discussion we will see that the trajectory, $\mathbf { r } ( t ) , t \in [ 0 , \tau ]$ is completely specified by the trajectory length λ, the speed $v = v ( u )$ , and the orientation or the tangent angle $\theta = \theta ( u )$ to the curve. λ is a scalar while speed and orientation are functions of u. These are the three unknowns, two functions and one scalar, that will be determined by the optimization process.

Since speed is the rate of change of arc length, we have

$$
v (u) = \frac {d s}{d t}.\tag{11}
$$

Using $\textstyle u = { \frac { s } { \lambda } }$ in the above equation, we get

$$
{\frac {d u}{d t}} = {\frac {v (u)}{\lambda}}.\tag{12}
$$

This gives,

$$
t = t (u) = \int_ {0} ^ {u} \frac {\lambda}{v (u)} d u.\tag{13}
$$

If v(u) is zero only at a finite number of points in $[ 0 , 1 ]$ , then $t ( u )$ is well defined for all $u \in [ 0 , 1 ]$

Equation (13) is a key relation and gives us the means to convert between the time domain and scaled arc-length domain. We now introduce the third unknown – the orientation or the tangent angle to the curve $\theta = \theta ( u )$ . Using the results of Section 5.2, we can show that

$$
| | \mathbf {r} ^ {\prime} (u) | | = \lambda .\tag{14}
$$

The tangent vector $\mathbf { r } ^ { \prime } ( u )$ to the curve $\mathbf { r } ( u )$ is given by

$$
\mathbf {r} ^ {\prime} (u) = | | \mathbf {r} ^ {\prime} (u) | | \mathbf {T} (u) = \lambda \mathbf {T} (u)\tag{15}
$$

where $\mathbf T ( u )$ is the tangent function.

$$
\mathbf {T} (u) = \left\{\cos (\theta (u)), \sin (\theta (u)) \right\}.\tag{16}
$$

The braces {} enclose the components of a 2D vector.

Thus, $\mathbf { r } ( u )$ can be computed via the following integrals.

$$
\mathbf {r} (u) = \mathbf {r} (0) + \lambda \left\{\int_ {0} ^ {u} \cos \theta (u) d u, \int_ {0} ^ {u} \sin \theta (u) d u \right\}.\tag{17}
$$

Now, if $\theta ( u )$ is known, $\mathbf { r } ( u )$ can be computed from Equation (17). If $v ( u )$ and λ are known, $t ( u )$ can be computed from Equation (13). Using these two, we can determine the function $\mathbf { r } ( t ) , t \in [ 0 , \tau ]$

We now have all the basic relations to use chain-rule to derive expressions for all the physical quantities needed to pose the constrained optimization problem. We drop explicit references to u as a function parameter to keep the expression concise.

We compute first, second, and third derivatives of r with respect to time. These expressions are easily derived in one or two steps of chain rule diferentiation and so we do not present the intermediate steps in detail.

$$
\dot {\mathbf {r}} = v \left\{\cos \theta , \sin \theta \right\}\tag{18}
$$

$$
\ddot {\mathbf {r}} = \frac {v}{\lambda} (v ^ {\prime} \left\{\cos \theta , \sin \theta \right\} + v \theta^ {\prime} \left\{- \sin \theta , \cos \theta \right\})\tag{19}
$$

$$
{\ddot {\mathbf {r}}} = {\frac {v}{\lambda^ {2}} \left((v ^ {\prime 2} + v v ^ {\prime \prime} - v ^ {2} \theta^ {\prime 2}) \left\{\cos \theta , \sin \theta \right\}\right)}
$$

$$
{ + } { \frac { v } { \lambda ^ { 2 } } \left( ( 3 v v ^ { \prime } \theta ^ { \prime } + v ^ { 2 } \theta ^ { \prime \prime } ) \left\{ - \sin \theta , \cos \theta \right\} \right) }\tag{20}
$$

From the equations above, the expressions for tangential acceleration $a _ { T }$ and normal acceleration $a _ { N }$ are

$$
a _ {T} = \ddot {\mathbf {r}} \cdot \mathbf {T} = \frac {v v ^ {\prime}}{\lambda}\tag{21}
$$

$$
a _ {N} = \ddot {\mathbf {r}} \cdot \mathbf {N} = \frac {v ^ {2} \theta^ {\prime}}{\lambda}.\tag{22}
$$

The tangential jerk $j _ { T }$ is

$$
j _ {T} = \dddot {\mathbf {r}} \cdot \mathbf {T} = \frac {v}{\lambda^ {2}} (v ^ {\prime 2} + v v ^ {\prime \prime} - v ^ {2} \theta^ {\prime 2})\tag{23}
$$

and the normal jerk $j _ { N }$ is

$$
j _ {N} = \ddot {\mathbf {r}} \cdot \mathbf {N} = \frac {v ^ {2}}{\lambda^ {2}} (3 v ^ {\prime} \theta^ {\prime} + v \theta^ {\prime \prime}).\tag{24}
$$

Here N is the direction normal to the tangent (rotated $\frac { \pi } { 2 }$ anti-clockwise). The signed curvature is given by

$$
\kappa (u) = \frac {\theta^ {\prime}}{\lambda}.\tag{25}
$$

The angular speed ω is given by

$$
\omega (u) = \frac {\theta^ {\prime} v}{\lambda}.\tag{26}
$$

We can use the Equations 23 and 24. to express the total discomfort

$$
J (\mathbf {r}, \tau) = \int_ {0} ^ {\tau} d t + w _ {T} \int_ {0} ^ {\tau} (\ddot {\mathbf {r}} \cdot \mathbf {T}) ^ {2} d t + w _ {N} \int_ {0} ^ {\tau} (\dddot {\mathbf {r}} \cdot \mathbf {N}) ^ {2} d t\tag{27}
$$

in terms of $v , \theta ,$ and λ. First, we express the travel time τ in terms of the primary unknowns.

$$
\tau = \int d t = \int_ {0} ^ {1} \frac {d t}{d u} d u = \int_ {0} ^ {1} \frac {\lambda}{v} d u.\tag{28}
$$

Using a similar change of variables in the integration (t → u), the total discomfort can be written as

$$
J (v, \theta , \lambda) = \int_ {0} ^ {1} \frac {\lambda}{v} d u + w _ {T} \int_ {0} ^ {1} \frac {v}{\lambda^ {3}} (v ^ {\prime 2} + v v ^ {\prime \prime} - v ^ {2} \theta^ {\prime 2}) ^ {2} d u + w _ {N} \int_ {0} ^ {1} \frac {v ^ {3}}{\lambda^ {3}} (3 v ^ {\prime} \theta^ {\prime} + v \theta^ {\prime \prime}) ^ {2} d u.\tag{29}
$$

The first integral $\left( J _ { \tau } \right)$ is the total time, the second integral $\left( J _ { T } \right)$ is total squared tangential jerk, and the third integral $\left( J _ { N } \right)$ is total squared normal jerk.

Note that except for the term due to total travel time, the primary variables v and θ and their derivatives enter the total discomfort expression polynomially.

The discomfort J is now a function of the primary unknown functions v, θ, and a scalar $\lambda ,$ the trajectory length. All references to time t have disappeared. However, once the unknowns are found via optimization, we must compute a mapping between t and u. This can be done using Equation (13).

## 6.5 Function spaces for v and θ for a finite discomfort

Now that we have a concrete expression for the discomfort J in Equation (29), it can be used to define the function spaces to which v and θ can belong so that the discomfort is well-defined (finite). This will, in turn, lead to conditions on the physical quantities for safe and comfortable motion. We have two distinct cases depending on whether the speed is zero at an end-point on not.

## Conditions for positive speeds

Let $\Omega = [ 0 , 1 ]$ and $H ^ { 2 } ( \Omega )$ be the Sobolev space of functions on Ω with square-integrable derivatives of up to order 2. Let $f : \Omega \to { \mathbb { R } }$ . Then

$$
f \in H ^ {2} (\Omega) \stackrel {{\mathrm{def}}} {{\Longleftrightarrow}} \int_ {\Omega} \left(\frac {d ^ {j} f}{d x ^ {j}}\right) ^ {2} d x <   \infty \forall j = 0, 1, 2.\tag{30}
$$

First, we show that if $v , \theta \in H ^ { 2 } ( \Omega )$ , then the integrals of squared tangential and normal jerk are finite. Using the Sobolev embedding theorem (Adams and Fournier, 2003) it can be shown that if $f \in H ^ { 2 } ( \Omega )$ then $f ^ { \prime } \in C ^ { 0 } ( \Omega )$ and by extension $f \in C ^ { 1 } ( \Omega )$ . Here $C ^ { j } ( \Omega )$ is the space of functions on Ω whose up to $j ^ { t h }$ derivatives are bounded and continuous. Thus, if $v , \theta \in H ^ { 2 } ( \Omega )$ , then all the lower derivatives are bounded and continuous. Physically this means that quantities like the speed, acceleration, and curvature are bounded and continuous − all desirable properties for comfortable motion.

Expanding all the jerk related terms in Equation (29), bounding all the non-second derivative terms by a constant using the results from the Sobolev embedding theorem, we immediately see that the jerk part of discomfort is finite if $v , \theta \in H ^ { 2 } ( \Omega )$ . This is a suficient condition only and not a necessary one as we shall see below.

We also need that the inverse of v be integrable so that $J _ { \tau }$ is finite. This is trivially true if v is uniformly positive, that is, $v \geq \overline { { v } } > 0$ for some constant positive v throughout the interval [0, 1]. However, v can be zero at one or both end-points because of the imposed conditions. Section 6.6 analyzes the boundary conditions in detail. Here we assume that speed on both end-points is positive. The cases with zero end-point speed are treated below in Section 6.5.

Thus, consider the case that v is positive on both end-points. Since v is speed and always non-negative, it can approach zero from above only. We make a justifiable assumption that v can be zero only at end-points if at all and not in the interior. Otherwise, the robot would stop and then start again. This is costly for discomfort since it increases travel time and leads to acceleration and deceleration. Of course, we can choose a motion in which $v = 0$ in the interior and it can still be a valid motion with finite discomfort. The assumption is that the trajectory that actually minimizes discomfort will not have a halt in between. Thus, if $v > 0$ on end-points, it remains uniformly positive in the interior and the discomfort is finite.

## Conditions for zero speed on boundary

Consider the case in which $v ( 0 ) = 0$ . The case $v ( 1 ) = 0$ can be treated in a similar manner. If $v ( 0 ) = 0 ,$ must not blow up faster than $\textstyle { \frac { 1 } { u ^ { p } } }$ where $p < 1$ . This is to keep $J _ { \tau }$ finite. This can be seen as follows. Lets assume $v ( u ) = u ^ { p }$ for some $p > 0$ (so that $v ( 0 ) = 0 )$ . This implies that $\begin{array} { r } { J _ { \tau } = \frac { \lambda } { 1 - p } } \end{array}$ provided $p < 1$ , otherwise it is not defined.

For simplicity, assume a 1D motion so that $\theta ( u ) \equiv 0$ . Then $\begin{array} { r } { J _ { T } = \frac { 1 } { \lambda ^ { 3 } } \frac { ( 1 - 2 p ) ^ { 2 } p ^ { 2 } } { 5 p - 3 } } \end{array}$ provided $p > { \frac { 3 } { 5 } }$ . Taking all conditions into account, if $v ( 0 ) = 0$ , the discomfort is finite if $v ( u )$ behaves like $u ^ { p }$ where ${ \frac { 3 } { 5 } } < p < 1$ However, in such a case, $\begin{array} { r } { \int _ { 0 } ^ { 1 } v ^ { \prime \prime 2 } d u = \frac { ( - 1 + p ) ^ { 2 } p ^ { 2 } } { 2 p - 3 } } \end{array}$ is defined and finite only if $p > 3 / 2$ . This conflicts with the assumption that $v \in H ^ { 2 } ( \Omega )$ . Thus, we can have a finite discomfort even if $v \not \in H ^ { 2 } ( \Omega )$ . We see that the reason for this is the zero speed boundary condition, which leads to $\begin{array} { r } { \int _ { 0 } ^ { 1 } v ^ { 3 } v ^ { \prime \prime 2 } d u } \end{array}$ being finite for $\textstyle { \frac { 3 } { 5 } } < p < 1$ even though $\begin{array} { r l } {  { \int _ { 0 } ^ { 1 } v ^ { \prime \prime 2 } d u } } \end{array}$ (which is the highest order term in $J _ { T } )$ is not finite for such a range of $p .$ .

If we look at the integral $\begin{array} { r } { J _ { T } = \frac { 1 } { \lambda ^ { 3 } } \frac { ( 1 - 2 p ) ^ { 2 } p ^ { 2 } } { 5 p - 3 } } \end{array}$ carefully, we see that it can be finite even if $\begin{array} { r } { p < \frac { 3 } { 5 } } \end{array}$ , provided $\begin{array} { r } { p = \frac { 1 } { 2 } } \end{array}$ . This is a special case because $\boldsymbol { v } \boldsymbol { v } ^ { \prime \prime } + \boldsymbol { v } ^ { \prime 2 }$ is identically zero for such a p and tangential jerk discomfort is finite for a 1-D motion.

For a mathematically meaningful problem we must treat zero speed boundary conditions separately from non-zero speed boundary condition. This analysis will be done in more detail in Sections 6.6 and 7 which are focused on boundary conditions and appropriate singular finite elements respectively.

## Summary

To summarize, the total discomfort is finite if $v , \theta \in H ^ { 2 } ( \Omega )$ and the inverse of v is integrable. Inverse of v is integrable if v is uniformly positive in [0, 1]. If zero speed boundary conditions are imposed, we will have to choose v outside $H ^ { 2 } ( \Omega )$ . In such a case, at $u = 0$ , it is suficient that v approaches zero as $u ^ { p }$ where $\textstyle { \frac { 3 } { 5 } } < p < 1$ or $\begin{array} { r } { p = \frac { 1 } { 2 } } \end{array}$ . For the right end point, where $u = 1$ , replace u with $( 1 - u )$ in the condition. We do not lose higher regularity of v throughout the interval Ω just because v /∈ $H ^ { 2 } ( \Omega )$ . Assume $v > 0$ in the interior, as justified above. Then $v \geq \overline { { v } } > 0$ in $\Omega _ { \delta } \ { \stackrel { \mathrm { d e f } } { = } } \ [ \delta , 1 - \delta ]$ where $\delta = \delta ( \overline { { v } } ) > 0$ . Thus $v \in H ^ { 2 } ( \Omega _ { \delta } )$ is necessary to keep total discomfort finite. This implies continuity and boundedness of velocity and acceleration in $\Omega _ { \delta } \forall \delta > 0$

## 6.6 Analysis of boundary conditions

The expression for the cost functional J in Equation (29) shows that the highest derivative order for v and θ is two. Thus, for the boundary value problem to be well-posed we need two boundary conditions on v and θ at each end-point − one on the function and one on the first derivative.

We also have to impose that the robot move from a specific starting point to a specific ending point. This condition is a set of two equality constraints on λ and θ based on Equation (17). If the motion is from positions $\mathbf { r } _ { 0 } \ \mathrm { t o } \ \mathbf { r } _ { \tau } .$ , then

$$
\mathbf {r} _ {\tau} - \mathbf {r} _ {0} = \lambda \left\{\int_ {0} ^ {1} \cos \theta d u, \int_ {0} ^ {1} \sin \theta d u \right\}.\tag{31}
$$

We now relate the mathematical requirement on v and θ boundary values above to expressions of physical quantities. We do this for the starting point only. The ending point relations are analogous.

## Positive speed on boundary

First, consider the case when $v > 0$ on the starting point. The speed v needs to be specified, which is quite natural. The u-derivative of $v ,$ however, is not tangential acceleration. The tangential acceleration is the t-derivative and is given by Equation (21). It is $\frac { v v ^ { \prime } } { \lambda }$ . Here v is known but λ is not. Thus specifying tangential acceleration gives us a constraint equation and not directly a value for $v ^ { \prime } ( 0 )$ . This is imposed as an equality constraint. Similarly, fixing a value for θ on starting point is natural. We “fix” the values of $\theta ^ { \prime } ( 0 )$ by fixing the signed curvature $\begin{array} { r } { \kappa = \frac { \theta ^ { \prime } } { \lambda } } \end{array}$ . As before, this leads to an equality constraint relating $\theta ^ { \prime } ( 0 )$ and λ if $\kappa \neq 0$ . Since choosing a meaningful non-zero value of $\kappa$ is dificult, it is natural to impose $\kappa = 0$ . In this case $\theta ^ { \prime } ( 0 ) = 0$ can be imposed easily.

## Zero speed on boundary

We now discuss the $v = 0$ case. If $v ( 0 ) = 0$ , then, as seen in Section 6.5, $v ( u )$ must behave like $u ^ { p }$ for $\textstyle { \frac { 3 } { 5 } } < p < 1$ or $\begin{array} { r } { p = \frac { 1 } { 2 } } \end{array}$ near $u = 0$ and $v ^ { \prime } ( u ) \sim u ^ { q }$ for $\begin{array} { r } { - \frac { 2 } { 5 } < q < 0 } \end{array}$ or $q = - \frac { 1 } { 2 }$ respectively. This means the $\scriptstyle \operatorname* { l i m } _ { u \to 0 } v ^ { \prime } ( u )$ is infinite. This leads to a dificulty in analyzing the expression for the tangential acceleration $\Big ( \frac { v v ^ { \prime } } { \lambda } \Big )$ without using limits. We prove that if $v \sim u ^ { p }$ at boundary, then the tangential acceleration is 0 if $\textstyle { \frac { 3 } { 5 } } \ C p < 1$ and it is finite but non-zero if $\begin{array} { r } { p = \frac { 1 } { 2 } } \end{array}$ . If $v ( u ) \sim u ^ { p }$ , then, $v v ^ { \prime } \sim u ^ { 2 p - \smile }$ . If $\textstyle { \frac { 3 } { 5 } } < p < 1$ , it means $\begin{array} { r } { \frac { \mathtt { I } } { 5 } < 2 p - 1 < 1 } \end{array}$ . Thus as $u  0 , v v ^ { \prime }  0$ because of the allowable range of $p .$ If $\begin{array} { r } { p = \frac { 1 } { 2 } } \end{array}$ , vv<sup>0</sup> behaves like a positive constant as $u \to 0$ . Hence $\begin{array} { r } { p = \frac { 1 } { 2 } } \end{array}$ corresponds to non-zero tangential acceleration.

We still have to decide with what strength does $v ^ { \prime } ( u )$ tend to infinity at an end-point. If $v = 0$ and $a \neq 0$ , it is clear that $v ^ { \prime } ( u ) \sim u ^ { - 1 / 2 }$ . If $v = 0$ and $a = 0$ , the analysis above has only shown that lim $\iota _ { u  0 } v ( u ) v ^ { \prime } ( u ) = 0$ and l $\scriptstyle \operatorname* { i m } _ { u \to 0 } v ^ { \prime } ( u ) = \infty$ . In this case, we need to use the time domain. The reason we have such a singularity is because of working in the arc-length domain. Consider starting from origin with zero speed and acceleration at zero time (t) in 1D. Expanding the distance traveled (s) as a function of time, we see that

$$
s (t) = 0 + 0 t + \frac {1}{2} 0 t ^ {2} + \frac {1}{6} j t ^ {3} + \dots .
$$

Here $j > 0$ is the jerk at $t = 0$ . We ignore the higher order terms. Then, to the lowest power of $t ,$ the speed as a function of t is

$$
v (t) = \frac {1}{2} j t ^ {2}.
$$

Eliminating t to relate v and s, we get

$$
v = \frac {6 ^ {2 / 3}}{2} j ^ {1 / 3} s ^ {2 / 3}.
$$

Now $s = \lambda u$ because u is the scaled arc-length parameter. Using this we get $v = C u ^ { 2 / 3 }$ , where all the constants are absorbed in C. Thus, $v ( u ) \sim u ^ { p }$ for $\textstyle p = { \frac { 2 } { 3 } }$ . This value of $p$ is within the acceptable range of $p ,$ the open interval $\textstyle { \left( { \frac { 3 } { 5 } } , 1 \right) }$ . This also tells us that

$$
v ^ {\prime} (u) \sim u ^ {- 1 / 3}\tag{32}
$$

is the appropriate strength of the singularity.

## Summary

To summarize, we must specify following boundary conditions at both end points: position, orientation, curvature, and speed. If a specified speed is non-zero, the tangential acceleration must be specified. If the speed is zero, the tangential acceleration can be zero. If tangential acceleration is non-zero, it must be positive if it is the starting point or must be negative if it is the ending point.

![](Gulati2013Nonlinear_figs/609f8260e291570e29e5c25518a81577d656f3aca5abe0887606f05ded715b75.jpg)  
Figure 3: Notation for star-shaped obstacles.  
A non-convex star-shaped obstacle is shown with its “center” {x<sub>0</sub>, y<sub>0</sub>} and a distance function $\rho = \rho ( \phi )$ . The distance function gives a single point on the boundary for $\phi \in [ 0 , 2 \pi ]$ . The robot trajectory must lie outside the obstacle.

## 6.7 Obstacle avoidance

For safe motion, it is necessary that the robot avoid obstacles while navigating. Simply speaking, obstacles are regions in the plane of motion through which the geometric path must not pass. Obstacles can be represented in a variety of ways. For example, convex polygons, rectangular cells, simple closed shapes like ellipses, or level sets of implicitly defined simple functions of two arguments are some possibilities.

## Modeling obstacles as star-shaped domains

We have chosen to model the “forbidden” region formed by the obstacles as a union of star-shaped domains with boundaries that are closed curves with piecewise continuous second derivative. A set in $\mathbb { R } ^ { n }$ is called a star-shaped domain if there exists at least one point $\mathbf { x } _ { \mathrm { 0 } }$ in the set such that the line segment connecting x<sub>0</sub> and x lies in the set for all x in the set. Intuitively this means that there exists at least one point in the set from which all other points are “visible”. We will refer to such a point $\mathbf { x } _ { \mathrm { 0 } }$ as a center of the star-shaped domain.

The choice of using star-shaped domains is made so that each point on the boundary of an obstacle can be treated as coming from a well-defined function in polar coordinates centered within the particular obstacle. See Figure 3. This also allows treatment of non-convex obstacles without subdividing them into a union of convex shapes. A big advantage is that we reduce the number of imposed constraints since the number of inequality constraints is proportional to the number of obstacles. This leads to a faster optimization process.

This approach is a special case of using level sets of an implicitly defined function as an obstacle boundary. What is diferent here is that given the description of the boundary in polar coordinates, which is easy to specify for common shapes, we construct an implicit function (see the following section). This is done based on the assumption that the boundary encloses a star-shaped region. The piecewise smoothness property is required to impose the obstacle constraint in a numerical optimization method. Since up to second derivative of constraint can be required, the obstacle boundary should also be smooth to that order (or at least piecewise smooth).

If an obstacle is not star-shaped, our framework can still handle it if it can be expressed as a finite union of piecewise smooth star-shaped domains. Eficient algorithms to decompose any polygon into a finite number of star-shaped polygons exist (Avis and Toussaint, 1981).

## Incorporating constraints for obstacle avoidance

We now derive a function for the inequality constraint that a given point in the plane is not inside the boundary of one star-shaped obstacle. It is easy to extend this to multiple points and multiple obstacles by just repeating the inequality with diferent parameters.

Let an obstacle be specified by its boundary in polar coordinates that are centered at $\mathbf { r } _ { 0 } = \{ x _ { 0 } , y _ { 0 } \}$ . Each $\phi \in [ 0 , 2 \pi )$ gives a point on the boundary using the distance $\rho ( \phi )$ from the obstacle origin. The distance function $\rho$ must be periodic with a period $2 \pi$ . See Figure 3.

Suppose we want a point $\mathbf { r } = \{ x , y \}$ to be outside the obstacle boundary. Define $C ( \mathbf { r } )$ as

$$
C (\mathbf {r}) = | | \mathbf {r} - \mathbf {r} _ {0} | | _ {2} - \rho (\arctan 2 (\mathbf {r} - \mathbf {r} _ {0}))\tag{33}
$$

where the subscript 2 refers to the Euclidean norm. It is obvious that $C ( \mathbf { r } ) \geq 0 \iff$ the point r is outside the obstacle. This can be seen using a 1D graph of $\rho ( \phi )$ . For example, let an obstacle be represented as shown in Figure $4 ( \mathrm { a } )$ . Figure 4(b) shows the same obstacle flattened out as a 1D curve. Then $C ( \mathbf { r } )$ is positive in the top region and negative below. The star-shaped property leads to a single-valued curve $\rho ( \phi )$ when flattened like this. The vector r is related to the primary variables in our optimization problem using Equation (17).

## Derivatives of obstacle avoidance constraint

We will need derivatives of $C ( \mathbf { r } )$ with respect to r for incorporating $C ( { \bf r } ) \ge 0$ as a constraint in the trajectory optimization problem. Here r is any point on the path that we want to lie outside a given obstacle. We can derive the following expressions for first and second derivatives of $C ( \mathbf { r } )$ . The derivatives of $\rho$ below are evaluated at $\phi = \arctan 2 ( \mathbf { r } - \mathbf { r } _ { 0 } )$ . To simplify the expressions, $x , y ,$ r refer to the ofsets from obstacle origin $\mathbf { r } _ { 0 }$ instead of absolute positions in the plane.

$$
\frac {\partial C}{\partial \mathbf {r}} = \frac {\mathbf {r}}{| | \mathbf {r} | | _ {2}} - \rho^ {\prime} (\phi) \frac {\{- y , x \}}{| | \mathbf {r} | | _ {2} ^ {2}}\tag{34}
$$

$$
\frac {\partial^ {2} C}{\partial \mathbf {r} ^ {2}} = \frac {1}{| | \mathbf {r} | | _ {2} ^ {3}} \left(1 - \frac {\rho^ {\prime \prime} (\phi)}{| | \mathbf {r} | | _ {2}}\right) \left[ \begin{array}{c c} y ^ {2} & - x y \\ - x y & x ^ {2} \end{array} \right] - \frac {\rho^ {\prime} (\phi)}{| | \mathbf {r} | | _ {2} ^ {4}} \left[ \begin{array}{c c} 2 x y & y ^ {2} - x ^ {2} \\ y ^ {2} - x ^ {2} & - 2 x y \end{array} \right]\tag{35}
$$

Obviously, the second derivative is a $2 \times 2$ matrix.

The constraint function $C ( \mathbf { r } )$ is piecewise diferentiable for all r except at a single point $\mathbf { r } = \mathbf { r } _ { 0 }$ . If $\mathbf { r } = \mathbf { r } _ { 0 }$ by chance, which is easily detectable, we know that the r is inside the obstacle and can perturbed to avoid this undefined behavior. Note that $C ( \mathbf { r } )$ remains bounded inside the obstacle. It is the derivatives that are not bounded as $\mathbf { r }  \mathbf { r } _ { 0 }$ Figure $4 ( \mathrm { c } )$ shows a surface plot of $C ( \mathbf { r } )$ for the obstacle shown in Figure $4 ( \mathrm { a } )$ . The contours of constant values are shown in Figure 4(d).

## Incorporating robot shape

The discussion on obstacle avoidance constraints so far has assumed that the robot is a point. In reality, the robot is not a point. To impose obstacle avoidance constraints in this case, the robot can be modeled as a closed curve that encloses the projection of its boundary in the plane of motion. We can choose a set of points on this curve and impose the constraint that all these points be outside all obstacles. The distance between any pair of points can be smaller than the smallest obstacle. We have currently not implemented this and this is part of future work.

![](Gulati2013Nonlinear_figs/6d393457d919bf47b4854a87b7c50a59cf865d1c9c05623e8ed4448bb63d642c.jpg)  
(a) Obstacle shape

![](Gulati2013Nonlinear_figs/8f488fab46c640e920c6c45a8d81d323d4120aadf411a30e8ac8879a4fe266f6.jpg)  
(b) Obstacle as a 1-D curve

![](Gulati2013Nonlinear_figs/aeaf870d3a2a62ab9895120520ab830c994569f7cc48deb279c44667d134b4ad.jpg)  
(c) Surface plot of constraint

![](Gulati2013Nonlinear_figs/3139d47827dbd6bda3be1daae10011f5cb9af22586a9c196ef6b2a1bc76d6993.jpg)  
(d) Level sets of constraint  
Figure 4: Obstacle and constraint plots.

The figures show an obstacle in polar coordinates in (a), and its 1-D representation in (b). The region with darker shade is the interior and a feasible trajectory must not pass through it. The surface plot of the corresponding constraint function $C ( \mathbf { r } )$ of Equation (33) is shown in (c) and its level set is shown in (d). The arrow marks the zero level set, which is the obstacle boundary.

## 6.8 The full nonlinear constrained optimization problem

We now summarize the nonlinear and constrained trajectory optimization problem taking into account all input parameters, all the boundary conditions, and all the constraints. This is the “functional” form of the problem (posed in function spaces). We will present an appropriate discretization procedure valid for all input combinations in the next chapter.

Minimize the discomfort functional J, where

$$
J (v, \theta , \lambda) = \int_ {0} ^ {1} \frac {\lambda}{v} d u + w _ {T} \int_ {0} ^ {1} \frac {v}{\lambda^ {3}} (v ^ {\prime 2} + v v ^ {\prime \prime} - v ^ {2} \theta^ {\prime 2}) ^ {2} d u + w _ {N} \int_ {0} ^ {1} \frac {v ^ {3}}{\lambda^ {3}} (3 v ^ {\prime} \theta^ {\prime} + v \theta^ {\prime \prime}) ^ {2} d u,
$$

given the following boundary conditions for both starting point and ending point

• position $( \mathbf { r } _ { 0 } , \mathbf { r } _ { \tau } )$ ，

• orientation $( \theta _ { 0 } , \theta _ { \tau } )$ ，

• signed curvature $\left( \kappa _ { 0 } , \kappa _ { \tau } \right)$

• speed $( v _ { 0 } \geq 0 , v _ { \tau } \geq 0 )$

• tangential acceleration $( a _ { T , 0 } , a _ { T , \tau } )$

and constraints on allowable range of

• speed $( v _ { m i n } = 0 , v _ { m a x } )$

• tangential acceleration $( a _ { T , m i n } , a _ { T , m a x } )$ 44

• normal acceleration $\left( a _ { N , m i n } , a _ { N , m a x } \right)$ ，

• angular speed $( \omega _ { m i n } , \omega _ { m a x } )$

• curvature, if necessary $( \kappa _ { m i n } = 0 , \kappa _ { m a x } )$

and

• number of obstacles $N _ { o b s }$

• locations of obstacles $\{ { \mathbf { c } } _ { i } \} _ { i = 1 } ^ { N _ { o b s } }$

• representation of obstacles that allows computation of $\{ \rho _ { i } ( \phi ) \} _ { i = 1 } ^ { N _ { o b s } }$ , for $\phi \in [ 0 , 2 \pi )$

and

• an initial guess for $( v ( u ) , \theta ( u ) , \lambda )$ , in $u \in [ 0 , 1 ]$ 2

• weights $w _ { T } > 0$ and $w _ { N } > 0$

![](Gulati2013Nonlinear_figs/87f6ad7b25da5fa648c7427eae56f1034d5c601c2a74951abdd6a6be68a3f462.jpg)  
Figure 5: Finite-element mesh for the optimization problem.

The figure at the top shows the finite-element mesh consisting of n elements and $n + 1$ nodes. There are 4 primary unknowns at each node – speed, orientation, and their derivatives with respect to the scaled-arc length parameter u. The figure on the bottom left shows how dynamic constraints are imposed. P points are chosen in the interior of each element, and speed, angular speed, curvature, and tangential and normal accelerations are computed at each of these points in terms of the primary unknowns. Bounds are then imposed as constraints on these computed values. The figure on the bottom right shows how obstacle constraints are imposed. Addition variables $( x , y )$ representing position are introduced at M points in the interior of each element and at each node. Each $( x , y )$ pair is related to each of its neighboring pairs by a constraint. For obstacle avoidance, a constraint is imposed on each $( x , y )$ pair so that it is stays outside all obstacles.

The constraint on starting and ending position requires that

$$
\mathbf {r} _ {\tau} - \mathbf {r} _ {0} = \lambda \left\{\int_ {0} ^ {1} \cos \theta d u, \int_ {0} ^ {1} \sin \theta d u \right\}
$$

Staying outside all obstacles requires that

$$
\left| \left| \mathbf {r} (u) - \mathbf {c} _ {i} \right| \right| _ {2} - \rho_ {i} (\arctan 2 (\mathbf {r} (u) - \mathbf {c} _ {i})) \geq 0 \forall i \in 1, \dots , N _ {\text { obs }}, \text { and } \forall u \in [ 0, 1 ]
$$

where

$$
\mathbf {r} (u) = \mathbf {r} (0) + \lambda \left\{\int_ {0} ^ {u} \cos \theta d u, \int_ {0} ^ {u} \sin \theta d u \right\}.
$$

As a post-processing step, we compute time t as a function of u using

$$
t = t (u) = \int_ {0} ^ {u} {\frac {\lambda}{v (u)}} d u
$$

and convert all quantities $( v , \theta , \mathbf { r } ,$ , and their derivatives) from u domain to t domain.

## 7 Numerical solution

The optimization problem posed in Section 6.8 is infinite dimensional since it is posed on infinite dimensional function spaces. This means that we must discretize it as a finite dimensional problem before it can be solved numerically. We saw in Section 6.6 that we must be able to impose two kinds of boundary conditions. In the first kind, the problem is set in the Sobolev space of functions whose up to second derivatives are square integrable. In the second kind, we must allow functions that are singular at the boundary (with a known strength) but still lie in the same Sobolev space in the interior. Keeping the problem setting and requirements mentioned above in mind, it is natural to use the Finite Element Method (FEM) to discretize it.

For the first kind of boundary conditions, where speed is non-zero at both boundaries, $v ( u )$ must belong to $H ^ { 2 } ( \Omega )$ . It is natural to use the basis functions in $C ^ { 1 } ( \Omega )$ , the space of functions that are continuous and have continuous first derivatives. In accordance with standard FEM practice (Hughes, 2000), we choose the cubic Hermite shape functions to discretize $v ( u )$ . For the second kind of boundary conditions, when either one or both the boundary points have zero speed specified, we must allow functions that are singular at the boundary (with a known strength) but still belong to $H ^ { 2 } ( \Omega )$ in the interior. We use special shape functions for $v ( u )$ on the boundary element where speed is zero so that $v ( u )$ has the appropriate strength of singularity at the boundary, and use regular cubic Hermite shape functions in the interior. For both kinds of boundary conditions, we use cubic Hermite shape functions for $\theta ( u )$ on all elements.

With the above choice of shape functions, an n element mesh for the problem consists of the following unknowns at each node – $v , v ^ { \prime } , \theta , \theta ^ { \prime }$ resulting in a total of $4 ( n + 1 )$ unknowns. In addition, the path length λ is also an unknown. For optimization, the values of the objective function, its gradient and Hessian, the values of constraints, and the gradient and Hessian of each constraint are required. For eficiency, it is desirable that objective function and constraint Hessians be sparse. We show in the second paper of this series that the Hessian of obstacle avoidance constraints can be kept sparse if we introduce 2N additional unknowns in the form of position $\mathbf { r } ( u _ { i } ) \ = \ \{ x ( u _ { i } ) , y ( u _ { i } ) \} _ { i = 1 } ^ { N }$ at N points on the mesh and a constraint $\begin{array} { r } { \mathbf { r } ( u _ { i } ) - \mathbf { r } ( u _ { i - 1 } ) = \lambda \left\{ \int _ { u _ { i - 1 } } ^ { u _ { i } } \cos \theta d u , \int _ { u _ { i - 1 } } ^ { u _ { i } } \right. } \end{array}$ sin $\theta d u \}$ between each pair of $\mathbf { r } ( u _ { i - 1 } )$ and $\mathbf { r } ( u _ { i } )$ . We 1 choose uniformly separated N points and let $N = n M + \bar { ( n ^ { . } + 1 ) }$ so that obstacle avoidance constraints are imposed at M points in the interior of each element and at each of the $n + 1$ nodes.

With the discretization above, the infinite dimensional problem of Section 6.8 is converted into a finitedimensional nonlinear constrained optimization problem. The objective now is to determine the values of the $4 ( n + 1 ) + 2 N + 1$ unknowns that minimize the discomfort cost functional and satisfy the boundary conditions and constraints described in (Section 6.8). To impose boundary conditions, we impose constraints on some of the degrees of freedom and eliminate some of the degrees of freedom at the end points. To impose dynamic constraints, we compute the speed v, tangential acceleration $a _ { T }$ , normal acceleration $a _ { N } .$ , angular speed ω, and curvature κ in terms of the unknowns at $P$ points in the interior of each element and impose bounds on these quantities as constraints. See Figure 5.

To numerically compute the integrals in the cost functional and constraints, we use Gauss quadrature formulas with 12 integration points. In our implementation, the number of elements in the finite element mesh, $n = 3 2$ , number of intervals per element for obstacle avoidance constraints, $M = 2 0$ , the number of points per element on which to impose dynamic constraints $P = 1 2$ . The rationale for choosing these particular values is discussed in the second paper in this series.

## 8 Initial guess for the optimization problem

Because of the non-linearity in the optimization problem, and the presence of both inequality and inequality constraints, it is crucial that a suitable initial guess of the trajectory be computed and provided to an optimization algorithm. Many software packages can generate their own “starting points”, but a good initial guess that is within the feasible region can easily reduce the computational efort (measured by number of function and derivative evaluation steps) many times. Not only that, reliably solving a nonlinear constrained optimization problem without a high quality initial guess can be extremely dificult. Because of these reasons, we invest considerable mathematical and computational efort to generate a high quality initial guess of the trajectory.

Our optimization problem is to find the scalar λ and the two functions θ and v that minimize the discomfort. We compute the initial guess of trajectory by computing λ and θ first and then computing v by solving a separate optimization problem. We emphasize that the initial guess computation process must deal with arbitrary inputs and reliably compute the initial guesses.

## 8.1 Initial guess of path

To compute initial guess for $\theta ( u )$ and λ for any pair of specified initial and final orientations $( \theta _ { 0 } , \theta _ { \tau } )$ , we solve an auxiliary (but simpler) nonlinear constrained optimization problem for the four pairs of orientations $( \theta _ { 0 } , \theta _ { \tau } ) , ( \theta _ { 0 } , \theta _ { \tau } ) , ( \theta _ { 0 } , \theta _ { \tau } + 2 \pi )$ , and $( \theta _ { 0 } , \theta _ { \tau } - 2 \pi )$ . We minimize

$$
J (\theta , \lambda) = \lambda + w \int_ {0} ^ {1} \theta^ {\prime \prime 2} d u\tag{36}
$$

where $w : = \operatorname* { m a x } ( \Delta L , R )$ , and $\theta$ must satisfy the boundary conditions, the two equality constraints of Equation (31), and the curvature constraint $| \theta ^ { \prime } ( u ) | \leq \lambda \kappa _ { \operatorname* { m a x } } \forall u \in [ 0 , 1 ]$ . We do not impose obstacle related constraints in this problem. Here $\Delta L$ is the distance between start and end positions and R is the minimum allowed radius of curvature. Note that this is a geometric and time is absent.

This method of computing four diferent initial guesses is based on a special kind of non-uniqueness of paths. This particular kind of non-uniqueness arises because a single physical orientation $\theta$ can correspond to multiple numerical values of $\textsf { ) } \left( \theta \pm 2 n \pi \ \forall n \in \mathbb { N } \right)$ . This is because θ is continuous and cannot jump to a diferent value in between. Of course, this optimization problem needs its own initial guess, and we use paths similar to Dubins curves to compute a suitable initial guess. Our method generates two diferent initial guesses for the auxiliary problem for the pair $( \theta _ { 0 } , \theta _ { \tau } )$ , leading to 4 initial guesses of $\theta ( u )$ for the discomfort minimization problem. λ is the length of the paths computed above. The non-uniqueness in paths and the computation of initial guess is discussed in greater detail in the second paper (Part II) of this series.

## 8.2 Initial guess of speed

For the case when both end-points have non-zero speed, we compute initial guess of $v ( u )$ by solving an auxiliary optimization problem. We minimize

$$
J (v) = \int_ {0} ^ {1} v ^ {\prime \prime 2} d u\tag{37}
$$

subject to boundary constraints $\begin{array} { r } { v ( 0 ) = v _ { 0 } > 0 , v ( 1 ) = v _ { 1 } > 0 , v ^ { \prime } ( 0 ) = \frac { a _ { 0 } \lambda } { v _ { 0 } } , v ^ { \prime } ( 1 ) = \frac { a _ { 1 } \lambda } { v _ { 1 } } } \end{array}$ and inequality constraints $v _ { \operatorname* { m i n } } ( u ) \leq v ( u ) \leq v _ { \operatorname* { m a x } } ( u )$ and $A _ { \operatorname* { m i n } } ( u ) \leq v ^ { \prime } ( u ) \leq A _ { \operatorname* { m a x } } ( u )$ . The expressions for v<sup>0</sup>(0) and $v ^ { \prime } ( 1 )$ come from the relation in Equation (21). The length λ is computed when the initial guess for $\theta$ is computed Here we choose $v _ { \mathrm { m i n } } ( u ) = \mathrm { m i n } ( v _ { 0 } , v _ { 1 } ) / 2$ and $v _ { \mathrm { m a x } } ( u )$ is a constant that comes from the hardware limits. The function $A _ { \mathrm { m i n } } ( u )$ is chosen to be the constant $1 0 a _ { \mathrm { m i n } } \lambda / \operatorname* { m i n } ( v _ { 0 } , v _ { 1 } )$ where $a _ { \mathrm { m i n } }$ is the minimum allowed physical acceleration. $A _ { \mathrm { m a x } } ( u )$ is chosen similarly using $a _ { \mathrm { m a x } }$

If both end-points have zero speeds, the function

$$
v (u) = v _ {\mathrm{max}} \left(4 u (1 - u)\right) ^ {2 / 3}\tag{38}
$$

satisfies the boundary conditions and singularities and has a maximum value of $v _ { \mathrm { m a x } }$ . This case does not require any optimization.

If only one of the end-points has a zero speed boundary condition, we split the initial guess for v into a sum of two functions. The first one takes care of the singularity and the second takes care of the non-zero speed boundary condition on the other end-point. We now maintain only the $v _ { \mathrm { m a x } }$ constraint because $v ^ { \prime } ( u )$ is unbounded and $v _ { \operatorname* { m i n } } = 0$ naturally. If the right end-point has zero speed, we choose

$$
v (u) = v _ {\mathrm{singular}} (u) + v _ {\mathrm{non-singular}} (u)\tag{39}
$$

where

$$
v _ {\mathrm{singular}} (u) = \frac {1 6}{9} 2 ^ {1 / 3} v _ {\mathrm{max}} u ^ {2} (1 - u) ^ {2 / 3}.\tag{40}
$$

This function has the correct singularity behavior and its maximum value is $v _ { \mathrm { m a x } } / 2$ . The non-singular part is computed via optimization so that the sum is always less than $v _ { \mathrm { m a x } }$ . For the other case, when left end-point has zero speed, the singular part (using symmetry) is

$$
\frac {1 6}{9} 2 ^ {1 / 3} v _ {\mathrm{max}} (1 - u) ^ {2} u ^ {2 / 3}.
$$

## 8.3 Summary

For any given pair of orientations, we compute four initial guesses of path $\theta ( u )$ and corresponding path lengths λ. To compute initial guess of speed $v ( u )$ , we treat zero speed and non-zero speed boundary conditions diferently. When speed is zero at both ends, we use Equation (38). When speed is non-zero at either ends, we use Equation (39). In this case, we compute $v _ { \mathrm { n o n - s i n g u l a r } } ( u )$ by solving the optimization problem Equation (37). In this case, four initial guesses of speed are computed corresponding to each guess of λ.

## 9 Evaluation and results

The motion planning framework described in this paper is expected to reliably plan trajectories for diferent types of boundary conditions. These trajectories should satisfy dynamic constraints and the corresponding geometric paths should not intersect obstacles. Further, this framework should reliably compute trajectories between a given pair of boundary conditions for a range of weights, $w _ { T }$ and $w _ { N } ,$ , so that users can customize the motion by changing these weights. In the following discussion, we refer to optimization problem of Section 6.8 as the discomfort minimization problem.

We begin by describing the input to the discomfort minimization problem. Some quantities in the input such as dynamic bounds are fixed, while others such as boundary conditions and obstacle locations and shapes are problem dependent. We also provide some implementation details

Next, we present illustrative examples showing the various steps of the solution method, and demonstrate some of the strengths of our method such as the ability to plan trajectories for a wide variety of boundary conditions and obstacle shapes.

We then analyze how varying the weight factors $f _ { T }$ and $f _ { N }$ afect the solution trajectory. Our objective is to find qualitative relationships between these weight factors and each of the terms in the discomfort measure (total travel time, integral of squared tangential jerk, and integral of squared normal jerk). These relationships should provide guidelines for user customization.

Next, to evaluate the reliability of our method, we construct a set of problems by varying boundary conditions and find the success rate. We also analyze the run-time and number of iterations to solve the discomfort minimization problem.

## 9.1 Experimental setting

The input to the discomfort minimization problem described in Section 6.8 consists of:

1. Number of elements, n, for finite element discretization. We choose $n = 3 2$ based on a numerical experiment based on convergence to the “exact” solution of the infinite dimensional optimization problem as the maximum finite element size is reduced. Details are in the second paper (Part II) of this series.

2. Number of intervals per element M, to compute the $\{ x , y \}$ pairs for imposing obstacle constraints (see Section 6.7 and Section 7). We choose $M = 2 0$ when obstacles are present, otherwise the choice is irrelevant.

3. Values of bounds on curvature, speed, angular speed, tangential acceleration, and normal acceleration (See Section 6.8). Curvature bound should be determined from the robot’s geometry. We choose the value for a typical assistive wheelchair. While we assume a point robot and do not consider robot shape for obstacle-avoidance, we do include curvature constraints based on the dimensions of a typical wheelchair. All other bounds should be chosen for comfort. In the absence of relevant comfort studies for assistive robots, we choose bounds on linear and angular speed based on our experience with an intelligent wheelchair (Gulati and Kuipers, 2008; Gulati et al., 2009; Murarka et al., 2009) and studies of comfort in ground vehicles (see Section 2.1). All these values are shown in Table 1.

<table><tr><td>Quantity</td><td>Lower Bound</td><td>Upper Bound</td></tr><tr><td>Curvature (1/m)</td><td>-1.8</td><td>1.8</td></tr><tr><td>Speed (m/s)</td><td>0.0</td><td>3.0</td></tr><tr><td>Angular speed (rad/s)</td><td>-1.57</td><td>1.57</td></tr><tr><td>Tangential acceleration (m/s $^2$ )</td><td>-1.0</td><td>1.0</td></tr><tr><td>Normal acceleration (m/s $^2$ )</td><td>-1.0</td><td>1.0</td></tr></table>

Table 1: Lower and upper bounds on curvature, speeds, and accelerations used in experiments. Curvature bounds are based on a minimum turning radius of 0.55 m.

4. Non-dimensional multiplying factors for weights, $f _ { T } > 0$ and $f _ { N } > 0$ . Both these values are set to 1 unless mentioned otherwise.

5. Representation of obstacles as star-shaped domains with piecewise $C ^ { 2 }$ boundary (see Section 6.7). In our experiments, we use circular, elliptical, and star-shaped polygonal obstacles. See Figures 11 and 12.

6. Boundary conditions on position, orientation, curvature, speed and tangential acceleration (see Section 6.6). These are problem specific and we describe these for each of the experiments.

We have implemented our code in C++. We use Ipopt, a robust large-scale nonlinear constrained optimization library (W¨achter and Biegler, 2006), also written in C++, to solve the optimization problem. We explicitly compute gradient and Hessian for the optimization problem in our code instead of letting Ipopt compute these using finite diference. This leads to greater robustness and faster convergence. We set the Ipopt parameter for relative tolerance as $1 0 ^ { - 8 }$ and set the maximum number of iterations to 500.

After optimization, the outputs are the nodal values of $v , v ^ { \prime } , \theta _ { : }$ , and $\theta ^ { \prime } { } _ { ; }$ , and the curve length λ (see Section 7). The functions $v ( u )$ and $\theta ( u ) , u \in [ 0 , 1 ]$ are known in terms of these nodal values. We use Equation (13) to construct a table of u values for $u \in [ 0 , 1 ]$ and the corresponding t values for $t \in [ 0 , \tau ]$ . The value of any of the quantities of interest (orientation, speed, etc.) at any time $t \in [ 0 , \tau ]$ is computed using this table by linear interpolation.

## 9.2 Illustrative examples

We begin by presenting an example that illustrates the optimization process. In Figure 6, the initial position is {0, 0} and final position is $\{ - 1 , - 4 \}$ . The initial and final orientations are both zero. The speed and tangential acceleration at both ends are also zero.

First, four initial guesses of path $( \theta ( u ) , u \in [ 0 , 1 ]$ and λ) are computed as described in Section 8.1. These four initial guesses are shown in Figure 6. The first two guessed have $\theta _ { \tau } = 0$ , the third guess has $\theta _ { \tau } = - 2 \pi$ and the fourth guess has $\theta _ { \tau } = 2 \pi$ . An initial guess of speed, $v ( u )$ , is computed as described in Section 8.2. In this example, speed at both ends is zero and hence $v ( u )$ is computed using Equation (38). Thus we get the same function $v ( u )$ for all guesses of path. See Figure 7.

The discomfort minimization problem is solved for each of these four initial guesses. The four solution paths that minimize discomfort are shown in Figure 8. The travel time and costs for the four solution paths are shown in Table 2. The path corresponding to Solution 1 has the minimum cost, and is thus in agreement with our intuitive notion of the best path among these four. Notice the circular arcs at the start and end of the path of Solution 2. These arcs have a constant radius equal to the minimum turning radius of the robot because of curvature constraints. If curvature constraints are not imposed, these arcs have a smaller radius and the path has a smaller length. Note that it is not always true that all four solutions are distinct since two or more problems starting from diferent initial guesses may converge to the same solution.

The solution speeds are shown in Figure 9. The final speeds in Solution 1 and Solution 2 are symmetric about $\begin{array} { r } { t = \frac { \tau } { 2 } } \end{array}$ because of the inherent “symmetry” due to zero orientation, speed, and acceleration at both ends. The final speeds in Solution 3 and Solution 4 are mirror images of each other about $\begin{array} { r } { t = \frac { \tau } { 2 } } \end{array}$ because the final orientations in these two are $- 2 \pi$ and 2π respectively. The figures also show that the initial guesses of the paths and speeds are quite good, which is important for nonlinear optimization.

In Figure 10, we introduce five elliptical obstacles for the same boundary conditions. All four initial guesses of path and solution paths are shown. The initial guesses of path and speed do not consider obstacles and hence are identical to those in Figures 8 and 9 respectively. Four distinct solution paths are found. The travel time and total cost for all four solutions is shown in Table 3, and is greater than for the problem of Figure 8 (see Table 2). The minimum cost path is that of Solution 1 which again agrees with our intuition. Notice how the path of Solution 3 passes above the lowermost elliptical obstacle, while the path of Solution 4 passes below the uppermost elliptical obstacle. Our experience with this and other examples shows that once the optimization algorithm takes a step that brings an iterate to one side of the obstacle, further iterations keep it on the same side. We believe that this is because paths passing an obstacle on diferent “sides” cannot be transformed to each other via a continuous deformation of the path and lie in disjoint feasible regions. The iterates in the optimization process cannot jump from one feasible region to a diferent feasible region in general.

![](Gulati2013Nonlinear_figs/d1522a16977a1cdde67d6aced6a4bddbe44aa8a728494fa9e804539e57005c25.jpg)

![](Gulati2013Nonlinear_figs/b2b4c7dbaef6b948366f86ffa88841cac03c1a9296bc133d88d7200fcbf0b074.jpg)

![](Gulati2013Nonlinear_figs/2b616ed63123a3b2620fe969223be516c438a0f12de253f3b26bdb93ac35f58b.jpg)

![](Gulati2013Nonlinear_figs/e2afd649ca9744244a5b82abe7cedf5f4fe9b27606a1e73bf566bd5eb0fe23e5.jpg)  
Figure 6: Four initial guess of path.

Problem input is as follows: initial $\mathrm { p o s i t i o n } = \{ 0 , 0 \}$ ， $\mathrm { o r i e n t a t i o n } = 0 ,$ speed = 0, tangential acceleration $= 0 ;$ final $\mathrm { p o s i t i o n } = \{ - 1 , - 4 \}$ , orientation = 0, speed = 0, tangential acceleration = 0. The four initial guesses of path are computed using the method described in Section 8.1 so that final orientation in $( \mathrm { a } ) , ( \mathrm { b } ) , ( \mathrm { c } )$ and (d) is $0 , 0 , - 2 \pi$ and 2π respectively. All quantities have appropriate units in terms of meters and seconds. Initial and final positions are shown by markers and orientations are indicated by arrows. While the path is parameterized by u, for ease of visualization, we show markers at equal intervals of time. Thus distance between markers is inversely proportional to speed.

![](Gulati2013Nonlinear_figs/d50763c6df84e5511d862d8699d3faa5d9b3bb3c34393dbe03b258c0f532518a.jpg)  
Figure 7: Initial guess of speed for problem of Figure 6.

In this case, because of zero speed boundary condition on both ends, the same initial guess of speed is produced for 2.5 2.5each path guess. When speed is non-zero on one or both ends, four distinct guesses of speed may be produced.

![](Gulati2013Nonlinear_figs/3057d36650287068cae151cbd78b48f72277e57b52d9166784e61b52f9179303.jpg)

![](Gulati2013Nonlinear_figs/f84251f55ba8fdbb0bcfb7abd5abcc39a70507830e0fd6fa7d021bf12f5cafff.jpg)

![](Gulati2013Nonlinear_figs/8ff59198447a367dd9cbb469c58506182784127a1876f1213fa1ea476473b272.jpg)

![](Gulati2013Nonlinear_figs/116a104261a79daf97ee1893626eb0a9626bfc90eda88c9459e644825ee4bf2c.jpg)  
Figure 8: Solution paths of the problem of Figure 6.

Final (optimal) path for each solution is shown as solid curve. Initial guess is shown as dashed curve. The number of DOFs for the discomfort minimization problem were 1403 and number of constraints were 3232. The total cost and travel time for the four solutions are shown in Table 2.

![](Gulati2013Nonlinear_figs/97102d2b0574a2aab431712365439b4fa8af16725cc0b9942d227508d7ceb1d1.jpg)  
Figure 9: Solution speeds of the problem of Figure 6.  
Final (optimal) speed for each solution is shown as the solid curve. Initial guess is shown as the dashed curve.

<table><tr><td>Solution Number</td><td>Travel time (s)</td><td>Total cost (s)</td></tr><tr><td>1</td><td>6.3</td><td>6.5</td></tr><tr><td>2</td><td>10.0</td><td>11.0</td></tr><tr><td>3</td><td>7.9</td><td>8.0</td></tr><tr><td>4</td><td>7.9</td><td>8.0</td></tr></table>

Table 2: Travel time and total cost for problem of Figure 6.

![](Gulati2013Nonlinear_figs/c9a700316407417389a488966e8f653c855fe8e39f5e8ed45d6df654dcffc22f.jpg)

![](Gulati2013Nonlinear_figs/69cb7763047954481c6affd962ce70d1df9eb6fee903384d6b5405bebf5e69a4.jpg)

![](Gulati2013Nonlinear_figs/285d66f455bbeb28f86468081c29d39b5b41092eb4ff7b46b81350e8ad3d0c43.jpg)

![](Gulati2013Nonlinear_figs/5dc51ceb5402597fe1a2f88e6b5fdb72402fab40e9ce343ec53ab6dd4478cee3.jpg)  
Figure 10: Solution paths to a problem with five elliptical obstacles.

The boundary conditions of this problem are identical to the problem of Figure 6. Four distinct solution paths in the neighborhood of the four initial guesses are found. Initial guesses are the dotted curves while the final solutions are the solid curves. This problem had 3195 constraints for obstacle-avoidance in addition to the constraints in Figure 6. The total cost and travel time for the four solutions are shown in Table 3.

<table><tr><td>Solution Number</td><td>Travel time (s)</td><td>Total cost (s)</td></tr><tr><td>1</td><td>7.0</td><td>7.1</td></tr><tr><td>2</td><td>11.7</td><td>11.9</td></tr><tr><td>3</td><td>9.1</td><td>9.4</td></tr><tr><td>4</td><td>10.3</td><td>10.4</td></tr></table>

Table 3: Travel time and total cost for problem of Figure 10.

Figure 11 show an example where the initial and final speeds are both non-zero. This scenario exemplifies one of the common navigation tasks for an autonomous mobile robot – that of navigating in a corridor or sidewalk or driving in a lane on a road. We show only one solution out of four in this case. Figure 11(a) has two rectangular obstacles, signifying a wall. In the sequence Figure 11(b)–(f), one obstacle is added at a time, and each time a path is found that avoids all the obstacles.

Figure 12 shows an example when the initial speed is non-zero and the initial acceleration is positive. There are four rectangular and two star-shaped obstacles. This is a particularly dificult case because it involves a non-zero speed and high acceleration(0.5 m/s<sup>2</sup>, half the maximum allowable acceleration) at the beginning and a narrow passage between obstacles. In this case, only one of the four initial guesses resulted in a solution. Notice the loop in the path near the start. This is because the initial speed and acceleration are non-zero, and hence a sharp 90 degree left turn is not possible without violating dynamic bounds. If dynamic bounds are removed, another path, without a loop, starting from another initial guess is also found as a solution. This path does not have a loop. Also notice how the path just touches the vertices of obstacles so that its length is as small as is consistent with comfort.

![](Gulati2013Nonlinear_figs/6261b8cbaa961720bcf0d9a8d535238efe798f16946d3b44ee4b94a34d5a619a.jpg)  
(a)

![](Gulati2013Nonlinear_figs/26cd5dcf4785ea0e15758212d606baf05a5605f6e4ff5f619deeedabaa26b99f.jpg)  
(b)

![](Gulati2013Nonlinear_figs/e5d5dd48196dc236869e604eddc437bb834618a7e92a9d3b3484bf6b07df57ff.jpg)  
(c)

![](Gulati2013Nonlinear_figs/a1146d35314026d179c35e39f4e41b416f98d4244bac51700391e19cc642d1d3.jpg)  
(d)

![](Gulati2013Nonlinear_figs/af8a49b94aa235d26bece66744fa9bf474d579cc25e9671ca2608f0f0ee32c2f.jpg)  
(e)

![](Gulati2013Nonlinear_figs/1d0d09d334192c8d476b482ea0480b77f012c5227644af037a4bc8a922a481ba.jpg)  
(f)  
Figure 11: Obstacle avoidance in a corridor-like setting with non-zero speed at both ends.

Problem input is as follows: initial $\mathrm { p o s i t i o n } = \{ 0 , 0 \}$ $\mathrm { o r i e n t a t i o n } = 0 ,$ speed = 1, tangential acceleration = 0; final $\mathrm { p o s i t i o n } = \{ 2 0 , 0 \}$ , orientation = 0, speed = 1, tangential acceleration = 0. One of the four solution paths is shown. Initial guess is shown as the dashed curve while solution is shown as the solid curve. (a) Only two rectangular obstacles, comprising the corridor walls are present. The solution path is a straight line. (b) Addition of a circular obstacle results in a path that passes below the obstacle. Another solution path that passes above the obstacle and is symmetric to this path about the center line would also be a solution with same cost. $( \mathrm { c } ) , ( \mathrm { d } ) , ( \mathrm { e } ) , ( \mathrm { f } )$ One more obstacle is added and the same problem is solved starting from the same initial guess as in (a). All quantities have appropriate units in terms of meters and seconds.

![](Gulati2013Nonlinear_figs/ee2dc07d9e4610dbaf4f9f4a08c9b1fa850fa1cab0e41a05d36f8e514101d68e.jpg)  
Figure 12: Illustrative example showing passage through narrow space between star-shaped obstacles with non-zero speed at both ends and high positive acceleration at start. Problem input is as follows: initial position $= \{ - 5 , - 5 \}$ , orientation = 0, speed = 1, tangential acceleration $= 0 . 5 ;$ final position $= \{ 2 . 5 , 4 5 \}$ , orientation $= \pi / 2 .$ , speed = 1, tangential acceleration = 0. Four rectangular and two star-shaped obstacles are present. Initial guess is shown as the dashed curve while solution is shown as the solid curve. The loop in the solution at the beginning of the path is because the initial acceleration is high and hence it is not possible to make a sharp turn without violating dynamic constraints. All quantities have appropriate units in terms of meters and seconds

## 9.3 Efect of weights on discomfort

In this section we analyze the efect of the two dimensionless factors $f _ { T }$ and $f _ { N }$ on the individual terms comprising the cost functional (travel time, integral of squared tangential jerk, and integral of squared normal jerk) (see Equation $( 7 ) )$ ). This analysis provides us with guidelines for choosing the values of weights for customization by human users. Henceforth, for conciseness, we will refer to the three terms – travel time, integral of squared tangential jerk, and integral of squared normal jerk as $\tau , J _ { T }$ and $J _ { N }$ respectively. Thus, the cost functional of Equation (7) is

$$
J = \tau + f _ {T} J _ {T} + f _ {N} J _ {N}
$$

For this experiment, we construct a problem with identical boundary conditions as that of the example in Figure 6. In order to delineate the efect of weights, we remove all constraints and solve the unconstrained problem for a range of factors $f _ { T }$ and $f _ { N }$ for each of the four initial guesses. $f _ { T }$ is varied from $2 ^ { - 1 3 } \ \mathrm { t o \ 2 ^ { 1 3 } }$ in a geometric sequence, each subsequent value being obtained by multiplying the current value by 10. For each value of $f _ { T } , \ f _ { N }$ is varied from $2 ^ { - 1 3 }$ to $2 ^ { 1 3 }$ in a similar manner. Thus each weight roughly ranges between 0.0001 and 10000. This results in $4 \times 2 7 \times 2 7 = 2 9 1 6$ problems out of which 97% were successfully solved. We show plots corresponding to only one of these four solutions. Plots for the remaining solutions are similar, although the number of problems that converge is diferent for each initial guess.

Figures 13, 14, and 15 show $\tau , J _ { T }$ and $J _ { N }$ respectively. In each figure, part $\mathrm { ( a ) }$ shows log of the respective quantity as a function of $f _ { T }$ and $f _ { N }$ on a log-log-log scale. Part (b) is a top view of the surface plot above. Part (c) shows slices of this surface plot at $f _ { N } = 1$ and $f _ { T } = 1$ respectively.

The “holes” in the surface plots correspond to the problems that did not converge to a solution. In general, the surfaces are rougher and there are more failures when $f _ { N }$ is much larger than $f _ { T }$ . This indicates that the problem becomes less “stable” as the weight factors are too imbalanced. (In reality there are more holes in the surfaces than there are non-convergent problems. This is an unfortunate artifact of the plotting software that we use. In the surface plot, a vertex corresponds to a problem rather than a cell. Thus, one non-convergent problem causes all the cells that share that vertex to be removed. The actual non-convergent problems correspond to the empty cells of Figure 16).

In this experiment, the ratio of tangential jerk weight to normal jerk weight has been varied by nearly 8 orders of magnitude and we get solutions in almost all cases.

From Figure 13, we see that the travel time increases with increase in weights. This is expected since large weights mean that the contribution of travel time to total discomfort is relatively low compared to the contribution of the terms due to jerk. We also see that τ monotonically increases with $f _ { T }$ . For low values of $f _ { N } ,$ , τ does not change appreciably with $f _ { N }$ . As the value of $f _ { N }$ increases beyond a threshold, τ monotonically increases with $f _ { N }$ . The rate of increase of τ with respect to $f _ { T }$ is higher than it is with respect to $f _ { N }$

From Figure 14, we observe that log $J _ { T }$ decreases linearly with log $f _ { T }$ while it is almost constant with respect to log $f _ { N }$ . Thus, the integral of squared tangential jerk, $J _ { T } ,$ , is related to $f _ { T }$ by a power law.

From Figure 15 we see that for low values of $f _ { T } , \ J _ { N }$ does not change appreciably with $f _ { T }$ . As the value of $f _ { T }$ increases beyond a threshold, $J _ { N }$ monotonically decreases with $f _ { T }$ . A similar behavior is observed with respect to $f _ { N }$ although the threshold value appears lower than that for $f _ { T }$ . Once the values exceed the threshold, the rate of change of $J _ { N }$ with respect to both $f _ { N }$ and $f _ { T }$ is almost the same.

Thus, we see that the integral of squared tangential jerk, $J _ { { \scriptscriptstyle T } }$ is a function of $f _ { T }$ alone, and travel time changes more rapidly by changing $f _ { T }$ compared to $f _ { N }$ . Integral of squared normal $\mathrm { j e r k } , J _ { N }$ is a function of both $f _ { T }$ and $f _ { N }$ . Whenever a relationship exist between $f _ { T }$ or $f _ { N }$ and any of the quantities travel time, integral of squared tangential jerk, and integral of squared normal jerk, it is of the form of a power law.

![](Gulati2013Nonlinear_figs/4d8bfda1cc5ebed43c3044adf3152d49362aa3e5268cc6023decf171503bc242.jpg)  
(a)

![](Gulati2013Nonlinear_figs/c846719f422bf8d264ce3d2c84f3e8d5a524d8b0c6d6b7f3451dfe82c94bef43.jpg)  
(b)

![](Gulati2013Nonlinear_figs/4a063060b0813fd3f17c12c9ab879c157ac120178aa5abc40dd17c7189b398dd.jpg)  
(c)

![](Gulati2013Nonlinear_figs/e185912a84253819ac31ebeb9b1e4e9d11cf9acd7b4a8ed20411ee351b16e092.jpg)  
(d)  
Figure 13: Efect of weights on travel time.  
(a) Surface plot of log τ as a function of $f _ { T }$ and $f _ { N }$ on a log-log scale. (b) Top view of the surface plot. (c) Slice of the surface plot at $f _ { N } = 1$ . (d) Slice of the surface plot at $f _ { T } = 1$

From this analysis, we can draw some useful guidelines for customizing weights for comfort even though the efect of weight on discomfort is nonlinear. Since $J _ { T }$ is a function of $f _ { T }$ alone, we can devise experiments that allow a user to choose $f _ { T }$ that keeps tangential jerk to an acceptable level. For example, we can devise experiments that consist primarily of straight line motion, and has zero speeds on both ends. In such a motion, normal component of jerk will make none or minimal contribution to discomfort. Hence, it would be easy to set $f _ { T }$ . Next, we can devise experiments that consist of at least some curved segments. The user can choose $f _ { N }$ to keep normal jerk during this curved motion to an acceptable level. Because of power law relationships, the weights should be varied in a geometric manner rather than a linear manner for faster customization.

Figure 16 shows the number of iterations taken by Ipopt to find a solution. Apart from a few isolated outliers that require large number of iterations, it is clear that the number of iterations is small in the region where $f _ { T }$ is not too small compared to $f _ { N }$ and both factors are not too small either. If $f _ { N }$ is much larger than $f _ { T }$ , the problems still converge in most cases but require many iterations. Most of the failures are when $f _ { N }$ is too large compared to unity. Hence, we recommend that for customization $f _ { N }$ should not be too large compared to $f _ { T }$ and both should be not too small compared to unity.

(a) Surface plot of log(integral of squared tangential jerk) as a function of $f _ { T }$ and $f _ { N }$ on a log-log scale. (b) Top view of the surface plot. (c) Slice of the surface plot at $f _ { N } = 1 .$ (d) Slice of the surface plot at $f _ { T } = 1$  
![](Gulati2013Nonlinear_figs/9ad35f4bd64e34e20eb58718cb7a90c5181e4732a439bd7fe57178f6cdb04140.jpg)  
(a)

![](Gulati2013Nonlinear_figs/60a1635fd8c92871d075ba3a87518991f3477431c202c2c7930347c0e98502b5.jpg)  
(b)

![](Gulati2013Nonlinear_figs/3844875d017b63da8bc824f7ea52555bf6c8236661e8cc54035c230567cf541c.jpg)  
(c)

![](Gulati2013Nonlinear_figs/d7cea5d1f96b7d49a8495aacf1dd0741632f323ea1b34b7b6abff17120cc1008.jpg)  
(d)  
Figure 14: Efect of weights on integral of squared tangential jerk.

![](Gulati2013Nonlinear_figs/13a33ffb21533ff44a02811dcbb3d4c15ca267c2ee898e85f90efb63b700e13c.jpg)

![](Gulati2013Nonlinear_figs/d3e9a3f792cf4b1f335444f011b0e511b16329490cf6f6d94f41e8f0336d2a4d.jpg)

(a)  
![](Gulati2013Nonlinear_figs/dbc98e89c47e06bc75c18c2e3dfbff7902abd41fe05fe4b18c21f686a060265b.jpg)  
(c)

(b)  
![](Gulati2013Nonlinear_figs/a0dc6235c227142e5232f385704015f97e686fa504893412c89f494b4ac0f288.jpg)  
(d)

<table><tr><td rowspan="30" colspan="101">fN 1\ fT</td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>126</td><td>28</td><td>61</td><td>24</td><td>19</td><td>35</td><td>19</td><td>30</td><td>63</td><td>31</td><td>31</td><td>39</td><td>11</td><td>45</td><td>18</td><td>11</td><td>12</td><td>20</td><td>17</td><td>17</td><td>17</td><td>17</td><td>30</td><td>18</td><td>28</td><td>19</td><td>60</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>41</td><td>47</td><td>32</td><td>78</td><td>24</td><td>22</td><td>62</td><td>78</td><td>58</td><td>44</td><td>26</td><td>41</td><td>262</td><td>16</td><td>10</td><td>11</td><td>12</td><td>19</td><td>17</td><td>17</td><td>17</td><td>17</td><td>66</td><td>18</td><td>28</td><td>19</td><td>51</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>30</td><td>211</td><td>21</td><td>23</td><td>204</td><td>29</td><td>20</td><td>27</td><td>21</td><td>45</td><td>59</td><td>21</td><td>179</td><td>12</td><td>12</td><td>11</td><td>12</td><td>20</td><td>17</td><td>17</td><td>17</td><td>17</td><td>54</td><td>18</td><td>37</td><td>19</td><td>49</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>79</td><td>26</td><td>86</td><td>20</td><td>19</td><td>19</td><td>18</td><td>19</td><td>16</td><td>24</td><td>57</td><td>18</td><td>12</td><td>12</td><td>11</td><td>11</td><td>12</td><td>25</td><td>17</td><td>17</td><td>17</td><td>17</td><td></td><td>18</td><td>231</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>38</td><td>55</td><td>62</td><td>431</td><td>37</td><td>17</td><td>17</td><td>41</td><td>121</td><td>214</td><td>19</td><td>11</td><td>24</td><td>13</td><td>12</td><td>11</td><td>12</td><td>29</td><td>17</td><td>17</td><td>17</td><td>17</td><td>173</td><td>18</td><td>80</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>29</td><td>33</td><td>18</td><td>231</td><td>15</td><td>22</td><td>20</td><td>18</td><td>22</td><td>35</td><td>27</td><td>12</td><td>47</td><td>11</td><td>23</td><td>12</td><td>12</td><td>24</td><td>17</td><td>17</td><td>17</td><td>17</td><td>220</td><td>18</td><td>31</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>28</td><td>37</td><td>111</td><td>52</td><td>22</td><td>22</td><td>26</td><td>18</td><td>15</td><td>18</td><td>35</td><td>63</td><td>23</td><td>12</td><td>19</td><td>16</td><td>16</td><td>20</td><td>358</td><td>17</td><td>17</td><td>17</td><td>92</td><td>18</td><td>374</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>21</td><td>174</td><td>71</td><td>25</td><td>25</td><td>24</td><td>55</td><td>64</td><td>20</td><td>19</td><td>11</td><td>15</td><td>9</td><td>9</td><td>20</td><td>18</td><td>17</td><td>14</td><td>38</td><td>17</td><td>57</td><td>17</td><td>31</td><td>18</td><td>61</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>85</td><td>35</td><td>42</td><td>65</td><td>23</td><td>213</td><td>14</td><td>16</td><td>28</td><td>41</td><td>17</td><td>14</td><td>16</td><td>12</td><td>18</td><td>16</td><td>35</td><td>21</td><td>225</td><td>34</td><td>41</td><td>19</td><td>33</td><td>18</td><td>18</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>105</td><td>42</td><td>149</td><td>47</td><td>56</td><td>34</td><td>18</td><td>19</td><td>11</td><td>13</td><td>13</td><td>18</td><td>9</td><td>100</td><td>17</td><td>26</td><td>17</td><td>22</td><td>24</td><td>47</td><td>84</td><td>19</td><td>26</td><td>18</td><td>18</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>32</td><td>33</td><td>20</td><td>44</td><td>20</td><td>14</td><td>23</td><td>55</td><td>14</td><td>51</td><td>11</td><td>11</td><td>14</td><td>13</td><td>17</td><td>31</td><td>15</td><td>20</td><td>22</td><td>23</td><td>45</td><td>19</td><td>31</td><td>19</td><td>25</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>25</td><td>65</td><td>27</td><td>46</td><td>26</td><td>30</td><td>26</td><td>18</td><td>14</td><td>25</td><td>12</td><td>10</td><td>10</td><td>15</td><td>18</td><td>23</td><td>15</td><td>15</td><td>70</td><td>147</td><td>36</td><td>17</td><td>103</td><td>19</td><td>107</td><td>19</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>88</td><td>35</td><td>54</td><td>42</td><td>52</td><td>58</td><td>28</td><td>43</td><td>13</td><td>15</td><td>16</td><td>24</td><td>12</td><td>160</td><td>12</td><td>18</td><td>15</td><td>14</td><td>14</td><td>17</td><td>16</td><td>23</td><td>24</td><td>19</td><td>31</td><td>20</td><td>19</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>84</td><td>74</td><td>58</td><td>34</td><td>45</td><td>163</td><td>58</td><td>45</td><td>22</td><td>17</td><td>62</td><td>11</td><td>34</td><td>12</td><td>18</td><td>11</td><td>16</td><td>14</td><td>13</td><td>28</td><td>17</td><td>23</td><td>27</td><td>36</td><td>23</td><td>19</td><td>38</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>45</td><td>31</td><td>356</td><td>52</td><td>49</td><td>21</td><td>33</td><td>23</td><td>16</td><td>95</td><td>11</td><td>16</td><td>39</td><td>14</td><td>13</td><td>15</td><td>12</td><td>15</td><td>13</td><td>12</td><td>20</td><td>167</td><td>40</td><td>24</td><td>25</td><td>18</td><td>22</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>90</td><td>69</td><td>135</td><td>76</td><td>40</td><td>29</td><td>25</td><td>25</td><td>23</td><td>20</td><td>19</td><td>68</td><td>24</td><td>14</td><td>15</td><td>12</td><td>14</td><td>18</td><td>14</td><td>12</td><td>18</td><td>16</td><td>22</td><td>172</td><td>147</td><td>23</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>74</td><td>115</td><td>91</td><td>83</td><td>39</td><td>314</td><td>83</td><td>40</td><td>74</td><td>33</td><td>24</td><td>28</td><td>16</td><td>15</td><td>153</td><td>13</td><td>17</td><td>13</td><td>16</td><td>13</td><td>16</td><td>20</td><td>19</td><td>22</td><td>24</td><td>67</td><td>239</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>138</td><td>124</td><td>176</td><td>159</td><td>154</td><td>38</td><td>137</td><td>43</td><td>35</td><td>34</td><td>32</td><td>20</td><td>18</td><td>18</td><td>20</td><td>257</td><td>12</td><td>14</td><td>12</td><td>13</td><td>16</td><td>16</td><td>18</td><td>30</td><td>21</td><td>32</td><td>39</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>103</td><td>223</td><td>81</td><td>190</td><td>56</td><td>89</td><td>38</td><td>42</td><td>49</td><td>73</td><td>27</td><td>25</td><td>37</td><td>26</td><td>25</td><td>18</td><td>24</td><td>12</td><td>13</td><td>16</td><td>18</td><td>17</td><td>39</td><td>22</td><td>231</td><td>26</td><td>30</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>72</td><td>111</td><td>112</td><td>155</td><td>41</td><td>78</td><td>104</td><td>39</td><td>36</td><td>84</td><td>84</td><td>33</td><td>33</td><td>88</td><td>19</td><td>87</td><td>21</td><td>13</td><td>12</td><td>14</td><td>12</td><td>13</td><td></td><td>21</td><td>23</td><td>21</td><td>23</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>73</td><td>81</td><td>70</td><td>113</td><td>113</td><td>99</td><td>86</td><td>77</td><td>38</td><td>149</td><td>47</td><td>59</td><td>33</td><td>44</td><td>29</td><td>20</td><td>22</td><td>32</td><td>13</td><td>14</td><td>13</td><td>15</td><td>14</td><td>21</td><td>21</td><td>22</td><td>26</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>82</td><td>82</td><td>78</td><td>130</td><td>103</td><td>55</td><td>52</td><td>64</td><td>299</td><td>38</td><td>95</td><td>43</td><td>31</td><td>38</td><td>50</td><td>68</td><td>19</td><td>19</td><td>19</td><td>15</td><td>13</td><td>16</td><td>13</td><td>14</td><td>21</td><td>23</td><td>21</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>459</td><td>186</td><td>78</td><td>67</td><td>56</td><td>131</td><td>46</td><td>54</td><td>108</td><td>97</td><td>52</td><td>38</td><td>56</td><td>102</td><td>37</td><td>49</td><td>20</td><td>112</td><td>20</td><td>31</td><td>16</td><td>15</td><td>14</td><td>13</td><td>15</td><td>20</td><td>21</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>102</td><td>87</td><td>101</td><td>71</td><td>125</td><td>112</td><td>142</td><td>258</td><td>199</td><td>123</td><td>86</td><td>127</td><td>41</td><td>44</td><td>50</td><td>36</td><td>68</td><td>42</td><td>36</td><td>32</td><td>20</td><td>56</td><td>14</td><td>16</td><td>16</td><td>15</td><td>20</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>285</td><td>66</td><td>99</td><td>113</td><td>158</td><td>44</td><td>134</td><td>78</td><td>205</td><td>73</td><td>76</td><td>78</td><td>124</td><td>434</td><td>55</td><td>46</td><td>42</td><td>32</td><td>25</td><td>22</td><td>25</td><td>63</td><td>351</td><td>123</td><td>51</td><td>14</td><td>15</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>118</td><td>216</td><td>175</td><td>103</td><td></td><td rowspan="2">184</td><td rowspan="2">199</td><td rowspan="2">255</td><td rowspan="2">80</td><td rowspan="2">83</td><td rowspan="2">47</td><td rowspan="2">48</td><td rowspan="2">56</td><td rowspan="2">278</td><td rowspan="2">43</td><td rowspan="2">41</td><td rowspan="2">31</td><td rowspan="2">75</td><td rowspan="2">52</td><td rowspan="2">43</td><td rowspan="2">24</td><td rowspan="2">19</td><td rowspan="2">19</td><td rowspan="2">17</td><td rowspan="2" colspan="62">8192</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>94</td><td>85</td><td>85</td><td>116</td><td>78</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

Figure 16: Number of iterations for the range of weight factors.  
The green cells indicate smaller number of iterations compared to red cells. It is clear that the least number of iterations are taken in the region where both factors are greater than 1/32 and one factor is roughly within 1/16 to 16 times the other. The empty cells correspond to problems that failed to converge.

## 9.4 Reliability

To evaluate the reliability of our method, we construct a set of 7500 problems with diferent boundary conditions and solve the full constrained optimization problem corresponding to each of the 4 initial guesses for each problem. We do not include obstacles in this test.

We generate the problem set as follows. Fix the initial position as {0, 0} and orientation as 0. Choose final position at diferent distances along radial lines from the origin. Choose 10 radial lines that start from 0 degrees and go up to 180 degrees in equal increments. The distance on the radial line is chosen from the set {1, 2, 4, 8, 16}. The angle of the radial line and the distance on the line determines the final position. Choose 30 final orientations starting from 0 up to 360 degrees (360 degrees not included) in equal increments. The speed, v, and tangential acceleration, a , at both ends are varied by choosing $\{ v , a _ { T } \}$ pairs from the set {{0, 0} , {1, −0.1} , {1, 0} , {1, 0.1} , {3, 0}}. Thus we have 10 radial lines, 5 distances on each radial line, 30 orientations, 5 {v, a } pairs, resulting in $1 0 \times 5 \times 3 0 \times 5 = 7 5 0 0$ cases.

Each problem has 189 degrees of freedom, 2018 constraints, out of which 66 are equality constraints and 1952 are inequality constraints. For computation of initial guess of path, we set the maximum number of iterations to 100. For discomfort minimization problem we set the maximum number of iterations to 200. An average of 3.6 solution paths were found for each problem. This average would be higher if we set the maximum number of iterations even higher. However, since we wanted to evaluate how reliably our method performed in a reasonable amount of computation time, we kept the maximum number of iteration as 200.

All the problems were solved on a computer with an Intel Core i7 CPU running at 2.67 GHz, 4 GB RAM, and 4 MB L-2 cache size. Histogram of run-time for computing the solution of the discomfort minimization problem is shown in Figure 17 respectively. In this histogram, we have removed 1% of cases that lie outside the range of the axis shown for better visualization. This histogram shows both successful and unsuccessful cases.

For each of the 7500 problems, each of the successful initial guesses was used to compute a solution of the discomfort minimization problem. For all the problems, at least one successful solution was computed. Table 4 shows the number of problems for which one, two, three, or four solutions were successfully computed.

From Figure 17 we see that 99% or more of the solutions of the full problem are computed in less than 4 seconds. To get an estimate of the percentage of outliers, we fit a Gaussian to each of the four guesses. The results are shown in Table 5. This is a simplified approximation and should be seen just as an indicator of reliability of the method. Time taken to compute the solution is further visualized in Figure 18 that shows a normalized cumulative histogram.

Histograms of number of iterations for computing final solution are shown in Figure 19. On average, 90% all four solutions were computed in 100 iterations or less.

![](Gulati2013Nonlinear_figs/cf182730b5418beda87c505da3114a81fd283c89fecce159830f885e1a8ac155.jpg)  
(a) 99% solved within 4 s.

![](Gulati2013Nonlinear_figs/495248e8802bff0bf2a4a90314965243d9974ab13b138356764b3cb16addb0f3.jpg)  
(b) 99% solved within 4 s.

![](Gulati2013Nonlinear_figs/6733fa7f62d8ea0e47c12988c819c86eb35e3fcb794b4f0377350877cf80d117.jpg)  
(c) 99% solved within 4 s.

![](Gulati2013Nonlinear_figs/bb1226b253c5be3ee68327e117ee47d7548276706c61540c67019abc078d2076.jpg)  
(d) 100% solved within 4 s.

Figure 17: Histogram of time taken to compute solution of discomfort minimization problem. This includes both successful and unsuccessful cases. Total 7500 cases.

![](Gulati2013Nonlinear_figs/d45b242e1119ec025a9d74eb780f0564d02f53684b05e45cdd2a3761de5e652e.jpg)  
(a) 99% solved within 4 s.

![](Gulati2013Nonlinear_figs/66ca094b26add98a7cadf9861126b8a504065964486020dcffa93328835d58f9.jpg)  
(b) 99% solved within 4 s.

![](Gulati2013Nonlinear_figs/72cf456d0888978ec5813989e0ed781c15bc939466545bd2483e25267a9e8922.jpg)  
(c) 99% solved within 4 s.

![](Gulati2013Nonlinear_figs/a48f5c1262ea8a8f73f957e0a673bec5c5d969644cf0ab987034aa19009aac58.jpg)  
(d) 100% solved within 4 s.

Figure 18: Normalized cumulative histogram of time taken to compute solution of discomfort minimization problem This includes both successful and unsuccessful cases. Total 7500 cases.

<table><tr><td>Percentage of problems</td><td>Number of successful solutions</td></tr><tr><td>0.39</td><td>1</td></tr><tr><td>6.20</td><td>2</td></tr><tr><td>34.45</td><td>3</td></tr><tr><td>58.96</td><td>4</td></tr></table>

Table 4: Percentage of problems with one, two, three, or four successfully computed solutions. At least one solution was found for all of the 7500 problems while all four solutions were found for almost 60% of the problems.

<table><tr><td>Solution</td><td>Gaussian (μ, σ)</td><td>Percentage of outliers</td></tr><tr><td>1</td><td>(0.668, 0.751)</td><td>3.56</td></tr><tr><td>2</td><td>(0.686, 0.795)</td><td>2.74</td></tr><tr><td>3</td><td>(0.612, 0.564)</td><td>3.35</td></tr><tr><td>4</td><td>(0.662, 0.344)</td><td>2.64</td></tr></table>

Table 5: Estimating the percentage of outliers in computation time for the discomfort minimization problem. Mean and standard deviation of the Gaussian fitted to the data of Figure 17. Points that lie outside $\left[ \mu - 3 \sigma , \mu + 3 \sigma \right]$ are outliers.

![](Gulati2013Nonlinear_figs/5eac55ed9d0a7eb4fad735e0f1ce1b6930897df61542ffbace6e439482642ffa.jpg)  
(a) 89% solved in 100 iterations or less

![](Gulati2013Nonlinear_figs/c02c116b77add02c6773e4d5f2bcaa0c70b8ba6f95b5f66400297b30ba29d92a.jpg)  
(b) 88% solved in 100 iterations or less

![](Gulati2013Nonlinear_figs/f30721c1136775ddcacffb2fc7e4113ef402663b89d009cbc63f7eaae7b34265.jpg)  
(c) 93% solved in 100 iterations or less

![](Gulati2013Nonlinear_figs/0533c7e0e9516e93531d0a87909cd3ddf0277c0aa65dfe2fbe2fe0610d552ca9.jpg)  
(d) 94% solved in 100 iterations or less

Figure 19: Histogram of number of iterations to compute solution of discomfort minimization problem. Total number of problems is 7500. The peak at 200 iterations is due to failed cases since maximum number of iterations was set to 200.

## 9.5 Discussion of results and limitations

Results show that our framework is capable of reliably planning trajectories between a large variety of boundary conditions and for a range of weights. 97% of 2916 unconstrained problems for a fixed boundary condition but varying weights were solved successfully when weights were varied by 8 orders of magnitude. Out of a set of 7500 examples with varying boundary conditions, and all dynamic constraints imposed, 3.6 solution paths, on average, were found per example. At least one solution was found for all of the problems and four solutions were found for roughly 60% of the problems. The time taken to compute the solution to the discomfort minimization problem was less than 10 seconds for all the cases, 99% of all problems were solved in less than 4 seconds, and roughly 90% were solved in less than 100 iterations.

We also saw that our framework can plan trajectories with a variety of boundary conditions that avoid obstacles. We presented concrete examples for circular, elliptical, and star-shaped obstacles.

Thus, our framework, with some more speedups in run-time, can be implemented for eficient and robust motion-planning of nonholonomic mobile robots. We will discuss possible way of achieving speedups in computational time in Section 10.1. One of the limitations of our current implementation is that if the initial guess of path passes through obstacles, it may take a large number of iterations for the optimization algorithm to converge to a solution, and sometimes a solution may not even be found. We have observed this on some example cases and this will need a more careful analysis in the future. One way to deal with this issue is to generate initial guesses of path that are obstacle free and this is part of future work.

There are many tasks in which an autonomous mobile robot must back up and then move towards the goal. For example, if an assistive robot is positioned at a user’s desk, it cannot move forward. To go anywhere it must back up first. Such tasks can be handled with the help of a high-level planner that breaks this sequence into two and provides a set of two boundary conditions in sequence to our framework – one for backing up and one for the goal. The intermediate waypoint can also be chosen by an optimization process.

In our method, we impose obstacle avoidance constraints on a discrete set of points on the path. Thus, we cannot guarantee that segments of the path between these points will not intersect obstacles. In practice, if the points are chosen to be close enough, so that distance between these points is smaller than most obstacles, the path would be collision-free. Even so, sharp pointed corners of obstacles can intersect the path. This is a problem that will arise with any discretization. This can be handled in two ways. First, when we incorporate robot’s body for obstacle-avoidance an extra margin of safety can be added. Second, obstacles can be represented with a piecewise smooth boundary curve that encloses the obstacle shape such that sharp corners are smoothed out.

## 10 Concluding remarks and directions for future research

We make two main contributions in this work. First, we characterize comfort for a user of an autonomous nonholonomic mobile robot. Among the various contributing factors to comfort, we focus on dynamic factors. For comfortable motion, a trajectory should have the following properties – it should satisfy boundary conditions on position, orientation, speed and tangential acceleration at the start and end points, have continuous acceleration, the geometric path should avoid obstacles, have curvature continuity, and should satisfy boundary conditions on curvature. In addition, the trajectory should respect bounds on curvature, speed, angular speed, and tangential and normal accelerations. While human user studies are required to validate this characterization of comfort, we believe that we have taken an important first step in formalizing motion comfort for autonomous mobile robots.

Second, we develop a nonlinear constrained optimization based motion planning framework to plan trajectories such that the trajectories minimize discomfort and have all the properties described above. To the best of our knowledge, this is the first comprehensive formulation of kinodynamic motion planning for a planar nonholonomic mobile robot that includes all of the following – a careful analysis of boundary conditions and continuity requirements on trajectory, dynamic constraints, obstacle avoidance constraints, and a robust numerical method that computes solution trajectories in a few seconds.

One of the strengths of our framework is that it is easy to incorporate additional kinematic and dynamic constraints, and additional terms can also be incorporated in the discomfort functional. Of course, care has to be taken to keep the problem mathematically meaningful.

We believe that our work is an important step in developing autonomous robots that are acceptable to human users. For application to real-world robotic systems, some important extensions to our framework will be required. First, our current implementation achieves obstacle avoidance for a point robot. We have described a method for incorporating robot shape, and this will have to be implemented. Second, our results show that time taken to find a solution is of the order of seconds. This will have to be reduced for real-time planning. We discuss these, and several other extensions, below.

## 10.1 Directions for future research

Incorporating robot shape for obstacle avoidance. We described a general method to incorporate arbitrary shaped robot body in Section 6.7. This method consists of modeling the robot as a closed curve that encloses the projection of its boundary in the plane of motion, choosing a set of points on this curve, and imposing the constraints that all these points be outside all obstacles. If m points are chosen on the boundary and there are n obstacles, this method will result in m × n constraints. A more eficient approach may be possible when the robot can be modeled by a simple shape such as a circle or a convex polygon. Since most mobile robots, in practice, have simple shapes, it is worthwhile to explore these shapes as special cases for obstacle avoidance.

Incorporating moving obstacles. One way to incorporate moving obstacles is to frequently update a map of the world and use this updated map to re-plan a new trajectory starting from the current state. For comfort of a human user, it may be useful to develop models that estimate a moving obstacle’s trajectory, and use this trajectory during planning. This could result in paths that have fewer changes in direction (compared to those found by fast-re planning) and are perceived to be more comfortable. Such obstacl models have been previously employed for motion planning (Fiorini and Shiller, 1998).

Culling obstacles intelligently. In our method, we choose a set of points on the path, and impose the constraint that all obstacles be outside all points on the path. In our earlier approaches, we have experimented with culling these obstacles intelligently so that the number of obstacle constraints is reduced. If the trajectory is well-behaved, that is, if the geometric path does not have too many self intersections, and if one iterate does not vary too wildly from the previous, then we may be able to achieve a reduction in the number of constraints.

First, we can remove, in advance, all obstacles that are too far from the initial guess of path. Second, for every point, we impose the constraint that it be outside obstacles within its “neighborhood” rather than being outside all obstacles. Under the above described conditions, if a point is outside obstacles in its neighborhood, it can be expected to be outside all other obstacles that are far from it. In our experiments with our current approach, we have observed that the above conditions hold if the initial guess of path is outside obstacles.

Computing initial guesses that avoid obstacles We have observed that the solution to the discomfort minimization problem converges slowly if the initial guess of path passes through an obstacle. We believe that we can achieve fast convergence if the initial guess of path lies outside obstacles even if it does not respect continuity and kinodynamic constraints. Many of the existing path planning approaches can be used to compute an initial guess of path that has the above properties.

Reducing computational time. For real-time implementation, it would be necessary to achieve a reduction in the computational time so that the problem is solved in a few milliseconds. Many steps can be taken to achieve this.

First, we have observed that when an initial guess of path is inside an obstacle, it takes longer for the optimization algorithm to converge to a solution. Therefore, it would be worthwhile to invest some efort in generating an initial guess of path that is outside obstacles. This would reduce the number of iterations required to find a solution.

Second, intelligently culling obstacles and eficiently implementing obstacle avoidance constraints for special robot shapes, as discussed earlier, could result in significant reduction in the number of constraints and faster computations in every iteration.

Third, a multi-step optimization procedure can be tried. A coarser finite element mesh with fewer elements can be used to find a solution which would serve as an initial guess for a problem with a finer mesh.

Finally, parallelism inherent in the problem can be exploited and parts of the program can be executed on a

GPU. For example, computation of constraint values, gradients and Hessians can be parallelized. Other such parallelisms should also be exploited. In addition, many other code optimizations can also be implemented.

Evaluating the “goodness” of discomfort measure. We have formulated a measure of discomfort based on comfort studies in ground vehicles such as automobiles and trains. To the best of our knowledge, no such studies have been conducted for assistive robots. Since discomfort is subjective, the best way to assess comfort is to ask a user. Hence, to validate this discomfort measure, human user studies should be conducted with enough users to yield statistically significant data. We provide some guidelines on how such a study may be conducted in Section 10.2 below.

Motion planning for non-planar surfaces. The motion planning framework presented in this work was developed for planning trajectories for a nonholonomic mobile robot moving on a plane. This assumption holds, for the most part, in indoor environments. For navigating in an urban outdoor environment, this framework can be extended by parameterizing the path as a space curve rather than a 2D curve and formulating the cost functional and constraints to take into account the 3D geometry of the surface on which the robot moves.

## 10.2 Implementation of the motion planning framework for human users

A human user study can be conducted to either confirm that the measure of discomfort is good by showing that multiple human users can achieve comfort after choosing the weights, or failing that, to provide additional insight into what might be missing. Below are some guidelines on implementing the framework on an assistive robot and conducting such a study.

• Our motion planning framework requires a representation of the local environment to plan trajectories. An occupancy-grid based representation can be used. In such a representation, obstacles are represented as occupied cells in the grid. See (Thrun et al., 2005) for a detailed discussion of such a representation. For eficient motion planning, these cells should be grouped together, where possible, into a single star-shaped polygon. When such a grouping yields an obstacle that is not star-shaped, it should be decomposed into a union of star-shaped polygons. An eficient algorithm for doing so can be found in (Avis and Toussaint, 1981).

• A goal state consisting of position, orientation, curvature, speed, and magnitude of tangential acceleration, is required as input to the motion planning framework. Position and orientation may be provided by a human user through some input device (e.g by clicking on a map as in (Murarka and Kuipers, 2009)). Curvature should be set to zero. Speed may be specified as zero if it is desired to stop at the final position, otherwise is should be a speed that is typically found comfortable by the user. Tangential acceleration should be set to zero. For navigating in large-scale space, a high-level planner such as that used in (Murarka and Kuipers, 2009) could be used for generating intermediate way points. Such a planner usually provides only position and orientation. The rest of the quantities can be provided according to the guidelines above.

• All necessary bounds should also be provided as input. The bounds in Table 1 may be used as a start if the study is conducted for an intelligent wheelchair, while the references cited in Section 2.1 can be used for the bounds if the study is conducted for an autonomous car.

• A controller that can track the planned trajectory should be implemented. We have achieved good tracking accuracy, in our previous work (Murarka et al., 2009), with a feedback-linearization based controller described in (Luca et al., 1998).

• Before performing human user experiments, the framework should be comprehensively tested in the environment in which the users will evaluate it. If the environment is likely to have moving obstacles, fast re-planning should be implemented. This requires trajectories to be computed in at most a tenth of second. A relatively safe indoor environment with no drop-ofs and other hazards should be chosen and common failure cases should be identified via experimentation.

• In the first step of the study, a user should be asked to manually operate the assistive robot on a variety of tasks. A speed that the user typically operates at should be determined from these tasks.

• Although a more detailed study than that described in Section 9.3 could yield an empirical relationship between weights and the individual terms in our discomfort measure, such a study is not an absolute prerequisite to performing human user studies. The two dimensionless factors correspond ing to the weights for integral of squared tangential jerk and squared normal jerk are the parameters that should be varied in the experiments.

• First, the weight factor for tangential jerk should be determined. To do this, the following experiment can be conducted. Set start and end boundary conditions such that motion is along a straight line. Set initial and final speed and acceleration to zero. Use the motion planning framework to plan trajectories for this task for a range of weight factors for tangential jerk. Ask the user to compare discomfort for every pair of weights. This comparison should include subjective questions on overall comfort as well as questions comparing the level of tangential jerk, and asking whether the time of travel was satisfactory. Vary the total length of the path and repeat the experiment for multiple lengths. Based on these experiments, fix a value of this weight factor.

• Next, the weight factor for normal jerk should be determined. To do this, the following experiment can be conducted. Set start at end boundary conditions such that most of the motion is along a curved path. One way to achieve this is by choosing final position very close to the start position such that the robot has to travel along a curve to reach the goal. Follow a procedure similar to the one described above (for tangential jerk) to determine the weight factor for normal jerk.

• Once the weight factors are determined, a set of motion tasks with a variety of boundary conditions should be performed and user should be asked to rate comfort.

• If the motion for the above tasks is found to be comfortable, then it can be concluded that the measure of discomfort, in fact, captures user discomfort. If not, a set of questions designed to learn what might be missing should be asked.

• In all cases, all quantitative information such as speed, acceleration, jerk, travel time, length of path etc., should be collected.

## 11 Acknowledgements

This work has taken place in the Intelligent Robotics Lab at the Artificial Intelligence Laboratory, The University of Texas at Austin. Research of the Intelligent Robotics lab was supported in part by grants from the National Science Foundation (IIS-0413257, IIS-0713150, and IIS-0750011), the National Institutes of Health (EY016089), and from the Texas Advanced Research Program (3658-0170-2007).

## References

Adams, R. A. and Fournier, J. F. (2003). Sobolev spaces. Elsevier.

Arechavaleta, G., Laumond, J.-P., Hicheur, H., and Berthoz, A. (2008). An optimality principle governing human walking. IEEE Transactions on Robotics, 24:5–14.

Avis, D. and Toussaint, G. (1981). An eficient algorithm for decomposing a polygon into star-shaped polygons. Pattern Recognition, 13(6):395–398.

Balkcom, D. J. and Mason, M. T. (2002). Time optimal trajectories for diferential drive vehicles. International Journal of Robotics Research, 21(3):199–217.

Barraquand, J. and Latombe, J.-C. (1989). On nonholonomic robots and optimal maneuvering. Revue dIntelligence Artificielle, 3(2):77–103.

Barraquand, J. and Latombe, J.-C. (1990). Robot motion planning: A distributed representation approach. International Journal of Robotics Research, 10:72–89.

Bianco, C. G. L. and Romano, M. (2004). Smooth motion generation for unicycle mobile robots via dynamic path inversion. IEEE Transactions on Robotics, 20(5):884 – 891.

Bianco, C. G. L. and Romano, M. (2005). Bounded velocity planning for autonomous vehicles. In IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 685–690.

Bobrow, J. E., Martin, B., Sohl, G., Wang, E. C., Park, F. C., and Kim, J. (2001). Optimal robot motions for physical criteria. Journal of Robotic Systems, 18(12):785–795.

Bryson, A. E. and Ho, Y.-C. (1975). Applied Optimal Control : Optimization, Estimation, and Control. Hemisphere Publishing Corporation.

Calinon, S. and Billard, A. (2009). Statistical learning by imitation of competing constraints in joint space and task space. Advanced Robotics, 23(15):2059–2076.

Canny, J. (1988). Complexity of robot motion planning. MIT press.

Canny, J. and Reif, J. (1987). New lower bound techniques for robot motion planning problems. In IEEE Symposium on Foundations of Computer Science, pages 49–60.

CEN (1999). Railway applications - ride comfort for passengers - measurements and evaluation. ENV 12299.

Chakroborty, P. and Das, A. (2004). Principles of Transportation Engineering. PHI Learning Pvt. Ltd.

Choset, H., Lynch, K. M., Hutchinson, S., Kantor, G., Burgard, W., Kavraki, L. E., and Thrun, S. (2005). Principles of Robot Motion: Theory, Algorithms, and Implementations. MIT Press.

Donald, B., Xavier, P., Canny, J., and Reif, J. (1993). Kinodynamic motion planning. Journal of the ACM, 40(5):1048–1066.

Dubins, L. E. (1957). On curves of minimal length with a constraint on average curvature and with prescribed initial and terminal positions and tangents. American Journal of Mathematics, 79:497–516.

Erdman, M. and Lozano-P´erez, T. (1987). On multiple moving objects. Algorithmica, 2(4):477–521.

Fehr, L., Langbein, W. E., and Skaar, S. B. (2000). Adequacy of power wheelchair control interfaces for persons with severe disabilities: A clinical survey. Journal of Rehabilitation Research and Development, 37(3):353–360.

Ferguson, D., Howard, T. M., and Likhachev, M. (2008). Motion planning in urban environments: Part I. In IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 1063–1069.

Fernandes, C., Gurvits, L., and Li, Z. X. (1991). A variational approach to optimal nonholonomic motion planning. In IEEE International Conference on Robotics and Automation, pages 680–685.

Fiorini, P. and Shiller, Z. (1998). Motion planning in dynamic environments using velocity obstacles. International Journal of Robotics Research, 17(2):760–772.

F¨orstberg, J. (2000). Ride comfort and motion sickness in tilting trains: Human responses to motion environments in train experiment and simulator experiments. PhD thesis, KTH Royal Institute of Technology.

Fraichard, T. (1996). Dynamic trajectory planning with dynamic constraints: A state-time space approach. In IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 1394–1400.

Fraichard, T. and Scheuer, A. (2004). From Reeds and Shepp’s to continuous-curvature paths. IEEE Transactions on Robotics and Automation, 20(6):1025–1035.

Full, R. and Koditschek, D. (1999). Templates and anchors: neuromechanical hypotheses of legged locomotion on land. Journal of Experimental Biology, 202(23):3325–3332.

Glover, J. (1900). Transition curves for railways. In Minutes of Proceedings of the Institution of Civil Engineers, pages 161–179.

Gulati, S. (2011). A framework for characterization and planning of safe, comfortable, and customizable motion of assistive mobile robots. In Ph.D. Thesis.

Gulati, S., Jhurani, C., and Kuipers, B. (2013). A nonlinear constrained optimization framework for comfortable and customizable motion planning of nonholonomic mobile robots – part ii. Submitted to The International Journal of Robotics Research.

Gulati, S., Jhurani, C., Kuipers, B., and Longoria, R. (2009). A framework for planning comfortable and customizable motion of an assistive mobile robot. In IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 4253–4260.

Gulati, S. and Kuipers, B. (2008). High performance control for graceful motion of an intelligent wheelchair. In IEEE International Conference on Robotics and Automation, pages 3932–3938.

Hall, D. L., Loshbough, R., and Robaszkiewicz, G. D. (1970). Jerk, acceleration, and limited pattern generator for an elevator system. U.S. Patent number: 3523232.

Havoutis (2012). Motion planning and reactive control on learnt skill manifolds. PhD thesis, The University of Edinburgh.

Howard, T. M. and Kelly, A. (2007). Optimal rough terrain trajectory generation for wheeled mobile robots. The International Journal of Robotics Research, 26(2):141–166.

Hsu, D., Kindel, R., Latombe, J.-C., and Rock, S. (2002). Randomized kinodynamic motion planning with moving obstacles. Int. J. Robotics Research, 21(3):233–255.

Hughes, T. J. (2000). The Finite Element Method: Linear Static and Dynamic Finite Element Analysis. Dover Publications.

Hwang, Y. K. and Ahuja, N. (1992). Gross motion planning – a survey. ACM Computing Surveys, 24(3):219 – 291.

ISO (1997). Mechanical vibration and shock – evaluation of human exposure to whole body vibrations - part 1: General requirements. ISO 2631-1.2(E).

Iwnicki, S. (2006). Handbook of Railway Vehicle Dynamics. CRC Press.

Jacobson, I. D., Richards, L. G., and Kuhlthau, A. R. (1980). Models of human comfort in vehicle environments. Human factors in transport research, 20:24–32.

Karaman, S. and Frazzoli, E. (2011). Sampling-based algorithms for optimal motion planning. The International Journal of Robotics Research, 30(7):846–894.

Kavraki, L. E., Svestka, P., Latombe, J.-C., and Overmars, M. (1996). Probabilistic roadmaps for path planning in high dimensional configuration spaces. IEEE Transactions on Robotics and Automation, 12(4):566–580.

Krapek, K. J. and Bittar, J. (1993). Elevator motion profile selection. U.S. Patent number: 5266757.

Lamiraux, F. and Laumond, J.-P. (2001). Smooth motion planning for car-like vehicles. IEEE Transactions on Robotics and Automation, 17(4).

Lamm, R., Psarianos, B., and Mailaender, T. (1999). Highway design and trafic safety engineering handbook. McGraw-Hill.

Langhaar, H. L. (1951). Dimensional Analysis and Theory of Models. Wiley.

Latombe, J.-C. (1991). Robot Motion Planning. Kluwer Academic Press.

Laumond, J.-P., Sekhavat, S., and Lamiraux, F. (1998). Guidelines in nonholonomic motion planning for mobile robots. In Laumond, J.-P., editor, Robot Motion Planning and Control, pages 1–53. Springer-Verlag, Berlin.

Laundhart (1887). Theory of the alignment. Schmorl & von Seefeld publishing house.

LaValle, S. M. (1998). Rapidly-exploring random trees: A new tool for path planning. Technical Report 98-11, Computer Science Department, Iowa State University.

LaValle, S. M. (2006). Planning Algorithms. Cambridge University Press.

LaValle, S. M. (2011a). Motion planning: The essentials. IEEE Robotics and Automation Society Magazine, 18(1):79–89.

LaValle, S. M. (2011b). Motion planning: Wild frontiers. IEEE Robotics and Automation Society Magazine, 18(2):108–118.

LaValle, S. M. and Kufner, J. J. (2001a). Randomized kinodynamic planning. International Journal of Robotics Research, 20(5):378–400.

LaValle, S. M. and Kufner, J. J. (2001b). Rapidly-exploring random trees: Progress and prospects. In Donald, B. R., Lynch, K. M., and Rus, D., editors, Algorithmic and Computational Robotics: New Directions, pages 293–308. A. K. Peters, Wellesley, MA.

Likhachev, M. and Ferguson, D. (2009). Planning long dynamically feasible maneuvers for autonomous vehicles. The International Journal of Robotics Research, 28(8):933–945.

Lin, M. C. and Manocha, D. (2004). Collision and proximity queries. In Goodman, J. E. and O’Rourke, J., editors, Handbook of Discrete and Computational Geometry, 2nd Ed., pages 787–807. Chapman and Hall/CRC Press, New York.

Luca, A. D., Oriolo, G., and Samson, C. (1998). Feedback control of a nonholonomic car-like robot. In Laumond, J.-P., editor, Robot Motion Planning and Control, pages 171–253. Springer-Verlag, Berlin.

McNaughton, M., Urmson, C., Dolan, J., and Lee, J. W. (2011). Motion planning for autonomous driving with a conformal spatiotemporal lattice. In IEEE International Conference on Robotics and Automation, pages 4889–4895.

Mirtich, B. (1998). Eficient algorithms for two-phase collision detection. In Gupta, K. and del Pobil, A., editors, Practical Motion Planning in Robotics: Current Approaches and Future Directions, pages 203–223. Wiley, New York.

Murarka, A., Gulati, S., Beeson, P., and Kuipers, B. (2009). Towards a safe, low-cost, intelligent wheelchair. In Workshop on Planning, Perception and Navigation for Intelligent Vehicles (PPNIV), pages 42–50.

Murarka, A. and Kuipers, B. (2009). A stereo vision based 3D mapping algorithm for detecting ramps, drop-ofs, and obstacles for safe local navigation. In IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 1646–1653.

Pepler, R. D., Sussman, E. D., and Richards, L. G. (1980). Passenger comfort in ground vehicles. Human factors in transport research, 20:76–84.

Piazzi, A., Bianco, C. G. L., and Romano, M. (2007). η<sup>3</sup> splines for the smooth path generation of wheeled mobile robots. IEEE Transactions on Robotics, 23(5).

Pivtoraiko, M., Knepper, R., and Kelly, A. (2009). Diferentially constrained mobile robot motion planning in state lattices. Journal of Field Robotics, 26(3):308–333.

Quinlan, S. (1994). Eficient distance computation between non-convex objects. In IEEE International Conference on Robotics and Automation, pages 3324 – 3329.

Ramamoorthy, S. and Kuipers, B. (2008). Trajectory generation for dynamic bipedal walking through qualitative model based manifold learning. In IEEE International Conference on Robotics and Automation, pages 359–366.

Reeds, J. A. and Shepp, L. A. (1990). Optimal paths for a car that goes both forward and backward. Pacific Journal of Mathematics, 145(2):367–393.

Richards, L. G. (1980). On the psychology of passenger comfort. Human factors in transport research, 20:15–23.

Schaal, S., Ijspeert, A., , and Billard, A. (2003). Computational approaches to motor learning by imitation. Philosophical Transactions: Biological Sciences, 1431(358):537–547.

Scheuer, A. and Laugier, C. (1998). Planning sub-optimal and continuous-curvature paths for car-like robots. In IEEE International Conference on Intelligent Robots and Systems, pages 25–371.

Shiller, Z. (1994). Time-energy optimal control of articulated paths with geometric path constraints. In International Conference on Robotics and Automation.

Shiller, Z. and Dubowsky, S. (1991). On computing the global time-optimal motions of robotic manipulators in the presence of obstacles. IEEE Transactions on Robotics and Automation, 7(6):785–797.

Shiller, Z. and Gwo, Y.-R. (1991). Dynamic motion planning of autonomous vehicles. IEEE Transactions on Robotics and Automation, 7(2):241–249.

Silberg, G., Wallace, R., Matuszak, G., Plessers, J., Brower, C., and Subramanian, D. (2012). Self-driving cars: The next revolution. Technical report, KPMG Center for Automotive Research.

Simpson, R. C., LoPresti, E. F., and Cooper, R. A. (2008). How many people would benefit from a smart wheelchair? Journal of Rehabilitation Research and Development, 45(1):53–72.

Sou\`eres, P. and Boissonnat, J. (1998). Optimal trajectories for nonholonomic mobile robots. In Laumond, J.-P., editor, Robot Motion Planning and Control, pages 93–170. Springer-Verlag, Berlin.

Spielbauer, H.-K. J. and Peters, M. (1995). Elevator start jerk removal. U.S. Patent number: 5424498.

Strizzi, J., Ross, I. M., and Fahroo, F. (2002). Towards real-time computation of optimal controls for nonlinear systems. In AIAA Guidance, Navigation, and Control Conference.

Suzuki, H. (1998). Research trends on riding comfort evaluation in japan. Proceedings of the Institution of Mechanical Engineers – Part F – Journal of Rail and Rapid Transit, 212(1):61–72.

Thrun, S., Burgard, W., and Fox, D. (2005). Probabilistic Robotics. MIT Press.

Tominaga, H. and Bavarian, B. (1990). Global robot path planning using exact variational methods. In IEEE International Conference on Systems, Man and Cybernetics, pages 617–619.

Troutman, J. L. (1995). Variational Calculus and Optimal Control: Optimization with Elementary Convexity. Springer, 2 edition.

Zefran, M. (1996). <sup>ˇ</sup> Continuous Methods for Motion Planning. PhD thesis, University of Pennsylvania, Philadelphia, PA.

W¨achter, A. and Biegler, L. T. (2006). On the implementation of a primal-dual interior point filter line search algorithm for large-scale nonlinear programming. Mathematical Programming, 106(1):25–57.