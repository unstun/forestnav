---
citation_key: Zheng2021Accelerating
arxiv_id: 2107.01259
arxiv_url: https://arxiv.org/abs/2107.01259
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:35:28Z
origin: ai+web
reviewed: false
---

# Introduction

Robotic motion planning with the goal of finding a dynamically feasible and optimal trajectory for the robot through an environment with obstacles has gained much progress over the past decades. As a fundamental problem in robotics applications, it is still a challenging problem to solve when the environment is complex with irregular obstacles and the dynamics of the robot are to be considered [@lavalle2011motion].

Sampling-based motion planning algorithms, such as rapidly exploring randomized trees (RRTs) [@lavalle2001randomized], have been developed to solve planning problems in high-dimensional continuous state spaces by incrementally building a tree through the search space. The asymptotic optimal variant of RRT, namely RRT\* [@Karaman2011Sampling], almost surely converges asymptotically to the optimal solution. RRT\* is well-suited for planning in high-dimensional spaces and obstacle-rich environments. Many applications of RRT\* have been studied in recent years [@Karaman2011Anytime; @gonzalez2015review; @gammell4asymptotically].

One limitation of RRT\* is that it requires any two points sampled in the planning space to be connected with an optimal trajectory. Thus, many works on RRT\* consider robots with simple dynamics [@Karaman2011Anytime; @Karaman2010Optimal] or assume a holonomic model and connect sampled points with straight lines [@Gammell2014InformedRRT]. For robots with differential constraints, the optimal trajectory between two states is obtained by solving a two-point boundary value problem (TPBVP), which is a non-trivial undertaking for complex nonlinear systems. The solution to this local TPBVP is also referred to as the steering function. A version of the RRT\* algorithm that explicitly considers differential dynamics is the kinodynamic RRT\* [@Dustin2013Kinodynamic; @Karaman2010Optimal].

Solving TPBVPs is the computationally dominant component of kinodynamic RRT\*, and thus researchers have looked into more efficient ways to solve these TPBVPs. A steering function based on LQR is used in [@Perez2012LQR]. A fixed-final-state free-final-time controller that optimally connects any pair of states is used in [@Dustin2013Kinodynamic]. Learning-based RRT\* algorithms are introduced in [@Wolfslag2018RRT-CoLearn; @zheng2021sampling; @Chiang2019RLRRT], where the TPBVP is solved using supervised learning [@Wolfslag2018RRT-CoLearn; @zheng2021sampling] and reinforcement learning [@Chiang2019RLRRT].

Another challenge of RRT\* is the slow convergence rate of the solution to the optimal one, which is especially evident for the kinodynamic case where the sampling space is not just the configuration space but the full state space. Heuristic and informed sampling methods have been developed to improve the convergence rate [@Gammell2014InformedRRT; @arslan2015machine; @janson2015fast]. However, these methods only consider the geometric planning problem and the dynamics of the robot is not considered. Good heuristics for improving the convergence of kinodynamic RRT\* is still an open research problem [@paden2017verification; @yi2018generalizing].

