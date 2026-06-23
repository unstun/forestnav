---
citation_key: Zheng2023IBBT
arxiv_id: 2304.10984
arxiv_url: https://arxiv.org/abs/2304.10984
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:45:56Z
origin: ai+web
reviewed: false
---

# Introduction

For safe and reliable autonomous robot operation in a real-world environment, consideration of various uncertainties becomes necessary. These uncertainties may arise from an inaccurate motion model, actuation or sensor noise, partial sensing, and the presence of other agents moving in the same environment. In this paper, we study the safe motion planning problem for robot systems with nontrivial dynamics, motion uncertainty, and state-dependent measurement uncertainty in an environment with non-convex obstacles.

Planning under uncertainty is referred to as belief space planning (BSP), where the state of the robot is characterized by a probability distribution function (pdf) over all possible states. This pdf is commonly referred to as the *belief* or information state [@Thrun2005Probabilistic; @Van2012Motion]. A BSP problem can be formulated as a partially observable Markov decision process (POMDP) problem [@Kaelbling1998Planning]. Solving POMDPs for continuous state, control, and observation spaces, is, however, intractable. Existing methods based on discretization are resolution-limited [@Porta2006Point; @shani2013survey]. Optimization over the entire discretized belief space to find a path is computationally expensive and does not scale well to large-scale problems. Online POMDP algorithms are often limited to short-horizon planning, have challenges when dealing with local minima, and are not suitable for global planning in large environments [@somani2013despot]

Planning in infinite-dimensional distributional (e.g., belief) spaces can become more tractable by using sampling-based methods [@Karaman2011Sampling]. For example, belief roadmap methods [@Prentice2009The] build a belief roadmap to reduce estimation uncertainty; the rapidly-exploring random belief trees (RRBT) algorithm [@Bry2011Rapidly] has been proposed to grow a tree in the belief space. Owing to their advantages in avoiding local minima, dealing with nonconvex obstacles and high-dimensional state spaces, along with their anytime property, sampling-based methods have gained increased attention in the robotics community [@Luders2013Robust; @Sun2015High; @Janson2018Monte; @Ichter2017Real; @Agha-Mohammadi2014FIRM].

Robot safety under uncertainty can be also formulated as a chance-constrained optimization problem [@Blackmore2011Chance; @Vitus2011Closed; @Wang2020Non-Gaussian; @Bry2011Rapidly]. In addition to minimizing the cost function, one also wants the robot not to collide with obstacles, with high probability. By approximating the chance constraints as deterministic constraints, references [@Blackmore2011Chance; @Vitus2011Closed; @Wang2020Non-Gaussian] solve the problem using an optimization-based framework. However, those approaches lack scalability with respect to problem complexity [@Aoude2013Prob], and the explicit representation of the obstacles is usually required.

