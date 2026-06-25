---
citation_key: Liu2022StarConvex
arxiv_id: 2204.04393
arxiv_url: https://arxiv.org/abs/2204.04393
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:20:33Z
origin: ai+web
reviewed: false
---

# Introduction

In many applications, such as inspection and surveillance, enabling a drone to adjust its motion to keep interesting objects visible has high priority. Many tasks even put forward a strict demand on visibility. For instance, in substation inspection and factory security patrolling, specific positions must be repeatedly observed one by one in large-scale scenes. The tasks are regarded as unsuccessful or failed if any prescribed position is left unobserved. Therefore, visibility is a key constraint while designing a trajectory planner for these applications.

Despite the significance of visibility, most works [@bonatti2018autonomous; @wang2021visibility; @jeon2020integrated] in the trajectory planning literature are not able to have a guarantee on it. Typically, they treat the visibility as an utility and optimize a handcrafted visibility cost along with other terms such as smoothness. However, such a formulation may trade off visibility for a smoother motion, which results in soft visibility constraints. Another work[@zhang2018perception] deterministically generates motion primitives and selects the best one among them. Although this method ensures visibility in a resolution complete manner, it inherently suffers from the discretization error and the curse of dimension, which cannot generate an optimal trajectory with pleasing maneuverability.

