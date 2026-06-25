---
citation_key: OrtizHaro2024iDbRRT
arxiv_id: 2403.10745
arxiv_url: https://arxiv.org/abs/2403.10745
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:36:28Z
origin: ai+web
reviewed: false
---

# Introduction

Kinodynamic motion planning is a fundamental problem in robotics where the goal is to find collision-free trajectories in high-dimensional, continuous, and non-convex spaces, while also considering actuation limits and dynamics of the robot. Over the last two decades, a wide variety of sampling-, search-, and optimization-based methods have been proposed to address (kinodynamic) motion planning problems.

A breakthrough was the introduction of Rapidly-exploring Random Trees (RRT) [@lavalle1998rapidly], a sampling-based method that incrementally builds a tree of configurations by expanding nodes towards randomly sampled new configurations. RRT-like algorithms (e.g., [@karaman2011sampling; @kuffner2000rrt; @bohlin2001randomized; @gammel2014informed; @RABITstar; @gammell2015batch]) are highly efficient for geometric planning, i.e., motion planning settings that involve only joint configurations of the system, since in the geometric setting, two configurations can be connected exactly by using linear interpolation.

Although RRT-like algorithms can be adapted for kinodynamic motion planning (e.g., [@webb2012kinodynamic; @long2020fuzzy]), their efficiency significantly decreases, as they typically require solving multiple two-point boundary value problems or the propagation of random control inputs. Two-point boundary problems, as they arise for most robotic systems, often do not have an analytic solution, and solving them is computationally expensive, generally requiring the solution of a nonlinear trajectory optimization problem. Propagating random control inputs tends to be uninformative for many systems, as random controls can lead to poor exploration of the state space, particularly in highly nonlinear systems such as quadrotors where random inputs often lead to instability in the system. Further, it is not clear how to perform a bidirectional search, as in RRT-Connect [@kuffner2000rrt], in the kinodynamic setting with the propagation of random inputs.

:::: figure
  ------------------------------------------------------------ ---------------------------------------------------------------
   ![image](OrtizHaro2024iDbRRT_figs/start_search.png){width="23.5%"}     ![image](OrtizHaro2024iDbRRT_figs/mid_search.png){width="23.5%"}
                              (a)                                                            (b)
   ![image](OrtizHaro2024iDbRRT_figs/finis_search.png){width="23.5%"}   ![image](OrtizHaro2024iDbRRT_figs/search_with_opt.png){width="23.5%"}
                              (c)                                                            (d)
  ------------------------------------------------------------ ---------------------------------------------------------------

::: caption
iDb-RRT combines a forward or bidirectional RRT search with motion primitives (Db-RRT) and trajectory optimization iteratively. (a,b) In the search step, the RRT is expanded by connecting motion primitives with a bounded discontinuity. (c) The output of the RRT is a trajectory with a bounded discontinuity in the dynamics constraints. (d) Using trajectory optimization, we generate a dynamically feasible trajectory. Problem visualization: *Planar Rotor in Double bugtrap*.
:::
::::

Alternative approaches for kinodynamic motion planning are optimization-based methods [@TrajOpt; @GuSTO; @malyutaConvexOptimizationTrajectory2021], which scale polynomially instead of exponentially but require an initial guess and may fail to converge; and search-based methods [@PivtoraikoThesis; @pivtoraikoKinodynamicMotionPlanning2011], which provide strong theoretical guarantees but require a pre-defined discretization of the state or control space. More recently, hybrid methods have been proposed to merge the strengths of the three previous approaches to kinodynamic motion planning [@natarajanInterleavingGraphSearch2021; @sakcakSamplingbasedOptimalKinodynamic2019; @DIRT; @kamat2022bitkomo; @natarajan2024pinsat]. Iterative Discontinuity-Bounded A\* (iDb-A\*) [@ortizharo2023idba] introduces an approach based on A\*-search with *motion primitives*, i.e., short and locally optimal trajectories, that are connected not necessarily exactly, but allowing for a bounded discontinuity between primitives. These discontinuities between the motion primitives are later rectified using trajectory optimization (TO). By iteratively combining optimization and search with an increasing number of motion primitives and a reduced discontinuity bound, this method achieves asymptotically optimal motion planning and outperforms state-of-the-art methods across various robotic systems. A primary limitation of iDb-A\* is its inefficiency in finding an initial solution, particularly in large environments, where the time required to find the initial solution remains high.

In this paper, we combine the strengths of the exploration of RRT with the concept of discontinuities between motion primitives and trajectory optimization. We present iDb-RRT ([i]{.underline}terative [D]{.underline}iscontinuity-[b]{.underline}ounded RRT), a new kinodynamic motion planning algorithm that builds on the ideas of allowing discontinuities in an initial motion from iDb-A\*, and integrates the RRT exploration strategy with short motion primitives and trajectory optimization. iDb-RRT samples a random configuration, then expands the configuration that is closest using applicable motion primitives with bounded discontinuity. Once a solution is found, we employ trajectory optimization to correct the discontinuities between motion primitives. By incrementally increasing the number of primitives and reducing the allowed discontinuity, our algorithm achieves probabilistic completeness.

We analyze both a forward and a bidirectional version of iDb-RRT. In the open-source benchmark *Dynobench* comprising 30 problems across 8 different systems, iDb-RRT significantly outperforms state-of-the-art methods in initial solution time, especially in complex scenarios requiring long-horizon planning or navigating through narrow passages.

# Related Work

In this section, we discuss previous work on RRTs for kinodynamic motion planning and methods combining sampling and optimization. A more comprehensive review of methods in kinodynamic motion planning can be found in [@ortizharo2023idba; @masoud2010kinodynamic].

