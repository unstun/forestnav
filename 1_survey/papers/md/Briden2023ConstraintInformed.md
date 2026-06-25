---
citation_key: Briden2023ConstraintInformed
arxiv_id: 2312.14336
arxiv_url: https://arxiv.org/abs/2312.14336
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:14:39Z
origin: ai+web
reviewed: false
---

# Nomenclature {#nomenclature .unnumbered}

::: longtable*
\@l @= l@ $N$ & number of discretization intervals\
$\theta$ & vector of problem parameters, $\theta \in {\mathbf{R}}^{n_p}$\
$x_t$ & state at time step $t$, $x_t \in {\mathbf{R}}^{n_x}$\
$u_t$ & control input at time step $t$, $u_t \in {\mathbf{R}}^{n_u}$\
$x^*$ & optimal state trajectory\
$u^*$ & optimal control trajectory\
$\lambda^*$ & optimal dual multipliers\
$\hat{x}$ & predicted state trajectory\
$\hat{u}$ & predicted control input\
$\hat{\lambda}$ & predicted dual multipliers\
$z = (x, y, \xi, \delta, v, \alpha)^T$ & configuration of the center point of the rear axle of the lunar rover in a fixed world frame $(x,y,\xi)$\
$u = (\delta_{\text{in}}, \alpha_{\text{in}})^T$ & control of the steering angle control input $\delta_{\text{in}}$ and acceleration control input $\alpha_{\text{in}}$\
$g_t$ & stage cost function at time step $t$\
$\psi_t$ & state transition function at time step $t$\
$f_{t,i}$ & inequality constraint function at time step $t$ for constraint $i$\
$\Theta$ & admissible set of parameters, $\Theta \subseteq {\mathbf{R}}^{n_p}$\
$\phi$ & parameters of neural network\
$\mathcal{D}$ & training dataset\
$\mathcal{L}$ & Lagrangian of the optimization problem\
$\beta_{\mathcal{L}}$ & weighting parameter for the Lagrangian in the merit function\
$\beta_{\mathcal{\nabla L}}$ & weighting parameter for the Lagrangian gradient in the merit function\
$\mathcal{I}$ & set of inequality constraints\
$\mathcal{E}$ & set of equality constraints
:::

# Introduction

[S]{.lettrine}[urface]{.smallcaps} rovers have a rich history of use in planetary exploration, and onboard autonomy has played a critical role in enabling new scientific discoveries. For example, Mars rover missions such as NASA's *Curiosity* and *Perseverance* have driven tens of kilometers through their mission lifetimes, and autonomous driving capabilities such as [ENav]{acronym-label="ENav" acronym-form="singular+short"} have played a crucial part in enabling the rovers to carry out valuable *in situ* measurements and scientific operations [@RankinMaimoneEtAl2020; @VermaMaimoneEtAl2023]. However, current rover missions operate at relatively low driving speeds, allowing [ENav]{acronym-label="ENav" acronym-form="singular+short"} to utilize a simple search-based approach that outputs geometric paths without considering the full system's high-fidelity dynamics, state, and actuator constraints. Future missions that call for operating at significantly faster speeds will require planners that include a trajectory optimization layer and allow the rover to plan trajectories that fully satisfy kinodynamic constraints.

However, Mars rover operations depend heavily on ground-in-the-loop involvement, particularly for navigating difficult or cluttered terrain. This reliance on ground operations limits the distances that rovers can autonomously travel. For instance, the most recent Decadal Survey [@NASEM2022] highlighted the Endurance Lunar rover mission, a long-range surface rover mission that requires driving several kilometers a day [@KeaneTikooEtAl2022]. Consequently, future rover mission concepts that involve driving significantly further distances than *Curiosity* or *Perseverance* require (1) greater onboard autonomy to minimize ground-in-the-loop interventions while (2) operating at significantly faster speeds. Compared to the *Curiosity* rover, *Perseverance* is equipped with more autonomy for planning and utilizes [ENav]{acronym-label="ENav" acronym-form="singular+short"}, a search-based planning approach that generates paths for the rover to follow [@ToupetDelSestoEtAl2020; @DaftryAbcouwerEtAl2022]. Follow-on work has further demonstrated the promise of learning-based approaches to enable faster planning [@DaftryAbcouwerEtAl2022].

Powered descent guidance for planetary landing is known to be particularly challenging for onboard computation; fuel optimal diverts for a general set of state and control constraints require the use of custom solvers to achieve sub-second-level predictions [@Dueri2017; @Elango2022; @kamath2023customized; @kamath2022realtime]. Increasingly complex missions, including Artemis II and Mars Sample Return, will require long-horizon trajectory optimization problems to be solvable online.

Despite the significant advancements in onboard numerical optimization solvers, flight-grade computers remain significantly resource-constrained, lacking the computational power required to solve trajectory optimization problems at the speeds required for real-time operation [@ErenPrachEtAl2017]. Recently, amortized optimization has emerged as a promising solution, leveraging data-driven methods to learn problem-solution mappings, significantly reducing the runtimes required to solve nonlinear optimization problems online [@Amos2023]. However, fully amortized approaches often function as black-box models, learning direct mappings from problem parameters to outcomes without explicitly incorporating the optimization problem's objective or constraints. A field that has been working to overcome these limitations is semi-amortized methods [@Amos2023; @KimWisemanEtAl2018; @MarinoYueEtAl2018]. These methods integrate the optimization problem's objectives and constraints into their models, preserving awareness of physical and safety constraints. Similar advancements include methods that adjust loss function corrective terms to ensure compliance with equality and inequality constraints [@DontiRolnickEtAl2021]. While these new methods make significant progress in incorporating problem-specific information into the learning process, previous work has been problem-specific, including only variational autoencoder architectures, and cannot be easily applied to general neural network architectures and constrained optimization problems. Further, while semi-amortized optimization-based methods incorporate problem-specific information into the learning process, they are often much slower than amortized optimization, requiring multiple expensive backpropagation steps [@KimWisemanEtAl2018].

In this work, we seek to bridge these gaps and develop a semi-amortized optimization approach for efficiently solving trajectory optimization problems on resource-constrained hardware. Including examples of a planetary rover mission and a spacecraft powered descent application. The new algorithm was developed with the following desiderata in mind:

1.  *Performant:* The controller should yield high-quality or near-optimal solutions with respect to some task metric.

2.  *Decision-focused:* The semi-amortized optimization approach should be cognizant of the constraints enforced by the controller downstream.

3.  *Generalizable:* The solution approach should not be tailored to a specific problem formulation and apply to a host of future missions requiring on-board trajectory optimization.

The advances in warm-starting, or initial guess generation, provided in this work have the capability to significantly progress the state-of-the-art for future autonomous surface rover missions and powered descent guidance.

