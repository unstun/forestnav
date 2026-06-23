---
citation_key: Garg2024Planning
arxiv_id: 2411.18913
arxiv_url: https://arxiv.org/abs/2411.18913
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:27:37Z
origin: ai+web
reviewed: false
---

Garg *et al.*: Undistorting Parametrized Configuration Spaces

::: IEEEkeywords
Motion and Path Planning, Optimization and Optimal Control, Bimanual Manipulation
:::

# Introduction {#sec:introduction}

motion planning is essential to developing and deploying robotic manipulation systems. Such systems need to produce efficient paths while obeying various constraints. Optimization-based motion planning, which minimizes an objective function while satisfying constraints, offers a powerful paradigm to solve this problem. The decision variables describe the robot's trajectory, the objective allows for choosing desired qualities in the solution, and constraints on these decision variables define obstacle avoidance, dynamic limits, and other interesting task-specific constraints such as coordinating arms in a bimanual system. However, the power of these techniques is tempered by the need to carefully formulate the optimization problems for reliability.

A manipulator's configuration space is often inherently nonconvex, and nonconvex trajectory optimization usually cannot guarantee optimality (due to local minima), or even feasibility. These guarantees are key to efficient and robust systems that can be used for repetitive motions in safety critical settings. To get a convex optimization formulation that allows for such guarantees, Graphs of Convex Sets (GCS) [@marcucci; @gcstrajopt] encodes the nonconvexities from obstacle avoidance as discrete decisions. Specifically, the inner approximation of planning or configuration space is represented as a series of intersecting collision free convex subsets. Then, constructing a graph (where vertices are a convex c-space set and edges connect intersecting sets) allows for searching discrete paths through these sets while simultaneously optimizing for the optimal continuous path within each set. Many relevant properties of the trajectory and its derivatives can be transcribed into convex costs and constraints [@gcstrajopt].

