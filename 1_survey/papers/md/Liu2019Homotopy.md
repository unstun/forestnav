---
citation_key: Liu2019Homotopy
arxiv_id: 1901.10094
arxiv_url: https://arxiv.org/abs/1901.10094
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:56:11Z
origin: ai+web
reviewed: false
---

# Introduction

A fundamental problem in robotic motion planning is to find a trajectory which meets the various constraints stemming from the system's dynamics, which can be of holonomic or non-holonomic type, and obstacle avoidance constraints, which include constraints on the magnitude of some of the variables describing the system (e.g., a maximal turning radius), or obstacles present in physical space. We propose here a new method to find a trajectory which takes into account all the above constraints--we call such a trajectory *admissible*--and illustrate its performance on several examples. The method is a homotopy method: given an initial state and a final desired state, ${\bf x}_i$ and ${\bf x}_f$ respectively, and an arbitrary curve joining ${\bf x}_i$ to ${\bf x}_f$ in state-space, the method *deforms* the curve into an admissible curve joining ${\bf x}_i$ to ${\bf x}_f$. We presented a preliminary version of this method, with only non-holonomic constraints, in [@Belabbas2017NewMF]. In this paper, we restrict the presentation to systems *affine in the control*, and leave the general case to subsequent work. We also refer the readers to the website[^2] for slides, sample Matlab code and examples showcasing the method.

The problem of motion planning in robotics and control is a canonical problem, and many methods have been proposed over the years. For this reason, we can only give here a very partial overview of the current state of the field, and emphasize that the method we propose is built on a rather different set of ideas. A large subset of the methods is focused on non-holonomic dynamics, since this problem is by itself difficult and with a long history [@laumond1998robot; @latombe2012robot; @choset2005principles; @Lav06]. Many of the proposed methods are based on the use of sinusoidal driving signals; the basic relation underlying these methods is the system approximation $$\begin{equation*}
\dot x= \lim_{\omega \to \infty} \left( \sqrt{\omega}   \sin (\omega t) f_1(x)+ \sqrt{\omega} \cos(\omega t) f_2(x)\right) \Leftrightarrow \dot x  = [f_1,f_2](x),
\end{equation*}$$ where $[f_1,f_2]$ is the Lie bracket [@do1992riemannian] of the vector fields $f_1,f_2$. Indeed, this insight is at the basis of the work of Brockett [@brockett1989rectification], Murray et al. [@murray1994mathematical], Laferriere and Sussman [@lafferriere1993differential]. Furthermore, interesting recent work shows that some special functions--which can be thought as generalizations of harmonic functions---play a distinguished role in solving under-actuated control problems [@gauthier2014minimal].

For control and verification of hybrid systems in general, we refer to [@tomlin2003computational] and for a recent survey of motion planning for self-driving vehicles in urban environment, we refer to [@paden2016survey]. Other approaches of interest to obtain feasible trajectories for given problems and dynamics including random sampling-based [@doi:10.1177/0278364911406761] graph-based [@1241712], and optimization-based approaches [@7041375] and approaches based on solvers for nonlinear dynamics.

# Background and problem set-up

We present some background and notation needed to explain the method. We refer to as vehicle/robot/plant whose motion we desire to plan as *the system*. The system is assumed to obey the controlled dynamics $$\begin{equation}
\label{eq:maindyn}\dot {\bf x} = \sum_{i=1}^p u_i f_i({\bf x}),
\end{equation}$$ where ${\bf x}\in M$ with $M$ a (at least locally) differentiable manifold called the *configuration space*, $f_i({\bf x})$ the *actuation vector fields* and ${\bf u}:=(u_1,\ldots,u_p) \in \mathbbm{R}^p$ the controls. We refer to as *workspace* the physical environment in which the system lives. We denote by $\Span_x \{ g_i \}$ the (real) vector space spanned by the vectors $g_i(x)$.

We call a *curve* in configuration space a piecewise differentiable function ${\bf x}(t):[0,T] \to M$, where $T>0$, and refer to ${\bf x}(0)$ and ${\bf x}(T)$ as start-point and end-point, respectively, of ${\bf x}(t)$. We refer to them collectively as *end-points*. We call the *image* of a curve a *path*; a path is thus a geometric object (a collection of "contiguous states") and the times at which each point in a path is visited are not specified.

A *fixed end-points homotopy* between the two curves ${\bf x}_1(t)$ and ${\bf x}_2(t)$ with the same end-points (i.e., ${\bf x}_1(0)={\bf x}_2(0)$ and ${\bf x}_1(T)={\bf x}_2(T)$) is a differentiable function ${\bf v}(s,t):[0,\infty)\times[0,T] \to M$ with the properties: $$\begin{align*}
{\bf v}(s,0) &= {\bf x}_1(0)&\mbox{for all } s \geq 0\\
{\bf v}(s,T) &= {\bf x}_1(T)&\mbox{for all } s \geq 0
\end{align*}$$

The *length* of a curve ${\bf x}(t)$ is defined with respect to an norm on the tangent bundle $TM$ of $M$. In the following, one can assume that $M=\mathbbm{R}^n$ and the tangent space of $M$ at ${\bf x}\in M$, denoted by $T_{{\bf x}}M$ is also $\mathbbm{R}^n$. A *Riemannian inner product* on $M$ is an given by piecewise differentiable symmetric positive definite bilinear form $G({\bf x}):T_{{\bf x}}M \times T_{{\bf x}}M \to \mathbbm{R}.$. With a slight abuse of notation, we also denote by $G({\bf x})$ its matrix representation in coordinates. Hence, we can think of $G({\bf x})$ as an ${\bf x}$-dependent positive definite symmetric matrix.

The *length* of a curve $p(t)$ is then given by $$\begin{equation}
\label{eq:dfL}L({\bf x}):= \int_0^T \sqrt{\dot {\bf x}^\top(t) G({\bf x}(t)) \dot {\bf x}(t)} dt.
\end{equation}$$

Finally, we introduce the Christoffels' symbols associated to $G({\bf x})$. To this end, denote by $g_{ij}$ the $ij$th entry of the matrix representation $G({\bf x})$, and by $g^{ij}$ the $ij$th entry of the matrix $G^{-1}({\bf x})$. The Christoffel's symbols are

$$\begin{equation}
\label{eq:defchristoffel} 
\Gamma_{jk}^i({\bf x}) := \frac{1}{2}\sum_l  g^{il}\left( \frac{\partial g_{lj}}{\partial x_k} +  \frac{\partial g_{lk}}{\partial x_j} -   \frac{\partial g_{jk}}{\partial x_l}\right)
\end{equation}$$

#### Problem definition.