![**Left**: a composite image of the real-world experiment in the view of fisheye cameras. The cylindrical objects are to be inspected, which are marked by yellow bounding boxes. **Right**: Illustration of the proposed visibility planner. The SCPs (yellow meshes) are constructed at the inspect spot (green dot). They form the SVC together with the convex polytopes (blue meshes) to ensure the visibility and safety of the trajectory (red line). ](Liu2022StarConvex_figs/image.png){#front_test width="100%"}

To bridge the above gap, this paper proposes a planner that can efficiently generates a trajectory with visibility assurance. To generalize to various applications, we define the *task representative points* (TRPs), which refer to the sites for inspection, the frontiers for the exploration, the places for surveillance, etc. Central to our approach is the visible space representation w.r.t. the TRPs and the corresponding constraint formulation. As we know, the line-of-sights from a point naturally form a star-shaped region. Based on this idea, we model the visible space as the star convex polytope (SCP), a compact and analytic representation. By utilizing the property of the constructed SCP, we formulate visibility constraint to facilate *star-convex constrained optimization*.

In summary, the proposed planner optimizes trajectory in a *safe and visible corridor* (SVC) which encodes visibility and safety requirements. The SCPs, accounting for the visibility constraints, make parts of it. The SVC is constructed by connecting all the SCPs by convex polytopes. The whole process runs in three steps. Firstly, the global optimal tour (i.e., the visiting sequence of the SCPs) is found and refined on SCPs. Secondly, the kinodynamic A\* path searching is conducted to find a collision-free path. Finally, the corridor is constructed incrementally by connecting all the SCPs with sequences of overlapping convex polytopes utilizing the searched trajectory. With the constructed SVC, we follow the work of [@wang2021geometrically] to optimize the trajectory spatially and temporally. The visibility constraint is further relaxed to convert the optimization problem into an unconstrained one that can be solved reliably and efficiently. To validate the planner, we apply it in the task of aerial inspection. Benchmark results show that our method is light-weighted, efficient, and scalable. To conclude, the contributions of this paper are as follows:

1.  Introduce a new visible space representation the star-convex polytope (SCP) and propose to formulate the visibility constraint for *star-convex constrained optimization*.

2.  Propose a visibility guaranteed planning framework, while retains the safety, feasibility, and energy efficiency of trajectory.

3.  Validate the proposed method by implementing simulation and real-world experiments in aerial inspection.

# Related Work

## Trajectory Planning with Visibility

 Many works [@jeon2019online; @jeon2020integrated] in trajectory planning design the visibility metric utilizing the minimum value of the Euclidean Signed Distance Field (ESDF) on the line between the TRPs and the robot. Since the metric is not differentiable, they use a sampling-based method to handle the metric in trajectory generation, which is time-consuming. Wang et al. [@wang2021visibility] propose a differentiable metric and yet it lacks a strong guarantee on visibility because the trajectory optimization trades off many costs. Instead of explicitly optimize visibility, Zhou et al. [@zhou2021raptor] present a perception-aware strategy. Nevertheless, the task-specific method can hardly be extended to other scenarios. Zhou et al. [@zhou2021fuel] propose an efficient exploration framework that naturally adapts to inspection tasks, whereas they only consider visibility in the sampling-based front-end. In this paper, we efficiently extract the visible space by SCP to facilitate trajectory planning.

## Trajectory Planning For Quadrotor

Trajectory planning for quadrotors can be categorized into the soft-constrained and hard-constrained approaches. The former formulates the trajectory generation as NLP to trade off several objectives, but they usually suffer from the issue of local minima[@oleynikova2016continuous]. By exploiting the properties of B-splines, Zhou et al.[@zhou2019robust] propose a method but the construction of ESDF is time-consuming, especially for the large-scale trajectory planning. While an ESDF-free planner is proposed [@zhou2020ego], but the trajectory generated highly rely on and limit to the collision- free guiding path. The hard-constrained method is pioneered by [@mellinger2011minimum] which form the problem as quadratic programming (QP) with trajectory represented as piecewise polynomials. The safety can be ensured by extracting convex safe regions[@liu2017planning]. To obtain more reasonable time allocation, alternating minimization [@wang2020alternating] and mixed integer-based[@tordesillas2019faster] based approach are proposed. Recently, Wang et al. [@wang2021geometrically] proposed a spatial and temporal optimization-based framework, which efficiently handles a wide variant of constraints. We follow the work [@wang2021geometrically] for trajectory optimization in this paper.

# Problem Statement

Consider a list of TRPs in 3D space $\mathbb{C} = \{ c_i \in \mathbb{R}^3 |1 \le i \le N \}$. The robot starting from the position $p_s \in \mathbb{R}^3$ is expected to inspect all of the points in $\mathbb{C}$ one by one and finally rest at the desired postion $p_f \in \mathbb{R}^3$. Commonly, the duration of inspection for each point is required to be last for at least a specific time $\mathbb{T} = \{\tau_i \in \mathbb{R} | 1 \le i \le N\}$. For an abitrary point in $\mathbb{R}^3$, $c_i$ is supposed to be visible to it if the line segment from the point to $c_i$ is collision free. Denote $\mathbb{S}_i \subseteq \mathbb{R}^3$ form the space where the point $v_i$ is visible. Since the occulusion effect against obstacles i.e. the visibility is the focus of this paper, we make the following assumptions:

1.  The sensor mounted on the robot has omnidirectional coverage, which is one kind of set up of UAVs and has certain research works [@gao2020autonomous].

2.  The visibility condition is satisfied only when the whole body of the robot is in the ball-shaped sensible regions around the points $\mathbb{C}$.

# Visible Space Representation

Normally, constructing a star-shape visible region on the point cloud map is non-trivial. Collision checking of the rays starting from the sites $c_i$ to the space needs either frequent kd-tree queries or discretization of the space. Apparently, these kinds of straightforward solutions are arduous and time-consuming. Inspired by [@zhong2020generating; @katz2007direct; @katz2015visibility], we introduce a new method to construct visibility space represented by star convex polytope, with the emphasis on compactness and efficiency.

## Star Convex Polytope Construction

In this paper, the obstacles are represented by point cloud map $\mathcal{M}_g$ which is organized in k-d tree structure. Our method to construct star convex polytope on $\mathcal{M}_g$ is composed of four steps: 1) point retrieval and augment, 2) point transformation, 3) convex hull construction, 4) inversion. The main idea of the method is to find the visible points by point transformation.

In order to construct the star-shaped region within a sphere boundary with radius $R$, we retrieve the local point cloud $\mathcal{M}_v$ surround the point $c_i$ by the range query on $\mathcal{M}_g$. In addition, augmented points, which are evenly sampled on the sphere boundary, are added to better facilitate the construction.

