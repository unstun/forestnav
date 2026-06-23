---
citation_key: Yang2025Recasting
arxiv_id: 2506.00351
arxiv_url: "https://arxiv.org/abs/2506.00351"
title: "Recasting Classical Motion Planning for Contact-Rich Manipulation"
authors_short: "Lin Yang et al."
year: 2025
direction_tag: J_homotopy_topology
source: pymupdf4llm
converted_at: 2026-06-23T18:18:32Z
origin: ai+web
reviewed: false
---

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

## Recasting Classical Motion Planning for Contact-Rich Manipulation 

Lin Yang, _Student Member, IEEE_ , Huu-Thiet Nguyen, Chen Lv, _Senior Member, IEEE_ , and Domenico Campolo _[∗]_ , _Member, IEEE_ 

_**Abstract**_ **—In this work, we explore how conventional motion planning algorithms can be reapplied to contactrich manipulation tasks. Rather than focusing solely on efficiency, we investigate how manipulation aspects can be recast in terms of conventional motion-planning algorithms. Conventional motion planners, such as Rapidly-Exploring Random Trees (RRT), typically compute collision-free paths in configuration space. However, in many manipulation tasks, contact is either unavoidable or essential for task success, such as for creating space or maintaining physical equilibrium. As such, we presents Haptic Rapidly-Exploring Random Trees (HapticRRT), a planning algorithm that incorporates a recently proposed optimality measure in the context of** _**quasi-static**_ **manipulation, based on the (squared) Hessian of manipulation potential. The key contributions are** _i_ ) **adapting classical RRT to operate on the quasi-static equilibrium manifold, while deepening the interpretation of haptic obstacles and metrics;** _ii_ ) **discovering multiple manipulation strategies, corresponding to branches of the equilibrium manifold.** _iii_ ) **validating the generality of our method across three diverse manipulation tasks, each requiring only a single manipulation potential expression. The video can be found at https://youtu.be/R8aBCnCCL40.** 

_**Index Terms**_ **—Manipulation planning, haptic metric, haptic obstacle, quasi-static manipulation, pendulum pushing, crowded bookshelf insertion, spring clip manipulation.** 

## I. INTRODUCTION 

OBOTIC manipulation typically involves the robot es- **R** tablishing contact with specific objects. It is essential for the robot to maintain contact with objects to successfully accomplish the tasks [1] . Classical motion planners, such as RRT, sample the configuration space to compute feasible paths while avoiding obstacles. However, in contact-rich manipulation, interactions between the robot and objects are essential for task success. For example, Fig.1 presents three contact-rich manipulation tasks that require purposeful force interaction: (a) inserting a book into a crowded shelf, which involves pushing aside surrounding books before insertion; (b) pushing a hinged pendulum, where the robot must apply directional force to influence a rotating object under gravity; and (c) manipulating a spring-loaded clip, where one arm must apply continuous force to open the clip before the other inserts an object. These tasks demand strategic planning over contact interactions. Traditional planners may easily fail as they do not account for force interactions and the need for controlled 

All authors are with the School of Mechanical and Aerospace Engineering, Nanyang Technological University (NTU), Singapore. _∗_ Corresponding author: d.campolo@ntu.edu.sg 

contact. This challenge highlights the necessity of a framework that integrates motion and contact interactions while evaluating different manipulation strategies. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0001-10.png)


**----- Start of picture text -----**<br>
axis<br>(b) Pushing a hinged pendulum to<br>a desired angle by applying sus-<br>tained directional force.<br>robot<br>(a) Inserting a book into a<br>crowded shelf by first pushing (c) Opening a spring-loaded clip<br>aside neighboring books to cre- with one arm before inserting an<br>ate enough space for a new<br>object.<br>book.<br>**----- End of picture text -----**<br>


Fig. 1: Three manipulation tasks require strategic force policy. 

Sampling-based methods, including rapidly-exploring random trees (RRT) [2], have proven to be effective for motion planning [3]. However, their reliance on collision avoidance makes them unsuitable for contact-intensive tasks. To address contact constraints, some approaches formulate the problem within a constraint manifold [4], leading to methods such as AtlasRRT [5] and IMACS [6]. However, these solutions primarily handle geometric constraints and can fail in various scenarios, such as when an object to be inserted is obstructed by other objects. Recent work [7] extends planning to both the robot joint space and the object configuration space but does not explicitly capture the force interactions required to rearrange obstructing objects. Other approaches have shown that constructing a spatiotemporal manifold can effectively handle complex geometric constraints [8], but these also neglect force interactions. 

A widely adopted approach to incorporating force interactions in manipulation is the quasi-static assumption [9]–[12], which simplifies the problem by focusing on contact forces while neglecting inertial and Coriolis effects. Recent studies [13], [14] have demonstrated that quasi-static assumption 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

offers significant theoretical advantages, as it allows force interactions to be modeled as derivable from a smooth potential. This potential unifies robot impedance control and physical contact modeling, enabling manipulation tasks to be framed as an optimization problem based on an intrinsic Riemannian metric (so-called haptic metric), defined as the squared Hessian of the reduced potential [13]. Within this framework, system variables are separated into internal states **z** and control inputs **u** , where the control inputs **u** guide the movement of indirectly controllable objects **z** along an implicitly defined equilibrium manifold ( _M[eq]_ ). Our earlier work [12] showed how to navigate on _M[eq]_ and compute optimal control policies, but a systematic exploration of implicit manifold and clear visualizations of key concepts were not provided. 

While quasi-static manipulation provides a structured approach to analyzing contact-rich tasks, determining a control policy for mechanical systems remains an open challenge. Traditional quasi-static methods often require extensive manually defined contact phases [9], [10], [15], limiting their flexibility. Similarly, learning from demonstration (LfD) approaches [16], [17] rely on human-provided trajectories and encode task knowledge through manual demonstrations. On the other hand, Reinforcement learning (RL) has been explored as an alternative [18], but it typically relies on task-specific reward functions, suffers from long training times, and faces the curse of dimensionality [19]. Conversely, classical planning algorithms (e.g., RRT) are computationally efficient in highdimensional spaces, though they are not directly applicable to contact-rich tasks. Motivated by these challenges, our key contributions are as follows: 

- 1) **Sampling-based planning for contact-rich manipulation:** We adapt the classical RRT planner to a quasistatic formulation, introducing HapticRRT, a method that plans over an implicit equilibrium manifold _M[eq]_ and incorporates visual tools to reveal how haptic metrics and obstacles emerge within this framework, providing intuitive insights into contact-rich planning. 

- 2) **Exploration of multiple manifold branches:** We introduce and interpret the concept of multiple branches in _M[eq]_ , highlighting their practical significance for success of manipulation tasks. 

- 3) **Validation across diverse manipulation tasks:** We evaluate HapticRRT on three representative contact-rich scenarios, demonstrating that HapticRRT discovers strategic manipulation behaviors in each case. 

