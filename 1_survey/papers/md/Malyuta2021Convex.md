---
citation_key: Malyuta2021Convex
arxiv_id: 2106.09125
arxiv_url: "https://arxiv.org/abs/2106.09125"
title: "Convex Optimization for Trajectory Generation"
authors_short: "Danylo Malyuta et al."
year: 2021
direction_tag: B_trajectory_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:42:06Z
origin: ai+web
reviewed: false
---

# Convex Optimization for Trajectory Generation

A Tutorial On Generating Dynamically Feasible Trajectories Reliably And Efficiently

Danylo Malyuta<sup>a,?</sup> , Taylor P. Reynolds<sup>a</sup>, Michael Szmuk<sup>a</sup>, Thomas Lew<sup>b</sup>, Riccardo Bonalli<sup>b</sup>, Marco Pavone<sup>b</sup>, and Behc¸et Ac¸ıkmes¸e<sup>a</sup>

<sup>a</sup> William E. Boeing Department of Aeronautics and Astronautics, University of Washington, Seattle, WA 98195, USA <sup>b</sup> Department of Aeronautics and Astronautics, Stanford University, Stanford, CA 94305, USA

Reliable and efficient trajectory generation methods are a fundamental need for autonomous dynamical systems of tomorrow. The goal of this article is to provide a comprehensive tutorial of three major con vex optimization-based trajectory generation methods: lossless convexification (LCvx), and two sequentia convex programming algorithms known as SCvx and GuSTO. In this article, trajectory generation is the computation of a dynamically feasible state and control signal that satisfies a set of constraints while opti mizing key mission objectives. The trajectory generation problem is almost always nonconvex, which typ ically means that it is not readily amenable to efficient and reliable solution onboard an autonomous vehicle. The three algorithms that we discuss use problem reformulation and a systematic algorithmic strategy to nonetheless solve nonconvex trajectory generation tasks through the use of a convex optimizer. The theoretical guarantees and computational speed offered by convex optimization have made the algo rithms popular in both research and industry circles. To date, the list of applications include rocket land ing, spacecraft hypersonic reentry, spacecraft rendezvous and docking, aerial motion planning for fixed wing and quadrotor vehicles, robot motion planning, and more. Among these applications are high-profil rocket flights conducted by organizations like NASA, Masten Space Systems, SpaceX, and Blue Origin. This article aims to give the reader the tools and understanding necessary to work with each algorithm, and to know what each method can and cannot do. A publicly available source code repository supports the numerical examples provided at the end of this article. By the end of the article, the reader should be ready to use each method, to extend them, and to contribute to their many exciting modern applications.

![](Malyuta2021Convex_figs/8d402a2b10eceb81bf86a8e73d0e6b97e423fbcce0636248b13fbad3e9887fce.jpg)

A<sup>exciting</sup> <sup>new</sup> <sup>applications</sup> <sup>that</sup> <sup>will</sup> <sup>transform</sup>our society. For example, autonomous aerialvehicles (AAVs) operating in urban envi-6.0<sup>9</sup> exciting new applications that will transform our society. For example, autonomous aerial vehicles (AAVs) operating in urban environments could deliver commercial goods, emergency medical supplies, monitor trafic, and provide threat alerts for national security [1]. At the same time, these applications present significant engineering challenges for performance, trustworthiness, and safety. For instance, AAVs can be a catastrophic safety hazard should they lose control or situational awareness over a populated area. Space missions, self-driving cars, and applications of autonomous underwater vehicles (AUVs) share similar concerns.

Generating a trajectory autonomously onboard the vehicle is not only desirable for many of these applications but also indeed a necessity when considering the deployment of autonomous systems either in remote areas with little to no communication, or at scale in a dynamic and uncertain world. For example, it is not possible to remotely control a spacecraft during a Mars landing scenario [2, 3, 4], nor is it practical to coordinate the motion of tens of thousands of delivery drones from a centralized location [1]. In these and many other scenarios, individual vehicles must be endowed with their own high qual ity decision making capability. Failure to generate a saf trajectory can result in losing the vehicle, the payload, and even human life. Reliable methods for trajectory generation are a fundamental need if we are to maintain public trust and the high safety standard that we have come to expect from autonomous or automatic systems [5].

Computational resource requirements are the second major consideration for onboard trajectory generation. Historically, this has been the driving factor for much of practical algorithm development [6, 7]. Although the modern consumer desktop is an incredibly powerfu machine, industrial central processing units (CPUs) can still be relatively modest [8]. This is especially true for spaceflight, where the harsh radiation environment of outer space prevents the rapid adoption of new computing technologies. For example, NASA’s flagship Mars rover “Perseverance” landed in 2021 using a BAE RAD750 PowerPC flight computer, which is a 20 year-old technology [9, 10]. When we factor in the energy requirements of powerful CPUs and the fact that trajectory generation is a small part of all the tasks that an autonomous vehicle must perform, it becomes clear that modern trajectory generation is still confined to a small computational footprint. Consequently, real time onboard trajectory generation algorithms must be computationally eficient.

We define trajectory generation to be the computation of a multi-dimensional temporal state and control signal that satisfies a set of specifications, while optimizing key mission objectives. This article is concerned exclusively with dynamically feasible trajectories, which are those that respect the equations of motion of the vehicle under consideration. Although it is commonplace to track dynamically infeasible trajectories using feedback control, at the end of the day a system can only evolve along dynamically feasible paths, whether those are computed upfront during trajectory generation or are the result of feedback tracking. Performing dynamically feasible trajectory generation carries two important advantages. First, it provides a method to systematically satisfy constraints (i.e., specifications) that are hard, if not impossible, to meet through feedback control. This includes, for example, translation-attitude coupled sensor pointing constraints. Secondly, dynamically feasible trajectories leave much less tracking error for feedback controllers to “clean up”, which usually means that tracking performance can be vastly improved. These two advantages shall become more apparent throughout the article.

Numerical optimization provides a systematic mathematical framework to specify mission objectives as costs or rewards to be optimized, and to enforce state and control specifications as well as the equations of motion via constraints. As a result, we can express trajectory generation problems as optimal control problems, which are infinite-dimensional optimization problems over function spaces [11, 12]. Since the early 1960s, optimal control theory has proven to be extremely powerful [6, 13]. Early developments were driven by aerospace applications, where every gram of mass matters and trajectories are typically sought to minimize fuel or some other massreducing metric (such as aerodynamic load and thereby structural mass). This led to work on trajectory algorithms for climbing aircraft, ascending and landing rockets, and spacecraft orbit transfer, to name just a few [14, 15, 16, 17, 18, 19]. Following these early applications, trajectory optimization problems have now been formulated in many practical areas, including aerial, underwater, and space vehicles, as well as for chemical processes [20, 21, 22], building climate control [23, 24, 25], robotics, and medicine [13], to mention a few.

At its core, optimization-based trajectory generation requires solving an optimal control problem of the following form (at this point, we keep the problem very general):

$$
\min _ {u, p, t _ {f}} J (x, u, p, t _ {f})\tag{1a}
$$

$$
\text { s.t. } \dot {x} (t) = f (x, u, p, t),\tag{1b}
$$

$$
\left(x (t), u (t), p, t _ {f}\right) \in \mathcal {C} (t), \forall t \in [ 0, t _ {f} ],\tag{1c}
$$

$$
\left(x (0), p\right) \in \mathcal {X} _ {0}, \left(x (t _ {f}), p\right) \in \mathcal {X} _ {f}.\tag{1d}
$$

The cost (1a) encodes the mission goal, the system dynamics are modeled by the diferential equation con straint (1b), the state and control specifications are en forced through (1c), and the boundary conditions are fixed by (1d). Note that Problem 1 makes a distinction between a control vector u(t), which is a temporal signal and a so-called parameter vector $p ,$ which is a static vari able that encodes other decision variables like temporal scaling.

In most cases, the solution of such an infinite-dimen sional optimization problem is neither available in closed form nor is it computationally tractable to numerically compute (especially in real-time). Instead, diferent solution methods have been proposed that typically share the following three main components:

Formulation: specification of how the functions J and $f ,$ and the sets ${ \mathcal { C } } , { \mathcal { X } } _ { 0 } .$ , and $\chi _ { f }$ are expressed mathe matically;

Discretization: approximation of the infinite-dimensional state and control signal by a finite-dimensional set of basis functions;

Numerical optimization: iterative computation of an optimal solution of the discretized problem.

Choosing the most suitable combination of these three components is truly a mathematical art form that is highly problem dependent, and not an established plug and-play process like least-squares regression [26]. No single recipe or method is the best, and methods that work well for some problems can fare much worse for others. Trajectory algorithm design is replete with prob lem dependent tradeofs in performance, optimality, and robustness, among others. Still, optimization literature (to which this article belongs) attempts to provide some formal guidance and intuition about the process. For the rest of this article, we will be interested in meth ods that solve the exact form of Problem 1, subject only to the initial approximation made by discretizing the continuous-time dynamics.

Many excellent references discuss the discretization component [13, 27, 28]. Once the problem is discretized, we can employ numerical optimization methods to obtain a solution. This is where the real technical challenge for reliable trajectory generation arise. Depending on the problem formulation and the discretization method, the finite-dimensional optimization problem that must be solved can end up being a nonlinear (i.e., noncon vex) optimization problem (NLP). However, NLP opti mization has high computational complexity, and there are no general guarantees of either obtaining a solution or even certifying that a solution does not exist [26, 29, 30]. Hence, general NLP methods may not be appropriate for control applications, since we need deterministic guar antees for reliable trajectory generation in autonomous control.

In contrast, if the discretized problem is convex, then it can be solved reliably and with an eficiency that exceeds all other areas of numerical optimization except for linear programming and least squares [26, 29, 31, 32, 33, 34]. This is the key motivation behind this article’s focus on a convex optimization-based problem formulations for trajectory generation. By building methods on top of convex optimization, we are able to leverage fast iterative algorithms with polynomial-time complexity [35, Theorem 4.7]. In plain language, given any desired solution accuracy, a convex optimization problem can be solved to within this accuracy in a predetermined number of arithmetic operations that is a polynomial function of the problem size. Hence, there is a deterministic bound on how much computation is needed to solve a given convex optimization problem, and the number of iterations cannot grow indefinitely like for NLP. These special properties, together with a mature theoretical understanding and an ever-growing list of successful real-world usecases, leave little doubt that convex optimization-based solution methods are uniquely well-suited to be used in the solution of optimal control problems.

Among the successful real-world use-cases of convex optimization-based trajectory generation are several inspiring examples from the aerospace domain. These include autonomous drones, spacecraft rendezvous and docking, and most notably planetary landing. The latter came into high profile as an enabling technology for reusability of the SpaceX Falcon 9 and Heavy rockets [36]. Even earlier, the NASA Jet Propulsion Laboratory (JPL) demonstrated the use of a similar method for Mars pinpoint landing aboard the Masten Xombie sounding rocket [37, 38, 39]. Today, these methods are being studied and adopted for several Mars, Moon, and Earth landing applications [8, 36]. Although each application has its own set of unique challenges, they all share the need to use the full spacecraft motion envelope with limited sensing, actuation, and fuel/power [8]. These considerations are not unique to space applications, and can be found in almost all autonomous vehicles such as cars [40, 41], walking robots [42, 43], and quadrotors [44].

Having motivated the use of convex optimization, we note that many trajectory generation problems have common sources of nonconvexity, among which are: nonconvex control constraints, nonconvex or coupled state-control constraints, and nonlinear dynamics. The goal of a convex optimization-based trajectory generation algorithm is to provide a systematic way of handling these nonconvexities, and to generate a trajectory using a convex solver at its core.

Two methods stand out to achieve this goal. In special cases, it is possible to reformulate the problem into a convex one through a variable substitution and a “lifting” (i.e., augmentation) of the control input into a higherdimensional space. In this case, Pontryagin’s maximum principle [11] can be used to show that solving the new problem recovers a globally optimal solution of the origi nal problem. This gives the approach the name lossless convexification (LCvx), and the resulting problem can often be solved with a single call to a convex solver. As one can imagine, however, LCvx tends to apply only to very specific problems. Fortunately, this includes some important and practically useful forms of rocket landing and other trajectory generation problems for spacecraf and AAV vehicles [6, 45, 46]. When LCvx cannot be used, convex optimization can be applied via sequen tial convex programming (SCP). This natural ex tension linearizes all nonconvex elements of Problem 1, and solves the convex problem in a local neighborhood where the linearization is accurate. Roughly speaking, the problem is then re-linearized at the new solution, and the whole process is repeated until a stopping crite rion is met. In the overall classification of optimization algorithms, SCP is a trust region method [29, 47, 48]. While SCP is a whole class of algorithms, our primar focus is on two particular and closely related method called SCvx (also known as successive convexification) and GuSTO [49, 50].

Let us go through the numerous applications where the LCvx, SCvx and GuSTO methods have been used. The LCvx method was originally developed for rocket landing [45, 51]. This was the method at the center of the afore mentioned NASA JPL multi-year flight test campaign for Mars pinpoint landing [37]. We hypothesize that LCvx is also a close relative of the SpaceX Falcon 9 termi nal landing algorithm [36]. The method also appears in applications for fixed-wing and quadrotor AAV trajec tory generation [46, 52], spacecraft hypersonic reentr [53, 54, 55], and spacecraft rendezvous and docking [56, 57]. The SCvx method, which applies to far more gen eral problems albeit with fewer runtime guarantees, has been used extensively for the general rocket landing prob lem [58, 59, 60, 61, 62, 63], quadrotor trajectory genera tion [52, 64, 65], spacecraft rendezvous and docking [66], and cubesat attitude control [67]. Recently, as part of the NASA SPLICE project to develop a next-generation planetary landing computer [8], the SCvx algorithm is being tested as an experimental payload aboard the Blue Origin New Shepard rocket [68]. The GuSTO method has been applied to free-flyer robots such as those used aboard the international space station (ISS) [50, 69, 70, 71], car motion planning [72, 73], aircraft motion plan ning [50], and robot manipulator arms [69].

This article provides a first-ever comprehensive tutorial of the LCvx, SCvx and GuSTO algorithms. Plac ing these related methods under the umbrella of a singl article allows to provide a unified description that high lights common ideas and helps the practitioner to know how, where, and when to deploy each method. Previous tutorials on LCvx and SCvx provide a complementar technical discussion [74, 75].

![](Malyuta2021Convex_figs/36759100e75bfab2afa050d1c85549048884b6afea290afa1da75419ba13c47b.jpg)  
FIGURE 1 A typical control architecture consists of trajectory generation and feedback control elements. This article discusses algorithms for trajectory generation, which traditionally provides reference and feedforward control signals. By repeatedly generating new trajectories, a feedback action is created that can itself be used for control. Repeated trajectory generation for feedback control underlies the theory of model predictive control.

There are two reasons for focusing on LCvx, SCvx, and GuSTO specifically. First, the authors are the developers of the three algorithms. Hence, we feel best positioned to provide a thorough description for these particular methods, given our experience with their implementation. Second, these three methods have a significant history of real-world application. This should provide confidence that the methods withstood the test of time, and have proven themselves to be useful when the stakes were high. By the end of the article, our hope is to have provided the understanding and the tools necessary in order to adapt each method to the reader’s particular engineering application.

Although our discussion for SCP is restricted to SCvx and GuSTO, both methods are closely related to other existing SCP algorithms. We hope that after reading this tutorial, the reader will be well-positioned to understand most if not all other SCP methods for trajectory generation. Applications of these SCP alternatives are discussed in the recent survey paper [6].

Finally, we note that this article is focused on solving a trajectory optimization problem like Problem 1 once in real-time. As illustrated in Figure 1, this results in a single optimal trajectory that can be robustly tracked by a downstream control system. The ability to solve for the trajectory in real-time, however, can allow for updating the trajectory as the mission evolves and more information is revealed to the autonomous vehicle. Repetitive trajectory generation provides a feedback action that can itself be used for control purposes. This approach is the driving force behind model predictive control (MPC), which has been applied to many application domains over the last three decades [76, 77, 78]. This article does not cover MPC, and we refer the interested reader to existing literature [78, 79].

The rest of this article is organized as follows. We begin with a short section on convex optimization, with the primary objective of highlighting why it is so useful for trajectory generation. The article is then split into three main parts. Part I surveys the major results of lossless convexification (LCvx) to solve nonconvex trajectory problems in one shot. Part II discusses sequential convex programming (SCP) which can handle very general and highly nonconvex trajectory generation tasks by itera tively solving a number of convex optimization problems. In particular, Part II provides a detailed tutorial on two modern SCP methods called SCvx and GuSTO [49, 50]. Lastly, Part III applies LCvx, SCvx, and GuSTO to three complex trajectory generation problems: a rocket powered planetary lander, a quadrotor, and a micrograv ity free-flying robotic assistant. Some important naming conventions and notation that we use throughout the ar ticle are defined in the “Abbreviations” and “Notation”.

To complement the tutorial style of this article, the numerical examples in Part III are accompanied by opensource implementation code linked in Figure 2. We use the Julia programming language because it is simple to read like Python, yet it can be as fast as C/C++ [80]. By downloading and running the code, the reader can recreate the exact plots seen in this article.

## Convex Optimization Background

Convex optimization seeks to minimize a convex objective function while satisfying a set of convex constraints. The technique is expressive enough to capture many trajectory generation and control applications, and is appealing due to the availability of solution algorithms with the following properties [26, 29]:

A globally optimal solution is found if a feasible solu tion exists;

A certificate of infeasibility is provided when a feasible solution does not exist;

The runtime complexity is polynomial in the problem size;

The algorithms can self-initialize, eliminating the need for an expert initial guess.

The above properties are fairly general and apply to most, if not all, trajectory generation and control

![](Malyuta2021Convex_figs/5e9dcc36f83a271eaa064e68dc01fa48a1485bae6a4248d9f70a5474acc60c05.jpg)  
github.com/dmalyuta/scp traj opt/tree/csm

FIGURE 2 The complete implementation source code for the numerical examples at the end of this article can be found in the csm branch of our open-source GitHub repository. The master branch provides even more algorithms and examples that are not covered in this article.

<table><tr><td>LCvx</td><td>Lossless convexification</td></tr><tr><td>LTV</td><td>Linear time-varying</td></tr><tr><td>SCP</td><td>Sequential convex programming</td></tr><tr><td>SQP</td><td>Sequential quadratic programming</td></tr><tr><td>LP</td><td>Linear program</td></tr><tr><td>QP</td><td>Quadratic program</td></tr><tr><td>SOCP</td><td>Second-order cone program</td></tr><tr><td>SDP</td><td>Semidefinite program</td></tr><tr><td>MILP</td><td>Mixed-integer linear program</td></tr><tr><td>NLP</td><td>Nonlinear (nonconvex) program</td></tr><tr><td>IPM</td><td>Interior point method</td></tr><tr><td>MPC</td><td>Model predictive control</td></tr><tr><td>ISS</td><td>International Space Station</td></tr><tr><td>KKT</td><td>Karush-Kuhn-Tucker</td></tr><tr><td>ODE</td><td>Ordinary differential equation</td></tr><tr><td>ZOH</td><td>Zeroth-order hold</td></tr><tr><td>FOH</td><td>First-order hold</td></tr><tr><td>DoF</td><td>Degree of freedom</td></tr><tr><td>Programming</td><td>Optimization</td></tr></table>

applications. This makes convex programming safer than other optimization methods for autonomous applications.

To appreciate what makes an optimization problem convex, we introduce some basic definitions here and defer to [26, 81] for further details. Two fundamental objects must be considered: a convex function and a convex set. For reference, Figure 3 illustrates a notional convex set and function. By definition, ${ \mathcal { C } } \subseteq \mathbb { R } ^ { n }$ is a convex set if and only if it contains the line segment connecting any two of its points:

$$
x, y \in \mathcal {C} \Rightarrow [ x, y ] _ {\theta} \in \mathcal {C}\tag{2}
$$

for all $\theta \in [ 0 , 1 ]$ ], where $[ x , y ] _ { \theta } \triangleq \theta x + ( 1 - \theta ) y$ . An important property is that convexity is preserved under set intersection. This allows us to build complicated convex sets by intersecting simpler sets. By replacing the word “sets” with “constraints”, we can readily appreciate how this property plays into modeling trajectory generation problems using convex optimization.

A function $f : \mathbb { R } ^ { n }  \mathbb { R }$ is convex if and only if dom f is a convex set and $f$ lies below the line segment connecting any two of its points:

$$
x, y \in \operatorname{dom} f \Rightarrow f ([ x, y ] _ {\theta}) \leq [ f (x), f (y) ] _ {\theta}\tag{3}
$$

for all $\theta \in [ 0 , 1 ]$ . A convex optimization problem is simply the minimization of a convex function subject to a number of convex constraints that act to restrict the search space:

$$
\min _ {x \in \mathbb {R} ^ {n}} f _ {0} (x)\tag{4a}
$$

$$
\mathrm{s.t.} f _ {i} (x) \leq 0, i = 1, \dots , n _ {\mathrm{ineq}},\tag{4b}
$$

<table><tr><td colspan="2">Notation</td></tr><tr><td>M</td><td>Matrices are capitalized letters</td></tr><tr><td>z</td><td>A scalar or vector variable</td></tr><tr><td>S</td><td>Sets are calligraphic capitalized let- ters</td></tr><tr><td>(a,b,c)</td><td>Concatenation of column or row vec-tors</td></tr><tr><td>ei</td><td>Standard i-th standard basis vector</td></tr><tr><td>In∈Rn×n</td><td>Identity matrix</td></tr><tr><td>v×</td><td>Skew symmetric matrix representa-tion of a cross product</td></tr><tr><td>diag(a,B,...)</td><td>(Block) diagonal matrix from scalars and/or matrices</td></tr><tr><td>dom f</td><td>Domain of a function</td></tr><tr><td>∇xf</td><td>The gradient vector or Jacobian matrix of f with respect to x</td></tr><tr><td>f[t]</td><td>Shorthand for a function evaluated at a particular time (e.g., f(t,x(t),u(t)))</td></tr></table>

![](Malyuta2021Convex_figs/ed80ae0062d5d4597078bf7b8bc765e0f14ee6682222797448ec3882119c2ca0.jpg)  
(a) A convex set contains all line segments connecting its points

![](Malyuta2021Convex_figs/3128f750baebdd0e5152525c0c9ee13f7e9c649add45be36f1b304800e6c91ee.jpg)  
(b) A convex function lies below all line segments connecting its points

FIGURE 3 Illustration of a notional convex set (a) and convex function (b). In both cases, the variable $\theta \in [ 0 , 1 ]$ generates a line segment between two points. The epigraph ep $\bar { f } \subseteq \mathbb { R } ^ { n } \times \mathbb { R }$ is the set of points which lie above the function, and itself defines a convex set.

$$
g _ {i} (x) = 0, i = 1, \dots , n _ {\mathrm{eq}},\tag{4c}
$$

where $f _ { 0 } : \mathbb { R } ^ { n }  \mathbb { R }$ is a convex cost function, $f _ { i } : \mathbb { R } ^ { n } $ <sup>R</sup> are convex inequality constraints, and $g _ { i } : \mathbb { R } ^ { n }  \mathbb { R }$ are afine equality constraints. The problem contains $n _ { \mathrm { i n e q } }$ inequality and $n _ { \mathrm { e q } }$ equality constraints. We stress that the equality constraints must be afine, which means that each function $g _ { i }$ is a linear expression in x plus a constant ofset. The equations of motion are equalit constraints, therefore basic convex optimization restricts the dynamics to be afine (i.e., linear time-varying at most). Handling nonlinear dynamics will be a major topic of discussion throughout this article.

Each constraint defines a convex set so that, together, (4b) and (4c) form a convex feasible set of values that the decision variable x may take. To explicitly connect this discussion back to the generic convex set introduced in (2), we can write the feasible set as:

$$
\begin{array}{c} \mathcal {C} = \Big \{x \in \mathbb {R} ^ {n}: f _ {i} (x) \leq 0, i = 1, \ldots , n _ {\text {ineq}}, \\ g _ {i} (x) = 0, i = 1, \ldots , n _ {\text {eq}} \Big \}. \end{array}\tag{5}
$$

A fundamental consequence of convexity is that any local minimum of a convex function is a global minimum [26, Section 4.2.2]. More generally, convex functions come with a plethora of properties that allow algorithm designers to obtain global information about function behavior from local measurements. For example, a diferentiable convex function is globally lower bounded by its local first-order approximation [26]. Thus, we may look at convexity as a highly beneficial assumption on function behavior that enables eficient algorithm design. Indeed, a landmark discovery of the twentieth century was that it is convexity, not linearity, that separates “hard” and “easy” problems [30].

For practitioners, the utility of convex optimization stems not so much from the ability to find the global minimum, but rather from the ability to find it (or indeed any other feasible solution) quickly. The field of numerical convex optimization was invigorated by the interior-point method (IPM) family of optimization algorithms, first introduced in 1984 by Karmarkar [82]. Today, convex optimization problems can be solved by primal-dual IPMs in a few tens of iterations [26, 31]. Roughly speaking, we can say that substantially large trajectory generation problems can usually be solved in under one second [9, 37, 63]. In technical parlance, IPMs have a favorable polynomial problem complexity: the number of iterations required to solve the problem to a given tolerance grows polynomially in the number of constraints $n _ { \mathrm { i n e q } } + n _ { \mathrm { e q } }$ . With some further assumptions, it is even possible to provide an upper bound on the number of iterations [35, 83]. We defer to [29, Chapters 14 and 19] for futher details on convex optimization algorithms. Throughout this article, our goal will be to leverage existing convex problem solvers to create higherlevel frameworks for the solution of trajectory generation problems.

## PART I: LOSSLESS CONVEXIFICATION

Lossless convexification (LCvx) is a modeling tech nique that solves nonconvex optimal control problems through a convex relaxation. In this method, Pontryagin’s maximum principle [11] is used to show that a convex relaxation of a nonconvex problem finds the globally optimal solution to the original problem, hence the method’s name. To date, the method has been extended as far as relaxing certain classes of nonconvex control constraints, such as an input norm lower bound (see “Convex Relaxation of an Input Lower Bound”) and a nonconvex pointing constraint (see “Convex Relaxation of an Input Pointing Constraint”).

The LCvx method has been shown to work for a large class of state-constrained optimal control problems, however a working assumption is that state constraint are convex. Lossless relaxation of nonconvex state constraints remains under active research, and some related results are available [46] (which we will cover in this section).

As the reader goes through Part I, it is suggested to keep in mind that the main concerns of lossless convexification are:

To find a convex lifting of the feasible input set;

To show that the optimal input of the lifted problem projects back to a feasible input of the original nonlifted problem.

Figure 4 chronicles the development history of LCvx. The aim of this part of the article is to provide a tu torial overview of the key results, so theoretical proof are omitted in favor of a more practical and action-ori ented description. Ultimately, our aim is for the reade to come away with a clear understanding of how LCvx can be applied to their own problems.

In the following sections, we begin by introducing LCvx for the input norm lower bound and pointing nonconvexities using a baseline problem with no state constraints. Then, the method is extended to handl afine and quadratic state constraints, followed b general convex state constraints. We then describe how the LCvx method can also handle a class of dynamical systems with nonlinear dynamics. For more general ap plications, embedding LCvx into nonlinear optimization algorithms is also discussed. At the very end of this part of the article, we cover some of the newest LCvx results from the past year, and provide a toy example that gives a first taste of how LCvx can be used in practice.

## No State Constraints

We begin by stating perhaps the simplest optimal con trol problem for which an LCvx result is available. Its salient features are a distinct absence of state constraints (except for the boundary conditions), and its only source of nonconvexity is a lower-bound on the input given b (6c). A detailed description of LCvx for this problem may be found in [45, 84, 86].

$$
\min _ {u, t _ {f}} m (t _ {f}, x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (g _ {1} (u (t))) \mathrm{d} t\tag{6a}
$$

$$
\text { s.t. } \dot {x} (t) = A (t) x (t) + B (t) u (t) + E (t) w (t),\tag{6b}
$$

$$
\rho_ {\mathrm{min}} \leq g _ {1} (u (t)), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{6c}
$$

![](Malyuta2021Convex_figs/007dd120187afcf0f15383d8479452b33e688568ec1cefedaaaa5ca34a35d0f8.jpg)  
FIGURE 4 Chronology of lossless convexification theory development. Note the progression from state-unconstrained problems to those with progressively more general state constraints and, finally, to problems that contain integer variables.

$$
x (0) = x _ {0}, b \left(t _ {f}, x \left(t _ {f}\right)\right) = 0.\tag{6d}
$$

In Problem $6 , t _ { f } > 0$ is the terminal time, $\boldsymbol { x } ( \cdot ) \in \mathbb { R } ^ { n }$ is the state trajectory, $u ( \cdot ) \in \mathbb { R } ^ { m }$ is the input trajectory, $w ( \cdot ) \in \mathbb { R } ^ { p }$ is an exogenous additive disturbance, $m : \mathbb { R } \times$ $\mathbb { R } ^ { n } \to \mathbb { R }$ is a convex terminal cost, $\ell : \mathbb { R } \to$ <sup>R</sup> is a convex and non-decreasing running cost modifier, $\zeta \in \{ 0 , 1 \}$ is a fixed user-chosen parameter to toggle the running cost, $g _ { 0 } , g _ { 1 } : \mathbb { R } ^ { m }  \mathbb { R } _ { + }$ are convex functions, $\rho _ { \mathrm { m i n } } > 0$ and $\rho _ { \mathrm { m a x } } > \rho _ { \mathrm { m i n } }$ are user-chosen bounds, and $b : \mathbb { R } \times \mathbb { R } ^ { n } \to$ $\mathbb { R } ^ { n _ { b } }$ is an afine terminal constraint function. Note that the dynamics in Problem 6 define a linear time varying (LTV) system. For all the LCvx discussion that follows, we will also make the following two assumptions on the problem data.

## Assumption 1

If any part of the terminal state is constrained then the Jacobian $\nabla _ { \boldsymbol { x } } b [ t _ { f } ] ~ \in ~ \mathbb { R } ^ { n _ { b } \times n }$ is full row rank, i.e., rank $\nabla _ { \boldsymbol { x } } b [ t _ { f } ] = n _ { b }$ . This implies that the terminal state is not over-constrained. ■

## Assumption 2

The running cost is positive definite, in other words $\ell ( z ) > 0$ for all $z \neq 0$ 

When faced with a nonconvex problem like Problem 6, an engineer has two choices. Either devise a nonlinear optimization algorithm, or solve a simpler problem that is convex. The mantra of LCvx is to take the latter approach by “relaxing” the problem until it is convex. In the case of Problem 6, let us propose the following relaxation, which introduces a new variable $\sigma ( \cdot ) \in \mathbb { R }$ called the slack input.

$$
\min _ {\sigma , u, t _ {f}} m \left(t _ {f}, x \left(t _ {f}\right)\right) + \zeta \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) d t
$$

$$
\text { s.t. } \dot {x} (t) = A (t) x (t) + B (t) u (t) + E (t) w (t),\tag{7a}
$$

$$
\rho_ {\mathrm{min}} \leq \sigma (t), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{7b}
$$

$$
g _ {1} (u (t)) \leq \sigma (t),\tag{7c}
$$

$$
x (0) = x _ {0}, b (t _ {f}, x (t _ {f})) = 0.\tag{7d}
$$

(7e)

The relaxation of the nonconvex input constraint (6c) to the convex constraints (7c)-(7d) is illustrated in $^ { 6 6 } \mathrm { C o n - }$ vex Relaxation of an Input Lower Bound” for the case of a throttleable rocket engine. Note that if (7d) is replaced with equality, then Problem 7 is equivalent to Problem 6. Indeed, the entire goal of LCvx is to prove that (7d) holds with equality at the globally optimal solution of Prob lem 7. Because of the clear importance of constraint (7d) to the LCvx method, we shall call it the LCvx equality constraint. This special constraint will be highlighted in red in all subsequent LCvx optimization problems.

Consider now the following set of conditions, which arise naturally when using the maximum principle to prove lossless convexification. The theoretical details are provided in [86, Theorem 2].

## Condition 1

The pair $\{ A ( \cdot ) , B ( \cdot ) \}$ must be totally controllable. This means that any initial state can be transferred to any final state by a bounded control trajectory in any finite time interval $[ 0 , t _ { f } ] ~ [ 4 6 , ~ 9 4 ]$ ]. If the system is time invariant, this is equivalent to A, B being controllable, and can be verified by checking that the controllabilit matrix is full rank or, more robustly, via the PBH test [95].

## Condition 2

Define the quantities:

$$
m _ {\mathrm{LCvx}} = \left[ \begin{array}{c} \nabla_ {x} m [ t _ {f} ] \\ \nabla_ {t} m [ t _ {f} ] + \zeta \ell (\sigma (t _ {f})) \end{array} \right] \in \mathbb {R} ^ {n + 1},\tag{8a}
$$

$$
B _ {\mathrm{LCvx}} = \left[ \begin{array}{c} \nabla_ {x} b [ t _ {f} ] ^ {\intercal} \\ \nabla_ {t} b [ t _ {f} ] ^ {\intercal} \end{array} \right] \in \mathbb {R} ^ {(n + 1) \times n _ {b}}.\tag{8b}
$$

The vector $m _ { \mathrm { L C v x } }$ and the columns of $\boldsymbol { B } _ { \mathrm { L C v x } }$ must be linearly independent. 

We can now state Theorem 1, which is the main lossless convexification result for Problem 6. The practical implication of Theorem 1 is that the solution of Problem 6 can be found in polynomial time by solving Prob lem 7 instead.

## Convex Relaxation of an Input Lower Bound

![](Malyuta2021Convex_figs/580d2f0e9fd3202f7dcf016845b491caff7e9572d208925a1421b0aef6438906.jpg)  
FIGURE S1 Relaxation of the nonconvex input constraint set (S1) to the convex set (S2) by using a slack input σ. If the optimal input $( u ^ { * } , \sigma ^ { * } ) \in \partial _ { \mathsf { L C v } \times } \mathcal { V }$ (S4), then $\boldsymbol { u } ^ { * }$ is feasible for the nonconvex constraint (S1).

typical rocket engine’s thrust is upper bounded by the engine’s performance and lower bounded by combustion instability issues for small thrusts. Thus, (6c) can be written as

$$
\rho_ {\min} \leq \| u \| _ {2} \leq \rho_ {\max},\tag{S1}
$$

so that $g _ { 0 } ( u ) = g _ { 1 } ( u ) \triangleq \Vert u \Vert _ { 2 }$ . The relaxation (7c)-(7d) then

## Theorem 1

The solution of Problem 7 is globally optimal for Problem 6 if Conditions 1 and 2 hold. 

There is a partial generalization of Theorem 1. First, restrict Problem 6 to the choices $\zeta ~ = ~ 1$ and $g _ { 0 } ~ = ~ g _ { 1 }$ Next, introduce a new pointing-like input constraint (9d). The quantities $\hat { n } _ { u } \in \mathbb { R } ^ { m }$ and $\hat { n } _ { g } \in \mathbb { R }$ are user-chosen parameters. The new problem takes the following form:

$$
\min _ {u, t _ {f}} m \left(t _ {f}, x \left(t _ {f}\right)\right) + \int_ {0} ^ {t _ {f}} \ell \left(g _ {0} (u (t))\right) d t\tag{9a}
$$

$$
\text { s.t. } \dot {x} (t) = A (t) x (t) + B (t) u (t) + E (t) w (t),\tag{9b}
$$

$$
\rho_ {\mathrm{min}} \leq g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{9c}
$$

$$
\hat {n} _ {u} ^ {\intercal} u (t) \geq \hat {n} _ {g} g _ {0} (u (t)),\tag{9d}
$$

$$
x (0) = x _ {0}, b (t _ {f}, x (t _ {f})) = 0.\tag{9e}
$$

Using (9d), one can, for example, constrain an airborne vehicle’s tilt angle. This constraint, however, is nonconvex for $\hat { n } _ { g } ~ < ~ 0 $ . We take care of this nonconvexity, along with the typical nonconvexity of the lower bound in (9c), by solving the following relaxation of the original problem:

$$
\min _ {\sigma , u, t _ {f}} m (t _ {f}, x (t _ {f})) + \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) \mathrm{d} t\tag{10a}
$$

$$
\text { s.t. } \dot {x} (t) = A (t) x (t) + B (t) u (t) + E (t) w (t),\tag{10b}
$$

$$
\rho_ {\mathrm{min}} \leq \sigma (t) \leq \rho_ {\mathrm{max}},\tag{10c}
$$

$$
g _ {0} (u (t)) \leq \sigma (t),\tag{10d}
$$

becomes:

$$
\rho_ {\min} \leq \sigma , \| u \| _ {2} \leq \min (\sigma , \rho_ {\max}).\tag{S2}
$$

Figure S1 shows how for $\boldsymbol { u } \in \mathbb { R } ^ { 2 }$ , going from (S1) to (S2) lifts a nonconvex annulus to a convex volume ,

$$
\begin{array}{c} \mathcal {V} \triangleq \{(u, \sigma) \in \mathbb {R} ^ {3}: \rho_ {\min} \leq \sigma , \\ \| u \| _ {2} \leq \min (\sigma , \rho_ {\max}) \}. \end{array}\tag{S3}
$$

The drawback is that inputs that were not feasible for (S1) become feasible for (S2). In particular, any u for which $\| u \| _ { 2 } < \rho _ { \mathsf { m i n } }$ is now feasible. However, for the special case of $( u , \sigma ) \in \partial _ { \mathsf { L C v x } } \mathcal { V }$ , where:

$$
\begin{array}{c} \partial_ {\mathrm{LCvx}} \mathcal {V} \triangleq \{(u, \sigma) \in \mathbb {R} ^ {3}: \rho_ {\min} \leq \sigma , \\ \| u \| _ {2} = \min (\sigma , \rho_ {\max}) \}, \end{array}\tag{S4}
$$

the input u is feasible. The goal of lossless convexification is to show that this occurs at the global optimum of Problem $^ { 7 , }$ in other words $( u ^ { * } ( t ) , \sigma ^ { * } ( t ) ) \in \partial _ { \mathsf { L C v x } } \mathcal { V }$ . Theorem 1 guarantees this.

$$
\hat {n} _ {u} ^ {\intercal} u (t) \geq \sigma (t) \hat {n} _ {g},
$$

$$
x (0) = x _ {0}, b \left(t _ {f}, x \left(t _ {f}\right)\right) = 0.\tag{10e}
$$

(10f)

Just like in Problem 7, we introduced a slack input $\sigma ( \cdot ) \in \mathbb { R }$ to strategically remove nonconvexity. Note once again the appearance of the LCvx equality constraint (10d). Meanwhile, the relaxation of (9d) to (10e) cor responds to a halfspace input constraint in the $( u , \sigma ) \in$ <sup>Rm+1</sup> space. A geometric intuition about the relaxation is illustrated in “Convex Relaxation of an Input Pointing Constraint” for a typical vehicle tilt constraint. Lossless convexification can again be shown under an extra Condition 3, yielding Theorem 2. Theoretical details are provided in [87, 96].

## Condition 3

Let $\boldsymbol { N } \in \mathbb { R } ^ { m \times ( m - 1 ) }$ be a matrix whose columns span the nullspace of $\hat { n } _ { u }$ in (9d). The pair $\{ A ( \cdot ) , B ( \cdot ) N \}$ must be totally controllable.

## Theorem 2

The solution of Problem 10 is globally optimal for Problem 9 if Conditions 1, 2, and 3 hold. 

## Affine State Constraints

The logical next step after Theorems 1 and 2 is to ask whether Problem 6 can incorporate state constraints. It turns out that this is possible under a fairly mild set of extra conditions. The results presented in this section originate from [88, 89, 97].

## Convex Relaxation of an Input Pointing Constraint

![](Malyuta2021Convex_figs/91da7a7044a062485d1bc1f646ad37035cc192d249b1776e9ae4e20a7c2edebb.jpg)  
FIGURE S2 Relaxation of the nonconvex input set (S5) to a convex set (S6) via intersection with a halfspace in the lifted $( u , \sigma )$ space. If the optimal input $( u ^ { * } , \sigma ^ { * } ) \in \partial _ { \mathsf { L C v } \times } \mathcal { V }$ then $\boldsymbol { \upsilon } ^ { * }$ is feasible for the nonconvex constraint (S5).

ractical mechanical systems, such as Segways and rockets, may have a constraint on their tilt angle away from an upright orientation. To model such cases, the inequality (9d) can be specialized to an input pointing constraint. By choosing $\hat { n } _ { g } = \cos ( \theta _ { \mathrm { { m a x } } } )$ and $g _ { 0 } ( u ) = \| u \| _ { 2 }$ , the constraint becomes

$$
\hat {n} _ {u} ^ {\top} u \geq \| u \| _ {2} \cos (\theta_ {\max}),\tag{S5}
$$

which constrains u to be no more than $\theta _ { \mathrm { { m a x } } }$ radians away

Afine inequality constraints are the simplest class of state constraints that can be handled in LCvx. The nonconvex statement of the original problem is a close relative of Problem 6:

$$
\min _ {u, t _ {f}} m (x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (g _ {1} (u (t))) d t\tag{11a}
$$

$$
\text { s.t. } \dot {x} (t) = A x (t) + B u (t) + E w,\tag{11b}
$$

$$
\rho_ {\mathrm{min}} \leq g _ {1} (u (t)), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{11c}
$$

$$
C u (t) \leq c,\tag{11d}
$$

$$
H x (t) \leq h,\tag{11e}
$$

$$
x (0) = x _ {0}, b \left(x \left(t _ {f}\right)\right) = 0.\tag{11f}
$$

First, we note that Problem 11 is autonomous, in other words the terminal cost in (11a), the dynamics (11b), and the boundary constraint (11f) are all independent of time. Note that a limited form of time variance can still be included through an additional time integrator state whose dynamics are $\dot { z } ( t ) = 1$ . The limitation here is that time variance must not introduce nonconvexity in the cost, in the dynamics, and in the terminal constraint (11f). The matrix of facet normals $H \in \mathbb { R } ^ { n _ { h } \times n }$ and the vector of facet ofsets $h \in \mathbb { R } ^ { n _ { h } }$ define a new poly topic (afine) state constraint set. A practical use-case for this constraint is described in “Landing Glideslope as an Afine State Constraint”. Similarly, $C \in \mathbb { R } ^ { n _ { c } \times m }$ and $c \in \mathbb { R } ^ { n _ { c } }$ define a new polytopic subset of the input confrom a nominal pointing direction $\hat { n } _ { u } .$ . The relaxed constraint (10e) becomes

$$
\hat {n} _ {u} ^ {\top} u \geq \sigma \cos (\theta_ {\max}),\tag{S6}
$$

which is a halfspace constraint and is thus convex even for $\theta _ { \operatorname* { m a x } } > \pi / 2$ , when (S5) becomes nonconvex.

Figure S2 shows how for $\boldsymbol { u } \in \mathbb { R } ^ { 2 }$ , relaxing (S5) to (S6) lifts an obtuse “pie slice” to a convex halfspace ,

$$
\mathcal {V} \triangleq \left\{\left(u, \sigma\right) \in \mathbb {R} ^ {3}: \hat {n} _ {u} ^ {\top} u \geq \sigma \cos \left(\theta_ {\max}\right), \| u \| _ {2} \leq \sigma \right\}.\tag{S7}
$$

The drawback is that inputs that were not feasible for (S5) become feasible for (S6). In particular, low magnitude inputs for which $\hat { n } _ { u } ^ { \operatorname { T } } u < \| u \| _ { 2 } \cos ( \theta _ { \operatorname* { m a x } } )$ become feasible. However, if $( u , \sigma ) \in \partial _ { \mathsf { L C v x } } \mathcal { V }$

$$
\partial_ {\mathrm{LCvx}} \mathcal {V} \triangleq \left\{\left(u, \sigma\right) \in \mathbb {R} ^ {3}: \hat {n} _ {u} ^ {\top} u \geq \sigma \cos \left(\theta_ {\max}\right), \| u \| _ {2} = \sigma \right\},\tag{S8}
$$

then the input u satisfies the original constraint (S5). The goal of lossless convexification is to show that this occurs at the global optimum, in other words $( u ^ { \ast } , \sigma ^ { \ast } ) \in \partial _ { \mathsf { L C v } \times } \mathcal { V } .$ Theorem 2 guarantees this.

straint set, as illustrated in “Using Halfspaces to Further Constrain the Input $\mathrm { S e t } ^ { \mathfrak { s } }$

Let us propose the following convex relaxation of Problem 11, which takes the familiar form of Problem 7:

$$
\min _ {\sigma , u, t _ {f}} m (x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) \mathrm{d} t\tag{12a}
$$

$$
\mathrm{s.t.} \dot {x} (t) = A x (t) + B u (t) + E w,\tag{12b}
$$

$$
\rho_ {\mathrm{min}} \leq \sigma (t), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{12c}
$$

$$
g _ {1} (u (t)) \leq \sigma (t),\tag{12d}
$$

$$
C u (t) \leq c,\tag{12e}
$$

$$
H x (t) \leq h,\tag{12f}
$$

$$
x (0) = x _ {0}, b (x (t _ {f})) = 0.\tag{12g}
$$

To guarantee lossless convexification for this convex relaxation, Condition 1 can be modified to handle the new state and input constraints (11d) and (11e). To this end, we use the following notion of cyclic coordinates from mechanics [98].

## Definition 1

For a dynamical system ${ \dot { x } } = f ( x )$ , with state $x \in \mathbb { R } ^ { n }$ any components of x that do not appear explicitly in $f ( \cdot )$ are said to be cyclic coordinates. Without loss of generality, we can decompose the state as follows:

$$
x = \left[ \begin{array}{c} x _ {c} \\ x _ {n c} \end{array} \right],\tag{13}
$$

## Landing Glideslope as an Affine State Constraint

![](Malyuta2021Convex_figs/0a73c30a482d76dd03d75d00896ff5e73d7f0e6b88d4fd108b497768dce27002.jpg)  
FIGURE S3 A spacecraft planetary landing glideslope cone can be approximated as an affine state constraint (11e). By adding more facets, a cone with circular cross-sections can be approximated to arbitrary precision.

typical planetary landing problem may include a glideslope constraint to ensure sufficient elevation during approach and to prevent the spacecraft from colliding with nearby terrain [45]. Letting $\hat { \pmb { e } } _ { 3 } \in \mathbb { R } ^ { 3 }$ represent the local vertical unit vector at the landing site, the glideslope

where $x _ { c } \in \mathbb { R } ^ { n _ { c } }$ are the cyclic and $x _ { n c } \in \mathbb { R } ^ { n _ { n c } }$ are the non-cyclic coordinates, such that $n _ { c } + n _ { n c } = n$ . We can then write ${ \dot { x } } = f ( x _ { n c } )$ 

Many mechanical systems have cyclic coordinates. For example, quadrotor drone and fixed-wing aircraft dynamics do not depend on the position or yaw angle [99]. Satellite dynamics in a circular low Earth orbit, frequently approximated with the Clohessy-Wiltshire-Hill equations [100], do not depend on the true anomaly angle which locates the spacecraft along the orbit.

With Definition 1 in hand, we call a cyclic transformation $\Psi _ { \mathrm { c } } : \mathbb { R } ^ { n }  \mathbb { R } ^ { n }$ any mapping from the state space to itself which translates the state vector along the cyclic coordinates. In other words, assuming without loss of generality that the state is given by (13), we can write:

$$
\Psi_ {\mathrm{c}} (x) = \left[ \begin{array}{c} x _ {c} + \Delta x _ {c} \\ x _ {n c} \end{array} \right]\tag{14}
$$

for some translation $\Delta x _ { c } \in \mathbb { R } ^ { n }$ . Let us now consider the polytopic state constraint (12f) and, in particular, let $\mathcal { F } _ { i } = \{ x \in \mathbb { R } ^ { n } : H _ { i } ^ { \top } x = h _ { i } \}$ be its i-th facet $( H _ { i } ^ { \mathsf { T } }$ is the i-th row of H). The following condition must then hold.

Let $\mathcal { F } _ { i } ~ = ~ \{ x ~ \in ~ \mathbb { R } ^ { n } ~ : ~ H _ { i } ^ { \top } x ~ = ~ h _ { i } \}$ denote the i-th facet of the polytopic state constraint (12f), for any requirement can be expressed as a convex second-order cone constraint:

$$
\hat {e} _ {3} ^ {\mathsf {T}} x \geq \| x \| _ {2} \cos (\gamma_ {\mathrm{gs}}),\tag{S9}
$$

where $\gamma _ { \tt S S } \in [ 0 , \pi / 2 ]$ is the glideslope angle, i.e. the maximum angle that the spacecraft position vector is allowed to make with the local vertical. As illustrated in Figure S3, we can approximate (S9) as an intersection of four halfspaces with the following outward normal vectors:

$$
\hat {n} _ {1} \triangleq \left[ \begin{array}{c} \cos (\gamma_ {\mathrm{gs}}) \\ 0 \\ - \sin (\gamma_ {\mathrm{gs}}) \end{array} \right], \hat {n} _ {2} \triangleq \left[ \begin{array}{c} 0 \\ \cos (\gamma_ {\mathrm{gs}}) \\ - \sin (\gamma_ {\mathrm{gs}}) \end{array} \right],\tag{S10a}
$$

$$
\hat {n} _ {3} \stackrel {\triangle} {=} \left[ \begin{array}{c} - \cos (\gamma_ {\mathrm{gs}}) \\ 0 \\ - \sin (\gamma_ {\mathrm{gs}}) \end{array} \right], \hat {n} _ {4} \stackrel {\triangle} {=} \left[ \begin{array}{c} 0 \\ - \cos (\gamma_ {\mathrm{gs}}) \\ - \sin (\gamma_ {\mathrm{gs}}) \end{array} \right].\tag{S10b}
$$

Thus, (S9) can be written in the form (11e) by setting:

$$
H = \left[ \begin{array}{c} \hat {n} _ {1} ^ {\textsf {T}} \\ \hat {n} _ {2} ^ {\textsf {T}} \\ \hat {n} _ {3} ^ {\textsf {T}} \\ \hat {n} _ {4} ^ {\textsf {T}} \end{array} \right], h = 0 \in \mathbb {R} ^ {4}.\tag{S11}
$$

$i \in \{ 1 , \ldots , n _ { h } \} . \ \mathrm { H } \ h _ { i } \neq 0$ , then there must exist a cyclic transformation $\Psi _ { \mathrm { c } }$ such that

$$
H _ {i} ^ {\intercal} \Psi_ {\mathrm{c}} (x) = 0.\tag{15}
$$

To visualize the implication of Condition 4, simpl consider the case of the landing glideslope constraint from “Landing Glideslope as an Afine State Constraint”. Because the position of a spacecraft in a constant grav ity field is a cyclic coordinate, Condition 4 confirms our intuitive understanding that we can impose landing at a coordinate other than the origin without compromising lossless convexification. Figure 5 provides an illustration.

From linear systems theory [89, 101, 102], it turns out that $x ( t ) \in \mathcal { F } _ { i }$ can hold for a non-zero time interval (i.e. the state “sticks” to a facet) if and only if there exists a triplet of matrices $\{ F _ { i } \ \in \mathbb { R } ^ { m \times n } , G _ { i } \ \in \ \mathbb { R } ^ { m \times n _ { v } } , H _ { i } \ \in$ $\mathbb { R } ^ { m \times p } \}$ such that:

$$
u (t) = F _ {i} x (t) + G _ {i} v (t) + H _ {i} w.\tag{16}
$$

The “new” control input $v ( t ) \in \mathbb { R } ^ { n _ { v } }$ efectively gets fil tered through (16) to produce a control that maintains $x ( \cdot )$ on the hyperplane $\mathcal { F } _ { i }$ . The situation is illustrated in Figure 6 in a familiar block diagram form. While the matrix triplet is not unique, a valid triplet may be com puted via standard linear algebra operations. The reade

## Using Halfspaces to Further Constrain the Input Set

![](Malyuta2021Convex_figs/3b6ba7562ec74ee1142c3a5b5e8369d90a8c1129a97bd12d1c1c43b2e8fee755.jpg)  
FIGURE S4 Halfspace constraints from (11d) can be used to select only portions of the nonconvex input set defined by (11c). The remaining feasible input set is filled in red.

T <sup>he</sup> <sup>input</sup> <sup>constraint</sup> <sup>set</sup> <sup>defined</sup> <sup>by</sup> <sup>(11c)</sup> <sup>generally</sup> <sup>lacks</sup><sub>the</sub> <sub>ability</sub> <sub>to</sub> <sub>describe</sub> <sub>constraints</sub> <sub>on</sub> <sub>individual</sub> <sub>input</sub> components, or on combinations thereof. To enhance the descriptiveness of the input constraint set, halfspace constraints in (11d) may be used. This is illustrated in Figure S4 where $g _ { 0 } ( \cdot ) = \| \cdot \| _ { 1 } , g _ { 1 } ( \cdot ) = \| \cdot \| _ { 2 }$ , and

![](Malyuta2021Convex_figs/0c9931fc2a9ad3d52baa0f7a6ec97e3cbe3a8bc5751b71641431d8cd63d9f4e3.jpg)  
FIGURE 5 Illustration of a landing glideslope constraint (red, sideview of Figure S3) that undergoes a cyclic shift in position along the positive x axis, to arrive at a new landing location (blue). Thanks to Condition 4, the LCvx guarantee continues to hold for the new glideslope constraint, even though the new constraint facets are not subspaces.

![](Malyuta2021Convex_figs/fb18041dffc0a9441a9f5924512329b71b14c8665a89f62e38c366facc71ddc5.jpg)  
FIGURE 6 Given $x ( 0 ) \in \mathcal { F } _ { i }$ , the dynamical system (11b) evolves on $\mathcal { F } _ { i }$ if and only if u(t) is of the form (16).

$$
C = \left[ \begin{array}{c} \hat {n} _ {1} ^ {\mathsf {T}} \\ \hat {n} _ {2} ^ {\mathsf {T}} \end{array} \right], c = \left[ \begin{array}{c} c _ {1} \\ 0 \end{array} \right].\tag{S12}
$$

For example, $u _ { 1 }$ and $u _ { 2 }$ may describe the concentrations of two chemical reactants – hydrochloric acid (HCl) and ammonia (NH ) – to produce ammonium chloride $( N H _ { 4 } C l )$ Then, the first affine constraint may describe the maximum concentration of ${ \mathsf { N H } } _ { 3 }$ while the second affine constraint may describe an inter-dependency in the concentrations of both reactants. Meanwhile, the by-now familiar constraint (11c) describes the joint reactant concentration upper and lower bounds.

may consult these operations directly in the source code of the LCvx examples provided at the end of this article.

The proof of LCvx for Problem 11 was originally developed in [88, 89]. The theory behind equation (16) is among the most abstract in all of LCvx, and we shall not attempt a proof here. The ultimate outcome of the proof is that the following condition must hold.

## Condition 5

For each facet $\mathcal { F } _ { i } \subseteq \mathbb { R } ^ { n }$ of the polytopic state constraint (12f), the following “dual” linear system has no transmission zeros:

$$
\begin{array}{l} \dot {\lambda} (t) = - (A + B F _ {i}) ^ {\top} \lambda (t) - (C F _ {i}) ^ {\top} \mu (t), \\ y (t) = (B G _ {i}) ^ {\top} \lambda (t) + (C G _ {i}) ^ {\top} \mu (t). \end{array}
$$

Transmission zeros are defined in [103, Section 4.5.1]. Roughly speaking, if there are no transmission zeros then there cannot exist an initial condition $\ b { \lambda } ( 0 ) \in \mathbb { R } ^ { n }$ and an input trajectory $\mu \in \mathbb { R } ^ { n _ { c } }$ such that $y ( t ) = 0$ for a nonzero time interval.

We can now state when lossless convexification holds for Problem 12. Note that the statement is very similar to Theorem 1. Indeed, the primary contribution of [88, 89] was to introduce Condition 5 and to show that LCvx holds by using a version of the maximum principle that includes state constraints [104, 105]. The actual lossless convexification procedure, meanwhile, does not change.

## Theorem 3

The solution of Problem 12 is globally optimal for Problem 11 if Conditions 2 and 5 hold. 

Most recently, a similar LCvx result was proved for problems with afine equality state constraints that can furthermore depend on the input [93]. These so-called mixed constraints are of the following form:

$$
y (t) = C (t) x (t) + D (t) u (t),\tag{17}
$$

where $y , C ,$ , and D are problem data.

## Quadratic State Constraints

In the last section, we showed an LCvx result for state constraints that can be represented by the afine description (11e). The natural next question is whether LCvx extends to more complicated state constraints. It turns out that a generalization of LCvx exists for quadratic state constraints, if one can accept a slight restriction to the system dynamics. This result was originally presented in [97, 102]. The nonconvex problem statement is as follows:

$$
\min _ {u, t _ {f}} m (x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (g _ {1} (u (t))) \mathrm{d} t\tag{18a}
$$

$$
\mathrm{s.t.} \dot {x} _ {1} (t) = A x _ {2} (t),\tag{18b}
$$

$$
\dot {x} _ {2} (t) = B u (t) + w,\tag{18c}
$$

$$
\rho_ {\mathrm{min}} \leq g _ {1} (u (t)), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{18d}
$$

$$
x _ {2} (t) ^ {\top} H x _ {2} (t) \leq 1,\tag{18e}
$$

$$
x _ {1} (0) = x _ {1, 0}, x _ {2} (0) = x _ {2, 0}, b (x (t _ {f})) = 0,\tag{18f}
$$

where $( x _ { 1 } , x _ { 2 } ) \ \in \ \mathbb { R } ^ { n } \times \mathbb { R } ^ { n }$ is the state that has been partitioned into two distinct parts, $u \in \mathbb { R } ^ { n }$ is an input of the same dimension, and the exogenous disturbance $w \in \mathbb { R } ^ { n }$ is some fixed constant. The matrix $H \in \mathbb { R } ^ { n \times n }$ is symmetric positive definite such that (18e) maintains the state in an ellipsoid. An example of such a constraint is illustrated in “Maximum Velocity as a Quadratic State Constraint”.

Although the dynamics (18b)-(18c) are less general than (11b), they can still accommodate problems related to vehicle trajectory generation. In such problems, the vehicle is usually closely related to a double integrator system, for which $A = I _ { n }$ and $B = I _ { n }$ such that $x _ { 1 }$ is the position and $x _ { 2 }$ is the velocity of the vehicle. The control u in this case is the acceleration.

The following assumption further restricts the problem setup, and is a consequence of the lossless convexification proof [88].

## Assumption 3

The matrices A, B, and H in Problem 11 are invertible. The functions $g _ { 0 } ( \cdot )$ and $g _ { 1 } ( \cdot )$ satisfy $\rho _ { \mathrm { m i n } } \le g _ { 1 } ( - B ^ { - 1 } w )$ and $g _ { 0 } ( - B ^ { - 1 } w ) \le \rho _ { \operatorname* { m a x } }$

Assumption 3 has the direct interpretation of requiring that the disturbance w can be counteracted by an input that is feasible with respect to (18d). The relaxed problem once again simply convexifies the nonconvex input lower bound by introducing a slack input:

$$
\min _ {\sigma , u, t _ {f}} m (x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) \mathrm{d} t
$$

$$
\mathrm{s.t.} \dot {x} _ {1} (t) = A x _ {2} (t),\tag{19a}
$$

$$
\dot {x} _ {2} (t) = B u (t) + w,\tag{19b}
$$

(19c)

$$
\rho_ {\mathrm{min}} \leq \sigma (t), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{19d}
$$

$$
g _ {1} (u (t)) \leq \sigma (t),\tag{19e}
$$

$$
x _ {2} (t) ^ {\top} H x _ {2} (t) \leq 1,\tag{19f}
$$

$$
x _ {1} (0) = x _ {1, 0}, x _ {2} (0) = x _ {2, 0}, b \left(x \left(t _ {f}\right)\right) = 0.\tag{19g}
$$

Thanks to the structure of the dynamics (19b)-(19c), it can be shown that Condition 1 is automatically satisfied. On the other hand, Condition 2 must be modified to account for the quadratic state constraint.

## Condition 6

If $\zeta = 0 .$ , the vector $\nabla _ { x } m [ t _ { f } ] \in \mathbb { R } ^ { 2 n }$ and the columns of the following matrix must be linearly independent:

$$
\tilde {B} _ {L C v x} = \left[ \begin{array}{c c} \nabla_ {x _ {1}} b [ t _ {f} ] ^ {\intercal} & 0 \\ \nabla_ {x _ {2}} b [ t _ {f} ] ^ {\intercal} & 2 H x _ {2} (t _ {f}) \end{array} \right] \in \mathbb {R} ^ {2 n \times (n _ {b} + 1)}.\tag{20}
$$

Note that Condition 6 carries a subtle but important implication. Recall that due to Assumption $1 , \nabla _ { \boldsymbol { x } } b [ t _ { f } ] ^ { \intercal }$ must be full column rank. Hence, if $\zeta ~ = ~ 0$ then the vector $\left( 0 , \ 2 H x _ { 2 } ( t _ { f } ) \right) \in \mathbb { R } ^ { 2 n }$ and the columns of $\nabla _ { \boldsymbol { x } } b [ t _ { f } ] ^ { \intercal }$ must be linearly dependent. Otherwise, $\tilde { B } _ { L C v x }$ is full column rank and Condition 6 cannot be satisfied. With this in mind, the following LCvx result was proved in [102, Theorem 2].

## Theorem 4

The solution of Problem 19 is globally optimal for Problem 18 if Condition 6 holds. 

## General Convex State Constraints

The preceding two sections discussed problem classes where an LCvx guarantee is available even in the presence of afine or quadratic state constraints. For obviou reasons, an engineer may want to impose more exotic constraints than aforded by Problems 11 and 18. Luck ily, an LCvx guarantee is available for general convex state constraints.

As may be expected, generality comes at the price of a somewhat weaker result. In the preceding sections, the LCvx guarantee was independent from the way in which the afine and quadratic state constraints get activated: instantaneously, for periods of time, or even for the entire optimal trajectory duration. In contrast, for the case of general convex state constraints, an LCvx guarantee will only hold as long as the state constraints are active pointwise in time. In other words, they get activated at isolated time instances and never persistently over a time interval. This result was originally provided in [86].

## Maximum Velocity as a Quadratic State Constraint

![](Malyuta2021Convex_figs/3bc4651421908ae3228b555a960ce8b7add54cdffeed41e44bd7b80bec921a0e.jpg)  
FIGURE S5 Illustration of the boundary of a maximum velocity constraint, which can be expressed as (18e).

The nonconvex problem statement is:

$$
\min _ {u, t _ {f}} m (x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (g _ {1} (u (t))) d t\tag{21a}
$$

$$
\mathrm{s.t.} \dot {x} (t) = A x (t) + B u (t) + E w,\tag{21b}
$$

$$
\rho_ {\mathrm{min}} \leq g _ {1} (u (t)), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{21c}
$$

$$
x (t) \in \mathcal {X},\tag{21d}
$$

$$
x (0) = x _ {0}, b (x (t _ {f})) = 0,\tag{21e}
$$

where $\mathcal { X } \subseteq \mathbb { R } ^ { n }$ is a convex set that defines the state constraints. Without the state constraint, Problem 21 is nothing but the autonomous version of Problem 6. As for Problem 11, time variance can be introduced in a limited way by using a time integrator state, as long as this does not introduce nonconvexity. The relaxed problem uses the by-now familiar slack variable relaxation technique for (21c):

$$
\min _ {\sigma , u, t _ {f}} m (x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) \mathrm{d} t\tag{22a}
$$

$$
\mathrm{s.t.} \dot {x} (t) = A x (t) + B u (t) + E w,\tag{22b}
$$

$$
\rho_ {\mathrm{min}} \leq \sigma (t), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{22c}
$$

$$
g _ {1} (u (t)) \leq \sigma (t),\tag{22d}
$$

$$
x (t) \in \mathcal {X},\tag{22e}
$$

$$
x (0) = x _ {0}, b (x (t _ {f})) = 0.\tag{22f}
$$

The LCvx proof is provided in [86, Corollary 3], and relies on recognizing two key facts:

1. When $x ( t ) \in$ int for any time interval $t \in [ t _ { 1 } , t _ { 2 } ]$ , the state of the optimal control problem is unconstrained along that time interval;

2. For autonomous problems (recall the description after Problem 11), every segment of the trajectory is itself optimal [102].

As a result, whenever $x ( t ) \ \in$ int , the solution of Problem 22 is equivalent to the solution of Problem 7.

f we set $A = I _ { n }$ and $B = I _ { n }$ in Problem 18 then the state $x _ { 2 }$ can be interpreted as a vehicle’s velocity. A maximum velocity constraint $\| x _ { 2 } \| _ { 2 } ~ \le ~ v _ { \mathsf { m a x } }$ can then be equivalently written in the form of (18e) as

$$
x _ {2} ^ {\top} (v _ {\max} ^ {- 2} I _ {n}) x _ {2} \leq 1.\tag{S13}
$$

Figure S5 illustrates the maximum velocity constraint.

![](Malyuta2021Convex_figs/307d89fe30875514c8fcd9eb4eb209609d94c898af86d144b8c3b140cf580822.jpg)  
FIGURE 7 The dashed blue curve represents any segment of the optimal state trajectory for Problem 21 that evolves in the interior of the state constraint set (21d). Because the optimal control problem is autonomous, any such segment is the solution to the stateunconstrained Problem 6. When $\zeta = 1$ and in the limit as $a  \infty$ LCvx applies to the entire (open) segment inside int [86].

Consider an interior trajectory segment, as illustrated in Figure 7. The optimal trajectory for the dashed portion in Figure 7 is the solution of the following fixed final state, free final time problem:

$$
\min _ {u, t _ {f}} m (z (t _ {e})) + \zeta \int_ {t _ {s}} ^ {t _ {e}} \ell (g _ {1} (u (t))) \mathrm{d} t\tag{23a}
$$

$$
\mathrm{s.t.} \dot {z} (t) = A z (t) + B u (t) + E w,\tag{23b}
$$

$$
\rho_ {\mathrm{min}} \leq g _ {1} (u (t)), g _ {0} (u (t)) \leq \rho_ {\mathrm{max}},\tag{23c}
$$

$$
z (t _ {s}) = x (t _ {s}), z (t _ {e}) = x (t _ {e}).\tag{23d}
$$

We recognize that Problem 23 is an instance of Problem 6 and, as long as $\zeta = 1$ (in order for Condition 2 to hold), Theorem 1 applies. Because $a > 0$ can be arbitrarily large in Figure 7, lossless convexification applies over the open time interval $( t _ { 1 } , t _ { 2 } )$ . Thus, the solution segments of the relaxed problem that lie in the interior of the state constraint set are feasible and globally optimal for the original Problem 21.

The same cannot be said when $x ( t ) \in \partial \mathcal { X }$ . During these segments, the solution can become infeasible for Problem 21. However, as long as $x ( t ) \in \partial \mathcal { X }$ at

## Permissible State Constraint Activation for General Convex State Constraints

![](Malyuta2021Convex_figs/be14bf5fb4ec2b384f3448021c82f2cdea3214b11bd4165b82ef033d4852c7ea.jpg)  
FIGURE S6 Illustration of when lossless convexification with general convex state constraints may fail. The two figures on the right show an in-plane projection of the 3D figure on the left. In (a) the glideslope constraint is only activated once prior to landing, hence the solution is lossless. In (b) the constraint is activated for a nontrivial duration and the solution may be infeasible over that interval.

et us go back to the landing glideslope constraint for a spacecraft, which was previously motivated in “Landing Glideslope as an Affine State Constraint”. Because Problem 21 allows us to use any convex state constraint, we can directly use the second-order cone constraint (S9).

As illustrated in Figure S6, lossless convexification in this case will only hold if the spacecraft touches the “landing cone” a finite number of times. In Figure S6(a), the glides-

isolated time instances, LCvx can be guaranteed to hold. This idea is further illustrated in “Permissible State Constraint Activation for General Convex State Constraints”.

When $\zeta = 0$ , the situation becomes more complicated because Condition 2 does not hold for Problem 23. This is clear from the fact that the terms defined in Condition 2 become:

$$
m _ {\mathrm{LCvx}} = \left[ \begin{array}{c} \nabla_ {z} m [ t _ {e} ] \\ 0 \end{array} \right], \quad B _ {\mathrm{LCvx}} = \left[ \begin{array}{c} I _ {n} \\ 0 \end{array} \right],
$$

which are clearly not linearly independent since $\boldsymbol { B } _ { \mathrm { L C v x } }$ is full column rank. Thus, even for interior segments the solution may be infeasible for Problem 21. To remedy this, [86, Corollary 4] suggests Algorithm 1. At its core, the algorithm relies on the following simple idea. By solving Problem 22 with the suggested modifications on line 3 of Algorithm 1, every interior segment once again becomes an instance of Problem 6 for which Theorem 1 holds. Furthermore, due to the constraint $x ( t _ { f } ) ~ = ~ x ^ { * } ( t _ { f } ^ { * } )$ , any solution to the modified problem will be optimal for the original formulation where $\zeta = 0$ (since $m ( x ( t _ { f } ) ) = m ( x ^ { \ast } ( t _ { f } ^ { \ast } ) ) )$ .

This modification can be viewed as a search for an equivalent solution for which LCvx holds. As a conlope constraint is activated only once at time t<sub>1</sub> prior to landing. Hence, $\mathcal { T } = \{ t \in [ 0 , t _ { f } ] : x ( t ) \in \partial \mathcal { X } \} = \{ t _ { 1 } , t _ { f } \}$ is a discrete set and Theorem 5 holds. Note that the constraint may be activated at other times, e.g. $\mathcal { T } = \{ t _ { 1 } , t _ { 2 } , t _ { f } \}$ , as long as these times are all isolated points.

In Figure S6(b) there is an interval of time for which the glideslope constraint is active. This results in a non-discrete set of state constraint activation times $\mathcal { T } = [ t _ { 1 } , t _ { 2 } ] \cup \{ t _ { f } \}$ . For $t \in \left[ t _ { 1 } , t _ { 2 } \right]$ , there is no LCvx guarantee and the solution of Problem 22 may be infeasible for Problem 21 over that interval.

For historical context, LCvx theory was initially developed specifically for planetary rocket landing. For this application, glideslope constraint activation behaves like Figure S6(a), so LCvx holds for that application. Indeed, the constraint (S9) was part of NASA Jet Propulsion Laboratory’s optimization-based rocket landing algorithm flight tests [37, 38, 39, S1, S2].

## REFERENCES

[S1] Behc¸et Ac¸ıkmes¸e et al. “Flight Testing of Trajectories Computed by G-FOLD: Fuel Optimal Large Divert Guidance Algorithm for Planetary Landing”. In: 23rd AAS/AIAA Space Flight Mechanics Meeting, Kauai, HI, 2013. AAS/AIAA, Feb. 2013.

[S2] Daniel P. Scharf et al. “ADAPT demonstrations of onboard large-divert Guidance with a VTVL rocket”. In: 2014 IEEE Aerospace Conference. IEEE, Mar. 2014. DOI: 10.1109/aero.2014.6836462.

Algorithm 1 Solution algorithm for Problem 21. When $\zeta = 0 .$ , a two-step procedure is used where an auxiliary problem with $\zeta = 1$ searches over the optimal solutions to the original problem.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1: Solve Problem 22 to obtain $x^{*}(t_{f}^{*})$
2: if $\zeta = 0$ then
3: Solve Problem 22 again, with the modifications:
» Use the cost $\int_{0}^{t_{f}} \ell(\sigma(t)) \mathrm{d}t$
» Set $b(x(t_{f})) = x(t_{f}) - x^{*}(t_{f}^{*})$
</div>

crete example, Problem 22 may be searching for a minimum miss distance solution for a planetary rocket land ing trajectory [85]. The ancillary problem in Algorithm 1 can search for a minimum fuel solution that achieves the same miss distance. Clearly, other running cost choices are possible. Thus, the ancillary problem’s running cost becomes an extra tuning parameter.

We are now able to summarize the lossless convex ification result for problems with general convex state constraints.

## Theorem 5

Algorithm 1 returns the globally optimal solution of

Problem 21 if the state constraint (21d) is activated at isolated time instances, and Conditions 1 and 2 hold. 

## Nonlinear Dynamics

A unifying theme of the previous sections is the assumption that the system dynamics are linear. In fact, across all LCvx results that we have mentioned so far, the dynamics did not vary much from the first formulation in (6b). Many engineering applications, however, involve non-negligible nonlinearities. A natural question is then whether the theory of lossless convexification can be extended to systems with general nonlinear dynamics.

An LCvx result is available for a class of nonlinear dynamical systems. The groundwork for this extension was presented in [46]. The goal here is to show that the standard input set relaxation based on the LCvx equality constraint is also lossless when the dynamics are nonlinear. Importantly, note that the dynamics themselves are not convexified, so the relaxed optimization problem is still nonlinear, and it is up to the user to solve the problem to global optimality. This is possible in special cases, for example if the nonlinearities are approximated by piecewise afine functions. This yields a mixed-integer convex problem whose globally optimal solution can be found via mixed-integer programming [106].

With this introduction, let us begin by introducing the generalization of Problem 6 that we shall solve using LCvx:

$$
\min _ {u, t _ {f}} m \left(t _ {f}, x \left(t _ {f}\right)\right) + \zeta \int_ {0} ^ {t _ {f}} \ell (g (u (t))) d t\tag{24a}
$$

$$
\text { s.t. } \dot {x} (t) = f (t, x (t), u (t), g (u (t))),\tag{24b}
$$

$$
\rho_ {\mathrm{min}} \leq g (u (t)) \leq \rho_ {\mathrm{max}},\tag{24c}
$$

$$
x (0) = x _ {0}, b \left(t _ {f}, x \left(t _ {f}\right)\right) = 0,\tag{24d}
$$

where $f : \mathbb { R } \times \mathbb { R } ^ { n } \times \mathbb { R } ^ { m } \times \mathbb { R } \to \mathbb { R } ^ { n }$ defines the nonlinear dynamics. Just as for Problem 9, it is required that $g _ { 0 } = g _ { 1 } \triangleq g$ . Consider the following convex relaxation of the input constraint by using a slack input:

$$
\min _ {\sigma , u, t _ {f}} m (t _ {f}, x (t _ {f})) + \zeta \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) \mathrm{d} t\tag{25a}
$$

$$
\mathrm{s.t.} \dot {x} (t) = f (t, x (t), u (t), \sigma (t)),\tag{25b}
$$

$$
\rho_ {\mathrm{min}} \leq \sigma (t) \leq \rho_ {\mathrm{max}},\tag{25c}
$$

$$
g (u (t)) \leq \sigma (t),\tag{25d}
$$

$$
x (0) = x _ {0}, b (t _ {f}, x (t _ {f})) = 0.\tag{25e}
$$

Note that the slack input σ makes a new appearance in the dynamics (25b). The more complicated dynamics require an updated version of Condition 1 in order to guarantee that LCvx holds.

## Condition 7

The pair $\{ \nabla _ { x } f [ t ] , \nabla _ { u } f [ t ] \}$ must be totally controllable on $[ 0 , t _ { f } ]$ for all feasible sequences of $x ( \cdot )$ and $u ( \cdot )$ for Problem 25 [46, 94]. 

Using the above condition, we can state the following quite general LCvx guarantee for problems that fit the Problem 24 template.

## Theorem 6

The solution of Problem 25 is globally optimal for Prob lem 24 if Conditions 2 and 7 hold. 

Alas, Condition 7 is generally quite dificult to check. Nevertheless, two general classes of systems have been shown to automatically satisfy this condition thanks to the structure of their dynamics [46]. These classes ac commodate vehicle trajectory generation problems with double integrator dynamics and nonlinearities like mas depletion, aerodynamic drag, and nonlinear gravity. The following discussion of these system classes can appear hard to parse at first sight. For this reason, we provide two practical examples of systems that belong to each class in “Examples of Losslessly Convexifiable Nonlinear Systems”.

The first corollary of Theorem 6 introduces the first class of systems. A key insight is that the nullspace con ditions of the corollary require that $2 m \geq n$ , in other words there are at least twice as many control variables as there are state variables. This is satisfied by some ve hicle trajectory generation problems where $2 m = n ,$ , for example when the state consists of position and velocit while the control is an acceleration that acts on all the velocity states. This is a common approximation for flying vehicles. We shall see an example for rocket landing in Part III of the article.

## Corollary 1

Suppose that the dynamics (24b) are of the form:

$$
x = \left[ \begin{array}{c} x _ {1} \\ x _ {2} \end{array} \right], f (t, x, u, g (u)) = \left[ \begin{array}{c} f _ {1} (t, x) \\ f _ {2} (t, x, u) \end{array} \right],\tag{26}
$$

where nul $| ( \nabla _ { u } f _ { 2 } ) = \{ 0 \}$ and nul $\left( \nabla _ { x _ { 2 } } f _ { 1 } \right) = \{ 0 \}$ . Then Theorem 6 applies if Condition 2 holds. 

The next corollary to Theorem 6 introduces the second class of systems, for which 2m $< n$ is allowed. This class is once again useful for vehicle trajectory generation problems where the dynamics are given by (27) and $g ( u )$ is a function that measures control efort. A practical example is when the state $x _ { 2 }$ is mass, which is depleted as a function of the control efort (such as thrust for a rocket).

## Corollary 2

Suppose that the dynamics (24b) are of the form:

$$
x = \left[ \begin{array}{c} x _ {1} \\ x _ {2} \end{array} \right], f (t, x, u, g (u)) = \left[ \begin{array}{c} f _ {1} (t, x, u) \\ f _ {2} (t, g (u)) \end{array} \right].\tag{27}
$$

Define the matrix:

$$
M \triangleq \left[ \begin{array}{c} (\nabla_ {u} f _ {1}) ^ {\intercal} \\ \frac {\mathrm{d} (\nabla_ {u} f _ {1}) ^ {\intercal}}{\mathrm{d} t} - (\nabla_ {u} f) ^ {\intercal} (\nabla_ {x} f _ {1}) ^ {\intercal} \end{array} \right].\tag{28}
$$

## Examples of Losslessly Convexifiable Nonlinear Systems

![](Malyuta2021Convex_figs/3fb32e779e7932b3b517b245cc25eb6c4987a43576384421a1ff326cd2f7d350.jpg)  
(a) Landing a rocket in the presence of nonlinear gravity and atmospheric drag.  
(b) Autonomous aircraft trajectory generation with a stall constraint and aerodynamic drag.  
FIGURE S7 Illustrations of two nonlinear system for which the lossless convexification result of Theorem 6 can be applied.

t first sight, the discussion around Corollaries 1 and 2 may be hard to parse into something useful. However, we will now show two concrete and very practical examples of dynamical systems that satisfy these corollaries. Both examples originate from [46].

## Nonlinear Rocket Landing

First, LCvx can be used for rocket landing with nonlinear gravity and aerodynamic drag. Both effects are important

Furthermore, suppose that the terminal constraint function b is afine and $x _ { 2 } ( t _ { f } )$ is unconstrained, such that $\nabla _ { x _ { 2 } } b = 0$ . Then Theorem 6 applies if null(M) = 0 and Condition 2 holds.

It must be emphasized that Problem 25 is still a nonlinear program and that for Theorem 6 to hold, a globally optimal solution of Problem 25 must be found. Although this cannot be done for general nonlinear programming, if the dynamics f are piecewise afine then the problem can be solved to global optimality via mixed-integer programming [106, 107, 108]. In this case, convexification of the nonconvex input lower bound reduces the number of disjunctions in the branch-and-bound tree, and hence lowers the problem complexity [46]. Several examples of nonlinear systems that can be modeled in this way, and which comply with Corollaries 1 and 2, are illustrated in “Approximating Nonlinear Systems with Piecewise Afine Functions”.

for landing either on small celestial bodies with a weak gravitational pull, or on planets with a thick atmosphere (such as our very own Earth). In this case, the lander dynamics can be written as:

$$
\ddot {r} (t) = g (r (t)) - \frac {c}{m (t)} \| \dot {r} (t) \| _ {2} \dot {r} (t) + \frac {T (t)}{m (t)},\tag{S14a}
$$

$$
\dot {m} (t) = - \alpha \| T (t) \| _ {2},\tag{S14b}
$$

where r denotes position, m is mass, T is thrust, c is the drag coefficient, α is inversely proportional to the rocket engine’s specific impulse, and $\smash { \boldsymbol { g } : \mathbb { R } ^ { 3 } \to \mathbb { R } ^ { 3 } }$ is the nonlinear gravity model. An illustration is given in Figure S7a.

We can rewrite the above dynamics using the template of (24b) by defining the state $x \triangleq ( r , \dot { r } , m ) \in \mathbb { R } ^ { 7 }$ , the input $u \triangleq T \in \mathbb { R } ^ { 3 }$ , and the input penalty function $g ( u ) \triangleq \| u \| _ { 2 }$ The equations of motion can then be written as (omitting the time argument for concision):

$$
\begin{array}{c} f (t, x, u, g (u)) = \left[ \begin{array}{c} f _ {r} (x, u) \\ f _ {\dot {r}} (x) \\ f _ {m} (g (u)) \end{array} \right], \\ = \left[ \begin{array}{c} \dot {r} \\ g (r) - c m ^ {- 1} \| \dot {r} \| _ {2} \dot {r} + T m ^ {- 1} \\ - \alpha \| T \| _ {2} \end{array} \right]. \end{array}
$$

(continued...)

## Embedded Lossless Convexification

The reader will notice that the LCvx theory of the pre vious sections deals with special cases of problems whose nonconvexity is “just right” for an LCvx guarantee to be provable using the maximum principle. Although such problems have found their practical use in prob lems like spaceflight [37] and quadrotor path planning [52], it leaves out many trajectory generation applica tions that do not fit the tight mold of original problem and conditions of the previous sections.

Despite this apparent limitation, LCvx is still highl relevant for problems that simply do not conform to one of the forms given in the previous sections. For such problems, we assume that the reader is facing the chal lenge of solving a nonconvex optimal control problem that fits the mold of Problem 39 (the subject of Part II of the article), and is considering whether LCvx can help. There is evidence that the answer is afirmative, by using LCvx theory only on the constraints that are losslessl convexifiable. We call this embedded LCvx, because it is used to convexify only part of the problem, while

(continued...)

This system belongs to the class in Corollary 2. In particular, let $\boldsymbol { f } _ { 1 } = \left( f _ { r } , f _ { \dot { r } } \right)$ and $f _ { 2 } = f _ { m }$ . Working out the algebra in (28), we have:

$$
M = \left[ \begin{array}{c c} 0 & m ^ {- 1} I \\ m ^ {- 1} I & M _ {2 2} \end{array} \right],\tag{S15}
$$

where $\begin{array} { r } { M _ { 2 2 } = - \frac { c } { m ^ { 2 } } \left( \| \dot { r } \| _ { 2 } I + \frac { \dot { r } \dot { r } ^ { \top } } { \| \dot { r } \| _ { 2 } } \right) + \alpha \frac { T T ^ { \top } } { m ^ { 2 } \| T \| _ { 2 } } } \end{array}$ . Thanks to the off-diagonal terms, nul $( M ) = \mathrm { \large ~ \left\{ 0 \right\} ~ }$ unconditionally, so the rocket lander dynamics satisfy the requirements of Corollary 2.

## AAV Trajectory Generation Without Stalling

An autonomous aerial vehicle (AAV) can lose control and fall out of the sky if its airspeed drops below a certain value. This occurs because the wings fail to generate enough lift, resulting in an aerodynamic stall. It was shown in [46] that a stall speed constraint of the form $v _ { \operatorname* { m i n } } \leq \| v \| _ { 2 }$ can be handled by LCvx via the following dynamics:

$$
\dot {r} (t) = v (t) + v _ {\infty} (t),\tag{S16a}
$$

$$
\dot {v} (t) = \kappa \big (v _ {d} (t) - v (t) \big) - c \| v (t) \| _ {2} v (t),\tag{S16b}
$$

where v is the airspeed, ˙r is the ground velocity, and $v _ { \infty }$ is the velocity of the air mass relative to the ground (also

the rest is handled by another nonconvex optimization method such as presented in Part II of this article. Because LCvx reduces the amount of nonconvexity present in the problem, it can significantly improve the convergence properties and reduce the computational cost to solve the resulting problem. An example of this approach for quadrotor trajectory generation is demonstrated in Part III.

The basic procedure for applying embedded LCvx is illustrated in Figure 8. As shown in Figure 8b, we reiterate that LCvx is not a computation scheme, but rather it is a convex relaxation with an accompanying proof of equivalence to the original problem. As such, it happens prior to the solution and simply changes the problem description seen by the subsequent numerical optimization algorithm.

There are a number of examples of embedded LCvx that we can mention. First, the previous section on nonlinear dynamics can be intepreted as embedded LCvx. For example, [46] solves a rocket landing problem where only the nonconvex input constraint (24c) is convexified. This leaves behind a nonconvex problem due to nonlinear dynamics, and mixed-integer programming is used to solve it. Another example is [109], where LCvx is embedded in a mixed-integer autonomous aerial vehicle trajectory generation problem in order to convexify a known as the freestream velocity). An illustration is given in Figure S7b.

The key transformation in (S16) is to make the desired airspeed $V _ { d }$ the control variable, and to include a velocity control inner-loop via a proportional controller with gain κ. Because the velocity dynamics are of first-order, v converges to $V _ { d }$ along a straight path in the velocity phase plane, hence the stall speed constraint is closely approximated for small control errors $\| v _ { d } - v \| _ { 2 }$ <sub>2</sub>.

We can rewrite the dynamics using the template of (24b) by defining the state $x \triangleq ( r , v ) \in \mathbb { R } ^ { 6 }$ and the input $u \triangleq v _ { d } \in$ $\mathbb { R } ^ { 3 }$ . The equations of motions can then be written as:

$$
\begin{array}{c} f (t, x, u, g (u)) = \left[ \begin{array}{c} f _ {r} (t, x) \\ f _ {v} (x, u) \end{array} \right], \\ = \left[ \begin{array}{c} v + v _ {\infty} \\ - \kappa v - c \| v \| _ {2} v + \kappa v _ {d} \end{array} \right]. \end{array}
$$

This system belongs to the class in Corollary 1. In particular, let $f _ { 1 } = f _ { r }$ and $f _ { 2 } = f _ { v }$ . We then have $\nabla _ { u } f _ { 2 } = - \kappa I$ and $\nabla _ { x _ { 2 } } f _ { 1 } = I .$ Therefore, nul $| ( \nabla _ { u } f _ { 2 } ) = \{ 0 \}$ and nul $| ( \nabla _ { x _ { 2 } } f _ { 1 } ) =$ 0 , so the aircraft dynamics satisfy the requirements of Corollary 1.

stall speed constraint of the form:

$$
0 <   v _ {\mathrm{min}} \leq \| v _ {c m d} (t) \| _ {2} \leq v _ {\mathrm{max}},\tag{29}
$$

where the input $v _ { c m d } ( \cdot ) \in \mathbb { R } ^ { 3 }$ is the commanded veloc ity, while $v _ { \mathrm { m i n } }$ and $v _ { \mathrm { m a x } }$ are lower and upper bounds that guarantee a stable flight envelope. The same constraint is also considered in [46]. In [53], the authors develop a highly nonlinear planetary entry trajectory optimiza tion problem where the control input is the bank an gle $\beta \in \mathbb { R }$ , parameterized via two inputs $u _ { 1 } \ { \stackrel { \triangle } { = } } \ \cos ( \beta )$ and $u _ { 2 } \triangleq \sin ( \beta )$ The associated constraint $\| u \| _ { 2 } ^ { 2 } = 1$ is convexified to $\| u \| _ { 2 } ^ { 2 } \leq 1$ , and equality at the optimal solution is shown in an LCvx-like fashion (the authors call it “assurance of active control constraint”). Simila methods are used in [55] in the context of rocket landing with aerodynamic controls. A survey of related meth ods is available in [110]. Finally, we will mention [52, 58] where embedded LCvx is used to convexify an input lower bound and an attitude pointing constraint for rocket landing and for agile quadrotor flight. Sequential convex programming from Part II is then using to solve the remaining nonlinear optimal control problems. The quadrotor application in particular is demonstrated as a numerical example in Part III.

As a result of the success of these applications, we fore see there being further opportunities to use LCvx as a strategy to derive simpler problem formulations. The re

## Approximating Nonlinear Systems with Piecewise Affine Functions

iecewise affine functions can be used for arbitrarily accurate approximation of any nonlinear function. This is the technique used by [46] to write the nonlinear dynamics (25b) in piecewise affine form. Doing so enables solving Problem 25 to global optimality via mixed-integer programming, which is imperative for the LCvx guarantee of Theorem 6. We now show how a piecewise affine approximation can be obtained in the general case, and concretely in the case of the dynamics from “Examples of Losslessly Convexifiable Nonlinear Systems”.

## General Case

We begin by finding a first-order approximation of the nonlinear equation $f : \mathbb { R } \times \mathbb { R } ^ { n } \times \mathbb { R } ^ { m } \times \mathbb { R } \to \mathbb { R } ^ { n }$ from (25b) about an operating point $\left( t , \bar { x } ^ { i } , \bar { u } ^ { i } \right) \in \mathbb { R } \times \mathbb { R } ^ { n } \times \mathbb { R } ^ { m }$ , where i is an integer index that shall become clear in a moment. Without loss of generality, assume that f is decomposable into an affine and a non-affine part:

$$
f = f _ {a} + f _ {n a}.\tag{S17}
$$

The first-order Taylor expansion of f is given by:

$$
f \approx f _ {a} + f _ {n a} ^ {i},
$$

$$
f _ {n a} ^ {i} \triangleq \bar {f} _ {n a} + (\nabla_ {x} \bar {f} _ {n a}) (x - \bar {x}) + (\tilde {\nabla} _ {u} \bar {f} _ {n a}) (u - \bar {u}),\tag{S18}
$$

where we have used the shorthand:

$$
f _ {n a} ^ {i} = f _ {n a} ^ {i} (t, x, u, g (u)),\tag{S19a}
$$

$$
\bar {f} _ {n a} = f _ {n a} \big (t, \bar {x} ^ {i}, \bar {u} ^ {i}, g (\bar {u} ^ {i}) \big),\tag{S19b}
$$

$$
\tilde {\nabla} _ {u} f _ {n a} = \nabla_ {u} f _ {n a} + (\nabla_ {g} f _ {n a}) (\nabla g) ^ {\top}.\tag{S19c}
$$

In (S19c), we understand $\nabla _ { g } f _ { n a }$ as the Jacobian of $f _ { n a }$ with respect to its fourth argument. Suppose that the linearization in (S18) is sufficiently accurate only over the hyperrect-

sult would be a speedup in computation for optimizationbased trajectory generation.

## The Future of Lossless Convexification

Lossless convexification is a method that solves nonconvex trajectory generation problems with one or a small number of calls to a convex solver. This places it among the most reliable and robust methods for nonconvex trajectory generation. The future of LCvx therefore has an obvious motivation: to expand the class of problems that can be losslessly convexified. The most recent result discussed in the previous sections is for problems with afine state constraints [89], and this dates back to 2014. In the past two years, LCvx research has been rejuvenated by several fundamental discoveries and practical methods angular region $\mathcal { R } ^ { i } \subset \mathbb { R } ^ { n } \times \mathbb { R } ^ { m }$ defined by the following in equalities:

$$
\bar {x} ^ {i} + b _ {L, x} ^ {i} \leq x \leq \bar {x} ^ {i} + b _ {U, x} ^ {i},\tag{S20a}
$$

$$
\bar {u} ^ {i} + b _ {L, u} ^ {i} \leq u \leq \bar {u} ^ {i} + b _ {U, u} ^ {i},\tag{S20b}
$$

where $b _ { L , x } ^ { i }$ and $b _ { U , x } ^ { i }$ represent the upper and lower bounds on the state, while $b _ { L , u } ^ { i }$ and $b _ { U , u } ^ { i }$ relate to the input. The index i now takes on a clear meaning: it represents the ith “validity” region. Without loss of generality, we assume $\mathcal { R } ^ { i } \cap \mathcal { R } ^ { j } = \emptyset \mathfrak { i } \mathfrak { i } \ne j$ . In general, $i = 1 , \dots , N$ , which means that f is approximated by affine functions over N regions. The piecewise affine approximation of f can then be written as:

$$
f _ {p w a} \triangleq f _ {a} + f _ {n a} ^ {i}, \text {   for   } i \text {   such   that   } (x, u) \in \mathcal {R} ^ {i}.\tag{S21}
$$

The big-M formulation can be used to write (S21) in a form that is readily used in a mixed-integer program [108]. To this end, let $M > 0$ be a sufficiently large fixed scalar parameter, and let $z ^ { i } \in \{ 0 , 1 \}$ be a binary variable indicating that $( x , u ) \in \mathcal { R } ^ { i }$ if and only if $z ^ { i } = 1$ Then, the piecewise affine dynamics in mixed-integer programming form are encoded by the following set of constraints:

$$
\dot {x} = f _ {a} (t, x, u, g (u)) + \sum_ {i = 1} ^ {N} z ^ {i} f _ {n a} ^ {i} (t, x, u, g (u)),\tag{S22a}
$$

$$
x \geq \bar {x} ^ {i} + b _ {L, x} ^ {i} - M (1 - z ^ {i}),\tag{S22b}
$$

$$
x \leq \bar {x} ^ {i} + b _ {U, x} ^ {i} + M (1 - z ^ {i}),\tag{S22c}
$$

$$
u \geq \bar {u} ^ {i} + b _ {L, u} ^ {i} - M (1 - z ^ {i}),\tag{S22d}
$$

$$
u \leq \bar {u} ^ {i} + b _ {U, u} ^ {i} + M (1 - z ^ {i}),\tag{S22e}
$$

$$
1 = \sum_ {i = 1} ^ {N} z ^ {i}.\tag{S22f}
$$

$$
(\text {continued...})
$$

that expand the method to new and interesting problem types. This section briefly surveys these new results.

## Fixed-final Time Problems

The first new LCvx result applies to a fixed-final time and fixed-final state version of Problem 6 with no state constraints. To begin, recognize that the classical LCvx result from Theorem 1 does not apply when both $t _ { f }$ and $x ( t _ { f } )$ are fixed. In this case, $B _ { \mathrm { L C v x } } = I _ { n + 1 }$ in (8b) and therefore its columns, which span all of $\mathbb { R } ^ { n + 1 }$ , cannot be linearly independent from $m _ { \mathrm { L C v x } }$ . Thus, traditionally one could not fix the final time and the final state simultaneously. Very recently, Kunhippurayil et al. [92] showed that Condition 2 is in fact not necessary for the

(continued...)

## Nonlinear Rocket Landing

Consider the rocket dynamics in (S14a) and, for simplicity, suppose that the mass is constant. Define the state $x \triangleq ( r , \dot { r } ) \in \mathbb { R } ^ { 6 }$ and the input $u \triangleq T \in \mathbb { R } ^ { 3 }$ . The non-affine part of the dynamics (S17) then takes the particular form:

$$
f _ {n a} = \left[ \begin{array}{c} 0 \\ g (r) - c m ^ {- 1} \| \dot {r} \| _ {2} \dot {r} \end{array} \right].\tag{S23}
$$

For simplicity, let us consider only the nonlinear gravity term, ${ \boldsymbol { g } } ( { \boldsymbol { r } } )$ . We will deal with atmospheric drag for AAV trajectory generation below. Suppose that $g ( r ) = ( 0 , 0 , g _ { z } ( r _ { z } ) )$ which means that we only need to consider the vertical component $g _ { z } : \mathbb { R } \to \mathbb { R } . \ \mathsf { A }$ typical profile is $g _ { z } ( r _ { z } ) = - \mu / r _ { z } ^ { 2 }$ where $\mu$ is the gravitational parameter. Given a reference point $\overline { { r } } _ { z } ^ { i } ,$ , we have:

$$
g _ {z} ^ {i} = g _ {z} (\bar {r} _ {z} ^ {i}) + g _ {z} ^ {\prime} (\bar {r} _ {z} ^ {i}) (r _ {z} - \bar {r} _ {z}).\tag{S24}
$$

Using (S21) and (S24), Figure S8 draws $g _ { z , p w a }$

![](Malyuta2021Convex_figs/ca5f15b50b86db233dabfd7f373ceb166a31f140770f0eda7a0af1ad409ebae0.jpg)

FIGURE S8 Illustration of a piecewise affine approximation of $g _ { z }$ , the z-component of the nonlinear gravity force, using (S24).

## AAV Trajectory Generation Without Stalling

Consider the AAV dynamics in (S16) and, for simplicity, assume constant altitude flight. Define the state $x \triangleq ( r , v ) \in$

following version of Problem 6:

$$
\min _ {u, t _ {f}} \int_ {0} ^ {t _ {f}} \ell (g (u (t))) \mathrm{d} t\tag{30a}
$$

$$
\text { s.t. } \dot {x} (t) = A x (t) + B u (t),\tag{30b}
$$

$$
\rho_ {\mathrm{min}} \leq g (u (t)) \leq \rho_ {\mathrm{max}},\tag{30c}
$$

$$
x (0) = x _ {0},   x (t _ {f}) = x _ {f},\tag{30d}
$$

where $t _ { f }$ is fixed and $x _ { f } \in \mathbb { R } ^ { n }$ specifies the final state. The lossless relaxation is the usual one, and is just a specialization of Problem 7 for Problem 30:

$$
\min _ {\sigma , u, t _ {f}} \int_ {0} ^ {t _ {f}} \ell (\sigma (t)) \mathrm{d} t\tag{31a}
$$

$$
\text { s.t. } \dot {x} (t) = A x (t) + B u (t) w (t),\tag{31b}
$$

$\mathbb { R } ^ { 4 }$ and the input $u = v _ { d } \in \mathbb { R } ^ { 2 }$ . The non-affine part of the dynamics (S17) then takes the particular form:

$$
f _ {n a} = \left[ \begin{array}{c} 0 \\ - c ^ {- 1} \| v \| _ {2} v \end{array} \right].\tag{S25}
$$

Let us focus on the aerodynamic drag term, $\begin{array} { r l } { f _ { d } } & { { } = } \end{array}$ $- c \| v \| _ { 2 } v$ . The first order Taylor expansion about a reference airspeed $\hat { v } ^ { j }$ is:

$$
f _ {d} ^ {i} = - c ^ {- 1} \| \bar {v} ^ {i} \| _ {2} \left[ I + \| \bar {v} ^ {i} \| _ {2} ^ {- 2} \bar {v} ^ {i} \bar {v} ^ {i ^ {\mathrm{T}}} \right] (v - \bar {v} ^ {i}).\tag{S26}
$$

Using (S21) and (S26), Figure S9 draws $f _ { d , p w a }$

![](Malyuta2021Convex_figs/0223c7a07b9e665ff63f245409ad5ce09699bdfdc62ed8f562e57e75a56fae60.jpg)

(a) Surface of the continuous function $- f _ { d , x }$ . The blue dots display op erating points at which the gradient is evaluated.

![](Malyuta2021Convex_figs/bceb9610697a91e86e92114dbf65cc84794a39a22db98addc292518fe0b8169d.jpg)  
(b) Surface of the discontinuous piecewise affine approximation $- f _ { d _ { X } , p w a } .$ The blue dashed rectangle in the airspeed space shows the boundary of the approximation validity region $\mathcal { R } ^ { j }$

FIGURE S9 Illustration of a piecewise affine approximation of $f _ { d _ { x } }$ the x-component of the aerodynamic drag force, using (S26).

$$
\rho_ {\mathrm{min}} \leq \sigma (t) \leq \rho_ {\mathrm{max}},
$$

$$
g (u (t)) \leq \sigma (t),\tag{31c}
$$

$$
x (0) = x _ {0},   x (t _ {f}) = x _ {f}.\tag{31d}
$$

(31e)

The following result is then proved in [92]. By dropping Condition 2, the result generalizes Theorem 1 and significantly expands the reach of LCvx to problems without state constraints.

## Theorem 7

The solution of Problem 31 is globally optimal for Prob lem 30 if Condition 1 holds and $t _ { f }$ is between the min imum feasible time and the time that minimizes (30a). For longer trajectory durations, there exists a solution to Problem 31 that is globally optimal for Problem 30.

![](Malyuta2021Convex_figs/972f0a45c836a44fa93969fcdd423728b019ea4a975de69dbd40cdd5094d7988.jpg)  
(a) The solution process for a nonconvex optimal control problem, without using LCvx.

![](Malyuta2021Convex_figs/3025914f3574336e93f0ec27434d5776d88137d231a6dc5abad0207c1fe123d6.jpg)  
(b) The solution process for a nonconvex optimal control problem, where LCvx is embedded to convexify part of the original problem.  
FIGURE 8 Illustration of how embedded LCvx can be used to solve an optimal control problem that does not fit into any of the templates presented in Part I of this article.

Perhaps the most important part of Theorem 7, and a significant future direction for LCvx, is in its final sentence. Although a lossless solution “exists”, how does one find it? An algorithm is provided in [92] to find the lossless solution, that is, one solution among many others which may not be lossless. This is similar to Theorem 5 and Algorithm 1: we know that slackness in (31d) may occur, so we devise an algorithm that works around the issue and is able to recover an input for which (31d) holds with equality. Most traditional LCvx results place further restrictions on the original problem in order to “avoid” slackness, but this by definition limits the applicability of LCvx. By instead providing algorithms which recover lossless inputs from problems that do not admit LCvx naturally, we can tackle lossless convexification “head on” and expand the class of losslessly convexifiable problems. A similar approach is used for spacecraft rendezvous in [56], where an iterative algorithm modifies the dynamics in order to extract bang-bang controls from a solution that exhibits slackness.

## Hybrid System Problems

Many physical systems contain on-of elements such as valves, relays, and switches [46, 108, 111, 112, 113]. Discrete behavior can also appear through interactions between the autonomous agent and its environment, such as through foot contact for walking robots [114, 115]. Modeling discrete behavior is the province of hybrid systems theory, and the resulting trajectory problems typically combine continuous variables and discrete logic elements (i.e., “and” and “or” gates) [111, 113, 116]. Because these is no concept like local perturbation for values that, for example, can only be equal to zero or one, problems with discrete logic are fundamentally more difficult. Traditional solution methods use mixed-integer programming [106]. The underlying branch-and-bound method, however, has poor (combinatorial) worst-case complexity. Historically, this made it very dificult to put optimization with discrete logic onboard computation ally constrained and safety-critical systems throughout aerospace, automotive, and even state-of-the-art robotics [117].

Two recent results showed that LCvx can be applied to certain classes of hybrid optimal control problems that are useful for trajectory generation [90, 91]. While the results are more general, the following basic problem will help ground our discussion:

$$
\min _ {u, \gamma , t _ {f}} \int_ {0} ^ {t _ {f}} \sum_ {i = 1} ^ {M} \| u _ {i} (t) \| _ {2} \mathrm{d} t\tag{32a}
$$

$$
\mathrm{s.t.} \dot {x} (t) = A x (t) + B \sum_ {i = 1} ^ {M} u _ {i} (t),\tag{32b}
$$

$$
\gamma_ {i} (t) \rho_ {\min, i} \leq \| u _ {i} (t) \| _ {2} \leq \gamma_ {i} (t) \rho_ {\max, i},
$$

$$
\gamma_ {i} (t) \in \{0, 1 \},\tag{32c}
$$

$$
C _ {i} u _ {i} (t) \leq 0,\tag{32d}
$$

(32e)

$$
x (0) = x _ {0}, b \big (t _ {f}, x (t _ {f}) \big) = x _ {f},\tag{32f}
$$

where M is the number of individual input vectors and the binary variables $\gamma _ { i }$ are used to model the on-of na ture of each input. Compared to the traditional Prob lem 6, this new problem can be seen as a system controlled by M actuators that can be either $ { { } ^ { 6 } \mathrm { o f f } ^ { 9 } }$ or “on” and norm-bounded in the $[ \rho _ { \mathrm { m i n } , i } , \rho _ { \mathrm { m a x } , i } ]$ interval. The afine input constraint (32e) represents an afine cone, and is a specialized version of the earlier constraint (11d). Figure 9 illustrates the kind of input set that can be modeled. Imitating the previous results, the convex re laxation uses a slack input for each control vector:

$$
\min _ {\sigma , u, \gamma , t _ {f}} \int_ {0} ^ {t _ {f}} \sum_ {i = 1} ^ {M} \ell (\sigma_ {i} (t)) \mathrm{d} t\tag{33a}
$$

$$
\text { s.t. } \dot {x} (t) = A x (t) + B \sum_ {i = 1} ^ {M} u _ {i} (t),\tag{33b}
$$

$$
\gamma_ {i} (t) \rho_ {\min, i} \leq \sigma_ {i} (t) \leq \gamma_ {i} (t) \rho_ {\max, i},\tag{33c}
$$

$$
\left\| u _ {i} (t) \right\| _ {2} \leq \sigma_ {i} (t),\tag{33d}
$$

$$
0 \leq \gamma_ {i} (t) \leq 1,\tag{33e}
$$

$$
C _ {i} u _ {i} (t) \leq 0,\tag{33f}
$$

$$
x (0) = x _ {0}, b \big (t _ {f}, x (t _ {f}) \big) = x _ {f},\tag{33g}
$$

where the only real novelty is that the $\gamma _ { i }$ variables have also been relaxed to the continuous [0, 1] interval.

Taking Problem 33 as an example, the works of [90, 91] prove lossless convexification from slightly diferent angles. In [91] it is recognized that Problem 33 will be a lossless convexification of Problem 32 if the dynami cal system is “normal” due to the so-called bang-bang principle [12, 118]. Normality is related to, but much stronger than, the notion of controllability from Con dition 1. Nevertheless, it is shown that the dynamical system can be perturbed by an arbitrarily small amount to induce normality. This phenomenon was previously observed in a practical context for rocket landing LCvx with a pointing constraint, which we discussed for Problem 9 [87]. Practical examples are shown for spacecraft orbit reshaping, minimum-energy transfer, and CubeSat diferential drag and thrust maneuvering. It is noted that while mixed-integer programming fails to solve the latter problem, the convex relaxation is solved in $< 0 . 1$ seconds.

![](Malyuta2021Convex_figs/250a6a9a34a9bfcae21a6a89fbea8ed6f9f5a025ddbbdfbdc0866a780e3d9616.jpg)  
FIGURE 9 Example of a feasible input set that can be modeled in Problem 32. It is a nonconvex disconnected set composed of the origin, a point, an arc, and a nonconvex set with an interior. For example, this setup can represent a satellite equipped with thrusters and drag plates, or a rocket with a thrust-gimbal coupled engine [90, 91].

The results in [57, 90] also prove lossless convexification for Problem 33. However, instead of leveraging normality and perturbing the dynamics, the nonsmooth maximum principle [104, 119, 120] is used directly to develop a set of conditions for which LCvx holds. These conditions are an interesting mix of problem geometry (i.e., the shapes and orientations of the constraint cones (33f)) and Conditions 1 and 2. Notably, they are more general than normality, so they can be satisfied by systems that are not normal. Practical examples are given for spacecraft rendezvous and rocket landing with a coupled thrust-gimbal constraint. The solution is observed to take on the order of a few seconds and to be more than 100 times faster than mixed-integer programming.

We see the works [90, 91] as complementary: [90] shows that for some systems, the perturbation proposed by [91] is not necessary. On the other hand, [91] provides a method to recover LCvx when the conditions of [90] fail. Altogether, the fact that an arbitrarily small perturbation of the dynamics can recover LCvx suggests a deeper underlying theory for how and why problems can be losslessly convexified. We feel that the search for this theory will be a running theme of future LCvx research, and its eventual discovery will lead to more general lossless convexification algorithms.

## Toy Example

The following example provides a simple illustration of how LCvx can be used to solve a nonconvex problem. This example is meant to be a “preview” of the practical application of LCvx. More challenging and realistic examples are given in Part III.

The problem that we will solve is minimum-efort control of a double integrator system (such as a car) with a constant “friction” term g. This can be written as a linear time-invariant instance of Problem 6:

$$
\min _ {u} \int_ {0} ^ {t _ {f}} u (t) ^ {2} \mathrm{d} t\tag{34a}
$$

$$
\mathrm{s.t.} \dot {x} _ {1} (t) = x _ {2} (t),
$$

$$
\dot {x} _ {2} (t) = u (t) - g,\tag{34b}
$$

$$
1 \leq | u (t) | \leq 2,\tag{34c}
$$

$$
x _ {1} (0) = x _ {2} (0) = 0,\tag{34d}
$$

(34e)

$$
x _ {1} (t _ {f}) = s, x _ {2} (t _ {f}) = 0, t _ {f} = 1 0.\tag{34f}
$$

The input $u ( \cdot ) \in \mathbb { R }$ is the acceleration of the car. The constraint (34d) is a nonconvex one-dimensional version of the constraint (S1). Assuming that the car has unit mass, the integrand in (34a) has units of Watts. The objective of Problem 34 is therefore to move a car by a distance s in $t _ { f } = 1 0$ seconds while minimizing the average power. Following the relaxation template provided by Problem 7, we propose the following convex relaxation to solve Problem 34:

$$
\min _ {\sigma , u} \int_ {0} ^ {t _ {f}} \sigma (t) ^ {2} \mathrm{d} t\tag{35a}
$$

$$
\mathrm{s.t.} \dot {x} _ {1} (t) = x _ {2} (t),\tag{35b}
$$

$$
\dot {x} _ {2} (t) = u (t) - g,\tag{35c}
$$

$$
1 \leq \sigma (t) \leq 2,\tag{35d}
$$

$$
| u (t) | \leq \sigma (t),\tag{35e}
$$

$$
x _ {1} (0) = x _ {2} (0) = 0,\tag{35f}
$$

$$
x _ {1} (t _ {f}) = s, x _ {2} (t _ {f}) = 0, t _ {f} = 1 0.\tag{35g}
$$

To guarantee that LCvx holds, in other words that Problem 35 finds the globally optimal solution of Prob lem 34, let us first attempt to verify the conditions of Theorem 1. In particular, we need to show that Con ditions 1 and 2 hold. First, from (34b)-(34c), we can extract the following state-space matrices:

$$
A = \left[ \begin{array}{c c} 0 & 1 \\ 0 & 0 \end{array} \right], B = \left[ \begin{array}{c} 0 \\ 1 \end{array} \right].\tag{36}
$$

We can verify that Condition 1 holds by either showing that the controllability matrix is full rank, or by using the PBH test [95]. Next, from (35a) and (35f)-(35g), we can extract the following terminal cost and terminal constraint functions:

$$
m (t _ {f}, x (t _ {f})) = 0, b (t _ {f}, x (t _ {f})) = \left[ \begin{array}{c} t _ {f} - 1 0 \\ x _ {1} (t _ {f}) - s \\ x _ {2} (t _ {f}) \end{array} \right].\tag{37}
$$

We can now substitute (37) into (8) to obtain:

$$
m _ {\mathrm{LCvx}} = \left[ \begin{array}{c} 0 \\ 0 \\ \sigma (t _ {f}) ^ {2} \end{array} \right], B _ {\mathrm{LCvx}} = I _ {3}.\tag{38}
$$

Thus, $\boldsymbol { B } _ { \mathrm { L C v x } }$ is full column rank and its columns cannot be linearly independent from $m _ { \mathrm { L C v x } }$ . We conclude that Condition 2 does not hold, so Theorem 1 cannot be applied. In fact, Problem 34 has both a fixed final time and a fixed final state. This is exactly the edge case for which traditional LCvx does not apply, as was mentioned in the previous section on future LCvx. Instead, we fal back on Theorem 7 which says that Condition 2 is not needed as long as $t _ { f }$ is between the minimum and optimal times for Problem 34. It turns out that this holds for the problem parameters used in Figure 10. The minimum time is just slightly below 10 s and the optima time is 13.8 s for Figure 10a and 13.3 s for Fig ure 10b. Most interestingly, lossless convexification fails (i.e., (35e) does not hold with equality) for $t _ { f }$ values al most exactly past the optimal time for Figure 10a, and just slightly past it for Figure 10b.

Although Problem 35 is convex, it has an infinite number of solution variables because time is continuous. To be able to find an approximation of the optimal solution using a numerical convex optimization algorithm, the problem must be temporally discretized. To this end, we apply a first-order hold (FOH) discretization with $N = 5 0$ temporal nodes, as explained in “Discretizing Continuous-time Optimal Control Problems”.

Looking at the solutions in Figure 10 for two values of the friction parameter g, we can see that the nonconvex constraint (34d) holds in both cases. We emphasize that this is despite the trajectories in Figure 10 coming from the solution of Problem 35, where $| u ( t ) | < 1$ is feasible. The fact that this does not occur is the salient feature of LCvx theory, and for this problem it is guaranteed by Theorem 7. Finally, we note that Figure 10 also plots the analytical globally optimal solution obtained via the maximum principle, where no relaxation nor discretization is made. The close match between this solution and the numerical LCvx solution further confirms the theory, as well as the accuracy of the FOH discretization method. Note that the mismatch at $t = 0$ in the acceleration plot in Figure 10b is a benign single-time-step discretization artifact that is commonly observed in LCvx numerical solutions.

## PART II: SEQUENTIAL CONVEX PROGRAMMING

We now move on to a diferent kind of convex optimization-based trajectory generation algorithm, known as sequential convex programming (SCP). The reader will see that this opens up a whole world of possibilities beyond the restricted capabilities of lossless convexification. One could say that if LCvx is a surgical knife to remove acute nonconvexity, then SCP is a catch-all sledgehammer for nonconvex trajectory design [6].

![](Malyuta2021Convex_figs/ce2ec6f4fd21d64c7d0dd3b7d6948a3101c052f8872164ae7e5e9bb13042c61f.jpg)

![](Malyuta2021Convex_figs/385f7c092add0e7d772d9b060cf9aca12eda60aa561e019a01f1395fe83a408f.jpg)

![](Malyuta2021Convex_figs/f51d3295c745a7014be690eabba06b86a80af850707e95fbf494dd0da7b5e418.jpg)  
(a) Solution of Problem 35 fo $g = 0 . 1 \mathsf { m } / \mathsf { s } ^ { 2 }$ and $s = 4 7 1$ m.

![](Malyuta2021Convex_figs/06a5c2e2b7db89f9f3af145aa6f150f4870bb5cc12f684f2514ff35947a10e90.jpg)

![](Malyuta2021Convex_figs/2f5ab13208cfcd290a07bd9b2221ace15473184263d33c8ebc93800bcc0ea1a7.jpg)

![](Malyuta2021Convex_figs/20e744e25f1fe002cbdb57440ba7efa6c947f83e45c6a126e59782e3b27817bd.jpg)  
(b) Solution of Problem 35 fo $g = 0 . 6 \mathsf { m } / \mathsf { s } ^ { 2 }$ and $s = 3 0 ~ \mathsf { m } .$

FIGURE 10 LCvx solutions of Problem 35 for two scenarios. The close match of the analytic solution using the maximum principle (drawn as a continuous line) and the discretized solution using LCvx (drawn as discrete dots) confirms that LCvx finds the globally optimal solution of the problem.

A wealth of industrial and research applications, including high-profile experiments, support this statement. Examples can be found in many engineering domains, ranging from aerospace [59, 121, 122, 123] and mechan ical design [124, 125] to power grid technology [126], chemical processes [127], and computer vision [128, 129]. Just last year, the Tipping Point Partnership between NASA and Blue Origin started testing an SCP algorithm (that we will discuss in this section) aboard the New Shepard rocket [8, 68]. Another application of SCP methods is for the SpaceX Starship landing flip maneuver [130]. Although SpaceX’s methods are undiscolsed, we know that convex optimization is used by the Falcon 9 rocket and that SCP algorithms are highly capable of solving such challenging trajectories [36, 131].

Further afield, examples of SCP can be found in medicine [132, 133], economics [134, 135], biology [136, 137], and fisheries [138]. Of course, in any of these applications, SCP is not the only methodology that can be used to obtain good solutions. Others might include interior point methods [13, 139], dynamic programming [140], augmented Lagrangian techniques [141], genetic or evolutionary algorithms [142], and machine learning and neural networks [143], to name only a few. However, it is our view that SCP methods are fast, flexible and eficient local optimization algorithms for trajectory generation. They are a powerful tool to have in a trajectory engineer’s toolbox, and they will be the focus of this part of the article.

As the name suggests, at the core of SCP is the idea of iterative convex approximation. Most, if not all, SCP algorithms for trajectory generation can be cast in the form illustrated by Figure 11. Strictly speaking, SCP methods are nonlinear local optimization algorithms. In particular, the reader will recognize that SCP algorithms are specialized trust region methods for continuous-time optimal control problems [29, 47, 48].

All SCP methods solve a sequence of convex approximations, called subproblems, to the original nonconvex problem and update the approximation as new solutions are obtained. Going around the loop of Figure 11, all algorithms start with a user-supplied initial guess, which can be very coarse (more on this later). At 1 , the SCP algorithm has available a socalled reference trajectory, which may be infeasible with respect to the problem dynamics and constraints. The nonconvexities of the problem are removed by a local linearization around the reference trajectory, while convex elements are kept unchanged. Well-designed SCP algorithms add extra features to the problem in order to maintain subproblem feasibility after linearization. The resulting convex continuous-time subproblem is then temporally discretized to yield a finite-dimensional convex optimization problem. The optimal solution to the discretized subproblem is computed at 2 , where the SCP algorithm makes a call to any appropriate convex optimization solver. The solution is tested at 3 against stopping criteria. If the test passes, we say that the algorithm has converged, and the most recent solution from 2 is returned. Otherwise, the solution is used to update the trust region (and possibly other parameters) that are internal to the SCP algorithm. The solution then becomes the new reference trajectory for the next iteration of the algorithm.

The SCP approach ofers two main advantages. First, a wide range of algorithms exist to reliably solve each convex subproblem at 2 . Because SCP is agnostic to the particular choice of subproblem optimizer, well-tested algorithms can be used. This makes SCP very attractive for safety-critical applications, which are ubiquitous throughout disciplines like aerospace and automotive en gineering. Second, one can derive meaningful theoreti cal guarantees on algorithm performance and computa tional complexity, as opposed to general NLP optimiza tion where the convergence guarantees are much weaker. Taken together, these advantages have led to the devel opment of very eficient SCP algorithms with runtimes low enough to enable real-time deployment for some ap plications [63].

A fundamental dilemma of NLP optimization is that one can either compute locally optimal solutions quickly, or globally optimal solutions slowly. SCP technique are not immune to this trade-of, despite the fact that certain subclasses of convex optimization can be viewed as “easy” from a computational perspective due to the availability of interior point methods. Some of the afore mentioned applications may favor the ability to com pute solutions quickly (i.e., in near real-time), such a aerospace and power grid technologies. Others, such as economics and structural truss design, may favor global optimality and put less emphasis on solution time (al though early trade studies may still benefit from a fast optimization method). Given the motivation from the beginning of this article, our focus is on the former class of algorithms that provide locally optimal solutions in near real-time.

This part of the article will provide an overview of the algorithmic design choices and assumptions that lead to efective SCP implementations. The core tradeofs in clude how the convex approximations are formulated, what structure is devised for updating the solutions, how progress towards a solution is measured, and how all of the above enables theoretical convergence and performance guarantees.

We hope that the reader comes away with the following view of SCP: it is an efective and flexible way to do trajectory optimization, and inherits some but not all of the theoretical properties of convex optimization. SCP works well for complex problems, but it is definitely not a panacea for all of nonconvex optimization. SCP can fail to find a solution, but usually a slight change to the parameters recovers convergence. This part of the article provides the reader with all the necessary insights to get started with SCP. The numerical examples in Part III provide a practical and open-source implementation of the algorithms herein.

![](Malyuta2021Convex_figs/e1aabb595776fd43b365a209746251b5c997f31e649c6abe421abe160f6fcb7a.jpg)  
FIGURE 11 Block diagram illustration of a typical SCP algorithm. Every SCP-based trajectory generation method is comprised of three major components: a way to guess the initial trajectory (Starting), an iteration scheme which refines the trajectory until it is feasible and locally optimal (Iteration), and an exit criterion to stop once the trajectory has been computed (Stopping). In a well-designed SCP scheme, the test (convergence) criterion is guaranteed to trigger, but the solution may be infeasible for the original problem.

## Historical Development of SCP

Tracing the origins of what we refer to as sequential convex programming is not a simple task. Since the field of nonlinear programming gained traction as a popular discipline in the 1960s and 70s, many researchers have explored the solution of nonconvex optimization problems via convex approximations. This section attempts to catalogue some of the key developments, with a focus on providing insight into how the field moved toward the present day version of sequential convex programming for trajectory generation.

The idea to solve a general (nonconvex) optimization problem by iteratively approximating it as a convex program was perhaps first developed using branchand-bound techniques [144, 145, 146, 147]. Early results were of mainly academic interest, and computationally tractable methods remained elusive. One of the most important ideas that emerged from these early investigations appears to be that of McCormick relaxations [148]. These are a set of atomic rules for constructing convex/concave relaxations of a specific class of functions that everywhere under-/over-estimate the original functions. These rules result in a class of SCP methods, and algorithms based on McCormick relaxations continue to be developed with increasing computational capabilities [149, 150, 151, 152].

Diference-of-convex programming is a related class of SCP methods [153, 154]. These types of algorithms rely on the formulation of nonconvex constraints as the difference between two convex functions, say $f = f _ { 1 } - f _ { 2 }$ where both $f _ { 1 }$ and $f _ { 2 }$ are convex functions. The advantage of this decomposition is that only the function $f _ { 2 }$ needs to be linearized in order to approximate the nonconvex function $f .$ The convex-concave procedure presented in [155] is one example of a successful implementation of this idea, and it has been applied, among other places, in the field of machine learning to support vector machines and principal component analysis [156].

Perhaps the earliest and simplest class of SCP methods whose structure resembles that shown in Figure 1 is, unsurprisingly, sequential linear programming (SLP) These algorithms linearize all nonlinear functions about a current reference solution so that each subproblem i a linear program. These linear programs are then solved with a trust region to obtain a new reference, and the process is repeated. Early developments came from the petroleum industry and were intended to solve large scale problems [157, 158]. From a computational per spective, SLP was initially attractive due to the maturit of the simplex algorithm. Over time, however, solvers for more general classes of convex optimization problems have advanced to the point that restricting oneself to linear programs to save computational resources at 2 in Figure 11 has become unnecessary, except perhaps for very large-scale problems.

Another important class of SCP methods is that of sequential quadratic programming (SQP). The works of Han [159, 160], Powell [161, 162, 163], Boggs and Tolle [164, 165, 166], and Fukushima [167] appear to have exerted significant influence on the early devel opments of SQP-type algorithms, and their impact remains evident today. An excellent survey was written by Boggs and Tolle [168] and an exhaustive monograph is available by Conn, Gould, and Toint [47]. SQP methods approximate a nonconvex program with a quadratic program using some reference solution, and then use the solution to this quadratic program to update the approximation. Byrd, Schnabel, and Schultz provide a general theory for inexact SQP methods [169]. The proliferation of SQP-type algorithms can

Because SCP is agnostic to the choice of subproblem optimizer, well-tested algorithms can be used, which is attractive for safety-critical applications.

be attributed to three main aspects: 1) their similarity with the familiar class of Newton methods, 2) the fact that the initial reference need not be feasible, and 3) the existence of algorithms to quickly and reliably solve quadratic programs. In fact, the iterates obtained by SQP algorithms can be interpreted either as solutions to quadratic programs or as the application of Newton’s method to the optimality conditions of the original problem [29]. SQP algorithms are arguably the most mature class of SCP methods [170], and modern developments continue to address both theoretical and applied aspects [171, 172].

Their long history of successful deployment in NLP solvers notwithstanding [170], SQP methods do come with several drawbacks. Gill and Wong nicely summarize the dificulties that can arise when using SQP methods [173], and we will only outline the basic ideas here. Most importantly (and this goes for any “second-order” method), it is dificult to accurately and reliably estimate the Hessian of the nonconvex program’s Lagrangian. Even if this is done, say, analytically, there is no guarantee that it will be positive semidefinite, and an indefinite Hessian results in an NP-hard nonconvex quadratic program. Hessian approximation techniques must therefore be used, such as keeping only the positive semidefinite part or using the BFGS update [174]. In the latter case, additional conditions must be met to ensure that the Hessian remains positive-definite. These impose both theoretical and computational challenges which, if unaddressed, can both impede convergence and curtail the real-time applicability of an SQP-type algorithm. Fortunately, a great deal of efort has gone into making SQP algorithms highly practical, resulting in mature algorithm packages like SNOPT [170].

One truly insurmountable drawback of SQP methods for trajectory generation in particular is that quadratic programs require all constraints to be afine in the solution variable. Alas, many motion planning problems are naturally subject to non-afine convex constraints. We have already seen an example of a second-order cone constraint that arises from a spacecraft glideslope requirement in “Landing Glideslope as an Afine State Constraint”, shown in Figure 5. For problems with nonafine convex constraints, the use of an SQP algorithm may require more iterations to converge compared to a more general SCP algorithm, leading to a reduction in computational eficiency. Moreover, each SQP iterate is not guaranteed to be feasible with respect to the original convex constraints, whereas the SCP iterates will be.

There are several classes of SCP algorithms that generalize the idea of SQP in order to deal with exactly this limitation. Semidefinite programs are the most general class of convex optimization problems for which eficient of-the-shelf solvers are available. Fares et al. introduced sequential semidefinite programming [175], which uses matrix variables that are subject to definiteness con straints. Such algorithms find application most com monly in robust control, where problems are formulated as (nonconvex) semidefinite programs with linear and bilinear matrix inequalities [176]. Recent examples have appeared for robust planetary rocket landing [177, 178]. We can view sequential semidefinite programming as the furthest possible generalization of SLP to the idea of ex ploiting existing convexity in the subproblems.

This article focuses on the class of SCP methods that solve a general convex program at each iteration, with out a priori restriction to one of the previously mentioned classes of convex programs (e.g., LPs, QPs, SOCPs, and SDPs). This class of SCP methods has been developed largely over the last decade, and represents the mos active area of current development, with successful ap plications in robot and spacecraft trajectory optimiza tion [6, 53, 59, 62, 63, 121, 122, 179, 180, 181, 182]. We focus, in particular, on two specific algorithms within this class of SCP methods: SCvx and GuSTO. Thes two algorithms are complementary in a number of ways, and enjoy favorable theoretical guarantees. On the one hand, the theoretical analysis of SCvx works with the temporally discretized problem and provides guarantee in terms of the Karush-Kuhn-Tucker (KKT) optimalit conditions [49, 64, 183]. On the other hand, GuSTO is analyzed for the continuous-time problem and provide theoretical guarantees in terms of the Pontryagin maxi mum principle [11, 12, 50, 69]. The numerical examples in Part III of this article are solved using both SCvx and GuSTO exactly as they are presented here. These ex amples illustrate that the methods are, to some degree, interchangeable.

Typically, although not necessarily, the convex solver used at 2 in Figure 11 is based on an interior poin method [31, 139]. This leads to a nice interpretation of SCP as the “next layer up” in a hierarchy of optimiza tion algorithms described in [26, Chapter 11], and which we illustrate in Figure 12. In the bottommost layer, we have the unconstrained Newton’s method, which solves a sequence of unconstrained QPs. The next layer solves linear equality constrained convex problems. This again uses Newton’s method, but with a more complicated step computation. The third layer is the IPM family of meth ods, which solve a convex problem with linear equalit and convex inequality constraints as a sequence of linear equality constrained problems. Thus, we may think of IPMs as iteratively calling the algorithm in layer 2 of Figure 12. Analogously, SCP solves a nonconvex problem as a sequence of convex problems with linear equality and convex inequality constraints. Thus, SCP iteratively calls an IPM algorithm from layer 3 . Numerical expe rience has shown that for most problems, IPMs require on the order of tens of iterations (i.e., calls to layer 2 ) to converge [26]. Similarly, our experience has been that SCP requires on the order of tens of iterations (i.e., calls to layer 3 ) to converge.

![](Malyuta2021Convex_figs/c7d159195ecab24f23941fab642a89158b493591af3d5a936d01ea577442603f.jpg)  
FIGURE 12 Sequential convex programming can be placed atop a hierarchy of classical optimization algorithms. In this illustration, the “width” of each layer is representative of the corresponding algorithm’s implementation and runtime complexity (to be used only as an intuitive guide). Each layer embeds within itself the algorithms from the layers below it.

The rest of this part of the article is organized as follows. We first state the general continuous-time optimal control problem that we wish to solve, and discuss the common algorithmic underpinnings of the SCP framework. We then describe the SCvx and GuSTO algorithms in full detail. At the end of Part II, we compare SCvx and GuSTO and give some advice on using SCP in the real world. Part III will present two numerical experiments that provide practical insight and highlight the capabilities of each algorithm.

## Problem Formulation

The goal of SCP methods is to solve continuous-time optimal control problems of the following form:

$$
\min _ {u, p} J (x, u, p)\tag{39a}
$$

$$
\text { s.t. } \dot {x} (t) = f \big (t, x (t), u (t), p \big),\tag{39b}
$$

$$
\big (x (t), p \big) \in \mathcal {X} (t),\tag{39c}
$$

$$
\big (u (t), p \big) \in \mathcal {U} (t),\tag{39d}
$$

$$
s (t, x (t), u (t), p) \leq 0,\tag{39e}
$$

$$
g _ {\mathrm{ic}} (x (0), p) = 0,\tag{39f}
$$

$$
g _ {\mathrm{tc}} (x (1), p) = 0,\tag{39g}
$$

where $\boldsymbol { x } ( \cdot ) \in \mathbb { R } ^ { n }$ is the state trajectory, $u ( \cdot ) \in \mathbb { R } ^ { m }$ is the control trajectory, and $p \in \mathbb { R } ^ { d }$ is a vector of parameters. The function $f : \mathbb { R } \times \mathbb { R } ^ { n } \times \mathbb { R } ^ { m } \times \mathbb { R } ^ { d } \to \mathbb { R } ^ { n }$ represents the (nonlinear) dynamics, which are assumed to be at least once continuously diferentiable. Initial and terminal boundary conditions are enforced by using the continuously diferentiable functions $g _ { \mathrm { i c } } : \mathbb { R } ^ { n } \times \mathbb { R } ^ { d } \to \mathbb { R } ^ { n _ { i c } }$ and $g _ { \mathrm { t c } } : \mathbb { R } ^ { n } \times \mathbb { R } ^ { d }  \mathbb { R } ^ { n _ { t c } }$ . We separate convex and non convex path $( { \mathrm { i . e . } }$ , state and control) constraints by using the convex sets $\mathcal { X } ( t )$ and $\mathcal { U } ( t )$ to represent convex path constraints, and the continuously diferentiable function $s : \mathbb { R } \times \mathbb { R } ^ { n } \times \mathbb { R } ^ { m } \times \mathbb { R } ^ { d } \to \mathbb { R } ^ { n _ { s } }$ to represent nonconvex path constraints. It is assumed that the sets $\mathcal { X } ( t )$ and $\mathcal { U } ( t )$ are compact $( { \mathrm { i . e . } }$ , closed and bounded). This amounts to saying that the vehicle cannot escape to infinity or apply infinite control action, which is obviously reasonable for all practical applications. Finally, note that Problem 3 is defined on the [0, 1] time interval, and the constraints (39b)-(39e) have to hold at each time instant.

We highlight that the parameter vector p can be used, among other things, to capture free initial and/or free fi nal time problems by making $t _ { 0 }$ and $t _ { f }$ elements of $p .$ . In particular, an appropriate scaling of time can transform the [0, 1] time interval in Problem 39 into a $[ t _ { 0 } , t _ { f } ]$ interval. This allows us to restrict the problem statement to the [0, 1] time interval without loss of generality [27]. We make use of this transformation in the numerical exam ples at the end of the article.

Hybrid systems like bouncing balls, colliding objects, and bipedal robots require integer variables in their op timization models. The integer variable type, however, is missing from Problem 39. Nevertheless, methods exist to embed integer variables into the continuous-variable formulation. Among these methods are state-triggered constraints [59, 61, 62, 65, 66, 112, 184], and homotopy techniques such as the relaxed autonomously switched hybrid system and composite smooth control [6, 185, 186]. We shall therefore move forward using Problem 39 “without loss of generality”, keeping in mind that there are methods to embed integer solution variables exactl or as an arbitrarily accurate approximation [6].

We also take this opportunity to note that Problem 39 is not the most general optimal control problem that SCP methods can solve. However, it is general enough for the introductory purpose of this article, and can already cover the vast majority of trajectory optimization problems [6]. The numerical implementation attached to this article (see Figure 2) was applied to solve problems ranging from quadrotor trajectory generation to spacecraft rendezvous and docking [66, 112].

The cost function in (39a) is assumed to be of the Bolza form [187]:

$$
J (x, u, p) = \phi (x (1), p) + \int_ {0} ^ {1} \Gamma (x (t), u (t), p) \mathrm{d} t,\tag{40}
$$

where the terminal cost $\phi : \mathbb { R } ^ { n } \times \mathbb { R } ^ { d } \to \mathbb { R }$ is assumed to be a convex function and the running cost $\Gamma : \mathbb { R } ^ { n } \times$ $\mathbb { R } ^ { m } \times \mathbb { R } ^ { d } \to \mathbb { R }$ can be in general a nonconvex function. Note that convexity assumptions on $\phi$ are without loss of generality. For example, a nonconvex $\phi$ can be replaced by a linear terminal cost $\tau _ { \mathrm { f } }$ (where $\tau _ { \mathrm { f } }$ becomes an element of $p )$ , and a nonconvex terminal boundary condition is added to the definition of $g _ { \mathrm { t c } }$ in (39g):

$$
\phi (x (1), p) = \tau_ {\mathrm{f}}.\tag{41}
$$

## SCP Algorithm Foundations

All SCP methods work by solving a sequence of local convex approximations to Problem 39, which we call subproblems. As shown in Figure 11, this requires having access to an existing reference trajectory at location 1 of the figure. We will call this a reference solution, with the understanding that this trajectory need not be a feasible solution to the problem (neither for the dynamics nor for the constraints). SCP methods update this reference solution after each passage around the loop of Figure 11, with the solution obtained at $\textcircled{2}$ becoming the reference for the next iteration. This begs the question: where does the reference solution for the first iteration come from?

## Initial Trajectory Guess

A user-supplied initial trajectory guess is responsible for providing the first SCP iteration with a reference solution. Henceforth, the notation $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ shall denote a reference trajectory on the time interval [0, 1].

We will see in the following sections that the SCP algorithms that we discuss, SCvx and GuSTO, are guaranteed to converge almost regardless of the initial trajectory guess. In particular, this guess can be grossly infeasible with respect to both the dynamics (39b) and the nonconvex constraints (39e)-(39g). However, the algorithms do require the guess to be feasible with respect to the convex path constraints (39c)-(39d). Assuring this is almost always an easy task, either by manually constructing a simplistic solution that respects the convex constraints, or by projecting an infeasible guess onto the $\mathcal { X } ( t )$ and $\mathcal { U } ( t )$ sets. For reference, both strategies are implemented in our open-source code linked in Figure 2.

Numerical experience has shown that both SCvx and GuSTO are extremely adept at morphing coarse initial guesses into feasible and locally optimal trajectories. This represents a significant algorithmic benefit, since most traditional methods, like SQP and NLP, require good (or even feasible) initial guesses, which can be very hard to come by [27, 28].

To give the reader a sense for what kind of initial guess can be provided, we present an initialization method called straight-line interpolation. We have observed that this technique works well for a wide variety of problems, and we use it in the numerical examples at the end of this article. However, we stress that this is merely a rule of thumb and not a rigorously derived technique.

We begin by fixing the initial and final states $x _ { \mathrm { i c } }$ and $x _ { \mathrm { t c } }$ that represent either single-point boundary condi tions or points in a desired initial and terminal set defined by (39f) and $( \mathrm { 3 9 g } )$ . The state trajectory is then defined as a linear interpolation between the two endpoints:

$$
\bar {x} (t) = (1 - t) x _ {\mathrm{ic}} + t x _ {\mathrm{tc}}, \mathrm{for} t \in [ 0, 1 ].\tag{42}
$$

If a component of the state is a non-additive quantity, such as a unit quaternion, then linear interpolation is not the most astute choice. In such cases, we opt for the simplest alternative to linear interpolation. For uni quaternions, this would be spherical linear interpolation [188].

Whenever possible, we select the initial input trajectory based on insight from the physics of the problem. For example, for an aerial vehicle we would choose an input that opposes the pull of gravity. In the case of a rocket, the choice can be $u _ { \mathrm { i c } } ~ = ~ - m _ { \mathrm { w e t } } g _ { \mathbb { Z } }$ and $u _ { \mathrm { t c } } =$ $- m _ { \mathrm { d r y } } g _ { \mathcal { L } }$ , where $m _ { \mathrm { w e t } }$ and $m _ { \mathrm { d r y } }$ are the initial and esti mated final masses of the vehicle, and $g \tau$ is the inertial gravity vector. If the problem structure does not readily admit a physics-based choice of control input, our go-to approach is to set the input to the smallest feasible value that is compliant with (39d). The intuition is that small inputs are often associated with a small cost (39a). In any case, the initial control solution is interpolated using a similar expression to (42):

$$
\bar {u} (t) = (1 - t) u _ {\mathrm{ic}} + t u _ {\mathrm{tc}}, \mathrm{for} t \in [ 0, 1 ].\tag{43}
$$

The initial guess for $\bar { p }$ can have a significant impact on the number of SCP iterations required to obtain a solution. For example, if $\bar { p }$ represents the final time of a free final time problem that evolves on the $[ 0 , t _ { f } ]$ interval, then it is best to guess a time dilation value that is reasonable for the expected trajectory. Since parameters are inherently problem specific, however, it is unlikel that any generic rule of thumb akin to (42) and (43) will prove reliable. Fortunately, since SCP runtime is usuall on the order of a few seconds or less, the user can ex periment with diferent initial guesses for $\bar { p }$ and come up with a good initialization strategy relatively quickly.

For all but the simplest problems, the initial guess $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ constructed above is going to be (highly) infeasible with respect to the dynamics and constraints of Problem 39. Nevertheless, SCP methods like SCvx and GuSTO can, and often do, converge to usable tra jectories using such a coarse initial guess. However, this does not relieve the user entirely from choosing an initial guess that exploits the salient features of their particu lar problem. A well-chosen initial guess will (likely) have the following three benefits for the solution process:

It will reduce the number of iterations and the time required to converge. This is almost always a driving objective in the design of a trajectory optimization algorithm since fast convergence is not only a welcome feature but also a hard requirement for onboard implementation in an autonomous system;

It will encourage the converged solution to be feasible for Problem 39. As mentioned, SCP methods like SCvx and GuSTO will always converge to a trajectory, but without a guarantee that the trajectory will be feasible for the original problem. The fact that the solution often is feasible with respect to Problem 39 is a remarkable “observation” that researchers and engineers have made, and it is a driving reason for the modern interest in SCP methods. Nevertheless, an observation is not a proof, and there are limits to how bad an initial guess can be. The only rule of thumb that is always valid is that one should embed as much problem knowledge as possible in the initial guess;

A better initial guess may also improve the converged trajectory’s optimality. However, the level of optimality is usually dificult to measure, because a globally optimal solution is rarely available for the kinds of difficult trajectory problems that we are concerned with using SCP. Nevertheless, some attempts to characterize the optimality level have been made in recent years [63, 189].

## Linearization

Let us now place ourselves at location 1 in Figure 11, and imagine that the algorithm is at some iteration during the SCP solution process. The first task in the way of constructing a convex subproblem is to remove the nonconvexities of Problem 39. For this purpose, recall that the algorithm has access to the reference trajectory $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ . If we replace every nonconvexity by its first-order approximation around the reference trajectory, then we are guaranteed to generate convex subproblems. Furthermore, these are computationally inexpensive to compute relative to second-order approximations (i.e., those involving Hessian matrices). As we alluded in the previous section on SCP history, linearization of all nonconvex elements is not the only choice for SCP – it is simply a very common one, and we take it for this article. To formulate the linearized nonconvex terms, the following Jacobians must be computed (the time argument is omitted where necessary to keep the notation short):

$$
A (t) \triangleq \nabla_ {x} f (t, \bar {x} (t), \bar {u} (t), \bar {p}),\tag{44a}
$$

$$
B (t) \triangleq \nabla_ {u} f (t, \bar {x} (t), \bar {u} (t), \bar {p}),\tag{44b}
$$

$$
F (t) \triangleq \nabla_ {p} f (t, \bar {x} (t), \bar {u} (t), \bar {p}),\tag{44c}
$$

$$
r (t) \triangleq f (t, \bar {x} (t), \bar {u} (t), \bar {p}) - A \bar {x} (t) - B \bar {u} (t) - F \bar {p},
$$

$$
C (t) \triangleq \nabla_ {x} s (t, \bar {x} (t), \bar {u} (t), \bar {p}),\tag{44d}
$$

(44e)

$$
D (t) \triangleq \nabla_ {u} s (t, \bar {x} (t), \bar {u} (t), \bar {p}),\tag{44f}
$$

$$
G (t) \triangleq \nabla_ {p} s (t, \bar {x} (t), \bar {u} (t), \bar {p}),\tag{44g}
$$

$$
r ^ {\prime} (t) \triangleq s (t, \bar {x} (t), \bar {u} (t), \bar {p}) - C \bar {x} (t) - D \bar {u} (t) - G \bar {p},
$$

$$
H _ {0} \triangleq \nabla_ {x} g _ {\mathrm{ic}} (\bar {x} (0), \bar {p}),\tag{44h}
$$

$$
K _ {0} \triangleq \nabla_ {p} g _ {\mathrm{ic}} (\bar {x} (0), \bar {p}),\tag{44i}
$$

(44j)

$$
\ell_ {0} \triangleq g _ {\mathrm{ic}} (\bar {x} (0), \bar {p}) - H _ {0} \bar {x} (0) - K _ {0} \bar {p},\tag{44k}
$$

$$
H _ {\mathrm{f}} \triangleq \nabla_ {x} g _ {\mathrm{tc}} (\bar {x} (1), \bar {p}),\tag{441}
$$

$$
K _ {\mathrm{f}} \triangleq \nabla_ {p} g _ {\mathrm{tc}} (\bar {x} (1), \bar {p}),\tag{44m}
$$

$$
\ell_ {\mathrm{f}} \triangleq g _ {\mathrm{tc}} (\bar {x} (1), \bar {p}) - H _ {\mathrm{f}} \bar {x} (1) - K _ {\mathrm{f}} \bar {p}.\tag{44n}
$$

These matrices can be used to write down the firstorder Taylor series approximations for each of $f , s ,$ g<sub>ic</sub>, and $g _ { \mathrm { t c } }$ . Note that we will not linearize the cost function (40) at this point, since SCvx and GuSTO make diferent assumptions about its particular form. Convexification of the cost function will be tackled separately in later sections on SCvx and GuSTO.

Using the terms in (44), we obtain the following approximation of Problem 39 about the reference trajectory:

$$
\min _ {u, p} J (x, u, p)\tag{45a}
$$

$$
\text { s.t. } \dot {x} (t) = A (t) x (t) + B (t) u (t) + F (t) p + r (t),
$$

$$
\left(x (t), p\right) \in \mathcal {X} (t),\tag{45b}
$$

$$
\big (u (t), p \big) \in \mathcal {U} (t),\tag{45c}
$$

$$
C (t) x (t) + D (t) u (t) + G (t) p + r ^ {\prime} (t) \leq 0,\tag{45d}
$$

$$
H _ {0} x (0) + K _ {0} p + \ell_ {0} = 0,\tag{45e}
$$

(45f)

$$
H _ {\mathrm{f}} x (1) + K _ {\mathrm{f}} p + \ell_ {\mathrm{f}} = 0.\tag{45g}
$$

Problem 45 is convex in the constraints and potentially nonconvex in the cost. Note that the convex path constraints in (39c)-(39d) are kept without approximation. This is a key advantage of SCP over methods like SLP and SQP, as was discussed in the previous section on SCP history.

Because the control trajectory u( ) belongs to an infi nite-dimensional vector space of continuous-time func tions, Problem 45 cannot be implemented and solved numerically on a digital computer. To do so, we must consider a finite-dimensional representation of the con trol function u(t), which can be obtained via temporal discretization or direct collocation [27, 190]. These representations turn the original infinite-dimensional optima control problem into a finite-dimensional parameter op timization problem that can be solved on a digital com puter.

In general, and rather unsurprisingly, solutions to discretized problems are only approximately optimal and feasible with respect to the original problem. In particular, a discrete-time control signal has fewer degrees of freedom than its continuous-time counterpart. Therefore, it may lack the flexibility required to exactly match the true continuous-time optimal control signal. By adding more temporal nodes, the approximation can become arbitrarily accurate, albeit at the expense of problem size and computation time.

Another problem with discretization is that the path constraints are usually enforced only at the discrete temporal nodes, and not over the entire time horizon. This can lead to (typically mild) constraint violation between the discrete-time nodes, although some techniques exist to remedy this artifact [191, 192].

The bad news notwithstanding, there are well established discretization methods that ensure exact satisfaction of the original continuous-time nonlinear dynamics (39b). Thus, the discretized solution can still produce strictly dynamically feasible continuous-time trajectories. We refer the reader to [6, 59, 62, 190] for detailed explanations of discretization methods that ensure exact satisfaction of the continuous-time nonlinear dynamics. An introduction to the technique that we will use for the numerical examples at the end of this article is given in “Discretizing Continuous-time Optimal Control Problems”.

Our systematic linearization of all nonconvex elements has ensured that Problem 45 is convex in the constraints, which is good news. However, linearization unsurprisingly has a price. We have inadvertently introduced two artifacts that must be addressed: artificial unboundedness and artificial infeasibility.

## Artificial Unboundedness

Linear approximations are only accurate in a neighborhood around the reference solution $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ Thus, for each $t \in [ 0 , 1 ]$ , the subproblem solution must be kept “suficiently close” to the linearization point defined by the reference solution. Another reason to not deviate too far from the reference is that, in certain malicious cases, linearization can render the solution unbounded below (i.e., the convex cost (45a) can be driven to negative infinity). We refer to this phenomenon as artificial unboundedness. To mitigate this problem and to quantify the meaning of “suficiently close”, we add the following trust region constraint:

$$
\begin{array}{c} \delta x (t) = x (t) - \bar {x} (t), \\ \delta u (t) = u (t) - \bar {u} (t), \\ \delta p = p - \bar {p}, \\ \alpha_ {x} \| \delta x (t) \| _ {q} + \alpha_ {u} \| \delta u (t) \| _ {q} + \\ \alpha_ {p} \| \delta p \| _ {q} \leq \eta , \text {for} t \in [ 0, 1 ]. \end{array}\tag{46}
$$

for some choice of $q ~ \in ~ \{ 1 , 2 , 2 ^ { + } , \infty \}$ and constants $\alpha _ { x } , \alpha _ { u } , \alpha _ { p } ~ \in ~ \{ 0 , 1 \}$ We use $q \ = \ 2 ^ { + }$ to denote the ability to impose the trust region as the quadratic two-norm squared. The trust region radius η is a fixed scalar that is updated between SCP iterations (i.e., passages around the loop in Figure 11). The update rule associated with the trust region measures how well the linearization approximates the original nonconvex elements at each iterate. This informs the algorithm whether to shrink, grow, or maintain the trust region radius. SCP methods can be diferentiated by how they update the trust region, and so the trust region update will be discussed separately for SCvx and GuSTO in the following sections.

Figure 13 shows a two-dimensional toy problem that exemplifies a single iteration of an SCP convergence pro cess. In this example, the “original problem” consist of one parabolic (nonconvex) equality constraint (blue), a convex equality constraint (green), and a convex half space inequality constraint (feasible to the left of the vertical red dashed line). The original problem is ap proximated about the reference solution ¯z, resulting in the blue dash-dot equality constraint and the same con vex equality and inequality constraints. The trust region is shown as the red circle, and represents the region in which the SCP algorithm has deemed the convex approx imation to be valid. Evidently, if the new solution z de viates too much from ¯z, the linear approximation of the parabola becomes poor. Moreover, had the green equal ity constraint been removed, removal of the trust region would lead to artificial unboundedness, as the cost could be decreased indefinitely.

Clearly, there is another problem with the lineariza tion in Figure 13 – the resulting subproblem is infeasi ble. This is because the green and blue dash-dot equality constraints do not intersect inside the set defined by the trust region and the convex inequality constraint halfspace. This issue is known as artificial infeasibility.

## Artificial Infeasibility

Linearization can make the resulting subproblem infea sible. Two independent cases can arise wherein the con straints imposed in Problem 45 are inconsistent (i.e., no feasible solution exists), even though the original con straints admit a non-empty feasible set:

In the first case, the intersection of the convexified path constraints may be empty. This occurs in the example of Figure 13, where no feasible solution exists because the linearized constraints (green and blue dash-dot) do not intersect to the left of the red in equality constraint;

In the second case, the trust region may be so small that it restricts the solution variables to a part of the solution space that is outside of the feasible set. In other words, the intersection of the trust region with the (non-empty) feasible region of the convexified con straints may itself be empty. This would have been the case in Figure 13 if the green and blue dash-dot lines were to intersect outside of the red trust region circle, but to the left of the halfspace inequality (for example, if ¯z was slightly further to the right).

The occurence of either case would prevent SCP from finding a new reference solution at 2 in Figure 11. Thus, the solution loop cannot continue, and the algorithm wil

## Discretizing Continuous-time Optimal Control Problems

uppose that we have a continuous-time linear time-S <sub>varying</sub> <sub>dynamical</sub> <sub>system</sub> <sub>governed</sub> <sub>by</sub> <sub>the</sub> <sub>ordinary</sub> differential equation (45b). To temporally discretize this system, we choose a set of N temporal nodes:

$$
0 = t _ {1} <   t _ {2} <   \dots <   t _ {N} = 1,\tag{S27}
$$

which do not need to be evenly spaced. The objective of any discretization method is to represent the state trajectory $x ( \cdot ) : [ 0 , 1 ] \to \mathbb { R } ^ { n }$ at each of these temporal nodes as a function of the state, control, and parameters at the temporal nodes. Mathematically, this transforms the ODE (45b) into a linear time-varying difference equation.

There are countless ways to achieve this objective, and [190] provides a comparative study of several such methods for motion planning problems. When choosing a method, it is important to remember that not all discretizations perform equally well. Coarse discretization techniques can render a convex subproblem infeasible even if the original optimal control problem is feasible. Moreover, different discretization methods will change the sparsity properties of the resulting convex subproblem, impacting the compu tational requirements for solving each subproblem at stage 2 in Figure 11.

In practice, two methods appear to be the most appropriate for SCP-based trajectory generation: pseudospectral and interpolating polynomial methods. Pseudospectral discretization has gained popularity after its original introduction to the optimal control community by Vlassenbroeck [S3, S4]. This method approximates both the state and control

fail. As a result, even if the original problem admits a feasible solution (shown as the black square in Figure 13), either of the two aforementioned scenarios would prevent SCP from finding it. We refer to this phenomenon as artificial infeasibility.

Artificial infeasibility in sequential convex programming was recognized early in the development of SCP algorithms [158, 161]. Two equivalent strategies exist to counteract this issue. One approach adds an unconstrained, but penalized, slack variable to each linearized constraint. This variable is sometimes called a virtual control when applied to the dynamics constraint (39b), and a virtual bufer when applied to other constraints [49]. To keep our language succinct, we will use virtual control in both cases.

The second approach penalizes constraint violations by augmenting the original cost function with soft penalty terms (45a). When the same functions and weights are used as to penalize the virtual control terms, this strategy results in the same optimality conditions.

trajectories using a basis of so-called Lagrange interpolating polynomials, over a non-uniform temporal grid defined by the roots of an orthogonal polynomial [28, S5, S6, S7]. In contrast, interpolating polynomial methods only approximate the control signal. This enables the exact solution of the LTV system (45b) over each time interval, yielding an “exact” discrete-time representation [59]. Here, exact means that the continuous- and discrete-time states match at the temporal nodes. A key attribute of interpolating polynomial discretization is that upon convergence, an SCP solution satisfying the discretized dynamics (S32a) will exactly satisfy the original nonlinear differential equation (39b).

As an example, we shall now present a discretization approach from the class of interpolating polynomial methods. This method, called first-order hold (FOH) interpolation, provides a suitable balance between optimality, feasibility, and computation time. We have found it to work well for many problems [37, 59, 190].

In FOH, the control signal $u ( \cdot ) \ : \ [ 0 , 1 ] \  \ \mathbb { R } ^ { m }$ is constrained to be a continuous and piecewise affine function of time. By defining the inputs at the temporal nodes, $\{ u _ { k } \} _ { k = 1 } ^ { N }$ the continuous-time signal is obtained by linear interpolation inside each time interval $[ t _ { k } , t _ { k + 1 } ]$

$$
\begin{array}{c} u (t) = \frac {t _ {k + 1} - t}{t _ {k + 1} - t _ {k}} u _ {k} + \frac {t - t _ {k}}{t _ {k + 1} - t _ {k}} u _ {k + 1}, \\ \triangleq \sigma_ {-} (t) u _ {k} + \sigma_ {+} (t) u _ {k + 1}. \end{array}\tag{S28}
$$

(continued...)

The ultimate result of both strategies is that subproblem is guaranteed to be feasible.

Because the virtual control is a new term that we add to the problem, it follows that the converged solution must have a zero virtual control in order to be feasible and physically meaningful with respect to the original problem. If, instead, the second strategy is used and constraint violations are penalized in the cost, the con verged solution must not violate the constraints (i.e., the penalty terms should be zero). Intuitively, if the converged solution uses a non-zero virtual control or has a non-zero constraint violation penalty, then it is not a solution of the original optimal control problem.

The fact that trajectories can converge to an infeasible solution is one of the salient limitations of SCP. However, it is not unlike the drawback of any NLP optimization method, which may fail to find a solution entirely even if one exists. When SCP converges to an infeasible solution, we call it a “soft” failure, since usually only a few virtual control terms are non-zero. A soft failure

(continued...)

The dynamics (45b) can then be expressed for $t \in \left[ t _ { k } , t _ { k + 1 } \right]$ as:

$$
\begin{array}{c} \dot {x} (t) = A (t) x (t) + B (t) \sigma_ {-} (t) u _ {k} + \\ B (t) \sigma_ {+} (t) u _ {k + 1} + F (t) p + r (t), \end{array}\tag{S29}
$$

which is again an LTV system, except for the fact that the control is no longer a continuous-time function $u ( \cdot )$ , but instead it is fully determined by the two vectors $u _ { k } , u _ { k + 1 } \in \mathbb { R } ^ { m }$ A standard result from linear systems theory is that the unique solution of (S29) is given by [95]:

$$
\begin{array}{c} x (t) = \Phi (t, t _ {k}) x (t _ {k}) + \int_ {t _ {k}} ^ {t} \Phi (t, \tau) \big [ B (\tau) \sigma_ {-} (\tau) u _ {k} \\ \qquad + B (\tau) \sigma_ {+} (\tau) u _ {k + 1} + F (\tau) p + r (\tau) \big ]   \mathrm{d} \tau , \end{array}\tag{S30}
$$

where $\phi ( t , t _ { k } )$ is the state transition matrix that satisfies the following matrix differential equation:

$$
\dot {\phi} (t, t _ {k}) = A (t) \phi (t, t _ {k}), \phi (t _ {k}, t _ {k}) = I _ {n}.\tag{S31}
$$

By setting $\begin{array} { r } { t { } = \begin{array} { l } { t _ { k + 1 } } \end{array} } \end{array}$ , (S30) allows us to write a linear time-varying difference equation that updates the discretetime state $x _ { k } = x ( t _ { k } )$ to the next discrete-time state $x _ { k + 1 } =$ $x \big ( t _ { k + 1 } \big )$

$$
x _ {k + 1} = A _ {k} x _ {k} + B _ {k} ^ {-} u _ {k} + B _ {k} ^ {+} u _ {k + 1} + F _ {k} p + r _ {k},\tag{S32a}
$$

$$
A _ {k} = \Phi (t _ {k + 1}, t _ {k}),\tag{S32b}
$$

$$
B _ {k} ^ {-} = A _ {k} \int_ {t _ {k}} ^ {t _ {k + 1}} \Phi (\tau , t _ {k}) ^ {- 1} B (\tau) \sigma_ {-} (\tau) \mathrm{d} \tau ,\tag{S32c}
$$

carries important information, since the temporal nodes and constraints with non-zero virtual control hint at how and where the solution is infeasible. Usually, relatively mild tuning of the algorithm parameters or the problem definition will recover convergence to a feasible solution. In relation to the optimization literature at large, the soft failure exhibited by SCP is related to one-norm regularization, lasso regression, and basis pursuit, used to find sparse approximate solutions [26, Section 11.4.1].

The specific algorithmic choices made to address artificial unboundedness (e.g., selection of the trust region radius update rule) and artificial infeasibility (e.g., virtual control versus constraint penalization) lead to SCP algorithms with diferent characteristics. The next two sections review two such methods, SCvx and GuSTO, and highlight their design choices and algorithmic properties. To facilitate a concise presentation, we henceforth suppress the time argument t whenever possible.

## The SCvx Algorithm

In light of the above discussion, the SCvx algorithm makes the following algorithmic choices:

$$
B _ {k} ^ {+} = A _ {k} \int_ {t _ {k}} ^ {t _ {k + 1}} \Phi (\tau , t _ {k}) ^ {- 1} B (\tau) \sigma_ {+} (\tau) d \tau ,
$$

$$
F _ {k} = A _ {k} \int_ {t _ {k}} ^ {t _ {k + 1}} \Phi (\tau , t _ {k}) ^ {- 1} F (\tau) \mathrm{d} \tau ,\tag{S32d}
$$

(S32e)

$$
r _ {k} = A _ {k} \int_ {t _ {k}} ^ {t _ {k + 1}} \Phi (\tau , t _ {k}) ^ {- 1} r (\tau) \mathrm{d} \tau .\tag{S32f}
$$

In implementation, the state transition matrix, the integrals (S32c)-(S32f), and the reference trajectory’s state $\bar { x } ( \cdot )$ are computed simultaneously over each interval $[ t _ { k } , t _ { k + 1 } ]$ This procedure is explained in more detail in [190], and pseudocode can be found in [63].

Ultimately, the update equation (S32a) is used to write N 1 affine equality constraints for $k = 1 , \ldots , N - 1$ , which represent the discretized dynamic feasibility constraint on the trajectory. Equation (55b) provides an example embedding of such constraints into an optimization problem.

## REFERENCES

[S3] Jacques Vlassenbroeck. “A chebyshev polynomial method for optima control with state constraints”. In: Automatica 24.4 (1988), pp. 499–506. DOI: 10.1016/0005-1098(88)90094-5.

[S4] Jacques Vlassenbroeck and R. Van Dooren. “A Chebyshev technique for solving nonlinear optimal control problems”. In: IEEE Transactions on Automatic Control 33.4 (1988), pp. 333–340. DOI: 10.1109/9.192187.

[S5] Carl de Boor and Blair Swartz. “Collocation at Gaussian Points”. In: SIAM Journal on Numerical Analysis 10.4 (Sept. 1973), pp. 582–606. DOI: 10.1137/0710052.

[S6] Anil V. Rao. “A Survey of Numerical Methods for Optimal Control”. In: Advances in the Astronautical Sciences 135 (2010), pp. 497–528.

[S7] I. Michael Ross and Mark Karpenko. “A review of pseudospectral optimal control: From theory to flight”. In: Annual Reviews in Control 36.2 (Dec. 2012), pp. 182–197. DOI: 10.1016/j.arcontrol.2012.09.002.

The terminal and running costs in (40) are both assumed to be convex functions. We already mentioned that this is without loss of generality for the terminal cost, and the same reasoning applies for the running cost. Any nonconvex term in the cost can be ofloaded into the constraints, and an example was given in (41);

To handle artificial unboundedness, SCvx enforces (46) as a hard constraint. While several choices are possible [49, 183], this article uses $\alpha _ { x } = \alpha _ { u } = \alpha _ { p } = 1$ The trust region radius η is adjusted at each iteration by an update rule, which we discuss below;

To handle artificial infeasibility, SCvx uses virtual control terms.

Let us begin by describing how SCvx uses virtual con trol to handle artificial infeasibility. This is done by augmenting the linear approximations (45b) and (45e)-(45g) as follows:

$$
\dot {x} = A x + B u + F p + r + E \nu ,\tag{47a}
$$

$$
\nu_ {s} \geq C x + D u + G p + r ^ {\prime},\tag{47b}
$$

![](Malyuta2021Convex_figs/0b33e65a11a7494c89cee6fbda017553f43e7a0ac0612b569d21a01e36979cec.jpg)  
FIGURE 13 A two-dimensional nonconvex toy problem that exemplifies a convex subproblem obtained during an SCP iteration. In this case, the cost function $L ( z ) = - z _ { 2 }$ and level curves of the cost are shown as gray dashed lines. The blue curve represents a nonconvex equality constraint, and its linearization is shown as the blue dash-dot line. Another convex equality constraint is shown in green, and a convex inequality constraint is shown as the vertical red dashed line. The trust region is the red circle centered at the linearization point z¯, and has radius $\eta .$ The optimal solution of the original (non-approximated) problem is shown as the black square. The convex subproblem is $\tt a r -$ tificially infeasible. Without the trust region and the green constraint, it would also be artifically unbounded.

$$
0 = H _ {0} x (0) + K _ {0} p + \ell_ {0} + \nu_ {\mathrm{ic}},\tag{47c}
$$

$$
0 = H _ {\mathrm{f}} x (1) + K _ {\mathrm{f}} p + \ell_ {\mathrm{f}} + \nu_ {\mathrm{tc}}.\tag{47d}
$$

where $\nu ( \cdot ) \in \mathbb { R } ^ { n _ { \nu } } , \nu _ { s } ( \cdot ) \in \mathbb { R } ^ { n _ { s } } , \nu _ { \mathrm { i c } } \in \mathbb { R } ^ { n _ { i c } }$ , and $\nu _ { \mathrm { t c } } ~ \in$ $\mathbb { R } ^ { n _ { t c } }$ are the virtual control terms. To keep notation manageable, we will use the symbol ˆν as a shorthand for the argument list $( \nu , \nu _ { s } , \nu _ { \mathrm { i c } } , \nu _ { \mathrm { t c } } )$

The virtual control ν in (47a) can be viewed simply as another control variable that can be used to influence the state trajectory. Like the other virtual control terms, we would like ν to be zero for any converged trajectory, because it is a synthetic input that cannot be used in reality. Note that it is required that the pair $( A , E )$ in $\left( 4 7 \mathrm { a } \right)$ is controllable, which is easy to verify using any of several available controllability tests [95]. A common choice is $E = I _ { n }$ , in which case $( A , E )$ is unconditionally controllable.

The use of non-zero virtual control in the subproblem solution is discouraged by augmenting the cost function with a virtual control penalty term. Intuitively, this means that virtual control is used only when it is necessary to avoid subproblem infeasibility. To this end, we define a positive definite penalty function $P : \mathbb { R } ^ { n } \times \mathbb { R } ^ { p } $ $\mathbb { R } _ { + }$ where p is any appropriate integer. The following choice is typical in practice:

$$
P (y, z) = \| y \| _ {1} + \| z \| _ {1},\tag{48}
$$

where y and z are placeholder arguments. The cost func tion (45a) is augmented using the penalty function as follows:

$$
\begin{array}{c} J _ {\lambda} (x, u, p, \hat {\nu}) \triangleq \phi_ {\lambda} (x (1), p, \nu_ {\mathrm{ic}}, \nu_ {\mathrm{tc}}) + \\ \int_ {0} ^ {1} \Gamma_ {\lambda} (x, u, p, E \nu , \nu_ {s}) \mathrm{d} t, \quad (4 9) \\ \phi_ {\lambda} (x (1), p, \nu_ {\mathrm{ic}}, \nu_ {\mathrm{tc}}) = \phi (x (1), p) + \lambda P (0, \nu_ {\mathrm{ic}}) + \lambda P (0, \nu_ {\mathrm{tc}}), \\ \Gamma_ {\lambda} (x, u, p, E \nu , \nu_ {s}) = \Gamma (x, u, p) + \lambda P \big (E \nu , \nu_ {s} \big). \end{array}
$$

The positive weight $\lambda \in \mathbb { R } _ { + + }$ is selected by the user, and must be suficiently large. We shall make this state ment more precise later in the section on SCvx conver gence guarantees. For now, we note that in practice it is quite easy to find an appropriately large λ value by selecting a power of ten. In general, λ can be a function of time, but we rarely do this in practice.

We also point to an important notational feature of (50), where we used Eν in place of ν for the argument list of $\Gamma _ { \lambda }$ . This will help later on to highlight that the continuous-time matrix E is substituted with its discretetime version after temporal discretization (see ahead in (53)).

The continuous-time convex subproblem that is solved at each iteration of the SCvx algorithm can then be stated formally as:

$$
\min _ {u, p, \hat {\nu}} J _ {\lambda} (x, u, p, \hat {\nu})\tag{51a}
$$

$$
\mathrm{s.t.} \dot {x} = A x + B u + F p + r + E \nu ,\tag{51b}
$$

$$
(x, p) \in \mathcal {X}, \quad (u, p) \in \mathcal {U},\tag{51c}
$$

$$
C x + D u + G p + r ^ {\prime} \leq \nu_ {s},\tag{51d}
$$

$$
H _ {0} x (0) + K _ {0} p + \ell_ {0} + \nu_ {\mathrm{ic}} = 0,
$$

$$
H _ {\mathrm{f}} x (1) + K _ {\mathrm{f}} p + \ell_ {\mathrm{f}} + \nu_ {\mathrm{tc}} = 0,\tag{51e}
$$

$$
\| \delta x \| _ {q} + \| \delta u \| _ {q} + \| \delta p \| _ {q} \leq \eta .\tag{51f}
$$

(51g)

It was mentioned in the previous section that Problem 51 is not readily implementable on a computer because it is a continuous-time, and hence infinite-dimensional, optimization problem. To solve the problem numerically, a temporal discretization is applied, such as the one discussed in “Discretizing Continuous-time Optimal Control Problems”. In par ticular, we select a set of temporal nodes $t _ { k } ~ \in ~ [ 0 , 1 ]$ for $k ~ = ~ 1 , \dots , N$ and recast the subproblem as a parameter optimization problem in the (overloaded) variables $\underline { { \boldsymbol { \ b { x } } } } \equiv \{ x _ { k } \} _ { k = 1 } ^ { N } , \ : \boldsymbol { \ b { u } } = \{ u _ { k } \} _ { k = 1 } ^ { N } , \ : p , \ : \boldsymbol { \nu } = \{ \nu _ { k } \} _ { k = 1 } ^ { N - 1 }$ , $\nu _ { s } = \{ \nu _ { s , k } \} _ { k = 1 } ^ { N } , \nu _ { \mathrm { i c } } ,$ , and $\nu _ { \mathrm { t c } } .$

Depending on the details of the discretization scheme, there may be fewer decision variables than there are tem poral nodes. In particular, for simplicity we will use a zeroth-order hold (ZOH) assumption (i.e., a piecewise constant function) to discretize the dynamics virtual control $\nu ( \cdot )$ . This means that the virtual control takes the value $\nu ( t ) = \nu _ { k }$ inside each time interval $[ t _ { k } , t _ { k + 1 } )$ ), and the discretization process works like any other interpolating polynomial method from “Discretizing Continuoustime Optimal Control Problems”. Because this leaves $\nu _ { N }$ undefined, we take $\nu _ { N } = 0$ for notational convenience whenever it appears in future equations.

The continuous-time cost function (49) can be discretized using any appropriate method. Pseudospectral methods, for example, specify a numerical quadrature that must be used to discretize the integral [28]. For simplicity, we shall assume that the time grid is uniform (i.e., $t _ { k + 1 } - t _ { k } = \Delta t$ for all $k = 1 , \ldots , N - 1 )$ and that trapezoidal numerical integration is used. This allows us to write the discrete-time version of (49) as:

$$
\mathcal {L} _ {\lambda} (x, u, p, \hat {\nu}) = \phi_ {\lambda} \big (x (1), p, \nu_ {\mathrm{ic}}, \nu_ {\mathrm{tc}} \big) + \operatorname{trapz} (\Gamma_ {\lambda} ^ {N}),\tag{52}
$$

$$
\Gamma_ {\lambda , k} ^ {N} = \Gamma_ {\lambda} (x _ {k}, u _ {k}, p, E _ {k} \nu_ {k}, \nu_ {s, k}).\tag{53}
$$

where trapezoidal integration is implemented by the function trapz : $\mathbb { R } ^ { N } \to \mathbb { R }$ , defined as follows:

$$
\operatorname{trapz} (z) \triangleq \frac {\Delta t}{2} \sum_ {k = 1} ^ {N - 1} z _ {k} + z _ {k + 1}.\tag{54}
$$

We call (52) the linear augmented cost function. This name is a slight misnomer, because (52) is in fact a general nonlinear convex function. However, we use the “linear” qualifier to emphasize that the cost relates to the convex subproblem for which all nonconvexities have been linearized. In particular, the virtual control terms can be viewed as linear measurements of dynamic and nonconvex path and boundary constraint infeasibility.

Lastly, the constraints (51c), (51d), and (51g) are enforced at the discrete temporal nodes $t _ { k }$ for each $k =$ $1 , \ldots , N$ . In summary, the following discrete-time convex subproblem is solved at each SCvx iteration (i.e., location $\textcircled{2}$ in Figure 11):

$$
\min _ {x, u, p, \hat {\nu}} \mathcal {L} _ {\lambda} (x, u, p, \hat {\nu})\tag{55a}
$$

$$
\mathrm{s.t.} x _ {k + 1} = A _ {k} x _ {k} + B _ {k} u _ {k} + F _ {k} p + r _ {k} + E _ {k} \nu_ {k},\tag{55b}
$$

$$
(x _ {k}, p) \in \mathcal {X} _ {k}, (u _ {k}, p) \in \mathcal {U} _ {k},\tag{55c}
$$

$$
C _ {k} x _ {k} + D _ {k} u _ {k} + G _ {k} p + r _ {k} ^ {\prime} \leq \nu_ {s, k},\tag{55d}
$$

$$
H _ {0} x _ {1} + K _ {0} p + \ell_ {0} + \nu_ {\mathrm{ic}} = 0,\tag{55e}
$$

$$
H _ {\mathrm{f}} x _ {N} + K _ {\mathrm{f}} p + \ell_ {\mathrm{f}} + \nu_ {\mathrm{tc}} = 0,\tag{55f}
$$

$$
\| \delta x _ {k} \| _ {q} + \| \delta u _ {k} \| _ {q} + \| \delta p \| _ {q} \leq \eta .\tag{55g}
$$

We want to clarify that (55b) is written as a shorthand convenience for discretized dynamics, and is not representative of every possible discretization choice. For example, (55b) is correct if ZOH discretization is used. However, as specified in (S32a), FOH discretization would lead to the following constraint that replaces (55b):

$$
x _ {k + 1} = A _ {k} x _ {k} + B _ {k} ^ {-} u _ {k} + B _ {k} ^ {+} u _ {k + 1} + F _ {k} p + r _ {k} + E _ {k} \nu_ {k}.
$$

The most general interpolating polynomial discretiza tion fits into the following discrete-time dynamics con straint:

$$
x _ {k + 1} = A _ {k} x _ {k} + \sum_ {j = 1} ^ {N} B _ {k} ^ {j} u _ {j} + F _ {k} p + r _ {k} + E _ {k} \nu_ {k},
$$

where the $j$ superscript indexes diferent input coeficient matrices. Other discretization methods lead to yet other afine equality constraints, all of which simply replace (55b) [190]. With this in mind, we will continue to write (55b) for simplicity. Furthermore, it is implicitly understood that the constraints (55b)-(55d) and (55g) hold at each temporal node.

Because Problem 55 is a finite-dimensional convex op timization problem, it can be solved to global optimal ity using an of-the-shelf convex optimization solver [26]. We shall denote the optimal solution by $x ^ { * } = \{ x _ { k } ^ { * } \} _ { k = 1 } ^ { \bar { N } } .$ $u ^ { * } = \{ u _ { k } ^ { * } \} _ { k = 1 } ^ { N } , p ^ { * } , \nu ^ { * } = \{ \nu _ { k } ^ { * } \} _ { k = 1 } ^ { N - 1 } , \nu _ { s } ^ { * } = \{ \nu _ { s , k } ^ { * } \} _ { k = 1 } ^ { \cdots \cdots } , \nu _ { \mathrm { i c } } ^ { * } ,$ and $\nu _ { \mathrm { t c } } ^ { * }$

## SCvx Update Rule

At this point, we know how to take a nonconvex opti mal control problem like Problem 39 and: 1) convexif it to Problem 45, 2) add a trust region (46) to avoid ar tificial unboundedness, 3) add virtual control terms (47) to avoid artificial infeasibility, 4) penalize virtual control usage in the cost (49), and 5) apply discretization to obtain a finite-dimensional convex Problem 55. In fact, this gives us all of the necessary ingredients to go around the loop in Figure 11, except for one thing: how to update the trust region radius $\eta$ in (46). In general, the trust region changes after each pass around the loop. In this section, we discuss this missing ingredient.

To begin, we define a linearization accuracy metric called the defect:

$$
\delta_ {k} \triangleq x _ {k + 1} - \psi (t _ {k}, t _ {k + 1}, x _ {k}, u, p)\tag{56}
$$

for $k = 1 , \ldots , N - 1$ . The function $\psi$ is called the flow map and its role is to $\mathrm { \Delta ^ { 6 } p r o p a g a t e ^ { 3 } }$ the control input u through the continuous-time nonlinear dynamics (39b), starting at state $x _ { k }$ at time $t _ { k }$ and evolving until the next temporal grid node $t _ { k + 1 } \ [ 1 9 3 ]$ ]. It is important that the flow map is implemented in a way that is consistent with the chosen discretization scheme, as defined below.

## Definition 2

The flow map ψ in (56) is consistent with the discretization used for Problem 55, if the following equation holds for all $k = 1 , \ldots , N - 1$

$$
\psi (t _ {k}, t _ {k + 1}, \bar {x} _ {k}, \bar {u}, \bar {p}) = A _ {k} \bar {x} _ {k} + B _ {k} \bar {u} _ {k} + F _ {k} \bar {p} + r _ {k}.\tag{57}
$$

There is an intuitive way to think about the consis tency property of $\psi .$ . The reader may follow along using the illustration in Figure 14. On the one hand, $\psi ( t _ { k } , t _ { k + 1 } , \bar { x } _ { k } , \bar { u } , \bar { p } )$ maps an initial state $\bar { x } _ { k }$ through the continuous-time nonlinear dynamics (39b) to a new state $\tilde { x } _ { k + 1 }$ On the other hand, the right-hand side of (57) does the same, except that it uses the linearized and discretized dynamics and outputs a new state $\hat { x } _ { k + 1 }$ . Because the linearization is being evaluated at the reference trajectory (i.e., at the linearization point), the linearized continuous-time dynamics will yield the exact same trajectory. Thus, the only diference between the left- and right-hand sides of (57) is that the right-hand side works in discrete-time. Consistency, then, simply means that propagating the continuous-time dynamics yields the same point as performing the discrete-time update $( \mathrm { i . e . , } \tilde { x } _ { k + 1 } = \hat { x } _ { k + 1 } )$ . For every discretization method that is used to construct Problem 55, there exists a consistent flow map.

![](Malyuta2021Convex_figs/7f6c54297f2c1d681e154796ddf494ba8342875eaa836547e0e938d7e0326c78.jpg)  
FIGURE 14 Illustration of the flow map consistency property in Definition 2. When the flow map is consistent with the discretization scheme, the state $\tilde { { x } } _ { k + 1 }$ propagated through the flow map (yellow circle) and the state $\hat { x } _ { k + 1 }$ propagated through the discrete-time linearized update equation (dashed green circle) match. When the reference trajectory is not dynamically feasible, it generally deviates from the flow map trajectory, hence $\tilde { { x } } _ { k + 1 }$ = $\bar { x } _ { k + 1 }$

The reader is likely already familiar with flow maps, even if the term sounds new. Consider the following concrete examples. When using forward Euler discretization, the corresponding consistent flow map is simply:

$$
\psi (t _ {k}, t _ {k + 1}, x _ {k}, u, p) = x _ {k} + \Delta t f (t _ {k}, x _ {k}, u _ {k}, p).\tag{58}
$$

When using an interpolating polynomial discretization scheme like the one described in “Discretizing Continuous-time Optimal Control Problems”, the corresponding consistent flow map is the solution to the dynamics (39b) obtained through numerical integration. In other words, the flow map satisfies the following conditions at each time instant $t \in [ t _ { k } , t _ { k + 1 } ]$

$$
\psi (t _ {k}, t _ {k}, x _ {k}, u, p) = x _ {k},\tag{59a}
$$

$$
\dot {\psi} (t _ {k}, t, x _ {k}, u, p) = f \big (t, \psi (t _ {k}, t, x _ {k}, u, p), u, p \big).\tag{59b}
$$

As illustrated in Figure 15, the defect (56) captures the discrepancy between the next discrete-time state $x _ { k + 1 }$ and the state obtained by using the flow map starting at time $t _ { k }$ . The defect has the following interpretation: a non-zero defect indicates that the solution to the sub problem is dynamically infeasible with respect to the original nonconvex dynamics. For a dynamically fea sible subproblem solution, the flow map trajectories in Figure 15 coincide with the discrete-time states at the discrete-time nodes. This is a direct consequence of the consistency property from Definition 2. We shall see this happen for the converged solutions of the numerical ex amples presented in Part III of this article (e.g., see Fig ures 23 and 31).

![](Malyuta2021Convex_figs/f2cb54d66fbf430fcfa9b324da43c92ce40fa8dd33236c13f334e162f705a604.jpg)  
FIGURE 15 Illustration of defect calculation according to (56). The flow map computation restarts at each discrete-time node. At each temporal node, the defect is computed as the difference between the discrete solution output by Problem 55 and the corresponding flow map value.

We now know how to compute a consistent flow map and how to use it to calculate defects using (56). We will now leverage defects to update the trust region radius in SCvx. First, define a nonlinear version of (52) as follows:

$$
\mathcal {J} _ {\lambda} (x, u, p, \hat {\nu}) = \phi_ {\lambda} \big (x (1), p, g _ {\mathrm{ic}} (x (0), p), g _ {\mathrm{tc}} (x (1), p) \big) +
$$

$$
\mathsf {t r a p z} (\Gamma_ {\lambda} ^ {N}),
$$

$$
\begin{array}{r} \Gamma_ {\lambda , k} ^ {N} = \Gamma_ {\lambda} \big (x _ {k}, u _ {k}, p, \delta_ {k}, \\ \left[ s (t _ {k}, x _ {k}, u _ {k}, p) \right] ^ {+} \big). \end{array}\tag{60}
$$

(61)

where the positive-part function $[ \cdot ] ^ { + }$ returns zero when its argument is negative, and otherwise just returns the argument. A salient feature of (60) is that it evaluates the penalty function (48) based on how well the actual nonconvex constraints are satisfied. To do so, when compared to (52), $E _ { k } \nu _ { k }$ is replaced with the defect $\delta _ { k }$ measuring dynamic infeasibility, $\nu _ { s , k }$ is replaced with the actual nonconvex path constraints (39e), while $\nu _ { \mathrm { i c } }$ and $\nu _ { \mathrm { t c } }$ are replaced by the actual boundary conditions (39f) and (39g). Because evaluation of the defect and the nonconvex path and boundary constraints is a nonlinear opera tion, we call (60) the nonlinear augmented cost function.

The SCvx algorithm uses the linear augmented cost (52) and the nonlinear augmented cost (60) to, roughl speaking, measure the accuracy of the convex approximation of Problem 39 by Problem 45. Using the reference solution and the optimal solution to Problem 55, SCvx defines the following scalar metric to measure convexification accuracy:

![](Malyuta2021Convex_figs/bcc01ddcf06142ecdc1c716f2becb769d0a5da1f27c5fae8099a20c2704d9453.jpg)  
FIGURE 16 The SCvx trust region update rule. The accuracy metric ρ is defined in (62) and provides a measure of how accurately the convex subproblem given by Problem 55 describes the original Problem 39. Note that Case 1 actually rejects the solution to Problem 55 and shrinks the trust region before proceeding to the next iteration. In this case, the convex approximation is deemed so poor that it is unusable

$$
\rho \triangleq \frac {\mathcal {J} _ {\lambda} (\bar {x} , \bar {u} , \bar {p}) - \mathcal {J} _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*})}{\mathcal {J} _ {\lambda} (\bar {x} , \bar {u} , \bar {p}) - \mathcal {L} _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*} , \nu^ {*} , \nu_ {s} ^ {*})}.\tag{62}
$$

Let us carefully analyze the elements of (62). First of all, the denominator is always nonnegative because the following relation holds [49, Theorem 3.10]:

$$
\mathcal {J} _ {\lambda} (\bar {x}, \bar {u}, \bar {p}) \geq \mathcal {L} _ {\lambda} (x ^ {*}, u ^ {*}, p ^ {*}, \nu^ {*}, \nu_ {s} ^ {*}).\tag{63}
$$

The proof of (63) works by constructing a feasible subproblem solution that matches the cost $\mathcal { I } _ { \lambda } ( \bar { x } , \bar { u } , \bar { p } )$ . Begin by setting the state, input, and parameter values to the reference solution $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ We now have to choose the virtual controls that make this solution feasible for Problem 55 and that yield a matching cost (55a). The consistency property from Definition 2 ensures that this is always possible to do. In particular, choose the dynamics virtual control to match the defects, and the other virtual controls to match the constraint values at the reference solution. This represents a feasible solution of Problem 55 whose cost equals $\mathcal { I } _ { \lambda } ( \bar { x } , \bar { u } , \bar { p } )$ . The optimal cost for the subproblem cannot be worse, so the inequality (63) follows.

If the denominator of (62) is zero, it follows from the above discussion that the reference trajectory is an optimal solution of the convex subproblem. This signals that it is appropriate to terminate SCvx and to exit the loop in Figure 11. Hence, we can use the denominator of (62) as part of a stopping criterion that avoids a division by zero. The stopping criterion is discussed further in the next section.

Looking at (62) holistically, it is essentially a ratio between the actual cost improvement (the numerator) and the predicted cost improvement (the denominator), achieved during one SCvx iteration [48]:

$$
\rho = \frac {\text { actual   improvement }}{\text { predicted   improvement }}.\tag{64}
$$

In fact, the denominator can be loosely interpreted as a lower bound prediction: the algorithm “thinks” that the actual cost improves by at least that much. We can thus adopt the following intuition based on seeing Prob lem 55 as a local model of Problem 39. A small $\rho$ value indicates that the model is inaccurate because the actua cost decrease is much smaller than predicted. $\operatorname { I f } \rho$ is close to unity, the model is accurate because the actual cost decrease is similar to the prediction. If the $\rho$ value is greater than unity, the model is “conservative” because it underestimates the cost reduction. As a result, large ρ values incentivize growing the trust region because the model is trustworthy and we want to utilize more of it. On the other hand, small $\rho$ values incentivize shrinking the trust region in order to not “overstep” an inaccurate model [49].

The SCvx update rule for the trust region radius η formalizes the above intuition. Using three user-defined scalars $\rho _ { 0 } , \rho _ { 1 } , \rho _ { 2 } \in ( 0 , 1 )$ that split the real number line into four parts, the trust region radius and reference trajectory are updated at the end of each SCvx iteration according to Figure 16. The user-defined constants $\beta _ { \mathrm { s h } } , \beta _ { \mathrm { g r } } > 1$ are the trust region shrink and growth rates, respectively. Practical implemenations of SCvx also let the user define a minimum and a maximum trust region radius by using η<sub>0</sub>, $\eta _ { 1 } > 0$

The choice of the user-defined scalars $\rho _ { 0 } , \rho _ { 1 }$ , and $\rho _ { 2 }$ greatly influences the algorithm runtime. Indeed, as shown in Figure 16, when $\rho < \rho _ { 0 }$ the algorithm will ac tually outright reject the subproblem solution, and wil resolve the same problem with a smaller trust region. This begs the question: can rejection go on indefinitely? If this occurs, the algorithm will be stuck in an infinite loop. The answer is no, the metric (62) must eventuall rise above $\rho _ { 0 }$ [49, Lemma 3.11].

## SCvx Stopping Criterion

The previous sections provide a complete description of the Starting and Iteration regions in Figure 11. A crucial remaining element is how and when to exit from the “SCP loop” of the Iteration region. This is defined by a stopping criterion (also called an exit criterion), which is implemented at location 3 in Figure 11. When the stopping criterion triggers, we say that the algorithm has converged, and the final iteration’s trajectory $\{ x ^ { * } ( t ) , u ^ { * } ( t ) , p ^ { * } \} _ { 0 } ^ { 1 }$ is output.

The basic idea of the stopping criterion is to measure how diferent the new trajectory $\{ x ^ { * } ( t ) , u ^ { * } ( t ) , p ^ { * } \} _ { 0 } ^ { 1 }$ is from the reference trajectory $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ . Intuitively, if the diference is small, then the algorithm considers the trajectory not worthy of further improvement and it is appropriate to exit the SCP loop. The formal SCvx exit criterion uses the denominator of (62) (i.e, the predicted cost improvement) as the stopping criterion [49, 64, 183, 192]:

$$
\mathcal {J} _ {\lambda} (\bar {x}, \bar {u}, \bar {p}) - \mathcal {L} _ {\lambda} (x ^ {*}, u ^ {*}, p ^ {*}, \nu^ {*}, \nu_ {s} ^ {*}) \leq \varepsilon ,\tag{65}
$$

where $\varepsilon \in \mathbb { R } _ { + + }$ is a user-defined (small) threshold. For notational simplicity, we will write (65) as:

$$
\bar {\mathcal {J}} _ {\lambda} - \mathcal {L} _ {\lambda} ^ {*} \leq \varepsilon .
$$

Numerical experience has shown a control-dependent stopping criterion to sometimes lead to an unnecessarily conservative definition of convergence [62]. For example, in an application like rocket landing, common vehicle characteristics (e.g., inertia and engine specific impulse) imply that relatively large changes in control can have little efect on the state trajectory and optimality. When the cost is control dependent (which it often is), (65) may be a conservative choice that will result in more iterations without providing a more optimal solution. We may thus opt for the following simpler and less conservative stopping criterion:

$$
\| p ^ {*} - \bar {p} \| _ {\hat {q}} + \max _ {k \in \{1, \dots , N \}} \| x _ {k} ^ {*} - \bar {x} _ {k} \| _ {\hat {q}} \leq \varepsilon ,\tag{66}
$$

where $\hat { q } \in \{ 1 , 2 , 2 ^ { + } , \infty \}$ defines a norm similarly to (46). Importantly, the following correspondence holds between (65) and (66). For any ε choice in (66), there is a (generally diferent) ε choice in (65) such that: if (65) holds, then (66) holds. We call this an “implication correspondence” between stopping criteria.

SCvx guarantees that there will be an iteration for which (65) holds. By implication correspondence, this guarantee extends to (66). In general, the user can define yet another stopping criterion that is tailored to the specific trajectory problem, as long as implication correspondence holds. In fact, we do this for the numerical examples at the end of the article, where we use the following stopping criterion that combines (65) and (66):

$$
(6 6) \text { holds   or } \bar {\mathcal {J}} _ {\lambda} - \mathcal {L} _ {\lambda} ^ {*} \leq \varepsilon_ {\mathrm{r}} | \bar {\mathcal {J}} _ {\lambda} |,\tag{67}
$$

where $\varepsilon _ { \mathrm { r } } \in \mathbb { R } _ { + + }$ is a user-defined (small) threshold on the relative cost improvement. The second term in (67) allows the algorithm to terminate when relatively little progress is being made in decreasing the cost, a signal that it has achieved local optimality.

## SCvx Convergence Guarantee

The SCvx trust region update rule in Figure 16 is designed to permit a rigorous convergence analysis of the algorithm. A detailed discussion is given in [49]. To arrive at the convergence result, the proof requires the following (mild) technical condition that is common to most if not all optimization algorithms. We really do mean that the condition is “mild” because we almost never check it in practice and SCvx just works.

## Condition 8

The gradients of the equality and active inequality constraints of Problem 39 must be linearly independent for the final converged trajectory output by SCvx. This is known as a linear independence constraint qualification (LICQ) [29, Chapter 12]. 

It is also required that the weight λ in (49) is suf ficiently large. This ensures that the integral penalt term in (49) is a so-called exact penalty function. A precise condition for “large enough” is provided in [49, Theorem 3.9], and a possible strategy is outlined follow ing the theorem in that paper. However, in practice, we simply iterate over a few powers of ten until SCvx con verges with zero virtual control. An approximate range that works for most problems is $1 0 ^ { 2 }$ to $1 0 ^ { 4 }$ . Once a mag nitude is identified, it usually works well across a wide range of parameter variations for the problem.

The SCvx convergence guarantee is stated below, and is proved in [49, Theorem 3.21]. Beside Condition 8, the theorem requires a few more mild assumptions on the inequality constraints in Problem 39 and on the penal ized cost (52). We do not state them here due to their technical nature, and refer the reader to the paper. It is enough to say that, like Condition 8, these assumptions are mild enough that we rarely check them in practice.

## Theorem 8

Suppose that Condition 8 holds and the weight λ in (49) is large enough. Regardless of the initial reference trajectory provided in Figure 11, the SCvx algorithm will always converge at a superlinear rate by iteratively solv ing Problem 55. Furthermore, if the virtual controls are zero for the converged solution, then it is a stationary point of Problem 39 in the sense of having satisfied the KKT conditions. 

Theorem 8 confirms that SCvx solves the KKT con ditions of the original Problem 39. Because these are first-order necessary conditions of optimality, they are also satisfied by local maxima and saddle points. Nevertheless, because each convex subproblem is minimized by SCvx, the event of converging to a stationary point that is not a local minimum is very small.

Theorem 8 also states that the convergence rate is superlinear [29], which is to say that the distance away from the converged solution decreases superlinearly [49, Theorem 4.7]. This is better than general NLP methods, and on par with SQP methods that usually also attain at most superlinear convergence [168].

In conclusion, note that Theorem 8 is quite intuitive and confirms our basic intuition. If we are “lucky” to get a solution with zero virtual control, then it is a local minimum of the original nonconvex Problem 39. The reader will be surprised, however, at just how easy it is to be “lucky”. In most cases, it really is a simple matter of ensuring that the penalty weight λ in (49) is large enough. If the problem is feasible but SCvx is not converging or is converging with non-zero virtual control, the first thing to try is to increase λ. In more dificult cases, some nonconvex constraints may need to be reformulated as equivalent versions that play nicer with the linearization process (the free-flyer example in Part III discusses this in detail). However, let us be clear that there is no a priori hard guarantee that the converged solution will satisfy $\hat { \nu } = 0$ . In fact, since SCvx always converges, even an infeasible optimal control problem can be solved, and it will return a solution for which ˆν is non-zero.

## The GuSTO Algorithm

The GuSTO algorithm is another SCP method that can be used for trajectory generation. The reader will find that GuSTO has a familiar feel to that of SCvx. Nevertheless, the algorithm is subtly diferent from both computational and theoretical standpoints. For example, while SCvx works directly with the temporally discretized Problem 55 and derives its convergence guarantees from the KKT conditions, GuSTO performs all of its analysis in continuous-time using Pontryagin’s maximum principle [11, 12, 49, 50]. Temporal discretization is only introduced at the very end to enable numerical solutions to the problem. GuSTO applies to versions of Problem 39 where the running cost in (40) is quadratic in the control variable:

$$
\Gamma (x, u, p) = u ^ {\intercal} S (p) u + u ^ {\intercal} \ell (x, p) + g (x, p),\tag{68}
$$

where the parameter $p ,$ as before, can be used to capture free final time problems. The functions S, \`, and $g$ must all be continuously diferentiable. Furthermore, the function S must be positive semidefinite. The dynamics must be afine in the control variable:

$$
f (t, x, u, p) = f _ {0} (t, x, p) + \sum_ {i = 1} ^ {m} u _ {i} f _ {i} (t, x, p),\tag{69}
$$

where the $f _ { i } : \mathbb { R } \times \mathbb { R } ^ { n } \times \mathbb { R } ^ { d } \to \mathbb { R } ^ { n }$ are nonlinear func tions representing a decomposition of the dynamics into terms that are control-independent and terms that linearly depend on each of the control variables $u _ { i } .$ . Note that any Lagrangian mechanical system can be expressed in the control afine form, and so (69) is applicable to the vast majority of real-world vehicle trajectory generation applications [194]. Finally, the nonconvex path constraints (39e) are independent of the control terms, i.e., $s ( t , x , u , p ) = s ( t , x , p )$ . Altogether, these assumptions specialize Problem 39 to problems that are convex in the control variable.

At its core, GuSTO is an SCP trust region method just like SCvx. Thus, it has to deal with the same issues of artificial infeasibility and artificial unboundedness. To this end, the GuSTO algorithm makes the following algorithmic choices:

To handle artificial unboundedness, GuSTO aug ments the cost function with a soft penalty on the violation of (46). Because the original Problem 39 is convex in the control variables, there is no need for a trust region with respect to the control and we use $\alpha _ { u } \ = \ 0$ . In its standard form, GuSTO works with default values $\alpha _ { x } = \alpha _ { p } = 1$ . However, one can choose diferent values $\alpha _ { x } , \alpha _ { p } > 0$ without afecting the convergence guarantees;

To handle artificial infeasibility, GuSTO augments the cost function with a soft penalty on nonconvex path constraint violation. As the algorithm progresses, the penalty weight increases.

From these choices, we can already deduce that a salient feature of the GuSTO algorithm is its use of soft penalties to enforce nonconvex constraints. Recall that in SCvx, the trust region (46) is imposed exactly, and the linearized constraints are (equivalently) relaxed b using virtual control (47). By penalizing constraints, GuSTO can be analyzed in continuous-time via the classical Pontryagin maximum principle [11, 12, 50, 69]. An additional benefit of having moved the state constraints into the cost is that the virtual control term employed in the dynamics (47a) can be safely removed, since linearized dynamics are almost always controllabl [72].

Let us begin by formulating the augmented cost func tion used by the GuSTO convex subproblem at 2 in Figure 11. This involves three elements: the original cost (40), soft penalties on path constraints that involve the state, and a soft penalty on trust region violation. We will now dicuss the latter two elements.

To formulate the soft penalties, consider a continu ously diferentiable, convex, and nondecreasing penalt function $h _ { \lambda } : \mathbb { R } \to \mathbb { R } _ { + }$ that depends on a scalar weight $\lambda \ge 1 \left[ 5 0 , 7 2 \right]$ . The goal of $h _ { \lambda }$ is to penalize any positive value and to be agnostic to nonpositive values. Thus, a simple example is a quadratic rectifier:

$$
h _ {\lambda} (z) = \lambda \big ([ z ] ^ {+} \big) ^ {2},\tag{70}
$$

where higher λ values indicate higher penalization. An other example is the softplus function [195]:

$$
h _ {\lambda} (z) = \lambda \sigma^ {- 1} \log \left(1 + e ^ {\sigma z}\right),\tag{71}
$$

where $\sigma \in \mathbb { R } _ { + + }$ is a sharpness parameter. As σ grows, the softplus function becomes an increasingly accurate approximation of λ max 0, z .

We use $h _ { \lambda }$ to enforce soft penalties for violating the constraints (39c) and (39e) that involve the state and parameter. To this end, let $w : \mathbb { R } ^ { n } \times \mathbb { R } ^ { d } \to \mathbb { R } ^ { n _ { w } }$ be a convex continuously diferentiable indicator function that is nonpositive if and only if the convex state constraints in (39c) are satisfied:

$$
w (x, p) \leq 0 \Leftrightarrow (x, p) \in \mathcal {X}.
$$

Note that because is a convex set, such a function always exists. Using w, s from (39e), and $h _ { \lambda } .$ , we can lump all of the state constraints into a single soft penalty function:

$$
g _ {\mathrm{sp}} (t, x, p) \triangleq \sum_ {i = 1} ^ {n _ {w}} h _ {\lambda} \bigl (w _ {i} (t, x) \bigr) + \sum_ {i = 1} ^ {n _ {s}} h _ {\lambda} \bigl (s _ {i} (t, x, p) \bigr).\tag{72}
$$

Another term is added to the augmented cost function to handle artificial unboundedness. This term penalizes violations of the trust region constraint, and is defined in a similar fashion as (72):

$$
g _ {\mathrm{tr}} (x, p) \triangleq h _ {\lambda} \big (\| \delta x \| _ {q} + \| \delta p \| _ {q} - \eta \big),\tag{73}
$$

although we note that hard enforced versions of the trust region constraint can also be used [72].

The overall augmented cost function is obtained by combining the original cost (39a) with (72) and (73). Because the resulting function is generally nonconvex, we take this opportunity to decompose it into its convex and nonconvex parts:

$$
J _ {\lambda} (x, u, p) \triangleq \breve {J} _ {\lambda} (x, p) + \tilde {J} _ {\lambda} (x, u, p),\tag{74a}
$$

$$
\breve {J} _ {\lambda} (x, p) = \phi (x (1), p) + \int_ {0} ^ {1} g _ {\mathrm{tr}} (x, p) +
$$

$$
\sum_ {i = 1} ^ {n _ {w}} h _ {\lambda} (w _ {i} (t, x)) \mathrm{d} t,\tag{74b}
$$

$$
\tilde {J} _ {\lambda} (x, u, p) = \int_ {0} ^ {1} \Gamma (x, u, p) + \sum_ {i = 1} ^ {n _ {s}} h _ {\lambda} (s _ {i} (t, x, p)) \mathrm{d} t.\tag{74c}
$$

The terms $g _ { \mathrm { t r } } ( x , p )$ and $h _ { \lambda } ( w _ { i } ( x ) )$ in (74b) are convex functions, since they are formed by composing a convex nondecreasing function $h _ { \lambda }$ with a convex function [26]. Thus, (74b) is the convex part of the cost, while (74c) is the nonconvex part.

Our ultimate goal is to construct a convex subproblem that can be solved at location 2 in Figure 11. Thus, the nonconvex part of the cost (74c) must be convexified around the reference trajectory $\{ \bar { x } ( t ) , \bar { u } ( t ) , \bar { p } \} _ { 0 } ^ { 1 }$ . This requires the following Jacobians in addition to the initial list (44):

$$
A ^ {\Gamma} \triangleq \nabla_ {x} \Gamma (\bar {x}, \bar {u}, \bar {p}),\tag{75a}
$$

$$
B ^ {\Gamma} \triangleq \nabla_ {u} \Gamma (\bar {x}, \bar {u}, \bar {p}),\tag{75b}
$$

$$
F ^ {\Gamma} \triangleq \nabla_ {p} \Gamma (\bar {x}, \bar {u}, \bar {p}).\tag{75c}
$$

Using (44e), (44g), and (75), we can write the convex approximation of (74c):

$$
\begin{array}{l} \tilde {L} _ {\lambda} (x, u, p) = \int_ {0} ^ {1} \Gamma (\bar {x}, \bar {u}, \bar {p}) + A ^ {\mathrm{r}} \delta x + B ^ {\mathrm{r}} \delta u + F ^ {\mathrm{r}} \delta p + \\ \sum_ {i = 1} ^ {n _ {s}} h _ {\lambda} \left(s _ {i} (t, \bar {x}, \bar {p}) + C _ {i} \delta x + G _ {i} \delta p\right) \mathrm{d} t, \end{array} \tag {7}\tag{76}
$$

where $C _ { i }$ and $G _ { i }$ are the i-th rows of the Jacobians (44e) and (44g), respectively. Note that, strictly speaking, ${ \tilde { L } } _ { \lambda }$ is not a linearized version of $\tilde { J } _ { \lambda }$ because the second term in (74c) is only linearized inside the $h _ { \lambda } ( \cdot )$ function.

Replacing ${ \tilde { J } } _ { \lambda }$ in (74a) with ${ \tilde { L } } _ { \lambda }$ , we obtain a convexified augmented cost function:

$$
L _ {\lambda} (x, u, p) = \breve {J} _ {\lambda} (x, p) + \tilde {L} _ {\lambda} (x, u, p).\tag{77}
$$

To summarize the above discussion, the continuoustime convex subproblem that is solved at each iteration of the GuSTO algorithm can be stated formally as:

$$
\min _ {u, p} L _ {\lambda} (x, u, p)\tag{78a}
$$

$$
\mathrm{s.t.} \dot {x} = A x + B u + F p + r,\tag{78b}
$$

$$
(u, p) \in \mathcal {U},\tag{78c}
$$

$$
H _ {0} x (0) + K _ {0} p + \ell_ {0} = 0,\tag{78d}
$$

$$
H _ {\mathrm{f}} x (1) + K _ {\mathrm{f}} p + \ell_ {\mathrm{f}} = 0.\tag{78e}
$$

Problem 78 can be compared to the SCvx continuous time convex subproblem, given by Problem 51. Broadl speaking, the problems are quite similar. Their main dif ferences stem from how the SCvx and GuSTO algorithms handle artificial infeasibility and artificial unboundedness. In the case of SCvx, virtual control terms are intro duced and a hard trust region (51g) is imposed. In the case of GuSTO, everything is handled via soft penalties in the augmented cost. The result is that penalty terms in the cost (78a) replace the constraints (51c), (51d), and (51g).

There is another subtle diference between Problem 7 and Problem 51, which is that GuSTO does not use virtual control terms for the linearized boundary con ditions (78d) and (78e). In SCvx, these virtual con trol terms maintain subproblem feasibility when the lin earized boundary conditions define hyperplanes that do not intersect with the hard-enforced convex state path constraints in (51c). This is not a problem in GuSTO, since the convex state path constraints are only penal ized in the cost (72), and violating them for the sake of retaining feasibility is allowed. Furthermore, the lin earized dynamics (78b) are theoretically guaranteed to be almost always controllable [72]. This implies that the dynamics (78b) can always be steered between the lin earized boundary conditions (78d) and (78e) [95].

Similar to how we treated Problem 51, a temporal discretization scheme must be applied in order to numerically solve the subproblem. Discretization proceeds in the same way as for SCvx: we select a set of temporal points $t _ { k } \in [ 0 , 1 ]$ for $k = 1 , \ldots , N$ , and recast Problem 78 as a parameter optimization problem in the (overloaded) variables $x = \{ \bar { x _ { k } } \} _ { k = 1 } ^ { N } , u = \{ u _ { k } \} _ { k = 1 } ^ { N }$ , and $p .$ The same discretization choices are available as for SCvx, such as described in “Discretizing Continuous-time Optimal Control Problems”.

The integrals of the continuous-time cost function (78a) also need to be discretized. This is done in a similar fashion to the way (52) was obtained from (49) for SCvx. For simplicity, we will again assume that the time grid is uniform with step size $\Delta t$ and that trapezoidal numerical integration (54) is used. For notational convenience, by combining the integral terms in (74b) and (76), we can write (77) compactly as:

$$
L _ {\lambda} (x, u, p) = \phi (x (1), p) + \int_ {0} ^ {1} L _ {\lambda} ^ {\Gamma} (x, u, p) \mathrm{d} t,\tag{79}
$$

where the convex function $L _ { \lambda } ^ { \Gamma }$ is formed by summing the integrands of (74b) and (76). We can then compute the discrete-time version of (79), which is the GuSTO equivalent of its SCvx counterpart (52):

$$
\mathcal {L} _ {\lambda} (x, u, p) = \phi (x (1), p) + \operatorname{trapz} \left(L _ {\lambda} ^ {\Gamma , N}\right),\tag{80}
$$

$$
L _ {\lambda , k} ^ {\Gamma , N} = L _ {\lambda} ^ {\Gamma} (x _ {k}, u _ {k}, p).\tag{81}
$$

Lastly, like in SCvx, the constraint (78c) is enforced only at the discrete temporal nodes. In summary, the following discrete-time convex subproblem is solved at each GuSTO iteration (i.e., location 2 in Figure 11):

$$
\min _ {x, u, p} \mathcal {L} _ {\lambda} (x, u, p)\tag{82a}
$$

$$
\mathrm{s.t.} x _ {k + 1} = A _ {k} x _ {k} + B _ {k} u _ {k} + F _ {k} p + r _ {k},\tag{82b}
$$

$$
(u _ {k}, p) \in \mathcal {U} _ {k},\tag{82c}
$$

$$
H _ {0} x _ {1} + K _ {0} p + \ell_ {0} = 0,\tag{82d}
$$

$$
H _ {\mathrm{f}} x _ {N} + K _ {\mathrm{f}} p + \ell_ {\mathrm{f}} = 0,\tag{82e}
$$

where it is implicitly understood that the constraints (82b) and (82c) hold at each temporal node.

## GuSTO Update Rule

We are now at the same point as we were in the SCvx section: by using Problem 82 as the discrete-time convex subproblem, all of the necessary elements are available to go around the loop in Figure 11, except for how to update the trust region radius η and the penalty weight λ. Both values are generally diferent at each GuSTO iteration, and we shall now describe the method by which they are updated. The reader will find the concept to be similar to how things worked for SCvx.

First, recall that GuSTO imposes the trust region (46) as a soft constraint via the penalty function (73). This means that the trust region constraint can possible be violated. If the solution to Problem 82 violates (46), GuSTO rejects the solution and increases the penalty weight λ by a user-defined factor $\gamma _ { f a i l } > 1$ . Otherwise, if (46) holds, the algorithm proceeds by computing the fol lowing convexification accuracy metric that is analogous to (62):

$$
\rho \triangleq \frac {\left| J _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*}) - L _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*}) \right| + \Theta^ {*}}{\left| L _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*}) \right| + \int_ {0} ^ {1} \| \dot {x} ^ {*} \| _ {2} \mathrm{d} t},\tag{83}
$$

where, recalling (39b) and (78b), we have defined:

$$
\dot {x} ^ {*} \triangleq A x ^ {*} + B u ^ {*} + F p ^ {*} + r,\tag{84a}
$$

$$
\Theta^ {*} \triangleq \int_ {0} ^ {1} \| f (t, x ^ {*}, u ^ {*}, p ^ {*}) - \dot {x} ^ {*} \| _ {2} d t.\tag{84b}
$$

Equation (84a) integrates to yield the continuous-time state solution trajectory. This is done in accordance with the temporal discretization scheme, such as the one de scribed in “Discretizing Continuous-time Optimal Con trol Problems”. As a result, the value of $\varTheta ^ { \ast }$ is nothing but a measure of the total accumulated error that results from linearizing the dynamics along the subproblem’s op timal solution. In a way, $\varTheta ^ { \ast }$ is the counterpart of SCvx defects defined in (56), with the subtle diference that while defects measure the discrepancy between the linearized and nonlinear state trajectories, $\varTheta ^ { \ast }$ measures the discrepancy between the linearized and nonlinear state dynamics.

The continuous-time integrals in (83) can, in principle, be evaluated exactly (i.e., to within numerical precision) based on the discretization scheme used. In practice, we approximate them by directly numerically integrat ing the solution of Problem 82 using (for example) trapezoidal integration (54). This means that we evaluate the following approximation of (83):

$$
\rho \approx \frac {\left| \mathcal {J} _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*}) - \mathcal {L} _ {\lambda} (x ^ {*} , u ^ {*} , p ^ {*}) \right| + \Theta^ {*}}{}
$$

$$
\left| \mathcal {L} _ {\lambda} (x ^ {*}, u ^ {*}, p ^ {*}) \right| + \mathsf {t r a p z} (x ^ {*})\tag{85}
$$

$$
\Theta^ {*} \approx \mathrm{trapz} (\Delta f ^ {*}),
$$

$$
\Delta f _ {k} ^ {*} = \| f (t _ {k}, x _ {k} ^ {*}, u _ {k} ^ {*}, p ^ {*}) - \dot {x} _ {k} ^ {*} \| _ {2}, \quad \mathsf {x} _ {k} ^ {*} = \| \dot {x} _ {k} ^ {*} \| _ {2}.
$$

The nonlinear augmented cost $\mathcal { I } _ { \lambda }$ in the numerator of (85) is a temporally discretized version of (74a). In particular, combine the integrals of (74b) and (74c) to express (74a) as:

$$
J _ {\lambda} (x, u, p) = \phi (x (1), p) + \int_ {0} ^ {1} J _ {\lambda} ^ {\Gamma} (x, u, p) \mathrm{d} t,\tag{86}
$$

which allows us to compute $\mathcal { I } _ { \lambda }$ as follows:

$$
\mathcal {J} _ {\lambda} (x, u, p) = \phi (x (1), p) + \operatorname{trapz} \left(J _ {\lambda} ^ {\Gamma , N}\right),\tag{87}
$$

$$
J _ {\lambda , k} ^ {\Gamma , N} = J _ {\lambda} ^ {\Gamma} (x _ {k}, u _ {k}, p).\tag{88}
$$

Looking at (83) holistically, it can be seen as a normalized error that results from linearizing the cost and the dynamics:

$$
\rho = \frac {\mathrm{costerror+dynamicserror}}{\mathrm{normalizationterm}}.
$$

(89)

Note that as long as the solution of Problem 82 is nontrivial $( \mathrm { i . e . , } x ^ { \ast } ( t ) = 0$ for all $t \in [ 0 , 1 ]$ does not hold), the normalization term is guaranteed to be strictly positive. Thus, there is no danger of dividing by zero.

For comparison, SCvx evaluates convexification accuracy through (64), which measures accuracy as a relative error in the cost improvement prediction. This prediction is a “higher order” efect: linearization error indirectly influences cost prediction error through the optimization of Problem 55. GuSTO takes a more direct route with (89), and measures convexification accuracy directly as a normalized error that results from linearizing both the cost and the dynamics.

Looking at (89), we can adopt the following intuition about the size of $\rho .$ As for SCvx, let us view Problem 82 as a local model of Problem 39. A large $\rho$ value indicates an inaccurate model, since the linearization error is large. A small $\rho$ value indicates an accurate model, since the linearization error is relatively small compared to the normalization term. Hence, large $\rho$ values incentivize shrinking the trust region in order to not overstep the model, while small $\rho$ values incentivize growing it in order to exploit a larger region of an accurate model. Note that the opposite intuition holds for SCvx, where small $\rho$ values are associated with shrinking the trust region.

The GuSTO update rule formalizes the above intuition. Using two user-defined constants $\rho _ { 0 } , \rho _ { 1 } \in ( 0 , 1 )$ that split the real number line into three parts, the trust region radius $\eta$ and the penalty weight λ are updated at the end of each GuSTO iteration according to Figure 17. Just like in SCvx, the user-defined constants $\beta _ { \mathrm { s h } } , \beta _ { \mathrm { g r } } > 1$ are the trust region shrink and growth rates, respectively. The sizes of the trust region and the penalty weight are restricted by user-defined constants: $\eta _ { 0 }$ is the minimum trust region radius, $\eta _ { 1 }$ is the maximum trust region radius, and $\lambda _ { 0 } \geq 1$ is the minimum penalty weight. Importantly, for cases 1 and 2 in Figure 17, whenever the solution of Problem 82 is accepted, the penalty weight λ is increased by a factor $\gamma _ { f a i l }$ if any of the nonconvex state constraints in (39e) are violated. This incentivizes subsequent iterates to become feasible with respect to (39e).

In addition, GuSTO requires that η eventually shrinks to zero as the SCP iterations progress (we cover this in more detail in a later section on GuSTO convergence) [72]. However, if the trajectory is converging, then $\delta x , \delta u , \delta p  0$ and the linearizations in Problem 78 are bound to become more accurate. Hence, we expect near-zero $\rho$ values when the trajectory is converging, which means that Figure 17 will grow the trust region instead of shrinking it. A simple remedy is to apply the following exponential shrink factor following the update in Figure 17:

$$
\eta \leftarrow \mu^ {[ 1 + k - k _ {*} ] ^ {+}} \eta ,\tag{90}
$$

where $\mu \in ( 0 , 1 )$ is an exponential shrink rate and $k _ { * } \geq 1$ is the first SCP iteration where shrinking is applied. The user sets both $\mu$ and $k _ { * }$ , and in this manner can regulate how fast the trust region shrinks to zero. We view low $\mu$ values and high $k _ { * }$ values as setting the algorithm up for a longer “exploration” phase prior to tightening the trust region.

## GuSTO Stopping Criterion

To complete the description of the GuSTO algorithm, it remains to define the stopping criterion used at location $\textcircled{3}$ of Figure 11. The formal GuSTO exit criterion directly checks if the control and parameters are all al most unchanged [50, 71]:

$$
\begin{array}{l} \Big (\| \bar {p} - p ^ {*} \| _ {\hat {q}} \leq \varepsilon \text {   and   } \\ \int_ {0} ^ {1} \| u ^ {*} (t) - \bar {u} (t) \| _ {\hat {q}} \leq \varepsilon \Big) \text {   or   } \lambda > \lambda_ {\max}, \end{array}\tag{91}
$$

where $\varepsilon \in \mathbb { R } _ { + + }$ and $\hat { q } \in \{ 2 , 2 ^ { + } , \infty \}$ have the same mean ing as before in (66), and the new parameter $\lambda _ { \operatorname* { m a x } } \in \mathbb { R } _ { + + }$ is a (large) maximum penalty weight.

When (91) triggers due to $\lambda _ { \mathrm { m a x } }$ , GuSTO exits with an unconverged trajectory that violates the state and/o trust region constraints. This is equivalent to SCvx ex iting with non-zero virtual control, and indicates that the algorithm failed to solve the problem due to inherent infeasibility or numerical issues.

Computing (91) can be computationally expensive due to numerical integration of the control deviation. We can simplify the calculation by directly using the discrete-time solution. This leads to the following stopping criterion:

$$
\begin{array}{r l} & {\| p ^ {*} - \bar {p} \| _ {\hat {q}} + \mathsf {t r a p z} (\Delta u ^ {*}) \leq \varepsilon \mathrm{or} \lambda > \lambda_ {\max},} \\ & {\Delta u _ {k} ^ {*} = \| u _ {k} ^ {*} - \bar {u} _ {k} \| _ {\hat {q}}.} \end{array}\tag{92}
$$

Just as discussed for SCvx, an implication correspon dence holds between the stopping criteria (91) and (92). In practice, we follow the example of (67) and add the option for exiting when relatively little progress is being made in decreasing the cost, which can often signal local optimality sooner than (92) is satisfied:

$$
\left(9 2\right) \text { holds   or } \left| \bar {\mathcal {J}} _ {\lambda} - \mathcal {J} _ {\lambda} ^ {*} \right| \leq \varepsilon_ {\mathrm{r}} \big | \bar {\mathcal {J}} _ {\lambda} \big |,\tag{93}
$$

where, as before, $\varepsilon _ { \mathbf { r } } ~ \in ~ \mathbb { R } _ { + + }$ is a user-defined (small) threshold on the relative cost improvement. The numerical examples at the end of the article implement (93).

## GuSTO Convergence Guarantee

Each iteration of the GuSTO numerical implementation can be seen as composed of three stages. Looking at Figure 11, first the convex Problem 82 is constructed and solved with a convex optimizer at location 2 . Using the solution, the stopping criterion (93) is checked at 3 . If the test fails, the third and final stage updates the trust region radius and soft penalty weight according to Figure 17 and (90). In this context, a convergence guarantee ensures that the stopping criterion at 3 in Figure 11 eventually triggers.

![](Malyuta2021Convex_figs/348d2ecab727bfa2ddc177ac2ff56da06332d7da5d14e2cfcd1e9ec44d0cbb11.jpg)  
FIGURE 17 The GuSTO trust region update rule. The accuracy metric ρ is defined in (83) and provides a measure of how accurately the convex subproblem given by Problem 82 describes the original Problem 39. Note that Cases 3 and 4 reject the solution to Problem 82. In Case 3, this is due to the convex approximation being deemed so inaccurate that it is unusable, and the trust region is shrunk accordingly. In Case 4, this is due to the trust region constraint (46) being violated.

GuSTO is an SCP algorithm that was designed and analyzed in continuous-time using the Pontryagin maximum principle [50, 72]. Thus, the first convergence guarantee that we are able to provide assumes that the GuSTO algorithm solves the continuous-time subproblem (i.e., Problem 78) at each iteration [50, Corollary III.1], [72, Theorem 3.2].

## Theorem 9

Regardless of the initial reference trajectory provided in Figure 11, the GuSTO algorithm will always converge by iteratively solving Problem 51. Furthermore, if $\lambda \leq \lambda _ { \operatorname* { m a x } }$ (in particular, the state constraints are exactly satisfied), then the solution is a stationary point of Problem 39 in the sense of having satisfied the necessary optimality conditions of the Pontryagin maximum principle. 1

We will emphasize once again the following duality between the GuSTO and SCvx convergence guarantees. Both algorithms can converge to infeasible points of the original Problem 39. For SCvx, this corresponds to a non-zero virtual control (recall Theorem 8). For GuSTO, this corresponds to $\lambda > \lambda _ { \mathrm { m a x } }$ . The situations are completely equivalent, and correspond simply to the diferent choices made by the algorithms to impose nonconvex constraints either with virtual control (as in SCvx) or as soft cost penalties (as in GuSTO).

Theorem 9 should be viewed as the GuSTO counterpart of Theorem 8 for SCvx. Despite the similarities between the two statements, there are three important nuances about Theorem 9 that we now discuss.

The first diference concerns how the GuSTO update rule in Figure 17 and (90) play into the convergence proof. In SCvx, the update rule from Figure 16 plays a critical role in proving convergence. Thus, SCvx is an

SCP algorithm that is intimately linked to its trust region update rule. This is not the case for GuSTO, whose convergence proof does not rely on the update rule defini tion at all. The only thing assumed by Theorem 9 is that the trust region radius η eventually shrinks to zero [72]. Ensuring this is the reason for (90). Thus, GuSTO is an SCP algorithm that accepts any update rule that eventu ally shrinks to zero. Clearly, some update rules may work better than others, and the one presented in this article is simply a choice that we have implemented in practice. Another simple update rule is given in [72]. Overall, the GuSTO update rule can be viewed as a mechanism by which to accept or reject solutions based on their con vexification accuracy, and not as a function designed to facilitate formal convergence proofs.

The reason why it is necessary to shrink the trust region to zero is the second nuanced detail of Theorem 9. In nonlinear optimization literature, most claims of convergence fall into the so-called weak convergence category [29, 196]. This is a technical term which means that a subsequence among the trajectory iterates $\{ x ^ { i } ( t ) , u ^ { i } ( t ) , p ^ { i } \} _ { 0 } ^ { \bar { 1 } }$ converges. For example, the subsequence may be $i \ = \ 1 , 3 , 5 , 7 , . . . ,$ while the iterates $i = 2 , 4 , 6 , . . .$ . behave diferently. Both SCvx and GuSTO provide, at the baseline, the weak convergence guarantee. The next step is to provide a strong convergence guarantee, which ensures that the full sequence of iterates converges. For SCvx, this is possible by leveraging properties of the update rule in Figure 16. As we mentioned in the above paragraph, GuSTO is more flexible in its choice of update rule. To get a converging iterate sequence, the additiona element (90) is introduced to force all subsequences to converge to the same value. Because our analysis for SCvx has shown the strong convergence guarantee to be tied exclusively to the choice of update rule, GuSTO can likely achieve a similar guarantee with an appropriatel

designed update rule.

The third and final nuanced detail of Theorem 9 is that it assumes continuous-time subproblems (i.e., Problem 78) are solved. In reality, the discretized Problem 82 is implemented on the computer. This diference between proof and reality should ring a familiar tone to Part I on LCvx, where proofs are also given using the continuoustime Pontryagin’s maximum principle, even though the implementation is in discrete-time. If the discretization error is small, the numerically implemented GuSTO algorithm will remain in the vicinity of a convergent sequence of continuous-time subproblem solutions. Thus, given an accurate temporal discretization, Theorem 9 can be reasonably assumed to apply for the numerical GuSTO algorithm [72].

Our default choice in research has been to use an interpolating polynomial method such as described in “Discretizing Continuous-time Optimal Control Problems”. This approach has three advantages [190]: 1) the continuous-time dynamics (78b) are satisfied exactly, 2) there is a cheap way to convert the discrete-time numerical solution into a continuous-time control signal, and 3) the discretized dynamics (82b) result in a more sparse problem than alternative formulations (e.g., pseudospectral), which benefits real-time solution. With this choice, discretization introduces only two artifacts: the control signal has fewer degrees of freedom, and the objective function (82a) is of from (78a) by a discretization error. Thus, by using an interpolating polynomial discretization we can rigorously say that Problem 82 finds a “local” optimum for a problem that is “almost” Problem 78. We say “local” because the control function has fewer DoFs, and “almost” due to discretization error in the objective function. At convergence, this means that the GuSTO solution satisfies the Pontryagin maximum principle for a slightly diferent problem than Problem 39. In practice, this technical discrepancy makes little to no diference.

## Implementation Details

We have now seen a complete description of the SCvx and GuSTO algorithms. In particular, we have all the elements that are needed to go around, and to eventually exit, the SCP loop in Figure 11. In this section, we discuss two implementation details that significantly improve the performance of both algorithms. The first detail concerns the temporal discretization procedure, and the second detail is about variable scaling.

## Temporal Discretization

The core task of discretization is to convert a continuoustime LTV dynamics constraint into a discrete-time constraint. For SCvx, this means converting (51b) to (55b). For GuSTO, this means converting (78b) to (82b). In all cases, our approach is to find the equivalent discrete-time representation of the consistent flow map ψ from Definition 2. The details of this conversion depend entirely on the type of discretization. One example was given in detail for FOH, which is an interpolating polynomial method, in “Discretizing Continuous-time Optimal Con trol Problems”. This example encapsulates a core issue with many other discretization schemes, so we will work with it for concreteness.

In FOH discretization, the integrals in (S32) require the continuous-time reference trajectory x¯(t), ¯u(t), ¯p in order to evaluate the corresponding Jacobians in (44). However, the convex subproblem solution only yields a discrete-time trajectory. To obtain the continuous-time reference, we use the continuous-time input obtained di rectly from (S28) and integrate (59) in tandem with the integrals in (S32). This operation is implemented over a time interval $[ t _ { k } , t _ { k + 1 } ]$ as one big integration of a con catenated time derivative composed of (59) and all the integrands in (S32) [63]. This saves computational resources by not repeating multiple integrals, and has the numerical advantage of letting an adaptive step integra tor automatically regulate the temporal resolution of the continuous-time reference trajectory. Because the inte gration is reset at the end of each time interval, the con tinuous-time reference state trajectory is discontinuous, as illustrated in Figure 15. Further details are provided in [63, 190] and the source code of our numerical examples, which is linked in Figure 2.

In theory, discretization occurs in the forward path of the SCP loop, just before subproblem solution, as shown in Figure 11. However, by integrating (59) as described above, we can actually obtain the SCvx defects that are needed at stage 3 in Figure 11. Integrating the flow map twice, once for discretization and another time for the defects, is clearly wasteful. Hence, in practice, we implement discretization at stage 3 in Figure 11, and store the result in memory to be used at the next iteration. Note that there is no computational benefit when the flow map does not need to be integrated, such as in (58). This is the case for many discretization schemes like for ward Euler, Runge-Kutta, and pseudospectral methods. The unifying theme of these methods is that the next dis crete-time state is obtained algebraically as a function of (a subset of) the other discrete-time states, rather than through a numerical integration process.

## Variable Scaling

The convex SCP subproblems consist of the following op timization variables: the states, the inputs, the parameter vector, and possibly a number of virtual controls. The variable scaling operation uses an invertible function to transform the optimization variables into a set of new “scaled” variables. The resulting subproblems are completely equivalent, but the magnitudes of the opti mization variables are diferent [26, 29].

SCvx and GuSTO are not scale-invariant algorithms. This means that good variable scaling can significantl impact not only how quickly a locally optimal solution is found, but also the solution quality (i.e., the level of optimality it achieves). Hence, it is imperative that the reader applies good variable scaling when using SCP to solve trajectory problems. We will now present a standard variable scaling technique that we have used successfully in practice.

To motivate our scaling approach, let us review the two major efects of variable magnitude on SCP algorithms. The first efect is common throughout scientific computing and arises from the finite precision arithmetic used by modern computers [13, 29, 32, 197, 198]. When variables have very diferent magnitudes, a lot of numerical error can accumulate over the iterations of a numerical optimization algorithm [29]. Managing variables of very diferent magnitudes is a common requirement for numerical optimal control, where optimization problems describe physical processes. For example, the state may include energy (measured in Joules) and angle (measured in radians). The former might be on the order of $1 0 ^ { 6 }$ while the latter is on the order of $1 0 ^ { 0 }$ [199]. Most algorithms will struggle to navigate the resulting decision space, which is extremely elongated along the energy axis.

The second efect of diferent variable magnitudes occurs in the formulation of the trust region constraint (46). This constraint mixes all of the states, inputs, and parameters into a single sum on its left-hand side. We have long been taught not to compare apples and oranges, and yet (without scaling), this is exactly what we are doing in (46). Reusing the previous example, a trust region radius $\eta = 1$ means diferent things for an an gle state than for an energy state. It would efectively bias progress to the angle state, while allowing almost no progress in the energy state. However, if we scale the variables to nondimensionalize their values, then the components in the left-hand side of (46) become comparable and the sum is valid. Thus, variable scaling plays an important role in ensuring that the trust region radius η is “meaningful” across states, inputs, and parameters. Without variable scaling, SCP algorithms usually have a very hard time converging to feasible solutions.

We now have an understanding that variable scaling should seek to nondimensionalize the state, input, and parameter vector in order to make them comparable. Furthermore, it should bound the values to a region where finite precision arithmetic is accurate. To this end, we have used the following afine transformation with success across a broad spectrum of our trajectory optimization research:

$$
x = S _ {x} \hat {x} + c _ {x},\tag{94a}
$$

$$
u = S _ {u} \hat {u} + c _ {u},\tag{94b}
$$

$$
p = S _ {p} \hat {p} + c _ {p},\tag{94c}
$$

where $\hat { x } \in \mathbb { R } ^ { n } , \hat { u } \in \mathbb { R } ^ { m }$ , and $\hat { p } \in \mathbb { R } ^ { d }$ are the new scaled variables. The user-defined matrices and ofset vectors in (94) are chosen so that the state, input, and parameter vector are roughly bounded by a unit hypercube: $x \in$ $[ 0 , 1 ] ^ { n } , u \in [ 0 , \bar { 1 ] } ^ { m }$ , and $p \in [ 0 , 1 ] ^ { d }$ . Another advantage to using a [0, 1] interval is that box constraint lower bounds on the variables can be enforced “for free” if the low-level convex solver operates on nonnegative variables [63].

To give a concrete example of (94), suppose that the state is composed of two quantities: a position that takes values in [100, 1000] m, and a velocity that takes values in $[ - 1 0 , \dot { 1 } 0 ] \ \mathrm { m s ^ { - 1 } } .$ . We would then choose $S _ { x } = \mathrm { d i a g } ( 9 0 0 , \bar { 2 } 0 ) \in \bar { \mathbb { R } } ^ { 2 \times 2 }$ and $c _ { x } = ( 1 0 0 , - 1 0 ) \in \mathbb { R } ^ { 2 }$ Most trajectory problems have enough problem-specific information to find an appropriate scaling. When exact bounds on possible variable values are unknown, an engineering approximation is suficient.

## Discussion

The previous two sections make it clear that SCvx and GuSTO are two instances of SCP algorithms that share many practical and theoretical properties. The algorithms even share similar parameters sets, which are listed in Table 1.

From a practical point of view, SCvx can be shown to have superlinear convergence rates under some mild additional assumptions. On the other hand, the theor of GuSTO allows one to leverage additional information from dual variables to accelerate the algorithm, provid ing quadratic convergence rates. Finally, both methods can be readily extended to account for manifold-type constraints, which can be thought of as implicit, nonlin ear equality constraints, and stochastic problem settings, e.g., [50, 69, 71, 73].

Although theoretical convergence proofs of SCvx and GuSTO do rely on a set of assumptions, these assump tions are not strictly necessary for the algorithms to work well in practice. Much of our numerical experience sug gests that SCP methods can be deployed to solve diverse and challenging problem formulations that do not necessarily satisfy the theory of the past two sections. It is often the case that what works best in practice, we can not (yet) prove rigorously in theory [184]. As Renegar writes regarding convex optimization [200, p. 51], “It is one of the ironies of the IPM literature that algorithms which are more eficient in practice often have somewhat worse complexity bounds.” The same applies for SCP methods, where algorithms that work better in practice may admit weaker theoretical guarantees in the general case [201].

The reader should thus feel free to modify and adapt the methods based on the requirements of their partic ular problem. In general, we suggest adopting a mod ify-first-prove-later approach. For example, when using SCvx, we are often able to significantly speed up conver gence by entirely replacing the trust region update step with a soft trust region penalty in the cost function [59, 62, 63].

To conclude Part II, we note that SCvx, GuSTO, and related SCP methods have been used to solve a plethora of trajectory generation problems, including: reusable launch vehicles [202, 203, 204], robotic manipulators [179, 205, 206], robot motion planning [207, 208, 209], and other examples mentioned in the article’s introduction and at the beginning of Part II. All of these SCP variants and applications should inspire the reader to come up with their own SCP method that works best for their particular application.

TABLE 1 A summary of the user-selected parameters for the SCvx and GuSTO algorithms.

<table><tr><td colspan="3">Parameter dependence:</td></tr><tr><td>SCvx</td><td>N q  $\hat{q}$  P  $\lambda$ </td><td> $\eta$   $\eta_0$   $\eta_1$   $\rho_0$   $\rho_1$   $\rho_2$   $\beta_{sh}$   $\beta_{gr}$   $\varepsilon$   $\varepsilon_r$ </td></tr><tr><td>GuSTO</td><td colspan="2">N q  $\hat{q}$  P  $h_\lambda$   $\lambda_0$   $\lambda_{\max}$   $\eta$   $\eta_0$   $\eta_1$   $\rho_0$   $\rho_1$   $\beta_{sh}$   $\beta_{gr}$   $\gamma_{fail}$   $\mu$   $k_*$   $\varepsilon$   $\varepsilon_r$ </td></tr><tr><td colspan="3">Parameter key:</td></tr><tr><td>N</td><td>N</td><td>density of temporal discretization</td></tr><tr><td>q</td><td> $\{1,2,2^+, \infty\}$ </td><td>trust region norm</td></tr><tr><td> $\hat{q}$ </td><td> $\{1,2,2^+, \infty\}$ </td><td>stopping criterion norm</td></tr><tr><td>P</td><td> $\mathbb{R}^n \times \mathbb{R}^p \to \mathbb{R}_+$ </td><td>positive definite penalty function</td></tr><tr><td> $h_\lambda$ </td><td> $\mathbb{R} \to \mathbb{R}_+$ </td><td>convex nondecreasing soft penalty function</td></tr><tr><td> $\lambda$ </td><td> $\mathbb{R}_{++}$ </td><td>penalty weight</td></tr><tr><td> $\lambda_0, \lambda_{\max}$ </td><td> $\ge 1$ </td><td>min (initial) and max penalty weight</td></tr><tr><td> $\eta$ </td><td> $\mathbb{R}_{++}$ </td><td>initial trust region radius</td></tr><tr><td> $\eta_0, \eta_1$ </td><td> $\mathbb{R}_{++}$ </td><td>min and max trust region radii</td></tr><tr><td> $\rho_0, \rho_1, \rho_2$ </td><td>(0,1)</td><td>trust region update parameters</td></tr><tr><td> $\beta_{sh}, \beta_{gr}$ </td><td>&gt;1</td><td>trust region shrink and growth factors</td></tr><tr><td> $\gamma_{fail}$ </td><td> $\mathbb{R}_{++}$ </td><td>penalty weight growth factor</td></tr><tr><td> $\mu$ </td><td>(0,1)</td><td>trust region exponential shrink rate</td></tr><tr><td> $k_*$ </td><td>N</td><td>first iteration when shrinking is applied</td></tr><tr><td> $\varepsilon$ </td><td> $\mathbb{R}_{++}$ </td><td>absolute trajectory change tolerance</td></tr><tr><td> $\varepsilon_r$ </td><td> $\mathbb{R}_{++}$ </td><td>relative cost improvement tolerance</td></tr></table>

## PART III: APPLICATION EXAMPLES

Parts I and II of this article provided the theoretical background necessary to start solving nonconvex trajectory generation problems using LCvx, SCvx, and GuSTO. This final part of the article is dedicated to doing just that: providing examples of how trajectory generation problems can be solved using the three algorithms. We cover rocket landing first, followed by quadrotor flight with obtacle avoidance, and finally six degree-of-freedom flight of a robot inside a space station. The implementation code that produces the exact plots seen in this part of the article is entirely available at the link in Figure 2. We provide a CVX-like parser interface to SCvx and GuSTO, so the reader can leverage the code to begin solving their own problems.

## LCvx: 3-DoF Fuel-Optimal Rocket Landing

Rocket-powered planetary landing guidance, also known as powered descent guidance (PDG), was the orig inal motivation for the development of lossless convexification. It makes use of several LCvx results that we presented, making it a fitting first example.

Work on PDG began in the late 1960s [19], and has since been extensively studied [210]. The objective is to find a sequence of thrust commands that transfer the vehicle from a specified initial state to a desired landing site without consuming more propellant than what is available. Using optimization to compute this sequence can greatly increase the range of feasible landing sites and the precision of the final landing location [211, 212, 213].

![](Malyuta2021Convex_figs/cf36d168042f9af4cb6b10a718721c6fe45fabcab34410bdc559c242695f6dc9.jpg)  
FIGURE 18 The Masten Xombie rocket near the end of a 750 m divert maneuver. Figure reproduced with permission from [37, Fig. 1].

Lossless convexification for PDG was first introduced in [45, 84], where minimizing fuel usage was the objective. It was the first time that convex optimization was shown to be applicable to PDG. This discovery unlocked a polynomial time algorithm with guaranteed conver gence properties for generating optimal landing trajectories. The work was later expanded to handle state constraints [86, 88, 102], to solve a mininimum landing error problem [85], to include nonconvex pointing constraints [87, S1], and to handle nonlinear terms in the dynamics such as aerodynamic drag and nonlinear gravity [46].

Today, we know that SpaceX uses convex optimization for the Falcon 9 rocket landing algorithm [36]. Flight tests have also been performed using lossless convexi fication in a collaboration between NASA and Masten Space Systems [37], as shown in Figure 18.

We will now present a lossless convexification PDG example based on a mixture of original ideas from [45, 87]. Note that LCvx considers the 3-degree-of-freedom (DoF) PDG problem, where the vehicle is modeled as a point mass. This model is accurate as long as attitude can be controlled in an inner loop faster than the outer translation control loop. This is a valid assumption for many vehicles, including rockets and aircraft. The thrust vector is taken as the control input, where its direction serves as a proxy for the vehicle attitude. We begin by stating the raw minimum fuel 3-DoF PDG problem.

$$
\min _ {T _ {c}, t _ {f}} \int_ {0} ^ {t _ {f}} \| T _ {c} (t) \| _ {2} \mathrm{d} t\tag{95a}
$$

$$
\mathrm{s.t.} \dot {r} (t) = v (t),\tag{95b}
$$

$$
\dot {v} (t) = g + \frac {T _ {c} (t)}{m (t)} - \omega^ {\times} \omega^ {\times} r (t) - 2 \omega^ {\times} v (t),\tag{95c}
$$

$$
\dot {m} (t) = - \alpha \| T _ {c} (t) \| _ {2},\tag{95d}
$$

$$
\rho_ {\mathrm{min}} \leq \| T _ {c} (t) \| _ {2} \leq \rho_ {\mathrm{max}},\tag{95e}
$$

$$
T _ {c} (t) ^ {\intercal} \hat {e} _ {z} \geq \| T _ {c} (t) \| _ {2} \cos (\gamma_ {p}),\tag{95f}
$$

$$
H _ {g s} r (t) \leq h _ {g s},\tag{95g}
$$

$$
\| v (t) \| _ {2} \leq v _ {\mathrm{max}},\tag{95h}
$$

$$
m _ {d r y} \leq m (t _ {f}),\tag{95i}
$$

$$
r (0) = r _ {0}, v (0) = v _ {0}, m (0) = m _ {w e t},\tag{95j}
$$

$$
r (t _ {f}) = v (t _ {f}) = 0.\tag{95k}
$$

The vehicle translational dynamics correspond to a double integrator with variable mass, moving in a constant gravitational field, viewed in the planet’s rotating frame. In particular, $r \in \mathbb { R } ^ { 3 }$ is the position, $\boldsymbol { v } \in \mathbb { R } ^ { 3 }$ is the velocity, $\boldsymbol { g } \in \mathbb { R } ^ { 3 }$ is the gravitational acceleration, and ω $\in \mathbb { R } ^ { 3 }$ is the planet’s constant angular velocity. The notation $\omega ^ { \times }$ denotes the skew-symmetric matrix representation of the cross product $\omega \times ( \cdot )$ . The mass $m \in$ R is depleted by the rocket engine according to (95d) with the fuel consumption rate

$$
\alpha \triangleq \frac {1}{I _ {s p} g _ {e}},\tag{96}
$$

where $g _ { e } \approx 9 . 8 0 7$ m $\mathrm { s } ^ { - 2 }$ is the Earth’s standard grav itational acceleration and $I _ { s p }$ s is the rocket engine’s specific impulse. As illustrated in Figure 19, $T _ { c } \in \mathbb { R } ^ { 3 }$ is the rocket engine thrust vector, which is upper and lower bounded via (95e). The lower bound was motivated in “Convex Relaxation of an Input Lower Bound”. The thrust vector, and therefore the vehicle attitude, also has a tilt angle constraint (95f) which prevents the vehicle from deviating by more than angle $\gamma _ { p }$ away from the vertical. Following the discussion in “Landing Glideslope as an Afine State Constraint”, we also impose an afine glideslope constraint via (95g) with a maximum glideslope angle $\gamma _ { g s }$ . The velocity is constrained to a maximum magnitude $v _ { \mathrm { m a x } }$ by (95h). The final mass must be greater than $m _ { d r y }$ (95i), which ensures that no more fuel is consumed than what is available. Constraints (95j) and (95k) impose fixed boundary conditions on the rocket’s state. In particular, the starting mass is $m _ { w e t } > m _ { d r y } .$

To begin the lossless convexification process, the standard input slack variable $\sigma \in \mathbb { R }$ from “Convex Relaxation of an Input Lower Bound” is introduced in order to remove the nonconvex lower bound in (95e). As a consequence, the familiar LCvx equality constraint appears in (97f). Following “Convex Relaxation of an Input Pointing Constraint”, this also replaces $\| T _ { c } ( t ) \| _ { 2 }$ in (95f) with σ(t) in (97g).

$$
\min _ {\sigma , T _ {c}, t _ {f}} \int_ {0} ^ {t _ {f}} \sigma (t) \mathrm{d} t\tag{97a}
$$

$$
\mathrm{s.t.} \dot {r} (t) = v (t),\tag{97b}
$$

$$
\dot {v} (t) = g + \frac {T _ {c} (t)}{m (t)} - \omega^ {\times} \omega^ {\times} r (t) - 2 \omega^ {\times} v (t),\tag{97c}
$$

$$
\dot {m} (t) = - \alpha \sigma (t),\tag{97d}
$$

$$
\rho_ {\mathrm{min}} \leq \sigma (t) \leq \rho_ {\mathrm{max}},\tag{97e}
$$

$$
\left\| T _ {c} (t) \right\| _ {2} \leq \sigma (t),\tag{97f}
$$

$$
T _ {c} (t) ^ {\intercal} \hat {e} _ {z} \geq \sigma (t) \cos (\gamma_ {p}),
$$

$$
H _ {g s} r (t) \leq h _ {g s},\tag{97g}
$$

(97h)

$$
\| v (t) \| _ {2} \leq v _ {\mathrm{max}},\tag{97i}
$$

$$
m _ {d r y} \leq m (t _ {f}),\tag{97j}
$$

$$
r (0) = r _ {0}, v (0) = v _ {0}, m (0) = m _ {w e t},\tag{97k}
$$

$$
r (t _ {f}) = v (t _ {f}) = 0.\tag{971}
$$

Next, we approximate the nonlinearity $T _ { c } / m$ in (97c). To this end, [45] showed that the following change of variables can be made:

$$
\xi \triangleq \frac {\sigma}{m}, u \triangleq \frac {T _ {c}}{m}, z \triangleq \ln (m).\tag{98}
$$

Using the new variables, note that

$$
\frac {\dot {m} (t)}{m (t)} = - \alpha \xi (t) \Rightarrow z (t) = z (0) - \alpha \int_ {0} ^ {t} \xi (\tau) \mathrm{d} \tau .\tag{99}
$$

Since the cost in (97a) maximizes $m ( t _ { f } )$ , and since $\alpha > 0$ , an equivalent cost is to minimize $\int _ { 0 } ^ { t _ { f } } \xi ( t ) \mathrm { d } t$ . It turns out that the new variables linearize all constraints except for the upper bound part of (97e). In the new variables, (97e) becomes:

$$
\rho_ {\mathrm{min}} e ^ {- z (t)} \leq \xi (t) \leq \rho_ {\mathrm{max}} e ^ {- z (t)}.\tag{100}
$$

To keep the optimization problem an SOCP, it is desirable to also do something about the lower bound in (100), which is a convex exponential cone. In [45], it was shown that the following Taylor series approxima tion is accurate to within a few percent, and is therefore acceptable:

$$
\mu_ {\min} (t) \left[ 1 - \delta z (t) + \frac {1}{2} \delta z (t) ^ {2} \right] \leq \xi (t),\tag{101a}
$$

$$
\mu_ {\mathrm{max}} (t) \big [ 1 - \delta z (t) \big ] \geq \xi (t),\tag{101b}
$$

where:

$$
\mu_ {\mathrm{min}} (t) = \rho_ {\mathrm{min}} e ^ {- z _ {0} (t)},\tag{102a}
$$

$$
\mu_ {\mathrm{max}} (t) = \rho_ {\mathrm{max}} e ^ {- z _ {0} (t)},\tag{102b}
$$

![](Malyuta2021Convex_figs/fea59469c1806ed3a30bb03d56868c7a0cd2e230786ddc8b0d2062d22586821f.jpg)  
FIGURE 19 Illustration of the 3-DoF PDG problem, showing some of the relevant constraints on the rocket-powered lander’s trajectory. The thrust direction $T _ { c } ( t ) / \| T _ { c } ( t ) \| _ { 2 }$ servers as a proxy for vehicle attitude.

$$
\delta z (t) = z (t) - z _ {0} (t),\tag{102c}
$$

$$
z _ {0} (t) = \ln (m _ {w e t} - \alpha \rho_ {\mathrm{max}} t).\tag{102d}
$$

The reference profile $z _ { 0 } ( \cdot )$ corresponds to the maxi mum fuel rate, thus $z _ { 0 } ( t )$ lower bounds $z ( t )$ . To ensure that physical bounds on $z ( t )$ are not violated, the following extra constraint is imposed:

$$
z _ {0} (t) \leq z (t) \leq \ln (m _ {w e t} - \alpha \rho_ {\min} t).\tag{103}
$$

The constraints (101) and (103) together approximate (100) and have the important property of being conservative with respect to the original constraint [45, Lemma 2]. Thus, using this approximation will not generate solutions that are infeasible for the original problem. We can now write the finalized convex relaxation of Problem 95.

$$
\min _ {\xi , u, t _ {f}} \int_ {0} ^ {t _ {f}} \xi (t) \mathrm{d} t\tag{104a}
$$

$$
\text { s.t. } \dot {r} (t) = v (t),\tag{104b}
$$

$$
\dot {v} (t) = g + u (t) - \omega^ {\times} \omega^ {\times} r (t) - 2 \omega^ {\times} v (t),\tag{104c}
$$

$$
\dot {z} (t) = - \alpha \xi (t),\tag{104d}
$$

$$
\mu_ {\min} (t) \left[ 1 - \delta z (t) + \frac {1}{2} \delta z (t) ^ {2} \right] \leq \xi (t),\tag{104e}
$$

$$
\mu_ {\max} (t) \big [ 1 - \delta z (t) \big ] \geq \xi (t),
$$

$$
\| u (t) \| _ {2} \leq \xi (t),\tag{104f}
$$

(104g)

$$
u (t) ^ {\top} \hat {e} _ {z} \geq \xi (t) \cos (\gamma_ {p}),\tag{104h}
$$

$$
H _ {g s} r (t) \leq h _ {g s},\tag{104i}
$$

$$
\| v (t) \| _ {2} \leq v _ {\mathrm{max}},\tag{104j}
$$

$$
\ln (m _ {d r y}) \leq z (t _ {f}),\tag{104k}
$$

$$
z _ {0} (t) \leq z (t) \leq \ln (m _ {w e t} - \alpha \rho_ {\mathrm{min}} t),
$$

$$
r (0) = r _ {0}, v (0) = v _ {0}, z (0) = \ln (m _ {w e t}),\tag{1041}
$$

$$
r (t _ {f}) = v (t _ {f}) = 0.\tag{104m}
$$

(104n)

Several conditions must now be checked to ascertain lossless convexification, i.e., that the solution of Prob lem 104 is globally optimal for Problem 95. To begin, let us view z in (104d) as a “fictitious” state that is used for concise notation. In practice, we know explicitly that $z ( t ) = \ln ( m _ { w e t } ) - \alpha \bar { \int _ { 0 } ^ { t } \xi ( t ) \mathrm { d } t }$ and thus we can replace every instance of $z ( t )$ in (104e)-(104l) with this expression. Thus, we do not consider z as part of the state and, furthermore, (104e), (104f), (104k), and (104l) are input and not state constraints. Defining the state as $x = ( r , v ) \in \mathbb { R } ^ { 6 }$ , the state-space matrices are

$$
A = \left[ \begin{array}{c c} 0 & I _ {3} \\ - \omega^ {\times} \omega^ {\times} & - 2 \omega^ {\times} \end{array} \right], B = \left[ \begin{array}{c} 0 \\ I _ {3} \end{array} \right], E = B.\tag{105}
$$

The pair A, B is unconditionally controllable and therefore Condition 1 is satisfied. We also need to verify Condition 3 due to the presence of the pointing constraint (104h). In this case $\hat { n } _ { u } = \hat { e } _ { z }$ and $\begin{array} { r l } { N = \lceil \hat { e } _ { x }  } & { { } \hat { e } _ { y } \rceil } \end{array}$ Condition 3 holds as long as $\boldsymbol { \omega } ^ { \times } \hat { e } _ { z } \neq 0$ , which means that the planet does not rotate about the local vertical of the landing frame.

![](Malyuta2021Convex_figs/b58e24359562cb2c465b43d79d4fcad46314a58f942fe570018341300dbb3bff.jpg)  
FIGURE 20 A force balance in the normal direction $\hat { n } _ { g s }$ can be used to guarantee that the glideslope constraint can only be activated instantaneously.

The glideslope constraint (104i) can be treated either via Condition 5 or by checking that it can only be instantaneously active. In this case, we can prove the latter by considering a force balance in the glideslope plane’s normal direction $\hat { n } _ { g s } .$ , as illustrated in Figure 20. We also invoke the fact that the optimal thrust profile for the rocket landing problem is bang-bang [45]. This allows to distill the verification down to a conservative condition that the following inequalities hold for all $\begin{array} { r } { \theta \in [ \frac { \pi } { 2 } - \gamma _ { p } - \gamma _ { g s } , \frac { \pi } { 2 } + \gamma _ { p } - \gamma _ { g s } ] \mathrm { . } } \end{array}$

$$
\rho_ {\mathrm{min}} \cos (\theta) <   m _ {d r y} \| g \| _ {2} \sin (\gamma_ {g s}),\tag{106a}
$$

$$
\rho_ {\max} \cos (\theta) > m _ {w e t} \| g \| _ {2} \sin (\gamma_ {g s}).\tag{106b}
$$

It turns out that for the problem parameters (108) of this example, the above inequalities hold. Therefore (104i) can only be instantaneously active and does not pose a threat to lossless convexification.

We also need to check Condition 2, which relates to the transversality condition of the maximum principle [11, 12, 187]. In the case of Problem 104, we have $m [ t _ { f } ] = 0$ and $b [ t _ { f } ] = x ( t _ { f } )$ , hence

$$
m _ {\text { LCvx }} = \left[ \begin{array}{c} 0 \in \mathbb {R} ^ {6} \\ \xi (t _ {f}) \end{array} \right], B _ {\text { LCvx }} = \left[ \begin{array}{c} I _ {6} \\ 0 \end{array} \right].\tag{107}
$$

Hence, as long as $\xi ( t _ { f } ) > 0$ , Condition 2 holds. Since $\xi ( t _ { f } ) ~ > ~ 0$ is guaranteed by the fact that the lower bound in (101) is greater than the exact lower bound $\rho _ { \mathrm { m i n } } e ^ { - z ( t _ { f } ) } > 0$ [45, Lemma 2], Condition 2 holds.

The remaining constraint to be checked is the maximum velocity bound (104j). Although it can be written as the quadratic constraint $v _ { \operatorname* { m a x } } ^ { - 2 } v ( t ) ^ { \top } v ( t ) \leq 1$ , the dynamics (104b)-(104c) do not match the form (18b)- (18c) required by the LCvx result for quadratic state constraints. Thus, we must resort to the more restricted statement for general state constraints in Theorem 5. According to Theorem 5, we conclude that lossless convexification will hold as long as the maximum velocity bound (104j) is activated at most a discrete number of times. In summary, we can conclude that the solution of Problem 104 is guaranteed to be globally optimal for Problem 95 as long as (104j) is never persistently active.

We now present a trajectory result obtained by solving Problem 104 using a ZOH discretized input signal with a $\Delta t = 1$ s time step (see “Discretizing Continuoustime Optimal Control Problems”). We use the following numerical parameters:

$$
g = - 3. 7 1 \hat {e} _ {z} \mathrm{ms} ^ {- 2}, m _ {d r y} = 1 5 0 5 \mathrm{kg},\tag{108a}
$$

$$
m _ {w e t} = 1 9 0 5 \mathrm{kg}, I _ {s p} = 2 2 5 \mathrm{s},\tag{108b}
$$

$$
\omega = (3. 5 \hat {e} _ {x} + 2 \hat {e} _ {z}) \cdot 1 0 ^ {- 3} \mathrm {\degrees} ^ {- 1},\tag{108c}
$$

$$
\rho_ {\mathrm{min}} = 4. 9 7 1 \mathrm{kN}, \rho_ {\mathrm{max}} = 1 3. 2 5 8 \mathrm{kN},\tag{108d}
$$

$$
\gamma_ {g s} = 8 6 ^ {\circ}, \gamma_ {p} = 4 0 ^ {\circ}, v _ {\mathrm{max}} = 5 0 0 \mathrm{km} \mathrm{h} ^ {- 1},
$$

$$
r _ {0} = 2 \hat {e} _ {x} + 1. 5 \hat {e} _ {z} \mathrm{km},\tag{108e}
$$

(108f)

$$
v _ {0} = 2 8 8 \hat {e} _ {x} + 1 0 8 \hat {e} _ {y} - 2 7 0 \hat {e} _ {z} \mathrm{km} \mathrm{h} ^ {- 1}.\tag{108g}
$$

Golden search [48] is used to find the optimal time of flight $t _ { f }$ . This is a valid choice because the cost function is unimodal with respect to $t _ { f } ~ [ 8 5 ]$ . For the problem parameters in (108), an optimal rocket landing trajectory is found with a minimum fuel time of flight $t _ { f } ^ { \ast } = 7 5 \ \mathrm { s } .$

Figure 21 visualizes the computed optimal landing tra jectory. From Figure 21(a), we can clearly see that the glide slope constraint is not only satisfied, it is also ac tivated only twice (once mid-flight and another time at touchdown), as required by the LCvx guarantee. From Figure 21(c), we can see that the velocity constraint is never activated. Hence, in this case, it does not pose a threat to lossless convexification. Several other in teresting views of the optimal trajectory are plotted in Figure $2 1 ( \mathrm { d } ) \mathrm { - } ( \mathrm { g } )$ . In all cases, the state and input constraints of Problem 95 hold. The fact that Problem 104 is a lossless convexification of Problem 95 is most evident during the minimum-thrust segment from about 40 to 70 seconds in Figure 21(f). Here, it is important realize that $\| T _ { c } ( t ) \| _ { 2 } < \rho _ { \mathrm { m i n } }$ is feasible for the relaxed problem. The fact that this never occurs is a consequence of the lossless convexification guarantee that (104g) holds with equality.

In conclusion, we emphasize that the rocket landing trajectory presented in Figure 21 is not just a feasible so lution, nor even a locally optimal one, but it is a globally optimal solution to this rocket landing problem. This means that one can do no better given these parameters and problem description.

## SCP: Quadrotor Obstacle Avoidance

We now move on to trajectory generation for problems which cannot be handled by LCvx. The objective of this first example is to compute a trajectory for a quadrotor that flies from one point to another through an obstaclefilled flight space. This example is sourced primaril from [52], and a practical demonstration is shown in Figure 22.

The quadrotor is modeled as a point mass, which is a reasonable approximation for small and agile quadrotors whose rotational states evolve over much shorter time scales than the translational states [45]. We express the equations of motion in an East-North-Up (ENU) inertial coordinate system, and take the state vector to be the position and velocity. Using a simple double-integrator model, the continuous-time equations of motion are expressed in the ENU frame as:

![](Malyuta2021Convex_figs/c0dd1b2d248bf6fafe846d6c37cd1b4bbfb87f51f81fa1831205229169d14763.jpg)  
FIGURE 22 A quadrotor at the University of Washington’s Autonomous Controls Laboratory, executing a collision-free trajectory computed by SCvx [52, 214, 215].

$$
\ddot {r} (\mathsf {t}) = a (\mathsf {t}) - g \hat {n},\tag{109}
$$

where $r \in \mathbb { R } ^ { 3 }$ denotes the position, $g \in \mathbb { R }$ is the (constant) acceleration due to gravity, $\hat { n } = ( 0 , 0 , 1 ) \in \mathbb { R } ^ { 3 }$ is the $^ { \mathrm { \bullet } } \mathrm { u p } ^ { \mathrm { \bullet } }$ direction, and $a ( \mathrm { t } ) \in \mathbb { R } ^ { 3 }$ is the commanded ac celeration, which is the control input. The time t spans the interval $[ 0 , t _ { f } ]$ . Because the previous section on SCP used a normalized time $t \in [ 0 , 1 ]$ ], we call t the absolute time and use the special font to denote it. We allow the trajectory duration to be optimized, and impose the following constraint to keep the final time bounded:

![](Malyuta2021Convex_figs/813eaba2192dd15095a5059a2b304463204aa2832c95c3b538eff687fa7aef4a.jpg)  
(a) Side view of the optimal landing trajectory. The glideslope constrain (103i) is activated at a single time instance mid-flight.

![](Malyuta2021Convex_figs/cdae7f4348deafec327879b4314b205a721642fd9141343802c0bb75c2a89b36.jpg)  
(d) Mass history. The vehicle uses a feasible amount of fuel.

(e) Pointing angle history. Constraint (103h) gets activated.  
![](Malyuta2021Convex_figs/122f4a2db064145c11da64f1f207c40f7f9881c9b2020830195438dd5b37ca20.jpg)

$$
t _ {f, \mathrm{min}} \leq t _ {f} \leq t _ {f, \mathrm{max}},\tag{110}
$$

where $t _ { f , \operatorname* { m i n } } \in \mathbb { R }$ and $t _ { f , \operatorname* { m a x } } \in \mathbb { R }$ are user-defined parameters. Boundary conditions on the position and velocit are imposed to ensure that the vehicle begins and ends at the desired states:

$$
r (0) = r _ {0}, \quad \dot {r} (0) = v _ {0},\tag{111a}
$$

$$
r (t _ {f}) = r _ {f}, \quad \dot {r} (t _ {f}) = v _ {f}.\tag{111b}
$$

The magnitude of the commanded acceleration is lim ited from above and below by the electric motor and propeller configuration, and its direction is constrained to model a tilt angle constraint on the quadrotor. In efect, the acceleration direction is used as a proxy for the vehicle attitude. This is an accurate approximation for a “flat” quadrotor configuration where the propellers are not canted with respect to the plane of the quadro tor body. Specifically, we enforce the following control

![](Malyuta2021Convex_figs/0064da7ea85425cc5f10f1f1438c5170d479279c1dd6839e3737981d4ebe63c2.jpg)

![](Malyuta2021Convex_figs/5678aa74e4d0af124523b249c443095add264443357dbbc8b7dcf2f2d869ca5b.jpg)  
(b) Front-on view of the optimal landing trajectory.  
(c) Velocity history. Constraint (103j) is never activated.

![](Malyuta2021Convex_figs/4d16d96dec5318d502e4f8f05bbb05e05c4fb28d8afcd164281a8408b1a11d18.jpg)  
(f) Thrust magnitude history. The LCvx equality constraint (96f) is tight.

![](Malyuta2021Convex_figs/8fef12a1c2fd50a9b0235ef4301685e37aa0bcd3689dee296b574877ace83a97.jpg)  
(g) Vertical thrust projection. The rocket never hovers  
FIGuRE 21 Various, views, of the globally optimal rocket landing trajectory obtained via lossless convexification for, Problem, 95 Circular markers show the discrete-time trajectory directly returned from the convex solver. Lines show the continuous-time trajectory, which is obtained by numerically integrating the ZOH discretized control signal through the dynamics (95b)-(95d). The exact match at every discrete-time node demonstrates that the solution is dynamically feasible for the actual continuous-time vehicle.

constraints:

$$
a _ {\mathrm{min}} \leq \| a (\mathfrak {t}) \| _ {2} \leq a _ {\mathrm{max}},\tag{112a}
$$

$$
\| a (\mathbf {t}) \| _ {2} \cos \theta_ {\mathrm{max}} \leq \hat {n} ^ {\intercal} a (\mathbf {t}),\tag{112b}
$$

where $0 < a _ { \mathrm { m i n } } < a _ { \mathrm { m a x } }$ are the acceleration bounds and $\theta _ { \mathrm { { m a x } } } ~ \in ~ ( 0 ^ { \circ } , 1 8 0 ^ { \circ } ]$ is the maximum angle by which the acceleration vector is allowed to deviate from the “up” direction.

Finally, obstacles are modeled as three-dimensional ellipsoidal keep-out zones, described by the following nonconvex constraints:

$$
\left\| H _ {j} \big (r (\mathfrak {t}) - c _ {j} \big) \right\| _ {2} \geq 1, \quad j = 1, \dots , n _ {\mathrm{obs}},\tag{113}
$$

where $c _ { j } \in \mathbb { R } ^ { 3 }$ denotes the center, and $H _ { j } \in \mathbb { S } _ { + + } ^ { 3 }$ defines the size and shape of the j-th obstacle. Note that the formulation allows the obstacles to intersect.

Using the above equations, we wish to solve the following free final time optimal control problem that minimizes control energy:

$$
\min _ {u, t _ {f}} \int_ {0} ^ {t _ {f}} \| a (\mathbf {t}) \| _ {2} ^ {2} \mathrm{d} \mathbf {t}\tag{114a}
$$

$$
\mathrm{s.t.} (1 0 9) - (1 1 3).\tag{114b}
$$

Due to the presence of nonconvex state constraints (113), only embedded LCvx applies to the above problem. In particular, LCvx can be used to handle the nonconvex input lower bound in (112a) along with the tilt constraint in (112b). This removes some of the nonconvexity. However, it is only a partial convexification which still leaves behind a nonconvex optimal control problem. Thus, we must resort to SCP techniques for the solution.

## SCvx Formulation

We begin by demonstrating how SCvx can be used to solve Problem 114. To this end, we describe how the problem can be cast into the template of Problem 39. Once this is done, the rest of the solution process is completely automated by the mechanics of the SCvx algorithm as described in the previous section. To make the notation lighter, we will omit the argument of time whenever possible.

Let us begin by defining the state and input vectors. For the input vector, note that the nonconvex input constraints in (112) can be convexified via embedded LCvx. In particular, the relaxation used for Problem 10 can losslessly convexify both input constraints by introducing a slack input $\sigma \in \mathbb { R }$ and rewriting (112) as:

$$
a _ {\mathrm{min}} \leq \sigma \leq a _ {\mathrm{max}},\tag{115a}
$$

$$
\| a \| _ {2} \leq \sigma ,\tag{115b}
$$

$$
\sigma \cos \theta_ {\mathrm{max}} \leq \hat {n} ^ {\intercal} a,\tag{115c}
$$

where (115b) is the familiar LCvx equality constraint. Thus, we can define the following state and “augmented”

TABLE 2 Algorithm parameters for the quadrotor obstacle avoidance example.

<table><tr><td colspan="4">Problem parameters:</td></tr><tr><td> $t_{f,\min}$ </td><td>0.0</td><td>s</td><td>min final time</td></tr><tr><td> $t_{f,\max}$ </td><td>2.5</td><td>s</td><td>max final time</td></tr><tr><td>g</td><td>9.81</td><td>m s $^{-2}$ </td><td>gravity</td></tr><tr><td> $a_{\min}$ </td><td>0.6</td><td>m s $^{-2}$ </td><td>min acceleration</td></tr><tr><td> $a_{\max}$ </td><td>23.2</td><td>m s $^{-2}$ </td><td>max acceleration</td></tr><tr><td> $\theta_{\max}$ </td><td>60</td><td>°</td><td>max tilt angle</td></tr><tr><td> $c_1$ </td><td>(1,2,0)</td><td>m</td><td>center of obstacle 1</td></tr><tr><td> $c_2$ </td><td>(2,5,0)</td><td>m</td><td>center of obstacle 2</td></tr><tr><td> $H_1$ </td><td>diag(2,2,0)</td><td>m $^{-1}$ </td><td>shape of obstacle 1</td></tr><tr><td> $H_2$ </td><td>diag(1.5,1.5,0)</td><td>m $^{-1}$ </td><td>shape of obstacle 2</td></tr><tr><td> $r_0$ </td><td>(0,0,0)</td><td>m</td><td>initial position vector</td></tr><tr><td> $v_0$ </td><td>(0,0,0)</td><td>m s $^{-1}$ </td><td>initial velocity vector</td></tr><tr><td> $r_f$ </td><td>(2.5,6,0)</td><td>m</td><td>final position vector</td></tr><tr><td> $v_f$ </td><td>(0,0,0)</td><td>m s $^{-1}$ </td><td>final velocity vector</td></tr></table>

Algorithm parameters:

<table><tr><td></td><td>SCvx</td><td>GuSTO</td></tr><tr><td>N</td><td>30</td><td>30</td></tr><tr><td>q</td><td>∞</td><td>∞</td></tr><tr><td> $\hat{q}$ </td><td>∞</td><td>∞</td></tr><tr><td>P</td><td>(48)</td><td>(48)</td></tr><tr><td> $h_{\lambda}$ </td><td></td><td>(71)</td></tr><tr><td>λ</td><td>30</td><td></td></tr><tr><td> $λ_0, λ_{max}$ </td><td></td><td> $10^4, 10^9$ </td></tr><tr><td>η</td><td>1</td><td>10</td></tr><tr><td> $η_0, η_1$ </td><td> $10^{-3}, 10$ </td><td> $10^{-3}, 10$ </td></tr><tr><td> $ρ_0, ρ_1, ρ_2$ </td><td>0, 0.1, 0.7</td><td>0.1, 0.9, -</td></tr><tr><td> $β_{sh}, β_{gr}$ </td><td>2, 2</td><td>2, 2</td></tr><tr><td> $γ_{fail}$ </td><td></td><td>5</td></tr><tr><td>μ</td><td></td><td>0.8</td></tr><tr><td> $k_*$ </td><td></td><td>6</td></tr><tr><td>ε</td><td>0</td><td>0</td></tr><tr><td> $ε_r$ </td><td>0</td><td>0</td></tr></table>

input vectors:

$$
x = \left[ \begin{array}{c} r \\ \dot {r} \end{array} \right] \in \mathbb {R} ^ {6}, \quad u = \left[ \begin{array}{c} a \\ \sigma \end{array} \right] \in \mathbb {R} ^ {4}.\tag{116}
$$

Next, we have to deal with the fact that Problem 39 uses normalized time $t \in [ 0 , 1 ]$ ], while Problem 114 uses absolute time $\mathrm { ~ t ~ } \in \ [ 0 , t _ { f } ]$ . To reconcile the two quantities, we use a one-dimensional parameter vector $p \in \mathbb R$ The parameter defines a time dilation such that the following relation holds:

$$
\mathsf {t} = p t,\tag{117}
$$

from which it follows that $p \equiv t _ { f }$ . In absolute time, the dynamics are given directly by writing (109) in terms of (116), which gives a set of time-invariant first-order ordinary diferential equations:

$$
f (x, u) = \left[ \begin{array}{c} \dot {r} \\ a - g \hat {n} \end{array} \right].\tag{118}
$$

For Problem 39, we need to convert the dynamics to normalized time. We do so by applying the chain rule:

$$
{\frac {\mathrm{d} x}{\mathrm{d} t}} = {\frac {\mathrm{d} x}{\mathrm{d} \mathbf {t}}} {\frac {\mathrm{d} \mathbf {t}}{\mathrm{d} t}} = p f (x, u),\tag{119}
$$

which yields the dynamics (39b) in normalized time:

$$
f (x, u, p) = p f (x, u).\tag{120}
$$

The convex path constraints (39c)-(39d) are easy to write. Although there are no convex state constraints, there are convex final time bounds (110). These can be included as a convex state path constraint (39c), which is mixed in the state and parameter. Using (117), we define the convex state path constraints as:

$$
\mathcal {X} = \bigl \{(x, p) \in \mathbb {R} ^ {6} \times \mathbb {R}: t _ {f, \min} \leq p \leq t _ {f, \max} \bigr \}.\tag{121}
$$

On the other hand, the convex input constraint set is given by all the input vectors that satisfy (115).

The nonconvex path constraints (39e) are given by the vector function $s : \mathbb { R } ^ { 3 }  \mathbb { R } ^ { n _ { \mathrm { o b s } } }$ , whose elements encode the obstacle avoidance constraints:

$$
s _ {j} (r) = 1 - \| H _ {j} (r - c _ {j}) \| _ {2}, \quad j = 1, \ldots , n _ {\mathrm{obs}}.\tag{122}
$$

We will briefly mention how to evaluate the Jacobian (44e) for (122). Suppose that a reference position trajectory $\{ \bar { r } ( t ) \} _ { 0 } ^ { 1 }$ is available, and consider the j-th obstacle constraint in (122). The following gradient then allows to evaluate (44e):

$$
\nabla s _ {j} (r) = - \frac {H _ {j} ^ {\intercal} H _ {j} (r - c _ {j})}{\left\| H _ {j} (r - c _ {j}) \right\| _ {2}}.\tag{123}
$$

The boundary conditions (39f) and (39g) are obtained from (111):

$$
g _ {\mathrm{ic}} \big (x (0), p \big) = \left[ \begin{array}{c} r (0) - r _ {0} \\ \dot {r} (0) - v _ {0} \end{array} \right],\tag{124a}
$$

$$
g _ {\mathrm{tc}} \big (x (1), p \big) = \left[ \begin{array}{c} r (1) - r _ {f} \\ \dot {r} (1) - v _ {f} \end{array} \right].\tag{124b}
$$

Lastly, we have to convert the cost (114a) into the Bolza form (40). There is no terminal cost, hence $\phi \equiv 0$ On the other hand, the direct transcription of the running cost would be $\Gamma ( x , u , p ) = p \sigma ^ { 2 }$ . However, we will simplify this by omitting the time dilation parameter. This simplification makes the problem easier by removing nonconvexity from the running cost, and numerical results still show good resulting trajectories. Furthermore, since SCvx augments the cost with penalty terms in (49), we will normalize the running cost by its nominal value in order to make it roughly unity for a “mild” trajectory. This greatly facilitates the selection of the penalty weight λ. By taking the nominal value of σ as the hover condition, we define the following running cost:

$$
\Gamma (x, u, p) = \left(\frac {\sigma}{g}\right) ^ {2}.\tag{125}
$$

We now have a complete definition of Problem 39 for the quadrotor obstacle avoidance problem. The only re maining task is to choose the SCvx algorithm parameters listed in Table 1. The rest of the solution process is completely automated by the general SCvx algorithm description in Part II.

## GuSTO Formulation

The GuSTO algorithm can also be used to solve Problem 114. The formulation is almost identical to SCvx, which underscores the fact that the two algorithms can be used interchangeably to solve many of the same problems. The quadratic running cost (68) encodes (125) as follows:

$$
S (p) = \mathrm{diag} \left(0, 0, 0, g ^ {- 2}\right),
$$

$$
\ell (x, p) = 0,\tag{126a}
$$

(126b)

$$
g (x, p) = 0.\tag{126c}
$$

We can also cast the dynamics (118) into the control afine form (69):

$$
f _ {0} (x) = \left[ \begin{array}{c} \dot {r} \\ - g \hat {n} \end{array} \right],\tag{127a}
$$

$$
f _ {i} (x) = \left[ \begin{array}{c} 0 \\ e _ {i} \end{array} \right], \quad i = 1, 2, 3,
$$

$$
f _ {4} (x) = 0,\tag{127b}
$$

(127c)

where $e _ { i } ~ \in ~ \mathbb { R } ^ { 3 }$ is the i-th standard basis vector. The reader may be surprised that these are the only changes required to convert the SCvx formulation from the previous section into a form that can be ingested by GuSTO. The only remaining task is to choose the GuSTO algorithm parameters listed in Table 1. Just like for SCvx, the rest of the solution process is completely automated by the general GuSTO algorithm description in Part II.

## Initial Trajectory Guess

The initial state reference trajectory is obtained by a simple straight-line interpolation as provided by (42):

$$
x (t) = (1 - t) \left[ \begin{array}{c} r _ {0} \\ v _ {0} \end{array} \right] + t \left[ \begin{array}{c} r _ {f} \\ v _ {f} \end{array} \right], \text {   for   } t \in [ 0, 1 ].\tag{128}
$$

The initial parameter vector, which is just the time dilation, is chosen to be in the middle of the allowed trajectory durations:

$$
p = \frac {t _ {f , \mathrm{min}} + t _ {f , \mathrm{max}}}{2}.\tag{129}
$$

The initial input trajectory is guessed based on insigh about the quadrotor problem. Ignoring any particular trajectory task, we know that the quadrotor will gener ally have to support its own weight under the influence of gravity. Thus, we choose a constant initial input guess that would make a static quadrotor hover:

$$
a (t) = g \hat {n}, \sigma (t) = g, \mathrm{for} t \in [ 0, 1 ].\tag{130}
$$

TABLE 3 Breakdown of subproblem size for the quadrotor obstacle avoidance example.

<table><tr><td></td><td>SCvx</td><td>GuSTO</td></tr><tr><td>Variables</td><td>640</td><td>542</td></tr><tr><td>Affine equalities</td><td>186</td><td>186</td></tr><tr><td>Affine inequalities</td><td>240</td><td>360</td></tr><tr><td>One-norm cones</td><td>29</td><td>0</td></tr><tr><td>Infinity-norm cones</td><td>61</td><td>31</td></tr><tr><td>Second-order cones</td><td>30</td><td>30</td></tr></table>

This initial guess is infeasible with respect to both the dynamics and the obstacle constraints, and it is extremely cheap to compute. The fact that it works well in practice highlights two facts: SCP methods are relatively easy to initialize, and they readily accept infeasible initial guesses. Note that in the particular case of this problem, an initial trajectory could also be computed using a convex version of the problem obtained by removing the obstacle constraints (113) and applying the LCvx relaxation (115).

## Numerical Results

We now have a specialized instance of Problem 39 and an initialization strategy for the quadrotor obstacle avoidance problem. The solution is obtained via SCP according to the general algorithm descriptions for SCvx and GuSTO. For temporal discretization, we use the FOH interpolating polynomial method from “Discretizing Continuous-time Optimal Control Problems”. The algorithm parameters are provided in Table 2, and the full implementation is available in the code repository linked in Figure 2. ECOS is used as the numerical convex optimizer at 2 in Figure 11 [216]. The timing results correspond to a Dell XPS 13 9260 laptop powered by an Intel Core i5-7200U CPU clocked at 2.5 GHz. The computer has 8 GiB LPDD3 RAM and 128 KiB L1, 512 KiB L2, and 3 MiB L3 cache.

The convergence process for both algorithms is illustrated in Figure 24. We have set the convergence tolerances $\varepsilon = \varepsilon _ { \mathrm { r } } = 0$ and we terminate both algorithms after 15 iterations. At each iteration, the algorithms have to solve subproblems of roughly equal sizes, as shown in Table 3. Diferences in the sizes arise from the slightly diferent subproblem formulations of each algorithm. Among the primary contributors are how artificial infeasibility and unboundedness are treated, and diferences in the cost penalty terms. Notably, GuSTO has no one-norm cones because it does not have a dynamics virtual control term like SCvx (compare (55b) and (82b)). Despite their diferences, Figure 24 shows that GuSTO and SCvx are equally fast.

The trajectory solutions for SCvx and GuSTO are shown in Figures 23 and 25. Recall that this is a free final time problem, and both algorithms are able to increase the initial guess (129) until the maximum allowed flight time $t _ { f , \operatorname* { m a x } } .$ Note that this is optimal, since a quadrotor minimizing control energy (114a) will opt for a slow trajectory with the lowest acceleration.

![](Malyuta2021Convex_figs/6f8b8a7d58dde7991625d6aa64d24598544720de8a0dfa55c178f156c131e03a.jpg)

![](Malyuta2021Convex_figs/5ebc14a9026e25b8aa7d5235c62e33b07adfa63b079baf3757f1a87ae0942781.jpg)  
(a) SCvx.

![](Malyuta2021Convex_figs/01846199be964be7a6c0b22d2fd449bb476e9effa078f88048126ce59428f2b6.jpg)

![](Malyuta2021Convex_figs/bf6424361e8effeb42b665e442889e3f9fd8920634cb6125f277039f8121a987.jpg)  
(b) GuSTO.  
FIGURE 23 The position trajectory evolution (left) and the final converged trajectory (right) for the quadrotor obstacle avoidance problem. The continuous-time trajectory in the right plots is obtained by numerically integrating the dynamics (131). The fact that this trajectory passes through the discrete-time subproblem solution confirms dynamic feasibility. The red lines in the right plots show the acceleration vector as seen from above.

The SCvx and GuSTO solutions are practically iden tical. The fact that they were produced by two diferent algorithms can only be spotted from the diferent con vergence histories on the left side in Figure 23. It is not always intuitive how the initial guess morphs into the final trajectory. It is remarkable that the infeasible tra jectories of the early iterations morph into a smooth and feasible trajectory. Yet, this is guaranteed by the SCP convergence theory in Part II. For this and many other trajectory problems, we have observed time and again how SCP is adept at morphing rough initial guesses into fine-tuned feasible and locally optimal trajectories.

Finally, we will make a minor note of that tempora discretization results in some clipping of the obstacle keep-out zones in Figure 23. This is the direct result of imposing constraints only at the discrete-time nodes. Various strategies exist to mitigate the clipping efect, such as increasing the radius of the keep-out zones, increasing the number of discretization points, imposing a suficiently low maximum velocity constraint, or numerically minimizing a function related to the state transition matrix [191, 192].

![](Malyuta2021Convex_figs/28bfbf297479dfeaf505565ad77ae281943a774fd459152f0c841fcead063900.jpg)

![](Malyuta2021Convex_figs/47a25a55338772692140c83553b1601b6e160ac1e0e2e0c50ed7efa6fb7431f5.jpg)  
(a) SCvx.

![](Malyuta2021Convex_figs/93713af797ad303c925d22c8f4f9b6bf1b0ef1192f296e7fae6d76a32c94d676.jpg)

![](Malyuta2021Convex_figs/7ce2d66c316f63cd929471191c67e97e4dabeda238f68def5c59247ab1d336e9.jpg)  
(b) GuSTO.  
FIGURE 24 Convergence and runtime performance for the quadrotor obstacle avoidance problem. Both algorithms take a similar amount of time and number of iterations to converge to a given tolerance. The runtime subplots in the bottom row show statistics on algorithm performance over 50 executions. The solution times per subproblem are roughly equal, which shows that the subproblem difficulty stays constant over the iterations. Formulate measures the time taken to parse the subproblem into the input format of the convex optimizer; Discretize measures the time taken to temporally discretize the linearized dynamics (45b); and Solve measures the time taken by the core convex numerical optimizer Each bar shows the median time. The blue trace across the diagonal shows the cumulative time obtained by summing the runtimes of a preceding iterations. Its markers are placed at the median time, and the error bars show the 10% (bottom) and 90% (top) quantiles. Because small runtime differences accumulate over iterations, the error bars grow with iteration count.

## SCP: 6-DoF Free-flyer

Having demonstrated the use of sequential convex programming on a relatively simple quadrotor trajectory, we now present a substantially more challenging example involving nonlinear 6-DoF dynamics and a more complex set of obstacle avoidance constraints.

The objective is to compute a trajectory for a 6-DoF free-flying robotic vehicle that must navigate through an environment akin to the International Space Station (ISS). Free-flyers are robots that provide assistance to human operators in micro-gravity environments [219, 220]. As shown in Figure 26, Astrobee and the JAXA

Internal Ball Camera (Int-Ball) are two recent successful deployments of such robots. Their goals include filming the ISS and assisting with maintenance tasks [221]. The particulars of this SCP example are taken primarily from [50].

The quadrotor in the previous section was modeled as a point mass whose attitude is approximated by the direction of the acceleration vector. The free-flyer, on the other hand, is a more complex vehicle that must generally perform coupled translational and rotational motion using a multi-thruster assembly. Maneuvers ma require to point a camera at a fixed target, or to emu late nonholonomic behavior for the sake of predictabilit and operator comfort [222, 223]. This calls for whole body motion planning, for which we model the free-flyer as a full 6-DoF rigid body with both translational and rotational dynamics.

To describe the equations of motion, we need to in troduce two reference frames. First, let $\mathcal { F } _ { \mathcal { T } }$ be an iner tial reference frame with a conveniently positioned, but otherwise arbitrary, origin. Second, let $\mathcal { F } _ { B }$ be a rotating reference frame afixed to the robot’s center of mass, and whose unit vectors are aligned with the robot’s principal axes of inertia. We call $\mathcal { F } _ { \mathcal { Z } }$ the inertial frame and $\mathcal { F } _ { B }$ the body frame. Correspondingly, vectors expressed in $\mathcal { F } _ { \mathcal { I } }$ are inertial vectors and carry an subscript $( \mathrm { e . g . } , x _ { \tau } )$ while those expressed in $\mathcal { F } _ { B }$ are body vectors and carry a subscript $( \mathrm { e . g . } , \ x _ { B } )$ . For the purpose of trajectory generation, we encode the orientation of $\mathcal { F } _ { B }$ with respect to $\mathcal { F } _ { \mathcal { T } }$ using a vector representation of a unit quaternion, $q _ { B  \tau } \in \mathbb { R } ^ { 4 }$

![](Malyuta2021Convex_figs/b78d1f2f8e99b1d0c3f420aff543fc2f3003cc7f8fcad87b675577fad4f4a3e0.jpg)

![](Malyuta2021Convex_figs/51abec4d4b6899269e66f03e98afc30304dbb7a23636b41184920ad3413b4fab.jpg)  
FIGURE 25 The acceleration norm and tilt angle time histories for the converged trajectory of the quadrotor obstacle avoidance problem. These are visually identical for SCvx and GuSTO, so we only show a single plot. The continuous-time acceleration norm is obtained from the FOH assumption (S28), while the continuous-time tilt angle is obtained by integrating the solution through the nonlinear dynamics. Similar to Figure 21, the acceleration time history plot confirms that lossless convexification holds (i.e., the constraint (115b) holds with equality).

Our convention is to represent the translational dynamics in $\mathcal { F } _ { \mathcal { Z } }$ and the attitude dynamics in $\mathcal { F } _ { B }$ . This yields the following Newton-Euler equations that govern the free-flyer’s motion [59]:

$$
\dot {r} _ {\mathcal {I}} (\mathfrak {t}) = v _ {\mathcal {I}} (\mathfrak {t}),\tag{131a}
$$

$$
\dot {v} _ {\mathcal {I}} (\mathfrak {t}) = m ^ {- 1} T _ {\mathcal {I}} (\mathfrak {t}),\tag{131b}
$$

$$
\dot {q} _ {\mathcal {B} \leftarrow \mathcal {I}} (\mathsf {t}) = \frac {1}{2} q _ {\mathcal {B} \leftarrow \mathcal {I}} (\mathsf {t}) \otimes \omega_ {\mathcal {B}} (\mathsf {t}),\tag{131c}
$$

$$
\dot {\omega} _ {\mathcal {B}} (\mathfrak {t}) = J ^ {- 1} \big (M _ {\mathcal {B}} (\mathfrak {t}) - \omega_ {\mathcal {B}} (\mathfrak {t}) ^ {\times} J \omega_ {\mathcal {B}} (\mathfrak {t}) \big).\tag{131d}
$$

The state variables in the above equations are the inertial position $r _ { \mathcal { Z } } \in \mathbb { R } ^ { 3 }$ , the inertial velocity $v _ { \mathcal { Z } } \in \mathbb { R } ^ { 3 }$ , the aforementioned unit quaternion attitude $q _ { B  \tau } \in \mathbb { R } ^ { 4 }$ and the body angular velocity $\boldsymbol { \omega } _ { B } \in \mathbb { R } ^ { 3 }$ . The latter variable represents the rate at which $\mathcal { F } _ { B }$ rotates with respect to $\mathcal { F } _ { \mathcal { T } }$ . The free-flyer’s motion is controlled by an inertial thrust vector $T _ { \mathcal { I } } \in \mathbb { R } ^ { 3 }$ and a body torque vector

![](Malyuta2021Convex_figs/adce7210cbba8ab998d962f3b2ba81e04785a133b1b7050fe7f01d6f93f26dd4.jpg)  
FIGURE 26 Two examples of free-flyer robots at the Internationa Space Station, the JAXA Int-Ball (left) and the Naval Postgraduate School/NASA Astrobee (right) [217, 218]. These robots provide a helping hand in space station maintenance tasks.

$M _ { B } \in \mathbb { R } ^ { 3 }$ . The physical parameters of the free-flyer, the mass $m > 0$ and the principal moment of inertia matrix $J \in \mathbb { R } ^ { 3 \times 3 }$ , are fixed. The dynamics are written in absolute time t that spans the interval $[ 0 , t _ { f } ]$ . We allow the final time $t _ { f }$ to be optimized, and bound it using the previous constraint (110).

The initial and final conditions for each state are specified in this example to be fixed constants:

$$
r _ {\mathcal {I}} (0) = r _ {0}, \qquad r _ {\mathcal {I}} (t _ {f}) = r _ {f},\tag{132a}
$$

$$
v _ {\mathcal {I}} (0) = v _ {0}, \qquad v _ {\mathcal {I}} (t _ {f}) = v _ {f},\tag{132b}
$$

$$
q _ {\mathcal {B} \leftarrow \mathcal {I}} (0) = q _ {0}, q _ {\mathcal {B} \leftarrow \mathcal {I}} (t _ {f}) = q _ {f},\tag{132c}
$$

$$
\omega_ {\mathcal {B}} (0) = 0, \qquad \omega_ {\mathcal {B}} (t _ {f}) = 0.\tag{132d}
$$

The free-flyer robot implements a 6-DoF holonomic ac tuation system based on a centrifugal impeller that pressurizes air, which can then be vented from a set of noz zles distributed around the body [224, 225]. Holonomic actuation means that the thrust and torque vectors are independent from the vehicle’s attitude [226]. The capability of this system can be modeled by the following control input constraints:

$$
\| T _ {\mathcal {I}} (\mathfrak {t}) \| _ {2} \leq T _ {\max}, \quad \| M _ {\mathcal {B}} (\mathfrak {t}) \| _ {2} \leq M _ {\max},\tag{133}
$$

where $T _ { \mathrm { m a x } } > 0$ and $M _ { \mathrm { m a x } } > 0$ are user-defined constants representing the maximum thrust and torque.

This problem involves both convex and nonconvex state constraints. Convex constraints are used to bound the velocity and angular velocity magnitudes to userdefined constants:

$$
\| v _ {\mathcal {I}} (\mathsf {t}) \| _ {2} \leq v _ {\max}, \quad \| \omega_ {\mathcal {B}} (\mathsf {t}) \| _ {2} \leq \omega_ {\max}.\tag{134}
$$

Nonconvex state constraints are used to model the (fic tional) ISS flight space and to avoid floating obstacles. The latter are modeled exactly as in the quadrotor ex ample using the constraints in (113). The flight space, on the other hand, is represented by a union of rectangular rooms. This is a dificult nonconvex constraint and its eficient modeling requires some explanation.

![](Malyuta2021Convex_figs/bb12f090e7f04c0d2db3f1654243c248263a2f6aa353cf4ff7dc2ca2891fec0d.jpg)  
(a)

![](Malyuta2021Convex_figs/21eac6c13b4259f8f1daad7f08e644628c5b14a4eb5b5f47c9c4ea770a2bdccd.jpg)  
(b)

![](Malyuta2021Convex_figs/f9d74731e205d65e106f9e049a8362852383ce45ae2bf53630e14370ae3c049e.jpg)  
(c)

![](Malyuta2021Convex_figs/f11b26f17ba964c7ffc11aca3003f6c6f7b03edbc26c0f9af2f995ce17e121f9.jpg)  
(d)  
FIGURE 27 A heatmap visualization of the exact SDF (143) and the approximate SDF (146) for several values of the sharpness parameter σ. Each plot also shows the SDF zero-level set boundary as a dashed line. This boundary encloses the feasible flight space, which corresponds to nonnegative values of the SDF.

At the conceptual level, the space station flight space is represented by a function $d _ { \mathrm { s s } } : \mathbb { R } ^ { 3 }  \mathbb { R }$ that maps inertial position to a scalar number. This is commonly referred to as a signed distance function (SDF) [227]. Let us denote the set of positions that are within the flight space by $\mathcal { O } _ { \mathrm { s s } } \subset \mathbb { R } ^ { 3 }$ . A valid SDF is given by any function that satisfies the following property:

$$
r _ {\mathcal {I}} \in \mathcal {O} _ {\mathrm{ss}} \Leftrightarrow d _ {\mathrm{ss}} (r _ {\mathcal {I}}) \geq 0.\tag{135}
$$

If we can formulate a continuously diferentiable $d _ { \mathrm { s s } }$ then we can model the flight space using (135) as the following nonconvex path constraint (39e):

$$
d _ {\mathrm{ss}} (r _ {\mathcal {I}}) \geq 0.\tag{136}
$$

Open-source libraries such as Bullet [228] are available to compute the SDF for obstacles of arbitrary shape. In this work, we will use a simpler custom implementation. To begin, let us model the space station as an assembly of several rooms. This is expressed as a set union:

$$
\mathcal {O} _ {\mathrm{ss}} \triangleq \bigcup_ {i = 1} ^ {n _ {\mathrm{ss}}} \mathcal {O} _ {i},\tag{137}
$$

where each room $\mathcal { O } _ { i }$ is taken to be a rectangular box:

$$
\mathcal {O} _ {i} \triangleq \left\{r _ {\mathcal {I}} \in \mathbb {R} ^ {3}: l _ {i} ^ {\mathrm{ss}} \leq r _ {\mathcal {I}} \leq u _ {i} ^ {\mathrm{ss}} \right\}.\tag{138}
$$

The coordinates $l _ { i } ^ { \mathrm { s s } }$ and $u _ { i } ^ { \mathrm { s s } }$ represent the “rear bottom right” and the “ahead top left” corners of the i-th room, when looking along the positive axis directions. Equivalently, but more advantageously for implementing the SDF, the set (138) can be represented as:

$$
\mathcal {O} _ {i} \triangleq \Big \{r _ {\mathcal {I}} \in \mathbb {R} ^ {3}: \left\| \frac {r _ {\mathcal {I}} - c _ {i} ^ {\mathrm{ss}}}{s _ {i} ^ {\mathrm{ss}}} \right\| _ {\infty} \leq 1 \Big \},\tag{139}
$$

where vector division is entrywise, and the new terms $c _ { i } ^ { \mathrm { s s } }$ and $s _ { i } ^ { \mathrm { s s } }$ are the room’s centroid and diagonal:

$$
c _ {i} ^ {\mathrm{ss}} = \frac {u _ {i} ^ {\mathrm{ss}} + l _ {i} ^ {\mathrm{ss}}}{2}, s _ {i} ^ {\mathrm{ss}} = \frac {u _ {i} ^ {\mathrm{ss}} - l _ {i} ^ {\mathrm{ss}}}{2}.\tag{140}
$$

To find the SDF for the overall flight space, we begin with the simpler task of writing an SDF for a single room. This is straightforward using (139):

$$
d _ {\mathrm{ss}, i} (r _ {\mathcal {I}}) \triangleq 1 - \left\| \frac {r _ {\mathcal {I}} - c _ {i} ^ {\mathrm{ss}}}{s _ {i} ^ {\mathrm{ss}}} \right\| _ {\infty},\tag{141}
$$

which is a concave function that satisfies a similar property to (135):

$$
r _ {\mathcal {I}} \in \mathcal {O} _ {i} \Leftrightarrow d _ {\mathrm{ss}, i} (r _ {\mathcal {I}}) \geq 0.\tag{142}
$$

Because $d _ { \mathrm { s s } , i }$ is concave, the constraint on the right side of (142) is convex. This means that constraining the robot to be inside room $\mathcal { O } _ { i }$ is a convex operation, which makes sense since $\mathcal { O } _ { i }$ is a convex set.

As the free-flyer traverses the flight space, one can imagine the room SDFs to evolve based on the robot’s position. When the robot enters the i-th room, $d _ { \mathrm { s s } , i }$ becomes positive and grows up to a maximum value of one as the robot approaches the room center. As the robot exits the room, $d _ { \mathrm { s s } , i }$ becomes negative and decreases in value as the robot flies further away. To keep the robot inside the space station flight space, the room SDFs have to evolve such that there is always at least one nonnega tive room SDF. This requirement precisely describes the overall SDF, which can be encoded mathematically as a maximization:

$$
d _ {\mathrm{ss}} (r _ {\mathcal {I}}) \triangleq \max _ {i = 1, \dots , n _ {\mathrm{ss}}} d _ {\mathrm{ss}, i} (r _ {\mathcal {I}}).\tag{143}
$$

We now have an SDF definition which satisfies the required property (135). Figure 27(a) shows an example scalar field generated by (143) for a typical space station layout. Visually, when restricted to a plane with a fixed altitude $r _ { \mathcal { T } , 3 }$ , the individual room SDFs form four-sided “pyramids” above their corresponding room.

The room SDFs $d _ { \mathrm { s s } , i }$ are concave, however the maximization in (143) generates a nonconvex function. Two possible strategies to encode (143) are by introducing integer variables or by a smooth approximation [46]. The former strategy generates a mixed-integer convex subproblem, which is possible to solve but does not fit the SCP algorithm mold of this article. As mentioned before for Problem 39, our subproblems do not involve integer variables. We thus pursue the smooth approximation strategy, which yields an arbitrarily accurate approximation of the feasible flight space $\mathcal { O } _ { \mathrm { s s } }$ and carries the significant computational benefit of avoiding mixed-integer programming.

The crux of our strategy is to replace the maximization in (143) with the softmax function. Given a general vector $v \in \mathbb { R } ^ { n }$ , this function is defined by:

$$
\mathsf {L} _ {\sigma} (v) = \sigma^ {- 1} \log \sum_ {i = 1} ^ {n} e ^ {\sigma v _ {i}},\tag{144}
$$

where $\sigma > 0$ is a sharpness parameter such that $\mathsf { L } _ { \sigma }$ upper bounds the exact max with an additive error of at most $\log ( n ) / \sigma$ . To develop intuition, consider the SDF (143) for two adjacent rooms and restricted along the j-th axis of the inertial frame. We can then write the SDF simply as:

$$
d _ {\mathrm{ss}} (r _ {\mathcal {I}, j}) = \max \bigg \{1 - \left| \frac {r _ {\mathcal {I} , j} - c _ {1 j} ^ {\mathrm{ss}}}{s _ {1 j} ^ {\mathrm{ss}}} \right|, 1 - \left| \frac {r _ {\mathcal {I} , j} - c _ {2 j} ^ {\mathrm{ss}}}{s _ {2 j} ^ {\mathrm{ss}}} \right| \bigg \}.\tag{145}
$$

Figure 28 illustrates the relationship between the exact SDF (145) and its approximation, which is obtained by replacing the max operator with $\mathsf { L } _ { \sigma }$ . We readily observe that $d _ { \mathrm { s s } }$ is indeed highly nonconvex, and that the approximation quickly converges to the exact SDF as σ increases. We now generalize this one-dimensional exam ple and replace (143) with the following approximation:

![](Malyuta2021Convex_figs/c32b703020a152e6d550513cd4e29a0c5761a20daee70bdbefe1c412121d8022.jpg)  
FIGURE 28 Illustration of the correspondence between between the exact SDF (143) and its approximation $\tilde { d } _ { \mathrm { s s } }$ using the softmax function (144). As the sharpness parameter σ increases, the approximation quickly converges to the exact SDF. This figure illustrates a sweep for $\sigma \in [ 1 , 5 ]$ , where lower values are associated with darker colors.

$$
\tilde {d} _ {\mathrm{ss}} (r _ {\mathcal {I}}) \triangleq \mathsf {L} _ {\sigma} \big (\delta_ {\mathrm{ss}} (r _ {\mathcal {I}}) \big),\tag{146a}
$$

$$
\delta_ {\mathrm{ss}, i} (r _ {\mathcal {I}}) \leq d _ {\mathrm{ss}, i} (r _ {\mathcal {I}}), \quad i = 1, \ldots , n _ {\mathrm{ss}},\tag{146b}
$$

where the new functions $\delta _ { \mathrm { s s } , i }$ as so-called “slack” room SDFs. The model (146) admits several favorable properties. First, (146a) is smooth in the new slack SDFs and can be included directly in (39e) as the following nonconvex path constraint:

$$
\tilde {d} _ {\mathrm{ss}} (r _ {\mathcal {I}}) \geq 0.\tag{147}
$$

Second, the constraints in (146b) are convex and can be included directly in (39c). Overall, the approximate SDF (146a) satisfies the following property:

$$
r _ {\mathcal {I}} \in \tilde {\mathcal {O}} _ {\mathrm{ss}} \Leftrightarrow \exists \delta_ {\mathrm{ss}} (r _ {\mathcal {I}}) \text {   such   that   (147)   holds. }\tag{148}
$$

where $\tilde { \mathcal { O } } _ { \mathrm { s s } } \subset \mathbb { R } ^ { 3 }$ is an approximation of $\mathcal { O } _ { \mathrm { s s } }$ that becomes arbitrarily more accurate as the sharpness parameter σ increases. The geometry of this convergence process is illustrated in Figure $2 7 ( \mathrm { b } ) \mathrm { - ( c ) }$ for a typical space station layout. Crucially, the fact that $\mathsf { L } _ { \sigma }$ is an upper bound of the max means that the approximate SDF $\tilde { d } _ { \mathrm { s s } }$ is nonnegative at the interfaces of adjacent rooms. In other words, the passage between adjacent rooms is not artificially blocked by our approximation.

Summarizing the above discussion, we wish to solve the following free final time optimal control problem that minimizes control energy:

$$
\min _ {T _ {\mathcal {I}}, M _ {\mathcal {B}}, t _ {f}} \int_ {0} ^ {t _ {f}} \| T _ {\mathcal {I}} (\mathfrak {t}) \| _ {2} ^ {2} + \| M _ {\mathcal {B}} (\mathfrak {t}) \| _ {2} ^ {2} \mathrm{d} \mathfrak {t}\tag{149a}
$$

$$
\text { s.t. } (1 3 1) - (1 3 4), (1 4 7), (1 1 0), (1 1 3).\tag{149b}
$$

## SCvx Formulation

Like for the quadrotor example, we begin by demonstrat ing how to cast Problem 149 into the standard template of Problem 39. While this process is mostly similar to that of the quadrotor, the particularities of the flight space constraint (147) will reveal a salient feature of efi cient modeling for SCP. Once the modeling step is done and an initial guess trajectory is defined, the solution process is completely automated by the general SCvx algorithm description in Part II. To keep the notation light, we omit the argument of time where possible.

Looking at the dynamics (131), we define the following state and control vectors:

$$
x = \left(r _ {\mathcal {I}}, v _ {\mathcal {I}}, q _ {\mathcal {B} \leftarrow \mathcal {I}}, \omega_ {\mathcal {B}}\right) \in \mathbb {R} ^ {1 3},\tag{150a}
$$

$$
u = \left(T _ {\mathcal {I}}, M _ {\mathcal {B}}\right) \in \mathbb {R} ^ {6}.\tag{150b}
$$

TABLE 4 Algorithm parameters for the 6-DoF freeflyer example.

<table><tr><td colspan="4">Problem parameters:</td></tr><tr><td> $t_{f,\min}$ </td><td>60</td><td>s</td><td>min final time</td></tr><tr><td> $t_{f,\max}$ </td><td>200</td><td>s</td><td>max final time</td></tr><tr><td>m</td><td>7.2</td><td>kg</td><td>free-flyer mass</td></tr><tr><td>J</td><td>0.1083 ·  $l_3$ </td><td>kg m2</td><td>free-flyer inertia matrix</td></tr><tr><td> $T_{\max}$ </td><td>20</td><td>mN</td><td>max two-norm of thrust</td></tr><tr><td> $M_{\max}$ </td><td>100</td><td>μNm</td><td>max two-norm of torque</td></tr><tr><td> $v_{\max}$ </td><td>0.4</td><td>ms-1</td><td>max free-flyer speed</td></tr><tr><td> $\omega_{\max}$ </td><td>1</td><td>° s-1</td><td>max free-flyer angular velocity</td></tr><tr><td> $c_1$ </td><td>(8.5, -0.15, 5.0)</td><td>m</td><td>center of obstacle 1</td></tr><tr><td> $c_2$ </td><td>(11.2, 1.84, 5.0)</td><td>m</td><td>center of obstacle 2</td></tr><tr><td> $c_3$ </td><td>(11.3, 3.8, 4.8)</td><td>m</td><td>center of obstacle 3</td></tr><tr><td> $H_1, H_2, H_3$ </td><td>3.33 ·  $l_3$ </td><td>m-1</td><td>shape of obstacles 1, 2, and 3</td></tr><tr><td> $l_i^{ss}$ </td><td>see code</td><td>m</td><td>room rear bottom right corner</td></tr><tr><td> $u_i^{ss}$ </td><td>see code</td><td>m</td><td>room ahead top left corner</td></tr><tr><td> $r_0$ </td><td>(6.5, -0.2, 5)</td><td>m</td><td>initial position vector</td></tr><tr><td> $v_0$ </td><td>(0.035, 0.035, 0)</td><td>ms-1</td><td>initial velocity vector</td></tr><tr><td> $q_0$ </td><td>-40(0, 1, 1)</td><td></td><td>initial attitude quaternion</td></tr><tr><td> $r_f$ </td><td>(11.3, 6, 4.5)</td><td>m</td><td>final position vector</td></tr><tr><td> $v_f$ </td><td>(0, 0, 0)</td><td>ms-1</td><td>final velocity vector</td></tr><tr><td> $q_f$ </td><td>0(0, 0, 1)</td><td></td><td>final attitude quaternion</td></tr><tr><td>σ</td><td>50</td><td></td><td>softmax sharpness parameter</td></tr><tr><td> $\varepsilon_{ss}$ </td><td>10-4</td><td></td><td>slack room SDF weight</td></tr><tr><td colspan="4">Algorithm parameters:</td></tr><tr><td></td><td>SCvx</td><td>GuSTO</td><td></td></tr><tr><td>N</td><td>50</td><td>30</td><td></td></tr><tr><td>q</td><td>∞</td><td>∞</td><td></td></tr><tr><td> $\hat{q}$ </td><td>∞</td><td>∞</td><td></td></tr><tr><td>P</td><td>(48)</td><td>(48)</td><td></td></tr><tr><td> $h_\lambda$ </td><td></td><td>(71)</td><td></td></tr><tr><td>λ</td><td>103</td><td></td><td></td></tr><tr><td> $λ_0, λ_{\max}$ </td><td></td><td>104, 109</td><td></td></tr><tr><td>η</td><td>1</td><td>1</td><td></td></tr><tr><td> $η_0, η_1$ </td><td>10-3, 10</td><td>10-3, 10</td><td></td></tr><tr><td> $ρ_0, ρ_1, ρ_2$ </td><td>0, 0.1, 0.7</td><td>0.1, 0.5, -</td><td></td></tr><tr><td> $β_{sh}, β_{gr}$ </td><td>2, 2</td><td>2, 2</td><td></td></tr><tr><td> $γ_{fail}$ </td><td></td><td>5</td><td></td></tr><tr><td>μ</td><td></td><td>0.8</td><td></td></tr><tr><td> $k_*$ </td><td></td><td>6</td><td></td></tr><tr><td>ε</td><td>0</td><td>0</td><td></td></tr><tr><td> $ε_r$ </td><td>0</td><td>0</td><td></td></tr></table>

Next, we define the parameter vector to serve two purposes. First, as for the quadrotor, we define a time dilation $\alpha _ { \mathrm { t } }$ such that (117) holds, yielding $\mathrm { { t } } = \alpha _ { \mathrm { { t } } } t$ . Second, we take advantage of the fact that (39c) is mixed in the state and parameter in order to place the slack room SDFs in (146b) into the parameter vector. In particular, we recognize that according to (55c), the constraint (146b) is imposed only at the discrete-time grid nodes. Thus, for a grid of N nodes, there are only $N n _ { \mathrm { s s } }$ instances of (146b) to be included. We can therefore define the following vector:

$$
\Delta_ {\mathrm{ss}} \triangleq \left(\delta_ {\mathrm{ss}} ^ {1}, \dots , \delta_ {\mathrm{ss}} ^ {N}\right) \in \mathbb {R} ^ {N n _ {\mathrm{ss}}},\tag{151}
$$

where $\delta _ { \mathrm { s s } } ^ { k } \equiv \delta _ { \mathrm { s s } } \big ( r _ { \mathcal { T } } ( t _ { k } ) \big )$ and $\Delta _ { \mathrm { s s } , i + ( k - 1 ) n _ { \mathrm { s s } } }$ denotes the slack SDF value for the i-th room at time $t _ { k }$ . To keep the notation concise, we will use the shorthand $\Delta _ { \mathrm { s s } , i k } \equiv$ $\Delta _ { \mathrm { s s } , i + ( k - 1 ) n _ { \mathrm { s s } } }$ . The overall parameter vector is then given

by:

$$
p = \left[ \begin{array}{c} \alpha_ {\mathfrak {t}} \\ \Delta_ {\mathrm{ss}} \end{array} \right] \in \mathbb {R} ^ {1 + N n _ {\mathrm{ss}}}.\tag{152}
$$

In absolute time, the dynamics (39b) are given directly by (131). As for the quadrotor, this forms a set of time invariant first-order ordinary diferential equations:

$$
f (x, u) = \left[ \begin{array}{c} v _ {\mathcal {I}} \\ m ^ {- 1} T _ {\mathcal {I}} \\ \frac {1}{2} q _ {\mathcal {B} \leftarrow \mathcal {I}} \otimes \omega_ {\mathcal {B}} \\ J ^ {- 1} \big (M _ {\mathcal {B}} - \omega_ {\mathcal {B}} ^ {\times} J \omega_ {\mathcal {B}} \big) \end{array} \right].\tag{153}
$$

The boundary conditions (39f) and (39g) are obtained from (132):

$$
g _ {\mathrm{ic}} \big (x (0), p \big) = \left[ \begin{array}{c} r _ {\mathcal {I}} (0) - r _ {0} \\ v _ {\mathcal {I}} (0) - v _ {0} \\ q _ {\mathcal {B} \leftarrow \mathcal {I}} (0) - q _ {0} \\ \omega_ {\mathcal {B}} (0) \end{array} \right],
$$

$$
g _ {\mathrm{tc}} \big (x (1), p \big) = \left[ \begin{array}{c} r _ {\mathcal {I}} (1) - r _ {f} \\ v _ {\mathcal {I}} (1) - v _ {f} \\ q _ {\mathcal {B} \leftarrow \mathcal {I}} (1) - q _ {f} \\ \omega_ {\mathcal {B}} (1) \end{array} \right].\tag{154a}
$$

(154b)

The dynamics are converted to normalized time in the same way as (120):

$$
f (x, u, p) = \alpha_ {\mathfrak {t}} f (x, u).\tag{155}
$$

The convex state and input path constraints (39c)- (39d) are straightforward. As for the quadrotor example, we leverage the mixed state-parameter nature of (39c) to include all of the convex state and parameter constraints. In particular, these are (110), (134), and (146b). Using the definition of time dilation, we translate (110) into the constraint:

$$
t _ {f, \mathrm{min}} \leq \alpha_ {\mathfrak {t}} \leq t _ {f, \mathrm{max}}.\tag{156}
$$

Using the definition of the concatenated slack SDF vector (151), we translate (146b) into the following con straints:

$$
\begin{array}{r l} \Delta_ {\mathrm{ss}, i k} \leq d _ {\mathrm{ss}, i} \big (r _ {\mathcal {I}} (t _ {k}) \big), & i = 1, \ldots , n _ {\mathrm{ss}}, \\ & k = 1, \ldots , N. \end{array}\tag{157}
$$

Consequently, the convex path constraint set in (39c) is given by:

$$
\begin{array}{c} \mathcal {X} = \big \{(x, p) \in \mathbb {R} ^ {1 3} \times \mathbb {R} ^ {1 + N n _ {\mathrm{ss}}}: (1 3 4), (1 5 6), \\ \text { and } (1 5 7) \text { hold } \big \}. \end{array}\tag{158}
$$

The convex input constraint set in (39d) is given simply by all the input vectors that satisfy (133).

The nonconvex path constraints (39e) for the free-flyer problem involve the ellipsoidal floating obstacles (113) and the approximate flight space constraint (147). The floating obstacle constraints are modeled exactly like fo the quadrotor using (122). For the flight space constraint, we leverage the concatenated slack SDF vector (151) and the eventual temporal discretization of the problem in order to impose (147) at each temporal grid node as follows:

$$
\mathsf {L} _ {\sigma} \big (\delta_ {\mathrm{ss}} ^ {k} \big) \geq 0, \quad k = 1, \ldots , N.\tag{159}
$$

Hence, the nonconvex path constraint function in (39e) can be written as $s : \mathbb { R } ^ { \bar { 3 } } \times \mathbb { R } ^ { N n _ { \mathrm { s s } } } \to \mathbb { R } ^ { n _ { \mathrm { o b s } } + 1 }$ . The first $n _ { \mathrm { o b s } }$ components are given by (122) and the last component is given by the negative left-hand side of (159).

It remains to define the running cost of the Bolza cost function (40). Like for the quadrotor, we scale the integrand in (149a) to be mindful of the penalty terms which the SCvx algorithm will add. Furthermore, we simplify the cost by neglecting time dilation and directly associating the absolute-time integral of (149a) with the normalized-time integral of (40). This yields the following convex running cost definition:

$$
\Gamma (x, u, p) = \left(\frac {\| T _ {\mathcal {I}} \| _ {2}}{T _ {\max}}\right) ^ {2} + \left(\frac {\| M _ {\mathcal {B}} \| _ {2}}{M _ {\max}}\right) ^ {2}.\tag{160}
$$

At this point, it may seem as though we are finished with formulating Problem 39 for SCvx. However, the seemingly innocuous flight space constraint (159) actually hides an important dificulty that we will now address. The importance of the following discussion cannot be overstated, as it can mean the diference between successful trajectory generation, and convergence to an infeasible trajectory (i.e., one with non-zero virtual control). In the case of the 6-DoF free-flyer, omission of the following discussion incurs a 40% optimality penalty for the value of (149a).

We begin investigating (159) by writing down its Jacobians, which SCvx will use for linearizing the constraint. Note that (159) is a function of only $\delta _ { \mathrm { s s } } ^ { k } \in \mathbb { R } ^ { n _ { \mathrm { s s } } }$ <sup>s</sup> , which is part of the concatenated slack SDF (151), and thus resides in the parameter vector. Hence, only the Jacobian (44g) is non-zero. Using the general softmax definition (144), the i-th element of $\nabla \mathsf { L } _ { \sigma } \bar { ( } \delta _ { \mathrm { s s } } ^ { k } )$ is given by:

$$
\frac {\partial \mathsf {L} _ {\sigma} \left(\delta_ {\mathrm{ss}} ^ {k}\right)}{\partial \delta_ {\mathrm{ss} , i} ^ {k}} = \left(\sum_ {j = 1} ^ {n _ {\mathrm{ss}}} e ^ {\sigma \delta_ {\mathrm{ss}, j} ^ {k}}\right) ^ {- 1} e ^ {\sigma \delta_ {\mathrm{ss}, i} ^ {k}}.\tag{161}
$$

When the slack SDF satisfies the lower-bound (157) with equality, the Jacobian (161) is an accurate representation of how the overall SDF (146a) changes due to small perturbations in the robot’s position. The problematic case occurs when this bound is loose. To illustrate the idea, suppose that the robot is located near the center of $\mathcal { O } _ { i } .$ , such that $d _ { \mathrm { s s } , i } ( r _ { \mathscr I } ( t _ { k } ) ) = 0 . 8$ . We assume that the rooms do not overlap and that the slack SDF values of the other rooms satisfy $\delta _ { \mathrm { s s } , j } ^ { k } = d _ { \mathrm { s s } , j } \big ( r _ { \mathcal { T } } ( t _ { k } ) \big ) = - 1$ for all $j \neq i .$ Since the robot is uniquely inside $\mathcal { O } _ { i }$ , the exact SDF (143) is locally a linear function of $d _ { \mathrm { s s } , i }$ and has a gradient $\partial d _ { \mathrm { s s } } / \partial d _ { \mathrm { s s } , i } = 1$ . Since we want the SCP subproblem to be an accurate local approximation of th nonconvex problem, we expect the same behavior for the approximate SDF (146a) for high values of σ. However, this may not be the case.

![](Malyuta2021Convex_figs/b6e007aa2c8f8089dcf34f4c2283eb436946454d5c01b42097709d517725e49d.jpg)  
FIGURE 29 Visualization of the effect of slackness in the SDF lowerbound constraint (146b) on the gradient of the approximate SDF (146a). This plot is obtained by setting ${ n _ { \mathrm { s s } } } = 6$ and $\delta _ { \mathrm { s s } , j } = - 1$ for all $j \neq i .$ The individual curves are obtained by gradually reducing $\delta _ { \mathrm { s s } , i }$ from its maximum value of $d _ { \mathrm { s s } , i }$ . As the sharpness parameter σ increases, a “cutoff” value appears, below which the approximate SDF becomes insensitive to changes in $\delta _ { \mathrm { s s } , i }$

Figure 29 illustrates what happens to the approximate SDF gradient (161) as the slackness in (157) increases. First, we note that when there is no slackness, increas ing the σ parameter does indeed make the approximate gradient converge to the exact value of one. However, as slackness grows, there is a distinct cutof value below which (161) becomes zero. This is known as a vanishing gradient problem, and has been studied extensivel for machine learning [229]. The core issue is that SCP relies heavily on gradient information in order to deter mine how to improve the feasibility and optimality of the subproblem solution. As an analogy, the gradient acts like a torchlight that illuminates the local surround ings in a dark room and allows one to take a step close to a light switch. When the gradient vanishes, so does the torchlight, and SCP no longer has information about which direction is best to take. Unless the solution is al ready locally optimal, a vanished gradient most often either blocks SCP from finding more optimal solutions, or forces it to use non-zero virtual control. The result is that the converged trajectory is either (heavily) subop timal or even infeasible.

Looking at Figure 29, one may ask, in order to recover gradient information, why does SCP not simply increase $\delta _ { \mathrm { s s } , i } ^ { k }$ above the vanishing threshold? But remember, it is the gradient that indicates that increasing $\delta _ { \mathrm { s s } , i } ^ { k }$ is a good approach in the first place. The situation is much like focusing your eyes on the flat region of the $\sigma = 5 0$ curve

## Favorable gradient behavior is instrumental for good performance.

on the very left in Figure 29. If you only saw the part of the curve for $\delta _ { \mathrm { s s } , i } ^ { k } / d _ { \mathrm { s s } , i } \big ( r _ { \mathcal { T } } ( t _ { k } ) \big ) \in [ - 3 , - 2 ]$ , you would also not know whether it is best to increase or decrease $\delta _ { \mathrm { s s } , i } ^ { k }$

Fortunately, the remedy is quite simple. Because (135) is a necessary and suficient condition, we know that slackness in (157) cannot be used to make the trajectory more optimal. In other words, a trajectory with non-zero slackness will not achieve a lower cost (149a). Hence, we simply need some way to incentivize the convex subproblem optimizer to make (157) hold with equality. Our approach is to introduce a terminal cost that maximizes the concatenated slack SDF:

$$
\phi (\Delta_ {\mathrm{ss}}) = - \varepsilon_ {\mathrm{ss}} \sum_ {k = 1} ^ {N} \sum_ {i = 1} ^ {n _ {\mathrm{ss}}} \Delta_ {\mathrm{ss}, i k},\tag{162}
$$

where $\varepsilon _ { \mathrm { s s } } ~ \in ~ \mathbb { R } _ { + + }$ is any user-chosen positive number. To make sure that (162) does not interfere with the extra penalty terms introduced by SCvx, we set $\varepsilon _ { \mathrm { s s } }$ to a very small but numerically tolerable value as shown in Table 4.

In summary, our investigation into (159) allowed us to identify a vanishing gradient issue. This resulted in a simple yet efective remedy in the form of a terminal cost (162). The discussion hopefully highlights three salient features of good modeling for SCP-based trajectory generation. First, SCP does not have equal performance for mathematically equivalent problem formulations (such as the free-flyer problem with and without (162)). Second, favorable gradient behavior is instrumental for good performance. Third, remedies to recover good performance for dificult problems are often surprisingly simple.

## GuSTO Formulation

Like for the quadrotor example, the GuSTO formulation is very similar to SCvx. We can express (160) as the quadratic running cost (68) as follows:

$$
S (p) = \mathrm{diag} \left(T _ {\max} ^ {- 2} I _ {3}, M _ {\max} ^ {- 2} I _ {3}\right),\tag{163a}
$$

$$
\ell (x, p) = 0,\tag{163b}
$$

$$
g (x, p) = 0.\tag{163c}
$$

The dynamics (153) are also cast into the control afine form (69):

$$
f _ {0} (x, p) = \left[ \begin{array}{c} v _ {\mathcal {I}} \\ 0 \\ \frac {1}{2} q _ {\mathcal {B} \leftarrow \mathcal {I}} \otimes \omega_ {\mathcal {B}} \\ - J ^ {- 1} \big (\omega_ {\mathcal {B}} ^ {\times} J \omega_ {\mathcal {B}} \big) \end{array} \right],\tag{164a}
$$

$$
f _ {i} (x, p) = \left[ \begin{array}{c} 0 \\ m ^ {- 1} e _ {i} \\ 0 \\ 0 \end{array} \right], \quad i = 1, 2, 3,\tag{164b}
$$

$$
f _ {i} (x, p) = \left[ \begin{array}{c} 0 \\ 0 \\ 0 \\ J ^ {- 1} e _ {i} \end{array} \right], \quad i = 4, 5, 6,\tag{164c}
$$

where $e _ { i } \in \mathbb { R } ^ { 3 }$ is the i-th standard basis vector. Just like for the quadrotor, we are “done” at this point and the rest of the optimization model is exactly the same as for SCvx in the last section.

## Initial Trajectory Guess

The initial trajectory guess is based on some simple in tuition about what a feasible free-flyer trajectory might look like. Although this guess is more complicated than the straight-line initialization used for the quadrotor, it is based on purely kinematic considerations. This make the guess quick to compute but also means that it does not satisfy the dynamics and obstacle constraints. The fact that SCP readily morphs this coarse guess into a feasible and locally optimal trajectory corroborates the efectiveness of SCP methods for high-dimensional non convex trajectory generation tasks.

To begin, the time dilation $\alpha _ { \mathrm { t } }$ is obtained by averaging the final time bounds as in (129). An “L-shape” path is then used for the position trajectory guess. In particular, recall that according to (132a), the free-flyer has to go from $r _ { 0 }$ to $r _ { f }$ . We define a constant velocity trajectory which closes the gap between $r _ { 0 }$ and $r _ { f }$ along the first axis, then the second, and finally the third, in a total time of $\alpha _ { \mathrm { t } }$ seconds. The trajectory thus consists of three straight legs with sharp 90 degree turns at the transition points, which is akin to the Manhattan or taxicab geome try of the one-norm [230]. The velocity is readily derived from the position trajectory, and is a constant-norm vec tor whose direction changes twice to align with the ap propriate axis in each trajectory leg. Furthermore, we initialize the concatenated slack SDF parameter vector (151) by evaluating (141) along the position trajector guess for each room and discrete-time grid node.

The attitude trajectory guess is only slightly more in volved, and it is a general procedure that we can recom mend for attitude trajectories. According to (132c), the free-flyer has to rotate between the attitudes encoded b $q _ { 0 }$ and $q _ { f }$ . Since quaternions are not additive and must maintain a unit norm to represent rotation, straight-lin interpolation from $q _ { 0 }$ to $q _ { f }$ is not an option. Instead, we use spherical linear interpolation (SLERP) [188, 231]. This operation performs a continuous rotation from q<sub>0</sub> to $q _ { f }$ at a constant angular velocity around a fixed axis. To define the operation, we introduce the exponential and logarithmic maps for unit quaternions:

$$
\operatorname{Exp} (q) \triangleq \alpha u, \text {   where   } \alpha \in \mathbb {R}, u \in \mathbb {R} ^ {3},\tag{165a}
$$

$$
\operatorname{Log} \left(\alpha u\right) \triangleq \left[ \begin{array}{c} u \sin (\alpha / 2) \\ \cos (\alpha / 2) \end{array} \right].\tag{165b}
$$

The exponential map converts a unit quaternion to its equivalent angle-axis representation. The logarithmic map converts an angle-axis rotation back to a quaternion, which we write here in the vectorized form used to implement $q _ { B  \mathcal { I } }$ in (131c). SLERP for the attitude quaternion $q _ { B  \mathcal { I } }$ can then be defined by leveraging (165):

$$
q _ {e} = q _ {0} ^ {*} \otimes q _ {f},\tag{166a}
$$

$$
q _ {\mathcal {B} \leftarrow \mathcal {I}} (t) = q _ {0} \otimes \mathsf {E x p} \left(t \mathsf {L o g} (q _ {e})\right),\tag{166b}
$$

where $q _ { e }$ is the error quaternion between $q _ { f }$ and $q _ { 0 } ,$ and $t \in [ 0 , 1 ]$ is an interpolation parameter such that $q _ { { \boldsymbol { B } }  \tau } ( 0 ) = q _ { 0 }$ and $q _ { { \boldsymbol { \mathsf { B } } }  { \boldsymbol { \mathsf { T } } } } ( 1 ) = q _ { f }$ . The angular velocity trajectory guess is simple to derive, since SLERP performs a constant velocity rotation around a fixed axis. Using (166a):

$$
\omega_ {\mathcal {B}} (t) = \alpha_ {\mathfrak {t}} ^ {- 1} \mathsf {L o g} (q _ {e}).\tag{167}
$$

The free-flyer is a very low thrust vehicle to begin with. By using (149a), we are in some sense searching for the lowest of low thrust trajectories. Hence, we expect the control inputs $T _ { \mathcal { I } }$ and $M _ { B }$ to be small. Without any further insight, it is hard to guess what the thrust and torque would look like for a 6-DoF vehicle in a microgravity environment. Hence, we simply set the initial control guess to zero.

## Numerical Results

We now have a specialized instance of Problem 39 and an initialization strategy for the 6-DoF free-flyer problem. The trajectory solution is generated using SCvx and GuSTO with temporal discretization performed using the FOH interpolating polynomial method in “Discretizing Continuous-time Optimal Control Problems”. The algorithm parameters are provided in Table 4, where the initial and final quaternion vectors are expressed in degrees using the angle-axis representation of (165a). ECOS is used as the numerical convex optimizer, and the full implementation is available in the code reposi tory linked in Figure 2.

TABLE 5 Breakdown of subproblem size for the 6- DoF free-flyer example.

<table><tr><td></td><td>SCvx</td><td>GuSTO</td></tr><tr><td>Variables</td><td>2267</td><td>3352</td></tr><tr><td>Affine equalities</td><td>663</td><td>663</td></tr><tr><td>Affine inequalities</td><td>350</td><td>1650</td></tr><tr><td>One-norm cones</td><td>49</td><td>0</td></tr><tr><td>Infinity-norm cones</td><td>401</td><td>351</td></tr><tr><td>Second-order cones</td><td>200</td><td>200</td></tr></table>

The convergence processes for SCvx and GuSTO are shown in Figure 30. We have again set $\varepsilon = \varepsilon _ { \mathrm { r } } = 0$ so that we can observe the convergence process for exactly 15 iterations. At each iteration, the algorithms solve a convex subproblem whose size is documented in Ta ble 5. Note that the subproblems of both algorithms are substantially larger than for the quadrotor example, and represent a formidable increase in dimensionality fo the numerical problem. However, modern IPMs easil handle problems of this size and we will see that the in creased variable and constraint count is of little concern. We further note that the larger number of variables and afine inequalities for $\mathrm { G u S T O }$ is due to how our imple mentation uses extra slack variables to encode the soft penalty function (70). Because GuSTO does not use a dynamics virtual control, it has no one-norm cones, while SCvx has several such cones to model the virtual con trol penalty (48). Due to its larger subproblem size and slightly more complicated code for including constraints as soft penalties, the “solve” and “formulate” times per subproblem are slightly larger for GuSTO in this exam ple. Nevertheless, both algorithms have roughly equa runtimes, and GuSTO has the advantage of converging to a given tolerance in slightly fewer iterations.

The converged trajectories are plotted in Figures 3 and 32. The left subplots in Figures 31a and 31b show a remarkably similar evolution of the initial guess into the converged trajectory. The final trajectories are visually identical, and both algorithms discover that the maximum allowed flight time of $t _ { f , \mathrm { m a x } }$ is control energy optimal, as expected.

Lastly, Figure 33 plots the evolution of the nonconvex flight space and obstacle avoidance inequalities (147) and (113). Our first observation is that the constraints hold at the discrete-time nodes, and that the free-flyer ap proaches the ellipsoidal obstacles quite closely. This is similar to how the quadrotor brushes against the obsta cles in Figure 23, and is a common feature of time- or energy-optimal trajectories in a cluttered environment. Our second observation concerns the sawtooth-like non smooth nature of the SDF time history. Around t = 25 s and t = 125 s, the approximate SDF comes close to zero even though the position trajectory in Figure 31 is not near a wall at those times. This is a consequence of our modeling, since the SDF is near-zero at the room in terfaces (see Figures 27 and 28), even though these are not physical “walls”. However, around $\mathrm {  ~ t ~ } = \mathrm { 1 0 0 ~ s } ,$ the flight space constraint (147) is actually activated as the free-flyer rounds a corner. Roughly speaking, this is in tuitively the optimal thing to do. Like a Formula One driver rounding a corner by following the racing line, the free-flyer spends less control efort by following the shortest path. An unfortunate consequence is that this results in minor clipping of the continuous-time flight space constraint. The issue can be mitigated by the same strategies as proposed in the last section for the quadrotor example [191, 192].

![](Malyuta2021Convex_figs/2445200497756c9e695604be76de744d1a24ce58395ec86a724c0c010b7f61fd.jpg)

![](Malyuta2021Convex_figs/71c58114272f36a6e3ee6d7f533cc4a9b09f47335d7354371b52015bed5b0c66.jpg)  
(a) SCvx.

![](Malyuta2021Convex_figs/882df14d280bf5ac8203f17b244fea3c212c481d9c71c6f261e662ee349942b2.jpg)

![](Malyuta2021Convex_figs/6c8f95657e2087afd0ae7d7670418a926cd18e5564e45631dea95daa8cd3f778.jpg)  
(b) GuSTO.  
FIGURE 30 Convergence and runtime performance for the 6-DoF free-flyer problem. Both algorithms take a similar amount of time to converge. The runtime subplots in the bottom row show statistics on algorithm performance over 50 executions. GuSTO converges slightly faster for thi example and, although both algorithms reach numerical precision for practical purposes, GuSTO converges all the way down to a $1 0 ^ { - 1 4 }$ tolerance. The plots are generated according to the same description as for Figure 24.

## CONCLUSIONS

Modern vehicle engineering is moving in the direction of increased autonomy. This includes aerospace, automotive, and marine transport, as well as robots on land, in the air, and in our homes. No matter the application, a common feature across autonomous systems is the basic requirement to generate trajectories. In a general sense, trajectories serve like plans to be executed in order for the system to complete its task. Due to the large scale of deployment and/or the safety-critical nature of the system, reliable real-time onboard trajectory generation has never been more important.

This article takes the stance that convex optimization is a prime contender for the job, thanks to 40 years of optimization research having produced a remarkable suite of numerical methods for quickly and reliably solving convex problems [26, 29, 34]. Many of these methods are now packaged as either commercial or open-source of-the-shelf codes [216, 232]. This makes the injection of convex optimization into an autonomous system easier than ever before, provided that the right high-level algorithms exist to leverage it.

To leverage convex optimization for the dificult task of nonconvex trajectory generation, this article provides an expansive tutorial of three algorithms. First, the lossless convexification (LCvx) algorithm is introduced to remove acute nonconvexities in the control input constraints. This provides an optimal control theory-backed way to transform certain families of nonconvex trajector generation tasks into ones that can be solved in one shot by a convex optimizer. A variable-mass rocket landing example at the end of the article illustrates a real-world application of the LCvx method.

Not stopping there, the article then motivates an en tire family of optimization methods called sequential convex programming (SCP). These methods use a linearizesolve loop whereby a convex optimizer is called several times until a locally optimal trajectory is obtained. SCP strikes a compelling middleground between “what is pos sible” and “what is acceptable” for safety-critical real time trajectory generation. In particular, SCP inher its much from trust region methods in numerical opti mization, and its performance is amenable to theoretica analysis using standard tools of analysis, constrained optimization, and optimal control theory [11, 29, 47]. This articles provides a detailed overview of two specific and closely related SCP algorithms called SCvx and GuSTO [49, 50]. To corroborate their efectiveness for dificult trajectory generation tasks, two numerical examples are presented based on a quadrotor and a space-station freeflyer maintenance robot.

![](Malyuta2021Convex_figs/74fe8fe3a87f1957929c2bd7fa60434e1ab71ea1d5deb1fce33d3b28c4c8c4e6.jpg)

![](Malyuta2021Convex_figs/d780cb4297f735e35ebf41f85d96601ec1d92375ed218c2f9761f1ae84114967.jpg)  
(a) SCvx.

![](Malyuta2021Convex_figs/0c10a98960a9905d1ec5655a1bfea4625d0fc923b90248692fbecca7c3f5dfdc.jpg)

![](Malyuta2021Convex_figs/37e9c1705170c88133dc8456dda6dcc7b31a52b1bcb5e1daa3ef7d318dcc2634.jpg)  
(b) GuSTO.

FIGURE 31 The position trajectory evolution (left) and the final converged trajectory (right) for the 6-DoF free-flyer problem. In the right plots for each algorithm, the continuous-time trajectory is obtained by numerically integrating the dynamics (131). The fact that this trajectory passes through the discrete-time subproblem solution confirms dynamic feasibility.  
![](Malyuta2021Convex_figs/a7e118923ab6e8c749ca150dfb84252b5d9ff4b7524e85339d6eb741dd676a76.jpg)

![](Malyuta2021Convex_figs/e898c918fac0d1a0f8dcc244e608f7949115fbcaa79816fd06c9c6169b0ef9b3.jpg)

![](Malyuta2021Convex_figs/52dd97c5a01fd7fb25224c12697976611857737efcc7be58f018f5008458f5b5.jpg)

![](Malyuta2021Convex_figs/ed84e7e4fb1f38448f1d7d7c75c8744608cc724c20699f67c6a39e042832c42b.jpg)

![](Malyuta2021Convex_figs/1b4209f0fa18e60958eba192d57b728c0a7fa6bfd6ff611b50b4f29366ac1802.jpg)

![](Malyuta2021Convex_figs/3605e199e799d27f41d3aed9ce84253ff2a39109d71753f616874fadf3b4f3f1.jpg)  
FIGURE 32 State and control time histories for the converged trajectory of the 6-DoF free-flyer problem. These are visually identical for SCvx and GuSTO, so we only show a single plot. Euler angles using the intrinsic Tait-Bryan convention are shown in place of the quaternion attitude. Like in Figure 25, the dots represent the discrete-time solution while the continuous lines are obtained by propagating the solution through the actual continuous-time dynamics (39b).

FIGURE 33 Signed distance function and obstacle avoidance time histories for the converged trajectory of the 6-DoF free-flyer problem. Like for Figure 32, these are visually identical for SCvx and GuSTO, so we only show a single plot. Note the highly nonlinear nature of the SDF, whose time history exhibits sharp corners as the robot traverses the feasible flight space. Although the SDF constraint (159) is satisfied at the discrete-time nodes, minor inter-sample constraint clipping occurs around 100 seconds as the robot rounds a turn in the middle of its trajectory (see Figure 31).

The theory behind LCvx, SCvx, and GuSTO is rel atively new and under active research, with the oldest method in this article (i.e., classical LCvx [84]) bein just 15 years old. We firmly believe that neither one of the methods has attained the limits of its capabilities, and this presents the reader with an exciting opportunit to contribute to the efort. It is clear to us that convex optimization has a role to play in the present and future of advanced trajectory generation. With the help of this article and the associated source code, we hope that the reader now has the knowledge and tools to join in the adventure.

## ACKNOWLEDGEMENTS

This work was supported in part by the National Science Foundation, Cyber-Physical Systems (CPS) pro gram (award 1931815), by the Ofice of Naval Research,

ONR YIP Program (contract N00014-17-1-2433), and by the King Abdulaziz City for Science and Technology (KACST). The authors would like to extend their gratitude to Yuanqi Mao for his invaluable inputs on sequential convex programming algorithms, to Abhinav Kamath for his meticulous review of every detail, and to Jonathan P. How for the initial encouragement to write this article.

## AUTHOR INFORMATION

Danylo Malyuta received the B.Sc. degree in Mechanical Engineering from EPFL and the M.Sc. degree in Robotics, Systems and Control from ETH Z¨urich. He is currently a Ph.D. candidate in the Autonomous Controls Lab at the Department of Aeronautics and Astronautics of the University of Washington. His research is primarily focused on computationally eficient optimization-based control of dynamical systems. Danylo has held internship positions at the NASA Jet Propulsion Laboratory, NASA Johnson Space Center, and Amazon Prime Air.

Taylor P. Reynolds received the B.S. degree in Mathematics & Engineering from Queen’s University in 2016. He received the Ph.D. degree from the Department of Aeronautics & Astronautics at the University of Washington in 2020 under the supervision of Mehran Mesbahi. During his Ph.D., Taylor worked with NASA JSC and Draper Laboratories to develop advanced guidance algorithms for planetary landing on the SPLICE project, and also co-founded the Aeronautics & Astronautics CubeSat Team at the University of Washington. He now works as a Research Scientist at Amazon Prime Air.

Michael Szmuk received the B.S. and M.S. degrees in Aerospace Engineering from the University of Texas at Austin. In 2019, he received the Ph.D. degree while working in the Autonomous Controls Lab at the Department of Aeronautics and Astronautics of the University of Washington, under the supervision of Beh¸cet A¸cıkme¸se. During his academic career, he completed internships at NASA, AFRL, Emergent Space, Blue Origin, and Amazon Prime Air. He now works as a Research Scientist at Amazon Prime Air, specializing in the design of flight control algorithms for autonomous air delivery vehicles.

Thomas Lew is a Ph.D. candidate in Aeronautics and Astronautics at Stanford University. He received the B.Sc. degree in Microengineering from Ecole Polytech-<sup>´</sup> nique F´ed´erale de Lausanne in 2017 and the M.Sc. degree in Robotics from ETH Z¨urich in 2019. His research focuses on the intersection between optimal control and machine learning techniques for robotics and aerospace applications.

Riccardo Bonalli obtained the M.Sc. degree in Mathematical Engineering from Politecnico di Milano, Italy in 2014 and the Ph.D. degree in applied mathematics from Sorbonne Universit´e, France in 2018 in collaboration with ONERA – The French Aerospace Lab. He is recipient of the ONERA DTIS Best Ph.D. Student Award 2018. He is now a postdoctoral researcher at the Department of Aeronautics and Astronautics at Stanford University. His main research interests concern theoretical and numerical robust optimal control with applications in aerospace systems and robotics.

Marco Pavone is an Associate Professor of Aeronau tics and Astronautics at Stanford University, where he is the Director of the Autonomous Systems Laboratory. Before joining Stanford, he was a Research Technologist within the Robotics Section at the NASA Jet Propulsion Laboratory. He received the Ph.D. degree in Aeronau tics and Astronautics from the Massachusetts Institute of Technology in 2010. His main research interests are in the development of methodologies for the analysis, design, and control of autonomous systems, with an emphasis on self-driving cars, autonomous aerospace vehi cles, and future mobility systems. He is a recipient of a number of awards, including a Presidential Early Ca reer Award for Scientists and Engineers, an ONR YIP Award, an NSF CAREER Award, and a NASA Earl Career Faculty Award. He was identified by the Ameri can Society for Engineering Education (ASEE) as one of America’s 20 most highly promising investigators under the age of 40. He is currently serving as an Associate Editor for the IEEE Control Systems Magazine.

Beh¸cet A¸cıkme¸se is a Professor at the Universit of Washington, Seattle. He received the Ph.D. degree in Aerospace Engineering from Purdue University. He was a senior technologist at the NASA Jet Propulsion Laboratory (JPL) and a lecturer at the California In stitute of Technology. At JPL, he developed contro algorithms for planetary landing, spacecraft formation flying, and asteroid and comet sample return missions. He developed the “flyaway” control algorithms used successfully in NASA’s Mars Science Laboratory (MSL) and Mars 2020 missions during the landings of Curiosity and Perseverance rovers on Mars. He is a recipient of the NSF CAREER Award, the IEEE Award for Technical Excellence in Aerospace Control, and numerous NASA Achievement awards for his contributions to NASA mis sions and technology development. His research interests include optimization-based control, nonlinear and robust control, and stochastic control.

## REFERENCES

[1] Rafaello D’Andrea. “Guest Editorial Can Drones Deliver?” In: IEEE Transactions on Automation Science and Engineering 11.3 (July 2014), pp. 647–648. <sup>doi</sup>: 10.1109/tase.2014.2326952.

[2] A. Miguel San Martin and Edward C. Lee Steven W. Wong. “The development of the MSL guidance, navigation, and control system for entry, descent, and landing”. In: 23rd Space Flight Mechanics Meeting. 2013.

[3] Adam D. Steltzner et al. “Mars Science Laboratory Entry, Descent, and Landing System Development Challenges”. In: Journal

of Spacecraft and Rockets 51.4 (July 2014), pp. 994–1003. <sup>doi</sup>: 10.2514/1.a32866.

[4] David W. Way et al. “Mars Science Laboratory: Entry, Descent, and Landing System Performance”. In: 2007 IEEE Aerospace Conference. IEEE, 2007. <sup>doi</sup>: 10.1109/aero.2007.352821.

[5] Gunter Stein. “Respect the unstable”. In: IEEE Control Systems 23.4 (Aug. 2003), pp. 12–25. <sup>doi</sup>: 10.1109/mcs.2003.1213600.

[6] Danylo Malyuta et al. “Advances in Trajectory Optimization for Space Vehicle Control”. In: Annual Reviews in Control (2021). under review.

[7] David A. Mindell. Digital Apollo. MIT Press, 2008. <sup>isbn</sup>: 9780262134972.

[8] John M. Carson III et al. “The SPLICE Project: Continuing NASA Development of GN&C Technologies for Safe and Precise Landing”. In: AIAA Scitech 2019 Forum. American Institute of Aeronautics and Astronautics, Jan. 2019. <sup>doi</sup>: 10.2514/6.2019- 0660.

[9] Daniel Dueri et al. “Customized Real-Time Interior-Point Methods for Onboard Powered-Descent Guidance”. In: Journal of Guidance, Control, and Dynamics 40.2 (Feb. 2017), pp. 197–212. <sup>doi</sup>: 10.2514/1.g001480.

[10] NASA. The Mars 2020 Rover’s “Brains”. https : / / mars . nasa.gov/mars2020/spacecraft/rover/brains/. 2020.

[11] Lev S. Pontryagin et al. The Mathematical Theory of Optimal Processes. Montreux: Gordon and Breach Science Publishers, 1986. <sup>doi</sup>: 10.1201/9780203749319.

[12] Leonard D. Berkovitz. Optimal Control Theory. Springer New York, 1974. <sup>doi</sup>: 10.1007/978-1-4757-6097-2.

[13] John T. Betts. Practical Methods for Optimal Control and Estimation Using Nonlinear Programming. SIAM, 2010. <sup>isbn</sup>: 9780898716887. <sup>doi</sup>: 10.1137/1.9780898718577.

[14] D.F. Lawden. Optimal Trajectories for Space Navigation. London: Butterworths, 1963.

[15] J-P. Marec. Optimal Space Trajectories. Amsterdam: Elsevier Scientific Publishing Company, 1979. <sup>isbn</sup>: 0444418121. <sup>doi</sup>: 10. 1002/oca.4660040210.

[16] Arthur Earl Bryson Jr. and Yu-Chi Ho. Applied Optimal Control. Washington, D.C.: Hemisphere Publishing Corporation, 1975. <sup>isbn</sup>: 0470114819.

[17] Donald E. Kirk. Optimal Control Theory: An Introduction. Englewood Clifs, NJ: Prentice-Hall, 1970. <sup>isbn</sup>: 9780486434841.

[18] James M Longuski, Jos´e J. Guzm´an, and John E. Prussing. Optimal Control with Aerospace Applications. Springer New York, 2014. <sup>doi</sup>: 10.1007/978-1-4614-8945-0.

[19] J. Meditch. “On the problem of optimal thrust programming for a lunar soft landing”. In: IEEE Transactions on Automatic Control 9.4 (Oct. 1964), pp. 477–484. <sup>doi</sup>: 10 . 1109 / tac . 1964 . 1105758.

[20] Manfred Morari and Jay H Lee. “Model predictive control: past, present and future”. In: Computers & Chemical Engineering 23.4-5 (1999), pp. 667–682.

[21] John W Eaton and James B Rawlings. “Model-predictive control of chemical processes”. In: Chemical Engineering Science 47.4 (1992), pp. 705–720.

[22] Peter J Campo and Manfred Morari. “Robust model predictive control”. In: 1987 American control conference. IEEE. 1987, pp. 1021–1026.

[23] Frauke Oldewurtel et al. “Use of model predictive control and weather forecasts for energy eficient building climate control”. In: Energy and Buildings 45 (2012), pp. 15–27.

[24] Yudong Ma et al. “Model predictive control for the operation of building cooling systems”. In: IEEE Transactions on control systems technology 20.3 (2011), pp. 796–803.

[25] Sorin C Bengea et al. “Implementation of model predictive control for an HVAC system in a mid-size commercial building”. In: HVAC&R Research 20.1 (2014), pp. 121–135.

[26] Stephen Boyd and Lieven Vandenberghe. Convex Optimization. Cambridge, UK: Cambridge University Press, 2004. <sup>isbn</sup>: 9780521833783.

[27] John T. Betts. “Survey of numerical methods for trajectory optimization”. In: Journal of Guidance, Control, and Dynamics 21.2 (1998), pp. 193–207. <sup>doi</sup>: 10.2514/2.4231.

[28] Matthew Kelly. “An Introduction to Trajectory Optimization: How to Do Your Own Direct Collocation”. In: SIAM Review 59.4 (Jan. 2017), pp. 849–904. <sup>doi</sup>: 10.1137/16m1062569.

[29] J. Nocedal and S. Wright. Numerical Optimization. Springer New York, 1999. <sup>isbn</sup>: 9780387303031. <sup>doi</sup>: 10.1007/978-0-387- 40065-5.

[30] R. Tyrrell Rockafellar. “Lagrange Multipliers and Optimal ity”. In: SIAM Review 35.2 (June 1993), pp. 183–238. <sup>doi</sup>: 10 . 1137/1035044.

[31] Stephen J. Wright. Primal-Dual Interior-Point Methods. Society for Industrial and Applied Mathematics, Jan. 1997. <sup>doi</sup>: 10. 1137/1.9781611971453.

[32] Philip E. Gill, Walter Murray, and Margaret H. Wright. Practical Optimization. Society for Industrial and Applied Mathematics, Jan. 2019. <sup>doi</sup>: 10.1137/1.9781611975604.

[33] C. Roos, T. Terlaky, and J.-Ph. Vial. Theory and Algorithms for Linear Optimization: An Interior Point Approach. Wiley, Oct. 2000. <sup>isbn</sup>: 9780470865934.

[34] Margaret H. Wright. “The interior-point revolution in opti mization: history, recent developments, and lasting consequences”. In: BULL. AMER. MATH. SOC. (N.S) 42 (2005), pp. 39–56.

[35] Jiming Peng, Cornelis Roos, and Tam´as Terlaky. “Primal-Dual Interior-Point Methods for Second-Order Conic Optimization Based on Self-Regular Proximities”. In: SIAM Journal on Optimization 13.1 (Jan. 2002), pp. 179–203. <sup>doi</sup>: 10.1137/s1052623401383236.

[36] Lars Blackmore. “Autonomous Precision Landing of Space Rockets”. In: The Bridge 4.46 (Dec. 2016), pp. 15–20.

[37] Daniel P. Scharf et al. “Implementation and Experimental Demonstration of Onboard Powered-Descent Guidance”. In: Journal of Guidance, Control, and Dynamics 40.2 (Feb. 2017), pp. 213– 229. <sup>doi</sup>: 10.2514/1.g000399.

[38] JPL and Masten Space Systems. 500 meter divert Xombie test flight for G-FOLD, Guidance for Fuel Optimal Large Divert validation. http://www.youtube.com/watch?v=1GRwimo1AwY. Aug 2012.

[39] JPL and Masten Space Systems. 750 meter divert Xombie test flight for G-FOLD, Guidance for Fuel Optimal Large Divert, validation. http://www.youtube.com/watch?v=jl6pw2oossU. July 2012.

[40] Brian Paden et al. “A Survey of Motion Planning and Control Techniques for Self-Driving Urban Vehicles”. In: IEEE Transactions on Intelligent Vehicles 1.1 (Mar. 2016), pp. 33–55. <sup>doi</sup>: 10.1109/tiv.2016.2578706.

[41] Martin Buehler, Karl Iagnemma, and Sanjiv Singh, eds. The DARPA Urban Challenge: Autonomous Vehicles in City Trafic. Springer Berlin Heidelberg, 2009. <sup>doi</sup>: 10.1007/978-3-642-03991- 1.

[42] Russell Buchanan et al. “Perceptive whole-body planning for multilegged robots in confined spaces”. In: Journal of Field Robotics 38.1 (June 2020), pp. 68–84. <sup>doi</sup>: 10.1002/rob.21974.

[43] Jean-Pierre Sleiman et al. “A Unified MPC Framework for Whole-Body Dynamic Locomotion and Manipulation”. In: IEEE Robotics and Automation Letters 6.3 (July 2021), pp. 4688–4695. doi<sub>: .</sub>

[44] Elia Kaufmann et al. “Deep Drone Racing: Learning Agile Flight in Dynamic Environments”. In: Proceedings of The 2nd Conference on Robot Learning. Ed. by Aude Billard et al. Vol. 87. Proceedings of Machine Learning Research. PMLR, Oct. 2018, pp. 133–145.

[45] Beh¸cet A¸cıkme¸se and Scott R. Ploen. “Convex Programming Approach to Powered Descent Guidance for Mars Landing”. In:

Journal of Guidance, Control, and Dynamics 30.5 (Sept. 2007), pp. 1353–1366. <sup>doi</sup>: 10.2514/1.27553.

[46] Lars Blackmore, Beh¸cet A¸cıkme¸se, and John M. Carson III. “Lossless convexification of control constraints for a class of nonlin ear optimal control problems”. In: Systems & Control Letters 61.8 (Aug. 2012), pp. 863–870. <sup>doi</sup>: 10.1016/j.sysconle.2012.04.010.

[47] Andrew R. Conn, Nicholas I. M. Gould, and Philippe L. Toint. Trust Region Methods. SIAM, Philadelphia, PA, 2000. <sup>doi</sup>: 10 . 1137/1.9780898719857.

[48] Mykel J. Kochenderfer and Tim A. Wheeler. Algorithms for Optimization. Cambridge, Massachusetts: The MIT Press, 2019. <sup>isbn</sup>: 9780262039420.

[49] Yuanqi Mao, Michael Szmuk, and Behcet Acikmese. “Successive Convexification: A Superlinearly Convergent Algorithm fo Non-convex Optimal Control Problems”. In: arXiv e-prints (2018). arXiv: 1804.06539.

[50] R. Bonalli et al. “GuSTO: Guaranteed Sequential Trajectory Optimization via Sequential Convex Programming”. In: IEEE International Conference on Robotics and Automation. 2019, pp. 6741–6747. <sup>doi</sup>: 10.1109/ICRA.2019.8794205.

[51] Matthew W. Harris and Beh¸cet A¸cıkme¸se. “Maximum Divert for Planetary Landing Using Convex Optimization”. In: Journal of Optimization Theory and Applications 162.3 (Dec. 2013), pp. 975– 995. <sup>doi</sup>: 10.1007/s10957-013-0501-7.

[52] M. Szmuk et al. “Convexification and real-time on-board optimization for agile quad-rotor maneuvering and obstacle avoidance”. In: IEEE/RSJ International Conference on Intelligent Robots and Systems. Vancouver, Canada, 2017, pp. 4862–4868. <sup>doi</sup>: 10.1109/IROS.2017.8206363.

[53] Xinfu Liu, Zuojun Shen, and Ping Lu. “Entry Trajectory Optimization by Second-Order Cone Programming”. In: Journal of Guidance, Control, and Dynamics 39.2 (Feb. 2016), pp. 227–241. <sup>doi</sup>: 10.2514/1.g001210.

[54] Zhenbo Wang and Michael J. Grant. “Constrained Trajectory Optimization for Planetary Entry via Sequential Convex Programming”. In: Journal of Guidance, Control, and Dynamics 40.10 (Oct. 2017), pp. 2603–2615. <sup>doi</sup>: 10.2514/1.g002150.

[55] Xinfu Liu. “Fuel-Optimal Rocket Landing with Aerodynamic Controls”. In: Journal of Guidance, Control, and Dynamics 42.1 (Jan. 2019), pp. 65–77. <sup>doi</sup>: 10.2514/1.g003537.

[56] Matthew W. Harris and Beh¸cet A¸cıkme¸se. “Minimum Time Rendezvous of Multiple Spacecraft Using Diferential Drag”. In: Journal of Guidance, Control, and Dynamics 37.2 (Mar. 2014), pp. 365–373. <sup>doi</sup>: 10.2514/1.61505.

[57] Danylo Malyuta and Beh¸cet A¸cıkme¸se. “Lossless convexification of non-convex optimal control problems with disjoint semicontinuous inputs”. In: Preprint (Nov. 2019), arXiv:1902.02726.

[58] Michael Szmuk, Behcet Acikmese, and Andrew W. Berning. “Successive Convexification for Fuel-Optimal Powered Landing with Aerodynamic Drag and Non-Convex Constraints”. In: AIAA Guidance, Navigation, and Control Conference. American Institute of Aeronautics and Astronautics, Jan. 2016. <sup>doi</sup>: 10.2514/6.2016-0378.

[59] Michael Szmuk, Taylor P Reynolds, and Beh¸cet A¸cıkme¸se. “Successive Convexification for Real-Time 6-DoF Powered Descen Guidance with State-Triggered Constraints”. In: Journal of Guidance, Control, and Dynamics 48.8 (2020), pp. 1399–1413. <sup>doi</sup>: 10.2514/1.G004549.

[60] Michael Szmuk and Beh¸cet A¸cıkme¸se. “Successive Convexifi cation for 6-DoF Mars Rocket Powered Landing with Free-Final Time”. In: 2018 AIAA Guidance, Navigation, and Control Conference. American Institute of Aeronautics and Astronautics, Jan. 2018 DQI: 10.2514/6. 2018-0617

[61] Michael Szmuk et al. “Successive Convexification for 6-DoF Powered Descent Guidance with Compound State-Triggered Constraints”. In: AIAA Scitech 2019 Forum. American Institute of Aeronautics and Astronautics, Jan. 2019. <sup>doi</sup>: 10.2514/6.2019- 0926.

[62] Taylor P. Reynolds et al. “Dual Quaternion-Based Powered Descent Guidance with State-Triggered Constraints”. In: Journal of Guidance, Control, and Dynamics 43.9 (Sept. 2020), pp. 1584– 1599. <sup>doi</sup>: 10.2514/1.g004536.

[63] Taylor P. Reynolds et al. “A Real-Time Algorithm for Non-Convex Powered Descent Guidance”. In: AIAA SciTech Forum. AIAA, 2020. <sup>doi</sup>: 10.2514/6.2020-0844

[64] Yuanqi Mao et al. “Successive Convexification of Non-Convex Optimal Control Problems with State Constraints”. In: IFAC-PapersOnLine 50.1 (2017), pp. 4063–4069. <sup>doi</sup>: 10.1016/j.ifacol.2017.08.789.

[65] Michael Szmuk et al. “Real-Time Quad-Rotor Path Planning Using Convex Optimization and Compound State-Triggered Constraints”. In: 2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, Nov. 2019. <sup>doi</sup>: 10.1109/ iros40897.2019.8967706.

[66] Danylo Malyuta et al. “Fast Trajectory Optimization via Successive Convexification for Spacecraft Rendezvous with Integer Constraints”. In: AIAA Scitech 2020 Forum. American Institute of Aeronautics and Astronautics, Jan. 2020. <sup>doi</sup>: 10.2514/6.2020-0616

[67] Taylor Reynolds et al. “SOC-i: A CubeSat Demonstration of Optimization-Based Real-Time Constrained Attitude Control”. In: 2021 IEEE Aerospace Conference. IEEE, Mar. 2021.

[68] NASA. NASA Tipping Point Partnership with Blue Ori gin to Test Precision Lunar Landing Technologies. https : //www.nasa.gov/directorates/spacetech/NASA\_Tipping\_Point\_ Partnership \_ to \_ Test \_ Precision \_ Lunar \_ Landing \_ Tech/. Sept. 2020.

[69] R. Bonalli et al. “Trajectory Optimization on Manifolds: A Theoretically-Guaranteed Embedded Sequential Convex Programming Approach”. In: Robotics: Science and Systems XV. Robotics: Science and Systems Foundation, 2019. <sup>doi</sup>: 10.15607/rss.2019. xv.078.

[70] S. Banerjee et al. “Learning-based Warm-Starting for Fast Sequential Convex Programming and Trajectory Optimization”. In: IEEE Aerospace Conference. Big Sky, Montana, Mar. 2020.

[71] Thomas Lew, Riccardo Bonalli, and Marco Pavone. “Chance-Constrained Sequential Convex Programming for Robust Trajectory Optimization”. In: 2020 European Control Conference (ECC). IEEE, May 2020. <sup>doi</sup>: 10.23919/ecc51009.2020.9143595.

[72] R. Bonalli, T. Lew, and M. Pavone. “Analysis of Theoreti cal and Numerical Properties of Sequential Convex Programming for Continuous-Time Optimal Control”. In: IEEE Transactions on Automatic Control (2021). Submitted.

[73] R. Bonalli, T. Lew, and M. Pavone. “Sequential Convex Programming For Non-Linear Stochastic Optimal Control”. In: (2021). Submitted.

[74] Yuanqi Mao, Michael Szmuk, and Beh¸cet A¸cıkme¸se. “A Tutorial on Real-time Convex Optimization Based Guidance and Control for Aerospace Applications”. In: 2018 Annual American Control Conference (ACC). IEEE, June 2018. <sup>doi</sup>: 10 . 23919 / acc . 2018.8430984

[75] Yuanqi Mao et al. “Convexification and Real-Time Optimization for MPC with Aerospace Applications”. In: Handbook of Model Predictive Control. Springer International Publishing, Sept. 2018, pp. 335–358. <sup>doi</sup>: 10.1007/978-3-319-77489-3\_15.

[76] David Q. Mayne. “Model predictive control: Recent develop ments and future promise”. In: Automatica 50.12 (Dec. 2014), pp. 2967–2986. <sup>doi</sup>: 10.1016/j.automatica.2014.10.128.

[77] Carlos E. Garcia, David M. Prett, and Manfred Morari. “Model predictive control: Theory and practice—A survey”. In: Automatica 25.3 (May 1989), pp. 335–348. <sup>doi</sup>: 10.1016/0005- 1098(89)90002-2.

[78] Utku Eren et al. “Model Predictive Control in Aerospace Sys tems: Current State and Opportunities”. In: Journal of Guidance, Control, and Dynamics 40.7 (July 2017), pp. 1541–1566. <sup>doi</sup>: 10. 2514/1.g002507.

[79] James B. Rawlings, David Q. Mayne, and Moritz M. Diehl. Model Predictive Control: Theory, Computation and Design. 2nd ed. Madison, WI: Nob Hill Publishing, 2017. <sup>isbn</sup>: 9780975937730.

[80] Jef Bezanson et al. “Julia: A fresh approach to numerical computing”. In: SIAM review 59.1 (2017), pp. 65–98.

[81] Ralph T. Rockafellar. Convex Analysis. Princeton, NJ: Princeton University Press, 1970. <sup>isbn</sup>: 9780691015866. <sup>doi</sup>: 10.2307/j. ctvcm4g0s.

[82] N. Karmarkar. “A new polynomial-time algorithm for linear programming”. In: Combinatorica 4.4 (Dec. 1984), pp. 373–395. <sup>doi</sup>: 10.1007/bf02579150.

[83] Jiming Peng, Cornelis Roos, and Tam´as Terlaky. Self-Regularity: A New Paradigm for Primal-Dual Interior-Point Algorithms. Princeton University Press, 2002. <sup>isbn</sup>: 9780691091938.

[84] Beh¸cet A¸cıkme¸se and Scott Ploen. “A Powered Descent Guidance Algorithm for Mars Pinpoint Landing”. In: AIAA Guidance, Navigation, and Control Conference and Exhibit. American Institute of Aeronautics and Astronautics, Aug. 2005. <sup>doi</sup>: 10.2514/6. 2005-6288.

[85] Lars Blackmore, Beh¸cet A¸cikme¸se, and Daniel P. Scharf. “Minimum-Landing-Error Powered-Descent Guidance for Mars Landing Using Convex Optimization”. In: Journal of Guidance, Control, and Dynamics 33.4 (July 2010), pp. 1161–1171. <sup>doi</sup>: 10.2514/1.47202

[86] Beh¸cet A¸cıkme¸se and Lars Blackmore. “Lossless convexification of a class of optimal control problems with non-convex control constraints”. In: Automatica 47.2 (Feb. 2011), pp. 341–347. <sup>doi</sup>: 10.1016/j.automatica.2010.10.037.

[87] John M. Carson III, Beh¸cet A¸cıkme¸se, and Lars Blackmore. “Lossless convexification of Powered-Descent Guidance with nonconvex thrust bound and pointing constraints”. In: Proceedings of the 2011 American Control Conference. IEEE, June 2011. <sup>doi</sup>: 10.1109/acc.2011.5990959.

[88] Matthew W. Harris and Beh¸cet A¸cıkme¸se. “Lossless convexification for a class of optimal control problems with linear state constraints”. In: 52nd IEEE Conference on Decision and Control. IEEE, Dec. 2013. <sup>doi</sup>: 10.1109/cdc.2013.6761017.

[89] Matthew W. Harris and Beh¸cet A¸cıkme¸se. “Lossless convexifi cation of non-convex optimal control problems for state constrained linear systems”. In: Automatica 50.9 (Sept. 2014), pp. 2304–2311. <sup>doi</sup>: 10.1016/j.automatica.2014.06.008.

[90] Danylo Malyuta and Beh¸cet A¸cikme¸se. “Lossless Convexification of Optimal Control Problems with Semi-continuous Inputs”. In: IFAC-PapersOnLine 53.2 (2020), pp. 6843–6850. <sup>doi</sup>: 10.1016/ j.ifacol.2020.12.341.

[91] Matthew W. Harris. “Optimal Control on Disconnected Sets using Extreme Point Relaxations and Normality Approximations”. In: IEEE Transactions on Automatic Control (2021), pp. 1–1. <sup>doi</sup>: 10.1109/tac.2021.3059682.

[92] Sheril Kunhippurayil, Matthew W. Harris, and Olli Jansson. “Lossless Convexification of Optimal Control Problems with An nular Control Constraints”. In: Automatica (2021).

[93] Sheril Kunhippurayil and Matthew W. Harris. “Strong Observability as a Suficient Condition for Non-singularity in Optimal Control with Mixed Constraints”. In: Automatica (2021).

[94] Henry D’Angelo. Linear Time-Varying Systems: Analysis and Synthesis. Allyn and Bacon, 1970.

[95] Panos J. Antsaklis and Anthony N. Michel. Linear Systems. Birkhauser Basel, 2006. <sup>isbn</sup>: 9780817644345. <sup>doi</sup>: 10 . 1007 / 0 - 8176-4435-0.

[96] Beh¸cet A¸cıkme¸se, John M. Carson III, and Lars Blackmore. “Lossless Convexification of Nonconvex Control Bound and Pointing Constraints of the Soft Landing Optimal Control Problem”. In: IEEE Transactions on Control Systems Technology 21.6 (Nov. 2013), pp. 2104–2113. <sup>doi</sup>: 10.1109/tcst.2012.2237346.

[97] Matthew Wade Harris. “Lossless Convexification of Optimal Control Problems”. PhD thesis. Austin: The University of Texas at Austin, 2014.

[98] L. D. Landau and E. M. Lifshitz. Mechanics. 2nd ed. Bristol UK: Pergamon Press, 1969.

[99] Warren F. Phillips. Mechanics of Flight. Hoboken, NJ: Wiley, 2010. <sup>isbn</sup>: 9780470539750

[100] Anton H. J. de Ruiter, Christopher J. Damaren, and James R. Forbes. Spacecraft Dynamics and Control: An Introduction. Wiley, 2013. <sup>isbn</sup>: 9781118342367.

[101] H. L. Trentelman, A. A. Stoorvogel, and M. Hautus. Control Theory for Linear Systems. Springer, 2001.

[102] Matthew W. Harris and Beh¸cet A¸cıkme¸se. “Lossless convexi fication for a class of optimal control problems with quadratic state constraints”. In: 2013 American Control Conference. IEEE, June 2013. <sup>doi</sup>: 10.1109/acc.2013.6580359.

[103] Sigurd Skogestad and Ian Postlethwaite. Multivariable Feedback Control: Analysis and Design. 2nd ed. Wiley, 2005. <sup>isbn</sup>: 9780470011676.

[104] Richard F. Hartl, Suresh P. Sethi, and Raymond G. Vickson. “A Survey of the Maximum Principles for Optimal Control Prob lems with State Constraints”. In: SIAM Review 37.2 (June 1995), pp. 181–218. <sup>doi</sup>: 10.1137/1037043.

[105] A. Milyutin and N. Osmolovskii. Calculus of Variations and Optimal Control. American Mathematical Society, 1998

[106] Tobias Achterberg and Roland Wunderling. “Mixed Integer Programming: Analyzing 12 Years of Progress”. In: Facets of Combinatorial Optimization. Springer Berlin Heidelberg, 2013, pp. 449– 481. <sup>doi</sup>: 10.1007/978-3-642-38189-8\_18.

[107] Tobias Achterberg. “Constrained Integer Programming”. PhD thesis. Berlin: Technische Universit¨at Berlin, 2007.

[108] Tom Schouwenaars et al. “Mixed integer programming for multi-vehicle path planning”. In: 2001 European Control Conference (ECC). IEEE, Sept. 2001. <sup>doi</sup>: 10.23919/ecc.2001.7076321.

[109] Zhe Zhang, Jun Wang, and Jianxun Li. “Lossless convexifi cation of nonconvex MINLP on the UAV path-planning problem”. In: Optimal Control Applications and Methods 39.2 (Dec. 2017), pp. 845–859. <sup>doi</sup>: 10.1002/oca.2380.

[110] Xinfu Liu, Ping Lu, and Binfeng Pan. “Survey of convex opti mization for aerospace applications”. In: Astrodynamics 1.1 (Sept. 2017), pp. 23–40. <sup>doi</sup>: 10.1007/s42064-017-0003-8.

[111] Alberto Bemporad and Manfred Morari. “Control of systems integrating logic, dynamics, and constraints”. In: Automatica 35.3 (Mar. 1999), pp. 407–427. <sup>doi</sup>: 10.1016/s0005-1098(98)00178-2.

[112] Danylo Malyuta and Beh¸cet A¸cıkme¸se. “Fast Continuous Embedding for Spacecraft Rendezvous Trajectory Optimization with Discrete Logic”. In: Journal of Guidance, Control, and Dynamics (submitted) (2021).

[113] Tom Schouwenaars. “Safe trajectory planning of autonomous vehicles”. Dissertation (Ph.D.) Massachusetts Institute of Technol ogy, 2006.

[114] Michael Posa, Cecilia Cantu, and Russ Tedrake. “A direct method for trajectory optimization of rigid bodies through contact”. In: The International Journal of Robotics Research 33.1 (Oct. 2013), pp. 69–81. <sup>doi</sup>: 10.1177/0278364913506757.

[115] Jemin Hwangbo, Joonho Lee, and Marco Hutter. “Per-Contact Iteration Method for Solving Contact Dynamics”. In: IEEE Robotics and Automation Letters 3.2 (Apr. 2018), pp. 895–902. <sup>doi</sup>: 10.1109/lra.2018.2792536.

[116] Rafal Goebel, Ricardo G. Sanfelice, and Andrew R. Teel. “Hybrid dynamical systems”. In: IEEE Control Systems 29.2 (Apr. 2009), pp. 28–93. <sup>doi</sup>: 10.1109/mcs.2008.931718.

[117] Russ Tedrake. “MIT’s Entry Into the DARPA Robotics Challenge”. In: Brains, Minds and Machines Summer Course. MIT OpenCourseWare. Cambridge MA, 2015.

[118] Henry Hermes and Joseph P. LaSalle. Functional Analysis and Time Optimal Control. Elsevier, 1969. <sup>isbn</sup>: 9780080955650.

[119] Richard Vinter. Optimal Control. Birkhauser, 2000. <sup>isbn</sup>: 0817640754.

[120] Francis Clarke. “The Pontryagin maximum principle and a unified theory of dynamic optimization”. In: Proceedings of the

Steklov Institute of Mathematics 268.1 (Apr. 2010), pp. 58–69. <sup>doi</sup>: 10.1134/s0081543810010062.

[121] Unsik Lee and Mehran Mesbahi. “Constrained Autonomous Precision Landing via Dual Quaternions and Model Predictive Control”. In: Journal of Guidance, Control, and Dynamics 40.2 (2017), pp. 292–308. <sup>doi</sup>: 10.2514/1.G001879.

[122] Xinfu Liu and Ping Lu. “Solving Nonconvex Optimal Control Problems by Convex Optimization”. In: Journal of Guidance, Control, and Dynamics 37.3 (2014), pp. 750–765. <sup>doi</sup>: 10.2514/1. 62110.

[123] R. Bonalli, B. H´eriss´e, and E. Tr´elat. “Optimal Control of Endo-Atmospheric Launch Vehicle Systems: Geometric and Computational Issues”. In: IEEE Transactions on Automatic Control 65.6 (2020), pp. 2418–2433. <sup>doi</sup>: 10.1109/TAC.2019.2929099.

[124] M. Koˇcvara. “On the modeling and solving of the truss design problem with global stability constraints”. In: Structural and Multidisciplinary Optimization 23 (2002), pp. 189–203. <sup>doi</sup>: 10. 1007/s00158-002-0177-3.

[125] Amir Beck, Aharon Ben-Tal, and Luba Tetruashvili. “A sequential parametric convex approximation method with applications to nonconvex truss topology design problems”. In: Journal of Global Optimization 47 (2010), pp. 29–51. <sup>doi</sup>: 10.1007/s10898- 009-9456-5.

[126] Wei Wei et al. “Optimal Power Flow of Radial Networks and Its Variations: A Sequential Convex Optimization Approach”. In: IEEE Transactions on Smart Grid 8.6 (2017), pp. 2974–2987. <sup>doi</sup>: 10.1109/TSG.2017.2684183.

[127] Lorenz T. Biegler. “Recent advances in chemical process optimization”. In: Chemie Ingenieur Technik 86.7 (2014), pp. 943– 952. <sup>issn</sup>: 15222640. <sup>doi</sup>: 10.1002/cite.201400033.

[128] Hao Jiang, Mark S. Drew, and Ze-Nian Li. “Matching by linear programming and successive convexification”. In: IEEE Transactions on Pattern Analysis and Machine Intelligence 29.6 (2007), pp. 959–975. <sup>doi</sup>: 10.1109/TPAMI.2007.1048.

[129] Tony F Chan, Selim Esedo¯glu, and Mila Nikolova. “Algorithms for finding global minimizers of image segmentation and denoising models”. In: SIAM Journal on Applied Mathematics 66.5 (2006), pp. 1632–1648.

[130] Space Exploration Technologies Corp. Starship — SN10 — High-Altitude Flight Recap. https://www.youtube.com/watch?v= gA6ppby3JC8. Mar. 2021.

[131] Danylo Malyuta et al. Starship landing SCP example. https: //github.com/dmalyuta/scp\_traj\_opt. Apr. 2021.

[132] D. Rocha, Cristiana J. Silva, and Delfim F. M. Torres. “Stability and optimal control of a delayed HIV model”. In: Mathematical Methods in the Applied Sciences 41.6 (2018), pp. 2251–2260. <sup>doi</sup>: 10.1002/mma.4207.

[133] Cristiana J. Silva, Helmut Maurer, and Delfim F. M. Torres. “Optimal control of a Tuberculosis model with state and control delays”. In: Mathematical Biosciences and Engineering 14.1 (2017), pp. 321–337. <sup>doi</sup>: 10.3934/mbe.2017021.

[134] Robert Dorfman. “An economic interpretation of optimal control theory”. In: American Economic Review 59.5 (1969), pp. 817–831. <sup>doi</sup>: https://www.jstor.org/stable/1810679.

[135] M.R. Caputo. Foundations of Dynamic Economic Analysis. Cambridge University Press, 2005. <sup>doi</sup>: 10 . 1017 / CBO9780511806827.

[136] Julio R Banga. “Optimization in computational systems biology”. In: BMC Systems Biology 2.47 (2008). <sup>doi</sup>: 10.1186/1752- 0509-2-47

[137] Anne Goelzer, Vincent Fromion, and G´erard Scorletti. “Cell design in bacteria as a convex optimization problem”. In: Automatica 47.6 (2011), pp. 1210–1218. <sup>doi</sup>: 10.1016/j.automatica. 2011.02.038.

[138] Matti Liski, Peter M Kort, and Andreas Novak. “Increasing returns and cycles in fishing”. In: Resource and Energy Economics 23.3 (2001), pp. 241–258. <sup>doi</sup>: 10.1016/S0928-7655(01)00038-0.

[139] Yurii Nesterov and Arkadii Nemirovskii. Interior-Point Polynomial Algorithms in Convex Programming. Society

for Industrial and Applied Mathematics, Jan. 1994. <sup>doi</sup>: 10.1137/1.9781611970791.

[140] Dimitri Bertsekas. Dynamic Programming and Optimal Control. 4th ed. Nashua, NH: Athena Scientific, 2017. <sup>isbn</sup>: 9781886529434.

[141] Dimitri Bertsekas. Convex Optimization Algorithms. Nashua, NH: Athena Scientific, 2015. <sup>isbn</sup>: 9781886529281.

[142] Melanie Mitchell. An Introduction to Genetic Algorithms. Cambridge, Massachusetts: The MIT Press, 1996. <sup>isbn</sup>: 9780262631853.

[143] Richard S. Sutton and Andrew G. Barto. Reinforcement Learning. 2nd ed. Cambridge, Massachusetts: The MIT Press, 2018. <sup>isbn</sup>: 9780262039246.

[144] James E. Falk and Richard M. Soland. “An Algorithm for Separable Nonconvex Programming Problems”. In: Management Science 15.9 (1969), pp. 550–569. <sup>doi</sup>: 10.1287/mnsc.15.9.550.

[145] Richard M. Soland. “An Algorithm for Separable Nonconvex Programming Problems II: Nonconvex Constraints”. In: Management Science 17.11 (1971), pp. 759–773. <sup>doi</sup>: 10.1287/mnsc.17. 11.759.

[146] Reiner Horst. “An algorithm for nonconvex programming problems”. In: Mathematical Programming 10 (1976), pp. 312–321 <sup>doi</sup>: 10.1007/BF01580678.

[147] R. Horst. “On the convexification of nonlinear programming problems: An applications-oriented survey”. In: European Journal of Operational Research 15.3 (1984), pp. 382–392. <sup>doi</sup>: 10.1016/ 0377-2217(84)90107-3.

[148] Garth P. McCormick. “Computability of global solutions to factorable nonconvex programs: Part I - Convex underestimating problems”. In: Mathematical Programming 10 (1976), pp. 147–175. <sup>doi</sup>: 10.1007/BF01580665.

[149] Alexander Mitsos, Benoˆıt Chachuat, and Paul I. Barton. “McCormick-Based Relaxations of Algorithms”. In: SIAM Journal on Optimization 20.2 (2009), pp. 573–601. <sup>doi</sup>: 10.1137/080717341

[150] A. Tsoukalas and Alexander Mitsos. “Multivariate Mc-Cormick relaxations”. In: Journal of Global Optimization 59 (2014), pp. 633–662. <sup>doi</sup>: 10.1007/s10898-014-0176-0.

[151] Adam B. Singer and Paul I. Barton. “Global solution of opti mization problems with parameter-embedded linear dynamic systems”. In: Journal of Optimization Theory and Applications 121 (2004), pp. 613–646. <sup>doi</sup>: 10.1023/B:JOTA.0000037606.79050.a7.

[152] Adam B. Singer and Paul I. Barton. “Bounding the Solutions of Parameter Dependent Nonlinear Ordinary Diferential Equations”. In: SIAM Journal on Scientific Computing 27.6 (2006), pp. 2167–2182. <sup>doi</sup>: 10.1137/040604388.

[153] Reiner Horst and N. V. Thoai. “DC programming: overview”. In: Journal of Optimization Theory and Applications 103.1 (1999), pp. 1–43. <sup>issn</sup>: 00223239. <sup>doi</sup>: 10.1023/a:1021765131316.

[154] Thomas Lipp and Stephen Boyd. “Variations and extension of the convex–concave procedure”. In: Optimization and Engineering 17.2 (2016), pp. 263–287. <sup>issn</sup>: 15732924. <sup>doi</sup>: 10.1007/ s11081-015-9294-x.

[155] A. L. Yuille and Anand Rangarajan. “The Concave-Convex Procedure”. In: Neural Computation 15.4 (2003), pp. 915–936. <sup>doi</sup>: 10.1162/08997660360581958.

[156] Gert R. Lanckriet and Bharath K. Sriperumbudur. “On the Convergence of the Concave-Convex Procedure”. In: Advances in Neural Information Processing Systems 22. Curran Associates, Inc., 2009, pp. 1759–1767.

[157] F. Palacios-Gomez, L. Lasdon, and M. Engquist. “Nonlinear Optimization by Successive Linear Programming”. In: Management Science 28.10 (1982), pp. 1106–1120. <sup>doi</sup>: 10.1287/mnsc.28. 10.1106.

[158] Richard H. Byrd et al. “An algorithm for nonlinear optimization using linear programming and equality constrained subproblems”. In: Mathematical Programing, Series B 100 (2003), pp. 27– 48. <sup>doi</sup>: 10.1007/s10107-003-0485-4.

[159] S. P. Han. “A Globally Convergent Method for Nonlinear Programming”. In: Journal of Optimization Theory and Applications 22.3 (1977), pp. 297–309. <sup>doi</sup>: 10.1007/BF00932858.

[160] S. P. Han and Olvi L. Mangasarian. “Exact penalty functions in nonlinear programming”. In: Mathematical Programming 17 (1979), pp. 251–269. <sup>doi</sup>: 10.1007/BF01588250.

[161] Michael J. D. Powell. “A fast algorithm for nonlinearly constrained optimization calculations”. In: Numerical Analysis. Ed. by G. A. Watson. Springer, Berlin, Heidelberg, 1978. Chap. Lecture Notes in Mathematics, pp. 144–157. <sup>doi</sup>: 10.1007/BFb0067703.

[162] Michael J. D. Powell. “Algorithms for nonlinear constraints that use lagrangian functions”. In: Mathematical Programming 14 (1978), pp. 224–248. <sup>doi</sup>: 10.1007/BF01588967.

[163] Michael J. D. Powell and Y. Yuan. “A recursive quadratic programming algorithm that uses diferentiable exact penalty functions”. In: Mathematical Programming 35 (1986), pp. 265–278. <sup>doi</sup>: 10.1007/BF01580880

[164] Paul T. Boggs, Jon W. Tolle, and Pyng Wang. “On the Local Convergence of Quasi-Newton Methods for Constrained Optimization”. In: SIAM Journal of Control and Optimization 20.2 (1982), pp. 161–171. <sup>doi</sup>: 10.1137/0320014.

[165] Paul T. Boggs and Jon W. Tolle. “A Family of Descent Functions for Constrained Optimization”. In: SIAM Journal on Numerical Analysis 21.6 (1984), pp. 1146–1161. <sup>doi</sup>: 10.1137/0721071.

[166] Paul T. Boggs and W. Jon Tolle. “A Strategy for Global Convergence in a Sequential Quadratic Programming Algorithm”. In: SIAM Journal of Numerical Analysis 26.3 (1989), pp. 600–623. <sup>doi</sup>: 10.1137/0726036.

[167] Masao Fukushima. “A Successive Quadratic Programming Algorithm with Global and Superlinear Convergence Properties”. In: Mathematical Programming 35 (1986), pp. 253–264. <sup>doi</sup>: 10. 1007/BF01580879.

[168] Paul T. Boggs and W. Jon Tolle. “Sequential Quadratic Programming”. In: Acta Numerica 4 (1995), pp. 1–52. <sup>doi</sup>: 10.1017/ S0962492900002518.

[169] Richard H. Byrd, Robert B. Schnabel, and Gerald A. Shultz. “Approximate solution of the trust region problem by minimization over two-dimensional subspaces”. In: Mathematical Programming 40-40.1-3 (Jan. 1988), pp. 247–263. <sup>doi</sup>: 10.1007/bf01580735.

[170] Philip E. Gill, Walter Murray, and Michael A. Saunders. “SNOPT: An SQP algorithm for large-scale constrained optimization”. In: SIAM Review 47.1 (2005), pp. 99–131. <sup>doi</sup>: 10.1137/ s0036144504446096

[171] John T. Betts and William P. Hufman. “Path-constrained trajectory optimization using sparse sequential quadratic programming”. In: Journal of Guidance, Control, and Dynamics 16.1 (1993), pp. 59–68. <sup>doi</sup>: 10.2514/3.11428.

[172] Craig T. Lawrence and Andr´e L. Tits. “A Computationally Eficient Feasible Sequential Quadratic Programming Algorithm”. In: SIAM Journal on Optimization 11.4 (2001), pp. 1092–1118. <sup>doi</sup>: 10.1137/s1052623498344562.

[173] Philip E. Gill and Elizabeth Wong. “Sequential quadratic programming methods”. In: Mixed Integer Nonlinear Programming. Ed. by J. Lee and S. Leyfer. Springer New York, 2012, pp. 147–224. <sup>doi</sup>: 10.1007/978-1-4614-1927-3\_6.

[174] Roger Fletcher. Practical Methods of Optimization. John Wiley & Sons, 2013. <sup>doi</sup>: 10.1002/9781118723203.

[175] B. Fares, D. Noll, and P. Apkarian. “Robust control via sequential semidefinite programming”. In: SIAM Journal of Control and Optimization 40.6 (2002), pp. 1791–1820. <sup>doi</sup>: 10.1137/ S0363012900373483.

[176] Stephen Boyd et al. Linear Matrix Inequalities in System and Control Theory. SIAM, Philadelphia, PA, 1994. <sup>doi</sup>: 10.1137/1. 9781611970777.

[177] Taylor Reynolds et al. “Funnel Synthesis for the 6-DOF Powered Descent Guidance Problem”. In: AIAA Scitech 2021 Forum. American Institute of Aeronautics and Astronautics, Jan. 2021. DQI:10.2514/6.2021-0504

[178] Taylor P. Reynolds. “Computation Guidance and Control for Aerospace Systems”. PhD thesis. Seattle, WA: University of Washington, 2021.

[179] J. Schulman et al. “Motion planning with sequential convex optimization and convex collision checking”. In: The International Journal of Robotics Research 33.9 (2014), pp. 1251–1270. <sup>doi</sup>: 10. 1177/0278364914528132

[180] Xinfu Liu, Zuojun Shen, and Ping Lu. “Solving the maximum-crossrange problem via successive second-order cone programming with a line search”. In: Aerospace Science and Technology 47 (2015), pp. 10–20. <sup>doi</sup>: 10.1016/j.ast.2015.09.008.

[181] Marco Sagliano. “Pseudospectral Convex Optimization for Powered Descent and Landing”. In: Journal of Guidance, Control, and Dynamics 41.2 (2017), pp. 320–334. <sup>doi</sup>: 10.2514/1.G002818

[182] Pedro Simpl´ıcio, Andr´es Marcos, and Samir Bennani. “Guidance of Reusable Launchers: Improving Descent and Landing Per formance”. In: Journal of Guidance, Control, and Dynamics 42.10 (2019), pp. 2206–2219. <sup>doi</sup>: 10.2514/1.G004155.

[183] Y. Mao, M. Szmuk, and B. A¸cıkme¸se. “Successive convexifi cation of non-convex optimal control problems and its convergence properties”. In: Conference on Decision and Control. IEEE, 2016, pp. 3636–3641. <sup>doi</sup>: 10.1109/CDC.2016.7798816.

[184] Michael Szmuk. “Successive Convexification & High Performance Feedback Control for Agile Flight”. PhD thesis. Seattle, WA: University of Washington, 2019.

[185] Harish Saranathan and Michael J. Grant. “Relaxed Autonomously Switched Hybrid System Approach to Indirect Multiphase Aerospace Trajectory Optimization”. In: Journal of Spacecraft and Rockets 55.3 (May 2018), pp. 611–621. <sup>doi</sup>: 10.2514/1.a34012.

[186] Ehsan Taheri et al. “A novel approach for optimal trajectory design with multiple operation modes of propulsion system, part 1”. In: Acta Astronautica 172 (July 2020), pp. 151–165. <sup>doi</sup>: 10. 1016/j.actaastro.2020.02.042.

[187] Daniel Liberzon. Calculus of variations and optimal control theory : a concise introduction. Princeton, N.J: Princeton University Press, 2012. <sup>isbn</sup>: 9781400842643.

[188] Ken Shoemake. “Animating rotation with quaternion curves”. In: Proceedings of the 12th annual conference on Computer graphics and interactive techniques - SIGGRAPH 1985. ACM PreSs, 1985 D0I: 10.1145/325334, 325242

[189] Taylor P. Reynolds and Mehran Mesbahi. “Optimal Planar Powered Descent with Independent Thrust and Torque”. In: Journal of Guidance, Control, and Dynamics 43.7 (July 2020), pp. 1225–1231. <sup>doi</sup>: 10.2514/1.g004701.

[190] Danylo Malyuta et al. “Discretization Performance and Accuracy Analysis for the Powered Descent Guidance Problem”. In: AIAA SciTech Forum. 2019. <sup>doi</sup>: 10.2514/6.2019-0925.

[191] Beh¸cet A¸cıkme¸se et al. “Enhancements on the Convex Programming Based Powered Descent Guidance Algorithm for Mars Landing”. In: AIAA/AAS Astrodynamics Specialist Conference and Exhibit. American Institute of Aeronautics and Astronautics, Aug. 2008. <sup>doi</sup>: 10.2514/6.2008-6426.

[192] Daniel Dueri et al. “Trajectory optimization with intersample obstacle avoidance via successive convexification”. In: 2017 IEEE 56th Annual Conference on Decision and Control (CDC) IEEE Dec. 2017 DQI: 10.1109/cdc 2017 8263811

[193] Morris W. Hirsch, Stephen Smale, and Robert L. Devaney. Diferential Equations, Dynamical Systems, and an Introduction to Chaos. Elsevier, 2013. <sup>doi</sup>: 10.1016/c2009-0-61160-0

[194] Francesco Bullo and Andrew D. Lewis. Geometric Control of Mechanical Systems. Springer New York, 2005. <sup>doi</sup>: 10.1007/978- 1-4899-7276-7.

[195] Charles Dugas et al. “Incorporating Second-Order Functional Knowledge for Better Option Pricing”. In: Proceedings of the 13th International Conference on Neural Information Processing Systems. NIPS’00. Denver, CO: MIT Press, 2000, pp. 451–457.

[196] P. A. Absil, R. Mahony, and B. Andrews. “Convergence of the Iterates of Descent Methods for Analytic Cost Functions”. In:

SIAM Journal on Optimization 16.2 (Jan. 2005), pp. 531–547. <sup>doi</sup>: 10.1137/040605266.

[197] Norbert Schorghofer. Lessons in scientific computing: numerical mathematics, computer technology, and scientific discovery. CRC Press, 2018. <sup>isbn</sup>: 9781315108353.

[198] I Michael Ross et al. “Scaling and Balancing for High-Performance Computation of Optimal Controls”. In: Journal of Guidance, Control, and Dynamics 41.10 (2018), pp. 2086–2097. <sup>doi</sup>: 10.2514/1.G003382.

[199] Danylo Malyuta. “An Optimal Endurance Power Limiter for an Electric Race Car Developed for the AMZ Racing Team”. IDSC-CO-PE-22. Semester project. Zurich, Switzerland: ETH Zurich, In stitute for Dynamic Systems and Control, Sept. 2016.

[200] James Renegar. A Mathematical View of Interior-Point Methods in Convex Optimization. Society for Industrial and Applied Mathematics, Jan. 2001. <sup>doi</sup>: 10.1137/1.9780898718812.

[201] Taylor P Reynolds and Mehran Mesbahi. “The Crawling Phenomenon in Sequential Convex Programming”. In: American Control Conference. Denver, CO: IEEE, 2020, pp. 3613–3618.

[202] Robert H. Goddard. A method of reaching extreme altitudes. 1920. <sup>doi</sup>: 10.1038/105809a0.

[203] P. Lu. “Entry guidance and trajectory control for reusable launch vehicle”. In: Journal of Guidance, Control, and Dynamics 20.1 (1997), pp. 143–149. <sup>doi</sup>: 10.2514/2.4008.

[204] B. Bonnard et al. “Optimal control with state constraints and the space shuttle re-entry problem”. In: Journal of Dynamical and Control Systems 9 (2003), pp. 155–199. <sup>doi</sup>: 10 . 1023 / A : 1023289721398.

[205] N. Ratlif et al. “CHOMP: Gradient optimization techniques for eficient motion planning”. In: IEEE International Conference on Robotics and Automation. IEEE, 2009, pp. 489–494. <sup>doi</sup>: 10. 1109/ROBOT.2009.5152817.

[206] M. Kalakrishnan et al. “STOMP: Stochastic trajectory optimization for motion planning”. In: IEEE International Conference on Robotics and Automation. IEEE, 2011, pp. 4569–4574. <sup>doi</sup>: 10.1109/ICRA.2011.5980280.

[207] L. E. Kavraki et al. “Probabilistic roadmaps for path planning in high-dimensional configuration spaces”. In: IEEE Transactions on Robotics and Automation 12.4 (1996), pp. 566–580. <sup>doi</sup>: 10.1109/70.508439

[208] Steven M. LaValle and James J. Kufner Jr. “Randomized kinodynamic planning”. In: The International Journal of Robotics Research 20.5 (2001), pp. 378–400. <sup>doi</sup>: 10.1177/02783640122067453.

[209] A. Majumdar and R. Tedrake. “Funnel libraries for real-time robust feedback motion planning”. In: The International Journal of Robotics Research 36.8 (2017), pp. 947–982. <sup>doi</sup>: 10 . 1177 / 0278364917712421.

[210] Scott Ploen, Bechet Acikmese, and Aron Wolf. “A Comparison of Powered Descent Guidance Laws for Mars Pinpoint Landing”. In: AIAA/AAS Astrodynamics Specialist Conference and Exhibit. American Institute of Aeronautics and Astronautics, Aug. 2006. <sup>doi</sup>: 10.2514/6.2006-6676.

[211] John M. Carson et al. “Capabilities of convex Powered-Descent Guidance algorithms for pinpoint and precision landing”. In: 2011 Aerospace Conference. IEEE, Mar. 2011. <sup>doi</sup>: 10.1109/aero.2011.5747244.

[212] A.A. Wolf et al. “Performance Trades for Mars Pinpoint Landing”. In: 2006 IEEE Aerospace Conference. IEEE, 2006. <sup>doi</sup>: 10.1109/aero.2006.1655793

[213] A. A. Wolf et al. “Improving the landing precision of an MSLclass vehicle”. In: 2012 IEEE Aerospace Conference. IEEE, Mar. 2012. <sup>doi</sup>: 10.1109/aero.2012.6187005.

[214] Skye Mceowen et al. “Visual Autonomy Interface for Optimization-Based Real-Time Motion Planning and Control”. In: IEEE International Conference on Robotics and Automation. Under review. IEEE, Oct. 2020.

[215] Autonomous Controls Laboratory. Scenario 5: Quadrotor Vehicle Tracking Performance. https://www.youtube.com/watch? v=Ou7ZfyiXeyw. Oct. 2020.

[216] Alexander Domahidi, Eric Chu, and Stephen Boyd. “ECOS: An SOCP solver for embedded systems”. In: 2013 European Control Conference (ECC). IEEE, July 2013, pp. 3071–3076. <sup>doi</sup>: 10. 23919/ecc.2013.6669541.

[217] National Aeronautics and Space Administration. What is Astrobee? https://www.nasa.gov/astrobee. Nov. 2020.

[218] Japan Aerospace Exploration Agency. First disclosure of images taken by the Kibo’s internal drone “Int-Ball”. https://iss. jaxa.jp/en/kiboexp/news/170714\_int\_ball\_en.html. July 2017.

[219] M. A. Estrada et al. “Free-flyer acquisition of spinning objects with gecko-inspired adhesives”. In: IEEE International Conference on Robotics and Automation. Stockholm, Sweden, 2016, pp. 4907– 4913. <sup>doi</sup>: 10.1109/ICRA.2016.7487696.

[220] M. Mote et al. “Collision-Inclusive Trajectory Optimization for Free-Flying Spacecraft”. In: Journal of Guidance, Control, and Dynamics 43.7 (2020), pp. 1247–1258. <sup>doi</sup>: 10.2514/1.G004788.

[221] T. Smith et al. “Astrobee: a new platform for free-flying robotics on the international space station”. In: International Symposium on Artificial Intelligence, Robotics and Automation in Space. Beijing, China, 2016.

[222] J. Barlow et al. “Astrobee: A New Platform for Free-Flying Robotics on the International Space Station”. In: International Symposium on Artificial Intelligence, Robotics, and Automation in Space (i-SAIRAS). 2016.

[223] Daniel Szafir, Bilge Mutlu, and Terry Fong. “Communicating Directionality in Flying Robots”. In: Proceedings of the Tenth Annual ACM/IEEE International Conference on Human-Robot Interaction. ACM, Mar. 2015. <sup>doi</sup>: 10.1145/2696454.2696475.

[224] Maria Bualat et al. “Astrobee: Developing a Free-flying Robot for the International Space Station”. In: AIAA SPACE 2015 Conference and Exposition. American Institute of Aeronautics and Astronautics, Aug. 2015. <sup>doi</sup>: 10.2514/6.2015-4643.

[225] JAXA. Ultra-compact triaxial attitude control module-Application to “Kibo” inboard drone (Int-ball). https : //youtu.be/ZtIARUS7Lqc. July 2017.

[226] Pedro Roque and Rodrigo Ventura. “Space CoBot: Modular design of an holonomic aerial robot for indoor microgravity environments”. In: 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, Oct. 2016. <sup>doi</sup>: 10.1109/IROS.2016.7759645.

[227] Tomas Akenine-M¨oller et al. Real-Time Rendering. 4th ed. CRC Press, July 2018. <sup>doi</sup>: 10.1201/b22086.

[228] Erwin Coumans and Yunfei Bai. PyBullet, a Python module for physics simulation for games, robotics and machine learning. http://pybullet.org. 2020.

[229] Ian Goodfellow, Yoshua Bengio, and Aaron Courville. Deep Learning. Cambridge, Massachusetts: The MIT Press, 2016. <sup>isbn</sup>: 9780262035613.

[230] Steven Michael LaValle. Planning Algorithms. Cambridge, UK: Cambridge University Press, 2006. <sup>isbn</sup>: 9780521862059.

[231] Joan Sola. “Quaternion kinematics for the error-state Kalman filter”. In: CoRR (2017).

[232] A. Zanelli et al. “FORCES NLP: an eficient implementation of interior-point methods for multistage nonlinear nonconvex programs”. In: International Journal of Control 93.1 (May 2017), pp. 13–29. <sup>doi</sup>: 10.1080/00207179.2017.1316017.