:::: {#fig:alg_outline .figure latex-placement="!t"}
![](Briden2023ConstraintInformed_figs/l4dc_hero.png){width="1.0\\columnwidth"}

::: caption
Schematic of the TOAST approach: learning warm starts for optimization using task-relevant merit functions. Warm starts (green) are predicted by the neural network (pink), which is trained offline with a Lagrangian-based merit function.
:::
::::

## Related Work

In recent years, there has been a flurry of work on applying data-driven and amortized optimization-based techniques, or learning to predict the solutions to similar instances of the same problem, for accelerating solution times for optimization problems [@KotaryFiorettoEtAl2021; @CauligiCulbertsonEtAl2022]. These techniques approach the problem of accelerating solution times for numerical optimization-based control through the lens of parametric programming, a technique to build a function $f : \theta \rightarrow x^*$ that maps the parameters, or context $\theta \subseteq \Theta$, of an optimization problem, $\mathcal{P}(\theta)$, to its solution, $x^*  (\theta) \in {\mathbf{R}}^{n_x}$ [@DuaKouramasEtAl2008]. This is accomplished by sampling $\theta$ representative of the problems of interest, solving for the $x^*$ corresponding to these $\Theta$, and then training an approximation $\hat{f}$ via supervised learning [@Amos2023].

[@DeLaCroixRossiEtAl2024; @GhoshTomarEtAl2024]

In contrast to fully-amortized methods, semi-amortized optimized models map the parameters, or context $\theta \subseteq \Theta$, of an optimization problem, $\mathcal{P}(\theta)$, to its solution, $x^*  (\theta) \in {\mathbf{R}}^{n_x}$ while accessing the objective function of the optimization problem, often iteratively [@Amos2023]. Previous work has established semi-amortized models for variational inference, allowing for the integration of solvers to improve prediction performance [@KimWisemanEtAl2018; @MarinoYueEtAl2018]. These semi-amortized methods involve additional iteration steps over the domain $\mathcal{Y}$ or a latent space $\mathcal{Z}$. Commonly, the optimization procedure is parameterized and integrated into the semi-amortized model $\hat{y}_\theta$, creating a bi-level setting if an outer-level learning problem and inner-level optimization problem [@FinnAbbeelEtAl2017; @KimWisemanEtAl2018; @AndrychowiczDenilEtAl2016]. Due to the computational efficiency requirements for real-time trajectory generation, this work maintains the idea of infusing the optimization process in the learning process, but we do not merge the two processes; to maximum runtime efficiency, all training of learning-based methods occur offline, where the optimization process informs the learning process, then only the learned initial guess is utilized online to warm-start the optimization solve. Maintaining the underlying feasibility and optimality guarantees of the solver.

Applications of amortized optimization for warm-starting trajectory optimization have shown tremendous promise in robotics. The authors in [@ChenWangEtAl2022; @SambharyaHallEtAll2022; @MorelliHofmannEtAl2024] propose using a neural network to warm start solutions for a [QP]{acronym-label="QP" acronym-form="singular+short"}-based [MPC]{acronym-label="MPC" acronym-form="singular+short"} controller. Additional works have studied extensions for quickly solving non-convex optimal control problems online. In [@IchnowskiAvigalEtAl2020], the authors train a neural network to learn the problem solution mapping for a non-convex robotic grasp optimization problem solved using [SQP]{acronym-label="SQP" acronym-form="singular+short"}. The authors in [@BridenGurgaEtAl2024] and [@GuffantiGammelliEtAl2024] train transformer neural networks to learn efficient warm-starts for numerical optimization solvers for trajectory optimization, including applications in powered descent guidance and spacecraft rendezvous. A learned mapping between problem parameters to the set of active tight constraints and final times was shown to reduce solution times for a powered descent guidance problem by more than an order of magnitude [@BridenGurgaEtAl2024]. In spacecraft rendezvous, the transformer-generated warm-starts converge to more fuel-efficient trajectories and higher constraint satisfaction, when compared to convex relaxation benchmarks [@GuffantiGammelliEtAl2024]. Not all approaches overlook the utilization of the learned mappings in relation to the trajectory optimization problem's structure. For example, the work of [@SambharyaStellato2024] demonstrates a methodology that integrates the underlying structure of the optimization problem by unrolling algorithm steps in the Douglas-Rachford (DR) splitting to solve the [QP]{acronym-label="QP" acronym-form="singular+short"}. Further improvements in interior point method-based warm starts for Successive Convex Programming (SCP) include utilizing the solution from the previous SCP iteration while developing an indicator for the degree of problem difference [@MorelliHofmannEtAl2024]. Our work aims to extend these works in semi-amortized optimization by creating a set of generalized merit functions that balance cost minimization with constraint satisfaction. These functions are generalizable to any constrained optimization problem.

## Statement of Contributions

In this work, we introduce Trajectory Optimization with Merit Function Warm Starts (TOAST), a framework designed to bridge the gap in the aforementioned fields of amortized optimization and nonlinear trajectory optimization. TOAST incorporates two separate phases to warm-start a general set of constrained optimization problems: 1) *Offline Learning*: a neural network is trained to map the problem parameters to the time-varying policy associated with a non-convex trajectory optimization problem and 2) *Online Inference and Solve*: the network and system dynamics are used to predict the full state and control trajectories for a new problem, and this prediction is used to warm start the numerical optimization solver. Rather than learning the fuel control policy and solution trajectory, we emphasize that only the control policy is learned by the neural network. The policy is then propagated through the full system dynamics to enforce the dynamic feasibility of the initial guess. The neural network formulation includes two architecture options: a recurrent neural network (RNN)-based long short-term memory (LSTM) architecture to improve model compactness and enforce the temporal structure of the [OCP]{acronym-label="OCP" acronym-form="singular+short"} and a transformer architecture for more complex [OCP]{acronym-label="OCP" acronym-form="singular+short"}s. The primary contribution of this work is developing a set of constraint-informed merit functions used for computing loss for the neural network during the offline learning phase. Informed by the Lagrangian and the KKT conditions from optimization theory, this novel set of *decision-focused* loss functions jointly learn to minimize the reconstruction error and the feasibility of the prediction using the merit function associated with the underlying trajectory optimization problem. We show through numerical simulations on a surface rover trajectory planning problem and a powered descent guidance problem that our proposed TOAST approach outperforms benchmark amortized optimization approaches with improved constraint satisfaction. As future rover missions incorporate increased onboard decision-making, dynamically feasible trajectory generation will be required to achieve strategic planned trajectories accurately. TOAST significantly improves the computational efficiency of onboard trajectory planning via initial guesses biased toward constraint satisfaction.

