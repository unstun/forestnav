---
citation_key: Yang2025Recasting
arxiv_id: 2506.00351
arxiv_url: "https://arxiv.org/abs/2506.00351"
title: "Recasting Classical Motion Planning for Contact-Rich Manipulation"
authors_short: "Lin Yang et al."
year: 2025
direction_tag: J_homotopy_topology
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:13:41Z
origin: ai+web
reviewed: false
---

# Recasting Classical Motion Planning for Contact-Rich Manipulation

Lin Yang, Student Member, IEEE, Huu-Thiet Nguyen, Chen Lv, Senior Member, IEEE, and Domenico Campolo<sup>∗</sup>, Member, IEEE

Abstract—In this work, we explore how conventional motion planning algorithms can be reapplied to contactrich manipulation tasks. Rather than focusing solely on efficiency, we investigate how manipulation aspects can be recast in terms of conventional motion-planning algorithms. Conventional motion planners, such as Rapidly-Exploring Random Trees (RRT), typically compute collision-free paths in configuration space. However, in many manipulation tasks, contact is either unavoidable or essential for task success, such as for creating space or maintaining physical equilibrium. As such, we presents Haptic Rapidly-Exploring Random Trees (HapticRRT), a planning algorithm that incorporates a recently proposed optimality measure in the context of quasi-static manipulation, based on the (squared) Hessian of manipulation potential. The key contributions are i) adapting classical RRT to operate on the quasi-static equilibrium manifold, while deepening the interpretation of haptic obstacles and metrics; ii) discovering multiple manipulation strategies, corresponding to branches of the equilibrium manifold. iii) validating the generality of our method across three diverse manipulation tasks, each requiring only a single manipulation potential expression. The video can be found at https://youtu.be/R8aBCnCCL40.

Index Terms—Manipulation planning, haptic metric, haptic obstacle, quasi-static manipulation, pendulum pushing, crowded bookshelf insertion, spring clip manipulation.

## I. INTRODUCTION

R <sup>OBOTIC</sup> <sup>manipulation</sup> <sup>typically</sup> <sup>involves</sup> <sup>the</sup> <sup>robot</sup> <sup>es-</sup>tablishing contact with specific objects. It is essential for the robot to maintain contact with objects to successfully accomplish the tasks [1] . Classical motion planners, such as RRT, sample the configuration space to compute feasible paths while avoiding obstacles. However, in contact-rich manipulation, interactions between the robot and objects are essential for task success. For example, Fig.1 presents three contact-rich manipulation tasks that require purposeful force interaction: (a) inserting a book into a crowded shelf, which involves pushing aside surrounding books before insertion; (b) pushing a hinged pendulum, where the robot must apply directional force to influence a rotating object under gravity; and (c) manipulating a spring-loaded clip, where one arm must apply continuous force to open the clip before the other inserts an object. These tasks demand strategic planning over contact interactions. Traditional planners may easily fail as they do not account for force interactions and the need for controlled contact. This challenge highlights the necessity of a framework that integrates motion and contact interactions while evaluating different manipulation strategies. 1 –,

![](Yang2025Recasting_figs/e90548133c0f2ed8fb8be473efacb7b032dc1f9e7fac01dfdd851de944ddc6da.jpg)

![](Yang2025Recasting_figs/f115412bfb033785da83f4dab23bf77a2bfe3b77f881357863a3fde78736f8db.jpg)  
(b) Pushing a hinged pendulum to a desired angle by applying sustained directional force.

(a) Inserting a book into a crowded shelf by first pushing aside neighboring books to create enough space for a new book.  
![](Yang2025Recasting_figs/38de710150e7833701d07ab14138a42afeb7f92ae49198d29047781888008ec3.jpg)  
(c) Opening a spring-loaded clip with one arm before inserting an object.  
Fig. 1: Three manipulation tasks require strategic force policy.

Sampling-based methods, including rapidly-exploring random trees (RRT) [2], have proven to be effective for motion planning [3]. However, their reliance on collision avoidance makes them unsuitable for contact-intensive tasks. To address contact constraints, some approaches formulate the problem within a constraint manifold [4], leading to methods such as AtlasRRT [5] and IMACS [6]. However, these solutions primarily handle geometric constraints and can fail in various scenarios, such as when an object to be inserted is obstructed by other objects. Recent work [7] extends planning to both the robot joint space and the object configuration space but does not explicitly capture the force interactions required to rearrange obstructing objects. Other approaches have shown that constructing a spatiotemporal manifold can effectively handle complex geometric constraints [8], but these also neglect force interactions.

A widely adopted approach to incorporating force interactions in manipulation is the quasi-static assumption [9]–[12], which simplifies the problem by focusing on contact forces while neglecting inertial and Coriolis effects. Recent studies [13], [14] have demonstrated that quasi-static assumption offers significant theoretical advantages, as it allows force interactions to be modeled as derivable from a smooth potential. This potential unifies robot impedance control and physical contact modeling, enabling manipulation tasks to be framed as an optimization problem based on an intrinsic Riemannian metric (so-called haptic metric), defined as the squared Hessian of the reduced potential [13]. Within this framework, system variables are separated into internal states z and control inputs u, where the control inputs u guide the movement of indirectly controllable objects z along an implicitly defined equilibrium manifold $( \mathcal { M } ^ { e q } )$ . Our earlier work [12] showed how to navigate on $\mathcal { M } ^ { e q }$ and compute optimal control policies, but a systematic exploration of implicit manifold and clear visualizations of key concepts were not provided.

While quasi-static manipulation provides a structured approach to analyzing contact-rich tasks, determining a control policy for mechanical systems remains an open challenge. Traditional quasi-static methods often require extensive manually defined contact phases [9], [10], [15], limiting their flexibility. Similarly, learning from demonstration (LfD) approaches [16], [17] rely on human-provided trajectories and encode task knowledge through manual demonstrations. On the other hand, Reinforcement learning (RL) has been explored as an alternative [18], but it typically relies on task-specific reward functions, suffers from long training times, and faces the curse of dimensionality [19]. Conversely, classical planning algorithms (e.g., RRT) are computationally efficient in highdimensional spaces, though they are not directly applicable to contact-rich tasks. Motivated by these challenges, our key contributions are as follows:

1) Sampling-based planning for contact-rich manipulation: We adapt the classical RRT planner to a quasistatic formulation, introducing HapticRRT, a method that plans over an implicit equilibrium manifold $\mathcal { M } ^ { e q }$ and incorporates visual tools to reveal how haptic metrics and obstacles emerge within this framework, providing intuitive insights into contact-rich planning.

2) Exploration of multiple manifold branches: We introduce and interpret the concept of multiple branches in $\mathcal { M } ^ { e q } .$ , highlighting their practical significance for success of manipulation tasks.

3) Validation across diverse manipulation tasks: We evaluate HapticRRT on three representative contact-rich scenarios, demonstrating that HapticRRT discovers strategic manipulation behaviors in each case.

To demonstrate the generality and significance of our approach, we evaluate HapticRRT on three manipulation tasks that represent different aspects of contact-rich planning. First, in a pendulum manipulation task, the robot must strategically apply force on an underactuated pendulum. Unlike the classical inverted pendulum [20], this task more closely resembles door handles [21]. Second, in a spring-loaded clip manipulation task, rather than using dexterous hands to squeeze the clip [22], we demonstrate non-prehensile manipulation using a standard two-finger gripper. Third, in a crowded book insertion scenario, prior methods [23], [24] often rely on carefully designed, task-specific hierarchical policies to rearrange clutter before insertion. In all three tasks, HapticRRT autonomously discovers strategic manipulation policies and identifies branches of the manifold, demonstrating its ability for generalized contact-rich planning.