To demonstrate the generality and significance of our approach, we evaluate HapticRRT on three manipulation tasks that represent different aspects of contact-rich planning. First, in a _pendulum manipulation_ task, the robot must strategically apply force on an underactuated pendulum. Unlike the classical inverted pendulum [20], this task more closely resembles door handles [21]. Second, in a _spring-loaded clip manipulation_ task, rather than using dexterous hands to squeeze the clip [22], we demonstrate non-prehensile manipulation using a standard two-finger gripper. Third, in a _crowded book insertion_ scenario, prior methods [23], [24] often rely on carefully designed, task-specific hierarchical policies to 

rearrange clutter before insertion. In all three tasks, HapticRRT autonomously discovers strategic manipulation policies and identifies branches of the manifold, demonstrating its ability for generalized contact-rich planning. 

## II. MANIPULATION PLANNING ON THE IMPLICIT EQUILIBRIUM MANIFOLD 

Building upon our previous work [12], we briefly introduce the key concepts of our framework, including the equilibrium manifold, haptic metric, and haptic obstacle, to ensure a self-contained presentation. The novel contributions in this paper lie in the introduction of multiple equilibrium branches, which we formally define in Sec. II-B and apply classical motion planner RRT into our framework, detailed in Sec. III. Furthermore, 3 separate representative tasks and their manifold are presented in Sec. IV, VI, V. 

## _A. Quasi-Static Mechanical Manipulation System_ 

Under quasi-static assumption, we describe the environment (objects) and robots as an _interconnected system Z × U_ [13], [14], where **z** _∈Z ⊂_ R _[N]_ represents the _internal state_ (also referred to as indirectly controllable objects) and **u** _∈U ⊂_ R _[K]_ is the _control_ of the robot (which can be interpreted as the desired pose in impedance control). The configuration of the system is determined solely by its manipulation potential _W_ ( **z** _,_ **u** ), such as elastic and gravitational energies. Define manipulation potential as a smooth field on the space _W_ : _Z × U →_ R. Equilibria **z** _[∗]_ are found from 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0002-12.png)


We define _∂_ **q** _W ≡_ [ _∂q_ 1 _W, . . . , ∂qa W_ ] _[T]_ , where _∂_ **q** = [ _∂q_ 1 _, . . . , ∂qa_ ] _[T]_ . Meanwhile, define the shorthand notation _∂_ **zz**[2] _[≡][∂]_ **[z]** _[∂]_ **z** _[T]_ for Hessians and mixed-derivative operators. Here, _∂_ **z** denotes the gradient with respect to **z** , which means internal forces acting on objects **z** . Under quasi-static assumption, the total force acting on the objects should be zero. We describe the interplays of objects and a robot, i.e., **f** ctrl = _−∂_ **u** _W_ the so-called _control forces_ [13]. A point is stable when its Hessian is positive definite, i.e., _∂_ **zz**[2] _[W][|][∗][≻]_[0][. Assuming the Hessian] _[ ∂]_ **zz**[2] _[W][∈]_[R] _[N][×][N]_[is of full] rank when _∂_ **z** _W_ ( **z** _[∗] ,_ **u** ) = **0** , via the _implicit function theorem_ [25], the set 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0002-14.png)


is a smooth embedded submanifold in the ambient space ( _Z × U_ ). We refer to _M[eq]_ as the _equilibrium manifold_ (EM) of the system. The state transitions are purely controlled by **u** . Thus, to guarantee the stability, the control should avoid getting close to singularities. Therefore, define haptic obstacle as 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0002-16.png)


where _λ >_ 0 is a threshold based on stiffness. 

## _B. Multiple Branches of Manifold_ 

Note, for quasi-static manipulations, solutions are often _multi-valued_ , e.g., manipulating an object with two hands, there may exist multiple stable configurations for the same grasping pose. Consequently, the equilibrium manifold _M[eq]_ 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

could contain multiple branches, as depicted in Fig. 2. Additionally, each stable solution _[m]_ **z** _[∗] i_[,][with] _[m][≥]_[1][indicating] multiplicity of equilibria, can only be identified after specifying the input **u** _i_ , leading to a natural projection, 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0003-02.png)


In practical terms, the existence of multiple branches means that same control policies can lead to distinct object states, depending on the historical control policy. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0003-04.png)


**----- Start of picture text -----**<br>
ℝ [𝐾]<br>pr<br>**----- End of picture text -----**<br>


Fig. 2: Configuration space ( _Z × U_ ) and multiple branches of equilibrium manifolds. For same control **u** , there could exist several internal state _[m]_ **z** _[∗] i_[.] 

## _C. Haptic Metric and Haptic Distance_ 

The notion of closeness between states is determined by a distance function. Following [13], [14], we defined the Riemannian metric of the control space _U_ , where the squared Hessian **G**[2] _m_[(] **[z]** _[∗]_[(] **[u]**[)] _[,]_ **[ u]**[)][is][called][the] _[haptic][metric]_[,][which] offers a more general measure of interaction. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0003-08.png)


which is computed as the Schur complement of the Hessian of the potential function _W_ ( _[m]_ **z** _[∗] ,_ **u** ), evaluated at equilibrium (i.e., _[m]_ **z** _[∗]_ ( **u** ) s.t. _∂_ **z** _W_ ( _[m]_ **z** _[∗] ,_ **u** ) = **0** ). 

For any control policy **u** ( _s_ ) : [0 _,_ 1] _→_ R _[K]_ connecting two points in the control space, haptic distance _S_ between any two points **u** (0) to **u** (1) is defined as, 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0003-11.png)


The greater force exerted by robot, the larger the value of _S_ . 

## III. HAPTICRRT 

We have introduced the basic framework, and the objective is to manipulate objects **z** to a desired position based on the task requirements. However, since **z** is implicitly defined, the exact value of **z** _[∗]_ ( **u** ) remains unknown. In this section, we present how classical sampling-based motion planners, RRT [2], can be integrated into our framework. By leveraging the tree structure of RRT, we explore the implicit equilibrium manifold until a feasible path connecting the initial state to the desired state is found. 

## _A. Sampling in Control Space_ 

Following the classical RRT approach, we assume that a tree _T_ is being incrementally constructed. At each iteration, a random node is selected. However, instead of sampling from the entire configuration space, we restrict our selection to the control space _U_ , choosing a random control input **u** rand. 

Next, we determine the nearest node in the control space, denoted as **u** near, and pair it with its corresponding state to form ( **z** near _,_ **u** near). Unlike standard RRT, this nearest neighbor selection considers both the Mahalanobis distance and the manipulation potential _W_ ( **z** _,_ **u** ). While proximity in configuration space remains important, the algorithm is biased toward nodes with lower potential. This reflects a trade-off: some contact is required to accomplish manipulation tasks, but excessive contact may indicate that the robot is stuck. Therefore, the revised distance incorporates both geometric proximity and energetic feasibility. The geometric term is represented by the Mahalanobis distance _∥_ **u** _−_ **u** rand _∥_ Σ, and the energetic term by the manipulation potential _W[β]_ ( **z** _,_ **u** ), where _β_ is a tunable parameter. This is implemented in Line 3 of Alg. 1. 

