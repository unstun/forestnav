---
citation_key: Ahmed2024Optimal
arxiv_id: 2403.00988
arxiv_url: https://arxiv.org/abs/2403.00988
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:58:49Z
origin: ai+web
reviewed: false
---

::::: {.figure latex-placement="t"}
:::: center
::: minipage
This paper has been accepted for publication in *IEEE/RSJ International Conference on Intelligent Robots and Systems*.

This is the author's version of an article that has, or will be, published in this journal or conference. Changes were, or will be, made to this version by the publisher prior to publication.

  -------------- -------------------------------------------------
            DOI: 10.1109/IROS58592.2024.10801342
    IEEE Xplore: `https://ieeexplore.ieee.org/document/10801342`
  -------------- -------------------------------------------------

Please cite this paper as:

S. S. Ahmed, M. Shalaby, J. Le Ny and J. R. Forbes, "Optimal Robot Formations: Balancing Range-Based Observability and User-Defined Configurations," in *IEEE/RSJ International Conference on Intelligent Robots and Systems*, October 2024.

©2024IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
:::
::::
:::::

# Introduction

The relative position and attitude between two robots, referred to as *relative pose*, must be reliably estimated when conducting multi-robot tasks. Accurate relative pose estimation is essential for tasks such as collaborative planning and mapping, formation control, and coverage path planning. Cameras with object-detection ability or LiDAR in combination with other sensors can estimate the relative pose to within an acceptable accuracy [@Li2022Localization; @SHEN2022; @Zheng2023; @Queralta2020; @Xu2021; @Guo2020; @Nguyen2023]. However, the need for the robots to be in the cameras' field-of-view, the high cost and weight of LiDAR, as well as the substantial computational power required by both, hinder their use in many applications.

Recently, ultra-wideband (UWB) transceivers, referred to as UWB *tags*, have been an increasingly popular choice for relative pose estimation due to their low cost, low weight, and low power consumption [@Yanjun2020SingleUwb; @Hepp2016PersonTO; @Samet2018; @Sahinoglu2008]. The typical ranging accuracy for standard UWB tags is $10\,\si{cm}$ between a pair of transceivers. UWB tags are oftentimes fixed to static anchors with known locations and are then used to localize tags placed on mobile robots [@Moron2022; @Shule2020UWB; @Muller2015; @Fang2021; @Shen2010; @Guo2017].

For anchor-free localization, fusing range measurements from two tags in each robot with inertial measurement unit (IMU) data using an extended Kalman filter (EKF) provides reliable relative pose estimates [@Shalaby2021RP; @Shalaby2023MR]. This setup relaxes all motion impositions such as the robots' need to be in persistent relative motion or the need for periodic line-of-sight between the cameras and the robots. However, even with two tags per robot, there are a finite number of non-unique solutions to the relative pose estimation problem, referred to as *ambiguities*. The presence of ambiguities causes the estimator to diverge in certain formations, such as when all the robots are in a straight line, as shown in Fig. [\[fig:1b\]](#fig:1b){reference-type="ref" reference="fig:1b"} [@Shabbir2024GSF; @Charles2022OptimalMF]. Despite using estimators suitable for handling these ambiguities, such as a Gaussian sum filter [@Shabbir2024GSF], maintaining these formations for a long period of time may still lead to estimator divergence.

