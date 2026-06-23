---
citation_key: Yu2026PISTO
arxiv_id: 2605.07215
arxiv_url: https://arxiv.org/abs/2605.07215
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:54:01Z
origin: ai+web
reviewed: false
---

# Introduction

Motion planning is central to robotics, enabling autonomous systems to generate collision-free, dynamically feasible trajectories in cluttered environments. While sampling-based methods such as PRM and RRT$^\star$ [@karaman2011sampling; @phillips2012asymptotically] provide strong exploration and asymptotic guarantees, their trajectories often require substantial post-processing for smoothness and dynamic feasibility. Consequently, trajectory optimization has become essential for high-performance planning in manipulation, mobile robotics, and aerial systems.

Optimization-based planners---including CHOMP [@ratliff2009chomp; @zucker2013chomp], sequential convex programming [@schulman2014motion], and Gaussian process methods [@mukadam2017gaussian; @mukadam2018gaussian]---represent trajectories in continuous time and optimize for smoothness, collision avoidance, and dynamic constraints. These approaches achieve impressive speed and scalability, but they rely on differentiable cost representations and remain susceptible to local minima in highly nonconvex environments.

Stochastic trajectory optimization broadens the class of tractable objectives by introducing sampling. STOMP [@kalakrishnan2011stomp] and path-integral methods such as PI$^2$ [@theodorou2010generalized] perturb candidate trajectories and update them via cost-weighted averaging, enabling optimization under non-differentiable and discontinuous costs. A natural question arises: what objective does STOMP implicitly optimize?

We show that STOMP minimizes the reverse KL divergence from a Boltzmann trajectory distribution, revealing an elegant variational inference structure underlying its updates. This connection places STOMP within a broader inference-based planning framework [@kappen2005path; @todorov2009efficient; @chen2016relation], where trajectory costs define a Boltzmann distribution whose high-probability mass concentrates on desirable plans. Gaussian variational inference formulations (GVIMP) [@yu2023gvimp] approximate this distribution with a structured Gaussian family, providing uncertainty quantification and a principled KL-divergence objective.

Building on this insight, we develop a proximal inference algorithm that stabilizes STOMP's updates. Proximal methods [@parikh2014proximal; @chen2022improved] augment each iterate with a penalty on the distance from the current solution, effectively creating a trust region that prevents overly aggressive steps. In the distributional setting, this naturally extends to KL-divergence penalties between successive proposals, controlling how rapidly the trajectory distribution evolves. By combining the variational inference perspective with proximal regularization, we obtain closed-form mean updates computable via importance-weighted Monte Carlo sampling---a simple, derivative-free algorithm that inherits STOMP's flexibility while offering principled stability guarantees.

***Contributions:***

- We reveal that STOMP implicitly minimizes KL divergence from a Boltzmann trajectory distribution, establishing its variational inference structure and motivating principled algorithmic improvements.

- We propose *Proximal Inference for Stochastic Trajectory Optimization (PISTO)*, which augments the reverse-KL objective with a proximal penalty between successive Gaussian proposals. This formulation admits a trust-region interpretation, stabilizes optimization dynamics, and yields closed-form mean updates computable via importance-weighted Monte Carlo sampling.

- We demonstrate PISTO's effectiveness across diverse robotics tasks: on motion planning benchmarks, PISTO achieves 89% success rate---outperforming CHOMP (63%), STOMP (68%), and natural gradient descent (76%)---while running twice as fast as competing stochastic methods. On contact-rich MuJoCo tasks, PISTO consistently outperforms CEM and MPPI baselines in reward despite non-differentiable dynamics.

# Related Work {#sec:related_work}

#### Planning as Inference

The interpretation of optimal control as probabilistic inference connects to linearly-solvable control [@todorov2009efficient], path-integral methods [@kappen2005path], and variational formulations in RL [@levine2018reinforcement]. Within motion planning, Toussaint [@toussaint2009robot] applied message passing on graphical models, while Stein Variational approaches [@power2024constrained] maintain trajectory distributions via particle-based inference. Our work builds on the Planning as Inference paradigm [@yu2023gvimp; @cosier2024unifying; @petrovic2019stochastic; @petrovic2022mixtures; @chang2025efficient] , which showed that trajectory optimization with control-energy regularization is equivalent to KL-divergence minimization from a Boltzmann distribution. We solve the inference problem using a proximal inference algorithm that provides stable optimization and efficient Monte Carlo estimation. Other works under this paradigm are closely related. The variational and heteroscedasticity GP planners [@cosier2024unifying; @petrovic2019stochastic] either rely on pre-defined kernels, induction point approximations, or start and goal states, which cannot be easily extended to control space optimization. Mixtures of Gaussian Processes for Trajectory Optimization (MGPTO) [@petrovic2022mixtures] obtains a multi-modal trajectory using a STOMP-style cost-weighted stochastic gradient estimate. P-GVIMP [@chang2025efficient] leverages GPU parallel computation to accelerate the mean and covariance updates in a gradient-descent landscape.

#### Trajectory Optimization