Importantly, we consider only nodes where the DEADEND flag is set to False, ensuring that the node remains valid for further expansion. The DEADEND label indicates whether a state encounters a haptic obstacle (as defined in Eq. 3); only states that do not face haptic obstacle are eligible for tree growth. 

In classical RRT, expansion typically proceeds by moving a fixed step toward **u** rand. However, in our framework, we must adhere to the quasi-static assumption, ensuring that the system remains on the equilibrium manifold. Direct expansion may disrupt continuity or lead to unstable configurations. Therefore, instead of taking a discrete step, we slowly move toward **u** rand to maintain stability. 

## **Algorithm 1** Sample a direction in control space 

## 1: **procedure** SAMPLE( _U, T_ ) 

- 2: **u** rand _←_ randomly select from _{U}_ 3: **u** near _←_ arg min _W[β]_ ( **z** _,_ **u** ) _∥_ **u** _−_ **u** rand _∥_ Σ _,_ ( **z** _,_ **u** ) _∈_ **u** 

- _T ,_ DEADEND = False 

- 4: **u** ˙ = ( **u** rand _−_ **u** near) _/∥_ **u** rand _−_ **u** near _∥_ 2 5: **return u** ˙ _,_ ( **z** _[∗]_ near _[,]_ **[ u]**[near][)] 

## _B. Extending via Adaptive ODE_ 

To move a node along _M[eq]_ , we follow the method as in our previous work [12], which employs an adaptive Ordinary Differential Equation (ODE) approach: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0003-25.png)


Eq. 7 consists of two key terms, the former (depicted as a blue arrow in Fig. 3) captures the linear relationship between the infinitesimal changes in **z** and **u** . The later (represented by the red arrow in Fig. 3) corresponds to Newton-Raphson infinitesimal adjustments, ensuring that the system remains on the equilibrium manifold. Since holding **u** constant leads to 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0004-01.png)


**----- Start of picture text -----**<br>
Hap�c<br>obstacle<br>+<br>+<br>**----- End of picture text -----**<br>


Fig. 3: Right: The adaptive ODE enables nodes to move along _M[eq]_ . Left: HapticRRT explores _M[eq]_ while ensuring that nodes remain on the manifold until either the haptic distance value reaches _ϵ_ or the ODE is terminated by haptic obstacle. 

out-of-equilibrium dynamics, this correction term is necessary. The parameter _η_ represents the step size. 

With this approach, we can track the evolution _t →_ **z** ( _t_ ) _∈_ R _[N]_ as the control parameters evolve as _t →_ **u** ( _t_ ) _∈_ R _[K]_ by numerically solving the adaptive ODE. This ensures that the tree structure is extended while remaining on EM. 

Moreover, similar to RRT strategy of extending the tree by a fixed distance _ϵ_ , we also extend our tree for a predetermined haptic distance. Within this framework, a functional value of haptic distance _ϕ_ , as defined in Eq. 6, is computed using the ODE, incorporating the haptic metric. Consequently, the ODE governing the entire system can be expressed as follows: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0004-06.png)


One termination condition occurs when _ϕ_ ( _t_ ) _≤ ϵ_ , at which point we return a new node ( **z** new _,_ **u** new) and set DEADEND = False. A false DEADEND flag indicates that the node is a valid expansion point for future tree growth. Conversely, if the node encounters a haptic obstacle (as defined in Eq. 3), tree expansion is also terminated. The EXTEND function is formally defined in Alg. 2. 

## **Algorithm 2** Extend on equilibrium manifold 

1: **procedure** EXTEND(( **z** near _,_ **u** near) _,_ **u** ˙ _, ϵ_ ) 2: **z** ( _t_ ) _,_ **u** ( _t_ ) _,_ _**ϕ**_ ( _t_ ) _←_ solve ODE via Eq. 8 3: **if** _**ϕ**_ ( _t_ ) _> ϵ_ **then** 4: Stop, DEADEND _←_ False 5: **if** det( _∂_ zzW( **z** (t) _,_ **u** (t))) _> λ_ **then** 6: Stop, DEADEND _←_ True 7: **return** ( **z** _[∗] new[,]_ **[ u]** _[new]_[) = (] **[z]**[(] _[t]_[)] _[,]_ **[ u]**[(] _[t]_[))] _[,]_ _**[ ϕ]**_[(] _[t]_[)] 

## _C. Overall Algorithm_ 

Alg. 3 presents our final planning framework. We begin by initializing a stable node ( **z** _[∗]_ start _[,]_ **[ u]**[start][)][on][EM,][ensuring] that the stability condition (Eq. 3) holds. Subsequently, the function SAMPLE returns both a direction and a candidate node for growth, while the function EXTEND generates a new node on EM. Finally, the new node and its corresponding edge are added to the tree, along with its DEADEND label to indicate whether further expansion is possible. The conceptual framework of HapticRRT is illustrated in Fig. 3. 

## **Algorithm 3** HapticRRT 

**Input:** ( **z** _[∗]_ start _[,]_ **[ u]**[start][)] _[ ∈M][eq]_[the][starting][point][on][the][equi-] librium manifold, _ϵ_ the geodesic size and _N_ the maximum number of attempts. **Output:** A search tree _T_ = ( _V, E_ ). 

- 1: _V ←{_ ( **z** start _,_ **u** start) _}_ ; _E ←∅_ 

- 2: **for** _n_ = 1 _, . . . , N_ **do** 3: **u** ˙ _,_ ( **z** _[∗]_ near _[,]_ **[ u]**[near][)] _[ ←]_[S][AMPLE][(] _[U][,][ T]_[ )] 4: ( **z** _[∗]_ new _[,]_ **[ u]**[new][)] _[,]_[ D][EAD][E][ND] _[←]_[E][X][-] TEND( **u** ˙ _,_ ( **z** _[∗]_ near _[,]_ **[ u]**[near][)] _[, ϵ]_[)] 

- 5: _V ← V ∪{_ ( **z** _[∗]_ new _[,]_ **[ u]**[new][)] _[,]_[ D][EAD][E][ND] _[}]_[;] _[E][←][E][ ∪] {_ ( **z** _[∗]_ near _[,]_ **[ z]** _[∗]_ new[)] _[,]_[ (] **[u]**[near] _[,]_ **[ u]**[new][)] _[}]_ 

- 6: **return** _T_ = ( _V, E_ ) 

## IV. MANIPULATION OF A PENDULUM 

In this section, we present a manipulation task involving a rectangular pendulum and a robot. Our approach employs a robot to interact with and manipulate the pendulum, where the motion of the pendulum is driven by the interaction between the robot and the pendulum [13]. To model this task, we follow the same mathematical tool as in our previous work [12], [26]. 

## _A. Superellipses and Contact Stiffness_ 

To apply our framework, we require only a _differentiable_ manipulation potential. One way to obtain this is by modeling the system using superquadrics (SQ), which, in 2D, are referred to as superellipses [27]. In the following, we introduce key components of our modeling approach. 

