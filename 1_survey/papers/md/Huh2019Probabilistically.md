---
citation_key: Huh2019Probabilistically
arxiv_id: 1901.00101
arxiv_url: "https://arxiv.org/abs/1901.00101"
title: "Probabilistically Safe Corridors to Guide Sampling-Based Motion Planning"
authors_short: "Jinwook Huh et al."
year: 2019
direction_tag: I_corridor_planning;O_dense_forest_narrow_passage
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:49:04Z
origin: ai+web
reviewed: false
---

# Probabilistically Safe Corridors to Guide Sampling-Based Motion Planning

Jinwook Huh<sup>1∗</sup>, Om<sup>¨</sup> ur Arslan¨ <sup>2∗</sup>, and Daniel D. Lee<sup>3</sup>

Abstract— In this paper, we introduce a new probabilistically safe local steering primitive for sampling-based motion planning in complex high-dimensional configuration spaces. Our local steering procedure is based on a new notion of a convex probabilistically safe corridor that is constructed around a configuration using tangent hyperplanes of confidence ellipsoids of Gaussian mixture models learned from prior collision history. Accordingly, we propose to expand a random motion planning graph towards a sample goal using its projection onto probabilistically safe corridors, which efficiently exploits the local geometry of configuration spaces for selecting proper steering direction and adapting steering stepsize. We observe that the proposed local steering procedure generates effective steering motion around difficult regions of configuration spaces, such as narrow passages, while minimizing collision likelihood. We evaluate the proposed steering method with randomized motion planners in a number of planning scenarios, both in simulation and on a physical 7DoF robot arm, demonstrating the effectiveness of our safety guided local planner over the standard straight-line planner.

## I. INTRODUCTION

Due to its simplicity and flexibility in handling a diverse set of configuration spaces without requiring an explicit representation, sampling-based motion planning is the mainstream approach to global motion planning for highdimensional, highly nonlinear robotic systems, such as robot manipulators [1]–[4]. However, the performance of such randomized motion planners strongly depends on the choice of distance measure, sampling method, and local steering; and is known to degrade significantly around complicated regions of configuration spaces, such as narrow passages [5], [6].

This performance degrade is usually considered as an issue of sampling, because uniform sampling has a Voronoi bias towards yet unexplored larger regions of configuration spaces; and accordingly many heuristic rejection sampling approaches and retraction methods are suggested to mitigate this issue, but retraction methods often require a distanceto-collision measure [7], [8]. On the contrary, assuming that this performance decay is due to the lack of effective local steering, in [9] a geometric local steering policy that can “feel” the local geometry of configuration spaces is proposed for efficient planning around narrow passages;

![](Huh2019Probabilistically_figs/9ba0b359f9ffb8b526ef656e7cc25ecff338abb75e0a1bcd76704c07f55de5a8.jpg)  
Fig. 1: (left) Probabilistically safe corridor in 3D space constructed around a sample configuration (red) by using tangent hyperplanes (gray) of confidence ellipsoids of a learned Gaussian mixture model of configuration space obstacles. (right) Local steering via probabilistically safe corridor in 2D space: An RRT is extended along the safe direction (red dotted line) towards the projection of a sample goal (red) onto the associated probabilistically safe corridor (red polygon), instead of the standard straight-line extension (blue dotted line) towards the sample goal.

however, its computation also requires a distance-to-collision measure. Since the exact computation of distance-to-collision in complex high-dimensional configuration spaces is hard [10], Gaussian mixture learning [11] and locally weighted regression [12] are applied to construct approximate probabilistic models of collision and collision-free subspaces of configuration spaces for fast collision checking and biased sampling over free space and difficult regions of configuration spaces. In particular, simultaneous modeling of collision and free subspaces is shown to be critical for local planning around narrow passages [13]. In this paper, by combining the strengths of [9] and [11], we introduce a new notion of probabilistically safe corridors for probabilistically safe guided local steering for sampling-based planning without requiring an explicit computation of distance-to-collision.

More precisely, we construct a probabilistically safe corridor around a configuration using tangent hyperplanes of confidence regions of learned Gaussian mixtures that separate the input configuration from the confidence ellipsoids, as illustrated in Fig. 1 (left). Accordingly, we propose a probabilistically safe local steering primitive towards a sample goal configuration via its projection onto the probabilistically safe corridor, as shown in Fig. 1 (right). Since the proposed steering method exploits the local geometry of configuration spaces via learned Gaussian mixture models (GMMs) and generates steering motion within probabilistically safe corridors, in our numerical simulation and experiments, we observe that it yields a better exploration of configuration spaces while minimizing collision likelihood.

In summary, the main contributions of the paper include:

i) a novel geometric approximation of configuration space obstacles by confidence ellipsoids of learned GMMs,

ii) a new construction of probabilistically safe corridors using tangent hyperplanes of confidence ellipsoids,

iii) an effective probabilistically safe local steering primitive that can minimize collision likelihood.

Using numerical simulations and real experiments, we demonstrate that the proposed probabilistically safe local steering approach can dramatically improve the performance of randomized motion planners around narrow passages and significantly outperforms the straight-line local planner in high dimensional configuration spaces by decreasing the number of collisions.

## II. RELATED WORK

Sampling-based planning approaches suffer from heavy computational time in complex environments since they typically require a considerable number of sample configurations and their collision checks. Therefore, several biased sampling methods [5], [14] and rejection sampling methods [15]–[17] are proposed to reduce the number of sample nodes and so to improve computational efficiency. However, these approaches have many heuristic parameters and require explicit configuration space information, such as visibility or collision boundaries, which usually limits their application to low dimensional settings. Another alternative approach to increase the computation efficiency is to reduce the number of collision checks, using either lazy collision checking [18]– [20] or fast probabilistic collision checks [11], [21]–[23]. Exact safety certificates are also utilized for minimizing the computational cost of collision checks [24]. However, these methods are still not able to address the narrow passage problem of sampling-based motion planning.

In order to resolve the narrow passage problem, Zhang and Manocha present a steering approach that retracts sample configurations to become more likely to be connected to nearby nodes [8]. However, it requires a significant number of iterations to find a new collision-free configuration that is around the collision boundary, and also requires an appropriate distance-to-collision measure. In practice, since the exact distance-to-collision measurement in high dimensional configuration spaces is very hard, its applicability is also limited to low dimensional motion planning problems. Moreover, workspace topology is utilized in biasing configuration space exploration for planning around difficult regions [25], [26], but the topology of high-dimensional configuration space (e.g., robot manipulators) is significantly different and more complex than the corresponding workspace topology.

Local safe corridors [27]–[30] recently find significant applications in collision-free motion planning by using sequential composition of simple local planners [31]. Such safe corridors are usually constructed based on a convex decomposition of the environment, which requires an explicit representation of the environment. In [9], a sensory steering algorithm is proposed for sampling-based motion planning that increases the connectivity of randomized motion planning graphs, especially around narrow passages, by exploiting local geometry of configuration spaces via convex local safe corridors. This construction is further extended to integrate local system dynamics and local workspace geometry in kinodynamic motion planning [32]. However, the original construction of sensory steering requires an explicit representation of configuration space obstacles or an explicit distance-to-collision metric, and so its direct application to high dimensional motion planning is limited. In this paper, we enhance this sensory steering algorithm to adapt it to high dimensional settings, such as robotic manipulation, by defining probabilistically safe corridors that are constructed using a learned approximate probabilistic model of a configuration space.

## III. SAFETY-GUIDED RRT

## VIA PROBABILISTICALLY SAFE CORRIDORS

In this section, we first present a brief overview of how learning of Gaussian mixtures<sup>1</sup> can be used for approximate probabilistic modeling of configuration spaces, and then introduce a new notion of a probabilistically safe corridor around a configuration that identifies a safe neighborhood of the configuration with minimal collision risk. Accordingly, we propose a practical extension<sup>2</sup> of the standard RRT planner, called Safety-Guided RRT (SG-RRT), where tree extension is guided to ensure safety constraints defined by probabilistically safe corridors.

## A. Gaussian Mixture Modeling of Configuration Spaces