:::: {#IllustrationOFpff .figure latex-placement="htb"}
![](Zheng2021Accelerating_figs/1figure1a.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/1figure1b.png){width="1\\columnwidth"}

::: caption
Motivation of the partial-final-state-free (PFF) optimal controller. (a) Existing kinodynamic RRT\* algorithms sample the full state space, which results in inefficient trajectories. (b) Kino-RRT\* with a PFF controller samples the reduced state-space to improve convergence performance.
:::
::::

In this paper, we build on previous work on the kinodynamic RRT\* [@Dustin2013Kinodynamic] and propose a new algorithm, called Kino-RRT\*, which shows faster convergence. We propose the idea of using a partial-final-state-free (PFF) optimal controller to reduce the sampling dimension of the state space. The motivation is illustrated in Figure [1](#IllustrationOFpff){reference-type="ref" reference="IllustrationOFpff"}. Instead of randomly sampling the full state space, the proposed Kino-RRT\* only samples part of the state space. The rest of the states are selected by the PFF optimal controller. Because part of the final state is computed by the PFF optimal controller to optimize the cost function, Kino-RRT\* samples in the state space with reduced dimension. The method can also be interpreted as a heuristic for state-space sampling. Choosing the partial-free final states by the PFF optimal controller is more efficient than uniformly random sampling, and thus the resulting algorithm achieves faster convergence. We derive an analytical solution of the PFF optimal controller for the case of linear systems. Note, however, that the idea of using PFF controller in kinodynamic RRT\* is not limited to linear systems. It can be adopted similarly to [@Xie2015Towards; @Wolfslag2018RRT-CoLearn; @zheng2021sampling] to deal with nonlinear dynamics as well.

Finding the optimal arrival time for the TPBVP in the kinodynamic RRT\* requires solving a root-finding problem of a high-order polynomial. Because the TPBVP is required to be solved repeatedly, the root-finding procedure can be computationally expensive. We therefore also propose a delayed and intermittent update of the optimal arrival time of all the edges in the tree to decrease the computation complexity of the kinodynamic RRT\* algorithm.

The remainder of the paper is organized as follows. Some related works are given in Section [2](#SecRelatedWorks){reference-type="ref" reference="SecRelatedWorks"}. The statement of the problem studied in this paper is given in Section [3](#SecProblemformulation){reference-type="ref" reference="SecProblemformulation"}. In Section [4](#SecPFF){reference-type="ref" reference="SecPFF"}, the PFF optimal controller is derived. The PFF optimal controller is a key ingredient of the proposed Kino-RRT\* algorithm, which is outlined in Section [5](#SecKino-RRT*){reference-type="ref" reference="SecKino-RRT*"}. The implementation of Kino-RRT\* on different robot systems is given in Section [6](#SecExperiment){reference-type="ref" reference="SecExperiment"}. Finally, Section [7](#secConclusion){reference-type="ref" reference="secConclusion"} concludes the paper.

# Related Works {#SecRelatedWorks}

Incremental sampling-based motion planning algorithms find an initial solution in high dimensional planning spaces quickly and then incrementally improving the solution. For motion planning of robot systems, considering the differential constraints is necessary for generating feasible trajectories. The extension of RRT\* to dynamic systems is studied in [@Karaman2010Optimal], where sufficient conditions ensuring asymptotic optimality of the RRT\* for dynamic systems were established. Every *local steering* and *distance function* in kinodynamic RRT\* requires the solution of a TPBVP [@Karaman2010Optimal]. Assuming a solver of the TPBVP is available, references [@karaman2013sampling; @schmerling2015optimaldriftless; @schmerling2015optimaldrift] study the radius of the neighbor nodes in kinodynamic RRT\* to guarantee asymptotic optimality.

Solving the TPBVPs is the computationally expensive component of the kinodynamic RRT\* algorithm. Infinite-horizon and finite-horizon LQR controllers were used as the steering function in kinodynamic RRT\* for linear or linearized systems in [@Perez2012LQR] and [@goretkin2013optimal], respectively. However, these methods cannot achieve the exact connection of two states, which is required in the kinodynamic RRT\* algorithm. A fixed-final-state free-final-time controller is used in [@Dustin2013Kinodynamic] to achieve the exact connection of any pair of states for linear or linearized systems. The optimal arrival time is computed by solving a root-finding problem. To deal with nonlinear dynamics, [@Xie2015Towards] directly uses a numerical solver to solve the TPBVP online, and [@sakcak2019sampling] uses discrete motion primitives. Learning-based methods also have been studied to solve the TPBVP in kinodynamic RRT\*. References [@Wolfslag2018RRT-CoLearn] and [@zheng2021sampling] use offline generated optimal trajectories and supervised learning to train neural networks to solve the TPBVP. In [@Chiang2019RLRRT], the steering function is realized by a local policy trained using Deep Reinforcement Learning.

Other works solve the sampling-based kinodynamic motion planning problem without relying on TPBVP solvers  [@hauser2016asymptotically; @Li2016Asymptotically]. These methods extended RRT-style shooting methods to kinodynamic planning by randomly sampling piece-wise constant control inputs of the system. However, the convergence to high-quality trajectories in practice can be slow by the use of random controls [@Xie2015Towards; @Sivaramakrishnan2019; @li2021mpc].

# Problem formulation {#SecProblemformulation}

The optimal kinodynamic motion planning problem is defined as finding a dynamically feasible trajectory for the robot to reach the goal state starting from an initial state, while satisfying the state and control constraints and minimizing a cost function [@Karaman2010Optimal; @Dustin2013Kinodynamic]. Specifically, given the planning domain $X$, free space $X_\mathrm{free}$, goal region $X_\mathrm{goal}$, initial state $x_0$, consider the dynamics of the robot $$\begin{equation}
\begin{split}
    \dot{x} =  A x + B u + c,
    \label{s3eq1}
\end{split}
\end{equation}$$ and the cost function, $$\begin{equation}
\begin{split}
    J(u) = \int_{0}^{T} (1 + u^\top R u) \, \mathrm{d}\tau,
    \label{s3eq2}
\end{split}
\end{equation}$$ the goal of the motion planning problem is to find a control $u(t)$, $t \in [0,T]$, such that the solution $x(t)$ to ([\[s3eq1\]](#s3eq1){reference-type="ref" reference="s3eq1"}) is obstacle-free, i.e. $x(t) \in X_\mathrm{free}$, $t \in [0,T]$, reaches the goal region, i.e. $x(T) \in X_\mathrm{goal}$, and minimizes the cost functional ([\[s3eq2\]](#s3eq2){reference-type="ref" reference="s3eq2"}). $A$, $B$, and $c$ are constant and given. ([\[s3eq1\]](#s3eq1){reference-type="ref" reference="s3eq1"}) represents the dynamics of a linear or linearized system.

RRT\*-type algorithms try to solve this problem by growing a tree, which involves sampling intermediate states (nodes) and making optimal connections between states (edges). This results in converging to the optimal solution asymptotically. In kinodynamic RRT\*, every edge between two states is the solution of a TPBVP given by $$\begin{equation}
\begin{split}
u^*= & \mathop{\arg\min}_{u} \ J(u), \\
\mathrm{s.t.} \ \ & \dot{x}= A x + B u + c,\\
& x(0)=x_a, \ x({t_{\rm f}})=x_b,
\label{s3eq3}
\end{split}
\end{equation}$$ where $J$ is the same as in ([\[s3eq2\]](#s3eq2){reference-type="ref" reference="s3eq2"}) but over the time interval $[0, {t_{\rm f}}]$, and $x_a$ and $x_b$ are the sampled initial state and final state of this edge, respectively. The solution of ([\[s3eq3\]](#s3eq3){reference-type="ref" reference="s3eq3"}) with free-final-time ${t_{\rm f}}$ is given in [@Dustin2013Kinodynamic]. Besides this fixed-final-state free-final-time controller, next, we will present a partial-final-state-free controller, which is the key ingredient of the proposed Kino-RRT\* algorithm.

# Partial-Final-State-Free Optimal Controller {#SecPFF}

Rewrite the state $x \in \mathbb{R}^n$ as the concatenation of two vectors $x = [x_1^\top \ x_2^\top]^\top$, where $x_1 \in \mathbb{R}^{n_1}$ and $x_2 \in \mathbb{R}^{n_2}$ with $n_1 + n_2 = n$. The partial-final-state-free (PFF) optimal control problem is given by $$\begin{equation}
\begin{split}
u^*= & \mathop{\arg\min}_{u} \ J(u), \\
\mathrm{s.t.} \ \ & \dot{x} = A x + B u + c,\\
& x(0)=x_a, \ x_1({t_{\rm f}})=x_c.
\label{s4eq1}
\end{split}
\end{equation}$$ First, we consider the case where the arrival time ${t_{\rm f}}$ is given. Instead of fixing the states $x(0)$ and $x({t_{\rm f}})$ as in ([\[s3eq3\]](#s3eq3){reference-type="ref" reference="s3eq3"}), only $x(0)$ and $x_1({t_{\rm f}})$ are fixed, and $x_2({t_{\rm f}})$ is free in ([\[s4eq1\]](#s4eq1){reference-type="ref" reference="s4eq1"}).

## The PFF Optimal Controller {#PFFController}

We solve this PFF optimal control problem using Pontryagin's Maximum Principle [@lewis2012optimal]. The Hamiltonian of the system is given by $$\begin{equation}
    H(x,u,t,\lambda) = 1 + u^\top R u + \lambda^\top (Ax + Bu + c).
    \label{eqHamilt}
\end{equation}$$ The necessary conditions for optimality are $$\begin{align}
    \dot{x} &= Ax +Bu + c, \label{eq4} \\ 
    \dot{\lambda} &= - \frac{\partial H}{\partial x} = - A^\top \lambda, \label{eq5} \\
    0 &= \frac{\partial H}{\partial u} = 2 R u + B^\top \lambda, \label{eq6} \\
    \mathrm{0} &= \lambda_2({t_{\rm f}}), \label{eq7}
\end{align}$$ where $\lambda = [\lambda_1^\top \ \lambda_2^\top]^\top$, $\lambda_1 \in \mathbb{R}^{n_1}$ is the costate of $x_1$, and $\lambda_2 \in \mathbb{R}^{n_2}$ is the costate of $x_2$. Solving for $u$ using ([\[eq6\]](#eq6){reference-type="ref" reference="eq6"}), we get $$\begin{equation}
    u = - \frac{1}{2}R^{-1} B^\top \lambda.
    \label{equ}
\end{equation}$$ Substituting ([\[equ\]](#equ){reference-type="ref" reference="equ"}) into ([\[eq4\]](#eq4){reference-type="ref" reference="eq4"}), yields $$\begin{equation}
    \dot{x} = Ax - \frac{1}{2} B R^{-1} B^\top \lambda + c.
    \label{eq8}
\end{equation}$$ The analytical solutions for the differential equations ([\[eq5\]](#eq5){reference-type="ref" reference="eq5"}) and ([\[eq8\]](#eq8){reference-type="ref" reference="eq8"}) are available and are given by $$\begin{align}
    \lambda(t) &= e^{A^\top ({t_{\rm f}}-t)} \lambda({t_{\rm f}}), \label{eq9} \\ 
    x(t) &= e^{At} x(0) - \frac{1}{2} G(t) \lambda({t_{\rm f}}) + \int_0^t e^{A(t-\tau)}c \, \mathrm{d}\tau, \label{eq10}
\end{align}$$ where $G(t) = \int_0^t e^{A(t- \tau)} B R^{-1} B^\top e^{A^\top ({t_{\rm f}}- \tau)} \, \mathrm{d}\tau$.

Note that if $\lambda({t_{\rm f}})$ is known, then the problem can be solved with the control given by ([\[equ\]](#equ){reference-type="ref" reference="equ"}) and ([\[eq9\]](#eq9){reference-type="ref" reference="eq9"}), and the state trajectory given by ([\[eq10\]](#eq10){reference-type="ref" reference="eq10"}). Thus, the problem remains to determine $\lambda_1({t_{\rm f}})$. To this end, evaluate ([\[eq10\]](#eq10){reference-type="ref" reference="eq10"}) at ${t_{\rm f}}$ to obtain $$\begin{equation}
     x({t_{\rm f}}) = \bar{x}({t_{\rm f}}) - \frac{1}{2} G({t_{\rm f}}) \lambda({t_{\rm f}}), \label{eq11}
\end{equation}$$ where $$\begin{equation}
    \bar{x}({t_{\rm f}}) \triangleq e^{A {t_{\rm f}}} x(0) + \int_0^{t_{\rm f}}e^{A({t_{\rm f}}-\tau)}c \, \mathrm{d}\tau.
\end{equation}$$ We may obtain $x_2({t_{\rm f}})$ and $\lambda_1({t_{\rm f}})$ by solving the linear equations ([\[eq11\]](#eq11){reference-type="ref" reference="eq11"}). Using ([\[eq7\]](#eq7){reference-type="ref" reference="eq7"}), rewrite ([\[eq11\]](#eq11){reference-type="ref" reference="eq11"}) as $$\begin{equation}
     \begin{bmatrix} \bar{x}_1({t_{\rm f}}) - x_1({t_{\rm f}}) \\ \bar{x}_2({t_{\rm f}}) - x_2({t_{\rm f}}) \end{bmatrix} = \frac{1}{2}\begin{bmatrix} G_{11}({t_{\rm f}}) & G_{12}({t_{\rm f}})  \\ G_{21}({t_{\rm f}}) & G_{22}({t_{\rm f}}) \end{bmatrix} \begin{bmatrix} \lambda_1({t_{\rm f}}) \\ \mathrm{0} \end{bmatrix},
     \label{eq12}
\end{equation}$$ where $\bar{x}({t_{\rm f}}) = [\bar{x}_1^\top({t_{\rm f}}) \ x_2^\top({t_{\rm f}})]^\top$. Note that $\bar{x}_1({t_{\rm f}}) - x_1({t_{\rm f}})$ is known and $\bar{x}_2({t_{\rm f}}) - x_2({t_{\rm f}})$ is unknown. Then, ([\[eq12\]](#eq12){reference-type="ref" reference="eq12"}) becomes $$\begin{align}
    2 (\bar{x}_1({t_{\rm f}}) - x_1({t_{\rm f}})) &= G_{11}({t_{\rm f}}) \lambda_1({t_{\rm f}}), \label{eq13}\\ 
    2 (\bar{x}_2({t_{\rm f}}) - x_2({t_{\rm f}})) &= G_{21}({t_{\rm f}}) \lambda_1({t_{\rm f}}). \label{eq14}
\end{align}$$ Assuming $(A, B)$ is controllable, it follows that $G({t_{\rm f}})$ is invertible and hence $G_{11}({t_{\rm f}})$ is invertible. From ([\[eq13\]](#eq13){reference-type="ref" reference="eq13"}), we can solve for $\lambda_1({t_{\rm f}})$ as follows $$\begin{equation}
    \lambda_1({t_{\rm f}}) = 2 G_{11}^{-1}({t_{\rm f}}) (\bar{x}_1({t_{\rm f}}) - x_1({t_{\rm f}})).
\end{equation}$$ $x_2({t_{\rm f}})$ can be computed from ([\[eq14\]](#eq14){reference-type="ref" reference="eq14"}). Finally, from ([\[equ\]](#equ){reference-type="ref" reference="equ"}) and ([\[eq9\]](#eq9){reference-type="ref" reference="eq9"}), the open-loop optimal control is given by $$\begin{equation}
     u(t) = - \frac{1}{2} R^{-1} B^\top e^{A^\top ({t_{\rm f}}-t)} \lambda({t_{\rm f}}). \label{eq15}
\end{equation}$$ Substituting ([\[eq15\]](#eq15){reference-type="ref" reference="eq15"}) into ([\[s3eq2\]](#s3eq2){reference-type="ref" reference="s3eq2"}), the optimal cost is $$\begin{equation}
    J(u^*) = {t_{\rm f}}+ \frac{1}{4} \lambda({t_{\rm f}})^\top G({t_{\rm f}}) \lambda({t_{\rm f}}).
\end{equation}$$

## The Optimal Arrival Time

Next, consider the case when ${t_{\rm f}}$ is free. In this case, we have the transversality condition [@lewis2012optimal] $$\begin{equation}
     H({t_{\rm f}}) = 0. \label{eq16}
\end{equation}$$ Substituting ([\[equ\]](#equ){reference-type="ref" reference="equ"}) into ([\[eqHamilt\]](#eqHamilt){reference-type="ref" reference="eqHamilt"}) and evaluating ([\[eqHamilt\]](#eqHamilt){reference-type="ref" reference="eqHamilt"}) at ${t_{\rm f}}$, then ([\[eq16\]](#eq16){reference-type="ref" reference="eq16"}) becomes $$\begin{equation}
\begin{split}
     H({t_{\rm f}}) = 1 + \lambda({t_{\rm f}})^\top (A x({t_{\rm f}}) + c) - \frac{1}{4} \lambda({t_{\rm f}})^\top B R^{-1} B^\top \lambda({t_{\rm f}}) = 0.
     \label{eqHamiTf}
\end{split}
\end{equation}$$ We find the optimal arrival time ${t_{\rm f}}$ by solving ([\[eqHamiTf\]](#eqHamiTf){reference-type="ref" reference="eqHamiTf"}), which requires finding the roots of a polynomial [@Dustin2013Kinodynamic].

## PFF with Quadratic Terminal Penalty {#PFFPenalty}

In some cases, it may be desired to add implicit constraints on the free-final-state. Here, we extend the PFF optimal controller by adding a quadratic penalty on the free-final-state to the cost function. Consider the PFF optimal control problem with the cost function, $$\begin{equation}
\begin{split}
    J(u) = \frac{1}{2} x_2({t_{\rm f}})^\top S x_2({t_{\rm f}}) + \int_{0}^{{t_{\rm f}}} (1 + u^\top R u) \, \mathrm{d}\tau.
\end{split}
\end{equation}$$ The necessary conditions for optimality for the PFF control problem ([\[s4eq1\]](#s4eq1){reference-type="ref" reference="s4eq1"}) with this new cost function are still given by ([\[eq4\]](#eq4){reference-type="ref" reference="eq4"})-([\[eq6\]](#eq6){reference-type="ref" reference="eq6"}), except that ([\[eq7\]](#eq7){reference-type="ref" reference="eq7"}) is now replaced by $$\begin{align}
    \lambda_2({t_{\rm f}}) &= \phi_x^\top(x({t_{\rm f}})) = S x_2({t_{\rm f}}), \label{s4eq24}
\end{align}$$ where $\phi(x({t_{\rm f}})) = \frac{1}{2} x_2({t_{\rm f}})^\top S x_2({t_{\rm f}})$.

Following the same derivation as before, we get the same expression given by ([\[eq11\]](#eq11){reference-type="ref" reference="eq11"}). The problem remains to solve for $\lambda({t_{\rm f}})$. Substituting ([\[s4eq24\]](#s4eq24){reference-type="ref" reference="s4eq24"}) into ([\[eq11\]](#eq11){reference-type="ref" reference="eq11"}), we get $$\begin{equation}
     \bar{x}({t_{\rm f}}) - x({t_{\rm f}}) = \frac{1}{2}G({t_{\rm f}}) \begin{bmatrix} \lambda_1({t_{\rm f}}) \\ S x_2({t_{\rm f}}) \end{bmatrix},
\end{equation}$$ which is equvalent to $$\begin{equation}
    \begin{bmatrix} \bar{x}_1({t_{\rm f}}) - x_1({t_{\rm f}}) \\ \bar{x}_2({t_{\rm f}}) \end{bmatrix} = M \begin{bmatrix} \lambda_1({t_{\rm f}}) \\ x_2({t_{\rm f}}) \end{bmatrix}, \label{s4eq26}
\end{equation}$$ where $$\begin{equation}
    M = \left( \frac{1}{2}G({t_{\rm f}}) \begin{bmatrix} I & \mathrm{0} \\ \mathrm{0} & S \end{bmatrix} + \begin{bmatrix} \mathrm{0} & \mathrm{0} \\ \mathrm{0} & I \end{bmatrix} \right).
\end{equation}$$ Note that $M$ is invertible. Thus, we can calculate $\lambda_1({t_{\rm f}})$ and $x_2({t_{\rm f}})$ from ([\[s4eq26\]](#s4eq26){reference-type="ref" reference="s4eq26"}). Along with ([\[s4eq24\]](#s4eq24){reference-type="ref" reference="s4eq24"}), we obtain $\lambda({t_{\rm f}})$.

# The Kino-RRT\* Algorithm {#SecKino-RRT*}

In this section, we present the details of the Kino-RRT\* algorithm, which is built on both the PFF controller and the fixed-final-state free-final-time controller. First, we summarize some primitive procedures used in the Kino-RRT\* algorithm. Some of these primitive procedures follow the work in [@Karaman2011Sampling].\
**Sampling:** The sampling procedure `SamplePFF` returns a partial state that is randomly sampled in a reduced state space and is collision-free in the corresponding reduced state space. For example, for a robot whose state space includes the position space and the velocity space, `SamplePFF` may sample a position of the robot that is collision-free.\
**Parent:** `parent`$(x)$ returns the parent node of $x$.\
**Nearest Neighbor:** Given a tree $G = (V,E)$, where $V$ is the node set and $E$ is the edge set, the procedure `Nearest`$(V,x)$ returns the node in $V$ that is closest to the state $x$.\
**Near Nodes:** The function `Near`$(V,x,r)$ returns all the nodes in $V$ that are contained in a ball of radius $r$ centered at $x$.\
**Collision Checking:** The function `CollisionFree`$(\tau)$ takes a trajectory $\tau$ (an edge segment) as an input and returns true if and only if $\tau$ lies entirely in the collision-free space. The function `CollisionPoint`$(x)$ returns true if and only if the point $x$ is collision-free.\
**Cost:** The procedure `Cost`$(x)$ returns the cost-to-come from the root node to $x$.\
**Segment Cost:** The procedure `SegCost`$(x_i,x_j)$ returns the cost to go from $x_i$ to $x_j$. Depending on $x_j$, this cost is obtained by either solving the PFF control problem or the fixed-final-state free-final-time control problem.\
**Shrink:** The procedure `Shrink`$(x_i, x_j)$ returns $x_j$ if the distance between $x_i$ and $x_j$ is less than or equal to $\ell$. Otherwise, it returns a new state $x_\mathrm{new}$ that lies on the line formed by $x_i$ and $x_j$ and is at a distance $\ell$ away from $x_i$ towards $x_j$. The `Shrink` procedure is consistent with the RRT\* algorithm dictates that segments should have a maximum length $\ell$. If one tries to connect two points that are far away, this connecting segment will collide with obstacles with a high probability.\
**Steering:** The procedure `SteerPFF`$(x_i,x_j)$ solves the TPBVP using the PFF optimal controller, and it returns a trajectory $\tau$ that starts from $x_i$ and ends at $x_j$. The procedure `Steer`$(x_i,x_j)$ solves the TPBVP using the fixed-final-state free-final-time controller, and it returns a trajectory $\tau$ that starts from $x_i$ and ends at $x_j$. Note that $x_j$ in `Steer`$(x_i,x_j)$ is a point in the full state space, while $x_j$ in `SteerPFF`$(x_i,x_j)$ is a point in the reduced sampling space.\
**FreeState:** The function `FreeSate` takes the trajectory $\tau$ returned by `SteerPFF`$(x_i,x_j)$ as input and returns the rest of the state $x_\mathrm{free}$ at the endpoint of the trajectory that is not specified by $x_j$.

::: algorithm
$V \leftarrow \{ x_\mathrm{init} \}$; $E \leftarrow \emptyset$; $G \leftarrow (V,E)$ $z_\mathrm{rand} \leftarrow \texttt{SamplePFF}$ $x_\mathrm{nearest} \leftarrow \texttt{Nearest}(V,z_\mathrm{rand})$ $z_\mathrm{new} \leftarrow \texttt{Shrink} (x_\mathrm{nearest}, z_\mathrm{rand})$ $\tau \leftarrow \texttt{SteerPFF}(x_\mathrm{nearest},z_\mathrm{new})$ $x_\mathrm{free} \leftarrow \texttt{FreeState}(\tau)$ $X_\mathrm{near} \leftarrow \texttt{Near}(V,z_\mathrm{new}, r)$ $(x_\mathrm{min},x_\mathrm{free}) \leftarrow \texttt{ChooseParent}(X_\mathrm{near},x_\mathrm{nearest},z_\mathrm{new})$ $x_\mathrm{new} \leftarrow (z_\mathrm{new}, x_\mathrm{free})$ $V \leftarrow V \cup \{ x_\mathrm{new} \}$ $E \leftarrow E \cup \{ (x_\mathrm{min},x_\mathrm{new}) \}$ $E \leftarrow \texttt{Rewire}(X_\mathrm{near},E,x_\mathrm{new},x_\mathrm{min})$ $G \leftarrow (V,E)$; $G$;
:::

::: algorithm
$x_\mathrm{min}\leftarrow x_\mathrm{nearest}$ $c_\mathrm{min} \leftarrow \texttt{Cost}(x_\mathrm{nearest})+\texttt{SegCost}(x_\mathrm{nearest},z_\mathrm{new})$ $\tau \leftarrow \texttt{SteerPFF}(x_\mathrm{near},z_\mathrm{new})$ $x_\mathrm{free} \leftarrow \texttt{FreeState}(\tau)$ $x_\mathrm{min}\leftarrow x_\mathrm{near}$ $c_\mathrm{min} \leftarrow \texttt{Cost}(x_\mathrm{near})+\texttt{SegCost}(x_\mathrm{near},z_\mathrm{new})$ $(x_\mathrm{min},x_\mathrm{free})$
:::

::: algorithm
$\tau \leftarrow \texttt{Steer}(x_\mathrm{new},x_\mathrm{near})$ $x_\mathrm{parent}\leftarrow \texttt{Parent}(x_\mathrm{near})$ $E \leftarrow E \setminus \{ (x_\mathrm{parent},x_\mathrm{near}) \}$ $E \leftarrow E \cup \{ (x_\mathrm{new},x_\mathrm{near}) \}$ $E$
:::

The complete algorithm is given by Algorithm [\[alg:Kino-RRT\*\]](#alg:Kino-RRT*){reference-type="ref" reference="alg:Kino-RRT*"}, Algorithm [\[alg:ChooseParent\]](#alg:ChooseParent){reference-type="ref" reference="alg:ChooseParent"}, and Algorithm [\[alg:Rewire\]](#alg:Rewire){reference-type="ref" reference="alg:Rewire"}. We use $z$ to denote a point in the reduced sampling space. The rest of the state (free-state) $x_\mathrm{free}$, which comes from the endpoint of the edge segment (state trajectory), is decided by the PFF optimal controller. After the `ChooseParent` step (line 11, Algorithm [\[alg:Kino-RRT\*\]](#alg:Kino-RRT*){reference-type="ref" reference="alg:Kino-RRT*"}), the free-state is found and is combined with the sampled state to form a point in the full state space (line 12, Algorithm [\[alg:Kino-RRT\*\]](#alg:Kino-RRT*){reference-type="ref" reference="alg:Kino-RRT*"}). Then, this point is added to the tree as a node (line 13, Algorithm [\[alg:Kino-RRT\*\]](#alg:Kino-RRT*){reference-type="ref" reference="alg:Kino-RRT*"}).

## Delayed and Intermittent Update of the Arrival Time

For both the PFF controller and the fixed-final-state controller, finding the optimal arrival time of the TPBVP requires solving a root-finding problem of a high-order polynomial (see ([\[eqHamiTf\]](#eqHamiTf){reference-type="ref" reference="eqHamiTf"})). This root-finding procedure will slow down the kinodynamic RRT\* algorithm, as the TPBVP is required to be solved repeatedly. Here we propose a delayed and intermittent update of the optimal arrival time, which is shown in Figure [2](#DelayedUpdate){reference-type="ref" reference="DelayedUpdate"}. The planning algorithm first grows a tree using a heuristic of the arrival time (for example, by setting a desired average speed) without solving the root-finding problem (Figure [2](#DelayedUpdate){reference-type="ref" reference="DelayedUpdate"}(a)). Then, we intermittently update all the edges in the tree using the optimal arrival time (Figure [2](#DelayedUpdate){reference-type="ref" reference="DelayedUpdate"}(b)). If the updated edge is in-collision, we will use the original edge. We call this method KinoD-RRT\*.

:::: {#DelayedUpdate .figure latex-placement="htb"}
![](Zheng2021Accelerating_figs/2figure1a.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/2figure1b.png){width="1\\columnwidth"}

::: caption
Delayed and intermittent update of the arrival time. (a) Grow a tree using a heuristic of the arrival time (blue lines). (b) Delayed update of the optimal arrival time (red lines). If the updated edge is in-collision (red dash lines), the original edge is used (blue lines).
:::
::::

# Experimental Results {#SecExperiment}

We tested the Kino-RRT\* algorithm on two kinodynamic systems: a 2D double integrator robot operating in a plane environment and a linearized quadrotor robot with a 10-dimensional state-space. We compared the Kino-RRT\* algorithm with a variant of the kinodynamic RRT\* algorithm. The only difference between the Kino-RRT\* and the compared algorithm (a variant of kinodynamic RRT\*) is the utilization of the PFF controller in Kino-RRT\*. The compared kinodynamic RRT\* algorithm samples the full state space and uses the fixed-final-state free-final-time controller to solve the TPBVPs. The gain of performance is solely due to the PFF controller. Thus, this comparison is informative.

## Implementation Details

In kinodynamic RRT\*, the near nodes are found by using the forward-reachable set or the backward-reachable set [@Dustin2013Kinodynamic; @schmerling2015optimaldrift]. Specifically, in line 12, Algorithm [\[alg:Kino-RRT\*\]](#alg:Kino-RRT*){reference-type="ref" reference="alg:Kino-RRT*"}, $\texttt{Near}(V,x, r)$ returns all nodes in $V$ such that the cost $J$ to go from these nodes to $x$ is less than $r$ (backward-reachable set). Check membership in the forward/backward reachable set for a set of nodes can be computationally expensive.

We use Euclidean distance to find the near nodes and the nearest node. This essentially means that we do not use the true distance. In this case, the forward-reachable set and the backward-reachable set are the same. For kinodynamic motion planning, the true distance between two states is the minimum cost $J$ from the solution of the TPBVP [@Karaman2010Optimal]. Using the true distance, the forward (or backward) reachable set defines an $\epsilon$-radius sub-Riemannian ball centered at $x$. It is showed in [@Li2016Asymptotically] that there always exists a certain size Euclidean hyper-ball inside such sub-Riemannian ball under mild conditions, which justifies the use of Euclidean norms. Euclidean distance is also used in [@Li2016Asymptotically]. After the nearest node and the near nodes are selected, the true distance is used in the `ChooseParent` and `Rewire` algorithms. The Euclidean distance is used only to pre-select relevant nodes and to help with the computations.

We also used a constant radius for the Euclidean hyper-ball for the near nodes, which implies a constant radius of the sub-Riemannian ball with respect to the true distance. Note that the kinodynamic RRT\* is asymptotically optimal with a constant neighbor radius. The implementation is the same for the Kino-RRT\* and the compared algorithm for an informative comparison. All experiments are done on a laptop computer with an Intel Core i5-8250U 1.6 GHz CPU and 8 GB of RAM.

## 2D Double Integrator {#SubSec2DDI}

The state of the 2D double integrator is given by $x = [p^\top \ v^\top]^\top$, where $p = [x_1 \ x_2]^\top$ is the position and $v = [x_3 \ x_4]^\top$ is the velocity. The control input is the acceleration. The system matrices are given by $$\begin{equation}
    A = \begin{bmatrix} 0 & I_2 \\ 0 & 0 \end{bmatrix}, \quad
    B = \begin{bmatrix} 0 \\ I_2 \end{bmatrix}, \quad
    c = 0.
\end{equation}$$ The weighting matrix in the cost function is set to $R = I_2$.

For both Kino-RRT\* and kinodynamic RRT\* the position is uniformly sampled within the boundary of the environment, that is, $p \in [0, 20]^2 \ \mathrm{m}$. The free-final-state of the PFF controller is the velocity. Thus, the Kino-RRT\* algorithm does not sample the velocity space. For the kinodynamic RRT\* algorithm, the velocity is uniformly sampled in $v \in [-2, 2]^2 \ \mathrm{m/s^2}$. Note that a larger interval for the velocity essentially requires searching in a larger state space, which will result in slower convergence. However, if the sampling velocity interval is too small, the search is confined to a small state space that may not contain the optimal solution. Here, the velocity interval is chosen to be small while containing the optimal solution.

:::: {#TreeDIcomp1 .figure}
![](Zheng2021Accelerating_figs/3fig94.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/3fig400.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/3fig2000.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/3fig4000.png){width="1\\columnwidth"}

::: caption
Kinodynamic RRT\* results of the 2D double integrator. The first figure corresponds to the first solution found. From the upper left to bottom right, the nodes expanded are $94$, $400$, $2000$, $4000$. The corresponding time to generate these trees are $0.053$, $0.22$, $2.38$, $8.17$ sec. The cost of best trajectory in the trees are $86.76$, $47.56$, $27.99$, $25.72$.
:::
::::

:::: {#TreeDIcomp2 .figure}
![](Zheng2021Accelerating_figs/4fig85.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/4fig400.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/4fig2000.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/4fig4000.png){width="1\\columnwidth"}

::: caption
Kino-RRT\* results of the 2D double integrator. The first figure corresponds to the first solution found. From the upper left to bottom right, the nodes in the tree are $85$, $400$, $2000$, $4000$. The corresponding time to generate these trees are $0.015$, $0.14$, $2.12$, $7.64$ sec. The cost of best trajectory in the trees are $37.46$, $25.97$, $18.72$, $16.42$.
:::
::::

![Comparison of Kino-RRT\* and kinodynamic RRT\* for the 2D double integrator case.](Zheng2021Accelerating_figs/Fig5costComp.png){#CostDIcomp width="0.55\\columnwidth"}

The results of the kinodynamic RRT\* algorithm and the Kino-RRT\* algorithm are given in Figure [3](#TreeDIcomp1){reference-type="ref" reference="TreeDIcomp1"} and Figure [4](#TreeDIcomp2){reference-type="ref" reference="TreeDIcomp2"}, respectively. The comparison of the Kino-RRT\* and the kinodynamic RRT\* is shown in Figure [5](#CostDIcomp){reference-type="ref" reference="CostDIcomp"}. In Figure [5](#CostDIcomp){reference-type="ref" reference="CostDIcomp"}, we can see that our algorithm finds a better trajectory from the beginning (the first solution). In fact, the solution found by Kino-RRT\* within 0.14 sec is comparable to the solution found by kinodynamic RRT\* that took 8 sec after expanding 4000 nodes. After the Kino-RRT\* finds the first solution, the cost enters a sharp decrease phase. For the kinodynamic RRT\* algorithm, the cost curve is close to flat after 8 sec, and the probability of sampling good states to decrease the cost is low. Kino-RRT\* is more than 50 times faster than the kinodynamic RRT\* to find a trajectory with the same cost. By sampling in a reduced state-space, the solution returned by Kino-RRT\* is close to the optimal solution after a few seconds of computation. However, for the kinodynamic RRT\* algorithm, it is difficult to sample good velocities that are comparable to the ones chosen by the PFF optimal controller, which leads to slow convergence.

:::: {#DelayedDIcomp .figure}
![](Zheng2021Accelerating_figs/Fig6costdelaya.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/Fig6costdelayb.png){width="1\\columnwidth"}

::: caption
Delayed and intermittent update of the optimal arrival time of the 2D double integrator. The arrival time is updated whenever another 500 nodes are added to the tree.
:::
::::

Figure [6](#DelayedDIcomp){reference-type="ref" reference="DelayedDIcomp"} shows the results of the delayed and intermittent update of the optimal arrival time. The Kinodynamic RRT\* combined with the delayed and intermittent update of the optimal arrival time is called Kinodynamic RRT\* with delay. Four methods, Kinodynamic RRT\*, Kinodynamic RRT\* with delay, Kino-RRT\*, and KinoD-RRT\*, are compared. Kinodynamic RRT\* with delay is 3 times faster than Kinodynamic RRT\* when expanding the same number of nodes. The planned trajectories have a similar cost for expanding the same number of nodes.

Kino-RRT\* with delay is also 3 times faster than Kino-RRT\* when expanding the same number of nodes. We can see that in Figure [6](#DelayedDIcomp){reference-type="ref" reference="DelayedDIcomp"}(b), KinoD-RRT\* (blue dash line) finds a better trajectory in the beginning because it can expand more nodes in a given time. However, Kino-RRT\* outperforms KinoD-RRT\* after some point. This is because the velocities (free-final-state) chosen by KinoD-RRT\* are not as optimized as the velocities chosen by Kino-RRT\*. The velocity chosen by the PFF controller is affected by the arrival time. Non-optimal arrival times (which is the case with KinoD-RRT\*) will result in a sub-optimal final velocity. Thus, the performance of delayed update depends on the heuristic for the arrival time.

## Linearized Quadrotor

A linearized quadrotor model adopted from [@Dustin2013Kinodynamic] is used. The 10-dimensional state is given by $x = [p^\top \ v^\top \ r^\top \ w^\top]^\top$, which consists of the three-dimensional position $p$ and velocity $v$, and the two-dimensional orientation $r$ and angular velocity $w$. The yaw rotation, which is a redundant degree of freedom, is not considered in the model. The system matrices are given by $$\begin{align*}
    A &= \begin{bmatrix} 0 & I_3 & 0 & 0 \\ 0 & 0 & \begin{bmatrix} 0 & g \\ -g & 0 \\ 0 & 0 \end{bmatrix} & 0 \\ 0 & 0 & 0 & I_2 \\ 0 & 0 & 0 & 0\end{bmatrix}, \quad
    B = \begin{bmatrix} 0 & 0 \\ \begin{bmatrix} 0 \\ 0 \\  \frac{1}{m} \end{bmatrix} & 0 \\ 0 & 0 \\ 0 & \frac{\ell I_2}{J} \end{bmatrix}, \\
    c &= 0,
\end{align*}$$ where $g$ is the gravitational acceleration, $m$ is the mass of the quadrotor, $\ell$ is the distance between the center of the vehicle and the rotors, and $J$ is the moment of inertia about the axes coplanar with the rotors. The control input of the system is $u = [u_f \ u_x \ u_y]^\top$, where $u_f$ is the total thrust of the rotors relative to the thrust needed for hovering, and $u_x$ and $u_y$ are the relative torques of roll and pitch, respectively.

The free-final-state of the PFF controller is $v$, $r$, and $w$. Thus the Kino-RRT\* algorithm only samples the position space. Since the quadrotor is linearized at the hovering state and the dynamics is sensitive to the roll and pitch angles, we will use the PPF controller with quadratic terminal penalty introduced in Section [4.3](#PFFPenalty){reference-type="ref" reference="PFFPenalty"}. The terminal penalty matrix is $S = \mathrm{diag}(0, 0, 0, 20, 20, 0, 0)$. The weighting matrix of the control is $R = \mathrm{diag}(15, 30, 30)$.

For both Kino-RRT\* and kinodynamic RRT\* the position is uniformly sampled within the boundary of the 3D environment. The sampling intervals of $v$, $r$, and $w$ for the kinodynamic RRT\* are $v \in [-2, 2]^3 \ \mathrm{m/s}$, $r \in [-1, 1]^2 \ \mathrm{rad}$, and $w \in [-4, 4]^2 \ \mathrm{rad/s}$, respectively.

:::: {#TreeQuadcomp1 .figure}
![](Zheng2021Accelerating_figs/10tree159.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/10tree400.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/10tree1000.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/10tree2000.png){width="1\\columnwidth"}

::: caption
Kinodynamic RRT\* results of the quadrotor. The first figure corresponds to the first solution found.
:::
::::

:::: {#TreeQuadcomp2 .figure}
![](Zheng2021Accelerating_figs/11tree133.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/11tree400.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/11tree1000.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/11tree2000.png){width="1\\columnwidth"}

::: caption
Kino-RRT\* results of the quadrotor. The first figure corresponds to the first solution found.
:::
::::

![Comparison of Kino-RRT\* and kinodynamic RRT\* for the linearized quadrotor.](Zheng2021Accelerating_figs/Fig12b.png){#CostQuadcomp width="0.55\\columnwidth"}

The results of the kinodynamic RRT\* algorithm and the Kino-RRT\* algorithm are given in Figure [7](#TreeQuadcomp1){reference-type="ref" reference="TreeQuadcomp1"} and Figure [8](#TreeQuadcomp2){reference-type="ref" reference="TreeQuadcomp2"}, respectively. In Figure [7](#TreeQuadcomp1){reference-type="ref" reference="TreeQuadcomp1"}, from the upper left to bottom right, the number of nodes in the tree are $159$, $400$, $1000$, $2000$. The corresponding time to generate these trees are $0.147$, $0.48$, $1.92$, $6.18$ sec. The cost of the best trajectory in these trees are $58.10$, $30.92$, $24.84$, $24.61$, respectively. In Figure [7](#TreeQuadcomp1){reference-type="ref" reference="TreeQuadcomp1"}, from upper left to bottom right, the number of nodes in the tree are $133$, $400$, $1000$, $2000$. The corresponding time to generate these trees are $0.19$, $0.84$, $3.72$, $11.35$ sec. The cost of the best trajectory in these trees are $20.31$, $19.13$, $15.56$, $15.52$, respectively. The comparison of Kino-RRT\* and kinodynamic RRT\* is shown in Figure [9](#CostQuadcomp){reference-type="ref" reference="CostQuadcomp"}. The solution of the PPF controller with quadratic terminal penalty is more complex than the fixed-final-state free-final-time controller. Thus, the Kino-RRT\* algorithm takes more time to expand the same number of nodes compared to the kinodynamic RRT\*. Because each node in Kino-RRT\* is more optimized, it still converges faster than the kinodynamic RRT\*.

Figure [10](#DelayedQuadcomp){reference-type="ref" reference="DelayedQuadcomp"} shows the results of the delayed and intermittent update of the optimal arrival time. For the linearized quadrotor example, the kinodynamic RRT\* with delay is 2 times faster than the kinodynamic RRT\* when expanding the same number of nodes, and is also 2 times faster for finding a trajectory with a similar cost. Similar performance improvement is observed for the KinoD-RRT\* compared to Kino-RRT\*. This performance improvement depends on the heuristic of the arrival time for the KinoD-RRT\* algorithm.

:::: {#DelayedQuadcomp .figure}
![](Zheng2021Accelerating_figs/Fig13a1.png){width="1\\columnwidth"}

![](Zheng2021Accelerating_figs/Fig13b1.png){width="1\\columnwidth"}

::: caption
Delayed and intermittent update of the optimal arrival time for the linearized quadrotor example.
:::
::::

# Conclusion {#secConclusion}

In this paper, we developed the Kino-RRT\* algorithm, which utilizes a partial-final-state-free (PFF) optimal controller to improve the convergence performance of sampling-based motion planning of kinodynamic systems. Instead of sampling the full state of the robot, Kino-RRT\* only samples part of the state-space and the rest of the states are optimized by the PFF optimal controller. Although the algorithm is demonstrated on linear systems, the idea of PFF can be used as in [@Xie2015Towards; @Wolfslag2018RRT-CoLearn; @zheng2021sampling] for nonlinear kinodynamic systems as well. We tested the algorithm on robot systems with 4-D and 10-D state-spaces. In both cases, Kino-RRT\* showed better convergence compared to the standard kinodynamic RRT\*, achieving trajectories with better cost using much less time to compute. The proposed Kino-RRT\* algorithm shows potential in real-time kinodynamic motion planning for high-dimensional dynamical systems.

[^1]: This work has been supported by NSF awards IIS-1617630 and IIS-2008695

[^2]: $^{1}$Dongliang Zheng is with School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA 30332, USA `dzheng@gatech.edu`

[^3]: $^{2}$Panagiotis Tsiotras is with School of Aerospace Engineering and Institute for Robotics and Intelligent Machines, Georgia Institute of Technology, Atlanta, GA 30332, USA `tsiotras@gatech.edu`