## II. MANIPULATION PLANNING ON THE IMPLICIT EQUILIBRIUM MANIFOLD

Building upon our previous work [12], we briefly introduce the key concepts of our framework, including the equilibrium manifold, haptic metric, and haptic obstacle, to ensure a self-contained presentation. The novel contributions in this paper lie in the introduction of multiple equilibrium branches, which we formally define in Sec. II-B and apply classical motion planner RRT into our framework, detailed in Sec. III. Furthermore, 3 separate representative tasks and their manifold are presented in Sec. IV, VI, V.

## A. Quasi-Static Mechanical Manipulation System

Under quasi-static assumption, we describe the environment (objects) and robots as an interconnected system ${ \mathcal { Z } } \times U$ [13], [14], where $\mathbf { z } \in \mathcal { Z } \subset \mathbb { R } ^ { N }$ represents the internal state (also referred to as indirectly controllable objects) and u $\in \mathcal { U } \subset \mathbb { R } ^ { K }$ is the control of the robot (which can be interpreted as the desired pose in impedance control). The configuration of the system is determined solely by its manipulation potential $W ( \mathbf { z } , \mathbf { u } )$ such as elastic and gravitational energies. Define manipulation potential as a smooth field on the space $W : \mathcal { Z } \times \mathcal { U } \to \mathbb { R }$ Equilibria $\mathbf { z } ^ { \ast }$ are found from

$$
\partial_ {\mathbf {z}} W (\mathbf {z} ^ {*}, \mathbf {u}) = \mathbf {0} \in \mathbb {R} ^ {N}.\tag{1}
$$

We define $\begin{array} { l l l } { { \partial _ { { \bf q } } W } } & { { \equiv } } & { { [ \partial _ { q _ { 1 } } W , \ldots , \partial _ { q _ { a } } W ] ^ { T } } } \end{array}$ , where $\begin{array} { r l } { \partial _ { \mathbf { q } } } & { { } = } \end{array}$ $[ \partial _ { q _ { 1 } } , \dots , \partial _ { q _ { a } } ] ^ { T }$ . Meanwhile, define the shorthand notation $\partial _ { \mathbf { z } \mathbf { z } } ^ { 2 } ~ \equiv ~ \partial _ { \mathbf { z } } \bar { \partial } _ { \mathbf { z } } ^ { T }$ for Hessians and mixed-derivative operators. Here, $\partial _ { \mathbf { z } }$ denotes the gradient with respect to $\mathbf { z } ,$ which means internal forces acting on objects $\mathbf { z } .$ Under quasi-static assumption, the total force acting on the objects should be zero. We describe the interplays of objects and a robot, i.e., $\mathbf { f } _ { \mathrm { c t r l } } = - \partial _ { \mathbf { u } } W$ the so-called control forces [13].

A point is stable when its Hessian is positive definite, i.e., $\partial _ { \mathbf { z } \mathbf { z } } ^ { 2 } W | _ { * } \succ 0$ . Assuming the Hessian $\partial _ { \mathbf { z } \mathbf { z } } ^ { 2 } \bar { W } \in \mathbb { R } ^ { N \times N }$ is of full rank when $\partial _ { \mathbf { z } } W ( \mathbf { z } ^ { * } , \mathbf { u } ) = \mathbf { 0 }$ , via the implicit function theorem [25], the set

$$
\mathcal {M} ^ {e q} := \left\{\left(\mathbf {z}, \mathbf {u}\right) \in \mathcal {Z} \times \mathcal {U} | \partial_ {\mathbf {z}} W (\mathbf {z}, \mathbf {u}) = \mathbf {0} \right\}\tag{2}
$$

is a smooth embedded submanifold in the ambient space $( { \mathcal { Z } } \times$ U ). We refer to $\mathcal { M } ^ { e q }$ as the equilibrium manifold (EM) of the system. The state transitions are purely controlled by u. Thus, to guarantee the stability, the control should avoid getting close to singularities. Therefore, define haptic obstacle as

$$
\det (\partial_ {\mathbf {z z}} ^ {2} \mathrm{W} (\mathbf {z}, \mathbf {u})) > \lambda > 0\tag{3}
$$

where $\lambda > 0$ is a threshold based on stiffness.

## B. Multiple Branches of Manifold

Note, for quasi-static manipulations, solutions are often multi-valued, e.g., manipulating an object with two hands, there may exist multiple stable configurations for the same grasping pose. Consequently, the equilibrium manifold $\mathcal { M } ^ { e q }$ could contain multiple branches, as depicted in Fig. 2. Additionally, each stable solution $\mathbf { \Delta } ^ { m } \mathbf { z } _ { i } ^ { * }$ , with $m \geq 1$ indicating multiplicity of equilibria, can only be identified after specifying the input $\mathbf { u } _ { i } .$ , leading to a natural projection,

$$
\mathrm{pr}: \left(^ {\mathrm{m}} \mathbf {z} _ {\mathrm{i}} ^ {*}, \mathbf {u} _ {\mathrm{i}}\right) \mapsto \mathbf {u} _ {\mathrm{i}}\tag{4}
$$

In practical terms, the existence of multiple branches means that same control policies can lead to distinct object states, depending on the historical control policy.

![](Yang2025Recasting_figs/c0a8c45066c4c13df0289ea8898730ba11effde5ca65c149d389d6aa8a4237c4.jpg)  
Fig. 2: Configuration space $( { \mathcal { Z } } \times U )$ and multiple branches of equilibrium manifolds. For same control u, there could exist several internal state $\mathbf { \Delta } ^ { m } \mathbf { z } _ { i } ^ { * }$

## C. Haptic Metric and Haptic Distance

The notion of closeness between states is determined by a distance function. Following [13], [14], we defined the Riemannian metric of the control space U, where the squared Hessian $\mathbf G _ { m } ^ { 2 } ( \mathbf { z } ^ { * } ( \mathbf { u } ) , \mathbf { u } )$ is called the haptic metric, which offers a more general measure of interaction.

$$
\mathbf {G} _ {m} (\mathbf {z} ^ {*} (\mathbf {u}), \mathbf {u}) := \partial_ {\mathbf {u u}} ^ {2} W - \partial_ {\mathbf {u z}} ^ {2} W (\partial_ {\mathbf {z z}} ^ {2} W) ^ {- 1} \partial_ {\mathbf {z u}} ^ {2} W,\tag{5}
$$

which is computed as the Schur complement of the Hessian of the potential function $W ( ^ { m } { \bf z } ^ { * } , { \bf u } )$ , evaluated at equilibrium $( \mathrm { i . e . , } ^ { m } \mathbf { z } ^ { \ast } ( \mathbf { u } )$ s.t. $\partial _ { \mathbf { z } } W ( ^ { m } \mathbf { z } ^ { * } , \mathbf { u } ) = \mathbf { 0 } )$

For any control policy $\mathbf { u } ( s ) : [ 0 , 1 ] \to \mathbb { R } ^ { K }$ connecting two points in the control space, haptic distance S between any two points u(0) to u(1) is defined as,

$$
S [ \mathbf {u} ] = \int_ {0} ^ {1} \sqrt {\dot {\mathbf {u}} ^ {T} \mathbf {G} _ {m} ^ {2} (\mathbf {z} ^ {*} (\mathbf {u}) , \mathbf {u}) \dot {\mathbf {u}}} d s\tag{6}
$$

The greater force exerted by robot, the larger the value of S.

## III. HAPTICRRT

We have introduced the basic framework, and the objective is to manipulate objects z to a desired position based on the task requirements. However, since z is implicitly defined, the exact value of ${ \bf z } ^ { \ast } ( { \bf u } )$ remains unknown. In this section, we present how classical sampling-based motion planners, RRT [2], can be integrated into our framework. By leveraging the tree structure of RRT, we explore the implicit equilibrium manifold until a feasible path connecting the initial state to the desired state is found.