Let C denote the configuration space of a robotic system embedded in an n-dimensional Euclidean space $\mathbb { R } ^ { n }$ , and denote by $\mathcal { F } \subset \mathcal { C }$ and ${ \mathcal { O } } \subset { \mathcal { C } } .$ , respectively, the free subspace and the collision subspace (i.e., obstacles) of the configuration space C, which, by definition, satisfy $\mathcal { F } = \mathcal { C } \setminus \mathcal { O }$ . In general, an explicit representation of the free space $\mathcal { F }$ or the collision space O in terms of simple geometric shapes is known to be very hard to obtain, especially for highdimensional complex systems such as robotic manipulators. Hence, as in [11], we consider approximate probabilistic representations of the free space $\mathcal { F }$ and the collision space $\mathcal { O }$ in terms of Gaussian mixtures models<sup>1</sup>, respectively, denoted by $\mathscr { G M } ( { \pmb { \mu } } _ { \mathcal { F } } , { \pmb { \Sigma } } _ { \mathcal { F } } , \omega _ { \mathcal { F } } )$ and $\mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \omega _ { \mathcal { O } } )$ , that are constructed using collision and collision-free sample configurations as described below. Here, a Gaussian mixture distribution $\mathcal { G M } ( \mu , \Sigma , \omega )$ , consisting of $K \in \mathbb { N }$ mixture components, is parametrized by a list of mixture means $\pmb { \mu } : =$ $( \mu _ { 1 } , \bar { \mu } _ { 2 } , \dots , \mu _ { K } ) \in ( \mathbb { R } ^ { n } ) ^ { K }$ , a list of positive-definite covariance matrices $\ b { \Sigma } : = ( \bar { \Sigma } _ { 1 } , \bar { \Sigma } _ { 2 } , \bar { \Sigma } \bar { \Sigma } ^ { \bar { \ n } } ) \in \left( \mathbb { R } ^ { n \times n } \right) ^ { K }$ and a list of normalized mixture weights $\omega : = ( \omega _ { 1 } , \omega _ { 2 } , \dots , \omega _ { K } ) \in$ $\left( \mathbb { R } _ { > 0 } \right) ^ { K }$ , satisfying $\textstyle \sum _ { k = 1 } ^ { K } \omega _ { k } = 1$ , and its value at a point $\mathbf { x } \in \mathbb { R } ^ { n }$ is given by

$$
\mathcal {G M} (\mathrm{x}; \boldsymbol {\mu}, \boldsymbol {\Sigma}, \boldsymbol {\omega}) := \sum_ {k = 1} ^ {K} \omega_ {i} \mathcal {N} (\mathrm{x}; \mu_ {k}, \Sigma_ {k}),\tag{1}
$$

![](Huh2019Probabilistically_figs/d833db601b82e90e3cde8582698a89869522e60a8778ee89c179b5394de334c0.jpg)  
Fig. 2: Examples of learned Gaussian mixture models. Ellipsoids show the confidence regions associated with the confidence level of $\kappa = 0 . 9 .$ (left) Gaussian mixtures in the 3D workspace shown in Fig. 9, (right) Gaussian mixtures in the configuration space of a 2DoF planar manipulator.

where $\mathcal { N } ( \mathrm { x } ; \mu , \Sigma )$ is the multivariate Gaussian distribution with mean $\mu$ and covariance matrix $\Sigma .$

$$
\mathcal {N} (\mathrm{x}; \mu , \Sigma) := \frac {1}{\det (2 \pi \Sigma) ^ {\frac {1}{2}}} \exp \left(- \frac {1}{2} (\mathrm{x} - \mu) ^ {\mathrm{T}} \Sigma^ {- 1} (\mathrm{x} - \mu)\right)\tag{2}
$$

Note that the numbers of mixtures, $K _ { \mathcal { F } }$ and $K _ { \mathcal { O } }$ , used for modeling the free space $\mathcal { F }$ and the collision space $\mathcal { O }$ can be different, especially the Meanshift clustering algorithm used in this paper automatically determines the number of mixture components using sample configurations based on a geometric bandwidth parameter as described below. It is also important to highlight that one can simply use $\mathscr { G M } ( { \mathrm { x } } , \mu _ { \mathcal { F } } , \Sigma _ { \mathcal { F } } , \omega _ { \mathcal { F } } )$ and $\mathcal { G M } ( \mathrm { x } , \mu _ { \mathcal { O } } , \Sigma _ { \mathcal { O } } , \omega _ { \mathcal { O } } )$ to estimate how likely a configuration is in collision, which is leveraged in [11] for fast collision checking and biased sampling. In addition to such demonstrated potential improvements, we shall show below that confidence regions of these Gaussian mixture models can be utilized for understanding the local geometry of the configuration space $\mathcal { C }$ and for increasing the quality of the local steering heuristic (which is the Euclidean distance in our case) to better approximate the true geodesic (cost-to-go) metric of the configuration space $\mathcal { C } .$

1) Learning Gaussian Mixtures: One can use a number of Expectation-Maximization (EM) variant methods for Gaussian mixture learning for modeling the free space $\mathcal { F }$ and the collision space $\mathcal { O }$ using collision and collisionfree sample configurations in an offline or online manner, as in our previous work [11]. In this paper, we apply the Meanshift clustering method [33] with a Gaussian kernel for learning Gaussian mixtures using collision information of sample configurations obtained during previous attempts of a randomized motion planner, which is a convenient way of learning from past experiences and exploiting the collision history. In addition, this approach resolves the problem that general mixture modeling approaches have no explicit way of determining the required number of mixtures, because the Meanshift clustering requires a kernel bandwidth B instead of the number of clusters $K .$ . The kernel bandwidth $B$ can be set based on the desired level of spatial resolution. With the bandwidth B, we initialize the clusters and then perform a single step EM update to estimate cluster statistics. We set the membership weight value as $z _ { k } ^ { i } = 1$ if the ith point in $N$ samples is included in the kth cluster, and $z _ { k } ^ { i } = 0$ otherwise.

Then, the cluster statistics (mass $m _ { k }$ , mean $\mu _ { k }$ , covariance matrix $\Sigma _ { k }$ , and weight $\omega _ { k } )$ for the kth cluster are given by

$$
\begin{array}{l} m _ {k} = \sum_ {i = 1} ^ {N} z _ {k} ^ {i}, \mu_ {k} = \frac {1}{m _ {k}} \sum_ {i = 1} ^ {N} z _ {k} ^ {i} \mathrm{x} _ {i}, \omega_ {k} = \frac {m _ {k}}{\sum_ {j = 1} ^ {K} m _ {j}}, \\ \Sigma_ {k} = \frac {1}{m _ {k}} \sum_ {i = 1} ^ {N} z _ {k} ^ {i} (\mathrm{x} _ {i} - \mu_ {k}) (\mathrm{x} _ {i} - \mu_ {k}) ^ {\mathrm{T}}, \text {for k\in\{1,\cdots,K\}}. \end{array}
$$

In Fig. 2, we present some examples of constructed probabilistic models of different configuration space and workspace by the suggested approach. Fig. 2 (left) shows a probabilistic model to define the collision space from 3D point clouds obtained by a depth sensor. Fig. 2 (right) shows the generated probabilistic models using collision information of samples in the configuration space of a 2DoF planar manipulator. Such probabilistic representations of configuration spaces can be utilized for collision likelihood estimation, as a computationally efficient alternative to the exact distance-to-collision measurement [11].

2) Confidence Regions of Gaussian Mixtures: While a Gaussian mixture model $\mathscr { G M } ( { \pmb { \mu } } _ { \mathcal { F } } , { \pmb { \Sigma } } _ { \mathcal { F } } , \omega _ { \mathcal { F } } )$ of the free space $\mathcal { F }$ can be used to bias sampling over the free space, in addition to its use in fast collision checking [11], we propose a new novel use of confidence regions of a Gaussian mixture model $\mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \omega _ { \mathcal { O } } )$ of the collision space O for understanding the local geometry of the configuration space ${ \mathcal { C } } ,$ which is the main contribution of the present paper.

Definition 1: The confidence region $\mathcal { C } _ { p } ( \kappa )$ of a continuous probability distribution $p : \mathbb { R } ^ { n }  \mathbb { R } _ { \geq 0 }$ associated with a confidence level $\kappa \in [ 0 , 1 ]$ is defined to be the super level set $\mathcal { L } _ { p } ( \tau ) : = \{ \mathrm { x } \in \mathbb { R } ^ { n } | p ( \mathrm { x } ) \geq \tau \}$ of $p ,$ for some $\tau \in \mathbb { R } _ { \geq 0 } .$ over which the cumulative mass distribution of $p$ is κ, i.e,