The problem that the method MotionSketch solves is the following: given a configuration space $M$, a set of holonomic, non-holonomic and obstacle avoidance constraints, an initial state ${\bf x}_i$ and a desired final state ${\bf x}_f$, provide a curve ${\bf x}(t):[0,T] \to M$ which respects these constraints and so that ${\bf x}(0)={\bf x}_i$, and ${\bf x}(T)={\bf x}_f$, and provide the control ${\bf u}$ that drive a control system from ${\bf x}_i$ to ${\bf x}_f$. From now on, we normalize the time $T$ to be equal to one; this is done for simplicity of exposition, and all the results below are easily extended to the case of arbitrary $T$. We recall that a curve that meets the constraints is an **admissible curve**.

#### Length of a curve.

In order to provide an intuitive justification of the method, we first revisit the definition of the generalized length of a curve given a Riemannian metric in [\[eq:dfL\]](#eq:dfL){reference-type="ref" reference="eq:dfL"}. See also Fig. [1](#fig:Lill){reference-type="ref" reference="fig:Lill"}. Since $G({\bf x})$ is positive definite for all ${\bf x}\in M$, we can factor it as $G({\bf x})=F({\bf x}) D({\bf x}) F^\top({\bf x})$, where $D({\bf x})$ is a positive definite diagonal matrix, and $F({\bf x})^\top F({\bf x}) = I$ (i.e., $F({\bf x})$ is an orthogonal matrix.) Let ${\bf x}(t):[0,1]\to M$ be a differentiable curve and let $0=t_0<t_1<\ldots<t_{l+1}=1$ provide subdivisions of the unit interval. We can then approximate $$\dot {\bf x}(t_i) \simeq \frac{1}{\Delta t_i} ({\bf x}(t_{i+1})-{\bf x}(t_i))= \frac{1}{\Delta t_i} (\Delta {\bf x}(t_i)),$$ where $\Delta t_i = t_{i+1}-t_i$, and the second equality defines $\Delta {\bf x}(t_i)$. Using these relations, we can approximate the length of ${\bf x}(t)$ as $$\begin{align*}
L({\bf x})&\simeq \sum_{i=1}^l \sqrt{(\frac{\Delta {\bf x}(t_i)}{\Delta t_i} )^\top F(t_i)D(t_i)F(t_i)\frac{\Delta {\bf x}(t_i)}{\Delta t_i}   } \Delta t_i \\
&\simeq \sum_{i=1}^l \sqrt{ (F(t_i)^\top\Delta {\bf x}(t_i))^\top D(t_i)(F(t_i)\Delta {\bf x}(t_i))},
\end{align*}$$ where we set $D(t_i):=D({\bf x}(t_i))$ and $F(t_i):=F({\bf x}(t_i))$. Since $F$ is an orthogonal matrix, we can think of $F^\top \Delta {\bf x}$ the vector of coordinates describing $\Delta {\bf x}$ in the basis spanned by the column vectors of $F$; more precisely, if we set $f_k$ to be the $k$th column of $F$ and set $\Delta {\bf x}_k(t_i) = f_k^\top \Delta {\bf x}(t_i)$, then we have $\Delta {\bf x}(t_i) = \sum_k f_k \Delta {\bf x}_k(t_i)$. Now denote by $d_k^2$ the $k$th diagonal entry of $D$ (recall that $D$ has positive diagonal entries). We obtain $$L({\bf x}) \simeq \sum_i \sum_{k=1}^n \Delta {\bf x}(t_i)_k d_k(t_i).$$ Hence, by adjusting the $d_i$ and the $f_k$ appropriately, we can *adjust which infinitesimal directions for a curve yield a larger length.* We show how this can be brought to bear on motion planning problems below.

::::: {#fig:Lill .figure}
::: center
![](Liu2019Homotopy_figs/main2-figure0.png)
:::

::: caption
Length of a discretized curve.
:::
:::::

# The method MotionSketch

The method contains the three following steps:

1.  Encode the constraints of the motion planning problem (obstacles, holonomic, nonholonomic and dynamical constraints) into a Riemannian inner product.

2.  Provide a curve in configuration space between the initial and final desired states. This curve, which we call the *sketch*, does *not* need to meet the holonomic, non-holonomic and dynamical constraints, but is required to avoid obstacles. Numerically solve the geometric heat flow (GHF), defined below, equation with the sketch as initial condition.

3.  Extract the controls from the solution of the GHF.

We now elaborate on the three items.

## Step 1: Encoding the constraints in a Riemannian inner product

We start with holonomic/non-holonomic constraints.

### Holonomic and non-holonomic constraints

Holonomic constraints can be formulated as a set of equations $$q_i({\bf x})=0,\quad i=1,2,\cdots, m_h$$ For each $i$ and an infinitesimally small motion $\delta {\bf x}$, we have the approximation $q_i({\bf x}_0+\delta {\bf x})\approx q_i({\bf x}_0)+\frac{\partial q_i}{\partial {\bf x}}\delta {\bf x}.$ In order to respect the constraint, $\delta {\bf x}$ needs to satisfy $q_i({\bf x}_0+\delta {\bf x})=q_i({\bf x}_0)=0$, thus we have $\frac{\partial q_i}{\partial {\bf x}}\delta {\bf x}=0$. This means that for ${\bf x}(t)$ to be an admissible curve, the direction of motion $\delta {\bf x}$ needs to be orthogonal to the vectors $\frac{\partial q_i}{\partial {\bf x}}$ for all $i$; in other words, it means the *undesirable* directions of motion are $\operatorname{span} \left\{\frac{\partial q_i}{\partial {\bf x}}\right\}$.

We now turn our attention to non-holonomic constraints, which we assume are formulated as a set of constraints on the allowed velocities $\dot {\bf x}$ when at state $x$ as follows: $$\dot {\bf x}^\top f_{c,j}({\bf x})=0,\quad j=1,2,\cdots, m_n.$$ The non-holonomic character of the constraints, which is reflected in the fact that they cannot be expressed as $\frac{d}{dt} q_{n}({\bf x}) = 0$ for some function $q_{n}({\bf x})$, does *not* play any particular function insofar our local encoding of the constraints is concerned; in fact, the undesirable directions of motion are easily seen to be in this case $\operatorname{span} \left\{f_{c,j}({\bf x})\right\}$.

Non-holonomic constraints can be presented as above, e.g. as non-slippage constraints, but they can also be encoded in the dynamics of the system, which is then called non-holononic. For this latter case, consider given the system of Eq. [\[eq:maindyn\]](#eq:maindyn){reference-type="eqref" reference="eq:maindyn"}. We set $f_{f,i}=f_i$ and $f_{c,j}$ to be the $m_n$ vectors orthogonal (for the Euclidean inner product) to $f_{f,i}$ for all $i=1,\cdots,p$.

#### Encoding the constraints

We set ${\bar p}:=n-m_n-m_h$. We define the $n\times(n-{\bar p})$ matrix $\bar F_c$ as the matrix with first $m_h$ columns given by $\frac{\partial q_i}{\partial {\bf x}}$ and the next $m_n$ columns given by the $f_{c,j}$. We assume that $\bar F_c({\bf x})$ is of constant rank almost everywhere in $M$, and we denote this rank by $l$, and set $p:=n-l$. If $m_h+m_n = l$, it is of *full column rank*, and we set $F_c({\bf x}):= \bar F_c({\bf x})$. Otherwise $m_h+m_n> l$ and the constraints are not independent, in the sense that satisfying a *subset* of the constraints insures that *all* constraints are met. We set $F_c({\bf x})$ to be a $n \times {l}$ matrix whose column span equals the column span of $\bar F_c({\bf x})$. Such matrix can be obtained, e.g., via the Gram-Schmidt process. Notice that $F_c$ is of full column rank $l=n-p$ and the *column space of $F_c$ contains all the undesirable directions of motion*.

Next, find a rank $p$ matrix $F_f({\bf x})\in\mathbbm{R}^{n\times p}$ such that $$F_f({\bf x})^\top F_c({\bf x})=0,$$ which again can be found using the Gram-Schmidt process. The column space of $F_f({\bf x})$ contains all the directions in which the system can move when at state ${\bf x}$. Note that in the absence of holonomic constraints, we can start with defining $F_f$ with columns $f_i$ as in Eq. [\[eq:maindyn\]](#eq:maindyn){reference-type="eqref" reference="eq:maindyn"} and choose $F_c$ the satisfy the above relation. Set $$\begin{equation}
\label{F(x)}
 F({\bf x})=\begin{pmatrix}
|&|\\
F_c({\bf x})&F_f({\bf x})\\
|&|
\end{pmatrix}
\end{equation}$$

Then $F({\bf x})\in\mathbbm{R}^{n\times n}$ and we define $$\begin{equation}
\label{H(x)}
H({\bf x})=F({\bf x})DF^\top ({\bf x})
\end{equation}$$ where $D=\operatorname{diag}([\underbrace{k \cdots k}_{n-p}\underbrace{ 1 \cdots 1}_p])$ is a constant matrix. Note that this $k$ is exactly the $d^2$ discussed in the Section II.b. In practice, we take $k$ to be of the order of $10\sim 1000$.

Using the interpretation of the length functional given in the previous section, it is easy to see that if $\dot {\bf x}$ is a direction that respects the constraints, it is not multiplied by $k$ in the inner product $\dot {\bf x}^\top H({\bf x})\dot {\bf x}$ with $H$ defined via [\[H(x)\]](#H(x)){reference-type="eqref" reference="H(x)"}, so $\dot {\bf x}^\top H({\bf x})\dot {\bf x}$ will not be scaled by $k$. On the other hand, if $\dot {\bf x}$ is a direction that violates a constraint, it has some components lying in $\operatorname{span} F_c({\bf x})$, and consequently $\dot {\bf x}^\top H({\bf x})\dot x$ is large.

Finally, we record here that the partial derivative of $H$ is given by $$\frac{\partial H}{\partial x_i}({\bf x})=2F D\frac{\partial F^\top}{\partial x_i}({\bf x}),$$ which is needed for the computation of the Christoffels symbols.

### Obstacle constraints

We described obstacles $\Omega_i\subset \mathbbm{R}^n$ in configuration space via functions $r_i:M \to \mathbbm{R}$ according to $$\Omega_i:=\{{\bf x}\in \mathbbm{R}^n:r_i({\bf x})\leq 0\}$$ The boundary of an obstacle is thus $\partial \Omega_i=\{{\bf x}\in \mathbbm{R}^n:r_i({\bf x})=0\}$. We incorporate obstacles in the Riemannian inner product via a barrier function $b({\bf x})=\sum_i b_i({\bf x})$ with the following properties:

1.  Each $b_i({\bf x})$ is positive and differentiable for all ${\bf x}\in \mathbbm{R}^n\backslash \Omega_i$

2.  $b_i({\bf x})\to\infty$ as ${\bf x}\to\partial \Omega_i$,

3.  $b({\bf x})=1$ when ${\bf x}$ is far away from all $\Omega_i$.

The idea is that we would like $b_i({\bf x})$ to be large when ${\bf x}$ is in the vicinity of $\Omega_i$, and becomes infinite if ${\bf x}\in\partial\Omega_i$. Thus if we multiply the metric tensor by $b({\bf x})$, the length of a path that is in the vicinity of an obstacle is much larger than the length of a path that steer well-clear of the obstacle, where quantifying "well-clear" is of course dependent on the choice of $b_i({\bf x})$ and how quickly it decays near the boundary of the obstacle. We illustrate this in Fig. [\[fig:obstaclew\]](#fig:obstaclew){reference-type="ref" reference="fig:obstaclew"}.

:::: figure
::: caption
(a).The length $l_1$ of the path passing near the obstacle is much larger that the length $l_2$ of the path staying far from the obstacles when the metric is scaled with $b({\bf x})$. (b) Two-links articulated arm can be described as a system with $4$ degrees of freedom and $2$ holonomic constraints relating the position $(x,y)$ of the tip to the joint angles $\theta_1,\theta_2$.
:::
::::

Such functions $b_i$ are also known as *barrier functions* in the optimization literature [@Nocedal99]. In the case when obstacles are balls, that is, $\Omega= \cup_{i=1}^l \{{\bf x}\in \mathbbm{R}^n:|{\bf x}-c_i|\leq r_i\}$, one candidate of such $b({\bf x})$ function will be a modification of penalty function from avoidance control [@Leitmann1980]: $$\begin{equation}
\label{b_ball}
b({\bf x})=1+\sum_{i=1}^l\left(\min\left\{0,\frac{\vert {\bf x}-c_i\vert^2-R_i^2}{\vert {\bf x}-c_i\vert^2-r_i^2}\right\}\right)^2
\end{equation}$$ where $R_i$ is such that $r_i<R_i$ for all $i=1,2,\cdots,l$, and $R_i$ can be thought of as a *radius of detection* of the obstacle, in the sense that outside this radius, the obstacle does not affect the metric. Notice that $b(x)$ defined in [\[b_ball\]](#b_ball){reference-type="eqref" reference="b_ball"} satisfies the 3 properties mentioned earlier. The derivative of $b$ is also not hard to compute. Note that one can cover any obstacles with balls and use the above barrier function as a default approach.

### simultaneous multi-vehicle path planning

Suppose there are $l$ vehicles and each of them has its own state ${\bf x}_j=\begin{pmatrix}x_{1j},x_{2j},\cdots x_{nj}\end{pmatrix}^\top\in \mathbb R^n$ and the dynamics is $\dot{\bf x}_j=F_j({\bf x}_j){\bf u}_j$. The $j$-th vehicle is supposed to drive from ${\bf x}_j(0)={\bf a}_j$ to ${\bf x}_j(T)={\bf b}_j$. Denote ${\bf x}^\top=\begin{pmatrix} {\bf x}_1^\top&\cdots{\bf x}_l^\top\end{pmatrix}$ and ${\bf u}^\top=\begin{pmatrix} {\bf u}_1^\top&\cdots{\bf u}_l^\top\end{pmatrix}$, then the system of multi-vehicle has total dimension of $lm$ and initial and final states $${\bf x}_i=\begin{pmatrix}{\bf a}_1\\\vdots\\{\bf a}_l\end{pmatrix},\quad{\bf x}_f=\begin{pmatrix}{\bf b}_1\\\vdots\\{\bf b}_l\end{pmatrix}.$$ and the overall dynamics is $$\begin{equation}
\label{bigF}
\dot {\bf x}=\operatorname{diag}(F_1({\bf x}_1),\cdots,F_l({\bf x}_l)){\bf u}:=F({\bf x}){\bf u}.
\end{equation}$$ While planning the path for all $l$ vehicles, they are also supposed to avoid collision with each other. In case of planar vehicles where $(x_{1,j},x_{2,j})$ represents the $xy$-coordinate of the $j$-th vehicle, collision between the $j,k$-th vehicles is avoided if $$\begin{equation}
\label{collision_dist}
(x_{1j}-x_{1k})^2+(x_{2j}-x_{2k})^2\geq r_c^2,
\end{equation}$$ where $r_c$ is a safety radius guaranteeing collision-free between two vehicles. Thus the [\[b_ball\]](#b_ball){reference-type="eqref" reference="b_ball"}-like barrier function induced from [\[collision_dist\]](#collision_dist){reference-type="eqref" reference="collision_dist"} is $$b_c({\bf x})=\sum_{j\neq k}\left(\min\left\{0,\frac{(x_{1j}-x_{1k})^2+(x_{2j}-x_{2k})^2-R^2}{(x_{1j}-x_{1k})^2+(x_{2j}-x_{2k})^2- r_c^2}\right\}\right)^2$$ Thus, whenever two vehicles are too close ($(x_{1j}-x_{1k})^2+(x_{2j}-x_{2k})^2\leq R^2$), $b_c({\bf x})$ becomes large and the metric at this state of vehicles is large. Notice that if we perform path planning for each individual vehicle first while treating the other vehicles as obstacles, the avoidance problem becomes dynamic in the sense that now the obstacles are moving with respect to time. Yet in our method avoidance of collision between vehicles and avoidance of static obstacles are processed in similar way and the result is promising as one can see later in our example.

In addition, Because $F({\bf x})$ in [\[bigF\]](#bigF){reference-type="eqref" reference="bigF"} is block diagonal, $H$ defined via [\[H(x)\]](#H(x)){reference-type="eqref" reference="H(x)"} is also block diagonal and its $j$-th block only involves ${\bf x}_j$. As a result, inverse of $H$ is in complexity of $O(lm^3)$ and computing $\frac{\partial H}{\partial x_i}$ for multi-vehicle has the same complexity as that for single vehicle. As a result, in each iteration of solving the numerical GHF equation, the complexity of computing all the Christoffel symbols is linear in $l$, the number of total vehicles.

### The inner product with three type of constraints

We now formally define the inner product used in the method: given $H({\bf x})$ as defined above from holonomic and non-holonomic constraints, and $b({\bf x})$ a barrier function for the obstacles, we set

$$G({\bf x}):=b({\bf x})H({\bf x})$$ With this construction, the partial derivatives of $G({\bf x})$ can be computed using the chain rule: $\frac{\partial}{\partial x_i}G({\bf x})=\frac{\partial b}{\partial x_i}({\bf x})H({\bf x})+b({\bf x})\frac{\partial H}{\partial x_i}({\bf x}).$ Hence the Christoffel symbols in [\[eq:defchristoffel\]](#eq:defchristoffel){reference-type="eqref" reference="eq:defchristoffel"} can be computed solely based on the values $H,\frac{\partial H}{\partial x_i},b,\frac{\partial b}{\partial x_i}$ at each state ${\bf x}$.

### Examples

#### The two-links manipulator

In this example we consider a two-links manipulator in the plane, see Fig. [\[fig:2links\]](#fig:2links){reference-type="ref" reference="fig:2links"}. The working space, in terms of the position of the tool tip $(x,y)$, is a subset of $\mathbbm{R}^2$. The configuration space when the joint angles are also taken into account can be treated as a subset of $\mathbbm{R}^4$. This system has 2 degrees of freedom and we can easily obtain the holonomic constraints: $$\begin{equation}
\label{eq:twoarmconst}
\left\{\begin{array}{c}
q_1({\bf x})=L_1\cos(\theta_1)+L_2\cos(\theta_2)-x=0\\
q_2({\bf x})=L_1\sin(\theta_1)+L_2\sin(\theta_2)-y=0
\end{array}
\right.
\end{equation}$$ Taking differential of the two constraints, we find

::: small
$$\begin{equation*}
\frac{\partial q_1}{\partial {\bf x}}=   (-1,\ 0,\ -L_1 \sin \theta_1,\-L_2 \sin \theta_2)^\top,\\ \frac{\partial q_2}{\partial {\bf x}}=(  0,\ -1,\ L_1 \cos \theta_1 ,\ L_2 \cos \theta_2 )^\top
\end{equation*}$$
:::

Thus we set $F_c  = \left(\begin{smallmatrix}1 & 0 \\ 0 & 1 \\ \sin\theta_{1}  & -\cos\theta_{1}  \\ \sin\theta_{2}  & -\cos\theta_{2}   \end{smallmatrix}\right)$ and we find $F_f =  \left(\begin{smallmatrix} -\sin\theta_{1} & -\sin\theta_{2}\\  \cos\theta_{1}  & \cos\theta_{2} \\  1 & 0\\    0 & 1 \end{smallmatrix}\right)$. We then set $F=(F_c\,|\, F_f)$.

We do not include obstacles and thus $b({\bf x})\equiv 1$ and $$\begin{align*}
G &= H =F\operatorname{diag}([k\, k\, 1\, 1])F^\top=
&\scalebox{1.2}{$\left(\begin{smallmatrix} {\sin^2\theta_1}+{\sin^2\theta_2}+k & -\frac{\sin 2\theta_1}{2}-\frac{\sin 2\theta_2}{2} & (k-1)\sin\theta_1 & (k-1) \sin\theta_2 \\
 -\frac{\sin 2\theta_1}{2}-\frac{\sin 2\theta_2 }{2} & {\cos^2 \theta_1 }+{\cos^2 \theta_2 }+k & -(k-1)\cos \theta_1   & -(k-1)\cos \theta_2  \\ (k-1) \sin \theta_1   & -(k-1)\cos \theta_1   & k+1 & k\cos(\theta_1-\theta_2) \\ (k-1)\sin \theta_2   & -\cos \theta_2 \, k-1  & k\,\cos \theta_1-\theta_2  & k+1 \end{smallmatrix}\right)$}
\end{align*}$$

#### The rolling coin or unicycle

:::: {#twofigs .figure}
::: caption
\(a\) A rolling coin or unicycle. is the side view. (b) In the mean-curvature flow, the curve $p(t,0)$ is continuously deformed in the direction of its normal, depicted by the red arrows. The final curve is a straight line. In general, the final curve is a length minimizing curve. is the corresponding angles
:::
::::

The kinematics of a unicycle can be modeled as $$\begin{equation}
\label{unicycle}
\begin{pmatrix}\dot x\\\dot y\\\dot \theta\end{pmatrix}=\begin{pmatrix}\cos\theta\\\sin\theta\\0\end{pmatrix}u_1+\begin{pmatrix}0\\0\\1\end{pmatrix}u_2
\end{equation}$$ where $(x,y)$ is the position of the unicycle in the plane and $\theta$ is its orientation. Notice that there is only one non-holonomic constraints in this model and the constraint is the direction $\begin{pmatrix}-\sin\theta& \cos\theta &0\end{pmatrix}^\top$ which prevents moving sideways and hence prevents slipping. Equivalently, because the model [\[unicycle\]](#unicycle){reference-type="eqref" reference="unicycle"} is affine in control, the free directions $F_f$ are simply the ones in [\[unicycle\]](#unicycle){reference-type="eqref" reference="unicycle"}. Hence $$F({\bf x})=\begin{pmatrix}
-\sin\theta&\cos\theta&0\\
\cos\theta&\sin\theta&0\\
0&0&1
\end{pmatrix},$$ from which we obtain $$\begin{equation*}
G({\bf x})=H({\bf x})=F \operatorname{diag}([k\ 1\ 1]) F^\top\\
=\begin{pmatrix}
\cos^2\theta+k\sin^2\theta&(1-k)\cos\theta\sin\theta&0\\
(1-k)\cos\theta\sin\theta&k\cos^2\theta+\sin^2\theta&0\\
0&0&1
\end{pmatrix}.
\end{equation*}$$

## Step 2: Initial sketch and solving the Geometric Heat Flow equation

Our method proceeds with solving the following GHF equation: $$\begin{equation}
\label{HFE}
\frac{\partial}{\partial s}v_i(s,t)=\frac{\partial^2}{\partial t^2}v_i(s,t)+\sum_{j,k}\Gamma_{jk}^i\frac{\partial v_j}{\partial t}\frac{\partial v_k}{\partial t}\quad i=1,2,\dots,n
\end{equation}$$ where $\Gamma_{jk}^i$ are the Christoffel symbols introduced in [\[eq:defchristoffel\]](#eq:defchristoffel){reference-type="eqref" reference="eq:defchristoffel"} for the inner product defined in the previous subsection. We impose the boundary conditions $$v(s,0)={\bf x}_i,v(s,1)={\bf x}_f$$ and a user defined initial condition, $$v(0,t)={\bf x}(t)$$ in order to find the solution. The initial curve ${\bf x}(t)$ is an arbitrary curves satisfying the following 2 conditions:

1.  It satisfies the boundary conditions: ${\bf x}(0)={\bf x}_i$ and ${\bf x}(1)={\bf x}_f$;

2.  It does not pass though any obstacles: $r({\bf x}(t))>0$ for all $t\in[0,1]$.

An important point here is that ${\bf x}(t)$ does not need to satisfy any holonomic or non-holonomic constraints; it can be simply a curve drawn from ${\bf x}_i$ to ${\bf x}_f$ without touching $\Omega$.

Notice that for each $s\geq 0$ fixed, the solution $v(s,\cdot)$ represent a curve connecting ${\bf x}_i$ to ${\bf x}_f$. As we explain below, as $s$ increases, $v(s,\cdot)$ is a curve that uses "less and less of the constrained directions", said precisely, $F_c^\top \frac{\partial}{\partial t} v(s,t)$ tends to zero. We set $s_{\max}$ to be the simulation time for the PDE (in our examples, between 1 and 20) and $${\bf x}_{sol}(\cdot)=v(s_{\max},\cdot).$$

#### Mean-curvature flows {#par:meanc}

We now elaborate on the origin of Eq. [\[HFE\]](#HFE){reference-type="eqref" reference="HFE"}: it is a type of curve-shortening flow [@curvebook2001], called a *mean-curvature flow* for a $1$-dimensional manifold (i.e. a curve) or *geometric heat flow*. For an introduction to mean-curvature flows in arbitrary dimensions, see [@colding2015mean]. For clarity of exposition, we present first the flow in two dimensional plane with the Euclidean inner product. We briefly mention steps that need to be taken for the general flow below.

Consider a curve $p(t):[0,1] \to \mathbbm{R}^2=(p_1(t),p_2(t))$, as depicted in Fig. [\[fig:meancurveflow\]](#fig:meancurveflow){reference-type="ref" reference="fig:meancurveflow"}. The scalar curvature [@do1992riemannian] of $p$ at $p(t)$ is defined as $\kappa(p(t))=\|\ddot p\|$. Denote by $N_{p(t)}$ the unit normal vector pointing "inward". The curvature of $p$ at $p(t)$ is then $\kappa(p(t)) N(p(t))$.

The mean-curvature flow for this curve is defined as follows: consider a *family* of curves $p(t,s)$, $s \geq 0$, where for each $s_0$ fixed, $p(t,s_0):[0,1]\to\mathbbm{R}^2$ is a curve joining $x_0$ to $x_1$, and $p(t,0)$ is the original curve. Then the mean-curvature flow is the partial differential equation $$\frac{\partial p}{\partial s} = \kappa(p(t,s)) N(p(t,s)).$$ Note that it is in fact a system of two PDEs. Looking at Fig. [\[fig:meancurveflow\]](#fig:meancurveflow){reference-type="ref" reference="fig:meancurveflow"}, it is easy to conclude intuitively that $\lim_{s \to \infty} p(t,s)$ converges to a straight line between $x_0$ and $x_1$. This is also the *shortest path* between $x_0$ and $x_1$ for the usual Euclidean metric. This is no accident, and we can show that in general the solution of this PDE converges to a curve of minimal length. For our purpose, we need to extend this idea in *two* directions: to $(i)$ curves in higher dimensions and $(ii)$ to a general Riemannian metric (or more precisely, inner product). One can show, after some extensive algebraic manipulations which we omit here, that the equivalent of the flow for a general curve in a Riemannian manifold is exactly the geometric heat flow presented in Eq. [\[HFE\]](#HFE){reference-type="eqref" reference="HFE"}.

## Step 3: Extracting the controls

The control can be directly computed: $$\begin{equation}
\label{control_extract}
{\bf u}(t)=F_f^\dagger({\bf x}_{sol}(t))\dot {\bf x}_{sol}(t)
\end{equation}$$ where $F_f^\dagger=(F_f^\top F_f)^{-1}F_f^\top$ is the pseudo-inverse of $F_f$. Notice that in the case ${\bf x}_{sol}$ is admissible, that is, if $\dot {\bf x}_{sol}(t)=F_fv(t)$ for some control ${\bf v}$, $${\bf u}=F_f^\dagger \dot x_{sol}=(F_f^\top F_f)^{-1}F_f^\top F_f {\bf v}={\bf v}$$ Thus we have recovered the control and ideally the system should exactly follow the path ${\bf x}_{sol}$. Notice that $F_fF_F^\dagger$ is a minimal square error projection onto the column space of $F_f$, the control extracted from [\[control_extract\]](#control_extract){reference-type="eqref" reference="control_extract"} will drive the system along a path that is close to ${\bf x}_{sol}$, even if $\dot {\bf x}_{sol}$ has small components in the constrained direction.

## On the implementation

As mentioned earlier, the key of our method is to find an inner product matrix $G$ and then solve the GHF equation [\[HFE\]](#HFE){reference-type="eqref" reference="HFE"}. In our case, this is processed in MATLAB. To be explicit, once we have obtained $F_c$ from the constraints, we implement them as symbolic vectors in MATLAB and thus find $F_f({\bf x})$. Subsequently, both $G({\bf x})$ and $\frac{\partial G}{\partial {\bf x}}$ can be derived symbolically and the symbolics are then replaced by state values and then stored in an $n\times n$ array `G` and an $n\times n\times n$ array `pG`, respectively. `pdepe` is then called with the boundary conditions and customized initial condition. In each iteration of solving the PDEs, the Christoffel symbols are computed from `G` and `pG` according to [\[eq:defchristoffel\]](#eq:defchristoffel){reference-type="eqref" reference="eq:defchristoffel"} and then stored in an $n\times n\times n$ array `Chris`. Notice that the `pdepe` solves PDEs of the general form $$c(s,t,x,\frac{\partial x}{\partial t})\frac{\partial x}{\partial s}=x^{-m}\frac{\partial}{\partial t}\left(t^m f(s,t,x,\frac{\partial x}{\partial t})\right)+s(s,t,x,\frac{\partial x}{\partial t})$$ Compare it to [\[HFE\]](#HFE){reference-type="eqref" reference="HFE"} we see that in our case we need to set\
`c=ones(4,1);m=0,f=DxDt` and `s(i)=DxDt’*Chris(i,:,:)*DxDt`. Eventually the numerical solution of `pdepe` will be in the form of `sol(t,s,i)`,

## Theoretical guarantee

Set $\Delta(x) = \operatorname{span} \frac{\partial q_i}{\partial x} \cap \operatorname{span} f_{c,j}$.

We call the constraints **satisfiable** if the distribution $\Delta$ satisfies the Lie algebraic rank condition (LARC). It is easy to see that it is a necessary condition for the existence of a trajectory joining arbitrary ${\bf x}_i$ and ${\bf x}_f$ while respecting the holonomic and non-holonomic constraints on the system. Under mild assumptions our method provides controls $\bar {\bf u}(t)$ so that the solution ${\bf x}^*(t)$ of $\dot {\bf x}= \sum_i \bar {\bf u}_i f_i$ by construction satisfies both the holonomic and non-holonomic constraints. In addition,

::: {#main_thm .theorem}
**Theorem 1**. *Suppose $F({\bf x})$ defined in [\[F(x)\]](#F(x)){reference-type="eqref" reference="F(x)"} is globally Lipschitz with constant $L$ and $\Vert F_c({\bf x})\Vert=1$ for all $x\in \mathbbm{R}^d$. Let $\bar E$ be the infimum of the energy functional $$E({\bf u})=\int_0^1|{\bf u}(t)|^2dt$$ over the space of controls that the corresponding state trajectory satisfies both the holonomic and non-holonomic constraints. For any arbitrary $k\in \mathbb N,s>0$, define ${\bf x}$ to be the part $v(\cdot, s)$ of the solution of [\[HFE\]](#HFE){reference-type="eqref" reference="HFE"}, ${\bf u}$ to be the control derived via [\[control_extract\]](#control_extract){reference-type="eqref" reference="control_extract"} and $\tilde {\bf x}$ to be the solution of [\[eq:maindyn\]](#eq:maindyn){reference-type="eqref" reference="eq:maindyn"} generated by ${\bf u}$ from $\tilde{\bf x}(0)={\bf x}_i$. Then for any $\epsilon>0$, there exists $T=T(\epsilon,k)$ such that for all $s\geq T$,*

1.  *$E({\bf u})\leq \bar E+\epsilon$;*

2.  *$|\tilde {\bf x}(t)-{\bf x}(t)|\leq \left(\sqrt{\frac{2t}{k}(\bar E+\epsilon)}\right)e^{L^2(\bar E+\epsilon)}$ for all $t\in[0,1]$. In particular, $|\tilde {\bf x}(1)-{\bf x}_f|\leq \left(\sqrt{\frac{2}{k}(\bar E+\epsilon)}\right)e^{L^2(\bar E+\epsilon)}$.*
:::

# Case study

#### Articulated arm

:::: {#two_links .figure}
::: caption
Vertical motion (a) and circular motion (c) of the two-links articulated arm. The links are in blue and black. The trajectory of the tip is marked in red. We draw the initial and final state and an intermediate state. The joint angles are given in (b) and (d) respectively. []{#two_links label="two_links"}
:::
::::

We first study the 2R robot introduced earlier. Our goal is to plan the motion of the tip of the arm, from an initial state ${\bf x}(0)={\bf x}_i=(\sqrt{2}/2,1-\sqrt{2}/2,\pi/2,-\pi/4)$, where we recall that the coordinates are $(x,y,\theta_1,\theta_2)$, to a final state ${\bf x}(1)={\bf x}_f=(\sqrt{2}/2,1+\sqrt{2}/2,\pi/2,\pi/4)$. We furthermore require the motion to follow a *straight line* given by $x=constant$. The resulting motion planning problem thus contains, in addition to the two holonomic constraints relating the tip of the arm to the angles given in Eq. [\[eq:twoarmconst\]](#eq:twoarmconst){reference-type="eqref" reference="eq:twoarmconst"}, the constraint $q_3({\bf x})=x-x_i=0$ and the corresponding constrained direction is $\frac{\partial q_3}{\partial {\bf x}}=(1,0,0,0)^\top$. Given these constraints, we implement the three steps of the method outlined above show the results in Fig. [3](#two_links){reference-type="ref" reference="two_links"}. We then replaced the constraint of vertical motion by asking that the tip follows an arc of a circle. The corresponding holonomic constraint is $q_4({\bf x})=(x-x_c)^2+(y-y_c)^2 - r=0$ for some constants $x_c,y_c,r$. The differential of this constraint is easily evaluated. We show in Fig. [\[two_link_circular\]](#two_link_circular){reference-type="ref" reference="two_link_circular"} the result obtained. Note that this illustrate the use of our method to solve *inverse kinematic problems* numerically.

#### Unicycle

Consider the unicyle described above with coordinates $(x,y,\theta)$. We desire to transfer the unicycle from $(x(0),y(0),\theta(0))=(-1,0,0)$ to $(x(1),y(1),\theta(1))=(1,0,0)$ without slip (a non-holonomic constraint). In addition, there are two point obstacles located at $(-0.7,0),(0.7,0)$ which the unicycle should avoid in the xy-plane. Provided these constraints, we first build an inner product $G(x)$ as described earlier. We then provide an arbitrary curve connecting $(-1,0,0)$ and $(1,0,0)$ and avoiding the obstacles--we called this curve the initial sketch. We opted simply for a sinusoidal curve in xy-plane and kept $\theta\equiv 0$, as shown in Fig. [\[3D_initial\]](#3D_initial){reference-type="ref" reference="3D_initial"}. As observed in Fig. [\[2D_initial\]](#2D_initial){reference-type="ref" reference="2D_initial"}, the unicycle certainly cannot follow this curve, as the motion direction is not aligned with the unicycle orientation or, in other words, the non-slip constraint is not met.

Recall that the solution of GHF equations [\[HFE\]](#HFE){reference-type="eqref" reference="HFE"} is a curve connecting the initial and final states when $s$ fixed. In Figs. [\[3D_0.0001\]](#3D_0.0001){reference-type="ref" reference="3D_0.0001"} to [\[3D_final\]](#3D_final){reference-type="ref" reference="3D_final"}, we show the gradual deformation of the curve in configuration space as $s$ increases. In the final step $s=4$, the curve becomes almost admissible and we see that the unicycle can basically follow such trajectory to reach its final state. It is worth noticing that because the obstacles are very close to the initial and final states, the unicycle has to move backward first in order to have more room to maneuver around said obstacles. Similarly, it overshoots the second obstacles before backing up and parking at its final destination.

:::: {#unicycle_solution .figure latex-placement="ht!"}
::: caption
Path planning for a unicycle avoiding two point obstacles. The red dots are the two obstacles, the blue curves are the solution of GHF equations at different $s$. In the plan views of initial curve and final curve, unicycle positions are marked along the curve, with its orientation labeled with red arrows
:::
::::

#### Car

We now illustrate our method for planning the motion of a car with position $(x,y) \in \mathbbm{R}^2$, body orientation $\phi$ and wheel angle $\theta$. A top view of car is illustrated in Fig. [\[fig:boxcar\]](#fig:boxcar){reference-type="ref" reference="fig:boxcar"} and the equations of motion equation are: $$\begin{equation}
\label{boxcar_dynamics}
\begin{pmatrix}\dot x\\\dot y\\\dot \theta\\ \dot \phi\end{pmatrix}
=u_1\begin{pmatrix}\cos\phi\\\sin\phi\\0\\\frac{1}{d}\sin\theta\end{pmatrix}+u_2\begin{pmatrix}0\\0\\1\\0\end{pmatrix},
\end{equation}$$ where $u_1$ is the throttle input, $u_2$ is the steering input and $d$ is the distance between front wheels axis and rear wheels axis. We have studied this example in our paper [@Belabbas2017NewMF], and we refer the reader to this paper for an explicit derivation of the corresponding $G({\bf x})$.

Our first experiment is a $180^\circ$ turn. Our initial sketch for this motion is illustrated in Fig. [\[car_180_initial\]](#car_180_initial){reference-type="ref" reference="car_180_initial"}. It is clear that, unless equipped with omniwheels or $d=0$, the car cannot perform the motion illustrated. Interestingly, Motionsketch deforms this curve into the well-known 3-points turn path illustrated in Fig. [\[car_180_free\]](#car_180_free){reference-type="ref" reference="car_180_free"}. This corresponds to the most efficient way of $180^\circ$ turning of a car in practice, assuming there are no any other spatial obstacles.

If in addition, we impose add parallel curbs, which are encoded in the barrier function $b({\bf x})$ as described earlier, the constrained space the car can move in results in additional back-and-forth. The narrower the street, the more back-and-forth are needed. We provide additional examples in the webpage[^3].

:::: {#car_180 .figure}
::: caption
Car $180^\circ$ turn experiment.
:::
::::

We conclude with the case of a car turning in a narrow street. The initial curve is simply an L-shaped curve in xy-plane with $\phi$ linear with respect to $t$ and $\theta\equiv 0$, as illustrated in Fig. [\[car_90_initial\]](#car_90_initial){reference-type="ref" reference="car_90_initial"}. With the curbs modeled as obstacles, our method generates the relatively "optimal" path for this corner turn. Interestingly enough, the car is able to perform the turn in one shot if the street is relatively wide as shown in Fig. [\[car_90_wide\]](#car_90_wide){reference-type="ref" reference="car_90_wide"}, or may need extra maneuvering if the street is narrow, as shown in Fig. [\[car_90_wide\]](#car_90_wide){reference-type="ref" reference="car_90_wide"}. We emphasize that both simulation are performed with the same initial curve provided in Fig. [\[car_90_initial\]](#car_90_initial){reference-type="ref" reference="car_90_initial"}. The only difference is the street width. Whether one shot or two is automatically determined by our method without any further specification.

Finally, we note that in addition to the curb of the streets which are modeled as obstacles in the xy-plane, we also put limits on the steering angle $\theta$ as an obstacle for the $\theta$ variable.

:::: {#car_90 .figure}
::: caption
Car street corner turn experiment
:::
::::

#### Multi-vehicle path planning

We show that multiple vehicles can be path planned simultaneously using our methods. In the first simulation two unicycles are initially at states $(0,1,0),(0,-1,0)$; that is, parked at xy-coordinate $(0,1),(0,-1)$ while both facing east. The task is to swap the position of the two unicycles. The initial sketch is a circle passing through the two unicycles -- clearly these two paths are infeasible since the orientation vectors of the unicycles are not tangent to the paths. After running our algorithm, the two initial sketch of paths deform into the two V-shaped paths and now the two unicycles are able to perform the swap of positions along such paths *while avoiding collisions*. While readers might think the previous example has no major difference compared with path planning for single vehicle and hence less challenging, the next example is more interesting and shows the power of our algorithm in multi-vehicle path planning. In this case one unicycle is supposed to move from $(-1,0,\pi/2)$ to $(1,0,\pi/2)$ while the other one is supposed to move from $(0,-1,0)$ to $(0,1,0)$.

:::: {#two_cars .figure}
::: caption
Multi-vehicles motion planning with collision avoidance. []{#two_cars label="two_cars"}
:::
::::

# Summary and discussion

We have provided in this paper a guide to the implementation of the method we termed MotionSketch for solving motion planning problems. We have illustrated the use of the method on examples with holonomic, non-holonomic and obstacle constraints, and have demonstrated that the method yields good practical results.

The salient points of the method were that it encodes all the constraints into a Riemannian inner product, and that it requires an initial sketch of the curve joining a desired final state to an initial state. This curve however does not need to meet the holonomic and non-holonomic constraints and is thus often easily obtained. In fact, if the space is convex, a straight line joining the two states most often meets the constraints.

Amongst the problems that are also readily solved using MotionSketch, but that we did not show here, we mention multi-vehicle motion planning with collision avoidance. For example, think of having to plan the trajectory of two non-holonomic cars with the constraints that they should avoid each other. This can be done using our method as follows: denote by $(x_i,y_i,\theta_i,\phi_i)$ the coordinates describing the state of car $i$, and by $G_i\in \mathbbm{R}^{4 \times 4}$ the corresponding Riemannian inner products modeling the constraints for each car (e.g. max turning angle as am obstacle in $\theta$, curbs, etc.). In order to model the two vehicles scenario, we first consider the cartesian product of the coordinates with metric $\bar G \in \mathbbm{R}^{8 \times 8}$ a block diagonal matrix with blocks $G_i$. In order to avoid collisions between the cars, it suffices to place an obstacle around the "diagonal" subspace $x_1=x_2$ and $y_1=y_2$. As we have seen earlier, adding obstacles to a metric only requires multiplying by a barrier function, hence we can set $G(x) = b(x) \bar G(x)$. This procedure generalizes in a straightforward way to the case of more than two vehicles.

#### On the computational complexity of solving the GHF

The numerically intensive part of the method lies in solving the geometric heat flow, which is a system of parabolic partial differential equations. We point out that solving such a PDE can be done rather efficiently, owing to the fact that the complexity scales polynomially with the dimension, and not exponentially, and the fact that there exists parallel algorithms to do so.

To elaborate on the first point, the main reason why the PDE we use scales well is that the *domain* of its solution has a *constant* dimension of two. For most PDEs encountered in engineering, such as the heat equation, or the Hamilton-Jacobi-Bellman equation, the dimension of the problem affects the dimension of the *domain* of the solution seeked, whereas is our case, it affects the dimension of the image of the solution. A linear increase in the dimension of the domain yields what is often referred to as the *curse of dimensionality*, as the number of interpolation points needed to represent a function on a domain of dimension $n$ grows exponentially with $n$. Note however that the domain of our PDE is *always* two-dimensional, but the dimension of the image increases linearly, the number of interpolation points grows *linearly* with the dimension. Hence our PDE does not suffer from the curse of dimensionality and thus scales well to higher-dimensional problems. We refer to, e.g., `\cite{}`{=latex} for a more detailed discussion on the complexity of solving such PDEs. In practice, using MATLAB on a common laptop computer with non-optimized code (in particular, MATLAB does not solve such PDEs using multiple cores), the computation time was of the order of seconds to minutes, depending on the complexity of the problem. Per our discussion above, we believe however that there is ample room for improvement on this front.

::: thebibliography
10

Mohamed-Ali Belabbas and Shenyu Liu. New method for motion planning for non-holonomic systems using partial differential equations. , pages 4189--4194, 2017.

Roger W Brockett. On the rectification of vibratory motion. , 20(1-2):91--96, 1989.

H. Choset, K.M. Lynch, S. Hutchinson, G. Kantor, W. Burgard, L. Kavraki, and S. Thrun. . A Bradford book. Prentice Hall of India, 2005.

Kai-Seng Chou and Xi-Ping Zhu. . CRC Press book, 2001.

Tobias Colding, William Minicozzi, Erik Pedersen, et al. Mean curvature flow. , 52(2):297--333, 2015.

H. Dai, A. Valenzuela, and R. Tedrake. Whole-body motion planning with centroidal dynamics and full kinematics. In *2014 IEEE-RAS International Conference on Humanoid Robots*, pages 295--302, Nov 2014.

M.P. do Carmo. . Mathematics (Boston, Mass.). Birkhäuser, 1992.

Jean-Paul Gauthier and Matthias Kawskiz. Minimal complexity sinusoidal controls for path planning. In *Decision and Control (CDC), 2014 IEEE 53rd Annual Conference on*, pages 3731--3736. IEEE, 2014.

Sertac Karaman and Emilio Frazzoli. Sampling-based algorithms for optimal motion planning. , 30(7):846--894, 2011.

J. Kuffner, S. Kagami, K. Nishiwaki, M. Inaba, and H. Inoue. Online footstep planning for humanoid robots. In *2003 IEEE International Conference on Robotics and Automation*, volume 1, pages 932--937 vol.1, Sept 2003.

Gerardo Lafferriere and Hector J Sussmann. A differential geometric approach to motion planning. In *Nonholonomic motion planning*, pages 235--270. Springer, 1993.

Jean-Claude Latombe. , volume 124. Springer Science & Business Media, 2012.

J.P. Laumond. . Lecture notes in control and information sciences. Springer, 1998.

S. M. LaValle. . Cambridge University Press, Cambridge, U.K., 2006. Available at http://planning.cs.uiuc.edu/.

G. Leitmann. Guaranteed avoidance strategies. , 32(4):569--576, Dec 1980.

Richard M Murray, Zexiang Li, S Shankar Sastry, and S Shankara Sastry. . CRC press, 1994.

Jorge Nocedal and Stephen J. Wright. , chapter 19. New York : Springer, 1999.

Brian Paden, Michal Čáp, Sze Zheng Yong, Dmitry Yershov, and Emilio Frazzoli. A survey of motion planning and control techniques for self-driving urban vehicles. , 1(1):33--55, 2016.

Claire J Tomlin, Ian Mitchell, Alexandre M Bayen, and Meeko Oishi. Computational techniques for the verification of hybrid systems. , 91(7):986--1001, 2003.
:::

[^1]: $^{*}$Shenyu Liu and Mohamed Ali Belabbas are with the department of Electrical and Computer Engineering and the Coordinated Science Laboratory, University of Illinois, Urbana-Champaign. `sliu113,belabbas@illinois.edu`

[^2]: <https://publish.illinois.edu/belabbas/motion-planning/>

[^3]: <https://publish.illinois.edu/belabbas/motion-planning/>