*Paper Organization:* This work is organized as follows: Section [2](#sec:technical_background){reference-type="ref" reference="sec:technical_background"} reviews the technical background for our approach, including the terminology for the learned solution mapping, optimization theory background, deep learning architectures, and an overview of decision-focused learning. Our technical approach is covered in Section [3](#sec:technical_approach){reference-type="ref" reference="sec:technical_approach"}, which describes the parametric machine learning problem, control input prediction, and dynamics propagation process and introduces our constraint-informed merit function warm start framework: Trajectory Optimization with Merit Function Warm Starts (TOAST). A set of numerical experiments evaluate the TOAST's performance for Lunar rover model predictive control (MPC) and Mars powered descent guidance in Section [4.3](#sec:application){reference-type="ref" reference="sec:application"}, including introducing the lunar rover problem and powered descent guidance problem formulations, evaluating loss function sensitivity, and evaluating the accuracy and constraint satisfaction for the TOAST LSTM framework, compared to mean-squared-error (MSE) loss. Finally, takeaways and conclusions for this work are reviewed in Section [5](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}.

# Preliminaries {#sec:technical_background}

## Learning a Solution Map

Given a vector of problem parameters $\theta\in{\mathbf{R}}^{n_p}$, a parametric [OCP]{acronym-label="OCP" acronym-form="singular+short"} can be written as $$\begin{equation}
 \label{eq:nlp}
\begin{array}{ll}
\underset{x_{0:N},u_{0:N}}{\textrm{minimize}} \!\!\!& \sum_{t=0}^{N} g_t(x_t,u_t;\theta) \\
\text{subject to}\!\!\!& x_0 = x_\textrm{init}(\theta),\\
& x_{t+1} = \psi_t(x_t,u_t;\theta), \quad t = 0, \dots, N-1,\\
& f_{t,i}(x_t,u_t;\theta) \leq 0, \quad\;\;\;\, t = 0, \dots, N, i = 1,\dots,n_{\mathrm{f}}, \\
\end{array}
\end{equation}$$ where the state $x_t\in{\mathbf{R}}^{n_x}$ and control $u_t\in{\mathbf{R}}^{n_u}$ are the continuous decision variables. Here, the stage cost $g_t(\cdot)$ and terminal cost $g_N(\cdot)$ are assumed to be convex functions, but the dynamical constraints $\phi_t (\cdot)$ and inequality constraints $f_{t,i}(\cdot)$ are assumed smooth but possibly non-convex. The objective function and constraints are functions of the parameter vector $\theta \in \Theta$, where $\Theta \subseteq {\mathbf{R}}^{n_p}$ is the admissible set of parameters.

In robotics, the [OCP]{acronym-label="OCP" acronym-form="singular+short"} is typically solved in a receding horizon fashion as the controller replans periodically, wherein the problem size typically stays fixed. Still, only the problem parameters $\theta$ vary between repeated optimization calls. This setting motivates learning function $f$ that maps problem parameters $\theta$ to the optimal solution $x^*$ for the [OCP]{acronym-label="OCP" acronym-form="singular+short"}, as the learned mapping can be utilized directly (e.g., imitation learning) or as a warm start initialization for the solver.

## Necessary Conditions for Optimality: KKT Conditions

For an inequality-constrained optimization problem, Equation [\[eq:nlp\]](#eq:nlp){reference-type="ref" reference="eq:nlp"}, the first order necessary conditions, or Karush-Kuhn-Tucker (KKT) conditions, must hold at a local optimum. If we take the boundary conditions in Equation [\[eq:nlp\]](#eq:nlp){reference-type="ref" reference="eq:nlp"}, to be defined inside of the set of equality constraints $\psi$, the KKT conditions are as follows,

::: definition
**Definition 1** (First Order Necessary Conditions: KKT Conditions). $$\mathcal{L}(z, \lambda) = \sum_{t=0}^{N} g_t(z_t) - \sum_{i \in \mathcal{I}} \lambda_i f_{t,i}(z_t) - \sum_{i \in \mathcal{E}} \lambda_i \psi_{t,i}(z_t), \; t = 0, \dots, N,$$

1.  $\nabla_x \mathcal{L}(z^*, \lambda^*) = 0$,

2.  $\psi(z^*) = 0, \quad i \in \mathcal{E}$,

3.  $f_i(z^*) \geq 0, \quad i \in \mathcal{I}$,

4.  $\lambda_i^* \geq 0, \quad i \in \mathcal{I}$,

5.  $\lambda_i^* f_i(x^*) = 0 \; \text{and} \; \lambda_j^* \psi_j(z^*) = 0, \quad i \in \mathcal{I}, \; j \in \mathcal{E}$.
:::

The sets $\mathcal{I}$ and $\mathcal{E}$ are the sets of indices for the inequality and equality constraints and $z$ represents the set of decision variables $z = (x, u)$ for the [OCP]{acronym-label="OCP" acronym-form="singular+short"}. Condition 1 denotes dual feasibility, conditions 2-3 include primal feasibility, and conditions 4-5 define complementary slackness. The Lagrangian $\mathcal{L}(z, \lambda)$, which includes the cost function $\sum_{t=0}^{N} g_t(z_t)$ and constraints $f_t$ and $\psi_t$, is equivalent to only the cost $\sum_{t=0}^{N} g_t(z_t)$ when the KKT conditions are met (by condition 5). Further, the gradient of the Lagrangian is zero when evaluated at a KKT point (by condition 1). Not only does the Lagrangian balance cost and constraint satisfaction, but minimization of the Lagrangian naturally meets the KKT conditions, necessary for optimality. This observation informs our choice of the Lagrangian and Lagrangian gradient for our set of constraint-informed merit functions in Section [3.1](#sec: merit functions for warm starts){reference-type="ref" reference="sec: merit functions for warm starts"}.

## Recurrent Neural Network Architectures

Unlike feedforward neural networks, [RNN]{acronym-label="RNN" acronym-form="singular+short"} architectures allow the use of previously gathered information to inform the current decision. Within the context of amortized optimization, recent works have shown how the inherently Markovian structure of the inference procedures used by [RNN]{acronym-label="RNN" acronym-form="singular+short"} architectures such as [LSTM]{acronym-label="LSTM" acronym-form="singular+short"} and [GRU]{acronym-label="GRU" acronym-form="singular+short"} can be used for tackling nonlinear trajectory optimization problems [@SabolYunEtAl2022; @CauligiChakrabartyEtAl2022]. In this work, we extend these [LSTM]{acronym-label="LSTM" acronym-form="singular+short"} frameworks to study the problem of learning warm starts for long-horizon nonlinear trajectory optimization problems in the context of decision-focused learning.

## Transformer Neural Network Architectures

Transformer neural networks (NNs) have shown improved performance in training long-horizon time series data, mitigating the vanishing or exploding gradient problem and allowing for parallelization during training [@Vaswani2017]. Multi-head attention mechanisms enable different parts of the input to garner attention while processing entire sequences in parallel. This work utilizes a transformer NN architecture to predict the control input and propagate the trajectory for the 3 DoF powered descent guidance problem, training the TOAST transformer architecture with the constraint-informed merit functions discussed in the following section.

## Decision-Focused Learning

Amortized optimization has recently gained attention for its potential to improve the computational efficiency of optimal control problems. However, fully amortized models use loss functions that overlook the integration of the trajectory optimization problem's intrinsic structure, as these models generally learn direct mappings from input parameters to solutions without explicit regard for the optimization's constraints and objectives. In contrast, semi-amortized methods actively incorporate these elements, utilizing detailed information about the optimization problem to inform the loss function. In this work, we draw inspiration from decision-focused learning, which integrates neural network training directly with operational decision-making [@WilderDilkinaEtAl2019; @MandiKotaryEtAl2023]. Unlike traditional learning-based approaches that utilize a standard catalog of loss functions, decision-focused learning customizes these functions to reflect the specific parameters and constraints of the optimization problems, aligning closely with the goals of semi-amortized approaches. This approach ensures that the learning process supports the practical deployment of models in decision-making scenarios, which is particularly relevant in control tasks where adherence to physical and safety constraints is crucial. While our approach is inspired by decision-focused learning, decision-focused learning involves integrating the predictions of uncertain quantities into the decision-making process, which differs from the deterministic nature of the direct optimization problems we address.

To extend such semi-amortized approaches, we turn to the solution techniques used for solving constrained optimization to formalize the concept of decision-focused losses and consider *merit functions*, which are a scalar-valued function of problem variables that indicate whether a new iterate is better or worse than the current iterate, with the goal of minimizing a given function [@NocedalWright2006]. Although a candidate merit function for unconstrained optimization problems is the objective function, a merit function for a constrained optimization problem must balance minimizing the cost function with a measure of constraint violation. For example, an admissible merit function for [\[eq:nlp\]](#eq:nlp){reference-type="eqref" reference="eq:nlp"} is the penalty function of the form $\phi(x,\mu) = f(x) + \mu \sum_{i \in \mathcal{E}} |c_i(x)| + \mu \sum_{i \in \mathcal{I}} [ c_i(x) ]^-$, where $[ c_i(x) ]^- = \max\{0, -c_i(x)\}$ (we refer the reader to [@NocedalWright2006] for a more exhaustive discussion and examples of merit functions). TOAST generalizes this definition of a merit function to develop a set of decision-focused loss function formulations to facilitate effective warm-starts for online [MPC]{acronym-label="MPC" acronym-form="singular+short"}.

# Technical Approach {#sec:technical_approach}

In this work, we seek to learn a solution mapping $f (\theta)$ that maps problem parameters $\theta$ to the optimizer $z^* = (x^*, u^*)$, where $x$ are the state trajectories and $u$ are the control inputs. This can be accomplished by approximating the solution map $f (\theta)$ using a deep neural network $f_\phi (\theta)$, wherein $\phi$ are the neural network parameters to be learned. By formulating this problem as a parametric machine learning problem, a dataset $\mathcal{D} = ((\theta_i, z_i))_{i=1}^n$, a parameterized function class $f_\phi$, and a loss function $L(z,f_\phi (\theta))$ are user-specified and the goal of the learning framework is to compute $\phi$ such that the expected risk on unseen data is minimized, $\min_\phi \mathbb{E}[L(z, f_\phi(\theta))]$. Note that the minimum expected risk over unseen data cannot be computed since we cannot access all unseen data. Assuming the training set is a sufficient representation of the unseen data, $\min_{\phi} L(z,f_\phi (\theta))$, the empirical risk (training loss) will well-represent the expected risk (test loss).

If $\hat{z}$ denotes the full primal solution prediction $(\hat{x}, \hat{u})$, then the "vanilla" approach to accomplish this would be to simply model $f_\phi (\cdot)$ as a regressor and output a prediction $\hat{z}$ for the full primal solution, i.e., $f_\phi (\theta) = \hat{z}$. However, this approach has the shortcoming that predicting the full primal solution $\hat{z} \in {\mathbf{R}}^{N(n_x+n_u)}$ can be challenging to supervise due to the large output dimensionality and current approaches do indeed scale poorly with increasing state dimension and time horizon [@ChenWangEtAl2022; @ZhangBujarbaruahEtAl2019].

Rather than learning the full mapping from $\theta$ to $\hat{z}$, we instead learn a time-varying policy $\pi_\tau (\cdot)$, i.e., $$\{ u_\tau \}_{\tau=0}^{N} = \{ \pi_\tau (\theta) \}_{\tau=0}^{N}$$ (see Figure [2](#fig:propagate){reference-type="ref" reference="fig:propagate"}). Given $x_0 = x_\textrm{init}(\theta)$, the state prediction $\hat{x}$ is recovered by simply forward propagating the dynamics: $$\begin{equation*}
\hat{x}_{t+1} = \psi_t(\hat{x}_t, \hat{u}_t; \theta), \quad t = 0, \dots, N-1.\\
\end{equation*}$$

:::: {#fig:propagate .figure latex-placement="!t"}
![](Briden2023ConstraintInformed_figs/propagate.png){width=".7\\linewidth"}

::: caption
Only the control policy and dual variables are predicted using the LSTM, and the state variables are recovered by propagating the controls through the system dynamics. During the learning process, the Lagrangian-based merit function uses the decision variables from the propagated dynamics to evaluate the chosen loss function.
:::
::::

The advantages of using an [RNN]{acronym-label="RNN" acronym-form="singular+short"} to learn the time-varying policy include:

1.  Using a more compact neural network model for $f_\phi (\cdot)$ that has output dimension in ${\mathbf{R}}^{n_u}$ and rather than in ${\mathbf{R}}^{N(n_x+n_u)}$.

2.  Incorporating the temporal structure of the problem via the [RNN]{acronym-label="RNN" acronym-form="singular+short"} in predicting decision variables.

We note that our proposed approach is closely related to the area of solving model-based trajectory optimization for imitation learning, an area of research that has extensive heritage [@ReskeCariusEtAl2021; @TagliabueKimEtAl2022; @CauligiChakrabartyEtAl2022]. However, we eschew the imitation learning terminology since our proposed approach still relies on running numerical optimization online, thereby preserving any guarantees of the underlying solver. We also note connections to shooting methods [@Betts1998; @Kelly2017], wherein the number of decision variables in a trajectory optimization problem is reduced by only optimizing over the controls $\{ u_t \}_{t=0}^N$. As is well known, however, shooting methods often struggle to find solutions for problems with challenging state constraints, but TOAST addresses this challenge by jointly predicting the dual variables for improved constraint satisfaction predictions.

The next section discusses our proposed approach to generating predictions that better satisfy system constraints.

## Merit Functions for Warm Starts {#sec: merit functions for warm starts}

To motivate the need for merit function-based learning, we consider the following simple optimization problem:

$$\begin{align*}
\text{minimize:} \quad & \text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (x^*_i - \hat{x}_i)^2 \\
\text{subject to:} \quad & x \leq 2,
\end{align*}$$

where $x^*$ is the optimal value of the decision variable and $\hat{x}$ is the prediction, for $N$-dimensional $x$. Figure [3](#fig:MSE){reference-type="ref" reference="fig:MSE"} demonstrates an example of the MSE for two separate predictions when the optimal value is $x^* = 1$. While the prediction $x = 3$ has a lower MSE, the prediction $x = -3$ is constraint satisfying. For safety-critical robotic applications, where constraint satisfaction is required for mission success, the constraint-satisfying prediction is often valued over cost minimization. In this work, we develop task-relevant merit functions that balance this trade-off in constraint satisfaction and cost minimization.

:::: {#fig:MSE .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/MSE_motivation.png){width=".8\\linewidth"}

::: caption
Mean-squared-error (MSE) for predicting $x = 1$ with constraint $x \leq 2$.
:::
::::

Let $\hat{z}(\theta) =(\hat{x}, \hat{u})$ be the initial prediction for the continuous decision variables of [\[eq:nlp\]](#eq:nlp){reference-type="eqref" reference="eq:nlp"} by a neural network model $f_\phi (\theta)$ for problem parameters $\theta$. The standard training loss for updating the parameters $\phi$ of the model would be the [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss function $L_{\text{MSE}} = \min_\phi \frac{1}{|\mathcal{D}|} \sum_{i=1}^{|\mathcal{D}|} \| \hat{z}_i(\theta) - z_i^*\|_2^2$, where $\mathcal{D}$ is the training set of tuples $\{ (\theta_i, z_i^*) \}_{i=1}^{|\mathcal{D}|}$ constructed by solving [\[eq:nlp\]](#eq:nlp){reference-type="eqref" reference="eq:nlp"} to optimality.

When comparing [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss to the set of TOAST merit functions, detailed below, we will benchmark our results against both [MSE]{acronym-label="MSE" acronym-form="singular+short"} and Primal [MSE]{acronym-label="MSE" acronym-form="singular+short"}.  [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss computes the mean-squared-error of the state, control input, and dual variables, and Primal [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss computes the mean-squared-error of the state and control decision variables only.

This work uses merit functions as decision-focused loss functions to supervise a problem-solution map for constrained optimization problems. Instead of using the standard [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss, we seek to generate better solution predictions $\hat{z}$ that allow for faster online convergence by explicitly penalizing system constraint violations. To accomplish this, we propose the following set of merit functions:

1.  **Lagrangian Loss** $$\begin{equation}
    L_{\mathcal{L}} = \min_\phi \frac{1}{|\mathcal{D}|} \sum_{i=1}^{|\mathcal{D}|} (\mathcal{L}(z^*; \theta) - \mathcal{L}(\hat{z}; \theta))^2, \label{eq:loss_lag_diff}
    \end{equation}$$

    where $\mathcal{L}(\hat{z}; \theta) = f(\hat{z}; \theta) + \hat{\lambda}^T g(\hat{z}; \theta)$ is the Lagrangian associated with [\[eq:nlp\]](#eq:nlp){reference-type="eqref" reference="eq:nlp"} evaluated at $\hat{z}$, $f$ is the cost function for the optimization problem, $\hat{\lambda}$ are the dual multipliers, and $g$ is a vector of constraints. Equality constraints are not shown in this formulation since all equality constraints are separated into two inequality constraints in the numerical examples.

2.  **Lagrangian with Gradient Loss** $$\begin{equation}
    L_{\nabla \mathcal{L}} = \min_\phi \frac{\beta_{\mathcal{L}}}{|\mathcal{D}|} \sum_{i=1}^{|\mathcal{D}|} (\mathcal{L}(z^*; \theta) - \mathcal{L}(\hat{z}; \theta))^2 + \beta_{\mathcal{\nabla L}}(\nabla_z \mathcal{L}(\hat{z}_i; \theta))^2. \label{eq:loss_lag_diff_kkt}
    \end{equation}$$

    This loss function follows from adding the KKT conditions' stationarity condition for optimization problems [@BoydVandenberghe2004; @NocedalWright2006]. Instead of using the stationarity condition alone, it was instead added to Lagrangian loss since learning with $(\nabla_z \mathcal{L}(\hat{z}_i; \theta))^2$ only often led to maximization, instead of minimization of the loss during learning. The parameters $\beta_{\mathcal{L}}$ and $\beta_{\mathcal{\nabla L}}$ are adjustable multipliers for scaling each quantity. For the numerical experiments in this work, $\beta_{\mathcal{L}} = 0.1$ and $\beta_{\mathcal{\nabla L}} = 0.01$.

3.  **Lagrangian MSE Loss** $$\begin{equation}
    L_{\mathcal{L} \text{ MSE}} = \min_\phi \frac{\beta_{\mathcal{L}}}{|\mathcal{D}|} \sum_{i=1}^{|\mathcal{D}|} (\mathcal{L}(z^*; \theta) - \mathcal{L}(\hat{z}; \theta))^2 + \frac{1}{|\mathcal{D}|} \sum_{i=1}^{|\mathcal{D}|} \| \hat{z}_i(\theta) - z_i^*\|_2^2. \label{eq:loss_lag_diff_mse}
    \end{equation}$$

    Lagrangian MSE loss is motivated by the regularization of the MSE loss. Consider the estimate $\mathbb{E}[(\hat{z}_i(\theta) - z_i^*)^2]$ which can be decomposed into the sum of $\text{Var}[\hat{z}_i(\theta)] + (\mathbb{E}[\hat{z}_i(\theta)-z_i^*])^2$, the sum of the variance of the predictions and the squared bias of the predictions vs. targets. Given that with an unbiased estimator $\mathbb{E}[\hat{z}] = z$, a high variance could result in a large error. When the estimates are outputs from a NN, we can include a bias term in the loss function; in our case, we have the Lagrangian $\frac{1}{|\mathcal{D}|} \sum_{i=1}^{|\mathcal{D}|} (\mathcal{L}(z^*; \theta) - \mathcal{L}(\hat{z}; \theta))^2$, which biases MSE loss towards constraint satisfaction. Similar to the use of ridge regression in the loss function to reduce overfitting.

# Numerical Experiments {#sec:numerical_experiments}

In this section, we validate TOAST in numerical experiments and focus on the surface rover trajectory optimization problem. The neural network architectures were implemented using the `PyTorch` machine learning library [@PaszkeGrossEtAl2017] with the ADAM optimizer [@KingmaBa2015] for training. The optimization problems are modeled using CasADi [@AnderssonGillisEtAl2019] and solved using the IPOPT sequential quadratic programming library [@WachterBiegler2006].

To benchmark our proposed approach, we compare our decision-focused merit function against vanilla [MSE]{acronym-label="MSE" acronym-form="singular+short"} and Primal [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss functions for training LSTM NN architectures, as well as the vanilla and collision-penalizing LSTM and feedforward architectures in [@SabolYunEtAl2022]. Table [1](#tab:algorithm_settings){reference-type="ref" reference="tab:algorithm_settings"} shows the settings used for the lunar rover benchmark problem, and Table [2](#tab:algorithm_settings_pdg){reference-type="ref" reference="tab:algorithm_settings_pdg"} shows the settings used for the powered descent guidance problem.

::: {#tab:algorithm_settings}
  ------------------------------------------------------ --------------
  **Parameter**                                          **Value**
  Discretization size ($N$)                              61
  Number of obstacles ($n_{\text{obs}}$)                 5
  Final Time ($T_f$)                                     30 s
  Wheelbase of the vehicle ($L$)                         2.7 m
  Radius ($r_{\text{dist}}$)                             0.075 m
  Min steering wheel angle ($\delta_{\min}$)             -90 deg
  Max steering wheel angle ($\delta_{\max}$)             90 deg
  Min velocity ($v_{\min}$)                              0 m/s
  Max velocity ($v_{\max}$)                              0.2778 m/s
  Min acceleration ($\alpha_{\min}$)                     -0.3 m/s$^2$
  Max acceleration ($\alpha_{\max}$)                     0.3 m/s$^2$
  Jerk weight ($\omega_{\text{jerk}}$)                   0.5
  Acceleration weight ($\omega_{\text{acceleration}}$)   1
  ------------------------------------------------------ --------------

  : Lunar Rover Settings
:::

::: {#tab:algorithm_settings_pdg}
  ---------------------------------- -----------------
  **Parameter**                      **Value**
  Discretization size ($N$)          21
  Final Time ($T_f$)                 30 s
  Gravitational Acceleration ($g$)   3.72076 m/s$^2$
  Specific Impulse (Isp)             225 s
  Dry Mass ($m_\text{dry}$)          2200 kg
  Minimum Thrust ($\rho_{\min}$)     18 kN
  Maximum Thrust ($\rho_{\max}$)     48 kN
  Max velocity ($v_{\max}$)          500 m/s
  ---------------------------------- -----------------

  : Powered Descent Guidance Settings
:::

To implement the decision-focused loss functions [\[eq:loss_lag_diff\]](#eq:loss_lag_diff){reference-type="eqref" reference="eq:loss_lag_diff"}- [\[eq:loss_lag_diff_mse\]](#eq:loss_lag_diff_mse){reference-type="eqref" reference="eq:loss_lag_diff_mse"}, the Lagrangian and Lagrangian gradient functions were automatically defined using CasADi's symbolic framework and integrated into `PyTorch` via AutoGrad classes. When training with dual variables, since `PyTorch` often returns very large dual variable values (on the order of $1e^6$), clipping is used to prevent instabilities or exploding gradients [@HaeserHinderEtAl2021]. Clipping was chosen instead of an alternative data standardization process since it maintains the physical information of whether a constraint is active or inactive. IPOPT was chosen as the solver since both primal and dual guesses can be provided to the solver, and it can be applied to nonconvex optimization problems. In practice, we found that providing warm start initializations for the dual variables alone did not affect the solve time for IPOPT. The TOAST architecture has three layers and 128 neurons.

## Surface Rover Problem

 []{#subsec:surface_rover_mpc label="subsec:surface_rover_mpc"}

We model the dynamics of a lunar rover [OCP]{acronym-label="OCP" acronym-form="singular+short"} using the bicycle kinematics model given in Equation [\[eq:state_defn\]](#eq:state_defn){reference-type="ref" reference="eq:state_defn"}  [@LiuPadenEtAl2018]: $$\begin{equation}
\begin{split}
\dot{z} = \begin{pmatrix}
v \cos\theta\\
v \sin\theta\\
\frac{v}{L} \tan \delta\\
-\lambda_1 \delta + \lambda_1 \delta_\mathrm{in}\\
\alpha \\
-\lambda_2 \alpha + \lambda_2 \alpha_\mathrm{in}\\
\end{pmatrix},
\end{split}
\quad\quad
\begin{split}
z = (x,y,\xi,\delta,v,\alpha)^T,\\
u = (\delta_\mathrm{in}, \alpha_\mathrm{in})^T.
\end{split}
\label{eq:state_defn}
\end{equation}$$ In this model, the state $z \in {\mathbf{R}}^6$ consists of the configuration of the center point of the rear axle of the vehicle in a fixed world frame $(x,y,\xi)$, the steering-wheel angle $\delta$, and the longitudinal speed and acceleration $v$ and $\alpha$, respectively [@LiuPadenEtAl2018]. The control $u\in{\mathbf{R}}^2$ consists of the steering angle control input $\delta_\mathrm{in}$ and acceleration control input $\alpha_\mathrm{in}$. The discrete-time update equation is approximated using a backward Euler rule.

The MPC formulation of the lunar rover OCP is then given by: $$\begin{equation}
 \label{eq:lunar rover ocp}
\begin{array}{ll}
\underset{z_{0:N},u_{0:N}}{\textrm{minimize}} \!\!\!& \sum_{t=0}^{N-1} \omega_{\text{jerk}} (\delta_{t+1} - \delta_t)^2 + \sum_{t=0}^N \omega_{\text{acc}} \alpha_t^2 \\
\text{subject to}\!\!\!& z_0 = z_\textrm{init}(\theta),\\
& z_{t+1} \leq \psi_t(z_t,u_t;\theta), \quad t = 0, \dots, N-1,\\
& z_{t+1} \geq \psi_t(z_t,u_t;\theta), \quad t = 0, \dots, N-1,\\
& z_{\min} \leq z_i \leq z_{\max}, \quad\;\;\;\, t = 0, \dots, N, \\
& u_{\min} \leq u_i \leq u_{\max}, \quad\;\;\;\, t = 0, \dots, N-1, \\
& r_{\text{dist}}^2 - [(x_t - r_{\text{obs}_i, x})^2 + (y_t - r_{\text{obs}_i, y})^2] \leq 0, \quad\;\;\;\, t = 0, \dots, N-1, i = 1,\dots,n_{\text{obs}}, \\
\end{array}
\end{equation}$$ where the cost function minimizes jerk and acceleration over the trajectory and $\omega_{\text{jerk}}$ and $\omega_{\text{acc}}$ are scaling factors. The dynamics are decomposed into two inequality constraints to allow for only non-negative duality multipliers. In addition to upper and lower bound constraints for the state and control inputs, collision avoidance constraints are formulated for every obstacle. The parameters used in this model were drawn from the Endurance-A Lunar rover mission concept studied in the most recent Planetary Decadal survey [@NASEM2022; @KeaneTikooEtAl2022].

## Loss Function Sensitivity {#sec:sensitivity}

To understand the loss landscape for the merit functions in Eqns. [\[eq:loss_lag_diff\]](#eq:loss_lag_diff){reference-type="eqref" reference="eq:loss_lag_diff"}- [\[eq:loss_lag_diff_mse\]](#eq:loss_lag_diff_mse){reference-type="eqref" reference="eq:loss_lag_diff_mse"}, a preliminary sensitivity analysis was conducted. A simple solution to the optimal control problem, [\[eq:lunar rover ocp\]](#eq:lunar rover ocp){reference-type="eqref" reference="eq:lunar rover ocp"}, was computed with $N = 4$ discretization nodes and two randomly distributed obstacles. Using the resulting $(x^*, u^*, \lambda^*)$ and clipping $\lambda^* \leq 1$, one hundred perturbations were created equidistantly between the values of $1e^{-6}$ and $1e^{-2}$ to slightly alter the decision variable values at the optimal solution. The sensitivity is then defined as $\frac{L}{\delta}$, where $L$ is the evaluated loss function and $\delta$ is the perturbation scale. The overall sensitivity computations include a combined norm term in the denominator, the sum of the norms of the differences between perturbed solutions. Figure [4](#fig:sensitivity){reference-type="ref" reference="fig:sensitivity"} shows the sensitivity of each loss function to perturbations in the state $x$, control input $u$, and dual variables $\lambda$.

:::: {#fig:sensitivity .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/sensitivity_final.png){width="\\linewidth"}

::: caption
Sensitivity analysis of loss functions: Lagrangian loss displays stable sensitivity; MSE variations decrease across perturbation scales. Integrated Lagrangian MSE loss combines sensitivities to $u$, $x$, and $\lambda$.
:::
::::

As is expected, we see that the MSE and Primal MSE loss, where [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss computes the mean-squared-error of the state, control input, and dual variables, and Primal [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss computes the mean-squared-error of the state and control decision variables only, demonstrated the same sensitivity distribution over $x$ and $u$. Including dual variables $\lambda$ in the MSE prediction likely reduced overall sensitivity because the included dual variables attain values less than or equal to one. For the Lagrangian loss, the largest degree of sensitivity was to the dual variables, and, in contrast to MSE and Primal MSE, the Lagrangian loss was not sensitive to changes in the control.

Overall, the Lagrangian loss on this perturbation scale forms a hyperplane with a slight amount of noise as the perturbation scale increases. When the Lagrangian gradient is added in, and the multipliers $\beta_{\mathcal{L}}$ and $\beta_{\mathcal{\nabla L}}$ are included in the loss, sensitivity is extremely low for all decision variables. Finally, Lagrangian MSE appears to blend the sensitivity to $u$ of the MSE and Primal MSE losses and the sensitivity to $x$ and $\lambda$ from the Lagrangian. The Lagrangian MSE loss function is the only loss function that maintains the approximately monotonically decreasing shape of the MSE loss for overall sensitivity. High sensitivity near the optimal solution for MSE, Primal MSE, and Lagrangian MSE losses could accelerate convergence to minima during training; the areas close to the optimal solution are more responsive to adjustments in the training process, potentially leading to more efficient learning. The low overall sensitivity of the Lagrangian and Lagrangian with Gradient merit functions to small perturbations may be advantageous for training or testing on adversarial examples.

The authors in [@SzegedyZarembaEtAl2014] observe that small adversarial perturbations on input images can change the NN's prediction. Therefore, since Lagrangian-based merit functions are less susceptible to minor input perturbations, they may be more robust to adversarial examples. Future work will further explore decision-focused learning in adversarial settings.

## Application: Lunar Rover MPC {#sec:application}

:::: {#fig:rover_trajectory .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/rover_trajectory_no_axes_ig.png){width=".5\\linewidth"}

::: caption
Optimal trajectory generated by TOAST using an LSTM NN predicted constraint-informed warm start (in grey) to solve the MPC problem for an optimal trajectory (in blue). Green arrows indicate the rover's heading, and obstacles are red circles.
:::
::::

:::: {#fig:lstm_cost_vs_constraints .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/costvsconstraints_LSTM_2.png){width=".7\\linewidth"}

::: caption
Cost difference vs. constraint satisfaction for TOAST predictions on test data.
:::
::::

:::: {#fig:timing .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/time_LSTM_final.png){width=".8\\linewidth"}

::: caption
Computation time for test dataset warm-starts using TOAST. The constraint-informed LSTM NN provides more than a 5-second speedup from the SQP.
:::
::::

To apply TOAST for the Lunar Rover MPC optimal control problem, an RNN-based LSTM neural network architecture was formulated. We sampled a training dataset of 7200 samples with problem parameters (initial and goal states and five obstacles) sampled from Eqn. [\[eq:lunar rover ocp\]](#eq:lunar rover ocp){reference-type="eqref" reference="eq:lunar rover ocp"} with $N=61$. Obstacles were generated along the heading and cross-track, defined by the randomly generated start and goal states. The train-test split for this problem is $80:20$. Additional results, which include a Feedforward NN architecture, are included in the Appendix.

Figure [5](#fig:rover_trajectory){reference-type="ref" reference="fig:rover_trajectory"} illustrates the lunar rover's trajectory for motion planning around obstacles. TOAST generates an optimal and constraint-satisfying trajectory by first computing an initial guess, shown by the dotted grey line, and then solving the trajectory optimization problem with IPOPT, resulting in the solid blue trajectory.

To analyze the tradeoff between cost minimization and constraint satisfaction, the image of the cost difference vs. constraint satisfaction is plotted in Figures [6](#fig:lstm_cost_vs_constraints){reference-type="ref" reference="fig:lstm_cost_vs_constraints"}-[13](#fig:ff_cost_vs_constraints){reference-type="ref" reference="fig:ff_cost_vs_constraints"}. From the KKT conditions, the optimal solution meets the complementary slackness condition, shown as the vertical green line. The red region on each plot indicates the location of infeasible dual variable predictions ($\hat{\lambda} < 0$). Lastly, note that predictions of the dual variables computed from the Primal MSE loss are random since they are not included in the loss function computation.

We see immediately that, while close in cost prediction, primal MSE predictions are largely infeasible for the LSTM NN. Lagrangian loss-trained predictions demonstrate the closest predictions to meeting the complementary slackness condition, with Lagrangian with Grad and Lagrangian MSE close in constraint satisfaction.

Timing results from applying TOAST to the online inference problem are plotted in Figure [7](#fig:timing){reference-type="ref" reference="fig:timing"}. Overall, the Lagrangian-regularized MSE merit function and the Primal MSE are close in dominating performance. Primal MSE is just 190 ms less than the mean computation time for Lagrangian MSE for the LSTM architecture (2.78 vs. 2.97 seconds).

Compared to the full SQP, all merit functions in the TOAST software architecture provide warm-starts that significantly reduce computation time. The decision-focused merit functions offer up to a 63% reduction in mean runtime for the LSTM NN.

Benchmarking against the MSE-based and collision-penalizing spacecraft swarm trajectory planning problem for 10 spacecraft, both warm start techniques reduce the 20-second mean solve time to less than 5 seconds [@SabolYunEtAl2022]. Our implementation using 50 more timesteps and less than 8000 training samples has 2.97 and 4-second runtimes. Which we conclude are comparable with the mean warm-started runtimes provided by [@SabolYunEtAl2022].

Table [3](#tab:performance_metrics){reference-type="ref" reference="tab:performance_metrics"} shows the performance metrics for each loss function for TOAST, where CV is the percent of violated constraints, AD is the average degree of constraint violation, and AD is the mean $\pm$, the standard deviation. The Lagrangian with Grad NN achieves the least percent of violated constraints, $11.21\%$, and the smallest degree of violation, $8.59$, for the LSTM NN. Benchmarking against the NN architectures in [@SabolYunEtAl2022], the average number of collisions increases by 0.043-0.114 for the FF NNs and increases by 0.092 for one of the LSTM NNs when collision-penalization is applied. In contrast, TOAST reliably decreases constraint violation by $0.65\%-5.33\%$ for the LSTM NN compared to vanilla [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss. Therefore, we have shown that decision-focused merit functions effectively learn trajectory predictions and feasibility.

::: {#tab:performance_metrics}
  **Metric**           **Category**            **TOAST**
  -------------------- ----------------------- ---------------------------------
  MSE                  CV (%) / AD             16.54 / 22.95 $\pm$ 2.12
                       MSE (State / Control)   3.53 / 0.032
  Primal MSE           CV (%) / AD             13.85 / 14.07 $\pm$ 5.98
                       MSE (State / Control)   0.068 / 0.033
  Lagrangian           CV (%) / AD             15.89 / 11.00 $\pm$ 5.95
                       MSE (State / Control)   1.06 / 0.033
  Lagrangian w/ Grad   CV (%) / AD             **11.21** / **8.59** $\pm$ 2.54
                       MSE (State / Control)   0.809 / **0.032**
  Lagrangian MSE       CV (%) / AD             13.90 / 13.61 $\pm$ 5.95
                       MSE (State / Control)   **0.068** / 0.032

  : Performance Metrics
:::

## Powered Descent Guidance Problem

 []{#subsec:powered_descent label="subsec:powered_descent"}

The powered descent guidance OCP dynamics are modeled in 3 degrees of freedom (DoF), with the spacecraft modeled as a point mass. Equation [\[eq:zdot_pdg\]](#eq:zdot_pdg){reference-type="ref" reference="eq:zdot_pdg"} shows the 3 DoF non-convex dynamics:

$$\begin{equation}
 \label{eq:zdot_pdg}
\begin{split}
\dot{z} = 
= \begin{pmatrix}
v \\
\frac{T}{m} - g \\
-\alpha \left\| T \right\|_2.
\end{pmatrix}
\end{split}
\quad\quad
\begin{split}
z = (x, y, z, v_x, v_y, v_z, m)^T,\\
u = (T_x, T_y, T_z)^T.
\end{split}
\end{equation}$$

The state $z \in  {\mathbf{R}}^7$ includes the spacecraft's position, velocity, and mass in a fixed world frame. The control $u \in {\mathbf{R}}^3$ includes the thrust control input $T$ in the $x$, $y$, and $z$ directions. The discrete-time update equation is approximated using a backward Euler rule.

The full powered descent guidance OCP minimizes fuel consumption subject to the state dynamics in Equation [\[eq:zdot_pdg\]](#eq:zdot_pdg){reference-type="ref" reference="eq:zdot_pdg"}, control, and state constraints:

$$\begin{equation}
 \label{eq:pdg_OCP}
\begin{array}{ll}
\underset{z_{0:N},u_{0:N}}{\textrm{minimize}} \!\!\!& \sum_{t=0}^{N-1} u_t^T u_t \Delta t / \omega_u \\
\text{subject to}\!\!\!& z_0 = z_\textrm{init}, \\
& z_{t+1} \leq z_t + \Delta t \cdot f(z_t, u_t), \quad t = 0, \dots, N-1, \\
& z_{t+1} \geq z_t + \Delta t \cdot f(z_t, u_t), \quad t = 0, \dots, N-1, \\
& z_{\min} \leq z_t \leq z_{\max}, \quad\;\;\;\, t = 0, \dots, N, \\
& u_{\min} \leq u_t \leq u_{\max}, \quad\;\;\;\, t = 0, \dots, N-1, \\
& \| v \|_2 \leq v_{\text{max}}, \quad\;\;\;\, t = 0, \dots, N, \\
& \rho_{\min} \leq \| T \|_2 \leq \rho_{\max}, \quad\;\;\;\, t = 0, \dots, N-1, \\
\end{array}
\end{equation}$$ where $\omega_u = 10^6$ is a scaling factor and the dynamics equality constraint is decomposed into two inequality constraints. Other constraints include state and control upper and lower bounds, as well as maximum velocity and minimum and maximum thrust constraints.

## Application: Mars 3 Degree-of-Freedom Powered Descent Guidance

A transformer-based TOAST neural network architecture to warm start Equation [\[eq:pdg_OCP\]](#eq:pdg_OCP){reference-type="ref" reference="eq:pdg_OCP"}. The training dataset was constructed using 7168 normally distributed samples for the initial conditions $z_0$, as shown in Table [4](#tab:sample_pdg){reference-type="ref" reference="tab:sample_pdg"}, with $N = 21$ discretization nodes with the origin as the landing location. The train-test split for this problem is 80:20, resulting in 1792 test samples.

::: {#tab:sample_pdg}
  **Sampled Variable**   **Range**
  ---------------------- ----------------------
  $x_0$                  \[-2500 m, 2500 m\]
  $y_0$                  \[-2500 m, 2500 m\]
  $z_0$                  \[500 m, 2000 m\]
  $v_{x0}$               \[-80 m/s, 80 m/s\]
  $v_{y0}$               \[-80 m/s, 80 m/s\]
  $v_{z0}$               \[-100 m/s, 0 m/s\]
  $m_{\text{wet}}$       \[2200 kg, 6600 kg\]

  : Sample Ranges for TOAST Training
:::

[]{#tab:sample_pdg label="tab:sample_pdg"}

The NN features, consisting of the initial state, and the decision variable targets, the full state and control solutions, are scaled using a min max scaling class to ensure training remains stable. Scaling is achieved by fitting a scale and min value defined by $\text{scale} = \frac{1}{X_{\max} - X_{\min} + 1e-8}$ and $\min = - X_{\min} \times \text{scale}$. Then the scaled value is defined as $X_\text{scaled} = \text{scale} \times X + \min$, which is then clamped to ensure the scaled values remain between zero and one.

Since convergence is not achieved when using IPOPT to solve the OCP in Equation [\[eq:pdg_OCP\]](#eq:pdg_OCP){reference-type="ref" reference="eq:pdg_OCP"} without an initial guess, a straight line initial guess, with thrust predicted to be constant and equal to the average of the minimum and maximum thrust values, was used to obtain both the training and test dataset but also as the baseline comparison for the SQP. Figure [8](#fig:pdg_straightline){reference-type="ref" reference="fig:pdg_straightline"} shows three straight line initial guesses and the optimal trajectories obtained after warm-starting and solving. Figure [9](#fig:pdg_warmstarted){reference-type="ref" reference="fig:pdg_warmstarted"} shows the Primal MSE and TOAST Lagrangian MSE predictions for the same three test cases and the converged trajectories after warm-starting.

:::: {#fig:pdg_comparison .figure latex-placement="ht"}
![Straight line initial guess and the converged solution for the powered descent guidance optimal control problem.](Briden2023ConstraintInformed_figs/pdg_straightline.png){#fig:pdg_straightline width="\\linewidth"}

![Primal and TOAST Lagrangian MSE trained transformer neural network outputs and the converged warm-started trajectories.](Briden2023ConstraintInformed_figs/pdg_warmstarted.png){#fig:pdg_warmstarted width="\\linewidth"}

::: caption
Comparison of straight line initial guesses and TOAST neural network initial guesses resulting in the converged solutions for the powered descent guidance problem.
:::
::::

Overall, the constraint-informed TOAST Lagrangian MSE trajectories are closer to the locally optimal solutions achieved after solving the OCP. Further, we note that these trajectories are generated by propagating neural network predicted thrusts through the system dynamics in Equation [\[eq:zdot_pdg\]](#eq:zdot_pdg){reference-type="ref" reference="eq:zdot_pdg"}. Therefore, the neural network predicted control inputs are often much closer to the locally optimal control input when compared to constant thrust initial guess used with the straight line initialization.

The tradeoff between cost minimization and constraint satisfaction for the non-standardized powered descent guidance problem is shown in Figure [11](#fig:costvconstraints_pdg){reference-type="ref" reference="fig:costvconstraints_pdg"}.

:::: {#fig:costvconstraints_pdg .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/costvconstraints_pdg_final.png){width=".6\\linewidth"}

::: caption
Cost difference vs. constraint satisfaction for **transformer predictions** on test data.
:::
::::

The y-axis shows the difference in cost between the optimal cost and the cost computed with the neural network predicted state, control, and dual variables. From the plot, the predicted cost is mostly either equal to or less than the optimal cost. Dual variables for the computation of constraint satisfaction are clipped between the values of -1 and 1, as for the previous problem, so any large values on the x-axis for constraint satisfaction are due to inequality constraint evaluations. Overall, the powered descent guidance problem has a much larger range of values for training and test trajectories, resulting in much larger evaluations of the cost and degree of constraint satisfaction. When comparing the baseline case of Primal MSE to the TOAST architectures Lagrangian MSE, it is evident that there is increased constraint satisfaction as well as closer to optimal cost for Lagrangian MSE.

Table [5](#tab:performance_metricsTransformer){reference-type="ref" reference="tab:performance_metricsTransformer"} shows the performance metrics for each loss function, where CV is the percent of violated constraints, AD is the average degree of constraint violation, and AD is shown using the mean $\pm$ the standard deviation. Comparing the unscaled constraint violation percentage and the average degree of constraint violation, TOAST Lagrangian MSE achieves a significant decrease in both, decreasing the percentage of constraint violated by 8% and reducing the degree of violation by almost 70%. Compared to Primal MSE, Lagrangian MSE also has a lower standard deviation for constraint violation. Lastly, Lagrangian MSE dominates for both standardized state and control accuracy; the MSE for the state variable is reduced by almost 25%, and control MSE reduces by 50% when comparing Lagrangian MSE to Primal MSE.

::: {#tab:performance_metricsTransformer}
  **Architecture**   **Metric**              **Transformer**
  ------------------ ----------------------- -----------------------------------------------------
  Primal MSE         CV (%) / AD             34.94 / 1.998 e$^{11}$ $\pm$ 1.438 e$^{11}$
                     MSE (State / Control)   0.1717 / 0.5505
  Lagrangian MSE     CV (%) / AD             **26.70** / **6.020 e$^{10}$** $\pm$ 6.506 e$^{10}$
                     MSE (State / Control)   **0.1295** / **0.2748**

  : Performance Metrics for the Transformer Neural Network
:::

::: flushleft
:::

Timing results for the TOAST Lagrangian MSE merit function, when compared to Primal MSE, are shown in Figure [12](#fig:time_all_pdg){reference-type="ref" reference="fig:time_all_pdg"}.

:::: {#fig:time_all_pdg .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/time_all_pdg.png){width="\\linewidth"}

::: caption
Computation time for 100 test data sampled warm-starts using TOAST Transformer. The constraint-informed Lagrangian MSE merit function provides a 20 ms mean speedup when compared to primal MSE.
:::
::::

From the timing results, it is evident that compared to the straight-line warm-started SQP, neural network-provided warm starts consistently result in faster runtimes; in the powered descent guidance problem, the SQP runtime was reduced from almost 500 ms to under 360 ms. Constraint-informed warm starting using the TOAST architecture also dominates for computational efficiency, as the Transformer Lagrangian MSE test case reduces runtime by over 30% when compared to the straight-line warm-started SQP and by more than 5% when compared to Primal MSE.

# Conclusion {#sec:conclusion}

By employing a two-step process of offline supervision and online inference using decision-focused merit functions, TOAST computes a learned mapping biased towards constraint satisfaction. Three merit functions were designed for training: Lagrangian Loss, Lagrangian with Gradient Loss, and Lagrangian MSE Loss. After applying TOAST to learn the time-varying policy of Lunar rover MPC and Mars powered descent guidance, benchmarking results demonstrate the expected distributional shifts towards constraint satisfaction on test data and a 100-millisecond to 5-second speedup. Future work will extend decision-focused learning to the problem of 6-degree-of-freedom powered descent guidance.

# Appendix {#appendix .unnumbered}

:::: {#fig:ff_cost_vs_constraints .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/costvsconstraints_FF_2.png){width=".7\\linewidth"}

::: caption
Cost difference vs. constraint satisfaction for **feedforward predictions** on test data.
:::
::::

:::: {#fig:ff_timing .figure latex-placement="ht"}
![](Briden2023ConstraintInformed_figs/time_FF_final.png){width=".8\\linewidth"}

::: caption
Computation time for test dataset warm-starts using TOAST with a feedforward NN. The feedforward NN provides more than a 5-second speedup from the SQP.
:::
::::

We sampled a training dataset of 1200 samples for the feedforward NN, with problem parameters (initial and goal states and five obstacles) sampled from Eqn. [\[eq:lunar rover ocp\]](#eq:lunar rover ocp){reference-type="eqref" reference="eq:lunar rover ocp"} with $N=61$. Obstacles were generated along the heading and cross-track, defined by the randomly generated start and goal states. The train-test split for this problem is $80:20$.

::: {#tab:performance_metricsFF}
  **Architecture**     **Metric**              **Feedforward**
  -------------------- ----------------------- ---------------------------------
  MSE                  CV (%) / AD             9.42 / 17.95 $\pm$ 5.47
                       MSE (State / Control)   0.157 / 0.00093
  Primal MSE           CV (%) / AD             12.56 / 15.73 $\pm$ 5.04
                       MSE (State / Control)   **0.122** / 0.005
  Lagrangian           CV (%) / AD             3.75 / 11.79 $\pm$ 3.42
                       MSE (State / Control)   0.981 / 0.0035
  Lagrangian w/ Grad   CV (%) / AD             2.21 / 11.75 $\pm$ 3.48
                       MSE (State / Control)   0.973 / 0.0008
  Lagrangian MSE       CV (%) / AD             **1.21** / **11.66** $\pm$ 3.37
                       MSE (State / Control)   1.01 / **0.00079**

  : Performance Metrics for the Feedforward Neural Network
:::

Full metrics for the feedforward architecture are shown in Table [6](#tab:performance_metricsFF){reference-type="ref" reference="tab:performance_metricsFF"}. While the feedforward NN denotes the Primal MSE loss as the merit function with the least state error, Lagrangian MSE achieves the minimum state error.

Figure [13](#fig:ff_cost_vs_constraints){reference-type="ref" reference="fig:ff_cost_vs_constraints"} shows the cost vs. constraint satisfaction for the feedforward NN architecture. For the feedforward NN, Lagrangian MSE dominates in constraint satisfaction, achieving $1.21\%$ violated constraints and an $11.66$ degree of constraint violation at the cost of a larger state error. Benchmarking against the NN architectures in [@SabolYunEtAl2022], the average number of collisions increases by 0.043-0.114 for the FF NNs and increases by 0.092 for one of the LSTM NNs when collision-penalization is applied. In contrast, TOAST reliably decreases constraint violation by $5.67\%-8.21\%$ for the Feedforward NN, compared to vanilla [MSE]{acronym-label="MSE" acronym-form="singular+short"} loss.

Figure [14](#fig:ff_timing){reference-type="ref" reference="fig:ff_timing"} shows the timing results for the feedforward NN. For the feedforward architecture, Lagrangian MSE offers a more than 2-second improvement in mean computation time over MSE (4 vs. 6.22 seconds). Further, the decision-focused merit functions offer up to a 63% reduction in mean runtime for the LSTM NN and a 54% reduction in mean runtime for the feedforward NN.

# Acknowledgments {#acknowledgments .unnumbered}

The authors would like to thank Breanna Johnson and Dan Scharf for their discussions during the development of this work. This research was carried out at the Jet Propulsion Laboratory, California Institute of Technology, under a contract with the National Aeronautics and Space Administration and funded through the internal Research and Technology Development program. This work was supported in part by a NASA Space Technology Graduate Research Opportunity 80NSSC21K1301.

[^1]: Doctoral Student, Department of Aeronautics and Astronautics, Massachusetts Institute of Technology; jbriden@mit.edu. AIAA Student Member (Corresponding Author).

[^2]: Robotics Technologist, Jet Propulsion Laboratory, California Institute of Technology.

[^3]: Technologist, Jet Propulsion Laboratory, California Institute of Technology.

[^4]: Rockwell International Career Development Professor and Associate Professor, Department of Aeronautics and Astronautics, Massachusetts Institute of Technology, Senior Member AIAA.

[^5]: Robotics Technologist, Jet Propulsion Laboratory, California Institute of Technology.