$$
\mathcal {C} _ {p} (\kappa) = \mathcal {L} _ {p} (\tau) \quad \text { such   that } \quad \int_ {\mathcal {L} _ {p} (\tau)} p (\mathrm{x}) \mathrm{d} \mathrm{x} = \kappa  .\tag{3}
$$

Hence, it is convenient to have $L _ { p } ( \kappa )$ denote the level function of $p$ that returns the corresponding level of $p$ defining the confidence region $\mathcal { C } _ { p } ( \kappa )$ , i.e.,

$$
\mathcal {C} _ {p} (\kappa) = \mathcal {L} _ {p} (L _ {p} (\kappa)).\tag{4}
$$

Although confidence regions of an arbitrary probability distribution cannot be expressed explicitly in terms of simple geometric shapes and so are needed to be computed numerically [34], confidence regions of Gaussian distributions have an analytical ellipsoidal form.

Remark 1: For any confidence level $\kappa \in [ 0 , 1 ]$ , the ellipsoidal confidence region $\mathcal { C } _ { \mathcal { N } ( \mu . \Sigma ) } ( \kappa )$ and the level function $L _ { \mathcal { N } ( \mu , \Sigma ) } ( \kappa )$ of the Gaussian distribution $\mathcal { N } ( \mathrm { x } ; \mu , \Sigma )$ are, respectively, given by

$$
\mathcal {C} _ {\mathcal {N} (\mu , \Sigma)} (\kappa) = \left\{\mathrm{x} \in \mathbb {R} ^ {n} \mid (\mathrm{x} - \mu) ^ {\mathrm{T}} \Sigma^ {- 1} (\mathrm{x} - \mu) \leq F _ {\chi_ {n} ^ {2}} ^ {- 1} (\kappa) \right\}\tag{5}
$$

$$
L _ {\mathcal {N} (\mu , \Sigma)} (\kappa) = \frac {1}{\det (2 \pi \Sigma) ^ {\frac {1}{2}}} \exp \left(- \frac {1}{2} F _ {\chi_ {n} ^ {2}} ^ {- 1} (\kappa)\right),\tag{6}
$$

where $F _ { \chi _ { n } ^ { 2 } } : \mathbb { R } _ { \ge 0 }  [ 0 , 1 ]$ denotes the cumulative probability distribution of $\chi _ { n } ^ { 2 }$ distribution with n degrees of freedom. Hence, for any $\tau \in \mathbb { R } _ { \geq 0 }$ , the confidence level κ of the super level set $\mathcal { L } _ { \mathcal { N } ( \mu , \Sigma ) } ( \tau )$ of the Gaussian distribution $\textstyle { \mathcal { N } } ( { \boldsymbol { \mu } } , { \boldsymbol { \Sigma } } )$ is explicitly given by

![](Huh2019Probabilistically_figs/ae8be55fc336044602c9bc808197bbbfc373ba8767b16a0f767e46052293ddc6.jpg)  
<sup>x</sup>(a)

![](Huh2019Probabilistically_figs/34e526a880b5bd0f066346f0a631e1aec93b24fdbb71f86743ddc9076ac65ba9.jpg)

![](Huh2019Probabilistically_figs/1ecd192bedd6ca9303c3a5c7da4154c0f209f44b4c4558c92d43c28a9f0cc832.jpg)  
(c)

<sup>x</sup>(b)  
![](Huh2019Probabilistically_figs/ca860b5668314a46736f659f0d9cfb2b4a6ececb0b20b04cb82238edd8fe4b90.jpg)  
(d)  
Fig. 3: GMM confidence regions. (a) Super level sets of individual Gaussians at confidence level $\begin{array} { r l r } { \kappa _ { k } } & { { } = } & { \kappa . } \end{array}$ (b) Super level sets of Gaussians at the confidence levels corresponding to a shared probability level. (c) An example configuration space (collisions are in blue and free space is in red) and (d) the associated confidence ellipsoids of learned GMM distributions from collision samples (black in (c)).

$$
\kappa = L _ {\mathcal {N} (\mu , \Sigma)} ^ {- 1} (\tau) = F _ {\chi_ {n} ^ {2}} \big (- \log \big (\tau^ {2} \det (2 \pi \Sigma) \big) \big).\tag{7}
$$

Accordingly, since it lacks an exact closed-form expression, we suggest approximating the confidence region of a Gaussian mixture distribution $\mathcal { G M } ( \mu , \Sigma , \omega )$ associated with a confidence level $\kappa \in [ 0 , 1 ]$ as a union of ellipsoidal confidence regions of individual Gaussians, associated with confidence levels $\pmb { \kappa } : = \left( \kappa _ { 1 } , \kappa _ { 2 } , \ldots , \kappa _ { K } \right)$ that satisfy $\textstyle \sum _ { k = 1 } ^ { K } \omega _ { k } \kappa _ { k } = \kappa$ , as

$$
\overline {{\mathcal {C}}} _ {\mathcal {G M} (\boldsymbol {\mu}, \boldsymbol {\Sigma}, \boldsymbol {\omega})} (\boldsymbol {\kappa}) := \bigcup_ {k = 1} ^ {K} \mathcal {C} _ {\mathcal {N} (\mu_ {k}, \Sigma_ {k})} (\kappa_ {k}),\tag{8}
$$

$$
= \bigcup_ {k = 1} ^ {K} \left\{\mathrm{x} \in \mathbb {R} ^ {n} | (\mathrm{x} - \mu_ {k}) ^ {\mathrm{T}} \Sigma_ {k} ^ {- 1} (\mathrm{x} - \mu_ {k}) \leq F _ {\chi_ {n} ^ {2}} ^ {- 1} (\kappa_ {k}) \right\},\tag{9}
$$

Observe that, by construction, we have

$$
\int_ {\overline {{\mathcal {C}}} _ {\mathcal {G M} (\boldsymbol {\mu}, \boldsymbol {\Sigma}, \boldsymbol {\omega}) ^ {(\kappa)}}} \mathcal {G M} (\mathrm{x}; \boldsymbol {\mu}, \boldsymbol {\Sigma}, \boldsymbol {\omega}) \mathrm{dx} \geq \kappa .\tag{10}
$$

A standard choice of the confidence levels of individual Gaussians is $\kappa _ { k } ~ = ~ \kappa$ for all k as shown in Fig. 3 (a); however, this usually yields a poor approximation of the actual confidence region of the mixture model because less accurate Gaussians with high variances become more influential in determining the confidence region. A more accurate analytical choice for the individual confidence levels is $\begin{array} { r } { \kappa _ { \boldsymbol { k } } ~ = ~ L _ { \mathcal { N } ( \mu _ { \boldsymbol { k } } , \Sigma _ { \boldsymbol { k } } ) } ^ { - 1 } \left( \frac { \tau } { \omega _ { \boldsymbol { k } } } \right) } \end{array}$ based on a shared probability level $\begin{array} { r } { \tau ~ = ~ \sum _ { k = 1 } ^ { K } \omega _ { k } ^ { 2 } L _ { \mathcal { N } ( \mu _ { k } , \Sigma _ { k } ) } ( \kappa ) } \end{array}$ [35]. Alternatively, in this paper, we use an iterative search algorithm to find a more accurate shared probability level τ as described in [35] and set $\begin{array} { r } { \kappa _ { k } = L _ { \mathcal { N } ( \mu _ { k } , \Sigma _ { k } ) } ^ { - 1 } \Big ( \frac { \tau } { \omega _ { k } } \Big ) } \end{array}$ for all k, as shown in Fig. 3 (b). With this approach, we obtain confidence regions of Gaussian mixture models that approximately represents configuration space obstacles, as illustrated in Fig. 3 (c)-(d).

## B. Probabilistically Safe Corridors

Suppose $\mathcal { G M } ( \mu _ { \mathcal { O } } , \Sigma _ { \mathcal { O } } , \omega _ { \mathcal { O } } )$ be a Gaussian mixture model constructed as described above for modeling the collision subspace O of a configuration space in $\mathbb { R } ^ { n }$ and let $\overline { { \mathcal { C } } } _ { \mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \pmb { \omega } _ { \mathcal { O } } ) } ( \pmb { \kappa } _ { \mathcal { O } } )$ be the corresponding approximate confidence region associated with a desired confidence level $\begin{array} { r } { \kappa = \sum _ { k = 1 } ^ { K \mathcal { O } } \omega _ { \mathcal { O } _ { k } } \kappa _ { \mathcal { O } _ { k } } } \end{array}$ . Accordingly, we define the probabilistically safe corridor around a configuration $\mathbf { p } \in { \dot { \mathbb { R } } } ^ { n }$ to be

