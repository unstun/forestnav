---
citation_key: Ku2026PCDiffuser
arxiv_id: 2603.10330
arxiv_url: https://arxiv.org/abs/2603.10330
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:20:57Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

Motion planning for autonomous driving must handle a wide spectrum of traffic interactions that are difficult to fully anticipate with hand-crafted rules. This has motivated data-driven planners that learn driving behavior from expert demonstrations, enabling generalization across diverse real-world scenarios [@caesar2021nuplan]. Among these approaches, diffusion-based planners have recently emerged as a strong paradigm for long-horizon planning [@janner2022diffuser; @ho2020ddpm]. By starting from a noisy trajectory and iteratively denoising it into a coherent plan, diffusion planners refine the entire horizon jointly, which helps avoid the compounding errors of autoregressive action prediction and yields globally consistent behavior over long rollouts [@janner2022diffuser; @zheng2025diffusionplanner; @tan2025flowplanner].

Despite these advantages, diffusion planners offer limited reliability guarantees. Their learned score function encourages trajectories that resemble the training distribution, but provides no formal mechanism to prevent unsafe outcomes when the scene departs from the data manifold. In rare or out-of-distribution traffic configurations, the generated plan can be physically plausible yet unsafe, including collision-inducing behaviors. This gap between strong average-case performance and the absence of worst-case guarantees is a central barrier to safety-critical deployment.