_1) Superellipses:_ As the shape of the pendulum is rectangular, we model it by a SQ which is implicitly defined by the equation: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0004-21.png)


where _ε_ determines the shape of SQ, and _a_ 1 _, a_ 2 define its size. To facilitate contact modeling, we rewrite Eq. 9 as an **inside-outside** function _F_ ( _x, y_ ), given by: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0004-23.png)


which possesses a useful property. For any given point ( _x_ 0 _, y_ 0), Eq. 10 determines its relation to SQ: outside if _F_ ( _x_ 0 _, y_ 0) _>_ 0, inside if ( _F_ ( _x_ 0 _, y_ 0) _<_ 0), and on the surface if _F_ ( _x_ 0 _, y_ 0) = 0. 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

_2) Contact stiffness:_ The inside-outside function _F_ ( _x, y_ ) from Eq. 10 can be leveraged to model contact interaction. To capture contact behavior, we define a nonlinear stiffness function _k_ ( _d_ ), which decides the contact force: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0005-02.png)


where _d_ 0 is a constant that decides the steepness of the stiffness curve, ensuring a smooth transition between the contact and non-contact states. The parameters _k_ max and _k_ min represent the maximum and minimum stiffness values, respectively, with _k_ max _≫ k_ min. The independent variable _d_ is computed from _F_ ( _x, y_ ), expressed in SQ frame. Due to the properties of the inside-outside function: When the point is outside SQ (non-contact region, _F_ ( _x, y_ ) _>_ 0), the stiffness remains at its minimum value _k_ min. When the point is inside SQ (contact region, _F_ ( _x, y_ ) _<_ 0), the stiffness increases, governed by _k_ ( _d_ ), to reflect contact interaction. 

## _B. Pendulum Modeling_ 

The system consists of a pendulum and a robot in a 2D plane. The pendulum is hinged at one end to the origin with length _L_ 0, and a body frame is attached at its center of mass (CoM) with mass _m_ . As illustrated in Fig. 4a, the system’s internal state variable is the pendulum angle, defined as **z** = _zθ ∈ S_[1] . A 2D point robot interacts with the tip of the pendulum, applying forces to manipulate its motion. The robot is denoted by **u** = [ _ux, uy_ ] _[⊤] ∈_ R[2] . Through this interaction, the robot indirectly controls the pendulum. The manipulation potential of the system is defined as: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0005-06.png)


where _W_ grav( **z** ) represents the gravitational potential of the pendulum, _W_ contact( **z** _,_ **u** ) captures the interaction energy between the pendulum and the robot. Other derivative terms can be computed analytically. 

## _C. HapticRRT for Pendulum Manipulation_ 

In previous work, Campolo et al. [14] computed EM for this system, demonstrating that the manipulation of a pendulum is analogous to planning on a ’staircase’ branch within the configuration space. For further details, we refer the reader to [14]. 

In Fig. 5, we set the maximum number of nodes to _N_ = 100 for HapticRRT. The underlying manifold, as identified by [14], is depicted in orange, serving as a backdrop for our analysis. The nodes of HapticRRT tree are represented by green points, while the edges connecting these nodes are shown as blue straight lines. Notably, when exploration begins from the ’staircase’ branch of the manifold, HapticRRT efficiently expands within this branch. Meanwhile, the red point marks where the ODE is terminated due to the presence of singularity, i.e., 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0005-11.png)


**----- Start of picture text -----**<br>
different mass<br>world<br>kinova<br>(b) Real world setup: pendu-<br>(a) System modeling. lum with different masses.<br>+<br>+<br>**----- End of picture text -----**<br>


Fig. 4: Manipulating a hinged pendulum with varying masses via sustained directional force. 

haptic obstacle (Eq. 3). This phenomenon commonly occurs when a node approaches the boundary of the branch or when the path leads to instability. As the node nears the boundary of the branch, it may transition into an unstable state, analogous to a scenario where a robot is holding a pendulum but suddenly releases it, leading to loss of control. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0005-14.png)


**----- Start of picture text -----**<br>
4<br>2<br>1<br>0<br>0.5<br>-2<br>0<br>-4<br>-1 -0.5<br>-0.5<br>0 0.5 -1 uy [m]<br>ux [m] 1<br>z* [rad]<br>**----- End of picture text -----**<br>


Fig. 5: HapticRRT navigates on one branch of _M[eq]_ , where green nodes represents stable state, red denotes unstable states (haptic obstacle). 

## _D. Visualization of Haptic Metric_ 

To better understand the concept of haptic metric, we visualize it as a blue ellipse, defined by the equation: **u** _[T]_ **G**[2] _m_[(] **[z]** _[∗]_[(] **[u]**[)] _[,]_ **[ u]**[)] **[u]**[=][1][.][This][ellipse][is][plotted][in][the][control] space ( _ux, uy_ in this case), as shown in Fig. 6. 

The size of the ellipse reflects the eigenvalues of the haptic metric, while the orientation of the ellipse provides further insights: 

- The long axis of ellipse corresponds to smaller eigenvalues, indicating that manipulation in that direction requires less force. Thus, pushing the pendulum along the tangent direction at the tip requires less force. 

- Conversely, the short axis represents the higher eigenvalue, indicating that squeezing the pendulum (applying force along to its length) requires more force. 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0006-01.png)


**----- Start of picture text -----**<br>
successfully opened. Moreover, the required force to open the<br>4 clip varies depending on the object’s size and the stiffness of<br>the clip. We apply HapticRRT to this task to reason about<br>2 contact forces and strategy.<br>0<br>-2<br>robot<br>-4 clip<br>1<br>0.5<br>0<br>1<br>-0.5 0.5<br>0<br>uy [m] -1 -1 -0.5 ux [m] clipboard<br>Haptic metric in control space U for the example of<br>while blue ellipse represents haptic metric. (b) Real world setup: spring-loaded<br>(a) System modeling. clip and clipboard.<br>z* [rad]<br>**----- End of picture text -----**<br>


successfully opened. Moreover, the required force to open the clip varies depending on the object’s size and the stiffness of the clip. We apply _HapticRRT_ to this task to reason about contact forces and strategy. 

Fig. 6: Haptic metric in control space _U_ for the example of pendulum, while blue ellipse represents haptic metric. 

Fig. 7: Manipulating a spring-loaded clip with varying clip type and object size. 

- Near the outer boundary of the staircase, the ellipses are larger, suggesting that manipulating the pendulum is easier at its tip than at its origin. 

## _A. Clip System Modeling_ 

## _E. Experiment_ 

We validate our method on a real world setup, as shown in Fig. 4b. A robot with a circular finger continuously pushes a hinged pendulum to rotate it toward a target configuration. The key challenge of this task is to sustain contact while adapting both the pushing direction and force according to the pendulum’s configuration and mass. 

We compare the proposed _HapticRRT_ with _AtlasRRT_ , implemented using the OMPL library [6], where the constraint equation for the inverted pendulum encodes its geometric constraints, and an external pushing force is manually specified. Theoretically, AtlasRRT does not take mass into account, as its constraint model is purely kinematic. Therefore, when the weight of the pendulum changes, it cannot infer the required amount of force. 