$$
\mathcal {S C} _ {\mathcal {O}} (\mathrm{p}) := \Bigg \{\mathrm{x} \Big | \frac {(\mathrm{p} - \mu_ {\mathcal {O} _ {k}}) ^ {\mathrm{T}} \Sigma_ {\mathcal {O} _ {k}} ^ {- 1} (\mathrm{x} - \mu_ {\mathcal {O} _ {k}})}{\| \Sigma_ {\mathcal {O} _ {k}} ^ {- \frac {1}{2}} (\mathrm{p} - \mu_ {\mathcal {O} _ {k}}) \| ^ {2}} \geq \min \left(\frac {\sqrt {F _ {\chi_ {n} ^ {2}} ^ {- 1} (\kappa_ {\mathcal {O} _ {k}})}}{\| \Sigma_ {\mathcal {O} _ {k}} ^ {- \frac {1}{2}} (\mathrm{p} - \mu_ {\mathcal {O} _ {k}}) \|}, 1 - \epsilon\right), \forall k \Bigg \},\tag{11}
$$

$$
= \left\{\mathrm{x} \in \mathbb {R} ^ {n} \Big | \frac {\left(\mu_ {\mathcal {O} _ {k} - \mathrm{p}}\right) ^ {\mathrm{T}} \Sigma_ {\mathcal {O} _ {k}} ^ {- 1} (\mathrm{x} - \mathrm{p})}{\left\| \Sigma_ {\mathcal {O} _ {k}} ^ {- \frac {1}{2}} \left(\mu_ {\mathcal {O} _ {k} - \mathrm{p}}\right) \right\| ^ {2}} \leq \max \left(1 - \frac {\sqrt {F _ {\chi_ {n} ^ {2}} ^ {- 1} \left(\kappa_ {\mathcal {O} _ {k}}\right)}}{\left\| \Sigma_ {\mathcal {O} _ {k}} ^ {- \frac {1}{2}} \left(\mu_ {\mathcal {O} _ {k} - \mathrm{p}}\right) \right\|}, \epsilon\right), \forall k \right\},\tag{12}
$$

which is constructed using tangent hyperplanes of confidence ellipsoids of Gaussians and is a closed convex polytope, as depicted Fig. 4. Here, $\epsilon \in \mathbb { R }$ is a scalar safety tolerance parameter, and k.k denotes the standard Euclidean norm, and for any positive-definite covariance matrix $\Sigma ~ \in ~ \mathbb { R } ^ { n \times n }$ , a positive-definite choice of $\Sigma ^ { - \frac { 1 } { 2 } }$ is $\begin{array} { r l r } { \Sigma ^ { - \frac { 1 } { 2 } } } & { { } = } & { \mathrm { V } \left( \mathrm { d i a g } \left( \frac { 1 } { \sqrt { \sigma _ { 1 } } } , \frac { 1 } { \sqrt { \sigma _ { 2 } } } , \dots , \frac { 1 } { \sqrt { \sigma _ { n } } } \right) \right) \mathrm { V ^ { T } } } \end{array}$ where $\Sigma =$ V diag $( \sigma _ { 1 } , \bar { \sigma _ { 2 } } , \ldots , \bar { \sigma } _ { n } ) \mathrm { V } ^ { \mathrm { T } }$ is the singular-value decomposition of Σ. It is also useful to observe from (5) that $F _ { \chi _ { \ v { r } _ { \ v { r } } } ^ { 2 } } ^ { - 1 } ( \kappa \mathcal { O } _ { \ v { k } } ) = \left\| \Sigma _ { \mathcal { O } _ { \ v { k } } } ^ { - \frac { 1 } { 2 } } ( \mu _ { \mathcal { O } _ { \ v { k } } } - \mathrm { p } ) \right\| ^ { 2 }$ for any confidence region boundary point $\mathrm { p } \in \partial \mathcal { C } _ { N \left( \mu _ { \mathcal { O } _ { k } } , \Sigma _ { \mathcal { O } _ { k } } \right) } ( \kappa _ { \mathcal { O } _ { k } } )$ . Hence, the safety constraints encoded by $\mathcal { S } \mathcal { C } _ { \mathcal { O } }$ are relaxed with increasing .

Proposition 1: For $\epsilon \geq 0$ , the probabilistically safe corridor ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { { p } } )$ of a configuration $\mathrm { p } \in \mathbb { R } ^ { n }$ is a nonempty convex neighborhood of p; and for $\epsilon > 0 , S C _ { \mathcal { O } } ( \mathrm { p } )$ strictly contains p in its interior $\ddot { S C } _ { \mathcal { O } } ( \mathrm { p } )$ , i.e., for any $\mathrm { p } \in \mathbb { R } ^ { n }$

$$
\mathrm{p} \in \mathcal {S C} _ {\mathcal {O}} (\mathrm{p}) \quad \forall \epsilon \geq 0, \text {   and   } \mathrm{p} \in \mathring {\mathcal {S C}} _ {\mathcal {O}} (\mathrm{p}) \quad \forall \epsilon > 0.\tag{13}
$$

Proof: By definition (12), the probabilistically safe corridor ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { p } )$ is constructed as an intersection of halfspaces and so is a convex polytope. Moreover, for any $\epsilon \geq 0$ (resp. $\epsilon > 0 )$ , these half-spaces are guaranteed to contain p (resp. strictly in their interiors). Thus, the result follows.

Proposition 2: For $\epsilon \leq 0$ , the probabilistically safe corridor ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { { p } } )$ of a probabilistically safe state ${ \mathrm { ~ p ~ } \in \ \mathbb { R } ^ { n } \mathrm { ~ } } \backslash$ $\overline { { \mathcal { C } } } _ { \mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \pmb { \omega } _ { \mathcal { O } } ) } ( \pmb { \kappa } _ { \mathcal { O } } )$ contains p in its interior $\breve { S C } _ { \cal O } ( \mathrm { p } )$ and is also probabilistically safe, i.e.,

$$
\begin{array}{c} \mathrm{p} \in \mathbb {R} ^ {n} \setminus \overline {{\mathcal {C}}} _ {\mathcal {G M} (\boldsymbol {\mu} _ {\mathcal {O}}, \boldsymbol {\Sigma} _ {\mathcal {O}}, \boldsymbol {\omega} _ {\mathcal {O}})} (\boldsymbol {\kappa} _ {\mathcal {O}}) \\ \implies \mathrm{p} \in \mathring {\mathcal {S C}} _ {\mathcal {O}} (\mathrm{p}) \subset \mathbb {R} ^ {n} \setminus \overline {{\mathcal {C}}} _ {\mathcal {G M} (\boldsymbol {\mu} _ {\mathcal {O}}, \boldsymbol {\Sigma} _ {\mathcal {O}}, \boldsymbol {\omega} _ {\mathcal {O}})} (\boldsymbol {\kappa} _ {\mathcal {O}}). \end{array}\tag{14}
$$

Proof: For any $\begin{array} { r } { \displaystyle \mathrm { ~ p ~ } \in \mathbb { R } ^ { n } \setminus \overline { { \mathcal { C } } } _ { \mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \omega _ { \mathcal { O } } ) } ( \pmb { \kappa } _ { \mathcal { O } } ) } \end{array}$ , we have from (5) that $\frac { \sqrt { F _ { x _ { n } ^ { 2 } } ^ { - 1 } \left( \kappa _ { \mathcal { O } _ { k } } \right) } } { \left\| \Sigma _ { \mathcal { O } _ { k } } ^ { - \frac { 1 } { 2 } } \left( \mathrm { p } - \mu _ { \mathcal { O } _ { k } } \right) \right\| } \ < 1 \leq 1 - \epsilon$ for all k. Hence, the result directly follows from (12) and the fact that for any safe configuration $\mathrm { p } \in \mathbb { R } ^ { n } \setminus \overline { { \mathcal { C } } } _ { \mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \omega _ { \mathcal { O } } ) } ( \pmb { \kappa } _ { \mathcal { O } } )$