## A. Sampling in Control Space

Following the classical RRT approach, we assume that a tree T is being incrementally constructed. At each iteration, a random node is selected. However, instead of sampling from the entire configuration space, we restrict our selection to the control space U, choosing a random control input $\mathbf { u } _ { \mathrm { r a n d } } .$

Next, we determine the nearest node in the control space, denoted as $\mathbf { u } _ { \mathrm { n e a r } } ,$ and pair it with its corresponding state to form $\left( \mathbf { z } _ { \mathrm { n e a r } } , \mathbf { u } _ { \mathrm { n e a r } } \right)$ . Unlike standard RRT, this nearest neighbor selection considers both the Mahalanobis distance and the manipulation potential $W ( \mathbf { z } , \mathbf { u } )$ . While proximity in configuration space remains important, the algorithm is biased toward nodes with lower potential. This reflects a trade-off: some contact is required to accomplish manipulation tasks, but excessive contact may indicate that the robot is stuck. Therefore, the revised distance incorporates both geometric proximity and energetic feasibility. The geometric term is represented by the Mahalanobis distance $\lVert \mathbf { u } - \mathbf { u } _ { \mathrm { r a n d } } \rVert _ { \Sigma ^ { \sharp } }$ , and the energetic term by the manipulation potential $W ^ { \beta } ( \mathbf { z } , \mathbf { u } )$ , where $\beta$ is a tunable parameter. This is implemented in Line 3 of Alg. 1.

Importantly, we consider only nodes where the DEADEND flag is set to False, ensuring that the node remains valid for further expansion. The DEADEND label indicates whether a state encounters a haptic obstacle (as defined in Eq. 3); only states that do not face haptic obstacle are eligible for tree growth.

In classical RRT, expansion typically proceeds by moving a fixed step toward $\mathbf { u } _ { \mathrm { r a n d } }$ . However, in our framework, we must adhere to the quasi-static assumption, ensuring that the system remains on the equilibrium manifold. Direct expansion may disrupt continuity or lead to unstable configurations. Therefore, instead of taking a discrete step, we slowly move toward $\mathbf { u } _ { \mathrm { r a n d } }$ to maintain stability.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Sample a direction in control space
1: procedure SAMPLE(U, T)
2: u$_{rand}$ ← randomly select from {U}
3: u$_{near}$ ← arg min W$^{\beta}$(z, u) ||u - u$_{rand}$ ||$_{\Sigma}$, (z, u) ∈ T, DEADEND = False
4: û = (u$_{rand}$ - u$_{near}$) / ||u$_{rand}$ - u$_{near}$ ||$_{2}$
5: return û, (z$^{*}_{near}$, u$_{near}$)
</div>

## B. Extending via Adaptive ODE

To move a node along $\mathcal { M } ^ { e q } .$ , we follow the method as in our previous work [12], which employs an adaptive Ordinary Differential Equation (ODE) approach:

$$
\dot {\mathbf {z}} = - (\partial_ {\mathbf {z z}} ^ {2} W) ^ {- 1} \partial_ {\mathbf {u z}} ^ {2} W \dot {\mathbf {u}} - \eta (\partial_ {\mathbf {z z}} ^ {2} W) ^ {- 1} \partial_ {\mathbf {z}} W\tag{7}
$$

Eq. 7 consists of two key terms, the former (depicted as a blue arrow in Fig. 3) captures the linear relationship between the infinitesimal changes in z and u. The later (represented by the red arrow in Fig. 3) corresponds to Newton-Raphson infinitesimal adjustments, ensuring that the system remains on the equilibrium manifold. Since holding u constant leads to out-of-equilibrium dynamics, this correction term is necessary. The parameter η represents the step size.

![](Yang2025Recasting_figs/c6a9b8009cf9cf6f17bf3a5d1836516a3260325577b1ae7657ef1025865c88be.jpg)  
Fig. 3: Right: The adaptive ODE enables nodes to move along $\mathcal { M } ^ { e q }$ . Left: HapticRRT explores $\mathcal { M } ^ { e q }$ while ensuring that nodes remain on the manifold until either the haptic distance value reaches ϵ or the ODE is terminated by haptic obstacle.

With this approach, we can track the evolution $t \to \mathbf { z } ( t ) \in$ $\mathbb { R } ^ { N }$ as the control parameters evolve as $t \to \mathbf { u } ( t ) \in \mathbb { R } ^ { K }$ by numerically solving the adaptive ODE. This ensures that the tree structure is extended while remaining on EM.

Moreover, similar to RRT strategy of extending the tree by a fixed distance ϵ, we also extend our tree for a predetermined haptic distance. Within this framework, a functional value of haptic distance ϕ, as defined in Eq. 6, is computed using the ODE, incorporating the haptic metric. Consequently, the ODE governing the entire system can be expressed as follows:

$$
\begin{array}{l} \frac {d}{d t} \left[ \begin{array}{c} \mathbf {z} \\ \mathbf {u} \\ \phi \end{array} \right] = \left[ \begin{array}{c} - (\partial_ {\mathbf {z z}} ^ {2} W) ^ {- 1} \partial_ {\mathbf {u z}} ^ {2} W \dot {\mathbf {u}} - \eta (\partial_ {\mathbf {z z}} ^ {2} W) ^ {- 1} \partial_ {\mathbf {z}} W \\ (\mathbf {u} _ {\text {rand}} - \mathbf {u} _ {\text {near}}) / \| \mathbf {u} _ {\text {rand}} - \mathbf {u} _ {\text {near}} \| _ {2} \\ \sqrt {\dot {\mathbf {u}} ^ {T} \mathbf {G} _ {m} ^ {2} (u) \dot {\mathbf {u}}} \end{array} \right] \\ \left[ \begin{array}{c} \mathbf {z} (0) \\ \mathbf {u} (0) \\ \phi (0) \end{array} \right] = \left[ \begin{array}{c} \mathbf {z} _ {\text {near}} ^ {*} \\ \mathbf {u} _ {\text {near}} \\ 0 \end{array} \right] \end{array}\tag{8a}
$$

(8b)

One termination condition occurs when $\phi ( t ) \leq \epsilon ,$ at which point we return a new node $\left( \mathbf { z } _ { \mathrm { n e w } } , \mathbf { u } _ { \mathrm { n e w } } \right)$ and set DEADEND $= { \mathrm { F a l } } s { \mathrm { e } }$ . A false DEADEND flag indicates that the node is a valid expansion point for future tree growth. Conversely, if the node encounters a haptic obstacle (as defined in Eq. 3), tree expansion is also terminated. The EXTEND function is formally defined in $\mathrm { A l g . }$ 2.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Extend on equilibrium manifold
1: procedure EXTEND((z$_{near}$, u$_{near}$), û, ε)
2:    z(t), u(t), φ(t) ← solve ODE via Eq. 8
3:    if φ(t) &gt; ε then
4:    ▾ Stop, DEADEND ← False
5:    if det(∂zz W(z(t), u(t))) &gt; λ then
6:    ▾ Stop, DEADEND ← True
7:    return (z$_{new}$*, u$_{new}$) = (z(t), u(t)), φ(t)
</div>

## C. Overall Algorithm