:::: {#fig:formation .figure latex-placement="t"}
::: caption
Comparing the coverage span of two formations. The circles represent the camera's field-of-view of each robot, and the red dots denote the location of the ranging tags. (a) The robots are clustered together to ensure high relative pose estimation accuracy, as shown in [@Charles2022OptimalMF]. (b) The robots are spread apart in a horizontal line to cover a larger area, which minimizes coverage time.
:::
::::

To address this issue, [@Charles2022OptimalMF] suggests keeping the team of robots in formations where they are close and clustered together, as shown in Fig. [\[fig:1a\]](#fig:1a){reference-type="ref" reference="fig:1a"}, which theoretically maximizes the relative pose estimation accuracy for two-tagged robots. However, these clustered formations are not ideal for applications such as infrastructure inspection or surveillance, where maximizing coverage is beneficial. An example of robot clustering resulting in reduced coverage is shown in Fig. [1](#fig:formation){reference-type="ref" reference="fig:formation"}.

This paper addresses the contrasting objectives of determining multi-robot formations that both (1) maximize coverage and (2) ensure close proximity between robots for good relative localization accuracy. Other multi-robot path planning mechanisms have focused on distributing the robots into different sectors in a large area, where each robot individually covers its sector to minimize overall coverage time [@Chen2021EfficientMC; @Tang2023; @Gao2018OptimalMC; @Lee2023CA; @Xiaoguang2018]. The robots generally localize themselves using the Global Positioning System (GPS). However, with a UWB ranging-based approach, the robots cannot be distributed into sectors since they must be in proximity to each other to achieve high relative pose estimation accuracy, as highlighted in [@Charles2022OptimalMF].

The key contribution of this paper is a cost function that brings the robots to any desirable formation, such as a "high-coverage" straight-line formation, while simultaneously maintaining high relative localization accuracy. This cost function has a component that provides the user with the ability to choose the direction and distance between any two adjacent robots. This feature enables the user to realize different formations for various applications, such as bridge inspection, as demonstrated in Section [4.4](#sec:bridge){reference-type="ref" reference="sec:bridge"}. User-defined formations can be achieved using acceleration inputs [@Dang2019FC; @Yan2021], but the proposed component within the cost function is easily customizable and integrable with the formulation of [@Charles2022OptimalMF]. Another component of this cost function allows the user to allocate a certain amount of overlap between adjacent robots' camera views, which is good for image-stitching and in improving mapping accuracy, as mentioned in [@Li2017]. Observability and collision avoidance terms are also incorporated into the cost function.

The "high-coverage" formations generated by minimizing the proposed cost function are tested in a planning task in simulation and experiment, where the robots localize themselves and unknown anchors using a simultaneous localization and mapping (SLAM) algorithm based on the EKF. Compared to the current state-of-the-art, the proposed formations significantly reduce coverage time with minimal impact on localization accuracy.

The remainder of this paper is organized as follows. The notation and preliminaries are defined in Section [2](#sec:problem_setup){reference-type="ref" reference="sec:problem_setup"}. The problem is motivated in Section [3](#sec:problem_formulation){reference-type="ref" reference="sec:problem_formulation"}. The proposed cost functions are in Section [4](#sec:optimization){reference-type="ref" reference="sec:optimization"}. The application of the cost function in simulations and experiments is in Section [5](#sec:coverage){reference-type="ref" reference="sec:coverage"}.

# Notation and Preliminaries {#sec:problem_setup}

Consider $N$ robots with IDs, $\ensuremath{\mathcal{P}} = \{1, \ldots, N\}$. Each robot is equipped with two ranging tags, resulting in a total of $2N$ tags collectively, as shown in Fig. [2](#fig:setup){reference-type="ref" reference="fig:setup"}. The physical points $\tau_1, \ldots, \tau_{2N}$ denote the location of the tags on the robots. The set of tag IDs is denoted as $\ensuremath{\mathcal{V}}~=~\{1, \ldots, 2N\}$. Each robot is assumed to be equipped with a downward or upward-facing camera that has a circular field-of-view with a known radius, $r_p$. The set of radii is denoted as $\ensuremath{\mathcal{R}} = \{r_1, \ldots, r_N\}$. The set $\ensuremath{\mathcal{E}}$ denotes the inter-tag range measurements. The bolded $\mbf{1}$ and $\mbf{0}$ are appropriately sized identity and zero matrices, respectively. Subscripts such as $\mbf{1}_{2 \times 2}$ and $\mbf{0}_{2 \times 1}$ may be used to explicitly indicate dimensions.

A 2-dimensional orthonormal reference frame $\ensuremath{\mathcal{F}}_p$ is attached to Robot $p$. A common global reference frame and a static point are denoted by $\ensuremath{\mathcal{F}}_g$ and $w$, respectively. The position of a chosen reference point in Robot $p$ relative to point $w$, resolved in $\ensuremath{\mathcal{F}}_p$ is denoted $\mbf{r}^{pw}_p \in \mathbb{R}^2$. Vectors resolved in different frames are related by the transformation $\mbf{r}_p^{pw}=\mbf{C}_{pq} \mbf{r}_q^{pw}$, $\mbf{C}_{pq} \in SO(2)$, where $$SO(2)$$ is the special Orthogonal group in 2D. For conciseness, Robot $p$ is referred to as $\text{R}_p$ in plot legends. The relative pose between Robots $p$ and $q$ is $$\begin{align}
    \mbf{T}_{pq} = \begin{bmatrix}
    \mbf{C}_{pq} & \mbf{r}^{qp}_p \\
    \mbf{0} & 1
    \end{bmatrix}\in SE(2),
\end{align}$$ where $$SE(2)$$ is the special Euclidean group in 2D. The exponential map of $$SE(2)$$ is denoted $\exp: \mathfrak{se}(2)~\rightarrow~SE(2)$, where $$\mathfrak{se}(2)$$ is the Lie algebra of $$SE(2)$$. The "wedge" operator is denoted $(\cdot)^\wedge: \mathbb{R}^3 \rightarrow \mathfrak{se}(2)$.

:::: {#fig:setup .figure latex-placement="t"}
![](Ahmed2024Optimal_figs/drones4.png){width="0.79\\columnwidth"}

::: caption
Problem setup for a two-tag multi-robot system, where Robot $p$ is equipped with tags $\tau_i$ and $\tau_j$, and a camera with a circular view of radius $r_p$ in the up or down direction. Without loss of generality, the pink robot, defined as Robot $1$, is considered to be the reference robot.
:::
::::

The poses of all the robots are expressed relative to Robot $1$, which is arbitrarily chosen to be the reference robot. As such, the state of the system is $$\begin{align}
\
    \label{eq:state_def}
  \mbf{x} = (\mbf{T}_{12}, \ldots, \mbf{T}_{1N}) \in SE(2)^{N-1}.
\end{align}$$ Denoting $\delta\ensuremath{\boldsymbol{\mathcal{\xi}}}_p \in \mathbb{R}^{3}$, and $\ensuremath{\delta{\mbf{x}}} = [\delta\ensuremath{\boldsymbol{\mathcal{\xi}}}_2^{\ensuremath{\mathsf{T}}}\cdots \delta\ensuremath{\boldsymbol{\mathcal{\xi}}}_N^{\ensuremath{\mathsf{T}}}]^{\ensuremath{\mathsf{T}}}\in \mathbb{R}^{3\times(N-1)}$, the $\oplus$ operator is defined as, $$\begin{align}
    \label{eq:oplus}
    \mbf{x} \oplus \delta \mbf{x} = (\mbf{T}_{12}\exp(\delta\ensuremath{\boldsymbol{\mathcal{\xi}}}_2^\wedge), \ldots, \mbf{T}_{1N}\exp(\delta\ensuremath{\boldsymbol{\mathcal{\xi}}}_N^\wedge)).
\end{align}$$ The position of Robot $p$ relative to Robot $q$, resolved in $\ensuremath{\mathcal{F}}_1$, is $$\begin{align}
    \mbf{r}^{pq}_1 = \mbf{D}\mbf{T}_{1p}\mbf{b} - \mbf{D}\mbf{T}_{1q}\mbf{b},
\end{align}$$ where $\mbf{D} = [\mbf{1}_{2 \times 2}\; \mbf{0}_{2\times1}]$, $\mbf{b} = [\mbf{0}_{1\times2}\;1]^{\ensuremath{\mathsf{T}}}$.

The range measurement of Tag $i$ relative to Tag $j$ in Robots $p$ and $q$, respectively, is modelled as $$\begin{align}
 \label{eq:meas_model}
    y_{ij} (\mbf{x}) &= \ensuremath{\left\Vert \mbf{D}\mbf{T}_{1p}
    \ensuremath{\tilde{\mbf{r}}}^{\tau_i p}_p
    - \mbf{D} \mbf{T}_{1q}
    \ensuremath{\tilde{\mbf{r}}}^{\tau_j q}_q
     \right\Vert} + \eta_{ij},
\end{align}$$ where $\ensuremath{\tilde{\mbf{r}}} = [\mbf{r}^{{\ensuremath{\mathsf{T}}}}\;1]^{\ensuremath{\mathsf{T}}}$, and $\eta_{ij}~\sim~\ensuremath{\mathcal{N}}(0, \sigma^2_{ij})$. Therefore, the augmented measurement vector is, $$\begin{align}
    \label{eq:meas_model2}
    \mbf{y} &= \mbf{g}(\mbf{x}) + \ensuremath{\boldsymbol{\mathcal{\eta}}} =\left[\begin{array}{ccc} \cdots & y_{ij}(\mbf{x}) & \cdots \end{array}\right]^{\ensuremath{\mathsf{T}}}+ \ensuremath{\boldsymbol{\mathcal{\eta}}} \in \mathbb{R}^{|\ensuremath{\mathcal{E}}|}, \nonumber \\
    &\hspace*{0.3cm}\forall (i,j) \in \ensuremath{\mathcal{E}}, \ensuremath{\boldsymbol{\mathcal{\eta}}} \sim \ensuremath{\mathcal{N}}(\mbf{0}, \mbf{R}), \; \mbf{R} = {\ensuremath{\mathrm{diag}}}(\ldots, \sigma_{ij}^2,\ldots).
\end{align}$$

## Optimization

This paper finds locally optimal formations by minimizing cost functions of $\mbf{x}\in SE(2)^{N-1}$, $J(\mbf{x})$. All such cost functions are minimized using a momentum-based gradient descent algorithm. This approach is preferred over a standard gradient descent method as it allows for faster convergence to a global or local minimum [@Qian1999]. The state is updated from $\mbf{x}_t$ to $\mbf{x}_{t+1}$ using a perturbation $\delta \mbf{x}_t \in \mathbb{R}^{3\times(N-1)}$ as $$\begin{align}
    \delta \mbf{x}_{t} &= - \Bigl(\alpha \nabla J(\mbf{x}_t) + \beta \delta \mbf{x}_{t-1}\Bigr)^{\ensuremath{\mathsf{T}}},\\
    \mbf{x}_{t+1} &= \mbf{x}_t \oplus \delta \mbf{x}_t,
\end{align}$$ where $\nabla J(\mbf{x}_t)$ is the gradient of the cost function numerically computed using finite difference [@Charles2020ComplexStep], $\alpha$ is the learning rate, and $\beta$ is the momentum parameter. Throughout the paper, the parameters $\alpha=0.001$ and $\beta=0.9$ are used. The optimization is terminated when $||\delta \mbf{x}_t|| < 10^{-4}$.

:::: {#fig:J_adj_formation .figure latex-placement="b"}
::: caption
Formations obtained by minimizing $J_{\text{adj}}(\mbf{x})$. The contours represent the heatmap of the cost function $J_{\text{adj}}(\mbf{x})$, by varying the position vector, $\mbf{r}^{mn}_{n}$, between all the robots.
:::
::::

# Motivation {#sec:problem_formulation}

The goal of this paper is to find multi-robot formations that minimize the coverage time of a given space, as shown in Fig. [1](#fig:formation){reference-type="ref" reference="fig:formation"}. The challenge is to balance this objective with the necessity for accurate relative pose estimation using range measurements. To find an appropriate multi-robot formation with good ranging-based relative pose estimation accuracy, [@Charles2022OptimalMF] proposes the minimization of $$\begin{align}
    \label{eq:opt_cost}
    J_\text{opt} (\mbf{x}) = J_\text{est} (\mbf{x}) + J_\text{col} (\mbf{x}),
\end{align}$$ where $J_\text{est} (\mbf{x})$ quantifies the relative pose estimation error and uncertainty using the Cramér-Rao lower bound [@Charles2022OptimalMF; @Simon2018; @Cano2023], and $J_\text{col} (\mbf{x})$ is the collision avoidance term. Note that, $$\begin{align}
    J_\text{est} (\mbf{x}) &= -\ln \det \Bigl(\mbf{H}(\mbf{x})^{\ensuremath{\mathsf{T}}}\mbf{R}^{-1} \mbf{H}(\mbf{x})\Bigr),
\end{align}$$ where $\mbf{H}(\mbf{x})$ is the Jacobian of the measurement model, derived for the inter-robot range measurements in [@Charles2022OptimalMF]. The collision avoidance term is defined as [@Xia2016] $$\begin{align}
    J^{mn}_{\text{col}}(\mbf{x}) &= \Biggl(\min\Biggl\{0, \frac{||\mbf{r}^{mn}_1||^2 - A^2}{||\mbf{r}^{mn}_1||^2 - d^2} \Biggr\}\Biggr)^2, \\
    J_{\text{col}}(\mbf{x}) &= \sum_{\substack{m, n \in \ensuremath{\mathcal{P}}, \\ m \neq n}} J^{mn}_{\text{col}}(\mbf{x}),
\end{align}$$ where $A$ is the activation radius and $d$ is the collision avoidance radius, set to $A = 0.9\,\si{m}$, and $d=0.5\,\si{m}$ throughout this paper. The multi-robot formations deduced by minimizing [\[eq:opt_cost\]](#eq:opt_cost){reference-type="eqref" reference="eq:opt_cost"} generally have the robots clustered together, where the robots have low area coverage as shown in Fig. [\[fig:1a\]](#fig:1a){reference-type="ref" reference="fig:1a"}. In fact, [@Charles2022OptimalMF] shows that a straight-line formation with high coverage, as shown in Fig. [\[fig:1b\]](#fig:1b){reference-type="ref" reference="fig:1b"}, unacceptably increases the relative pose estimation error. However, in theory, there are many "high-coverage" formations, possibly near the local minima of $J_{\text{est}}(\mbf{x})$, where the ranging-based relative pose estimation accuracy is high. These formations are achievable by minimizing a different cost function, as presented in Section [4](#sec:optimization){reference-type="ref" reference="sec:optimization"}.

# Proposed Cost Functions {#sec:optimization}

Two novel cost functions are proposed in this section, which are added to [\[eq:opt_cost\]](#eq:opt_cost){reference-type="eqref" reference="eq:opt_cost"}. The first one allows any desirable multi-robot formation acquisition suitable for the task, and the second one ensures a certain degree of overlap between adjacent robots' camera views. The final cost function also takes relative localization accuracy and collision avoidance into account. Minimizing the final cost function helps the robots adopt "high coverage" formations, such as a "near" straight-line formation while ensuring consistently high accuracy in relative localization. The problem is approached in 2D since most robots, such as ground vehicles or quadcopters, only have heading as a rotational degree of freedom for planning purposes.

## Adjacent Robot Formation Cost Function

Let $N$ robots be initially positioned at random locations. The goal of this section is to allocate the robots into any desired formation, with all formations being relative to Robot $1$, the reference robot. The idea is to minimize the error between the actual and desired position vector between any two robots, which results in the cost function $$\begin{align}
    \label{eq:adj_cost0}
    &J^{mn}_{\text{adj}}(\mbf{x}) = \Bigl|\Bigl|\mbf{r}^{mn}_{1} - \sum_{k=n}^{m-1} (r_{k+1} + r_k) \mbf{n}^{(k)}_1\Bigr|\Bigr|^2,\\
    \label{eq:adj_cost}
    &J_{\text{adj}}(\mbf{x}) = \sum_{\substack{n, m \in \ensuremath{\mathcal{P}}, \\ n < m}} J^{mn}_{\text{adj}}(\mbf{x}),
\end{align}$$ where $r_k$ and $\mbf{n}^{(k)}_1$ are user-defined parameters that determine the radial distance and direction between adjacent robots, respectively. $\mbf{n}^{(k)}_1$ is the desired unit vector associated with the position of Robot $k+1$ relative to its adjacent robot, Robot $k$, resolved in $\ensuremath{\mathcal{F}}_1$. All the desired unit vectors, starting with the one from the reference robot, Robot $1$, can be written compactly as, $$\begin{align}
    \mbf{n}_1 = \left[\begin{array}{ccc} \mbf{n}^{(1){\ensuremath{\mathsf{T}}}}_1 & \cdots & \mbf{n}^{(N-1){\ensuremath{\mathsf{T}}}}_1 \end{array}\right]^{\ensuremath{\mathsf{T}}}\in \mathbb{R}^{2\times(N-1)}.
\end{align}$$ The desired position vector of Robot $m$ relative to Robot $n$, resolved in $\ensuremath{\mathcal{F}}_1$ is found using the summation term in [\[eq:adj_cost0\]](#eq:adj_cost0){reference-type="eqref" reference="eq:adj_cost0"}.

This cost function places the robots adjacent to each other in ascending order of their IDs without determining the shortest path the robots should take to form the desired formation, as shown in Fig. [\[fig:c1\]](#fig:c1){reference-type="ref" reference="fig:c1"}. However, this is not ideal, and Algorithm [\[alg:sort\]](#alg:sort){reference-type="ref" reference="alg:sort"} sorts the robot IDs so that the robots take the shortest path possible to the user-defined formation. This algorithm finds the permutation of the robot IDs that minimizes the overall distance traveled by the robots to reach the desired formation using the Hungarian matching algorithm [@Kuhn1955], and is faster than a brute-force approach.

The sorted set of robot IDs and radii are denoted $\ensuremath{\mathcal{P}}_s~=~\{s_1,\ldots,s_N\}$ and $\ensuremath{\mathcal{R}}_s = \{r_{s_1},\ldots,r_{s_N}\}$, respectively. For conciseness, $\mbf{r}^{s_ns_m}_{s_n}$ is denoted as $\ensuremath{\bar{\mbf{r}}}^{nm}_n$, the attitude between robots $s_n$ and $s_m$ is denoted as $\ensuremath{\bar{\mbf{C}}}_{nm}$, and the radius of Robot $s_n$ is denoted as $\bar{r}_{n}$. For this sorted set of robot IDs, [\[eq:adj_cost0\]](#eq:adj_cost0){reference-type="eqref" reference="eq:adj_cost0"} becomes $$\begin{align}
    \label{eq:adj_cost1}
    &J^{mn}_{\text{adj}}(\mbf{x}) = \Bigl|\Bigl|\ensuremath{\bar{\mbf{r}}}^{mn}_1 - \sum_{k=n}^{m-1} (\bar{r}_{k+1} + \bar{r}_{k} ) \mbf{n}^{(k)}_1\Bigr|\Bigr|^2.
    % &J_{\text{adj}}(\mbf{x}) = \sum_{\substack{s_n, s_m \in \mc{P}_s, \\ n < m}} J^{mn}_{\text{adj}}(\mbf{x}),
\end{align}$$ Note that, $\mbf{n}_1$ denotes the desired unit vectors between adjacent robots starting from the reference robot, Robot $1$, and therefore is not affected by the sorting of the IDs.

:::: algorithm
Input: $\mbf{x}$, $\ensuremath{\mathcal{P}}$, $\ensuremath{\mathcal{R}}$, $\mbf{n}_1$.\
Output: $\ensuremath{\mathcal{P}}_s$, $\ensuremath{\mathcal{R}}_s$.

::: algorithmic
Let $\mbf{r}_1 \triangleq \left[\begin{array}{ccc} \mbf{r}^{21}_1 & \cdots & \mbf{r}^{N1}_1 \end{array}\right]^{\ensuremath{\mathsf{T}}}$,\
and $\mbf{p} = \left[\begin{array}{ccc} 2 & \cdots &  N\end{array}\right]^{\ensuremath{\mathsf{T}}}$, where $2, \ldots, N \in \ensuremath{\mathcal{P}} \setminus \{1\}$. $d_{\text{avg}} \leftarrow \frac{2}{N}\sum_{n=1}^N r_n$. Compute the approximate target locations in the goal formation,\
$\mbf{r}^{*}_1 \leftarrow \left[\begin{array}{ccc} \sum_{k=1}^2 d_{\text{avg}} \mbf{n}^{(k){\ensuremath{\mathsf{T}}}}_1 & \cdots  & \sum_{k=1}^N d_{\text{avg}} \mbf{n}^{(k){\ensuremath{\mathsf{T}}}}_1\end{array}\right]^{\ensuremath{\mathsf{T}}}$\
$\quad \; \triangleq \left[\begin{array}{ccc} \mbf{r}^{d_2d_1{\ensuremath{\mathsf{T}}}}_1 & \cdots & \mbf{r}^{d_Nd_1{\ensuremath{\mathsf{T}}}}_1 \end{array}\right]^{\ensuremath{\mathsf{T}}}$. Create a matrix cost function based on the distance traveled by each robot to the goal formation,\
$\mbf{C}(i,j) \leftarrow ||\mbf{r}^{*}_1(i) - \mbf{r}_1(j)||^2$ for $i,j \in \{1,\ldots,N-1\}$. Let $\mbf{P}$ be a permutation matrix, and ${\ensuremath{\mathrm{tr}}}(\cdot)$ is the trace operator. Find the permutation matrix that minimizes the overall distance traveled by the robots using the Hungarian matching algorithm [@Kuhn1955], $\mbf{P}^* \leftarrow \underset{\mbf{P}}{\min}\;{\ensuremath{\mathrm{tr}}}(\mbf{C}\mbf{P})$. $\ensuremath{\mathcal{P}}_s \leftarrow \{1\} \cup \{i^\text{th} \text{ element of }\mbf{P}^* \mbf{p}\} \triangleq \{s_1,\ldots, s_N\}$. $\ensuremath{\mathcal{R}}_s \leftarrow \{r_{s_n}\}$.
:::
::::

Fig. [\[fig:c2\]](#fig:c2){reference-type="ref" reference="fig:c2"} depicts a straight-line formation acquisition by minimizing $J_\text{adj} (\mbf{x})$ with sorted robot IDs. With sorted IDs, the robots reach a straight-line formation by traveling a shorter overall distance compared to the one with unsorted IDs, shown in Fig. [\[fig:c1\]](#fig:c1){reference-type="ref" reference="fig:c1"}. In both cases $\mbf{n}^{(k)}_1~=~[1\quad 0]^{\ensuremath{\mathsf{T}}},\, k~=~1,\ldots,N-1$.

Another instance of the implementation of this cost function is shown in Fig. [\[fig:c3\]](#fig:c3){reference-type="ref" reference="fig:c3"}, where the robots are in a V-shaped formation. The parameters used for this example are $\mbf{n}^{(k)}_1 = [1\quad 1]^{\ensuremath{\mathsf{T}}},\, k = 1,\ldots,4$, $\mbf{n}^{(k)}_1 = [1\;-1]^{\ensuremath{\mathsf{T}}}, \, k = 5,\ldots,8$, and radii $\bar{r}_k = 0.5\,\si{m}$.

In the rest of this paper, unless $\mbf{n}_1$ is stated, the sorted set of IDs is computed using $\mbf{n}^{(k)}_1=[1\quad 0]^{\ensuremath{\mathsf{T}}}, k~=~1,\ldots, N-1$, to maximize coverage span in the $x$-direction.

## Camera Overlap Cost Function

To simultaneously enable overlap of the camera views of adjacent robots, and to ensure that no more than two adjacent camera views overlap, which in turn helps in maximizing coverage, minimizing the cost function $$\begin{align}
    \label{eq:overlap_cost}
    &J^{mn}_{\text{overlap}}(\mbf{x}) = \nonumber\\
    &\Bigl|\Bigl|\ensuremath{\bar{\mbf{r}}}^{mn}_{1} - (1-\lambda)\Bigl(2\sum_{k=n}^m \bar{r}_{k} - \bar{r}_{n} - \bar{r}_{m} \Bigr) \ensuremath{\bar{\mbf{n}}}^{mn}_1\Bigr|\Bigr|^2,\\
    &J_{\text{overlap}}(\mbf{x}) = \sum_{\substack{s_n, s_m \in \ensuremath{\mathcal{P}}_s,\\ n < m}} J^{mn}_{\text{overlap}}(\mbf{x})
\end{align}$$ is proposed, where $\lambda \in [0, 1]$ represents the percentage of the radial distance between the robots that overlap. The direction vector $\ensuremath{\bar{\mbf{n}}}^{mn}_1$ is the unit vector pointing from Robot $s_n$ to Robot $s_m$ in the body frame of Robot $1$ and is given by $$\begin{align}
    \ensuremath{\bar{\mbf{n}}}^{mn}_1 = \frac{\ensuremath{\bar{\mbf{r}}}^{mn}_{1}}{||\ensuremath{\bar{\mbf{r}}}^{mn}_{1}||}.
\end{align}$$

An example formation with $\lambda = 0.25$ is shown in Fig. [4](#fig:overlap){reference-type="ref" reference="fig:overlap"}. From the contours in the left plot, note that the cost function is designed to create valleys at a distance equivalent to the summation term in [\[eq:overlap_cost\]](#eq:overlap_cost){reference-type="eqref" reference="eq:overlap_cost"} scaled by $(1-\lambda)$ around Robot $1$, and similar valleys exist around all other robots. The intersection of these valleys causes the robots to overlap their camera views with adjacent robots. The advantage of this cost function is that, regardless of where the robots are initially located, every robot will end up overlapping its camera's field-of-view with adjacent robots. Therefore, this cost function is not limited to any specific formation.

:::: {#fig:overlap .figure latex-placement="t"}
::: caption
The formation with adjacent camera overlap after minimizing $J_{\text{overlap}}$, with $\lambda = 0.25$. The left plot shows the effects of the heatmap of $J_{\text{overlap}}(\mbf{x})$ from the perspective of only Robot $1$, and the right plot shows the effects of the heatmap from the perspective of all the robots. Only position $\mbf{r}^{mn}_{n}$ is varied between all the robots to generate the heatmaps.
:::
::::

## Overall Cost Function

By encoding user-defined requirements for certain formations, such as a straight-line formation, and radii overlap mathematically, the proposed cost functions can be added to [\[eq:opt_cost\]](#eq:opt_cost){reference-type="eqref" reference="eq:opt_cost"} to achieve a comprehensive solution for formations that accommodate a variety of factors. These factors include the need for high coverage, the necessity for accurate relative pose estimation, and the requirement for camera overlap, among others. The overall cost function is given by, $$\begin{align}
    \label{eq:opt_cost2}
    J_{\text{cov}}(\mbf{x}) = J_{\text{adj}}(\mbf{x}) + J_{\text{overlap}}(\mbf{x}) + J_{\text{est}}(\mbf{x}) + J_{\text{col}}(\mbf{x}).
\end{align}$$ Fig. [5](#fig:overlap1){reference-type="ref" reference="fig:overlap1"} depicts an example formation with coverage in the $x$-direction by minimizing $J_\text{cov}(\mbf{x})$. The plots highlight the importance of $J_\text{overlap}(\mbf{x})$ in preventing the robots from non-uniformly spreading apart due to the other cost function components, notably $J_\text{adj}(\mbf{x})$. The cost $J_\text{cov}(\mbf{x})$ serves to design suitable formations for planning problems and therefore the optimization is done offline. These formation results can then be stored in the memory of the robots and used for online planning. Handling online planning initiatives like real-time non-line-of-sight issues between tags or the need for formation changes in the presence of obstacles is beyond the scope of this paper.

:::: {#fig:overlap1 .figure latex-placement="t"}
::: caption
Final formation acquisition with coverage in the $x$-direction without (top) and with (bottom) the camera overlap cost function, $J_\text{overlap}(\mbf{x})$.
:::
::::

## Bridge Inspection Example {#sec:bridge}

The usefulness of $J_{\text{cov}}(\mbf{x})$ is shown in the bridge inspection application in Fig. [\[fig:bridge_cov\]](#fig:bridge_cov){reference-type="ref" reference="fig:bridge_cov"}. Here, $5$ quadcopters with top-facing cameras inspect the underside of a bridge with no access to GPS, and two other GPS-enabled quadcopters are placed at an arbitrary angle to the inspection robots to get good localization accuracy. The desired formation is a straight-line formation of the inspection robots with some camera overlap, while ensuring that the localization accuracy is high. For $7$ robots, this is achieved by minimizing $J_{\text{cov}}(\mbf{x})$ with the parameters, $$\begin{align}
    &\mbf{n}^{(1)}_1 = \begin{bmatrix}1 \\ 1\end{bmatrix}, \mbf{n}^{(6)}_1 = \begin{bmatrix}1 \\ -1\end{bmatrix}, \mbf{n}^{(k)}_1 = \begin{bmatrix}1\\ 0\end{bmatrix}, \quad k = 2, \ldots, 5, \nonumber \\
    \label{eq:bridge}
    &J_{\text{overlap}}^{mk}(\mbf{x}) = 0, \forall k \in \ensuremath{\mathcal{P}}_s\setminus\{m\}, m \in \{1,N\},
\end{align}$$ and there are no inter-tag range measurements between the two GPS-enabled robots. Notice that, the robots under the bridge have a "near" straight line formation, such that they avoid unobservable ranging-tag configurations, and are additionally aided by the GPS-enabled quadcopters to localize themselves. These planning decisions are possible because of the flexibility in customizing $J_{\text{cov}}(\mbf{x})$. In contrast, the best formation of $5$ robots obtained by minimizing $J_{\text{opt}}(\mbf{x})$ is shown in Fig. [\[fig:bridge_opt\]](#fig:bridge_opt){reference-type="ref" reference="fig:bridge_opt"}. The two GPS-enabled robots are randomly placed without the help of $J_{\text{opt}}(\mbf{x})$. The inspection robots are not in a straight line, thus increasing inspection time.

:::: {#fig:bridge .figure latex-placement="t"}
::: caption
Comparison of formations obtained by minimizing $J_{\text{opt}}(\mbf{x})$ and $J_{\text{cov}}(\mbf{x})$ for a bridge inspection task.
:::
::::

# Application: Multi-robot Coverage {#sec:coverage}

A multi-robot coverage path planning task is where the usefulness of the proposed cost function is demonstrated. The goal is to inspect a large area in a short amount of time, while ensuring good relative localization accuracy. This is achieved by minimizing $J_{\text{cov}}(\mbf{x})$ with the parameters, $\mbf{n}^{(k)}_1~=~[1\quad 0]^{\ensuremath{\mathsf{T}}}$, $\bar{r}_k~=~0.5\, \si{m}, \,k~=~1, \ldots, N-1$, and $\lambda = 0.25$. The resultant formation is compared with a straight-line formation and a clustered formation in a coverage path planning task. These formations, along with the heatmap of $J_\text{est}(\mbf{x})$, are shown in Fig. [7](#fig:formations){reference-type="ref" reference="fig:formations"}, and denoted as, $$\begin{align}
    \mbf{x}_i \triangleq \mathop{\mathrm{arg\,min}}_{\mbf{x}} J_{i}(\mbf{x}), \quad 
    i \in \{\text{adj}, \text{opt}, \text{cov}\}.
\end{align}$$ The high-value regions in the heatmap of $\mbf{x}_\text{adj}$ already indicate that this formation has low relative pose estimation accuracy.

:::: {#fig:formations .figure latex-placement="t"}
::: caption
Comparison of the coverage path planning task using the three formations. (a) The heatmap of $J_\text{est}(\mbf{x})$ identifies that the straight-line formation has the highest and the cluster formation has the lowest estimation error, as expected. (b) Comparison of the coverage time for the three formations. The $\mbf{x}_{\text{cov}}$ formation has a $35.5\%$ time reduction, as compared to the $\mbf{x}_{\text{opt}}$ formation, while maintaining good relative pose estimation accuracy. (c) Various RMSE plots for the three formations over 100 Monte Carlo trials. The $\mbf{x}_{\text{cov}}$ formation has comparable inter-robot position and attitude RMSEs to the $\mbf{x}_{\text{opt}}$ formation.
:::
::::

## Simulation

The robots are initially placed near the origin of a $10\,\si{m}~\times~24\,\si{m}$ area. They cover the space using a square-wave pattern often used in optimal coverage path planning problems [@Chen2021EfficientMC; @Gao2018OptimalMC; @Xiaoguang2018]. For simplicity, the map of the environment is assumed to be known except for the position of two static landmarks with ranging tags fitted on them. A list of waypoints is assigned to an arbitrarily chosen leader, which is Robot $1$ here, and the other robots follow the leader in a formation using the velocity control, $$\begin{align}
    \mbf{u}^{\text{reach target}/g}_n &= \mbf{u}^{\text{formation}/g}_n + \mbf{u}^{\text{waypoint}/g}_n,
\end{align}$$ where each control term is resolved in the robot's body frame. The components $\mbf{u}^{\text{formation}/g}_n$ and $\mbf{u}^{\text{waypoint}/g}_n$ are given in [@Queiroz2019 Chap. 2]. The trajectory generated using this control law is shown in Fig. [\[fig:f2\]](#fig:f2){reference-type="ref" reference="fig:f2"}. Note that, each corner of the square-wave pattern is treated as a static waypoint. Once Robot $1$ reaches one corner in formation with the other robots, it moves to the next corner.

The EKF-SLAM algorithm, similar to [@sola2014], is used to assess the relative pose estimation accuracy. This estimation directly impacts the precision of localizing the landmarks within the context of an inspection task. EKF-SLAM is used over a batch method since it is computationally less expensive and suitable for online implementation. The interoceptive measurements are the velocity inputs in the body frame of the robots at $100\,\si{Hz}$ as shown in [@Shabbir2024GSF], and the exteroceptive measurements are either inter-tag or tag-landmark range measurements at $110\,\si{Hz}$ with a covariance matrix $\mbf{R}=0.1^2\mbf{1}\,\si{m}^2$. It is assumed that the robots receive range measurements from the static landmarks only when they are within a $2\,\si{m}$ radius of the landmark. Additionally, Robot $1$ receives GPS measurements at $50\,\si{Hz}$ with a standard deviation of $0.1\,\si{m}$ in each component to help localize itself in the global reference frame $\ensuremath{\mathcal{F}}_g$.

::: tabularx
0.95 \|c\|Y\|Y\|\
& $\mbf{x}_\text{opt}$ (Eq.[\[eq:opt_cost\]](#eq:opt_cost){reference-type="eqref" reference="eq:opt_cost"}) & $\mbf{x}_\text{cov}$ (proposed)\
Landmark$_1$ Est. Error & $35.4$ $\%$ & $58.8$ $\%$\
Landmark$_2$ Est. Error & $29.6$ $\%$ & $31.6$ $\%$\
Inter-robot Att. RMSE & $47.0$ $\%$ & $40.0$ $\%$\
Inter-robot Pos. RMSE & $66.2$ $\%$ & $59.4$ $\%$\
:::

[]{#tab:sim label="tab:sim"}

The $\mbf{x}_\text{cov}$ (proposed) formation exhibits a $35.5\%$ reduction in coverage time compared to $\mbf{x}_\text{opt}$ (clustered formation), with only $17\%$ and $11\%$ loss in relative attitude and position estimation accuracy, respectively, as shown in Fig. [\[fig:f2\]](#fig:f2){reference-type="ref" reference="fig:f2"} and Fig [\[fig:f3\]](#fig:f3){reference-type="ref" reference="fig:f3"}. Table [\[tab:sim\]](#tab:sim){reference-type="ref" reference="tab:sim"} displays the percentage reduction in median estimation errors of $\mbf{x}_\text{opt}$ and $\mbf{x}_\text{cov}$ with respect to $\mbf{x}_\text{adj}$ for $100$ Monte Carlo simulations. It highlights that there is a trade-off when using $\mbf{x}_\text{cov}$ vs $\mbf{x}_\text{opt}$; $\mbf{x}_\text{cov}$ (proposed) has slightly worse inter-robot attitude and position RMSEs, but either comparable or lower landmark estimation errors than $\mbf{x}_\text{opt}$, indicating $J_\text{cov}(\mbf{x})$'s effectiveness in attaining highly observable, and "high-coverage" formations. The median estimation errors for $\mbf{x}_\text{cov}$ (proposed) are $0.448\,\si{m}$, $0.088\,\si{m}$, $0.032\,\si{rad}$, and $0.062\,\si{m}$ for Landmark$_1$, Landmark$_2$, inter-robot attitude, and position, respectively. This affirms that the proposed cost function allows a slight decrease in relative pose estimation accuracy to gain a significant reduction in coverage time, compared to the clustered formation, $\mbf{x}_\text{opt}$.

:::: {#fig:experiment_setup1 .figure latex-placement="t"}
::: caption
Experimental setup.
:::
::::

## Experiment {#sec:exp}

The EKF-SLAM algorithm is tested with the same formations on real quadcopters to experimentally validate that the "high-coverage" formations found by minimizing $J_\text{cov}(\mbf{x})$ (proposed) have good localization accuracy. Due to space limitations, each experiment is conducted with $3$ Uvify IFO-S quadcopters moving back and forth in a $4\,\si{m} \times 6\,\si{m}$ space, at a constant height, while in formation for $47\,\si{s}$. Two landmarks with UWB tags are placed at the edge of the room. The remaining two robots, with two tags each, are simulated to be in formation with the other three during the experiment. The Tags $i$ and $j$ in the robots are placed at $$\begin{align}
    \mbf{r}^{\tau_ip}_p = \begin{bmatrix}0.17 \\ -0.17 \\ -0.05\end{bmatrix}, \quad
    \mbf{r}^{\tau_jp}_p = \begin{bmatrix}-0.17 \\ 0.17 \\ -0.05\end{bmatrix},
\end{align}$$ and $r_p = 0.7,\,p \in \ensuremath{\mathcal{P}}$, with units in meters. Since the simulations establish that the $\mbf{x}_{\text{cov}}$ (proposed) formation reduces coverage time, the primary goal is to validate that this benefit does not significantly compromise the localization accuracy in real-world experiments. The experimental details are shown in Fig. [8](#fig:experiment_setup1){reference-type="ref" reference="fig:experiment_setup1"}.

The process model involves velocity inputs at $10\,\si{Hz}$ in the body frame of the robots as shown in [@Shabbir2024GSF], the landmarks are static, and the measurement model involves inter-tag and tag-landmark range measurements at $80\,\si{Hz}$. For this experiment, DWM$1000$ UWB transceivers are used. The ranging protocol and UWB calibration procedure are as in [@Shalaby2023Calibration]. The velocity inputs with added noise are obtained by performing finite difference on ground truth position data, extracted from the Vicon motion-capture system. The added noise has a standard deviation of $0.01\,\si{rad}$ and $0.1\,\si{m}$ for the angular velocity and translational velocity components, respectively. Any interoceptive sensor data, such as IMU reading or velocity obtained using visual inertial odometry in the body frame of the robots would work as well. A covariance of $0.1^2\,\si{m}^2$ is set for the measurements received by the ranging tags in the simulated robots. Robot $1$ is also given noisy ground truth position data as GPS measurements at $30\,\si{Hz}$ with a standard deviation of $0.1\,\si{m}$ in each component.

The results are shown in Fig. [9](#fig:exp_results){reference-type="ref" reference="fig:exp_results"}. As expected, the estimator diverges for the straight-line formation due to observability issues. The landmark position and inter-robot relative pose estimation accuracy for the $\mbf{x}_{\text{cov}}$ (proposed) formation and the clustered one are similar. Furthermore, the $\mbf{x}_{\text{cov}}$ (proposed) formation maintains landmark position estimation error within the $\pm 3\sigma$ bounds, indicating low estimation error uncertainty. In Table [\[tab:exp\]](#tab:exp){reference-type="ref" reference="tab:exp"}, this formation also demonstrates a significant reduction in median estimation error compared to the straight-line formation: at least $26.9\%$ for Landmark$_1$ and Landmark$_2$, and $32.9\%$ and $62.1\%$ for inter-robot attitude and position estimates, respectively, approaching levels seen in the clustered formation, $\mbf{x}_\text{opt}$. These error metrics in values are $0.112\,\si{m}$, $0.073\,\si{m}$, $0.056\,\si{rad}$, and $0.041\,\si{m}$ for Landmark$_1$, Landmark$_2$, inter-robot attitude, and position, respectively. The experiments again validate the claim of $J_\text{cov}({\mbf{x}})$ (proposed) producing "high coverage" formations with insignificant loss in relative pose estimation accuracy.

:::: {#fig:exp_results .figure latex-placement="t"}
![](Ahmed2024Optimal_figs/16_.png){width="\\columnwidth"}

::: caption
Different error metrics for the three formations in the experiment. The proposed formation has comparable RMSEs to the clustered formation while swiping a larger area. The shaded regions in the landmark position estimation error plots represent the $\pm 3\sigma$ bounds of the estimator.
:::
::::

::: tabularx
0.95 \|c\|Y\|Y\|\
& $\mbf{x}_\text{opt}$ (Eq.[\[eq:opt_cost\]](#eq:opt_cost){reference-type="eqref" reference="eq:opt_cost"}) & $\mbf{x}_\text{cov}$ (proposed)\
Landmark$_1$ Est. Error & $74.1$ $\%$ & $71.1$ $\%$\
Landmark$_2$ Est. Error & $24.2$ $\%$ & $26.9$ $\%$\
Inter-robot Att. RMSE & $32.4$ $\%$ & $32.9$ $\%$\
Inter-robot Pos. RMSE & $64.4$ $\%$ & $62.1$ $\%$\
:::

[]{#tab:exp label="tab:exp"}

# Conclusion {#sec:conclusion}

This paper presents, in both simulation and experiment, that with the help of a few geometry-based constraints, "high coverage" formations can be achieved even if they are not optimal for inter-robot range-based relative pose estimation. The reduction in estimation accuracy for these formations is insignificant. The easy customizability of the proposed cost function to achieve "high coverage" formations with acceptable relative pose estimation accuracy is one of its strongest points. It can be used for a variety of applications such as multi-robot coverage, multi-robot search and rescue, and multi-robot inspection. Future work includes adopting this cost function for problems in 3D and extending the implementation of this cost function in online planning initiatives where the robots are tasked to cover a large area while avoiding obstacles.

[^1]: This work was supported by the NSERC Discovery and Alliance Grant programs, and the Canadian Foundation for Innovation (CFI) program.

[^2]: S. S. Ahmed, M. A. Shalaby, and J. R. Forbes are with the Department of Mechanical Engineering, McGill University, 817 Sherbrooke St. W., Montreal, QC H3A 0C3, Canada. J. Le Ny is with the Department of Electrical Engineering, Polytechnique Montreal, Montreal, QC H3T 1J4, Canada. {`syed.shabbir.ahmed@mail.mcgill.ca}`.