![](Huh2019Probabilistically_figs/f67aa5757efdfddfa09e736ac1b8e76a5843b5d7f8db5ef636e2ac985b07d76a.jpg)  
Fig. 4: Local steering via probabilistically safe corridors. (left) Example tree extension using a probabilistically safe corridor in 2D space, (right) Probabilistically safe corridor in 3D space.

the probabilistically safe corridor ${ \mathcal { S C } } ( \mathrm { p } ; \mu _ { \mathcal { O } } , \Sigma _ { \mathcal { O } } , \kappa _ { \mathcal { O } } )$ is bounded by tangent hyperplanes of confidence regions of individual Gaussians that strictly separates the point p from the Gaussian confidence ellipsoids. ■

Note that the safe corridor ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { { p } } )$ around a probabilistically unsafe configuration $\mathrm { p } \in \overline { { \mathcal { C } } } _ { \mathcal { G M } ( \pmb { \mu } _ { \mathcal { O } } , \pmb { \Sigma } _ { \mathcal { O } } , \pmb { \omega } _ { \mathcal { O } } ) } ( \pmb { \kappa } _ { \mathcal { O } } )$ can be empty for $\epsilon < 0 .$ , especially for Gaussian mixture models with significant overlap. Fortunately, many Gaussian mixture learning algorithms yield proper mixture models with minimal overlap. Moreover, in order to resolve this issue, one can consider using a nonnegative , which adaptively relaxes the safety constraints of ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { p } )$ depending on the safety level of the configuration p and yields a nonempty relatively safe corridor ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { { p } } )$ . Thus, an optimal selection of  is $\epsilon = 0 .$ which ensures nonempty safe corridors for all configurations (Proposition 1) and exact probabilistically safe corridors for probabilistically safe configurations (Proposition 2).

## C. Guided Steering via Safe Corridors

We now describe a novel use of probabilistically safe corridors for guided local steering of sampling-based planning, in particular, RRTs. In the original RRTs, a sample configuration $\mathrm { \ q _ { r a n d } }$ is randomly drawn in the configuration space, and then its nearest node ${ \mathrm { q } } _ { \mathrm { n e a r } }$ in the tree is found based on a distance measure, which is set to be the standard Euclidean distance in this paper. Then, a new configuration $\mathrm { { q } n e w }$ is slightly extended from ${ \mathrm { { q } } } _ { \mathrm { { n e a r } } }$ towards ${ \mathrm { q } } _ { \mathrm { r a n d } } .$ , say using the standard straight-line steering. If $\mathrm { { q } n e w }$ is collision-free, it is added to the tree as a new node, which is connected to the nearest node. If $\mathrm { { q } _ { n e w } }$ collides with an obstacle, then tree construction repeats with another $\mathrm { \ q _ { r a n d } }$

In this paper, we propose a new approach for tree expansion where $\mathrm { q } _ { \mathrm { n e w } }$ is adjusted to head towards collision-free space using probabilistically safe corridors $\mathcal { S } \mathcal { C } _ { \mathcal { O } }$ , as shown in Fig. 4, by projecting $\mathrm { \ q _ { r a n d } }$ onto $S C _ { O } ( \mathrm { q _ { n e a r } } )$ as follows:

$$
\mathrm {q_ {proj} = \Pi_ {\mathcal {S C} _ {\mathcal {O}} (\mathrm {q_ {near}})} (\mathrm {q_ {rand}})}\tag{15}
$$

where $\Pi _ { A } ( \mathbf { x } ) : = \arg \operatorname* { m i n } _ { \mathbf { a } \in A } \| \mathbf { x } - \mathbf { a } \|$ is the metric projection of a point x $\mathbf { \Psi } \in \mathbb { R } ^ { n }$ onto a closed convex set $A \subseteq \mathbb { R } ^ { n }$ ; that is to say, $\Pi _ { A } ( \mathbf { x } )$ returns the closest point of set A to the input point x. Hence, the tree is extended towards $\mathrm { { q _ { p r o j } } }$ instead of q<sub>rand</sub>, as shown in Fig. 4.

Proposition 3: If a sampling-based motion planning algorithm is probabilistically complete for the standard straightline steering, then the straight-line steering towards the projected goal onto probabilistically safe corridors, as described in (15), preserves its probabilistic completeness for $\epsilon > 0 .$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Tree Extension in Configuration Space
Require: :  $\mu_{O}$ ,  $\Sigma_{O}$ 
1:  $\mathcal{T}.init(q_{init})$ ;
2: while Distance( $q_{goal}$ ,  $q_{new}$ ) &gt;  $d_{min}$  do
3:  $q_{rand} \leftarrow$  GetRandomSampling(), iter = 0;
4: while iter &lt; max_iter do
5:  $q_{near} \leftarrow$  GetNearestNeighbor( $T$ ,  $q_{rand}$ );
6:  $q_{proj} \leftarrow$  SteeringGuide( $\mu_{O}$ ,  $\Sigma_{O}$ ,  $q_{near}$ ,  $q_{rand}$ );
7:  $q_{adj} \leftarrow$  StraightLineSteering( $q_{near}$ ,  $q_{proj}$ ,  $\delta$ );
8: if StraightLine( $q_{near}$ ,  $q_{adj}$ ) is Collision-Free then
9:  $\mathcal{T}.addTree(q_{adj})$ , iter = iter + 1;
10: else
11: break;
12: end if
13: end while
14: end while
</div>

Proof: The result simply follows from Proposition 1 because the probabilistically safe corridor ${ \mathcal { S C } } _ { \mathcal { O } } ( \mathrm { p } )$ of a configuration $\mathbf { p } \in \mathbb { R } ^ { n }$ strictly contains p in its interior for $\epsilon > 0$ and the metric projection onto a probabilistically safe corridor locally behaves as the identity map. In other words, for $\epsilon > 0 .$ , the straight-line steering toward the projected goal onto probabilistically safe corridors is locally equivalent to the standard unconstrained straight-line steering.

One computational challenge of our guided steering approach is that it requires to recompute the metric projection of $\mathrm { \ q _ { r a n d } }$ onto $S C _ { O } ( \mathrm { q _ { n e a r } } )$ for each new selection of $\mathrm { \ q _ { r a n d } }$ and so ${ \mathrm { q } } _ { \mathrm { n e a r } }$ . Metric projection onto a convex polytope can be solved using any state-of-the-art quadratic optimization solver. For efficiency, we apply the active-set method for quadratic optimization, which is an iterative solver that ensures a feasible solution and a decrement on the objective function at each iteration. This enables us to inherit some useful information from prior computation and stop its computation after some desired number of iterations. In order to reduce to computational cost, we keep $\mathrm { \ q _ { r a n d } }$ the same until a maximum number of iteration max iter is reached. This enables us to warm-start the active set method with the active constraints of the previous computation. If active constraints at the optimal solution are given, then a quadratic optimization problem with inequality constraints can be converted into a quadratic problem with equality constraints, which requires significantly less computational time to solve the optimization problem. For example, previous active constraints could be still active for slightly changed ${ \mathrm { q } } _ { \mathrm { n e a r } }$ if the sample goal $\mathrm { \ q _ { r a n d } }$ is kept the same. Therefore, to increase computational efficiency, we always check first if the quadratic optimization is feasible with previously active hyperplane constraints of probabilistically safe corridors.