Alg. 3 presents our final planning framework. We begin by initializing a stable node $\left( \mathbf { z } _ { \mathrm { s t a r t } } ^ { * } , \mathbf { u } _ { \mathrm { s t a r t } } \right)$ on EM, ensuring that the stability condition (Eq. 3) holds. Subsequently, the function SAMPLE returns both a direction and a candidate node for growth, while the function EXTEND generates a new node on EM. Finally, the new node and its corresponding edge are added to the tree, along with its DEADEND label to indicate whether further expansion is possible. The conceptual framework of HapticRRT is illustrated in Fig. 3.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 HapticRRT
Input: (z$^{*}_{start}$, u$_{start}$) ∈ M$^{eq}$ the starting point on the equilibrium manifold, ε the geodesic size and N the maximum number of attempts.
Output: A search tree T = (V, E).
1: V ← {(z$_{start}$, u$_{start}$)}; E ← ∅
2: for n = 1, ..., N do
3:    û, (z$^{*}_{near}$, u$_{near}$) ← SAMPLE(U, T)
4:    (z$^{*}_{new}$, u$_{new}$), DEADEND ← EX-
    TEND(ù, (z$^{*}_{near}$, u$_{near}$), ε)
5:    V ← V ∪ {(z$^{*}_{new}$, u$_{new}$), DEADEND}; E ← E ∪
    {(z$^{*}_{near}$, z$^{*}_{new}$), (u$_{near}$, u$_{new}$)}
6: return T = (V, E)
</div>

## IV. MANIPULATION OF A PENDULUM

In this section, we present a manipulation task involving a rectangular pendulum and a robot. Our approach employs a robot to interact with and manipulate the pendulum, where the motion of the pendulum is driven by the interaction between the robot and the pendulum [13]. To model this task, we follow the same mathematical tool as in our previous work [12], [26].

## A. Superellipses and Contact Stiffness

To apply our framework, we require only a differentiable manipulation potential. One way to obtain this is by modeling the system using superquadrics (SQ), which, in 2D, are referred to as superellipses [27]. In the following, we introduce key components of our modeling approach.

1) Superellipses: As the shape of the pendulum is rectangular, we model it by a SQ which is implicitly defined by the equation:

$$
\left(\frac {x}{a _ {1}}\right) ^ {\frac {2}{\varepsilon}} + \left(\frac {y}{a _ {2}}\right) ^ {\frac {2}{\varepsilon}} = 1\tag{9}
$$

where ε determines the shape of SQ, and $a _ { 1 } , a _ { 2 }$ define its size. To facilitate contact modeling, we rewrite Eq. 9 as an inside-outside function $F ( x , y )$ , given by:

$$
F (x, y) = \left(\frac {x}{a _ {1}}\right) ^ {\frac {2}{\varepsilon}} + \left(\frac {y}{a _ {2}}\right) ^ {\frac {2}{\varepsilon}} - 1\tag{10}
$$

which possesses a useful property. For any given point $( x _ { 0 } , y _ { 0 } )$ , Eq. 10 determines its relation to SQ: outside if $F ( x _ { 0 } , y _ { 0 } ) > 0$ , inside if $( F ( x _ { 0 } , y _ { 0 } ) < 0 )$ , and on the surface if $F ( x _ { 0 } , y _ { 0 } ) = 0$

2) Contact stiffness: The inside-outside function $F ( x , y )$ from Eq. 10 can be leveraged to model contact interaction. To capture contact behavior, we define a nonlinear stiffness function $k ( d )$ , which decides the contact force:

$$
k (d) = k _ {\mathrm{min}} + \frac {1 - \tanh (d / d _ {0})}{2} k _ {\mathrm{max}}.\tag{11}
$$

where $d _ { 0 }$ is a constant that decides the steepness of the stiffness curve, ensuring a smooth transition between the contact and non-contact states. The parameters $k _ { \mathrm { m a x } }$ and $k _ { \mathrm { m i n } }$ represent the maximum and minimum stiffness values, respectively, with $k _ { \mathrm { m a x } } \gg k _ { \mathrm { m i n } }$ . The independent variable d is computed from $F ( x , y )$ , expressed in SQ frame. Due to the properties of the inside-outside function: When the point is outside SQ (non-contact region, $F ( x , y ) \ > \ 0 )$ , the stiffness remains at its minimum value $k _ { \mathrm { m i n } }$ . When the point is inside SQ (contact region, $F ( x , y ) < 0 )$ , the stiffness increases, governed by $k ( d )$ to reflect contact interaction.

## B. Pendulum Modeling

The system consists of a pendulum and a robot in a 2D plane. The pendulum is hinged at one end to the origin with length $L _ { 0 } ,$ , and a body frame is attached at its center of mass (CoM) with mass m. As illustrated in Fig. 4a, the system’s internal state variable is the pendulum angle, defined as $\mathbf { z } = z _ { \theta } \in S ^ { 1 }$ . A 2D point robot interacts with the tip of the pendulum, applying forces to manipulate its motion. The robot is denoted by $\dot { \mathbf { u } } = [ u _ { x } , u _ { y } ] ^ { \top } \in \mathbb { R } ^ { \bar { 2 } }$ . Through this interaction, the robot indirectly controls the pendulum. The manipulation potential of the system is defined as:

$$
\begin{array}{l} W (\mathbf {z}, \mathbf {u}) = W _ {\text {grav}} (\mathbf {z}) + W _ {\text {contact}} (\mathbf {z}, \mathbf {u}), \\ \qquad = \frac {1}{2} m g L _ {0} \sin z _ {\theta} + \frac {1}{2} k \bigg ((u _ {x} - L _ {0} \cos z _ {\theta}) ^ {2} \\ \qquad \qquad + (u _ {y} - L _ {0} \sin z _ {\theta}) ^ {2} \bigg), \end{array}\tag{12}
$$

where $W _ { \mathrm { g r a v } } ( \mathbf { z } )$ represents the gravitational potential of the pendulum, $W _ { \mathrm { c o n t a c t } } ( \mathbf { z } , \mathbf { u } )$ captures the interaction energy between the pendulum and the robot. Other derivative terms can be computed analytically.

## C. HapticRRT for Pendulum Manipulation

In previous work, Campolo et al. [14] computed EM for this system, demonstrating that the manipulation of a pendulum is analogous to planning on a ’staircase’ branch within the configuration space. For further details, we refer the reader to [14].

In Fig. 5, we set the maximum number of nodes to $N = 1 0 0$ for HapticRRT. The underlying manifold, as identified by [14], is depicted in orange, serving as a backdrop for our analysis. The nodes of HapticRRT tree are represented by green points, while the edges connecting these nodes are shown as blue straight lines. Notably, when exploration begins from the ’staircase’ branch of the manifold, HapticRRT efficiently expands within this branch. Meanwhile, the red point marks where the ODE is terminated due to the presence of singularity, i.e., haptic obstacle (Eq. 3). This phenomenon commonly occurs when a node approaches the boundary of the branch or when the path leads to instability. As the node nears the boundary of the branch, it may transition into an unstable state, analogous to a scenario where a robot is holding a pendulum but suddenly releases it, leading to loss of control.

![](Yang2025Recasting_figs/3397835d612053b24ee06920db4b3323b71d91ccae4970624edbc65eb67634a5.jpg)

![](Yang2025Recasting_figs/494c75174dcfd2ea8bccb094c38f112f79822250a96764feb149fcec53301031.jpg)  
(a) System modeling.  
(b) Real world setup: pendulum with different masses.  
Fig. 4: Manipulating a hinged pendulum with varying masses via sustained directional force.

![](Yang2025Recasting_figs/17455affc2d02730252c79c49fabc9e306635d37d6a2a051e2917a91276aeb8f.jpg)  
Fig. 5: HapticRRT navigates on one branch of $\mathcal { M } ^ { e q }$ , where green nodes represents stable state, red denotes unstable states (haptic obstacle).

## D. Visualization of Haptic Metric

To better understand the concept of haptic metric, we visualize it as a blue ellipse, defined by the equation: $\mathbf { u } ^ { T } \mathbf { G } _ { m } ^ { 2 } ( \mathbf { z } ^ { * } ( \mathbf { u } ) , \mathbf { u } ) \mathbf { u } = 1$ . This ellipse is plotted in the control space $( u _ { x } , u _ { y }$ in this case), as shown in Fig. 6.