As shown in Table IV, when the pendulum is light (0.1 kg), both methods perform well. However, when the pendulum is heavy (0.5 kg), AtlasRRT fails while our method succeeds. This highlights a key difference between motion planning and manipulation planning where our framework incorporates contact and gravity into the manipulation potential, allowing HapticRRT to reason about the need for sustained pushing and to adapt the force accordingly, therefore spend longer time. 

TABLE I: Success rate and planning time under different **pendulum masses** . 

|**Method**|**0.1 kg pendulum**|**0.5 kg pendulum**|**Time (s)**|
|---|---|---|---|
|**AtlasRRT [6]**<br>**HapticRRT**|4/5<br>5/5|0/5<br>5/5|0.076<br>0.305|



## V. MANIPULATION OF SPRING-LOADED CLIP 

The next manipulation task involves operating a springloaded clip and clipboard. This task requires sequential execution: the object can only be inserted after the clip has been 

We model the contact interaction between the object and the clip using a nonlinear stiffness function _k_ ( _d_ ) (Eq.11), along with proxies representing contact points. For details of the proxy modeling approach, we refer the reader to [12]. In brief, the proxy parameterizes the contact location on a SQ surface that is closest to the manipulated object, formulated as: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0006-16.png)


where **p** ( _γ_ ) denotes the position of the proxy on the clip, and **c** ( **z** ) denotes the relevant corner point of the object. We have multiple proxies to capture all the contact points. 

We define the manipulation potential as illustrated in Fig. 7a. To simplify the representation, we define the control and state variables as **u** = [ _uly, urx_ ] and **z** = [ _zθ,_ **z** _r_ ], where **z** _r_ = [ _zly, zrx_ ] denotes the positions of the dual arm end effectors. In addition, the clip includes a rotational stiffness term _kθ_ that resists its opening. 

The overall manipulation potential is defined as: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0006-20.png)


This potential consists of three components: _W_ ctrl represents the control energy applied by the robot, _W_ clip captures the rotational resistance of the clip, and _W_ contact models the contact energy between the object and the clip. 

It is worth noting that the only difference between the classical clip and the clipboard task lies in the grasping position of the robot’s left arm and pushing direction. Therefore, the manipulation potential formulation remains the similar for both cases. 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

## _B. Multiple Branches Discovery_ 

Branches emerge when two objects push against each other, allowing the manipulated object to slide to either side of the other object [28]. We apply _HapticRRT_ to explore _M[eq]_ in clip scenario, with results shown in Fig. 8. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-03.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-04.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-05.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-06.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-07.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-08.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-09.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-10.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-11.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-12.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-13.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-14.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-15.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-16.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-17.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-18.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-19.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-20.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-21.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-22.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-23.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-24.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-25.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-26.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-27.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-28.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-29.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-30.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-31.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-32.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-33.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-34.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-35.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-36.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-37.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-38.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-39.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-40.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-41.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-42.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-43.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-44.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-45.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-46.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-47.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-48.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-49.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-50.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-51.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-52.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-53.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-54.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-55.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-56.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-57.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-58.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-59.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-60.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-61.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-62.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-63.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-64.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-65.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-66.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-67.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-68.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-69.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-70.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-71.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-72.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-73.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-74.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-75.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-76.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-77.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-78.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-79.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-80.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-81.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-82.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-83.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-84.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-85.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-86.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-87.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-88.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-89.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-90.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-91.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-92.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-93.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-94.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-95.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-96.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-97.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-98.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-99.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-100.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-101.png)


**----- Start of picture text -----**<br>
(a) Multiple branches of M [eq] . (b) W ( z [∗] ,  u ) across branches.<br># 10 [-3] # 10 [-3]<br>20 20<br>10 10<br>0 0<br>-0.04 -0.02 0 0.02 0.04 0.06 -0.04 -0.02 0 0.02 0.04 0.06<br>X [m] X [m]<br>(c) Grey mesh: stuck. (d) Orange mesh: success.<br>Y [m] Y [m]<br>**----- End of picture text -----**<br>


Fig. 8: These mesh plots show the discovered branches. Grey mesh corresponds to incorrect operation sequences where the object becomes stuck in front of the clip (Fig. 8c). Orange mesh represents successful insertions following the correct sequence (Fig. 8d). 

In this example, two distinct branches indicate: 

- **Grey branch:** This branch corresponds to the robot pushing the object before opening the clip. In Fig. 8a, the grey mesh is located where _uly_ is large (the left arm does not push the clip), and _zθ_ remains around _−_ 0 _._ 4 (the clip remains closed). As a result, _urx_ does not exceed 0.4, indicating that the object cannot enter the clip. In Fig. 8b, the grey mesh exhibits higher potential values, consistent with physical resistance. 

- **Orange branch:** This branch corresponds to first opening the clip and then inserting the object. In Fig. 8a, the orange mesh appears when _uly_ is close to zero (the robot opens the clip), and _zθ_ increases accordingly. Consequently, _urx_ approaches to zero, meaning the object successfully enters the clip. This successful behavior is also reflected in Fig. 8b, where the orange mesh has lower potential values. 

## _C. Comparison with Prior Method_ 

Classical motion planners such as AtlasRRT [6] are inadequate for tasks involving contact-rich manipulation, as they do not model the state of passive objects or the required contact forces. 

To address such limitations, learning-based approaches (e.g., reinforcement learning (RL) and evolutionary strategies (ES)) are often employed. In our prior work [12], we proposed a policy optimization framework that combines Dynamic Movement Primitives (DMPs) with black-box optimization (BBO). This method can be viewed as a form of policy search, conceptually related to REINFORCE and ES [29]. 

In this section, we compare the proposed HapticRRT with our previous BBO method. As shown in Table II, HapticRRT significantly reduces the required computation time. This result highlights the efficiency of tree-based planner over iterative optimization. Meanwhile, hapticRRT achieves optimality within the tree structure, though not necessarily global optimality. Hence hapticRRT has a larger haptic distance _ϕ_ . 

TABLE II: Comparison of HapticRRT with a prior optimization-based approach. 

|**Method**|Computing time|Haptic distance|
|---|---|---|
|**DMP-BBO [12]**|16.14 s|23.92|
|**HapticRRT**|2.74 s|27.23|



## _D. Experiment: Real World Validation_ 

We validate our method in four real world cases: three involving spring-loaded clothespins with different object sizes, and one involving a clipboard. In each case, the robot uses a two-finger gripper to grasp one side of the clip, while the other side is placed against a table to enable non-prehensile manipulation, thus avoiding reliance on a dexterous hand. Another robot grasp the object to insert as Fig.7b. 

TABLE III: Successful rate under different condition. 

||**Clip Type**|clothespin|clothespin|clothespin|clipboard|
|---|---|---|---|---|---|
||**Object size**|5 mm|3 mm|1 mm|5 mm|
||**Success Rate**|5/5|5/5|5/5|4/5|



