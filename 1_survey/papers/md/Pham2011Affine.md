---
citation_key: Pham2011Affine
arxiv_id: 1104.3270
arxiv_url: https://arxiv.org/abs/1104.3270
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:24:49Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Nonholonomic Motion Planning, Kinematics, Wheeled Robots, Marine Robotics
:::

# Introduction {#sec:intro}

A bicycle, a car, an aircraft, or a submarine are but a few examples of nonholonomic systems. Planning trajectories for such systems is difficult because, by nature, some of their degrees of freedom can only be controlled in a coupled manner (see e.g. [@Lau98book] and references therein). As a consequence, when such systems encounter on their ways an unexpected event (e.g. a random perturbation of the system state or of the target state, an unforeseen obstacle, etc.), it may be more efficient to *deform* in some manner the initially planned trajectory rather than to re-plan entirely a new one [@KhaX97icra; @KN03IJRR; @LamX04tr; @SeiX10wafr].

Lamiraux and colleagues [@LamX04tr] suggested to iteratively deform the original path by perturbing infinitesimally the control inputs at each iteration. However, as underlined by Seiler and colleagues [@SeiX10wafr], that method requires re-integrating the whole trajectory at each iteration, which is computationally expensive. These authors then described a new method based on Lie group symmetries, which requires re-integrating only *parts* of the trajectory.

The Lie groups considered in [@CheX08tr; @SeiX10wafr] are in fact Euclidean (or isometry) groups. We propose here to use larger Lie groups, namely, *affine* groups, which contain the Euclidean transformations as subgroups. Using affine transformations allows making more versatile trajectory corrections. In particular, the corrections are *exact* and can be computed *algebraically*, *in one step*, which makes iterative deformations [@LamX04tr] or gradient search [@CheX08tr; @SeiX10wafr] unnecessary. Furthermore, there is no need to re-integrate even a part of the trajectory. Note that, in contrast with previous works where the studied systems are invariant under Euclidean transformations [@CheX08tr; @SeiX10wafr], here trajectories and control inputs are not in general affine-invariant. More technical precautions need therefore to be taken to define and guarantee the feasibility (or admissibility) of the deformed trajectories under the system nonholonomic constraints. In particular, the admissibility conditions are formulated using differential equations with discontinuous right-hand sides [@Fil88book].

