---
citation_key: QuinteroPea2023Stochastic
arxiv_id: 2309.16862
arxiv_url: https://arxiv.org/abs/2309.16862
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:08:02Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Robots in unstructured environments must reliably plan safe (*i.e.*, collision-free) motions using only uncertain, noisy sensor percepts. For robots in human-oriented environments (*e.g.*, home or assistive robotics), this capability is crucial---as unsafe motions may hurt humans---and challenging, as these robots are often high degree-of-freedom ([df]{.smallcaps}) manipulators. Reliable safety under uncertainty requires not only producing plans that are unlikely to collide, but also providing evidence that plans are trustworthy. Moreover, for practical use, planners need to efficiently support complex environments without knowledge of the true environment geometry.

However, most work on motion planning under uncertainty makes simplifying assumptions about robot or environment geometry (*e.g.*, point robots or environments with only known, simple geometry) [@dawson2020; @blackmore2011_chance-constrained; @lew20_chanceconstrained; @luders10_chanceconstrained; @summers18], does not scale to high [df]{.smallcaps} systems, or places strict assumptions on the distributions of noise (*e.g.*, only translational noise, segmented to individual objects or normally distributed) [@quinteropena2021_robustoptimization; @dawson2020; @dai19].

In contrast, we introduce a method for reliable, safe motion planning for high [df]{.smallcaps} systems under sensing uncertainty that directly models inherent sensor noise without placing assumptions on the environment. We propose to quantify the aleatoric uncertainty of the sensor with an implicit model of the stochastic signed distance fields between the robot's links and points in the environment, conditioned on the robot's configuration. By explicitly modeling this uncertainty, we can both compute safe paths given only noisy sensing and approximately bound the remaining risk of collision.