The size of the ellipse reflects the eigenvalues of the haptic metric, while the orientation of the ellipse provides further insights:

• The long axis of ellipse corresponds to smaller eigenvalues, indicating that manipulation in that direction requires less force. Thus, pushing the pendulum along the tangent direction at the tip requires less force.

• Conversely, the short axis represents the higher eigenvalue, indicating that squeezing the pendulum (applying force along to its length) requires more force.

![](Yang2025Recasting_figs/2114ad1916806065bb701b5f2dd982970d4b89dc505b36234f44c34cd577448a.jpg)  
Fig. 6: Haptic metric in control space U for the example of pendulum, while blue ellipse represents haptic metric.

• Near the outer boundary of the staircase, the ellipses are larger, suggesting that manipulating the pendulum is easier at its tip than at its origin.

## E. Experiment

We validate our method on a real world setup, as shown in Fig. 4b. A robot with a circular finger continuously pushes a hinged pendulum to rotate it toward a target configuration. The key challenge of this task is to sustain contact while adapting both the pushing direction and force according to the pendulum’s configuration and mass.

We compare the proposed HapticRRT with AtlasRRT, implemented using the OMPL library [6], where the constraint equation for the inverted pendulum encodes its geometric constraints, and an external pushing force is manually specified. Theoretically, AtlasRRT does not take mass into account, as its constraint model is purely kinematic. Therefore, when the weight of the pendulum changes, it cannot infer the required amount of force.

As shown in Table IV, when the pendulum is light (0.1 kg), both methods perform well. However, when the pendulum is heavy (0.5 kg), AtlasRRT fails while our method succeeds. This highlights a key difference between motion planning and manipulation planning where our framework incorporates contact and gravity into the manipulation potential, allowing HapticRRT to reason about the need for sustained pushing and to adapt the force accordingly, therefore spend longer time.

TABLE I: Success rate and planning time under different pendulum masses.

<table><tr><td>Method</td><td>0.1 kg pendulum</td><td>0.5 kg pendulum</td><td>Time (s)</td></tr><tr><td>AtlasRRT [6]</td><td>4/5</td><td>0/5</td><td>0.076</td></tr><tr><td>HapticRRT</td><td>5/5</td><td>5/5</td><td>0.305</td></tr></table>

## V. MANIPULATION OF SPRING-LOADED CLIP

The next manipulation task involves operating a springloaded clip and clipboard. This task requires sequential execution: the object can only be inserted after the clip has been successfully opened. Moreover, the required force to open the clip varies depending on the object’s size and the stiffness of the clip. We apply HapticRRT to this task to reason about contact forces and strategy.

![](Yang2025Recasting_figs/fe8ccdc90b424c2f0c8cd02c142fa0ab8c23d699f39feb44b78858ebf53e5ef4.jpg)

![](Yang2025Recasting_figs/6a3a6fd2cb75431a489d7b74c08a130bfb789cc6fea8319b0d3f4c7207837026.jpg)  
(a) System modeling.  
(b) Real world setup: spring-loaded clip and clipboard.  
Fig. 7: Manipulating a spring-loaded clip with varying clip type and object size.

## A. Clip System Modeling

We model the contact interaction between the object and the clip using a nonlinear stiffness function k(d) (Eq.11), along with proxies representing contact points. For details of the proxy modeling approach, we refer the reader to [12]. In brief, the proxy parameterizes the contact location on a SQ surface that is closest to the manipulated object, formulated as:

$$
\underset {\gamma} {\arg \min} \| \mathbf {c} (\mathbf {z}) - \mathbf {p} (\gamma) \|, \quad \gamma \in [ 0, 2 \pi ]\tag{13}
$$

where $\mathbf { p } ( \gamma )$ denotes the position of the proxy on the clip, and c(z) denotes the relevant corner point of the object. We have multiple proxies to capture all the contact points.

We define the manipulation potential as illustrated in Fig. 7a. To simplify the representation, we define the control and state variables as $\mathbf { u } = [ u _ { l y } , u _ { r x } ]$ and $\mathbf { z } = [ z _ { \theta } , \mathbf { z } _ { r } ]$ , where ${ \mathbf z } _ { r } =$ $[ z _ { l y } , z _ { r x } ]$ denotes the positions of the dual arm end effectors. In addition, the clip includes a rotational stiffness term $k _ { \theta }$ that resists its opening.

The overall manipulation potential is defined as:

$$
\begin{array}{l} W (\mathbf {z} ^ {*}, \mathbf {u}) = W _ {\mathrm{ctrl}} + W _ {\mathrm{clip}} + W _ {\mathrm{contact}} \\ = \frac {1}{2} (\mathbf {u} - \mathbf {z} _ {r}) ^ {T} \mathbf {K} _ {c} (\mathbf {u} - \mathbf {z} _ {r}) + \frac {1}{2} k _ {\theta} (\mathbf {z} _ {\theta} - \mathbf {z} _ {\theta , 0}) ^ {2} \\ + \sum_ {i} \sum_ {j} \frac {1}{2} k (d _ {i j}) \| \mathbf {c} _ {i j} - \mathbf {p} _ {i j} \| ^ {2} \end{array} \tag {14}\tag{14}
$$

This potential consists of three components: $W _ { \mathrm { c t r l } }$ represents the control energy applied by the robot, $W _ { \mathrm { c l i p } }$ captures the rotational resistance of the clip, and $W _ { \mathrm { c o n t a c t } }$ models the contact energy between the object and the clip.

It is worth noting that the only difference between the classical clip and the clipboard task lies in the grasping position of the robot’s left arm and pushing direction. Therefore, the manipulation potential formulation remains the similar for both cases.

## B. Multiple Branches Discovery

Branches emerge when two objects push against each other, allowing the manipulated object to slide to either side of the other object [28]. We apply HapticRRT to explore $\mathcal { M } ^ { e q }$ in clip scenario, with results shown in Fig. 8.

![](Yang2025Recasting_figs/d7f0140b6e19ef0122661c02951dc1e6a7a47296928f7cc5726ff5b101782e9a.jpg)  
(a) Multiple branches of $\mathcal { M } ^ { e q }$

![](Yang2025Recasting_figs/c47dfa692f8c847a24afd4b74cdf9062f88e6d5a04ef96700fda39c5e97f00c0.jpg)  
(b) W ${ \bf \omega } ^ { \prime } ( \mathbf { z } ^ { * } , \mathbf { u } )$ across branches.

![](Yang2025Recasting_figs/c1aad4363331826a23f55a407d5242e9b0c590847b343ff59695df98b2b05749.jpg)

![](Yang2025Recasting_figs/cf9cb3acf5a35f165fcffcd8310c9ed42e1878c3a6fa07332ac5033be1edae2c.jpg)  
(c) Grey mesh: stuck.  
(d) Orange mesh: success.  
Fig. 8: These mesh plots show the discovered branches. Grey mesh corresponds to incorrect operation sequences where the object becomes stuck in front of the clip (Fig. 8c). Orange mesh represents successful insertions following the correct sequence (Fig. 8d).

In this example, two distinct branches indicate:

• Grey branch: This branch corresponds to the robot pushing the object before opening the clip. In Fig. 8a, the grey mesh is located where $u _ { l y }$ is large (the left arm does not push the clip), and $z _ { \theta }$ remains around −0.4 (the clip remains closed). As a result, $u _ { r x }$ does not exceed $0 . 4 ,$ indicating that the object cannot enter the clip. In Fig. 8b, the grey mesh exhibits higher potential values, consistent with physical resistance.