In section [2](#sec:general){reference-type="ref" reference="sec:general"}, we present the general framework of affine trajectory correction. We then apply this framework to derive position and orientation correction algorithms for two classical examples in nonholonomic mobile robotics: the general class of planar wheeled robots (sections [3](#sec:wheeled){reference-type="ref" reference="sec:wheeled"}) and a tridimensional underwater vehicle (section [4](#sec:uwv){reference-type="ref" reference="sec:uwv"}). In section [5](#sec:appli){reference-type="ref" reference="sec:appli"}, we study some more elaborate applications including trajectory correction for a car towing trailers, obstacle avoidance, feedback control and gap-filling techniques. Finally, in section [6](#sec:discussion){reference-type="ref" reference="sec:discussion"}, we discuss the advantages and drawbacks of the presented method, its domain of applicability, and possible future developments.

A preliminary version [@Pha11rss] of the present manuscript describing position and orientation correction algorithms for the unicycle, the bicycle and an underwater vehicle was accepted for presentation at the conference *Robotics: Science and Systems* 2011.

# General framework {#sec:general}

## Affine spaces and affine transformations {#sec:prelim}

An affine space is a set $\mathbb{A}$ together with a group action of a vector space $\mathbb{W}$. An element $\mathbf{w}\in\mathbb{W}$ transforms a point $P\in\mathbb{A}$ into another point $P'$ by $P'=P+\mathbf{w},$ which can also be noted $\overrightarrow{PP'}=\mathbf{w}$.

Given a point $O\in\mathbb{A}$ (the origin), an affine transformation $\mathcal{F}$ of the affine space can be defined by a couple $(\mathbf{w},\mathcal{M})$ where $\mathbf{w}\in\mathbb{W}$ and $\mathcal{M}$ is a non-singular endomorphism of $\mathbb{W}$ (i.e. a non-singular linear application $\mathbb{W}\rightarrow\mathbb{W}$). The transformation $\mathcal{F}$ operates on $\mathbb{A}$ by $$\forall P\in\mathbb{A} \quad \mathcal{F}(P)=O+
\mathcal{M}(\overrightarrow{OP})+\mathbf{w}.$$ Note that, if $P_0$ is a fixed-point of $\mathcal{F}$, then $\mathcal{F}$ can be written in the form $$\forall P\in\mathbb{A} \quad \mathcal{F}(P)=P_0+
\mathcal{M}(\overrightarrow{P_0P}).$$

## Admissible trajectories and admissible trajectory deformations {#sec:intro-adm}

Let us consider a commanded system of dimension $N$. Suppose that $n$ of the system variables form an affine space. As an example, consider the unicycle model [@Lau98book] $$\begin{equation}
  \label{eq:unicycle}
  \left\{
    \begin{array}{ccc}
      \dot{x} & = & v\cos(\theta)\\
      \dot{y} & = & v\sin(\theta)\\
      \dot{\theta} & = & \omega
   \end{array} \right.,
\end{equation}$$ where $(v,\omega)$ are the system control inputs (or commands) and $(x,y,\theta)$, the system variables. The $(x,y)$ space can be viewed as an affine space of dimension $n=2$. We call $(x,y)$ the *base variables* and the associated affine space, the *base space*.

We say that a full-space trajectory $\bar{\mathcal{C}}(t)_{t\in[0,T]}$ ($\bar{\mathcal{C}}(t)=(x(t),y(t),\theta(t))$ in the above example) is *admissible* if one can find a set of admissible commands ($v$ and $\omega$ in the example) that generates $\bar{\mathcal{C}}$. A base-space trajectory $\mathcal{C}$ ($\mathcal{C}=(x,y)$ in the example) is admissible if there exists an admissible full-space trajectory whose projection on the base space coincides with $\mathcal{C}$.

Let $\mathcal{C}(t)_{t\in[0,T]}$ be a base-space trajectory and $\tau\in[0,T]$, a given time instant. We say that a transformation $\mathcal{F}$ occurring at $\tau$ *deforms* $\mathcal{C}(t)_{t\in[0,T]}$ into $\mathcal{C}'(t)_{t\in[0,T]}$ if $$\begin{array}{rcl}
 \forall t<\tau &~& \mathcal{C}'(t)=\mathcal{C}(t)\\
 \forall t\geq\tau &~&\mathcal{C}'(t)=\mathcal{F}(\mathcal{C}(t)).
\end{array}$$

Given an admissible base-space trajectory $\mathcal{C}$, an affine transformation $\mathcal{F}$ is said to be admissible if $\mathcal{F}$ deforms $\mathcal{C}$ into an admissible trajectory.

## Differential equations with discontinuous right-hand sides {#sec:disc}

For convenience, we denote by $\mathscr{D}^0$ the space of *piecewise continuous functions with finite limits at the discontinuity points* -- or piecewise $C^0$ functions (see Fig. [1](#fig:ex){reference-type="ref" reference="fig:ex"}, top plot, for an example). Typically, the linear acceleration of a mobile robot would belong $\mathscr{D}^0$: indeed, any brusque press on the throttle or on the brake pedal would correspond to a discontinuity of the linear acceleration.

:::: {#fig:ex .figure latex-placement="ht"}
![](Pham2011Affine_figs/example_d0.png){width="5cm"}

::: caption
Examples of functions of $\mathscr{D}^0$ (top) and of $\mathscr{D}^1$ (bottom). Note that the top function is actually the derivative of the bottom function.
:::
::::

Let $u$ be a function of $\mathscr{D}^0$ and consider the following differential equation with discontinuous right-hand side (see [@Fil88book]) $$\begin{equation}
  \label{eq:disc}
  \left\{
\begin{array}{rcl}
\dot{x}(t)&=&u(t)\\
x(0)&=&x_0\\
\end{array} \right..
\end{equation}$$

It follows from the definition of $\mathscr{D}^0$ that any solution $x$ of system ([\[eq:disc\]](#eq:disc){reference-type="ref" reference="eq:disc"}) is $C^0$ and piecewise $C^1$. Conversely, for any function $x$ which is $C^0$ and piecewise $C^1$, one has $\dot{x}\in\mathscr{D}^0$. For convenience, we denote by $\mathscr{D}^1$ the space of such $x$ functions (see Fig. [1](#fig:ex){reference-type="ref" reference="fig:ex"}, bottom plot, for an example).

Finally, we denote by $\mathscr{D}^2$ the space of differentiable functions whose derivatives are in $\mathscr{D}^1$. This definition does not involve technical difficulties since the functions of $\mathscr{D}^1$ are continuous.

In the unicycle example of section [2.2](#sec:intro-adm){reference-type="ref" reference="sec:intro-adm"}, if the linear and angular accelerations $a$ and $\omega$ are assumed to be in $\mathscr{D}^0$ then the linear velocity $v$ and the orientation $\theta$ will belong to $\mathscr{D}^1$, which implies in turn that the position $(x,y)$ belongs to $\mathscr{D}^2$.

## Dimension of the space of admissible affine deformations {#sec:affinedef}

From the previous section, one can see that, typically, some of the variables are required to be *continuous*. These continuity conditions are particularly critical at the time instant $\tau$ when the deformation occurs. In general, if one needs to guarantee the continuities of $m$ variables at $\tau$, this will define $m$ constraints on the set of admissible affine transformations. On the other hand, the affine transformations of an $n$-dimensional space form a Lie group of dimension $n+n^2$ ($n$ coordinates for the translation and $n^2$ coordinates for the endomorphism of the associated vector space, where $n$ is the number of base variables). Consequently, if $n+n^2>m$, one could expect to have at our disposal $\tau$ and $n+n^2-m$ "extra degrees of freedom" to achieve the desired correction while staying admissible.

For wheeled robots of class I (see section [3.3](#sec:class1){reference-type="ref" reference="sec:class1"}) and wheeled robots of class II (section [3.4](#sec:class2){reference-type="ref" reference="sec:class2"}), the base space $(x,y)$ is of dimension $n=2$. We show that there are respectively $m=4$ and $m=5$ continuity conditions for these systems, yielding respectively $n+n^2-m=2$ and $n+n^2-m=1$ "extra degrees of freedom". We then suggest how to play with $\tau$ and these "extra degrees of freedom" to make corrections towards virtually any desired final position and orientation. For the tridimensional underwater vehicle (section [4](#sec:uwv){reference-type="ref" reference="sec:uwv"}), the base space $(x,y,z)$ is of dimension $n=3$ and there are $m=6$ continuity conditions, yielding $n+n^2-m=6$ "extra degrees of freedom".

# Affine trajectory correction for planar wheeled robots {#sec:wheeled}

The above presented framework suggests the following general scheme to study affine trajectory correction for a particular system

1.  check the conditions for a base-space trajectory to be admissible;

2.  characterize the set of admissible affine deformations;

3.  compute the admissible affine deformation that achieves the desired trajectory correction.

To illustrate, let us now apply the above scheme to wheeled robots, which constitute an important class of nonholonomic systems.

## Model description

At the kinematic level, any wheeled robot whose wheels obey the rolling without slipping constraints can be modeled by [@CamX96tr] $$\left\{\begin{array}{ccl}
\dot \xi&=&B(\xi,\beta)\eta\\
\dot \beta&=&\zeta
\end{array}\right.$$ where $\xi=(x,y,\theta)^\top$ is the *posture* of the robot and $\beta=(\beta_1\dots\beta_h)^\top$ contains the steering angles of the *centered orientable conventional wheels* ($h=0$ if there are no such wheels). As in the unicycle example of section [2.2](#sec:intro-adm){reference-type="ref" reference="sec:intro-adm"}, we choose $x$ and $y$ to be the base variables. The base space is thus of dimension 2. The non-base variables are $\theta$ and $\beta_1\dots\beta_h$.

Throughout this section [3](#sec:wheeled){reference-type="ref" reference="sec:wheeled"}, we assume, to avoid singularities, that the linear velocity $\sqrt{\dot x^2+\dot y^2}$ of the robot is always strictly positive.

The commands of the system are given by $\eta$, which contains the linear velocities of well-defined reference points on the frame of the robot, and $\zeta$, which contains the rates of change of the steering angles of the centered orientable wheels. We assume that the commands obey the following conditions

- the space of admissible commands $\eta$ is $\mathscr{D}^1$. This is consistent with the fact that the linear accelerations $a$ of the reference points, which are the derivatives of $\eta$, are in $\mathscr{D}^0$. The possible discontinuities of $a$ would correspond to e.g. brusque presses on the throttle or on the brake pedal;

- the space of admissible commands $\zeta$ is $\mathscr{D}^0$. The possible discontinuities of $\zeta$ would correspond to e.g. hard turns of the steering wheel in a car.

## Admissible base-space trajectories

As shown in [@CamX96tr], any planar wheeled mobile robot can be described by one out of the five sets of "forward" kinematic equations of Table [\[tab:wheeled\]](#tab:wheeled){reference-type="ref" reference="tab:wheeled"}, given a suitable choice of a reference point and of a basis attached to the robot frame.

::: table*
[]{#tab:wheeled label="tab:wheeled"}

+-------+----------------------+--------------------------------------------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------+
| Type  | Examples             | "Forward" kinematic equations (cf [@CamX96tr])                                 | "Reverse" equations                                                          | Admissibility cond.                                     |
+:=====:+:====================:+:==============================================================================:+:============================================================================:+:=======================================================:+
| (3,0) |   -------------      |   ---------------------------------------------------------------------------- | $\begin{array}{ccl}                                                          |   ---------------------------                           |
|       |       Omni-          |                               $\begin{array}{ccl}                              |         \theta&\in& \mathscr{D}^2 \textrm{ (arbitrary)}\\                    |    $(x,y) \in \mathscr{D}^2$                            |
|       |    directional       |              (\dot x,\dot y)^\top&=&\mathbf{R}(\theta)(\eta_1,\eta_2)^\top \\  |         (\eta_1,\eta_2)^\top&=&\mathbf{R}(\theta)^{-1}(\dot x,\dot y)^\top\\ |   ---------------------------                           |
|       |      robots          |                                    \dot \theta&=&\eta_3                        |         \eta_3&=&\dot \theta                                                 |                                                         |
|       |   -------------      |                                       \end{array}$                             |       \end{array}$                                                           |                                                         |
|       |                      |                where $\mathbf{R}(\theta)=\left(\begin{array}{cc}               |                                                                              |                                                         |
|       |                      |                                   \cos\theta&-\sin\theta\\                     |                                                                              |                                                         |
|       |                      |                                    \sin\theta&\cos\theta                       |                                                                              |                                                         |
|       |                      |                                    \end{array}\right)$                         |                                                                              |                                                         |
|       |                      |   ---------------------------------------------------------------------------- |                                                                              |                                                         |
+-------+----------------------+--------------------------------------------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------+
| (2,0) |   --------------     | $\begin{array}{ccl}                                                            | $\begin{array}{ccl}                                                          |   ----------------------------------------------------- |
|       |     Two-wheel        |         \dot x&=&-\eta_1\sin\theta\\                                           |         \theta&=&\mathrm{arctan2}(\dot y,\dot x)\\                           |                 $(x,y) \in \mathscr{D}^2$               |
|       |    differential      |         \dot y&=&\eta_1\cos\theta\\                                            |         \eta_1&=&\sqrt{\dot x^2+\dot y^2}\\                                  |    $\mathrm{arctan2}(\dot y,\dot x) \in \mathscr{D}^2$  |
|       |       drive          |         \dot \theta&=&\eta_2                                                   |         \eta_2&=&\dot \theta                                                 |   ----------------------------------------------------- |
|       |   --------------     |       \end{array}$                                                             |       \end{array}$                                                           |                                                         |
+-------+----------------------+--------------------------------------------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------+
| (2,1) | Unicycle             | $\begin{array}{ccl}                                                            | $\begin{array}{ccl}                                                          |   ---------------------------                           |
|       |                      |         \dot x&=&-\eta_1\sin(\theta+\beta)\\                                   |         \theta&\in& \mathscr{D}^2 \textrm{ (arbitrary)}\\                    |    $(x,y) \in \mathscr{D}^2$                            |
|       |                      |         \dot y&=&\eta_1\cos(\theta+\beta)\\                                    |         \beta&=&\mathrm{arctan2}(\dot y,\dot x)-\theta\\                     |   ---------------------------                           |
|       |                      |         \dot \theta&=&\eta_2\\                                                 |         \eta_1&=&\sqrt{\dot x^2+\dot y^2}\\                                  |                                                         |
|       |                      |         \dot\beta&=&\zeta_1                                                    |         \eta_2&=&\dot \theta\\                                               |                                                         |
|       |                      |       \end{array}$                                                             |         \zeta_1&=&\dot\beta                                                  |                                                         |
|       |                      |                                                                                |       \end{array}$                                                           |                                                         |
+-------+----------------------+--------------------------------------------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------+
| (1,1) |   -----------        | $\begin{array}{ccl}                                                            | $\begin{array}{ccl}                                                          |   ----------------------------------------------------- |
|       |    Bicycle,          |         \dot x&=&-\eta_1L\sin\theta\sin\beta\\                                 |         \theta&=&\mathrm{arctan2}(\dot y,\dot x)\\                           |                 $(x,y) \in \mathscr{D}^2$               |
|       |    kinematic         |         \dot y&=&\eta_1L\cos\theta\sin\beta\\                                  |         \beta&=&\mathrm{arctan2}(\dot y/(L\cos\theta),\dot\theta)\\          |    $\mathrm{arctan2}(\dot y,\dot x) \in \mathscr{D}^2$  |
|       |       car            |         \dot \theta&=&\eta_1\cos\beta\\                                        |         \eta_1&=&\sqrt{\dot x^2+\dot y^2}/(L\sin\beta)\\                     |   ----------------------------------------------------- |
|       |   -----------        |         \dot\beta&=&\zeta_1                                                    |         \zeta_1&=&\dot\beta                                                  |                                                         |
|       |                      |       \end{array}$                                                             |       \end{array}$                                                           |                                                         |
+-------+----------------------+--------------------------------------------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------+
| (1,2) |   ------------------ | $\begin{array}{ccl}                                                            | $\begin{array}{ccl}                                                          |   ---------------------------                           |
|       |         Kludge       |         \dot x&=&-\eta_1(2L\cos\theta\sin\beta_1\sin\beta_2\\                  |         \theta&\in& \mathscr{D}^2 \textrm{ (arbitrary)}\\                    |    $(x,y) \in \mathscr{D}^2$                            |
|       |         robot        |         &&+L\sin\theta\sin(\beta_1+\beta_2))\\                                 |         \beta_1&=&\mathrm{arctan2}(\dot x\cos\theta+\dot y\sin\theta,\\      |   ---------------------------                           |
|       |    (cf [@CamX96tr])  |         \dot y&=&-\eta_1(2L\sin\theta\sin\beta_1\sin\beta_2\\                  |         &&2L\dot\theta-\dot x\sin\theta+\dot y\cos\theta)\\                  |                                                         |
|       |   ------------------ |         &&-L\cos\theta\sin(\beta_1+\beta_2))\\                                 |         \beta_1&=&\mathrm{arctan2}(\dot x\cos\theta+\dot y\sin\theta,\\      |                                                         |
|       |                      |         \dot \theta&=&\eta_1\sin(\beta_2-\beta_1)\\                            |         &&-2L\dot\theta-\dot x\sin\theta+\dot y\cos\theta)\\                 |                                                         |
|       |                      |         \dot\beta_1&=&\zeta_1\\                                                |         \eta_1&=&\dot\theta/\sin(\beta_2-\beta_1)\\                          |                                                         |
|       |                      |         \dot\beta_2&=&\zeta_2                                                  |         \zeta_1&=&\dot\beta_1\\                                              |                                                         |
|       |                      |       \end{array}$                                                             |         \zeta_2&=&\dot\beta_2                                                |                                                         |
|       |                      |                                                                                |   \end{array}$                                                               |                                                         |
+-------+----------------------+--------------------------------------------------------------------------------+------------------------------------------------------------------------------+---------------------------------------------------------+
:::

For each type of robot, we now characterize the admissible base-space trajectories given the spaces of admissible commands assumed in the previous section. The reader is referred to Table [\[tab:wheeled\]](#tab:wheeled){reference-type="ref" reference="tab:wheeled"} for the necessary notations and equations.

### Type (3,0) {#sec:30}

Consider $(\eta_1,\eta_2,\eta_3)\in\mathscr{D}^1$. The third "forward" kinematic equation ($\dot\theta=\eta_3$) implies that $\theta\in\mathscr{D}^2$. The first and the second forward equations then imply that $x\in\mathscr{D}^2$ and $y\in\mathscr{D}^2$.

Conversely, consider a base-space trajectory $\mathcal{C}=(x,y)\in\mathscr{D}^2$. One can choose an arbitrary function $\theta\in\mathscr{D}^2$ and then compute $(\eta_1,\eta_2,\eta_3)\in\mathscr{D}^1$ by the "reverse" equations.

In summary, a base-space trajectory of a (3,0) wheeled robot is admissible if and only if it belongs to $\mathscr{D}^2$.

### Type (2,0) {#sec:20}

Consider $(\eta_1,\eta_2)\in\mathscr{D}^1$. As previously, the forward equations imply that $x$ and $y$ belong to $\mathscr{D}^2$.

Conversely, consider a base-space trajectory $\mathcal{C}=(x,y)\in\mathscr{D}^2$. One can then compute $\theta$ by the first reverse equation $\theta=\mathrm{arctan2}(\dot y,\dot x)$ where $$\mathrm{arctan2}(b,a)=\left\{
    \begin{array}{cc}
      \pi/2 & \textrm{if $a=0$ and $b\geq0$}\\
      -\pi/2 & \textrm{if $a=0$ and $b<0$}\\
      \arctan(b/a) & \textrm{if $a\neq 0$}
    \end{array} \right..$$ Remark that the so-calculated $\theta$ belongs to $\mathscr{D}^1$, but not necessarily to $\mathscr{D}^2$. Next, one can compute $\eta_2$ by the third reverse equation. For $\eta_2$ to be in $\mathscr{D}^1$, one would need $\theta\in\mathscr{D}^2$. As just remarked, the latter condition is *not automatically* guaranteed by $\mathcal{C}=(x,y)\in\mathscr{D}^2$. On the other hand, demanding that $\mathcal{C}=(x,y)\in\mathscr{D}^3$ would be unduly restrictive. Thus the condition $\theta\in\mathscr{D}^2$ must be specified as an independent supplementary condition.

In summary, a base-space trajectory $\mathcal{C}$ of a (2,0) robot is admissible if and only if it belongs to $\mathscr{D}^2$, *and* if the function $\theta$ -- as computed from $\mathcal{C}$ by the first reverse equation -- also belongs to $\mathscr{D}^2$.

Note that these admissibility conditions can also be formulated in terms of continuity constraints on the path curvature [@BoiX94inria; @FS04tr].

### Type (2,1) {#sec:21}

Consider $(\eta_1,\eta_2)\in\mathscr{D}^1$ and $\zeta\in\mathscr{D}^0$. The third and fourth forward equations imply that $\theta$ and $\beta$ belong respectively to $\mathscr{D}^2$ and $\mathscr{D}^1$. Next, the first and second forward equations imply that $x$ and $y$ belong to $\mathscr{D}^2$.

Conversely, consider a base-space trajectory $\mathcal{C}=(x,y)\in\mathscr{D}^2$. One can choose an arbitrary function $\theta\in\mathscr{D}^2$ and then compute successively $\beta\in\mathscr{D}^1$, $(\eta_1,\eta_2)\in\mathscr{D}^1$, and $\zeta\in\mathscr{D}^0$ by the reverse equations.

In summary, as for (3,0) robots, a base-space trajectory of a (2,1) robot is admissible if and only if it belongs to $\mathscr{D}^2$.

### Type (1,1) {#sec:11}

As previously, a necessary condition for the admissibility of a base-space trajectory is that it belongs to $\mathscr{D}^2$. Conversely, consider $\mathcal{C}=(x,y)\in\mathscr{D}^2$. The first reverse equation allows to compute $\theta\in\mathscr{D}^1$. Remark that, as for $(2,0)$ robots, the so-calculated $\theta$ does not necessarily belong to $\mathscr{D}^2$. Next, $\beta$ can be computed from the second reverse equation. Remark that the derivative of $\theta$ is used in the computation of $\beta$, such that $\beta$ belongs to $\mathscr{D}^0$, but not necessarily to $\mathscr{D}^1$. However, in order to compute next $\zeta$, one needs $\beta\in\mathscr{D}^1$, and consequently $\theta\in\mathscr{D}^2$.

In summary, as for (2,0) robots, a base-space trajectory $\mathcal{C}$ of a (1,1) robot is admissible if and only if it belongs to $\mathscr{D}^2$, *and* if the function $\theta$ -- as computed from $\mathcal{C}$ by the first reverse equation -- also belongs to $\mathscr{D}^2$.

### Type (1,2) {#sec:12}

This type of robots can be treated in the same way as (3,0) and (2,1) robots. A base-space trajectory of a (1,2) robot is admissible if and only if it belongs to $\mathscr{D}^2$.

### Summary {#sec:sum}

Following the previous development, one can divide wheeled robots in two classes. Class I comprises robots of type (3,0), (2,1), and (1,2), or in other words, those whose *degrees of maneuvrability* [@CamX96tr] equal 3. A base-space trajectory for robots of this class is admissible if and only if it belongs to $\mathscr{D}^2$.

Class II comprises robots of type (2,0) and (1,1), or in other words, those whose *degrees of maneuvrability* equal 2. A base-space trajectory $\mathcal{C}=(x,y)$ for robots of this class is admissible if and only if it belongs to $\mathscr{D}^2$ *and* if the function $\theta=\mathrm{arctan2}(\dot y,\dot x)$ also belongs to $\mathscr{D}^2$.

**Important remark:** From a computational viewpoint, if one obtains an admissible base-space trajectory $\mathcal{C}'(t)_{t\in[0,T]}$ (for instance by deforming a given $\mathcal{C}(t)_{t\in[0,T]}$), the reverse equations allow to easily compute the commands that generate that trajectory by some differentiations and elementary operations. $\triangle$

**Relationship with flatness theory:** Our approach here bears some resemblance with flatness theory [@FliX95ijc]. In both cases, a reduced set of variables is manipulated (here: the base variables; in flatness theory: the flat outputs) and the state of the other variables are subsequently recovered from this reduced set (here: using the reverse equations). There are however two important differences. First, in our approach, certain non-base variables, in some systems, are not computed from the base variables but chosen arbitrarily: e.g. the orientation $\theta$ in wheeled robots of class I (see above) or the roll angle $\phi$ in the underwater vehicle (see section [4.2](#sec:uwv-traj){reference-type="ref" reference="sec:uwv-traj"}). Second, in some systems, certain non-base variables are computed from the base variables using *integration*: e.g. the orientation $\theta_i$ ($i>0$) of the trailers (see section [5.1](#sec:trailers){reference-type="ref" reference="sec:trailers"}). In flatness theory, *all* non-base variables must be computed from the flat outputs, and they must be done so using only differentiations and algebraic operations.

Finally, note that it could be interesting to study affine deformations of the trajectories of the flat outputs. $\triangle$

## Class I robots {#sec:class1}

We now characterize the affine deformations that preserve the admissibility of base-space trajectories for robots of class I. Using this characterization, we then suggest practical algorithms for trajectory correction.

### Admissible deformations {#sec:uni-addef}

Consider an admissible base-space trajectory $\mathcal{C}(t)_{t\in[0,T]}$ and an affine deformation $\mathcal{F}$ occurring at time $\tau$ that deforms $\mathcal{C}$ into $\mathcal{C}'$. In what follows, we note $v=\sqrt{\dot x^2+\dot
  y^2}$ (the linear velocity of the robot) and $\theta=\mathrm{arctan2}(\dot
y,\dot x)$ (its orientation). Note that, following section [3.2.6](#sec:sum){reference-type="ref" reference="sec:sum"}, $\mathcal{C}$ is admissible if and only if $(x,y)\in\mathscr{D}^2$, i.e., if and only if $(v,\theta)\in\mathscr{D}^1$. Note also that the function $\theta$ here is not the same as the $\theta$ chosen arbitrarily in Table [\[tab:wheeled\]](#tab:wheeled){reference-type="ref" reference="tab:wheeled"}. For instance, the unicycle described by equations ([\[eq:unicycle\]](#eq:unicycle){reference-type="ref" reference="eq:unicycle"}) is a in fact a (2,1) robot, with the following correspondance between the variables $$\begin{equation}
  \left\{
    \begin{array}{ccc}
    \theta_\mathrm{robot} &=& 0\\
    \beta_\mathrm{robot} &=& \theta_\mathrm{unicycle}-\pi/2\\
    {\eta_1}_\mathrm{robot} &=& v_\mathrm{unicycle}\\
    {\eta_2}_\mathrm{robot} &=& 0\\
    \zeta_\mathrm{robot} &=& \omega_\mathrm{unicycle}
    \end{array}
    \right..
\end{equation}$$

One has first, by definition, $\mathcal{C}'(t)_{t\in(\tau,T]}=\mathcal{F}(\mathcal{C}(t)_{t\in(\tau,T]})$. Since $\mathcal{F}$ is a smooth application, it is clear that $\mathcal{C}'(t)_{t\in(\tau,T]}$ -- note that the interval is open at $\tau$ -- is in $\mathscr{D}^2$ if and only if $\mathcal{C}(t)_{t\in(\tau,T]}$ is in $\mathscr{D}^2$.

Regarding the time instant $\tau$, the continuities of $x$ and $y$ impose that $\mathcal{F}(\mathcal{C}(\tau))=\mathcal{C}(\tau)$. Thus $\mathcal{F}$ can be written in the form $$\begin{equation}
\label{eq:f}
\forall P\in\mathbb{A} \quad \mathcal{F}(P)=\mathcal{C}(\tau)+
\mathcal{M}(\overrightarrow{\mathcal{C}(\tau)P}).
\end{equation}$$

One now needs to guarantee the *continuities* of $v$ and $\theta$ at $\tau$, since the two remaining conditions (differentiability and finite limits for the derivative) do not depend on the behavior of $\mathcal{C}'$ at the discrete point $\tau$, and are therefore already satisfied by virtue of the smoothness of $\mathcal{F}$.

Consider the velocity *vector* $\mathbf{v}=(\dot{x},\dot{y})^\top$. Remark that the continuity of this velocity vector is equivalent to those of $v$ and $\theta$. The continuity of $\mathbf{v}$ means that $\mathbf{v}(\tau-)$ and $\mathbf{v}(\tau+)$ (where the signs $-$ and $+$ denote respectively the left and right limits) are well defined, and that $\mathbf{v}(\tau-)=\mathbf{v}(\tau+)=\mathbf{v}(\tau)$.

Similarly, the continuity of $\mathbf{v}'$ would mean $\mathbf{v}'(\tau+)=\mathbf{v}'(\tau-)=\mathbf{v}(\tau)$. On the other hand, one has $\mathbf{v}'(\tau+)=\mathcal{M}(\mathbf{v}(\tau))$. These equalities together imply $\mathcal{M}(\mathbf{v}(\tau))=\mathbf{v}(\tau)$.

Let us now decompose $\mathcal{M}$ is the basis $\{\mathbf{u}_\parallel,\mathbf{u}_\perp\}$ where $\mathbf{u}_\parallel=(\cos(\theta),\sin(\theta))^\top$ is the unit tangent vector and $\mathbf{u}_\perp=(-\sin(\theta),\cos(\theta))^\top$ is the unit normal vector. The condition $\mathcal{M}(\mathbf{v}(\tau))=\mathbf{v}(\tau)$ is equivalent to $$\begin{equation}
  \label{eq:uni-adm}
  \exists \lambda,\mu \in \mathbb{R} \quad \mathbf{M}=\left(
    \begin{array}{rcl}
      1&\lambda\\
      0&1+\mu
    \end{array}
  \right),
\end{equation}$$ where $\mathbf{M}$ is the matrix representing $\mathcal{M}$ in the basis $\{\mathbf{u}_\parallel,\mathbf{u}_\perp\}$.

In summary, the admissible affine transformations at time $\tau$ form a Lie group of dimension 2, parameterized by $\lambda$ and $\mu$ in equation ([\[eq:uni-adm\]](#eq:uni-adm){reference-type="ref" reference="eq:uni-adm"})

### Trajectory correction {#sec:trajcor}

We consider only the correction of the final position and assume that $\tau$ is given. It is possible to achieve more complex corrections (e.g. correcting the final orientation) or to choose "optimal" $\tau$s: these developments are left to the reader.

From equation ([\[eq:f\]](#eq:f){reference-type="ref" reference="eq:f"}), to correct the final position $\mathcal{C}(T)$ towards a desired position $P_d=(x_d,y_d)$, one needs to look for a linear application $\mathcal{M}$ such that $$\begin{equation}
\label{eq:m}
\mathcal{M}(\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)})=\overrightarrow{\mathcal{C}(\tau)P_d}.
\end{equation}$$ Let $\mathbf{Q}=[\mathbf{u}_\|,\mathbf{u}_\perp]$ and let the matrix representing $\mathcal{M}$ in the basis $\{\mathbf{u}_\|,\mathbf{u}_\perp\}$ be $$\mathbf{M}=\left(\begin{array}{cc}
1&\lambda\\
0&1+\mu\\
\end{array} \right).$$ Equation ([\[eq:m\]](#eq:m){reference-type="ref" reference="eq:m"}) implies $$\begin{equation}
  \label{eq:uni-cond}
  \mathbf{Q}\mathbf{M}\mathbf{Q}^{-1} \left(\begin{array}{c}
x(T)-x(\tau)\\
y(T)-y(\tau)\\
\end{array} \right)
  = \left(\begin{array}{c}
x_d-x(\tau)\\
y_d-y(\tau)\\
\end{array} \right).
\end{equation}$$ Let next $$\left(\begin{array}{c}
x_1\\
y_1\\
\end{array} \right) =
\mathbf{Q}^{-1} \left(\begin{array}{c}
x(T)-x(\tau)\\
y(T)-y(\tau)\\
\end{array} \right),$$ $$\left(\begin{array}{c}
x_2\\
y_2\\
\end{array} \right) =
\mathbf{Q}^{-1} \left(\begin{array}{c}
x_d-x(\tau)\\
y_d-y(\tau)\\
\end{array} \right).$$ Equation ([\[eq:uni-cond\]](#eq:uni-cond){reference-type="ref" reference="eq:uni-cond"}) then implies $$\lambda=(x_2-x_1)/y_1,
\quad
\mu=(y_2-y_1)/y_1,$$ provided that $y_1\neq 0$, i.e. that the tangent at $\tau$ does not go through $\mathcal{C}(T)$ (see also discussion in section [3.4.2](#sec:pos){reference-type="ref" reference="sec:pos"}). Fig. [8](#fig:uni){reference-type="ref" reference="fig:uni"} shows examples of trajectory corrections for the unicycle.

Note that any desired position in the whole space -- and not only those in the vicinity of the initially planned final position as in [@SeiX10wafr] -- can theoretically be reached. Remark on the other hand that the distance (e.g. the $L_2$ distance) of the corrected *trajectory* from the original trajectory is a continuous function of $\lambda$ and $\mu$, meaning that using small $\lambda$s and $\mu$s results in small changes in the overall trajectory (and in the commands).

## Class II robots {#sec:class2}

### Admissible deformations {#admissible-deformations}

Consider an admissible base-space trajectory $\mathcal{C}$ of a class II robot and an affine deformation $\mathcal{F}$ occurring at time $\tau$ that deforms $\mathcal{C}$ into $\mathcal{C}'$. In what follows, we note $v=\sqrt{\dot x^2+\dot
  y^2}$ (the linear velocity of the robot), $\theta=\mathrm{arctan2}(\dot y,\dot
x)$ (its orientation), and $\omega=\dot\theta$ (its angular velocity). Note that, following section [3.2.6](#sec:sum){reference-type="ref" reference="sec:sum"}, $\mathcal{C}$ is admissible if and only if $v\in\mathscr{D}^1$ and $\omega\in\mathscr{D}^1$.

Following the same reasoning as in section [3.3.1](#sec:uni-addef){reference-type="ref" reference="sec:uni-addef"}, one can show that $\mathcal{C}'(t)_{t\in(\tau,T]}$ is in $\mathscr{D}^2$ if and only if $\mathcal{F}(\mathbf{v}(\tau))=\mathbf{v}(\tau)$, where $\mathbf{v}(\tau)$ is is the velocity vector at $\tau$. One now needs to check the continuities of $\omega'$ at $\tau$ and at the discontinuity points of the second derivative of $\mathcal{C}$ (the continuity and differentiability of $\omega'$ elsewhere are already guaranteed by the smoothness of $\mathcal{F}$, cf. section [3.3.1](#sec:uni-addef){reference-type="ref" reference="sec:uni-addef"}).

Consider for this the acceleration vector $\mathbf{a}
=(\ddot{x},\ddot{y})^\top$. By definition, one has $$\mathbf{a}=a\mathbf{u}_\parallel+v\omega\mathbf{u}_\perp,$$ with $\mathbf{a}$ not necessarily continuous. One can next write $$\begin{equation}
  \label{eq:a}
  \mathbf{a}\cdot\mathbf{u}_\perp=v\omega.
\end{equation}$$

Consider now a time instant $t>\tau$ when $\mathbf{a}$ is possibly discontinuous, that is $\mathbf{a}(t-)\neq\mathbf{a}(t+)$. Since $\omega$ and $v$ are continuous, one has by equation ([\[eq:a\]](#eq:a){reference-type="ref" reference="eq:a"}) $$\mathbf{a}(t-)\cdot\mathbf{u}_\perp(t)=\mathbf{a}(t+)\cdot\mathbf{u}_\perp(t),$$ or, in other words, that $\mathbf{a}(t+)-\mathbf{a}(t-)$ and $\mathbf{u}_\parallel(t)$ are collinear. Here comes into play a nice property of affine transformations: they preserve collinearity. Using this property, one obtains that $\mathcal{M}(\mathbf{a}(t+)-\mathbf{a}(t-))$ and $\mathcal{M}(\mathbf{u}_\parallel(t))$ are collinear. But the former vector is no other than $\mathbf{a}'(t+)-\mathbf{a}'(t-)$ and the latter is collinear with $\mathbf{u}'_\parallel(t)$, since $$\mathbf{u}'_\parallel(t)=\frac{\mathcal{M}(\mathbf{u}_\parallel(t))}{\|\mathcal{M}(\mathbf{u}_\parallel(t))\|}.$$ Thus $\mathbf{a}'(t-)\cdot\mathbf{u}'_\perp(t)=\mathbf{a}'(t+)\cdot\mathbf{u}'_\perp(t)$, which in turn implies the continuity of $\omega'$ at $t$ (note that this conclusion also relies on the fact that $v'$ is nonzero if $v$ is nonzero, owing to the non-singularity of $\mathcal{M}$).

**Remark:** Since the affine group is the largest transformation group of the plane that preserves collinearity, the previous development shows that it is also the largest group that preserves the admissibility of every trajectory of a class II robot! $\triangle$

Turning now to the time instant $\tau$, the same reasoning as previously shows that $\omega'$ is continuous at $\tau$ if and only if $$\mathbf{a}'(\tau+)\cdot\mathbf{u}_\perp(\tau)=\mathbf{a}(\tau)\cdot\mathbf{u}_\perp(\tau),$$ or equivalently, if $$\begin{equation}
  \label{eq:ii}
  \mathcal{M}(\mathbf{a}(\tau))\cdot\mathbf{u}_\perp(\tau)=\mathbf{a}(\tau)\cdot\mathbf{u}_\perp(\tau).
\end{equation}$$

Remark now that, since $\mathbf{v}\cdot\mathbf{u}_\perp=0$, condition ([\[eq:ii\]](#eq:ii){reference-type="ref" reference="eq:ii"}) is in fact equivalent to $$\exists \lambda\in\mathbb{R} \quad \mathcal{M}(\mathbf{a}(\tau))=\mathbf{a}(\tau)+\lambda\mathbf{v}(\tau).$$

Denoting by $\mathcal{B}$ the linear application such that $\mathcal{B}(\mathbf{v}(\tau))=\mathbf{0}$ and $\mathcal{B}(\mathbf{a}(\tau))=\mathbf{v}(\tau)$ (one can compute $\mathcal{B}$ explicitly by $\mathcal{B}=[\mathbf{0},\mathbf{v}(\tau)][\mathbf{v}(\tau),\mathbf{a}(\tau)]^{-1}$), one obtains $$\exists \lambda\in\mathbb{R} \quad \mathcal{M}=\mathcal{I}+\lambda\mathcal{B},$$ where $\mathcal{I}$ is the identity application.

In summary, the admissible affine transformations at time $\tau$ form a Lie group of dimension 1, given by $\{\mathcal{I}+\lambda\mathcal{B}\}_{\lambda\in\mathbb{R}}$.

**Inflection points:** The previous development is valid only when $\mathbf{v}(\tau)$ and $\mathbf{a}(\tau)$ are non-collinear, that is, when $\mathcal{C}(\tau)$ is not an *inflection point* (see also [@BenX09pcb] for an interesting discussion on inflection points in the context of human movements). $\triangle$

### Trajectory correction I: position correction using one affine deformation {#sec:pos}

Let us now play with $\tau$ and the "extra degree of freedom" $\lambda$ to make trajectory corrections.

For this, we first study how the final position of the trajectory $\mathcal{C}(T)$ is affected by an admissible affine deformation occurring at time $\tau$. By definition, one has $$\begin{array}{rcl}
  \mathcal{C}'(T)&=&\mathcal{C}(\tau)+(\mathcal{I}+\lambda\mathcal{B})(\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)})\\
  &=&\mathcal{C}(T)+\lambda\mathcal{B}(\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)}).
\end{array}$$

Let us decompose $\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)}$ in the (in general non-orthonormal) basis $\{\mathbf{v}(\tau),\mathbf{a}(\tau)\}$ $$\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)}=\gamma \mathbf{v}(\tau) + \delta \mathbf{a}(\tau).$$

By definition of $\mathcal{B}$, one has $$\begin{equation}
  \label{eq:endpoint}
  \mathcal{C}'(T)=\mathcal{C}(T)+\lambda\delta\mathbf{v}(\tau).
\end{equation}$$ Consequently, if $\delta$ is nonzero (that is, if $\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)}$ and $\mathbf{v}(\tau)$ are non-collinear, or in other words, if the tangent at $\tau$ does not go through $\mathcal{C}(T)$), then the locus of $\mathcal{C}'(T)$ when $\lambda$ varies is the line that goes through $\mathcal{C}(T)$ and that collinear with $\mathbf{v}(\tau)$.

In order to make a correction of the final position from $\mathcal{C}(T)$ to a desired position $P_d$, it therefore suffices to

1.  compute the vector $\mathbf{e}_d=\overrightarrow{\mathcal{C}(T)P_d}$;

2.  find a time instant $\tau$ when the tangent $\mathbf{u}_\parallel(\tau)$ is collinear with $\mathbf{e}_d$;

3.  compute $\lambda=\overline{\mathbf{e}_d}/(\delta\overline{\mathbf{v}(\tau)})$ where the overline denotes the signed norm;

4.  make the affine deformation of parameter $\lambda$ at time $\tau$.

Fig. [2](#fig:pos){reference-type="ref" reference="fig:pos"} shows some examples of trajectory correction for a kinematic car, which is a robot of type (1,1). The equation of a kinematic car is given by [@Lau98book] $$\begin{equation}
  \label{eq:kincar}
  \left\{
    \begin{array}{ccc}
      \dot{x} & = & v\cos(\theta)\\
      \dot{y} & = & v\sin(\theta)\\
      \dot{\theta} & = & \frac{v\tan(\beta)}{L}\\
      \dot{\beta}&=&\zeta\\    
    \end{array} \right.,
\end{equation}$$ which can be put in the form of a robot of type (1,1) (cf. Table [\[tab:wheeled\]](#tab:wheeled){reference-type="ref" reference="tab:wheeled"}) using the following correspondance between the variables $$\begin{equation}
  \left\{
    \begin{array}{ccc}
      \theta_\mathrm{robot} &=& \theta_\mathrm{car}-\pi/2\\
      \beta_\mathrm{robot} &=& \pi/2-\beta_\mathrm{car}\\
      {\eta_1}_\mathrm{robot} &=&
      v_\mathrm{car}/(L\cos\beta_\mathrm{car})\\
      \zeta_\mathrm{robot} &=& -\zeta_\mathrm{car}
    \end{array}
  \right..
\end{equation}$$

:::: {#fig:pos .figure latex-placement="ht"}
![image](Pham2011Affine_figs/correct_pos_xy.png){height="5cm"} ![image](Pham2011Affine_figs/correct_pos_other.png){height="5cm"}

::: caption
Accessible final positions (in cyan) and two examples of position corrections. The original trajectory is in red. For each correction, the black plain line represents the tangent at $\tau$ while the black dotted line joins the original final position $\mathcal{C}(T)$ to the desired final position $P_d$. Note the collinearity of the plain line and the dotted line.
:::
::::

**Accessible positions:** From the previous development, it appears that a position $P_d$ is accessible if and only if the original trajectory $\mathcal{C}(t)_{t\in[0,T]}$ has a tangent that is parallel to $\overrightarrow{\mathcal{C}(T)P_d}$. Therefore the set of the trajectory tangents (minus the tangents at the inflection points) determine the accessible directions for position corrections, as shown in Fig. [2](#fig:pos){reference-type="ref" reference="fig:pos"}. $\triangle$

### Trajectory correction II: orientation correction using one affine deformation {#sec:or}

Remark that, if $\delta=0$ in equation ([\[eq:endpoint\]](#eq:endpoint){reference-type="ref" reference="eq:endpoint"}), the final position $\mathcal{C}(T)$ does not move when $\lambda$ varies. However, the final *orientation* does vary with $\lambda$. Exploiting this fact, one can make corrections to the final orientation without changing the final position.

As remarked earlier, $\delta=0$ when $\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)}$ and $\mathbf{v}(\tau)$ are collinear, that is, when the tangent line at time $\tau$ goes through $\mathcal{C}(T)$. Consequently, in order to make a correction of the final tangent vector from $\mathbf{u}_\parallel(T)$ to a desired tangent vector $\mathbf{u}_d$ while keeping the final position unchanged, it suffices to (see Fig. [3](#fig:or){reference-type="ref" reference="fig:or"}A)

1.  find a time instant $\tau$ such that the tangent line at $\tau$ goes through $\mathcal{C}(T)$;

2.  compute the appropriate $\lambda$ (see below);

3.  make the affine deformation of parameter $\lambda$ at time $\tau$.

:::::: {#fig:or .figure latex-placement="ht"}
::: minipage
**A**\
![image](Pham2011Affine_figs/correct_or.png){width="4cm"}
:::

::: minipage
**B**\
![image](Pham2011Affine_figs/compute_lambda_or.png){width="3cm"}
:::

::: caption
**A**: accessible final orientations (in cyan) and two examples of orientation corrections. The black line represents the tangent at $\tau$. Note that the black line goes through the final position, which remains unchanged by the orientation corrections. **B**: illustration for the computation of $\lambda$ in the correction of the final orientation.
:::
::::::

**Computation of $\lambda$:** Remark that the final orientation of the deformed trajectory is given by the vector $\mathcal{M}(\mathbf{u}_\parallel(T))$. Observe next that $$\mathcal{M}(\mathbf{u}_\parallel(T))=\mathbf{u}_\parallel(T)+\lambda\delta_u\mathbf{v}(\tau)$$ where $\delta_u$ is the coefficient multiplying $\mathbf{a}(\tau)$ in the decomposition of $\mathbf{u}_\parallel(T)$ in the basis $\{\mathbf{v}(\tau),\mathbf{a}(\tau)\}$.

Consider the intersection $I$ between the line containing $\mathbf{u}_d$ and the line parallel to $\mathbf{v}$ and which goes through the tip of $\mathbf{u}_\parallel(T)$ (see illustration in Fig. [3](#fig:or){reference-type="ref" reference="fig:or"}B). The directed distance between $I$ and the tip of $\mathbf{u}_\parallel(T)$ is given by $$d=\frac{\sin(\widehat{\mathbf{v}(\tau),\mathbf{u}_\parallel(T)})}
{\tan(\widehat{\mathbf{v}(\tau),\mathbf{u}_d})}
-\cos(\widehat{\mathbf{v}(\tau),\mathbf{u}_\parallel(T)}).$$ The appropriate $\lambda$ must then satisfy $$\lambda\delta_u\overline{\mathbf{v}(\tau)}=d,$$ which leads to $\lambda=d/(\delta_u\overline{\mathbf{v}(\tau)})$. $\triangle$

**Accessible orientations:** The accessible orientations are restricted to the half-circle defined by the tangent line and in which lies $\theta(T)$, as shown in Fig. [3](#fig:or){reference-type="ref" reference="fig:or"}A. Note that different choices of the tangent lines (when there exist more than one possible tangent line) induce different sets of accessible orientations, whose union forms the total set of accessible orientations. Note that the tangents at the inflection points are also forbidden here. $\triangle$

### Trajectory correction III: position correction using *two* affine deformations

One can in fact *compose* several affine deformations to achieve more powerful trajectory corrections. In particular, composing two deformations allows making position correction towards any desired final position in space, *so long as the initial trajectory $\mathcal{C}$ is not a straight line*, as follows (see Fig. [4](#fig:2steps){reference-type="ref" reference="fig:2steps"})

1.  select two (non-inflection) time instants $\tau_1$ and $\tau_2$, with $\tau_1<\tau_2$, such that $\mathbf{v}(\tau_1)$ and $\mathbf{v}(\tau_2)$ are non-collinear. Such two time instants exist since $\mathcal{C}$ is not a straight line;

2.  decompose $\overrightarrow{\mathcal{C}(T)P_d}$ in the basis $\{\mathbf{v}(\tau_1),\mathbf{v}(\tau_2)\}$ as $\overrightarrow{\mathcal{C}(T)P_d}=
      \alpha_1\mathbf{v}(\tau_1)+\alpha_2\mathbf{v}(\tau_2)$;

3.  apply a first deformation on $\mathcal{C}$ at $\tau_2$ to obtain $\mathcal{C}'$, with $\mathcal{C}'(T)=\mathcal{C}(T)+\alpha_2\mathbf{v}(\tau_2)$;

4.  apply a second deformation on $\mathcal{C}'$ at $\tau_1$ to obtain $\mathcal{C}''$, with $\mathcal{C}''(T)=\mathcal{C}'(T)+\alpha_1\mathbf{v}(\tau_1)$. By construction $\mathcal{C}''(T)=\mathcal{C}(T)+\alpha_2\mathbf{v}(\tau_2)+\alpha_1\mathbf{v}(\tau_1)=P_d$.

:::: {#fig:2steps .figure latex-placement="ht"}
![image](Pham2011Affine_figs/two_xy.png){height="5cm"} ![image](Pham2011Affine_figs/two_other.png){height="5cm"}

::: caption
Position correction using two successive affine deformations. Note that the desired final position at $P_d=(20,40)$ is not accessible by any single deformation because the initial trajectory $\mathcal{C}$ (red) has no tangent parallel with the line $\mathcal{C}(T)P_d$ (yellow line). To overcome this, $\mathcal{C}$ is first deformed into $\mathcal{C}'$ (blue), which in turn is deformed into $\mathcal{C}''$ (green).
:::
::::

It is crucial that the deformation at $\tau_2$ is made first (and the deformation at $\tau_1$ only second) so as to leave the velocity vector at $\tau_1$ unchanged ($\mathbf{v}'(\tau_1)=\mathbf{v}(\tau_1)$).

### Trajectory correction IV: position and orientation correction using *three* affine deformations {#sec:3steps}

Composing *three* affine deformations allows achieving both the desired final position and orientation as follows (see Fig. [5](#fig:3steps){reference-type="ref" reference="fig:3steps"})

1.  select three (non-inflection) time instants $\tau_1$, $\tau_2$, and $\tau_3$ with $\tau_1<\tau_2<\tau_3$, such that $\mathbf{v}(\tau_1)$, $\mathbf{v}(\tau_2)$ and $\mathbf{v}(\tau_3)$ are pairwise non-collinear. Such three time instants exist since $\mathcal{C}$ is not a straight line;

2.  apply a first deformation on $\mathcal{C}$ at $\tau_3$ to obtain $\mathcal{C}'$, with $\mathcal{C}'(T)=\mathcal{C}(T)+\alpha_3\mathbf{v}(\tau_3)$, where $\alpha_3$ is a coefficient to be tuned later;

3.  following the results of the previous section, one can use the second and third deformations to correct back to the desired position $\mathcal{C}'''(T)=P_d$. Remark that the final *orientation* of $\mathcal{C}'''$ depends on $\alpha_3$ as shown in Fig. [5](#fig:3steps){reference-type="ref" reference="fig:3steps"}. The formula to algebraically compute $\alpha_3$ as a function of the desired final orientation can be obtained in a similar way as in section [3.4.3](#sec:or){reference-type="ref" reference="sec:or"}.

:::: {#fig:3steps .figure latex-placement="ht"}
![image](Pham2011Affine_figs/three_a.png){height="5cm"} ![image](Pham2011Affine_figs/three_b.png){height="5cm"}

::: caption
Position and orientation correction using three successive affine deformations. The left and right plots correspond to two different values of $\alpha_3$. Remark that the trajectory $\mathcal{C}'''$ (magenta) ends at the same position ($P_d=(20,40)$) in the left and right plots, but that its final orientation differs significantly between the two plots. By varying $\alpha_3$, it is thus possible to cover a large range of possible desired final orientations while keeping the desired final position fixed.
:::
::::

Finally, remark that one can also set the final linear speed to arbitrary values while keeping the final position and orientation unchanged by using the extension technique of section [5.4](#sec:gap){reference-type="ref" reference="sec:gap"}.

# Affine trajectory correction for a tridimensional underwater vehicle {#sec:uwv}

## Model description

A tridimensional underwater vehicle can be modeled by the following equations [@NS92icra] $$\begin{equation}
  \label{eq:uwv}
  \left\{
    \begin{array}{ccc}
      \dot{x} & = & v\cos\psi\cos\theta\\
      \dot{y} & = & v\sin\psi\cos\theta\\
      \dot{z} & = & -v\sin\theta\\
      \left(\begin{array}{c}
          \dot{\phi}\\
          \dot{\theta}\\
          \dot{\psi}
        \end{array} \right)&=&
      \mathbf{R}(\phi,\theta) \left(\begin{array}{c}
          \omega_x\\
          \omega_y\\
          \omega_z
        \end{array} \right)
    \end{array} \right.,
\end{equation}$$ where $(v,\omega_x,\omega_y,\omega_z)$ are the system commands, $(x,y,z,\phi,\theta,\psi)$ the system variables, and $$\mathbf{R}(\phi,\theta)=\left(\begin{array}{ccc}
1&\sin\phi\tan\theta&\cos\phi\tan\theta\\
0&\cos\phi&-\sin\phi\\
0&\sin\phi\sec\theta&\cos\phi\sec\theta
\end{array} \right).$$

We choose $x$, $y$, and $z$ to be the base variables. The base space is thus of dimension 3. The non-base variables are $\phi$, $\theta$, and $\psi$.

As in the case of planar wheeled robots, the admissible commands $v$ are assumed to be in $\mathscr{D}^1$ (allowing possible discontinuities in the linear acceleration). The admissible commands $\omega_x$, $\omega_y$, and $\omega_z$ are assumed to be in $\mathscr{D}^0$.

## Admissible base-space trajectories {#sec:uwv-traj}

Following the same line of reasoning as previously, a necessary condition for the admissibility of a base-space trajectory $\mathcal{C}(t)_{t\in[0,T]}=(x(t),y(t),z(t))_{t\in[0,T]}$ is that $x$, $y$ and $z$ belong to $\mathscr{D}^2$.

Conversely, assume that $x$, $y$ and $z$ belong to $\mathscr{D}^2$. Remark first that, from the system equations ([\[eq:uwv\]](#eq:uwv){reference-type="ref" reference="eq:uwv"}), the "roll" angle $\phi$ is independent of $(x(t),y(t),z(t))_{t\in[0,T]}$. Next, given an arbitrary roll angle profile $\phi(t)_{t\in[0,T]}\in\mathscr{D}^1$, one can safely write the following reverse equations (assuming that the velocity is always strictly positive and that the trajectory stays away from the singularities of the Euler angles [@NS92icra]) $$\left\{
    \begin{array}{ccc}
      \psi&=&\mathrm{arctan2}(\dot{y},\dot{x})\\
      v&=&\sqrt{\dot{x}^2+\dot{y}^2+\dot{z}^2}\\
      \theta&=&\arcsin(\dot{z}/v)\\
      \left(\begin{array}{c}
          \omega_x\\
          \omega_y\\
          \omega_z
        \end{array} \right)&=&
      \mathbf{R}(\phi,\theta)^{-1}
      \left(\begin{array}{c}
          \dot{\phi}\\
          \dot{\theta}\\
          \dot{\psi}
        \end{array} \right)
    \end{array} \right.,$$

In summary, a base-space trajectory is admissible if and only if it is in $\mathscr{D}^2$.

## Admissible affine deformations

Consider now an admissible base-space trajectory $\mathcal{C}$ and an affine deformation $\mathcal{F}$ occurring at time $\tau$ that deforms $\mathcal{C}$ in to $\mathcal{C}'$. As in section [3.3.1](#sec:uni-addef){reference-type="ref" reference="sec:uni-addef"}, one can show that $\mathcal{C}'(t)_{t\in(\tau,T]}$ belongs to $\mathscr{D}^2$, owing to the smoothness of $\mathcal{F}$.

At the time instant $\tau$, the continuities of $x$, $y$ and $z$ impose that $\mathcal{F}(\mathcal{C}(\tau))=\mathcal{C}(\tau)$. Thus $\mathcal{F}$ can be written in the form $$\begin{equation}
  \label{eq:uwv-addef}
  \forall P\in\mathbb{A} \quad \mathcal{F}(P)=\mathcal{C}(\tau)+
  \mathcal{M}(\overrightarrow{\mathcal{C}(\tau)P}).
\end{equation}$$

Next, following again the same reasoning as in section [3.3.1](#sec:uni-addef){reference-type="ref" reference="sec:uni-addef"}, the continuities of $v$, $\psi$ and $\theta$ are equivalent to setting $\mathcal{M}(\mathbf{v}(\tau))=\mathbf{v}(\tau)$.

In summary, an affine deformation $\mathcal{F}$ occurring at time $\tau$ is admissible if and only if $\mathcal{M}(\mathbf{v}(\tau))=\mathbf{v}(\tau)$ when $\mathcal{F}$ is written in the form ([\[eq:uwv-addef\]](#eq:uwv-addef){reference-type="ref" reference="eq:uwv-addef"}). As a consequence, the admissible affine transformations at time $\tau$ form a Lie group of dimension 6.

In practice, we shall compute $\mathcal{M}$ in the basis $\{\mathbf{u}_\|,\mathbf{w}_1,\mathbf{w}_2\}$ where $\mathbf{w}_1$ and $\mathbf{w}_2$ are two arbitrary unit vectors forming an orthonormal basis with $\mathbf{u}_\|$. In this basis, the condition $\mathcal{M}(\mathbf{v}(\tau))=\mathbf{v}(\tau)$ is equivalent to setting the first column of the matrix that represents $\mathcal{M}$ to $(1,0,0)$. It suffices then to find the six remaining coefficients.

## Trajectory correction {#trajectory-correction}

We consider only the correction of the final position, at a given $\tau$. It is possible to achieve more complex corrections as well (correcting the final orientation, avoiding obstacles, etc.) or to optimize the time instant $\tau$: these developments are left to the reader.

Theoretically, three free coefficients are sufficient to reach any final position. As a consequence, we have here more coefficients than needed. We solve this "redundancy" problem by choosing an affine transformation that is the "closest" to the identity matrix, i.e., that affects the least the original trajectory.

As in section [3.3.2](#sec:trajcor){reference-type="ref" reference="sec:trajcor"}, to correct towards a desired position $P_d=(x_d,y_d,z_d)$, one needs to look for a linear application $\mathcal{M}$ such that $$\begin{equation}
\label{eq:m2}
\mathcal{M}(\overrightarrow{\mathcal{C}(\tau)\mathcal{C}(T)})=\overrightarrow{\mathcal{C}(\tau)P_d}.
\end{equation}$$ Let $\mathbf{Q}=[\mathbf{u}_\|,\mathbf{w}_1,\mathbf{w}_2]$ and let the matrix representing $\mathcal{M}$ in the basis $\{\mathbf{u}_\|,\mathbf{w}_1,\mathbf{w}_2\}$ be $$\mathbf{M}=\left(\begin{array}{ccc}
1&\lambda&\mu\\
0&1+\nu&\xi\\
0&\sigma&1+\chi
\end{array} \right).$$ Equation ([\[eq:m2\]](#eq:m2){reference-type="ref" reference="eq:m2"}) implies $$\begin{equation}
  \label{eq:uwv-cond}
  \mathbf{Q}\mathbf{M}\mathbf{Q}^{-1} \left(\begin{array}{c}
x(T)-x(\tau)\\
y(T)-y(\tau)\\
z(T)-z(\tau)
\end{array} \right)
  = \left(\begin{array}{c}
x_d-x(\tau)\\
y_d-y(\tau)\\
z_d-z(\tau)
\end{array} \right).
\end{equation}$$ Let next $$\left(\begin{array}{c}
x_1\\
y_1\\
z_1
\end{array} \right) =
\mathbf{Q}^{-1} \left(\begin{array}{c}
x(T)-x(\tau)\\
y(T)-y(\tau)\\
z(T)-z(\tau)
\end{array} \right),$$ $$\left(\begin{array}{c}
x_2\\
y_2\\
z_2
\end{array} \right) =
\mathbf{Q}^{-1} \left(\begin{array}{c}
x_d-x(\tau)\\
y_d-y(\tau)\\
z_d-z(\tau)
\end{array} \right).$$ Equation ([\[eq:uwv-cond\]](#eq:uwv-cond){reference-type="ref" reference="eq:uwv-cond"}) then implies $$\begin{equation}
  \label{eq:underdet}
  \mathbf{U}
  \left(\begin{array}{c}
      \lambda\\
      \mu\\
      \nu\\
      \xi\\
      \sigma\\
      \chi
    \end{array} \right) =
  \left(\begin{array}{c}
      x_2-x_1\\
      y_2-y_1\\
      z_2-z_1
    \end{array} \right),
\end{equation}$$ where $$\mathbf{U}=\left(\begin{array}{cccccc}
      y_1&z_1&0&0&0&0\\
      0&0&y_1&z_1&0&0\\
      0&0&0&0&y_1&z_1
    \end{array} \right).$$

The $(\lambda,\mu,\nu,\xi,\sigma,\chi)$ with minimal norm (i.e. that yields a $\mathcal{M}$ closest to identity according to the Frobenius distance) and that satisfies the under-determined system ([\[eq:underdet\]](#eq:underdet){reference-type="ref" reference="eq:underdet"}) is given by $$\mathbf{U}^+\left(\begin{array}{c}
      x_2-x_1\\
      y_2-y_1\\
      z_2-z_1
    \end{array} \right),$$ where $\mathbf{U}^+$ denotes the Moore-Penrose pseudo-inverse of $\mathbf{U}$.

Finally, one needs to choose the "independent" angle $\phi(t)_{t\in[\tau,T]}$. Here our strategy consists of keeping the same $\phi$ as in the original trajectory. Other strategies (e.g. keeping the same *absolute* roll as in the original trajectory) can also be used. Fig. [6](#fig:uwv){reference-type="ref" reference="fig:uwv"} shows some examples of trajectory corrections.

:::: {#fig:uwv .figure latex-placement="ht"}
![image](Pham2011Affine_figs/uwv_xyz.png){height="5cm"} ![image](Pham2011Affine_figs/uwv_other.png){height="6cm"}

::: caption
Examples of trajectory corrections for an underwater vehicle. The original trajectory is in red.
:::
::::

# Further applications {#sec:appli}

We now use the trajectory correction algorithms just developped as basic tools to tackle more complex tasks. We mostly use the kinematic car (which is a wheeled robot of type (1,1) and class II, see section [3.2.4](#sec:11){reference-type="ref" reference="sec:11"}) as illustrative example but the following developments can be easily adapted to other nonholonomic systems, provided that affine corrections are available for these systems.

## Wheeled robots towing trailers {#sec:trailers}

A kinematic car towing $p$ trailers can be modeled by $$\begin{equation}
  \label{eq:trail}
  \left\{
    \begin{array}{ccc}
      \dot{x} & = & v\cos(\theta_0)\\
      \dot{y} & = & v\sin(\theta_0)\\
      \dot{\theta}_0 & = & \frac{v\tan(\beta)}{L_0}\\
      \dot{\beta}&=&\zeta\\
      &&\textrm{and for $i=1\dots p$}\\
      \dot{\theta}_i & = &
      \frac{v}{L_i} \left(\prod_{j=1}^{i-1}{\cos(\theta_{j-1}-\theta_j)}\right)
      \sin(\theta_{i-1}-\theta_i)
    \end{array} \right.,
\end{equation}$$ where $(v,\zeta)$ are the system commands (respectively the linear velocity of the car and the rate of change of the steering angle) and $(x,y,\beta,\theta_0,\theta_1,\dots\theta_n)$, the system variables (respectively, the $x$ and $y$ coordinates of the car in the laboratory reference frame, the steering angle, the angle of the car with respect to the laboratory reference frame, the angle of the first trailer with respect to the laboratory reference frame, etc.).

The same reasoning as in the case of the simple kinematic car shows that a base-space trajectory $\mathcal{C}=(x,y)$ is admissible only if it belongs to $\mathscr{D}^2$ and if $\theta_0$ -- computed from $\mathcal{C}$ by $\theta_0=\mathrm{arctan2}(\dot y,\dot x)$ -- belongs to $\mathscr{D}^2$. Conversely, assume that $\mathcal{C}$ is in $\mathscr{D}^2$ and $\theta_0$ -- computed from $\mathcal{C}$ -- is in $\mathscr{D}^2$. One can then safely compute $v\in\mathscr{D}^1$, $\beta\in\mathscr{D}^1$, $\theta_0\in\mathscr{D}^2$ (by assumption) and $\zeta\in\mathscr{D}^0$ as in the case of the simple car. Next, to obtain $\theta_i$ (for $i=1\dots n$), it suffices to solve successively the following (ordinary) differential equations $$\dot{\theta}_i=\frac{v}{L_i}
\left(\prod_{j=1}^{i-1}{\cos(\theta_{j-1}-\theta_j)}\right)
\sin(\theta_{i-1}-\theta_i)$$ In summary, the set of admissible base-space trajectories of a car towing $p$ trailers is the same as that of a simple car. As a consequence, the admissible affine deformations and the trajectory correction algorithms for a car towing $p$ trailers are also the same as those for a simple car. An example of trajectory correction for a car towing two trailers is given in Fig. [7](#fig:trail){reference-type="ref" reference="fig:trail"}.

Note that we have no "control" over the configurations of the trailers, contrary to the literature (transformations to chained forms [@MS93tac; @SE95tac], flatness theory [@FliX95ijc], etc.). However, consider the (commonly encountered) case when the end of the initially planned trajectory consists of a straight segment, in order to align the trailers with the car. Since affine transformations preserve collinearity, the end of the *corrected* trajectory will also consist of a straight line, which automatically guarantees the alignment of the trailers with the car.

Note finally that it could be interesting to study affine deformations of the trajectory of the flat output [@FliX95ijc], which is, in the present case, the middle of the rear wheels axle of the last trailer (assuming that each trailer is hooked up at the middle of the rear wheels axle of the preceding trailer).

:::: {#fig:trail .figure latex-placement="ht"}
![image](Pham2011Affine_figs/trail_xy.png){height="5cm"} ![image](Pham2011Affine_figs/trail_other.png){height="6cm"}

::: caption
Trajectory correction for a car towing two trailers. One can imagine the following scenario: a trajectory $\mathcal{C}$ (red) is initially planned to park the car with trailers in a given parking slot; following the occupation of that parking slot, a new trajectory $\mathcal{C}'''$ (magenta) is obtained by deforming the red trajectory using the algorithm of section [3.4.5](#sec:3steps){reference-type="ref" reference="sec:3steps"} (where the blue and green trajectories correspond respectively to $\mathcal{C}'$ and $\mathcal{C}''$). The new trajectory allows the car to be parked in a neighboring slot, with the same final orientation. Note that the collinearity-preserving property of affine transformations automatically guarantees the straightness of the final segments of the blue, green and magenta trajectories, which in turn implies the alignment of the trailers with the car.
:::
::::

## Obstacle avoidance {#sec:obs}

In the trajectory correction algorithms previously developped, one can in fact replace the final time $T$ by any time instant $t>\tau$. This allows implementing interactive obstacle avoidance algorithms as follows

1.  determine a time instant $t_\mathrm{obs}$ when the initially planned trajectory would collide with the obstacle;

2.  select a new, non colliding, intermediate position $(x_\mathrm{inter},y_\mathrm{inter})$ to which one could make a correction;

3.  make the correction of $(x(t_\mathrm{obs}),y(t_\mathrm{obs}))$ towards $(x_\mathrm{inter},y_\mathrm{inter})$, using $\tau$(s) $<t_\mathrm{obs}$;

4.  re-correct the final position towards the initially planned final position, using $\tau$(s) $\geq t_\mathrm{obs}$.

:::: {#fig:uni .figure latex-placement="ht"}
![image](Pham2011Affine_figs/obs_xy.png){height="5cm"} ![image](Pham2011Affine_figs/obs_other_deform.png){height="5cm"}

::: caption
An example of obstacle avoidance for the unicycle. The original trajectory $(x,y)$ (red) was planned knowing the position of the black obstacles. During the execution, an unforeseen obstacle (cyan) appears on the original path. A new trajectory $(x_1,y_1)$ (blue) is obtained by deforming the original trajectory. The blue star indicates the position $(x(\tau_1),y(\tau_1))$ where the deformation occurs, and the black plain line joins $(x(t_\mathrm{obs}),y(t_\mathrm{obs}))$ to $(x_\mathrm{inter},y_\mathrm{inter})$. Next, in order to get back to the original target, an other trajectory (green) is obtained by deforming the blue one. The green star indicates the position $(x_1(\tau_2),y_1(\tau_2))$ where the deformation occurs, and the black dashed line joins $(x_1(T),y_1(T))$ to $(x(T),y(T))$.
:::
::::

This algorithm can be run iteratively to avoid all obstacles.

One can also prescribe a specific position/orientation of the trajectory at a given time instant $t_\mathrm{door}$ (this is desirable for instance when two large obstacles are close to each other, leaving between them a small doorway through which the robot could go), as follows

1.  make the correction of $(x(t_\mathrm{door}),y(t_\mathrm{door}))$ towards the specified intermediate position;

2.  make the correction of $\theta(t_\mathrm{door})$ towards the specified intermediate orientation;

3.  re-correct the final position towards the initially planned final position, using $\tau$(s) $>t_\mathrm{door}$.

## Feedback control

So far, we have been focusing on perturbations affecting the state of the target (position and/or orientation) or the environment (unexpected appearance of obstacles). Here we show, through a simplified feedback control algorithm, how affine corrections can also be used to deal with perturbations affecting the robot's own state.

Consider again the example of the kinematic car. Assume that a trajectory has been initially planned (black trajectory in Fig. [9](#fig:ofc){reference-type="ref" reference="fig:ofc"}A), in terms of the time series of the control inputs $(a_\mathrm{plan}(t)_{t\in[0,T]},\zeta_\mathrm{plan}(t)_{t\in[0,T]})$. Assume now that these control imputs are *corrupted* by random perturbations $$\forall t\in[0,T]\quad 
\left\{
\begin{array}{ccc}
a(t)&=&a_\mathrm{plan}(t)+\xi_1(t)\\
\zeta(t)&=&\zeta_\mathrm{plan}(t)+\xi_2(t)
\end{array}\right.,$$ where $\xi_1$ and $\xi_2$ two piecewise constant random functions. The red trajectories in Fig. [9](#fig:ofc){reference-type="ref" reference="fig:ofc"}A represent several trajectories of the car corresponding to different realizations of the pertubations $\xi_1$ and $\xi_2$. One can notice that the perturbations make the final positions of the red trajectories deviate randomly from the target (denoted by the magenta dot). This can also be noted from the variability profile (red curve in Fig. [9](#fig:ofc){reference-type="ref" reference="fig:ofc"}B), which is nonzero at the end of the movement.

:::::: {#fig:ofc .figure latex-placement="ht"}
::: minipage
**A**\
![image](Pham2011Affine_figs/ofc_xy.png){height="5cm"}
:::

::: minipage
**B**\
![image](Pham2011Affine_figs/ofc_var.png){height="3cm"}
:::

::: caption
Feedback control using affine corrections. **A**: uncorrected sample trajectories (red), corrected using at most one correction (blue) or at most five corrections (green). The initially planned trajectory is in black. **B**: variability profiles computed across 2000 realizations of the random perturbations $\xi_1$ and $\xi_2$.
:::
::::::

We propose the following feedback control algorithm inspired from [@TJ02nat; @PH09jnp]. The algorithm maintains at every step two time series $(a_\mathrm{cur}(t)_{t\in[0,T]},\zeta_\mathrm{cur}(t)_{t\in[0,T]})$ termed "currently planned control inputs". These time series are initialized at the values of $(a_\mathrm{plan}(t)_{t\in[0,T]},\zeta_\mathrm{plan}(t)_{t\in[0,T]})$. The movement time $T$ is divided in $S+1$ equal parts. At each time instant $t_i=iT/(S+1)$, $i=1\dots S$, the robot is given the possibility to make a correction as follows

1.  compute the final position of the robot, had the control inputs $(a_\mathrm{cur}(t)_{t\in[t_i,T]},\zeta_\mathrm{cur}(t)_{t\in[t_i,T]})$ been applied starting at the current state $\bar{\mathcal{C}}(t_i)$ and until the end of the movement. Denote this final simulated position $(x_\mathrm{sim},y_\mathrm{sim})$;

2.  compute appropriate trajectory deformations with $\tau(s)>t_i$ to correct the final position from $(x_\mathrm{sim},y_\mathrm{sim})$ towards $(x_\mathrm{target},y_\mathrm{target})$. This gives rise to new time series of control inputs, denoted $(a_\mathrm{new}(t)_{t\in[t_i,T]},\zeta_\mathrm{new}(t)_{t\in[t_i,T]})$;

3.  if the new control inputs are acceptable (i.e. do not imply too large accelerations or too sharp turns), set $a_\mathrm{cur}(t)_{t\in[t_i,T]}\leftarrow a_\mathrm{new}(t)_{t\in[t_i,T]}$ and $\zeta_\mathrm{cur}(t)_{t\in[t_i,T]}\leftarrow
      \zeta_\mathrm{new}(t)_{t\in[t_i,T]}$. Otherwise, keep the current values of $a_\mathrm{cur}$ and $\zeta_\mathrm{cur}$.

Figure [9](#fig:ofc){reference-type="ref" reference="fig:ofc"}A shows the results of the feedback control algorithm for $S=1$ (blue curves) and $S=5$ (green curve). Note that the blue and green curves are driven by the same realizations of the perturbations as the red curves (uncorrected trajectories). However, the blue and green curves end up much closer to the target position. Figure [9](#fig:ofc){reference-type="ref" reference="fig:ofc"}B confirms this observation: the final variabilities of the corrected trajectories (blue and green profiles) at $T$ are much lower ($\sim$`<!-- -->`{=html}1.3m) than that of the uncorrected trajectories ($\sim$`<!-- -->`{=html}6m).

One could ask: why make multiple corrections (green) while making one unique correction (blue) yields approximately the same final average error? Figure [10](#fig:ofc_stats){reference-type="ref" reference="fig:ofc_stats"} shows that $S=1$ is associated with larger values of $a$, $\zeta$ and $\beta$ than $S=5$. This is because when the robot is allowed to make multiple corrections, the changes to $a$ and $\zeta$ are *distributed* instead of being concentrated in one single large correction near the end of the trajectory. Figure [9](#fig:ofc){reference-type="ref" reference="fig:ofc"}B confirms this observation: the green variability profile ($S=5$) starts decreasing before the blue variability profile ($S=1$). Note however that choosing $S>5$ does not improve the algorithm.

:::: {#fig:ofc_stats .figure latex-placement="ht"}
![](Pham2011Affine_figs/ofc_stats.png){height="7cm"}

::: caption
Statistics of the feedback control algorithm across 2000 realizations of the random perturbations $\xi_1$ and $\xi_2$. The X-axis represents the maximum number of corrections allowed $S$. The horizontal lines report the values corresponding to the uncorrected trajectories ($S=0$).
:::
::::

Finally, note that this algorithm is not a trajectory-tracking algorithm but rather a simplified implementation of "optimal feedback control" [@TJ02nat; @PH09jnp].

## Gap filling for sampling-based kinodynamic planners {#sec:gap}

Gap-reduction techniques are a core component of any sampling-based kinodynamic planner [@CheX08tr]. As an example, consider the approach proposed in [@LK01ijrr], which consists of growing two rapidly-exploring random tree (RRT) rooted respectively at the initial state and at the target state -- a solution trajectory is obtained when these two trees intersect. When nonholonomic constraints are present, exact intersections of the trees occur with probability zero, such that one usually assumes intersection when the trees are within a nonzero distance of each other, yielding thereby a *gap* in the solution trajectory. As the performance of the planner critically depends on the permitted gap size (the larger the permitted gap size, the quicker the growing trees find an "intersection", but also the more difficult filling the gaps), efficient gap-reduction techniques have been shown to dramatically improve the performance of the planner [@CheX08tr].

We now show how affine corrections can be used to fill trajectory gaps. Consider two trajectories $\mathcal{C}_1(t)_{t\in[0,T_1]}$ and $\mathcal{C}_2(t)_{t\in[0,T_2]}$ of a kinematic car (respectively in red and cyan in Fig. [11](#fig:gap){reference-type="ref" reference="fig:gap"}) separated by a gap. We first "prepare" the two trajectories as follows

1.  grow a first stub with time duration $\Delta_a$ at the end of $\mathcal{C}_1$. Using the time interval $[T_1,T_1+\Delta_a]$, bring the steering angle $\beta_1$ to 0 by "counter-steering" (i.e. turning the steering wheel back to the straight-ahead position);

2.  grow a second stub with time duration $\Delta_b$ at the end of the extended $\mathcal{C}_1(t)$. During this time interval, the steering angle $\beta_1$ is kept to 0, resulting in a straight segment. One can easily verify that the (doubly) extended trajectory $\mathcal{C}_1(t)_{t\in[0,T_1+\Delta_a+\Delta_b]}$ is admissible. The two stubs are shown by dashed red lines in Fig. [11](#fig:gap){reference-type="ref" reference="fig:gap"};

3.  similarly, grow two other stubs at the *beginning* of $\mathcal{C}_2$ (shown by dashed cyan lines in Fig. [11](#fig:gap){reference-type="ref" reference="fig:gap"}).

After this "preparation", we have two trajectories which respectively ends and begins by straight segments. The lengths of the added stubs depend on the $\Delta$s and can be made relatively short if the $\beta$s are small and large braking and counter-steering rates are permitted. We can now use the position and orientation algorithms given in the previous sections to bring the end of the extended $\mathcal{C}_1$ towards the beginning of the extended $\mathcal{C}_2$. Fig. [11](#fig:gap){reference-type="ref" reference="fig:gap"} shows an example of such correction using three succesive affine deformations (cf. section [3.4.5](#sec:3steps){reference-type="ref" reference="sec:3steps"}). The admissibility conditions are verified by observing that

- since affine transformations preserve collinearity, the corrected extended trajectory $\mathcal{C}'''_1$ (magenta) also ends by a straight segment. When this straight segment connects with the straight segment at the beginning of the extended $\mathcal{C}_2$, the continuity of $\beta$ is guaranteed;

- regarding the continuity of $v$, one can use the straight parts around the connection point to modulate the speed profile to make it continuous *without altering the geometric path*: see the yellow lines in the plots of $a$ and $v$ in Fig. [11](#fig:gap){reference-type="ref" reference="fig:gap"}.

:::: {#fig:gap .figure latex-placement="ht"}
![image](Pham2011Affine_figs/fill_xy.png){height="5cm"} ![image](Pham2011Affine_figs/fill_other.png){width="8cm"}

::: caption
Filling trajectory gaps. Top plot: geometric paths. The original trajectories to be connected are showned in plain red line ($\mathcal{C}_1$) and plain cyan line ($\mathcal{C}_2$). These trajectories are first "prepared" by growing stubs at their extremities (red and cyan dashed lines). The extended $\mathcal{C}_1$ is then corrected into $\mathcal{C}'''_1$ (magenta) by three successive affine deformations (the blue and green lines represent the intermediate trajectories $\mathcal{C}'_1$ and $\mathcal{C}''_1$ ). Note that $\mathcal{C}'''_1$ smoothly connects with $\mathcal{C}_2$. Bottom plot: profiles of the other variables. The yellow lines in the plots of $a$ and $v$ show the modifications that make $v$ continuous without changing the geometric paths.
:::
::::

# Discussion {#sec:discussion}

As stated at the beginning of section [3](#sec:wheeled){reference-type="ref" reference="sec:wheeled"}, one can apply the following general scheme to study affine trajectory corrections for nonholonomic systems

1.  check the conditions for a base-space trajectory to be admissible. Often (but not always), a base-space trajectory is admissible if it -- and some functions computed from it -- belong to certain classes $\mathscr{D}^i$;

2.  based on the admissibility conditions of trajectories, particularly at the time instant when the deformation occurs, characterize the set of admissible affine deformations. Often (but not always), the admissible affine deformations at a given time instant form a Lie group of dimension $n+n^2-m$ where $n$ is the number of base variables and $m$ the number of continuity conditions;

3.  finally, play with $\tau$ and the $n+n^2-m$ "extra degrees of freedom" to achieve the desired correction. If there are more "extra degrees of freedom" than needed, one can "optimize" by choosing the affine transformations that are the closest to identity.

This general scheme suggests in turn the classes of systems that can or cannot be tackled by the proposed method. For instance, an underwater vehicle whose changes in turning rate ($\rho_x=\dot{\omega}_x$, $\rho_y=\dot{\omega}_y$, $\rho_z=\dot{\omega}_z$) are required to be continuous could probably be treated by the method (since in this case $n+n^2-m=3$). The development of the theory to deal with other classes of nonholonomic systems are also the subject of ongoing efforts.

Holonomic systems, such as the end-point of a robotic manipulator, are not subject, by nature, to the differential constraints with which the current manuscript is concerned. However, it is sometimes desirable for efficiency reasons to *artificially enforce* some differential constraints, such as the continuity of the velocity vector. For instance, if a planned *path* is not $\mathscr{C}^1$ at some points, the robot must stop-and-start at these points [@KanX08iros], which clearly is an undesired behavior. In this perspective, the regularity-preserving deformation algorithms developped here can also be useful for holonomic trajectory planning.

As just remarked, this manuscript is mostly concerned with the differential constraints that stem from the nonholonomic nature of the considered systems. In practice, other constraints, such as upper limits on the absolute acceleration or on the trajectory curvature, could further restrict the set of admissible affine deformations. This can be treated by observing that the changes in acceleration or curvature from the original trajectory can be computed from the affine transformation at hand (see also [@BenX09pcb]). The integration of such constraints into the current framework represents an important task (see e.g. [@HL07icra]).

Another promising direction of research may consist of *combining* the approach presented here with existing approaches for trajectory planning and deformation. We have mentioned earlier possible interactions with flatness theory. A complementary use of affine-based and perturbation-based deformations [@LamX04tr] may also lead to more efficient algorithms. For instance, affine corrections perform badly when the original trajectory is close to a straight line. Using the results in [@LamX04tr], it should be possible to slightly perturb the original trajectory to generate local curved portions, which subsequently allow applying affine deformations with greater effectiveness.

As mentioned in the Introduction, one advantage of the method presented in this manuscript is that it requires no re-integration of the trajectory. On the other hand, *differentiations* of the trajectory must be performed in order to recover the commands (see "Important remark" in section [3.2.6](#sec:sum){reference-type="ref" reference="sec:sum"}). Note however that, if multiple deformations are made, the differentiations need to be performed only *once*, after all the deformations have been applied.

The group property of affine transformations can also be used to further accelerate the computations (as in [@SeiX10wafr] with Euclidean transformations). Assume for instance that two affine transformations $\mathcal{F}_1$ and $\mathcal{F}_2$ are applied at time instants $\tau_1$ and $\tau_2$, with $\tau_1<\tau_2$. Then one can apply $\mathcal{F}_1$ to $\mathcal{C}(t)_{t\in[\tau_1,\tau_2]}$ and next $\mathcal{F}_2\circ\mathcal{F}_1$, which is also an affine transformation, to $\mathcal{C}(t)_{t\in(\tau_2,T]}$.

Another advantage, also mentioned in the Introduction, is that the method presented here can be executed *in one step*, while other methods require iterative deformations of the trajectory [@LamX04tr] or gradient descent to find the appropriate deformation coefficients [@CheX08tr; @SeiX10wafr]. This may result in significant performance gains, in particular, in real-time applications or in highly compute-intensive tasks such as the building of probabilistic roadmaps [@LK01ijrr].

Finally, the method is exact: for example, a desired position can be reached *exactly*, and not only approached iteratively "as close as we want". This may have important consequences. For example, in the *initial* trajectory planning, one would no longer need to spend time finding a trajectory that ends very close to the target. Instead, one can plan a trajectory that ends roughly somewhere near the target, and then make an affine deformation towards the exact target position.

A last word on the biological implications of the ideas presented here. One source of inspiration for the present work was indeed the recent studies of affine invariance in human perception and movements (see e.g. [@BenX09pcb] and references therein). Conversely, one could ask (and experimentally test) whether humans use algorithms similar to those described here to correct their hand or locomotor trajectories.

## Acknowledgments {#acknowledgments .unnumbered}

The author is deeply grateful to Prof. Daniel Bennequin, Prof. Yoshihiko Nakamura, and Dr. Oussama Kanoun for their highly valuable suggestions and comments. This research was funded by an University of Tokyo grant and by a JSPS postdoctoral fellowship.