Sampling-based methods often grow the search tree towards a randomly sampled configuration by solving two-point boundary value problems [@kinodynamicRRT] to connect two states precisely, or by propagating random control inputs [@shomeAsymptoticallyOptimalKinodynamic2021b]. Previous work has focused on improving the expansion step (also called steering function) for specific systems [@webb2012kinodynamic; @LQR-RRTstar; @goretkin2013optimal], better exploration by most informative sampling [@SSTstar; @tang2020vector], better heuristics [@wang2022efficient], better integration of nonlinear solvers as a subroutine in sampling-based planners [@RABITstar; @stoneman2014embedding], or using motion primitives [@sakcakSamplingbasedOptimalKinodynamic2019] in a discretized configuration space. Compared to the previously discussed methods, our approach plans with the full dynamics (with bounded discontinuity), does not require discretization of the workspace, and does not require solving two-point boundary value problems in the RRT expansion step. This is enabled by leveraging precomputed motion primitives and allowing discontinuities in the planning stage, which are later fixed using trajectory optimization (TO).

Leveraging TO is a common approach for both geometric [@kamat2022bitkomo; @RABITstar] and kinodynamic motion planning, e.g., as a final post-processing step to improve cost and smoothness [@ravankar2018path].

In kinodynamic planning, previous work often involves planning using a simplified geometric model [@bortoff2000path; @allen2019real; @leu2022long] and tracking the resulting reference using trajectory optimization or an optimization-based controller. This approach is commonly used in high-dimensional systems, e.g., [@bry2015aggressive; @wahba2023kinodynamic] for UAVs or [@jelavic2023lstp; @bellicoso2018dynamic] for legged robots. Unfortunately, initially using a simplified model and accounting for the full dynamics later is limiting and might lead to infeasible optimization problems if the initial guess is not close to a dynamically feasible trajectory [@li2021model].

We also use TO for computing the final feasible trajectory, but we plan with the full dynamics (with bounded discontinuity). As this discontinuity can be made arbitrarily low, and optimization and search are combined iteratively, iDb-RRT is probabilistically complete under mild assumptions.

# Problem Definition

We consider a robot with a continuous state $\mathbf{x}\in \mathcal{X}$ (e.g., $\mathcal{X}\subseteq \mathbb{R}^{d_x}$) and a control vector $\mathbf{u}\in \mathcal{U}\subset \mathbb{R}^{d_u}$. The dynamics of the robot are deterministic, described by a differential equation, $$\begin{equation}
 \dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{u}).
    \label{eq:dynamics}
\end{equation}$$ To employ gradient-based optimization, we assume that we can compute the Jacobian of $\mathbf{f}$ with respect to $\mathbf{x}$ and $\mathbf{u}$, typically available in systems studied in kinodynamic motion planning, such as mobile robots or rigid-body articulated systems. We use $\mathcal{X}_{\text{free}} \subseteq \mathcal{X}$ to denote the collision-free space, i.e., the subset of states that are not in collision with the obstacles in the environment.