1) Tree Extension in the Configuration Space: Algorithm 1 presents the pseudocode for the proposed tree extension methods in the configuration space. Here, the nearest node $\mathrm { { \mathrm { q } } _ { \mathrm { n e a r } } }$ of a random goal $\mathrm { \Phi _ { q r a n d } }$ in tree $\tau$ is extended by a new node $\mathrm { \Delta q _ { a d j } }$ towards the projected goal $\mathrm { { q _ { p r o j } } }$ through the probabilistically safe corridor $\mathcal { S } \mathcal { C } _ { \mathcal { O } }$ of q<sub>near</sub>. If the random goal $\mathrm { \ q _ { r a n d } }$ satisfies the safety corridor constraints, then the tree is directly extended to the random goal, just like the standard straight-line extension method. In our implementation, we set the maximum number of iterations, max iter (Line 4), for using the same random goal $\mathrm { \ q _ { r a n d } }$ to be 3, and we select the maximum stepsize of the straight-line planner, δ (Line 7), manually depending on the desired accuracy level of collision checks.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Tree Extension in Task Space
Require: :  $\mu_{O}$ ,  $\Sigma_{O}$ 
1:  $T.init(e_{init}, q_{init})$ ;
2: while Distance(qgoal,  $q_{new}$ ) &gt;  $d_{min}$  do
3:  $q_{rand} \leftarrow \text{GetRandomSampling}()$ ;
4:  $q_{near} \leftarrow \text{GetNearestNeighbor}(\mathcal{T}, q_{rand})$ ;
5:  $q_{new} \leftarrow \text{StraightLineSteering}(q_{near}, q_{rand}, \delta)$ ;
6:  $X_{rand}, X_{near}, X_{new} \leftarrow FwdKin(q_{rand}, q_{near}, q_{new})$ ;
7:  $X_{proj} \leftarrow SteeringGuide(\mu_{O}, \Sigma_{O}, X_{near}, X_{rand})$ ;
8:  $\Delta X_{adj} \leftarrow \frac{X_{proj} - X_{near}}{||X_{proj} - X_{near}||} \cdot ||X_{new} - X_{near}||$ ;
9:  $q_{adj} \leftarrow q_{near} + J^{\dagger}(q_{near})\Delta X_{adj}$ ;
10: if StraightLine( $q_{near}, q_{adj}$ ) is Collision-Free then
11: T.addTree( $q_{adj}$ );
12: end if
13: end while
</div>

2) Tree Extension in the Task Space: For task space planning, we also use probabilistically safe corridors for guiding the end-effector of a manipulator as described in Algorithm 2. Using forward kinematics, we define $\mathrm { X _ { r a n d } }$ to be the end-effector position of the random goal $\mathrm { \ q _ { r a n d } }$ and $\mathrm { X } _ { \mathrm { n e a r } }$ to be the end-effector position of the nearest node $\mathrm { \Phi _ { q n e a r } }$ of $\mathrm { \Phi _ { q r a n d } }$ in tree T . Here, our objective is to steer the end-effector position $\mathrm { X } _ { \mathrm { n e a r } }$ towards $\mathrm { X _ { r a n d } }$ via the projection $\mathrm { X _ { p r o j } }$ of $\mathrm { X _ { r a n d } }$ onto the $S C _ { O } ( \mathrm { X } _ { \mathrm { n e a r } } )$ along the safe corridor $S C _ { O } ( \mathrm { X } _ { \mathrm { n e a r } } )$ in 3D space, as shown in Fig. 4. Accordingly, we select a steering step that is proportional with the stepsize of the standard straight-line steering of the end-effector as

$$
\Delta \mathrm{X} _ {\mathrm{adj}} = \frac {\mathrm{X} _ {\mathrm{proj}} - \mathrm{X} _ {\mathrm{near}}}{| | \mathrm{X} _ {\mathrm{proj}} - \mathrm{X} _ {\mathrm{near}} | |} \cdot | | \mathrm{X} _ {\mathrm{new}} - \mathrm{X} _ {\mathrm{near}} | |,\tag{16}
$$

and determine the corresponding configuration as:

$$
\mathrm{q} _ {\text { adj }} = \mathrm{q} _ {\text { near }} + J ^ {\dagger} (\mathrm{q} _ {\text { near }}) \Delta \mathrm{X} _ {\text { adj }},\tag{17}
$$

where $J ^ { \dagger }$ is the pseudoinverse of manipulator Jacobian $^ { J , }$ satisfying $J ^ { \dagger } \ = \ \mathsf { \bar { J } } ^ { T } ( J J ^ { T } ) ^ { - 1 }$ . In Fig. 5, we illustrate the guided steering of a manipulator using probabilistically safe corridors in task space: The new configuration (magenta), suggested by the standard straight line planner, collides with obstacles, whereas the adjusted configuration (green), consistent with probabilistically safe corridors, moves in the tangent direction of obstacles.

3) GMM-based Biased Sampling: In our experiments, we also compute the mixtures of Gaussian $\mathscr { G M } ( { \bf x } , \mu _ { \mathcal { F } } , \Sigma _ { \mathcal { F } } , \omega _ { \mathcal { F } } )$

![](Huh2019Probabilistically_figs/e40f61c0cb99f05f3f40b421e9ae2df3919e004434061c809866a9e33f2790fd.jpg)  
Fig. 5: Examples of task-space steering of a robotic manipulator. Here, the new configuration (magenta), suggested by the straight line planner from the nearest configuration (black), is adjusted to a better configuration (green) based on the associated probabilistically safe corridor.

for modeling the free space, which is used for biased sampling over the free space as described in [11]. For the settings where biased sampling is used, instead of uniform sampling in Line 3 in Algorithms 1 and 2, we randomly sample a configuration from the collision-free Gaussian mixture distribution $\mathcal { G M } ( \mathrm { x } , \mu _ { \mathcal { F } } , \Sigma _ { \mathcal { F } } , \omega _ { \mathcal { F } } )$ . This sampling method increases the likelihood of a new sample being collision-free, and so can increase the computational efficiency of planning as discussed below.

## IV. RESULTS

We evaluate SG-RRT in various environments using both a simulator and a real robot. We analyze the performance of SG-RRT by comparison with several existing RRT approaches. In addition, we demonstrate SG-RRT on a real humanoid robot and provide results under real settings. All experiments are performed on a 2.7GHz PC, and all planners are implemented in Matlab.

## A. Learning Gaussian Mixture Models

In all our experiments, we learn Gaussian mixture models offline by using the samples generated during the standard RRT planning (which was rich enough for accurate modeling, see Fig. 6(b)) and by manually selecting the kernel bandwidth for the Meanshift clustering so that the desired level of representation resolution is guaranteed. In particular, we select the Gaussian kernel sizes for the Meanshift clustering as 10 degrees for 2DoF manipulator planning, 20 degrees for 7DoF manipulator planning, and 5 cm for task space planning. GMM learning takes 1.61 seconds for 191 clusters from 10,000 collision samples for 2DoF manipulator, 58.97 seconds for 1,096 clusters from 19,456 collision samples for 7DoF manipulator, and 3.64 seconds for 189 clusters from a 3D point cloud (including 18,413 data points) for task space planning. For probabilistically safe corridors, we set the desired confidence level $\kappa ~ = ~ 0 . 9$ and the safety tolerance $\epsilon = 0 . 0 1$ for all cases. In future work, we plan to consider online GMM learning for adaptive motion planning in dynamic environments.

## B. 2DoF Planar Manipulator

For ease of visual presentation, we first consider motion planning of a 2DoF planar manipulator whose first link is 0.4 units long and second link is 1.6 units long as illustrated

![](Huh2019Probabilistically_figs/1a89aab56356a8dd10a0465390098e28f853af66a013530eeaa3fdcba51ca538.jpg)  
(a) Workspace

![](Huh2019Probabilistically_figs/eb8951787791a18d4448328dee5ac4d9a2c8d4b63b367121167657d66495745e.jpg)  
(b) RRT

![](Huh2019Probabilistically_figs/73e327ba98b38db5bcfe09ef4462907eb7b93835605d4b606b9b4dc5ef54ac26.jpg)  
(c) SG-RRT

Execution time  
![](Huh2019Probabilistically_figs/b214df4e0a763120cfd65665e756cdcd663378004171252450e1fd4753d04000.jpg)  
(d) Execution Time

![](Huh2019Probabilistically_figs/4e518f6a1e942fa30caac552a755d91a4ac1179d1d78ccc5a52bc4685bbca38d.jpg)  
(e) Number of Collision Checks  
Fig. 6: RRT planning performance for a 2 DoF planar manipulator

in Fig. 6(a). In Fig. 6, we compare the computational performance of several variants of RRT planners (the standard RRT, the biased-RRT with 10% goal bias, and the bidirectional RRT) with and without our proposed safety guided steering. Here, GMMs are learned offline along the collision space boundary (as shown in Fig. 3 (d)) using collision samples obtained during the standard RRT planning (green points in Fig. 6(b)) and they are used online for constructing probabilistically safe corridors. In our quantitative evaluation, we consider the total execution time and the total number of collision checks as a performance measure, and we obtain the statistics (average and standard deviation) of these performance measures by running each planning algorithm for 50 times for 20 different start and goal pairs. In overall, we observe that our safety guided steering increases computation performance significantly over the standard straightline steering by dramatically reducing the required number of planning iterations (i.e., collision checks) to find a path between any given start and goal pair, as shown in Fig. 6(e). Because safety guided steering via probabilistically safe corridors minimizes collision risk by adaptively adjusting steering direction and stepsize. As a result, our safety guided local planner yields steering action that are significantly less likely to be in collision; whereas the standard straight-line planner ends up being in collision with more than 50% chance, as seen in Fig. 6(e). Finally, we find it useful to emphasize that the construction of and the projection onto a probabilistically safety corridor takes around 0.2 msec in average for each new sample (denoted by “CorridorTime” in Figure 6 (d)), which is in the same order of magnitude as the computation cost of a collision check that takes around 0.3 msec.

