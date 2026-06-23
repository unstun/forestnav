---
citation_key: Alboni2026CACTOBIC
arxiv_id: 2602.19699
arxiv_url: https://arxiv.org/abs/2602.19699
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:49:51Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

Trajectory Optimization (TO) is a widely used and flexible technique for solving robotic control problems. In TO, the high-level task is formulated as a constrained Optimal Control Problem (OCP), where the optimization variables are the system's state and control trajectories. Constraints enforce compliance with system dynamics and kinematics, actuator limits, and task-specific requirements. However, OCPs are typically highly non-convex, making gradient-based solvers prone to converge to poor local minima. While global methods based on the Hamilton--Jacobi--Bellman equation or Dynamic Programming [@bellman1954theory] exist, their applicability is limited by the curse of dimensionality.

Deep Reinforcement Learning (RL) emerged as an alternative framework, particularly for continuous state and action spaces. Algorithms such as DDPG [@DDPG], SAC [@SAC], and PPO [@PPO] have demonstrated strong performance in robotic control tasks. Due to their exploratory nature, RL methods are generally less sensitive to local minima but they typically suffer from high sample complexity and long training times.

To overcome the complementary limitations of TO and RL, hybrid approaches combining the two have recently gained significant research attention. A popular choice is to rely on *TO imitation*: policies are trained to mimic TO or model predictive control (MPC) solutions---through value-based or action-based imitation---to reduce online computational costs and to leverage sensor feedback [@carius2020mpc; @ghezzi2023imitation]. However, these methods neither improve TO solution's quality, nor guarantee constraint satisfaction. Accounting for policy approximation errors in the TO problem can lead to better results [@levine2013guided; @lidec2022enforcing], but it inherits the same limitations.

Other methods use learned policies or value functions to warm-start TO or to define terminal costs, thereby accelerating optimization and guiding the solver toward improved solutions [@reiter2024ac4mpc; @ceder2024bird]. While effective for TO, these approaches provide no benefits for RL training.

An increasingly prominent class of approaches embeds TO directly within the RL framework to improve training efficiency. These methods can be classified based on where TO is included: *post-policy*, *pre-policy*, or as a *residual* policy. *Post-policy* methods evaluate TO after the policy. Some methods learn cost or constraint parameters [@romero2024actor; @zarrouki2024safe], leveraging MPC's safety and stability guarantees, but require solving TO online and face convergence challenges. Others use TO as actor and learn its terminal cost [@lowrey2018plan; @jordana2025infinite], accelerating training and improving constraint handling, yet potentially yielding suboptimal solutions or neglecting sensor feedback. Another variant initializes TO with an RL policy [@CACTO; @morgan2021model], improving convergence speed and solution quality, yet still does not exploit sensor feedback. In *pre-policy* methods, TO generates reference trajectories or auxiliary information that are inputted to the RL policy, effectively speeding up training [@jenelten2024dtc]. *Residual* methods instead learn a residual policy to improve TO-generated control inputs with learned corrections [@silver2018residual]. While both *pre-policy* and *residual* methods accelerate training, they require online TO and depend on its ability to find high-quality solutions; moreover, learned policies may violate constraints even when TO does not.\
In this work, we extend CACTO [@CACTO; @alboni2024cacto], a *post-policy* algorithm that exploits the interplay between TO and RL to accelerate training. The actor policy generates the initial guess for TO, leveraging the exploratory nature of RL to avoid convergence to poor local minima, while TO guides the learning process of the RL agent.

The primary limitation of CACTO is scalability. As the system complexity increases, TO becomes more expensive, and actor--critic training requires more iterations to converge. We investigate strategies to reduce the computational burden in both TO and RL phases. Our main contributions are:

- A method to identify state-space regions where an improvement of the actor policy is more likely.

- A new version of CACTO's algorithm, called CACTO-BIC, that exploits biased initial conditions (BIC) and GPU-based computation to achieve improved sample and time efficiency.

- A JAX-based [@jax2018github] open-source implementation of CACTO-BIC that exploits GPUs to solve TO problems and train neural networks.

- The first validation of CACTO on real hardware through experiments on a quadruped robot.