The results are summarized in Table III. For each setting, we repeat the execution of the output policy five times in the real world. All clothespin cases achieve success, while the clipboard case has a single failure (4/5 success). This demonstrates that HapticRRT produces robust and repeatable behavior for contact-rich manipulation tasks. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0007-117.png)


**----- Start of picture text -----**<br>
4 Simulated vs. Experimental Force - 1 mm object<br>2 ±1 Std<br>Mean freal<br>0 fsimu<br>-2<br>0 2 4 6 8 10 12 14 16 18 20<br>Time (s)<br>4 Simulated vs. Experimental Force - 3 mm object<br>2 ±1 Std<br>Mean freal<br>0 fsimu<br>-2<br>0 2 4 6 8 10 12 14 16<br>Time (s)<br>Simulated vs. Experimental Force - 5 mm object<br>4<br>±1 Std<br>2 Mean freal<br>0 fsimu<br>-2<br>0 5 10 15 20<br>Time (s)<br> (N)Fy<br> (N)Fy<br> (N)Fy<br>**----- End of picture text -----**<br>


Fig. 9: Simulation v.s. experiment: External force on left arm during clip manipulation. 

We also compare the predicted contact force with real world data for the three clothespin cases. The force data is collected from the Kinova joint torque sensors, and post-processed to 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

estimate external contact force. As shown in Fig. 9, the blue lines indicate the mean and variance over five experimental trials, while the red lines represent the predicted force ( _−∂uW_ ) from our framework. 

The force profiles closely match. At the beginning, the left arm applies near-zero force, as opening the clip is unnecessary when the object is still far away, which conserves energy. As the object approaches the clip, HapticRRT increases the left arm’s pushing force to open the clip appropriately. Among all cases, the 5 mm object requires the highest force, as the clip must open the widest to allow insertion. 

## VI. CROWDED BOOKSHELF INSERTION 

Building upon our previous work [12], we apply HapticRRT to a contact-rich task: inserting a book into a crowded shelf where the available space is insufficient for direct insertion. To complete the task, the robot must first push neighboring books aside before inserting the new one. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-05.png)


**----- Start of picture text -----**<br>
foam<br>kinova<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-06.png)


**----- Start of picture text -----**<br>
world<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-07.png)


**----- Start of picture text -----**<br>
(a) Modeling of book insertion. (b) Experimental setup.<br>**----- End of picture text -----**<br>


Fig. 10: Modeling and experimental setup of the bookshelf insertion. The book **z** _b_ is inserted into a narrow space ( _w_ 2 _< w_ 1) under contact and resistance from neighboring books. 

## _A. Crowded Shelf Modeling_ 

We reuse the modeling framework from [12], as illustrated in Fig. 10a. The robot manipulates the book in a planar space, with control input **u** = [ _ux, uy, uθ_ ] _[T] ∈ SE_ (2) and book state **z** _b_ = [ _zx, zy, zθ_ ] _[T]_ . Two neighboring books, **z** 1 and **z** 2, are modeled as passive bodies connected to virtual springs with stiffness matrices **K** 1 and **K** 2, and rest positions **z** _i,_ 0. The gripper uses impedance control with stiffness matrix **K** _c_ . As in prior sections, contact interactions are modeled using proxy _γ_ , and the overall manipulation potential is defined as: 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-11.png)


This potential consists of three terms: _W_ ctrl is the control energy from the impedance control, _W_ resist captures the passive resistance of the neighboring books, and _W_ contact models contact interactions among books. 

## _B. Exploring Equilibrium Manifold_ 

We apply HapticRRT to explore _M[eq]_ in this bookshelf insertion task. Fig. 11 illustrates the resulting mesh representations and the exploration tree. Specifically, we visualize _zy_ against control inputs _uθ_ and _uy_ in Fig. 11a, and the corresponding manipulation potential _W_ ( **z** _[∗] ,_ **u** ) in Fig. 11b. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-15.png)


**----- Start of picture text -----**<br>
z*  v.s. u<br>y<br>70<br>0.1<br>-0.1-0.2-0.30 19542423 3 23911673851663611237362610432128 [57] 25134034659176652227114335620197304615314945272958693560555018648 4762415124446848534265<br>-0.5<br>0 0.5 -0.2 0 0.2<br>u 3  (rad) uy (m)<br>z y<br>*  (m)<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-16.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-17.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-18.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-19.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-20.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-21.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-22.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-23.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-24.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-25.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-26.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-27.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-28.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-29.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-30.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-31.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-32.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-33.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-34.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-35.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-36.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-37.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-38.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-39.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-40.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-41.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-42.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-43.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-44.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-45.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-46.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-47.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-48.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-49.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-50.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-51.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-52.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-53.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-54.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-55.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-56.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-57.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-58.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-59.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-60.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-61.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-62.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-63.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-64.png)



![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0008-65.png)


**----- Start of picture text -----**<br>
(a) HapticRRT discovers M [eq] . (b) W ( z [∗] ,  u ) across manifold.<br>**----- End of picture text -----**<br>


Fig. 11: HapticRRT explores _M[eq]_ and reveals distinct insertion strategies. 

We select _zy_ as the vertical axis in Fig. 11a, since _zy_ = 0 corresponds to a fully inserted book. In the grey mesh, _zy_ remains flat as _uy_ increases, indicating that the book is getting stuck in front of the neighboring books due to insufficient space. In contrast, the orange mesh represents a different strategy discovered by HapticRRT, where the robot first shifts the neighboring books to create space before inserting the target book. As a result, _zy_ increases significantly, indicating successful insertion. A similar trend is observed in Fig. 11b. When the robot pushes forward without addressing the environmental constraints, the manipulation potential _W_ ( **z** _[∗] ,_ **u** ) increases continuously. In contrast, once HapticRRT discovers wedging-in policy, the potential decreases, suggesting that the task has been successfully executed. 

## _C. Comparison on Book Insertion_ 

As discussed in Section V-C, we also compare HapticRRT with the DMP-BBO approach on the crowded book insertion task. 

As shown in Table IV, HapticRRT again achieves significantly lower computation time, indicating superior planning efficiency. However, since this task is more complex than the previous one, the BBO method benefits from a longer optimization time, resulting in a lower haptic distance _ϕ_ due to its ability to explore global optimal solutions. 

TABLE IV: Compare on book insertion. 

||**Method**|Computing time|Haptic distance|
|---|---|---|---|
||**DMP-BBO [12]**<br>**HapticRRT**|791.22 s<br>48.71 s|22.06<br>35.78|



IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

## _D. Experiment: Real World Validation_ 

The experimental setup is shown in Fig. 10b. Foam sheets are attached to both sides of the bookshelf to simulate stiffness, and several books are placed to leave a narrow slot of width _w_ 2. A Kinova Gen3 robot grasps a book of width _w_ 1 _> w_ 2, making direct insertion infeasible. To evaluate robustness, we vary both the book width and its initial position across trials. 

TABLE V: Successful rate under different condition. 