![](Huh2019Probabilistically_figs/bfb52c29ea03b9e00f0482c99092c83a3b1f9a6d568a870f6dc9d68138aff6dc.jpg)  
Fig. 7: Safety-guided RRT planning performance with respect to the number of collision samples used for GMM learning

![](Huh2019Probabilistically_figs/52e5eecbf8b138b164c09fa3b26426d231ee530846146232d4cd1c2dd796a919.jpg)

![](Huh2019Probabilistically_figs/6bee8a9844ace6ae2406d6f1eac1ce7cf48f41609d7d6640d948d5ee6e96b865.jpg)  
Fig. 8: (left) PRM with the standard straight-line planner, (right) PRM with our safety guided local planner

In Fig. 7, we demonstrate how the average number of RRT iterations (i.e., collision checks), required for finding a path between any given start and goal pair, changes with the number of sample collision configurations (i.e., training data) used for Gaussian mixture learning. As expected, the performance of RRT planning with safety guided steering increases with the increasing size of training data as a result of increasing accuracy of the Gaussian mixture model.

In Fig. 8, we present an application of our safety guided steering to the probabilistic roadmap (PRM) planning of the 2DoF planar manipulator. As seen in Fig. 8, our safety guided steering noticeably increases the connectivity of a PRM as compared to the standard straight-line planner. Here, two vertices of a PRM is said to be connected if safety guided steering can joining them in at most 100 steps. Finally, to briefly compare the computation cost of the learning phases of the GMM and PRM methods, we provide in Table I the average computation time for the GMM and PRM constructions for the 2DoF planar manipulator planning. As expected, for the same number of samples, GMM learning is around two orders of magnitude faster then the PRM construction because the connectivity test of PRMs is significantly computationally costly than the nearest neighbor search and the statistics computation of GMM.

TABLE I: GMM and PRM Computation Times

<table><tr><td colspan="4">GMM Construction Time (sec)</td><td colspan="4">PRM Construction Time (sec)</td></tr><tr><td>Num. of Samples</td><td>Sampling Time</td><td>GMM Time</td><td>Total Time</td><td>Num. of Vertices</td><td>PRM Time</td><td>Collision Checks</td><td>Connected PRM</td></tr><tr><td>300</td><td>0.1665</td><td>0.0489</td><td>0.2154</td><td>100</td><td>2.4750</td><td>7,983</td><td>No</td></tr><tr><td>500</td><td>0.2023</td><td>0.1220</td><td>0.3244</td><td>150</td><td>5.4377</td><td>18,361</td><td>No</td></tr><tr><td>1,000</td><td>0.3855</td><td>0.2632</td><td>0.6487</td><td>200</td><td>10.3674</td><td>35,306</td><td>No</td></tr><tr><td>2,000</td><td>0.7640</td><td>0.4236</td><td>1.1876</td><td>250</td><td>16.0856</td><td>55,517</td><td>No</td></tr><tr><td>4,000</td><td>1.5159</td><td>0.8545</td><td>2.3704</td><td>300</td><td>23.0590</td><td>81,274</td><td>Yes</td></tr><tr><td>6,000</td><td>2.2659</td><td>1.2205</td><td>3.4904</td><td>350</td><td>30.2114</td><td>107,841</td><td>Yes</td></tr><tr><td>8,000</td><td>2.8811</td><td>1.4230</td><td>4.3011</td><td>400</td><td>38.6380</td><td>134,851</td><td>Yes</td></tr><tr><td>10,000</td><td>3.6009</td><td>1.6100</td><td>5.2109</td><td>450</td><td>49.1138</td><td>171,122</td><td>Yes</td></tr></table>

![](Huh2019Probabilistically_figs/8f3e3718bb1ebdd2d9e7d0f1eba1b67b5982f88803d7e4b4609a9aee16930176.jpg)

![](Huh2019Probabilistically_figs/29971de742c04cae79f8da41e70f6a78fd3fd1f6cb31f6db4d9b9a7d0d52a341.jpg)

![](Huh2019Probabilistically_figs/cf8f1274a0f098a8777e3bc21be52576bdd6fcad6111e9d0e62f2ebd57859998.jpg)  
Fig. 9: RRT planning performance for a 7DoF manipulator: (top) Sequential planning tasks, (middle) Average execution time, (bottom) Average number of collision checks

## C. 7DoF Manipulator in 3D Space

In order to validate the performance of SG-RRT quantitatively in high dimensional space, we compare it with traditional approaches with a 7DoF manipulator in 3D space using the Webots simulator of the Cyberbotics Ltd. company. Fig. 9 (top) shows the simulation scenario that is composed of seven sequential planning tasks. This scenario includes a difficult task, where the robot must remove its arm from the lower shelf and then insert it into the upper shelf. The simulation trials are repeated 50 times for accurate evaluation, and we use the average execution time and the number of collision checks as the evaluation criteria.

For the comparison, we evaluate the standard RRT, safeguided RRT (SG-RRT), and safe-guided RRT in the task space (WSSG-RRT). In addition, since we can apply GMMbased sampling as described in Section III-C.3, we also evaluate GMM-based RRT (Gmm-RRT), GMM-based safeguided RRT (GmmSG-RRT), and GMM-based safe-guided RRT in the task space (GmmWSSG-RRT). Note that we apply a bidirectional method (RRT-Connect) [36] in all approaches. The Gmm-RRT can be faster than the standard RRT, and the GmmSG-RRT is the fastest among all approaches. The WSSG-RRT and the GmmWSSG-RRT are faster than the RRT and Gmm-RRT. This demonstrates that the end-effector of the manipulator is effectively guided by the safe corridor in the high dimensional space, and it can reduce the computational time and the number of collision checks compared to traditional approaches. We also observe in Fig. 9 that SGRRT planning is faster and requires less collision checks in configuration spaces than in task spaces, because probabilistically safe corridors are geometrically more informative when constructed in configuration spaces than in task spaces. Therefore, the tree extension with the safe corridor is significantly more efficient than the traditional methods.

## D. Physical Robot Experiments

We demonstrate the performance of SG-RRT on a 7DoF manipulator (length: 85cm) of an actual humanoid robot and an RGBD camera (ASUS Xtion Live Pro) with the scenario shown in Fig. 10 (top). The robot is positioned 35cm from the shelf (35cm × 37cm) on the table. Figure 10 presents the comparison results of GmmSG-RRT and the standard RRT in terms of the execution time and the number of collision checks. Note that we apply a bidirectional method (RRT-Connect) and give 10% goal biased samples. Since the GmmSG-RRT adjusts a new node in the direction that avoids obstacles using probabilistically safe corridors and also utilizes biased sampling over collision-free space, the sample connectivity increases around narrow spaces, and tree expansion efficiently avoids obstacles. GmmSG-RRT is significantly efficient even when the robot needs to insert its arm onto the shelf. On the other hand, the computational time and the number of collision checks for the standard RRT planner dramatically increases in such complicated tasks.

![](Huh2019Probabilistically_figs/f0df1a021f561a1f7d27160697693382f17ee2814755fcaa084ba29895e405af.jpg)

![](Huh2019Probabilistically_figs/3fd5a9b51f7d47ed23b5da277b1ed41940edc3f6026b268b758699c5dcbab48b.jpg)

![](Huh2019Probabilistically_figs/ff21c63e5a03b579b5e1542e64df460418f49f4873de5b845e2cf40d0e873bdb.jpg)  
Fig. 10: RRT planning performance with an actual physical robot: (top) Experiment with a physical robot, (middle) Average execution time, (bottom) Average number of collision checks

## V. DISCUSSION

