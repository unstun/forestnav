---
citation_key: Marinho2016Functional
arxiv_id: 1601.03648
arxiv_url: https://arxiv.org/abs/1601.03648
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:06:24Z
origin: ai+web
reviewed: false
---

# Introduction & Related Work {#sec:intro}

Motion planning is an important component of robotics: it ensures that robots are able to safely move from a start to a goal configuration without colliding with obstacles. *Trajectory optimizers* for motion planning focus on finding feasible configuration-space trajectories that are also efficient---e.g., approximately locally optimal for some cost function. Recently, trajectory optimizers have demonstrated great success in a number of high-dimensional real-world problems. [@quinlan1993elastic; @schulman2013finding; @todorov2005generalized; @van2011lqg] Often, they work by defining a cost functional over an infinite-dimensional Hilbert space of trajectories, then taking steps down the functional gradient of cost to search for smooth, collision-free trajectories. [@Zucker13; @Ratliff09] In this work we exploit the same functional gradient approach, but with a novel approach to trajectory representation. While previous algorithms are derived for trajectories in Hilbert spaces in theory, *in practice* they commit to a finite parameterization of trajectories in order to instantiate a gradient update [@Zucker13; @park2012itomp; @stomp]---typically a large but finite list of discretized waypoints. The number of waypoints is a parameter that trades off between computational complexity and trajectory expressiveness. Our work frees the optimizer from a discrete parameterization, enabling it to perform gradient descent on a much more general trajectory parameterization: reproducing-kernel Hilbert spaces (RKHSs), [@smolabook; @KW71; @aronszajn50] of which waypoint parameterizations are merely one instance. RKHSs impose just enough structure on generic Hilbert spaces to enable a concrete and implementable gradient update rule, while leaving the choice of parameterization flexible: different kernels lead to different geometries.

Our contribution is two-fold. Our *theoretical* contribution is the formulation of functional gradient descent motion planning in RKHSs, as the minimization of a cost functional regularized by the RKHS norm. Regularizing by the RKHS norm is a common way to ensure smoothness in function approximation, [@hofman08] and we apply the same idea to trajectory parametrization. By choosing the RKHS appropriately, the trajectory norm can quantify different forms of smoothness or efficiency, such as any low $n$-th order derivative. [@yuan10] So, RKHS norm regularization can be tuned to prefer trajectories that are smooth with, for example, low velocity, acceleration, or jerk.

Our *practical* contribution is an algorithm for very efficient motion planning in inherently smooth trajectory space with low-dimensional parameterizations. Unlike discretized parameterizations, which require many waypoints to produce smooth trajectories, our algorithm can represent and search for smooth trajectories with only a few point evaluations. The inherent smoothness of our trajectory space also increases efficiency; our parametrization allows the optimizer to take large steps at every iteration without violating trajectory smoothness, therefore converging to a collision-free trajectory faster than competing approaches.