![Simulated motion planning problem under sensing uncertainty. The environment is composed of noisy points (blue spheres) to be avoided. The robot must plan to grasp the cylinder without colliding with the table or objects. Our method transforms a candidate path (red) into a safe path (purple) by solving a sequence of optimization problems that account for sensing uncertainty. Cutouts show parts of the path transformation: the arm is pushed away from noisy regions to attain safer behavior.](QuinteroPea2023Stochastic_figs/fig1.png){#fig:planning_framework2 width="90%"}

Specifically, we contribute

::: enumerate*
a variational inference perspective on modeling stochastic signed distance fields for motion planning (inspired by [@shen2021_stochastic_neural]), used to learn

an implicit neural model of sensor-specific noisy egocentric distance, which we incorporate in

a novel chance-constrained inverse kinematics ([ik]{.smallcaps}) formulation, allowing us to create

a hierarchical planner that produces minimal risk motions (with respect to the learned distance model and an uncertainty-agnostic initial motion plan) in realistic environments
:::

. Our learned model directly predicts distribution parameters for noisy distance measurements to arbitrary points in the environment, allowing it to capture the aleatoric uncertainty of the sensor in question without assuming that noise is segmented to the level of individual objects or requiring knowledge of object geometry. We empirically validate that our model correctly predicts both distance values and their uncertainty, and that our planner finds motion plans that are both safe (*i.e.*, minimize risk) and reliable (*i.e.*, the predicted risk matches or conservatively upper-bounds the empirically measured probability of collision). We further compare our planner to a commonly used baseline and show that, despite longer planning times, we produce significantly safer and higher-quality plans.

# Preliminaries {#sec:background_and_problem_definition}

We consider a robot with $n$ controllable joints and configuration space $\mbox{\ensuremath{\mathcal{Q}}}\subseteq \mathbf{R}^n$. We assume that the environment is represented by noisily measured 3D points corresponding to the external surfaces of objects. Point clouds [@kuntz2020_fast] are an example of such a representation. These coordinates are usually computed from depth information from, *e.g.*, a RGB-D camera or LiDAR, which is subject to imperfect measurements and other sources of errors. The distance from the sensor to an object's surface can be modeled as a random variable with Gaussian distribution [@khoshelham2012_accuracy]. This source of sensing uncertainty tends to dominate in the settings we consider; the robot's proprioception (*i.e.*, via joint encoders) is typically much less noisy.

In "normal" motion planning, we seek a collision-free path $\rho$ connecting the initial robot configuration $q_{start} \in \mbox{\ensuremath{\mathcal{Q}}}$ to a goal region $\mbox{\ensuremath{\mathcal{Q}_{goal}}}\subset \mbox{\ensuremath{\mathcal{Q}}}$, *i.e.*, $\rho : [0,1] \rightarrow \mbox{\ensuremath{\mathcal{Q}_{free}}}$, $\rho(0) = q_{start}, \rho(1) \in \mbox{\ensuremath{\mathcal{Q}_{goal}}}$. The goal of motion planning under sensing uncertainty is to find a path that is safe despite imperfect sensing information. More specifically, we want a path whose probability of collision (*i.e.*,*risk of collision*) is no larger than a given threshold $\Delta$. This problem can be formulated as the chance-constrained optimization problem [\[prob:prob1\]](#prob:prob1){reference-type="ref" reference="prob:prob1"}: $$\label{prob:chance_constrained_traj_formulation}
\begin{align}
\tag{Prob. 1}\label{prob:prob1}
& \underset{q_0, \dots, q_T}{\text{min}}
& & f(q_{0:T}) \nonumber \\
& \text{s.t.} 
& & q_0 = q_{\text{start}},\; q_T \in \mbox{\ensuremath{\mathcal{Q}_{goal}}}, \nonumber\\
& & & q^{l} \leq q_t \leq q^{u}, \; t \in [0,\dots,T],  \nonumber\\
& & & \ensuremath{\mbox{Pr}\left(\bigwedge_t q_t \in \mbox{\ensuremath{\mathcal{Q}_{free}}}\right)} \geq 1 - \Delta, \; \label{eq:chance_constrained_traj_nocollision}
\end{align}$$ where $q_0,\dots,q_T$ are waypoints of a discretized path, $f$ is the objective function (*e.g.*, to encourage smooth, short paths), and $q^l$ and $q^u$ are lower and upper joint limits. [\[eq:chance_constrained_traj_nocollision\]](#eq:chance_constrained_traj_nocollision){reference-type="eqref" reference="eq:chance_constrained_traj_nocollision"} is a chance constraint enforcing that the probability of having no collisions *along the path* remains above the threshold. Unfortunately, this probability cannot be expressed in a tractable form suitable for optimization.

# Related Work {#sec:related_work}

## Motion Planning under environmental uncertainty {#sec:motion_planning_under_environmental_uncertainty}

Collision chance constraints, or constraints on the probability that a robot's trajectory collides with a noisy environment, have been successfully used for safe motion planning under uncertainty by a wide range of work. Chance constraints are typically determinized to keep the planning problem tractable. These deterministic reformulations are then used by either optimization [@blackmore06_aprobabilistic; @blackmore2011_chance-constrained; @lew20_chanceconstrained; @dawson2020] or sampling [@luders10_chanceconstrained; @luders10_chanceconstrained; @summers18; @kajsa2023_distributionally]-based motion planners to generate provably safe trajectories. Similarly, we also reformulate and enforce chance constraints to guarantee a desired maximum risk of collision. For example, @blackmore06_aprobabilistic [@blackmore2011_chance-constrained] create a disjunctive convex optimization problem that can be solved with branch-and-bound; @luders10_chanceconstrained build a tree-like planner that validates states against the reformulated constraints. @summers18 uses a similar idea for non-Gaussian uncertainty and moment-based ambiguity sets of distributions. Finally, @dawson2020 propose a differentiable surrogate risk for manipulator robots and convex obstacles under Gaussian translational uncertainty that is guaranteed to never underestimate the true risk, enforced by constraints in a nonlinear program. Many of these methods rely on simplified robot shapes, *e.g.*, point robots [@blackmore2011_chance-constrained; @luders10_chanceconstrained; @summers18; @lew20_chanceconstrained], obstacle shapes, *e.g.*, polyhedral [@blackmore2011_chance-constrained; @luders10_chanceconstrained; @summers18] or convex [@lew20_chanceconstrained; @dawson2020], and the noise model, *e.g.*, additive Gaussian noise on obstacle positions [@blackmore2011_chance-constrained; @luders10_chanceconstrained; @dawson2020]. In contrast, our method is designed for high-[df]{.smallcaps} robots and complex, noisy scenes, where point-robot assumptions are insufficient and strict assumptions on the noise distribution may not hold.

When reformulating chance constraints, most methods allocate equal risk for every waypoint and/or obstacle in the path to make the problem tractable [@blackmore2011_chance-constrained; @luders10_chanceconstrained; @summers18; @lew20_chanceconstrained]. However, this strategy can lead to overly conservative solutions, since robot configurations that are far from noisy obstacles will still be forced to satisfy difficult risk bounds. A few works have considered non-uniform risk allocation, either by formulating multi-stage optimization problems [@ono08], iteratively penalizing and relaxing risky waypoints from previous solutions [@dai19], or using differentiable surrogate risks encoded as variables in a nonlinear optimization problem [@dawson2020]. Similar to [@blackmore06_aprobabilistic; @lew20_chanceconstrained], our method enforces joint chance constraints by using the union bound (Boole's inequality) and solving a set of individual chance constraints. However, in our method, the risk bound of individual chance constraints for all obstacle-link pairs are decision variables in our optimization formulation.

Other methods design certificates that verify that a path is safe under a noise model. @vandeberg2010_lqgmp assess path safety by assuming a linear-quadratic controller with Gaussian uncertainty (LQG-MP). Several candidate paths are generated using a sampling-based planner and the best is chosen for execution. @axelrod18 certify a path as safe for a given level of risk if the robot's swept volume does not intersect a set of unsafe regions. @park2020_efficient design probabilistic collision checkers for non-Gaussian distributions, which they use in an optimization-based planner to encourage safety. @quinteropena2021_robustoptimization also handle non-Gaussian distributions by solving a robustly formulated sequential convex programming problem. @dai19 generate candidate paths, propagate the uncertainty along the path using LQG-MP and estimate the resulting risk of collision via numerical integration. Our proposed approach also generates risk-agnostic candidate paths which it then transforms into safe paths by solving a sequence of convex optimization problems.

## Implicit Representations and Uncertainty Quantification {#sec:implicit_neural_representations_and_uncertainty_quantification}

Recent machine learning advances have produced efficient implicit neural representations of spatial information, such as Neural Radiance Fields (NeRFs) [@mildenhall2020_nerf] and Signed Distance Fields [@park2019_deepsdf]. Robotics researchers have used these representations to learn multi-object dynamics [@driess2022_learningmultiobject], as manipulation planning constraints [@driess2021_learning_models], to achieve reactive robot manipulation [@koptev2023_neural_joint] and to perform visual-only robot navigation [@adamkiewicz2022_vision-only]. Beyond their compact, efficient storage [@adamkiewicz2022_vision-only], these representations are advantageous for planning due to their continuous representation of geometry [@adamkiewicz2022_vision-only; @koptev2023_neural_joint; @kurenkov2022_nfomp_neural] and ability to be learned directly from sensor data [@camps2022_learning]. Recent work has also investigated quantifying the uncertainty of a learned model [@clements2019_risk; @lahlou2023_deup; @acharya2023_learningtoforecast]. Methods to estimate both aleatoric and epistemic uncertainty have been proposed in the computer vision [@kendall2017_what; @vasconcelos2023_uncertainr; @shen2021_stochastic_neural] and reinforcement learning [@acharya2023_learningtoforecast; @clements2019_risk; @lahlou2023_deup] literatures. This is important to enable the design of uncertainty-aware algorithms for downstream tasks. For example, @shen2021_stochastic_neural [@shen2022_conditional] propose probabilistic frameworks that attempt to capture uncertainty in a NeRF for synthetic novel view and depth-map estimation. Similarly, our method takes a probabilistic approach to quantifying aleatoric sensing uncertainty. However, our proposed neural representation also fuses kinematic information about a robot with spatial information to produce a robot-configuration-conditioned probabilistic distance model.

![Our stochastic implicit neural signed distance functions uses **a)** a robot configuration $q$ and **b)** one noisy point $x$ as input. **c)** Inputs go through a positional encoding layer and then through $4$ fully connected layers of size $256$. Finally, two separate layers of size $K$ output the mean and standard deviation parameters of **d)** each link's distribution modeling the noisy signed distance conditioned on $q,x$.](QuinteroPea2023Stochastic_figs/nn.png){#fig:planning_framework width="\\linewidth"}

# Safe Motion Planning with a Stochastic Neural Representation {#sec:technical-approach}

In this work, we assume that information about the environment is captured through a sensor as noisy $3$D points, akin to a point cloud. This noise is aleatoric from the perspective of the planner as it stems from immutable properties of the sensor and is irreducible. We propose to quantify this aleatoric sensing uncertainty through a stochastic implicit neural representation that models noisy signed distances between the environment and the robot geometry. Our neural representation, inspired by [@koptev2023_neural_joint], captures not only geometric information about the environment (as in work based on NeRFs [@driess2022_learningmultiobject; @adamkiewicz2022_vision-only] or SDFs [@driess2021_learning_models; @kurenkov2022_nfomp_neural; @camps2022_learning]), but also kinematic information about the robot itself, which makes it suitable for motion planning for manipulation. We find safe paths despite sensing errors by using this representation in a novel *hierarchical motion planner*, instead of directly attempting to reformulate and solve [\[prob:prob1\]](#prob:prob1){reference-type="ref" reference="prob:prob1"}. Our planner first finds a candidate path using only the noisy sensed points (without knowledge of their noise), and then uses this candidate path and a user-provided bound on the risk of collision to compute a safe path. The following sections describe our aleatoric sensing representation and planning framework.

## Stochastic Neural Implicit Signed Distance Representation {#sec:stochastic_neural_implicit_signed_distance_representation}

@koptev2023_neural_joint propose an implicit neural representation that models the signed distance between each robot link and arbitrary points in space. The neural representation learns $\Gamma: \mbox{\ensuremath{\mathcal{Q}}}\times \mathbb{R}^3 \rightarrow \mathbb{R}^K$ comprising $K$ related mappings $\Gamma_k: \mbox{\ensuremath{\mathcal{Q}}}\times \mathbb{R}^3 \rightarrow \mathbb{R}$. Each $\Gamma_k(q,x)$ is the minimum distance function for the $k$-th robot link ($1 \le k \le K$), evaluated at the 3D point $x$ when the robot is in configuration $q$. This representation is useful for motion planning for manipulation due to

::: enumerate*
representing distances to arbitrary points in the workspace without depending on specific geometry and

its gradients point away from obstacles in *configuration space*
:::

.

Inspired by this representation, we propose to learn a distribution, $S$, over signed distance functions, such that the distance between each robot link and points in the workspace is modeled as a Gaussian random variable. We want to learn the posterior of $S$ conditioned on a training set $\mathcal{T}$ consisting of a finite collection of robot configurations $q_i$, 3D points $x_i$ and per-link noisy signed distance values $d_i^k$, *i.e.*,$\mathcal{T} = \{\left ( \{d_i^k\}_{k=1}^{K}, q_i, x_i \right)\}_{i=1}^{N}$.

We formulate the problem using a Bayesian approach [@shen2021_stochastic_neural] to compute the posterior $\ensuremath{\mbox{Pr}\left(S | \mathcal{T}\right)}$. Note that explicitly computing this posterior is intractable since it would require the computation of the evidence *i.e.*, the marginal density of the observations. Instead, we approximate it using variational inference (VI), where a parametric distribution $\psi_{\theta}(S)$ approximates the true distribution. The goal of VI is to find the parametric distribution that is closest to the true distribution, measured via their KL divergence [@blei2017_variational]. As the KL divergence is not computable because it requires the evidence, VI typically optimizes the evidence lower bound (ELBO) [@blei2017_variational]. For our problem, the VI formulation is: $$\label{eq:deterministic_nnik}
\begin{align}
& \underset{\theta}{\text{min}}
 \underbrace{\mathbb{E}_{\psi_{\theta}(S)}\log\left( \frac{\psi_{\theta}(S)}{p\left(S\right)} \right)}_{\text{KL-divergence prior}} - \underbrace{\mathbb{E}_{\psi_{\theta}(S)}\log\left( \ensuremath{\mbox{Pr}\left(\mathcal{T}~|~S\right)}\right)}_{\text{Log likelihood}}\; \label{eq:neg_elbow}
\end{align}$$ where the first term is the KL divergence between $\psi_{\theta}$ and a prior $p(S)$ on the signed distance field, to encourage densities close to the prior, and the second term is the negative training set likelihood over the approximate posterior $\psi_{\theta}$, which will choose parameters $\theta$ that best explain the observed data.

We assume that $\psi_{\theta}$ can be factored as the product of independent Gaussian densities, $\psi^k_{\theta}(d|q,x)$, representing the distance fields for each robot link $k$. These densities are jointly modeled as a neural network, $\Gamma(q,x)$, that outputs the parameters of $\psi_{\theta}$, $\{\mu_{1}, \sigma_{1},\dots,\mu_{K}, \sigma_{K}\}$ (see [2](#fig:planning_framework){reference-type="ref+label" reference="fig:planning_framework"} for network architecture). The second term in [\[eq:neg_elbow\]](#eq:neg_elbow){reference-type="ref+label" reference="eq:neg_elbow"} is computed in closed form using the likelihood of the Gaussian distribution. For the first term we assume that (similar to $\psi_\theta$) the prior can be factored as a product of Gaussians, $p^k(d)$ with parameters $\{\mu^p_{k}, \sigma^p_{k},\}$. The KL divergence between these distributions can be computed analytically as: $$\begin{align*}
\text{KL}\left( \psi_{\theta}(S) || p \left(S \right) \right) &= 
   \sum_{k=1}^{K}\sum_{x \in \mathbb{R}^3}\sum_{q \in \mathbb{Q}}\text{KL}\left(\psi_{\theta}^k(S | x,q) || p^k \left(S \right) \right) \\
  &\approx \sum_{k=1}^{K}\sum_{i}\frac{\sigma_{k,i}^2 + (\mu^p_{k,i} - \mu_{k,i})^2}{2{\sigma^p_{k,i}}^2}   -\log \sigma_{k,i}
\end{align*}$$ In practice, we use a fixed number of samples to remove the dependency of the approximate posterior on $x$ and $q$.

## Chance-Constrained Hierarchical Planning {#sec:chance-constrained_layered_planning}

We propose a hierarchical motion planner to generate safe robot motions, described in [\[algo:safe_motion_planning\]](#algo:safe_motion_planning){reference-type="ref+label" reference="algo:safe_motion_planning"}. First, an off-the-shelf motion planner [@kavraki96_probabilistic; @lavalle00_rapidly; @kuffner00_rrtconnect; @ratliff09_chomp; @schulman2014_motion] is used to find a candidate path $\rho^c$ in the noisy sensed environment $\Xi$ ([\[line:motion_planning\]](#line:motion_planning){reference-type="ref+label" reference="line:motion_planning"}) . For each waypoint of $\rho^c$ ([\[line:waypoint_it\]](#line:waypoint_it){reference-type="ref+label" reference="line:waypoint_it"}), we solve a chance-constrained [ik]{.smallcaps} problem ([ccikopt]{.smallcaps}, [\[line:ccikopt\]](#line:ccikopt){reference-type="ref+label" reference="line:ccikopt"}) to compute the motion to the *next* waypoint. We use the pose of the robot's end-effector at $q^c_{j+1}$ as a soft constraint for the $j$-th [ik]{.smallcaps} problem, encouraging solutions close to the original path. We accumulate the risk allocated to each waypoint to ensure that it does not exceed the bound $\Delta$ for the total path ([\[line:remaining_risk\]](#line:remaining_risk){reference-type="ref+label" reference="line:remaining_risk"}). Each [ik]{.smallcaps} problem is allowed up to the full remaining risk available, and returns an upper bound on the risk allocated to the corresponding waypoint. This method can be seen as using $\rho^c$ as *guidance* for the sequence of [ik]{.smallcaps} problems, while flexibly accommodates the allowable risk bounds to compute a safe path, $\rho^s$.

::: algorithm
$\leftarrow$ $(q_{start}, \mbox{\ensuremath{\mathcal{Q}}}_{goal}, \Xi)$ []{#line:motion_planning label="line:motion_planning"} $\Delta_0 \leftarrow \Delta$, $q^s_0 \leftarrow q^c_0$ return $[q^s_0, \dots,q^s_T], \Delta_{T-1}$
:::

We extend the [ik]{.smallcaps} formulation of [@koptev2023_neural_joint] to the chance-constrained [ik]{.smallcaps} setting in [\[prob:prob2\]](#prob:prob2){reference-type="ref" reference="prob:prob2"}: $$\begin{align}
\tag{Prob. 2}\label{prob:prob2}
& \underset{\bm{\Delta q}, \bm{\delta}}{\text{min}} \nonumber
& & \bm{\Delta q^{T}} Q \bm{\Delta q} + \bm{\delta^{\top}}D\bm{\delta}\nonumber\\
& \text{s.t.}
& & q^{l} \leq q^s_j + \bm{\Delta q} \leq q^{u} \nonumber \\
& & & \text{FK}(q^s_j) + J^{\top}(q^s_j)\bm{\Delta q} = \text{FK}(q^c_{j+1}) + \bm{\delta} \nonumber \\
& & & \ensuremath{\mbox{Pr}\left(\bigwedge_{r,k}  -\nabla \Gamma_{k,r}^{\top} \bm{\Delta q} \leq \Gamma_{k,r} - r_r\right)} \geq 1 - \Delta_j \label{eq:original_joint_chance_constraint}
\end{align}$$ with decision variables $\bm{\Delta q}$ and $\bm{\delta}$. $\bm{\Delta q}$ corresponds to the robot motion between $q^s_j$ and $q^s_{j+1}$; $\bm{\delta}$ is a vector of slack variables that provide flexibility on the goal pose of the end-effector. We minimize a quadratic function of the decision variables to encourage small motions that end close to the original end-effector pose from $\rho^c$. Constraint [\[eq:original_joint_chance_constraint\]](#eq:original_joint_chance_constraint){reference-type="eqref" reference="eq:original_joint_chance_constraint"} is the joint chance constraint requiring the risk of collision to remain under a given threshold $\Delta_j$ for all robot links $1 \le k \le K$ and noisy points $1 \le r \le R$. In its deterministic version [@koptev2023_neural_joint], when $\Gamma_{k,r} = \Gamma_k(q^s_{j},x_r)$ becomes small, $\bm{\Delta q}$ is forced to align with $-\nabla \Gamma_{k,r}$ (which points away from collision with $r$) to avoid potential collisions. In our approach, $\Gamma_{k,r}$ are random Gaussian variables, and we enforce that the probability that this constraint is satisfied is above a given threshold. In the next section we describe our reformulation of the constraint to make the problem tractable.

## Reformulation of the Chance-Constrained IK Problem {#sec:reformulation_of_chance_constrained_IK_problem}

For simplicity, let $\bm{x^{\top}} = [\bm{\Delta q^{\top}}, \bm{\delta^{\top}}]$, $A = \text{diag}([Q,~D])$, $B = [J^{\top}(q^s_j),~-I]$, $c^{\top} = [-\nabla \Gamma_{k,r}^{\top},~0 ]$, $g = \Gamma_{k,r} - r_r$, and $b = \text{FK}(q^c_{j+1})-\text{FK}(q^s_j)$. We also use the following facts:\

::: enumerate*
$\ensuremath{\mbox{Pr}\left(\bigwedge_i A_i\right)} \geq 1 - p \iff \ensuremath{\mbox{Pr}\left(\bigvee_i  \bar{A}_i\right)} \leq p$

$\ensuremath{\mbox{Pr}\left(\bigvee_i A_i\right)} \leq p \Longleftarrow \sum_i \ensuremath{\mbox{Pr}\left(A_i\right)} \leq p$

$\sum_i \ensuremath{\mbox{Pr}\left(A_i\right)} \leq p \Longleftarrow \ensuremath{\mbox{Pr}\left(A_i\right)} \leq p_i, \; \forall i, \sum_i p_i \leq p$
:::

.

We rewrite [\[eq:original_joint_chance_constraint\]](#eq:original_joint_chance_constraint){reference-type="eqref" reference="eq:original_joint_chance_constraint"} in simplified notation, then apply **(4a-c)**: $$\begin{align*}
&\ensuremath{\mbox{Pr}\left(\bigwedge_r\bigwedge_k c^{\top}\bm{x} \leq g\right)} \geq 1-\Delta_j, &\\
&\Longleftarrow \sum_r \ensuremath{\mbox{Pr}\left( \bigvee_k  c^{\top}\bm{x} \geq g \right)} \leq \Delta_j, & \text{\textbf{(4a)}, \textbf{(4b)}}\\
&\Longleftarrow \sum_k\ensuremath{\mbox{Pr}\left( c^{\top}\bm{x} \geq g \right)} \leq \bm{y_r} \; \forall r, \; \sum_r \bm{y_r} \leq \Delta_j, & \text{\textbf{(4c)}, \textbf{(4b)}}\\
&\Longleftarrow \ensuremath{\mbox{Pr}\left(c^{\top}\bm{x} \geq g\right)} \leq \bm{\gamma_{k,r}} \; \forall r, k, \; \sum_{k,r}\bm{\gamma_{k,r}} \leq \Delta_j, & \text{\textbf{(4c)}}\\
&= \ensuremath{\mbox{Pr}\left(c^{\top}\bm{x} \leq g \right)} \geq 1 - \bm{\gamma_{k,r}} \; \forall r, k, \; \sum_{r,k}\bm{\gamma_{k,r}} \leq \Delta_j&
\end{align*}$$ where $\bm{\gamma_{k,r}}$ is the risk allocated to link $k$ and point $r$. By properties of the Gaussian CDF [@prekopa1995_stochastic], we know $\ensuremath{\mbox{Pr}\left(a^{\top}b \leq c\right)} \geq p \iff a^Tb-\mu_c+\sigma_c\phi^{-1}(p) \leq 0$ for $c \sim \mathcal{N}(\mu_c, \sigma^2_c)$, where $\phi^{-1}$ is the inverse CDF of the standard normal distribution. Thus, we can write the following deterministic reformulation for [\[eq:original_joint_chance_constraint\]](#eq:original_joint_chance_constraint){reference-type="eqref" reference="eq:original_joint_chance_constraint"}:

$$\begin{align}
    c^{\top}\bm{x}-\mu_{k,r}+\sigma_{k,r}\phi^{-1}(\bm{\bar{\gamma}_{k,r}}) &\leq 0 \; \forall k,r \label{eq:reformulated_constraint1}\\
    \sum_{k,r}(1-\bm{\bar{\gamma}_{k,r}}) &\leq \Delta_j\label{eq:reformulated_constraint2}
\end{align}$$ where $\bm{\bar{\gamma}_{k,r}} = 1-\bm{\gamma_{k,r}}$. Finally, we provide a conservative reformulation of [\[eq:reformulated_constraint1\]](#eq:reformulated_constraint1){reference-type="eqref" reference="eq:reformulated_constraint1"} by noting that, for $0.5 \leq x < 1$, $\sqrt{\pi/8}\log\left( x/(1-x) \right) \geq \phi^{-1}(x)$, allowing:

$$\begin{equation}
 \text{\eqref{eq:reformulated_constraint1}}\Longleftarrow c^{\top}\bm{x}-\mu_{k,r}+\sigma_{k,r}\sqrt{\frac{\pi}{8}}\log\left( \frac{\bm{\bar{\gamma}_{k,r}}}{1-\bm{\bar{\gamma}_{k,r}}} \right) \leq 0 \label{eq:deterministic_reformulated_chance_constraint}
\end{equation}$$ which requires the risk variables to be in $0 < \bm{\gamma_{k,r}} \leq 0.5$. This restriction is reasonable in our context since we are interested in paths with low collision risk. Using [\[eq:reformulated_constraint2\]](#eq:reformulated_constraint2){reference-type="eqref" reference="eq:reformulated_constraint2"} and [\[eq:deterministic_reformulated_chance_constraint\]](#eq:deterministic_reformulated_chance_constraint){reference-type="eqref" reference="eq:deterministic_reformulated_chance_constraint"} instead of [\[eq:original_joint_chance_constraint\]](#eq:original_joint_chance_constraint){reference-type="eqref" reference="eq:original_joint_chance_constraint"} allows us to write the following optimization problem: $$\begin{align*}
\tag{Prob. 3}\label{prob:prob3}
& \underset{\bm{x}, \bm{\bar{\gamma}}}{\text{min}}
& & \bm{x}^{\top} A \bm{x} + h^{\top}\bm{\bar{\gamma}}\\
& \text{s.t.}
& & x_l \leq \bm{x} \leq x^u \;\\
& & & \bar{\gamma}_l \leq \bm{\bar{\gamma}} \leq \bar{\gamma}^u \;\\
& & & B\bm{x} = b \;\\
& & & c^{\top}\bm{x}-\mu_{k,r}+\sigma_{k,r}\sqrt{\frac{\pi}{8}}\log\left( \frac{\bm{\bar{\gamma}_{r,k}}}{1-\bm{\bar{\gamma}_{r,k}}} \right) \leq 0,\; \forall k,r \\
& & &\sum_{r,k}(1-\bm{\bar{\gamma_{k,r}}}) \leq \Delta_j
\end{align*}$$

We have added a linear term on the objective function of the reformulated problem to minimize the amount of risk allocated to the waypoint at the $j$-th iteration. This per-waypoint minimum risk behavior of our formulation is necessary to account for potentially high-risk future waypoints on the path. It also has the effect of allowing us to *globally* minimize (with respect to $\Gamma$ and $\rho^c$) the risk of $\rho^s$. To solve [\[prob:prob3\]](#prob:prob3){reference-type="ref" reference="prob:prob3"}, we create piecewise-affine conservative approximations of the $\log$ functions in the collision risk chance-constraints. This approximation creates mixed-integer programs that can be solved using commercial solvers [@gurobi] to global optimality at the cost of potentially high computation time.

# Evaluation and Results {#sec:experiments}

We evaluate our proposed approach on a $n=8$ [df]{.smallcaps} Fetch robot with $K=11$ links, corresponding to those in the kinematic chain of its end effector (including the torso and fingers). We use PyBullet [@coumans2021_pybullet] for collision checking, PyTorch [@paszke2019_pytorch] for neural network training, OMPL's Python bindings [@sucan2012_ompl] for planning and Gurobi [@gurobi] as our optimizer. All experiments were conducted on an Intel i7-12700K CPU and a RTX2080Ti GPU.

## Implicit Neural Representation {#sec:results_stochastic_signed_distance_neural_representation}

We parameterize our implicit stochastic distance model as a feed-forward neural network ([2](#fig:planning_framework){reference-type="ref+label" reference="fig:planning_framework"}c). For a $n$-[df]{.smallcaps} robot, the network takes an input tensor of size $3 * (n + 3)$ comprising the $n$ values of the robot configuration concatenated with the $3$ coordinates of the environment point, as well as the sine and cosine of these values. These trigonometric components serve as a form of positional encoding similar to that used in standard neural radiance fields [@mildenhall2020_nerf]. The network has a shared core of four fully connected 256-wide layers with rectified linear unit (ReLU) activation. For a robot with $K$ links, the output of these layers is used (independently) with one additional fully connected layer of size $256 \times K$ to predict the mean distance from the environment point to each link's geometry, as well as with another fully connected layer of size $256 \times K$ and a softplus layer of size $K$ to predict the standard deviation of these distances.

We generate a dataset of noisy distance samples from a simulated sensor to train the distance model. Similarly to @koptev2023_neural_joint, we sample a set of robot configurations ($Q$) uniformly at random. For each configuration, we sample a set of environment points uniformly at random ($P_R$), a set of environment points *near* to each link ($P_N$) and a set of environment points *inside* each link ($P_I$). We compute the true shortest distance between each point and link using PyBullet. We then simulate a set of noisy sensor measurements ($NS$) with mean at the true distance for each environment point and a fixed standard deviation ($\sigma$). In our experiments, $|Q| = 3000$, $|P_R| = 500$, $|P_N| = K * 10$, $|P_I| = K * 20$, $|NS| = 50$, and $\sigma = \SI{2}{\cm}$. This results in a total of 2.49 million sampled points, each of which has 50 noisy distance samples. Empirically, this dataset is roughly balanced between points in collision and points in free space.

We train the model on the collected dataset for $500$ epochs with an Adam [@kingma2014adam] optimizer, learning rate of $1\times 10^{-4}$, and batch size of $512$. We verify its performance by predicting distance distributions between robot links and a set of randomly generated 3D points from the waypoints of $1000$ discretized paths. The gripper link shows an average error of $\SI{1}{\cm}$ for mean and $\SI{3.7}{\mm}$ for standard deviation while the elbow attains $\SI{0.7}{\mm}$ and $\SI{0.3}{\mm}$, respectively. [3](#fig:neural_network_results){reference-type="ref+label" reference="fig:neural_network_results"} shows the predicted and true distribution parameters for one path, one randomly selected point and these two robot links.

![Comparison between true and predicted probability distribution parameters (mean at the top and standard deviation at the bottom) for the distance between robot links and a randomly generated point in space for the Gripper (left) and Elbow (right) links along a path of $500$ waypoints. Note that---despite the visual gap---the actual error in standard deviation is small, less than 1 mm.](QuinteroPea2023Stochastic_figs/nn_perf.png){#fig:neural_network_results width="99%"}

## Safe Motion Planning with Implicit Neural Representation

We evaluate our proposed approach on a set of simulated tabletop manipulation problems generated using [MotionBenchMaker]{.smallcaps} [@chamzas2022-motion-bench-maker]. The Fetch robot needs to plan to grasp an object, avoiding collisions with the table and obstacles upon it ([1](#fig:planning_framework2){reference-type="ref+label" reference="fig:planning_framework2"}). We create 50 problems by randomly perturbing the positions ($\pm 2.5$cm in $x,y,z$) and orientations ($\pm15^{\circ}$) of the objects of a nominal scene and the relative pose of the robot's base ($\pm10$cm in $x, y, z$ and $\pm90^{\circ}$) with respect to the table. The environment is represented as a point cloud-like set of noisy 3D spheres of different radii that covers the (unknown to the planner) collision geometries of all objects. We assume that the table's geometry is noise-free while the objects on top are noisily sensed, per [5.1](#sec:results_stochastic_signed_distance_neural_representation){reference-type="ref+label" reference="sec:results_stochastic_signed_distance_neural_representation"}. Note that these problems were designed by @chamzas2022-motion-bench-maker to be challenging and "realistic" from the motion planning perspective and require the robot to plan long, elaborate paths that need to avoid the table and then dodge collisions with the objects on top.

We compare the performance and safety of our approach with a commonly used baseline: inflating the environment's geometry to encourage the computation of paths that maintain larger clearance and have therefore less chances of colliding. We inflate each sphere by increasing its radius by $20\%, 40\%,$ or $60\%$. We also include results of $0\%$ inflation as a baseline to show the performance of a planner that is unaware of the sensing uncertainty. Motion plans for all baselines, as well as the candidate paths used by our method, are computed using RRT-Connect [@kuffner00_rrtconnect] with simplification enabled to encourage short and smooth paths.

We estimate the risk of collision for each computed path using Monte-Carlo sampling with $20,000$ samples, where each sample draws sphere poses from the noisy sensed distribution. For our method, we also show the guaranteed path-wise risk bound (Risk Bound) and estimated risk of collision of the candidate path before optimization (Initial Risk). All problems have a maximum number of $15$ attempts to find any valid (*i.e.*, collision-free with respect to the inflated obstacles, for the baselines) plan. The results are shown in [4](#fig:risk){reference-type="ref+label" reference="fig:risk"}.

:::: {#fig:risk .figure}
::: caption
Estimated CDF of the risk attained by each method on all 50 problems.
:::
::::

We note that the uncertainty-unaware planner produces paths with the highly variable risk of collision (an average of $60\%$), which is likely unacceptable for safety-critical applications. For higher parameter values of the inflated baseline, the estimated risk of collision decreases as expected due to a larger $\mathcal{Q}$-space obstacle region that encourages larger clearance with the true geometry. However, there is no clear relation between the inflation increase and the drop in risk which makes the baselines difficult to tune when a desired level of risk is required (see also [1](#tbl:results){reference-type="ref+label" reference="tbl:results"}). Additionally, we note that success rate (not shown here) for the baseline methods started dropping significantly as the inflation ratio increased, suggesting a potential limit on minimum risk that they can attain for these problems. We give our planner a maximum allowable risk bound of $10\%$ and ask it to return the minimum risk for each waypoint. Our proposed approach can compute paths with significantly lower risk for most problems, starting from risky candidate paths.

For each problem and method we also compute the path length and end-effector displacement as path quality metrics, as well as the time taken by the planner. The results are summarized in [1](#tbl:results){reference-type="ref+label" reference="tbl:results"}.

::: {#tbl:results}
          Method  EE Disp. (m)    Path Length (rad.)     Path Risk     Planning Time (s)
  -------------- --------------- -------------------- --------------- -------------------
     Inflated 0%  $2.32\pm0.82$     $7.91\pm2.53$      $0.60\pm0.33$    $3.51\pm10.42$
    Inflated 20%  $2.39\pm0.76$     $8.34\pm2.74$      $0.48\pm0.29$     $3.61\pm9.55$
    Inflated 40%  $2.33\pm0.79$     $8.27\pm2.86$      $0.42\pm0.26$    $5.85\pm13.73$
    Inflated 60%  $2.38\pm0.85$     $8.57\pm3.18$      $0.28\pm0.25$    $5.69\pm12.95$
        Proposed  $2.16\pm0.60$     $6.93\pm2.26$      $0.01\pm0.02$   $150.63\pm55.38$

  : Mean and standard deviation of path quality metrics for all methods on the 50 problems.
:::

[]{#tbl:results label="tbl:results"}

The table shows mean and standard deviation for each method over all $50$ problems. The large values of path length and end-effector displacement are evidence of the high complexity of the computed paths due to the challenging motion planning problems. Our method finds paths with lowest end-effector displacement and path length, which is the result of the minimization of motion displacement in our planner. However, our method shows planning times that are orders of magnitude larger than the baselines. This is mostly due to a large number of risk constraints being added to each chance-constrained problem, which creates large mixed-integer programs that require deep branch and bounds searches to find optimal solutions. Despite this, it is noteworthy that our method can find paths with the lowest collision risk among the baselines without sacrificing path quality.

# Concluding Remarks {#sec:conclusion}

This paper presents a novel approach to planning under sensing uncertainty for high [df]{.smallcaps} robots that reliably computes safe paths without strong assumptions on the true environment geometry. Our planner relies on an implicit neural representation trained to capture aleatoric uncertainty arising from the robot's sensor. Our representation does not place assumptions on the environment but instead directly approximates signed distance distributions between the robot and points in space, conditioned on robot configurations. We further show how this representation can be integrated with a hierarchical planner to compute paths with guaranteed bounds on the probability of collision (up to the quality of the model). We have experimentally validated the merits of our approach on challenging, realistic manipulation motion planning problems to show that our method is capable of finding safe paths despite sensing uncertainty without reducing path quality. As future work we will investigate how to further reduce the need for conservative over-approximations in our approach, since this will allow us to solve more tightly constrained motion planning problems, such as those found in manipulation in clutter. We will also seek to reduce the time taken by our method, in part by applying intelligent constraint subset selection heuristics [@hauser_semiinfinite_2021] to simplify the optimization problems solved at each waypoint. Finally, we will further investigate the need to consider the epistemic uncertainty coming from our neural representation for planning; a problem that has recently gained much attention in machine learning [@acharya2023_learningtoforecast].

[^1]: All authors are affiliated with the Department of Computer Science, Rice University, Houston TX, USA `{carlosq, wbthomason, zak, anastasios, kavraki}@rice.edu`. This work was supported in part by NSF RI 2008720, NSF ITR 2127309 for the Computing Research Association CIFellows Project, and Rice University Funds.
