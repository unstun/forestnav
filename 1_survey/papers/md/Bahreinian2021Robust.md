---
citation_key: Bahreinian2021Robust
arxiv_id: 2105.14118
arxiv_url: https://arxiv.org/abs/2105.14118
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:33:53Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

The problem of motion planning from an initial state toward a goal state has received great attention in mobile robotics. One of the currently most popular techniques for solving this problem is represented by sampling-based algorithms, where the planner is not given an explicit representation of the environment (e.g., via polygons), but instead uses a *sampling function* that can be used to query whether an arbitrary point is in free space or inside an obstacle. Together with a *steering function* that can find trajectories between samples, algorithms such as `RRT`$^*$ and derivatives build a *tree* that is rooted at the goal location and that extends toward every reachable point in the free space. When such tree arrives at a given starting location, a nominal feasible path can be found by tracing it back along the tree to the root. However, in practice, following this path requires full knowledge of the position in the environment and a lower-level control to compensate for disturbances. Additionally, although the sampling process naturally reveals information about the obstacles via sample collisions, such information is typically discarded after planning; relatedly, traditional approaches do not address the fact that there might be discrepancies between the implicit map given by the sampling function and the real free configuration space.

In this paper we take advantage of the capabilities of `RRT`$^*$-like algorithms to effectively represent the free configuration space, but augment it with linear output-feedback controllers that guide the state along the edges of the tree graph based on the observation of *landmarks*, points whose location is known in the map and that can be easily recognized (but can be generally distinct from the obstacles or generated samples). Our output-feedback controllers provide remedies to the three aforementioned shortcomings of traditional methods:

::: enumerate*
it enables us to simplify the tree representation (i.e., reduce the number of nodes) while also extending it to regions that were not explicitly sampled;

it steers clear of obstacles (within the resolution limits given by the finite sampling) by explicitly avoiding samples that were found in collision; and

it provides robustness to discrepancies in the map used for the planning that are reflected in the landmarks (if the actual landmark locations are somewhat different, the resulting control will change accordingly and without replanning).
:::

## Review of prior work

Sampling-based planning algorithms, such as Probabilistic Road Map [@kavraki1996probabilistic], Rapidly exploring Random Tree (`RRT`$^*$) [@rrt; @lavalle2001randomized] and asymptotically optimal Rapidly Exploring Random Tree (`RRT`$^*$), [@karaman2011sampling], have become popular in the last few years due to their good practical performance, and their probabilistic completeness [@lavalle2006planning; @lavalle2001randomized; @karaman2011sampling]. There have also been extensions considering perception uncertainty [@renganathan2020towards]. However, these algorithms only provide nominal paths, and assume that a separate low-level controller exists to generate collision-free trajectories at run time. For trajectory planning that takes into account non-trivial dynamical systems of the robot, kinodynamic `RRT`$^*$ [@lavalle2001randomized; @lavalle2006planning] and closed-loop `RRT`$^*$ (`CL-RRT`, [@kuwata2008motion]) and `CL-RRT#` grow the tree by sampling control inputs and then propagating forward the nonlinear dynamics (with the optional use of stabilizing controllers and tree rewiring to approach optimality). Further in this line of work, there has been a relatively smaller amount of works on algorithms that focus on producing controllers as opposed to simple reference trajectories. The `safeRRT` algorithm [@positiveInvariant; @weiss2017motion] generates a closed-loop trajectory from an initial state to the desired goal by expanding a tree of local state-feedback controllers to maximize the volume of corresponding positive invariant sets while satisfying the input and output constraints. Based on the same idea and following the `RRT`$^*$ approach, the `LQR-tree` algorithm [@tedrake2009lqr] creates a tree by sampling over state space and stabilizes the tree with a linear quadratic regulator (LQR) feedback. With respect to the present paper, the common trait among all these works is the use of full state feedback (as opposed to output feedback).

Separately, the state-of-the-art method for synthesizing safe and stable control commands is represented by the combination of Control Barrier Functions (CBF) and Control Lyapunov Function (CLF) [@ames2014control; @hsu2015control; @borrmann2015control]; however, these approaches are in general not complete for complex environments (i.e., they might fail to reach the goal even when a feasible path exists).

In our algorithm, we use the min-max robust Linear Programming (LP) controller synthesis method from [@Mahroo]. However, that work assumes that a polyhedral convex cell decomposition of the environment is available, which greatly reduces the applicability of that method. Moreover, that work also does not test the resulting controllers in a real experimental setting.

## Proposed approach and contributions

As mentioned above, at a high level, our approach first converts an implicit representation of the environment to a simplified tree graph via sampling, and then builds a sequence of linear output feedback controllers to generate piece-wise linear control laws for navigation. To build the tree, we use the `RRT`$^*$ algorithm with two modifications:

::: enumerate*
we post-process the tree to minimize the number of nodes and decrease the overall path length of each branch, and

we do not discard the samples that are found to be in collision with obstacles.
:::

In addition to the sample-based tree and collision samples, we assume that the environment includes a set of landmarks that the robot can sense, such that for any location in the free space at least one landmark is available (in practice, these landmarks could correspond to visual features on the surface of obstacles, although we do not place any restriction on their location).