|**Experiment Type**|initial pose|initial pose|initial pose|initial pose|initial pose|book size|
|---|---|---|---|---|---|---|
|**Variation**|x=-0.05 m|x=-0.025 m|x= 0 m|x=0.025 m|x=0.05 m|increased|
|**Success Rate**|5/5|5/5|4/5|5/5|4/5|4/5|



In most cases, the control trajectory from HapticRRT successfully executed the task. However, some failures occurred due to the jagged and non-optimal nature of the trajectory, leading to excessive force application. In some cases, the book was pushed too hard, causing deformation and slippage, which resulted in failure. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0009-06.png)


**----- Start of picture text -----**<br>
Push aside Push forward Slide in<br>0.05 0.05 0.05<br>0 0 0<br>-0.05 -0.05 -0.05<br>-0.1 -0.1 -0.1<br>-0.15 -0.15 -0.15<br>-0.2 -0.2 -0.2<br>-0.25 -0.25 -0.25<br>simulation simulation simulation<br>-0.3 experiment -0.3 experiment -0.3 experiment<br>-0.35 -0.35 -0.35<br>-0.1 0 0.1 -0.1 0 0.1 -0.1 0 0.1<br>x (m) x (m) x (m)<br>(a) Simulation v.s. experiment: trajectory of the book  z ( t )<br>during the insertion process.<br>Simulated v.s. experimental force<br>20<br>±1 Std<br>0 Mean<br>Simulated<br>-20<br>0 5 10 15 20 25 30 35 40<br>Time<br>Simulated v.s. experimental force<br>0<br>-20 ±1 StdMean<br>Simulated<br>-40<br>0 5 10 15 20 25 30 35 40<br>Time<br>Simulated v.s. experimental force<br>5<br>±1 Std<br>0 Mean<br>Simulated<br>-5<br>0 5 10 15 20 25 30 35 40<br>Time<br>(b) Simulation v.s. experiment: External wrench during the<br>insertion process.<br>y (m) y (m) y (m)<br>Fx<br>Fy<br>=<br>**----- End of picture text -----**<br>


Fig. 12: Real-world implementation of HapticRRT: trajectory and force comparison. 

One typical insertion policy and its real-world implementation are shown in Fig. 12. The book trajectory **z** ( _t_ ) in both the simulation and experiment are plotted in orange and green, respectively, with the short lines indicating the book’s orientation. In the experiment, the contact force is computed 

from the external torque reading from robot joint sensor, and adjusted to account for the weight of the manipulated book. The simulated contact force (red curve) is defined as _−∂_ **u** _W_ . Similar to previous analysis, the blue lines indicate the mean and variance over five experimental trials. HapticRRT automatically discovers an interpretable three-phase insertion strategy after initial contact: 

- **Push aside:** The robot applies strong lateral force ( _Fx_ , _τ_ ) to shift the neighboring book and create space. 

- **Push forward:** Once sufficient space is available, the robot begins insertion. The forward force _Fy_ increases, reflecting resistance along the insertion axis. 

- **Slide in:** As the book enters the shelf, resistance decreases and _Fx_ converges. However, _Fy_ and _τ_ remain non-zero, since HapticRRT does not optimize for minimal force, and may apply excess effort after successful insertion. 

The force trends and magnitudes in both simulation and real world trials show strong consistency, validating the effectiveness of HapticRRT in contact-rich manipulation. 

## VII. CONCLUSION 

In this work, we proposed HapticRRT, a haptic samplingbased motion planning algorithm within a novel manipulation framework. By integrating classical motion planning into contact-rich manipulation, our method successfully discovers multiple branches of the equilibrium manifold and finds feasible solutions for contact-rich tasks. We validated our approach in various tasks: pendulum manipulation, crowded bookshelf insertion and clip manipulation. Through these experiments, we visualized the physical meaning of haptic metrics and haptic obstacles, demonstrating the interpretability of our framework. Compared to classical motion planners, and our prior approach, HapticRRT demonstrates higher planning efficiency across diverse settings. The results demonstrate the robustness of HapticRRT, achieving a high success rate across varying conditions. Additionally, real-world experiments confirmed that the observed policy aligns well with simulation, proving the reliability of our framework. More importantly, this work bridges the gap between collision-free motion planning and manipulation planning, showcasing its broad potential for real-world applications. Future directions include improving sampling efficiency and developing an online adaptation mechanism using force feedback for realtime adjustments. 

## ACKNOWLEDGMENT 

This research is supported by the National Research Foundation, Singapore, under the NRF Medium Sized Centre scheme (CARTIN). 

We would like to express our sincere gratitude to Donghan Yu for his insightful discussions and technical suggestions during the early stage of this work. 

## REFERENCES 

- [1] M. Suomalainen, Y. Karayiannidis, and V. Kyrki, “A survey of robot manipulation in contact,” _Robotics and Autonomous Systems_ , vol. 156, p. 104224, 2022. 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

- [2] S. LaValle, “Rapidly-exploring random trees: A new tool for path planning,” _Research Report 9811_ , 1998. 

- [3] J. O. Jimenez and W. Suleiman, “Visualizing high-dimensional configuration spaces: A comprehensive analytical approach,” _IEEE Robotics and Automation Letters_ , 2024. 

- [4] Z. Kingston, M. Moll, and L. E. Kavraki, “Sampling-based methods for motion planning with constraints,” _Annual review of control, robotics, and autonomous systems_ , vol. 1, pp. 159–185, 2018. 

- [5] L. Jaillet and J. M. Porta, “Path planning under kinematic constraints by rapidly exploring manifolds,” _IEEE Transactions on Robotics_ , vol. 29, no. 1, pp. 105–117, 2012. 

- [6] Z. Kingston, M. Moll, and L. E. Kavraki, “Exploring implicit spaces for constrained sampling-based planning,” _The International Journal of Robotics Research_ , vol. 38, no. 10-11, pp. 1151–1178, 2019. 

- [7] A. S. Morgan, K. Hang, B. Wen, K. Bekris, and A. M. Dollar, “Complex in-hand manipulation via compliance-enabled finger gaiting and multimodal planning,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 4821–4828, 2022. 

- [8] Y. Zhou, G. Sun, Y. Miao, Y. Zhang, X. Chen, and H. Wang, “Spatiotemporal optimal trajectory planning for safe planar manipulation of a moving object,” _IEEE Transactions on Industrial Electronics_ , vol. 71, no. 7, pp. 7466–7476, 2023. 

- [9] D. E. Whitney _et al._ , “Quasi-static assembly of compliantly supported rigid parts,” _Journal of Dynamic Systems, Measurement, and Control_ , vol. 104, no. 1, pp. 65–77, 1982. 

- [10] R. Ozawa and K. Tahara, “Grasp and dexterous manipulation of multifingered robotic hands: a review from a control view point,” _Advanced Robotics_ , vol. 31, no. 19-20, pp. 1030–1050, 2017. 

- [11] L. Yang, M. Z. Ariffin, B. Lou, C. Lv, and D. Campolo, “A planning framework for robotic insertion tasks via hydroelastic contact model,” _Machines_ , vol. 11, no. 7, p. 741, 2023. 