• Orange branch: This branch corresponds to first opening the clip and then inserting the object. In Fig. 8a, the orange mesh appears when $u _ { l y }$ is close to zero (the robot opens the clip), and $z _ { \theta }$ increases accordingly. Consequently, $u _ { r x }$ approaches to zero, meaning the object successfully enters the clip. This successful behavior is also reflected in Fig. 8b, where the orange mesh has lower potential values.

## C. Comparison with Prior Method

Classical motion planners such as AtlasRRT [6] are inadequate for tasks involving contact-rich manipulation, as they do not model the state of passive objects or the required contact forces.

To address such limitations, learning-based approaches (e.g., reinforcement learning (RL) and evolutionary strategies (ES)) are often employed. In our prior work [12], we proposed a policy optimization framework that combines Dynamic Movement Primitives (DMPs) with black-box optimization (BBO). This method can be viewed as a form of policy search, conceptually related to REINFORCE and ES [29].

In this section, we compare the proposed HapticRRT with our previous BBO method. As shown in Table II, HapticRRT significantly reduces the required computation time. This result highlights the efficiency of tree-based planner over iterative optimization. Meanwhile, hapticRRT achieves optimality within the tree structure, though not necessarily global optimality. Hence hapticRRT has a larger haptic distance ϕ.

TABLE II: Comparison of HapticRRT with a prior optimization-based approach.

<table><tr><td>Method</td><td>Computing time</td><td>Haptic distance</td></tr><tr><td>DMP-BBO [12]</td><td>16.14 s</td><td>23.92</td></tr><tr><td>HapticRRT</td><td>2.74 s</td><td>27.23</td></tr></table>

## D. Experiment: Real World Validation

We validate our method in four real world cases: three involving spring-loaded clothespins with different object sizes, and one involving a clipboard. In each case, the robot uses a two-finger gripper to grasp one side of the clip, while the other side is placed against a table to enable non-prehensile manipulation, thus avoiding reliance on a dexterous hand. Another robot grasp the object to insert as Fig.7b.

TABLE III: Successful rate under different condition.

<table><tr><td>Clip Type</td><td>clothespin</td><td>clothespin</td><td>clothespin</td><td>clipboard</td></tr><tr><td>Object size</td><td>5 mm</td><td>3 mm</td><td>1 mm</td><td>5 mm</td></tr><tr><td>Success Rate</td><td>5/5</td><td>5/5</td><td>5/5</td><td>4/5</td></tr></table>

The results are summarized in Table III. For each setting, we repeat the execution of the output policy five times in the real world. All clothespin cases achieve success, while the clipboard case has a single failure (4/5 success). This demonstrates that HapticRRT produces robust and repeatable behavior for contact-rich manipulation tasks.

![](Yang2025Recasting_figs/0f3936495bf24287c414e3ec162b142bcdb1e2f02bc7c0a42a9eb1382f83eea0.jpg)  
Fig. 9: Simulation v.s. experiment: External force on left arm during clip manipulation.

We also compare the predicted contact force with real world data for the three clothespin cases. The force data is collected from the Kinova joint torque sensors, and post-processed to estimate external contact force. As shown in Fig. 9, the blue lines indicate the mean and variance over five experimental trials, while the red lines represent the predicted force $( - \partial _ { u } W )$ 1 from our framework.

The force profiles closely match. At the beginning, the left arm applies near-zero force, as opening the clip is unnecessary when the object is still far away, which conserves energy. As the object approaches the clip, HapticRRT increases the left arm’s pushing force to open the clip appropriately. Among all cases, the 5 mm object requires the highest force, as the clip must open the widest to allow insertion.

## VI. CROWDED BOOKSHELF INSERTION

Building upon our previous work [12], we apply HapticRRT to a contact-rich task: inserting a book into a crowded shelf where the available space is insufficient for direct insertion. To complete the task, the robot must first push neighboring books aside before inserting the new one.

![](Yang2025Recasting_figs/c0215a4385b7a7932cd2a76341d76d42e0b983630cbd5b70d2ba6231fbd38814.jpg)

![](Yang2025Recasting_figs/019c117a5be6562d87af3709bc105ca6566b4df666c16fa9a32c38ac75cd2666.jpg)  
(a) Modeling of book insertion.  
(b) Experimental setup.  
Fig. 10: Modeling and experimental setup of the bookshelf insertion. The book $\mathbf { z } _ { b }$ is inserted into a narrow space $( w _ { 2 } <$ $w _ { 1 } )$ under contact and resistance from neighboring books.

## A. Crowded Shelf Modeling

We reuse the modeling framework from [12], as illustrated in Fig. 10a. The robot manipulates the book in a planar space, with control input $\mathbf { u } = [ u _ { x } , u _ { y } , u _ { \theta } ] ^ { T } \in S E ( 2 )$ and book state ${ \bf z } _ { b } = [ z _ { x } , z _ { y } , z _ { \theta } ] ^ { T }$ . Two neighboring books, $\mathbf { z } _ { 1 }$ and $\mathbf { z } _ { 2 } .$ are modeled as passive bodies connected to virtual springs with stiffness matrices $\mathbf { K } _ { 1 }$ and $\mathbf { K } _ { 2 } ,$ and rest positions $\mathbf { z } _ { i , 0 } .$ . The gripper uses impedance control with stiffness matrix $\mathbf { K } _ { c } .$ As in prior sections, contact interactions are modeled using proxy γ, and the overall manipulation potential is defined as:

$$
\begin{array}{l} W (\mathbf {z} ^ {*}, \mathbf {u}) = W _ {\mathrm{ctrl}} + W _ {\mathrm{resist}} + W _ {\mathrm{contact}} \\ \qquad = \frac {1}{2} (\mathbf {u} - \mathbf {z} _ {b}) ^ {T} \mathbf {K} _ {c} (\mathbf {u} - \mathbf {z} _ {b}) \\ \qquad + \sum_ {i = 1, 2} \frac {1}{2} (\mathbf {z} _ {i} - \mathbf {z} _ {i, 0}) ^ {T} \mathbf {K} _ {i} (\mathbf {z} _ {i} - \mathbf {z} _ {i, 0}) \\ \qquad + \sum_ {i} \sum_ {j} \frac {1}{2} k (d _ {i j}) \| \mathbf {c} _ {i j} - \mathbf {p} _ {i j} \| ^ {2} \end{array}\tag{15}
$$

This potential consists of three terms: $W _ { \mathrm { c t r l } }$ is the control energy from the impedance control, $W _ { \mathrm { r e s i s t } }$ captures the passive resistance of the neighboring books, and $W _ { \mathrm { c o n t a c t } }$ models contact interactions among books.

## B. Exploring Equilibrium Manifold

We apply HapticRRT to explore $\mathcal { M } ^ { e q }$ in this bookshelf insertion task. Fig. 11 illustrates the resulting mesh representations and the exploration tree. Specifically, we visualize $z _ { y }$ against control inputs $u _ { \theta }$ and $u _ { y }$ in Fig. 11a, and the corresponding manipulation potential $W ( \mathbf { z } ^ { * } , \mathbf { u } )$ in Fig. 11b.

![](Yang2025Recasting_figs/2d0c3eac07b9efcef41c463da683dcc680879fb6cba16830a495e2aabc1592df.jpg)

![](Yang2025Recasting_figs/0954f42ac555c84ee3d7f7e085f6b02fecb4939cd1f13f2f3c8fd07ad7645ed6.jpg)  
(a) HapticRRT discovers $\mathcal { M } ^ { e q } .$ (b) $W ( \mathbf { z } ^ { * } , \mathbf { u } )$ across manifold.  
Fig. 11: HapticRRT explores $\mathcal { M } ^ { e q }$ and reveals distinct insertion strategies.