Gradient-based methods such as CHOMP [@ratliff2009chomp; @zucker2013chomp], TrajOpt [@schulman2014motion], and GPMP [@mukadam2017gaussian] achieve fast convergence but require differentiable costs. Sampling-based methods relax this requirement: STOMP [@kalakrishnan2011stomp] uses cost-weighted averaging, path integral methods (PI$^2$ [@theodorou2010generalized], MPPI [@williams2017mppi]) derive updates from stochastic control, and CEM [@rubinstein1999cem] fits distributions to elite samples. Our method differs by: (i) revealing STOMP's variational inference structure via KL-divergence; (ii) introducing proximal regularization for trust-region stability; and (iii) deriving closed-form updates amenable to importance sampling.

Our method introduces three key innovations over these approaches: (i) an explicit connection between STOMP's objective and KL-divergence minimization, revealing its variational inference structure; (ii) proximal regularization that stabilizes updates with a trust-region interpretation; and (iii) a reversed KL formulation yielding closed-form mean updates amenable to unbiased importance sampling.

# Stochastic Trajectory Optimization as Variational Inference Planning {#sec:framework}

In this section, we establish the theoretical foundation of our approach by connecting classical stochastic trajectory optimization with variational inference. We begin by introducing the STOMP framework, followed by its interpretation as a variational inference problem.

## Stochastic Trajectory Optimization (STOMP)

Stochastic Trajectory Optimization for Motion Planning (STOMP) [@kalakrishnan2011stomp] is a gradient-free optimization framework designed to handle non-differentiable and discontinuous cost functions. It explores the trajectory space by generating stochastic perturbations around a nominal trajectory and updating it based on the exponentiated cost of these samples.

Let $Y \in \mathbb{R}^{n(T+1)}$ represent the mean of a $T$-length state trajectory, defined as $Y \triangleq \{x_t\}_{t=0}^T$. STOMP seeks to minimize the expectation of a cost functional over a proposal Gaussian distribution $\tilde{Y} \sim \mathcal{N}(Y, \Sigma)$: $$\begin{equation}
\label{eq:obj_stomp}
\min_Y \mathcal{J}_1(Y) \triangleq \mathbb{E}_{\tilde{Y}} \left[ S(\tilde{Y}) + \frac{1}{2} \tilde{Y}^\top R \tilde{Y} \right],
\end{equation}$$ where $S(\tilde{Y}) = \sum_{t=0}^T V(\tilde{Y}_t)$ is the state-dependent potential (e.g., obstacle avoidance) and $R = A^\top A$ is the control cost matrix for double integrator dynamics, with $A \in \mathbb{R}^{(T-1) \times (T+1)}$ the finite-difference acceleration operator applying the stencil $[1,-2,1]/\Delta t^2$ at interior nodes.

This stochastic formulation allows the planner to \"smooth\" the cost landscape, effectively escaping local minima that often trap purely gradient-based methods.

## Variational Inference Interpretation of STOMP

