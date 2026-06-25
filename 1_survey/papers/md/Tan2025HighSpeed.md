---
citation_key: Tan2025HighSpeed
arxiv_id: 2503.11072
arxiv_url: https://arxiv.org/abs/2503.11072
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:27:53Z
origin: ai+web
reviewed: false
---

:::: frontmatter
[^1]

,

::: keyword
Trajectory optimization; convex programming; artificial potential field
:::
::::

# Introduction

As industrial technology continues to advance, a growing number of automotive devices have been developed, making trajectory generation a crucial area of research. Trajectory generation and motion planning focus on determining appropriate control strategies for agents---such as robots, drones, and other autonomous systems---to navigate from a starting point to a target while avoiding obstacles. An efficient planning algorithm is essential, as it can significantly reduce energy consumption and travel time while ensuring safety, ultimately leading to considerable economic benefits. Over the past decades, numerous planning algorithms have been developed. Despite varying methodologies and application contexts, these approaches can be broadly classified into three main categories [@three_methods]: search-based, sampling-based, and optimization-based methods. Among search-based algorithms, the A\* algorithm, introduced in 1968 [@{A*}], efficiently identifies optimal paths using heuristic functions [@{A*_effect}]. However, it faces high computational demands in large-scale or dense grid environments [@{A*_shorthand2}]. Subsequent enhancements such as D\* [@{D*}], which supports dynamic replanning in response to new obstacles, and ARA\* [@{ARA*}], which improves efficiency through incremental search, have improved the adaptability. Nevertheless, these variants still inherit the core scalability limitations of A\*, restricting their use in large-scale real-time applications.

In the domain of sampling-based algorithms, the Rapidly-exploring Random Tree (RRT) method offers an effective framework for obstacle avoidance by probabilistically exploring the configuration space [@RRT]. While standard RRT is valued for its simplicity and flexibility, its variant RRT\* [@{RRT*}] achieves asymptotic optimality at the expense of higher computational load. Although many RRT extensions have shown advantages in specific applications [@RRT_f4], issues such as hardware limitations and kinematic infeasibility continue to restrict their broader adoption. [Complementary to sampling-based approaches, the advancement of model predictive control (MPC) has enabled systematic solution of trajectory generation problems through optimization techniques.]{style="color: blue"} Indirect methods, such as those employing Pontryagin's maximum principle or Lagrange multipliers [@Pon] [@Lag], offer analytical insights but are often computationally challenging due to sensitivity to initial conditions and implementation complexity. In contrast, direct methods reformulate the optimal control problem into nonlinear programming (NLP) via parameterization and discretization, allowing numerical solutions using Newton's method [@Newton], ADMM [@ADMM0], [@ADMM] or heuristic (e.g., genetic algorithms) approaches. The common parameterzation and discretization methods include direct shooting method, collocation method and Pseudo-Spectrum Method, etc. Discrete optimization problems of this type are generally NP-hard and thus unsuitable for real-time onboard computation. Fortunately, convexification techniques can yield tractable solutions for specific problem classes by exploiting the efficiency of convex optimization. For non-convex input constraints---such as minimum thrust in rocket models---lossless convex relaxation [expands]{style="color: blue"} the control vector to transform constraints into convex forms [@LCVX1]. Despite introducing additional variables, the relaxed problem remains easier to solve due to its convex structure. For non-convex state constraints like obstacle avoidance, sequential convex programming can rapidly produce feasible trajectories [@SCP], though it may converge to suboptimal solutions [@tutorial]. Techniques such as adding trust regions [@TRSCVX], tightening approximations, or softening constraints can mitigate ill-conditioning and reduce artificial infeasibility [@GuSTO]. Direct optimization methods are widely used in time-optimal control. As for discrete model predictive control problems are relatively straightforward to formulate, line search methods can be effectively employed to determine the optimal control time. Alternatively, time-optimal control can also be addressed by solving a series of fixed-time optimal control subproblems iteratively [@Racing]. However, this method depends heavily on extensive map information and typically lacks terminal constraints, which may restrict its practical applicability.

This paper addresses the problem of generating collision-free trajectories in environments with static and dynamic obstacles. To enhance solution quality and time optimality in motion planning, we propose a dynamic trajectory generation algorithm based on an iterative two-layer optimization framework. Each iteration employs a small [period]{style="color: blue"} planning cycle with fixed final time, which is decomposed into two trajectory optimization subproblems and a trajectory search step. By incrementally construct planning cycles and concatenate segmented control inputs, the method produces a globally admissible control sequence capable of dynamic obstacle avoidance. Furthermore, we introduce two trajectory search algorithms for the optimization loop and analyze their feasibility conditions. The main contributions of this work are summarized as follows.

- We employ trajectory searching methods to generate restricted convex regions guided by nominal solutions, effectively mitigating non-convexity while maintaining feasibility. Additionally, we propose a customized artificial potential field method with kinematic reliability to serve as the trajectory search algorithm. This tailored approach can also function independently as a standalone planning algorithm in specific case.

- Our proposed algorithms have been validated to generate trajectories that achieve an approximately [local optimal control time]{style="color: blue"} under specified conditions and moderate assumptions. Compared with conventional motion planning solvers based on sequential convex programming, the proposed method exhibits enhanced robustness in dynamic environments while substantially reducing computational overhead---findings supported by numerical experiments, which demonstrate both a higher success rate and shorter total computation time.

- By decomposing the complete problem into planning cycles and solving one planning cycle in parallel mode while moving, we have developed a robust framework that ensures both reliability and precision while only relying on a part of map information at a specific time.

In the remainder of this paper, Section II formulates the optimal control problem and establishes the theoretical foundation for our approach. Section III introduces the two-layer optimization model and develops the corresponding trajectory search algorithms, along with a thorough analysis of their properties and effectiveness. Section IV presents numerical experiments conducted in both static and dynamic environments. Finally, Section V concludes the paper with a summary of findings.