:::: {#fig:setup .figure latex-placement="t"}
![](Garg2024Planning_figs/hardware_setup.png){width="\\linewidth"}

![](Garg2024Planning_figs/7dof_setup_cropped.png){width="\\linewidth"}

::: caption
Experiments include constrained bimanual motion planning between shelves (top) and certifiable 7DoF KUKA iiwa tr no [aj]{style="color: black"} [aj]{style="color: black"} ectories between bins ( no [bottom]{style="color: black"} [bottom]{style="color: black"} ). The red path is the original result, and the blue path is our improved result.
:::
::::

no [When the configuration space does not admit finite Euclidean inner approximations, it may be possible under a change of coordinates. For example, end-effector constraints in bimanual robots such as two hands rigidly attached to the same object require planning on a nonlinear manifold in configuration space. Analytic inverse kinematics (IK) enables parameterizing convex sets on this manifold [@constrained_bimanual]. Planning over the space of 3D rotations using GCS requires a Euler angles parametrization [@ggcs_thesis §2.7.5]. Even in cases where c-space admits inner approximations, no [parameterization]{style="color: black"} [parameterization]{style="color: black"} can enable useful functionality or properties. For example, using the half tangent rational parametrization to write robot kinematics enables rigorous algebraic collision free certification [@ciris; @amice2023certifying].]{style="color: black"} [When the configuration space does not admit finite Euclidean inner approximations, it may be possible under a change of coordinates. For example, end-effector constraints in bimanual robots such as two hands rigidly attached to the same object require planning on a nonlinear manifold in configuration space. Analytic inverse kinematics (IK) enables parameterizing convex sets on this manifold [@constrained_bimanual]. Planning over the space of 3D rotations using GCS requires a Euler angles parametrization [@ggcs_thesis §2.7.5]. Even in cases where c-space admits inner approximations, no [parameterization]{style="color: black"} [parameterization]{style="color: black"} can enable useful functionality or properties. For example, using the half tangent rational parametrization to write robot kinematics enables rigorous algebraic collision free certification [@ciris; @amice2023certifying].]{style="color: black"}

no [While]{style="color: black"} [While]{style="color: black"} these parametrizations no [enable GCS to solve key robotics problems, they are also non-isometric]{style="color: black"} [enable GCS to solve key robotics problems, they are also non-isometric]{style="color: black"} ; the shortest path in the parametrized space may not be the shortest path in the configuration space. This distortion leads to suboptimal results when the convex objective used in the parametrized space is a weak approximation for the true objective. no [Handling nonconvex objectives in GCS]{style="color: black"} [Handling nonconvex objectives in GCS]{style="color: black"} , such as the true objective from the original space, gives more modeling freedom no [and widens]{style="color: black"} [and widens]{style="color: black"} the breadth of problems we can tackle.

no [This work's key contribution is using Projected Gradient Descent to optimize nonconvex objectives in a GCS setting.]{style="color: black"} [This work's key contribution is using Projected Gradient Descent to optimize nonconvex objectives in a GCS setting.]{style="color: black"} A gradient based solver guarantees local optimality around the initial guess if the objective is Lipschitz-continuous. We keep constraints convex, so a small convex program can project infeasible solutions back to feasibility. By exploiting structured nonconvexity, *our solver improves optimality of solutions while maintaining feasibility guarantees*.

For each of the three parametrizations mentioned earlier (bimanual IK, Euler angles, rational kinematics), we formulate and test a nonconvex objective against a convex surrogate in the GCS formulation. This nonconvex optimization is treated as a post-processing step, improving the best solution from GCS. Our method offers significant quantitative and qualitative improvements to motion plans across multiple experiments: path lengths and trajectory times shorten and visual artifacts of planning in the distorted parametrized space are undone. Expanding beyond just countering distortions, we also optimize over a general nonconvex cost, spatial curvature, to speed up bimanual trajectories.

In the rest of no [the]{style="color: black"} [the]{style="color: black"} paper, we review related work on nonconvex trajectory optimization and give necessary background on GCS and nonconvexity no [in GCS]{style="color: black"} [in GCS]{style="color: black"} . Then, we describe our methodology, relevant implementation details, and experimental setups. Finally, we no [show]{style="color: black"} [show]{style="color: black"} results, and conclude with a brief discussion of limitations of our work and potential directions for future research.

# Background and Related Work {#sec:related_work}

Sampling-based planners such as Probabilistic Roadmaps [@PRM] and Rapidly Exploring Random-Trees [@RRT] work very well in practice for kinematic planning problems. By growing finer approximations of the configuration space through sampling, they will eventually find a solution if one exists. Some methods, such as RRT$^{*}$[@rrtstar], can even achieve asymptotic optimality. However, these planners on their own struggle to handle more complex objectives.

Using optimization to solve for the entire trajectory enables more modeling freedom. Objectives can be used to prioritize choice qualities (such as distance or speed) and general constraints are essential for handling dynamics. Roboticists implement optimization based motion planning through a variety of different formulations, including direct collocation [@directcollocation], Augmented Lagrangian [@augmented_langrangian], and pseudo-spectral methods [@pseudo_spectral]. These transcriptions can then be solved using general purpose solvers such as SNOPT [@snopt] or gradient-based methods. For example, KOMO uses gradient descent on an Augmented Lagrangian transcription [@komo], and CHOMP uses covariant gradient descent [@chomp]. Nonconvexity will often be handled with clever initialization or stochasticity, such as in STOMP [@stomp]. cuRobo [@curobo_icra23] moves all constraints into the objective and leverages parallelization to simultaneously consider many initial guesses. Across all of these approaches, the formulation remains nonconvex, lacking feasibility or optimality guarantees.

## Graphs of Convex Sets {#sec:methodology:gcs}

Graph of Convex Sets (GCS) presents a new strategy for solving no [the shortest path problem]{style="color: black"} [the shortest path problem]{style="color: black"} with continuous and discrete decisions. Formally, a GCS is a graph, where each vertex $v$ has an associated continuous variable $x_v$ within a convex set $X_v$, and each edge $(u,v)$ is a convex function of $x_u$ and $x_v$. Finding the shortest path $\mathcal P$ through this graph can then be formulated as a Mixed Integer Convex Problem (MICP) with $\mathcal P$ and $x_v$ as decision variables [@marcucci §5].

no [GCS can be used to solve motion planning problems when given convex collision-free sets. These sets constitute the vertices of $\mathcal P$, and their union is an inner approximation of our planning space. The decision variable $x_v$ describes the continuous trajectory through the set $v$. As in GcsTrajOpt [@gcstrajopt], we define $x_v$ as the control points of a Bézier curve to parametrize the continuous trajectory.]{style="color: black"} [GCS can be used to solve motion planning problems when given convex collision-free sets. These sets constitute the vertices of $\mathcal P$, and their union is an inner approximation of our planning space. The decision variable $x_v$ describes the continuous trajectory through the set $v$. As in GcsTrajOpt [@gcstrajopt], we define $x_v$ as the control points of a Bézier curve to parametrize the continuous trajectory.]{style="color: black"} This choice admits convex path continuity and differentiability constraints, and no [guarantees]{style="color: black"} [guarantees]{style="color: black"} collision-avoidance of the whole trajectory [@gcstrajopt p.9]. GcsTrajOpt minimizes the distance between adjacent control points as a proxy for minimizing the length of the curve [@marcucci]. We use the same objective for the convex relaxation and any convex optimization we do.

The above discussion focuses only on the path, but in GcsTrajOpt, $x_v$ also has a time-scaling variable, $h$. no [We want to avoid nonconvex acceleration constraints that use this time parametrization variable.]{style="color: black"} [We want to avoid nonconvex acceleration constraints that use this time parametrization variable.]{style="color: black"} Instead, we use no [TOPP-RA (Time Optimal Path Parametrization based on Reachability Analysis) [@toppra]]{style="color: black"} [TOPP-RA (Time Optimal Path Parametrization based on Reachability Analysis) [@toppra]]{style="color: black"} to generate timed trajectories from our planned spatial paths. no [Any differentiable path can be navigated under acceleration constraints by slowing down, so using TOPP-RA maintains feasibility guarantees by keeping nonconvexity out of our constraints.]{style="color: black"} [Any differentiable path can be navigated under acceleration constraints by slowing down, so using TOPP-RA maintains feasibility guarantees by keeping nonconvexity out of our constraints.]{style="color: black"} So, for a collision free convex set $Q_i$, our vertices are of dimension $Q_i^{d+1}$ given Bézier curves of degree $d$ with $d+1$ control points.

## Parametrizing Configuration Space {#sec:backg:parametrization}

In some cases the configuration space benefits from being parametrized to enable building convex sets for GCS or generating collision free certificates. In this sub-section we review three such parametrizations and associated related works that apply GCS to manipulation motion planning problems. These parametrizations form the three main cases we will tackle with our method in the rest of the paper.

### IK and Constrained Bimanual Planning {#sec:backg:ik}

Constrained bimanual manipulation, no [or when]{style="color: black"} [or when]{style="color: black"} two robot arms move with a fixed transform between their end effectors, requires a equality constraint in task space. no [This non-linear inequality prevents us from using GCS on the $\mathbb{R}^{14}$ configuration manifold as it is. ]{style="color: black"} [This non-linear inequality prevents us from using GCS on the $\mathbb{R}^{14}$ configuration manifold as it is. ]{style="color: black"} Cohn et al. [@constrained_bimanual] use no [IK]{style="color: black"} [IK]{style="color: black"} to determine the joint angles of a subordinate robot given the end effector position of the leading arm. This parametrization collapses the $\mathbb{R}^{14}$ full joint space into an $\mathbb{R}^{8}$ space formed by the leading arm's joints and a redundancy factor (required to generate consistent joint angles for the subordinate arm). However, no [minimizing path length in the $\mathbb{R}^{8}$ only minimizes the path length for the leading arm and ignores the subordinate arm.]{style="color: black"} [minimizing path length in the $\mathbb{R}^{8}$ only minimizes the path length for the leading arm and ignores the subordinate arm.]{style="color: black"} As a result, paths visibly favor the leading arm.

### Euler Angles and GCS on $\mathop{\mathrm{SO}}(3)$ {#sec:backg:so3}

Planning over $\mathop{\mathrm{SO}}(3)$, the set of 3D rotations, is an important motion planning domain in robotics. As any roboticist knows, there are many different ways to represent rotations. Rotation matrices perfectly represent $\mathop{\mathrm{SO}}(3)$, but require bilinear constraints when included in optimization problems (constraints to ensure the validity of the Rotation matrix). Cohn et al. [@ggcs_thesis] explores different parametrizations to plan over rotations with GCS: Euler angles, axis-angle, and quaternions. The axis-angle and quaternion representations require piecewise-linear approximations, and also require solving two planning problems due to double cover of $\mathop{\mathrm{SO}}(3)$. Though Euler angles are quicker to plan over, the original work observes planning with Euler angles gives longer paths than the quaternion and axis-angle approximations. This discrepancy is due to the distortion of the underlying geometry of $\mathop{\mathrm{SO}}(3)$: distances get arbitrarily large when approaching gimbal lock.

### Rational Kinematics to Certify Collision Free {#sec:backg:rkin}

The forward kinematic mapping (needed for checking if a configuration is collision-free) is a trigonometric polynomial. Amice et al. [@ciris] no [write this nonconvex relationship as a]{style="color: black"} [write this nonconvex relationship as a]{style="color: black"} multi-linear polynomial, using the tangent half-angle substitution $s=\tan\frac{\theta}{2}$, further implying $$\sin(\theta)=(1-s^2)/(1+s^2),\; \cos(\theta)=(2s^2)/(1+s^2),$$ for $\theta\in(-\pi,\pi)$. no [Changing coordinates allows the formulation of Semi-Definite Programs (SDPs) to certify non-collision of regions in the robot's rational c-space with task space obstacles.]{style="color: black"} [Changing coordinates allows the formulation of Semi-Definite Programs (SDPs) to certify non-collision of regions in the robot's rational c-space with task space obstacles.]{style="color: black"} This certification can be done for individual convex sets [@ciris], or even an entire trajectory [@amice2023certifying].

:::: {#fig:stereo .figure latex-placement="t"}
![](Garg2024Planning_figs/stereo.png){width="\\textwidth"}

::: caption
A stereographic projection about $N$ projects the bottom of the black rectangle as being smaller than the top. An optimal distance planner operating in the post-projection (parametrized) space would favor the bottom despite the sides being equal in actuality. Image generated using [@animation-stereo].
:::
::::

The *rational* parametrization of kinematics, similar to the Stereographic Projection, is non-isometric. no [Most obviously]{style="color: black"} [Most obviously]{style="color: black"} when $\theta$ approaches $\pm \pi$, $\tan\frac{\theta}{2}$ asymptotically approaches to $\pm \infty$. This means that in the parametrized space, as joint values approach limits at $\pm \pi$, distances grow arbitrarily. More generally, equidistant points in the original space will be closer together in parametrized space no [near zero]{style="color: black"} [near zero]{style="color: black"} than the same points further away from zero. Therefore, a convex formulation of distance in the parametrized no [space]{style="color: black"} [space]{style="color: black"} will be inaccurate. Specifically, we expect if any joint is moving near $\pm \pi$ away from the point of stereographic projection, no [the]{style="color: black"} [the]{style="color: black"} paths planned will be sub-optimal due to no [distortion]{style="color: black"} [distortion]{style="color: black"} .

For all of these cases, convex objectives being minimized in GCS are in the parametrized spaces and therefore subject to the discussed pathologies. The planner clearly would benefit from the use of nonconvex objectives that represent no [the true objectives in the original space]{style="color: black"} [the true objectives in the original space]{style="color: black"} . This work bridges the gap between using nonconvex objectives and maintaining guarantees of GCS due to convexity.

## Nonconvexity and GCS

There is precedent for no [handling]{style="color: black"} [handling]{style="color: black"} nonconvexity in GCS or similar optimization frameworks. The original GcsTrajOpt preprint [@gcstrajopt_preprint] suggested using convex approximations to incorporate nonconvex objectives and constraints. In line with this suggestion, existing GCS works using the parametrizations from [2.2](#sec:backg:parametrization){reference-type="ref+Label" reference="sec:backg:parametrization"} use a convex surrogate objective to approximate the optimal solution. While this approach preserves convexity, the approximations are inherently heuristic and must be hand-designed. Moreover, optimizing for an approximation no [bounds]{style="color: black"} [bounds]{style="color: black"} the optimality of the solution by the quality of the approximation. The nuances of the approximations can also lead to systematic pathologies, such as the imbalance between arms in the bimanual planning domain.

Another approach is to no [use]{style="color: black"} [use]{style="color: black"} local convex approximations of the nonconvexity. Clark and Xie [@clark2023planning] suggest approximating the nonconvex costs using piecewise-linear approximations and creating smaller sets within which the objective is convex. This approach maintains convexity, but may scale poorly when dealing with complex objectives and finer approximations. Using a mix of biconvex alternation and local convex approximation, Fast Path Planning [@fpp] handles a bilinear in a similar set-up as GCS. The nonconvexity in this problem is contained to the constraints and is handled using alternation. The nonconvexity being a bilinear nonconvexity is key to enabling this method. Our work aims to enable a broader class of nonconvexity in the objective functions.

Enabling GCS to handle nonconvexity without approximation expands the method's applicability and improves solution quality. We restrict ourselves to nonconvexity in only the objective to improve motion planning results while maintaining guarantees. This restriction does prevent us from handling acceleration constraints, due to their nonconvexity in the GcsTrajOpt formulation. Von Wrangel [@davidthesis] presents specific strategies for handling certain common nonconvexities in GCS, including acceleration constraints. But the empirical success comes without strong guarantees.

# Methodology {#sec:methodology}

## Nonlinear Changes of Coordinates {#sec:methodology:nonlinearCoC}

Each of the parametrizations no [from]{style="color: black"} [from]{style="color: black"} [2.2](#sec:backg:parametrization){reference-type="ref+Label" reference="sec:backg:parametrization"} distort the robot's configuration space by introducing a nonlinear change of coordinates. More formally, each domain has a smooth (nonlinear) transformation $\alpha: Q \rightarrow C$ that maps $x$ from the more useful *parametrized space* $Q$ to a point $\alpha(x)$ in the original configuration space $C$. Each of the works used GCS to solve for a trajectory in $Q$, which then is remapped to $C$ using $\alpha$ to get an actual robot trajectory. However, since $\alpha$ is a nonlinear transformation, the minimum length no [path]{style="color: black"} [path]{style="color: black"} in $Q$ is not guaranteed to be the minimum length no [path]{style="color: black"} [path]{style="color: black"} in $C$.

The key limitation is that the convex path length cost in $Q$ can be arbitrarily far from the true objective: minimizing distance in $C$. Using $\alpha$ no [in the objective]{style="color: black"} [in the objective]{style="color: black"} enables changing coordinates back to the original space $C$ and defining a true (now nonconvex) objective, but the sets and constraints stay convex in the parametrized space $Q$.

For the constrained bimanual case, no [we define]{style="color: black"} [we define]{style="color: black"} $\alpha: \mathbb{R}^{8} \rightarrow \mathbb{R}^{14}$ is as the nonlinear analytic IK function with an original configuration space of both arms' joints ($\mathbb{R}^{14}$) and a parametrized space of one arm's joints and the self-motion of the other arm ($\mathbb{R}^{8}$). For planning over $\mathop{\mathrm{SO}}(3)$ with Euler angles, $\alpha: \mathbb{R}^{3} \rightarrow \mathbb{R}^{4}$ is the standard conversion from Euler angles to quaternions. For planning in the rational parametrization of kinematics, $\alpha$ is defined as $\theta=2\tan^{-1} s$.

## Formulating the Optimization {#sec:methodology:solver}

The nonconvex objective using $\alpha$ still needs to be expressed in terms of our decision variables $x_v$, the control points of the Bézier curve in $Q$. We cannot directly apply $\alpha$ on $x_v$ to define a distance objective as the remapped control points from $Q$ do not define a same Bézier curve in $C$. However, any points along the Bézier curve in $Q$ will still be along the same path in $C$, and any point along the Bézier curve is a convex combination of its control points. Therefore, a piecewise-linear approximation of the curve in $Q$ no [maps]{style="color: black"} [maps]{style="color: black"} to a piecewise-linear approximation in $C$ using $\alpha$.

The representative cost can then be the length of this piecewise-linear approximation. For the bimanual and rational configuration no [experiments, we]{style="color: black"} [experiments, we]{style="color: black"} sum the Euclidean distance between each adjacent pair of points in the full configuration space. For $\mathop{\mathrm{SO}}(3)$, we use the length of the Spherical Linear Interpolation (SLERP) path since the underlying geometry is a sphere. For better results, we square the length of each no [piece. This objective is better numerically for the optimizer and in the limit of an infinitely-fine discretization, it will both produce the same answer as a piecewise L2 norm [@riemanniangeo p.189]. For our experiments, using 10 samples per region to estimate the path strikes a good balance of accuracy and speed: a higher resolution approximation will be more accurate, but require more computational effort.]{style="color: black"} [piece. This objective is better numerically for the optimizer and in the limit of an infinitely-fine discretization, it will both produce the same answer as a piecewise L2 norm [@riemanniangeo p.189]. For our experiments, using 10 samples per region to estimate the path strikes a good balance of accuracy and speed: a higher resolution approximation will be more accurate, but require more computational effort.]{style="color: black"}

The GcsTrajOpt [@gcstrajopt] transcription with the original convex objective in the changed coordinates can be written no [as the following]{style="color: black"} [as the following]{style="color: black"} where $x_{ij}$ is the $j^{th}$ control point of the Bézier curve in set $Q_i$:

::: mini*
\|s\| \_i = 0\^v \_j = 0\^d \|\|x\_ij-x\_ij-1\|\|
:::

Our proposed optimization is:

::: mini*
\|s\| \_i = 0\^v \_k = 0\^10 f((x\_ik), (x\_ik-1))\^2
:::

where $x_{ik}$ is the $k^{th}$ sampled point in set $Q_i$ and $f(a, b)$ gives the distance between two points $a$ and $b$ in $C$. Note that both optimizations live in $Q$ with collision free sets $Q_i \subseteq Q$ but have different objectives. Thus, our optimization problem is specifically structured to isolate the nonconvexity in the objective function via the parametrization $\alpha$.

## Projected Gradient Descent

To exploit the aforementioned structure, we use *Projected Gradient Descent* (PGD) to maintain guarantees of feasibility and optimality. PGD is an iterative first-order or gradient-based solver with two parts: the gradient step and the projection back into feasibility. PGD steps in the direction of steepest decrease of the objective until a minimum is achieved. If any step yields an infeasible configuration, the solver projects the updated point back into feasible space. Because the constraints remain convex, the projection, a quadratic program finding the closest point in the set, solved with Mosek [@mosek], always returns a solution. Moreover, the convergence of PGD is well-understood if the multiplication factor of the negative gradient is less than or equal to the Lipschitz constant of our objective function [@lipschitz]. Our objective landscapes do not admit Lipschitz constants, but those that do can leverage this useful guarantee.

## Solver Performance

Beyond theoretical guarantees, certain implementation details further improve the performance of our solver.

### Initialization

As PGD finds local minimizers, the solution highly depends on the initialization. Within the GCS workflow, this initialization can come from two distinct candidates: after or during the rounding procedure (the step which projects the convex relaxation result to the near optimal discrete solution). no [Post-processing]{style="color: black"} [Post-processing]{style="color: black"} the solution after rounding is a great way to quickly improve a fixed discrete path in the parametrized space. We focus on this method, but one could also use this nonconvex optimization for each sampled path as an integral component of the rounding stage.

### Optimal Step Sizes

Our objectives are too complex to easily identify the Lipschitz constant and theoretically no [find]{style="color: black"} [find]{style="color: black"} a good step size. no [Classical PGD would then require manually tuning step size, so]{style="color: black"} [Classical PGD would then require manually tuning step size, so]{style="color: black"} we use the backtracking line search PGD [@backtracking], which searches for an optimal step size. It repeatedly halves an upper bound on the step size till the Armijo condition of sufficient decrease is met. This keeps the solver from overshooting minima while no [converging fast]{style="color: black"} [converging fast]{style="color: black"} .

### Gradient Precompilation

Initially, gradient computations were no [most]{style="color: black"} [most]{style="color: black"} of the runtime. Precompiling gradients with JAX [@jax] moves this time cost offline no [to speed]{style="color: black"} [to speed]{style="color: black"} up the PGD iterations. Compiling gradients for each vertex individually also allows us to re-use computations for no [start goal pair.]{style="color: black"} [start goal pair.]{style="color: black"}

### Affine Projections

With the gradients pre-compiled and checking for feasibility being fast because our feasible space can be expressed as a halfspace intersection, the majority of the time cost comes from the QP projection step. To reduce the number of QP solves and optimize for speed, we initially project onto the affine hull of the feasibility polyhedron. This projection satisfies any equality constraints such as path continuity and differentiability. This projection is much cheaper than the QP projection, since we can efficiently compute the affine hull. (All equality constraints are known explicitly, and the convex sets making up the GCS are positive volume, since they are produced by the IRIS-NP algorithm [@irisnp].) In some cases (especially with smaller step sizes), this projection will suffice to push the solution back into feasibility, saving time for the solver. If the point is still infeasible, the solver runs the full QP.

### Convergence Criteria

The solver tracks the moving average of the cost over the last 5 iterations, and terminates when the average changes by less than 0.5%. The moving average prevents us from terminating early; the cost occasionally jumps for a single iteration before continuing on a significant downward trend. For cases that do not converge, the solver terminates after a maximum of 70 iterations. We hypothesize this occurs when the projection step increases the cost too much, indicating a high Lipschitz constant. In practice for these experiments, optimizations that converged, typically converged well before 70 iterations.

## More general nonconvex objectives: Curvature {#sec:methodology:curvature}

So far the methodology has focused primarily on the special case of eliminating the distortion caused by non-isometric parametrizations. However, we can also optimize for any smooth nonconvex objective, expanding our modeling power. Some examples of useful nonconvex objectives would be minimizing curvature (or other higher-order path derivatives) or penalizing proximity to obstacles.

Penalizing the *curvature* of the path $$% \frac{\sqrt{|x'|^2|x''|^2 - (x' \cdot x'')^2}}{|x'|^{3}}
\kappa=\left(\left|\left|x'\right|\right|^{-3}\right)\sqrt{\left|\left|x'\right|\right|^2\left|\left|x''\right|\right|^2-\left(x'\cdot x''\vphantom{\left|\left|x'\right|\right|}\right)^2}$$ should help no [TOPP-RA]{style="color: black"} [TOPP-RA]{style="color: black"} produce better trajectories, as high curvature paths contain tight turns, that require a slower traversal to stay within acceleration limits. Although such paths might be longer than those produced by a pure shortest-path trajectory, they can be traversed more quickly.

We define this objective no [too]{style="color: black"} [too]{style="color: black"} over sampled points along the path defined by $x_v$. Given sampled points, we calculate the curvature of each point and then apply the RealSoftMax (a smooth maximum function) to approximate the maximum curvature of our paths. We expect paths under this optimization will have higher path length but lower no [duration]{style="color: black"} [duration]{style="color: black"} when time-parametrized by no [TOPP-RA]{style="color: black"} [TOPP-RA]{style="color: black"} .

# Experiments {#sec:experiments}

In this section, we detail the results collected on the three motion planning domains of interest: constrained bimanual, $\mathop{\mathrm{SO}}(3)$ with Euler angles, and rational kinematics. For all of our experiments, we solve the GCS problem with the original convex objective first and then run the projected gradient descent to improve the solution. Interactive recordings of all trajectories and other results are available online at <https://shrutigarg914.github.io/pgd-gcs-results/>

:::: {#fig:curvature .figure latex-placement="b"}
![](Garg2024Planning_figs/curvature.png){width="85%"}

::: caption
Optimizing jointly for curvature and distance yields quicker trajectories but longer distances--the curvature-regularized path is farther from the shelf.
:::
::::

## Constrained Bimanual Motion Planning

In this experiment, two iiwas navigate a shelf while keeping the transform between end effectors constant, as if they were jointly carrying an object as shown in [1](#fig:setup){reference-type="ref+Label" reference="fig:setup"}. We evaluate the PGD solver on the key start and goal pairs from [@constrained_bimanual] both on hardware and in simulation. The comparison of these benchmark paths before and after optimizing for the nonconvex objective is presented in [1](#tab:topmiddlebottom){reference-type="ref+Label" reference="tab:topmiddlebottom"}. The "GCS" column indicates using the convex $\mathbb{R}^{8}$ objective, the "Distance" column indicates using the nonconvex $\mathbb{R}^{14}$ objective, and the "Curvature + Distance" column indicates no [using a linear]{style="color: black"} [using a linear]{style="color: black"} combination of the nonconvex $\mathbb{R}^{14}$ objective and the nonconvex curvature cost with a ratio of 8 to 0.01 respectively. no [This ratio is a hand tuned parameter to compensate for the path distance objective being on the order of 100 times greater than the path curvature objective.]{style="color: black"} [This ratio is a hand tuned parameter to compensate for the path distance objective being on the order of 100 times greater than the path curvature objective.]{style="color: black"} While the $\mathbb{R}^{14}$ objective results in the shortest paths, regularizing for lower curvature lengthens paths, but shortens traversal times after no [TOPP-RA]{style="color: black"} [TOPP-RA]{style="color: black"} 's re-timing. Visually, minimizing this joint objective leads to more rounded paths, as shown in [3](#fig:curvature){reference-type="ref+Label" reference="fig:curvature"}.

To quantify the difference in distance traveled between the arms, we define the *imbalance* of a trajectory as $(d_s - d_c)/(d_s + d_c)$, where $d_c$ is the distance traveled by the controlled arm and $d_s$ is the distance traveled by the subordinate arm. When both arms travel comparable distances, the imbalance distribution centers around 0. When one arm travels much longer distributions than the other, the imbalance metric approaches $\pm1$ in magnitude. Table [1](#tab:topmiddlebottom){reference-type="ref" reference="tab:topmiddlebottom"} shows that this imbalance metric approaches 0 after post-processing under the $\mathbb{R}^{14}$ objective. In [4](#fig:pathlengthcomp){reference-type="ref+Label" reference="fig:pathlengthcomp"}, we see paths favour the leading arm less. no [The imbalance for jointly optimizing curvature and distance is higher than optimizing just the distance indicating that smoother paths are more imbalanced.]{style="color: black"} [The imbalance for jointly optimizing curvature and distance is higher than optimizing just the distance indicating that smoother paths are more imbalanced.]{style="color: black"} This asymmetry likely comes from the same-handedness of the iiwas.

For a more comprehensive analysis, we randomly sample 100 start and end points from the valid and reachable configuration space. Paths generated are on average 20.60% shorter in the $\mathbb{R}^{14}$ configuration space after applying our post-processing step. no [These paths take on average 31.02% less time to navigate.]{style="color: black"} [These paths take on average 31.02% less time to navigate.]{style="color: black"} The imbalance shifts towards 0, indicating that the paths for the subordinate arm are more comparable to the leading arm after the nonconvex optimization. These improvements took an average of 0.0554 seconds of compute (approximately 13.7 iterations) in addition to the 2.133 seconds that the surrogate convex optimization takes.

::: {#tab:topmiddlebottom}
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Top to Middle                                                                                                                                                                                                              |
+:================+:==============================================================:+:======================================================================:+:==============================================================:+
|                 | GCS                                                            | Distance                                                               | Distance + Curvature                                           |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Trajectory Time | 4.889                                                          | 3.469                                                                  | **3.243**                                                      |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| R14 Path Length | 4.241                                                          | **3.766**                                                              | 3.884                                                          |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Imbalance       | no [0.331]{style="color: black"} [0.331]{style="color: black"} | no [**0.117**]{style="color: black"} [**0.117**]{style="color: black"} | no [0.216]{style="color: black"} [0.216]{style="color: black"} |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Middle to Bottom                                                                                                                                                                                                           |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
|                 | GCS                                                            | Distance                                                               | Distance + Curvature                                           |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Trajectory Time | 5.326                                                          | 3.08                                                                   | **2.99**                                                       |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| R14 Path Length | 3.325                                                          | **3.175**                                                              | 3.247                                                          |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Imbalance       | no [0.162]{style="color: black"} [0.162]{style="color: black"} | no [**0.099**]{style="color: black"} [**0.099**]{style="color: black"} | no [0.110]{style="color: black"} [0.110]{style="color: black"} |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Top to Bottom                                                                                                                                                                                                              |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
|                 | GCS                                                            | Distance                                                               | Distance + Curvature                                           |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Trajectory Time | 7.48                                                           | 4.263                                                                  | **3.99**                                                       |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| R14 Path Length | 5.622                                                          | **5.048**                                                              | 5.13                                                           |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+
| Imbalance       | no [0.190]{style="color: black"} [0.190]{style="color: black"} | no [**0.084**]{style="color: black"} [**0.084**]{style="color: black"} | no [0.122]{style="color: black"} [0.122]{style="color: black"} |
+-----------------+----------------------------------------------------------------+------------------------------------------------------------------------+----------------------------------------------------------------+

: Optimizing over the nonconvex cost improves metrics for the three no [benchmark]{style="color: black"} [benchmark]{style="color: black"} trajectories.
:::

:::: {#fig:pathlengthcomp .figure latex-placement="t"}
![](Garg2024Planning_figs/imbalance.png){width="88%"}

::: caption
Paths become more centered no [as the nonconvex objective accounts for the distance traveled by both arms. The original convex objective just accounts for the controlled arm.]{style="color: black"} [as the nonconvex objective accounts for the distance traveled by both arms. The original convex objective just accounts for the controlled arm.]{style="color: black"}
:::
::::

80% of the runtime is solving QP projections. The affine projection is only useful when step size is fixed. When using backtracking to determine step size, the projection onto the affine hull is almost never sufficient. This observation indicates to us that at our boundary the gradients are consistently pointing outward. This is not unexpected, since the collision-avoidance constraints are active at the boundary, and moving closer to obstacles generally allows a shorter path length.

## Planning over $\mathop{\mathrm{SO}}(3)$

For our last experiment, we plan over random start and goal 3D rotations independent of a simulation or hardware set-up. To cover SO(3), we set up the same charts and convex regions as in [@ggcs_thesis] for the Euler angles, quaternions, and axis-angle parametrizations. The latter two use piecewise-linear approximations of the original $\mathop{\mathrm{SO}}(3)$ space and act as baselines. We run PGD on the Euler angles setting only. The Euler angles GCS graph is fully connected and optimizes Euclidean distance within each set, so the shortest path between any two points will be a linear path, regardless of the order of our Bézier curves. For time-efficiency, we generate order one GCS solutions and initialize the PGD solver with the control points evenly spaced along each line segment.

:::: {#fig:so3_experiment .figure latex-placement="tb"}
::: {#fig:trajt_comp .figure}
![image](Garg2024Planning_figs/annotated_so3_cropped.png){width="\\linewidth"} []{#fig:trajt_comp label="fig:trajt_comp"}
:::

::: caption
Comparing the distributions of relative error of paths with respect to the SLERP distance between start and goal orientations. The PGD significantly improves the results of the Euler angles parametrization.
:::
::::

Given there are no obstacles, SLERP gives the shortest path between any two orientations. We use it as the closed-form ground truth distance. [6](#fig:so3_experiment){reference-type="ref+Label" reference="fig:so3_experiment"} shows the distribution of relative error in path length for the three representations of $\mathop{\mathrm{SO}}(3)$ when planning across 125 random start and goal pairs, along with the PGD post-processing on the Euler angles paths. The distribution of error for Euler angles shifts significantly closer to 0 after running PGD. The relative error decreases by 42.5% on average. This improvement has a bimodal distribution: for some paths the PGD greatly improves the solution, but for others, there is little improvement to be made. The latter might be local minima, where the global optimal lies on a different discrete path.

These improvements on average no [take]{style="color: black"} [take]{style="color: black"} seconds no [in addition to ]{style="color: black"} [in addition to ]{style="color: black"} the 17.28 seconds no [taken]{style="color: black"} [taken]{style="color: black"} to generate the original solutions for Euler angles. Of this time, the solver only ran for 0.62 seconds. The remaining 3.46 seconds were no [spent re-using]{style="color: black"} [spent re-using]{style="color: black"} vertices and Bézier curves from the original solution and could be further optimized. Comparatively, planning with axis-angles no [takes]{style="color: black"} [takes]{style="color: black"} seconds. At a lower resolution quaternions take 16.73 seconds, but for higher resolutions, their solve time is on the order of minutes. no [Our method offers a way to generate more accurate paths using]{style="color: black"} [Our method offers a way to generate more accurate paths using]{style="color: black"} Euler angles while still being faster than the more accurate axis-angle and quaternion representations. no [Moreover, of the three, only Euler angles allow for using IRIS-NP [@irisnp] to grow collision-free regions in the presence of obstacles.]{style="color: black"} [Moreover, of the three, only Euler angles allow for using IRIS-NP [@irisnp] to grow collision-free regions in the presence of obstacles.]{style="color: black"}

## Rational Parametrizations of Robot Kinematics

We have two experimental settings in simulation that use the rational kinematics parametrization. One is a 3 degree-of-freedom iiwa (four of the joints are locked) that moves within a vertical 2D plane. The other is a 7 degree-of-freedom iiwa mounted on a table, as shown in [1](#fig:setup){reference-type="ref+Label" reference="fig:setup"}. The nominal position (i.e. point of projection) for both iiwas is when the arms stand straight up with all joint angles at 0. All the regions in the 3DoF case are certified to be completely collision-free using the Certified IRIS algorithm [@ciris]. All the trajectories in the 7DoF setting can be certified using [@amice2023certifying].

For the 3DoF planar iiwa, no [qualitatively]{style="color: black"} [qualitatively]{style="color: black"} the paths become less biased towards the point of projection: in [7](#fig:ciris_results){reference-type="ref+Label" reference="fig:ciris_results"}, the the PGD refinement no [reduces the]{style="color: black"} [reduces the]{style="color: black"} extraneous spike towards the nominal pose. Quantitatively, most paths no [show little]{style="color: black"} [show little]{style="color: black"} improvement across 100 random start and goal points among the shelves. On average, the paths get 0.2% shorter and most terminate within 7 iterations and 0.22 seconds. no [The example in Figure [7](#fig:ciris_results){reference-type="ref" reference="fig:ciris_results"} shows a 1.2% improvement in path length. Weaker numerical results are expected as the configuration space distorts most intensely near the joint limits, so the average case does not have much room for improvement.]{style="color: black"} [The example in Figure [7](#fig:ciris_results){reference-type="ref" reference="fig:ciris_results"} shows a 1.2% improvement in path length. Weaker numerical results are expected as the configuration space distorts most intensely near the joint limits, so the average case does not have much room for improvement.]{style="color: black"}

For the 7dof iiwa, the projected gradient descent on random paths in configuration space between the bins results in 3.89% shorter in path lengths and a 4.74% shorter trajectory times. When one or more joints travel near their limits, these improvements are higher. For example, [7](#fig:ciris_results){reference-type="ref+Label" reference="fig:ciris_results"} shows a trajectory that gets 10.8% shorter and 17.6% faster.

:::: {#fig:ciris_results .figure latex-placement="t"}
![](Garg2024Planning_figs/7dof_ciris_random_cropped.png){width="\\linewidth"}

![](Garg2024Planning_figs/3dof_ttb_cropped.png){width="\\linewidth"}

::: caption
The 3DoF iiwa (right) skews towards the nominal position in the original GCS solution (in red). The 7DoF iiwa (left) shows improvement in path before and after the post-processing for a random start and goal configuration.
:::
::::

# Discussion {#sec:discussion}

We have presented a method to solve GCS problems with nonconvex objectives, granting greater modeling freedom and yielding better motion plans. By keeping the constraints convex, we maintain the feasibility guarantees of GCS and avoid the inconsistency typical of nonconvex optimizations.

Our method is particularly effective when accounting for the distortion from nonlinear parametrizations of planning spaces. In constrained bimanual motion planning, our post-processing step produces paths that are more balanced between the arms, 20% shorter on average, and 31.02% faster after being time-parametrized. For Euler angles, the paths are 40% shorter on average. no [Beyond undistorting paths, the approach enables optimizing general nonconvex objectives such as curvature. For the bimanual setting, we find paths with greater curvature radii and quicker traversal. The lack of significant change in path length in the average for the rational kinematic case suggests that the distortion from the stereographic projection is not usually significant. Thus, planning in this parametrization of configuration space and enabling rigorous certification plausibly outweighs the minor cost increase. Even then, our method produces strong improvements in the worst case, and in the average case with little room for change, the solver terminates quickly.]{style="color: black"} [Beyond undistorting paths, the approach enables optimizing general nonconvex objectives such as curvature. For the bimanual setting, we find paths with greater curvature radii and quicker traversal. The lack of significant change in path length in the average for the rational kinematic case suggests that the distortion from the stereographic projection is not usually significant. Thus, planning in this parametrization of configuration space and enabling rigorous certification plausibly outweighs the minor cost increase. Even then, our method produces strong improvements in the worst case, and in the average case with little room for change, the solver terminates quickly.]{style="color: black"}

:::: {#fig:clutter .figure latex-placement="b"}
![](Garg2024Planning_figs/clutter_front.png){width="\\linewidth"}

![](Garg2024Planning_figs/clutter_back.png){width="\\linewidth"}

::: caption
no [A 7DoF iiwa reaching among shelves. Re-optimizing improves the path in the large region (in the top shelf), but shows minimal change for segments through smaller regions.]{style="color: black"} [A 7DoF iiwa reaching among shelves. Re-optimizing improves the path in the large region (in the top shelf), but shows minimal change for segments through smaller regions.]{style="color: black"}
:::
::::

An obvious limitation of the proposed method is added computation time. We use a Python based custom PGD; no [Commercial solvers, compiled languages, and performance optimization will speed up a mature implementation. This post-processing step will certainly be worth the additional runtime in cases like surgical robots that require strong guarantees and high quality. We have focused our numerical results on sparse environments. Our method works in dense clutter (see [8](#fig:clutter){reference-type="ref+Label" reference="fig:clutter"}) given IRIS regions generated using new methods that better scale with environment complexity [@iriszo]. But the regions are smaller, leaving less room for improvement. In many contexts, robots move through areas of dense and sparse clutter, and our method can improve segments in the sparser regions, without adding collisions or worsening the trajectory in the densely-cluttered areas.]{style="color: black"} [Commercial solvers, compiled languages, and performance optimization will speed up a mature implementation. This post-processing step will certainly be worth the additional runtime in cases like surgical robots that require strong guarantees and high quality. We have focused our numerical results on sparse environments. Our method works in dense clutter (see [8](#fig:clutter){reference-type="ref+Label" reference="fig:clutter"}) given IRIS regions generated using new methods that better scale with environment complexity [@iriszo]. But the regions are smaller, leaving less room for improvement. In many contexts, robots move through areas of dense and sparse clutter, and our method can improve segments in the sparser regions, without adding collisions or worsening the trajectory in the densely-cluttered areas.]{style="color: black"}

Future work no [could]{style="color: black"} [could]{style="color: black"} include larger scale parallelization, especially if we integrate our post-processing step into the rounding stage. cuRobo [@curobo_icra23] has shown incredible results by solving many nonconvex trajectory optimization problems in parallel. This step could also be used in an Anytime Motion Planning framework [@mishani2023constant] where the later parts of a trajectory are refined as the earlier parts are traversed. Another possibility is using the nonconvex objectives with incremental search methods such as GCS\* [@gcsstar] no [and Multi Query Shortest Path Problem in GCS [@mqspp].]{style="color: black"} [and Multi Query Shortest Path Problem in GCS [@mqspp].]{style="color: black"} Lastly, we no [work on]{style="color: black"} [work on]{style="color: black"} designing better convex surrogates which still play an important role during the convex relaxation and initialization stages. Under clearly deficient convex surrogates (such as in the original constrained bimanual case), one can try to hand-design a better surrogate or potentially generate them automatically using learning-based approaches.

[^1]: Manuscript received: November, 11, 2024; Revised February, 26, 2025; Accepted March, 30, 2025.

[^2]: This paper was recommended for publication by Editor Lucia Pallottino upon evaluation of the Associate Editor and Reviewers' comments. This work was supported by Amazon.com, PO No. 2D-06310236, Lincoln Labs, MIT EECS Advanced Undergraduate Research Opportunities Program (SuperUROP) and the National Science Foundation Graduate Research Fellowship Program under Grant No. 2141064.

[^3]: $^{1}$Computer Science and Artificial Intelligence Laboratory (CSAIL), Massachusetts Institute of Technology, 32 Vassar St, Cambridge, MA, 02139 `[sgrg,tcohn,russt]@mit.edu`

[^4]: Digital Object Identifier (DOI): see top of this page.