We then propose a way to define convex cells around each node in the tree that ensure progress from that node to its parent via a CLF constraint, while using the samples found in collision to form a local convex approximation of the free space for obstacle avoidance via CBF constraints. We apply the method of [@Mahroo] to formulate a min-max robust Linear Program that synthesizes a controller for each cell which takes as inputs relative position measurements of the landmarks and outputs a control signal that respects and balances the stability constraint from the CLF, and the safety (collision avoidance) constraints from the CBF. Additionally, we show how to easily recompute the controllers (online) to handle the case where subsets of landmarks are not visible (e.g., due to the the camera's limited field of view). To summarize, the main contributions of this work are:

- Integrate high-level `RRT`$^*$ path planning, with low-level CLF-CBF LP control synthesis, thus allowing the method of [@Mahroo] to be applied to general environments for which a cell decomposition is not available;

- Introduce a new algorithm to simplify and improve a tree generated by `RRT`$^*$ algorithm with a finite number of samples (which, in general, is not optimal).

- Introduce a new method to reformulate the controller to navigate with a limited field of view.

- Obtain a method that, thanks to the use of visual features of the environment (landmarks) and output feedback controllers, automatically adapts `RRT`$^*$ solutions to deformations of the environment and deviations from the nominal path without replanning;

- Implement the proposed algorithm in a real-world environment to validate the performance of our algorithm.

# BACKGROUND {#sec:background}

In this section, we review the CLF and CBF constraints, and the `RRT`$^*$ method in the context of our proposed work.

## System Dynamics

We assume that the robot has control-affine dynamics of the form $$\begin{equation}
\label{sys1}
  \dot{x}=Ax+Bu,
\end{equation}$$ where $x \in \mathcal{X}\subset\mathbb{R}^{n}{}$ denotes the state, $u\in\mathcal{U}\subset\mathbb{R}^{m}{}{}$ is the system input, and $A\in\mathbb{R}^{n\times n}{}$, $B\in\mathbb{R}^{n\times m}{}$ define the linear dynamics of the system. We assume that the pair $(A,B)$ is controllable, and that $\mathcal{X}_i$ and $\mathcal{U}$ are polytopic, $$\begin{align}
\label{state_limits}
  \mathcal{X}=\{x\mid A_{x}x\leq b_{x}\},&& \mathcal{U}=\{u\mid A_{u}u\leq b_u\},
\end{align}$$ Note that, in our case, $\mathcal{X}$ will be a convex cell centered around a sample in the tree (Section [2.5](#sec:environment){reference-type="ref" reference="sec:environment"}).

## Tree graphs

A graph is a tuple $(\mathcal{V},\mathcal{E})$ where $\mathcal{V}$ represents a set of nodes and $\mathcal{E}$ represents a set of edges. If $(i,j)\in \mathcal{E}$, we say that $j$ is the parent of node $j$. An oriented tree $\mathcal{T}$ is a graph where each node has exactly one parent, except for the *root*, which has no parents. We refer to nodes without children as *leaves*.

## Optimal Rapidly-Exploring Random Tree (`RRT`$^*$) {#sec:rrtstar}

In this section we review `RRT`$^*$, an algorithm which is typically used for single-query path planning, but that can also be used to build a representation of the free configuration space starting from a given root node (in this paper we use it for the latter purpose). The algorithm builds a tree $\mathcal{T}$ and is summarized in Algorithm [\[alg:RRT\*\]](#alg:RRT*){reference-type="ref" reference="alg:RRT*"}, and its main functions are:

- RandomSample: return a random sample from a uniform probability distribution in configuration space $\mathcal{X}$.

- IsSampleCollision: return *True* if the given sample is in collision with an obstacle.

- Nearest: return the node in $\mathcal{V}$ closest to the random sample $x_{\text{rand}}$.

- Near: return a set of nodes in $\mathcal{V}$ within distance $r^*$ from the $x_{\text{rand}}$ where $r^*$ is defined as $$\begin{equation}
      r^* = \min (\gamma^*(\frac{\log{\abs{\mathcal{V}}}}{\mathcal{V}})^{\frac{1}{d+1}},\eta),
  \end{equation}$$ $d$ is the dimension of the configuration space, $\eta$ is the constant in the definition of the Steering function, $\gamma^* = 2((1+\frac{1}{d})\frac{A_{\text{free}}}{\pi})^{\frac{1}{d}}$, and $A_{\text{free}}$ represents the area of the free space.

- Steering: given two states $p$ and $p'$, and $\eta$, return a path from $p$ toward $p'$ with length $\eta$ if there is no collision between the path and the obstacles.

- isEdgeCollision: given two states $p$ and $p'$, return *True* if there is no collision between the path that connects $p$ to $p'$ and the obstacles; note that in general this function is typically built by using IsSampleCollision.

- Rewire: check if the cost of the nodes in $X_{\text{near}}$ is less through $x_{\text{new}}$ as compared to their older costs, then its parent is changed to $x_{\text{new}}$.

For this paper, the only modification to the original `RRT`$^*$ algorithm is represented by line $\ref{al:store collision}$ in Algorithm [\[alg:RRT\*\]](#alg:RRT*){reference-type="ref" reference="alg:RRT*"}, which stores random samples that were found to be in collision with an obstacle in the list $\mathcal{V}_{\text{collision}}$ instead of discarding them; this list is then returned by the algorithm and will be used to define the CBF constraints in our algorithm (see Section [3.4](#sec:tree-CBF){reference-type="ref" reference="sec:tree-CBF"}). In general, `RRT`$^*$ is guaranteed to be asymptotically complete and optimal, although these guarantees do not necessarily hold with a finite number of samples.

:::: algorithm
::: algorithmic
Input (Obstacle lists $\mathcal{O}$, start point, max$_{\text{itr}}$, $\eta$) $\mathcal{V}\gets$ start point, $\mathcal{E}\gets \emptyset$, $\mathcal{V}_{\text{collision}}\gets\emptyset$ $x_{\text{rand}}\leftarrow$ RandomSample []{#al:store collision label="al:store collision"}Append $x_{\text{rand}}$ to $\mathcal{V}_{\text{collision}}$ and break $x_{\text{nearest}}\leftarrow$ Nearest$(G=(V,E),x_{\text{rand}})$ $x_{\text{new}}\leftarrow$ Steer$(x_{\text{nearest}},x_{\text{rand}},\eta)$ $X_{\text{near}}\leftarrow$ Near$(G=(V,E),x_{\text{new}},r^{*})$ $\mathcal{V}\leftarrow \mathcal{V}\cup {x_{\text{new}}}$ $x_{\text{min}} \leftarrow x_{\text{nearest}}$ $c_{\text{min}} \leftarrow$ cost$_{\text{nearest}}+\text{norm}(x_{\text{nearest}},x_{\text{new}})$ $x_{\text{min}}\leftarrow x_{\text{near}}$ $c_{\text{min}} \leftarrow$ cost$_{\text{near}}+\text{norm}(x_{\text{near}},x_{\text{new}})$ $\mathcal{E}\leftarrow \mathcal{E}\cup{(x_{\text{min}},x_{\text{new}})}$ $\mathcal{E}\leftarrow$Rewire$((\mathcal{V},\mathcal{E}),X_{\text{near}},x_{\text{new}})$ return $\mathcal{T}=(\mathcal{V}, \mathcal{E})$, $\mathcal{V}_{\text{collision}}$.
:::

[]{#alg:RRT* label="alg:RRT*"}
::::

:::: algorithm
::: algorithmic
$x_{\text{parent}}\leftarrow$ Parent($x_{\text{near}}$) $\mathcal{E}\leftarrow (\mathcal{E}-\{x_{\text{parent}},x_{\text{near}}\}) \cup{(x_{\text{new}},x_{\text{near}})}$ return $\mathcal{E}$.
:::

[]{#alg:rewire label="alg:rewire"}
::::

## Control Lyapunov and Barrier Functions (CLF, CBF) {#sec:ECBF}

In this section we review CLF and CBF constraints, which are differential inequalities that ensure stability and safety (set invariance) of a control signal $u$ with respect to the dynamics [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"}. These constraints are defined. First, it is necessary to review the following.

::: definition
The Lie derivative of a differentiable function $h$ for the dynamics [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"} with respect to the vector field $Ax$ is defined as $\mathcal{L}_{Ax}h(x)=\frac{\partial h(x(t))}{\partial x}^\mathrm{T}Ax$.
:::

Applying this definition to [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"} we obtain $$\begin{equation}
\label{Lie}
  % h^r(x)=\cL_{Ax}^rh(x)+\cL_B\cL_{Ax}^{r-1}h(x)u
  \dot{h}(x)=\mathcal{L}_{Ax}h(x)+\mathcal{L}_Bh(x)u.
\end{equation}$$

In this work, we assume that Lie derivatives of $h(x)$ of the first order are sufficient [@Isidori:book95] (i.e., $h(x)$ has relative degree 1 with respect to the dynamics [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"}); however, the result could be extended to the higher relative degree, as discussed in [@Mahroo].

We now pass to the definition of the differential constraints. Consider a continuously differentiable function $V(x):\mathcal{X}\to\mathbb{R}^{}{}$, $V(x)\geq 0$ for all $x\in\mathcal{X}$, with $V(x)=0$ for some $x\in\mathcal{X}$.

::: definition
[]{#def:ECLF label="def:ECLF"} The function $V(x)$ is a *Control Lyapunov Function* (CLF) with respect to [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"} if there exists positive constants $c_1,c_2,c_v$ and control inputs $u\in \mathcal{U}$ such that $$\begin{equation}
\label{cons:clf}
    \begin{aligned}
      \mathcal{L}_AV(x)+\mathcal{L}_BV(x)u+c_v V(x)\leq 0,\forall x \in \mathcal{X}.
    \end{aligned}
\end{equation}$$ Furthermore, [\[cons:clf\]](#cons:clf){reference-type="eqref" reference="cons:clf"} implies that $\lim_{t\to\infty}V(x(t))=0$.
:::

Consider a continuously differentiable function $h(x):\mathcal{X}\to\mathbb{R}^{}{}$ which defines a safe set $\mathcal{C}$ such that $$\begin{equation}
\label{set_c}
  \begin{aligned}
    \mathcal{C}&=\{x\in \mathbb{R}^{n}{}|\;h(x)\geq0\},\\
    \partial \mathcal{C}&=\{x\in \mathbb{R}^{n}{}|\;h(x)=0\},\\
    {Int}(\mathcal{C})&=\{x\in \mathbb{R}^{n}{}|\;h(x)>0\}.
  \end{aligned}
\end{equation}$$ In our setting, the set $\mathcal{C}$ will represent a convex local approximation of the free configuration space (in the sense that $x\in\mathcal{C}$ does not contain any sample that was found to be in collision). We say that the set $\mathcal{C}$ is *forward invariant* (also said *positive invariant* [@positiveInvariant]) if $x(t_0) \in \mathcal{C}$ implies $x(t)\in \mathcal{C}$, for all $t\geq 0$ [@zcbf1].

::: definition
[]{#def:ECBF label="def:ECBF"} The function $h(x)$ is a *Control Barrier Function* with respect to [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"} if there exists a positive constant $c_h$, control inputs $u\in \mathcal{U}$, and a set $\mathcal{C}$ such that $$\begin{equation}
\label{cons:cbf}
    \mathcal{L}_{Ax}h(x)+\mathcal{L}_Bh(x)u+c_hh(x)\geq 0,\forall x \in \mathcal{C}.
\end{equation}$$ Furthermore, [\[cons:cbf\]](#cons:cbf){reference-type="eqref" reference="cons:cbf"} implies that the set $\mathcal{C}$ is forward invariant.
:::

## Environment {#sec:environment}

As mentioned in the previous section, the environment is implicitly represented by the Sample function. Additionally, we assume that the robot can measure the displacement $\hat{l}_i-x$ between its position $x$ and its set of *landmarks* $\hat{l}_i$. The location of $\hat{l}_i$ is assumed to be known and fixed in the environment. Note that the landmarks $\hat{l}_i$, from the point of view of our algorithms, can be arbitrary as long as there is at least one landmark visible from any point $x$ in the free configuration space. The landmarks do not need to be chosen from the samples of the `RRT`$^*$ algorithm, or from the obstacles. Furthermore, we assume that the total extent of the environment is bounded by a convex polyhedron $\mathcal{X}_{\text{env}}$ (e.g., simple box constraints).

# FEEDBACK CONTROL PLANNING VIA `RRT`$^*$ {#sec:problem-setup}

At a high level, our algorithm first divides the configuration space into cells according to a tree-graph representation of the environment, and then computes a controller for each cell that can be used to move the robot along the tree starting from any initial location. More in detail, our solution is comprised of the following steps:

1.  Run `RRT`$^*$, and then simplify the generated tree.

2.  Define a convex cell around every node of the tree while taking into account the position of its parent.

3.  Define the CLF and CBF constraints for each cell.

4.  Use a robust LP formulation to compute a controller for each cell that respects the CLF and CBF constraints.

5.  Reformulate the controller in terms of visible and invisible landmarks for the limited field of view of the robot.

Below we give the details of each one of the steps.

:::: {#fig:tree .figure latex-placement="t"}
::: caption
Obstacles are represented by blue circles, and the start point of `RRT`$^*$ is located at the origin. In Fig. [\[fig:tree-1\]](#fig:tree-1){reference-type="ref" reference="fig:tree-1"}, yellow dots show the samples in collision with the obstacles, and the generated tree from `RRT`$^*$ is plotted in green. Fig. [\[fig:tree-2\]](#fig:tree-2){reference-type="ref" reference="fig:tree-2"} depicts the simplified tree following Section [3.1](#sec:simplified-tree){reference-type="ref" reference="sec:simplified-tree"}.
:::
::::

## Simplified Tree Graph {#sec:simplified-tree}

We start with a tree $\mathcal{T}= (\mathcal{V},\mathcal{E})$ generated by the traditional `RRT`$^*$ algorithm from Section [2.3](#sec:rrtstar){reference-type="ref" reference="sec:rrtstar"}. Since the number of samples is finite, the generated tree is not asymptotically optimal but it has a large number of nodes. We simplify the tree such that the tree has less number of nodes while it keeps track of all samples in collision with obstacles by following three steps:

1.  []{#it:ppr label="it:ppr"} *Post Processing Rewiring* (PPR, Algorithm [\[alg:rewiring\]](#alg:rewiring){reference-type="ref" reference="alg:rewiring"}): similarly to $\mathtt{\theta^*}$ [@nash2007theta], we examine each node starting from the root and using a breadth-first order, and use the function isEdgeCollision to check if it can be connected to an ancestor (testing from the parent and then moving toward the root) without collisions and while lowering the path length.

2.  Remove Crossing (RC, Algorithm [\[alg:rc\]](#alg:rc){reference-type="ref" reference="alg:rc"}), if edge $(i,j)$ crosses edge $(p,q)$ with an intersection at point $k$, we add point $k$ to $\mathcal{V}$, and edges $(i,k)$ and $(p,k)$ to $\mathcal{E}$. Then, we compare the costs of reaching the start point from $k$ through edges $(k,j)$ and $(k,q)$, and add the smallest one to $\mathcal{E}$ as the parent of node $k$.

3.  []{#it:ctl label="it:ctl"} Cutting the Leaves (CtL, Algorithm [\[alg:cutting\]](#alg:cutting){reference-type="ref" reference="alg:cutting"}), for a node that has multiple leaves as children, we only keep a single leaf in the middle.

4.  We repeat steps [\[it:ppr\]](#it:ppr){reference-type="ref" reference="it:ppr"}-[\[it:ctl\]](#it:ctl){reference-type="ref" reference="it:ctl"} until there are no changes in $\mathcal{T}$.

Fig. [1](#fig:tree){reference-type="ref" reference="fig:tree"} shows an example of the procedure, starting from the `RRT`$^*$ tree (Fig. [\[fig:tree-1\]](#fig:tree-1){reference-type="ref" reference="fig:tree-1"}), and ending with the simplified tree after the three steps (Fig. [\[fig:tree-2\]](#fig:tree-2){reference-type="ref" reference="fig:tree-2"}).

Note that as a consequence of the simplifying steps above, it is possible to connect each sample from the original `RRT`$^*$ to the simplified tree with a straight line, which suggests that the simplified tree will be a good roadmap representation [@Choset:book05] of the free configuration space reachable from the root.

:::: algorithm
::: algorithmic
Input ($\mathcal{T}=(\mathcal{V},\mathcal{E})$) $\mathcal{E}\leftarrow \mathcal{E}-${node$_i$,Parent(node$_i$)} $\cup$ node$_i$,Parent(Parent(node$_i$)) return $\mathcal{T}=(\mathcal{V},\mathcal{E})$
:::
::::

:::: algorithm
::: algorithmic
Input ($\mathcal{T}=(\mathcal{V},\mathcal{E})$) $k =$intersection $(i,j)$ and $(p,q)$ $(i)\leftarrow k$ $(p)\leftarrow k$ $\mathcal{E}\leftarrow \mathcal{E}-\{(i,j),(p,q)\}$ $\mathcal{E}\leftarrow \mathcal{E}\cup{\{(i,k),(p,k)\}}$ $\text{cost}_j \leftarrow$ reach start point through node $j$ $\text{cost}_q \leftarrow$ reach start point through node $q$ $\mathcal{E}\leftarrow \mathcal{E}\cup{\{(k,j)\}}$ $\mathcal{E}\leftarrow \mathcal{E}\cup{\{(k,q)\}}$ return $\mathcal{T}=(\mathcal{V},\mathcal{E})$
:::

[]{#alg:rc label="alg:rc"}
::::

:::: algorithm
::: algorithmic
Input ($T=(V,E)$) angles$_i$ $\leftarrow$ angles$_i$ $\cup$ Angle =$(i,j)$ $j_{largest}$ $\leftarrow$ LargestAngle(angles$_i$) $j_{smallest}$ $\leftarrow$ SmallestAngle(angles$_i$) $E_s \leftarrow E_s \cup \{i,j_{largest}\}\cup \{i,j_{smallest}\}$ $V_s \leftarrow V_s \cup \{j_{largest}\}\cup \{j_{smallest}\}$ return $T_s=(V_s,E_s)$
:::

[]{#alg:ppr label="alg:ppr"}
::::

## Environment Constraints {#tree-X}

For each edge $(i,j) \in E_{}$ in the tree, we define a cell $\mathcal{X}_{ij}$ as $$\begin{equation}
  \mathcal{X}_{ij} = \mathcal{X}_{V_i} \cap \mathcal{X}_{P_i} \cap \mathcal{X}_{\text{env}}, \label{Xi}
\end{equation}$$ where $$\label{state_convex}
  \begin{align}
    &
   \small{\mathcal{X}_{V_{ij}} =\{x| (x-x_i)^\mathrm{T}\frac{x_k-x_i}{\norm{x_k-x_i}}\leq\frac{\norm{x_k-x_i}}{2}, k\in\mathcal{V}\setminus\{j\}\} \label{Xvi}} \\
    & \small {\mathcal{X}_{P_{ij}} =\{x| (x-x_i)^\mathrm{T}\frac{x_j-x_i}{\norm{x_j-x_i}}\leq \norm{x_j-x_i}, i,j\in\mathcal{V}\}},
      \label{Xij}
 \end{align}$$ and $\norm{x_k-x_i}$ and $x \in\mathbb{R}^{n}{}$ is the Euclidean distance between nodes $i,k\in\mathcal{V}$; the polyhedron $\mathcal{X}_{ij}$ is similar to a Voronoi region [@latombe2012robot], and is defined by a set of perpendicular bisector of segments $i,k$ for $k\in \mathcal{V}\setminus\{j\}$, and by the line perpendicular to $i,j$ passing through $j$. The inequalities in [\[Xvi\]](#Xvi){reference-type="eqref" reference="Xvi"}-[\[Xij\]](#Xij){reference-type="eqref" reference="Xij"} can be written in matrix form of [\[state_limits\]](#state_limits){reference-type="eqref" reference="state_limits"}. Note that $\mathcal{X}_{ij}$ contains all the points that are closest to $i$ than other vertices in $\mathcal{T}$, but it also includes the parent $j$; we empirically noticed that with the latter modification we obtained more robust results. An example of $\mathcal{X}_{ij}$ is shown in Fig. [2](#fig:CBF-X){reference-type="ref" reference="fig:CBF-X"}

## Stability by CLF {#sec:tree-CLF}

To stabilize the navigation along an edges of a tree, we define the Lyapunov function $V_{ij}(x)$ as $$\begin{equation}
\label{V}
  V_{ij}(x)=z_{ij}^T (x-x_{j}),
\end{equation}$$ where $z_{ij}\in \mathbb{R}^{n}{}$ is the for edge $(i,j)$, $x_{j} \in \text{\emph{exit face}}$ is the position of the parent of node $i$, and $V_{ij}(x)$ reaches its minimum $V(x)=0$ at $x_j$. Note that the Lyapunov function represents, up to a constant, the distance $d(x,x_j)$ between the current system position and the exit face. By Definition [\[def:ECLF\]](#def:ECLF){reference-type="ref" reference="def:ECLF"}, $V_{ij}(x)$ is a CLF.

::: definition
[]{#exitface label="exitface"} For $\mathcal{X}_{ij}$, we define the exit direction as $z_{ij}= \frac{x_j-x_i}{\norm{x_j-x_i}}$ that is a unit vector from node $j$ towards node $i$ where $j\in\mathcal{V}_s$ is the parent of node $i$.
:::

## Safety by CBF {#sec:tree-CBF}

In this section, we define barrier functions $h_{ij}(x)$ that defines a cone representing a local convex approximation of the free space between $i$ and $j$, in the sense that it excludes all samples in $\mathcal{V}$ that are on the way from $i$ to $j$. In particular, we use the following steps (we consider only the 2-D case, although similar ideas could be applied to the 3-D case):

1.  Define set $\mathcal{O}_{ij}\subset\mathcal{V}_{\text{collision}}$ whose projection falls on the segment $i,j$, i.e., $$\begin{equation}
        \mathcal{O}_{ij}=\{o\in\mathcal{V}_\text{collision}\mid0\leq\mathop{\mathrm{proj}}_{ij}(o)\leq 1\}
    \end{equation}$$ where $$\begin{equation}
        \mathop{\mathrm{proj}}_{ij}(o)=\frac{(\mathbf{x}_i-\mathbf{x}_j)^\mathrm{T}(\mathbf{x}_i-\mathbf{x}_o)}{\norm{\mathbf{x}_i-\mathbf{x}_j}}
    \end{equation}$$ is the scalar projection of the vector $o$ onto the segment $i,j$.

2.  From the set $\mathcal{O}_{ij}$, we choose two samples such that $$\begin{equation}
    \label{o_cbf}
        \begin{aligned}
          & o_{u} =\min_{o\in\mathcal{O}_{ij}}\{\mathbf{x}_o-\text{proj}^{io}_{ij} | \theta_{io}>0\} \\
          &  o_{d} = \min_{o\in\mathcal{O}_{ij}}\{\mathbf{x}_o-\text{proj}^{io}_{ij} | \theta_{io}<0\}
        \end{aligned}
    \end{equation}$$ where $\theta_{io}=\angle(i,j,o)$ is the oriented angle between edge $(i,j)$ and line $(x_o,x_i)$.

3.  We write the equations of two lines passing through $\{i,o_{u}\}$ and $\{i,o_{d}\}$ in a matrix form using $A_{h_{i}}\in \mathbb{R}^{2\times n}{}$, $b_h\in \mathbb{R}^{2}{}$ to define the invariant set $$\begin{equation}
        \mathcal{C}_{ij}=\{x\in\mathbb{R}^{2}{}:A_{h_{ij}}\mathbf{x}+b_{h_{i}}>0\}.
    \end{equation}$$

The corresponding CBF is then defined as $$\begin{equation}
\label{h}
  h_{ij}(x)=A_{h_{ij}}x+b_{h_{ij}}.
\end{equation}$$ An example of the set $\mathcal{C}_{ij}$ is shown in Fig. [2](#fig:CBF-X){reference-type="ref" reference="fig:CBF-X"}. Note that the region $\mathcal{C}_{ij}$ might not include the entire cell $\mathcal{X}_{ij}$. However, the controller will be designed to satisfy the CBF and CLF constraints over the entire cell $\mathcal{X}_{ij}$; in practice, this means that if the robot starts in the region $\mathcal{X}_{ij}\setminus\mathcal{C}_{ij}$, it will be driven toward the boundary of $\mathcal{C}_{ij}$ (this is a consequence of the CBF constraint, and can be proved in a similar way as the original result [@ames2014control]).

:::: {#fig:CBF-X .figure latex-placement="t"}
::: caption
The Voronoi-like region $\mathcal{X}_{ij}$ for edge $(i,j)$, and the corresponding CBF constraints; green points and arrows: other vertices and edges in the tree $\mathcal{T}$; red points: collision samples in $\mathcal{V}_s$; black line: $\mathcal{X}_{\text{env}}$; green dashed lines: $\mathcal{X}_{V_{ij}}$ and $\mathcal{X}_{P_{ij}}$; shaded region: $\mathcal{X}_{ij}$; red dotted lines: CBF constraints $h_i$. For the CBF constraints, note that the projection of vector $(i,o_4)$ onto edge $(i,j)$ does not lie between node $i$ and node $j$, hence $o_4$ does not support a constraint; moreover, from [\[o_cbf\]](#o_cbf){reference-type="eqref" reference="o_cbf"}, $o_d = o_1$ and $o_u= o_2$ are the closet points (in angle) to the edge $(i,j)$ and are on two sides of the edge $(i,j)$.
:::
::::

## Controller {#sec:tree-controller}

We assume that the robot can only measure the relative displacements between the robot's position $x$ and the landmarks in the environment, which corresponds to the output function $$\begin{equation}
\label{vec-landmarks}
  y=(L-x\mathbf{1}^\mathrm{T})^\vee=L^\vee-\mathcal{I}x=\mathop{\mathrm{stack}}{(l_i- x)},
\end{equation}$$ where $L_\in\mathbb{R}^{n\times n_l}{}$ is a matrix of landmark locations, $i=1,\hdots,n_l$ that $n_l$ is the number of landmarks, $A^\vee$ represents the vectorized version of a matrix $A$, $\mathcal{I}=\mathbf{1}_{nl} \otimes I_n$, and $\otimes$ is the Kronecker product. Our goal is to find a feedback controller of the form $$\begin{equation}
\label{u}
  u_{ij}(K)=K_{ij}y,
\end{equation}$$ where $K_{ij} \in \mathbb{R}^{m\times nn_l}{}$ are the feedback gains that need to be found for each cell $\mathcal{X}_{ij}$. Intuitively, a controller of the form [\[u\]](#u){reference-type="eqref" reference="u"} corresponds to a control command that is a weighted linear combination of the measured displacements $y$. The goal is to design $u(y)$ such that the system is driven toward the exit direction $z_{ij}$ while avoiding obstacles. Note that, to define a controller for edge $(i,j)$, the landmarks do not necessarily need to belong to $\mathcal{X}_{ij}$, and, in general, each cell could use a different set of landmarks (we explore this direction further in Section [3.6](#sec:limited-field-of-view){reference-type="ref" reference="sec:limited-field-of-view"}).

Following the approach of [@Mahroo], and using the CLF-CBF constraints reviewed in Section [2](#sec:background){reference-type="ref" reference="sec:background"}, we encode our goal in the following feasibility problem:

$$\begin{equation}
\label{findK}
  \begin{aligned}
    & \textrm{find} \;\;{K_{ij}}\\
    & \textrm{subject to}:\\
    &\{\text{CBF:}\;-( \mathcal{L}_{A_ix}h_{ij}(x)+\mathcal{L}_Bh_{ij}(x)u+c^\mathrm{T}_hh_{ij}(x))\}\leq 0,\\
    & \{\text{CLF:}\quad\mathcal{L}_{A_ix}V_{ij}(x)+\mathcal{L}_BV_{ij}(x)u+c^\mathrm{T}_v{V_{ij}}(x)\}\leq 0,\\
    &u\in\mathcal{U},\;\;\forall x\in \mathcal{X}_{ij},\;\;(i,j)\in\mathcal{E}.
  \end{aligned}
\end{equation}$$

In practice, we aim to find a controller that satisfies the constraints in [\[findK\]](#findK){reference-type="eqref" reference="findK"} with some margin. Note that the constraints in [\[findK\]](#findK){reference-type="eqref" reference="findK"} need to be satisfied for all $x$ in the region $\mathcal{X}_{ij}$, i.e., the same control gains should satisfy the CLF-CBF constraints at every point in the region. We handle this type of constraint by rewriting [\[findK\]](#findK){reference-type="eqref" reference="findK"} using a min-max formulation [@Mahroo], arriving to the following robust optimization problem: $$\begin{equation}
\label{opt_margin}
\centering
  \begin{aligned}
    &\min_{K_{ij},S_{V_{ij}},S_{h_{ij}}}\;w_{h_{ij}}^\mathrm{T}S_{h_{ij}}+w_{V_{ij}}S_{V_{ij}}\\
    &\textrm{\textrm{subject to}\;}\\
    &\max_x \text{CBF}\leq S_{h_{ij}} ,\\
    &\max_x \text{CLF}\leq S_{V_{ij}},\\
    & S_{V_{ij}},S_{h_{ij}} \leq 0,\;\;u\in\mathcal{U},\;\; \forall x\in \mathcal{X}_{ij},\;\; (i,j)\in\mathcal{E}.
  \end{aligned}
\end{equation}$$ From [\[Lie\]](#Lie){reference-type="eqref" reference="Lie"}, the Lie derivatives of $h_{ij}(x)$ and $V_{ij}(x)$ are written as: $$\begin{equation}
\label{cons-Lie}
  \begin{aligned}
    & \dot{h}_{ij}(x)=A_{hij}\dot{x} =A_{hij}(A x+B u),\\
    & \dot{V}_{ij}(x) =z_{ij}^\mathrm{T}\dot{x}= z_{ij}^\mathrm{T}(Ax+Bu).
  \end{aligned}
\end{equation}$$ Combining [\[vec-landmarks\]](#vec-landmarks){reference-type="eqref" reference="vec-landmarks"}, [\[u\]](#u){reference-type="eqref" reference="u"}, and [\[cons-Lie\]](#cons-Lie){reference-type="eqref" reference="cons-Lie"} with [\[sys1\]](#sys1){reference-type="eqref" reference="sys1"}, the constraints in [\[opt_margin\]](#opt_margin){reference-type="eqref" reference="opt_margin"} can be rewritten as: $$\begin{equation}
\label{primal-cbf}
  \begin{aligned}
    & \text{CBF constraint:}\\
    &\begin{bmatrix}
      \underset{x}{\max}-(A_{hij}A-A_{hij}B K_{ij}\mathcal{I}+{c_h}A_{hij})x\\
      \textrm{subject to}\;\;\;A_{xij} x \leq b_{xij}\\
    \end{bmatrix}
    \leq \\&
    \quad \quad  \quad \quad \quad \quad \quad  \quad \quad  \quad \quad
    S_{h_{ij}}+c_bb_{hij}+{A_{hij}}B K_{ij}L_{ij}^\vee,\\
  \end{aligned}
\end{equation}$$ $$\begin{equation}
\label{primal-clf}
  \begin{aligned}
    & \text{CLF constraint:}\\
    &\begin{bmatrix}\underset{x}{\max}(z_{ij}^\mathrm{T}A-z_{ij}^\mathrm{T}BK_{ij}\mathcal{I}+{c_v}z_{ij}^\mathrm{T})x \\
      \textrm{subject to}\;\;\;A_{xij} x \leq b_{xij}

    \end{bmatrix}
    \leq \\&
    \quad \quad  \quad \quad \quad \quad \quad  \quad \quad  \quad \quad S_{Vij}+c_vz_{ij}^\mathrm{T}x_{j}-z_{ij}^T B K_{ij}L_{ij}^\vee,\\
  \end{aligned}
\end{equation}$$ Constraints in [\[primal-cbf\]](#primal-cbf){reference-type="eqref" reference="primal-cbf"}, [\[primal-clf\]](#primal-clf){reference-type="eqref" reference="primal-clf"} are linear in terms of variable $x$, so we can write dual forms of the constraints as $$\begin{equation}
\label{dual-conscbf}
  \begin{aligned}
    & \text{CBF dual constraint:}\\
    &\begin{bmatrix}
      &\min_{\lambda_{bj}} \lambda_{bij}^\mathrm{T}b_{xij} \\
      &\textrm{subject to}\;\\
      & A_{xij} ^\mathrm{T}\lambda_{bij}=(-A_{hij}A+A_{hij}B K_{ij}\mathcal{I}-{c_h}A_{hij})^\mathrm{T}\\
      & \lambda_{bij}\geq 0,
    \end{bmatrix} \leq\\& \quad  \quad \quad  \quad \quad  \quad \quad  \quad \quad \quad
    S_{hij}+c_hb_{hij}+{A_{hij}}B_{ij} K_{ij}L_{ij}^\vee,
  \end{aligned}
\end{equation}$$ $$\begin{equation}
\label{dual-consclf}
  \begin{aligned}
    & \text{CLF dual constraint:}\\
    &\begin{bmatrix}
      &\min_{\lambda_l}\lambda_{lij}  ^\mathrm{T}b_{xij}\\
      &\textrm{subject to}\;\\
      &  A_{xij}^\mathrm{T}\lambda_{lij}
      =(z_{ij}^\mathrm{T}A-z_{ij}^\mathrm{T}BK_{ij}\mathcal{I}+{c_v}z_{ij}^\mathrm{T})^\mathrm{T}\\
      & \lambda_{lij} \geq 0
    \end{bmatrix}\leq \\& \quad \quad  \quad \quad  \quad \quad  \quad \quad  \quad \quad \quad S_{Vij}+c_vz_{ij}^\mathrm{T}x_{j}-z_{ij}^TB K_{ij}L_{ij}^\vee,
  \end{aligned}
\end{equation}$$ Consequently, [\[opt_margin\]](#opt_margin){reference-type="eqref" reference="opt_margin"} with the dual constraints becomes: $$\begin{equation}
\label{opt-dual}
  \begin{aligned}
    &\min_{K,S_{V},S_{h}}\;w_{h}^\mathrm{T}S_{h}+w_{V}S_{V}\\
    &\textrm{subject to}:\\
    &\text{CBF dual constraint} ,\\
    &\text{CLF dual constraint},\\
    % &\text{Actuator dual constraint},\\
    & S_h,S_V \leq 0,
  \end{aligned}
\end{equation}$$ From [@Mahroo Lemma 1], the optimization problem [\[opt_margin\]](#opt_margin){reference-type="eqref" reference="opt_margin"} is equivalent to [\[opt-dual\]](#opt-dual){reference-type="eqref" reference="opt-dual"}.

Staring from a point $x\in\mathcal{X}_{ij}$, $u_{ij}$ drives the robot toward $x_j$, the robot switches its controller to $u_{jq}$ when $\norm{x-x_j}\leq\epsilon$ where node $q$ is the parent of node $j$.

## Control With the Limited Field of View {#sec:limited-field-of-view}

In the formulation above and in the work of [@Mahroo], it is implicitly assumed that the controller has access to all the landmarks measurements at all times. However, in practice, a robot will only be able to detect a subset of the landmarks due to a limited field of view or environment occlusions. To tackle this issue, we show in this section that the controller $u$ [\[u\]](#u){reference-type="eqref" reference="u"} can be designed using multiple landmarks (as in the preceding section), but then computed using a single landmark.

::: proposition
[]{#prop:limited field view label="prop:limited field view"} Let $K=\begin{bmatrix}K_1,\cdots,K_i,\cdots, K_l\end{bmatrix}$ be a partition of the controller matrix conformal with $L^\vee$. Given an arbitrary landmark $\hat{l}_i$ (column of $L$), the controller [\[u\]](#u){reference-type="eqref" reference="u"} can be equivalently written as $$\begin{equation}
\label{u_new}
    u = \sum_jK_jy_i+k_{\text{bias},i}
\end{equation}$$ where $k_{\text{bias},i}\in\mathbb{R}^{n}{}$ is a constant vector given by $$\begin{equation}
    k_{\text{bias},i}=\sum_{j\neq i}K_j(\hat{l}_j-\hat{l}_i)
\end{equation}$$
:::

::: proof
*Proof.* Using the conformal partition of $K$, we can expand [\[u\]](#u){reference-type="eqref" reference="u"} as $$\begin{equation}
\label{decomU}
    u = \sum_jK_j(\hat{l}_j-x)%=\sum_jK_jy_j-\sum_jK_jx.
\end{equation}$$ Adding and subtracting $\sum_j K_j y_i$ and reordering, we have $$\begin{equation}
\label{u_limited}
    u = %\sum_jK_jy_j-\sum_j K_j y_i+\sum_j K_j y_i-\sum_jK_jx=
    \sum_j K_j (\hat{l}_i-x)+\sum_j K_j(\hat{l}_i-\hat{l}_j),
\end{equation}$$ from which the claim follows. ◻
:::

Using the fact that the global positions of the landmarks are known during planning, our new Proposition [\[prop:limited field view\]](#prop:limited field view){reference-type="ref" reference="prop:limited field view"} shows that it is possible to implement the controller $u$ by measuring a single displacement $y_i$; moreover, since the original controller [\[u\]](#u){reference-type="eqref" reference="u"} is smooth, one can also switch among different landmarks without introducing discontinuities in the control. Although we stated our result for a single landmark, it is possible to prove a similar claim for any subset of landmarks.

:::: {#fig:Matlab-sim .figure latex-placement="b"}
::: caption
Simulated trajectories for various start points for the original environment (Fig. [\[fig:Matlab-org\]](#fig:Matlab-org){reference-type="ref" reference="fig:Matlab-org"}) and for a deformed version of the same environment (Fig. [\[fig:Matlab-rotate\]](#fig:Matlab-rotate){reference-type="ref" reference="fig:Matlab-rotate"}). The start points for each trajectory are represented by star markers.
:::
::::

# SIMULATION AND EXPERIMENTAL RESULTS

To assess the effectiveness of the proposed algorithm, we run a set of validation using both MATLAB simulations and experiments using ROS on a Create 2 robot by iRobot [@iCreate]. While the optimization problem guarantees exponential convergence of the robot to the stabilization point, in these experiments the velocity control input $u$ has been normalized to achieve constant velocities along the edges of the trees.

:::: {#fig: .figure latex-placement="t"}
::: caption
The Create 2 robot used for the experiments is shown in Fig. [\[fig:robot\]](#fig:robot){reference-type="ref" reference="fig:robot"}. We use AprilTags (Fig. [\[fig:apriltag-figure\]](#fig:apriltag-figure){reference-type="ref" reference="fig:apriltag-figure"}) as the landmarks for the algorithm.
:::
::::

:::: {#fig:real-example .figure latex-placement="t"}
::: caption
On the left, Fig. [\[fig:original-env\]](#fig:original-env){reference-type="ref" reference="fig:original-env"} shows the original environment used for our experiment. On the right, Fig. [\[fig:rotated-env\]](#fig:rotated-env){reference-type="ref" reference="fig:rotated-env"} shows the deformed version of the environment.
:::
::::

## MATLAB Simulation

The simulated MATLAB environment is presented in Fig. [1](#fig:tree){reference-type="ref" reference="fig:tree"}, where the obstacles are represented by blue circles. To generate the `RRT`$^*$ we set the maximum number of iterations in `RRT`$^*$ to $1000$, and we choose $\eta=60$. The generated tree from `RRT`$^*$ and its simplified form are shown in Fig. [\[fig:tree-1\]](#fig:tree-1){reference-type="ref" reference="fig:tree-1"} and Fig. [\[fig:tree-2\]](#fig:tree-2){reference-type="ref" reference="fig:tree-2"} respectively. Then, we compute a controller for each edge of the simplified tree as described in Section [3.5](#sec:tree-controller){reference-type="ref" reference="sec:tree-controller"}. Fig. [3](#fig:Matlab-sim){reference-type="ref" reference="fig:Matlab-sim"} shows the resulting trajectories from four initial positions on two versions of the environment: one with the obstacles identical to the ones used during planning (Fig. [\[fig:Matlab-org\]](#fig:Matlab-org){reference-type="ref" reference="fig:Matlab-org"}), and one with deformed obstacles (Fig. [\[fig:Matlab-rotate\]](#fig:Matlab-rotate){reference-type="ref" reference="fig:Matlab-rotate"}); for the latter, also the landmarks have been modified accordingly. In all cases, the robot reaches the desired goal location by applying the sequence of controllers found during planning. Note that the deformed environment in Fig. [\[fig:Matlab-rotate\]](#fig:Matlab-rotate){reference-type="ref" reference="fig:Matlab-rotate"} is successfully handled without replanning (i.e., by using the original controllers). This shows that our algorithm can be robust to (often very significant) deformations of the environment; however, there are also cases where, without replanning, the designed controllers might fail. Empirically, we noticed that there is a trade-off between obtaining shortest paths (that, by their nature, graze the obstacles) and the robustness of the controller; we plan to study this trade-off in future work.

:::: {#fig:experiment-results .figure latex-placement="b"}
::: caption
Real trajectories followed by the Create for both the original and deformed environments. For all the tested start points, the robot converged to the expected goal position.
:::
::::

## iRobot Create 2 Experiment

We further tested our algorithm on a Create 2 robot in lab environments that were similar to those used during the simulation. A bird's-eye view of the experimental setup is shown in Fig. [5](#fig:real-example){reference-type="ref" reference="fig:real-example"}. The robot is equipped with a calibrated onboard Arducam for Raspberry Pi camera [@arducam], and we use OptiTrack motion capture system with 44 infra-red cameras to collect ground truth position information (the motion capture system is not used by our controller). The landmarks are represented by fiducials (AprilTags [@Wang2016]), and are placed at known positions and orientations with respect to the reference frame of the motion capture, using unique codes for data association. Our implementation is based on the Robot Operating System (ROS, [@ROS]).

There are three practical considerations that need to be taken into account in the implementation. First, due to the limited field of view of the camera, we use Proposition [\[prop:limited field view\]](#prop:limited field view){reference-type="ref" reference="prop:limited field view"} to compute the controller based on one of the fiducials detected by the camera at each time instant. Second, the approach presented in the previous sections implicitly assumes that the robot has access to the measurements $Y$ in a frame which is rotationally aligned with the world reference frame. To satisfy this assumption, the measured displacement of an AprilTag with respect to the Create in world coordinates $\left({}^{W}t_{AT-C}\right)$ is computed as: $$\begin{equation}
  {}^{W}\mathbf{t}_{AT-C} = {}^{W}\mathbf{R}_{AT} \cdot \left( {}^{C}\mathbf{R}_{AT} \right)^{\top} \cdot {}^{C}\mathbf{t}_{AT-C},
\end{equation}$$ where ${}^{C}\mathbf{t}_{AT-C}$ is the measured displacement in Create coordinates, ${}^{C}\mathbf{R}_{AT}$ is the measured orientation of the AprilTag with respect to the Create, and ${}^{W}\mathbf{R}_{AT}$ is the *a priori* known orientation of the AprilTag with respect to the world reference frame. Finally, $y_i\doteq{}^{W}\mathbf{t}_{AT-C}$ is used to compute the next control input $u$ following equation [\[u_limited\]](#u_limited){reference-type="eqref" reference="u_limited"}.

Finally, previous sections assumed a linear dynamical model for the robot, while the Create 2 has a unicycle dynamics. We map the original 2D input $u$ to a linear velocity $u_x$ along the $x$ axis of the robot and an angular velocity $\omega_z$ around the $z$ axis of the robot using a rather standard low-level controller:

$$\begin{align}
% Too long for just one row, I think split is best:
%fixed
u_x = \small{\dfrac{\alpha}{\left\| u \right\|}
\begin{bmatrix}
    \cos{\varphi} \\ \sin{\varphi}
  \end{bmatrix}}^\mathrm{T}u,&&
\omega_z = \small{\frac{\beta}{\left\| u \right\|} \begin{bmatrix}0\\0\\1\end{bmatrix}^\mathrm{T}\left(
                       \begin{bmatrix}
                         \cos{\varphi} \\ \sin{\varphi} \\ 0
                       \end{bmatrix}
  \times \begin{bmatrix}
    u \\ 0
  \end{bmatrix} \right)}
\end{align}$$ where $\varphi$ is the instantaneous yaw rotation of the robot with respect to the world reference frame, which is extracted from ${}^{C}\mathbf{R}_{AT}$ and ${}^{W}\mathbf{R}_{AT}$, and $\times$ represent the 3-D cross product; $\alpha$ and $\beta$ are user-defined scalar gains, 0.1 and 0.5 respectively.

Fig. [6](#fig:experiment-results){reference-type="ref" reference="fig:experiment-results"} depicts the real robot trajectories. Both in the original and deformed environments, the robot followed the edges of the `RRT`$^*$ tree and reached the expected goal for all starting positions and with the same control gains, despite the fact that the measurements were obtained with vision alone, and despite the different dynamics of the robot.

# CONCLUSIONS AND FUTURE WORKS {#sec:conclusions}

In this work, we introduced a new approach to integrate the high-level `RRT`$^*$ path planning with a low-level controller. We represented the environment via a simplified tree graph by implementing a modified sampling-based `RRT`$^*$ algorithm. We defined convex cells around the nodes of the tree and formulated a min-max robust Linear Program with CLF and CBF constraints to guarantee the stability and safety of the system. We built a robust output feedback controller for each cell which takes relative displacement measurements between a set landmarks positions and position of the robot as an input. We addressed the limited filed of view of the robot issue by reformulating a controller based on the visible landmarks. We validated our approach on both simulation environment and real-world environment and represented the robustness of our algorithm by applying the controller to a significantly deformed environment without replanning. We plan to prove the robustness of our algorithm theoretically and define the conditions of robustness of the controller in our future work. Furthermore, we plan to study the trade-off between optimal navigation and the robustness of the controller.

[^1]: This work was supported by ONR MURI N00014-19-1-2571 "Neuro-Autonomy: Neuroscience-Inspired Perception, Navigation, and Spatial Awareness"

[^2]: $^{1}$Division of Systems Engineering at Boston University, Boston, MA, 02215 USA. {`mahroobh@bu.edu}`

[^3]: $^{2}$Department of Mechanical Engineering at Boston University, Boston, MA, 02215 USA. M. Mitjans is additionally supported by "la Caixa" Foundation fellowship LCF/BQ/AA18/11680117. {`mmitjans@bu.edu}`

[^4]: $^{3}$Department of Mechanical and System Engineering.{`tron@bu.edu}`