Our experiments demonstrate the effectiveness of planning under RKHS, and show how different choices of kernels yield different forms of trajectory efficiency. Section [6](#sec:results){reference-type="ref" reference="sec:results"} illustrates these advantages of RKHSs, and compares different choices of kernels.

# Trajectories in an RKHS {#sec:planning_rkhs}

In this paper we perform trajectory optimization in a more restricted space of trajectories, we constrain the domain where trajectories are defined to *Reproducing Kernel Hilbert Spaces*. We trade off representational power for an inherent smooth representation of trajectories, given by a kernel metric.

A trajectory is a function $\boldsymbol\xi:[0,1]\to\mathcal C$ mapping time $t\in[0,1]$ to robot configurations $\boldsymbol{\xi}(t)\in\mathcal{C}\equiv\mathbb R^D$. We can treat a set of trajectories as a Hilbert space by defining vector-space operations such as addition and scalar multiplication of trajectories. [@kreyszig92] And, we can upgrade our Hilbert space to an RKHS $\mathcal H$ by assuming additional structure: for any $y\in\mathcal C$ and $t\in[0,1]$, the functional $\xi\mapsto\langle y, \xi(t)\rangle$ must be continuous. [@smolabook; @W98; @Ratliff07] Note that, since configuration space is typically multidimensional ($D>1$), our trajectories form an RKHS of *vector-valued* functions, [@pontil05] defined by the above property. The reproducing Kernel associated with a vector valued RKHS, becomes a matrix valued kernel ${K}: [0,1]\times[0,1]\rightarrow \mathcal{C}\times\mathcal{C}$. Eq. [\[eq:vecrkhs\]](#eq:vecrkhs){reference-type="ref" reference="eq:vecrkhs"} represents the kernel matrix of joint interactions for two different time instances: $$\begin{align}
\label{eq:vecrkhs}
{K}(t,t')=\begin{bmatrix}
k_{1,1}(t,t')& k_{1,2}(t,t')\ \  \dots\  k_{1,D}(t,t')\\
k_{2,1}(t,t')& k_{2,2}(t,t')\ \  \dots\  k_{2,D}(t,t')\\
\vdots &\ddots\ \ \ \ \ \ \ \ \ \ \ \vdots\\
k_{D,1}(t,t')& k_{D,2}(t,t')\ \  \dots\ k_{D,D}(t,t')
\end{bmatrix}
\end{align}$$ This matrix has a very intuitive physical interpretation. It can be regarded as an inertia tensor of a rigid body changing over time. Each element $k_{d,d'}(t,t')$ tells us how joint $\xi_d(t)$ affects the motion of joint $\xi_{d'}(t')$, *i.e.* its degree of correlation or similarity between the two configurations. In practice, off-diagonal terms of ([\[eq:vecrkhs\]](#eq:vecrkhs){reference-type="ref" reference="eq:vecrkhs"}) will not be zero, hence perturbations of a given joint $d$ propagate through time, as well as, through the rest of the joints. The norm and inner product defined in a coupled RKHS can be written in terms of the kernel matrix, via the reproducing property (trajectory evaluation can be represented as an inner product of the vector valued functions in the RKHS): $$\begin{align}
\boldsymbol{y}^{\top}\boldsymbol{\xi}(\cdot)&= \langle \xi, {K}(t,\cdot) \boldsymbol{y}\rangle_{\mathcal{H}},\ \ \forall{\boldsymbol{y}\in \mathcal{C}}
\begin{matrix}\end{matrix}
\end{align}$$

A trajectory in the RKHS admits a representation in terms of the finite support {$t_i\}_{i=1}^{N}\in \mathcal{T}$. $$\begin{align}
\boldsymbol{y}^{\top}\boldsymbol{\xi}^{\ast} (\cdot)&= \sum_{t_i\in \mathcal{T}} a_{i} {K}(t,t_i)\boldsymbol{y}\begin{matrix}\end{matrix}
\end{align}$$ If we consider the configuration vector $\boldsymbol{y}\equiv \boldsymbol{e}_d$ to be the indicator of joint $d$, then we can capture its evolution over time $\xi_d(t)= \sum_{d'=1}^{D} \sum_i a_{i,d'} k_{d,d'}(t,t_i)$, taking into account the effect of all other joints $d'$.

The inner product in $\mathcal{H}$ of functions $\boldsymbol{\xi}^1(\cdot) =  \sum_{i,d} a_{i,d}k(t_i,\cdot)\boldsymbol{e}_d$ and $\boldsymbol{\xi}^2(\cdot) =  \sum_{j,d} b_{j,d}k(t_j,\cdot)\boldsymbol{e}_d$ is defined as: $$\begin{align}
&\langle \boldsymbol{\xi}^1,\boldsymbol{\xi}^2 \rangle_{\mathcal{H}}=\sum_d \langle \xi_d^1,\xi_d^2 \rangle_{\mathcal{H}}=\sum_d\sum_{i,j} a_{i,d}b_{j,d} k(t_i,t_j)\\ \label{eq:norm}
&\|\boldsymbol{\xi}\|^2_{\mathcal{H}} = \langle\boldsymbol\xi,\boldsymbol\xi\rangle = \sum_d \sum_{i,j} a_{i,d} a_{j,d} k(t_i,t_j)
\begin{matrix}\end{matrix}
\end{align}$$ For example, in the Gaussian RBF RKHS (with kernel $k_d(t,t') =\text{exp}(\|t-t'\|^2/2\sigma^2)$), a trajectory is a weighted sum of radial basis functions: $$\begin{align}
\label{eq:rbftraj}
\boldsymbol{\xi}(t) =& \sum_{d,i} a_{i,d}\   \text{exp}\left(\frac{\|t-t_i\|^2}{2\sigma^2}\right)\boldsymbol{e}_d,\ \ {a_{i,d}}\in\mathbb{R}
\begin{matrix}\end{matrix}
\end{align}$$ The coefficients $a_{i,d}$ assess how important a particular joint $d$ at time $t_i$ is to the overall trajectory. They can be interpreted as weights of local perturbations to the motions of different joints centered at different times. The trajectory norm measures the size of the perturbations, and the correlation among them, quantifying how complex the trajectory is in the RKHS.

# Motion Planning in an RKHS {#sec:trajopt}

In this section we describe how trajectory optimization can be achieved by functional gradient descent in an RKHS of trajectories.

## Cost Functional {#sec:cost}

We introduce a cost functional $\mathcal{U}:\mathcal{H}\rightarrow \mathbb{R}$ that maps each trajectory to a scalar cost. This functional quantifies the quality of a given a trajectory (function in the RKHS). $\mathcal{U}$ trades off between a regularization term that measures the efficiency of the trajectory, and an obstacle term that measures its proximity to obstacles: $$\begin{align}
\label{eq:cost}
&\mathcal{U}[\boldsymbol{\xi}]= \mathcal{U}_{obs}[\boldsymbol{\xi}] +\frac{\beta}{2}\|\boldsymbol{\xi}\|_{\mathcal{H}}^2
 \begin{matrix}\end{matrix}
\end{align}$$ As described in Section [4](#sec:norm){reference-type="ref" reference="sec:norm"}, we choose our RKHS so that the regularization term encodes our desired notion of smoothness or trajectory efficiency (minimum length, velocity, acceleration, jerk).

The obstacle cost functional is defined on trajectories in configuration space, but obstacles are defined in the robot's workspace $\mathcal{W}\equiv \mathbb{R}^3$. So, we connect configuration space to workspace via a *forward kinematics* map $x$: if $\mathcal B$ is the set of body points of the robot, then $x:\mathcal C\times\mathcal B\to\mathcal W$ tells us the workspace coordinates of a given body point when the robot is in a given configuration. We can then decompose the obstacle cost functional as: $$\begin{align}
\label{eq:reduce}
{\mathcal{U}}_{obs}[\boldsymbol{\xi}] &= \mathop{\textrm{reduce}}_{t,u} c\left(x(\boldsymbol{\xi}(t),u)\right)
\begin{matrix}\end{matrix}
\end{align}$$ where $\textrm{reduce}$ is an operator that aggregates costs over the entire trajectory and robot body---e.g., a supremum or an integral, see Section [5](#sec:costa){reference-type="ref" reference="sec:costa"}. We assume that the $\textrm{reduce}$ operator takes (at least approximately) the form of a sum over some finite set of (time, body point) pairs $\boldsymbol{\mathcal T}(\boldsymbol\xi)$: $$\begin{align}
\label{eq:empirical}
{\mathcal{U}}_{obs}[\boldsymbol{\xi}] &= \sum_{(t,u)\in\boldsymbol{\mathcal T}(\boldsymbol\xi)} c\left(x(\boldsymbol{\xi}(t),u)\right)
\begin{matrix}\end{matrix}
\end{align}$$ For example, the supremum operator takes this form except on a measure-zero set of trajectories: whenever there is a unique supremum $(t,u)$, then $\boldsymbol{\mathcal T}(\boldsymbol\xi)$ is the singleton set $\{(t,u)\}$. Integral operators do not take this form, but they can be well approximated in this form using quadrature rules, see Section [5.0.2](#sec:integralcost){reference-type="ref" reference="sec:integralcost"}.

:::: algorithm
::: algorithmic
Initialize to a straight line trajectory ${\xi}^0_d(t)=\xi_d(0)+ (\xi_d(1)-\xi_d(0))t$. Compute $\mathcal{U}_{obs}[\boldsymbol{\xi}^n]$ ([\[eq:funccost\]](#eq:funccost){reference-type="ref" reference="eq:funccost"}). Find the support $\boldsymbol{\mathcal{T}}(\boldsymbol{\xi})=\{t_i,u_i\},i=1,\dots,N$ time/body points ([\[eq:empirical\]](#eq:empirical){reference-type="ref" reference="eq:empirical"}). Evaluate the gradient cost $\nabla c(\boldsymbol{\xi}(t_i),u_i)$ and $\mathbf{J}(t_i,u_i)$ Update trajectory:\
$\qquad\qquad\boldsymbol{\xi}^{n+1}= (1-\frac{1}{\lambda})\boldsymbol{\xi}^{n}-\frac{1}{\lambda}
\sum_{(t, u)\in\boldsymbol{\mathcal T}(\boldsymbol\xi)} \left(  \mathbf J^\top(t,u) \nabla c(x(\boldsymbol{\xi}(t),u))\right)^\top K(t,\cdot)$ If constraints are present, project onto constraint set (Section [\[eq:constsol\]](#eq:constsol){reference-type="ref" reference="eq:constsol"}). ***Return:*** Final trajectory $\boldsymbol{\xi}^{*}$ and costs $\|\boldsymbol{\xi}\|^2_{\mathcal{H}}, \mathcal{U}_{obs}$.
:::
::::

## Optimization {#sec:opt}

We can derive the functional gradient update by minimizing a local quadratic approximation of $\mathcal U_{\rm obs}$: $$\begin{align}
\label{eq:mini}
\boldsymbol{\xi}^{n+1}=&\ \text{arg}\min\limits_{\boldsymbol{\xi}}\ \ \langle \boldsymbol{\xi}-\boldsymbol{\xi}^n, \nabla \mathcal{U}[\boldsymbol{\xi}^n] \rangle_{\mathcal{H}} + \frac{\lambda}{2}\|\boldsymbol{\xi}-\boldsymbol{\xi}^n\|^2_{\mathcal{H}}
\begin{matrix}\end{matrix}
\end{align}$$ The quadratic term is based on the RKHS norm, meaning that we prefer "smooth" updates, analogous to @Zucker13 This minimization admits a solution in closed form: $$\begin{align}
\label{eq:update}
% &\sum_{t_i\in\mathcal{T}} \nabla c[\boldsymbol{\xi}^n,t_i]J^Tk(t_i,\cdot)  + (\beta-\lambda)\boldsymbol{\xi}^n + \lambda \boldsymbol{\xi} = 0\\
%\nabla_{\boldsymbol{\xi}} \left [\sum_{t_i\in\mathcal{T}}  \langle \boldsymbol{\xi},  \nabla c[\boldsymbol{\xi}^n,t_i]J^Tk(t_i,\cdot) \rangle_{\mathcal{H}} + (\beta-\lambda) \langle \boldsymbol{\xi}, \boldsymbol{\xi}^n \rangle_{\mathcal{H}}+\frac{\lambda}{2}\langle \boldsymbol{\xi},\boldsymbol{\xi} \rangle_{\mathcal{H}} \right ] &=0 \nt
\boldsymbol{\xi}^{n+1}(\cdot)& = \left(1-\frac{1}{\lambda}\right)\boldsymbol{\xi}^n(\cdot) -\frac{1}{\lambda} \nabla \mathcal{U}_{obs}[\boldsymbol{\xi}^n](\cdot)
\begin{matrix}\end{matrix}
\end{align}$$ Since we have assumed that the cost functional $\mathcal{U}_{obs}[\boldsymbol{\xi}]$ depends only on a finite set of points $\boldsymbol{\mathcal{T}}(\boldsymbol\xi)$ ([\[eq:empirical\]](#eq:empirical){reference-type="ref" reference="eq:empirical"}), it is straightforward to show that the functional gradient update has a finite representation (so that the overall trajectory, which is a sum of such updates, also has a finite representation). In particular, assume the workspace cost field $c$ and the forward kinematics function $x$ are differentiable; then we can obtain the cost functional gradient by the chain rule: [@Ratliff07; @smolabook] $$\begin{align}
\label{eq:funccost}
\nabla\mathcal{U}_{obs}(\cdot)=\sum_{(t, u)\in\boldsymbol{\mathcal T}(\boldsymbol\xi)}
  \left(\mathbf J^\top(t,u) \nabla c(x(\boldsymbol{\xi}(t),u))\right)^{\top}K(t,\cdot)
\begin{matrix}\end{matrix}
\end{align}$$ where $\mathbf J(t,u) = \frac{\partial}{\partial \boldsymbol\xi(t)}x(\boldsymbol\xi(t),u) \in \mathbb{R}^{3\times D}$ is the workspace Jacobian matrix at time $t$ for body point $u$, so that the kernel function $K(t,\cdot)$ is the gradient of $\boldsymbol\xi(t)$ with respect to $\boldsymbol\xi$. The kernel matrix is fully defined in Equation ([\[eq:vecrkhs\]](#eq:vecrkhs){reference-type="ref" reference="eq:vecrkhs"}).

This solution is a generic form of functional gradient optimization with a *directly instantiable* obstacle gradient that does not depend on a predetermined set of waypoints, offering a more expressive representation with fewer parameters. We derive a constrained optimization update rule, by solving the KKT conditions for a vector of Lagrange multipliers, see Section [8.3](#sec:constraints){reference-type="ref" reference="sec:constraints"}. The full method is summarized as Algorithm [\[alg:trajopt\]](#alg:trajopt){reference-type="ref" reference="alg:trajopt"}.

# Trajectory Efficiency as Norm Encoding in RKHS {#sec:norm}

In different applications it is useful to consider different notions of trajectory efficiency or smoothness. We can do so by choosing RKHSs with appropriate norms. For example, it is often desirable to penalize the velocity, acceleration, jerk, or other derivatives of a trajectory instead of (or in addition to) its magnitude. To do so, we can take advantage of a *derivative reproducing property*: let $\mathcal H_1$ be one of the coordinate RKHSs from our trajectory representation, with kernel $k$. If $k$ has sufficiently many continuous derivatives, then for each partial derivative operator $D^\alpha$, there exist representers $(D^\alpha k)_t\in\mathcal H_1$ such that, for all $f\in\mathcal H_1$, $(D^\alpha f)(t) = \langle (D^\alpha k)_t, f\rangle$ [@zhou08 Theorem 1]. (Here $\alpha$ is a multi-set of indices, indicating which partial derivative we are referring to.) We can therefore define a new RKHS with a norm that penalizes the partial derivative $D^\alpha$: the kernel is $k^\alpha(t, t') = \langle (D^\alpha k)_t, (D^\alpha k)_{t'}\rangle$. If we use this RKHS norm as the smoothness penalty for our trajectories, then our optimizer will automatically seek out trajectories with low velocity, acceleration, or jerk.

Consider an RBF kernel with a reproducing first order derivative: $D^{1}k(t,t_i) =D^1k_{t_i}[t]= \frac{(t-t_i)}{2 \sigma^2} k(t,t_i)$ is the reproducing kernel for the velocity profile of a trajectory defined in an RBF kernel space $k(t,t_i)= \frac{1}{\sqrt{2\pi\sigma^2}}\exp(-\|t-t_i\|^2/2\sigma^2)$. The velocity profile can be written as $D^{1}\boldsymbol{\xi} (t) = \sum_i \beta_i D^{1} k(t,t_i)$, with endpoint conditions $D^1 \boldsymbol{\xi}(0)=\dot{\boldsymbol{q}}_i,\ D^1\boldsymbol{\xi}(1) = \dot{\boldsymbol{q}}_f$.

The trajectory can be found by integrating $D^1\boldsymbol{\xi}(t)$ once and projecting onto the nullspace of the constraints $\boldsymbol{\xi}(0)=\boldsymbol{q}_i,\boldsymbol{\xi}(1)=\boldsymbol{q}_f$. $$\begin{align}
\boldsymbol{\xi}(T) &= \int\limits_0^1 D^{1} \boldsymbol{\xi}(t) dt = \sum_i \beta_i \int\limits_0^1  \frac{(t-t_i)}{2 \sigma^2}  k(t,t_i) dt= \sum_i \beta_i \left[k(T,t_i) - k(0,t_i)\right] +\boldsymbol{q}_i
\begin{matrix}\end{matrix}
\end{align}$$ The initial condition is verified automatically and the endpoint condition can be written as $\boldsymbol{q}_f = \sum_i \beta_i \left[k(1,t_i) - k(0,t_i)\right] +\boldsymbol{q}_i$, this imposes additional information over the coefficients $\beta_i\in \mathcal{C}$. Here we explicitly considered only a $\mathcal{H}^1$ space, but extensions to higher order derivatives can be derived similarly integrating p times to obtain the trajectory profile. Constraints over higher derivatives can be computed using any constraint projection method. The update rule in this setting can be derived using the natural gradient in the space, where the new obstacle gradient becomes: $$\begin{align}
\nabla U_{obs}[\boldsymbol{\xi}](t) &= \sum_j^n\sum_{(t_i,u_i)\in \mathcal{T}} \left( \mathbf{J}^\top(t_i,u_i) \nabla c(\ x(\boldsymbol{\xi}(t_i),u_i)\ )\right)^\top D^{j} k(t_i,t)\ \ \label{eq:dergrad}
\begin{matrix}\end{matrix}
\end{align}$$ Regularization schemes in different RKHSs may encode different forms of trajectory efficiency. We provide a form of penalizing trajectory complexity in different forms by minimizing the trajectory norm in the RKHS. This may be defined in terms of the reproducing kernel, by sums, products, tensor product of kernels, or any closed kernel operation.

## Kernel Metric in RKHS {#sec:vecnorm}

The norm provides a form of quantifying how complex a trajectory is in the space associated with the RKHS kernel metric $K$. The kernel metric is determined by the kernel functions we choose for the RKHS, as we have seen before (Section [4](#sec:norm){reference-type="ref" reference="sec:norm"}). Likewise, the set of time points $\mathcal{T}$ that support the trajectory contribute to the design of the kernel metric: $$\begin{align}
 \|\boldsymbol{\xi}\|_{\mathcal{H}}^2&=\sum_{d}\sum_{t_i,t_j\in \mathcal{T}} {a}_{d,i} k_{d,d'}(t_i,t_j) {a}_{d',j}\\ \notag
 &=\sum_{t_i,t_j\in \mathcal{T}} \boldsymbol{a}_{i}^\top K(t_i,t_j) \boldsymbol{a}_{j'},\ \ \boldsymbol{a}_i,\boldsymbol{a}_j\in\mathbb{R}^{D}\\ \notag
 &=\boldsymbol{a}^\top \boldsymbol{K}(\mathcal{T},\mathcal{T})\boldsymbol{a}, \boldsymbol{a}\in\mathbb{R}^{DN}
 \begin{matrix}\end{matrix}
\end{align}$$ Here $\boldsymbol{a}$ is the concatenation of all coefficients $\boldsymbol{a}_i$ over $\mathcal{T},\ |\mathcal{T}|=N$. $\boldsymbol{K}(\mathcal{T},\mathcal{T})\in\mathbb{R}^{DN\times DN}$ is the *Gram matrix* for all time points in the support of $\boldsymbol{\xi}$, and all joint angles of the robot. This matrix expresses the degree of correlation or similarity among different joints throughout the time points in $\mathcal{T}$. It can be interpreted, alternatively, as a tensor metric in a Riemannian manifold. [@Amari98; @Ratliff15] Its inverse is the key element that bridges the gradient of functional cost $\nabla \mathcal{U}$ (gradient in the RKHS, Eq.[\[eq:funccost\]](#eq:funccost){reference-type="ref" reference="eq:funccost"} ), and its conventional gradient (Euclidean gradient).[^1] $$\begin{align}
\nabla \mathcal{U} = \boldsymbol{K}^{-1}(\mathcal{T},\mathcal{T}) \nabla_{E}\ \mathcal{U}\\ \notag
\begin{matrix}\end{matrix}
\end{align}$$ The minimizer of the full functional cost $\mathcal{U}$ has a closed form solution in ([\[eq:update\]](#eq:update){reference-type="ref" reference="eq:update"}). Where the gradient $\nabla \mathcal{U}$, is the natural gradient in the RKHS. This can be seen as a warped version of the obstacle cost gradient according to the RKHS metric.

# Cost Functional Analysis {#sec:costa}

Next we analyze how the cost functional (different forms of the reduce operation in Section [3.1](#sec:cost){reference-type="ref" reference="sec:cost"}), affect obstacle avoidance performance, and the resulting trajectory (Section [5](#sec:costa){reference-type="ref" reference="sec:costa"}). In this paper, we adopt a maximum cost version (Section [5.0.1](#sec:maxcost){reference-type="ref" reference="sec:maxcost"}), and an approximate integral cost version of the obstacle cost functional (Section [5.0.2](#sec:integralcost){reference-type="ref" reference="sec:integralcost"}). Other variants could be considered, providing the trajectory support remains finite, but we leave this as future work. Additionally, we compare the two forms (Section [5.1](#sec:integralcost-experiments){reference-type="ref" reference="sec:integralcost-experiments"}), against a more commonly used cost functional, the path integral cost, [@Ratliff09] and we show our formulations do not perform worse, while being faster to compute. Based on these experiments, in the remaining sections of the paper we consider only the max cost formulation, which we believe represents a good tradeoff between speed and performance.

### Max Cost Formulation {#sec:maxcost}

The maximum obstacle cost penalizes points in the trajectory close to obstacles, *i.e.* high cost regions in workspace (regions inside/near obstacles). This maximum cost version of the reduce operation, considered in Eq.([\[eq:reduce\]](#eq:reduce){reference-type="ref" reference="eq:reduce"}), can be described as picking time points (sampling), deepest inside or closest to obstacles, see Figure [1](#fig:1){reference-type="ref" reference="fig:1"}.

:::: {#fig:1 .figure latex-placement="ht!"}
![](Marinho2016Functional_figs/explanation_all.png){width=".6\\textwidth"}

::: caption
At every iteration, the optimizer takes the current trajectory (black) and identifies the point of maximum obstacle cost $t_i$ (orange points). It then updates the trajectory by a point evaluation function centered around $t_i$. Grey regions depict isocontours of the obstacle cost field (darker means closest to obstacles, higher cost).
:::
::::

The sampling strategy for picking time points to represent the trajectory cost can be chosen arbitrarily, and further improved for time efficiency. In this paper, we consider a simple version, where we sample points along sections of the trajectory, and choose $Nx$ maximum violating points, one per section.

This max cost strategy allows us to represent trajectories in terms of a few points, rather then a set of finely discretized waypoints. This is a simplified version of the obstacle cost functional, that yields a more compact representation.[@Ratliff09; @park2012itomp; @stomp]

### Integral Cost Formulation {#sec:integralcost}

Instead of scoring a trajectory by the supremum of obstacle cost over time and body points, it is common to integrate cost over the entire trajectory and body, with the trajectory integral weighted by arc length to avoid velocity dependence. [@Zucker13] While this path integral depends on all time and body points, we can approximate it to high accuracy from a finite number of point evaluations using numerical quadrature. [@numericalrecipes] $\boldsymbol{\mathcal{T}}(\boldsymbol\xi)$ then becomes the set of abscissas of the quadrature method, which can be adaptively chosen on each time step (e.g., to bracket the top few local optima of obstacle cost), see Section [8.1](#sec:pathintegralapprox){reference-type="ref" reference="sec:pathintegralapprox"}. In our experiments, we have observed good results with Gauss-Legendre quadrature.

## Integral vs. Max cost Formulation {#sec:integralcost-experiments}

:::: {#fig:comparisons .figure latex-placement="ht!"}
::: caption
a) The integral costs after 5 large steps comparing between optimizing using our obstacle cost formulation with Gaussian RBG kernels vs. the integral formulation (using waypoints). b) A comparison between Gaussian RBF kernel integral cost using our max formulation vs. the approximate quadrature cost (20 points, 10 iterations).
:::
::::

We show that our new formulation does not hinder the optimization -- that it leads to practically equivalent results as an integral over time and body points. [@Zucker13] To do so, we manipulate the cost functional formulation, and measure the resulting trajectories' cost in terms of the integral formulation. Figure [\[fig:maxint\]](#fig:maxint){reference-type="ref" reference="fig:maxint"} shows the comparison: the integral cost increased by only $5\%$ when optimizing for the max. Additionally we tested the max cost formulation against the approximate integral cost using a Gauss-Legendre quadrature method. We performed tests over 100 randomly sampled scenarios and measured the final obstacle cost after 10 iterations. We used 20 points to represent the trajectory in both cases. Figure [\[fig:maxaint\]](#fig:maxaint){reference-type="ref" reference="fig:maxaint"} shows the approximate integral cost formulation is only $8\%$ above the max approach.

# Experimental Results {#sec:results}

In what follows, we compare the performance of RKHS trajectory optimization vs. a discretized version (CHOMP) on a set of motion planning problems in a 2D world for a 3 DOF link planar arm as in Figure [4](#fig:kernels){reference-type="ref" reference="fig:kernels"}, and how different kernels with different norms affect the performance of the algorithm (Section [6.1](#sec:main_experiment){reference-type="ref" reference="sec:main_experiment"}). We then, introduce a series of experiments that illustrate why RKHSs improve optimization (Section [6.2](#sec:larger_steps){reference-type="ref" reference="sec:larger_steps"}).

## RKHS with Radial Basis vs. Waypoints {#sec:main_experiment}

For our main experiment, we systematically evaluate the two parameterizations across a series of planning problems. Although, Gaussian RBFs are a default choice of kernel in many kernel methods, RKHSs can also easily represent other types of kernel functions, *e.g.* For example, B-splines are a popular parameterization of smooth functions, [@ZK95; @PZM95; @Blake98] that are able to express smooth trajectories while avoiding obstacles, even though they are finite dimensional kernels. The choice of kernel should be application driven, and any reproducing kernel can easily be considered under the the optimization framework presented in this paper.

In the following experiment, we manipulate the parameterization (waypoints vs different kernels) as well as the number of iterations (which we use as a covariate in the analysis). To control for the cost functional as a confound, we use the max formulation for both parameterizations. We use iterations as a factor because they are a natural unit in optimization, and because the amount of time per iteration is similar: the computational bottleneck is computing the maximum penetration points. We measure the obstacle and smoothness cost of the resulting trajectories. For the smoothness cost, we use the norm in the waypoint parameterization as opposed to the norm in the RKHS as the common metric.\

:::: {#fig:kernelcost .figure latex-placement="ht!"}
::: caption
Cost over iterations for a 3DoF robot in 2D. Error bars show the standard error over 100 samples.
:::
::::

:::: {#fig:kernels .figure latex-placement="ht!"}
::: caption
Robot 3DoF in C-space. Trajectory after 10 iterations: top-left: Gaussian RBF kernel, top-right: B-splines kernel, bottom-left: Laplaceian RBF kernel, bottom-right: Waypoints.
:::
::::

The RKHS parameterization results in comparable obstacle cost and lower smoothness cost for the same number of iterations. We use 100 different random obstacle placements and keep the start and goal configurations fixed as our experimental setup. The trajectory is represented with 4 maximum violation points over time and robot body points. In the analysis we performed a t-test using the last iteration samples, and showed that the Gaussian RBF RKHS representation resulted in significantly lower obstacle cost ($t(99)=-2.63$, $p<.01$) and smoothness cost ($t(99)=-3.53$, $p<.001$), supporting our hypothesis. We expect this to be true because with the Gaussian RBF parameterization can take larger steps without breaking smoothness, see Section [6.2](#sec:larger_steps){reference-type="ref" reference="sec:larger_steps"}.

We observe that Waypoints and Laplacian RBF kernels with large widths have similar behavior, while Gaussian RBF and B-splines kernels provide a smooth parameterization that allows the algorithm to take larger steps at each iteration. These kernels provide the additional benefit of controlling the motion amplitude, being the most suitable in the implementation of an adaptive motion planner. Laplacian RBF kernels yield similar results as the waypoint parameterization, since it is less affected by the choice of the width of the kernel. Figure [4](#fig:kernels){reference-type="ref" reference="fig:kernels"} provides a qualitative evaluation of the effect of different kernel choices. We compare the effectiveness of obstacle avoidance over 10 iterations, in 100 trials, of 12 randomly placed obstacles in a 2D environment, see Figure [4](#fig:kernels){reference-type="ref" reference="fig:kernels"}.

## RKHSs Allow Larger Steps than Waypoints {#sec:larger_steps}

[]{#fig:largesteps label="fig:largesteps"}

:::: {.figure latex-placement="ht!"}
::: caption
a) 2d trajectory of 1dof robot in a maze environment (obstacle in shaded grey). b)Trajectory profile using different kernels (5 time points in white).
:::
::::

One practical advantage of using an Gaussian RBF RKHS instead of the waypoint parameterization is the ability to take large steps during the optimization. Figure [2](#fig:comparisons){reference-type="ref" reference="fig:comparisons"} compares the two, while taking large steps: it takes 5 Gaussian RBF iterations to solve the problem, but would take 28 iterations with smaller steps for the waypoint parameterization -- otherwise, large steps cause oscillation and break smoothness. The resulting obstacle cost is always lower with Gaussian RBFs ($t(99)=5.32$, $p<.0001$). The smoothness cost is higher ($t(99)=8.86$, $p=<.0001$), as we saw in the previous experiment as well-- qualitatively, however, as Figure [\[fig:largesteps\]](#fig:largesteps){reference-type="ref" reference="fig:largesteps"} shows, the Gaussian RBF trajectories appear smoother, even after just one iteration, as they do not break differential continuity. So far, we used 100 waypoints to represent the trajectory, and only 5 kernel evaluation points for the RKHS. We did also test the waypoint parameterization with 5 waypoints, in order to have an equivalently low dimensional representation. This resulted in much poorer behavior with regards to differential continuity.

## Real World Experiments on a 7-DOF Manipulator

Figure [5](#fig:7dofsd){reference-type="ref" reference="fig:7dofsd"} shows a comparison between the waypoint parametrization (CHOMP) and the RKHS Gaussian RBF on a 7-DOF manipulation task. Figure [\[fig:7dof2\]](#fig:7dof2){reference-type="ref" reference="fig:7dof2"} shows the end-effector traces, after 10 iterations of optimization, for both methods. The path for CHOMP (blue) is very non-smooth and collides with the counter while the Gaussian RBF optimization is able to find a smoother path (orange) that is not in collision. Note that we only use a single max-point for the RKHS version, which leads to much less computation per iteration, as compared to CHOMP. Figure [\[fig:7dof\]](#fig:7dof){reference-type="ref" reference="fig:7dof"} shows the results from both methods after 25 iterations of optimization. CHOMP is now able to find a collision-free path, but the path is still not very smooth as compared to the RKHS-optimized path. These results echo our findings from the robot simulation and planar arm experiments. We are currently looking at more experiments in these high-dimensional configuration spaces, where we believe the RKHS approach with its better representative power can find smoother collision-free paths faster.

:::: {#fig:7dofsd .figure latex-placement="ht!"}
::: caption
7-dof robot experiment, plotting end-effector position from start to goal. (a) Gaussian RBF RKHS with 1 max point (10 iterations, $\lambda=20,\beta=0.5$) vs. Waypoints (10 iterations, $\lambda=200$). (b) Gaussian RBF RKHS with 1 max point (25 iterations, $\lambda=20,\beta=0.5$) vs. Waypoints (25 iterations, $\lambda=200$). []{#fig:7dofsd label="fig:7dofsd"}
:::
::::

# Discussion and Future Work {#sec:discussion}

In this work we presented an expressive kernel approach to trajectory representation: we represent smooth trajectories as vectors in an RKHS. Different kernels lead to different notions of smoothness, including commonly-used variants as special cases. We introduced a functional gradient trajectory optimization method based on our RKHS representation, and demonstrated that this optimizer can take large steps, leading to a smooth and collision-free trajectory faster than optimizers that use less-flexible representations. We can think of the functional gradient iteration as automatically adapting the temporal resolution of our trajectory during optimization.

Our work is only the first step in exploring RKHSs for motion planning. In the future, we are excited about the potential of this work for both learning from experience and learning from demonstration. First, a low-dimensional trajectory parameterization enables us to more easily generate a diverse set of initial trajectories for an optimizer, aiding techniques that learn how to score initial trajectories for a new motion planning problem based on data from old problems. [@Dey12] Second, RKHSs enable us to plan with kernels learned from user demonstrations, leading to spaces in which more predictable motions have lower norm, and ultimately fostering better human-robot interaction. [@dragan14fam]

# Appendix {#sec:app}

## Finite approximation of Path Integral Cost {#sec:pathintegralapprox}

Trajectory optimization in RKHSs can be derived for different types of obstacle cost functionals, provided that trajectories have a finite representation. Previous work defines a obstacle cost in terms of the arc-length integral of the trajectory. [@Zucker13] We approximate the path integral cost functional, with a finite representation using integral approximation methods, such as quadrature methods. [@numericalrecipes]Consider a set of finite time points $t_i\in \boldsymbol{\mathcal{T}}$ to be the abscissas of an integral approximation method. We use a Gauss-Legendre quadrature method, and represent $t_i$ as roots of the Legendre polynomial $P_n(t)$ of degree $n$. Let $w_i$ be the respective weights on each cost sample: $$\begin{align}
\label{eq:funcintcost}
 \mathcal{U}_{obs}[\boldsymbol{\xi}]  = \int\limits_0^1  c\left[\boldsymbol{\xi}(t) \right] \left\|D^1\boldsymbol{\xi}(t)\right\| dt &\approx \sum_{t_i\in\mathcal{T}}  \omega_i\ c\left[\boldsymbol{\xi}(t_i) \right] \left\|D^1\boldsymbol{\xi}(t_i)\right\|
 \begin{matrix}\end{matrix}
\end{align}$$ with coefficients, and the Legendre polynomials obtained recursively from the Rodriguez Formula: $$\begin{align*}
 P_n &=  2^{n}\sum\limits_{j=0}^{n} t^{j} \dbinom{n}{j} \dbinom{\frac{n+j-1}{2}}{n} \\ \notag
  w_i &= \frac{2}{\left( 1-t_i^2 \right) [D^1P_n(t_i)]^2}
\end{align*}$$ We denote $D^1\equiv \frac{d}{dt}$ the first order time derivative. Using this notation, we are able to work with integral functionals, using still a finite set of time points to represent the full trajectory.

## Waypoint Parameterization as an Instance of RKHS {#sec:waypoints}

Consider a general Hilbert space of trajectories $\xi \in \Xi$, (not necessarily an RKHS) equipped with an inner product $\langle \xi_1,\xi_2\rangle_{\Xi} =  \xi_1^T A \xi_2$. In the waypoint representation, [@Zucker13] $A$ is typically the Hessian matrix over points in the trajectory, which makes the norm in $\xi$ penalize unsmooth and inefficient trajectories, in the sense of high acceleration trajectories. The minimization under this norm $\|\xi\|_A=\sqrt{\xi^TA\xi}$ performs a line search over the negative gradient direction, where $A$ dictates the shape of the manifold over trajectories. This paper generalizes the waypoint parameterization, we can represent waypoints by representing the trajectory in terms of delta Dirac basis functions $\langle \xi, \delta(t,\cdot)\rangle= \xi(t)$ with an additional smoothness metric $A$. Without A, each individual point is allowed to change without affecting points in the vicinity. Previous work, overcome this caveat by introducing a new metric that propagates changes of a single point in the trajectory to all the other points. Kernel evaluations in this case become $k(t_i,\cdot)=A^{-1}\delta(t_i,\cdot)$, where $\xi(t) = \sum_i a_i A^{-1}\delta(t_i,\cdot)$. The inner product of two functions is defined as $\langle \xi_1,\xi_2\rangle_{A} = \sum_{i,j}  a_ib_i A^{-1}\delta(t_i,t_i)$.\
Here $\delta(t_i,\cdot)$ represents the finite dimensional delta function which is one for point $t_i$ and zero for all the other points. A trajectory in the waypoint representation becomes a linear combination of the columns of $A^{-1}$. Columns of $A^{-1}$ dictate how the corresponding point will affect the full trajectory.\
For an arbitrary kernel representation the behavior of these points over the full trajectory are associated with the kernel functions associated with the space. For radial basis functions the trajectory is represented as gaussian functions centered at a set of chosen time points (fewer in practice) instead of the full trajectory waypoints. In this sense, we have a more compact trajectory representation using RKHSs.

## Constrained optimization {#sec:constraints}

Consider equality and inequality constraints on the trajectory $h(\boldsymbol{\xi}(t)) = 0,\ g(\boldsymbol{\xi}(t)) \leq 0$, respectively. We define fixed start and goal configurations as equallity type of constraints, and joint limits as inequalities. We write them as inner product with kernel functions in the RKHS:\
$$\begin{align}
 h(\cdot)^\top\boldsymbol{y}&\leftarrow\langle \boldsymbol{\xi},K(t_o,\cdot)\boldsymbol{y}\rangle_{\mathcal{H}} - \boldsymbol{q_o}^\top\boldsymbol{y}=0,\ \boldsymbol{q_o}\in\mathcal{C},\ \text{for}\ t_o=\{0,1\} \\
 g(\cdot)^\top\boldsymbol{y}&\leftarrow\langle \boldsymbol{\xi},K(t_p,\cdot)\boldsymbol{y}\rangle_{\mathcal{H}}-\boldsymbol{q_p}^\top\boldsymbol{y}\leq 0,\ \boldsymbol{q_p}\in\mathcal{C},\ \text{for}\ t_p=[0,1] 
 \begin{matrix}\end{matrix}
\end{align}$$ for any $\boldsymbol{y}\in \mathcal{C}$, writting each configuration as the the respective Lagrange multipliers, $\boldsymbol{\gamma}^o,\ \boldsymbol{\mu}^p \in \mathbb{R}^{D}$ to the objective function ([\[eq:mini\]](#eq:mini){reference-type="ref" reference="eq:mini"}), associated with each constraint $o$, $p$, yields: $$\begin{align}
\label{eq:constsol}
 \boldsymbol{\xi}^{n+1}(\cdot)=&\ \text{arg}\min\limits_{\boldsymbol{\xi}}\ \ \langle \boldsymbol{\xi}-\boldsymbol{\xi}^n, \nabla \mathcal{U}[\boldsymbol{\xi}^n] \rangle_{\mathcal{H}} + \frac{\lambda}{2}\|\boldsymbol{\xi}-\boldsymbol{\xi}^n\|^2_{\mathcal{H}}  + {\boldsymbol{\gamma^o}}^\top h[\boldsymbol{\xi}] + {\boldsymbol{\mu^p}}^\top g[\boldsymbol{\xi}]
 \begin{matrix}\end{matrix}
\end{align}$$

Solving the KKT system for the stationary point of ([\[eq:constsol\]](#eq:constsol){reference-type="ref" reference="eq:constsol"}) for ($\boldsymbol{\xi}, \gamma^o,\mu^p$), with $\mu^p\geq 0$, we obtain the constrained solution ([\[eq:constsolution\]](#eq:constsolution){reference-type="ref" reference="eq:constsolution"}).\
Let $\textrm{d}c_j \equiv \boldsymbol{J}^\top(t_j,u_j)\nabla c\left(x(\boldsymbol{\xi}^n(t_j),u_j)\right)$.The full update rule becomes: $$\begin{align}
\label{eq:constsolution}
 \boldsymbol{\xi}^{*}(\cdot) = &\left(1-\frac{\beta}{\lambda}\right)\boldsymbol{\xi}^n(\cdot) -\frac{1}{\lambda}\left( \sum_{t_j\in \boldsymbol{\mathcal{T}}}  K(t_j,\cdot)\textrm{d}c_j + K(t_o,\cdot)\boldsymbol{\gamma^o} + K(t_p,\cdot)\boldsymbol{\mu^p}\right)
 \begin{matrix}\end{matrix}
\end{align}$$ This constrained optimization solution, ends up augmenting the finite support set ($\mathcal{T}$) with points that are in constraint violation, weighting the kernel functions by the respective Lagrange multipliers. Each of the multipliers can be interpreted as a quantification of how much the points $t_o$ or $t_p$ violate the respective constraints.

[^1]: This is what makes the optimization process covariant (invariant to reparametrization).