In this paper, we present an effective local steering approach for sampling-based motion planning using probabilistically safe corridors of learned Gaussian mixture models of configuration spaces. We construct a probabilistically safe corridor around a configuration using tangent hyperplanes of confidence ellipsoids of Gaussian mixture models that are learned using collision history to approximate configuration space obstacles. Accordingly, we propose a probabilistically safe local steering primitive that extends a random motion planning graph towards a sample goal using its projection onto the associated probabilistically safe corridor, which heuristically minimizes collision likelihood. We observe that the proposed local steering approach improves the performance of sampling-based planning in challenging regions, especially narrow passages, by adjusting steering direction and stepsize. In our simulations and experiments with a real robot manipulator, we demonstrate that our proposed safety guided local planner shows significant performance improvement over the standard straight-line planner for randomized motion planning of 2DoF and 7DoF manipulators. In a future paper, we plan to extend our work using online GMM learning for uncertainty-aware adaptive planning.

## REFERENCES

[1] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars, “Proba-<sup>ˇ</sup> bilistic roadmaps for path planning in high-dimensional configuration spaces,” IEEE Trans. Robot. Autom., vol. 12, no. 4, pp. 566–580, 1996.

[2] S. M. LaValle and J. J. Kuffner, “Randomized kinodynamic planning,” Int. J. Robot. Res., vol. 20, no. 5, pp. 378–400, 2001.

[3] D. Hsu, J.-C. Latombe, and R. Motwani, “Path planning in expansive configuration spaces,” in Proc. IEEE Int. Conf. Robot. Autom., 1997, pp. 2719–2726.

[4] S. Karaman, M. R. Walter, A. Perez, E. Frazzoli, and S. Teller, “Anytime motion planning using the RRT\*,” in Proc. IEEE Int. Conf. Robot. Autom., 2011, pp. 1478–1483.

[5] D. Hsu, L. E. Kavraki, J.-C. Latombe, R. Motwani, and S. Sorkin, “On finding narrow passages with probabilistic roadmap planners,” in Int. Work. on Algorithmic Foundations of Robotics, 1998, pp. 141–154.

[6] S. R. Lindemann and S. M. LaValle, “Current issues in sampling-based motion planning,” in Int. Symp. Robotics Research, 2005, pp. 36–54.

[7] M. Saha, J.-C. Latombe, Y.-C. Chang, and F. Prinz, “Finding narrow passages with probabilistic roadmaps: The small-step retraction method,” Autonomous Robots, vol. 19, no. 3, pp. 301–319, 2005.

[8] L. Zhang and D. Manocha, “An efficient retraction-based RRT planner,” in IEEE Int. Conf. Robot. Autom., 2008, pp. 3743–3750.

[9] O. Arslan, V. Pacelli, and D. E. Koditschek, “Sensory steering for sampling-based motion planning,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2017, pp. 3708–3715.

[10] J. Denny, M. Morales, S. Rodriguez, and N. M. Amato, “Adapting RRT growth for heterogeneous environments,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2013, pp. 1772–1778.

[11] J. Huh and D. D. Lee, “Learning high-dimensional mixture models for fast collision detection in rapidly-exploring random trees,” in Proc. IEEE Int. Conf. Robot. Autom., 2016, pp. 63–69.

[12] B. Burns and O. Brock, “Sampling-based motion planning using predictive models,” in IEEE Int Conf Robot Autom, 2005, pp. 3120–3125.

[13] J. Denny and N. M. Amato, “Toggle PRM: A coordinated mapping of C-free and C-obstacle in arbitrary dimension,” in Int. Work. on Algorithmic Foundations of Robotics. Springer, 2013, pp. 297–312.

[14] V. Boor, M. H. Overmars et al., “The Gaussian sampling strategy for probabilistic roadmap planners,” in Proc. IEEE Int. Conf. Robot. Autom., 1999, pp. 1018–1023.

[15] A. Shkolnik and R. Tedrake, “Sample-based planning with volumes in configuration space,” arXiv preprint arXiv:1109.3145, 2011.

[16] A. Shkolnik, M. Walter, and R. Tedrake, “Reachability-guided sampling for planning under differential constraints,” in Proc. IEEE Int. Conf. Robot. Autom., 2009, pp. 2859–2865.

[17] A. Yershova, L. Jaillet, T. Simeon, and S. M. LaValle, “Dynamic- ´ domain RRTs: Efficient exploration by controlling the sampling domain,” in IEEE Int. Conf. Robot. Autom., 2005, pp. 3856–3861.

[18] V. Hwang, M. Phillips, S. Srinivasa, and M. Likhachev, “Lazy validation of experience graphs,” in Proc. IEEE Int. Conf. Robot. Autom., 2015, pp. 912–919.

[19] G. Sanchez and J.-C. Latombe, “On delaying collision checking´ in PRM planning: Application to multi-robot coordination,” Int. J. Robotics Res., vol. 21, no. 1, pp. 5–26, 2002.

[20] R. Bohlin and L. E. Kavraki, “Path planning using lazy PRM,” in IEEE Int. Conf. Robot. Autom., 2000, pp. 521–528.

[21] J. Huh, B. Lee, and D. D. Lee, “Adaptive motion planning with highdimensional mixture models,” in Proc. IEEE Int. Conf. Robot. Autom., 2017, pp. 3740–3747.

[22] J. Pan and D. Manocha, “Fast and robust motion planning with noisy data using machine learning,” in Int. Conf. on Machine Learning, 2013.

[23] G. S. Aoude, B. D. Luders, J. M. Joseph, N. Roy, and J. P. How, “Probabilistically safe motion planning to avoid dynamic obstacles with uncertain motion patterns,” Autonomous Robots, vol. 35, no. 1, pp. 51–76, 2013.

[24] J. Bialkowski, M. Otte, S. Karaman, and E. Frazzoli, “Efficient collision checking in sampling-based motion planning via safety certificates,” Int. J. Robot. Res., vol. 35, no. 7, pp. 767–796, 2016.

[25] E. Plaku, L. E. Kavraki, and M. Y. Vardi, “Motion planning with dynamics by a synergistic combination of layers of planning,” IEEE Trans. Robot. Autom., vol. 26, no. 3, pp. 469–482, 2010.

[26] J. Denny, R. Sandstrom, A. Bregger, and N. M. Amato, “Dynamic ¨ region-biased rapidly-exploring random trees,” in Int. Work. on Algorithmic Foundations of Robotics, 2016.

[27] R. Wein, J. van den Berg, and D. Halperin, “Planning high-quality paths and corridors amidst obstacles,” Int. J. Robot. Res., vol. 27, no. 11-12, pp. 1213–1231, 2008.

[28] R. Geraerts, “Planning short paths with clearance using explicit corridors,” in IEEE Int. Conf. Robot. Autom., 2010, pp. 1997–2004.

[29] J. Chen, T. Liu, and S. Shen, “Online generation of collision-free trajectories for quadrotor flight in unknown cluttered environments,” in IEEE Int. Conf. Robot. Autom., 2016, pp. 1476–1483.

[30] S. Liu, M. Watterson, K. Mohta, K. Sun, S. Bhattacharya, C. J. Taylor, and V. Kumar, “Planning dynamically feasible trajectories for quadrotors using safe flight corridors in 3-d complex environments,” IEEE Robot. Autom. Letters, vol. 2, no. 3, pp. 1688–1695, 2017.

[31] D. C. Conner, A. Rizzi, and H. Choset, “Composition of local potential functions for global robot control and navigation,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2003, pp. 3546– 3551.

[32] V. Pacelli, O. Arslan, and D. E. Koditschek, “Integration of local geometry and metric information in sampling-based motion planning,” in IEEE Int. Conf. Robot. Autom., 2018, pp. 3061–3068.

[33] Y. Cheng, “Mean shift, mode seeking, and clustering,” IEEE Trans Pattern Anal Mach Intell, vol. 17, no. 8, pp. 790–799, 1995.

[34] R. J. Hyndman, “Computing and graphing highest density regions,” The American Statistician, vol. 50, no. 2, pp. 120–126, 1996.

[35] O. Arslan, “Approximating confidence regions of Gaussian mixtures by unions of ellipsoids,” in preparation.

[36] J. J. Kuffner and S. M. LaValle, “RRT-Connect: An efficient approach to single-query path planning,” in IEEE Int. Conf. Robot. Autom., vol. 2, 2000, pp. 995–1001.