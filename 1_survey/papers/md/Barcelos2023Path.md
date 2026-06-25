---
citation_key: Barcelos2023Path
arxiv_id: 2308.04071
arxiv_url: https://arxiv.org/abs/2308.04071
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:02:31Z
origin: ai+web
reviewed: false
---

# Introduction

Trajectory optimisation is one of the key tools in robotic motion, used to find control signals or paths in obstacle-cluttered environments that allow the robot to perform desired tasks. These trajectories can represent a variety of applications, such as the motion of autonomous vehicles or robotic manipulators. In most problems, we consider a *state-space model*, where each distinct situation for the world is called a *state*, and the set of all possible states is called the *state space* [@lavalle_planning_2006]. When optimising candidate trajectories for planning and control, two criteria are usually considered: *optimality* and *feasibility*. Although problem dependant, in general, the latter evaluates in a binary fashion whether the paths generated respect the constraints of both the robot and the task, such as physical limits and obstacle avoidance. Conversely, optimality is a way to measure the quality of the generated trajectories with respect to task-specific desired behaviours. For example, if we are interested in smooth paths we will search for trajectories that minimise changes in velocity and/or acceleration. The complexity of most realistic robot planning problems scales exponentially with the dimensionality of the state space and is countably infinite. When focusing on motion planning, a variety of algorithms have been proposed to find optimal and feasible trajectories. These can be roughly divided into two main paradigms: sampling-based and trajectory optimisation algorithms.