:::: {#fig:PC-Diffuser .figure latex-placement="h"}
![](Ku2026PCDiffuser_figs/PC-Diffuser_overview.png){width="\\linewidth"}

::: caption
Overview of the proposed PC-Diffuser safety augmentation framework.
:::
::::

A natural response is to combine diffusion planning with formal safety enforcement mechanisms such as control barrier functions (CBFs). However, existing integrations often miss at least one of three requirements that matter in practice. First, safety should be certified on the trajectory that will be executed under the vehicle dynamics (i.e., the rollout induced by tracking/control), not merely on intermediate diffusion iterates or raw waypoint sequences. Second, that certification must be dynamics-consistent: enforcing purely geometric constraints on waypoints, or using an inconsistent motion model, can produce "safe" plans that are not physically realizable. Third, the correction should be minimally invasive, preserving the planner's intended path as much as possible to avoid large distributional shifts that degrade driving quality, inducing overly conservative or even unsafe behavior. Achieving all three simultaneously is nontrivial: enforcing CBF constraints aggressively can distort the learned behavior, while enforcing them weakly (or at the wrong time index) can fail to certify the executed trajectory.

To bridge this gap, we propose **PC-Diffuser**, a framework that injects a certifiable, path-consistent structure into the denoising loop so that safety is enforced during generation rather than repaired afterward. In doing so, we aim to answer three fundamental questions when it comes to improving safety for diffusion-based planning: (1) *Which is the right object to certify?* (i.e., the executed rollout induced by tracking/control rather than intermediate diffusion iterates or waypoint sequences); (2) *How can we make certification dynamics-consistent?* so that safety guarantees align with what the vehicle can physically execute; and (3) *How should the safety correction change the plan?* such that violations are resolved with minimal disruption to the planner's intended path and without introducing large distributional shifts that degrade driving quality. The **main contributions** of this paper are:

1.  We introduce a certifiable, path-consistent barrier-function structure that jointly supports rollout-time safety, dynamic feasibility, and minimal deviation from the learned diffusion behavior, enabling safety enforcement that is both physically meaningful and minimally invasive.

2.  We integrate this structure directly into the denoising loop, allowing iterative, context-aware safeguarding during generation and thereby reducing reliance on one-shot post-processing that can be brittle in rare or out-of-distribution scenarios.

3.  We evaluate on the nuPlan closed-loop benchmark [@caesar2021nuplan] and show that PC-Diffuser eliminates the majority of catastrophic failures on the all-collision challenge set, driving the collision rate down from 100% to 10.29%, outperforming popular baseline methods. This is done without compromising driving performance, demonstrated by an improvement in nuplan's composite score on standard Val14 and Test14-hard splits relative to the vanilla baseline diffusion planner.

# Related Works

A growing body of work has sought to improve the safety of diffusion-based planners, spanning guidance at the score level, constrained denoising, and post-processing safety layers.

**Score-guidance for safety.** DiffusionPlanner [@zheng2025diffusionplanner] steers the denoising process toward safer behaviors by backpropagating gradients from a hand-crafted reward classifier into the diffusion score. While effective in biasing samples, gradient-based guidance does not provide a formal safety certificate and can introduce artifacts that are dynamically inconsistent, since the guided trajectory is not necessarily generated through a dynamics-respecting rollout. Additionally, hand-crafted reward classifier often doesn't provide meaningful gradients and often disrupts the model's learned driving behavior.

**Constrained denoising via CBFs.** SafeDiffuser [@xiao2023safediffuser] and SafeFlow [@dai2025safeflow] introduce Constrained denoising methods through embedding Control Barrier Function constraints directly into the denoising process, enforcing forward invariance across the diffusion index rather than over rollout time. While this guarantees that consecutive denoising iterates remain in a CBF-safe set, the diffusion index is not rollout time: the final executed trajectory carries no formal safety certificate, and dynamic feasibility is left unaddressed.

**Optimization-based safety layers.** A complementary line of work enforces safety by filtering controls or trajectories through constrained optimization. CBF-QP [@ames2017cbfqp] applies a reactive safety filter at each control step, which can ignore the planner's long-horizon intent and induce conservative, myopic deviations from the learned behavior. MPC-CBF [@zeng2021mpccbf] incorporates lookahead by imposing CBF constraints within a receding-horizon formulation, but the resulting problem is often non-convex and challenging to solve reliably in real time, and the corrected solutions can drift away from the learned distribution.

**Validation and fallback.** PACS [@romer2025pacs] and RAIL [@leung2024rail] validate a learned plan via reachability analysis and switch to a backup policy when collision is predicted. This preserves the original plan when already safe, but the fallback behavior, often emergency braking, can itself be hazardous or overly disruptive in dense, interactive traffic.

In contrast to the above approaches, our goal is to couple diffusion generation with certifiable safety in a way that targets the executed rollout. Specifically, we enforce CBF forward invariance over rollout time instead of diffusion time, design the correction to be minimally disruptive so the plan remains close to the intended trajectory and learned distribution, and jointly search for a safe trajectory with the diffusion planner rather than relying on a rule-defined fallback policy.

# Preliminaries

## Vehicle Dynamics

We model the ego vehicle with a kinematic bicycle model with state $\mathbf{x} = (x, y, \theta, \delta, v) \in \mathbb{R}^5$ (position, heading, steering angle, speed) and control $\mathbf{u} = (\dot\delta, a)$ (steering rate, acceleration). The dynamics are $\dot{\mathbf{x}} = f(\mathbf{x}) + g(\mathbf{x})\,\mathbf{u}$ and control affine in $(\mathbf{x},\mathbf{u})$, with $$\begin{equation}
    f(\mathbf{x}) = \begin{bmatrix} v\cos\theta \\ v\sin\theta \\ \frac{v\tan\delta}{L} \\ 0 \\ 0 \end{bmatrix}, \quad
    g(\mathbf{x}) = \begin{bmatrix} 0 & 0 \\ 0 & 0 \\ 0 & 0 \\ 1 & 0 \\ 0 & 1 \end{bmatrix},
    \label{eq:bicycle}
\end{equation}$$ where $L$ is the wheelbase.

## Control Barrier Functions

For a control-affine system, a continuously differentiable function $h: \mathbb{R}^n \to \mathbb{R}$ is a *Control Barrier Function* (CBF) [@ames2019cbf] for the safe set $\mathcal{S} = \{\mathbf{x} : h(\mathbf{x}) \geq 0\}$ if there exists an extended class-$\mathcal{K}_\infty$ function $\alpha$ such that $$\begin{equation}
    \sup_{u \in \mathcal{U}}\!\left[\nabla h(\mathbf{x})^\top\!\left(f(\mathbf{x}) + g(\mathbf{x})u\right)\right] \geq -\alpha\!\left(h(\mathbf{x})\right),
    \label{eq:cbf}
\end{equation}$$ for all $\mathbf{x} \in \mathcal{S}$. Any Lipschitz controller satisfying [\[eq:cbf\]](#eq:cbf){reference-type="eqref" reference="eq:cbf"} renders $\mathcal{S}$ forward invariant [@ames2019cbf]. The minimally invasive safe controller is obtained via the *CBF-QP*: $$\begin{equation}
\begin{aligned}
    u^* = \arg\min_{u \in \mathcal{U}}\;& \|u - u_{\mathrm{nom}}\|^2 \\
    \mathrm{s.t.}\quad& \nabla h(\mathbf{x})^\top\!\left(f(\mathbf{x}) + g(\mathbf{x})\,u\right) \geq -\alpha\!\left(h(\mathbf{x})\right).
\end{aligned}
\label{eq:cbf_qp}
\end{equation}$$

## Diffusion-Based Planning

We adopt Denoising diffusion probabilistic model (DDPM) [@ho2020ddpm] for trajectory planning and generate an ego-state trajectory over a rollout horizon $K$. Let $\boldsymbol{\tau} = (\mathbf{x}_1,\ldots,\mathbf{x}_K)\in\mathbb{R}^{K\times 4}$ ($x, y, cos \theta, sin \theta$) denote the trajectory, where each $\mathbf{x}_k$ is the ego state at rollout time $k$. Diffusion planning generates $\boldsymbol{\tau}$ by running a learned reverse-time denoising process for $T$ steps, starting from isotropic Gaussian noise $\boldsymbol{\tau}_T \sim \mathcal{N}(\mathbf{0},\mathbf{I})$.

At each diffusion step $t$, the denoising network $\epsilon_\theta(\boldsymbol{\tau}_t,t)$ predicts the noise component in the current noisy sample $\boldsymbol{\tau}_t$ which can be used to form an estimate of the underlying clean trajectory: $$\begin{equation}
    \hat{\boldsymbol{\tau}}_0^{(t)} = \frac{1}{\sqrt{\bar{\alpha}_t}}
    \left(\boldsymbol{\tau}_t - \sqrt{1-\bar{\alpha}_t}\;\epsilon_\theta(\boldsymbol{\tau}_t,t)\right),
    \label{eq:clean_estimate}
\end{equation}$$ where $\bar{\alpha}_t$ denotes the cumulative noise schedule. The next iterate $\boldsymbol{\tau}_{t-1}$ is then sampled from the DDPM reverse transition: $$\begin{equation}
    \boldsymbol{\tau}_{t-1} = \sqrt{\bar{\alpha}_{t-1}}\;\hat{\boldsymbol{\tau}}_0^{(t)}
    + \sqrt{1-\bar{\alpha}_{t-1}}\;\hat{\boldsymbol{\epsilon}}^{(t)} + \sigma_t \mathbf{z},
    \label{eq:ddpm_step}
\end{equation}$$ where $\hat{\boldsymbol{\epsilon}}^{(t)} = \epsilon_\theta(\boldsymbol{\tau}_t,t)$, $\mathbf{z}\sim\mathcal{N}(\mathbf{0},\mathbf{I})$, and $\sigma_t$ controls the injected sampling noise. Repeating [\[eq:ddpm_step\]](#eq:ddpm_step){reference-type="eqref" reference="eq:ddpm_step"} from $t=T$ down to $t=0$ yields a final denoised trajectory, which serves as the planner's output. Throughout the paper, we use $k$ to index rollout time, $t$ to index diffusion time, and $j$ to index agent index.

# Methodology

Our framework is guided by two motivating questions:

1.  *What* certifiable structure should be incorporated into a diffusion planner?

2.  *How* should the certifiable structure be integrated into the diffusion planner?

A key design choice underlying both questions is *what object we certify*. To address Q1, we identify three properties a certifiable structure must satisfy and introduce a mechanism for each: a capsule-distance control barrier function for *safety*, a path-tracking controller to map waypoints to dynamically feasible controls for *dynamic feasibility*, and a path-consistent correction for *minimal distributional deviation*. To address Q2, we integrate this structure into *every* denoising step by correcting the predicted clean trajectory estimate and re-injecting it into the diffusion process, enabling the planner to co-adapt to safety corrections rather than applying a one-shot post-hoc filter. We detail each component below.

## Safety: Capsule Distance Barrier Function

We achieve the first property, *safety*, using the control barrier function (CBF) framework (Section III-B), which enforces forward invariance of a collision-free set through inequality constraints on the time derivative of a barrier function $h$. A common choice defines $h$ using Euclidean distance between vehicle center points, but this inflates the effective collision boundary and can be overly conservative in tight geometries (e.g., intersections and narrow lanes). Instead, we represent each vehicle by its longitudinal axis (a line segment connecting the centers of the front and rear ends) and define the barrier using the *capsule distance*, i.e., the minimum distance between the two segments (Fig. [2](#fig:capsule_distance){reference-type="ref" reference="fig:capsule_distance"}).

:::: {#fig:capsule_distance .figure latex-placement="h"}
![](Ku2026PCDiffuser_figs/capsule_distance_diagram.png){width=".7\\columnwidth"}

::: caption
Capsule distance diagram. Each vehicle is represented by its longitudinal axis (line segment). Then the capsule distance is the minimum distance between the two segments minus $r_n + r_e$, the sum of half widths of the two vehicles.
:::
::::

Specifically, we represent each vehicle's longitudinal axis as a line segment connecting its rear-end center $P$ to its front-end center $Q$. Given two such segments parameterized by $S_1(s) = P_1 + s(Q_1 - P_1)$ and $S_2(r) = P_2 + r(Q_2 - P_2)$ for $s, r \in [0,1]$, the capsule distance is $$\begin{equation}
    d_{\text{cap}}(S_1, S_2) = \min_{s,\, r \,\in\, [0,1]} \| S_1(s) - S_2(r) \|.
    \label{eq:capsule_distance}
\end{equation}$$ We define the barrier function for ego and neighbor $j$ as $$\begin{equation}
    h^j(\mathbf{x}) = d_{\text{cap}}\!\left(S_{\text{ego}}(\mathbf{x}),\; S_j(\mathbf{x}^j)\right) - d_{\text{safe}},
    \label{eq:capsule_cbf}
\end{equation}$$ where $d_{\text{safe}} > 0$ is a safety margin.

::: {#prop:smooth .proposition}
**Proposition 1** (Smoothness of the Capsule Barrier). *For any ego state $\mathbf{x}=(x,y,\theta,\delta,v)$ and neighbor state $\mathbf{x}^j$ with $d_{\mathrm{cap}}(S_{\mathrm{ego}}(\mathbf{x}), S_j(\mathbf{x}^j))>0$, the capsule barrier $h^j(\mathbf{x}) = d_{\mathrm{cap}}(S_{\mathrm{ego}}(\mathbf{x}), S_j(\mathbf{x}^j)) - d_{\mathrm{safe}}$ is continuously differentiable with respect to $\mathbf{x}$ whenever the closest-point pair attaining $d_{\mathrm{cap}}$ is unique.*
:::

::: proof
*Proof.* Define the squared capsule distance $$\begin{align}
  D(\mathbf{x}) \;&=\; \min_{(s,r)\in[0,1]^2}
  \bigl\|S_1(s,\mathbf{x})-S_2(r,\mathbf{x}^j)\bigr\|^2 \nonumber \\
  &\triangleq\; \min_{(s,r)\in[0,1]^2} \phi(\mathbf{x},s,r).
\end{align}$$

For each fixed $(s,r)$, $\phi$ is $C^\infty$ in $\mathbf{x}$, since $S_1$ depends on $\mathbf{x}$ through $\cos\theta$ and $\sin\theta$. The constraint set $[0,1]^2$ is compact, so the minimum is attained. By Danskin's theorem [@danskin1966], when the minimizer $(s^*\!,r^*)$ is unique, $$\begin{align}
  \nabla_{\!\mathbf{x}} D &=\; \nabla_{\!\mathbf{x}} \phi(\mathbf{x},s^*\!,r^*) \\
  \;&=\; 2\bigl(S_1(s^*\!,\mathbf{x})-S_2(r^*)\bigr)^{\!\top}
    \frac{\partial S_1}{\partial \mathbf{x}}\!(s^*\!,r^*;\mathbf{x}).
\end{align}$$ Uniqueness holds whenever the segments are not parallel, which is the generic case. The chain rule gives $\nabla_{\!\mathbf{x}} d_{\mathrm{cap}} = \hat{n}^{\top}\! \frac{\partial S_1}{\partial\mathbf{x}}$, where $\hat{n}$ is the unit vector from the closest point on $S_2$ to the closest point on $S_1$. ◻
:::

This ensures that $\dot{h}^j$ is well-defined along the rollout dynamics, so we can enforce CBF-based safety constraints once we specify which control input we are allowed to adjust in Section [4.4](#sec:pc_cbf){reference-type="ref" reference="sec:pc_cbf"}.

## Dynamic Feasibility: Certifying the Executed Rollout

Diffusion planners produce waypoint trajectories, not the control inputs $(a,\delta)$ needed to certify safety under vehicle dynamics. A natural alternative is to generate action sequences directly [@mizuta2024cobl; @wang2025alpamayo] instead of target waypoints, but this can reintroduce compounding errors and training instability [@mizuta2024cobl], undermining the advantage of trajectory-level diffusion. We instead retain waypoint generation and introduce an explicit *interface* from waypoints to a dynamically feasible rollout.

Given the predicted clean trajectory $\hat{\boldsymbol{\tau}}_0^{(t)} = (\hat{\mathbf{x}}_1, \ldots, \hat{\mathbf{x}}_K)$, we track it sequentially with a linearized LQR controller [@rajamani2011vehicle] to produce a nominal control $\mathbf{u}_{\mathrm{nom},k} = (a_{\mathrm{nom},k},\, \delta_{\mathrm{nom},k})$ at each rollout step $k$. This nominal control respects the kinematic bicycle model [\[eq:bicycle\]](#eq:bicycle){reference-type="eqref" reference="eq:bicycle"} by construction and induces a dynamically feasible nominal rollout. Importantly, it also provides the control inputs that the CBF-QP [\[eq:cbf_qp\]](#eq:cbf_qp){reference-type="eqref" reference="eq:cbf_qp"} requires, unifying trajectory-space planning with action-space safety enforcement within a single framework.

## Minimal Distributional Deviation: Path-Consistent Corrections

While a generic safety filter may perturb both acceleration and steering, such corrections can alter the planned path geometry and push the vehicle away from the diffusion model's learned behavior. This can degrade driving quality and may introduce unsafe side effects (e.g., drifting toward adjacent lanes). We therefore require safety corrections to be *path-consistent*: they should primarily adjust *how fast* the vehicle traverses the planned path rather than *where* it goes.

We implement path-consistency by fixing steering to the tracked nominal value $\delta_k=\delta_{\mathrm{nom},k}$ and allowing the safety filter to modify only the longitudinal channel. With steering held fixed, the safety-corrected control is obtained by solving $$\begin{equation}
\begin{aligned}
    a_k^* = \arg\min_{a_k \in \mathcal{U}_a}\;& \|a_k - a_{\mathrm{nom},k}\|^2 \\
    \mathrm{s.t.}\quad& \nabla h^j(\mathbf{x}_k)^\top\!\bigl(f(\mathbf{x}_k) + g(\mathbf{x}_k)\,[a_k,\, \delta_{\mathrm{nom},k}]^\top\bigr) \\
    &\qquad \geq -\alpha\!\bigl(h^j(\mathbf{x}_k)\bigr), \quad \forall\, j \in \mathcal{R},
\end{aligned}
\label{eq:pc_cbf_qp}
\end{equation}$$ where $\mathcal{U}_a$ denotes admissible accelerations and $\mathcal{R}$ is the set of safety-critical agents (defined in Section [4.6](#sec:practical){reference-type="ref" reference="sec:practical"}). This restriction preserves the spatial geometry of the planned path by preventing lateral deviations, while still providing sufficient authority to avoid collisions through speed modulation. In the next subsection, we show how this constrained correction can be implemented efficiently using an equivalent velocity-level formulation.

## Path-Consistent Capsule CBF (PC-CBF) Safety Filter {#sec:pc_cbf}

We now compose the three components introduced above into a unified *PC-CBF safety filter*. PC-CBF uses the capsule barrier to enforce safety on the *executed* rollout induced by the bicycle dynamics, while preserving the planned path geometry by restricting safety corrections primarily to the longitudinal direction. Concretely, PC-CBF takes a planned waypoint trajectory as input and returns a corrected, dynamically feasible rollout by (i) tracking the path to obtain $\delta_{\mathrm{nom},k}$, (ii) projecting the nominal speed onto the CBF-admissible set, and (iii) rolling out the bicycle dynamics with the corrected longitudinal command.

Given a planned trajectory $\hat{\boldsymbol{\tau}}_0^{(t)}$ and predicted neighbor trajectories $\{\hat{\boldsymbol{\tau}}^{(j)}\}_{j \in \mathcal{R}}$, PC-CBF proceeds sequentially over rollout steps $k=1,\ldots,K$. At each rollout step, an LQR tracker produces a nominal control $(a_{\mathrm{nom},k},\delta_{\mathrm{nom},k})$ to follow the remaining waypoints under the bicycle model [\[eq:bicycle\]](#eq:bicycle){reference-type="eqref" reference="eq:bicycle"}. To preserve path geometry, we fix steering to $\delta_k=\delta_{\mathrm{nom},k}$ and enforce the capsule barrier condition against agents in $\mathcal{R}$ by modulating speed.

Under fixed steering, the capsule barrier time derivative along the bicycle dynamics [\[eq:bicycle\]](#eq:bicycle){reference-type="eqref" reference="eq:bicycle"} admits the velocity-linear form $$\begin{equation}
    \dot{h}^j
    = \underbrace{\frac{\partial h^j}{\partial x}\cos\theta
    + \frac{\partial h^j}{\partial y}\sin\theta
    + \frac{\partial h^j}{\partial \theta}\frac{\tan\delta_{\mathrm{nom},k}}{L}}_{\displaystyle \triangleq\; \frac{\partial h^j}{\partial v}}
    \cdot v,
    \label{eq:hdot_v}
\end{equation}$$ which yields a velocity-level CBF constraint $\dot{h}^j \geq -\alpha(h^j)$.

::: {#def:vel_cbf .definition}
**Definition 1** (Fixed-Steering CBF). *Fix $\delta=\delta_{\mathrm{nom},k}$ and consider the induced rollout dynamics obtained from [\[eq:bicycle\]](#eq:bicycle){reference-type="eqref" reference="eq:bicycle"} with steering held fixed, where the effective decision variable is the speed $v\ge 0$. Define the safe set $$\begin{equation}
\mathcal{C}^j \;=\; \{\mathbf{x} \mid h^j(\mathbf{x}) \ge 0\}.
\end{equation}$$ We say that the capsule barrier $h^j$ is a *control barrier function* (CBF) for the induced fixed-steering rollout dynamics if $h^j$ is continuously differentiable on $\mathcal{C}^j$ and, for all $\mathbf{x}\in\mathcal{C}^j$, the admissible set $$\begin{equation}
K_{\mathrm{cbf}}(\mathbf{x})
=
\Bigl\{v\geq 0 \ \Bigm|\  \dot{h}^j(\mathbf{x}) \ge -\alpha\!\bigl(h^j(\mathbf{x})\bigr)\Bigr\}
\end{equation}$$ is nonempty.*
:::

::: {#thm:cbf .theorem}
**Theorem 1** (Feasibility of Velocity-Level Capsule CBF). *Under fixed steering $\delta=\delta_{\mathrm{nom},k}$, for every $\mathbf{x}$ with $h^j(\mathbf{x})\geq 0$, the set $$\begin{equation}
K_{\mathrm{cbf}}(\mathbf{x})
=
\Bigl\{v\geq 0 \ \Bigm|\  \frac{\partial h^j}{\partial v}(\mathbf{x})\,v
\geq -\alpha\!\bigl(h^j(\mathbf{x})\bigr)\Bigr\}
\end{equation}$$ is nonempty.*
:::

::: proof
*Proof.* By Proposition [1](#prop:smooth){reference-type="ref" reference="prop:smooth"}, $h^j$ is continuously differentiable on the domain where the closest-point pair is unique, hence $\dot{h}^j$ is well-defined. Under fixed steering, $\dot{h}^j = (\partial h^j/\partial v)\,v$ via [\[eq:hdot_v\]](#eq:hdot_v){reference-type="eqref" reference="eq:hdot_v"}. Two cases arise: *(i)* If $\partial h^j/\partial v \geq 0$, any $v\geq 0$ satisfies the constraint. *(ii)* If $\partial h^j/\partial v < 0$, choosing $v=0$ yields $\dot{h}^j=0\geq -\alpha(h^j)$ since $\alpha(h^j)\geq 0$ for $h^j\geq 0$. Thus $K_{\mathrm{cbf}}(\mathbf{x})$ is nonempty. ◻
:::

Proposition [1](#prop:smooth){reference-type="ref" reference="prop:smooth"} and Theorem [1](#thm:cbf){reference-type="ref" reference="thm:cbf"} together establish that the capsule barrier $h^j$ in [\[eq:capsule_cbf\]](#eq:capsule_cbf){reference-type="eqref" reference="eq:capsule_cbf"} is a CBF for the induced fixed-steering rollout dynamics in the sense of Definition [1](#def:vel_cbf){reference-type="ref" reference="def:vel_cbf"}.

::: {#cor:invariance .corollary}
**Corollary 1** (Forward Invariance). *If $v(\mathbf{x})$ is selected such that $v(\mathbf{x}) \in K_{\mathrm{cbf}}(\mathbf{x})$ for all $\mathbf{x}\in\mathcal{C}^j$ (e.g., by solving [\[eq:v_cbf\]](#eq:v_cbf){reference-type="eqref" reference="eq:v_cbf"}), then $\mathcal{C}^j$ is forward invariant under the resulting closed-loop rollout dynamics (Section III-B).*
:::

We therefore compute the minimally modified safe speed by solving $$\begin{equation}
\begin{aligned}
    v_k^* = \arg\min_{v_k}\;& \|v_k - v_{\mathrm{nom},k}\|^2 \\
    \mathrm{s.t.}\quad& \frac{\partial h^j}{\partial v}\, v_k \geq -\alpha(h^j),\quad \forall\, j \in \mathcal{R},
\end{aligned}
    \label{eq:v_cbf}
\end{equation}$$ and recover the corresponding acceleration as $a_k^* = (v_k^* - v_k)/\Delta t$. This velocity-level implementation avoids a higher-order CBF (HOCBF) [@xiao2021hocbf], which would require differentiating $\dot{h}^j$ again and introducing additional class-$\mathcal{K}$ hyperparameters, often resulting in more sensitive behavior.

Finally, we propagate the ego state forward using the bicycle model [\[eq:bicycle\]](#eq:bicycle){reference-type="eqref" reference="eq:bicycle"} with $(a_k^*,\delta_{\mathrm{nom},k})$ and repeat for $k=1,\ldots,K$. The resulting rollout $\hat{\boldsymbol{\tau}}_0^{*} = (\hat{\mathbf{x}}_1^*, \ldots, \hat{\mathbf{x}}_K^*)$ is (i) dynamically feasible by construction, (ii) safe with respect to all agents in $\mathcal{R}$ by enforcing the CBF constraint at every rollout step, and (iii) path-consistent since the spatial path is tracked through $\delta_{\mathrm{nom},k}$ while safety is achieved primarily through speed modulation. The full PC-CBF procedure is summarized in Algorithm [\[alg:pc_cbf\]](#alg:pc_cbf){reference-type="ref" reference="alg:pc_cbf"}.

::: algorithm
$\hat{\mathbf{x}}_1^* \leftarrow \hat{\mathbf{x}}_1$ $\hat{\boldsymbol{\tau}}_0^{*} = (\hat{\mathbf{x}}_1^*,\, \ldots,\, \hat{\mathbf{x}}_K^*)$
:::

## Integrating Certifiable Structure into Diffusion Planning

Having established *what* certifiable structure to incorporate (Q1), we now address *how* to integrate it into the diffusion planner (Q2). A natural baseline is to apply PC-CBF as a post-hoc filter on the final denoised trajectory $\boldsymbol{\tau}_0$. However, such a one-shot correction is oblivious to the diffusion model's internal generation: the planner has no opportunity to adapt, and the corrected output may be unlikely under the learned distribution.

Our key insight is to enforce the certifiable structure *within* the denoising process by operating on the predicted clean trajectory estimate. At each denoising step $t$, the diffusion model produces a noisy trajectory $\boldsymbol{\tau}_t$, from which we extract the predicted clean trajectory $\hat{\boldsymbol{\tau}}_0^{(t)}$ via [\[eq:clean_estimate\]](#eq:clean_estimate){reference-type="eqref" reference="eq:clean_estimate"}. This clean estimate is the model's current best estimate of the final plan and is therefore a meaningful object on which to enforce rollout-time safety, unlike the noisy state $\boldsymbol{\tau}_t$ itself.

We apply PC-CBF to $\hat{\boldsymbol{\tau}}_0^{(t)}$ to obtain the corrected estimate $\hat{\boldsymbol{\tau}}_0^{*(t)}$, and then re-noise it back into the diffusion process: $$\begin{equation}
    \boldsymbol{\tau}_{t-1} = \sqrt{\bar{\alpha}_{t-1}}\;\hat{\boldsymbol{\tau}}_0^{*(t)} + \sqrt{1 - \bar{\alpha}_{t-1}}\;\hat{\boldsymbol{\epsilon}}^{(t)} + \sigma_t \mathbf{z},
    \label{eq:corrected_denoise}
\end{equation}$$ where $\hat{\boldsymbol{\epsilon}}^{(t)} = \bigl(\boldsymbol{\tau}_t - \sqrt{\bar{\alpha}_t}\,\hat{\boldsymbol{\tau}}_0^{*(t)}\bigr) / \sqrt{1 - \bar{\alpha}_t}$ is the re-estimated noise consistent with the corrected clean estimate and $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$. Subsequent denoising steps then operate on a trajectory that already accounts for safety, enabling **co-adaptation**: the diffusion planner refines the corrected estimate back toward its learned distribution while preserving the certifiable structure. As $t \to 0$, $\hat{\boldsymbol{\tau}}_0^{(t)}$ sharpens and the required safety corrections diminish, converging to a trajectory that is both safe and consistent with the learned behavior.

## PC-Diffuser and Practical Considerations {#sec:practical}

Enforcing the CBF constraint against all $N$ neighboring agents is often unnecessarily conservative and computationally expensive, since most nearby agents pose no collision risk (e.g., vehicles traveling in the opposite direction on separated lanes or parked vehicles on the side). Instead of relying on hand-crafted geometric heuristics, we leverage the diffusion planner's predicted neighbor trajectories to focus certification on a smaller set of safety-critical agents.

Concretely, at each denoising step $t$ we evaluate the minimum barrier value between the ego's predicted trajectory and each neighbor $j$: $$\begin{equation}
    h^j_{\min} = \min_{k \in \{1,\ldots,K\}} h^j\!\left(\hat{\mathbf{x}}_k,\;\hat{\mathbf{x}}_k^j\right).
\end{equation}$$ Agent $j$ is added to the safety-critical set $\mathcal{R}$ whenever $h^j_{\min} \leq \eta$ for a user-specified threshold $\eta \geq 0$. The set $\mathcal{R}$ is accumulated across denoising steps: once an agent is flagged as critical at step $t$, it remains in $\mathcal{R}$ for all subsequent steps. This monotonic accumulation prevents oscillatory inclusion and exclusion as $\hat{\boldsymbol{\tau}}_0^{(t)}$ sharpens during denoising.

Our full framework, summarized in Algorithm [\[alg:pc_cbf_denoise\]](#alg:pc_cbf_denoise){reference-type="ref" reference="alg:pc_cbf_denoise"}, proceeds as follows at each denoising step $t$:

1.  **Predict.** Extract the clean trajectory estimate $\hat{\boldsymbol{\tau}}_0^{(t)}$ from the noisy state via [\[eq:clean_estimate\]](#eq:clean_estimate){reference-type="eqref" reference="eq:clean_estimate"}.

2.  **Filter.** Update the safety-critical agent set $\mathcal{R}$ based on predicted proximity.

3.  **Correct.** Apply PC-CBF (Section [4.4](#sec:pc_cbf){reference-type="ref" reference="sec:pc_cbf"}) to obtain the safe, dynamically feasible, path-consistent trajectory $\hat{\boldsymbol{\tau}}_0^{*(t)}$.

4.  **Re-noise.** Inject the corrected estimate back into the diffusion process via [\[eq:corrected_denoise\]](#eq:corrected_denoise){reference-type="eqref" reference="eq:corrected_denoise"}.

After all denoising steps complete, the first action of $\boldsymbol{\tau}_0^*$ is executed and the planning loop resets.

::: algorithm
$\mathcal{R} \leftarrow \emptyset$ $\boldsymbol{\tau}_0^*$
:::

# Evaluation

We aim to validate two hypotheses: (H1: the structure to enforce) jointly enforcing safety, dynamic feasibility, and path-consistency reduces collisions while maintaining driving quality, and (H2: the way to integrate) integrating corrections iteratively within denoising, instead of just applying once in a post-hoc manner, keeps the corrected trajectory closer to the learned distribution, yielding safer long-horizon behavior. To evaluate these claims, we test on the nuPlan closed-loop benchmark using DiffusionPlanner [@zheng2025diffusionplanner] as our base model, one of the strongest performing learning-based model that jointly forecasts neighbors' trajectory which we can leverage to construct our certifiable structure. For baselines, we compare against popular safety augmentation strategies: Classifier Guidance [@zheng2025diffusionplanner], diffusion-time barrier constraints [@xiao2023safediffuser], and optimization-based safety filters [@zeng2021mpccbf], which are general safety augmentation methods that do not leverage nuPlan's neighbor policy (IDM[@treiber2000idm]) as a prior or simulate multiple proposals on-the-fly to better reflect real-life performance.

## Dataset and Metrics

The nuPlan benchmark [@caesar2021nuplan] provides approximately 1,300 hours of expert driving data collected across four cities (Las Vegas, Boston, Pittsburgh, Singapore) with auto-labeled object tracks and traffic light states. Our evaluation uses nuPlan's closed-loop reactive simulation, which represents logged traffic with birds-eye-view (BEV) representation and resimulates agent behavior using the Intelligent Driver Model (IDM) [@treiber2000idm] for longitudinal car-following.

We evaluate on two standard splits: *Val14*, which contains up to 100 scenarios per type across 14 scenario types and *Test14-hard*, a curated 280-scenario subset in which rule-defined planners struggle.

To further isolate safety-critical performance, we extract *all* 68 scenarios from Val14 in which the base model DiffusionPlanner [@zheng2025diffusionplanner] collides (100% collision rate by construction), representing roughly 7% of Val14 and constituting its most challenging subset. We refer to this subset as the *all-collision challenge set*.

We report two metrics: the *collision rate* and nuPlan's built-in *composite score* [@caesar2021nuplan]. $$\begin{equation}
    s = \prod_{i \in \mathcal{M}} m_i \;\cdot\; \sum_{j \in \mathcal{A}} w_j \, a_j,
    \label{eq:nuplan_score}
\end{equation}$$ where $m_i \in \{0, 0.5, 1\}$ are hard multiplier metrics (at-fault collision, drivable area compliance, progress, driving direction) that zero or halve the score upon violation, and $a_j$ are weighted soft metrics including time-to-collision maintenance ($w=5$), route progress ($w=5$), speed limit compliance ($w=4$), and comfort ($w=2$).

## Quantitative Analysis Against Baselines

We compare PC-Diffuser against three families of safety augmentation methods, all applied to the same base planner: (i) Classifier Guidance, (ii) SafeDiffuser, and (iii) MPC-CBF. Classifier Guidance [@zheng2025diffusionplanner] steers the denoising process via gradients of a hand-crafted energy-based classifier aiming to increase the distance from vehicle in collision. SafeDiffuser [@xiao2023safediffuser] incorporates barrier constraints on the denoising process with three barrier-value scheduling variants (Robust-Safe Diffuser, Relaxed-Safe Diffuser, Time-Varying-Safe Diffuser) aiming to mitigate a *local trap problem* where the denoising process cannot progress without violating the CBF constraint. Lastly, MPC-CBF [@zeng2021mpccbf] embeds CBF constraints into the receding-horizon optimization, aiming to satisfy the CBF constraint throughout the receding horizon. Compared to these baseline methods, PC-Diffuser reduces the collision rate from 100% to 10.29% on the all-collision challenge set compared to 74--89% for all baselines, while simultaneously achieving the highest composite score (0.59 vs. $\leq$`<!-- -->`{=html}0.15).

To verify that these safety improvements do not come at the cost of degraded driving performance, we additionally evaluate on the full Val14 and Test14-hard splits. Despite the additional constraints from our certifiable structure, PC-Diffuser instead improves the base model's composite score from *0.83* to *0.88* on Val14 and from *0.69* to *0.78* on Test14-hard, confirming that the certifiable structure enhances safety without sacrificing driving quality.

The significant improvement in both collision rate and composite score on the all-collision challenge set (Table [\[tab:collision_subset\]](#tab:collision_subset){reference-type="ref" reference="tab:collision_subset"}) while preserving strong driving performance on full data splits demonstrates the effectiveness of our certifiable structure and PC-diffuser framework supporting H1 and H2.

:::: {#fig:qualitative .figure latex-placement="ht"}
![Diffuser (vanilla)](Ku2026PCDiffuser_figs/vanilla_plan.png){#fig:qual_vanilla width="\\textwidth"}

![Classifier Guidance](Ku2026PCDiffuser_figs/classifier_guidance_plan.png){#fig:qual_classifier width="\\textwidth"}

![Relaxed-Safe Diffuser](Ku2026PCDiffuser_figs/SafeDiffuser_plan.png){#fig:qual_safediffuser width="\\textwidth"}

![MPC-CBF](Ku2026PCDiffuser_figs/mpc_cbf_plan.png){#fig:qual_mpc width="\\textwidth"}

![PC-Diffuser (ours)](Ku2026PCDiffuser_figs/ours_plan.png){#fig:qual_ours width="\\textwidth"}

::: caption
Qualitative comparison on a collision critical intersection scenario. The ego vehicle (orange box) approaches from the left. Planned trajectory for ego is depicted in bright gradient while neighbors' is depicted in blue-green gradient. The first Collision in the future timeframe is marked with a red x. The vanilla Diffuser (a) and Classifier Guidance (b) collide with an oncoming traffic. SafeDiffuser (c) produces a safe but dynamically infeasible trajectory. MPC-CBF (d) produces safe and feasible trajectory but deviates into the on-coming lane. PC-Diffuser (e) yields to the on-coming traffics before safely making a left turn while preserving a lane-consistent trajectory. More qualitative comparisons are available in the accompanying video.
:::
::::

## Qualitative Analysis Against Baselines

Figure [8](#fig:qualitative){reference-type="ref" reference="fig:qualitative"} provides a qualitative comparison on a safety-critical intersection scenario where the ego vehicle has to make a left-turn to a congested lane while avoiding two oncoming vehicles. In this scenario, due to the oncoming traffic and high congestion, the ideal maneuver is to yield and slowly make a left-turn when available.

As shown in Fig. [8](#fig:qualitative){reference-type="ref" reference="fig:qualitative"}(a), vanilla DiffusionPlanner [@zheng2025diffusionplanner], trained to predict the most likely trajectory based on its training data, produces a natural and smooth left-turn trajectory. However, without a safety certificate, it fails to avoid a collision with the latter on-coming vehicle. Similarly, Classifier Guidance [@zheng2025diffusionplanner] (via distance energy-based classifier), as shown in Fig. [8](#fig:qualitative){reference-type="ref" reference="fig:qualitative"}(b), also produces a smooth, high-quality trajectory but without the safety certificate, it also fails to avoid collision. On the other hand, SafeDiffuser, as shown in Fig. [8](#fig:qualitative){reference-type="ref" reference="fig:qualitative"}(c), provides a safety certificate but without the dynamic feasibility, it produces a physical meaningless trajectory as the denoising process was interfered by CBF constraint on the diffusion time. Relaxed-Safe Diffuser variant was incorporated to tackle this problem, however, it is not foolproof and still resulted in physically infeasible trajectory. MPC-CBF, as shown in Fig. [8](#fig:qualitative){reference-type="ref" reference="fig:qualitative"}(d), provides both safety certificate and dynamic feasibility through CBF and model dynamics constraints. Yet, as it is geometrically unconstrained, it ignores the intended behavior of the diffusion planner and swerves into the on-coming lane which is highly undesirable. In contrast to these baseline methods, PC-Diffuser, as shown in Fig. [8](#fig:qualitative){reference-type="ref" reference="fig:qualitative"}(e), simultaneously satisfies safety, dynamic feasibility, and path-consistency, and yields to the oncoming traffic before initializing a left-turn while remaining lane-consistent.

The qualitative failure analysis of the baseline methods and the safe maneuver of PC-Diffuser at the safety-critical intersection demonstrates the importance of jointly enforcing safety, dynamic feasibility, and path-consistency, supporting H1.

## Ablation Study

To understand the contribution of each component of PC-Diffuser, we systematically remove one component at a time and re-evaluate on the all-collision challenge set (Table [\[tab:ablation\]](#tab:ablation){reference-type="ref" reference="tab:ablation"}).

:::: {#fig:slack_counts .figure latex-placement="!t"}
![](Ku2026PCDiffuser_figs/slack_activation_comparison.png){width="\\columnwidth"}

::: caption
Average slack activation rate (%) in the CBF-QP across denoising steps. Iterative PC-CBF shows monotonically decreasing corrections as denoising progresses, indicating convergence to a safe trajectory. Single-step PC-CBF (dashed line) applies a larger correction at the final step with higher slack activation rate due to the absence of iterative refinement.
:::
::::

**Iterative safeguard.** Applying PC-CBF only at the final denoising step, rather than throughout the process, increases the collision rate by ${\sim}6\%$ and lowers the composite score by 0.12. To understand why, we examine how often the slack variables in the CBF-QP are activated across denoising steps (Figure [9](#fig:slack_counts){reference-type="ref" reference="fig:slack_counts"}). With iterative correction, slack activation decreases monotonically as denoising progresses, producing trajectories that increasingly satisfy safety constraints on their own. By contrast, single-step correction sees no such convergence and must apply a larger one-shot adjustment at the end. The benefit compounds over simulation time: the gap between slack activation during the first denoising step and post-hoc correction is  2.5% (Figure [9](#fig:slack_counts){reference-type="ref" reference="fig:slack_counts"}) while when we only consider slack violation rate of the first simulation step, the gap is much smaller at 0.65%. An improvement in the slack activation rate over long-term indicates that iterative correction steers the diffusion model toward trajectories that yields safer long-horizon by jointly searching for a safe trajectory together with diffusion planner, supporting H2.

**Selective filtering.** Without filtering out benign agents degrades the composite score by 0.12 as expected as our capsule CBF constraints can hinder the vehicle progress by promoting unnecessarily conservative behavior (e.g. vehicles from on-coming lane). Interestingly removing the filtering provides a modest improvement on collision rate ($+1.5\%$). This is mainly due to PC-diffuser occasionally finding a safe-set which without the selective filtering would've been considered unsafe due to overly conservative constraint.

Among all components, **Dynamic feasibility** has the largest impact. To isolate this component while maintaining the rest of PC-Diffuser, we replace the LQR path-following controller with an arc-reparameterization that still satisfies CBF constraints and path-consistency. Removing dynamic feasibility raises the collision rate by ${\sim}11\%$ and lowers the composite score by 0.29, indicating that kinematic grounding is crucial for both safety and driving quality, which further supports H1. We note that despite the lack of dynamic feasibility, the arc-reparameterization method outperforms all baseline methods (Table [\[tab:collision_subset\]](#tab:collision_subset){reference-type="ref" reference="tab:collision_subset"}) as path-consistency still respects the learned dynamics from the diffusion model, mitigating much of the adverse effects of kinematic infeasibility.

# Conclusion & Limitations

We presented PC-Diffuser, a safety augmentation framework that integrates a certifiable structure into diffusion-based planning through path-consistent barrier functions. We introduced a novel capsule distance CBF safety filter, a framework to enforce dynamic feasibility on trajectory-space diffusion models, a way to reduce deviation from learned distribution via geometric consistency, and an innovative way to integrate these properties during the denoising process (generation) rather than as a post-hoc correction.

Despite these efforts, our approach has several limitations. First, although the iterative integration of PC-CBF allows for neighbors' trajectory forecast to adapt according to PC-Diffuser's correction on ego's plan, our framework still remains reactive and is limited in anticipating reactions from human drivers, which could potentially be improved via active uncertainty mitigation methods [@yiwei2026icra].

Second, our evaluation relies on nuPlan's IDM-based reactive simulation, which is less ideal and resulted in $\sim$`<!-- -->`{=html}10% collision rate with PC-Diffuser on the all-collision challenge set, mostly during the intersections where many vehicles following IDM policy will drive from various directions, trapping the ego vehicle and causing a collision. A more suitable benchmark with a higher-fidelity and naturalistic neighbor vehicle policy remains a future work.

[^1]: $^{1}$Eugene Ku and Yiwei Lyu are with Texas A&M University, College Station, TX 77843, USA. `{yjean234, yiweilyu}@tamu.edu`