# BACKGROUND

This section summarizes the latest formulation of CACTO (originally called CACTO-SL [@alboni2024cacto]), an algorithm for solving finite-horizon discrete-time optimal control problems such as:

::: mini
\|l\|\[2\]\<b\> L(X,U) \_k=0\^T -1 l_k(x_k,u_k) + l_T(x_T) []{#OCP_optimizationProblem label="OCP_optimizationProblem"}
:::

where $X = \{x_0, \dots, x_T\}$ and $U = \{u_0, \dots, u_{T-1}\}$ are the state and control sequences, with $x_k \in \mathbb{R}^n$ and $u_k \in \mathbb{R}^m$. The cost $L(\cdot)$ combines running costs $l_k$ and a terminal cost $l_T$, while the constraints enforce system dynamics, control bounds, and initial conditions.

CACTO begins by solving $N$ TO problems from randomly sampled initial states, using standard warm-starting (e.g., setting all states to $x_{\mathrm{init}}$ and controls to zero). As the OCP horizon is finite, the actor policy and the critic value are time dependent, so also the initial time is randomized in each TO instance and the time is appended to the state vector, $\tilde{x}=[x,t]$. For each state of each optimized trajectory, CACTO computes the partial $K$-step cost-to-go $\bar{V}$, where $K$ is a user-defined parameter representing the Temporal Difference lookahead horizon. The value function's gradient $\bar{V}_x$ is also computed, using the backward pass of Differential Dynamic Programming (DDP) [@jacobson1970differential]. These values $(\bar{V}, \bar{V}_x)$, together with the associated state, control, and state after $K$ steps, are stored in a replay buffer.

Afterwards, the critic and actor neural networks are trained for $M$ iterations using mini-batches sampled from the replay buffer. The critic approximates the value function and its gradient by matching $\bar{V}$ and $\bar{V}_x$:

::: mini!
\|l\|\[2\]\<b\> (\|V - V( \| \^V))\^2 + k_s (\|V\_x - S_x V\_ (\|\^V))\^2 []{#critic_update label="critic_update"}
:::

where $V(\cdot)$, $V_{\tilde{x}}(\cdot)$ and $\theta^V$ are the critic network, its gradient (with respect to $\tilde{x}$) and its parameters, $k_s$ is the weight of the gradient term, and $S_x$ the selection matrix to exclude the partial derivative of $V$ with respect to time. The actor is updated by minimizing the Q-value:

::: mini!
\|l\|\[2\]\<b\> l(,(\|\^))+V\_\^V(f(,(\|\^))) []{#actor_update label="actor_update"}
:::

where $\mu(\cdot)$ and $\theta^\mu$ are the actor network and its parameters. The improved actor policy then generates rollouts that warm-start the subsequent TO problems, closing the loop between TO and RL.

In [@CACTO], CACTO was shown to outperform other RL algorithms such as DDPG [@DDPG] and PPO [@PPO] as warm-start provider in terms of training time.

# BIASED INITIAL STATES SAMPLING

Identifying regions of the state space with high potential for policy improvement is a challenging problem.

Exploration strategies in RL can be broadly categorized into undirected and directed approaches. Undirected exploration relies on stochastic action selection, such as $\epsilon$-greedy policies, to explore the state space without explicitly accounting for uncertainty or novelty. Directed exploration, in contrast, uses signals derived from the agent's learning process or auxiliary models to guide behavior toward less familiar or more uncertain regions. A common class of directed methods employs intrinsic rewards or exploration bonuses, including count-based or approximate count methods [@bellemare2016unifying], uncertainty metrics [@lowrey2018plan], and curiosity-driven approaches such as prediction-error bonuses and random network distillation [@pathak2017curiosity; @burda2018exploration]. Several works have also explored initial-state or restart-based exploration. These approaches often assign scores to states to prioritize which ones to explore further. Criteria for scoring include the system's sensitivity [@parsa2023where2start], the familiarity [@schenke2021improved], the uncertainty [@yin2023sample], or the TD error [@tavakoli2018exploring]. [@messikommer2024contrastive], proposes a structured replay buffer that groups states by task relevance and prioritizes sampling from unmastered sub-tasks. When available, prior or expert knowledge can also be leveraged to further guide exploration.\
We address the exploration problem by leveraging the insight that the value function $\bar{V}(x)$ associated with locally optimal solutions is generally *piecewise continuous*.

## Motivating Example: Discontinuous Value Function {#sec:1Dex}

Let us illustrate how the structure of the value function associated with a locally optimal policy can help us tackle the exploration problem. We focus on a toy problem with a 1D state, single integrator dynamics, and a cost with two local minima (see Fig. [1](#fig:f1){reference-type="ref" reference="fig:f1"}). Solving TO problems with a naive initial guess, highlights the presence of two basins of attraction, $\mathcal{R}_1$, and $\mathcal{R}_2$, each corresponding to a different local minimum (see Fig. [1](#fig:f1){reference-type="ref" reference="fig:f1"}).

:::: {#fig:f1 .figure latex-placement="tbp"}
![](Alboni2026CACTOBIC_figs/Ex1D_tris.png){width="0.9\\columnwidth"}

::: caption
Cost and Value obtained with TO using a naive initial guess. The critic smooths the Value's discontinuities.
:::
::::

Within each basin, the real Value $\bar{V}$ is continuous, but it is discontinuous at the shared boundary $\mathcal{R}_1 \cap \mathcal{R}_2 \triangleq \partial \mathcal{R}$. In the neighborhood of $\partial \mathcal{R}$, $\bar{V}$ is lower (i.e. better) in $\mathcal{R}_1$ than in $\mathcal{R}_2$.

After training the critic with the first batch of TO episodes, the network smooths out the discontinuity (see Fig. [1](#fig:f1){reference-type="ref" reference="fig:f1"}) in a region $\mathcal{N}$ around $\partial \mathcal{R}$, where the critic either underestimates or overestimates the true value $\bar{V}$: $$\begin{align}
V( \bar{x} | \theta_V) > \bar{V}(\bar{x}) \qquad \forall \bar{x} \in \mathcal{N} \cap \mathcal{R}_1 \\ 
V( \bar{x} | \theta_V) < \bar{V}(\bar{x}) \qquad \forall \bar{x} \in \mathcal{N} \cap \mathcal{R}_2
\end{align}$$ Therefore in $\mathcal{N}$ the critic's gradient will point towards $\mathcal{R}_2$. Due to this gradient, during the policy improvement phase the actor can improve in $\mathcal{N} \cap \mathcal{R}_2$, learning to steer the state toward $\mathcal{R}_1$ rather than $\mathcal{R}_2$. This example reveals that the regions near value function's discontinuities hold great potential for policy improvement.

## General case: Discontinuous Value Function

The phenomenon shown in Section [3.1](#sec:1Dex){reference-type="ref" reference="sec:1Dex"} frequently occurs in problems with multiple local minima. Each local minimum defines a basin of attraction where the value function is continuous, while discontinuities typically appear at the boundaries between basins. These discontinuities highlight regions with great potential for policy improvement. In contrast, sampling initial states far from such discontinuities likely leads the actor to simply imitate TO.

## Detecting Informative Regions via Critic Uncertainty

Approximating the value function close to the discontinuities is particularly challenging for the critic network, which cannot accurately represent abrupt changes due to its continuous activation functions. As a result, the critic tends to incur larger errors near these boundaries. We suggest leveraging the uncertainty estimation of the critic's output to identify the value's discontinuities. An additional neural network, referred to as *std-critic*, is introduced to predict the standard deviation of the critic. Following [@stdlearning], this network is trained at the end of each actor--critic update phase by minimizing the negative log-likelihood of a normal distribution:

::: mini!
\|l\|\[2\]\<b\> (V\^(\|\^)) + []{#std_critic_update label="std_critic_update"}
:::

where $V^{\text{std}}(\cdot)$ and $\theta^{\text{std}}$ are the *std-critic* network and its parameters. The first term of this loss pushes $V^{std}$ to be small everywhere, while the second term pushes $V^{\text{std}}$ to increase when the critic's error is large. We train this network after the critic to avoid issues during the early stages of learning. The initial states with the highest potential for policy improvement are then selected according to their predicted uncertainty $V^{\text{std}}(\tilde{x})$.

## Algorithm Overview

An overview of the CACTO-BIC (Biased Initial Conditions) algorithm is illustrated in Fig. [2](#fig:CACTO_scheme){reference-type="ref" reference="fig:CACTO_scheme"}.

:::: {#fig:CACTO_scheme .figure latex-placement="t"}
![](Alboni2026CACTOBIC_figs/BICS10nomargins.png){width="90%"}

::: caption
Overview of CACTO-BIC with biased initial-state sampling.
:::
::::

During the first iteration, as in the original CACTO framework [@CACTO], initial states for the TO problems are sampled uniformly at random. From the second iteration onward, a set of $10N$ candidate initial states is sampled and ranked based on $V^{\text{std}}$. The top $N$ samples are then selected for the next TO batch. Moreover, since trajectories starting from these initial states provide more information, we can reduce the number of problems solved from the second iteration (see Section [5.1](#ssec:bics_results){reference-type="ref" reference="ssec:bics_results"} for details).

# GPU-based computation

To reduce the computation time of the algorithm by leveraging GPUs, the entire framework was migrated to JAX, a Python library for accelerator-oriented array computation and program transformation [@jax2018github]. The migration is beneficial in two ways: first, migrating to GPU the neural network training---accounting for about 90% of CACTO's total computation time--- yields significant speedups; second, performing TO directly on GPU eliminates any CPU-GPU data-transfer overhead, in addition to reducing TO's computation time, which significantly grows with the complexity of the system.

Migrating to GPU-based computation required some adaptations to meet the constraints of parallel processing: GPUs require fixed-size arrays and uniform computation across batches to enable efficient vectorization, leading to the following two key challenges.

## Fixed number of iterations {#ssec:iteration_number}

Because GPUs execute batched computations in parallel, all TO problems in a batch must undergo the same number of optimization iterations. Consequently, the maximum number of iterations, $max\_iter$, becomes a crucial hyperparameter. Setting this value too low may lead to premature termination, and hence to collect too few or insufficiently informative samples. In contrast, setting it too large can cause longer runtimes, since hard-to-converge problems dominate the batch's overall computation time, slowing the entire pipeline. Moreover, the ideal number of iterations may vary as the policy improves, as better initial guesses generally lead to faster convergence.

To determine the maximum number of iterations, we suggest to solve a large set of problems using a naive warm-start and a high iteration limit ($max\_iter=1000$), generating a dataset of the iterations needed to converge. The maximum number of iterations can then be set to the 99th percentile of iteration counts for the first iteration of CACTO (where the naive warm-start is used) and to the 50th percentile for subsequent iterations (where CACTO's actor provides the warm-start).

## Regularization for matrix inversion

In iLQR [@jacobson1970differential], it is crucial to regularize the Hessian of the value function so that it is positive definite.

The standard regularization consists in increasing the local control-cost Hessian with a diagonal term: $\tilde{Q}_{uu} = Q + \mu I_{m},$ where $\mu$ plays the role of a Levenberg-Marquardt parameter. During the backward pass, if the line search fails, $\mu$ is increased and the backward pass is retried, otherwise, $\mu$ is decreased.

This approach is computationally efficient when solving problems sequentially on a CPU. However, it becomes impractical when solving multiple problems in parallel on a GPU, where such iterative tuning can significantly slow down the batched computation.

This issue is addressed through regularization based on the eigenvalue decomposition. The eigenvalues $S$ and corresponding eigenvectors $W$ of the state-cost Hessian and the control-cost Hessian are computed, the eigenvalues are clipped from below by a user-defined constant $\epsilon>0$, $S^\prime = \max(S,\epsilon)$, and the matrices are reconstructed: $$\begin{align}
  Q_+ &= W \, \text{diag}(S^\prime) \, W^T, \quad
  Q_{psd} &= \frac{1}{2} (Q_+ + Q_+^T)
\end{align}$$ This procedure handles poorly-conditioned Hessians, while avoiding additional iterative steps. As a result, it is better suited for large-batch processing on GPUs.

## Implementation Details

The system dynamics and cost functions, implemented using the CasADi library [@casadi] in CACTO-SL [@alboni2024cacto], were converted into JAX-compatible functions through the Jaxadi library [@jaxadi2024]. For TO, we replaced the previous solver with an iLQR implementation from the Trajax library [@trajax], which provides the additional benefit of computing the gradient of the value function (used for training the critic network) while solving the optimal control problem. The neural networks were implemented using the Flax library [@flax2020github], allowing the entire pipeline to remain on the GPU. Our new implementation is open-source and available on the [GitHub page of the project](https://anonymous.4open.science/r/cacto-487E/README.md).

# RESULTS

This section presents our evaluation of CACTO-BIC. First, we assess the impact of the biased initial-state sampling on data efficiency (Section [5.1](#ssec:bics_results){reference-type="ref" reference="ssec:bics_results"}). Second, we analyze the computational benefits of the GPU-based implementation (Section [5.2](#ssec:gpu_results){reference-type="ref" reference="ssec:gpu_results"}). Third, we compare CACTO-BIC with a state-of-the-art RL algorithm (Section [5.3](#ssec:ppo_results){reference-type="ref" reference="ssec:ppo_results"}). Finally, we demonstrate the scalability of the approach through experiments on a high-dimensional quadruped robot, AlienGO [@aliengo] (Section [5.4](#ssec:aliengo_results){reference-type="ref" reference="ssec:aliengo_results"}).

## Biased Initial State Sampling {#ssec:bics_results}

We evaluate the proposed exploration method on the same benchmark scenarios used in [@CACTO; @alboni2024cacto]. The task consists in minimizing the distance between the robot's end-effector and a target, while avoiding three elliptical obstacles (encoded with large penalties) and minimizing control effort. An additional reward is provided in the neighborhood of the target, as shown in Fig. [3](#fig:CostFunction_comp){reference-type="ref" reference="fig:CostFunction_comp"}.

:::: {#fig:CostFunction_comp .figure latex-placement="tbp"}
::: caption
Cost function excluding the control effort term, with target set at $[-7,0]$.
:::
::::

When the system starts from the *Hard Region* (highlighted in Fig. [3](#fig:CostFunction_comp){reference-type="ref" reference="fig:CostFunction_comp"}), it becomes challenging for a gradient-based solver to converge to the globally optimal solution.

We consider three systems of increasing complexity: a point mass with state $(x, y, v_x, v_y, t) \in \mathbb{R}^5$ and control $(a_x, a_y) \in \mathbb{R}^2$, a jerk-controlled version of the *Dubins car model* [@dubins] with state $(x,y,\theta,v,a,t) \in \mathbb{R}^6$ and control $(\omega,j) \in \mathbb{R}^2$, and a 3-degree-of-freedom (DoF) planar manipulator with a 7-dimensional state space and a 3-dimensional control input. We compare three algorithms:

1.  CACTO as presented in [@alboni2024cacto];

2.  CACTO-BIC: CACTO with biased initial-state sampling and a reduced number of TO episodes (25%) from the 2nd iteration onward;

3.  CACTO with reduced TO episodes (as CACTO-BIC), but without biased initial-state sampling.

All algorithms run for the same number of learning iterations (i.e. updates of the neural networks). Fig. [4](#fig:CACTO-SL-BICScomparison){reference-type="ref" reference="fig:CACTO-SL-BICScomparison"} shows the median (across 5 runs) of the mean cost (across initial conditions) as a function of the number of TO episodes. The results show that CACTO-BIC achieves comparable performance using $30-40\%$ of the number of TO episodes. However, this improvement comes with increased training time due to the additional std-critic network. With CACTO-BIC, the percentage of computation time devoted to training the networks rises to $93-94\%$. This motivates moving to the GPU.

:::: {#fig:CACTO-SL-BICScomparison .figure latex-placement="tb"}
::: caption
Median (across 5 runs) of the mean cost (across initial conditions) starting from the Hard Region for the point mass (top), the *Dubins car*, and the manipulator (bottom). Shaded areas represent first and third quartiles. Data are sampled every *n* updates. When multiple measurements occur at the same TO episode count, the last one is plotted.
:::
::::

## Computational Efficiency of GPU Computation {#ssec:gpu_results}

First, we assessed the speedup achievable when solving a batch of TO problems on a GPU for different batch sizes: $[10, 50, 100, 250, 500, 1000, 5000, 10000]$.

Fig. [5](#fig:TOBatchSize){reference-type="ref" reference="fig:TOBatchSize"} shows that while the CPU computation time scales approximately linearly with batch size, the GPU benefits from parallelization: the time per problem decreases as the batch size increases, eventually saturating, demonstrating the advantage of GPU-based TO.

:::: {#fig:TOBatchSize .figure latex-placement="tb"}
::: caption
Speedups for TO on GPU (w.r.t. CPU) for the point mass, the *Dubins car*, and the manipulator. Dashed lines represent speedups with random initial states and maximum number of iterations, selected as described in Section [4.1](#ssec:iteration_number){reference-type="ref" reference="ssec:iteration_number"}, while solid lines represent speedups with initial conditions selected using CACTO-BIC and maximum number of iterations set as in the two versions.
:::
::::

We now analyze the speedup achieved through the new GPU-accelerated implementation of CACTO-BIC. The number of TO problems solved in parallel was 300, 500, and 550 in the first iteration for the point mass, Dubins car and manipulator, respectively. From the second iteration onward, the batch size was reduced to 25%. The initial time is set to 0 in each TO instance. Table [1](#tab:comp_comp_time){reference-type="ref" reference="tab:comp_comp_time"} reports the computation times to perform the same updates using three versions of CACTO-BIC: a single-thread CPU version, a multi-thread CPU version, and the novel GPU version.

::: {#tab:comp_comp_time}
+-----------------------------+-------------------------+---------+
| **System** (nb. of updates) | **CPU**                 | **GPU** |
+:===========================:+:==========:+:==========:+:=======:+
| 2-3                         | 1 core     | 10 cores   |         |
+-----------------------------+------------+------------+---------+
|                             | 23 min     | 22 min     | 44 s    |
+-----------------------------+------------+------------+---------+
|                             | 3 h 44 min | 3 h 34 min | 7 min   |
+-----------------------------+------------+------------+---------+
|                             | 5 h 35 min | 5 h 15 min | 6 min   |
+-----------------------------+------------+------------+---------+

: Comparison between CPU and GPU versions of CACTO-BIC. GPU runtimes do not include the warm-up phase required for the JIT compilation of the TO solver.
:::

This test was performed on a workstation equipped with an AMD Ryzen 9 7950X CPU, 192 GB of RAM, and an NVIDIA RTX 6000 GPU with 48 GB VRAM, running on Ubuntu 22.04.

The results show that using 10 cores to parallelize the TO problems has little effect on the total computation time as most time is spent for training the neural networks. The novel GPU version of CACTO-BIC achieves instead remarkable speedups ($\approx$`<!-- -->`{=html}30x for the point mass and Dubins car, and $\approx$`<!-- -->`{=html}56x for the manipulator).

Although GPUs have far more cores than CPUs, the resulting speedups are smaller than this hardware difference suggests. Several factors contribute to this limitation. First, the TO problems are solved in batches on the GPU. Therefore a few hard instances may dominate the total computation time and cap the achievable speedup. Second, computations rely on reduced numerical precision. Although this improves raw throughput, it can introduce numerical instability and increase the number of required iterations.

By analyzing the time spent in the TO phase (creating the warm-start and solving TO problems) and in the RL phase (training networks), we observe that their relative contribution varies across systems, but remains comparatively balanced. Specifically, the TO and RL phases account for approximately 42% and 53% of the total time in the point mass, 61% and 37% in the Dubins car, and 22% and 75% in the manipulator.

It follows that the speedup comes mainly from training the networks on the GPU, which is 51-85$\times$ faster than on the CPU in our tests. In contrast, the speedup in the TO phase is modest (3-5$\times$) for the Dubins car and point mass, but it becomes significant (19$\times$) for the most complex system.

## Comparison with PPO {#ssec:ppo_results}

To evaluate CACTO-BIC w.r.t. state-of-the-art RL, we selected Proximal Policy Optimization (PPO) [@PPO] as a benchmark. For a fair comparison, we employed the fully GPU-based implementation of PPO provided by BRAX [@brax2021github]. Our analysis focuses on two aspects: first, learning a warm-start policy for a problem that exhibits local minima; second, learning a control policy for a classic benchmark problem, a customized version of the *Reacher* environment. Fig. [6](#fig:comparison_WS){reference-type="ref" reference="fig:comparison_WS"} reports the mean cost obtained using CACTO-BIC's and PPO's policies as warm-start for TO in the Point Mass and Manipulator environments. CACTO-BIC converged in one-third of the time in the first environment and in just 7% in the second one.

:::: {#fig:comparison_WS .figure latex-placement="tb"}
::: caption
Warm-start provider comparison: Median (across 5 runs) of the mean cost (across initial conditions) starting from the Hard Region for the point mass (top), and the manipulator (bottom). Shaded areas represent first and third quartiles.
:::
::::

In Fig. [7](#fig:comparison_policy){reference-type="ref" reference="fig:comparison_policy"} we compare CACTO-BIC and PPO in the Reacher Environment. Also in this case, CACTO-BIC achieves a similar cost in $\approx$`<!-- -->`{=html}10% of the computation time.

:::: {#fig:comparison_policy .figure latex-placement="tb"}
::: caption
Policy comparison: Median (across 5 runs) of the mean cost (across initial conditions) for a customized *Reacher* environment. Shaded areas represent first and third quartiles.
:::
::::

## Hardware experiments {#ssec:aliengo_results}

To evaluate CACTO's scalability and its potential for real-time applications we tested it on AlienGO, a quadrupedal robot featuring 12 degrees of freedom [@aliengo]. We address the problem of navigation in confined environments, with even terrain, and the presence of a moving obstacle. The robot must reach a moving target (see Fig. [8](#fig:setup){reference-type="ref" reference="fig:setup"}) while avoiding collisions with both the moving obstacle (a sphere of radius 0.5 m) and the walls of the room (a rectangle with sides ranging from 2 m to 10 m). We consider a fixed trotting gait with alternating diagonal leg pairs making contact with the ground.

Since legged robots have non-differentiable dynamics [@wensing2023optimization], which are not compatible with gradient-based TO, we adopt a hierarchical approach. We combine a high-level policy relying on a simplified differentiable model, with a low-level policy using the complete robot dynamics. The high-level policy is trained with CACTO-BIC, while the low-level policy is trained with the RL algorithm CAT [@chane2024cat], which can handle non-differentiable dynamics. In practice, CACTO-BIC's actor is used as a standalone policy to provide reference trajectories to the low-level policy.

### High-level policy

To train this policy, we employed a nonlinear version of the Linear Inverted Pendulum Model [@kajita2003biped]. The state $x \in \mathbb{R}^{15}$ comprises the 2D offsets of the front and rear support feet relative to the associated shoulders $\Delta p_f$ and $\Delta p_r$, the Center of Mass (CoM) position $c \in \mathbb{R}^2$ and velocity $\dot{c} \in \mathbb{R}^2$ on the horizontal plane, the step index $s_{idx} \in \mathbb{N}$, which encodes both the current contact phase and time, the obstacle position $c_{obs} \in \mathbb{R}^2$ and the location of the four walls, expressed as offsets with respect to the global reference frame $\Delta_{walls} \in \mathbb{R}^4$. $$\begin{equation}
x \triangleq (\Delta p_f, \Delta p_r, c, \dot{c}, s_{idx}, c_{obs}, \Delta_{walls}) \in \mathbb{R}^{15}.
\end{equation}$$ The target position is assumed to be the origin.

Assuming a trotting gait and constant Center of Pressure (CoP) during each contact phase, the control vector $u \in \mathbb{R}^6$ includes the offsets of front and rear support feet w.r.t. the associated shoulder in the next contact phase, $\Delta p_f ^ +, \Delta p_r ^ + \in \mathbb{R}^2$, a scalar $\alpha \in [0,1]$ that expresses the CoP as a convex combination of the support foot positions, and the contact phase duration $\delta t$: $$\begin{equation}
u \triangleq (\Delta p_f^+, \Delta p_r^+, \alpha, \delta t) \in \mathbb{R}^{6}
\end{equation}$$

The cost function penalizes the CoM-target distance, the CoM velocities, and a barrier-like cost penalizes CoM velocities beyond prescribed bounds. A smooth logarithmic reward is used to encourage reaching a narrow region around the target. Control regularization discourages deviations from nominal values: zero foot displacements, centered CoP ($\alpha=0.5$), and nominal contact-phase duration ($\delta t=0.375$ s). Obstacle avoidance is enforced through smooth logarithmic penalties. The algorithm took $\approx$`<!-- -->`{=html}109 s to converge. In this scenario, leveraging the GPU for solving the TO problems yields a substantial speedup, roughly 345$\times$.

### Low-level policy {#lowlevel}

The low-level policy is trained using a constrained RL algorithm [@chane2024cat], which builds upon PPO [@PPO], employing Isaac Gym for GPU simulation. The goal of this policy is to track the references generated by the high-level policy. During training, the high-level policy is rolled out in open loop, and updated only at the beginning of each new contact phase to enhance stability and robustness [@villa2017model].

The low-level policy receives as observations: the base state (position and orientation, linear and angular velocity, and projected gravity), the target base position and linear velocity, yaw orientation error, foot placement errors, a binary flag indicating the active diagonal contact pair, the remaining time in the current gait phase, joint positions, velocities and the previous action.

The reward function encourages accurate tracking of base position and orientation, linear and angular velocity, and the desired foot contact locations. Regularization terms are included to improve smoothness. All safety and style-related constraints are divided into soft constraints (which define a termination probability as a function of the constraint violation) and hard constraints (which cause immediate termination of the episode).

### Aliengo Simulation and Hardware results

The experiments are conducted in an indoor area of 4 m$\times$`<!-- -->`{=html}4 m (see Fig. [8](#fig:setup){reference-type="ref" reference="fig:setup"}). The obstacle and the target are either stationary or manually actuated, depending on the experiment.

:::: {#fig:setup .figure latex-placement="tbp"}
::: caption
Experimental setup: The lines define a 4 m $\times$ 4 m operational area.
:::
::::

State feedback is obtained from a motion capture system, which measures position and orientation of the robot, the obstacle and the target. Velocities are estimated by finite differencing and low-pass filtering.

Results are shown in the accompanying video.

# CONCLUSIONS

This paper presented CACTO-BIC, an extension of CACTO designed to improve scalability and computational efficiency in combined TO-RL framework by biasing the initial-state sampling using value function properties and leveraging GPU acceleration.

Experimental results demonstrate that the proposed sampling strategy effectively identifies state-space regions where actor policy improvement is more likely, leading to a $2.5-3.5\times$ increase in sample efficiency. In addition, GPU-based computation achieves 30-250$\times$ speedup compared to CACTO, with increasing benefits as system complexity grows. When compared to PPO, CACTO-BIC achieves similar final costs requiring only $7-30\%$ of the training time. Finally, experiments on the AlienGO quadruped robot show that CACTO-BIC scales to high-dimensional robotic systems and can be effectively used for real robot control.

Future works will focus on extending the proposed approach to handle constraints using augmented Lagrangian formulations [@crl]. In addition, we will explore the integration of sampling-based optimization techniques, such as MPPI [@mppi], to tackle non-differentiable dynamics. Finally, applying domain randomization may improve robustness to uncertain dynamics enhancing generalization to real-world systems [@domrand].

[^1]: $^{1}$ are with the Dept. of Industrial Engineering, University of Trento, Italy \[`elisa.alboni`,`pietronoah.crestaz`,`andrea.delprete`\]`@unitn.it`

[^2]: $^{2}$ is with LAAS-CNRS, Université de Toulouse, CNRS, Toulouse, France. `pncrestaz@laas.fr`