We select $z _ { y }$ as the vertical axis in Fig. 11a, since $z _ { y } = 0$ corresponds to a fully inserted book. In the grey mesh, $z _ { y }$ remains flat as $u _ { y }$ increases, indicating that the book is getting stuck in front of the neighboring books due to insufficient space. In contrast, the orange mesh represents a different strategy discovered by HapticRRT, where the robot first shifts the neighboring books to create space before inserting the target book. As a result, $z _ { y }$ increases significantly, indicating successful insertion. A similar trend is observed in Fig. 11b. When the robot pushes forward without addressing the environmental constraints, the manipulation potential $W ( \mathbf { z } ^ { * } , \mathbf { u } )$ increases continuously. In contrast, once HapticRRT discovers wedging-in policy, the potential decreases, suggesting that the task has been successfully executed.

## C. Comparison on Book Insertion

As discussed in Section V-C, we also compare HapticRRT with the DMP-BBO approach on the crowded book insertion task.

As shown in Table IV, HapticRRT again achieves significantly lower computation time, indicating superior planning efficiency. However, since this task is more complex than the previous one, the BBO method benefits from a longer optimization time, resulting in a lower haptic distance $\phi$ due to its ability to explore global optimal solutions.

TABLE IV: Compare on book insertion.

<table><tr><td>Method</td><td>Computing time</td><td>Haptic distance</td></tr><tr><td>DMP-BBO [12]</td><td>791.22 s</td><td>22.06</td></tr><tr><td>HapticRRT</td><td>48.71 s</td><td>35.78</td></tr></table>

![](Yang2025Recasting_figs/6967ab134901f15e38e95954be758c5f32bfc7a86f53407bc0cbd256a3ecba7a.jpg)

## D. Experiment: Real World Validation

The experimental setup is shown in Fig. 10b. Foam sheets are attached to both sides of the bookshelf to simulate stiffness, and several books are placed to leave a narrow slot of width w . A Kinova Gen3 robot grasps a book of width $w _ { 1 } > w _ { 2 } ,$ making direct insertion infeasible. To evaluate robustness, we vary both the book width and its initial position across trials.

TABLE V: Successful rate under different condition.

<table><tr><td>Experiment Type</td><td>initial pose</td><td>initial pose</td><td>initial pose</td><td>initial pose</td><td>initial pose</td><td>book size</td></tr><tr><td>Variation</td><td>x=-0.05 m</td><td>x=-0.025 m</td><td>x= 0 m</td><td>x=0.025 m</td><td>x=0.05 m</td><td>increased</td></tr><tr><td>Success Rate</td><td>5/5</td><td>5/5</td><td>4/5</td><td>5/5</td><td>4/5</td><td>4/5</td></tr></table>

In most cases, the control trajectory from HapticRRT successfully executed the task. However, some failures occurred due to the jagged and non-optimal nature of the trajectory, leading to excessive force application. In some cases, the book was pushed too hard, causing deformation and slippage, which resulted in failure.

(a) Simulation v.s. experiment: trajectory of the book z(t) during the insertion process.  
![](Yang2025Recasting_figs/4f1539b58a09b1f1fb1a46f0a19acfc6869576cb6beec0004c6b1ccda4234899.jpg)  
(b) Simulation v.s. experiment: External wrench during the insertion process.  
Fig. 12: Real-world implementation of HapticRRT: trajectory and force comparison.

One typical insertion policy and its real-world implementation are shown in Fig. 12. The book trajectory z(t) in both the simulation and experiment are plotted in orange and green, respectively, with the short lines indicating the book’s orientation. In the experiment, the contact force is computed from the external torque reading from robot joint sensor, and adjusted to account for the weight of the manipulated book. The simulated contact force (red curve) is defined as $- \partial _ { \mathbf { u } } W$ . Similar to previous analysis, the blue lines indicate the mean and variance over five experimental trials. HapticRRT automatically discovers an interpretable three-phase insertion strategy after initial contact:

• Push aside: The robot applies strong lateral force $( F _ { x }$ τ ) to shift the neighboring book and create space.

• Push forward: Once sufficient space is available, the robot begins insertion. The forward force $F _ { y }$ increases, reflecting resistance along the insertion axis.

• Slide in: As the book enters the shelf, resistance decreases and $F _ { x }$ converges. However, $F _ { y }$ and τ remain non-zero, since HapticRRT does not optimize for minimal force, and may apply excess effort after successful insertion.

The force trends and magnitudes in both simulation and real world trials show strong consistency, validating the effectiveness of HapticRRT in contact-rich manipulation.

## VII. CONCLUSION

In this work, we proposed HapticRRT, a haptic samplingbased motion planning algorithm within a novel manipulation framework. By integrating classical motion planning into contact-rich manipulation, our method successfully discovers multiple branches of the equilibrium manifold and finds feasible solutions for contact-rich tasks. We validated our approach in various tasks: pendulum manipulation, crowded bookshelf insertion and clip manipulation. Through these experiments, we visualized the physical meaning of haptic metrics and haptic obstacles, demonstrating the interpretability of our framework. Compared to classical motion planners, and our prior approach, HapticRRT demonstrates higher planning efficiency across diverse settings. The results demonstrate the robustness of HapticRRT, achieving a high success rate across varying conditions. Additionally, real-world experiments confirmed that the observed policy aligns well with simulation, proving the reliability of our framework. More importantly, this work bridges the gap between collision-free motion planning and manipulation planning, showcasing its broad potential for real-world applications. Future directions include improving sampling efficiency and developing an online adaptation mechanism using force feedback for realtime adjustments.

## ACKNOWLEDGMENT

This research is supported by the National Research Foundation, Singapore, under the NRF Medium Sized Centre scheme (CARTIN).

We would like to express our sincere gratitude to Donghan Yu for his insightful discussions and technical suggestions during the early stage of this work.

## REFERENCES

[1] M. Suomalainen, Y. Karayiannidis, and V. Kyrki, “A survey of robot manipulation in contact,” Robotics and Autonomous Systems, vol. 156, p. 104224, 2022.

[2] S. LaValle, “Rapidly-exploring random trees: A new tool for path planning,” Research Report 9811, 1998.

[3] J. O. Jimenez and W. Suleiman, “Visualizing high-dimensional configuration spaces: A comprehensive analytical approach,” IEEE Robotics and Automation Letters, 2024.

[4] Z. Kingston, M. Moll, and L. E. Kavraki, “Sampling-based methods for motion planning with constraints,” Annual review of control, robotics, and autonomous systems, vol. 1, pp. 159–185, 2018.

[5] L. Jaillet and J. M. Porta, “Path planning under kinematic constraints by rapidly exploring manifolds,” IEEE Transactions on Robotics, vol. 29, no. 1, pp. 105–117, 2012.

[6] Z. Kingston, M. Moll, and L. E. Kavraki, “Exploring implicit spaces for constrained sampling-based planning,” The International Journal of Robotics Research, vol. 38, no. 10-11, pp. 1151–1178, 2019.

[7] A. S. Morgan, K. Hang, B. Wen, K. Bekris, and A. M. Dollar, “Complex in-hand manipulation via compliance-enabled finger gaiting and multimodal planning,” IEEE Robotics and Automation Letters, vol. 7, no. 2, pp. 4821–4828, 2022.

[8] Y. Zhou, G. Sun, Y. Miao, Y. Zhang, X. Chen, and H. Wang, “Spatiotemporal optimal trajectory planning for safe planar manipulation of a moving object,” IEEE Transactions on Industrial Electronics, vol. 71, no. 7, pp. 7466–7476, 2023.

[9] D. E. Whitney et al., “Quasi-static assembly of compliantly supported rigid parts,” Journal of Dynamic Systems, Measurement, and Control, vol. 104, no. 1, pp. 65–77, 1982.