:::: {#fig:intro-image .figure latex-placement="t"}
![](Barcelos2023Path_figs/robot-kitchen-scenario.png){width=".8\\linewidth"}

::: caption
[]{#fig:intro-image label="fig:intro-image"} **An episode of the *Kitchen* scene.** Depicted is one of the collision-free paths found by SigSVGD on a reaching task using a 7 DOF Franka Panda arm on the MotionBenchMaker planning benchmark.
:::
::::

Sampling-based planning [@gammell_asymptotically_2021] is a class of planners with *probabilistically complete* and *asymptotically optimal* guarantees [@al-bluwi_motion_2012]. These approaches decompose the planning problem into a series of sequential decision-making problems with a tree-based [@lavalle_randomized_2001] or graph-based [@kavraki_probabilistic_1996; @jaillet_path_2008] approach. However, most approaches are limited in their ability to encode kinodynamic cost like trajectory curvature [@heilmeier_minimum_2020] or acceleration torque limits [@berntorp_models_2014]. In addition, despite the completeness guarantee, sampling-based planners are often more computationally expensive as the search space grows and can obtain highly varying results due to the random nature of the algorithms.

Trajectory optimisation algorithms [@gonzalez_review_2016] use different techniques to minimise a cost functional that encourages solutions to be both optimal and feasible. The most direct optimisation procedure relies on a differentiable cost function and uses functional gradient techniques to iteratively improve the trajectory quality [@ratliff_chomp_2009]. However, many different strategies have been proposed. For example, one may start from a randomly initialised candidate trajectory and proceed by adding random perturbations to explore the search space and generate approximate gradients, allowing any arbitrary form of cost functional to be encoded [@kalakrishnan_stomp:_2011]. The same approach can be used to search for control signals and a local motion plan concurrently [@williams_aggressive_2016]. Finally, a locally optimal trajectory can also be obtained via decomposing the planning problem with sequential quadratic programming [@schulman_finding_2013]. A drawback of these methods is that they usually find solutions that are locally optimal and may need to be run with different initial conditions to find solutions that are feasible or with lower costs.

Our goal with the present work is to propose a new trajectory optimisation method to improve path diversity. More specifically, we focus on a class of algorithms that perform trajectory optimisation parallel optimisation of a batch of trajectories. This concurrent optimisation of several paths in itself already alleviates the proneness to local minima, since many initial conditions are evaluated simultaneously. Nonetheless, we show how a proper representation of trajectories when performing functional optimisation leads to increased diversity and solutions with a better global property, either with direct gradients or Monte Carlo-based gradient approximations. As an illustrative example, refer to [2](#fig:2d_planning){reference-type="ref+label" reference="fig:2d_planning"}.

Our approach is based on two cornerstones. On one hand, we use a modification of Stein Variational Gradient Descent (SVGD) [@liu_stein_2016], a variational inference method to approximate a posterior distribution with an empirical distribution of sampled particles, to optimise trajectories directly on a structured Reproducing Kernel Hilbert Space (RKHS).

The structure of this space is provided by the second pillar of our approach. We leverage recent advancements in rough path theory to encode the sequential nature of paths in the RKHS using a Path Signature Kernel [@kiraly_kernels_2019; @salvi_signature_2021]. Therefore we can approximate the posterior distribution over optimal trajectories with structured particles during the optimisation while still taking into account motion planning and control idiosyncrasies.

More concretely, the main contributions of this paper are listed below:

- We introduce the use of path signatures [@lyons_rough_2014] as a canonical feature map to represent trajectories over high-dimensional state spaces;

- Next, we outline a procedure to incorporate the signature kernel into a variational inference framework for motion planning;

- Finally, we demonstrate through experiments in both planning and control that the proposed procedure results in more diverse trajectories, which aid in avoiding local minima and lead to a better optimisation outcome.

The paper is organised as follows. In [2](#sec:related){reference-type="ref+Label" reference="sec:related"} we review related work, contrasting the proposed method to the existing literature. In [3](#sec:background){reference-type="ref+Label" reference="sec:background"} we provide background on path signatures and motion planning as variational inference, which are the foundational knowledge for the method outlined in [4](#sec:method){reference-type="ref+Label" reference="sec:method"}. Finally, in [5](#sec:results){reference-type="ref+Label" reference="sec:results"} we present a number of simulated experiments, followed by relevant discussions in [6](#sec:conclusion){reference-type="ref+Label" reference="sec:conclusion"}.

# Related Work {#sec:related}

![ **Qualitative analysis of 2D planning task.** The plot shows the final 20 trajectories found with different optimisation methods. The colour of each path shows its normalised final cost. Note how all batch gradient descent trajectories converge to two modes of similar cost. Paths found by SVMP are already more diverse, but one of the gradient descent modes is lost. Note how when multiple trajectories converge to a single trough, the knots are pushed away by the repulsive force resulting in suboptimal solutions. Conversely, paths found by SigSVGD are diverse and able to find more homotopic solutions, including those found by BGD. Note also how paths are able to converge to the same trough without being repelled by one another since the repulsive force takes into account the entire trajectory and not exclusively the spline knot placement. That also allows for paths that are more direct and coordinated than SVMP. ](Barcelos2023Path_figs/obstacle_planning.png){#fig:2d_planning width="\\linewidth"}

Trajectory optimisation refers to a class of algorithms that start from an initial sub-optimal path and find a, possibly local, optimal solution by minimising a cost function. Given its broad definition, there are many seminal works in the area. One influential early work is Covariant Hamiltonian Optimisation for Motion Planning (CHOMP) [@ratliff_chomp_2009] and related methods [@zucker_chomp_2013; @byravan_space-time_2014; @marinho_functional_2016]. The algorithm leverages the covariance of trajectories coupled with Hamiltonian Monte Carlo to perform annealed functional gradient descent. However, one of the limitations of CHOMP and related approaches is the need for a fully-differentiable cost function.

In Stochastic Trajectory Optimisation for Motion Planning (STOMP) [@kalakrishnan_stomp:_2011] the authors address this by approximating the gradient from stochastic samples of noisy trajectories, allowing for non-differentiable costs. Another approach used in motion planning are quality diversity algorithms, at the intersection of optimisation and evolutionary strategies, of which Covariance Matrix Adaptation Evolution Strategy (CMA-ES) is the most prominent [@hansen_reducing_2003; @hamalainen_ppo-cma_2020; @tjanaka_training_2022]. CMA-ES is a derivative-free method that uses a multivariate normal distribution to generate and update a set of candidate solutions, called individuals. The algorithm adapts the covariance matrix of the distribution based on the observed fitness values of the individuals and the search history, balancing exploration and exploitation of the search space. Because of its stochastic nature, it is ergodic and copes well with multi-modal problems. Nonetheless, it may require multiple initialisations and it typically requires more evaluations than gradient-based optimisers [@hansen_cma_2016].

TrajOpt [@schulman_finding_2013], another prominent planner, adopts a different approach solving a sequential quadratic program and performing continuous-time collision checking. Contrary to sampling-based planners, these trajectory optimisation methods are fast, but only find locally optimal solutions and may require reiterations until a feasible solution is found. Another issue common to these approaches is that in practice they require a fixed and fine parametrisation of trajectory waypoints to ensure feasibility and smoothness, which negates the benefit of working on continuous trajectory space. To address this constraint, in [@marinho_functional_2016] the authors restrict the optimisation and trajectory projection to an RKHS with an associated squared-exponential kernel. However, the cost between sparse waypoints is ignored and the search is still restricted to a deterministic trajectory. Another approach was proposed in GPMP [@dong_motion_2016; @mukadam_simultaneous_2017; @mukadam_continuous-time_2018] by representing trajectories as Gaussian Processes (GP) and looking for a *maximum a posteriori* (MAP) solution of the inference problem.

More closely related to our approach are [@lambert_entropy_2021; @yu_gaussian_2022] which frame motion planning as a variational inference problem and try to estimate the posterior distribution represented as a set of trajectories. In [@yu_gaussian_2022], the authors modify GPMP with a natural gradient update rule to approximate the posterior. On the other hand, in Stein Variational Motion Planning (SVMP) [@lambert_entropy_2021] the posterior inference is optimised using Stein variational gradient descent. This method is similar to ours, but the induced RKHS does not take into account the sequential nature of the paths being represented, which leads to a diminished repulsive force and lack of coordination along the dimensions of the projected space.

In contrast, our approach---which we will refer to as Kernel Signature Variational Gradient Descent (SigSVGD)---uses the path signature to encode the sequential nature of the functional being optimised. We argue that this approach leads to a better representation of trajectories promoting diversity and finding better local solutions. To empirically corroborate this claim we use the Occam's razor principle and take SVMP as the main baseline of comparison since it more closely approximates our method.

We note that the application of trajectory optimisation need not be restricted to motion planning. By removing the constraint of a target state and making the optimisation process iterative over a rolling horizon we retrieve a wide class of Model Predictive Controllers with applications in robotics [@williams_aggressive_2016; @barcelos_disco_2020; @barcelos_dual_2021; @lambert_stein_2020]. Stein Variational MPC (SVMPC) [@lambert_stein_2020] uses variational inference with SVGD optimisation to approximate a posterior over control policies and more closely resembles SigSVGD. However, like SVMP, it too does not take into account the sequential nature of control trajectories and we will illustrate how our approach can improve the sampling of the control space and promote better policies.

# Background {#sec:background}

![[]{#fig:pathsig_invariance label="fig:pathsig_invariance"} **Signature invariance to reparametrisation.** *Left*: Plot of the coordinates of a two dimensional path $P_{t}$ over time. Here $P_{t}^{1} = \cos (8.5 t)$ and $P_{t}^{2} = t$. *Centre*: Plot of the two coordinates of path $P_{t}$ reparameterised by function $\psi$. Now, $P_{\psi(t)}^{1} = \cos (8.5 t^{4})$ and $P_{\psi(t)}^{2} = t^{4}$. *Right*: Plots of path $P_{t}$ and its reparameterised version $P_{\psi(t)}$ are shown overlapping to illustrate how the change in time is irrelevant if the goal is achieving diverse paths. The signature of degree 2 for both paths is $\{1, -1.6,  1,  1.3, -0.9, -0.7,  0.5\}$. ](fig/pathsig_invariance.pdf){#fig:pathsig_invariance}

## Trajectory Optimisation in Robotics {#sec:prelim}

Consider a system with state ${\boldsymbol{\mathbf{x}}}\in {\mathcal{\MakeUppercase{X}}}$ and let us denote a *trajectory* of such system as $\MakeUppercase{x}: [a, b] \to {\mathcal{\MakeUppercase{X}}}$, where ${\mathcal{\MakeUppercase{X}}}$ is an appropriate Euclidean space or group. We shall use the notation $\MakeUppercase{x}_{t}$ to denote the dependency on time $t \in [a, b]$. The trajectory $\MakeUppercase{x}$ describes a *path* in ${\mathcal{\MakeUppercase{X}}}$ and we shall use the two denominations interchangeably. In trajectory optimisation the goal is to find the optimal path $\MakeUppercase{x}^{*}$ from a given starting state ${\boldsymbol{\mathbf{x}}}_{s}$ to a certain goal state ${\boldsymbol{\mathbf{x}}}_{g}$. This can be done by minimising a cost functional that codifies our desired behaviour $\costFn \colon {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\to \mathbb{\MakeUppercase{R}}^{+}$, where ${\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}$ is the Hilbert space of trajectories [@king_pregrasp_2013]: $$\begin{equation}
\label{eq:traj_optim_prob}
    \MakeUppercase{x}^{*} \coloneqq \operatornamewithlimits{\arg\min}_{\MakeUppercase{x}} \costFn[\MakeUppercase{x}],
    \text{~s.t.~} \MakeUppercase{x}_a= {\boldsymbol{\mathbf{x}}}_{s}\; \textup{and} \; \MakeUppercase{x}_b= {\boldsymbol{\mathbf{x}}}_{g}.
\end{equation}$$ Typically, $\costFn$ is a bespoke functional that includes penalties for trajectory non-smoothness, total energy, speed and acceleration tracking, as well as length. To ensure that the solution is feasible and collision-free, additional equality and inequality constraints may also be included [@schulman_finding_2013]. Alternatively, we can solve an unconstrained problem and include additional penalties to the cost functional as soft-constraints [@zucker_chomp_2013; @ratliff_chomp_2009].

Finally, we draw the reader's attention to the fact that the problem stated in [\[eq:traj_optim_prob\]](#eq:traj_optim_prob){reference-type="ref+label" reference="eq:traj_optim_prob"} can be viewed as an open-loop optimal control problem. If the solution can be found in a timely manner, the same problem can be cast onto a Model Predictive Control [@camacho_model_2013; @barcelos_disco_2020; @barcelos_dual_2021] framework $$\begin{equation}
\label{eq:control_prob}
    \MakeUppercase{u}^{*} \coloneqq \operatornamewithlimits{\arg\min}_{\MakeUppercase{u}} \costFn[\MakeUppercase{x}, \MakeUppercase{u}],
    \text{~s.t.~} \MakeUppercase{x}_a= {\boldsymbol{\mathbf{x}}}_{s},
\end{equation}$$ where $\MakeUppercase{u}: [a, b] \to {\mathcal{\MakeUppercase{U}}}$ is a path of control inputs on a given Euclidean space and the mapping to ${\mathcal{\MakeUppercase{X}}}$ is given by the dynamical system $\transFn$ such that $\dot{{\boldsymbol{\mathbf{x}}}} = \transFn ({\boldsymbol{\mathbf{x}}}, {\boldsymbol{\mathbf{u}}}, t)$. That is to say, we now influence the path $\MakeUppercase{x}$ indirectly through input $\MakeUppercase{u}$, and at any time $t$ the problem is solved for a finite interval. The closed-loop solution arises from applying only the first immediate control action before re-optimising the solution.

## Path Signature {#sec:pathsig}

A multitude of practical data streams and time series can be regarded as a path, for example, video, sound, financial data, control signals, handwriting, etc. The path signature transforms such multivariate sequential data (which may have missing or irregularly sampled values) into an infinite-length series of real numbers that uniquely represents a trajectory through Euclidean space. Although formally distinct and with notably different properties, one useful intuition is to think of the signature of a path as akin to a Fourier transform, where paths are summarised by an infinite series of feature space coefficients. Consider a path $\MakeUppercase{x}$ traversing space ${\mathcal{\MakeUppercase{X}}}\subseteq \mathbb{\MakeUppercase{R}}^{c}$ as defined in [3.1](#sec:prelim){reference-type="ref+label" reference="sec:prelim"}. Note that at any time $t$ such path can be decomposed in $\MakeUppercase{x}_{t} = \left\{ \MakeUppercase{x}_{t}^{1}, \MakeUppercase{x}_{t}^{2}, \ldots, \MakeUppercase{x}_{t}^{c} \right\}$. Now recall that for a one-dimensional path $\MakeUppercase{x}_{t}$ and a function $\anyfunction$, the path integral of $\anyfunction$ along $\MakeUppercase{x}$ is defined by: $$\begin{equation}
\label{eq:path_integral}
    \int_{a}^{b} \anyfunction (\MakeUppercase{x}_{t}) {\operatorname{d}}\MakeUppercase{x}_{t} = \int_{a}^{b} \anyfunction (\MakeUppercase{x}_{t}) \dot{\MakeUppercase{x}_{t}} {\operatorname{d}}t .
\end{equation}$$

In particular, note that the mapping $t \to \anyfunction (\MakeUppercase{x}_t)$ is also a path. In fact, [\[eq:path_integral\]](#eq:path_integral){reference-type="ref+label" reference="eq:path_integral"} is an instance of the Riemann-Stieltjes integral [@chevyrev_primer_2016], which computes the integral of one path against another. Let us now define the *1-fold iterated* integral, which computes the increment of the $i$-th coordinate of the path at time $t$ as: $$\begin{equation}
    {\signature*[\MakeUppercase{x}]}_{t}^{i} =
    \int\limits_{\mathclap{a< t_1 < t}} {\operatorname{d}}\MakeUppercase{x}_{t_1}^{i} =
    \MakeUppercase{x}_{t}^{i} - \MakeUppercase{x}_{a}^{i} ,
\end{equation}$$ and we again emphasise that ${\signature[\MakeUppercase{x}]}_{t}^{i}$ is also a real valued path. This allows us to apply the same iterated integral recursively and we proceed by defining the *2-fold iterated* integral [@chen_iterated_1954; @chen_iterated_1977] as: $$\begin{equation}
    {\signature*[\MakeUppercase{x}]}_{t}^{i, j} = \int\limits_{\mathclap{a< t_2 < t}}
    {\signature*[\MakeUppercase{x}]}_{ t_2}^{i} {\operatorname{d}}\MakeUppercase{x}_{t_2}^{j} =
    \int\limits_{\mathclap{a< t_1 < t_2 < t}} {\operatorname{d}}\MakeUppercase{x}_{t_1}^{i} {\operatorname{d}}\MakeUppercase{x}_{t_2}^{j} .
\end{equation}$$ Informally, we can proceed indefinitely and we retrieve the path signature by collecting all iterated integrals of the path $\MakeUppercase{x}$. A geometric intuition of the signature can be found in [@chevyrev_primer_2016; @yang_developing_2017] where the first three iterated integrals represent displacement, the Lévy area [@lyons_differential_2007] and volume of the path respectively.

::: definition
**Definition 1** (Signature [@chevyrev_primer_2016]). *The *signature* of a path $\MakeUppercase{x}: t \in [a, b] \to \mathbb{\MakeUppercase{R}}^{c}$, denoted by ${\signature[\MakeUppercase{x}]}_{t}$, is the infinite series of all iterated integrals of $\MakeUppercase{x}$. Formally, ${\signature[\MakeUppercase{x}]}_{t}$ is the sequence of real numbers $$\begin{equation}
        {\signature*[\MakeUppercase{x}]}_{t} = \bigl(
            1, {\signature*[\MakeUppercase{x}]}_{t}^{1}, \ldots, {\signature*[\MakeUppercase{x}]}_{t}^{c},
            {\signature*[\MakeUppercase{x}]}_{t}^{1, 1}, {\signature*[\MakeUppercase{x}]}_{t}^{1, 2}, \ldots  
        \bigr) ,
\end{equation}$$ where the iterated integrals are defined as: $$\begin{equation}
        {\signature*[\MakeUppercase{x}]}_{t}^{i_{1}, \ldots, i_{k}} = \int\limits_{a< t_{k} < t}
        \ldots \int\limits_{{a< t_{1} < t_{2}}} {\operatorname{d}}\MakeUppercase{x}_{t_1}^{i_{1}} \ldots 
        {\operatorname{d}}\MakeUppercase{x}_{t_k}^{i_k} ,
\end{equation}$$ and the superscripts are drawn from the set ${\mathcal{\MakeUppercase{M}}}$ of all multi-indexes, $$\begin{equation}
        {\mathcal{\MakeUppercase{M}}} = \bigl\{ (i_1, \ldots, i_k) \mid k\geq 1, i_1, \ldots, i_k\in \{ 1, \ldots, c\}   \bigr\}.
\end{equation}$$*
:::

In practice we often apply a truncated signature up to a degree $d$, that is ${\signature^{d}[\MakeUppercase{x}]}_{t}$, defined as the finite collection of all terms of the signature up to multi-indices of length $d$.

The path signature was originally introduced by Chen [@chen_integration_1958] who applied it to piecewise smooth paths and further developed by Lyons and others [@amendola_varieties_2019; @boedihardjo_signature_2016; @hambly_uniqueness_2010; @lyons_rough_2014]. The number of elements in the path signature depends on the dimension of the input $c$ and the degree $d$, and is given by $c^{d}$. Therefore the time and space scalability of the signature is rather poor ($O(c^d)$), but this can be alleviated with the use of kernel methods as we will discuss in [4](#sec:method){reference-type="ref+label" reference="sec:method"}. The signature of a path has several interesting properties which make it inherently interesting for applications in robotics.

### Canonical feature map for paths: {#canonical-feature-map-for-paths .unnumbered}

For all effects, the path signature can be thought of as a *linear* feature map [@fermanian_embedding_2021] that transforms multivariate sequential data into an infinite length series of real numbers which uniquely represents a trajectory through Euclidean space. This is valid even for paths with missing or irregularly sampled values [@boedihardjo_signature_2016; @hambly_uniqueness_2010].

### Time-reversal: {#time-reversal .unnumbered}

We informally define the time-reversed path $\overleftarrow{\MakeUppercase{x}}$ as the original path $\MakeUppercase{x}$ moving backwards in time. It follows that the tensor product of the signatures ${\signature[\MakeUppercase{x}]}_{a,b} \otimes {\signature[\overleftarrow{\MakeUppercase{x}}]}_{a,b} = 1$, which is the identity operation.

### Uniqueness: {#uniqueness .unnumbered}

The signature of every non tree-like path is unique [@hambly_uniqueness_2010]. A tree-like path is one in which a section exactly retraces itself. Tree-like paths are quite common in real data (e.g. in cyclic actions) and this could be a limiting factor of the signature's application. However, it has been proven [@hambly_uniqueness_2010] that if a path has at least one monotonous coordinate, then its signature is unique. The main significance of this result is that it provides a practical procedure to guarantee signature uniqueness by, for example, including a time dimension.

### Invariance under reparametrisation: {#invariance-under-reparametrisation .unnumbered}

An important difficulty when vying for diversity in trajectory optimisation is the potential symmetry present in the data. This is particularly true when dealing with sequential data, such as, for instance, trajectories of an autonomous vehicle. In this case, the problem is compounded as there is an infinite group of symmetries given by the reparametrisation of a path (i.e. continuous surjections in the time domain to itself), each leading to distinct similarity metrics. In contrast, the path signature acts as a filter that is invariant to reparametrisation removing these troublesome symmetries and resulting in the same features as shown in [3](#fig:pathsig_invariance){reference-type="ref+Label" reference="fig:pathsig_invariance"}.

### Dimension is independent of path length: {#dimension-is-independent-of-path-length .unnumbered}

The final property we will emphasise is how the dimension of the signature depends on its degree and the intrinsic dimension of the path, but is independent of the path length. In other words, the signature dimension is invariant to the degree of discretisation of the path.

## Stein Variational Gradient Descent {#sec:svgd}

Variational inference (VI) [@blei_variational_2017] is an established and powerful method for approximating challenging posterior distributions in Bayesian Statistics. As opposed to Markov chain Monte Carlo (MCMC) [@haugh_tutorial_2021] approaches, in VI the inference problem is cast as an optimisation problem in which a candidate distribution $\qPdf^{*}[{\boldsymbol{\mathbf{x}}}]$ within a distribution family ${\mathcal{\MakeUppercase{Q}}}$ is chosen to best approximate the target distribution $\pPdf[{\boldsymbol{\mathbf{x}}}]$. This is typically obtained by minimising the Kullback-Leibler (KL) divergence: $$\begin{equation}
 \label{eq:vi_obj}
    \qPdf^{*} = \operatornamewithlimits{\arg\min}_{\qPdf \in {\mathcal{\MakeUppercase{Q}}}} \
    D_\mathrm{KL} \bigl(\qPdf||\pPdf\bigr) .
\end{equation}$$ The solution also maximises the Evidence Lower Bound (ELBO), as expressed by the following objective $$\begin{equation}
    \qPdf^{*} = \operatornamewithlimits{\arg\max}_{\qPdf \in {\mathcal{\MakeUppercase{Q}}}}
    \expectation_{\qPdf}[\big][\log \pPdf[{\boldsymbol{\mathbf{x}}}]]
    - D_\mathrm{KL} \bigl(\qPdf[{\boldsymbol{\mathbf{x}}}]||\pPdf[{\boldsymbol{\mathbf{x}}}]\bigr) .
\end{equation}$$

The main challenge that arises is defining an appropriate ${\mathcal{\MakeUppercase{Q}}}$. Stein variational gradient descent (SVGD) [@liu_stein_2016] addresses this issue while also solving for [\[eq:vi_obj\]](#eq:vi_obj){reference-type="ref+label" reference="eq:vi_obj"} by performing Bayesian inference in a non-parametric nature, removing the need for assumptions on restricted parametric families for $\qPdf [{\boldsymbol{\mathbf{x}}}]$. This approach approximates a posterior $\pPdf [{\boldsymbol{\mathbf{x}}}]$ with a set of particles ${\{{\boldsymbol{\mathbf{x}}}^i\}}_{i= 1}^{N_{p}}$, ${\boldsymbol{\mathbf{x}}}\in \mathbb{\MakeUppercase{R}}^{p}$. These particles are iteratively updated in parallel according to: $$\begin{equation}
\label{eq:stein_update}
    {\boldsymbol{\mathbf{x}}}^{i} \leftarrow {\boldsymbol{\mathbf{x}}}^{i} + 
    \epsilon\scoreFunc^{*}[{\boldsymbol{\mathbf{x}}}^{i}],
\end{equation}$$ given a step size $\epsilon$. The function $\scoreFunc[\cdot]$ is known as the score function and defines the velocity field that maximally decreases the KL-divergence: $$\begin{equation}
\label{eq:stein_optim}
    \scoreFunc^{*} = 
    \operatornamewithlimits{\arg\max}_{\scoreFunc \in {\mathcal{\MakeUppercase{H}}}}~\bigl\{
        -\grad_{\epsilon} D_\mathrm{KL} \bigl(\qPdf_{[\epsilon\scoreFunc]}||\pPdf\bigr),
        \text{~s.t.~} \|\scoreFunc\|_{{\mathcal{\MakeUppercase{H}}}} \leq 1
    \bigr\},
\end{equation}$$ where ${\mathcal{\MakeUppercase{H}}}$ is a Reproducing Kernel Hilbert Space (RKHS) induced by a positive-definite kernel $k:{\mathcal{\MakeUppercase{X}}}\times{\mathcal{\MakeUppercase{X}}}\to\mathbb{\MakeUppercase{R}}$, and $\qPdf_{[\epsilon\scoreFunc]}$ indicates the particle distribution resulting from taking an update step as in [\[eq:stein_update\]](#eq:stein_update){reference-type="ref+label" reference="eq:stein_update"}. Recall that an RKHS ${\mathcal{\MakeUppercase{H}}}$ associated with a kernel $k$ is a Hilbert space of functions endowed with an inner product $\inner{\cdot}{\cdot}$ such that $f({\boldsymbol{\mathbf{x}}}) = \inner{f}{k(\cdot, {\boldsymbol{\mathbf{x}}})}$ for any $f \in {\mathcal{\MakeUppercase{H}}}$ and any ${\boldsymbol{\mathbf{x}}}\in{\mathcal{\MakeUppercase{X}}}$ [@scholkopf_learning_2002]. In [@liu_stein_2016], the problem in [\[eq:stein_optim\]](#eq:stein_optim){reference-type="eqref" reference="eq:stein_optim"} has been shown to yield a closed-form solution which can be interpreted as a functional gradient in ${\mathcal{\MakeUppercase{H}}}$ and approximated with the set of particles: $$\begin{equation}
 \label{eq:stein_score_func}
    \scoreFunc^{*} [{\boldsymbol{\mathbf{x}}}] = \expectation_{{\boldsymbol{\mathbf{y}}}\sim \hat{\qPdf}} [\big]
    [k \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}} \grad_{{\boldsymbol{\mathbf{y}}}} \log \pPdf[{\boldsymbol{\mathbf{y}}}] + \grad_{{\boldsymbol{\mathbf{y}}}} k \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}}],
\end{equation}$$ with $\hat{\qPdf} = \frac{1}{N_{p}} \sum_{i= 1}^{N_{p}} \delta\lparen{\boldsymbol{\mathbf{x}}}^{i}\rparen$ being an empirical distribution that approximates $\qPdf$ with a set of Dirac delta functions $\delta\lparen{\boldsymbol{\mathbf{x}}}^{i}\rparen$. For SVGD, $k$ is typically a translation-invariant kernel, such as the squared-exponential or the Matérn kernels [@liu_stein_2016; @rasmussen_gaussian_2006].

# Method {#sec:method}

Our main goal is to find a diverse set of solutions to the problem presented in [3.1](#sec:prelim){reference-type="ref+label" reference="sec:prelim"}. To that end, we begin by reformulating [\[eq:traj_optim_prob\]](#eq:traj_optim_prob){reference-type="ref+label" reference="eq:traj_optim_prob"} as a probabilistic inference problem. Next, we show that we can apply SVGD to approximate the posterior distribution of trajectories with a set of sampled paths. Finally, in [4.3](#sec:sig_svgd){reference-type="ref+label" reference="sec:sig_svgd"}, we present our main contribution discussing how we can promote diversity among the sample paths by leveraging the Path Signature Kernel.

## Stein Variational Motion Planning {#sec:svgd_mp}

To reframe the trajectory optimisation problem described in [\[eq:traj_optim_prob\]](#eq:traj_optim_prob){reference-type="ref+label" reference="eq:traj_optim_prob"} as probabilistic inference we introduce a binary optimality criterion, $\mathcal{O}: {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\to \{0, 1\}$, analogously to [@barcelos_dual_2021; @levine_reinforcement_2018]. Simplifying the notation with $\mathcal{O}$ indicating $\mathcal{O}~=~1$, we can represent the posterior distribution of optimal trajectories as $\pPdf[\MakeUppercase{x}\mid\mathcal{O}] \propto \pPdf[\mathcal{O}\mid\MakeUppercase{x}] \pPdf[\MakeUppercase{x}]$, for a given optimality likelihood $\pPdf[\mathcal{O}\mid\MakeUppercase{x}]$ and trajectory prior $\pPdf[\MakeUppercase{x}]$. The *maximum a posteriori* (MAP) solution is given by finding the mode of the negative log posterior: $$\begin{equation}
    \label{eq:mp_as_pi}
    \begin{aligned}
        \MakeUppercase{x}^{*} &= \operatornamewithlimits{\arg\min}_{\MakeUppercase{x}} -\log  \pPdf[\mathcal{O}\mid\MakeUppercase{x}] - \log \pPdf[\MakeUppercase{x}] \\
                     &= \operatornamewithlimits{\arg\min}_{\MakeUppercase{x}} \lambda\costFn[\MakeUppercase{x}] - \log \pPdf[\MakeUppercase{x}],
    \end{aligned}
\end{equation}$$ where the last equality arises from the typical choice of the exponential distribution to represent the optimality likelihood, i.e. $\pPdf[\mathcal{O}\mid\MakeUppercase{x}] = \exp (-\lambda\costFn[\MakeUppercase{x}])$ with $\lambda$ being a temperature hyper-parameter.

Rather than finding the MAP solution, we are interested in approximating the full posterior distribution, which may be multi-modal, and generating diverse solutions for the planning problem. As discussed in [3.3](#sec:svgd){reference-type="ref+label" reference="sec:svgd"}, we can apply SVGD to approximate the posterior distribution with a collection of particles. In the case at hand each of such particles is a sampled path, such that [\[eq:stein_score_func\]](#eq:stein_score_func){reference-type="ref+label" reference="eq:stein_score_func"} can be rewritten as: $$\begin{equation}
\label{eq:svmp_score_func}
    {\scoreFunc}^{*} (\MakeUppercase{x}) = \expectation_{\MakeUppercase{y}\sim \hat{\qPdf}} [\big] 
    [k \parens{\MakeUppercase{y}, \MakeUppercase{x}} \grad_{\MakeUppercase{y}} \log \pPdf[\MakeUppercase{y}\mid\mathcal{O}] + \grad_{\MakeUppercase{y}} k \parens{\MakeUppercase{y}, \MakeUppercase{x}}].
\end{equation}$$

The score function presented in [\[eq:svmp_score_func\]](#eq:svmp_score_func){reference-type="ref+label" reference="eq:svmp_score_func"} is composed of two competing forces. On one hand, we have the kernel smoothed gradient of the log-posterior pushing particles towards regions of higher probability. Whereas the second term acts as a repulsive force, pushing particles away from one another.

It is worth emphasising that the kernel function is *static*, i.e. it does not consider the sequential nature of the input paths. In effect, for a path of dimension $c$ and $s$ discrete time steps, the inputs are projected onto a space ${\mathcal{\MakeUppercase{V}}} \subset \mathbb{\MakeUppercase{R}}^{c\times s}$ in which similarities are evaluated.

Finally, the posterior gradient can be computed by applying Bayes' rule, resulting in: $$\begin{equation}
\label{eq:svmp_grad}
    \grad_{\MakeUppercase{y}} \log \pPdf[\MakeUppercase{y}\mid\mathcal{O}] =  \grad_{\MakeUppercase{x}} \log \pPdf[\MakeUppercase{y}] - \grad_{\MakeUppercase{y}} \lambda\costFn[\MakeUppercase{y}].
\end{equation}$$

## Stein Variational Motion Planning with Smooth Paths {#sec:svmp_on_splines}

In previous work [@barfoot_batch_2014; @dong_motion_2016; @lambert_entropy_2021; @mukadam_continuous-time_2018] the prior distribution in [\[eq:svmp_grad\]](#eq:svmp_grad){reference-type="ref+label" reference="eq:svmp_grad"} is defined in a way to promote smoothness on generated paths. This typically revolves around defining Gaussian Processes [@rasmussen_gaussian_2006] as priors and leveraging factor graphs for efficiency. Although effective, this approach still requires several latent variables to describe a desired trajectory, which implies on a higher dimensional inference problem.

Importantly, the problem dimensionality is directly related to the amount of repulsive force exerted by the kernel. In large dimensional problems, the repulsive force of translation-invariant kernels vanishes, allowing particles to concentrate around the posterior modes which results in an underestimation of the posterior variance [@zhuo_message_2018]. This problem is further accentuated when considering the static nature of the kernel function, as discussed in the previous section.

In order to keep the inference problem low-dimensional while still enforcing smooth paths we make use of *natural cubic splines* and aim to optimise the location of a small number of knots. These knots may be initialised in different ways, such as perturbations around a linear interpolation from the starting state ${\boldsymbol{\mathbf{x}}}_{s}$ and goal state ${\boldsymbol{\mathbf{x}}}_{g}$, sampled from an initial solution given by a shooting method (e.g. RRT [@lavalle_randomized_2001]), or drawn randomly from within the limits of ${\mathcal{\MakeUppercase{X}}}$. For simplicity, in this work we will opt for the latter.

Since path smoothness is induced by the splines, the choice of prior is more functionally related to the problem at hand. If one desires some degree of regularisation on the trajectory optimisation, a multivariate Gaussian prior centred at the placement of the initial knots may be used. Conversely, if we only wish to ensure the knots are within certain bounds, a less informative smoothed approximation of the uniform prior may be used. More concretely, for a box $B = {x\colon a\leq x \leq b}$, such prior would be defined as: $$\begin{equation}
    \pPdf[x] \propto \exp{\left(- d{\left(x, B\right)}^2 / \sqrt{(2 \sigma^2)}\right)}
\end{equation}$$ where the distance function $d\left(x, B\right)$ is given by $d\left(x, B\right) = \min |x - x'|, \; x' \in B$. Finally, we could define both a prior and hyper-prior if we wish to combine both effects (see [9](#app:hyperprior){reference-type="ref+label" reference="app:hyperprior"} for details).

As discussed in [3.1](#sec:prelim){reference-type="ref+label" reference="sec:prelim"} the cost functional $\costFn$ imposes penalties for collisions and defines the relevant performance criteria to be observed. Since only a small number of knots is used for each path, some of these criteria and, in particular, collision checking require that we discretise the resulting spline in a sufficiently dense amount of points. It is worth mentioning that $\costFn$ is typically non-differentiable and that the gradient in [\[eq:svmp_grad\]](#eq:svmp_grad){reference-type="ref+label" reference="eq:svmp_grad"} is usually approximated with Monte Carlo samples [@barcelos_dual_2021]. However, as this introduces an extra degree of stochasticity in the benchmark comparison, we will restrict our choice of $\costFn$ to be differentiable. We will discuss the performance criteria of each problem in the experimental section.

::: algorithm*
Sample $\set*{\MakeUppercase{x}_{t_0}^{i}}_{i= 1}^{N_{p}} \sim \qPdf[\MakeUppercase{x}_{t_0}]$
:::

## Stein Variational Motion Planning with Path Signature Kernel {#sec:sig_svgd}

In this section we present our main contribution, which is a new formulation for motion planning in which Path Signature can be used to efficiently promote diversity in trajectory optimisation through the use of Signature Kernels. In [3](#sec:background){reference-type="ref+label" reference="sec:background"} we discussed some desirable properties of the signature transform. The key insight is that the space of linear combination of signatures forms an algebra, which enables it as a faithful feature map for trajectories [@kiraly_kernels_2019].

With that in mind, perhaps the most straightforward use of the signature would be to redefine the kernel used in [\[eq:stein_optim,eq:stein_score_func\]](#eq:stein_optim,eq:stein_score_func){reference-type="ref+label" reference="eq:stein_optim,eq:stein_score_func"} as $\bar{k} \parens*{\MakeUppercase{x}, \MakeUppercase{y}} = k \parens*{{\signature[\MakeUppercase{x}]}_{t}, {\signature[\MakeUppercase{y}]}_{t}}$. However, as seen in [3](#sec:background){reference-type="ref+label" reference="sec:background"}, this approach would not be scalable given the exponential time and space complexity of the signature w.r.t. to its degree. A single evaluation of the Gram kernel matrix for $\bar{k}$ would be an operation of order $O(n^2 \cdot c^{d})$, where $n$ is the number of concurrent paths being optimised, $d$ is the degree of the signature, and $c$ is the dimensionality of the space ${\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\ni \MakeUppercase{x}, \MakeUppercase{y}$. Furthermore, kernel $\bar{k}$ is static in the sense that it does not take into account the sequential nature of its domain. Rather than a kernel $k \colon {\mathcal{\MakeUppercase{X}}}\times {\mathcal{\MakeUppercase{X}}}\to \mathbb{\MakeUppercase{R}}$, we want to define a kernel $k^{+} \colon {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\times {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\to \mathbb{\MakeUppercase{R}}$, which takes into account the structure induced by paths.

Hence, we take a different approach and proceed by first projecting paths to an RKHS onto which we will then compute the signature. That is, given a kernel $k^{+} \colon {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\times {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}\to \mathbb{\MakeUppercase{R}}$, a path $\MakeUppercase{x}\in {\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{X}}}}$ can be lifted to a path in the RKHS ${\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{H}}}}$ through the map $k_{\MakeUppercase{x}}\colon t \mapsto k \parens{\MakeUppercase{x}_{t}, \cdot}$, where ${\mathcal{\MakeUppercase{P}}}_{{\mathcal{\MakeUppercase{H}}}}$ is the set of ${\mathcal{\MakeUppercase{H}}}$-valued paths. Finally, we compute the signature of the lifted path $\signature \parens*{k_{\MakeUppercase{x}}}_{t}$ and use it as our final feature map.

At first glance, this further deteriorates scalability, since most useful ${\mathcal{\MakeUppercase{P}}}_{\mathcal{\MakeUppercase{H}}}$ are infinite dimensional, rendering this approach infeasible. However, results presented by @kiraly_kernels_2019 [Corollary 4.9] show that this approach can be completely kernelised. This allows them to define a *truncated signature kernel*, ${k}^{+}\colon \parens{\MakeUppercase{x}_{t}, \MakeUppercase{y}_{t}} \mapsto \inner{\signature^{d} \parens{k_{\MakeUppercase{x}}}_{t}}{\signature^{d} \parens{k_{\MakeUppercase{y}}}_{t}}$, that can be efficiently computed using only evaluations of a static kernel $k \parens{{\boldsymbol{\mathbf{x}}}, {\boldsymbol{\mathbf{y}}}}$ at discretised timestamps. The number of evaluations depends on the truncation degree $d$ and number of discretised steps $l$. Several algorithmic approaches are considered in [@kiraly_kernels_2019] with dynamic programming having complexity $O \parens{n^2 \cdot l^2 \cdot d}$ to compute a $\parens{n\times n}$-Gram matrix. Otherwise, approximations can be used to reduce the complexity to linear on $l$ and $n$. However, even though the importance of the terms in the signature decay factorially [@lyons_rough_2014], the amount of coefficients grows exponentially, which means that for high values of $d$ the kernel $k^{+}$ would be restricted to low-dimensional applications.

Nonetheless, recent work [@salvi_signature_2021] proved that for two continuously differentiable input paths the complete *signature kernel*, $$\begin{equation}
\label{eq:sig_kernel}
    {k}^{\oplus}\colon \parens{\MakeUppercase{x}_{t}, \MakeUppercase{y}_{t}} \mapsto \inner{\signature \parens{k_{\MakeUppercase{x}}}_{t}}{\signature \parens{k_{\MakeUppercase{y}}}_{t}},
\end{equation}$$ is the solution of a second-order, hyperbolic partial differential equation (PDE) known as Goursat PDE. Solving this PDE is a problem of complexity $O \parens{l^2 \cdot c}$, so still restrictive on the discretisation of the path. However, by its intrinsic nature, the PDE can be parallelised, turning the complexity into $O \parens{l\cdot c}$, as long as the GPU is able to accommodate the required number of threads. Therefore the untruncated signature kernel can be efficiently and parallel computed using state-of-the-art hyperbolic PDE solvers and finite-difference evaluations of the static kernel $k$.

Hence, we can directly apply $k^{\oplus}$ in [\[eq:svmp_score_func\]](#eq:svmp_score_func){reference-type="ref+label" reference="eq:svmp_score_func"} and we now have a way to properly represent sequential data in feature space, resulting in the final gradient update function: $$\begin{equation}
\label{eq:sigmp_score_func}
    {\scoreFunc}^{*} (\MakeUppercase{x}) = \expectation [\big]
    [k^{\oplus} \parens{\MakeUppercase{y}, \MakeUppercase{x}} \grad_{\MakeUppercase{y}} \log \pPdf[\MakeUppercase{y}\mid\mathcal{O}] + \grad_{\MakeUppercase{y}} k^{\oplus} \parens{\MakeUppercase{y}, \MakeUppercase{x}}],
\end{equation}$$ where the expectation is taken by sampling paths $\MakeUppercase{y}$ from $\hat{\qPdf}$. For convenience, we will use the acronym SigSVGD whether the algorithm is used for planning or control problems. A complete overview of the algorithm is presented in [\[algo:sigsvgd\]](#algo:sigsvgd){reference-type="ref+label" reference="algo:sigsvgd"}.

# Results {#sec:results}

In this section we present results to demonstrate the correctness and applicability of our method in a set of simulated experiments, ranging from simple 2D motion planning to a challenging benchmark for robotic manipulators.

## Motion Planning on 2D Terrain {#sec:exp_2d_planning}

Our first set of experiments consists of trajectory optimisation in a randomised 2D terrain illustrated in [2](#fig:2d_planning){reference-type="ref+label" reference="fig:2d_planning"}. Regions of higher cost, or hills, are shown in a darker shade whereas valleys are in a lighter colour. The terrain is parameterised by a series of isotropic Multivariate Gaussian distributions placed randomly according to a Halton sequence and aggregated into a Gaussian Mixture Model denoted by $\pPdf_{\text{map}}$.

Paths are parameterised by natural cubic splines with $N_{k}= 2$ intermediary knots, apart from the start and goal state. Our goal is to find the best placement for these knots to find paths from origin to goal that avoid regions of high cost but are not too long. We adopt the following cost function in order to balance trajectory length and navigability: $$\begin{equation}
\label{eq:2d_palnning_cost}
\costFn[{\boldsymbol{\mathbf{x}}}_{t}] = \sum_{t \in \bracks{a, b}} \parens[\Big]{\pPdf_{\text{map}}[{\boldsymbol{\mathbf{x}}}_{t}] + 75 \, \norm{{\boldsymbol{\mathbf{x}}}_{t} - {\boldsymbol{\mathbf{x}}}_{t-1}}_{2}},
\end{equation}$$ where the $\ell^{2}$-norm term is a piecewise linear approximation of the trajectory length. To ensure the approximation is valid each trajectory is decimated into 100 waypoints before being evaluated by [\[eq:2d_palnning_cost\]](#eq:2d_palnning_cost){reference-type="ref+label" reference="eq:2d_palnning_cost"}.

The initial knots are randomly placed and the plots in [2](#fig:2d_planning){reference-type="ref+label" reference="fig:2d_planning"} show the final 20 trajectories found with three different optimisation methods. Furthermore, the colour of each path depicts its normalised final cost. On the left we can see the solutions found with Batch Gradient Descent (BGD) and note how all trajectories converge to two modes of similar cost. The SVMP results are more diverse, but failed to capture one of the BGD modes. Also note how, when multiple trajectories converge to a single trough, the spline knots are pushed away by the repulsive force resulting in suboptimal solutions. On the other hand, the trajectories found by SigSVGD are not only more diverse, finding more homotopic solutions, but are also able to coexist in the narrow valleys. This is possible since the repulsive force is being computed in the signature space and not based on the placement of the knots. Furthermore, notice how for the same reason the paths are more direct and coordinated when compared to SVMP.

## Point-mass Navigation on an Obstacle Grid {#sec:exp_nav}

::: {#tab:part2d_results}
                           Cost               Steps        
  ----------------- ------------------- ------------------ --
  SigSVGD            **1056.0 (58.4)**   **189.3 (12.6)**  
  SVMPC                1396.4 (73.0)       239.1 (49.4)    
  MPPI                1740.7 (192.3)       290.8 (23.7)    
  CMA-ES$^{\dag}$           ---                ---         

  : **Point-mass navigation results**. The table shows the mean and standard deviation for 20 episodes. *Cost* indicates the total accrued cost over the episode. CMA-ES cost is not shown as it couldn't complete the task on any episodes. *Steps* indicates the total amount of time-steps the controller needed to reach the goal. $^{\dag}$CMA-ES couldn't complete any episodes, so results are omitted.
:::

![[]{#fig:part2d_results label="fig:part2d_results"} **Point-mass navigation trajectories**. The plot shows an intermediate time-step of the navigation task for SigSVGD, on the left, and SVMPC, on the right. An inset plot enlarges a patch of the map just ahead of the point-mass. The rollout colour indicate from which of the policies, i.e. paths in the optimisation, they originate, whereas fixed motion primitives are shown in purple. Note how rollouts generated by SigSVGD are more disperse, providing a better gradient for policy updates. ](fig/trajectories_plot.pdf){#fig:part2d_results width="\\linewidth"}

Here, our goal is to demonstrate the benefits of applying the signature kernel Model Predictive Control (MPC). To that end, we reproduce the point-mass planar navigation task presented in [@barcelos_dual_2021; @lambert_stein_2020] and compare SVMPC against and a modified implementation using SigSVGD. The objective is to navigate an holonomic point-mass robot from start to goal through an obstacle grid. Since the system dynamics is represented as a double integrator model with non-unitary mass $m$, the particle acceleration is given by $\Ddot{{\boldsymbol{\mathbf{x}}}} = m^{-1} {\boldsymbol{\mathbf{u}}}$ and the control signal is the force applied to the point-mass. We adopt the same cost function as in [@barcelos_dual_2021], that is: $$\begin{equation*}
\begin{split}
    &\costFn[{\boldsymbol{\mathbf{x}}}_{t}, {\boldsymbol{\mathbf{u}}}_{t}] =
    0.5 \, {\boldsymbol{\mathbf{e}}}_{t}^\mathsf{T}{\boldsymbol{\mathbf{e}}}_{t}
    + 0.25 \, \dot{{\boldsymbol{\mathbf{x}}}_{t}}^\mathsf{T}\dot{{\boldsymbol{\mathbf{x}}}_{t}}
    + 0.2 \, {\boldsymbol{\mathbf{u}}}_{t}^\mathsf{T}{\boldsymbol{\mathbf{u}}}_{t}
    + %
  \ifdefined\mathbbb%
    \mathbbb{1}%
  \else%
    \boldsymbol{\mathbb{1}}%
  \fi\{\operatorname{col.}\} \, p \\
    &\costFn_{\text{term}}[{\boldsymbol{\mathbf{x}}}_{t}, {\boldsymbol{\mathbf{u}}}_{t}] =
    1000 \, {\boldsymbol{\mathbf{e}}}_{t}^\mathsf{T}{\boldsymbol{\mathbf{e}}}_{t}
    + 0.1 \, \dot{{\boldsymbol{\mathbf{x}}}_{t}}^\mathsf{T}\dot{{\boldsymbol{\mathbf{x}}}_{t}} \,,
\end{split}
\end{equation*}$$ where ${\boldsymbol{\mathbf{e}}}_{t} = {\boldsymbol{\mathbf{x}}}_{t} - {\boldsymbol{\mathbf{x}}}_{g}$ is the instantaneous position error and $p = 10^6$ is the penalty when a collision happens.

:::: {#tab:motionbench_results .figure}
![image](Barcelos2023Path_figs/robot_best.png) ![image](Barcelos2023Path_figs/robot_length.png) ![image](Barcelos2023Path_figs/robot_nll.png)

::: caption
[]{#tab:motionbench_results label="tab:motionbench_results"} **Motion planning benchmark**. Results shown are the mean and standard deviation over 5 episodes for 4 distinct requests, totalling 20 iterations per scene. Best result is highlighted with a hatched bar. *Lowest cost* depicts the cost of the best trajectory found. *Path length* is the piecewise linear approximation of the end-effector trajectory length for the best trajectory. *NLL* indicates the negative log likelihood and, since we are using an exponential likelihood, represents the total cost of all sampled trajectories.
:::
::::

To create a controlled environment with several multi-modal solutions, obstacles are placed equidistantly in a grid (see [4](#fig:part2d_results){reference-type="ref+label" reference="fig:part2d_results"}). The simulator performs a simple collision check based on the particle's state and prevents any future movement in case a collision is detected, simulating a crash. Barriers are also placed at the environment boundaries to prevent the robot from easily circumventing the obstacle grid. As the indicator function makes the cost function non-differentiable, we need to compute approximate gradients using Monte Carlo sampling [@lambert_stein_2020]. Furthermore, since we are using a stochastic controller, we also include CMA-ES and Model Predictive Path Integral (MPPI) [@williams_aggressive_2016] in the benchmark. A detailed account of the hyper-parameters used in the experiment is presented in [7](#app:exp_hyperparams){reference-type="ref+label" reference="app:exp_hyperparams"}.

In this experiment, each of the particles in the optimisation is a path that represents the mean of a stochastic control policy. Gradients for the policy updates are generated by sampling the control policies and evaluating *rollouts* via an implicit model of the environment. As CMA-ES only entertains a single solution at any given time, to make the results comparable we increase the amount of samples it evaluates at each step to be equivalent to the number of policies times the number of samples in SVMPC. One addition to the algorithm in [@lambert_stein_2020] is the inclusion of particles with predefined primitive control policies which are not optimised. For example, a policy which constantly applies the minimum, maximum, or no acceleration are all valid primitives. These primitive policies are also included in every candidate solution set of CMA-ES.

The inlay plot in [4](#fig:part2d_results){reference-type="ref+label" reference="fig:part2d_results"} illustrates how SigSVGD promotes policies that are more diverse, covering more of the state-space on forward rollouts. The outcome can be seen on [1](#tab:part2d_results){reference-type="ref+label" reference="tab:part2d_results"}. SigSVGD finds lower cost policies and is able to reach the goal in fewer steps than SVMPC. Due to the dynamical nature of the problem, we are unable to run the optimisation for many iterations during each time-step, as we need to get actions from the controller at a fast rate. This poses a challenge to CMA-ES, which crashed on all episodes despite having a much larger number of samples per step.

## Benchmark Comparison on Robotic Manipulator

:::: {#fig:motionbench_paths .figure}
![Box](Barcelos2023Path_figs/box_panda.png){width="\\linewidth"}

![Bookshelf Small](Barcelos2023Path_figs/bookshelf_small_panda.png){width="\\linewidth"}

![Bookshelf Tall](Barcelos2023Path_figs/bookshelf_tall_panda.png){width="\\linewidth"}

![Bookshelf Thin](Barcelos2023Path_figs/bookshelf_thin_panda.png){width="\\linewidth"}

![Cage](Barcelos2023Path_figs/cage_panda.png){width="\\linewidth"}

![Table Bars](Barcelos2023Path_figs/table_bars_panda.png){width="\\linewidth"}

![Table Pick](Barcelos2023Path_figs/table_pick_panda.png){width="\\linewidth"}

![Table Under](Barcelos2023Path_figs/table_under_pick_panda.png){width="\\linewidth"}

::: caption
[]{#fig:motionbench_paths label="fig:motionbench_paths"} **Visualisation of SigSVGD in the motion planning benchmark.** The *Blue* and *Grey* lines denote the end-effector's trajectories with the former highlighting the trajectory with the lowest cost. The *Orange* and *Green* tinted robot poses denote the start and target configuration, respectively. The translucent robot poses denote in-between configurations of the lowest-cost solution.
:::
::::

To test our approach on a more complex planning problem we compare batch gradient descent (i.e. parallel gradient descent on different initialisations), SVMP and SigSVGD in robotic manipulation problems generated using MotionBenchMaker [@chamzas_motionbenchmaker_2022]. A problem consists of a scene with randomly placed obstacles and a consistent request to move the manipulator from its starting pose to a target configuration. For each scene in the benchmark, we generate 4 different requests and run the optimisation with 5 random seeds for a total of 20 episodes per scene.

The robot used is a Franka Emika Panda with 7 Degrees of Freedom (DOF). The cost function is designed to generate trajectories that are smooth, collision-free and with a short displacement of the robot's end-effector. We once again resort to a fully-differentiable function to reduce the extraneous influence of approximating gradients with Monte Carlo samples. As is typical in motion planning, the optimisation is performed directly in *configuration space* (C-space), which simplifies the search for feasible plans. To reduce the sampling space and promote smooth trajectories, we once again parameterise the path of each of the robot joints with natural cubic splines, adopting 3 intermediary knots besides those at the initial and target poses.

### Regularising Path Length and Dynamical Motions

\
Finally, the use of splines to interpolate the trajectories ensures smoothness in generated trajectories, but that does not necessarily imply in smooth dynamics for the manipulator. To visualise this, consider, for example, a trajectory in $\mathcal{Q}$ parameterised by a natural cubic spline. The configurations ${\boldsymbol{\mathbf{q}}}$ in between each knot can be interpolated, resulting in a smooth trajectory of the robot end-effector in Euclidean coordinates in SE(3). However, the same end-effector trajectory could be traversed in a constant linear speed or with a jerky acceleration and deceleration motion. More specifically, if we use a fixed number of interpolated configurations between knots without care to impose dynamical restrictions to the simulator, knots that are further apart will result in motions with greater speed and acceleration since a larger distance would be covered during the same interval. To avoid these abrupt motions on the robots joints, we introduce the term $\costFn_{\text{dyn}}$ to the cost function, which penalises the linear distance between consecutive configurations: $$\begin{equation}
\label{eq:dyn_cost}
    \costFn_{\text{dyn}}= \sum_{i= 2}^{p} {\boldsymbol{\mathbf{w}}}^{\mathsf{T}} \norm{{\boldsymbol{\mathbf{q}}}_{i} - {\boldsymbol{\mathbf{q}}}_{i- 1}}_{2},
\end{equation}$$ where $p$ is the number of intermediary configurations chosen when discretising the path spline and the weight ${\boldsymbol{\mathbf{w}}}$ can be used to assign a higher importance to certain robot joints. We choose to adopt a vector ${\boldsymbol{\mathbf{w}}}$ which is a linear interpolation from 1 to 0.7, where the higher value is assigned to the base joint of the manipulator and progressively reduced until the end-effector. A similar approach as the one presented in [\[eq:dyn_cost\]](#eq:dyn_cost){reference-type="ref+label" reference="eq:dyn_cost"} can be used to penalise the length of the robot's trajectory in workspace. We include a final term to our cost function, $\costFn_{\text{len}}$, that penalises exclusively the length of the end-effector path. This brings us to our final cost function: $$\begin{equation}
\label{eq:manipulator_total_cost}
    \costFn = 2.5 \, \costFn_{\text{len}}+ 2.5 \, \costFn_{\text{dyn}}+ \costFn_{\text{col}}+ 10 \, \costFn_{\text{s-col}},
\end{equation}$$ where each of the terms are respectively the cost for path length, path dynamics, collision with the environment and self-collision. The optimisation is carried out for 500 iterations and the kernel repulsive force is scheduled with cosine annealing [@loshchilov_sgdr_2017]. By reducing the repulsive force on the last portion of the optimisation, we allow trajectories at the same local minima to converge to the modes and are able to qualitatively measure the diversity of each approach.

The results shown on [5](#tab:motionbench_results){reference-type="ref+label" reference="tab:motionbench_results"} demonstrate how SigSVGD achieves better results in almost all metrics for every scenario. The proper representation of paths results in better exploration of the configuration space and leads to better global properties of the solutions found. This can be seen in [6](#fig:motionbench_paths){reference-type="ref+label" reference="fig:motionbench_paths"}, which shows the end-effector paths for SigSVGD and SVMP. One of such paths is also illustrated in [1](#fig:intro-image){reference-type="ref+label" reference="fig:intro-image"}. Results found by SigSVGD also show a higher percentage of feasible trajectories and lower contact depths for rollouts in collision (see [\[tab:sim_col_results\]](#tab:sim_col_results){reference-type="ref+label" reference="tab:sim_col_results"}).

::: table*
+-------------------------+------------------------------------+---------------------------------+------------------------------------+
|                         | SigSVGD                            | SVMP                            | Batch Gradient Descent             |
+:========================+:===============:+:================:+:===============:+:=============:+:===============:+:================:+
| 2-3(lr)4-5(lr)6-7 Scene | Contact Depth   | Feasible Pct.    | Contact Depth   | Feasible Pct. | Contact Depth   | Feasible Pct.    |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Box                     | 3.74 (2.30)     | **94.99 (3.78)** | **3.62 (1.95)** | 94.96 (3.32)  | 3.63 (1.95)     | 94.97 (3.31)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Bookshelf Small         | **1.32 (2.50)** | **96.63 (5.48)** | 1.55 (2.19)     | 96.20 (4.68)  | 1.56 (2.20)     | 96.18 (4.71)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Bookshelf Tall          | 0.56 (1.78)     | 98.30 (4.65)     | 0.27 (0.60)     | 99.02 (1.76)  | **0.27 (0.59)** | **99.03 (1.74)** |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Bookshelf Thin          | **2.78 (3.11)** | **94.59 (4.94)** | 3.14 (3.50)     | 93.54 (5.57)  | 3.14 (3.50)     | 93.54 (5.57)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Cage                    | 2.13 (1.82)     | **96.12 (2.92)** | **2.00 (1.67)** | 96.11 (2.89)  | **2.00 (1.67)** | 96.11 (2.89)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Kitchen                 | **9.82 (6.95)** | 88.04 (9.85)     | 10.61 (6.45)    | 88.59 (6.21)  | 10.62 (6.71)    | **88.61 (6.21)** |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Table Bars              | **9.46 (7.43)** | **92.42 (5.89)** | 9.52 (8.05)     | 92.09 (6.69)  | 9.70 (8.44)     | 92.05 (6.85)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Table Pick              | **0.22 (0.67)** | **99.56 (1.67)** | 0.83 (1.04)     | 98.06 (2.62)  | 0.83 (1.02)     | 98.08 (2.43)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
| Table Under             | **3.33 (2.60)** | **93.63 (5.36)** | 5.16 (4.75)     | 90.19 (8.21)  | 5.18 (4.77)     | 90.06 (8.30)     |
+-------------------------+-----------------+------------------+-----------------+---------------+-----------------+------------------+
:::

### Robot Collision as Continuous Cost

\
Typically collision-checking is a binary check and non-differentiable. To generate differentiable collision checking with informative gradients, we resort to continuous occupancy grids. Occupancy grid maps are often generated from noisy and uncertain sensor measurement by discretising the space $\mathcal{W}$ where the robot operates (know as *workspace*) into grid-cells, where each cell represents an evenly spaced field of binary random variables that corresponds to the presence of an obstacle at the given location. However, the discontinuity in-between each cell means these grid maps are non-differentiable and not suitable for optimisation-based planning. A continuous analogue of an occupancy map can be generalised by a kernelised projection to high-dimensional spaces [@ramos_hilbert_2016] or with distance-based methods [@jones_3d_2006].

In this work we trade off the extra complexity of the methods previously mentioned for a coarser but simpler approach. Inspired by [@danielczuk_object_2021], we learn the occupancy of each scene using a neural network as a universal function approximator. We train the network to approximate a continuous function that returns the likelihood of a robot configuration being occupied. The rationale for this choice is that, since all methods are optimised under the same conditions, the comparative results should not be substantially impacted by the overall quality of the map. Additionally, the trained network is fast to query and fast to obtain derivatives with respect to inputs, properties that are beneficial for querying of large batches of coordinates for motion planning.

Given a dataset of $n$ pairs of coordinates and a binary value which indicates whether the coordinate is occupied, i.e. $\mathcal{D}= \set{ \parens{{\boldsymbol{\mathbf{x}}}_{i}, y_{i}} }_{i=1}^{n}$, where ${\boldsymbol{\mathbf{x}}}_{i} \in \mathcal{W}\subseteq \mathbb{\MakeUppercase{R}}^{w}$, and $y_{i} \in \set{0,1}$, for $i=1,\ldots, n$. The network then learns a mapping $\fcol$ between a coordinate of interest ${\boldsymbol{\mathbf{x}}}$ and the probability of it being occupied, that is, $\fcol[{\boldsymbol{\mathbf{x}}}] = \prob[y= 1 \mid{\boldsymbol{\mathbf{x}}}]$. A dataset of this format can be obtained, for instance, from depth sensors as point clouds. We model $\fcol$ as a fully-connected neural network, with $\tanh$ as the activation function between hidden layers, and $\mathrm{sigmoid}$ as the output layer. The final network is akin to a binary classification problem, which can be learned via a binary cross-entropy loss with gradient descent optimisers. As such, we can construct a collision cost function $\fcol\colon \mathcal{W}\to \mathbb{\MakeUppercase{R}}$ that maps workspace coordinates into cost values associated at the corresponding locations.

A similar problem occurs when ascertaining whether a given configuration of the robot's joints is unfeasible, leading to a self-collision. We address this issue in a similar manner, by training a separate neural network to approximate a continuous function $\fscol$ which maps configurations of the robot to the likelihood of they being in self-collision. More precisely, $\fscol\colon \mathcal{Q}\to \mathbb{\MakeUppercase{R}}$, where $\fscol[{\boldsymbol{\mathbf{q}}}] = \prob[y= 1 \mid{\boldsymbol{\mathbf{q}}}]$, for ${\boldsymbol{\mathbf{q}}}_{i} \in \mathcal{Q}\subseteq \mathbb{\MakeUppercase{R}}^{d}$, and $y_{i} \in \set{0,1}$. The dataset used to train $\fscol$ is generated by randomly choosing configurations within the joint limits of the robot and performing a binary self-collision check provided by the robot's API.

### Bringing Collision Cost from Workspace to Configuration Space

\
Collision checking requires information about the workspace geometry of the robot to determine whether it overlaps with objects in the environment. On the other hand, we assume that the robot movement is defined and optimised in C-space. The cost functions to shape robot behaviour are often defined in the Cartesian task space. We denote C-space as $\mathcal{Q}\subseteq \mathbb{\MakeUppercase{R}}^{d}$, where there are $d$ joints in the case of a robotic manipulator. The joint configurations, ${\boldsymbol{\mathbf{q}}}\in \mathcal{Q}$, are elements of the C-space, while Cartesian coordinates in task space are denoted as ${\boldsymbol{\mathbf{x}}}\in \mathcal{W}$. We now outline the procedure of *pulling* a cost gradient defined in the workspace to the C-space.

We start by defining $b$ body points on the robot, each with a forward kinematics function $\ffk_{i}$ mapping configurations to the Cartesian coordinates ${\boldsymbol{\mathbf{x}}}_i$ at the body point, $\ffk_{i} \colon \mathcal{Q}\to \mathcal{W}$, for each $i= 1, \ldots, b$. Let the Jacobian of the forward kinematics functions w.r.t. the joint configurations be denoted as $$\begin{equation}
    {\jacob[\cdot]}_{\ffk}^{i} = \frac{{\operatorname{d}}\ffk_{i}}{{\operatorname{d}}{\boldsymbol{\mathbf{q}}}} \parens{\cdot}.
\end{equation}$$ The derivative of a cost potential $\costFn_{\text{col}}$ which operates on the body points, such as the occupancy cost potential, can then be *pulled* into the C-space with: $$\begin{equation}
    \grad_{{\boldsymbol{\mathbf{q}}}} \costFn = \sum_{i= 1}^{b} {\jacob[{\boldsymbol{\mathbf{q}}}]}_{\ffk}^{i} \grad_{{\boldsymbol{\mathbf{x}}}} \costFn,
\end{equation}$$ which allows us to update trajectory in the C-space $\mathcal{Q}$ with cost in the Cartesian space $\mathcal{W}$.

# Conclusion {#sec:conclusion}

This work, to the best of our knowledge, is the first to introduce the use of path signatures for trajectory optimisation in robotics. We discuss how this transformation can be used as a canonical *linear* feature map to represent trajectories and how it possesses many desirable properties, such as invariance under time reparametrisation. We use these ideas to construct SigSVGD, a kernel method to solve control and motion planning problems in a variational inference setting. It approximates the posterior distribution over optimal paths with an empirical distribution comprised of a set of vector-valued particles which are all optimised in parallel.

In previous work it has been shown that approaching the optimisation from the variational perspective alleviates the problem of local optimality, providing a more diverse set of solutions. We argue that the use of signatures improves on previous work and can lead to even better global properties. Despite the signature poor scalability, we show how we can construct fast and paralellisable signature kernels by leveraging recent results in rough path theory. The RKHS induced by this kernel creates a structured space that captures the sequential nature of paths. This is demonstrated through an extensive set of experiments that the structure provided helps the functional optimisation, leading to better global solutions than equivalent methods without it. We hope the ideas herein presented will serve an inspiration for further research and stimulate a groundswell of new work capitalising on the benefits of signatures in many other fields within the robotics community.

# Experiments Hyper-parameters {#app:exp_hyperparams}

In [2](#tab:exp_hyperparams){reference-type="ref+label" reference="tab:exp_hyperparams"} we present the relevant hyper-parameters to reproduce the results in the paper. It is worth mentioning that the terrain in the 2D motion planning is randomly generated and will vary on each simulation. Another source of randomness arises when using Monte Carlo samples to approximate the gradient of the log posterior distribution. Furthermore, due to the stochastic nature of the initial placement of the spline knots, results will vary despite using analytic gradients.

::: {#tab:exp_hyperparams}
  Parameter                                                2D Terrain                          Point-mass Navigation                    Manipulator Benchmark
  -------------------------------------------------- ----------------------- --------------------------------------------------------- -----------------------
  Initial state, ${\boldsymbol{\mathbf{x}}}_{s}$      $\bracks{0.25, 0.75}$                    $\bracks{-1.8, -1.8}$                      Problem dependent
  Environment maximum velocity                                 ---                                   5 m ^−1^                                    ---
  Environment maximum acceleration                             ---                                      ---                                      ---
  Number of spline knots, $N_{k}$                               4                                       ---                                       5
  Number of particles, $N_{p}$                                 20                                       30                                       20
  Particle prior                                             Uniform          $\normal[\MakeUppercase{x}, {\boldsymbol{\mathbf{1}}}]$          Uniform
  Number of action samples, $N_{\operatorname{a}}$             ---                                      10                                       ---
  Cost likelihood inverse temperature, $\lambda$               1.0                                      1.0                                      1.0
  Control authority, ${\MakeUppercase{\Sigma}}$                ---                                     $5^2$                                     ---
  Control horizon, $H$                                         ---                                      30                                       ---
  Stationary kernel, $k\parens{\cdot, \cdot}$          Squared-exponential                      Squared-exponential                      Squared-exponential
  Stationary Kernel bandwidth, $\sigma$                        1.5                               Silverman's rule                                1.5
  Signature kernel bandwidth, $\sigma$                         1.5                                     5.65                                      1.5
  Signature kernel degree, $d$                                  4                                        3                                        6
  Optimiser class                                             Adam                                     Adam                                     Adam
  Learning rate, $\epsilon$                                5 × 10^−2^                                    1                                   1 × 10^−3^

  : Hyper-parameters used in the experiments.
:::

# Path Following Example {#sec:exp_obst_field}

As a motivating example in [7](#fig:tracking){reference-type="ref+label" reference="fig:tracking"} we depict the results of a simple two-dimensional path following task. The goal is to reduce the error between the desired path and candidate paths. Since we want the error to be as small as possible, the optimal path is one centred at the origin across time. The objective function is defined as a correlated multivariate Normal distribution across 10 consecutive discrete time-steps such that the optimality likelihood is computed for the entire discretised path. As the cost function is convex and we are optimising the paths directly---i.e. not searching for an indirect policy that generates the candidate paths---the solution is trivial. Nonetheless, the example is useful to illustrate the differences between SigSVGD and SVMP.

:::: {#fig:tracking .figure latex-placement="h"}
![](Barcelos2023Path_figs/sequential_distribution.png)

::: caption
**Qualitative analysis of trajectory tracking task.** *Left*: Contour plot of the optimality distribution over sequential time-steps (on $z$-axis). *Centre-left*: Cross-section plot at a given time-step of initial path coordinates. The colour of each path indicates its normalised optimality probability. *Centre-right*: Cross-section plot of the paths after SVGD optimisation. The sampled paths are diverse and capture the variance of the target distribution. Note, however, that many non-optimal trajectories are close to the origin due to the lack of coordination between consecutive time-steps. *Right*: Cross-section plot of the paths after SigSVGD optimisation. Note how we achieve both diversity and a concentration of optimal paths near the origin.
:::
::::

The initial paths are sampled from a uniform distribution and optimised with SVMP and SigSVGD for 200 iterations. The length scale of the squared-exponential kernel is computed according to Silverman's rule [@silverman_density_1986] based on the initial sample for SigSVGD and updated at each iteration using the same method for SVMP. The results in [7](#fig:tracking){reference-type="ref+label" reference="fig:tracking"} show how both methods are able to promote diversity on the resulting paths. However, close inspection of the SVMP solution illustrates how coordinates of the candidate paths at each time-step are optimised without coordination, resulting in many paths crisscrossing and non-optimal paths close to the origin. Conversely, SigSVGD is promoting diversity of complete paths, rather than coordinates at each cross-sectional time-step, resulting in more direct paths with higher optimality likelihood.

# Including Hyper-priors in SigSVGD {#app:hyperprior}

As mentioned in [4.2](#sec:svmp_on_splines){reference-type="ref+label" reference="sec:svmp_on_splines"}, if one wants to constraint the feasible set of the SVGD optimisation a *hyper-prior* can be included in the algorithm. Let $\pdf{h}[\cdot]$ be a hyper-prior and $\pPdf[\cdot]$ the prior distribution over particles ${\boldsymbol{\mathbf{x}}}, {\boldsymbol{\mathbf{y}}}\in {\mathcal{\MakeUppercase{X}}}$ and recall that the *score function* at each update is computed according to $$\begin{equation*}
    {\scoreFunc}^{*} ({\boldsymbol{\mathbf{x}}}) = \expectation_{{\boldsymbol{\mathbf{y}}}\sim \pPdf} [\big]
    [k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}} \grad_{{\boldsymbol{\mathbf{y}}}} \log \pPdf[{\boldsymbol{\mathbf{y}}}\mid\mathcal{O}] + \grad_{{\boldsymbol{\mathbf{y}}}} k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}}],
\end{equation*}$$ where the posterior distribution can be factored in $\log \pPdf[{\boldsymbol{\mathbf{y}}}\mid\mathcal{O}] = \logLik[\mathcal{O}\mid{\boldsymbol{\mathbf{y}}}] + \log \pPdf[{\boldsymbol{\mathbf{y}}}]$. We can include the hyper-prior in the formulation by variable substitution. Let $\log \pdf{\hat{p}}[\cdot] = \log \pPdf[\cdot] + \log \pdf{h}[\cdot]$, then $$\begin{align*}
    {\scoreFunc}^{*} ({\boldsymbol{\mathbf{x}}}) &= \expectation_{{\boldsymbol{\mathbf{y}}}\sim \pPdf} [\big]
    [k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}} \grad_{{\boldsymbol{\mathbf{y}}}} \log \pPdf[{\boldsymbol{\mathbf{y}}}\mid\mathcal{O}] + \grad_{{\boldsymbol{\mathbf{x}}}} k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}}] \\
    {\scoreFunc}^{*} ({\boldsymbol{\mathbf{x}}}) &= \expectation_{{\boldsymbol{\mathbf{y}}}\sim \pPdf} [\bigg]
    [k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}} \grad_{{\boldsymbol{\mathbf{y}}}} \bracks[\big]{\logLik[\mathcal{O}\mid{\boldsymbol{\mathbf{y}}}] + \log \pdf{\hat{p}}[{\boldsymbol{\mathbf{y}}}]}
    + \grad_{{\boldsymbol{\mathbf{y}}}} k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}}] \\
    {\scoreFunc}^{*} ({\boldsymbol{\mathbf{x}}}) &= \expectation_{{\boldsymbol{\mathbf{y}}}\sim \pPdf} [\bigg]
    [k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}} \grad_{{\boldsymbol{\mathbf{y}}}} \bracks[\big]{\logLik[\mathcal{O}\mid{\boldsymbol{\mathbf{y}}}] + \log \pPdf[{\boldsymbol{\mathbf{y}}}] + \log \pdf{h}[{\boldsymbol{\mathbf{y}}}]}
    + \grad_{{\boldsymbol{\mathbf{y}}}} k^{\oplus} \parens{{\boldsymbol{\mathbf{y}}}, {\boldsymbol{\mathbf{x}}}}],
\end{align*}$$ where $\pdf{h}[\cdot]$ can be any differentiable probability density function. $\hfill\blacksquare$

[^1]: $^{*}$`lucas.barcelos@sydney.edu.au`

[^2]: $^{1}$The University of Sydney, Australia

[^3]: $^{2}$CSIRO, Australia

[^4]: $^{3}$NVIDIA, United States
