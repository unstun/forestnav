---
citation_key: Liu2026GoalConditioned
arxiv_id: 2604.02821
arxiv_url: https://arxiv.org/abs/2604.02821
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:53:03Z
origin: ai+web
reviewed: false
---

# Introduction

Motion planning in environments with complex geometric constraints -- arising from obstacles, workspace boundaries, and configuration space structure -- remains a fundamental challenge in robotics.

Classical sampling-based methods such as probabilistic roadmaps (PRM) [@Kavraki1996ProbabilisticRF] and rapidly-exploring random trees (RRT) [@LaValle1998RapidlyexploringRT] are simple to implement and widely used, but suffer from certain limitations. In particular, they are inherently finite in their representation: RRTs are generated from a fixed start position (single-query) while PRMs can handle a finitely-many sampled start and end positions (multi-query) [@lavalle2006planning]. They do not define a smooth feedback policy from all possible start and end positions (all-pairs). Furthermore, they are inherently model-based and difficult to adapt to learning-based methodologies such as learning from demonstration (LfD) [@ravichandar2020recent].

An emerging paradigm represents the desired motion via a continuous dynamical system whose solutions serve directly as executable trajectories, see e.g. [@ab2011gmm; @billardLearningAdaptiveReactive2022; @pmlr-v162-zhi22a; @jinLearningFlexibleNeural2023c; @guptaCompactOneshotModelling2026]. This approach has the advantage that it effectively defines a feedback policy, so it is robust, adaptable, and real-time implementable, and compatible with learning frameworks such as LfD when the dynamical models are parameterized, e.g. neural ordinary differential equations (neural ODEs).

The dynamical systems approach to robot motion generation can be traced back to classical approaches such as potential fields [@Khatib1985Real] which combine attractive and repulsive forces but suffer can from local minima [@Tilove1989localminimum] and instability in narrow passages [@Koren1991PotentialFM]. Mitigating these issues remains an ongoing research activity [@Huber2024avoidance]. Navigation function, introduced by Koditschek and Rimon [@koditschek1990robot], provide a theoretical foundation that is closely related to the concept of a Lyapunov function. They provide a construction of for simplified "sphere worlds", and showed how they can in principle be adapted to more complex but topologically-equivalent spaces via diffeomorphisms, however at the time constructive methods were lacking.