- [12] L. Yang, S. H. Turlapati, C. Lv, and D. Campolo, “Planning for quasistatic manipulation tasks via an intrinsic haptic metric: A book insertion case study,” _IEEE Robotics and Automation Letters_ , 2025. 

- [13] D. Campolo and F. Cardin, “A geometric framework for quasi-static manipulation of a network of elastically connected rigid bodies,” _Applied Mathematical Modelling_ , vol. 143, p. 116003, 2025. 

- [14] D. Campolo and F. Cardin, “Quasi-static mechanical manipulation as an optimal process,” in _2023 62nd IEEE Conference on Decision and Control (CDC)_ , pp. 4753–4758. IEEE, 2023. 

- [15] A. Salem and Y. Karayiannidis, “Robotic assembly of rounded parts with and without threads,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 2467–2474, 2020. 

- [16] D. Wang, C. Qiu, J. Lian, W. Wan, Q. Pan, and Y. Dong, “Cooperative control for dual-arm robots based on improved dynamic movement primitives,” _IEEE Transactions on Industrial Electronics_ , 2024. 

- [17] N. Chen, L. Wan, and Y.-J. Pan, “Robust and adaptive dexterous manipulation with vision-based learning from multiple demonstrations,” _IEEE Transactions on Industrial Electronics_ , 2024. 

- [18][´] I. Elguea-Aguinaco, A. Serrano-Mu˜noz, D. Chrysostomou, I. InziarteHidalgo, S. Bøgh, and N. Arana-Arexolaleiba, “A review on reinforcement learning for contact-rich robotic manipulation tasks,” _Robotics and Computer-Integrated Manufacturing_ , vol. 81, p. 102517, 2023. 

- [19] Z. Bing, H. Zhou, R. Li, X. Su, F. O. Morin, K. Huang, and A. Knoll, “Solving robotic manipulation with sparse reward reinforcement learning via graph-based diversity and proximity,” _IEEE Transactions on Industrial Electronics_ , vol. 70, no. 3, pp. 2759–2769, 2022. 

- [20] S. Irfan, L. Zhao, S. Ullah, A. Mehmood, and M. Fasih Uddin Butt, “Control strategies for inverted pendulum: A comparative analysis of linear, nonlinear, and artificial intelligence approaches,” _Plos one_ , vol. 19, no. 3, p. e0298093, 2024. 

- [21] J. Shaikh-Mohammed, Y. Alharbi, and A. Alqahtani, “Door-opening technologies: Search for affordable assistive technology,” _Technologies_ , vol. 11, no. 6, p. 177, 2023. 

- [22] U. Kim, D. Jung, H. Jeong, J. Park, H.-M. Jung, J. Cheong, H. R. Choi, H. Do, and C. Park, “Integrated linkage-driven dexterous anthropomorphic robotic hand,” _Nature communications_ , vol. 12, no. 1, p. 7177, 2021. 

- [23] T. Nakajima, T. Yoshimi, M. Mizukawa, and Y. Ando, “A study of book arrangement task by robot arm-book insert operation to bookshelf,” in _2011 IEEE/SICE International Symposium on System Integration (SII)_ , pp. 738–743. IEEE, 2011. 

- [24] B. Sygo, S.-C. Liu, F. Wieczorek, M. Koshil, M. G¨orner, N. Hendrich, and J. Zhang, “Multi-stage book perception and bimanual manipulation 

for rearranging book shelves,” in _International Conference on Intelligent Autonomous Systems_ , pp. 495–507. Springer, 2023. 

- [25] M. Spivak, _Calculus on manifolds: a modern approach to classical theorems of advanced calculus_ . CRC press, 2018. 

- [26] L. Yang, H.-T. Nguyen, C. Lv, D. Campolo, and F. Cardin, “An energybased numerical continuation approach for quasi-static mechanical manipulation,” _Data-Centric Engineering_ , vol. 6, p. e18, 2025. 

- [27] A. Jaklic, A. Leonardis, and F. Solina, _Segmentation and recovery of superquadrics_ , vol. 20. Springer Science & Business Media, 2000. 

- [28] T. Poston and I. Stewart, _Catastrophe theory and its applications_ . Courier Corporation, 2014. 

- [29] F. Stulp and O. Sigaud, “Robot skill learning: From reinforcement learning to evolution strategies,” _Paladyn, Journal of Behavioral Robotics_ , vol. 4, no. 1, pp. 49–61, 2013. 

**Lin Yang** received his Bachelor’s degree from Beihang University, Beijing, China, in 2022. He is currently pursuing the Ph.D. degree under the supervision of Assoc. Prof. Lyu Chen and Assoc. Prof. Domenico Campolo from the school of MAE NTU. His current research interests include contact-rich manipulation via haptcs based SLAM, planning and sim2real. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0010-30.png)


**Huu-Thiet Nguyen** received the degree of engineer in control and automation engineering from Hanoi University of Science and Technology, Hanoi, Vietnam in 2015, and the PhD degree in electrical and electronic engineering from Nanyang Technological University, Singapore in 2022. He is currently a postdoctoral researcher at Nanyang Technological University. His research interests include robot control, robot learning, and machine learning in robotics and physical systems. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0010-32.png)


**Chen Lv** (Senior Member, IEEE) received the Ph.D. degree from the Department of Automotive Engineering, Tsinghua University, China, in 2016. From 2014 to 2015, he was a Joint Ph.D. Researcher with the EECS Department, University of California at Berkeley. He is currently an Assistant Professor with Nanyang Technology University, Singapore. His research interests include cyber-physical systems, hybrid systems, advanced vehicle control, and intelligence, where he has contributed over 90 articles and holds 12 granted Chinese patents. He received the Highly Commended Paper Award of IMechE, U.K., in 2012, the National Fellowship for Doctoral Student in 2013, the NSK Outstanding Mechanical Engineering Paper Award in 2014, China SAE Outstanding Paper Award in 2015, the 1st Class Award of China Automotive Industry Scientific and Technological Invention in 2015, Tsinghua University Outstanding Doctoral Thesis Award in 2016, and the IV2018 Best Workshop/Special Issue Paper Award. He serves as a Guest Editor for _IEEE Intelligent Transportation Systems Magazine_ , _IEEE/ASME TRANSACTIONS ON MECHATRONICS_ , and _Applied Energy_ ; and an Associate Editor/Editorial Board Member for _International Journal of Vehicle Autonomous Systems_ , _International Journal of Electric and Hybrid Vehicles_ , and _International Journal of Vehicle Systems Modelling and Testing_ . 

**Domenico Campolo** received the Ph.D. degree in microengineering from Scuola Superiore Sant’ Anna, Pisa, Italy, in 2002. He is currently an Associate Professor and the Director of the Robotics Research Centre, School of Mechanical and Aerospace Engineering, Nanyang Technological University, Singapore. He is also the Co-Founder of ArtiCares Pte Ltd., an international company specializing in rehabilitation and assistive robotics. 


![](1_survey/papers/md/Yang2025Recasting_figs/Yang2025Recasting.pdf-0010-35.png)