We discretize the dynamics [\[eq:dynamics\]](#eq:dynamics){reference-type="eqref" reference="eq:dynamics"} with a zero-order hold, i.e., we assume the applied control is constant during a time step of duration $\Delta t$. The discretized dynamics can then be written as, $$\begin{equation}
 \label{eq:dynamics_discrete} \mathbf{x}_{k+1} \approx \text{step}(\mathbf{x}_k, \mathbf{u}_k) \equiv \mathbf{x}_k + \mathbf{f}(\mathbf{x}_k, \mathbf{u}_k)\Delta t \,,
\end{equation}$$ using a small $\Delta t$ to ensure the accuracy of the Euler approximation. We use $K \in \mathbb{N}$ to denote the number of time steps (which is not fixed but subject to optimization), $\mathbf{X}= \langle \mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_K \rangle$ to denote the sequence of states sampled at times $0, \Delta t, \dots, K\Delta t$ and $\mathbf{U}= \langle \mathbf{u}_0, \mathbf{u}_1, \ldots, \mathbf{u}_{K-1} \rangle$ to denote the sequence of controls applied to the system for the time frames $[0,\Delta t), [\Delta t, 2\Delta t), \ldots, [(K-1)\Delta t, K\Delta t)$. The objective of navigating the robot from its start state $\mathbf{x}_s$ to a goal state $\mathbf{x}_g$ can then be framed as the search problem, $$\label{eq:motion-planning} \begin{align}                               & \text{find } {\mathbf{U},\mathbf{X},K} \label{eq:j}                                                                      \\ \text{s.t.
                                          } & \mathbf{x}_{k+1} = \text{step}(\mathbf{x}_k, \mathbf{u}_k)                     & \forall k \in \{0,\ldots,K-1\} \label{eq:step} \,, \\
                                            & \mathbf{u}_k \in \mathcal{U}& \forall k \in \{0,\ldots,K-1\} \label{eq:u} \,,    \\
                                            & \mathbf{x}_k \in \mathcal{X}_{\text{free}} \subseteq \mathcal{X}& \forall k \in \{0,\ldots,K\} \label{eq:x} \,,      \\
                                            & \mathbf{x}_0 = \mathbf{x}_s; \,\, \mathbf{x}_K = \mathbf{x}_g \label{eq:terminal} \,.
    \end{align}$$

In this paper we focus on finding a valid trajectory quickly (i.e, very little compute time), as opposed to finding the optimal solution. Although there is no explicit minimization of a cost function in our algorithms, we can evaluate the cost of the trajectory a posteriori. We use the cost term $J(\mathbf{U},\mathbf{X}) = \sum_{k=0}^{K-1} j(\mathbf{u}_k,\mathbf{x}_k)\, \Delta t$, with $j(\mathbf{u}_k,\mathbf{x}_k) = 1$ for minimal time (span) (alternatively, one might use $j(\mathbf{u}_k,\mathbf{x}_k) = \|\mathbf{u}_k\|^2$ for minimal control effort). We assume the dynamics function $\text{step}(\mathbf{x},\mathbf{u})$, control space $\mathcal{U}$, state space $\mathcal{X}$, and cost function $j(\mathbf{x},\mathbf{u})$, are known before solving the problem, which allows us to precompute motion primitives.

# iDb-RRT

## Background

Our approach relies on two concepts, that we now define.

::: {#def:discontinuity-bounded-solution .definition}
**Definition 1** (Discontinuity Bounded Solution). *A trajectory $\mathbf{X}= (\mathbf{x}_0, \ldots ,\mathbf{x}_K) , \mathbf{U}= (\mathbf{u}_0, \ldots, \mathbf{u}_{K-1})$ is a $\delta$-discontinuity bounded solution of the kinodynamic motion planning problem [\[eq:motion-planning\]](#eq:motion-planning){reference-type="ref+label" reference="eq:motion-planning"} if: $d(\mathbf{x}_{k+1}, \text{step}(\mathbf{x}_k, \mathbf{u}_k)) \leq \delta$, $d(\mathbf{x}_{0}, \mathbf{x}_s) \leq \delta$, $d(\mathbf{x}_{K}, \mathbf{x}_g) \leq \delta$, $\mathbf{x}_k \in \mathcal{X}_{\text{free}}$ and $\mathbf{u}_k \in \mathcal{U}$, where $d(\cdot,\cdot)$ is a distance function, e.g., a weighted Euclidean norm, and $\delta \ge 0$.*
:::

The search step of our algorithm, Db-RRT, generates solutions that are discontinuity bounded, while the trajectory optimization step rectifies these solutions to satisfy [\[eq:motion-planning\]](#eq:motion-planning){reference-type="ref+label" reference="eq:motion-planning"}.

::: {#def:motion-primitive .definition}
**Definition 2** (Motion Primitive). *A motion primitive $m = (\mathbf{X}, \mathbf{U}, \mathbf{x}_s, \mathbf{x}_f, c)$ is a sequence of states $\mathbf{X}= (\mathbf{x}_0, \ldots ,\mathbf{x}_N)$, $\mathbf{x}_k \in \mathcal{X}$, and controls $\mathbf{U}= (\mathbf{u}_0, \ldots, \mathbf{u}_{N-1})$, $\mathbf{u}_k \in \mathcal{U}$ that fulfill the dynamics $\mathbf{x}_{k+1} = \mathop{\mathrm{step}}(\mathbf{x}_k,\mathbf{u}_k)$. It connects the start state $\mathbf{x}_s = \mathbf{x}_0$ and the final state $\mathbf{x}_f = \mathbf{x}_N$, with a corresponding cost $c \in \mathbb{R}^+$. The length of the motion primitive (i.e., the number of states and controls) is randomized.*
:::

A large set of motion primitives can be generated offline by sampling random start and goal states, and attempting to connect them using nonlinear trajectory optimization algorithms. This results in a superior distribution of primitives in terms of coverage of the state space, compared to propagating random control inputs, and it guarantees asymptotic coverage of the state space [@ortizharo2023idba]. Importantly, we can later use known properties of the system to adapt primitives on-the-fly to match a state during the search, e.g., by using translation invariance of mobile robots, we can *translate* a primitive to match the position components of the state space [@ortizharo2023idba]. [1](#fig:primitives){reference-type="ref+label" reference="fig:primitives"} displays four motion primitives in the system *planar rotor* and how they can be connected with a bounded discontinuity.

:::: {#fig:primitives .figure}
![image](OrtizHaro2024iDbRRT_figs/plot2_v2.png){width=".4\\textwidth"} ![image](OrtizHaro2024iDbRRT_figs/plot_v2.png){width=".3\\textwidth"}

::: caption
*Top*: Four motion primitives in the system *Planar rotor*. The initial state (green), final state (red) and duration are randomized. *Bottom*: During the search step (Db-RRT), motion primitives are connected allowing for a bounded discontinuity. In this visualization, we connect these four motion primitives from left to right. The green and red configurations indicate the first and last configurations of each primitive. Note that their rotation component does not match exactly (further, discontinuities in the velocity components are not shown).
:::
::::

## Overview

Our approach is summarized in [\[alg:overview\]](#alg:overview){reference-type="ref+label" reference="alg:overview"}. We assume that a large set of motion primitives $\mathcal{M}_{\mathrm{L}}$ has been precomputed and is available before planning. iDb-RRT iteratively runs two steps until the first valid solution is found:

- An RRT search algorithm that connects motion primitives with bounded discontinuity, called Db-RRT. The output is a discontinuity bounded solution, i.e., a collision-free trajectory with bounded violation of dynamic constraints ([1](#def:discontinuity-bounded-solution){reference-type="ref+label" reference="def:discontinuity-bounded-solution"}).

- Gradient-based trajectory optimization, which attempts to repair the discontinuities between the motion primitives to produce a dynamically feasible trajectory.

If the search fails to find a solution within a given timeout (TerminateCondition), we increase the number of available motion primitives. If gradient-based optimization fails, we reduce the allowed discontinuity. In practice, we typically require only one or two outer iterations (that is, a call to the search and optimization algorithms) to find a solution. We decrease the allowed discontinuity following a geometric sequence, $d_i = d_{i-1} \cdot d_r$ with a fixed rate $d_r<1$, and increase the number of primitives also following a geometric sequence $m_i = m_{i-1} \cdot m_r$ with a fixed rate $m_r>1$.

::: algorithm
[]{#alg:overview label="alg:overview"} $\delta \leftarrow \delta_0$ $\mathcal{M}\leftarrow \ChoosePrimitives(\mathcal{M}_{\mathrm{L}})$
:::

## Db-RRT: RRT with Motion Primitives

Db-RRT is an RRT algorithm that connects motion primitives with bounded discontinuity, following the general RRT algorithm to choose the next state to expand. This approach provides a Voronoi bias (i.e., nodes at the frontier of the search tree are more likely to get expanded), thus rapidly exploring the feasible state space. In [\[alg:rrt\]](#alg:rrt){reference-type="ref+label" reference="alg:rrt"}, we describe our Db-RRT algorithm and highlight our modifications from RRT. In Db-RRT, the expansion operation is performed using motion primitives with bounded discontinuity. Given the state $\mathbf{x}_{\text{near}}$, we assess which primitives are applicable (e.g., [\[alg:db-rrt-focused:expand\]](#alg:db-rrt-focused:expand){reference-type="ref+label" reference="alg:db-rrt-focused:expand"} in [\[alg:rrt-togoal\]](#alg:rrt-togoal){reference-type="ref+label" reference="alg:rrt-togoal"}). We then differentiate between focused expansion ( [\[alg:rrt-togoal\]](#alg:rrt-togoal){reference-type="ref+label" reference="alg:rrt-togoal"}), where we select the primitive that brings us closest to $\mathbf{x}_{\text{rand}}$ from a finite number of nearby candidates, and uninformed expansion ( [\[alg:rrt-torand\]](#alg:rrt-torand){reference-type="ref+label" reference="alg:rrt-torand"}), where we choose one collision-free primitive at random. With a small probability (the so-called goal bias), we expand towards the goal state instead of a random state.

We stop when we find a state that is within a distance lower than $\delta$ of the goal state. Further, the value of $\delta$ is also used to avoid creating nodes in the tree that are too close to previously discovered nodes.

Both expansion strategies are guaranteed to find a solution, if one exists, given sufficient compute time. The inherent trade-off is that [\[alg:rrt-togoal\]](#alg:rrt-togoal){reference-type="ref+label" reference="alg:rrt-togoal"} requires more compute time, as it involves evaluating collisions for multiple motion primitives, but it provides a more focused and uniform expansion. In our implementation, we utilize [\[alg:rrt-togoal\]](#alg:rrt-togoal){reference-type="ref+label" reference="alg:rrt-togoal"} for expansions towards the goal and [\[alg:rrt-torand\]](#alg:rrt-torand){reference-type="ref+label" reference="alg:rrt-torand"} for expansions towards random nodes, but any combination of these two approaches is valid. Focused and uninformed expansion are analogous to guided Monte-Carlo and Monte-Carlo propagation in classic RRT literature, but in Db-RRT we use motion primitives instead of randomly sampled controls.

::: algorithm
[]{#alg:rrt label="alg:rrt"}

$\mathcal{T} \leftarrow \AddNode(\mathbf{x}_s)$
:::

## Db-RRT-Connect and other Db-RRT variants

The expansion step of Db-RRT ( [\[alg:rrt-togoal,alg:rrt-torand\]](#alg:rrt-togoal,alg:rrt-torand){reference-type="ref+label" reference="alg:rrt-togoal,alg:rrt-torand"}) can be integrated with many of the variations and enhancements of RRT that have been previously proposed,

#### Backward and Bidirectional Search

Inspired by RRT-Connect [@kuffner2000rrt], we present a bidirectional variant of Db-RRT, where we grow two trees, one from the start (using standard motion primitives) and one from the goal (using reversed motion primitives), and attempt to connect them. The expansion step in a backward search mirrors that of a forward search but requires reversing the order of states and controls in the motion primitives beforehand. The two trees are connected if two of their states are within the discontinuity bound.

#### Asymptotically Optimal Algorithms

Db-RRT can also be applied to RRT variants that require connecting two states precisely, instead of only expanding the state towards random targets. The discontinuity bound $\delta$ can be leveraged to consider two states as equivalent---thereby enabling their exact connection in any rewiring step, such as in RRT\* [@karaman2011sampling]. Such rewiring steps, which are essential for the asymptotic optimality of RRT\* and its variants, are already implemented in iDb-A\* [@ortizharo2023idba].

::: algorithm
$\mathcal{M}_c \gets \texttt{NearestR}(\mathbf{x}_o, \mathcal{M}, \delta)$ []{#alg:db-rrt-focused:expand label="alg:db-rrt-focused:expand"}

$m_{\text{b}}  = NULL , \quad d_{\text{b}} = \infty$

$NULL, NULL$
:::

::: algorithm
$\mathcal{M}_c \gets \texttt{NearestR}(\mathbf{x}_o, \mathcal{M}, \delta)$

$NULL, NULL$
:::

## Trajectory Optimization

The output of Db-RRT is a sequence of states and controls that connects the start and goal states with a bounded discontinuity, see [1](#def:discontinuity-bounded-solution){reference-type="ref+label" reference="def:discontinuity-bounded-solution"}. In the optimization step of iDb-RRT, we employ nonlinear trajectory optimization to repair the discontinuity between the motion primitives and to obtain a feasible and locally optimal trajectory.

For gradient-based trajectory optimization, we require the gradients of the dynamics and the cost function with respect to the states and controls. These can be easily obtained for most robotics systems using finite differences, analytic expressions, or a differentiable simulator. Instead of the binary collision check in Db-RRT, we now use a signed distance function.

In the trajectory optimization step, the number of time steps $K$ is fixed by the output of Db-RRT. If desired, we can also optimize the duration of the trajectory by including the length of the time interval in the optimization problem or using other techniques, as explored in [@ortizharo2023idba]. Because our goal is to find a valid trajectory quickly, we choose not to include the time interval as an optimization variable. This choice is supported by the fact that trajectories from RRT-like algorithms tend to be suboptimal, where the time duration of the initial guess is often sufficient to reach the goal.

To solve the trajectory optimization problem, we use the Differential Dynamic Programming (DDP) algorithm, which is a second-order method for solving optimal control problems of the form Eq. [\[eq:ddp\]](#eq:ddp){reference-type="eqref" reference="eq:ddp"}. Collision and goal constraints, and state and control bounds of the original kinodynamic motion planning problem are added to the cost [\[eq:trajectory-optimization\]](#eq:trajectory-optimization){reference-type="eqref" reference="eq:trajectory-optimization"} with a squared penalty method and a max activation function for inequalities. Further, we include small regularization terms on the control effort and the acceleration of the system to improve convergence. $$\begin{align} \min_{ \mathbf{X}, \mathbf{U}} & \sum_{k=0}^{K-1} c(\mathbf{x}_k,\mathbf{u}_k) + c_K(\mathbf{x}_K)\,, \label{eq:trajectory-optimization} \\ \text{s.t.
                  %
              } \quad               & \mathbf{x}_{k+1} = \text{step}(\mathbf{x}_{k},\mathbf{u}_k) \quad \forall k \in \{0,\ldots,K-1\}\,,     \\
                                    & \mathbf{x}_0 = \mathbf{x}_s\,.
    \end{align}
 \label{eq:ddp}$$ In particular, we use the optimization algorithm *Feasibility-driven DDP* [@Crocoddyl], which can be warm-started with an infeasible sequence of states and controls, providing a good balance between local convergence and globalization.

## Analysis

The RRT algorithm is probabilistically complete [@kinodynamicRRT; @kleinbortProbabilisticCompletenessRRT2019a], that is, the probability of eventually finding a solution, if one exists, converges to one. The proof assumes that the planning problem is $\delta_1$-robust (informally: the solution should not require traversing a \"gap\" smaller than $\delta_1$) and that the dynamics are Lipschitz continuous. Formally, it uses an inductive argument over overlapping balls that cover the solution trajectory, demonstrating that the probability of finding an edge between neighboring balls is non-zero.

We first consider Db-RRT ([\[alg:rrt\]](#alg:rrt){reference-type="ref+label" reference="alg:rrt"}) with the precondition that we have a sufficiently large set of motion primitives $\mathcal{M}_{\mathrm{L}}$ and a discontinuity bound $\delta < \delta_1$. Then, the additional if-condition in [\[alg:rrt:change2\]](#alg:rrt:change2){reference-type="ref+label" reference="alg:rrt:change2"} does not prevent finding a solution. [\[alg:rrt:change1\]](#alg:rrt:change1){reference-type="ref+Label" reference="alg:rrt:change1"} changes the distribution for the expansion operation but continues to assign a positive probability density to all successors for large sets of randomly generated $\mathcal{M}_{\mathrm{L}}$. Next, we consider iDb-RRT ([\[alg:overview\]](#alg:overview){reference-type="ref+label" reference="alg:overview"}). If Db-RRT fails to find a solution because at least one precondition is violated (a large $\mathcal{M}_{\mathrm{L}}$ and $\delta < \delta_1$), we adjust both parameters and repeat (), yielding a non-zero probability of executing Db-RRT with parameters that fulfill our assumptions. Finally, we assume that there exists a $\delta$ such that if Db-RRT generates a $\delta$-discontinuity bounded solution, the trajectory optimization algorithm will converge with a non-zero probability, which makes our algorithm, iDb-RRT, probabilistically complete.

In practice, we demonstrate that we can use a large discontinuity $\delta$ and a small number of primitives to efficiently find solutions to a wide range of problems.

# Experiments

We evaluate iDb-RRT on 30 problems that include 8 different dynamical systems in various environments. The first 16 problems are inspired by previous work on kinodynamic motion planning [@SSTstar; @shomeAsymptoticallyOptimalKinodynamic2021b; @hoenig2022benchmarking; @granados2022towards] (*selected problems* in [@ortizharo2023idba], first 16 rows in [\[tab:all\]](#tab:all){reference-type="ref+label" reference="tab:all"}). Furthermore, we include 14 additional problems with the same dynamical systems but in larger, more complex environments with more obstacles, which require longer trajectories (last 14 rows in [\[tab:all\]](#tab:all){reference-type="ref+label" reference="tab:all"}).

All benchmark problems are available in *Dynobench*. It provides a C++ implementation of the dynamical systems (dynamics with analytical Jacobians, state, and bound constraints), collision and signed distance function (based on the Flexible Collision Library, FCL), the environments (in human-friendly YAML files), and visualization tools.

Implementations of iDb-RRT and the other planners are available in *Dynoplan*, including the motion primitives and instructions to replicate the benchmark results. Visualizations of the problems and examples of solution trajectories computed by our algorithm are available on our website.

## Dynamical Systems

:::: {#fig:newproblems .figure}
  --------------------------------------------------------------------- --------------------------------------------------------------------- --------------------------------------------------------------------- --------------------------------------------------------------------- ---------------------------------------------------------------------
   ![image](OrtizHaro2024iDbRRT_figs/jue_29_feb_2024_15--49--15_EST.png){width="12%"}   ![image](OrtizHaro2024iDbRRT_figs/jue_29_feb_2024_15--46--37_EST.png){width="18%"}   ![image](OrtizHaro2024iDbRRT_figs/jue_29_feb_2024_15--55--37_EST.png){width="18%"}   ![image](OrtizHaro2024iDbRRT_figs/jue_29_feb_2024_16--18--46_EST.png){width="18%"}   ![image](OrtizHaro2024iDbRRT_figs/jue_29_feb_2024_16--21--33_EST.png){width="18%"}
                                   (a)                                                                   (b)                                                                   (c)                                                                   (d)                                                                   (e)
  --------------------------------------------------------------------- --------------------------------------------------------------------- --------------------------------------------------------------------- --------------------------------------------------------------------- ---------------------------------------------------------------------

::: caption
Five kinodynamic motion planning problems in our benchmark *Dynobench*, with a solution found by `iDb-RRT-C`. (a) *Rotor Pole - Up obstacles 2* (b) *Unicycle 2 - Narrow passage* (c) *Car with Trailer - Double bugtrap* (d) *Quadrotor v0 - Recovery obstacles 2* (e) *Quadrotor v1 - Double window*.
:::
::::

We include a diverse range of dynamical systems and environments, featuring varying state dimensionality (from 3 to 14), the number of underactuated degrees of freedom, and controllability. All systems use explicit Euler integration [\[eq:dynamics_discrete\]](#eq:dynamics_discrete){reference-type="eqref" reference="eq:dynamics_discrete"}, with $\Delta t=\SI{0.1}{s}$ for all car-like robots and $\Delta t=\SI{0.01}{s}$ for the flying robots and the *Acrobot*.

The 8 systems are (see [@ortizharo2023idba] for a detailed explanation): *Unicycle 1 ($1^{\text{st}}$ order)*: 3-dimensional state space and 2-dimensional control space. *Unicycle 2 ($2^{\text{nd}}$ order)*: 5-dimensional state space and 2-dimensional acceleration control. *Car with trailer*: 4-dimensional state space and a 2-dimensional control space, *Acrobot*: 4-dimensional state space and 1-dimensional control space. *Quadrotor v0*: 13-dimensional state space and a 4-dimensional control space (force for each of the four motors)[^4]. *Quadrotor v1*: The state space is the same as in *Quadrotor v0*, but controls are now the total thrust and torques in the body frame. *Planar rotor*: 6-dimensional state space and 2-dimensional control space, also with 1.3 thrust-to-weight ratio. *Rotor pole*: 2-dimensional control space and 8-dimensional state space.

## Metrics

Each experiment is run 20 times with different random seeds on a desktop computer[^5], single-core. We report:

- $t [s]$: Compute time to get the first solution (median).

- $c [s]$: Cost of the first solution. As a cost, we use the duration of the found trajectory, in seconds (median).

If all the runs of an algorithm fail to find a solution before the timeout of 60 s, we use a dash ('-') in the table. If less than 50% of the runs find a solution, we report the best value but add an asterisk ('\*') to indicate a low success rate.

## Algorithms

We analyze two variants of the iDb-RRT family ( [\[alg:overview\]](#alg:overview){reference-type="ref+label" reference="alg:overview"}):

- `iDb-RRT-F`: using a forward Db-RRT ( [\[alg:rrt\]](#alg:rrt){reference-type="ref+label" reference="alg:rrt"}).

- `iDb-RRT-C`: using a bidirectional Db-RRT inspired by RRT-Connect.

We compare our algorithms against state-of-the-art methods that use optimization, search, and sampling, and have available open-source implementations.

$\bullet$ For a sampling-based approach, we use the kinodynamic version of RRT implemented in OMPL [@OMPL] (Open Motion Planning Library), which uses the propagation of random control inputs to grow the search tree. Since sampling-based kinodynamic approaches cannot reach a goal state exactly, we use a goal region using the same value of $\delta$ used in iDb-A\* and iDb-RRT. We denote this algorithm as `Kino-RRT`.

$\bullet$ For optimization-based planning, we choose a standard combination of a geometric motion planner and a trajectory optimizer, which we denote as `Geo-RRT-TO` . Specifically, we use a *geometric* RRT (using the implementation in OMPL) to plan using only the position and orientation of the system, without considering velocity and dynamics. The trajectory optimizer (also based on Feasibility-driven DDP [@Crocoddyl], see [@ortizharo2023idba] for details) is warm-started with the geometric guess. If trajectory optimization fails, we run RRT again from scratch and repeat.

$\bullet$ `iDb-A*` is a hybrid method that integrates search with motion primitives and trajectory optimization, but uses incremental A\*-searches instead of RRT. Notably, `iDb-A*` has been designed to combine asymptotic optimality with good anytime behavior, as it starts with a small number of motion primitives and incrementally increases the number of available motion primitives during each A\*-search. We terminate the algorithm once the first solution is found.

In all algorithms, all hyperparameters are chosen per dynamical system.

## Results -- Comparison with Baselines

::: table*
+-----------------------------------+---------------------+------------------------+-----------------------+------------------------+---------------------+
| Problem                           | iDb-RRT-F           | iDb-RRT-C              | Geo-RRT-TO            | iDb-A\*                | Kino-RRT            |
+:==================================+:=========:+:=======:+:=========:+:==========:+:=========:+:=========:+:=========:+:==========:+:=========:+:=======:+
| 2-3(lr)4-5(lr)6-7(lr)8-9(lr)10-11 | t \[s\]   | c \[s\] | t \[s\]   | c \[s\]    | t \[s\]   | c \[s\]   | t \[s\]   | c \[s\]    | t \[s\]   | c \[s\] |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Acrobot/Swing up                  | 0.35      | 5.39    | **0.25**  | 5.95       | 0.82      | **4.21**  | 1.49      | 5.53       | 0.32      | 6.83    |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Acrobot/Swing up obstacles v1     | 0.36      | 5.37    | **0.18**  | **4.86**   | 0.80      | 5.06      | 1.92      | 5.80       | 0.38      | 6.19    |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Car with trailer/Kink             | 0.23      | 53.05   | 0.24      | 60.85      | 0.59      | 34.45     | 1.29      | **31.10**  | **0.20**  | 68.50   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Car with trailer/Park             | 0.10      | 10.85   | **0.05**  | 14.00      | 0.10      | **5.05**  | 0.11      | 17.90      | **0.05**  | 8.15    |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Planar rotor/Hole                 | **0.56**  | 8.88    | 1.00      | 10.93      | 8.63      | 5.47      | 11.77     | **3.49**   | 3.04\*    | 5.99\*  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Planar rotor/Bugtrap              | 1.44      | 9.97    | **1.04**  | 10.48      | 0.46\*    | 7.84\*    | 12.79     | **5.17**   | 39.23     | 10.55   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Rotor pole/Swing up obstacles     | 1.91      | 8.20    | **1.14**  | 8.38       | 10.70     | 6.09      | 2.96      | **3.98**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Rotor pole/Small window           | 3.84      | 9.43    | **1.14**  | 9.30       | 6.21\*    | 2.99\*    | 4.39      | **4.54**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v0/Recovery             | 0.83      | 5.61    | **0.71**  | 5.25       | 1.12      | **2.53**  | 1.32      | 5.57       | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v0/Recovery obstacles   | 1.29      | 6.41    | 1.37      | 6.20       | **0.71**  | **3.90**  | 1.53      | 5.72       | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v1/Obstacle             | 0.87      | 6.00    | 1.36      | 7.03       | **0.25**  | **2.72**  | 2.53      | 4.54       | 40.68\*   | 4.90\*  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v1/Window               | **0.61**  | 5.22    | 0.88      | 7.99       | 9.05      | 5.53      | 1.64      | **3.71**   | 9.83\*    | 10.08\* |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 1 v0/Bugtrap             | 0.13      | 33.05   | **0.11**  | 30.45      | 0.40      | 40.35     | 0.52      | **22.20**  | 0.14      | 70.30   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 1 v2/Wall                | 0.09      | 30.70   | **0.04**  | 31.95      | 0.91      | 24.30     | 0.94      | **19.60**  | 0.24      | 49.45   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 2/Bugtrap                | 0.16      | 59.65   | **0.09**  | 56.35      | 0.61      | 43.50     | 1.65      | **25.30**  | 0.18      | 69.25   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 2/Park                   | 0.03      | 12.20   | **0.01**  | 9.85       | 0.12      | 6.15      | **0.01**  | **5.80**   | 0.05      | 13.20   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Car with trailer/Double bugtrap   | 0.70      | 93.90   | **0.65**  | 101.60     | 2.44\*    | 53.00\*   | 1.71      | **46.80**  | 3.63      | 96.65   |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Car with trailer/Narrow passage   | **0.57**  | 122.55  | 0.62      | 132.05     | 0.82\*    | 74.50\*   | 8.61      | **53.90**  | 2.33      | 136.25  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Planar rotor/Recovery obstacles 2 | **0.48**  | 10.75   | 0.52      | 10.95      | 6.54\*    | 8.94\*    | 20.39     | **6.04**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Planar rotor/Double bugtrap       | 1.97      | 14.05   | **1.84**  | **13.78**  | \-        | \-        | \-        | \-         | 19.49\*   | 10.30\* |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Rotor pole/Up obstacles 2         | 4.94      | 10.68   | **2.11**  | 12.15      | \-        | \-        | 14.80     | **5.00**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Rotor pole/Small window 2         | 3.87      | 11.59   | **1.87**  | 11.91      | 0.32\*    | 5.71\*    | 11.84     | **6.18**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v0/Double bugtrap 3D    | 5.80      | 11.87   | **4.43**  | 13.19      | \-        | \-        | 23.42     | **6.36**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v0/Recovery obstacles 2 | **2.50**  | 9.74    | 2.58      | 10.26      | 0.33\*    | 3.90\*    | 6.49      | **6.41**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v1/Recovery obstacles 2 | 2.50      | 9.71    | **2.38**  | 9.68       | 0.30\*    | 3.72\*    | 59.71     | **6.23**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Quadrotor v1/Double Window        | **2.18**  | 7.79    | 2.54      | 10.86      | 0.42\*    | 4.62\*    | 25.74     | **5.09**   | \-        | \-      |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 1 v0/Double bugtrap      | 0.23      | 60.10   | 0.21      | 60.10      | 1.70      | 64.75     | 0.92      | **30.10**  | **0.17**  | 109.30  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 1 v0/Narrow passage      | 0.22      | 81.40   | **0.17**  | 90.35      | 1.14      | 83.90     | 1.88      | **37.30**  | 0.20      | 133.55  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 2/Double bugtrap         | 0.30      | 94.45   | 0.28      | 90.40      | 2.21      | 70.85     | 2.37      | **34.60**  | **0.25**  | 103.30  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
| Unicycle 2/Narrow passage         | 0.31      | 122.50  | **0.24**  | 118.20     | 1.11      | 84.30     | 7.30      | **42.70**  | 0.34      | 124.95  |
+-----------------------------------+-----------+---------+-----------+------------+-----------+-----------+-----------+------------+-----------+---------+
:::

Results are summarized in [\[tab:all\]](#tab:all){reference-type="ref+label" reference="tab:all"}. Due to space constraints, we report only the median of each metric. A graphical representation of these results using boxplots is available on our website. In general, we observe that `iDb-A*` has lower variance than `iDb-RRT`, `Kino-RRT`, and `Geo-RRT-TO`. `iDb-RRT-F` and `iDb-RRT-C` solve all problems with a success rate of 100% (except two problems each, where they achieve 80-90% success rate), outperforming all baseline algorithms in terms of compute time to generate a solution (e.g., `iDb-RRT-C` is the fastest in 19 problems, and `iDb-RRT-F` is the fastest in 6 problems).

- `Kino-RRT`: it finds a first solution in low-dimensional car-like systems in a competitive timeframe (but slower than `iDb-RRT-F` in 13 out of 19 cases) with a higher average cost. However, in agile systems (e.g., flying robots), propagation of random control inputs is very inefficient, and `Kino-RRT` fails to find a solution in 11 problems out of 30.

- `Geo-RRT-TO` often requires multiple runs of RRT to provide a suitable initial guess for trajectory optimization, and sometimes fails completely as the initial guesses never contain information about the dynamics of the system (solving only 18 out of 30 problems with a success rate above 50%). If the initial guess works for the optimizer, it can be very fast (`Geo-RRT-TO` is faster than `iDb-RRT-F` in 7 problems).

- `iDb-A*`: is the strongest baseline, with success rate of 100% in all problems except *Planar rotor/Double bugtrap*. However, `iDb-A*` is always outperformed in the time to find the first solution by `iDb-RRT-C`. The difference between `iDb-A*` and `iDb-RRT-C` increases in the new benchmark (last 14 problems), which require longer plans, with improvements up to 10-20x. On the other hand, the first solution found with `iDb-A*` has a better cost than any other algorithm in 23 cases.

## Discussion

#### Forward vs Bidirectional Search

Comparing our two variants, we observe that `iDb-RRT-C` is better in 21 out of 30 problems in terms of compute time. These results agree with previous experiments in the RRT literature, where RRT-Connect is generally faster than a forward search (in robotics problems, starting a search from the start and the goal is often beneficial because these configurations are often close to obstacles and narrow passages).

#### Number of primitives and discontinuity bound

Connecting primitives with discontinuities allows our algorithms to plan using a reduced number of primitives. As a reference, for the system *Unicycle 1 v0*, we use an initial set of 200 primitives and an initial discontinuity bound of 0.3. The discontinuity is computed with a weighted Euclidean norm (e.g., weight 1 for position and 0.5 for orientation); thus a $\delta$ of $0.3$ could represent up to 30 cm of discontinuity in position or 0.6 rad in orientation. Such discontinuities are large enough that the trajectory is not directly applicable to the real robot, but it can be efficiently repaired in the nonlinear trajectory optimization step of iDb-RRT. For the *Quadcopter v0*, we use 5000 primitives and a discontinuity bound of 0.35, and for the *Rotor pole*, we use 8000 motions and a discontinuity bound of 0.45. The time spent to generate one motion primitive (offline) ranges from 10ms for car-like robots to up to 5s for flying robots (most of the time is spent attempting to solve two-point boundary value problems that do not have a solution).

#### Analysis of compute time in iDb-RRT

In iDb-RRT, the time spent in trajectory optimization dominates the total compute time. For instance, the compute time required to optimize one trajectory in the new benchmark problems with flying robots is between 1s and 3s, while in car-like robots is between 50ms and 200ms. In addition, in the systems *Quadrotor v0* and *Quadrotor v1*, trajectory optimization may fail at the first attempt, and finding a feasible solution requires multiple iterations of iDb-RRT. For car-like systems, we can compute trajectories of duration up to 50s in less than 1s. For flying robots, we require between 0.5s and 4s to generate trajectories of duration up to 14s. A straightforward way to speed up the trajectory optimization step is to reduce the time discretization from 0.01s to 0.05s (with an expected 5x speedup).

#### RRT is easier to tune than incremental A\*

The running time of A\* with motion primitives in a continuous space is highly sensitive to the number of motion primitives, i.e., the discretization level. With too few primitives, the problem becomes unsolvable; with too many, the state space to be expanded becomes unmanageably large. Conversely, our iDb-RRT algorithms lack an explicit notion of a branching factor. As confirmed by our results, the RRT approach naturally adapts to efficiently solving both simple and complex problems alike, obviating the need for choosing a branching factor while also providing faster exploration.

#### Limitations and future work

The main limitation of iDb-RRT, similar to iDb-A, lies in its scalability to higher-dimensional systems. As the dimensionality increases, the number of motion primitives required to cover the state space with a small discontinuity grows exponentially. This issue can be partially mitigated by planning with larger discontinuities. In our benchmark, we successfully scaled to 13-DOF for the *Quadrotor* and 8-DOF for *Rotor pole*, thanks to leveraging translation invariance and the second-order linear velocity invariance of the dynamics. To effectively scale to higher dimensions, we see great potential in using function approximation to learn a more informative distance metric and to combine motion primitives with deep generative models or learned policies.

# Conclusion

We present iDb-RRT, a novel algorithm for kinodynamic motion planning that combines search and optimization within the framework of Rapidly-Exploring Random Trees (RRT). Our algorithm connects motion primitives with a bounded discontinuity as the expansion step of an RRT, which is later repaired using trajectory optimization. iDb-RRT is probabilistically complete and finds solutions faster than state-of-the-art kinodynamic motion planning across a diverse set of problems.

Comparatively, iDb-RRT and iDb-A\* possess complementary strengths: the former finds solutions significantly faster, while the latter converges to optimal solutions with more compute time. Together, they demonstrate that combining motion primitives, bounded discontinuity, and trajectory optimization, is a promising approach for both sampling-based and search-based motion planning.

[^1]: Website: <https://quimortiz.github.io/idbrrt/>

[^2]: Code is available at Dynoplan (<https://github.com/quimortiz/dynoplan>) and Dynobench (<https://github.com/quimortiz/dynobench>).

[^3]: $^{1}$Machines in Motion Laboratory, New York University, USA, $^{2}$TU Berlin, Germany, $^{3}$Computational Robotics Lab, ETH Zurich, CH. This work was in part supported by the National Science Foundation grants 1932187, 2026479, 2222815 and 2315396.

[^4]: We use the parameters of the Crazyflie 2.1, where the low thrust-to-weight ratio of 1.3 is very challenging for kinodynamic motion planning.

[^5]: Intel(R) Xeon(R) W-2145 CPU @ 3.70GHz