In this paper, we focus on sampling-based approaches similar to [@Bry2011Rapidly; @Luders2013Robust; @Summers2018Distributionally]. One challenge of sampling-based algorithms for planning under uncertainty is the lack of the optimal substructure property, which has been discussed in [@Bry2011Rapidly; @Agha-Mohammadi2014FIRM; @Zheng2021Belief]. The lack of optimal substructure property is further explained by the lack of total ordering on paths based on cost. Specifically, it is not enough to only minimize the usual cost function  --  explicitly finding paths that reduce the uncertainty of the robot is also important (see Figure [1](#BBTmotivation){reference-type="ref" reference="BBTmotivation"}(a)). The RRBT algorithm proposed in [@Bry2011Rapidly] overcomes the lack of optimal substructure property by introducing a partial-ordering of belief nodes and by keeping all non-dominated nodes in the belief tree. Note that without this partial-ordering, the methods in [@Luders2013Robust; @Sun2015High; @Janson2018Monte; @Summers2018Distributionally] may not be able to find a solution, even if one exists. Minimizing the cost and checking the chance constraints can only guarantee that the existing paths in the tree satisfy the chance constraints. Without searching for paths that explicitly reduce state uncertainty, it will be difficult for future paths to satisfy the chance constraints.

In this paper, we propose the Informed Batch Belief Tree (IBBT) algorithm, which improves over the RRBT algorithm with the introduction of *batch sampling* and *ordered graph search guided by an informed heuristic*. Firstly, IBBT uses the partial ordering of belief nodes as in [@Bry2011Rapidly]. Compared to [@Luders2013Robust; @Sun2015High; @Janson2018Monte; @Summers2018Distributionally], IBBT is able to find sophisticated plans that visit and revisit the information-rich region to gain information. Secondly, RRBT uses unordered search like RRT\* while IBBT uses batch sampling and ordered search. RRBT adds one sample each time to the graph randomly. As shown in [@janson2015fast] and [@gammell2020batch], ordered searches such as FMT\* and BIT\* perform better than RRT\*. Thirdly, RRBT only uses the cost-to-come cost to guide the belief tree search while IBBT introduces a cost-to-go heuristic and uses the total path cost heuristic for informed belief tree search. After adding a sample, RRBT performs an exhaustive graph search. Thus all non-dominated belief nodes are added to the belief tree. With batch sampling and informed graph search, IBBT avoids adding unnecessary belief nodes. Thus, IBBT is able to find the initial solution in a shorter time and has better cost-time performance compared to RRBT.

# Related Works {#SecRelatedWorks}

In [@Prentice2009The], the problem of finding the minimum estimation uncertainty path for a robot from a starting position to a goal is studied by building a roadmap. In [@Bry2011Rapidly; @Van2011LQG-MP], it was noted that the true *a priori* probability distribution of the state should be used for motion planning instead of assuming maximum likelihood observations [@Prentice2009The; @Platt2010Belief]. A linear-quadratic Gaussian (LQG) controller along with the RRT algorithm [@lavalle2001randomized] were used for motion planning in [@Van2011LQG-MP]. To achieve asymptotic optimality, the authors in [@Bry2011Rapidly] incrementally construct a graph and search over the graph to find all non-dominated belief nodes. Given the current graph, the Pareto frontier of belief nodes at each vertex is saved, where the Pareto frontier is defined by considering both the path cost and the node uncertainty.

In [@Sun2015High] high-frequency replanning is shown to be able to better react to uncertainty during plan execution. Monte Carlo simulation and importance sampling are used in [@Janson2018Monte] to compute the collision probability. Moving obstacles are considered in [@Aoude2013Prob]. In [@Liu2014Incremental], state dependence of the collision probability is considered and incorporated with chance-constraint RRT\* [@Luders2013Robust; @Luders2010Chance]. In [@Shan2017Belief], a roadmap search method is proposed to deal with localization uncertainty; however, solutions for which the robot needs to revisit a position to gain information are ruled out. Distributionally robust RRT is proposed in [@Summers2018Distributionally; @Safaoui2021Risk], where moment-based ambiguity sets of distributions are used to enforce chance constraints instead of assuming Gaussian distributions. Similarly, a moment-based approach that considers non-Gaussian state distributions is studied in [@Wang2020Moment]. In [@Ho2022Gaussian], the Wasserstein distance is used as a metric for Gaussian belief space planning. The algorithm is compared with RRBT. However, from the simulation results, RRBT usually finds better (lower cost) plans and thus has a better convergence performance.

Other works that are not based on sampling-based methods formulate the chance-constrained motion planning problem as an optimization problem [@Blackmore2011Chance; @Vitus2011Closed; @Wang2020Non-Gaussian]. In those methods, the explicit representation of the obstacles is usually required. The obstacles may be represented by convex constraints or polynomial constraints. The chance constraints are then approximated as deterministic constraints and the optimization problem is solved by convex [@Vitus2011Closed] or nonlinear programming [@Wang2020Non-Gaussian]. Differential dynamic programming has also been used to solve motion planning under uncertainty [@Van2012Motion; @Sun2021Belief; @Rahman2021Uncertainty]. These algorithms find a locally optimal trajectory in the neighborhood of a given reference trajectory. The algorithms iteratively linearize the system dynamics along the reference trajectory and solve an LQG problem to find the next reference trajectory.

# Problem formulation {#SecProblemformulation}

We consider the problem of planning for a robot with nontrivial dynamics, model uncertainty, measurement uncertainty from sensor noise, and obstacle constraints. The state-space $\mathcal{X}$ is decomposed into free space $\mathcal{X}_\mathrm{free}$ and obstacle space $\mathcal{X}_\mathrm{obs}$. The motion planning problem is given by $$\begin{align}
& \mathop{\arg\min}_{u_k} \ \mathbb{E}\left[\sum_{k=0}^{N-1} J(x_k, u_k) \right], \label{eq:obj}\\
\mathrm{s.t.} \ \ & x_0 \sim \mathcal{N}(\bar{x}_s,P_0), \ \bar{x}_N=\bar{x}_g, \label{eq:constraint1}\\
& P(x_k \in \mathcal{X}_\mathrm{obs}) < \delta, \ k = 0, \cdots, N, \label{eq:constraint2}\\
& x_{k+1} = f(x_k,u_k,w_k), \ k=0,\ldots,N-1, \label{eq:nonlinearModel}\\
& y_k = h(x_k,v_k), \ k=0,\ldots,N-1, \label{eq:nonlinearModel1}
\end{align}$$ where ([\[eq:nonlinearModel\]](#eq:nonlinearModel){reference-type="ref" reference="eq:nonlinearModel"}) and ([\[eq:nonlinearModel1\]](#eq:nonlinearModel1){reference-type="ref" reference="eq:nonlinearModel1"}) are the motion and sensing models, respectively. Furthermore, $x_k \in \mathbb{R}^{n_x}$ is the state, $u_k \in \mathbb{R}^{n_u}$ is the control input, and $y_k \in \mathbb{R}^{n_y}$ is the measurement at time step $k = 0,1,\ldots,N-1$, where the steps of the noise processes $w_k \in \mathbb{R}^{n_w}$ and $v_k \in \mathbb{R}^{n_y}$ are i.i.d standard Gaussian random vectors, respectively. We assume that $(w_k)_{k=0}^{N-1}$ and $(v_k)_{k=0}^{N-1}$ are independent. Expression ([\[eq:constraint1\]](#eq:constraint1){reference-type="ref" reference="eq:constraint1"}) is the boundary condition for the motion planning problem. The goal is to steer the system from some initial distribution to a goal state. Since the robot state is uncertain, the mean of the final state $\bar{x}_N$ is constrained to be equal to the goal state $\bar{x}_g$. Condition ([\[eq:constraint2\]](#eq:constraint2){reference-type="ref" reference="eq:constraint2"}) is a chance constraint that enforces safety of the robot.

Similar to [@Bry2011Rapidly], the motion plan considered in this paper is formed by a nominal trajectory and a feedback controller that stabilizes the system around the nominal trajectory. Specifically, we will use a `Connect` function that returns a nominal trajectory and a stabilizing controller between two states $\bar{x}^a$ and $\bar{x}^b$, $$\begin{equation}
        (\bar{X}^{a,b}, \bar{U}^{a,b}, K^{a,b}) = \texttt{Connect}(\bar{x}^a, \bar{x}^b),
\end{equation}$$ $\bar{X}^{a,b}$ and $\bar{U}^{a,b}$ are the sequence of states and controls of the nominal trajectory, and $K^{a,b}$ is a sequence of the corresponding feedback control gains. The nominal trajectory can be obtained by solving a deterministic optimal control problem with boundary conditions $\bar{x}^a$ and $\bar{x}^b$, and system dynamics $\bar{x}_{k+1} = f(\bar{x}_k,\bar{u}_k,0)$. The stabilizing controller can be computed using, for example, finite-time LQR design [@Agha-Mohammadi2014FIRM].

A Kalman filter is used for online state estimation, which gives the state estimate[^4] $\hat{x}_k$ of $(x_k - \bar{x}_k)$. Thus, the control at time $k$ is given by $$\begin{align}
        u_k = \bar{u}_k + K_k \hat{x}_k. \label{eq:feedbackControl}
\end{align}$$

With the introduction of the `Connect` function, the optimal motion planning problem ([\[eq:obj\]](#eq:obj){reference-type="ref" reference="eq:obj"})-([\[eq:nonlinearModel1\]](#eq:nonlinearModel1){reference-type="ref" reference="eq:nonlinearModel1"}) is reformulated as finding the sequence of intermediate states $(\bar{x}^0, \bar{x}^1, \cdots, \bar{x}^{\ell})$. The final control is given by $$\begin{align}
        (u_k)_{k=0}^{N-1} = (\texttt{Connect}(\bar{x}^0, \bar{x}^1), \cdots, \texttt{Connect}(\bar{x}^{\ell - 1}, \bar{x}^{\ell})).
\end{align}$$ The remaining problem is to find the optimal sequence of intermediate states and enforce the chance constraints ([\[eq:constraint2\]](#eq:constraint2){reference-type="ref" reference="eq:constraint2"}).

# Covariance Propagation {#Sec:Preliminary}

We assume that the system given by ([\[eq:nonlinearModel\]](#eq:nonlinearModel){reference-type="ref" reference="eq:nonlinearModel"}) and ([\[eq:nonlinearModel1\]](#eq:nonlinearModel1){reference-type="ref" reference="eq:nonlinearModel1"}) is locally well approximated by its linearization along the nominal trajectory. This is a common assumption as the system will stay close to the nominal trajectory using the feedback controller [@Agha-Mohammadi2014FIRM; @Zheng2021Belief]. Define $$\begin{align}
    \check{x}_k &= x_k - \bar{x}_k, \label{a}\\
    \check{u}_k &= u_k - \bar{u}_k, \label{b}\\
    \check{y}_k &= y_k - h(\bar{x}_k, 0). \label{c}
\end{align}$$ By linearizing along $(\bar{x}_k,\bar{u}_k)$, the error dynamics is $$\begin{equation}
\begin{split}
    \check{x}_k &= A_{k-1} \check{x}_{k-1} + B_{k-1} \check{u}_{k-1} + G_{k-1} w_{k-1}, \\
    \check{y}_k &= C_k \check{x}_k + D_k v_k.
    \label{EQ:LTV}
\end{split}
\end{equation}$$ We will consider this linear time-varying system hereafter. A Kalman filter is used for estimating $\check{x}_k$ and is given by $$\begin{align}
    \hat{x}_{k} & = \hat{x}_{k^{\mbox{\scriptsize{-}}}} + L_k (\check{y}_k - C_k \hat{x}_{k^{\mbox{\scriptsize{-}}}}), \label{KFdynamics}\\
    \hat{x}_{k^{\mbox{\scriptsize{-}}}} & = A_{k-1} \hat{x}_{k-1} + B_{k-1} \check{u}_{k-1},
    \label{KFdynamics1}
\end{align}$$ where, $$\begin{align}
L_k & =\tilde{P}_{k^{\mbox{\scriptsize{-}}}} C_k ^{\mbox{\tiny\sf T}}( C_k \tilde{P}_{k^{\mbox{\scriptsize{-}}}} C_k ^{\mbox{\tiny\sf T}}+ D_k D_k ^{\mbox{\tiny\sf T}})^{-1}, \label{KFupdatea} \\
\tilde{P}_k & =( I - L_k C_k) \tilde{P}_{k^{\mbox{\scriptsize{-}}}}, \label{KFupdateb}\\
\tilde{P}_{k^{\mbox{\scriptsize{-}}}} & = A_{k-1} \tilde{P}_{k-1} A_{k-1} ^{\mbox{\tiny\sf T}}+G_{k-1} G_{k-1} ^{\mbox{\tiny\sf T}},
\label{KFupdatec}
\end{align}$$ and $L_k$ is the Kalman gain. The covariances of $\check{x}_k$, $\hat{x}_k$ and $\tilde{x}_k \triangleq \check{x}_k - \hat{x}_k$ are denoted as $P_k = \mathbb{E}[\check{x}_k \check{x}_k ^{\mbox{\tiny\sf T}}]$, $\hat{P}_k = \mathbb{E}[\hat{x}_k \hat{x}_k ^{\mbox{\tiny\sf T}}]$ and $\tilde{P}_k = \mathbb{E}[\tilde{x}_k \tilde{x}_k ^{\mbox{\tiny\sf T}}]$, respectively. Note that the covariance of $x_k$ is also given by $P_k$ and the estimation error covariance $\tilde{P}_k$ is computed from ([\[KFupdateb\]](#KFupdateb){reference-type="ref" reference="KFupdateb"}). From ([\[EQ:LTV\]](#EQ:LTV){reference-type="ref" reference="EQ:LTV"})-([\[KFdynamics1\]](#KFdynamics1){reference-type="ref" reference="KFdynamics1"}), it can be verified that $\mathbb{E}[\check{x}_k] = \mathbb{E}[\hat{x}_k] = \mathbb{E}[\hat{x}_{k^{\mbox{\scriptsize{-}}}}]$. Since $\mathbb{E}[\check{x}_0] = 0$, by choosing $\mathbb{E}[\hat{x}_0] = 0$, we have $\mathbb{E}[\hat{x}_k] = 0$ for $k = 0, \cdots, N$. Using ([\[KFdynamics\]](#KFdynamics){reference-type="ref" reference="KFdynamics"}) and ([\[KFdynamics1\]](#KFdynamics1){reference-type="ref" reference="KFdynamics1"}) we also have that $$\begin{equation}
\begin{split}
    \hat{P}_k &= \mathbb{E}[\hat{x}_k \hat{x}_k ^{\mbox{\tiny\sf T}}]  \\
    &= \mathbb{E}[\hat{x}_{k^{\mbox{\scriptsize{-}}}} \hat{x}_{k^{\mbox{\scriptsize{-}}}} ^{\mbox{\tiny\sf T}}] + L_k (C_k \tilde{P}_{k^{\mbox{\scriptsize{-}}}} C_k ^{\mbox{\tiny\sf T}}+ D_k D_k ^{\mbox{\tiny\sf T}}) L_k^{\mbox{\tiny\sf T}}\label{estimatedstateCov}\\
    &= (A_{k-1}+B_{k-1}K_{k-1}) \hat{P}_{k-1} (A_{k-1}+B_{k-1}K_{k-1}) ^{\mbox{\tiny\sf T}}+ L_k C_k \tilde{P}_{k^{\mbox{\scriptsize{-}}}}
\end{split}
\end{equation}$$ Using the fact that $\mathbb{E}[\hat{x}_k \tilde{x}_k ^{\mbox{\tiny\sf T}}] = 0$, it can be verified that $P_k = \hat{P}_k + \tilde{P}_k$. Thus, given the feedback gains $K_k$ and the Kalman filter gain $L_k$, we can predict the covariances of the state estimation error and the state along the trajectory, which also provides the state distributions in the case of a Gaussian distribution.

# Informed Batch Belief Tree Algorithm {#SecBBT}

## Motivation

:::: {#BBTmotivation .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/1figa.png){width="1\\columnwidth"}

![](Zheng2023IBBT_figs/1figb.png){width="1\\columnwidth"}

::: caption
\(a\) RRBT: Two paths reach the same point $B$. The red path detours to an information-rich region to reduce uncertainty. Both paths are explored and preserved in the belief tree in RRBT as it finds all non-dominatd belief nodes. (b) IBBT avoids exploring unnecessary belief nodes. If the blue path $\overline{BG}$ satisfies the chance constraint, the whole blue path $\overline{SBG}$ satisfies the chance constraint and has a lower cost than the red path $\overline{SABG}$. The operation of finding more paths reaching $B$ with less uncertainty (but larger cost), including the red one, becomes redundant.
:::
::::

The motivation of IBBT is shown in Figure [1](#BBTmotivation){reference-type="ref" reference="BBTmotivation"}. Two paths reach point $B$ in Figure [1](#BBTmotivation){reference-type="ref" reference="BBTmotivation"}(a). The red path reaches $B$ with a large cost but with low uncertainty. The blue path reaches $B$ with a small cost but with high uncertainty. In this case, the blue path cannot dominate the red path, as it will incur a high probability of chance constraint violation for future segments of the path. Thus, in RRBT, both paths are preserved in the belief tree. More specifically, RRBT will find all non-dominated belief nodes by exhaustively searching the graph.

However, IBBT avoids exhaustive graph search and hence avoids adding unnecessary belief nodes. In Figure [1](#BBTmotivation){reference-type="ref" reference="BBTmotivation"}(b), if the blue path $\overline{BG}$ (starting anywhere inside the blue ellipse) satisfies the chance constraint, the blue path $\overline{SBG}$ will be the solution of the problem since it satisfies the chance constraints and has a lower cost than $\overline{SABG}$. The operation of searching the current graph to find more paths reaching $B$ with less uncertainty (but a higher cost), including the red one, becomes redundant.

Here, we assume that the cost of the nominal trajectory, $\sum_{k=0}^{N-1} J(\bar{x}_k, \bar{u}_k)$, makes most of the cost in ([\[eq:obj\]](#eq:obj){reference-type="ref" reference="eq:obj"}). That is, for the path $\overline{BG}$, starting from the red ellipse and the blue ellipse will incur a similar cost. Reducing the uncertainty at node $B$ is mainly for satisfying the chance constraint of the future trajectory. Such an assumption can also be found, for example, in [@Ichter2017Real].

RRBT performs an exhaustive search to find all non-dominated nodes whenever a vertex is added to the graph. Specifically, RRBT will spend a lot of effort finding nodes with low uncertainty but a high cost-to-come. Such nodes are only necessary if they are indeed part of the optimal path. If the blue path in Figure [1](#BBTmotivation){reference-type="ref" reference="BBTmotivation"}(b) is the solution, we do not need to search for other non-dominated nodes (red ellipse). However, since we do not know if the future blue path $\overline{BG}$ will satisfy the chance constraint or not, the red node may still be needed. Thus, IBBT explores the graph and adds belief nodes to the belief tree only when is necessary. This is done by batch sampling and using an informed heuristic.

## Nominal Trajectory Graph

The stochastic motion planning problem ([\[eq:obj\]](#eq:obj){reference-type="ref" reference="eq:obj"})-([\[eq:nonlinearModel1\]](#eq:nonlinearModel1){reference-type="ref" reference="eq:nonlinearModel1"}) is divided into a simpler deterministic planning problem and a belief tree search problem. The deterministic planning problem is given by $$\begin{align}
& \mathop{\arg\min}_{\bar{u}_k} \ \sum_{k=0}^{N-1} J(\bar{x}_k, \bar{u}_k), \label{DeterministicObj}\\
\mathrm{s.t.} \ \ & \bar{x}_0 = \bar{x}_s, \ \bar{x}_N=\bar{x}_g, \\
& \bar{x}_k \notin \mathcal{X}_\mathrm{obs}, \ k = 0, \cdots, N, \\
& \bar{x}_{k+1} = f(\bar{x}_k,\bar{u}_k,0).
\end{align}$$

The deterministic planning problem can be solved using sampling-based methods. The Rapidly-exploring Random Graph (RRG) [@Karaman2011Sampling] algorithm is adopted to add a batch of samples and maintain a graph of nominal trajectories. Similarly, the PRM algorithm [@Kavraki1996Prob] may be used in place of RRG.

::: algorithm
$\bar{x}_\mathrm{rand} \leftarrow \texttt{SampleFree}$ $v_\mathrm{nearest} \leftarrow \texttt{Nearest}(V, \bar{x}_\mathrm{rand})$ $e_\mathrm{nearest} \leftarrow \texttt{Connect}(v_\mathrm{nearest}.\bar{x}, \bar{x}_\mathrm{rand})$ $V_\mathrm{near} \leftarrow \texttt{Near}(V, \bar{x}_\mathrm{rand})$ $V \leftarrow V \cup \{ v(\bar{x}_\mathrm{rand}) \}$ $E \leftarrow E \cup \{ e_\mathrm{nearest} \}$ $e \leftarrow \texttt{Connect}(\bar{x}_\mathrm{rand}, v_\mathrm{nearest}.\bar{x})$ $E \leftarrow E \cup \{ e \}$ $e \leftarrow \texttt{Connect}(v_\mathrm{near}.\bar{x}, \bar{x}_\mathrm{rand})$ $E \leftarrow E \cup \{ e \}$ $e \leftarrow \texttt{Connect}(\bar{x}_\mathrm{rand}, v_\mathrm{near}.\bar{x})$ $E \leftarrow E \cup \{ e \}$ $G, V_\mathrm{new}$
:::

The RRG-D algorithm given by Algorithm [\[alg:RRG-D\]](#alg:RRG-D){reference-type="ref" reference="alg:RRG-D"} follows the RRG algorithm developed in [@Karaman2011Sampling] with the additional consideration of system dynamics. RRG-D uses the `Connect` function introduced in Section [3](#SecProblemformulation){reference-type="ref" reference="SecProblemformulation"} to build a graph of nominal trajectories. The edge is added to the graph only if the nominal trajectory is obstacle-free, which is indicated by the `ObstacleFree` checking in Algorithm [\[alg:RRG-D\]](#alg:RRG-D){reference-type="ref" reference="alg:RRG-D"}. RRG-D draws $m$ samples whenever it is called by the IBBT algorithm. The $m$ samples constitute one batch. The sampled states $\bar{x}$ along with the edges $e$ connecting them generate a graph in the search space. For belief space planning, each vertex $v$ has both state information $v.\bar{x}$ and belief information $v.N$. We use $v(\bar{x})$ to refer to the vertex $v$ whose state is $v.\bar{x}$. RRG-D returns the updated new graph and the newly added vertex set $V_\mathrm{new}$.

## IBBT

The Informed Batch Belief Tree algorithm repeatedly performs two main operations: It first builds a graph of nominal trajectories to explore the state space of the robot, and then it searches over this graph to grow a belief tree in the belief space. The IBBT algorithm is given by Algorithm [\[alg:IBBT\]](#alg:IBBT){reference-type="ref" reference="alg:IBBT"} and Algorithm [\[alg:GS\]](#alg:GS){reference-type="ref" reference="alg:GS"}.

::: algorithm
$n.P \leftarrow P_0$; $n.\tilde{P} \leftarrow \tilde{P}_0$; $n.c \leftarrow 0$; $n.h \leftarrow \mathrm{Inf}$; $n.\mathrm{parent} \leftarrow \mathrm{null}$ $v_s.N \leftarrow \{n\}$; $v_g.N \leftarrow \emptyset$ $v_s.\bar{x} \leftarrow \bar{x}_s$; $v_g.\bar{x} \leftarrow \bar{x}_g$ $v_s.h \leftarrow \mathrm{Inf}$; $v_g.h \leftarrow 0$ $V \leftarrow \{v_s, v_g\}$; $E \leftarrow \emptyset$; $G \leftarrow (V, E)$ $Q \leftarrow \{n\}$; $Cost \leftarrow \mathrm{Inf}$ $(G, V_\mathrm{new}) = \texttt{RRG-D}(G,m)$ $G = \texttt{ValueIteration}(G)$ $Q \leftarrow Q \cup v_\mathrm{neighbor}.N$ $\texttt{Prune}(Q, Cost)$ $Q \leftarrow Q \cup v_g.N$ $(G, Q, \mathrm{flag}) = \texttt{GraphSearch}(G, Q)$ $Cost = \min\{ n.c | \forall n \in v_g.N\}$ $G, \mathrm{flag}$;
:::

::: algorithm
$\mathrm{flag} \leftarrow \mathbf{False}$ $n \leftarrow \texttt{Pop}(Q)$ $\mathrm{flag} \leftarrow \mathbf{True}$ $G, Q, \mathrm{flag}$; $n_\mathrm{new} \leftarrow \texttt{Propagate}(e_\mathrm{neighbor}, n)$ $\mathrm{succ}, G \leftarrow \texttt{AppendBelief}(G, v_\mathrm{neighbor}, n_\mathrm{new})$ $Q \leftarrow Q \cup \{n_\mathrm{new}\}$ $G, Q, \mathrm{flag}$;
:::

Additional variables are needed to define a belief tree. A belief node $n$ is defined by a state covariance $n.P$, an estimation error covariance $n.\tilde{P}$, a cost-to-come $n.c$, a heuristic cost-to-go $n.h$, and a parent node index $n.\mathrm{parent}$. A vertex $v$ is defined by a state $v.\bar{x}$, a set of belief nodes $v.N$, and a vertex cost $v.h$.

The graph search given by Algorithm [\[alg:GS\]](#alg:GS){reference-type="ref" reference="alg:GS"} repeats two primitive procedures to grow a belief tree: *Belief node selection* which selects the best node in the belief queue for expansion; *Belief propagation* which propagates the selected belief node to its neighbor vertices to generate new belief nodes. The metric to rank the belief nodes in the belief queue is vital for efficient graph search.

:::: {#Heuristic .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/heuristic1.png){width="1\\columnwidth"}

![](Zheng2023IBBT_figs/heuristic2.png){width="1\\columnwidth"}

::: caption
\(a\) Nominal trajectory graph. Each edge is computed by solving a deterministic optimal control problem with edge cost given by ([\[DeterministicObj\]](#DeterministicObj){reference-type="ref" reference="DeterministicObj"}). (b) Two belief nodes are shown at vertex $v_i$.
:::
::::

Based on the nominal trajectory graph, we can compute the cost-to-go for all vertices. A nominal trajectory graph is shown in Figure [2](#Heuristic){reference-type="ref" reference="Heuristic"}(a). Every edge in the graph is computed by solving a deterministic optimal control problem with edge cost given by ([\[DeterministicObj\]](#DeterministicObj){reference-type="ref" reference="DeterministicObj"}). We compute the cost-to-go $v_i.h$ using value iteration for every vertex in the graph. $v_i.h$ is the true cost-to-go for the nominal trajectory graph and is an informed, admissible cost-to-go heuristic for the belief tree search problem. Here we assume that $J(\bar{x}_k, \bar{u}_k) \leq \mathbb{E} \left[ J(x_k, u_k) \right]$, thus $\sum_{k=0}^{N-1} J(\bar{x}_k, \bar{u}_k) \leq \mathbb{E}\left[\sum_{k=0}^{N-1} J(x_k, u_k) \right]$. This assumption is true when $J(x_k, u_k)$ is a convex function by using Jensen's inequality [@Feller1991An]. For example, a quadratic cost is very common in robotics applications where we want to minimize control effort and state uncertainty (covariance). Moreover, additional chance constraint checking is performed in the belief tree search. Therefore, $\sum_{k=0}^{N-1} J(\bar{x}_k, \bar{u}_k)$ is an underestimate of the actual cost.

The nodes in the belief node queue are ranked based on the total heuristic cost $n.f = n.c + n.h$. All belief nodes at the same vertex have the same heuristic cost-to-go and $n.h = v.h$. In Figure [2](#Heuristic){reference-type="ref" reference="Heuristic"}(b), two belief nodes $n_1$, $n_2$ are shown at vertex $v_i$. Their total heuristic costs are $n_1.f = n_1.c + v_i.h$ and $n_2.f = n_2.c + v_i.h$, respectively.

The partial ordering of belief nodes is defined as follows [@Bry2011Rapidly]. Let $n_a$ and $n_b$ be two belief nodes of the same vertex $v$. We use $n_a < n_b$ to denote that belief node $n_b$ is dominated by $n_a$. $n_a < n_b$ is true if $$\begin{equation}
    (n_{a}.f < n_{b}.f) \land (n_{a}.P < n_{b}.P) \land (n_{a}.\tilde{P} < n_{b}.\tilde{P}).
\end{equation}$$ In this case, $n_a$ is better than $n_b$ since it traces back a path that reaches $v$ with less cost and less uncertainty compared with $n_b$. Next, we summarize some primitive procedures used in the IBBT algorithm.\
**Pop:** $\texttt{Pop}(Q)$ selects the best belief node in term of the lowest cost $n.f$ from belief queue $Q$ and removes it from $Q$.\
**Propagate:** The `Propagate` procedure implements three operations: covariance propagation, chance constraint evaluation, and cost calculation. $\texttt{Propagate}(e, n)$ performs the covariance propagation using ([\[KFupdatea\]](#KFupdatea){reference-type="ref" reference="KFupdatea"})-([\[estimatedstateCov\]](#estimatedstateCov){reference-type="ref" reference="estimatedstateCov"}). It takes an edge $e$ and a belief node $n$ at the starting vertex of the edge as inputs. Chance constraints are evaluated using the state covariance $P_k$ along the edge. If there are no chance constraint violations, a new belief $n_\mathrm{new}$ is returned, which is the final belief at the end vertex of the edge. Otherwise, the procedure returns no belief. The cost-to-come of $n_\mathrm{new}$ is the sum of $n.c$ and the cost of edge $e$ by applying the controller ([\[eq:feedbackControl\]](#eq:feedbackControl){reference-type="ref" reference="eq:feedbackControl"}) associated with $e$.\
**Append Belief:** The function `AppendBelief`$(G,v,n_\mathrm{new})$ decides if the new belief $n_\mathrm{new}$ should be added to vertex $v$ or not. If $n_\mathrm{new}$ is not dominated by any existing belief nodes in $v.N$, $n_\mathrm{new}$ is added to $v.N$. Note that adding $n_\mathrm{new}$ means extending the current belief tree such that $n_\mathrm{new}$ becomes a leaf node of the current belief tree. Next, we also check if any existing belief node in $v.N$ is dominated by $n_\mathrm{new}$. If an existing belief is dominated, its descendant and the node itself are pruned.\
**Prune Node Queue:** The function `Prune`$(Q,Cost)$ removes nodes in $Q$ whose total heuristic cost is greater than $Cost$. $Cost$ is the cost of the current solution found.\
**Value Iteration:** The function `ValueIteration`$(G)$ computes the cost-to-go for all vertices in $G$ use value iteration. The value iteration is done using the nominal trajectory graph. For vertices whose cost-to-go values are computed in the last iteration (before calling this function), their values are reused for initialization for faster convergence.\
In Algorithm [\[alg:IBBT\]](#alg:IBBT){reference-type="ref" reference="alg:IBBT"}, Line 1-5 initializes the graph and the belief tree. The initial condition of the motion planning problem is given by the starting state $\bar{x}_s$, state covariance $P_0$, and estimation error covariance $\tilde{P}_0$. The goal state is $\bar{x}_g$. In Line 6, the queue $Q$ is initialized with the initial node $n$ and the cost of the current solution is set as infinity. In Line 8, the RRG-D is called to add $m$ samples and maintain a graph of nominal trajectories, $V_\mathrm{new}$ is the set of newly added vertices after calling RRG-D. Based the on the nominal trajectory graph, cost-to-go for all vertices in $G$ is computed using value iteration (Line 9). Line 10-12 update the belief node queue after batch sampling. For every vertex that has an outgoing edge towards $v_\mathrm{new}$, all the belief nodes at that vertex are added to the queue.

In Algorithm [\[alg:GS\]](#alg:GS){reference-type="ref" reference="alg:GS"}, the belief $n$ is propagated outwards to all the neighbor vertices of $v(n)$ to grow the belief tree in Line 7-11. $v(n)$ refers to the vertex associated with $n$. $v_\mathrm{neighbor}$ is a neighbor of $v(n)$ when there is an edge $e_\mathrm{neighbor}$ from $v(n)$ to $v_\mathrm{neighbor}$ in the graph. The new belief $n_\mathrm{new}$ is added to the $v_{\mathrm{neighbor}}.N$ and $Q$ if the belief tree extension is successful. Then, $n$ is marked as the parent node of $n_\mathrm{new}$. Note that each belief node traces back a unique path from the initial belief node. For every belief node in the belief tree, we already found a feasible path (satisfies chance constraint) to this node. Algorithm [\[alg:GS\]](#alg:GS){reference-type="ref" reference="alg:GS"} terminates when the belief node at $\bar{x}_g$ is selected for expansion (Line 4-6, Algorithm [\[alg:GS\]](#alg:GS){reference-type="ref" reference="alg:GS"}) or $Q$ is empty. In the first case, the best solution is found. In the second case, no solution exists given the current graph.

# Experimental Results {#SecExperiment}

In this section, we test the IBBT algorithm for different motion planning problems and compared the results with the RRBT algorithm [@Bry2011Rapidly].

:::: {#FirstEnv:tree .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/2figa.png){width="1\\columnwidth"}

![](Zheng2023IBBT_figs/2figb.png){width="1\\columnwidth"}

::: caption
\(a\) Nominal trajectory graph and belief tree from the RRBT algorithm. (b) Nominal trajectory graph and belief tree from the IBBT algorithm. Both algorithms stop when they find the first solution. The extra ellipses in the left figure indicate that RRBT adds more nodes to the belief tree by exhaustive search. IBBT avoids unnecessary belief nodes expansion and find the same solution faster.
:::
::::

:::: {#FirstEnv:result .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/2figc.png){width="0.38\\columnwidth"}

::: caption
First solution found by both algorithms.
:::
::::

:::: {#FirstEnv:compare .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/3fig.png){width="0.6\\columnwidth"}

::: caption
Comparison between the IBBT and the RRBT algorithms. IBBT is faster to find the first solution.
:::
::::

## Double Integrator

The first planning environment is shown in Figure [3](#FirstEnv:tree){reference-type="ref" reference="FirstEnv:tree"}. The gray areas are obstacles and the blue region is the information-rich region, that is, the measurement noise is small when the robot is in this region. We use the 2D double integrator dynamics with motion and sensing uncertainties as an example. The system model is linear and is given by $$\begin{equation}
\begin{split}
    {x}_{k+1} &= A_k x_k + B_k u_k + G_k w_k, \\
    y_k &= C_k x_k + D_k v_k,
    \label{DoubleIntegrator}
\end{split}
\end{equation}$$ where the system state includes position and velocity, the control input is the acceleration. The system matrices are given by $$\begin{equation}
    A_k = \begin{bmatrix} 1 & 0 & \Delta t & 0 \\ 0 & 1 & 0 & \Delta t \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}, \quad
    B_k = \begin{bmatrix} \Delta t^2/2 & 0 \\ 0 & \Delta t^2/2 \\ \Delta t & 0 \\ 0 & \Delta t \end{bmatrix}, \quad
    C_k = I_4,
\end{equation}$$ $G_k = \sqrt{\Delta t} \, \mathrm{diag}(0.03, 0.03, 0.02, 0.02)$, and $D_k = 0.01 I_4$ when the robot is in a information-rich region, otherwise $D_k = I_4$.

To compute the nominal trajectories, the analytical solution is available [@Zheng2021Belief]. An LQG controller is used to compute the feedback gain $K$ in the `Connect` function. The collision probability in the chance constraint is approximated using Monte Carlo simulations. We sample from the state distribution and count the number of samples that collide with the obstacles. The ratio of collided samples to the total samples is the approximate collision probability.

We compared the performance of RRBT and IBBT to find the first solution. The belief tree from RRBT is shown in Figure [3](#FirstEnv:tree){reference-type="ref" reference="FirstEnv:tree"}(a), and the belief tree from IBBT is shown in Figure [3](#FirstEnv:tree){reference-type="ref" reference="FirstEnv:tree"}(b). Both algorithms use the same set of states and find the same solution, which is given in Figure [4](#FirstEnv:result){reference-type="ref" reference="FirstEnv:result"}. The robot first goes down to the information-rich region to reduce its uncertainty, while directly moving toward to goal will violate the chance constraint.

Fewer belief nodes are searched and added to the tree using IBBT compared with RRBT, even though they return the same solution. IBBT uses batch sampling and computes the informed cost-to-go heuristic to guide the belief tree search, while RRBT only uses the cost-to-come. RRBT tries to find all non-dominated belief nodes whenever a vertex is added to the graph. Thus, it will find belief nodes that have low uncertainty but high cost-to-come (shown as small ellipses in Figure [3](#FirstEnv:tree){reference-type="ref" reference="FirstEnv:tree"}(a)). However, if such a node is not part of the solution path, this computation is not necessary. The comparison of the results is shown in Figure [5](#FirstEnv:compare){reference-type="ref" reference="FirstEnv:compare"}. The solving time for IBBT and RRBT is around 0.05 sec and 0.14 sec respectively.

:::: {#SecondEnv .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/5FirstSol.png){width="\\columnwidth"}

![](Zheng2023IBBT_figs/5FinalSol1.png){width="\\columnwidth"}

::: caption
Planning results of double integrator. (a) The first solution returned by IBBT; (b) Final solution with solving time less than 2 sec.
:::
::::

:::: {#SecondEnv:compare .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/6CostTime.png){width="0.66\\columnwidth"}

::: caption
Comparison between IBBT and RRBT. IBBT has better cost-time performance and finds the first solution with less time.
:::
::::

The second planning environment is shown in Figure [6](#SecondEnv){reference-type="ref" reference="SecondEnv"}. The problem setting is similar to the first environment except that more obstacles and information-rich regions are added. The first solution and the improved solution are shown in Figure [6](#SecondEnv){reference-type="ref" reference="SecondEnv"}(a) and Figure [6](#SecondEnv){reference-type="ref" reference="SecondEnv"}(b), respectively. The green lines are the mean trajectories. The gray lines around the green lines are the Monte-Carlo simulation results. The comparison with the RRBT algorithm is given in Figure [7](#SecondEnv:compare){reference-type="ref" reference="SecondEnv:compare"}. After finding the initial solution, both algorithms are able to improve their solution when more samples are added to the graph but IBBT is able to find a better solution in a much shorter time.

## Dubins Vehicle

Finally, we tested our algorithm using the Dubins vehicle model. The deterministic discrete-time model is given by $$\begin{equation}
\begin{split}
    {x}_{k+1} &= x_k + \cos{\theta_{k}} \Delta t, \\
    {y}_{k+1} &= y_k + \sin{\theta_{k}} \Delta t, \\
    {\theta}_{k+1} &= \theta_k + u_k \Delta t.
    \label{Eq:Dubin}
\end{split}
\end{equation}$$ The nominal trajectory for the Dubins vehicle is chosen as the minimum length path connecting two configurations of the vehicle. The analytical solution for the nominal trajectory is available in [@LaValle2006Planning].

After linearization, the error dynamics around the nominal path is given by ([\[DoubleIntegrator\]](#DoubleIntegrator){reference-type="ref" reference="DoubleIntegrator"}), where the system matrices are $$\begin{equation}
    A_k = \begin{bmatrix} 1 & 0 & -\sin{\theta_k} \Delta t \\ 0 & 1 & \cos{\theta_k}\Delta t \\ 0 & 0 & 1 \end{bmatrix}, \quad
    B_k = \begin{bmatrix} 0 \\ 0 \\ \Delta t \end{bmatrix}, \quad
    C_k = I_3.
\end{equation}$$ $G_k = \sqrt{\Delta t}\, \mathrm{diag}(0.02, 0.02, 0.02)$, $D_k = 0.1 I_3$ when the robot is in a information-rich region, otherwise $D_k = 2 I_3$. An LQG controller is used to compute the feedback gain $K$, the weighting matrices of the LQG cost are $Q = 2 I_3$ and $R = 1$.

The first solution and the improved solution are shown in Figure [8](#Fig:Dubin){reference-type="ref" reference="Fig:Dubin"}(a) and Figure [8](#Fig:Dubin){reference-type="ref" reference="Fig:Dubin"}(b), respectively. The green line is the mean trajectory. The gray lines around the green lines are the Monte-Carlo simulations. The comparison with the RRBT algorithm is given in Figure [9](#Dubin:compare){reference-type="ref" reference="Dubin:compare"}. After finding the initial solution, both algorithms are able to improve their current solution when more samples are added to the graph. Again, IBBT has better cost vs. time performance.

:::: {#Fig:Dubin .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/7FirstSol.png){width="\\columnwidth"}

![](Zheng2023IBBT_figs/7FinalSol.png){width="\\columnwidth"}

::: caption
Planning results of the Dubins vehicle. (a) First solution. (b) Final solution.
:::
::::

:::: {#Dubin:compare .figure latex-placement="htb"}
![](Zheng2023IBBT_figs/8CostTime.png){width="0.66\\columnwidth"}

::: caption
Comparison between IBBT and RRBT. IBBT has better cost-time performance and finds the first solution with less time.
:::
::::

# Conclusion {#secConclusion}

We developed an online, anytime, incremental algorithm, IBBT, for motion planning under uncertainties. The algorithm considers a robot that is partially observable, has motion uncertainty, and operates in a continuous domain. The algorithm interleaves between batch sampling, building a graph of nominal trajectories in the state space, and searches over the graph to grow a belief tree. The heuristic cost-to-go is computed using the nominal trajectory graph along with value iteration. This cost-to-go along with the cost-to-come provides an informed heuristic to guide the belief tree search. The algorithm finds motion plans that converge to the optimal one as more batches of samples are added to the graph. We have tested the IBBT algorithm in different planning environments. The proposed algorithm finds non-trivial motion plans and provides better solutions using a smaller amount of time compared with previous methods.

[^1]: This work has been supported by NSF award IIS-2008695 and by Ford through the Georgia Tech/Ford Alliance program.

[^2]: $^{1}$Dongliang Zheng is a Ph.D. student with the School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA 30332, USA. Email: `dzheng@gatech.edu`

[^3]: $^{2}$Panagiotis Tsiotras is a Professor with the School of Aerospace Engineering and Institute for Robotics and Intelligent Machines, Georgia Institute of Technology, Atlanta, GA 30332, USA. Email: `tsiotras@gatech.edu`

[^4]: Note non-standard notation.