*Notations:* throughout the subsequent sections, all sets are defined in $\mathbb{R}^n$ with context-specific $n$, and the [Euclidean norm]{style="color: blue"} $\left\| {\mathbf{a}} \right\| = \sqrt {\left\langle {\left. {{\mathbf{a,a}}} \right\rangle } \right.}  = \sqrt {{{\mathbf{a}}^ \top }{\mathbf{a}}}$, and we further let $\|\mathbf a \|_Q = \sqrt{\mathbf a^\top Q \mathbf a}$ with [$Q$ being a positive definite weighting matrix]{style="color: blue"}. The diameter of a set $\mathcal{S} \subset \mathbb{R}^n$ is defined as $$\begin{equation*}
    {\mathrm{diam}{(\mathcal S)}} := \left\{ \begin{array}{l}
        \quad   0, \hfill \mathcal S = \emptyset ,\\
        \sup \{ \|\mathbf y - \mathbf x\| :\mathbf x,\mathbf y \in \mathcal S\}, \hfill \quad else,
    \end{array} \right.
\end{equation*}$$ and for some $\mathbf x_0 \in \mathbb R^n$ with non-negative real number $d$, we denote by $\mathcal B(\mathbf x_0, d)$ the closed ball centered at $\mathbf x_0$ with radius $d$: $$\mathcal B(\mathbf x_0, d) := \{\mathbf x \in \mathbb R^n : \|\mathbf x - \mathbf x_0\| \leq d\}.$$ Sliced vectors are denoted $\mathbf{a}[i:j]$, representing rows $i$ to $j$ of column vector $\mathbf{a}$ (e.g., $\mathbf{a} = [a_1,a_2,a_3,a_4]^\top \Rightarrow \mathbf{a}[2:3] = [a_2,a_3]^\top$). For a set $\mathcal{S} \subseteq \mathbb{R}^{\ell_s}$, the sliced set is defined as $$\mathcal S[a:b] := \big\{ \mathbf x[a:b] \big| \mathbf x \in \mathcal S \big\}.$$ The gradient of a differentiable function $f : \mathbb R^n \mapsto \mathbb R$ is denoted $\nabla f(\mathbf{x}) := \left[ \frac{\partial f}{\partial x_1}, \cdots, \frac{\partial f}{\partial x_n} \right]^\top$. We use $\text{Null}(\cdot)$ for the null space, and $\mathrm{cl}(\cdot)$, $\mathrm{conv}(\cdot)$ for the closure and convex hull respectively. The term *speed* refers to the Euclidean norm of velocity.

# Problem Formulation

## Classic Framework

Trajectory generation aims to compute feasible and safe trajectories for a vehicle within a structured environment $\mathcal{M}$---referred to as the map---that contains obstacles, a target region, and an initial state. In this paper, $\mathcal M$ is defined in a unified Euclidean space. Each obstacle is denoted as $\mathcal{O}_i$ for $i \in \{1, 2, \dots, n_{obs}\}$, with $n_{obs}$ the total number of obstacles. The volume occupied by the vehicle is represented by $\mathcal{V}$. [As]{style="color: blue"} $\mathcal{M}$ is generally bounded, we assume that each $\mathcal O_i$ is bounded and that $\mathcal{V} \subset \mathcal{M}$ holds at all times. This simplification allows us to focus on the core contributions without loss of generality, as [the map containment constraints]{style="color: blue"} can be incorporated when needed. Collisions are strictly prohibited throughout the task, expressed mathematically as: $$\begin{equation}
    \mathcal O_i \bigcap \mathcal V = \emptyset \ , \ i \in \{1,2,\cdots,n_{obs}\}.
\end{equation}$$ For irregularly shaped obstacle regions $\mathcal{O}_i$, obtaining exact analytic descriptions is often intractable. To overcome this challenge, we adopt an approximation involves enclosing each obstacle region $\mathcal{O}_i$ within a union of closed balls. Specifically, there must exist some positions $x, p_1, p_2, \cdots, p_{n_{obs}} \in \mathcal M$ with $$\begin{equation}
    {{\mathcal O}_i} \subseteq {\mathcal B}({p_i},{\mathrm{diam}{(\mathcal O_i)}}/2) \label{eq3}
\end{equation}$$ for $i = 1,2, \cdots, n_{obs}$, and $$\begin{equation}
    {\mathcal V} \subseteq {\mathcal B}(x,\mathrm{diam}{(\mathcal V)}/2). \label{eq4}
\end{equation}$$ For conciseness, we denote $\mathcal{B}_i := \mathcal{B}(p_i, \mathrm{diam}(\mathcal{O}_i)/2)$ and $\mathcal{B}_{\mathcal{V}} := \mathcal{B}(x, \mathrm{diam}(\mathcal{V})/2)$ for such $x, p_1, \cdots, p_{n_{obs}}$. Thus, an approximated scenario can be created by substitute $\mathcal O_i , \mathcal V$ with $\mathcal B_i, \mathcal B_{\mathcal V}$. In the approximated scenario, prior knowledge of obstacle shapes is no longer required, significantly simplifying the design of subsequent algorithms. Consequently, the obstacle avoidance constraints can be expressed as $$\begin{equation}
    \|x - p_i\| \ge \frac{\mathrm{diam}{(\mathcal O_i)} + \mathrm{diam}{(\mathcal V)}}{2} := r_i \label{nonconvex_position_con},
\end{equation}$$ where $x$, $p_i$ and $r_i \geq 0$ are critical parameters used in constructing the planning problem. This shape approximation relies on two key assumptions, formalized as Assumptions 1 and 2 below.

::: {#original_A1 .assumption}
**Assumption 1**. *Given the map, both the initial and target positions lie outside all obstacle regions $\mathcal B_i$ for $i \in \{1,2,\cdots,n_{obs}\}$.*
:::

::: {#original_A2 .assumption}
**Assumption 2**. *For any pair of indices $i,j \in \{1, \cdots, n_{obs}\}$ with $i \neq j$, the obstacle regions are mutually disjoint. Furthermore, we assume the existence of a positive constant $\ell$ that $${\mathcal B}({p_i},{r_i} + 0.5\ell) \cap {\mathcal B}({p_j},{r_j} + 0.5\ell) = \emptyset$$ for all $i \ne j$.*
:::

Assumption 1 serves as the foundational premise underpinning all subsequent analyses. Assumption 2 introduces a more flexible condition, which can be intuitively understood as allowing multiple small obstacles---along with the gaps between them---to be treated as a single larger obstacle, as illustrated in Fig. 1. It is therefore evident that Assumption 2 is relatively mild.

:::: {#fig:fig1 .figure latex-placement="H"}
![](Fig1){width="85%"}

::: caption
A single irregular obstacle (top left) can be approximated by a closed ball (top right), while multiple densely clustered small obstacles (bottom left) may be merged into a larger enclosing ball (pink circle, bottom right) for simplified representation.
:::
::::

In this work, we define the state vector as $z(t) := [x^\top, \dot x^\top]^\top$ and consider a control-affine dynamic system $$\begin{equation}
    \dot{z}(t) = f_c(z,u) = f_a(z) + f_b(z) \cdot u, \label{non_linear_original}
\end{equation}$$ where $f_c$ is differentiable and $u$ denotes the control input. Physical constraints are given by $z^{\top}Q_1 z \le 1$ and $u^{\top}Q_2 u \le 1$, with $Q_1, Q_2$ being strictly positive definite weighting matrices. These constraints reflect practical limitations such as maximum speed limits ($\| \dot x\| \leq v_{\max}$), control input bounds ($\|u\| \leq u_{\max}$), and friction effects. Let $z_0$ and $z_f$ as the initial and one of the target state, respectively. The boundary constraints are then expressed as $$\begin{align}
    & z(0) = z_0   \label{initial_condition}, \\
    & \|z(t_f) - z_f\|_{Q_0} \leq \gamma , \label{boundary_condition}
\end{align}$$ where $Q_0$ is a positive definite weighting matrix, $t_f$ denotes the final time profiling the task's time cost, $z(t_f)$ is the ending state and [\[boundary_condition\]](#boundary_condition){reference-type="eqref" reference="boundary_condition"} profiles the target area.

With the objective of minimizing the control time, the original trajectory optimization problem is formulated as $$\begin{alignat}
{2}
    & \min_{z,u} && t_f \\
    & \mathrm{\quad s. t.} \ \ &&  \eqref{non_linear_original} - \eqref{boundary_condition}, \\
    & && \|z\|_{Q_1}^2 \leq 1,  \ \ \|u\|_{Q_2}^2 \leq 1.
\end{alignat}$$ To enable numerical optimization, the continuous problem must be discretized and parameterized. Given a fixed time step $h$, substitute $z(t)$ by $\{z_1, \cdots, z_{N+1}\}$ and $u(t)$ by $\{u_1, \cdots, u_N\}$ with $h$ as the sampling period, [\[non_linear_original\]](#non_linear_original){reference-type="eqref" reference="non_linear_original"} can be then discretized into the algebraic form: $$\begin{align}
    &z_{i+1} - z_{i} = h f_c(z_i, u_i), \nonumber \\
    & \quad \Rightarrow z_{i+1} := f(z_i, u_i). \label{c2d_original}
\end{align}$$ We denote $\{z_1, \cdots, z_{N+1}; u_1, \cdots, u_N\}$ by $\{Z; U\}_N$, then a discretized optimization problem $\mathcal P_0$ is obtained as $$\begin{align}
    &{\min}_{\{Z; U\}_N} &&Nh \nonumber \\
    & \mathrm{\quad s. t.}  &&\eqref{c2d_original}, \nonumber\\
    & &&\ G_1(z_i) := z_i^{\top}Q_1 z_i - 1 \leq 0, \label{DQ_1} \\
    & &&G_2(u_i) := u_i^{\top}Q_2 u_i - 1 \leq 0, \label{DQ_2}  \\
    & &&z_1 = z_0, \label{initial_condition_discrete} \\
    & &&\|z_{N+1} - z_f\|_{Q_0} \leq \gamma, \label{boundary_condition_d}\\
    & &&\|z_i[1:2] - p_j\|\ge r_j, 1 \leq j \leq n_{obs}  \label{nonconvex_position_con_discrete}.
\end{align}$$

## Our Proposed Framework

We assume $\mathcal P_0$ is solvable. As $\mathcal P_0$ exhibits a typical structure commonly found in related literature, this assumption is mild, and also necessary. However, solving $\mathcal P_0$ quickly and robustly remains challenging due to its non-convex nature. In our framework, $\mathcal P_0$ is not solved directly. Instead, we iteratively construct and solve discretized approximated problems using a fixed time step $h$ and pre-selsected $N$. By concatenating the resulting trajectory segments, $\mathcal P_0$ can be effectively solved under mild assumptions.

We further linearize [\[c2d_original\]](#c2d_original){reference-type="eqref" reference="c2d_original"} as $$\begin{equation}
    z_{i+1} := A(z_0) z_i + B(z_0) u_i + w(z_0), \label{c2d_var}
\end{equation}$$ where $A_c(z_0), B_c(z_0)$ are the Jacobi matrices of $f$ at $z_0$, and $w_c(z_0)$ denotes the draft. In the most special case, if $u(t)$ represents the acceleration, then we have $$A_c(\cdot) \equiv \left( {\begin{array}{*{20}{c}}
        \mathbf O_{2 \times 2}&\mathbf I_{2 \times 2}\\
        \mathbf O_{2 \times 2}&\mathbf O_{2 \times 2}
\end{array}} \right),B_c(\cdot) \equiv \left( {\begin{array}{*{20}{c}}
        \mathbf O_{2 \times 2}\\
        \mathbf I_{2 \times 2}
\end{array}} \right),w_c(\cdot) \equiv 0,$$ where $\mathbf I_{2 \times 2}$ is the 2-dimensional identity matrix, $\mathbf O_{2 \times 2}$ is the $2 \times 2$ zero matrix. Let $$\begin{equation}
    J(z_i,u_i) = [z_f - z_{N+1}]^\top Q_0 [z_f - z_{N+1}], \label{J_P_1}
\end{equation}$$ then two problems classes can be formulated as $\mathcal P_1(z_0; N)$: $$\begin{align}
    &{\min}_{\{Z; U\}_N} \hspace{-7em}  &&\eqref{J_P_1} \nonumber \\
    & \mathrm{\; \; \; s. t.} && \eqref{c2d_original}, \eqref{DQ_1} - \eqref{initial_condition_discrete}, \eqref{nonconvex_position_con_discrete} \nonumber
\end{align}$$ and $\mathcal P_1'(z_0; N ; A(z_0), B(z_0))$: $$\begin{align}
    &{\min}_{\{Z; U\}_N} \hspace{-7em} &&\eqref{J_P_1} \nonumber \\
    & \mathrm{\; \; \; s. t.} &&\eqref{DQ_1}-\eqref{initial_condition_discrete} ,\eqref{nonconvex_position_con_discrete}, \eqref{c2d_var} \nonumber
\end{align}$$ In the subsequent content, when no ambiguity arises, we also adopt the simplified notations $\mathcal P_1(\cdot), \mathcal P_1(z_0; \cdot)$, $\mathcal P_1'(\cdot), \mathcal P_1'(z_0; \cdot)$, etc. In both problem classes, $N$ is referred to as the horizon, $Nh$ is called the [control time]{style="color: red"}. Throughout our method, $\mathcal P_0$ is solved equivalently by solving some $\mathcal{P}_1(\cdot)$ with small $Nh$ iteratively. [For weakly nonlinear systems with sufficiently short control times, the use of approximated dynamics---with continuous updates to $A(z_0)$, $B(z_0)$, and $w(\cdot)$---preserves solution accuracy. That is, the solution of $\mathcal{P}_1'(z_0; N; A(z_0), B(z_0))$ closely approximates that of $\mathcal{P}_1(z_0; N)$. Therefore, the short-control time problem $\mathcal{P}_1(\cdot)$ cab be replaced by $\mathcal{P}_1'(z_0; N; A(z_0), B(z_0))$, while $z_0$, $N$, $A(z_0)$, and $B(z_0)$ are updated in real time to maintain precision.]{style="color: blue"} The formulating and solving of $\mathcal{P}_1(z_0; N)$ is called a **planning cycle**.

# Algorithm and Analysis

[As the solution of $\mathcal P_0$ is obtained by iteratively run planning cycles, each planning cycle is further computed through three sequential subroutines in our works. At the start of each planning cycle, the current state $z_0$ along with matrices $A(z_0)$ and $B(z_0)$ are determined to formulate $\mathcal P_1'(\cdot)$. Then, a relaxed version of $\mathcal P_1'(\cdot)$---called the relaxed problem---is solved to generate a nominal solution and extract a collision-free convex region, and a strict convex optimization within this region is formulated to compute the final trajectory segment. This convex-styled process maintains the robustness and fasten the computation. This section provides a detailed breakdown of these steps and conducts the corresponding mathematical analyses to validate their efficacy.]{style="color: blue"}

## [Reformulation of Planning Cycles]{style="color: blue"}

[With given $z_0, N, A(z_0), B(z_0)$, we denote the relaxed problem by $\mathcal P_r(z_0; N; A(z_0), B(z_0))$, which derived from $\mathcal P_1'(z_0; N; A(z_0), B(z_0))$ while [\[boundary_condition_d\]](#boundary_condition_d){reference-type="eqref" reference="boundary_condition_d"} and all the non-convex obstacle avoiding constraints [\[nonconvex_position_con_discrete\]](#nonconvex_position_con_discrete){reference-type="eqref" reference="nonconvex_position_con_discrete"} are removed, i.e. we have $\mathcal P_r(z_0; N, A(z_0), B(z_0))$:]{style="color: blue"} $$\begin{align}
    &{\min}_{\{Z; U\}_N} \hspace{-10em} &&\eqref{J_P_1} \nonumber \\
    &\mathrm{\; \; \; s. t.} && \eqref{DQ_1} - \eqref{initial_condition_discrete}, \eqref{c2d_var}. \nonumber
\end{align}$$ The convexity of $\mathcal P_r(\cdot)$ is ensured since [\[boundary_condition_d\]](#boundary_condition_d){reference-type="eqref" reference="boundary_condition_d"} is not considered in this problem. If $\mathcal P_r(z_0; N; A(z_0), B(z_0))$ is solvable, then its optimizer is referred to as the nominal solution of $\mathcal P_r(z_0; N; A(z_0), B(z_0))$.

::: remark
**Remark 1**. *Note that we have $z_1 = z_0$ according to [\[initial_condition_discrete\]](#initial_condition_discrete){reference-type="eqref" reference="initial_condition_discrete"}. Therefore, $\mathcal P_1(z_0; N)$ and $\mathcal P_1'(z_0;N;\cdot)$ can also be seen as optimization problems of $\{z_2, \cdots, z_{N + 1}, u_1, \cdots, u_N\}$.*
:::

Suppose is a constraint-complaint solution of $\mathcal P_1'(z_0; N; A(z_0), B(z_0))$ denoted by $$F := {\{\tilde z_1, \cdots ,\tilde z_{N+1}; \tilde u_1, \cdots , \tilde u_N\}},$$ $\{\bar z_1, \cdots ,\bar z_{N+1}; \bar u_1, \cdots , \bar u_N\}$ is the optimizer of the corresponding $\mathcal P_r(z_0; N; A(z_0), B(z_0))$, then a linear interpolation can be implemented as $$\begin{align*}
    z_i[1:2] = (\lambda \tilde z_i + (1 - \lambda) \bar z_i)[1:2],
\end{align*}$$ where a given $\lambda$ determines [the]{style="color: blue"} unique $z[1:2]$. The method for obtaining $F$ is referred to as the **searching algorithm**, which will be detailed in a later subsection. Building upon the interpolation method, as $\tilde z_i[1:2]$ is collision-free points, we define $\lambda_{\min} := \{\lambda_{\min,1},\lambda_{\min,2}, \cdots , \lambda_{\min,N+1}\}$ with $$\begin{align*}
    \lambda_{\min,i} = \max \bigg( 
    \bigcup_{j=1}^{n_{\text{obs}}} \big\{ 
    & \max\big\{ \lambda_i : 
    \exists p_j, r_j, 
     \nonumber \\
    & \| z_i[1:2] - p_j \| = r_j 
    \big\}, 0 
    \big\} \bigg).
\end{align*}$$ $\!\!$Under the definition of $\lambda_{\min,i}$, any $z_i[1:2] = (\lambda \tilde z_i + (1 - \lambda) \bar z_i)[1:2]$ with $0 < \lambda_{\min,i} < \lambda < 1$ is a collision-free point in $\mathcal M$, while $[\lambda_{\min,i} \tilde z_i + (1- \lambda_{\min,i}) \bar z][1:2]$ lies on the edge of one obstacle if $\lambda_{\min,i} = 0$. By further introducing variables $\lambda_{f,i}$ and $\lambda_{d,i}$ with $i = 1, 2, \cdots, N + 1$ and letting $$\begin{align}
    z_i &= (1 - \lambda _{\min,i} - \lambda_{f,i} + \lambda_{\min,i}\lambda_{f,i}) \bar{z}_{i} \nonumber  \\
    & \quad +(\lambda_{\min,i} + \lambda_{f,i} - \lambda_{\min,i}\lambda_{f,i}-\lambda_{d,i})\tilde z_i  \nonumber \\ 
    & \quad + \lambda_{d,i} \tilde z_{\min\{1,i-1\}}, \label{z_transfer}
\end{align}$$ some convex sets of $\mathcal M$ can be extracted as $$\begin{align}
    \textcolor{blue}{\mathcal Z_i = \big\{ z_i \big|\eqref{z_transfer}, 0 \leq \lambda_{d,i} \leq \lambda_{f,i} \leq 1 \big\}, 1 \leq i \leq N + 1}.
\end{align}$$

![A Visualization of obtaining $\mathcal Z_i$](Tan2025HighSpeed_figs/subsets.png){#subset width="100%"}

$\!\!$Fig. [2](#subset){reference-type="ref" reference="subset"} above illustrates the construction and geometric interpretation of $\mathcal Z_i[1:2]$, $\lambda_{\min,i}, \lambda_{f,i}$ and $\lambda_{d,i}$.

Although the convexity of these extracted sets are guaranteed, the non-feasibility may remain. To further ensure the feasibility, linear inequality constraints on $\lambda_{f,i} , \lambda_{d,i}$ are introduced as $$\begin{equation}
    \lambda_{d,i} \leq k_i \lambda_{f,i},  \label{constraint_di}
\end{equation}$$ where $0 \leq k_i \leq 1$ [is]{style="color: blue"} pre-selected to keep the convexified area out of obstacles. Define $$\begin{align*}
    \lambda_{f} &:= (\lambda_{f,1},\lambda_{f,2},\cdots,\lambda_{f,N+1})^{\top}, \\
    \lambda_{d} &:= (\lambda_{d,1},\lambda_{d,2},\cdots,\lambda_{d,N+1})^{\top},
\end{align*}$$ and let $$\begin{align}
    J_s(\lambda_f, \lambda_d; \rho) &:= J(z_i, u_i) + \rho \cdot \|z_0 - z_f\| \|\lambda_f - \mathbf{1}\|^2 \label{Js}
\end{align}$$ with the weighting parameter $\rho \geq 0$, then the corresponding strict problem can be formulated as $\mathcal P_s(z_0; N; A(z_0), B(z_0))$: $$\begin{align}
    & \mathop {\min }\limits_{\{ {\lambda _f}, {\lambda _{d}}\} } \hspace{-7em} &&\hspace{-3em}J_s(\lambda_f, \lambda_d; \rho) \nonumber \\
    & \mathrm{\quad \ \ s. t.} &&\hspace{-3em}0 \leq \lambda_{f,i} \leq 1,   \label{constraint_fi}\\
    &  &&\hspace{-3em}\eqref{DQ_1} - \eqref{initial_condition_discrete}, \eqref{c2d_var} , \eqref{constraint_di}. \nonumber
\end{align}$$ According to [\[z_transfer\]](#z_transfer){reference-type="eqref" reference="z_transfer"} and the given dynamics, the right hand side of [\[Js\]](#Js){reference-type="eqref" reference="Js"} is also a function of $\lambda_f, \lambda_d$.

[For given $\mathcal P_1'(z_0; N; A(z_0), B(z_0))$, we now examine the solvability of the corresponding $\mathcal P_r(\cdot), \mathcal P_s(\cdot)$. Clearly, if $\mathcal P_1'(z_0; N; A(z_0), B(z_0))$ is solvable, then $\mathcal P_r(z_0; N; A(z_0), B(z_0))$ is also solvable since it has a relaxed constraint set. On other hand, $\mathcal P_s(z_0; N; A(z_0), B(z_0))$ is solvable if $\{\tilde z_1, \cdots, \tilde z_{N + 1}; \tilde u_1, \cdots, \tilde u_N \}$ satisfies the constraints of $\mathcal P_1'(\cdot)$ --- that is, when $\lambda_f = \mathbf 0$ and $\lambda_d = \mathbf 0$. However, if $\mathcal P_1'(z_0; N; A(z_0), B(z_0))$ is unsolvable, specific challenges may occur, which we refer to as connective infeasibility as formalized in Definition 1.]{style="color: blue"}

::: definition
**Definition 1**. *[$\mathcal P_1'(z_0; N; A(z_0), B(z_0))$ is said to exhibit **connective infeasibility** when, despite the problem $\mathcal{P}_0$ being solvable, either the relaxed or strict problem derived from $\mathcal P_1'(z_0; N; A(z_0), B(z_0))$ becomes unsolvable.]{style="color: blue"}*
:::

[Connective infeasibility may occur when the terminal state $z_{N+1}$ simultaneously satisfies: (1) the positional proximity to obstacles ($z_{N+1}[1:2]$ near obstacle boundaries), and (2) the conflicting dynamics (significant velocity toward obstacles).]{style="color: blue"} To mitigate the connective infeasibility, the term $\rho$ is introduced in $\mathcal P_s(\cdot)$ to enhance the robustness, where it is referred to as the safety term. Based on the preceding developments, our solution framework can be summarized in Fig. [3](#fig:subprocess){reference-type="ref" reference="fig:subprocess"} below.

![Processes solving $\mathcal P_0$ in the proposed framework](Tan2025HighSpeed_figs/subprocess.png){#fig:subprocess width="100%"}

## Entire Algorithm

The entire algorithm of our proposed method is represented as Algorithm 1.

:::: algorithm
::: algorithmic
: The map information $\mathcal M$.\
$K \gets 1$;\

$F^{(K)} := \{\tilde z_1^{(K)}, \cdots ,\tilde z_{N^{(K)}+1}^{(K)}; \tilde u_1^{(K)}, \cdots , \tilde u_{N^{(K)}}^{(K)}\}$ [through Searching Algorithm]{style="color: blue"} Calculate $\{z_1^{(K)}, \cdots, z_{N^{(K)} + 1}^{(K)}; u_1^{(K)}, \cdots, z_{N^{(K)}}^{(K)}\}$ $\{ u_1^{(K)},\cdots,u_{\hat N^{(K)}}^{(K)}\}$ $K \gets K+1$;\
:::
::::

In Algorithm 1 and subsequent analysis, we use superscription $(\cdot)^{(K)}$ to represent problems, relative variables and parameters in the $K^{\mathrm{th}}$ planning cycle. To be detailed, let $\mathcal P_{(\cdot)}^{(K)}$, $\mathcal P_1'^{(K)}$ be the abbreviation of $\mathcal P_{(\cdot)}(z_0^{(K)}; N^{(K)}; A^{(K)}, B^{(K)})$, $\mathcal P_1'(z_0^{(K)}; N^{(K)}; A^{(K)}, B^{(K)})$. $\bar z_i^{(K)}$ ($\bar u_i^{(K)}$) and $\tilde z_i^{(K)}$ ($\tilde u_i^{(K)}$) are derived from $\mathcal P_r^{(K)}$ and a feasible solution of the $K^{\text{th}}$ planning cycle respectively by searching algorithm. $\{\lambda_f^{(K)}, \lambda_d^{(K)}\}$ is the optimizer of $\mathcal P_s^{(K)}$, while $z_i^{(K)}, u_i^{(K)}$ are computed from $\{\lambda_f^{(K)}, \lambda_d^{(K)}\}$. Algorithm 1 follows a concise iterative structure: it solves the current planning cycle, updates the initial state $z_0$ using the resulting solution, and proceeds to construct and solve the next planning cycle. This iterative process continues until the quit condition [\[boundary_condition_d\]](#boundary_condition_d){reference-type="eqref" reference="boundary_condition_d"} is reached. In this process, the entire control is obtained by sequentially concatenating $\{u_1^{(i)}, \cdots , u_{\hat N^{(i)}}^{(i)}\}, i = 1, 2, \cdots$. Note $N^{(K)}$ is initially generated from searching algorithms correspondingly, and subsequently they are used as the problem size in both $\mathcal P_r^{(K)}$ and $\mathcal P_s^{(K)}$. To maintain the performance of Algorithm 1, the solution of one planning cycle is applied only partially by choosing a smaller $\hat N^{(K)}$ and applying $\{ u_1,\cdots,u_{\hat N^{(K)}}\}$. Before proceeding with the algorithm analysis, we will first present two customized trajectory searching algorithms which demonstrate good performance in experiments.

## Customized Vortex Artificial Potential Field

Based on the artificial potential field (APF) [@APF] method, we propose the Customized Vortex Artificial Potential Field (CVAPF) method as a trajectory search algorithm. Tailored for double-integrator systems, it readily extends to general affine models. Conventional APF simulates a virtual force field to navigate while avoiding obstacles, inspired by physical systems under conservative forces. It's enhancement, the Vortex-APF (VAPF) [@VAPF_Intro], extends traditional potential fields by incorporating a vortex field that modulate repulsion into rotational patterns, aiding navigation in complex environments. As in both APF and VAPF, the attractive potential is defined as $$\begin{equation}
    P_{att}(z[1:2]) =  \big\|z[1:2] -  z_f[1:2]\big\|^2.
\end{equation}$$ The repulsive potential acts to drive the vehicle away from obstacles, [and]{style="color: blue"} we formulate it with the form similar to [@APF_REP] as $$\begin{equation}
    P_{rep}(z[1:2]) = \zeta \sum\limits_{j = 1}^{n_{obs}} {\exp \left( {\frac{{ - \beta  \cdot (\left\| {z[1:2] - {p_j}} \right\| - {r_j})}}{{{r_j}}}} \right)},
\end{equation}$$ [where $\beta$ and $\zeta$ are pre-selected positive weights.]{style="color: blue"} For the APF algorithm, the moving direction can be obtained instantly by calculating $-(\nabla P_{att} + \nabla P_{rep})$ directly. For the VAPF algotirhm, the vortex field $E_v(z[1:2])$ is orthogonal to $\nabla P_{rep}(z[1:2])$. Its direction $\mathbf{d}(z[1:2])$ is selected from the unit set $$\mathcal{D}(z[1:2]) := \left\{ \tilde{\mathbf{d}} \in \mathrm{Null}(\nabla P_{rep}(z[1:2])) \mid \| \tilde{\mathbf{d}} \| = 1 \right\}.$$ The field magnitude is scaled by $\zeta_v$, giving $E_v(z[1:2]) = \zeta_v \, \mathbf{d}(z[1:2])$. In a 2D map, the set $\mathcal{D}(\cdot)$ contains at least two candidate directions. When $\nabla P_{rep}(z[1:2]) = \mathbf{0}$, the direction $\mathbf{d}(z[1:2])$ may be chosen as any unit vector. By incorporating additional directional selection criteria [@SAPF]---rather than restricting to a single turning direction as in [@LTAPF]---the VAPF algorithm can achieve improved path quality. For instance, it could help to find a shorter way when avoiding an obstacle in the forward of the vehicle, as shown in Fig.2. Denote the expected subsequent moving direction of point $\tilde z_i$ as $E_{\tilde z_i}^\dagger$, then the VAPF algorithm calculates

![The solid red line and the dashed blue line represent two possible paths on a map. However, sharp turns in the red path typically signal that the vehicle is slowing down at those points, leading to longer travel times and lower solution quality.](Fig2){#fig:fig2 width="80%"}

$$\begin{align}
    {E({{\tilde z}_i}[1:2])}  &=  - \big(\nabla {P_{att}}({\tilde z_i}[1:2]) + \nabla {P_{rep}}({\tilde z_i}[1:2]) \big) \nonumber\\
    & \quad + {E_v}({\tilde z_i}[1:2]), \nonumber
\end{align}$$ and $$\begin{equation}
    E^\dag({\tilde z}_i[1:2])  = \frac{E(\tilde z_i[1:2])}{\|E(\tilde z_i[1:2])\|}. \nonumber
\end{equation}$$ The vortex field mitigates local minima issues common in APF [@OSC], [@APF_LOCAL_MINIMA], enabling smoother navigation in complex environments.

To further ensure dynamic feasibility, CVAPF introduces a speed search step: once a direction is selected, feasible speeds consistent with physical constraints are computed. If available, a velocity combining direction and admissible speed is chosen; otherwise, a safe deceleration is applied to slow the vehicle while steering it toward the target direction. The complete CVAPF procedure is outlined in Algorithm 2.

:::: algorithm
::: algorithmic
: Map Information $\mathcal M$, Current state $z_0^{(K)}$, speed and accelerations $v_{\max}, a_{\max}$.\
$N \gets 0$; $\tilde z_0 \gets z_0^{(K)}$;\

\
\
\
\
\
\
\
$N \gets N+1$

; \
\
:::
::::

In Algorithm 2, $a_{safe}$ is utilized to lower the speed of the agent and alter its direction. Since $$\begin{equation*}
    \begin{aligned}
        \big\| {{a_{safe}}} \big\| &= \left\| {{a_1}{E^\dag }({\tilde z_{i + 1}}[1:2]) - {a_0}\frac{{{\tilde z_i}[3:4]}}{{\|{\tilde z_i}[3:4]\|}}} \right\| \hfill \\
        &\leq \bigg\| {{a_1}{E^\dag }({\tilde z_{i + 1}}[1:2])} \bigg\| + \left\| {{a_0}\frac{{{\tilde z_i}[3:4]}}{{\|{\tilde z_i}[3:4]\|}}} \right\| \hfill \\
        &= {a_1} + {a_0}, \hfill \\ 
\end{aligned}
\end{equation*}$$ $a_{safe} \leq a_{\max}$ can be easily guaranteed by selecting $a_1$ and $a_0$ with $a_0 + a_1 \leq a_{\max}$.

The $N$ determined by Algorithm 2 is critical in generating [high-quality]{style="color: blue"} trajectories, [as larger values of $N$ correspond to longer period and further compromise both real-time performance and solution accuracy]{style="color: blue"}. [Moreover, we have found that having the trajectory searching algorithm terminate at a safer position is helpful to enhance the robustness, for instance, the connective infeasibility can greatly be mitigated.]{style="color: blue"} On this basis, Algorithm 2 introduces a $\mathtt{Not\_Safe}$ sign. Define $$\begin{equation}
    {T_s} := \Big\{ t \in \left[ {0,{t_w}} \right]\Big| {{z_{N+1}}[1:2] + {z_{N+1}}[3:4]  t \in \bigcup\limits_{i = 1}^{n_{obs}} {{\mathcal B_i}} }  \Big\}, \nonumber
\end{equation}$$ then $\mathtt{Not\_Safe}$ is given by $$\mathtt{Not\_Safe} = \left\{ \begin{aligned}
    &0, \quad &&T_s = \emptyset, \\
    &1,  &&else,
\end{aligned} \right.$$ and $\min \ T_s$ is also a vital parameter used in the updating of $\rho^{(K)}$, where a smaller $\min \ T_s$ requires bigger $\rho^{(K)}$. Since $N^{(K)}$ generated in Algorithm 2 can be large, adjusting $N^{(K)}$ is meaningful to maintain the precision. These steps also show the necessity to substitute $N^{(K)}$ with $\hat N^{(K)}$ in Algorithm 1. Therefore, $N_ {\max}$ is further introduced to confine the length of applied control input.

## Customized Dynamic Window Approach

The Customized Dynamic Window Approach (CDWA) is designed as another searching algorithm for nonlinear models based on dynamic window approach (DWA) [@DWA]. By judiciously balancing the trade-offs between speed and safety, DWA enables agents to navigate dynamic environments with minimal risks. The DWA centers on the concept of a "dynamic window." This window represents the set of feasible control inputs available to an agent in its current state. Its construction incorporates multiple state factors, including position, orientation, and velocity. System-specific constraints are also integral to this formulation. From the agent's perspective, it is essential to predict proper actions based on its current state---i.e., to construct a dynamic window. From the algorithm designer's standpoint, defining a policy to select actions from these feasible sets is equally critical.

In order to apply DWA effectively in our work, [the]{style="color: blue"} CDWA is proposed. Following the general DWA methods, we first identify the dynamic window at the current state, which is achieved by calculating the possible control inputs based on constraints. Next, a subset of these feasible inputs is extracted for evaluation according to the map information, accompanied with $\mathtt{Not\_Safe}$ flag and $\min T_s$. The state of the next time step is instantly anticipated using the chosen input while refreshing the current state by the anticipated state in the end. Repeat these processes several loops to ultimately generate a trajectory consisting of $N$ inputs and $N+1$ states. The pseudo-code of our proposed CDWA is demonstrated in Algorithm 3 below.

:::: algorithm
::: algorithmic
: Map information $\mathcal M$, state $z_0$.\
;\
:::
::::

## Theoretical Guarantees

We subsequently show the convergence property of Algorithm 1 in a mild assumption given in Assumption [3](#todo20241117){reference-type="ref" reference="todo20241117"}.

::: {#todo20241117 .assumption}
**Assumption 3**. *[there exists a contraction factor $0 \leq \kappa < 1$]{style="color: blue"}, which makes $$\begin{equation}
        \frac{J_s({\lambda_f}^{(K)} , {\lambda_d}^{(K)}; \rho^{(K)})}
        {J_s({\lambda_f}^{(K-1)} , {\lambda_d}^{(K-1)}; \rho^{(K-1)})} \leq \kappa  \label{ass3}
\end{equation}$$ [hold for all but finitely many iterations $K$]{style="color: blue"}. In other words, the number of iterations that violate [\[ass3\]](#ass3){reference-type="eqref" reference="ass3"} is limited.*
:::

We discuss two complementary circumstances to explain the reasonableness of Assumption [3](#todo20241117){reference-type="ref" reference="todo20241117"}. For the Case I, consider that $J_s({\lambda_f}^{(K-1)} , {\lambda_d}^{(K-1)}; \rho^{(K-1)}) \gg \gamma$. Under this precondition, the cost from velocity can be set to a relatively small level if a $Q_0$ is chosen properly, and the cost function is then mainly decided by the position. Thus, $J_s({\lambda_f}^{(K+1)} , {\lambda_d}^{(K+1)}; \rho^{(K+1)}) \leq J_s({\lambda_f}^{(K)} , {\lambda_d}^{(K)}; \rho^{(K)})$ is naturally satisfied with the assistance of the searching algorithm if the initial velocity $z^{(K)}_{0}[3:4]$ remains moderate. On the other hand, if the initial velocity is undesirable, e.g. the vehicle moves away from the target area at maximum speed, it can still achieve [\[ass3\]](#ass3){reference-type="eqref" reference="ass3"} after several cycles. Moreover, when encountering obstacles, the vehicle necessitates strategic decision-making regarding its directional maneuver. Since all the obstacles are circle-like, there exists at least one direction that makes the vehicle get closer to the target area. The search algorithm can prioritize this direction. Experiments also show the mildness of Case I. Case II is complementary to Case I. When $J_s({\lambda_f}^{(K-1)} , {\lambda_d}^{(K-1)}; \rho^{(K-1)}) \gg \gamma$ is not satisfied, properly readjusting $\rho^{(K)}$ can drive the vehicle to meet the boundary constraint according to the convexity property of $\mathcal P_s$ if the trajectory searching algorithm can divert the vehicle to the target area. Thus, Assumption 3 is moderate. Combined with Assumption 1, it can be proven that the target area is reachable within limited planning cycles, as demonstrated in Theorem 1.

::: {#theorem_1 .theorem}
**Theorem 1**. *For given $\gamma$, $z^{(K+1)}_{N+1}$ can be obtained with $\| z^{(K+1)}_{N+1} - z_f \|_{Q_0} \leq \gamma$ after executing finite planning cycles.*
:::

***Proof.*** Under Assumption 4, suppose [\[ass3\]](#ass3){reference-type="eqref" reference="ass3"} is violated at the planning cycle $K_1 , K_2 , \cdots , K_m$, and we define $$\begin{equation}
    \kappa_i  = \frac{J_s({\lambda _f^{(K_i + 1)}},{\lambda _d^{(K_i + 1)}};\rho^{(K_i + 1)})}{J_s({\lambda _f^{(K_i)}},{\lambda _d^{(K_i)}};\rho^{(K_i)})}.
\end{equation}$$ Apparently, $K_m + 1$ cannot be the last iteration. For any $K \geq K_m$, we have $$\begin{equation}
    \prod\limits_{i = 1}^K {\frac{{J_s({\lambda _f^{(i+1)}},{\lambda _d^{(i+1)}};\rho^{(i+1)})}}{{J_s({\lambda _f^{(i)}},{\lambda _d^{(i)}};\rho^{(i)})}}}  \leq {\kappa ^{K - m}} \cdot \prod\limits_{i = 1}^m {{\kappa _i}} .
\end{equation}$$ Since $\| z^{(K+1)}_{N+1} - z_f \| \geq \gamma$ keeps true during each planning cycle except the last one, $J_s({\lambda _f^{(K)}},{\lambda _d^{(K)}};\rho^{(K)}) \geq \gamma$ is then consistently satisfied, which indicates that $\kappa _i \leq J_s({\lambda _f^{(K_i + 1)}},{\lambda _d^{(K_i + 1)}};\rho^{(K_i + 1)}) / \gamma$ are too bounded for any $\kappa_i$. Consequently, we have $$\begin{align}
    \left\| {z_{N + 1}^{(K + 1)} - {z_f}} \right\|_{Q_0} &\leq J_s({\lambda _f^{(K+1)}},{\lambda _d^{(K+1)}},\rho^{(K+1)}) \nonumber \\
    & \leq  J_s({\lambda _f^{(1)}},{\lambda _d^{(1)}},\rho^{(1)}) {\kappa ^{K - m}} \cdot \prod\limits_{i = 1}^m {{\kappa _i}}.
\end{align}$$ Take $$\begin{equation}
    K > \frac{{\left( {\log \frac{\gamma}{J_s({\lambda _f^{(1)}},{\lambda _d^{(1)}},\rho^{(1)})} - \sum\limits_{i = 1}^m {\log {\kappa _i}} } \right)}}{{\log \kappa }} + m,
\end{equation}$$ then $\| z^{(K+1)}_{N^{(K)}+1} - z_f \|_{Q_0} \leq \gamma$ holds after executing $K$ planning cycles, thereby completes the proof. $\square$

[Building upon Theorem [1](#theorem_1){reference-type="ref" reference="theorem_1"}, we will further establish the sufficient condition for the local optimality property of the concatenated solution. Here, two assumptions are required for further analysis, which is demonstrated as Assumptions [4](#Full_Rank){reference-type="ref" reference="Full_Rank"}-[5](#KKT){reference-type="ref" reference="KKT"}.]{style="color: blue"}

::: {#Full_Rank .assumption}
**Assumption 4**. *In the subsequent analysis, for each planning cycle $\mathcal{P}_1'(z_0^{(K)}; N^{(K)}; A^{(K)}, B^{(K)})$, $B^{(K)}$ has full column rank. For the corresponding problem $\mathcal{P}_1(z_0^{(K)}; N^{(K)})$, the Jacobian matrix $\left( \frac{\partial f}{\partial u} \right)^\top$ evaluated at the optimizer is also of full column rank.*
:::

::: remark
**Remark 2**. *Assumption 4 is both important and mild. For a full-column-rank Jacobian $\big(\frac{\partial f}{\partial u}\big)^\top$, we have $\left( \frac{\partial f}{\partial u} \right)^\top \upsilon = 0 \Rightarrow \upsilon = 0$ for any relevant vector $\upsilon$, which is crucial in subsequent theoretical proofs. Moreover, this condition is naturally satisfied in most underactuated systems, aligning well with practical engineering applications.*
:::

We further introduce $\mathscr L_2(z_0;\cdot), \mathscr L_3(z_0;\cdot), \cdots$ to denote the Lagrangian function of $\mathcal P_1(z_0;N; \cdot)$. Namely, in $\mathcal P_1(z_0;N)$, we define $$\begin{align}
    &\mathscr L_{N}(z_0;z_i, u_i, \upsilon_i, \zeta_{ij}, s_i, q_i) := \left\| {{z_{N+1 }}} \right\|_{{Q_0}}^2 \nonumber \\
    &\quad + \sum\limits_{i = 1}^{N} {{\upsilon _i}\left( {{z_{i + 1}} - f(z_i, u_i)} \right)}  \nonumber \\
    & \quad + \sum\limits_{i = 1}^{N + 1} {\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta _{ij}}\left( {r_j^2 - {{\left\| {{z_i}[1:2] - {p_j}} \right\|}^2}} \right)} } \nonumber \\
    & \quad + \sum\limits_{i = 1}^{N+1} {{s_i}{G_1}({z_i})}  + \sum\limits_{i = 1}^{N} {{q_i}{G_2}({u_i})}, \label{lagrange}
\end{align}$$ where $\upsilon_i, \zeta_{ij}, s_i, q_i$ are Lagrange multipliers.

::: {#KKT .assumption}
**Assumption 5**. *The local optimizer of $\mathcal{P}_1(z_0; N)$ (if exists) satisfies the Mangasarian--Fromovitz constraint qualification (MFCQ) [@MFCQ]. Specifically, at such a optimizer, the gradients of all active equality constraints are linearly independent, and there exists a vector that is:*

*1). a descent direction for all active inequality constraints;*

*2). orthogonal to the gradients of all equality constraints.*
:::

Under Assumption 5, if $\mathcal P_1(\cdot)$ admits a local optimizer, then there exists a pair of Lagrange multipliers such that the optimizer satisfies the Karush--Kuhn--Tucker (KKT) conditions. This result further leads to Theorem 2.

::: {#revised_th_2 .theorem}
**Theorem 2**. *Suppose $\mathcal{P}_1(z_0; m)$ has a local optimizer $\{z_1^1, z_2^1, \cdots, z_{m+1}^1; u_1^1, \cdots, u_m^1\}$. For any $m'\leq m-1$, if $\{z_1^2, z_2^2, \cdots, z_{n+1}^2; u_1^2, \cdots, u_n^2\}$ is a local [optimizer]{style="color: blue"} of $\mathcal{P}_1(z_{m'+1}^1; n)$, ${u_{1}^2}^{\top}Q_2 u_{1}^2<1$ and ${u_{m'+1}^1}^{\top}Q_2 u_{m'+1}^1<1$, then $$\begin{align*}
        \big \{z_1^1,\dots,z_{m'}^1,z_1^2,\dots,z_{n+1}^2; u_1^1,\dots,u_{m'}^1,u_1^2,\dots,u_n^2\big \}
\end{align*}$$ satisfies the KKT conditions of $\mathcal{P}_1(z_0; m'+n)$ with the corresponding multipliers.*
:::

***Proof.*** See Appendix A. $\square$

For the approximated problem $\mathcal P_1'(\cdot)$, we can analogy show the reasonableness of solution concatenate when using approximated dynamics; [this]{style="color: blue"} is demonstrated in Corollary [1](#col.1){reference-type="ref" reference="col.1"}.

::: {#col.1 .corollary}
**Corollary 1**. *Suppose $\{z_1^1, \cdots, z_{m+1}^1; u_1^1, \cdots, u_m^1\}$ locally solves a [variant]{style="color: blue"} of $\mathcal P_1'(z_0; m; \cdot )$, with the dynamic constraints changed as $z_{i+1} = A_i^1 z_i + B_i^1 u_i + w_i^1$, and $\{z_1^2, \cdots, z_{n+1}^2; u_1^2 , \cdots, u_n^2\}$ locally [solving]{style="color: blue"} an [variant]{style="color: blue"} of $\mathcal P_1'(z_{m'+1}^1; n; \cdot)$, where the dynamics are substituted by $z_{i+1} = A_i^2 z_i + B_i^2 u_i + w_i^2$. Then, $$\{z_1^1,\cdots, z_{m'+1}^1, z_2^2, \cdots z_{n+1}^2; u_1 \cdots , u_{n'}^1, u_2^2, \cdots, u_n^2\}$$ locally solves a [variant]{style="color: blue"} of $\mathcal P_1'(z_0; m' + n, \cdot)$, where the corresponding constraint matrices are substituted by $$(A_i, B_i, w_i) = \left\{ 
    \begin{array}{ll}
        (A_i^1, B_i^1, w_i^1), & \quad i \le m', \\
        (A_{i - m'}^2, B_{i - m'}^2, w_{i - m'}^2), & \quad i > m'
    \end{array} 
    \right.$$ as long as [the]{style="color: blue"} following conditions are satisfied:*

*1). [the constraints]{style="color: blue"} ${u_{m'}^1}^\top Q_2 u_{m'}^1 < 1$ , ${{u}_{m'+1}^1}^\top Q_2 {u}_{m'+1}^1 < 1$ and ${{u}_{m'+1}^2}^\top Q_2 {u}_{m'+1}^2 < 1$ hold simultaneously;*

*2). [the matrices]{style="color: blue"} $B_{m'}^1$, ${B}_{m'+1}^1$ and $B_{1}^2$ are of full column rank.*
:::

Theorem 2 and Corollary 1 reveal the soundness of concatenating segmented control inputs and further illuminate the rule of adjusting $N^{(K)}$. Although we only considered concatenating 2 segments in the analysis, it is easy to extend the conclusion to multiple trajectory synthesis cases. Moreover, in some specific cases, the aforementioned trajectory synthesizing method can reliably identify the global optimal trajectory, even when dealing with non-convex constraint sets. The result is established in Theorem 3.

::: theorem
**Theorem 3**. *[Under]{style="color: blue"} the notations and conditions of Theorem [2](#revised_th_2){reference-type="ref" reference="revised_th_2"}, [solve]{style="color: blue"} $\mathcal P_1(z_0;\cdot), \mathcal P_1(z_{m'+1}^1;\cdot)$ by [Algorithm 1. If]{style="color: blue"} $f$ is further affine and the corresponding $\lambda_{min}$ of $\mathcal P_s(z_0;\cdot)$ and $\mathcal P_s(z_{m'+1}^1;\cdot)$ are all [zero]{style="color: blue"}, then $$\big \{z_1^1,\dots,z_{m'}^1,z_1^2,\dots,z_{n+1}^2; u_1^1,\dots,u_{m'}^1,u_1^2,\dots,u_n^2\big \}$$ globally solves $\mathcal P_1(z_0;m'+n)$.*
:::

***Proof.*** Since $f$ is affine, we have $\mathcal P_1(z_0; m' + n) = \mathcal P_1'(z_0; m' + n; \frac{\partial f}{\partial z_0}^\top,\frac{\partial f}{\partial u}^\top)$ for any $z_0$. Let us recall $\mathcal P_r(z_0; m' + n; A , B)$ following $$\begin{align}
    &{\min}_{\{Z;U\}_N} \hspace{-5em} &&(z_{m'+n+1} - z_f)^\top Q_0 (z_{m'+n+1} - z_f) \nonumber\\
    &\text{\;\; s. t.}  &&\eqref{DQ_1}-\eqref{initial_condition_discrete}, \eqref{c2d_var}. \nonumber
\end{align}$$ If all the corresponding $\lambda_{\min,i} \equiv 0$, then for both of $\mathcal P_1'(z_0; m; \cdot)$ and $\mathcal P_1'(z_{m'+1}^1; n; \cdot)$, the corresponding optimizer coincide with [those of]{style="color: blue"} $\mathcal P_r(z_0; m; \cdot)$ and $\mathcal P_r(z_{m'+1}^1; n; \cdot)$ respectively. Hence, we can conclude that $$\big \{z_1^1,\dots,z_{m'}^1,z_1^2,\dots,z_{n+1}^2; u_1^1,\dots,u_{m'}^1,u_1^2,\dots,u_n^2\big \}$$ is also the optimizer of $\mathcal P_r(z_0; m'+n; \cdot)$. With the convexity of $\mathcal P_r(\cdot)$, it can further prove the global optimality of the concatenated solution. Since the global optimal solution of $\mathcal P_r(z_0; m'+n;\cdot)$ has a lower or equal cost of $\mathcal P_1'(z_0; m'+n;\cdot)$, it can [be obtained]{style="color: blue"} that the concatenated solution is also the global optimizer of $\mathcal P_1'(z_0; m'+n;\cdot)$. This completes the proof. $\square$

[ The aforementioned analysis can be readily extended to scenarios involving the concatenation of solutions across multiple planning cycles. Indeed, these theoretical results demonstrate the validity of iteratively solving each $\mathcal P_1'(z_0^{(K)}; N^{(K)}; A^{(K)}, B^{(K)})$ in Algorithm 1.]{style="color: blue"} In the subsequent discussion, we [discuss]{style="color: blue"} another critical index: time cost of the entire control. Given [that]{style="color: blue"} our discretization is based on fixed step lengths, Algorithm 1 utilizes $\hat N^{(K)}$ from its planning cycles to profile time cost. In fact, we can obtain the final time of entire control as ${t_f} = h{\sum}_{i = 1}^{K - 1} {{{\hat N}^{(i)}}}  + h{{\hat N}^{(K)}} .$ Since $h{{\hat N}^{(K)}} \le h{N_{\max }}$, one can obtain a preciser evaluation of $t_f$ by applying a smaller $N_{\max}h$. However, it is unnecessary to calculate an accurate $t_f$ to present the ["time-optimality"]{style="color: blue"} of the entire control. Instead, we could demonstrate that $t_f$ is achieved approximately to local minimal final time. To show this claim, suppose that $\{z_1^{(j)}, \cdots, z_{\hat N^{(K)}+1}^{(j)} \}$ are extracted from solving $\mathcal P_1'(z_0^{(1)}; \cdot), \mathcal P_1'(z_0^{(2)};\cdot), \cdots, \mathcal P_1'(z_0^{(K)};\cdot)$, and that the solution of $\mathcal P_1'(z_0^{(K)};\cdot)$ satisfies the quit condition of Algorithm 1; then, we have $\hat N^{(K)} = N^{(K)}$. If $\{z^{(1)}_1,\cdots,z^{(K)}_{ N^{(K)}+1};u^{(1)}_1,\cdots,u^{(K)}_{ N^{(K)}}\}$ is a local optimal solution of $\mathcal P_1(z_0^{(1)}; h{\sum}_{i = 1}^{K - 1} {{{\hat N}^{(i)}}}  + h{{\hat N}^{(K)}}; \cdot)$, then there exists a neighbor scaled by $\delta$ for arbitrary $\{z^{(1)}_1(\delta),\cdots,z^{(K)}_{N^{(K)}+1}(\delta); u^{(1)}_1(\delta),\cdots,u^{(K)}_{N^{(K)}}(\delta)\}$ satisfying all of the constraints of $\mathcal P_1(\cdot)$. [We further have]{style="color: blue"} $$\|z_{N^{(K)}+1}^{(K)}(\delta) - z_f\|_{Q_0}^2 \geq \|z_{N^{(K)}+1}^{(K)}- z_f\|_{Q_0}^2.$$ If it further holds $(z_{N^{(K)}+1}^{(K)}(\delta) - z_f)^\top Q_0 (z_{N^{(K)}+1}^{(K)}(\delta) - z_f) \geq \gamma^2$, Algorithm 1 will continue with at least one planning cycle. In this circumstance, suppose $U(\delta) = \{u^{(1)}_1(\delta),\cdots,u^{(K)}_{N+1}(\delta),\cdots\}$ is an available control of $\mathcal P_0$, then it can be obtained that $t_f(\delta) - t_f \geq h$ with $t_f(\delta)$ the final time of using $U(\delta)$. Otherwise, if $(z_{N^{(K)}+1}^{(K)}(\delta) - z_f)^\top Q_0 (z_{N^{(K)}+1}^{(K)}(\delta) - z_f) \leq \gamma^2$, then we have $t_f(\delta) = t_f$. The tendency toward local optimal solutions becomes more pronounced with shorter time horizons. To show this, we rewrite the quit condition to an equivalent form as $$\begin{equation}
    \|z_{N^{(K)}+1}^{(K)} - z_f\|^2_{Q_0} \leq \gamma^2.
\end{equation}$$ Then, we have $$\begin{align}
    & \|z_{N^{(K)}+1}^{(K)} - z_f\|^2_{Q_0} -   \|z_{N^{(K)}+1}^{(K-1)} - z_f\|^2_{Q_0} \label{time_opt_2} \\
    & \leq 2\|z_1^{(1)} - z_f\| \|z_{N^{(K)}+1}^{(K)} - z_{N^{(K)}+1}^{(K-1)}\| \label{11} \|Q_0\|_2 \\
    & \leq 2 \|z_1^{(1)} - z_f\| \cdot  \Bigg ( \left\| {z_{{N^{(K)}} + 1}^{(K)} - z_{{{\hat N}^{(K - 1)}} + 1}^{(K - 1)}} \right\| \nonumber \\
    & \quad + \left\| {z_{{{\hat N}^{(K - 1)}} + 1}^{(K - 1)} - z_{{N^{(K - 1)}} + 1}^{(K - 1)}} \right\| \Bigg) \cdot \|Q_0\|_2.   \label{time_opt_1}
\end{align}$$ For $\left\| {z_{{N^{(K)}} + 1}^{(K)} - z_{{{\hat N}^{(K - 1)}} + 1}^{(K - 1)}} \right\|$, we can further obtain $$\begin{align}
    &\left\| {z_{{N^{(K)}} + 1}^{(K)} - z_{{{\hat N}^{(K - 1)}} + 1}^{(K - 1)}} \right\| \nonumber \\
    &= \left\| {z_{{N^{(K)}} + 1}^{(K)} - z_1^{(K)}} \right\| \nonumber \\
    & \leq   \sum\limits_{i = 1}^{N^{(K)}} {\left\| {z_{i + 1}^{(K)} - z_i^{(K)}} \right\|} \nonumber \\
    & =  h \cdot \underbrace{ \sum\limits_{i = 1}^N {\left\| {{A_c(z_0^{(K)})}z_i^{(K)} + {B_c(z_0^{(K)})}u_i^{(K)} + {w_c(z_0^{(K)})}} \right\|}}_{M} \nonumber \\
    & \leq N_{\max} h \cdot M. \label{bounded}
\end{align}$$ Similarly, $$\begin{align}
    &{\left\| {z_{{{\hat N}^{(K - 1)}} + 1}^{(K - 1)} - z_{{N^{(K - 1)}} + 1}^{(K - 1)}} \right\|} \nonumber \\
    &\le \sum\limits_{i = {{\hat N}^{(K - 1)}} + 1}^{{N^{(K-1)}}} {\left\| {z_{i + 1}^{(K - 1)} - z_i^{(K - 1)}} \right\|} \nonumber \\
    &\leq N_{\max} h \cdot M.  \label{bounded_2}
\end{align}$$ In [the]{style="color: blue"} above steps, [\[11\]](#11){reference-type="eqref" reference="11"} is a direct result of Assumption [3](#todo20241117){reference-type="ref" reference="todo20241117"}. With the boundness of $u^{(K)}_i$ and $z^{(K)}_i$, [\[time_opt_1\]](#time_opt_1){reference-type="eqref" reference="time_opt_1"}, [\[bounded\]](#bounded){reference-type="eqref" reference="bounded"} and [\[bounded_2\]](#bounded_2){reference-type="eqref" reference="bounded_2"} indicate $\eqref{time_opt_2} \to 0$ as $N_{\max}h \to 0$. With $\| z_{{N^{(K-1)}} + 1}^{(K-1)} - z_f \|_{Q_0} > \gamma$ and $\| z_{{N^{(K)}} + 1}^{(K)} - z_f \|_{Q_0} \leq \gamma$, we can obtain $\| z_{{N^{(K)}} + 1}^{(K)} - z_f \|_{Q_0} \to \gamma^-$ as $N_{\max}h \to 0$. Hence, we can choose a sufficient small $N_{\max}h$, that making all $\{u^{(1)}_1(\delta),\cdots,u^{(K)}_{N+1}(\delta)\}$ failed to meet the quit condition for given $\delta$ except [for]{style="color: blue"} $\{u^{(1)}_1,\cdots,u^{(K)}_{N+1}\}$ itself. Thus, $h\sum\nolimits_{i = 1}^K {{{\hat N}^{(i)}}}$ converges to a local minimal $t_f$.

::: remark
**Remark 3**. *Although $h\sum\nolimits_{i = 1}^K {{{\hat N}^{(i)}}}$ converges to a local minimum as $N_{\max}h \to 0$, some undesired phenomenons may appear if $N_{\max}h$ is too small, e.g. the conditions of Theorem 2 may be difficult to be satisfied. Therefore, $t_f$ can generally approximate to a local minimal final time since a lower bound of $N_{\max}h$ should be added.*
:::

Next, some sufficient conditions for the equivalence of solving $\mathcal P_s(z_0^{(K)};N^{(K)};A^{(K)},B^{(K)})$ and $\mathcal P_1'(z_0^{(K)};N^{(K)};A^{(K)},B^{(K)})$ will be provided. We begin with defining the relative interior solution.

::: definition
**Definition 2**. *[A feasible solution to $\mathcal{P}_s^{(K)}(\cdot)$ is called a *relative interior solution* if for all $1 \leq i \leq N^{(K)} + 1$, the computed position components $z_i^{(K)}[1:2]$ lie in the relative interior of $\mathcal{Z}_i[1:2]$.]{style="color: blue"}*
:::

::: theorem
**Theorem 4**. *When $\rho^{(K)} = 0$, the [corresponding]{style="color: blue"} $\{z_1^{(K)}, \cdots, z_{N^{(K)}+1}^{(K)}; u_1^{(K)}, \cdots, u_{N^{(K)}}^{(K)}\}$ calculated from the optimal solution of $\mathcal P_s^{(K)}(z_0^{(K)};N^{(K)}; \cdot)$ is a local optimizer for $\mathcal P_1'(z_0^{(K)};N^{(K)}; \cdot)$, if at least one of the following two conditions is satisfied:*

*1). all $\lambda_{min,i}^{(K)} = 0$ or $\tilde z_i = \bar z_i$, $i \in \{1,\cdots,N^{(K)}+1\}$;*

*2). the obtained optimizer of $\mathcal P_s^{(K)}$ is a relative interior solution.*
:::

***Proof.*** See Appendix B. $\square$

:::: {style="color: blue"}
::: remark
**Remark 4**. *Theorem 4 requires two preconditions. The first precondition is satisfied when the solution to the corresponding problem $\mathcal{P}_r(\cdot)$ is collision-free. The later holds if the optimizer of $\mathcal{P}_1'(\cdot)$ lies strictly in the generated convex region. In a subset of the map where obstacles are not overly dense, the first precondition is typically met.*
:::
::::

We have analyzed properties of Algorithm 1 under the assumption that the safety term is disabled, i.e., $\rho^{(j)} = 0$ in each $\mathcal P_s^{(j)}$. We now briefly examine the effect of the safety term. Suppose $\{\lambda_f^*(\rho) , \lambda_d^*(\rho)\}$ is an optimal solution of $\mathcal P_s(z_0^{(K)}; \cdot)$ with $\rho^{(K)} = \rho$. Then, we can obtain $$\begin{align}
    J_s(\lambda_f^*(0) , \lambda_d^*(0);0) &\leq J_s(\lambda_f^*(\rho) \lambda_d^*(\rho);\rho), \nonumber \\
    & \leq J_s(\lambda_f^*(0) , \lambda_d^*(0);0)  \nonumber \\
    & \quad + \rho \cdot \|z^{(K)}_0 - z_f\|  \|\lambda_f^*(0) - \mathbf{1}\|^2 \nonumber \\
    & \leq J_s(\lambda_f^*(0) , \lambda_d^*(0);0) \nonumber \\
    & \quad + \rho N_{\max} \|z^{(K)}_0 - z_f\|. \label{error}
\end{align}$$ To analyze the error derive from the safety term, we need to present two important theorems first, which are demonstrated as Theorem 5 and Theorem 6, respectively.

:::: {style="color: blue"}
::: {#diameter .theorem}
**Theorem 5**. *Suppose $\Theta : \mathbb R^{l_\Theta} \supset \mathbb E \mapsto \mathbb R$ is a continuous closed convex function with unique optimizer, and the minimum of $\Theta$ is denoted by $\Theta_{opt}$. Define $\Phi_\Theta(s) := \mathrm{diam}{(\mathrm{Lev}(\Theta,s))}$, then $\Phi_\Theta(s)$ is upper semi-continuous for $s \in [\Theta_{opt} , \infty)$. Here, $$\begin{equation}
        \mathrm{Lev}(\Theta,s) = \left\{ {{\bf{x}} \ |\Theta({\bf{x}}) < s} \right\} \nonumber
\end{equation}$$ is the strict sublevel set of $\Theta$ at $s$, and $$\begin{equation}
        \overline {{\rm{Lev}}} (\Theta,s) = \left\{ {{\bf{x}} \ |\Theta({\bf{x}}) \le s} \right\} \nonumber
\end{equation}$$ is the sublevel set of $\Theta$ at $s$.*
:::
::::

***Proof.*** See Appendix C. $\square$

Theorem [5](#diameter){reference-type="ref" reference="diameter"} is based on the condition that the optimizer of $\Theta$ is unique. If this condition is not satisfied, it can also easily obtain that $\Phi_\Theta(s)$ is upper semi-continuous for $s \in (\Theta_{opt},\infty)$ while its upper semi-continuous range changes to $[\overline {{\rm{Lev}}} (\Theta,\Theta_{opt}), \infty)$. Using similar mathematical method, we can further prove another important theorem, which is presented as Theorem 6.

::: theorem
**Theorem 6**. *[Suppose $\Theta : \mathbb R^{l_\Theta} \supset \mathbb E \to \mathbb R$ is a closed convex function, and $\mathbb E \ne \emptyset$ is a closed convex set.]{style="color: blue"} Denote $X^*$ as the optimal set of $\Theta$, [where ${\Theta}(\mathbf x^*) =\min\{\Theta(\mathbf x)| \mathbf x \in \mathbb E\} :={\Theta}_{opt}$]{style="color: blue"} for any $\mathbf x^* \in X^*$. If $X^*$ is bounded, then $$\varphi(s) := \left\{ 
    \begin{aligned}
        & \mathop {\max }\limits_{\mathbf{x} \in \mathrm{Lev}(\Theta,s)} \left\{ \left\| \mathrm{Proj}_{X^*}(\mathbf{x}) - \mathbf{x} \right\| \right\}, && \Theta_{\mathrm{opt}} < s, \\
        & 0, && \text{else}
    \end{aligned} 
    \right.$$ is upper semi-continuous for $s \in [\Theta_{opt},\infty)$, and $$\begin{equation}
        \mathop {\lim }\limits_{s \to {\Theta}_{opt}^ + } \left( {\mathop {\max }\limits_{{\bf{x}} \in {\rm{cl}}({\rm{Lev}}({\Theta},s))} \left\| {{\bf{x}} - \mathrm{Proj}_{X^*}\left( {\bf{x}} \right)} \right\|} \right) = 0,  \label{th_6.2}
\end{equation}$$[ where $\mathrm{Proj}_{X^*}(\mathbf x) := \arg\min_{\mathbf y \in \mathbb E} \{\|\mathbf y - \mathbf x\| | \mathbf x \in X^*\}$ is the projection of $\mathbf x$ with respect to $X^*$.]{style="color: blue"}*
:::

***Proof.*** See Appendix D. $\square$

Since $\mathcal P_s(\cdot)$ is convex, combining [\[error\]](#error){reference-type="eqref" reference="error"} we can obtain that as $\rho /\|Q_0\|_2 \to 0^+$ the difference between $\{\lambda_f^*(\rho), \lambda_d^*(\rho)\}$ and $\{\lambda_f^*(0),  \lambda_d^*(0)\}$ converges to 0 according to the conclusion of Theorem 5 and 6. As a result, it is reasonable to consider the solution of $\mathcal P_s(\cdot)$ as the optimal solution of $\mathcal P_1'(\cdot)$ while ignoring the effect of the safety term, if $\|Q_0\|_2 \gg \rho$ and any of the two cases in Theorem 4 is satisfied.

Despite the aforementioned strict problems can be solved with lower computational burdens, their local optimality condition is not as moderate as initially thought. If a stricter local optimal solution is required, SCP can also be an effective substitution for searching algorithms; that is to use SCP algorithm solving $P_1(z_0^{(K)}; \cdots)$ directly rather than $P_1'(z_0^{(K)}; \cdots)$. [In fact, there are three approaches for solving the control problem: (1) solving each planning cycle in the framework of Algorithm 1; (2) the conventional approach directly addresses the original non-convex problem using either general non-convex optimization techniques or sequential convex programming (SCP) methods; and (3) a hybrid alternative that explicitly solves $\mathcal P_1(\cdot)$ with NLP Algorithms.]{style="color: blue"}

## Contribution Summary

We now summarize section 3 and the main contributions of our work. Subsections 3.1---3.2 introduce the novel time-optimal MPC method. In 3.3, the proposed CVAPF method employs a novel end-to-end computation framework integrating state and control. It (1) can be directly deployed as a trajectory planning method, and (2) achieves high robustness through the incorporation the safety acceleration $a_{safe}$ ​and the condition flag $\mathtt{Not\_Safe}$. Subsection 3.4 provides theoretical support through two original results---Theorems 2 and 4---which, to the best of our knowledge, represent new contributions to the field. Theorem 2 formalizes the local optimality preservation under trajectory concatenation, while Theorem 4 further establishes the equivalence between solutions of $\mathcal P_1'(\cdot)$ over local subsets of $\mathcal M$ and those derived in the global configuration space.

# Numerical Experiments

In this section, some numerical experiments are presented to illustrate the capabilities of Algorithm 1 in both static and time-varying map scenarios. We conduct these experiments using MATLAB 2017a with an Intel Core i7 9th 8GB-RAM with the assistance of the CVX toolbox [@cvx21] [@cvx22].

## Experiments with Static Maps

In this part, we generate maps with fixed circular obstacles to evaluate the algorithm's capability in static scenarios. The dynamics are chosen as the double integrator model, where the constraint [\[DQ_1\]](#DQ_1){reference-type="eqref" reference="DQ_1"}, [\[DQ_2\]](#DQ_2){reference-type="eqref" reference="DQ_2"} are specialized as $\|z_i[1:2]\| \leq v_{\max}$, $\|u_i\| \leq a_{\max}$. Some critical parameters are presented in Table [\[table_parameters\]](#table_parameters){reference-type="ref" reference="table_parameters"}.

During map generation, circular obstacles are randomly placed using a built-in random function with seed 20250712. A validation step ensures both target reachability and compliance with map constraints. To illustrate vehicle performance, we select one map and conduct simulations using Algorithm 1 and comparative SCP algorithms. The resulting trajectories are visualized in Fig. [5](#fig:fig3){reference-type="ref" reference="fig:fig3"}.

:::: {#fig:fig3 .figure latex-placement="h"}
![](Fig3){width="100%"}

::: caption
Trajectories generated by 2 distinct algorithm
:::
::::

In Fig. [5](#fig:fig3){reference-type="ref" reference="fig:fig3"}, the red line represents the trajectory of locations obtained using Algorithm 1 with the CVAPF searching algorithm, while the blue line depicts the trajectory of locations obtained by a general sequential convex programming algorithm parameterized with 24 nodes. The trajectory of Algorithm 1 is concatenated by 14 segmented trajectory, while in 12 planning cycles, the precondition of Theorem 4 can be satisfied. Throughout this work, implementations of the SCP algorithm employ a deterministic initialization strategy. During the preparation phase, we set $u_i \equiv 0$ and $z_i = (i - 1)\frac{z_f - z_0}{N} + z_0$. This "initial guess" is then refined by running a few SCP iterations with a large trust region, yielding the final initial guess used in subsequent optimization. Notably, both of the two location trajectories are available yet exhibit varying qualities. The numerical characteristics of the two trajectories are listed in TABLE [\[tab:quality_cmp\]](#tab:quality_cmp){reference-type="ref" reference="tab:quality_cmp"}.

Correspondingly, the control inputs are shown in Fig.4. In the two charts, the red dashed line represents the acceleration of the $x$-direction, while the blue dashed line represents the acceleration of the $y$-direction.

:::: {#fig:fig4 .figure latex-placement="h"}
![](Fig4a){width="110%" height="27%"}

::: caption
The inputs generated by distinct algorithms: (1) Algorithm 1 with CVAPF, (2) Comparative SCP Algorithm.
:::
::::

In this experiment, we set the SCP algorithm to use 24 nodes since we observed that increasing the number of nodes significantly raises computational cost, while reducing it further leads to substantial loss of accuracy. To further evaluate the capability of Algorithm 1, we employ various metrics in subsequent experiments. Here, we employ the unicycle model, where the feasible trajectory are obtained by CDWA. Specifically, we utilize indexes such as $t_f$, [success rate]{style="color: blue"}, and computational time to assess performance. We first test the computation time. In this part, each algorithm is individually tested on 100 maps, with results plotted in Fig. 5 and statistical indicators listed in TABLE [\[tab:tab4\]](#tab:tab4){reference-type="ref" reference="tab:tab4"}.

![A comparison of the running time between SCPs and our algorithm](Fig8){#fig:fig8 width="100%"}

:::: {style="color: blue"}
In the 1296 planning cycles, there are only 179 planning cycles which is out of the precondition of Theorem 4. For the success rate in TABLE [\[tab:tab4\]](#tab:tab4){reference-type="ref" reference="tab:tab4"}, some clarifications must be presented here. We evaluate a trial "success" if the obtained solution can exactly navigate the vehicle to the target area without violate any obstacle avoidance constraint. It should be noted that the factors contributing to unsuccessful trials differ between our proposed algorithm and baseline methods due to their inherent technical distinctions. As detailed in TABLE [1](#success){reference-type="ref" reference="success"}, we establish separate failure criteria for each algorithm.

::: {#success}
  **Failure Mode**       **Algorithm 1**   **Competed SCP**
  ---------------------- ----------------- ------------------
  Infeasibility          $\checkmark$      $\checkmark$
  Constraint violation   $\checkmark$      $\checkmark$
  Excessive comp. time   $\checkmark$      $\times$

  : Failure Criteria Comparison
:::

The "" in the table indicates that the occurrence of the corresponding condition is considered an experimental failure when using that particular algorithm. Conversely, "$\times$" signifies that the specified condition does not constitute a failure criterion for the respective algorithm. The term "Infeasibility" means connective infeasibility and solver infeasibility (namely, the numerical solver cannot run correctly due to no solution exists, ill-conditioned solutions, etc.) for Algorithm 1, while artificial infeasibility and solver infeasibility for Competed SCP. For our proposed framework, the vehicle must complete each planning cycle within this horizon duration to maintain operational continuity, hence excessive computational time of a cycle is not acceptable, while in competed SCP algorithms, this factor is not need to consider.
::::

Fig.[7](#fig:fig8){reference-type="ref" reference="fig:fig8"} further reveals that Algorithm 1 outperforms SCP algorithms in terms of calculation efficiency, with a shorter average computing time while having a more concentrated distribution of results. In contrast, SCP algorithms exhibit longer computation times and a more scattered distribution.

## Experiments with Dynamic Maps

In this part, we will conduct experiments to show the robustness of Algorithm 1 in time-varying maps with moving obstacles. First, we revise and add some extra parameters shown in Table [\[tab:5\]](#tab:5){reference-type="ref" reference="tab:5"} to profile a time-varying map.

Here, $v_o$ is applied to depict the maximal speed of obstacles, where for arbitrary $p_i(t)$ there exists $\|p_i(t + \tilde t) - p_i(t)\| \leq v_o \cdot |\tilde t|$ for any $t$ and $\tilde t$. For clarity, we first demonstrate Algorithm 1 in a toy example with 3 obstacles, as a sparse layout allows clear visualization of its behavioral characteristics. Subsequently, to validate scalability, we test the algorithm in a dynamic scenario containing 20 moving obstacles. To simulate realistic obstacle motion, each obstacle's position is updated via a double-integrator model with saturation. At each simulation step, the current velocity of an obstacle is measured, and---in a manner analogous to the DWA---a feasible set of accelerations consistent with the next velocity is constructed. An acceleration value is then randomly selected (with seed 0) from this set to update the obstacle's state. The obstacle's velocity and position are then updated sequentially through numerical integration. In the example, two figures are plotted to show the specific movement of the vehicle and obstacles in two distinct perspectives, which are demonstrated in Fig. 6.

:::: {#fig3D .figure latex-placement="h"}
\

::: caption
Obstacle avoidance experiment in time-varied scenarios: A Result
:::
::::

In Fig.[8](#fig3D){reference-type="ref" reference="fig3D"}, both graphs share the same vertical axis, representing the time. When the vertical coordinates are specified, the corresponding horizontal plane represents the danger areas from obstacles at that particular moment. The solid black line indicates the vehicle's trajectory throughout the task. By combining these two charts, it becomes evident that Algorithm 1 effectively avoids obstacles, showcasing its capability with the assistance of searching algorithms in a dynamic map. Furthermore, to aid readers in comprehending the obstacle avoidance capabilities of the vehicle more clearly, we provide a corresponding display diagram as depicted in Fig.[9](#fig:fig6){reference-type="ref" reference="fig:fig6"}.

:::: {#fig:fig6 .figure latex-placement="!h"}
![](Fig6){width="90%"}

::: caption
The minimal distance to danger zones during the task. in this figure, the minimal value is 0.2760
:::
::::

In Fig.7, the minimal distance between the vehicle and danger zones is demonstrated. It shows that the vehicle keeps a distance bigger than 0.2760m from all the danger zones at any time.

With $n=20$, we conduct subsequent experiments, testing Algorithm 1 with 150 diverse maps. The results are demonstrated in TABLE [\[tab:4\]](#tab:4){reference-type="ref" reference="tab:4"}. [The last column of TABLE [\[tab:4\]](#tab:4){reference-type="ref" reference="tab:4"} is the rate of planning cycles which satisfies the preconditions of Theorem 4.]{style="color: blue"}

# Conclusion

Our two-layer optimization-based planning algorithm demonstrated its capability in both theoretical proof and numerical experiments. Specifically, the proposed algorithm generates near time-optimal trajectory with a higher speed while maintain the success rate. [The meaning of "near time-optimal" is of three fold. (1) The computed trajectory's final time must be an integer multiple of the discretization step $h$. Although the exact local optimum may not be attained, the algorithm performs well with a small $h$. (2) Despite the use of an approximated affine model, the solution becomes more precise when the system nonlinearity is mild and the planning horizon is sufficiently short. (3) While the preconditions of Theorem 4 may occasionally fail to hold, the resulting trajectories still exhibit near-local-optimal behavior overall. Moreover, experimental results indicate that occasional violation of these preconditions has limited impact on the final time.]{style="color: blue"} However, the model still encounters challenges in extreme scenarios. One key limitation arises from its discrete solution generation, which only guarantees the feasibility in given discrete time points. As a result, it may struggle with feasibility at interpolated states, which is also a common issue faced by general motion planning algorithms. When the planning horizon for a single cycle is excessively long, the timeliness of solutions is compromised, and the algorithm may fail in dynamic scenarios where obstacles continue to shift. Additionally, the computation time for a single planning cycle may exceed the horizon of the latest generated control sequences, potentially leading to loss of vehicle control. To address these shortcomings of Algorithm 1, our future works will focus on enhancing robustness through more reliable searching methods and conducting a detailed analysis of general nonlinear vehicle models.

# Proof of Theorem 2

We consider the Lagrangian $\mathscr L_{m' + n}(z_0;\cdot)$. If $\{z_1 ^*, z_2 ^*, \cdots, z_{m'+n+1}^*; u_1^*, \cdots, u_{m'+n}^*\}$ with [the]{style="color: blue"} corresponding Lagrange multipliers locally solves $\mathcal P_1(z_0; m'+n)$, we can immediately list [the]{style="color: blue"} following KKT conditions: $$\begin{align}
        &\begin{aligned}
            \frac{{\partial \mathscr L_{m'+n}(z_0;\cdot)}}{{\partial z_i^*}} &= \frac{\partial}{\partial z_i^*} {\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta_{ij}^*}\left( {r_j^2 - {{\left\| {z_i^*[1:2] - {p_j}} \right\|}^2}} \right)} }   \\
            & \quad  - {\frac{\partial f}{\partial z_i^*}}^\top \cdot \upsilon_i^* + {\upsilon_{i - 1}^*} + 2s_i^* {Q_1}z_i^* \\
            & = \mathbf 0,
        \end{aligned} \label{th2mna}\\
        &\frac{{\partial \mathscr L_{m' + n}(z_0;\cdot)}}{{\partial u_i^*}} =  - {\frac{\partial f}{\partial u_i^*}}^\top \cdot \upsilon_i^* + 2 q_i^* {Q_2}u_i^* = \mathbf 0, \label{th2mnb}\\
        &{{\upsilon _i^*}\left( {{z_{i + 1}^*} - f(z_i^*, u_i^*)} \right)} = \mathbf 0, \label{th2mnc} \\
        &{{\zeta _{ij}^*}\left( {r_j^2 - {{\left\| {{z_i}^*[1:2] - {p_j}}\right\|}^2}} \right)} = \mathbf 0, \label{th2mnd}\\
        &{s_i^*{G_1}(z_i^*)} = 0, \label{th2mne}\\
        &{q_i^*{G_2}(u_i^*)} = 0, \label{th2mnf}\\
        &\upsilon_i^*, \zeta_{ij}^*, q_i^*, s_i^* \geq 0, \label{th2mng}
    \end{align}
    and for $i = m' + n + 1$, there exist
    \begin{align}
        \frac{{\partial  \mathscr L_{m' +n}(z_0;\cdot)}}{{\partial z_{i}^*}} &= \frac{\partial}{\partial z_{i}^*} {\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta_{i,j}^*}\left( {r_j^2 - {{\left\| {z_{i}^*[1:2] - {p_j}} \right\|}^2}} \right)}}\nonumber \\
        & \quad - {\frac{\partial f}{\partial z_i^*}}^\top\upsilon_{i}^* + {\upsilon_{m'+n}^*} + 2 s_{i}^* {Q_1}z_{i}^* \nonumber \\
        &= \mathbf 0. \label{th2mnh}
    \end{align}$$ For [\[th2mna\]](#th2mna){reference-type="eqref" reference="th2mna"}, the range of $i$ is $2\leq i \leq m'+n+1$, for [\[th2mnb\]](#th2mnb){reference-type="eqref" reference="th2mnb"}, [\[th2mnc\]](#th2mnc){reference-type="eqref" reference="th2mnc"}, [\[th2mne\]](#th2mne){reference-type="eqref" reference="th2mne"}, [\[th2mnf\]](#th2mnf){reference-type="eqref" reference="th2mnf"}, the range of $i$ is $1 \leq i \leq m'+ n$, while for [\[th2mnd\]](#th2mnd){reference-type="eqref" reference="th2mnd"}, the index range is $1 \leq i \leq m'+n+1$. Similarly, the optimizer of $\mathcal P_1(z_0; m)$, namely $\{z_1^1, z_2^1, \cdots, z_{m+1}^1; u_1^1, \cdots, u_m^1\}$, must satisfy $$\begin{align}
        &\begin{aligned}
            \frac{\partial \mathscr{L}_m(z_0;\cdot)}{\partial z_i^1} 
            &=  \frac{\partial}{\partial z_i^1} \sum_{j=1}^{n_{\text{obs}}} \zeta_{ij}^1 \left( r_j^2 - \| z_i^1[1:2] - p_j \|^2 \right)  \\
            &\quad -\frac{\partial f}{\partial z_i^1}^\top \upsilon_i^1 + \upsilon_{i-1}^1 + 2s_i^1 Q_1 z_i^1  \\
            &= \mathbf{0},
        \end{aligned}  \label{th2ma} \\
        &\frac{{\partial \mathscr L_m(z_0;\cdot)}}{{\partial u_i^1}} = - {\frac{\partial f}{\partial u_i^1}}^\top \upsilon_i^1 + 2q_i^1 {Q_2}u_i^1 = \mathbf 0 ,\label{th2mb}\\
        &{{\upsilon _i^1}\left( {{z_{i + 1}^1} - f(z_i^1, u_i^1)} \right)} = \mathbf 0 ,\label{th2mc}\\
        &{{\zeta _{ij}^1}\left( {r_j^2 - {{\left\| {z_i^1[1:2] - {p_j}} \right\|}^2}} \right)} = \mathbf 0,\label{th2md}\\
        &{s_i^1{G_1}(z_i^1)} = 0,\label{th2me}\\
        &{q_i^1{G_2}(u_i^1)} = 0,\label{th2mf}\\
        &\upsilon_i^1, \zeta_{ij}^1, q_i^1, s_i^1 \geq 0\label{th2mg}
    \end{align}$$ with some multipliers $\upsilon_i^1, \zeta_{ij}^1, q_i^1, s_i^1$. In [\[th2ma\]](#th2ma){reference-type="eqref" reference="th2ma"}-[\[th2mg\]](#th2mg){reference-type="eqref" reference="th2mg"}, the range of $i$ is $1 \leq i \leq m'$ for [\[th2mb\]](#th2mb){reference-type="eqref" reference="th2mb"}, [\[th2mc\]](#th2mc){reference-type="eqref" reference="th2mc"}, [\[th2mf\]](#th2mf){reference-type="eqref" reference="th2mf"}, $1 \leq m'+1$ for [\[th2md\]](#th2md){reference-type="eqref" reference="th2md"}, [\[th2me\]](#th2me){reference-type="eqref" reference="th2me"} while $2 \leq i \leq m'+1$ for [\[th2ma\]](#th2ma){reference-type="eqref" reference="th2ma"}. For $\{z_1^2, z_2^2, \cdots, z_{n+1}^2; u_1^2, \cdots, u_n^2\}$ with the corresponding multipliers $\{\upsilon_i^2, \zeta_{ij}^2, q_i^2, s_i^2\}$, we have $$\begin{align}
        &\begin{aligned}
            \frac{{\partial \mathscr L_n(z_{1}^2;\cdot)}}{{\partial z_i^2}} &=  \frac{\partial}{\partial z_i^2} {\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta_{ij}^2}\left( {r_j^2 - {{\left\| {z_i^2[1:2] - {p_j}} \right\|}^2}} \right)}}\\
            & \quad - {\frac{\partial f}{\partial z_i^2}}^\top \upsilon_i^2 + {\upsilon_{i - 1}^2} + 2s_i^2 {Q_1}z_i^2 \\
            & = \mathbf 0, 
        \end{aligned} \label{th2na} \\
        &\frac{{\partial \mathscr L_n(z_{1}^2;\cdot)}}{{\partial u_i^2}} =  - {\frac{\partial f}{\partial u_i^2}}^\top\upsilon_i^2+ 2 q_i^2 {Q_2}u_i^2 = \mathbf 0,\label{th2nb} \\
        &{{\upsilon _i^2}\left( {{z_{i + 1}^2} - f(z_i^2, u_i^2)} \right)} = \mathbf 0 , \label{th2nc}\\
        &{{\zeta _{ij}^2}\left( {r_j^2 - {{\left\| {z_i^2[1:2] - {p_j}} \right\|}^2}} \right)} = \mathbf 0, \label{th2nd} \\
        &{s_i^2{G_1}(z_i^2)} = 0, \label{th2ne}\\
        &{u_i^2{G_2}(u_i^2)} = 0, \label{th2nf}\\
        &\upsilon_i^2, \zeta_{ij}^2, q_i^2, s_i^2 \geq 0 \label{th2ng}
    \end{align}
    for appropriate indexes $i,j$ and
    \begin{align}
        \frac{{\partial \mathscr L_n(z_{1}^2;\cdot)}}{{\partial z_{n+1}^2}} &=      \frac{\partial}{\partial z_n^2} {\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta_{n+1,j}^2}\left( {r_j^2 - {{\left\| {z_n^2[1:2] - {p_j}} \right\|}^2}} \right)}} \nonumber \\
        & \quad - {\frac{\partial f}{\partial z_i^2}}^\top\upsilon_{n+1}^2 + {\upsilon_{n}^2} + 2s_{n+1}^2 {Q_1}z_{n+1}^2 \nonumber \\
        & = \mathbf 0. \label{th2nh}
    \end{align}$$ Now, we take $z_1 = z_1^1$, $z_2 = z_2^1$, $\cdots$, $z_{m'+1} = z_{m'+1}^1$, $z_{m'+2} = z_2^2$, $\cdots, z_{m'+n+1} = z^2_{n+1}$ and $u_1 = u_1^1, \cdots, u_{m'} = u_{m'}^1, u_{m'+1} = u_1^2, \cdots, u_{m'+n} = u_n^2$, and define $$\begin{align*}
    \mathbf Z &:= \{z_1, z_2, \cdots, z_{m'+n+1}\},\\
    \mathbf U &:= \{u_1, u_2, \cdots, u_{m'+n}\},\\
    \bm{\zeta} &:= \big\{\zeta_{1j}^1, \zeta_{2j}^1, \cdots, \zeta_{m'+1,j}^1, \zeta_{2j}^2, \cdots, \zeta_{n+1,j}^2\big\}_{j = 1}^{n_{obs}},\\
    \bm{\upsilon} &:= \big\{ \upsilon_1^1, \cdots, \upsilon_{m'+1}^1, \upsilon_{2}^2, \cdots, \upsilon_{n+1}^2 \big\},\\
    \mathbf q &:= \{q_1^1, \cdots, q_{m'+1}^1, q_2^2, \cdots, q_{n+1}^2 \},\\
    \mathbf s &:= \{s_1^1, \cdots, s_{m'+1}^1, s_2^2, \cdots, s_{n+1}^2 \}.
\end{align*}$$ We then show that $\{\mathbf Z, \mathbf U, \bm{\zeta}, \bm{\upsilon}, \mathbf q, \mathbf s\}$ reaches a KKT point of $\mathscr L_{m'+n}(z_0, \cdot)$. In fact, we only need to show $\frac{{\partial \mathscr L_{m'+n}(z_0;\cdot)}}{{\partial {z_{m' + 2}}}} = \mathbf 0$, namely, to prove $$\begin{align}
    &\frac{\partial }{{\partial {z_{m'+1}}}}\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta_{m'+2,j}}\left( {r_j^2 - {{\left\| {{z_{m'+2}}[1:2] - {p_j}} \right\|}^2}} \right)} \nonumber \\
    & \quad - {\frac{\partial f}{\partial z_{m'+2}}}^\top  \upsilon_{m'+2} + \upsilon_{m'+1} = \mathbf 0 \label{th2_3}
\end{align}$$ as [\[th2ma\]](#th2ma){reference-type="eqref" reference="th2ma"}-[\[th2mg\]](#th2mg){reference-type="eqref" reference="th2mg"} and [\[th2na\]](#th2na){reference-type="eqref" reference="th2na"}-[\[th2nh\]](#th2nh){reference-type="eqref" reference="th2nh"} profile all other KKT conditions of $\mathscr L_{m'+n}(z_0; \cdot)$ for the given variables $\{\mathbf Z, \mathbf U, \bm{\zeta}, \bm{\upsilon}, \mathbf q, \mathbf s\}$. If ${u_{1}^2}^{\top}Q_2 u_{1}^2<1$, then $q_{m'+1} = q_1^2 = 0$. As a result, [combining]{style="color: blue"} with [\[th2nb\]](#th2nb){reference-type="eqref" reference="th2nb"}, we can obtain $$\begin{align*}
    -{\frac{\partial f}{\partial u_1^2}}^\top \upsilon_1^2 + 2 q_1^2 Q_2 u_1^2 = -{\frac{\partial f}{\partial u_1^2}}^\top \upsilon_1^2 + \mathbf 0 = \mathbf 0,
\end{align*}$$ which apparently indicates $\upsilon_1^2 = \mathbf 0$ since ${\frac{\partial f}{\partial u_1^2}}^\top$ is of full column rank. Similarly, we have $\upsilon_{m'+1}^1 = \mathbf 0$. That means $$\begin{align}
    &\frac{\partial }{{\partial {z_{2}^2}}}\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta_{2,j}^2}\left( {r_j^2 - {{\left\| {{z_{2}^2}[1:2] - {p_j}} \right\|}^2}} \right)}\nonumber \\
    & \quad -{\frac{\partial f}{\partial z_2^2}}^\top \upsilon_{2}^2 + \upsilon_{m'+1}^1 = \mathbf 0 \label{th2_4}
\end{align}$$ as we substitute $\upsilon_1^2$ by $\upsilon_{m'+1}^1$. By further substituting $\upsilon_2^2 = \upsilon_{m'+2}$, $\upsilon_{m'+1}^1 = \upsilon_{m'+1}$, $z_2^2 = z_{m'+2}$, $\zeta_{2,j}^2 = \zeta_{m'+2,j}$ into [\[th2_4\]](#th2_4){reference-type="eqref" reference="th2_4"}, we get [\[th2_3\]](#th2_3){reference-type="eqref" reference="th2_3"}. [This]{style="color: blue"} completes the proof. $\square$

# Proof of Theorem 4

For simplicity, the indicator of iteration order are omitted, e.g. $z^{(K)}$ [is abbreviate as]{style="color: blue"} $z$. Take $\rho = 0$. Recall that the Lagrange function of $\mathcal P_1'(z_0; N; \cdot)$ can be formulated as $\mathscr L_N(z_0 ; z,u,\upsilon,\zeta,s,q)$, with the same form of the template [\[lagrange\]](#lagrange){reference-type="eqref" reference="lagrange"}. For the optimizer of $\mathscr L_N$ with the [corresponding]{style="color: blue"} multipliers, the KKT conditions are obtained as $$\left\{ \begin{array}{l}
    Az_i^* + Bu_i^* - z_{i + 1}^* = {\bf{0}},\\ 
    s_i^*{G_1}({z_i^*}) = {\bf{0}},\\ 
    q_i^*{G_2}({u_i^*}) = {\bf{0}},\\ 
    \zeta _{ij}^*\left( {r_j^2 - {{\left\| {{z_i^*}[1:2] - {p_j}} \right\|}^2}} \right) = {\bf{0}},\\ 
    s_i^* \ge 0,q_i^* \ge 0,\zeta _{ij}^* \geq 0,\\ 
    {z_1^*} = {z_0},
\end{array} \right.$$ and $$\begin{equation}
    \{ {z^*_i},{u^*_i}\}  = \mathop {\arg \min }\limits_{{z _{i}},{u _{i}}} {\mathscr L_N} \label{argmin}
\end{equation}$$ with proper indexes $i$ under Assumption [5](#KKT){reference-type="ref" reference="KKT"}. Our goal is to show the computed state-control series $\{z_1, \cdots, z_{N+1}; u_1, \cdots, u_N\}$ by the optimizer of $\mathcal P_s(z_0;N; \cdot)$ satisfies the above KKT conditions. Take $$\begin{equation}
    \mathscr L_N' = \mathscr L_N - \sum\limits_{i = 1}^{N + 1} {\sum\limits_{j = 1}^{{n_{obs}}} {{\zeta _{ij}}\left( {r_j^2 - {{\left\| {{z_i}[1:2] - {p_j}} \right\|}^2}} \right)} }. \nonumber
\end{equation}$$ Then, for such $\mathcal P_s(\cdot)$, the corresponding Lagrange function can be formed as $$\begin{align}
    &{\mathscr L_s}(z_0 ; z,u,\upsilon ,\eta,\sigma,\xi,s,q) = \mathscr L_N'  \nonumber \\
    &+ \sum\limits_{i = 1}^{N + 1} {({\eta_i} - {\sigma_i}){\lambda _{f,i}} - {\eta_i}}  + \sum\limits_{i = 1}^{N + 1} {{\xi_i}({\lambda _{d,i}} - {k_i}{\lambda _{f,i}})},
\end{align}$$ where $\eta_i, \sigma_i, \xi_i$ are Lagrange multipliers. If $\lambda_{\min,i} = 0$ holds for arbitrary $i$, then the nominal trajectory itself is feasible, which is also a minimizer of $\mathscr L_N$. Otherwise, if a relative interior solution is obtained, we have $\zeta_{ij}^* = \eta_i^* = \sigma_i^* =  \xi_i^* = 0$ for all $i$ by complement slackness condition. Actually, now we can obtain that $\mathscr L_s \equiv \mathscr L_N$. The first order optimality conditions of the strict problem are $$\begin{equation}
    \left\{ \begin{array}{l}
        \frac{{\partial {\mathscr L_s}}}{{\partial {\lambda _{f,i}^*}}} = 0, \\
        \frac{{\partial {\mathscr L_s}}}{{\partial {\lambda _{f,d}^*}}} = 0
    \end{array} \right.
\end{equation}$$ or $$\begin{equation}
    \{ {\lambda _{f,i}^*},{\lambda _{d,i}^*}\}  = \mathop {\arg \min }\limits_{{\lambda _{f,i}},{\lambda _{d,i}}} {\mathscr L_s}. \label{argmin_lambda}
\end{equation}$$

In $\mathcal P_s(\cdot)$, it is worth noting that one pair of $\{\lambda_{f,i},\lambda_{d,i}\}$ determines $\{z_i\}_{i = 1}^{N + 1}$ uniquely. With Assumption [4](#Full_Rank){reference-type="ref" reference="Full_Rank"}, we further obtain that a given $\{\lambda_{f,i},\lambda_{d,i}\}$ determines a unique $\{z_1, \cdots, z_{N+1}; u_1, \cdots, u_N\}$. In other words, [\[argmin_lambda\]](#argmin_lambda){reference-type="eqref" reference="argmin_lambda"} is a sufficient condition of [\[argmin\]](#argmin){reference-type="eqref" reference="argmin"}. Thereby, we complete the proof. $\square$

# Proof of Theorem [5](#diameter){reference-type="ref" reference="diameter"} {#proof-of-theorem-diameter}

It is easy to obtain two properties of $\Phi_{\Theta}$: (i) since the minimizer of $\Phi_{\Theta}$ is a singleton [(according to the precondition)]{style="color: blue"}, we have $\Phi_{\Theta}({\Theta}_{opt}) = \Phi_{\Theta}({\Theta}_{opt}^+) = 0$; (ii) for $s_1 \geq s_2 \geq {\Theta}_{opt}$, we have $$\begin{align*}
    \Phi_{\Theta}(s_1) &= \mathrm{diam}{(\text{Lev}(\Theta, s_1))} \\
    &\geq \mathrm{diam}{(\text{Lev}(\Theta, s_2))} = \Phi_{\Theta}(s_2) \geq 0. %展开解释了性质二
\end{align*}$$ Suppose $\Phi$ is not upper semi-continuous at $\tilde s > {\Theta}_{opt}$. Then, [leveraging]{style="color: blue"} the monotonic non-decrease property of $\Phi_{\Theta}$, for any given $\delta > 0$, there exists an $\epsilon > 0$ with $$\begin{equation}
    \Phi_{\Theta}(\tilde s + \delta) - \Phi_{\Theta}(\tilde s) \geq \epsilon. \label{lev1}
\end{equation}$$ Suppose $\mathbf x(\tilde s) , \mathbf y(\tilde s)$ are one pair of the cluster points of $\mathrm{Lev}({\Theta},\tilde s)$ where their distance reaches $\mathrm{diam}{(}{\mathrm{Lev}({\Theta},\tilde s)})$. Then, with [\[lev1\]](#lev1){reference-type="eqref" reference="lev1"} we can derive $$\begin{align}
    \Phi_{\Theta}(\tilde s + \delta) - \Phi_{\Theta}(\tilde s) &= \|\mathbf x(\tilde s + \delta) - \mathbf y (\tilde s + \delta)\|  \nonumber \\
    & \ \ \ - \|\mathbf x(\tilde s ) - \mathbf y (\tilde s)\| \nonumber \\
    & \leq \| \mathbf x(\tilde s + \delta) - \mathbf x (\tilde s)\| \nonumber \\
    & \ \ \ + \| \mathbf y(\tilde s + \delta) - \mathbf y (\tilde s)\|.
\end{align}$$ Thus, we have $$\begin{equation}
    \| \mathbf x(\tilde s + \delta) - \mathbf x (\tilde s)\| + \| \mathbf y(\tilde s + \delta) - \mathbf y (\tilde s)\| \geq \epsilon. \label{lev2}
\end{equation}$$ Since [\[lev2\]](#lev2){reference-type="eqref" reference="lev2"} holds for arbitrary $\{\mathbf x(\tilde s + \delta), \mathbf y(\tilde s + \delta)\} \subset \mathrm{cl}(\mathrm{diam}{(\mathrm{Lev}({\Theta},\tilde s + \delta))})$ with $\| \mathbf x(\tilde s + \delta)- \mathbf y(\tilde s + \delta)\| = \Phi_{\Theta}(\tilde s + \delta)$, we can further obtain $$\begin{align}
    \epsilon & \le \min _{{\bf{x}}(\tilde s + \delta ),{\bf{y}}(\tilde s + \delta )} \left\{ {\left\| {{\bf{x}}(\tilde s + \delta ) - {\bf{x}}(\tilde s)} \right\|} \right. \nonumber \\
    & \quad \left. { + \left\| {{\bf{y}}(\tilde s + \delta ) - {\bf{y}}(\tilde s)} \right\|} \right\}.
    \label{lev3}
\end{align}$$ Utilize the fact that all the strict [sublevel]{style="color: blue"} sets are open, we can derive $\mathbf x(\tilde s) , \mathbf y(\tilde s)$ lie on the boundary of $\mathrm{cl}(\mathrm{Lev}(\Theta,\tilde s))$ with $\Theta(\mathbf x(\tilde s)) = \Theta (\mathbf y(\tilde s)) = \tilde s$. Then, by choosing a non-increasing series $\{\delta_n\}$ which converges to 0, we have $$\begin{align}
    &\left( {\mathop {\lim }\limits_{\delta  \to {0^ + }} {\rm{Lev}}({\Theta},\tilde s + \delta )} \right)\backslash {\rm{Lev}}({\Theta},\tilde s) \nonumber \\
    & = \left( {\mathop {\lim }\limits_{n \to \infty } \bigcap\limits_{i = 1}^n {{\rm{Lev}}({\Theta},\tilde s + {\delta _i})} } \right)\backslash {\rm{Lev}}({\Theta},\tilde s) \nonumber \\
    & = \overline {{\rm{Lev}}} ({\Theta},\tilde s) \backslash {\rm{Lev}}({\Theta},\tilde s) \nonumber \\
    & = \left\{ {{\bf{x}} \ | \ {\Theta}({\bf{x}}) = \tilde s} \right\}.
\end{align}$$ By [\[lev3\]](#lev3){reference-type="eqref" reference="lev3"}, at least one inequality of $$\left\{ \begin{array}{l}
    \left\| {{\bf{x}}(\tilde s + \delta ) - {\bf{x}}(\tilde s)} \right\| \ge \varepsilon /2,\\
    \left\| {{\bf{y}}(\tilde s + \delta ) - {\bf{y}}(\tilde s)} \right\| \ge \varepsilon /2
\end{array} \right.$$ holds as $\delta \to 0^+$, which indicates that ${{\bf{x}}(\tilde s + \delta )}$ or ${{\bf{y}}(\tilde s + \delta )}$ is out of $\mathrm{cl}(\mathrm{Lev}({\Theta},\tilde s))$ (Note that the fact holds since once ${\bf{x}}(\tilde s + \delta ),{\bf{y}}(\tilde s + \delta ) \in \mathrm{cl}(\mathrm{Lev} ({\Theta},\tilde s))$, [\[lev1\]](#lev1){reference-type="eqref" reference="lev1"} and [\[lev3\]](#lev3){reference-type="eqref" reference="lev3"} cannot be satisfied simultaneously). Hence, suppose $\left\| {{\bf{x}}(\tilde s + \delta ) - {\bf{x}}(\tilde s)} \right\| \ge \varepsilon /2$ as $\delta \to 0^+$, we can found a $\mathbf x^\dagger$ with $\mathbf x^\dagger \not \in \mathrm{cl}(\mathrm{Lev} ({\Theta},\tilde s)), \mathbf x^\dagger \in \left( {{\rm{Lev}}({\Theta},\tilde s) \cup \left\{ {{\bf{x}}\ | \ {\Theta}({\bf{x}}) = \tilde s} \right\}} \right)\backslash {\rm{Lev}}({\Theta},\tilde s)$. Note $$\begin{equation}
    \overline {{\rm{Lev}}} ({\Theta},\tilde s) = \left( {\mathop {\lim }\limits_{n \to \infty } \bigcap\limits_{i = 1}^n {{\rm{Lev}}({\Theta},\tilde s + {\delta _i})} } \right), \nonumber
\end{equation}$$ which preserves the convexity of $\overline {{\rm{Lev}}} ({\Theta},\tilde s)$. Moreover, we have $$\begin{align}
    &\mathrm{conv}({\rm{Lev}}({\Theta},\tilde s),\mathbf x^\dagger) \backslash {\rm{Lev}}({\Theta},\tilde s) \nonumber \\ &\subset \overline {{\rm{Lev}}} ({\Theta},\tilde s)\backslash {\rm{Lev}}({\Theta},\tilde s) \nonumber \\
    & = \left\{ {{\bf{x}}:{\Theta}({\bf{x}}) = \tilde s} \right\}. \label{lev5}
\end{align}$$ By [\[lev5\]](#lev5){reference-type="eqref" reference="lev5"}, there exists some interior points in $\left\{ {{\bf{x}}\ | \ {\Theta}({\bf{x}}) = \tilde s} \right\}$. Take $\mathbf x^* \in \mathrm{int} \{\mathbf x \ | \ {\Theta}(\mathbf x) = \tilde s\}$, then there exists $\mathcal B(\mathbf x^* , r)$ with $\Theta(\mathbf x) \equiv \tilde s$ for any $\mathbf x \in \mathcal B(\mathbf x^* , r)$, which indicates $\mathbf 0 \in \partial {\Theta}(\mathbf x^*)$. By Fermat condition and the convexity of ${\Theta}$, $\mathbf x^*$ is an optimizer of ${\Theta}$. However, with ${\Theta}(\mathbf x^*) = \tilde s > {\Theta}_{opt}$, the optimality of $\mathbf x^*$ contradicts to the convexity. Hence, $\Phi_f$ cannot be discontinuous at $\tilde s \in ({\Theta}_{opt},\infty)$. Combining with (i), we can further derive that $\Phi_{\Theta}(s)$ is upper semi-continuous for $s \in [{\Theta}_{opt},\infty)$. This completes the proof. $\square$

In the proof, if ${\Theta}$ is defined in $\mathbb R^{\ell_{\Theta}}$, then ${\Theta} : \mathbb E \to \mathbb R$ can also written as ${\Theta}'$: $${\Theta}'({\bf{x}}) = \left\{ \begin{array}{l}
    {\Theta}({\bf{x}}) + {I_ \mathbb E}({\bf{x}}), \ \ \hfill {\bf{x}} \in \mathbb E,\\
    {I_\mathbb E}({\bf{x}}), \ \ \hfill {\bf{x}} \notin \mathbb E,
\end{array} \right.$$ where $I_{\mathbb E}$ is the indicator function defined by $${I_{\mathbb E}}({\bf{x}}) \textcolor{blue}{:=} \left\{ \begin{array}{l}
    0, \hfill {\bf{x}} \in \mathbb E ,\\
    \infty, \hfill {\bf{x}} \notin \mathbb E .
\end{array} \right.$$

# Proof of Theorem 6

[We still use the notation $\Phi_{\Theta}(s)$ to represent $\mathrm{diam}{(\text{Lev}(\Theta, s))}$.]{style="color: blue"} Suppose there are two non-empty strict [sublevel]{style="color: blue"} sets $L_1 = \mathrm{Lev}({\Theta},s_1)$ and $L_2 = \mathrm{Lev}({\Theta},s_2)$, where $\Phi_{\Theta}(s_1) = D_1$, $\Phi_{\Theta}(s_2) = D_2$ and $D_2 > D_1 \geq \Phi_{\Theta}({\Theta}_{opt}^+)$. [Take]{style="color: blue"} $\mathbf x^*(D_1) \in \mathrm{cl}(L_1) , \mathbf x^*(D_2) \in \mathrm{cl}(L_2)$ with $\mathbf y^*(L_1),\mathbf y^*(L_2)$ being their corresponding projection on $X^*$. Then, we have $$\begin{align}
    0 & \leq \|\mathbf x^*(L_2) - \mathbf y^*(L_2)\| - \|\mathbf x^*(L_1) - \mathbf y^*(L_1)\| \nonumber \\
    &\leq \|\mathbf x^*(L_2) - \mathbf x^*(L_1)\| + \|\mathbf y^*(L_2) - \mathbf y^*(L_1)\| \nonumber \\
    &\leq 2\|\mathbf x^*(L_2) - \mathbf x^*(L_1)\|. \label{th6.1}
\end{align}$$ By the boundness of $X^*$, $\Phi_{\Theta}({\Theta}_{opt}^+) < \infty$ holds. We first prove [\[th6.1\]](#th6.1){reference-type="eqref" reference="th6.1"} converges to 0 as $D_2 - D_1 \to 0$. Suppose there exists $\epsilon > 0$ making $\|\mathbf x^*(L_2) - \mathbf y^*(L_2)\| - \|\mathbf x^*(L_1) - \mathbf y^*(L_1)\| \geq \epsilon$ for any $D_2 > D_1 > \mathrm{diam}{(X^*)}$, then utilize [\[th6.1\]](#th6.1){reference-type="eqref" reference="th6.1"} we can obtain $\min \left\{ {\left\| {{{\bf{x}}^*}({L_2}) - {{\bf{x}}^*}({L_1})} \right\|} \right\} > \frac{\epsilon}{2}.$ By the continuity of ${\Theta}$, we can further obtain $$\min \left\{ {\left\| {{{\bf{x}}^*}({L_1}) - {{\bf{x}}^*}({L_1})} \right\|} \right\} = 0 > \frac{\epsilon}{2}$$ as $D_2 \to D_1$, which contradicts to $\epsilon > 0$. Therefore, $$\begin{equation}
    \max_{\mathbf x \in \mathrm{cl}(\mathrm {Lev}({\Theta},s))}\|\mathbf x - \mathrm{Proj}_{X^*}(\mathbf x) \| \label{th6.2}
\end{equation}$$ is an upper semi-continuous function of $D$ for $D \in [\Phi_{\Theta}({\Theta}_{opt}^+),\Phi_{\Theta}(+\infty)).$ Moreover, by utilizing [\[th6.2\]](#th6.2){reference-type="eqref" reference="th6.2"} we can obtain $$\begin{equation}
    \varphi({\Theta}_{opt}) = 0 = \varphi({\Theta}_{opt}^+). \label{th6.3}
\end{equation}$$ This completes the proof. $\square$

[^1]: This work is supported in part by the National Natural Science Foundation of China (62173191)