[10] R. Ozawa and K. Tahara, “Grasp and dexterous manipulation of multifingered robotic hands: a review from a control view point,” Advanced Robotics, vol. 31, no. 19-20, pp. 1030–1050, 2017.

[11] L. Yang, M. Z. Ariffin, B. Lou, C. Lv, and D. Campolo, “A planning framework for robotic insertion tasks via hydroelastic contact model,” Machines, vol. 11, no. 7, p. 741, 2023.

[12] L. Yang, S. H. Turlapati, C. Lv, and D. Campolo, “Planning for quasistatic manipulation tasks via an intrinsic haptic metric: A book insertion case study,” IEEE Robotics and Automation Letters, 2025.

[13] D. Campolo and F. Cardin, “A geometric framework for quasi-static manipulation of a network of elastically connected rigid bodies,” Applied Mathematical Modelling, vol. 143, p. 116003, 2025.

[14] D. Campolo and F. Cardin, “Quasi-static mechanical manipulation as an optimal process,” in 2023 62nd IEEE Conference on Decision and Control (CDC), pp. 4753–4758. IEEE, 2023.

[15] A. Salem and Y. Karayiannidis, “Robotic assembly of rounded parts with and without threads,” IEEE Robotics and Automation Letters, vol. 5, no. 2, pp. 2467–2474, 2020.

[16] D. Wang, C. Qiu, J. Lian, W. Wan, Q. Pan, and Y. Dong, “Cooperative control for dual-arm robots based on improved dynamic movement primitives,” IEEE Transactions on Industrial Electronics, 2024.

[17] N. Chen, L. Wan, and Y.-J. Pan, “Robust and adaptive dexterous manipulation with vision-based learning from multiple demonstrations,” IEEE Transactions on Industrial Electronics, 2024.

[18] <sup>´</sup>I. Elguea-Aguinaco, A. Serrano-Munoz, D. Chrysostomou, I. Inziarte-˜ Hidalgo, S. Bøgh, and N. Arana-Arexolaleiba, “A review on reinforcement learning for contact-rich robotic manipulation tasks,” Robotics and Computer-Integrated Manufacturing, vol. 81, p. 102517, 2023.

[19] Z. Bing, H. Zhou, R. Li, X. Su, F. O. Morin, K. Huang, and A. Knoll, “Solving robotic manipulation with sparse reward reinforcement learning via graph-based diversity and proximity,” IEEE Transactions on Industrial Electronics, vol. 70, no. 3, pp. 2759–2769, 2022.

[20] S. Irfan, L. Zhao, S. Ullah, A. Mehmood, and M. Fasih Uddin Butt, “Control strategies for inverted pendulum: A comparative analysis of linear, nonlinear, and artificial intelligence approaches,” Plos one, vol. 19, no. 3, p. e0298093, 2024.

[21] J. Shaikh-Mohammed, Y. Alharbi, and A. Alqahtani, “Door-opening technologies: Search for affordable assistive technology,” Technologies, vol. 11, no. 6, p. 177, 2023.

[22] U. Kim, D. Jung, H. Jeong, J. Park, H.-M. Jung, J. Cheong, H. R. Choi, H. Do, and C. Park, “Integrated linkage-driven dexterous anthropomorphic robotic hand,” Nature communications, vol. 12, no. 1, p. 7177, 2021.

[23] T. Nakajima, T. Yoshimi, M. Mizukawa, and Y. Ando, “A study of book arrangement task by robot arm-book insert operation to bookshelf,” in 2011 IEEE/SICE International Symposium on System Integration (SII), pp. 738–743. IEEE, 2011.

[24] B. Sygo, S.-C. Liu, F. Wieczorek, M. Koshil, M. Gorner, N. Hendrich,¨ and J. Zhang, “Multi-stage book perception and bimanual manipulation

for rearranging book shelves,” in International Conference on Intelligent Autonomous Systems, pp. 495–507. Springer, 2023.

[25] M. Spivak, Calculus on manifolds: a modern approach to classical theorems of advanced calculus. CRC press, 2018.

[26] L. Yang, H.-T. Nguyen, C. Lv, D. Campolo, and F. Cardin, “An energybased numerical continuation approach for quasi-static mechanical manipulation,” Data-Centric Engineering, vol. 6, p. e18, 2025.

[27] A. Jaklic, A. Leonardis, and F. Solina, Segmentation and recovery of superquadrics, vol. 20. Springer Science & Business Media, 2000.

[28] T. Poston and I. Stewart, Catastrophe theory and its applications. Courier Corporation, 2014.

[29] F. Stulp and O. Sigaud, “Robot skill learning: From reinforcement learning to evolution strategies,” Paladyn, Journal of Behavioral Robotics, vol. 4, no. 1, pp. 49–61, 2013.

![](Yang2025Recasting_figs/0b1888c063edb2c6be98ebadb6cf8d59f58994393d1fde56f4aaccedf9c1fc22.jpg)

Lin Yang received his Bachelor’s degree from Beihang University, Beijing, China, in 2022. He is currently pursuing the Ph.D. degree under the supervision of Assoc. Prof. Lyu Chen and Assoc. Prof. Domenico Campolo from the school of MAE NTU. His current research interests include contact-rich manipulation via haptcs based SLAM, planning and sim2real.

![](Yang2025Recasting_figs/7deef1428662a9fcfe17179b834a1f3f111efc96b1a50eef51005e2dbea26ac7.jpg)

Huu-Thiet Nguyen received the degree of engineer in control and automation engineering from Hanoi University of Science and Technology, Hanoi, Vietnam in 2015, and the PhD degree in electrical and electronic engineering from Nanyang Technological University, Singapore in 2022. He is currently a postdoctoral researcher at Nanyang Technological University. His research interests include robot control, robot learning, and machine learning in robotics and physical systems.

![](Yang2025Recasting_figs/0aacd2b10a8d9ee812e6b4c1ee61672672621012b8b4f1429384df84fb167408.jpg)

Chen Lv (Senior Member, IEEE) received the Ph.D. degree from the Department of Automotive Engineering, Tsinghua University, China, in 2016. From 2014 to 2015, he was a Joint Ph.D. Researcher with the EECS Department, University of California at Berkeley. He is currently an Assistant Professor with Nanyang Technology University, Singapore. His research interests include cyber-physical systems, hybrid systems, advanced vehicle control, and intelligence, where he has contributed over 90 articles and holds 12 granted Chinese patents. He received the Highly Commended Paper Award of IMechE, U.K., in 2012, the National Fellowship for Doctoral Student in 2013, the NSK Outstanding Mechanical Engineering Paper Award in 2014, China SAE Outstanding Paper Award in 2015, the 1st Class Award of China Automotive Industry Scientific and Technological Invention in 2015, Tsinghua University Outstanding Doctoral Thesis Award in 2016, and the IV2018 Best Workshop/Special Issue Paper Award. He serves as a Guest Editor for IEEE Intelligent Transportation Systems Magazine, IEEE/ASME TRANSACTIONS ON MECHATRON-ICS, and Applied Energy; and an Associate Editor/Editorial Board Member for International Journal of Vehicle Autonomous Systems, International Journal of Electric and Hybrid Vehicles, and International Journal of Vehicle Systems Modelling and Testing.

![](Yang2025Recasting_figs/1e298d3ab3307c3993d063e82f6fc85eed8550b6c1e6e4b10f62c3613f900201.jpg)

Domenico Campolo received the Ph.D. degree in microengineering from Scuola Superiore Sant’ Anna, Pisa, Italy, in 2002. He is currently an Associate Professor and the Director of the Robotics Research Centre, School of Mechanical and Aerospace Engineering, Nanyang Technological University, Singapore. He is also the Co-Founder of ArtiCares Pte Ltd., an international company specializing in rehabilitation and assistive robotics.