:::: {#fig:boundary_mapping .figure latex-placement="!t"}
![](Liu2026GoalConditioned_figs/corridor2ball.png){width="\\linewidth"}

::: caption
Our approach is based on learning a bi-Lipschitz diffeomorphism $g$ that maps a geometrically complex safe set $\mathcal{X}_{\text{safe}}$ in the $\mathcal{X}$-space (left) onto the unit ball in the $\mathcal{Z}$-space (right). Then simple straight-line point-to-point motions in $\mathcal{Z}$-space can be smoothly pulled back to $\mathcal{X}$ space, defining a goal-conditioned neural ODE which guarantees stability and safety and takes the form of a natural gradient flow.
:::
::::

The central challenge therefore is designing (or learning) a dynamical system with the required properties: it should be sufficiently smooth, flexible enough to reproduce the desired task behavior, have some (preferably global) stability properties, and provide the ability to avoid obstacles or other unsafe regions.

Lyapunov stability theory provides a principled framework for designing stable dynamical systems. The classical work of Wilson [@wilson1967structure], combined with the resolution of the generalized Poincaré Conjecture [@anderson2004geometrization] established that all Lyapunov functions have level sets homeomorphic to spheres, and diffeomorphic for all dimensions other than five. Such results are closely related to the problem of global linearization of nonlinear systems, see [@kvalheimGlobalLinearizationHyperbolicity2025] and references therein. This naturally suggests parameterizing Lyapunov functions as the composition of a diffeomorphism and a simple quadratic [@wang2024monotone; @Cheng2024LearningSA].

Early work ensuring stability in the dynamical systems approach to motion planning relied on quadratic Lyapunov functions, limiting flexibility [@ab2011gmm]. Increasing flexibility via state diffeomorphisms has been explored from several directions. To our knowledge it was first applied the context of stable nonlinear system identification: [@tobenkin2010convex; @tobenkin2017convex] learned contracting dynamics via polynomial diffeomorphisms of the state space, enforced via sum-of-squares programming. The idea was explicitly applied to robot motion planning in [@NEUMANN20151], by integrating diffeomorphisms with the method of [@ab2011gmm], however the class of diffeomorphisms was quite limited. A more flexible class of diffeomorphisms based on Gaussian radial basis function kernels was investigated in [@PERRIN201651].

More recently, neural network methods based on normalizing flows have been developed [@rana2020euclideanizing] and extended to limit cycles [@pmlr-v162-zhi22a] and adaptation to environmental changes [@pmlr-v168-zhi22a]. The present paper builds most directly on[@Cheng2024LearningSA], which proposed a class of exponentially stable neural dynamics constructed using *bi-Lipschitz* neural networks [@wang2024monotone]. This model class provides not only certified stability but explicit bounds on the rate of stability and potential overshoot, as well as fast splitting-based algorithms for inversion.

Robotics includes many potentially safety-critical or mission-critical applications, and certifying safety of learning-based methods is a major area of current research (see, e.g., the reviews [@brunke2022safe; @manchester2026neural] and references therein). In the context of the dynamical systems approach to motion planning, a recent work [@nawaz2024learning] proposed combining learned neural ODEs with control Lyapunov functions (CLFs) and control barrier functions (CBFs). On the other hand, it is known that existence of a CLF and a CBF separately does not guarantee existence of a compatible CLF-CBF pair [@mestres2025converse], which complicates the learning setup.

In the aforementioned approaches to ensuring stability and safety in dynamical systems LfD, it is generally assumed that the goal-state of the motion is fixed before the learning process, i.e. it is a single-query setup. Changes to the goal state can sometimes be incorporated, but would generally require retraining and/or fresh certification of stability and safety of the resulting motion.

**Contributions.** In this paper, we propose a class of goal-conditioned neural dynamical systems that incorporate built-in guarantees of global exponential stability and safety (safe set forward invariance), for *all* combinations of initial state and goal state within the safe set. The models are compatible with learning-based paradigms for motion planning, such as learning from demonstration. The main contributions are: (1) a systematic approach for constructing goal-conditioned dynamical systems via diffeomorphisms; (2) theoretical results establishing guarantees of safety and exponential stability regardless of goal location; (3) a tractable machine learning formulation for a diffeomorphism; (4) empirical validation confirming the effectiveness of the proposed approach.

**Notation.** A mapping $f:\mathbb{R}^n\rightarrow\mathbb{R}^m$ is said to be of class $C^k$ if it has up to $k$th continuous derivatives. A continuously differentiable mapping $g:\mathbb{R}^n\rightarrow\mathbb{R}^n$ is called a diffeomorphism if it is a bijection and its inverse $g^{-1}$ is also differentiable. Given a $C^1$ function $V:\mathbb{R}^n \rightarrow \mathbb{R}$, its gradient is taken as $\nabla V:=\bigl(\partial V/\partial x\bigr)^\top$. We denote unit ball as $\mathcal{B}^n=\{x\in \mathbb{R}^n:|x|\leq 1\}$, where $|\cdot|$ is the Euclidean norm. Given a set $X\subset\mathbb{R}^n$, we use $\partial X$ and $\mathrm{Int}(X)$ to denote its boundary and interior, respectively.

# Preliminaries and Problem Formulation {#sec:problem setup}

## The Dynamic Approach for Motion Planning

The basic motion planning problem in robotics usually considers the robot dynamics to be *fully-actuated* and *velocity-controlled*, i.e. $$\begin{equation}
\label{eq:robot-dyn}
    \dot{x}(t)=u(t).
\end{equation}$$ where $x(t)\in \mathcal{X}\subseteq \mathbb{R}^n$ is the state, e.g., $x(t)$ could be the position of a robot arm's end effector.

While the dynamics are very simple, the difficulty comes from two sources. Firstly, the requirement for collision avoidance and other safety constraints, which can be represented as $$\begin{equation}
 % \label{eq:robot-dyn}
   x(t)\in \mathcal{X}_{\text{safe}}\quad \forall\, t\geq 0
\end{equation}$$ where $\mathcal{X}_{\text{safe}}\subset \mathcal{X}$ is a safe set that may have complex geometry. We denote by $\mathcal{X}_{\text{unsafe}}$ its complement $\mathcal{X}_{\text{unsafe}}= \mathcal{X}\setminus \mathcal{X}_{\text{safe}}$, i.e., the set of unsafe states.

Secondly, the motion task may be complex and only partially specified. While it usually includes motion towards a goal position $x_\star$, among the infinite variety of possible motions approach the same goal, the desirable ones may be specified only indirectly via a limited set of demonstration data. The robot motion should not only accurately reproduce the training demonstrations, but also generalize to new conditions and react gracefully to disturbances. This generally requires some form of *smoothness* and *stability* of the dynamics.

## Problem Statement

In this work, we focus on a learning-based *all-pairs* motion planning problem, where both $x_0$ and $x_\star$ are allowed to be arbitrary points in $\mathcal{X}_{\text{safe}}$. Specifically, we aim to learn a smooth goal-conditioned dynamical system of the form $$\begin{equation}
 \label{eq:system}
    \dot{x}(t) = f(x(t), x_\star),\quad x(0)=x_0,
\end{equation}$$ where $f(x_\star,x_\star)=0$ for all $x_\star\in \mathcal{X}_{\text{safe}}$, i.e. the goal state is an equilibrium.

To formalize the desired properties of [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"}, we first recall the following standard definition:

::: {#def:forward_inv .defn}
*Definition 1*. For a given dynamical system with state $x(t)$, a set $\mathcal S$ is called *forward invariant* if $x(0)\in \mathcal S$ implies $x(t)\in\mathcal S$ for all $t\geq 0$.
:::

We use the following notions of safety and stability for a goal-conditioned system:

::: {#def:safe .defn}
*Definition 2*. System [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} is called *safe* w.r.t. the set $\mathcal{X}_{\text{safe}}$ if for any goal state $x_\star\in \mathcal{X}_{\text{safe}}$, the set $\mathcal{X}_{\text{safe}}$ is forward invariant.
:::

::: {#def:exp-convergence .defn}
*Definition 3* ([@hines2011equilibrium]). System [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} is globally *equilibrium-independent exponentially stable* if for any initial state $x_0\in\mathcal{X}$ and any equilibrium $x_\star\in \mathcal{X}$, the solution $x(t)$ satisfies $$\begin{equation*}
        |x(t) - x_\star| \leq \kappa e^{-\lambda t} |x_0 - x_\star|, \quad \forall t \geq 0,
\end{equation*}$$ for some $\kappa\geq 1$ and $\lambda>0$.
:::

Here we are interested in the following problem.

::: prob
*Problem 1*. Given training data characterising the safe and unsafe sets: $$\begin{equation}
\label{eq:datasets}
    \begin{split}
        \mathcal{D}_{\text{safe}}&=\{x_i: x_i\in \mathcal{X}_{\text{safe}}\}_{1\leq i\leq M}, \\
        \mathcal{D}_{\text{unsafe}}&=\{x_j: x_j\in \mathcal{X}_{\text{unsafe}}\}_{1\leq j\leq N},
    \end{split}
\end{equation}$$ and additionally some task-relevant data for the system's desired behaviour *inside* the safe set, e.g. demonstration data: $$\begin{equation}
    \mathcal{D}_{\text{demo}}=\{(x_{k}, x_{k,\star}, \dot{x}_{k}): x_k,x_{k,\star}\in \mathcal{X}_{\text{safe}}\}_{1\leq k\leq K},
\end{equation}$$ the goal is to learn a smooth dynamical system of the form [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} with the following properties:

- The system [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} is safe w.r.t. the set $\mathcal{X}_{\text{safe}}$.

- The system [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} has a known bound on velocity on the safe set: $|f(x,x_\star)|\le B$ for all $x,x_\star\in\mathcal{X}_{\text{safe}}$.

- The system [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} is globally equilibrium-independent exponentially stable.

- The system [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} effectively mimics the demonstration data $\mathcal{D}_{\text{demo}}$ inside $\mathcal{X}_{\text{safe}}$, or otherwise meets the training objectives, and generalizes smoothly.
:::

We note that the first three objectives can be considered hard constraints, with the caveat that the first requirement depends on the extent that the data sets $\mathcal{D}_{\text{safe}}$ and $\mathcal{D}_{\text{unsafe}}$ accurately represent the true sets $\mathcal{X}_{\text{safe}}, \mathcal{X}_{\text{unsafe}}$.

The fourth requirement is somewhat loose, but will generally be supported by having a sufficiently *flexible* class of models to meet the training objective while ensuring satisfaction of the first three requirements, as well as some possibility to tune the smoothness of the model.

## Preliminaries on Bi-Lipschitz Diffeomorphisms

To formulate our approach, we first require some technical machinery. We extensively utilise bi-Lipschitz diffeomorphisms:

::: {#def:bi-lip .defn}
*Definition 4*. The diffeomorphism $g:\mathbb{R}^n\to\mathbb{R}^n$ is said to be *bi-Lipschitz* if for all $x_1, x_2\in \mathbb{R}^n$, we have $$\begin{equation}
    \label{eq:bi-lipschitz}
        \mu|x_1-x_2|\leq |g(x_1)-g(x_2)|\leq \nu |x_1-x_2|
\end{equation}$$ for some $\nu \geq \mu >0$.
:::

Note that $g^{-1}$ is also a bi-Lipschitz diffeomorphism as $$\begin{equation}
\label{eq:bi-lipschitz-inverse}
    \frac{1}{\nu} |z_1-z_2|\leq \bigl|g^{-1}(z_1)-g^{-1}(z_2)\bigr|\leq \frac{1}{\mu} |z_1-z_2|.
\end{equation}$$ Moreover, $g$ also induces a Riemmanian metric $$\begin{equation}
\label{eq:metric}
    M(x):=G(x)^\top G(x)
\end{equation}$$ with $G(x)=\partial g(x)/\partial x$ as the Jacobian of $g$ at $x$, where $M$ gives a notion of local distance [@boothby2003introduction]. Since $g$ is bi-Lipschitz, $M$ is uniformly bounded, i.e., $$\begin{equation}
\label{eq:uniform-bound}
    \mu^2 I\preceq M(x)\preceq \nu^2I, \quad \forall x\in \mathbb{R}^n.
\end{equation}$$

# Main Theoretical Results {#sec:main results}

In this section, we provide a systematic approach to construct an all-pairs motion planner [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} using bi-Lipschitz diffeomorphisms.

## All-Pairs Motion Planning via Natural Gradient Flow

Let $g:\mathbb{R}^n\rightarrow\mathbb{R}^n$ be a bi-Lipschitz diffeomorphism. We take the candidate Lyapunov function as follows $$\begin{equation}
 \label{eq:v-func}
    V(x,x_\star)= \tfrac{\lambda}{2}|g(x)-g(x_\star)|^2.
\end{equation}$$ where $\lambda>0$ is a tunable parameter. We then construct the dynamics [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} based on the natural gradient flow of $V(x,x_\star)$, i.e., $$\begin{equation}
\label{eq:natural_gradient}
    \dot{x} =f(x,x_\star):= -M(x)^{-1} \nabla_x \nabla V(x, x_\star).
\end{equation}$$ The matrix inverse is well-defined due to [\[eq:uniform-bound\]](#eq:uniform-bound){reference-type="eqref" reference="eq:uniform-bound"}, and the system has a unique equilibrium point at $x_\star$. Our main theoretical result is as follows.

::: {#thm:main .thm}
**Theorem 1**. *If there exists a bi-Lipschitz diffeomorphism $g:\mathcal{X}_{\text{safe}}\rightarrow \mathcal{B}^n$, then the following statements hold:*

1.  *System [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is safe w.r.t. the set $\mathcal{X}_{\text{safe}}$.*

2.  *The vector field in [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is bounded $$\begin{equation}
    \label{eq:vel_bound}
                |f(x,x_\star)|\leq \frac{2\lambda}{\mu}.
    \end{equation}$$*

3.  *System [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is globally equilibrium-independent exponentially stable.*
:::

As shown in [@rana2020euclideanizing], under the coordinate transformation $z=g(x)$, system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is equivalent to $$\begin{equation}
\label{eq:z_dynamics}
    \dot{z}=\lambda(z_\star-z)
\end{equation}$$ with $z_\star=g(x_\star)$. Thus, system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} has explicit solutions of $$\begin{equation}
\label{eq:xt}
    x(t)=g^{-1}(z(t))
\end{equation}$$ where $$\begin{equation}
\label{eq:zt}
    z(t)=z_0e^{-\lambda t}+z_\star \bigl(1-e^{-\lambda t}\bigr)
\end{equation}$$ with $z_0=g(x_0)$.

Statement 1): The main idea is that under the diffeomorphism $g$, the transformed safe set $\mathcal{Z}_{\text{safe}}:=\mathcal{B}^n$ which is convex, and from [\[eq:zt\]](#eq:zt){reference-type="eqref" reference="eq:zt"} we have that $z(t)$ is a straight line from $z_0$ to $z_\star$. Hence for any $z_0$ and $z_\star$ in $\mathcal{Z}_{\text{safe}}$ the path between them remains in $\mathcal{Z}_{\text{safe}}$, i.e. $z(t)\in \mathcal{Z}_{\text{safe}}$ for all $t\geq 0$. Passing back to $x(t)=g^{-1}(z(t))$, this implies that $x(t)\in \mathcal{X}_{\text{safe}}$ for all $t\geq 0$.

Statement 2): The $\mathcal{Z}$-space dynamics [\[eq:z_dynamics\]](#eq:z_dynamics){reference-type="eqref" reference="eq:z_dynamics"} is a push forward map of [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"}: $$\begin{equation}
\label{eq:push-forward}
    G(x)f(x,x_\star)=\lambda(z_{\star}-z),
\end{equation}$$ which further implies $$\begin{equation}
\label{eq:vf-bound}
    |f(x,x_\star)|\leq \lambda |z-z_\star|/\|G(x)\|\leq \frac{2\lambda}{\mu}
\end{equation}$$ since $z,z_\star\in \mathcal{B}^n$ and $g$ has lower Lipschitz bound of $\mu$.

Statement 3): Since $g$ is bi-Lipschitz, we obtain $$\begin{equation}
\label{eq:x-exp-stable}
    \begin{split}
    |x(t)-x_\star|&=|g^{-1}(z(t))-g^{-1}(z_\star)| \leq  \frac{1}{\mu} |z(t)-z_\star|\\
    &=\frac{1}{\mu}|z_0-z_\star|e^{-\lambda t} \leq \frac{\nu}{\mu}|x_0-x_\star|e^{-\lambda t}.
\end{split}
\end{equation}$$ System [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is equilibrium-independent exponentially stable.

::: remark
*Remark 1*. While [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} can be considered as a feedback controller to be implemented in real-time for the system [\[eq:robot-dyn\]](#eq:robot-dyn){reference-type="eqref" reference="eq:robot-dyn"}, there is also often need to predict future motions in simulation. For this case, we can sample the analytic solution [\[eq:zt\]](#eq:zt){reference-type="eqref" reference="eq:zt"} for $z(t)$ at a grid of points, and pass them in parallel through $g^{-1}$ to obtain $x(t)$. When a fast inverse algorithm is available $g$, as in [@wang2024monotone], this can be done in parallel on a GPU.
:::

::: remark
*Remark 2*. It can be shown that system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is incrementally exponentially stable w.r.t. the incremental Lyapunov $V(x_1,x_2)$. From the contraction theory perspective ([@Lohmiller1998Contraction]), system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is contracting w.r.t. the metric $M(x)$ in [\[eq:metric\]](#eq:metric){reference-type="eqref" reference="eq:metric"} [@yi2023equivalence Thm. 1], see also [@wensing2020beyond].
:::

It is clear from the proof that without any additional effort, we can extend the above theorem by replacing the set $\mathcal{B}^n$ to any convex, compact set $\mathcal{Z}_{\text{safe}}$ so that $\mathcal{X}_{\text{safe}}$ admits more complicated shapes (e.g., with sharp corners).

::: corollary
*Corollary 1*. Suppose that $g:\mathcal{X}_{\text{safe}}\rightarrow \mathcal{Z}_{\text{safe}}$ is a bi-Lipschitz diffeomorphism, where $\mathcal{Z}_{\text{safe}}\subset\mathbb{R}^n$ is a convex and compact set. Then, Statement 1) and 3) hold. For Statement 2), the vector field is bound $$|f(x,x_\star)|\leq \frac{D\lambda}{\mu},$$ where $D$ is the diameter of $\mathcal{Z}_{\text{safe}}$, i.e., $$D:=\max_{z_1,z_2\in \mathcal{Z}_{\text{safe}}} |z_1-z_2|.$$
:::

::: remark
*Remark 3*. If $\mathcal{X}_{\text{safe}}$ is not diffeomorphic to a ball, e.g., $\mathcal{X}_{\text{safe}}$ contains holes, then the approach needs to be modified. The navigation function approach includes strategies for dealing with this via diffeomorphism to a "sphere world" in which the free space is a ball with a finite number of ball-shaped obstacles removed [@romon1990exact]. Under certain conditions, almost-global stability can still be certified. We leave the details of the extension for a future work.
:::

## Safety Properties

The key property of our approach is that it guarantees safety for arbitrary start/goal pairs. In the control literature, safety in the form of forward invariance of a set is often certified by a barrier function, as defined below (see e.g. [@amesControlBarrierFunction2017a]):

::: defn
*Definition 5*. Consider a nonlinear system $\dot{x}=f(x,t)$. A continuously differentiable function $h:\mathbb{R}^n\rightarrow \mathbb{R}$ is called a *barrier function* of $\mathcal{X}_{\text{safe}}$ if there exist a class $\mathcal{K}$ function $\alpha(\cdot)$ such that $$\begin{gather}
        h(x)\geq 0\quad \forall x\in \mathcal{X}_{\text{safe}}, \label{eq:B-safe}\\
        h(x)<0\quad \forall x\in \mathcal{X}_{\text{unsafe}}, \label{eq:B-unsafe} \\
        \frac{\partial h}{\partial x}f(x,t)\geq -\alpha(h) \quad \forall x\in \mathcal{X}. \label{eq:B-decay}
    \end{gather}$$
:::

Note that the Lyapunov function $V(x,x_\star)$ in [\[eq:v-func\]](#eq:v-func){reference-type="eqref" reference="eq:v-func"} is not a barrier function for $\mathcal{X}_{\text{safe}}$ as $V(x,x_\star)$ may not be a constant for all $x\in \partial \mathcal{X}_{\text{safe}}$. The following result gives an explicit construction of barrier function for the proposed goal-conditioned neural ODE [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"}.

::: {#prop:barrier .prop}
**Proposition 1**. *Suppose that conditions of Theorem [1](#thm:main){reference-type="ref" reference="thm:main"} hold. Then, the forward invariance of $\mathcal{X}_{\text{safe}}$ can be certified by the following barrier function $$\begin{equation}
\label{eq:barrier}
        h(x)=1- \left|g(x)\right|^2.
\end{equation}$$*
:::

Since $g:\mathcal{X}_{\text{safe}}\rightarrow \mathcal{B}^n$ is a bi-Lipschitz diffeomorphism, then $h(x)$ satisfies [\[eq:B-safe\]](#eq:B-safe){reference-type="eqref" reference="eq:B-safe"} - [\[eq:B-unsafe\]](#eq:B-unsafe){reference-type="eqref" reference="eq:B-unsafe"}. The time derivative of $h$ yields $$\begin{equation}
        \begin{split}
            \dot{h}&=2\lambda g(x)^\top G(x)M(x)^{-1}G(x)^\top (g(x)-g(x_\star))\\
            &=2\lambda g(x)^\top(g(x)-g(x_\star)).
        \end{split}
\end{equation}$$ For $x\in \mathcal{X}_{\text{safe}}$, we have $$\begin{equation*}
        \dot{h}=2\lambda (|g(x)|^2-1)+2\lambda(1-g(x)^\top g(x_\star)) \geq -2\lambda h(x)
\end{equation*}$$ where the last inequality follows by $g(x),g(x_\star)\in \mathcal{B}^n$. For $x\in \mathcal{X}_{\text{unsafe}}$ (i.e. $|g(x)|>1$ and $h(x)<0$), we can obtain $$\begin{equation}
        \begin{split}
            \dot{h}&=2\lambda(|g(x)|^2-g(x)^\top g(x_\star))\\
            &\geq 2\lambda |g(x)|(|g(x)|-|g(x_\star)|)>0.
        \end{split}
\end{equation}$$ Thus, [\[eq:B-decay\]](#eq:B-decay){reference-type="eqref" reference="eq:B-decay"} holds and $h(x)$ is a barrier function of $\mathcal{X}_{\text{safe}}$.

## Time-Varying Goal Location

When the goal position is time-varying with uncertain but bounded velocity, e.g. to reach for a moving object, the following result shows that our approach still guarantees safety and converges to a bounded region around the goal.

::: {#prop: 1 .thm}
**Theorem 2**. *Consider system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} with time-varying goal $x_\star(t)$ with $|\dot{x}_{\star}(t)|\leq b$ for all $t\geq 0$. If $g:\mathcal{X}_{\text{safe}}\rightarrow\mathcal{Z}_{\text{safe}}$ is a bi-Lipschitz diffeomorphism, where $\mathcal{Z}_{\text{safe}}$ is a convex compact set, then the following statements hold:*

1.  *The set $\mathcal{X}_{\text{safe}}$ is forward invariant.*

2.  *The time-varying vector field is bounded $$|f(x,x_\star(t))|\leq \frac{2\mu}{\lambda}.$$*

3.  *For any $x_0\in \mathcal{X}_{\text{safe}}$, the tracking error $\epsilon(t):=x(t)-x_\star(t)$ satisfies $$\begin{equation}
                |\epsilon(t)|\leq \frac{\nu}{\mu}\left(|\epsilon(0)|e^{-\lambda t}+\frac{b}{\lambda}\right).
    \end{equation}$$*
:::

Statement 1): System [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} with time-varying $x_\star(t)$ can also be transformed into $\dot{z}=\lambda(z_\star(t)-z)$ with $z_{\star}(t)=g(x_\star(t))$. Since $\mathcal{Z}_{\text{safe}}$ is compact and convex, then the time-varying vector field $\lambda(z_\star(t)-z)$ always points into $\mathcal{Z}_{\text{safe}}$ or is tangent to $\partial \mathcal{Z}_{\text{safe}}$ for any $z\in\partial \mathcal{Z}_{\text{safe}}$ and $z_{\star}(t)\in \mathcal{Z}_{\text{safe}}$. By Nagumo's theorem [@nagumo1942lage] we obtain that $\mathcal{Z}_{\text{safe}}$ is forward invariant, implying that $\mathcal{X}_{\text{safe}}$ is forward invariant under [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"}.

Statement 2) follows directly by [\[eq:push-forward\]](#eq:push-forward){reference-type="eqref" reference="eq:push-forward"} and [\[eq:vf-bound\]](#eq:vf-bound){reference-type="eqref" reference="eq:vf-bound"}. We now focus on Statement 3). First, the dynamics of $\epsilon_z(t):=z(t)-z_\star(t)$ in the $\mathcal{Z}$-space can be rewritten as $$\dot{\epsilon}_z=-\lambda \epsilon_z-\dot{z}_{\star}(t),$$ where $|\dot{z}_\star(t)|\leq \nu b$. This implies $|\epsilon_z(t)|\leq |\epsilon_z(0)|e^{-\lambda t}+\nu b/\lambda$. Finally, following the procedure in [\[eq:x-exp-stable\]](#eq:x-exp-stable){reference-type="eqref" reference="eq:x-exp-stable"} yields $$\begin{split}
        |\epsilon(t)|\leq \frac{1}{\mu}|\epsilon_z(t)|
        \leq \frac{\nu}{\mu}\left(|\epsilon(0)|e^{-\lambda t}+\frac{b}{\lambda}\right).
    \end{split}$$

## Finite-time Convergence via Euclidean Norm Potential

Similar to [@rana2020euclideanizing], the proposed Lyapunov function $V(x,x_\star)$ can incorporate a more general potential function $\Phi:\mathbb{R}^n\rightarrow \mathbb{R}$, i.e., $$\begin{equation}
    V(x,x_\star)=\Phi(g(x)-g(x_\star)).
\end{equation}$$ Then, the dynamics of [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} in the $\mathcal{Z}$-space becomes $$\begin{equation}
\label{eq:z-phi}
    \dot{z}=-\nabla_z \Phi(z-z_\star)
\end{equation}$$ which can be pulled back in to $\mathcal{X}$ space. If $\Phi$ continuously differentiable and satisfies the *Polyak-Łojasiewicz* (PL) condition [@polyak1963gradient; @lojasiewicz1963topological], then global exponential stability can still be established.

If finite-time convergence is desired, then $\Phi$ can be taken as the Euclidean norm (i.e., $\Phi(z)=\lambda|z|$), instead of the norm squared, and then system [\[eq:z-phi\]](#eq:z-phi){reference-type="eqref" reference="eq:z-phi"} becomes $$\begin{equation}
    \dot{z}=-\lambda \frac{z-z_\star}{|z-z_\star|},
\end{equation}$$ although the dynamics is not smooth at the goal $z_\star$. Since the resulting trajectory has unit velocity in $\mathcal{Z}$ space, we can, analogously to Theorem [1](#thm:main){reference-type="ref" reference="thm:main"}, obtain simple upper and lower bounds on the vector field velocity in the $\mathcal{X}$-space, i.e., $$\begin{equation}
    \frac{\lambda}{\nu} \leq  |f(x,x_\star)|\leq \frac{\lambda}{\mu}.
\end{equation}$$

## Natural Gradient Flow *v.s.* Gradient Flow

A natural question for the proposed approach is: what advantages does natural gradient flow offer over standard gradient flow? Our answer is as follows: standard gradient flow does not provide safety guarantees when $x_\star$ varies.

Given a Lyapunov function $V(x,x_\star)$ in [\[eq:v-func\]](#eq:v-func){reference-type="eqref" reference="eq:v-func"}, we consider the following gradient flow dynamics: $$\begin{equation}
\label{eq:grad-flow}
    \dot{x}=-\nabla_x V(x, x_\star).
\end{equation}$$ From [@Cheng2024LearningSA Thm. 1], we can conclude that the above system achieves equilibrium-independent exponential stability. However, it cannot provide safety guarantees for all $x_\star\in \mathcal{X}_{\text{safe}}$, see the example below.

::: {#ex:shear_transformation .example}
*Example 1*. Consider the mapping $g:\mathbb{R}^2\to\mathbb{R}^2$ defined by $$\begin{equation}
\label{eq:g analytical}
    g(x) =
    \begin{bmatrix} 1 & 0 \\ h(x_1) & 1 \end{bmatrix}
    \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
\end{equation}$$ where $h(x_1) = 2\sin(x_1) + \cos(5x_1) - 3x_1$. It is a bi-Lipschitz diffeomorphism with $g^{-1}$ defined by $x_1=z_1$ and $x_2=z_2-h(z_1)z_1$. We take $\mathcal{Z}_{\text{safe}}= \mathcal{B}^2$ and $\mathcal{X}_{\text{safe}}= g^{-1}(\mathcal{Z}_{\text{safe}})$.

:::: {#fig:ngd-vs-gd .figure latex-placement="!tb"}
  ------------------------------------------------------
   ![image](Liu2026GoalConditioned_figs/snail_goal_origin.png){width="85%"}
                  \(a\) $x_\star=(0, 0)$
    ![image](Liu2026GoalConditioned_figs/snail_goal_new.png){width="85%"}
                \(b\) $x_\star\neq (0, 0)$
  ------------------------------------------------------

::: caption
Trajectory samples and vector field on the boundary for the natural gradient flow [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} (blue) and the gradient flow [\[eq:grad-flow\]](#eq:grad-flow){reference-type="eqref" reference="eq:grad-flow"} (black) with different goal points, where red curves are the boundaries.
:::
::::

When $x_\star=(0,0)$, we have that $V(x,x_\star)$ is a barrier function for both [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} and [\[eq:grad-flow\]](#eq:grad-flow){reference-type="eqref" reference="eq:grad-flow"}. Thus, $\mathcal{X}_{\text{safe}}$ is forward invariant in both cases, see Fig. [2](#fig:ngd-vs-gd){reference-type="ref" reference="fig:ngd-vs-gd"}(a). When $x_\star$ changes, it is no longer a barrier function as $V(x,x_\star)$ is not a constant for $x\in \partial \mathcal{X}_{\text{safe}}$. Fig. [2](#fig:ngd-vs-gd){reference-type="ref" reference="fig:ngd-vs-gd"}(b) shows that $\mathcal{X}_{\text{safe}}$ is no longer a forward-invariant set for [\[eq:grad-flow\]](#eq:grad-flow){reference-type="eqref" reference="eq:grad-flow"}. This is also supported by the fact that its vector field points outward at some part of the boundary. For the proposed approach, $\mathcal{X}_{\text{safe}}$ is forward invariant as the vector field of [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} always points inward for all $x_\star\in \mathcal{X}_{\text{safe}}$. A barrier function $h(x)$ can be constructed via [\[eq:barrier\]](#eq:barrier){reference-type="eqref" reference="eq:barrier"}.
:::

## Comparison with Navigation Function based Approach

When the goal state $x_\star$ is fixed, a classical approach [@koditschek1990robot] to construct system [\[eq:system\]](#eq:system){reference-type="eqref" reference="eq:system"} is via gradient flow $$\begin{equation}
\label{eq:navigation-func}
    \dot{x} = -\nabla \phi(x)
\end{equation}$$ where $\phi : \mathcal{X}_{\text{safe}}\to [0,1]$ is a *navigation function* satisfying the following conditions:

- $\phi$ is Morse function (i.e., $\phi$ is smooth and it has no degenerate critical point);

- $\phi$ has a unique minimum on $\mathcal{X}_{\text{safe}}$ at $x_\star$ and no other critical points;

- $\nabla\phi$ is bounded on $\mathcal{X}_{\text{safe}}$;

- $\phi(x)=1$ for all $x\in \partial \mathcal{X}_{\text{safe}}$.

The navigation function $\phi$ serves as both a Lyapunov function and a barrier function since $$\dot{\phi}=-|\nabla \phi(x)|^2 <0, \quad \forall x \in \mathcal{X}_{\text{safe}}, \;x\neq x_\star.$$ Note that $\phi(x)=|g(x)|^2$ with $g:\mathcal{X}_{\text{safe}}\rightarrow \mathcal{B}^n$ and $g(x_\star)=0$ is a validate navigation function. However, one needs to recompute $g$ when $x_\star$ changes.

Compared with the navigation based approach, our method is more flexible as it does not require recomputing $g$ when $x_\star$ changes since it uses different certificate functions for stability and safety, although both are expressed in terms of a single learned diffeomorphism $g$.

## Compared with Existing Diffeomorphism based Dynamical Approaches

The diffeomorphism based approach has also been recently explored for learning stable neural ODE from demonstration, see [@rana2020euclideanizing; @pmlr-v162-zhi22a; @pmlr-v168-zhi22a]. Specifically, those approaches take the following gradient flow in the $\mathcal{Z}$-space: $$\begin{equation}
\label{eq:z-gen}
    \dot{z}=-\nabla \Phi(z)
\end{equation}$$ where the potential function $\Phi$ is positive definite, convex, continuously differentiable, and radially unbounded. And a natural gradient dynamics in the $\mathcal{X}$-space is constructed by pulling [\[eq:z-gen\]](#eq:z-gen){reference-type="eqref" reference="eq:z-gen"} back to the $\mathcal{X}_{\text{safe}}$-space via a diffeomorphism $g$. The primary goal of those approaches is to learn stable dynamics that mimics the demonstration data.

Different from those approaches, our method can learn both stable and safe dynamics from data. The second difference is that our approach can generalize to unseen goal point without retraining the model. Finally, our approach imposes explicit bounds on the diffeomorphism $g$, which can be seen as effective regularization preventing overfitting. Meanwhile, explicit bounds on tracking error and vector field magnitude can be obtained, which is useful for practical applications.

# Learning an All-Pairs Motion Planner {#sec:learning}

In this section, we aim to translate the above theoretical construction into a tractable machine learning setup, detailing the choice of training data, model class, and loss functions.

We parameterize the diffeomorphism $g$ by some smooth bi-Lipschitz neural network $g_\theta:\mathbb{R}^n\to\mathbb{R}^n$ with $\theta\in \mathbb{R}^p$ as the learnable parameter. By construction, system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is smooth and globally equilibrium-independent experientially stable, as shown in Theorem [1](#thm:main){reference-type="ref" reference="thm:main"}. To ensure safety, one needs to learn a $g_\theta$ that can be used to characterize the set $\mathcal{X}_{\text{safe}}$. Since a candidate Lyapunov function $V(x,x_\star)$ is used in the model construct, we seek to separate the safe and unsafe datasets in [\[eq:datasets\]](#eq:datasets){reference-type="eqref" reference="eq:datasets"} via a Lyapunov sublevel set of $V$. Specifically, we pick up a point $\hat{x}_{\star} \in \mathcal{D}_{\text{safe}}$ as the goal and take $g_\theta(\hat{x}_{\star})=0$. Then, the Lyapunov function in [\[eq:v-func\]](#eq:v-func){reference-type="eqref" reference="eq:v-func"} can be written as $$\begin{equation}
\label{eq:vtx}
    \tilde{V}_\theta(x)=V(x,\hat{x}_\star)=\frac{\lambda}{2}|g_\theta(x)|^2,
\end{equation}$$ whose sublevel sets are $\Omega_{\theta}^{c}=\{x: \tilde{V}_\theta(x)\leq c\}$ with $c>0$. Note that $\Omega_{\theta}^{c}$ is diffeomorphic to $\mathcal{B}^n$ for any $\theta\in \mathbb{R}^p$ and $c>0$. Now, the learning problem becomes: find a pair $(c,\theta)$ such that $$\label{eq:levelset}
    \begin{align}
        x_i\in \mathcal{D}_{\text{safe}}\; &\Rightarrow\; x_i\in \Omega_\theta^c, \label{eq:levelset-safe}\\
        x_j\in \mathcal{D}_{\text{unsafe}}\; &\Rightarrow \; x_j \notin \Omega_\theta^c \label{eq:levelset-unsafe}.
    \end{align}$$

## Training Data

To solve the above learning problem, we need to assign labels to the points from the datasets $\mathcal{D}_{\text{safe}}$ and $\mathcal{D}_{\text{unsafe}}$. An intuitive approach is to associate $x_i\in \mathcal{D}_{\text{safe}}$ and $x_j\in \mathcal{D}_{\text{unsafe}}$ with labels of 0 and 1, respectively. The learning problem in [\[eq:levelset\]](#eq:levelset){reference-type="eqref" reference="eq:levelset"} is formulated as a classification task, where $\tilde{V}_\theta(x)$ is the classifier. However, those labels do not provide informative geometric information in $\mathcal{D}_{\text{safe}}$ and $\mathcal{D}_{\text{unsafe}}$.

By leveraging the existing sampling-based motion planning algorithms (e.g. PRM [@Kavraki1996ProbabilisticRF] or RRT [@LaValle1998RapidlyexploringRT]), we can assign each point $x_i\in\mathcal{D}_{\text{safe}}$ with a label $c_i$ indicating the shortest path length from $x_i$ to the targe $\hat{x}_{\star}$. Specifically, we first construct a graph by connecting each $x_i$ to a set of its nearby neighbors in $\mathcal{D}_{\text{safe}}$. From this graph, we can define the cost-to-go function $d:\mathcal{D}_{\text{safe}}\to\mathbb{R}_{\geq0}$ as the shortest path distance from sample $x\in \mathcal{D}_{\text{safe}}$ to the goal $\hat{x}_\star$, which is a proxy for the distance between $x_i$ and $\hat{x}_{\star}$. The function $d(x)$ naturally reflects the geometry of $\mathcal{X}_{\text{safe}}$: samples near the goal attain small values, while samples that are distant or geometrically separated from $\hat{x}_\star$ attain large values. Thus, $d(x)$ provides meaningful information for training $\tilde{V}_\theta(x)$. Then, we construct the training datasets as follows: $$\begin{align}
        \bar{\mathcal{D}}_{\text{safe}}&=\{(x_i,c_i): c_i=d(x_i),\, x_i\in \mathcal{D}_{\text{safe}}\}\label{eq:d_safe} \\
        \bar{\mathcal{D}}_{\text{unsafe}}&=\{(x_j,c_j): c_j=\bar{c}+\delta,\,x_j\in \mathcal{D}_{\text{unsafe}}\}\label{eq:d_unsafe}
    \end{align}$$ where $\bar{c}$ is the maximum label value in $\bar{\mathcal{D}}_{\text{safe}}$, and $\delta>0$ is a hyperparameter which ensures that there exists $c\in [\bar{c},\bar{c}+\delta]$ satisfying [\[eq:levelset\]](#eq:levelset){reference-type="eqref" reference="eq:levelset"}.

## Model Class

In this work, we use the BiLipNet [@wang2024monotone] as the model class for $g_\theta$. BiLipNets can enforce certified bi-Lipschitz bounds $\mu$ and $\nu$ via a method derived from [@wang2023direct] which are, to the authors knowledge, the tightest available. The bi-Lipschitz bounds are trainable parameters, and their ratio $\tfrac{\nu}{\mu}$ can be considered a tunable *distortion* parameter, describing how much the learnt representation of $\mathcal{X}_{\text{safe}}$ distorts from a unit ball, and therefore how much the learnt trajectories can deviate from straight lines -- notice that this also appears in the overshoot constant for our exponential convergence bound [\[eq:x-exp-stable\]](#eq:x-exp-stable){reference-type="eqref" reference="eq:x-exp-stable"}. The lower bound $\mu$ also appears in our bound on velocity [\[eq:vel_bound\]](#eq:vel_bound){reference-type="eqref" reference="eq:vel_bound"}.

BiLipNets have a number of other advantages: firstly, BiLipNets admits a direct model parameterization, which allows training within the standard unconstrained optimization methods such as stochastic gradient descent. Secondly, the feedthrough layer architecture can improve the model expressivity without suffering from vanishing gradients. Thirdly, BiLipNets have a structure that admits fast splitting-based solvers for computing the model inverse.

## Loss Function

The loss function will generally include two components. The first component trains the diffeomorphism to map the safe set $\mathcal{X}_{\text{safe}}$ onto the unit ball. However, this leaves substantial flexibility for the shape of the mapping *inside* $\mathcal{X}_{\text{safe}}$, so a second task-specific loss term can be employed which may take many forms, e.g. training the dynamics [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} to mimic demonstration trajectories.

For the first task, i.e., achieving [\[eq:levelset\]](#eq:levelset){reference-type="eqref" reference="eq:levelset"}, we choose the following loss function $$\begin{equation}
\label{eq: loss base}
    \mathcal{L}(\theta)=\mathcal{L}_{\text{safe}}(\theta)+\mathcal{L}_{\text{unsafe}}(\theta)
\end{equation}$$ where $$\begin{equation*}
    \begin{split}
        \mathcal{L}_{\text{safe}}(\theta)&=\frac{1}{|\Bar{\mathcal{D}}_{\text{safe}}|}\sum \max\bigl(\tilde{V}_\theta(x_i)-c_i, 0\bigr)^2, \\
        \mathcal{L}_{\text{unsafe}}(\theta)&=\frac{1}{|\Bar{\mathcal{D}}_{\text{unsafe}}|}\sum \max\bigl(c_j-\tilde{V}_\theta(x_j), 0\bigr)^2.
    \end{split}
\end{equation*}$$ The term $\mathcal{L}_{\text{safe}}$ penalizes the samples from $\Bar{\mathcal{D}}_{\text{safe}}$ for which $\tilde{V}_\theta(x_i)>c_i$ is required to ensure [\[eq:levelset-safe\]](#eq:levelset-safe){reference-type="eqref" reference="eq:levelset-safe"}, while $\mathcal{L}_{\text{unsafe}}$ penalizes the samples from $\Bar{\mathcal{D}}_{\text{unsafe}}$ for which $\tilde{V}_\theta(x_j)<\Bar{c}$ to ensure [\[eq:levelset-unsafe\]](#eq:levelset-unsafe){reference-type="eqref" reference="eq:levelset-unsafe"}.

The loss function for the second task may take various forms. E.g., when the demonstration dataset is available, we can define $$\begin{equation*}
    \mathcal{L}_{\text{task}}(\theta)=\frac{1}{|\mathcal{D}_{\text{demo}}|}\sum\bigr(  \Dot{x}_k - f_\theta(x_k, x_{k,\star}) \bigl)^2
\end{equation*}$$ where $f_\theta$ is the vector filed in [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} with $g_\theta$. The total loss is taken as $\mathcal{L}_{t}=\mathcal{L}+\rho\mathcal{L}_{\text{task}}$ with weighting $\rho>0$.

# Numerical Experiments {#sec:numeric experiment}

We illustrate the proposed approach on a 2D corridor navigation task (see Fig. [3](#fig:rrt){reference-type="ref" reference="fig:rrt"}), where we aim to generate safe and smooth trajectories from any initial configuration $x_0\in\mathcal{X}_{\text{safe}}$ to any goal $x_\star\in\mathcal{X}_{\text{safe}}$ in the presence of geometric obstacles. All experiments are implemented in Python using JAX and executed on an NVIDIA RTX 4090 GPU. Code is available at <https://github.com/acfr/Goal-Conditioned-Safe-ODE>.

## Data Generation and Training details

As shown in Fig. [3](#fig:rrt){reference-type="ref" reference="fig:rrt"} (left), we initialized RRT [@LaValle1998RapidlyexploringRT] at a fixed goal $\hat{x}_\star$ to generate a shortest-path tree over $\mathcal{X}_{\text{safe}}$. This automatically provides the dataset pair $(x_i,d(x_i))$ where $d(x_i)$ is the cost-to-go with $x_i\in\mathcal{X}_{\text{safe}}$, see Fig. [3](#fig:rrt){reference-type="ref" reference="fig:rrt"} (right). We take 2,500 samples to formulate the dataset $\bar{\mathcal{D}}_{\text{safe}}$ in [\[eq:d_safe\]](#eq:d_safe){reference-type="eqref" reference="eq:d_safe"}. Another 2,500 samples are uniformly sampled in $\mathcal{X}_{\text{unsafe}}$, which forms $\bar{\mathcal{D}}_{\text{unsafe}}$ in [\[eq:d_unsafe\]](#eq:d_unsafe){reference-type="eqref" reference="eq:d_unsafe"}.

:::: {#fig:rrt .figure latex-placement="!tb"}
![](Liu2026GoalConditioned_figs/rrt.png){width="\\linewidth"}

::: caption
RRT data (gray) in the corridor environment. (Left) RRT rooted at $\hat{x}_{\star}$, with a representative trajectory (blue) in $\mathcal{X}$. (Right) Corresponding cost-to-go field $d(\cdot)$ visualized via contour lines over $\mathcal{X}_{\text{safe}}$.
:::
::::

We use BiLipNet from [@wang2024monotone] to parameterize the bi-Lipschitz diffeomorphism $g_\theta$. The network is trained based on the loss function in [\[eq: loss base\]](#eq: loss base){reference-type="eqref" reference="eq: loss base"} via the Adam optimizer [@kingma2015adam] with a batch size of 16 for 1500 epochs.

## Results and Discussions

Fig. [1](#fig:boundary_mapping){reference-type="ref" reference="fig:boundary_mapping"} shows the learned mapping $g$ that transforms $\mathcal{X}_{\text{safe}}'\subset \mathcal{X}_{\text{safe}}$ in the $\mathcal{X}$-space (Left) to a unit ball $\mathcal{B}^2$ in the $\mathcal{Z}$-space (Right). $\partial \mathcal{X}_{\text{safe}}'$ and $\partial \mathcal{B}^2$ are indicated by red curves while $\partial \mathcal{X}_{\text{safe}}$ is in black. $\partial \mathcal{X}_{\text{safe}}'$ conforms to the geometry of the obstacle boundaries, which is neither convex nor star-convex.

Fig. [4](#fig:natural_gradient_flow){reference-type="ref" reference="fig:natural_gradient_flow"} shows that complex trajectories of the natural gradient flow system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} (left) are equivariant to linear trajectories of system [\[eq:z_dynamics\]](#eq:z_dynamics){reference-type="eqref" reference="eq:z_dynamics"} (right) under the coordination change. Pulling back straight lines in $\mathcal{Z}$-space (Fig. [4](#fig:natural_gradient_flow){reference-type="ref" reference="fig:natural_gradient_flow"} right) through $g_{\theta}^{-1}$ yields safe trajectories in $\mathcal{X}_{\text{safe}}$ (Fig. [4](#fig:natural_gradient_flow){reference-type="ref" reference="fig:natural_gradient_flow"} left) that respect the obstacle geometry. All trajectories in Fig. [4](#fig:natural_gradient_flow){reference-type="ref" reference="fig:natural_gradient_flow"} (left) also converge to $\hat{x}_\star$.

:::::::::: {#fig:natural_gradient_flow .figure latex-placement="!tb"}
::::: minipage
::: minipage
![](Liu2026GoalConditioned_figs/corridor_goal_origin_x.png){width="\\linewidth"}
:::

::: minipage
![](Liu2026GoalConditioned_figs/corridor_goal_origin_z.png){width="\\linewidth"}
:::
:::::

::::: minipage
::: minipage
Trajectories in $\mathcal{X}$ Space
:::

::: minipage
Trajectories in $\mathcal{Z}$ Space
:::
:::::

::: caption
Trajectories generated by system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} from multiple initial configurations to the goal $\hat{x}_\star$ in the training dataset. (Left) Smooth, safe paths in the $\mathcal{X}$-space. (Right) Those paths are transformed into straight-line trajectories in the $\mathcal{Z}$-space, demonstrating the geometric simplification induced by $g_{\theta}$.
:::
::::::::::

Fig. [5](#fig:NGF-varying-goal){reference-type="ref" reference="fig:NGF-varying-goal"} illustrates that multiple trajectories converge to a distinct, previously unseen goal $x_\star$ (red cross). This indicates system [\[eq:natural_gradient\]](#eq:natural_gradient){reference-type="eqref" reference="eq:natural_gradient"} is equilibrium-independent stable and safe. Note that the model was trained using data corresponding to a *single* goal, but it generalizes gracefully to a goal in a completely different location.

:::::::::: {#fig:NGF-varying-goal .figure latex-placement="!tb"}
::::: minipage
::: minipage
![](Liu2026GoalConditioned_figs/corridor_goal_new_x.png){width="\\linewidth"}
:::

::: minipage
![](Liu2026GoalConditioned_figs/corridor_goal_new_z.png){width="\\linewidth"}
:::
:::::

::::: minipage
::: minipage
Trajectories in $\mathcal{X}$ Space
:::

::: minipage
Trajectories in $\mathcal{Z}$ Space
:::
:::::

::: caption
Generalization to previously unseen goal $x_\star$ without retraining. (Left) Smooth, safe paths in the $\mathcal{X}$-space converging to a new goal $x_\star$ (red cross) from multiple initial configurations. (Right) In the $\mathcal{Z}$-space, the paths are transformed into straight-line trajectories within the unit ball.
:::
::::::::::

# Conclusion {#sec:conclusion}

In this paper, we presented a learning-based approach for safe, stable, and smooth all-pairs motion planning. Our approach uses a bi-Lipschitz diffeomorphism to transform a geometrically complex safe set into the unit ball, and complex motions within this set into simple linear stable dynamics which corresponds to a goal-conditioned natural gradient in the original state space. This approach guarantees that both safety and exponential stability are preserved regardless of the goal location within the safe set. Empirical results in 2D corridor navigation task illustrate the the proposed approach.

[^1]: \*This work was supported in part by the Australian Research Council through projects DP230101014 and IH210100030.

[^2]: The authors are with the Australian Centre for Robotics (ACFR), and the School of Aerospace, Mechanical and Mechatronic Engineering, The University of Sydney, Sydney, NSW 2006, Australia `ruigang.wang@sydney.edu.au`