:::: {#scp .figure latex-placement="htp"}
![](Liu2022StarConvex_figs/scp_concat.png)

::: caption
**Top**: Illustration of SCP construction in 2D. The blue dotted curve is the inversion of the convex hull. **Bottom**: SCP visualization in 3D as colorful mesh. It is generated on point cloud with $R=6m$.
:::
::::

With the point set $\mathcal{M}_v$ and center $c_i$, we perform point transformation that flip all the points to outside of the sphere boundary. As shown in the [Figure [2](#scp){reference-type="ref" reference="scp"}](#scp), the point $x$ is transfer to $\hat{x}$ along the ray $\overrightarrow{c_i x}$. The corresponding function is suppose to be monotonically decreasing. Here, we simply use the ball flipping function with ball radius $r$: $$\begin{equation}
\label{ball-flipping}
\hat{x} = F(x) = x - c_i + 2(r - \| x - c_i \| ) \frac{x - c_i}{\|x - c_i\|}.
\end{equation}$$

Then, we calculate the convex hull of the flipped points by the efficient convex hull algorithm [@barber1996quickhull]. Inherently, points that lie on the convex hull are the images of the visible points. Similarly, the convex hull is the image of the underlying star-shaped boundary of visible space. Thus we can obtain the SCP by applying the inversion of ([\[ball-flipping\]](#ball-flipping){reference-type="ref" reference="ball-flipping"}) on the convex hull and denote it as $\mathcal{S}_i$. Morever, the point that can be mapped outside the convex hull is bound to be visible by $c_i$. The Point-In-SCP check can be performed by checking whether the flipping of the point is outside of the convex hull.

## Star-Convex Constrained Optimization

The visibility planning entails the study of the following optimization problem: $$\begin{equation}
\begin{aligned}
\min_{x} \quad & \mathcal{J}(x), \quad
\mathrm{s.t.} &  x \in \mathcal{S}_i,
\end{aligned}
\label{star_opt}
\end{equation}$$ where $\mathcal{J}(x)$ is the user-defined cost function. Suppose the SCP is closed by $K$ faces in $\mathbb{R}^3$. Instead of considering it directly, the flipped convex polytope $\mathcal{P}_i$ is utilized. By the $\mathcal{H}-$representation of convex polytope, it can be defined as $$\begin{equation}
\mathcal{P}_i = \{ x \in \mathbb{R}^3 |  \mathbf{A}x \preceq \mathbf{b} \},
\end{equation}$$ where the matrix $\mathbf{A} = [n_1^T, \cdots, n_K^T]^T \in \mathbb{R}^{K\times3}$ is build by the outer normal vectors of each face $n_i, i = 1, \cdots, K$ and $\mathbf{b} = [n_1^Ta_1, \cdots, n_K^Ta_K] \in \mathbb{R}^K$ is formed by arbitrary points $a_i$ on each faces. By the property of SCP, the visibility constraint is equivalent to the insurance that the flipped point $\hat{x}$ is outside of $\mathcal{P}_i$, which is expressed as $$\begin{equation}
\Xi \big(\hat{x}) > d_{\min},
\label{star_con_p}
\end{equation}$$ where $d_{\min}$ is the user-defined safe margin and $\Xi(\cdot)$ is the signed distance function on $\mathcal{P}_i$. The signed distance equals to zero on the surface of the convex hull. The inside and the outside of it correspond to the negative and positive Euclidean distances respectively. To be more specific, the signed distance is defined as $$\begin{equation}
\Xi(\hat{x}) = \max_i \Big\{ d_i =  n_i^T(\hat{x} - a_i) \Big| i = 1, 2, \cdots K \Big\}.
\label{max}
\end{equation}$$ However, the maximum function introduces the non-smooth gradient and keep it away from the efficient solution of the optimization with sophisticated solvers. To resolve this issue, we turn to enforce the point visibility constraint via smooth approximation of the maximum function. Inspired by [@lutz2021efficient], we employ the log-sum-exp function to make the approximation. Thus, ([\[max\]](#max){reference-type="ref" reference="max"}) can be written as $$\begin{equation}
\Xi(\hat{x})=
LSE\big(d_1, \cdots, d_K\big) = \frac{1}{\alpha}log \big(e^{\alpha d_1}+ \cdots + e^{\alpha d_K} \big),
\end{equation}$$ where the $\alpha \in \mathbb{R}^{+}$ is an adjustable variable that can control the quality of the approximation, with $LSE \big(d_1, d_2, \cdots, d_K \big) \rightarrow \max\big(d_1, d_2, \cdots, d_K\big)$ for $\alpha \rightarrow +\infty$. Furthermore, we relax the original optimization problem ([\[star_opt\]](#star_opt){reference-type="ref" reference="star_opt"}) by constraint violation to convert it into an unconstrained problem: $$\begin{equation}
\begin{aligned}
\min_{x} \quad  \mathcal{J}(x) +  \mathcal{V}(\widehat{LSE}), \\ 
\end{aligned}
\label{star_opt_uncon}
\end{equation}$$ where $$\begin{equation}
\mathcal{V}(\widehat{LSE}) = \lambda \max \big\{\widehat{LSE}, 0 \big\}^3.
\label{scp_v}
\end{equation}$$ The $\lambda \in \mathbb{R}^+$ is the an extremely large penalty weight and the $\widehat{LSE}$ stand for $$\begin{equation}
\begin{aligned}
\widehat{LSE} \big(\hat{x} | \mathcal{S}_i \big) =  d_{\min} - \frac{1}{\alpha} log \big( \sum_{i = 1}^{K} e^{\alpha d_i } \big).
\end{aligned}
\label{lsehat}
\end{equation}$$ Apparently, the violation term ([\[scp_v\]](#scp_v){reference-type="ref" reference="scp_v"}) preserves the $C^2$ condition, making the second order gradient attainable. Given the visible space $\mathcal{S}_i$, we can derive the gradient of $\mathcal{V}$ w.r.t. $x$ from ([\[ball-flipping\]](#ball-flipping){reference-type="ref" reference="ball-flipping"}), ([\[scp_v\]](#scp_v){reference-type="ref" reference="scp_v"}) and ([\[lsehat\]](#lsehat){reference-type="ref" reference="lsehat"}) and denote it by $g_{scp}$. The gradient is zero when $\widehat{LSE} \le 0$, and for $\widehat{LSE} > 0$, the gradient is given as $$\begin{equation}
g_{scp}=
\frac{\partial \mathcal{V}}{\partial x} = 
6 \lambda {\widehat{LSE}}^2  \frac{ \displaystyle \sum_{i = 1}^{K} e^{\alpha d_i } n_i}
{\displaystyle \sum_{i = 1}^{K} e^{\alpha d_i }}
\frac{r}{\displaystyle \| x \|^3}
\big( \| x \|^2 - xx^T- \frac{\| x \|^3}{2r} \big).
\end{equation}$$ We will employ the formation ([\[star_opt_uncon\]](#star_opt_uncon){reference-type="ref" reference="star_opt_uncon"}) for visibility planning in the following sections.

**Remark.** The formulation ([\[star_opt_uncon\]](#star_opt_uncon){reference-type="ref" reference="star_opt_uncon"}) is an appropriate adaptation of ([\[star_opt\]](#star_opt){reference-type="ref" reference="star_opt"}) for optimization efficiency and the hard constraint in ([\[star_opt\]](#star_opt){reference-type="ref" reference="star_opt"}) guarantees the visibility. Although ([\[star_opt_uncon\]](#star_opt_uncon){reference-type="ref" reference="star_opt_uncon"}) shares a similar cost structure with other visibility planners [@bonatti2018autonomous; @wang2021visibility; @jeon2020integrated], they are essentially different. The trajectory optimization formulation in [Sec. [5.3](#traj_opt_sec){reference-type="ref" reference="traj_opt_sec"}](#traj_opt_sec) allows we take extremely large value for the visibility penalty weight while [@bonatti2018autonomous; @wang2021visibility; @jeon2020integrated] can not. Otherwise, they will result in non-smooth and less efficient trajectories.

# Visibility Guaranteed Planner

As shown in the [Figure [3](#principle2){reference-type="ref" reference="principle2"}](#principle2), a complete pipeline of visibility guaranteed planner is presented in this section. Due to the differential flatness property of multicopters, we can optimize the trajectory in the space of the selected flat output (i.e. the translation of the center of mass and the Euler-yaw angle). To facilitate the trajectory optimization, the map $\mathcal{M}_g$ is modified by one-to-eight cubic inflation with regards to each point in it. Thus, the map encode the configuration space, and the SCP generated on it can be directly employed as the visibility constraint for trajectory optimization.

## Route Generation and Refinement

In order not to introduce binary variables to the whole problem, a reasonable visiting sequence of the spots can be obtained in advance by solving the traveling salesman problem (TSP). Similar to [@zhou2021fuel], we model it as a standard Asymmetric TSP (ATSP) that can be solved efficiently by Lin--Kernighan heuristic (LKH) [@helsgaun2000effective]. we further optimize route waypoints $\{w_i  \in \mathbb{R}^3 | i = 1, \cdots, N \}$ on the SCPs to direct the robot for more efficient trajectory. The problem is formulated as finding the minimum of the sum of length on SCPs: $$\begin{equation}
\begin{aligned}
\min_{w_1, \cdots, w_N} \quad & \|p_s - w_1 \| + \| w_N - p_f \| + \sum_{i = 2}^{N} \|w_i - w_{i - 1} \|,    \\ 
\mathrm{s.t.} \quad &  w_i \in \mathcal{S}_i, \, \forall i = 1, \cdots, N.
\end{aligned}
\label{min_len}
\end{equation}$$ For simplification, $w_0, w_{N+1}$ are alternatively used for $p_s$ and $p_f$ hereafter. According to ([\[star_opt_uncon\]](#star_opt_uncon){reference-type="ref" reference="star_opt_uncon"}), we further make a relaxation of ([\[min_len\]](#min_len){reference-type="ref" reference="min_len"}) to convert it to an unconstrained NLP (nonlinear programming) with cost function $$\begin{equation}
\begin{gathered}
J_w =  \sum_{i = 1}^{N} \sqrt{ \| w_i - w_{i - 1} \|^2 + \epsilon } 
 + \Lambda^T \sum_{i = 1}^{N} \mathcal{V}(\widehat{LSE}\big(w_i | \mathcal{S}_i \big) ), 
\end{gathered}
\end{equation}$$ where the $\Lambda = [\lambda_1, \cdots, \lambda_N]^T \in \mathbb{R}^N$ is the penalty weight vector and $\epsilon$ is a small value number for $C^2$ condition. By utilizing the previously-derived gradient $g_{scp}$, the gradient propagation of $J_w$ can be obtained for $w_1, \cdots, w_N$: $$\begin{equation}
\frac{\partial J_w}{w_i} = \frac{\| w_i - w_{i - 1} \|}
{\displaystyle \sqrt{\| w_i - w_{i - 1} \|^2 + \epsilon } } - 
\frac{\| w_{i + 1} - w_{i} \|}
{\displaystyle \sqrt{\| w_{i + 1} - w_{i} \|^2 + \epsilon } } + 
\lambda_i g_{scp}.
\end{equation}$$ Then, the route $w_0 \rightarrow w_1 \rightarrow w_2 \rightarrow \cdots, \rightarrow w_N \rightarrow w_{N+1}$ can be obtained by combining the problem of TSP with the optimization problem ([\[min_len\]](#min_len){reference-type="ref" reference="min_len"}), which makes preparation for the corridor construction afterwards.

![The whole pipeline is conducted in three steps: 1) route generation and refinement 2) path finding 3) SVC construction 4) trajectory optimization.](Liu2022StarConvex_figs/principle2_2.png){#principle2 width="80%"}

## Safe and Visible Corridor Construction

The route generated is not collision free but provide promising flight directions. The route waypoints serve as local goals for kinodynamic A\* to search for a collision free path. We convert the point cloud map to voxel map and perform the search on it, which can save orders of time.

Based on the searched path, the SVC can be constructed incrementally by connecting the SCPs by sequences of overlapping convex polytopes. For the convex polytope generation, we adopt the efficient method presented in [@zhong2020generating] which directly makes modifications to SCP. Consequently, the elements of the corridor can be organized in a unified struct. The intersection between the path and convex polytope is calculated by recursively subdividing the Bézier form of the trajectory and checking the control points of it. For the SCP, the intersection between the path and it can be found via the Point-In-SCP test. The convex polytope is built at the intersection until it reaches the next waypoint. Note that we add some augment points to separate the $j^{th}$ and the $(j+2)^{th}$ convex polytopes.

::::: {#large_scale .figure latex-placement="h"}
::: center
![](Liu2022StarConvex_figs/large_scale_with_points_2.png)
:::

::: caption
Simulation in large scene with scale $40 \times 150 \, m$. The scene is composed of 150 pillar-shaped obstacles and 60 ring-shaped ones. There are randomly generated 40 spots for inspection and the corresponding SCPs are shown in different colors. The trajectory is generated in 4.4s and is guaranteed to inspect all the sites.
:::
:::::

## Trajectory Optimization {#traj_opt_sec}

Given the constructed SVC, the trajectory generation problem can be formulate as the following time-spatial optimization problem:

$$\begin{align}
 \min_{\sigma(t)} \; & \int_{0}^{T_{\Sigma}} \| \sigma^{(3)}(t) \|^{2} dt + \rho T_{\Sigma}, \label{trajopt}     \\ 
 \mathrm{s.t.} \quad & [\sigma(0), \sigma^{(1)}(0), \sigma^{(2)}(0) ] = [p_s, v_s, a_s], \tag{\ref{trajopt}{a}} \label{trajopt_a}   \\ 
 & [\sigma(T_{\Sigma}), \sigma^{(1)}(T_{\Sigma}), \sigma^{(2)}(T_{\Sigma}) ] = [p_f, v_f, a_f], \nonumber \\
 & \sigma(t) \in \mathcal{F}, \quad  \forall t \in [0, T_{\Sigma}],  \tag{\ref{trajopt}{b}} \label{trajopt_b} \\
 & \| \sigma^{(1)}(t) \| \le v_m, \| \sigma^{(2)}(t) \| \le a_m, \forall t \in [0, T_{\Sigma}],  \tag{\ref{trajopt}{c}} \label{trajopt_c}  \\
 %& \forall i = 1, 2, \ldots, N, \exists t_a, \, t_b, \,  0 < t_a < t_b < T, \,  \\ 
 %& \quad  t_b - t_a > \tau_i, \, such \: that \: \sigma(t) \in S_i, \forall t\in[t_a, t_b]  \\
 &\boldsymbol{\sigma^{i}(t) \in S_i, \, T_i > \tau_i} , \nonumber  \\
 &\boldsymbol{\forall i = 1, 2, \cdots, N } , \tag{\ref{trajopt}{d}} \label{trajopt_d}
\end{align}$$ where $\sigma(t): \mathbb{R} \mapsto \mathbb{R}^3$ is a polynomial spline over $[0, T_{\Sigma}]$ with time allocation $[T_1, T_2, \cdots, T_N]$ on SCPs, $T_{\Sigma}$ the total time of $\sigma(t)$, $\rho$ the time regularization weight. The trajectory is constrained to be collision free, dynamic feasible, and visibility capable, which corresponds to the conditions in ([\[trajopt_b\]](#trajopt_b){reference-type="ref" reference="trajopt_b"}), ([\[trajopt_c\]](#trajopt_c){reference-type="ref" reference="trajopt_c"}) and ([\[trajopt_d\]](#trajopt_d){reference-type="ref" reference="trajopt_d"}) respectively. Then, we denote by $\mathcal{F}$ the resultant safe and visible corridor, $v_m$ and $a_m$ the dynamic limits, $\sigma^{i}(t)$ the segment of $\sigma(t)$ that is assigned to the $i^{th}$ SCP.

To solve the optimization problem ([\[trajopt\]](#trajopt){reference-type="ref" reference="trajopt"}), we generally adopt the directly constructed minimum control trajectory *MINCO* from [@wang2021geometrically]. Similar to [@wang2021geometrically], smooth maps are utilized to exactly eliminate spatial and time constraints. The dynamic constraint ([\[trajopt_c\]](#trajopt_c){reference-type="ref" reference="trajopt_c"}) is transformed into a finite-dimensional one via integral of constraint violation. For brevity, we refer reader to [@wang2021geometrically] for more details.

For the star-convex constraint in ([\[trajopt_d\]](#trajopt_d){reference-type="ref" reference="trajopt_d"}), we make a relaxation via integral of constraint violations. According to ([\[star_opt_uncon\]](#star_opt_uncon){reference-type="ref" reference="star_opt_uncon"}), we eliminate the constraint by defining the time integral penalty for visibility: $$\begin{equation}
I(\mathcal{S}_i, \eta_i) = \frac{T_i}{\eta_i} \sum_{j = 0}^{\eta_i } \mathcal{V} \Big( \widehat{LSE} \big(\sigma(j \frac{T_i}{\eta_i} ) | \mathcal{S}_i \big)
\Big),
\label{vis_intgral_pen}
\end{equation}$$ where $T_i$ is the time for the $i^{th}$ segment of the trajectory, and $\eta_i$ controls the relative resolution of the quadrature. For the minimum time constraint in ([\[trajopt_d\]](#trajopt_d){reference-type="ref" reference="trajopt_d"}), we take the decision variable mapping $$\begin{equation}
T_i = e^{\xi_i} + \tau_i,
\label{t_diffeo}
\end{equation}$$ to eliminate the constraint as well, where $\xi = (\xi_1, \cdots, \xi_N)$ is $C^{\infty}$ diffeomorphic to $T = (T_1, \cdots, T_N)$ . By incorporating ([\[vis_intgral_pen\]](#vis_intgral_pen){reference-type="ref" reference="vis_intgral_pen"}) and ([\[t_diffeo\]](#t_diffeo){reference-type="ref" reference="t_diffeo"}) into the optimization framework [@wang2021geometrically], the optimization problem ([\[trajopt\]](#trajopt){reference-type="ref" reference="trajopt"}) can be transformed into the unconstrained control effort minimization problem which can be solved efficiently and reliably.

# Application On Aerial Inspection 

Our planner can be employed for exploration, tracking, and many other applications with task-specific modification. To best evaluate our planner and motivated by the need to regularly inspect factories or substations, we test our planner under site inspection background, where our planner can be employed without extra effort. The task requires that a drone can observe every spot for enough time while saving the task time and energy as much as possible.

## Simulation and Benchmark Comparisons

We test the proposed method in a randomly generated environment consisting of pillar-shaped and ring-shaped obstacles. To demonstrate the scalability of the method, three scenarios are designed with increasing problem scale:

- *Small*: $20 \times 20\, m$, $15$ pillars and $6$ rings, $3$ spots.

- *Medium*: $40 \times 40 \, m$, $60$ pillars and $20$ rings, $10$ spots.

- *Large*: $80 \times 80 \, m$, $150$ pillars and $60$ rings, $20$ spots.

We set the dynamic limits of drone as $v_{max} = 4.0 \, m/s$ and $a_{max} = 6.0 \, m/s$. All the simulations are conducted with a 2.6 GHz Intel i7-9750H processor.

In the implementation, we set $R = 6.0 \, m$ to confine the SCP in a ball, $r = 20 \, m$ for ball flipping. In the trajectory generation, we use, $\rho = 150$, $\eta_i = 10$. For the LSE function, we set $\alpha = 100.0$, which can make an approximation with the precision of 0.01. We benchmark the method with [@zhou2021fuel] whose planning framework is similar to ours (i.e. TSP + trajectory optimization). Although [@zhou2021fuel] is a local planner, our evaluation spectrum covers both the local and global scales. The computation time ([Figure [6](#cp_time){reference-type="ref" reference="cp_time"}](#cp_time)) of our method shows it is also adequate for replanning. For Zhou's method, we make a few modifications to fit into our application. Firstly, the frontier information structure is left out because TRPs are already given in site inspection. The TRPs are equivalent to the average positions of frontier clusters in Zhou's method. Secondly, the viewpoints are generated without considering the yaw angle and occlusion effect is degraded to points connectivity to comply with the omnidirectional sensor assumption. Thirdly, the route is generated and refined by constructing a graph on visible points by Euclidean distance instead of the path length searched by A\*, for the reason of saving computation time.

::: tabular
ccccc Scene Scale & Method & Traj dur (s) & Int ($J^2$) & Vis cap & Zhou et. al & **6.9** & 546.5 & 80% & Proposed & 7.7 & **159.3** & **100%** & Zhou et. al & **31.4** & 819.5 & 54% & Proposed & 32.8 & **371.2** & **100%** & Zhou et. al & **63.5** & 1063.9 & 37% & Proposed & 65.3 & **487.8** & **100%**
:::

[]{#bench_res label="bench_res"}

![Comparison of the generated trajectory. The red ball is the sensible region for each spot. The trajectory planned by Zhou's method failed to inspect the left bottom spot. ](Liu2022StarConvex_figs/comp_vis_slim.png){#comp_traj}

The [Table [\[bench_res\]](#bench_res){reference-type="ref" reference="bench_res"}](#bench_res) shows the statistics on the trajectory quality. The visible capability refers to the ratio of observed spots. Owing to the SCP and the corresponding constraint formulation, our method can guarantee the visibility of all the spots, while Zhou's method loses many hits for them. In addition, our method is more smooth and energy-efficient, indicated by the criterion of Int($J^2$) (time integral of squared jerk). This primarily benefits from the powerful trajectory optimization framework [@wang2021geometrically]. The optimized trajectory duration is higher than Zhou's but still comparable to it. Without the hard visibility constraint, Zhou's method tends to reduce the length of trajectory, which will reduce the execution time, as shown in [Figure [5](#comp_traj){reference-type="ref" reference="comp_traj"}](#comp_traj).

:::: {#cp_time .figure latex-placement="h"}
![](Liu2022StarConvex_figs/cppp.png)

::: caption
Benchmark comparison of the computational time for different scales (The ESDF construction time is not counted in Zhou's). Both the trajectory optimization and the pipeline time are evaluated. The shaded area is the $4/5 \sigma$ interval, where $\sigma$ is the standard deviation.
:::
::::

The comparison of the computational time is shown in [Figure [6](#cp_time){reference-type="ref" reference="cp_time"}](#cp_time). Our method is faster than Zhou's by orders of magnitudes and is more reliable. Lacking a compact environment abstraction (e.g. SVC), the trajectory optimization time of Zhou's takes almost $99\%$ of the whole pipeline. The proposed method spends about $42\%$ of total time for the generation of SCPs, route, and SVC, but they highly speed up trajectory optimization. As the problem scale increase, our method can still finish in seconds. A more large scale test of the proposed method is shown in [Figure [4](#large_scale){reference-type="ref" reference="large_scale"}](#large_scale).

## Real-World Experiment

:::: {#exp .figure latex-placement="h"}
![](Liu2022StarConvex_figs/exp.png){width="90%"}

::: caption
Real world scene to test the proposed method. Refer to [Figure [1](#front_test){reference-type="ref" reference="front_test"}](#front_test) for the labels. The color map indicates the velocity of the quadrotor.
:::
::::

We conduct real-world indoor experiment to validate the proposed method, as shown in [Figure [7](#exp){reference-type="ref" reference="exp"}](#exp). The upright cylindrical obstacles are the targets to be inspected. The map is pre-built using lidar by LIO-SAM [@legoloam2018shan] and the trajectory is planned offline. The quadrotor we used is equipped with an Intel Realsense D435 for state estimation and Insta 360 One X2[^6] for omnidirectional perception. The maximum velocity and acceleration are set as $1.5\, m/s$ and $1.0 \, m/s^2$. The minimum inspection time for each object is set as $1.0 s$.

The test environment and the associate results are displayed in [Figure [7](#exp){reference-type="ref" reference="exp"}](#exp). The quadrotor is able to inspect all the targets. Since the quadrotor is not necessary to be closest to the targets as long as they are visible, it slows down and inspect the target through the gap. The test shows that the SCP can excavates almost all visible regions and the formulated *star-convex constrained optimization* renders reasonable trajectory for visibility planning.

# Conclusion

In this paper, we introduce a compact and efficient space representation the SCP and propose to formulate the visibility constraint for *star-convex constrained optimization*. By utilizing the SCP, we design a visibility guaranteed planning framework, while retains the safety, feasibility, and energy efficiency of trajectory. The experimental results show that the method is efficient, scalable, and visibility guaranteed.

The main limitation of our method the is the omnidirectional perception assumption of the sensor model. In the future, we will take limited FOV of sensors into consideration and plan the yaw angle in trajectory optimization.

[^1]: 1 State Key Laboratory of Industrial Control Technology, Institute of Cyber-Systems and Control, Zhejiang University, Hangzhou, 310027, China.

[^2]: 2 Huzhou Institute of Zhejiang University, Huzhou, 313000, China.

[^3]: 3 Department of Mechanical Engineering, The University of Hong Kong.

[^4]: This work was supported by the National Natural Science Foundation of China under Grants 62003299.

[^5]: Corresponding author: Fei Gao, `fgaoaa@zju.edu.cn`

[^6]: https://www.insta360.com/