The objective [\[eq:obj_stomp\]](#eq:obj_stomp){reference-type="eqref" reference="eq:obj_stomp"} admits a Variational Inference (VI) interpretation that recasts trajectory optimization as approximating an optimal path distribution. Any cost function over trajectories induces a Boltzmann distribution $$\begin{equation}
p^\star(\tilde{Y}) \propto \exp\left( -S(\tilde{Y}) \right),
\end{equation}$$ where low-cost trajectories receive high probability mass; this construction underlies the connection between optimal control and inference [@kappen2005path; @todorov2009efficient] and path-integral methods [@theodorou2010generalized]. In [\[eq:obj_stomp\]](#eq:obj_stomp){reference-type="eqref" reference="eq:obj_stomp"}, the state-dependent potential $S(\tilde{Y})$ captures task-specific objectives such as obstacle avoidance, while the control cost $\frac{1}{2}\tilde{Y}^\top R \tilde{Y}$ with $R = A^\top A$ corresponds to a Gaussian smoothness prior $\mathcal{N}(0, R^{-1})$ favoring low-acceleration paths. Combining the two yields the main result connecting STOMP to VI.

::: {#thm:stomp_vi .theorem}
**Theorem 1** (Variational Inference Formulation of STOMP). *Consider the stochastic trajectory optimization objective [\[eq:obj_stomp\]](#eq:obj_stomp){reference-type="eqref" reference="eq:obj_stomp"}. Let $\Sigma \succ 0$ be a fixed covariance and $R \succ 0$ be the control cost matrix. Minimizing $\mathcal{J}_1$ over the mean trajectory $Y$ is equivalent to solving the variational inference problem: $$\begin{equation}
\label{eq:obj_STOMP_KL}
\min_Y \; D_{\mathrm{KL}}\left( \mathcal{N}(Y, \Sigma) \;\|\; {\mathbb Y}^\star \right),
\end{equation}$$ where the target distribution is the energy-based posterior: $$\begin{equation}
{\mathbb Y}^\star \propto \exp\left( -S(\tilde{Y}) \right) \mathcal{N}(0, R^{-1}).
\end{equation}$$*
:::

::: proof
*Proof.* See Appendix [6.1](#sec:appendix_proofs){reference-type="ref" reference="sec:appendix_proofs"}-(a). ◻
:::

# Proximal Inference for Stochastic Trajectory Optimization {#sec:methods}

We introduce a novel paradigm for solving the motion planning inference problem: Proximal Inference for Stochastic Trajectory Optimization (PISTO). PISTO reverses the argument order in the KL divergence and augments the objective with a Gaussian proximal term, converting each iteration into a proximal inference minimization whose optimizer admits a closed-form expectation representation amenable to Monte Carlo estimation.

## Solution to the Reverse KL Minimization Problem

We first introduce an important moment-matching solution result in reverse KL minimization problems.

::: {#lem:cem .lemma}
**Lemma 1** (Reverse KL Minimization and Moment-matching Solution). *Consider the reverse KL objective obtained by swapping distributions in [\[eq:obj_STOMP_KL\]](#eq:obj_STOMP_KL){reference-type="eqref" reference="eq:obj_STOMP_KL"}: $$\begin{equation}
\label{eq:obj_STOMP_reverseKL}
\min_Y \; D_{\mathrm{KL}} \left( {\mathbb Y}^\star \parallel \mathcal{N}(Y, \Sigma) \right),
\end{equation}$$ where ${\mathbb Y}^\star \propto e^{-S(\Tilde{Y})} \mathcal{N}(0, R^{-1})$. The gradient of the objective [\[eq:obj_STOMP_reverseKL\]](#eq:obj_STOMP_reverseKL){reference-type="eqref" reference="eq:obj_STOMP_reverseKL"} with respect to $Y$ is $$\begin{align}
\label{eq:grad_CE}
    \nabla_Y D_{\mathrm{KL}} \left( {\mathbb Y}^\star \parallel \mathcal{N}(Y, \Sigma) \right) 
    & = \mathbb{E}_{{\mathbb Y}^\star} \left[ - \Sigma^{-1} (\Tilde{Y} - Y) \right],
\end{align}$$ and the optimal mean is given by $$\begin{equation}
Y^\star = \mathbb{E}_{{\mathbb Y}^\star}[\Tilde{Y}].
\end{equation}$$ With the choice $\Sigma = R^{-1}$ and proposal distribution $\Tilde{Y} \sim \mathcal{N}(Y, R^{-1})$, the importance sampling estimator is $$\begin{equation}
\label{eq:importance_sampling_weight}
\hat{Y}^\star = \sum_{m=1}^{M} \bar{w}_m (Y + \varepsilon_m), \quad \bar{w}_m = \frac{e^{-(S(Y + \varepsilon_m) + \varepsilon_m^\top R Y)}}{\sum_{j=1}^{M} e^{-(S(Y + \varepsilon_j) + \varepsilon_j^\top R Y)}},
\end{equation}$$ where $\varepsilon_m \sim \mathcal{N}(0, R^{-1})$ are i.i.d. samples.*
:::

The proof of Lemma [1](#lem:cem){reference-type="ref" reference="lem:cem"} can be found in [@williams2018information].

## The main PISTO Formulation

::: {#thm:prox_vi .theorem}
**Theorem 2** (Proximal Inference Update). *Consider the proximal update for the VI problem [\[eq:obj_STOMP_KL\]](#eq:obj_STOMP_KL){reference-type="eqref" reference="eq:obj_STOMP_KL"}: $$\begin{align}
Y_{k+1} = \arg\min_Y \; & D_{\mathrm{KL}} \left( \mathcal{N}(Y,\Sigma) \parallel {\mathbb Y}^\star \right) 
\\
&+ \frac{1}{\eta} D_{\mathrm{KL}}\left(\mathcal{N}(Y,\Sigma) \parallel \mathcal{N}(Y_k,\Sigma)\right),
\end{align}$$ where $\eta > 0$ is the step size parameter, $Y_k$ is the current iterate, and ${\mathbb Y}^\star \propto e^{-S(\Tilde{Y})} \mathcal{N}(0, R^{-1})$ is the target distribution. Then the proximal update is equivalent to KL projection onto a surrogate distribution: $$\begin{equation}
\label{eq:prox_KL}
Y_{k+1} = \arg\min_Y \; D_{\mathrm{KL}} \left( \mathcal{N}(Y,\Sigma) \parallel {\mathbb Y}^\star_k \right),
\end{equation}$$ where the surrogate target ${\mathbb Y}^\star_k$ admits the explicit form $$\begin{equation}
{\mathbb Y}^\star_k \propto \left( e^{-S(\Tilde{Y})} \mathcal{N}(0, R^{-1}) \right)^{\frac{\eta}{\eta+1}} \left( \mathcal{N}(Y_k, \Sigma) \right)^{\frac{1}{\eta+1}}.
\end{equation}$$*
:::

::: proof
*Proof.* Appendix [6.1](#sec:appendix_proofs){reference-type="ref" reference="sec:appendix_proofs"}-(c). ◻
:::

::: remark
**Remark 1**. *The surrogate distribution ${\mathbb Y}^\star_k$ geometrically interpolates between the true target ${\mathbb Y}^\star$ and the current Gaussian approximation $\mathcal{N}(Y_k, \Sigma)$. As $\eta \to \infty$, the surrogate converges to the true target, recovering standard VI. For finite $\eta$, the proximal term regularizes the update, improving numerical stability and convergence.*
:::

## Moment-matching Solution to the Proximal Inference

Eq. [\[eq:prox_KL\]](#eq:prox_KL){reference-type="eqref" reference="eq:prox_KL"} indicates that each proximal iteration is itself a VI problem with respect to the surrogate distribution ${\mathbb Y}^\star_k$, which is typically easier to handle than the original Boltzmann distribution. To compute the update, we solve the reverse KL-minimization projection $$\begin{equation}
\label{eq:CE_prob_step_k}
Y_{k+1}=\arg\min_Y D_{\mathrm{KL}} \left( {\mathbb Y}^\star_k  \parallel \mathcal{N}(Y,\Sigma)\right).
\end{equation}$$ To sample from ${\mathbb Y}^\star_k$, we rewrite it in a tilted-Gaussian form by completing the square. Letting $\gamma \triangleq \frac{\eta}{\eta+1}$, we obtain $$\begin{align}
    \log {\mathbb Y}^\star_k 
    &\propto 
    -\gamma S(\Tilde{Y}) - \frac{1}{2} (\Tilde{Y}-\mu_k)^\top P(\Tilde{Y}-\mu_k),
\end{align}$$ where $P = \gamma R + (1-\gamma)\Sigma^{-1}$ and $\mu_k = (1-\gamma)P^{-1}\Sigma^{-1}Y_k$. This representation reveals that ${\mathbb Y}^\star_k$ behaves like a Gaussian whose mean is shifted by the proximal term, modulated by an exponential tilt involving the cost function: $$\begin{align}
    {\mathbb Y}^\star_k \propto e^{-\gamma S(\Tilde{Y})}\mathcal{N}(\Tilde{Y}; \mu_k, P^{-1}).
\end{align}$$ Applying the gradient identity from [\[eq:grad_CE\]](#eq:grad_CE){reference-type="eqref" reference="eq:grad_CE"} to the reverse KL-minimizing objective [\[eq:CE_prob_step_k\]](#eq:CE_prob_step_k){reference-type="eqref" reference="eq:CE_prob_step_k"} and setting it to zero yields the following result.

::: {#thm:moment_matching .theorem}
**Theorem 3** (Moment-Matching Update). *The solution to the reverse KL-minimization projection [\[eq:CE_prob_step_k\]](#eq:CE_prob_step_k){reference-type="eqref" reference="eq:CE_prob_step_k"} satisfies the condition $$\begin{align}
    \nabla_{Y}D_{\mathrm{KL}} \left( {\mathbb Y}^\star_k  \parallel \mathcal{N}(Y,\Sigma)\right) = \mathbb{E}_{{\mathbb Y}^\star_k}\left[ -\Sigma^{-1}(\Tilde{Y} - Y) \right] = 0,
\end{align}$$ which admits the closed-form moment-matching update $$\begin{align}
\label{eq:moment_matching_update}
    Y_{k+1} = \mathbb{E}_{{\mathbb Y}^\star_k}[ \Tilde{Y} ].
\end{align}$$ That is, the next iterate is simply the mean of the surrogate distribution ${\mathbb Y}^\star_k$.*
:::

## Importance Sampling

To estimate the expectation in [\[eq:moment_matching_update\]](#eq:moment_matching_update){reference-type="eqref" reference="eq:moment_matching_update"}, we employ importance sampling from a Gaussian proposal distribution. Similar to Eq. [\[eq:importance_sampling_weight\]](#eq:importance_sampling_weight){reference-type="eqref" reference="eq:importance_sampling_weight"}, the weight at iteration $k$ is $$\begin{align*}
    w_k(\Tilde{Y}) &\triangleq \frac{e^{-\gamma S(\Tilde{Y})} \mathcal{N}(\Tilde{Y}; \mu_k, P^{-1})}{\mathcal{N}(\Tilde{Y}; Y_k, P^{-1})}  \propto e^{-\gamma S(\Tilde{Y}) - \Tilde{Y}^T P (Y_k - \mu_k)}.
\end{align*}$$ In the common choice $\Sigma = R^{-1}$, the expression simplifies considerably, as $P = R$ and $\mu_k = (1-\gamma)Y_k$: $$\begin{align}
    w_k(\Tilde{Y}) \propto  e^{-\gamma (S(\Tilde{Y}) + \Tilde{Y}^T R Y_k) }.
\end{align}$$ Using these weights, we obtain a Monte-Carlo estimation of the proximal update: $$\begin{align}
    Y_{k+1} \approx \sum_{m=1}^{M}\; \frac{e^{-\gamma (S(Y_k + \varepsilon_m) + \varepsilon_m^T R Y_k)}}{\sum_{j=1}^{M} e^{-\gamma (S(Y_k + \varepsilon_j) + \varepsilon_j^T R Y_k)}} (Y_k + \varepsilon_m),
\end{align}$$ where $\varepsilon_m \sim \mathcal{N}(0, R^{-1}), \;m=1,\dots,M$ are sampled independently. This Monte Carlo estimator completes the proximal inference update, providing a stable and efficient mechanism for refining the Gaussian approximation at each iteration.

:::: algorithm
::: algorithmic
Accumulated cost $S(\cdot)$, smoothness matrix $R$, Cholesky factor $L$ with $LL^\top = R^{-1}$, sample size $M$, proximal parameter $\eta$, current iterate $Y_k$, temperature $\tau$ Updated iterate $Y_{k+1}$ Compute $\gamma \gets \dfrac{\eta}{\eta + 1}$ **Sample:** Draw $\{\varepsilon_m\}_{m=1}^M$ where $\varepsilon_m = L z_m$, $z_m \sim \mathcal{N}(0, I)$ **Evaluate:** For each $m = 1, \ldots, M$, compute importance weights $$w_m \gets \exp\!\Big(-\frac{\gamma}{\tau} \, S(Y_k + \varepsilon_m) - (\varepsilon_m)^\top R \, Y_k \Big)$$ **Normalize:** Compute normalized weights $$\bar{w}_m \gets \frac{w_m}{\sum_{j=1}^M w^{(j)}}, \quad \forall m$$ **Update:** Compute weighted mean $$Y_{k+1} \gets Y_k + \sum_{m=1}^M \bar{w}_m \, \varepsilon_m$$ $Y_{k+1}$
:::
::::

:::: {.figure latex-placement="h"}
![Box Scene](Yu2026PISTO_figs/pce_box.png){width="90%"}

![Kitchen Scene](Yu2026PISTO_figs/pce_kitchen.png){width="95%"}

![Bookshelf Scene](Yu2026PISTO_figs/pce_bookshelf_thin.png){width="90%"}

![Table Scene](Yu2026PISTO_figs/pce_table.png){width="90%"}

::: caption
Results of PISTO in different motion planning benchmarking scenes.
:::
::::

:::: {#fig:humanoidstandup .figure latex-placement="h"}
![The PushT Task. Optimization time: $260.62 (s)$. ](Yu2026PISTO_figs/pushT.png){width="90%"}

![The Humanoid Running Task. Optimization time: $142.21 (s)$.](Yu2026PISTO_figs/humanoidrun.png){width="90%"}

![The Humanoid Standing Up Task. Optimization time: $168.11 (s)$. ](Yu2026PISTO_figs/humanoidstandup.png){width="90%"}

::: caption
The optimization results for contact-rich tasks.
:::
::::

:::: {.figure latex-placement="h"}
![PISTO](Yu2026PISTO_figs/kitchen_pce.png){width="\\textwidth"}

![NGD](Yu2026PISTO_figs/kitchen_ndg.png){width="\\textwidth"}

![STOMP](Yu2026PISTO_figs/kitchen_stomp.png){width="\\textwidth"}

![CHOMP](Yu2026PISTO_figs/kitchen_chomp.png){width="\\textwidth"}

::: caption
Results of different planners in the Kitchen scene in the database.
:::
::::

## Policy Optimization for Contact-Rich Tasks {#sec:rl_to}

We now extend PISTO to policy optimization in the action space, where the decision variable is the *control sequence* $U = \{u_t\}_{t=0}^{T-1}$ and states evolve according to known dynamics models.

#### Formulation

Given initial state $x_0 \in \mathbb{R}^{d_x}$, consider the finite-horizon optimal control problem: $$\begin{equation}
\label{eq:mpc_objective}
\min_{U} \; \sum_{t=0}^{T-1} c(x_t, u_t)
\end{equation}$$ subject to the dynamics and control constraints: $$\begin{align}
x_{t+1} &= g(x_t, u_t), \quad t = 0, \ldots, T-1, \label{eq:dynamics} \\
u_t &\in \mathcal{U} \subseteq \mathbb{R}^{d_u}, \quad t = 0, \ldots, T-1, \label{eq:control_bounds}
\end{align}$$ where $U = (u_0, \ldots, u_{T-1}) \in \mathbb{R}^{T \times d_u}$, $c: \mathbb{R}^{d_x} \times \mathbb{R}^{d_u} \to \mathbb{R}$ is the stage cost, $g: \mathbb{R}^{d_x} \times \mathbb{R}^{d_u} \to \mathbb{R}^{d_x}$ is the dynamics model, and $\mathcal{U} = [\underline{u}, \bar{u}]$ is the admissible control set.

#### Composite Structure of the Objective

The state trajectory is uniquely determined by the initial condition and control sequence via recursive application of [\[eq:dynamics\]](#eq:dynamics){reference-type="eqref" reference="eq:dynamics"}. We formalize this through the *flow map* $\phi_t: \mathbb{R}^{d_x} \times \mathbb{R}^{t \times d_u} \to \mathbb{R}^{d_x}$: $$\begin{equation}
\label{eq:flow_map}
x_t = \phi_t(x_0, u_{0:t-1}) \triangleq \underbrace{g \circ g \circ \cdots \circ g}_{t \text{ times}}(x_0, u_{0:t-1}),
\end{equation}$$ with the convention $\phi_0(x_0) = x_0$. Substituting into [\[eq:mpc_objective\]](#eq:mpc_objective){reference-type="eqref" reference="eq:mpc_objective"} and defining the *rollout cost* $$\begin{equation}
\label{eq:rollout_cost}
S(U; x_0) \triangleq \sum_{t=0}^{T-1} c\bigl(\phi_t(x_0, u_{0:t-1}), u_t\bigr),
\end{equation}$$ the optimal control problem reduces to the form of [\[eq:obj_stomp\]](#eq:obj_stomp){reference-type="eqref" reference="eq:obj_stomp"}: $$\begin{equation}
\label{eq:policy_opt_stomp}
\min_U \; \mathbb{E}_{\tilde{U}} \left[ S(\tilde{U}; x_0) + \frac{1}{2} \tilde{U}^\top R \tilde{U} \right],
\end{equation}$$ where the quadratic term $\frac{1}{2} \tilde{U}^\top R \tilde{U}$ regularizes the control sequence for temporal smoothness. Algorithm [\[alg:pisto\]](#alg:pisto){reference-type="ref" reference="alg:pisto"} applies directly in this setting, with each sample $\tilde U^{(i)} \sim \mathcal{N}(U, \Sigma)$ evaluated by rolling out the dynamics $\phi_t$ to obtain $S(\tilde U^{(i)}; x_0)$. This formulation enables PISTO to optimize directly in control space without requiring differentiability of $g$ or $c$, and admits efficient parallelization of rollouts on modern GPU hardware.

## Covariance and Proximal Step Size Annealing

To balance exploration and exploitation, we implement covariance scheduling with adaptive temperature scaling. We scale the smoothness matrix, $\bar{R} = \sigma_k \times R$, and use $\bar{R}$ matrix as the actual matrix that we sample from. The covariance scale $\sigma_k$ follows cosine annealing: $$\begin{equation}
    \sigma_k = \sigma_{\text{final}} + \frac{1}{2}(\sigma_{\text{init}} - \sigma_{\text{final}})\left(1 + \cos\left(\frac{\pi k}{K_{\mathrm{max}}}\right)\right),
\end{equation}$$ where $k$ is the current iteration and $K_{\mathrm{max}}$ the maximum. We introduce an adaptive annealing scheme for the proximal step size parameter $\eta$ governing the exploration-exploitation trade-off in importance-weighted trajectory optimization. We also introduce an additional temperature parameter $\tau$ to scale the impact of the adaptive proximal step size. The importance weights are $w_m \propto \exp\left(-\frac{\gamma}{\tau} S(Y_k + \varepsilon_m) - (\varepsilon_m)^\top R Y_k\right)$. We anneal $\eta$ from small to large values via an exponential schedule $\eta(t) = \eta_{\text{initial}} \cdot (\eta_{\text{final}} / \eta_{\text{initial}})^{t/T}$, where small $\eta$ encourages exploration through nearly uniform weights while large $\eta$ exploits high-reward samples with peaked weights. The temperature $\tau$ amplifies only the energy term, leaving regularization unaffected, enabling independent control over reward sensitivity and trajectory smoothness .

:::: {#fig:benchmarking_result .figure latex-placement="h"}
![Success Rate](Yu2026PISTO_figs/Success_Rate_New.png){width="\\textwidth"}

![Planning Time](Yu2026PISTO_figs/Planning_Time_New.png){width="\\textwidth"}

![Path Length](Yu2026PISTO_figs/Path_Length_New.png){width="\\textwidth"}

![Path Clearance](Yu2026PISTO_figs/Path_Clearance_New.png){width="\\textwidth"}

::: caption
Benchmark Performance Statistics
:::
::::

# Experiments

All experiments were run on a computer with an Intel Core i7-12800H CPU. The MuJoCo experiments were run on a computer with an NVIDIA RTX 4090 GPU. The code for this paper is implemented in C++ for the motion planning tasks, and in Python for the trajectory optimization tasks in MuJoCo.

## Motion Planning for Robot Arms

For collision avoidance, we define the state cost $V(Y_t)$ using two formulations. The *signed-distance* cost approximates the robot as a union of spheres and evaluates $$\begin{equation}
    V_{\rm coll}(Y_t) = \big\| h_{\delta}\left( d_{\mathrm{sdf}}(F(Y_t)) \right) \big\|_{\Sigma_{\rm obs}}^{2},
\end{equation}$$ where $F(\cdot)$ is the forward kinematics, $d_{\mathrm{sdf}}(\cdot)$ queries a precomputed signed distance field (SDF), and the hinge function $h_{\delta}(\cdot)$ penalizes penetrations within margin $\delta$. The non-differentiable *indicator* cost, used in MoveIt benchmarking experiments, imposes a fixed penalty on detected collision: $$\begin{equation}
    V_{\rm coll}(Y_t) = W_{\rm obs}\, \mathbf{1}_{\mathrm{CollisionDetected}(Y_t)}.
\end{equation}$$ The weights $\Sigma_{\rm obs}$ and $W_{\rm obs}$ are task-dependent hyper-parameters.

## Policy Optimization Tasks

We tested the PISTO algorithm on various tasks defined in MuJoCo [@todorov2012mujoco]. We used Bayesian optimization-based parameter sweeping to obtain the recommended parameters for each task. Figure [1](#fig:humanoidstandup){reference-type="ref" reference="fig:humanoidstandup"} illustrates the optimization process for a standing up task for a $17$-DOF humanoid robot. Table [\[tab:combined_benchmarking\]](#tab:combined_benchmarking){reference-type="ref" reference="tab:combined_benchmarking"} records the achieved rewards for different tasks. *Planning and Runtime Results:* Table [\[tab:combined_benchmarking\]](#tab:combined_benchmarking){reference-type="ref" reference="tab:combined_benchmarking"} records PISTO's performance in contact-rich trajectory optimization tasks, compared with CEM and MPPI methods. The results are averaged over $50$ independent runs. Our proposed PISTO algorithm significantly outperforms both baselines across all five contact-rich tasks, achieving approximately $1.5\times$ improvement on Walker2d and $2.8\times$ on HumanoidRun compared to the best baseline, while converting negative MPPI performance on PushT ($-0.17$) into a positive reward of $0.46$. PISTO also runs $1.4\times$--$3.2\times$ faster than baselines on most tasks, with particularly notable speedups on HumanoidRun ($36.5$s vs. $\sim$`<!-- -->`{=html}115s). The tight standard deviations indicate reliable convergence despite discontinuous contact dynamics. Notably, PISTO achieves successful results for the $17$-DOF humanoid running and standing-up tasks within minutes. These results validate PISTO's robustness for trajectory optimization in hybrid dynamical systems.

:::: table*
::: tabular
llcccccccc **Task** & **Method** & &**Success/Reward** & **Time (s)** & **Path Length** & **Path Clearance**\
\
& CHOMP & & 63.05% & 0.498 & 8.519 & 0.108\
& STOMP & & 67.59% & [0.481]{.underline} & [8.424]{.underline} & 0.113\
& NGD & & [75.76]{.underline}% & 0.499 & 8.838 & **0.161**\
& PISTO & & **88.57**% & **0.237** & **8.421** & [0.124]{.underline}\
& & **Runtime**\
(lr)2-4 (lr)5-8 **Task** & PISTO & CEM & MPPI & PISTO & CEM & MPPI &\
\
PushT & $\textbf{0.4559} \pm 0.1291$ & $0.1004 \pm 0.1416$ & $-0.1715 \pm 0.1407$ & $134.6235s \pm 0.8061 s$ & $229.17s \pm 1.48s$ & $228.55s \pm 1.44s$ &\
Hopper & $\textbf{1.2645} \pm 0.0201$ & $0.6931 \pm 0.1390$ & $0.9195 \pm 0.1222$ & $49.13s ± 1.51s$ & $58.76s \pm 2.61s$ & $58.53s \pm 2.47s$ &\
Walker2d & $\textbf{1.2622} \pm 0.0828$ & $0.8603 \pm 0.1107$ & $0.7505 \pm 0.1642$ & $65.99s \pm 1.50s$ & $75.13s \pm 2.57s$ & $75.14s \pm 2.72s$ &\
HumanoidRun & $\textbf{1.3385} \pm 0.2921$ & $0.4106 \pm 0.2509$ & $0.485 \pm 0.3104$ & $36.48s \pm 1.64s$ & $117.62s \pm 14.42s$ & $112.91s \pm 12.98s$ &\
HumanoidStandUp & $\textbf{0.679} \pm 0.058$ & $0.4609 \pm 0.008$ & $0.529 \pm 0.0390$ & $65.29s \pm 2.02s$ & $55.18s \pm 1.44s$ & $54.24s \pm 2.94s$ &\
:::
::::

## Benchmarking with MoveIt Motion Planning Algorithms

We further benchmark PISTO against several representative optimization-based baselines using MoveIt, including the official implementations of STOMP and CHOMP, as well as a natural gradient descent (NGD) method [@yu2023gvimp]. Experiments are conducted on the Franka Emika Panda across seven manipulation environments from the MotionBenchMaker [@chamzas2021motionbenchmaker] dataset, including *Kitchen*, *Bookshelf Tall*, *Bookshelf Thin*, *Table Pick*, *Table Under Pick*, *Box*, and *Cage*, with over 300 planning tasks in total.

For a fair comparison, all planners are initialized using the same joint-space straight-line interpolation between the start and goal configurations. We repeat each planning task 20 times with different random seeds. A run is considered successful if the resulting trajectory is collision-free and satisfies joint limits. Figure [2](#fig:benchmarking_result){reference-type="ref" reference="fig:benchmarking_result"} summarizes the benchmarking results in terms of success rate, planning time, path length, and path clearance.

# Conclusion {#sec:conclusion}

We presented the Proximal Inference for Stochastic Trajectory Optimization (PISTO), a principled algorithm for motion planning formulated as Gaussian variational inference. By revealing STOMP's implicit variational structure, we introduced a proximal formulation that regularizes updates via KL penalties, yielding closed-form moment-matching updates amenable to importance sampling. The resulting algorithm is simple, derivative-free, and parallelizable. Experiments demonstrated that PISTO achieves 89% success on motion planning benchmarks---outperforming CHOMP, STOMP, and natural gradient baselines---while additional MuJoCo experiments validated its effectiveness for high-dimensional, contact-rich tasks. Future work includes incorporating gradients when available, jointly optimizing mean and covariance, and extending to receding-horizon MPC.

## Proofs {#sec:appendix_proofs}

#### Proof of Theorem [1](#thm:stomp_vi){reference-type="ref" reference="thm:stomp_vi"} {#proof-of-theorem-thmstomp_vi}

Define the accumulated state cost $S(\Tilde{Y}) = \sum_{t=0}^T V(\Tilde{Y}_t)$. Since the covariance $\Sigma$ is fixed, the expectation of the quadratic deviation term simplifies via the trace identity $\mathbb{E}[(\Tilde{Y} - Y)^\top R (\Tilde{Y} - Y)] = \operatorname{tr}(R\Sigma)$. Thus, $$\begin{equation*}
\mathcal{J}_1 = \mathbb{E}_{\Tilde{Y}}[S(\Tilde{Y})] + \frac{1}{2}\operatorname{tr}(R\Sigma) + \frac{1}{2}Y^\top R Y.
\end{equation*}$$

We recognize that $\mathbb{E}_{\Tilde{Y}}[S(\Tilde{Y})] = -\mathbb{E}_{\Tilde{Y}}[\log e^{-S(\Tilde{Y})}]$. Combining this with the KL divergence between Gaussians, $$\begin{align*}
&D_{\mathrm{KL}}\left( \mathcal{N}(Y, \Sigma) \| \mathcal{N}(0, R^{-1}) \right) \nonumber
\\
=& \frac{1}{2}\left( \operatorname{tr}(R\Sigma) + Y^\top R Y - \log\det(\Sigma R) - (T+1) \right)
\end{align*}$$ where the last two terms are constants, we obtain $$\begin{equation}
\mathcal{J}_1 = D_{\mathrm{KL}}\left( \mathcal{N}(Y, \Sigma) \| {\mathbb Y}^\star \right) + \text{const},
\end{equation}$$ by introducing the un-normalized ${\mathbb Y}^\star \propto e^{-S(\Tilde{Y})} \mathcal{N}(0, R^{-1})$. Here, the constant is independent of $Y$. Since only the mean $Y$ is optimized, minimizing $\mathcal{J}_1$ is equivalent to minimizing the KL divergence to the target posterior ${\mathbb Y}^\star$.

#### Proof of Theorem [2](#thm:prox_vi){reference-type="ref" reference="thm:prox_vi"} {#proof-of-theorem-thmprox_vi}

Let $q_Y$ and $q_{Y_k}$ denote the density functions of $\mathcal{N}(Y, \Sigma)$ and $\mathcal{N}(Y_k, \Sigma)$, respectively. The proximal objective can be written as $$\begin{align*}
\mathcal{J}_k &= D_{\mathrm{KL}} \left( \mathcal{N}(Y,\Sigma) \parallel {\mathbb Y}^\star \right) + \frac{1}{\eta} D_{\mathrm{KL}}\left(\mathcal{N}(Y,\Sigma) \parallel \mathcal{N}(Y_k,\Sigma)\right) \nonumber \\
&= \mathbb{E}_{\mathcal{N}(Y,\Sigma)}\left[ \left( 1 + \frac{1}{\eta} \right) \log q_Y - \log {\mathbb Y}^\star - \frac{1}{\eta} \log q_{Y_k} \right].
\end{align*}$$ Factoring out the coefficient $\frac{\eta+1}{\eta}$ yields $$\begin{align*}
\mathcal{J}_k &= \frac{\eta+1}{\eta} \, \mathbb{E}_{\mathcal{N}(Y,\Sigma)} \left[ \log q_Y - \log\left( ({\mathbb Y}^\star)^{\frac{\eta}{\eta+1}} (q_{Y_k})^{\frac{1}{\eta+1}} \right) \right] \nonumber \\
&\propto D_{\mathrm{KL}} \left( \mathcal{N}(Y, \Sigma) \parallel {\mathbb Y}^\star_k \right),
\end{align*}$$ where we identify the surrogate distribution as $$\begin{equation*}
{\mathbb Y}^\star_k \propto ({\mathbb Y}^\star)^{\frac{\eta}{\eta+1}} (q_{Y_k})^{\frac{1}{\eta+1}}.
\end{equation*}$$ Substituting the explicit form of ${\mathbb Y}^\star$ completes the proof.

## Implementation Details

#### Elite Sample Selection

To improve convergence and reduce variance, we incorporate elite-set selection within the importance sampling step. Given $M$ rollouts, we define an elite subset $\mathcal{M}_e \subset \{1, \dots, M\}$ containing samples in the lowest $K_{\mathrm{elite}}$-th percentile of cost. Importance weights for $m \notin \mathcal{M}_e$ are set to zero, while for $m \in \mathcal{M}_e$: $$\begin{equation}
    w_m = \frac{\exp(-\gamma J(Y_m) / \tau)}{\sum_{j \in \mathcal{M}_e} \exp(-\gamma J(Y_j) / \tau)},
\end{equation}$$ where $J(\cdot)$ is the trajectory cost and $\tau$ is an adaptive temperature. This selective pressure ensures updates are driven by successful explorations, enabling efficient navigation of non-convex cost landscapes.

#### Momentum-Accelerated Exponential Moving Average

To stabilize convergence and accelerate optimization, we apply a momentum-based update scheme. Let $\hat{Y}_{k+1}$ denote the candidate trajectory computed as the weighted expectation over the elite set $\hat{Y}_{k+1} = \sum_{m \in \mathcal{M}_e} w_m (Y_k + \varepsilon_m).$ We compute the update direction $\Delta_k = \hat{Y}_{k+1} - Y_k$ and maintain a momentum buffer $v_k$ via exponential moving average: $$\begin{equation*}
    v_{k+1} = \beta v_k + (1 - \beta) \Delta_k,
\end{equation*}$$ where $\beta \in [0, 1)$ is the momentum decay coefficient. The trajectory is then updated as: $Y_{k+1} = Y_k + \lambda v_{k+1},$ where $\lambda \in (0, 1]$ is the step size. This two-stage temporal regularization dampens oscillations through directional smoothing while providing momentum for navigating non-smooth cost regions. We also allow the Adam-type [@kingma2014adam] gradient update rule as an option.

[^1]: H. Yu and Y. Chen are with the School of Aerospace Engineering, Z. Chang is with the School of Electrical and Computer Engineering, Georgia Institute of Technology, Atlanta, GA; {hyu419, zchang40, yongchen}@gatech.edu
