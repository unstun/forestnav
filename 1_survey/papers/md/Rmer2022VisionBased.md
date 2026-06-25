---
citation_key: Rmer2022VisionBased
arxiv_id: 2209.06936
arxiv_url: https://arxiv.org/abs/2209.06936
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:24:34Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Planning under Uncertainty, Object Detection, Segmentation and Categorization, Deep Learning for Visual Perception.
:::

# Introduction

robots operate in the real world, safety requires the avoidance of unintended collisions. In order to detect any form of obstacles, visual perception using deep learning (DL) has gained growing attention in recent years . While DL-based perception systems have achieved impressive results in various tasks, several issues prevent their applicability in many safety-critical systems. Firstly, DL models are typically trained using large datasets [@Sun17; @Shelhamer17], which are often not available for custom robotics tasks. However, the creation and annotation of task specific datasets is generally costly, such that small datasets are desirable. Moreover, DL models are prone to causing prediction errors in previously unseen situations [@Kendall17], such that a reliable quantification of their predictive uncertainty is important to enable a cautious behavior of the robotic system. Finally, even when uncertainty information is available, it is often not in the parametric form required for uncertainty-aware planning algorithms, such that additional simplifications are necessary [@Zhu2019].

## Related Work

A common approach in existing work is to address visual perception by semantic segmentation [@Milioto2019]. In recent years, the focus of segmentation approaches has been on DL architectures due to the impressive accuracy achieved with fully convolutional networks [@Shelhamer17]. However, DL is inherently miscalibrated and therefore often produces over-confident predictions [@Kendall17], such that research has focused on improving uncertainty quantification of DL. While Bayesian neural networks with dropout have attracted interest early on [@Gal16], deep ensembles [@Lakshminarayanan17] have gained increasing attention due to their often demonstrated superior performance, reasonable computational cost for inference and parallelizability [@Ovadia2019] . These advantages have also been shown when applying them to semantic segmentation [@Mehrtash2020], but they typically require large training datasets and do not extend to low data regimes, in which ensembling alone is generally insufficient to obtain well-calibrated uncertainty estimates [@rahaman2021]. In order to mitigate this limitation, numerous methods for data augmentation have been proposed [@Devries2017; @Zhang2018] with the goal of improving the generalizability and robustness. The main focus of these augmentation schemes is usually the avoidance of overfitting, such that the dataset size is commonly increased by merely a low factor, often two, and by applying not more than three augmentation methods [@Uzun2021]. However, this is insufficient to achieve robust calibration for small task-specific datasets which are often not representative in terms of diversity.

The results of semantic segmentation can directly be used for robotic motion planning, but such approaches ignore uncertainties in the perception [@Bartolomei2020]. Previous works on motion planning with probabilistic environment representation mostly assume known obstacle geometry and Gaussian distributed object position [@Zhu2019; @Park2018; @Kamel2017]. While these assumptions allow for the derivation of analytical chance constraints, a coarse over-approximation of obstacles can lead to excessive conservatism of planned paths in complex environments. A finer obstacle parameterization or the individual representation of each obstacle can become computationally challenging, especially when the number of obstacles is large, and representing a variation of the uncertainty in the vicinity of the obstacles is difficult. Safe perception-based navigation has also been addressed using Hamilton-Jacobi reachability [@Bajcsy.2019], but the computational cost increases significantly for irregular obstacle surfaces. Other approaches rely on deterministic error bounds for positions estimated using visual perception, such that robust planning methods can be employed [@Dean2020]. Since these error bounds require dense training data in practice, large datasets must generally be available for such approaches. Hence, there exists no uncertainty-aware and flexible approach for safe motion planning based on semantic segmentation when merely a small, non-representative dataset is available.

## Contribution

We propose a general framework for motion planning with uncertainty based on visual perception via probabilistic semantic segmentation. In the perception module, we enable the training of well-calibrated semantic segmentation models for small, non-representative datasets by combining deep ensembles with massive data augmentation. By modifying training images with eight different methods, we increase the dataset size by a factor of 20, which allows us to obtain reliable probabilistic occupancy information. In the safe motion planning module, we avoid conservatism and computational complexity due to parametric obstacle representations by formulating the path planning problem in an uncertain environment as a scenario optimization problem. This allows us to directly determine collision probabilities using the results from probabilistic semantic segmentation, which we exploit in a scenario chance constrained version of the popular RRT\* algorithm [@Karaman2011]. For the resulting path, we propose safe velocity scheduling to ensure safe robot motion despite tracking inaccuracies. We demonstrate the effectiveness of the proposed data augmentation approach for visual perception and the scenario-based path planning formulation in a comparison to state-of-the-art methods. Moreover, we evaluate the safety and robustness of our framework in an experiment with a robotic manipulator.

# Problem Statement

We consider widely-used camera-based perception based on a DL model, which requires labeled data for training. However, due to the lack of suitable training data for many specific robotic applications and the inherent miscalibration of neural networks [@Kendall17], it is generally difficult to obtain an accurate representation of the environment with reliable information on uncertainty. Therefore, we investigate this problem in this letter as formalized in the following.

::: {#prob1 .problem}
**Problem 1** (Uncertainty in visual perception). *Assume a small dataset with low variety is given, which contains RGB images $\bm{C}\!\in\!\mathbb{R}^{H\times W\times 3}$ with height/width $H$/$W$ of marked obstacles with arbitrary pose, geometry and size. Based on the dataset, we consider the problem of training a DL model $\bm{f}:\mathbb{R}^{H\times W\times 3}\times \Theta\rightarrow [0,1]^{H\times W}$ with parameters $\bm{\theta}\!\in\!\Theta$ which outputs for each point $(i,j)$ in an image $\bm{C}$ the probability of being occupied by an obstacle $\mathcal{O}$, i.e., $P((i,j)\!\in\!\mathcal{O})\!=\!f_{ij}(\bm{C},\bm{\theta})$.*
:::

Based on the probabilities of obstacles in the image space, the robotic system must be capable of planning a safe trajectory of poses $\{\bm{p}|\,\bm{p}\in\mathcal{T}\}$ in the task space $\mathcal{T}$. Since each pose $\bm{p}$ implies that the robot occupies some region $\mathcal{R}(\bm{p})\subset\mathcal{W}$ of the physical workspace $\mathcal{W} \subseteq \mathbb{R}^3$, a pose $\bm{p}$ is only collision-free if the set $\mathcal{R}(\bm{p})$ lies completely in the obstacle-free subset $\mathcal{W}_{\mathrm{free}}\subset\mathcal{W}$. However, this cannot be ensured deterministically in general as merely an uncertain estimate of the obstacles and consequently $\mathcal{W}_{\mathrm{free}}$ is available from the visual perception module. Therefore, we aim to satisfy the constraints imposed by $\mathcal{W}_\mathrm{free}$ probabilistically via individual chance constraints with a prescribed probability threshold $\delta\in(0,1)$. This leads to the following formal definition of a $\delta$-safe motion, which is illustrated in [1](#fig:planning_idea){reference-type="ref+label" reference="fig:planning_idea"}.

::: definition
**Definition 1** ($\delta$-safe motion). *The motion $\hat{\bm{\pi}}:[0,\tau]\rightarrow \mathcal{T}$ executed within the time interval $[0,\tau]$ is called $\delta$-safe if it satisfies $P(\bm{x} \in \mathcal{W}_\mathrm{free}) \geq 1-\delta$, ${\forall \bm{x} \in \mathcal{R}(\hat{\bm{\pi}}(t))}$, $\forall t \in [0,\tau]$.*
:::

:::: {#fig:planning_idea .figure}
::: caption
We aim to plan a trajectory $\bm{\pi}:[0,\tau]\rightarrow \mathcal{T}$ in the task space such that during the executed motion $\bm{\hat{\pi}}(\cdot)$, any point $\bm{x}\in\mathcal{R}(\bm{\hat{\pi}}(t))$ occupied by the robot $\mathcal{R}(\bm{\hat{\pi}}(t))$ lies inside the free workspace $\mathcal{W}_\mathrm{free}$ with a probability of at least $1-\delta$ for all $t\in[0,\tau]$.
:::
::::

In this definition, safety is introduced using an individual condition for each time instance, which is a commonly considered requirement for planning in uncertain environments [@Zhu2019; @Park2018]. However, these conditions are posed on the motion $\hat{\bm{\pi}}(\cdot)$ *realized by the robotic system*, which is a significantly stronger notion of safety than merely requiring their satisfaction for the *planned trajectory* $\bm{\pi}:[0,\tau]\rightarrow \mathcal{T}$, which is also illustrated in Fig. [1](#fig:planning_idea){reference-type="ref" reference="fig:planning_idea"}. Therefore, this safety notion clearly cannot be ensured without additional information about the dynamics of the robotic system, such that we assume the availability of a control law with guaranteed tracking error bounds as formalized in the following.

::: {#ass:track_error .assumption}
**Assumption 1** (Velocity-dependent tracking error bound). *The tracking error of the robotic system is bounded by a non-decreasing function $\gamma:\mathbb{R}_0^+\rightarrow \mathbb{R}_0^+$ of its reference velocity, i.e., $\|\hat{\bm{\pi}}(t)-\bm{\pi}(t)\|_2\leq\gamma(\|\dot{\bm{\pi}}(t)\|)$.*
:::

This assumption reflects the fact that the tracking error of robotic systems often grows with increasing reference velocity due to unmodeled effects in control laws, e.g., friction or imprecise inertia parameters. Note that it does not require exact tracking for zero velocity, such that it can also be employed for underactuated robots, which can exhibit relatively large tracking errors at low velocities. Reducing the conservatism for such systems using more sophisticated controllers, e.g., based on barrier functions [@Dean2020], is subject to future work. Tracking error bounds can be obtained, e.g., statistically from experiments [@Nubert2020]. However, generating test trajectories that cover a sufficiently wide range of operating conditions can be challenging for higher-dimensional task spaces.

In addition to safety, other criteria often have to be considered during planning. While they can be represented using general cost functions in principle, we restrict ourselves to commonly found path integrals over immediate costs $c:\mathcal{T}\rightarrow R_{0,+}$, such that their velocity-independence can be exploited to employ computationally more efficient solution approaches [@Bobrow1985]. Therefore, we address the following safe vision-based planning problem.

::: {#prob2 .problem}
**Problem 2** (Safe vision-based motion planning). *Given the uncertain estimate of the obstacles obtained from the visual perception system and the velocity-dependent tracking error bound in [1](#ass:track_error){reference-type="ref+label" reference="ass:track_error"}, we consider the problem of finding a trajectory $\bm{\pi}(\cdot)$, which minimizes the cost $c$ along the path defined through $\bm{\pi}(\cdot)$ and ensures $\delta$-safety of the resulting executed motion $\hat{\bm{\pi}}(\cdot)$, i.e., []{#eq:prob_statement label="eq:prob_statement"} $$\begin{align}
\label{eq:prob_cost}
        % &\min\limits_{\bm{\pi}} \int\limits_{0}^{1} \frac{c(\bm{\pi}(s))}{\|\dot{\bm{\pi}}(s)\|}\mathrm{d} s\\
        &\min\limits_{\bm{\pi}(\cdot)} \int_{0}^{\tau} c(\bm{\pi}(t))\|\dot{\bm{\pi}}(t)\|_2\mathrm{d}t \quad \text{such that  $\hat{\bm{\pi}}(\cdot)$ is $\delta$-safe.} %P(\bm{x}(s)\in\mathcal{X}_{\mathrm{free}})\geq 1-\delta\quad \forall s\in [0,1].
\end{align}$$*
:::

# Visual Perception with Uncertainty Representation

In order to address [1](#prob1){reference-type="ref+label" reference="prob1"}, it is necessary to probabilistically solve a classification problem for each pixel, which is commonly referred to as semantic segmentation. Therefore, we briefly introduce the fundamentals of training DL models for semantic segmentation in [3.1](#subsec:semseg){reference-type="ref+label" reference="subsec:semseg"}, before we show the extension to an ensemble of DL models to obtain occupancy probabilities for each pixel in [3.2](#subsec:ensemble){reference-type="ref+label" reference="subsec:ensemble"}. Finally, we develop a data augmentation approach to achieve more robust uncertainty estimation in [3.3](#subsec:augment){reference-type="ref+label" reference="subsec:augment"}.

## Deep Learning for Semantic Segmentation {#subsec:semseg}

For classifying each pixel in an image using semantic segmentation, we employ the commonly used approach of fully convolutional networks (FCNs) with an encoder-decoder structure [@Shelhamer17]. The encoder applies convolutional and pooling layers, capturing contextual information in a feature vector with downsampled spatial dimensions. In the decoder, the spatial dimensions are upsampled back to the input image size $H \times W$, allowing for pixel-wise dense predictions. We apply atrous convolutional layers with different rates in parallel (Atrous Spatial Pyramid Pooling), which allows to capture objects at multiple scales [@Chen2018]. In the final layer of the model, we employ the softmax activation function for the output channel of every image pixel $(i,j)$. Denoting the parameters of the DL model by $\hat{\bm{\theta}}$, this yields a function $\hat{f}_{ij}(\cdot,\hat{\bm{\theta}})$ for every pixel, which outputs a probability-like value for pixel $(i,j)$ not being occupied by an obstacle, i.e., $\hat{f}_{ij}(\bm{C},\hat{\bm{\theta}})\in [0,1]$. For the training process, we employ the commonly used cross-entropy loss ${\mathcal{L}'(y_{ij},\!\hat{\bm{\theta}})\!=\!-y_{ij}\!\log\!\big(\hat{f}_{ij}(\bm{C},\!\hat{\bm{\theta}})\!\big)}\!-\!{(1-y_{ij})\!\log\!\big(1\!-\!\hat{f}_{ij}(\bm{C},\!\hat{\bm{\theta}})\!\big)}$, where $y_{ij} = 0$ if $(i,j)\in\mathcal{O}$, i.e., pixel $(i,j)$ lies in an obstacle, and $y_{ij}=1$ otherwise. It is computed pixel-wise and summed over the spatial dimensions of the final layer, resulting in the total loss $\mathcal{L}(\hat{\bm{\theta}}) = \sum_{ij} \mathcal{L}'(y_{ij},\hat{\bm{\theta}})$.

## Probabilistic Segmentation using Deep Ensembles {#subsec:ensemble}

:::: {#fig:augmentation_methods .figure}
::: caption
We employ eight methods for data augmentation to systematically add missing variety to the dataset. This increases robustness of the trained segmentation model to differences in perceived scenes and reduces the epistemic uncertainty typically caused by insufficient coverage of the input space by the training samples.
:::
::::

Even though DL models for semantic segmentation yield probability-like outputs, these values are generally not well suited as a measure of uncertainty due to the inherent miscalibration and overconfidence of NNs [@Kendall17]. We address this issue by employing an ensemble of models which is known to produce well calibrated uncertainty predictions with suitable training data [@Ovadia2019]. An ensemble consists of multiple distinct models, called ensemble members. For training the ensemble, we initialize each ensemble member with random model parameters and randomly shuffle the training data before each epoch [@Lakshminarayanan17]. The models are trained independently, such that they capture different features within the data. For inference, the individual member predictions are combined to the final prediction by considering the ensemble as a uniformly-weighted mixture of $M$ models, i.e., $\bm{f}(\bm{C},\bm{\theta})=\sum\nolimits_{m=1}^{M} \hat{\bm{f}}(\bm{C}, \hat{\bm{\theta}}_m)/M$, where $\hat{\bm{\theta}}_m$ denotes the parameters of the $m$-th member concatenated into the overall parameter vector $\bm{\theta}$. Since each function $f_{ij}(\cdot,\bm{\theta})$ also yields values in the range $[0,1]$, but generally exhibits a better calibration, we use it to determine the occupancy probabilities of pixels in the following.

## Data Augmentation for Dataset Diversification {#subsec:augment}

[]{#sec:meth_data_aug label="sec:meth_data_aug"}

While deep ensembles can also be used for learning from small datasets in principle, it has been demonstrated that the resulting performance in semantic segmentation strongly depends on the size of the training set [@Sun17]. Moreover, due to the low variation in the training dataset considered in [1](#prob1){reference-type="ref+label" reference="prob1"}, the estimated epistemic uncertainty may not be well-calibrated when actually employing the deep ensemble in applications with more diverse images [@rahaman2021]. Therefore, directly training a deep ensemble using a small dataset with low variation would be unreliable in safety-critical applications.

In order to mitigate this effect, we propose to massively augment the training data to artificially add the missing variation to the data. The underlying idea of this augmentation is to apply label-preserving transformations to the annotated images, as well as to the corresponding segmentation masks [@Shorten2019]. This idea can be exploited, e.g., when merely few annotated images of the different operating environments are available, to artificially modify their backgrounds as proposed in [@Ghiasi2021]. Moreover, the robustness of the ensemble against partial object occlusions can be increased by randomly erasing parts of the labeled object [@zhong2020]. In total, we identify eight augmentation methods for straightforwardly adding missing information to segmentation datasets, which are illustrated in [2](#fig:augmentation_methods){reference-type="ref+label" reference="fig:augmentation_methods"}. To create as diverse training samples as possible, we combine the augmentation methods by successively applying them to the same image. The key idea of our augmentation scheme is to randomly combine seven augmentation methods by applying each with a probability of $0.5$, after replacing the background. In that way, we not only apply multiple augmentation methods to the same image, but also vary the set of methods used. As a result, our augmentation scheme introduces much more variety than if certain methods were always applied in the exact same way and order. This allows us to substantially improve the segmentation performance and the quality of the uncertainty quantification using deep ensembles when only a small non-representative dataset is available.

::: remark
**Remark 1**. *While our proposed approach can improve uncertainty quantification, it does not provide calibration guarantees. In order to obtain them, re-calibration techniques can be applied, e.g., by re-scaling the output of the deep ensemble such that obstacle pixels are guaranteed to be correctly classified with the desired probability or higher [@guo2017calibration]. Suitable scaling factors can be obtained from test images, e.g., using data-driven optimization approaches [@Campi2009]. Alternatively, the empirical accuracy of the deep ensemble can be determined using test images, such that generalization guarantees such as [@Bradford2019 Theorem 1] can be exploited to certify a reduced accuracy . Note that the results from both of these approaches are best when the calibration is already high, which underlines the importance of our proposed approach.*
:::

# Safe Vision-Based Motion Planning

Based on the probabilistic semantic segmentation results, the goal is to plan and execute a $\delta$-safe motion as introduced in [2](#prob2){reference-type="ref+label" reference="prob2"}. To this end, we split the planning problem into path planning and velocity scheduling. For solving the former, we present a scenario optimization approach in [4.1](#subsec:path_plan){reference-type="ref+label" reference="subsec:path_plan"} and discuss its integration into the RRT\* algorithm in [4.2](#subsec:rrt){reference-type="ref+label" reference="subsec:rrt"}. Subsequently, we determine the maximum velocity profile along the obtained path still admitting a $\delta$-safe motion in [4.3](#subsec:trajectory_planning){reference-type="ref+label" reference="subsec:trajectory_planning"}.

## Path Planning as Scenario Optimization Problem {#subsec:path_plan}

In order to admit a planning in the task space $\mathcal{T}$ of a robotic system, it is generally necessary to augment the probabilistic semantic segmentation result to 3D by using depth information, e.g., from a LiDAR scanner, a stereo camera system or available knowledge about the scene. Potential errors in the depth measurements can be considered, e.g., by enlarging the obstacle accordingly in the direction of the camera. This allows us to compute the occupancy probability $P(\bm{x} \in \mathcal{W}_\mathrm{free})$ for each point $\bm{x}$ in the 3D workspace $\mathcal{W}$. Moreover, we can determine the possibly occupied region ${\mathcal{R}(\bm{\pi}(t)) \oplus \mathcal{B}({\eta}(\gamma(\|\dot{\bm{\pi}}(t)\|){)})}$ in the workspace for each pose along a trajectory $\bm{\pi}(t)\in\mathcal{T}$, where $\mathcal{B}(r)$ is a sphere with radius $r$, $\gamma(\|\dot{\bm{\pi}}(t)\|)$ represents the tracking error bound defined in [1](#ass:track_error){reference-type="ref+label" reference="ass:track_error"}, and $\eta(\cdot)$ maps the task space error to the maximum resulting workspace error. The function $\eta$ can be computed based on the Jacobian mapping task space velocities to the work space. The computation of $\eta$ simplifies and the conservatism reduces if the tracking error in the task space orientation can be neglected. The condition for a pose $\bm{\pi}(t)\in\mathcal{T}$ being $\delta$-safe can be expressed as $$\begin{align}
    P(\bm{x} \in \mathcal{W}_\mathrm{free}) \geq 1-\delta, \forall \bm{x} \in \mathcal{R}(\bm{\pi}(t)) \oplus \mathcal{B}({\tilde{\gamma}}(\|\dot{\bm{\pi}}(t)\|)){,}
\end{align}$$ where $\tilde{\gamma}(\cdot)\vcentcolon=\eta(\gamma(\cdot))$. As the dependence on the reference velocity $\dot{\bm{\pi}}(\cdot)$ is not suitable for standard path planning algorithms, we substitute it with a desired minimum velocity $\underline{v}\in\mathbb{R}_+$. This allows us to split the safe motion planning problem into a simple path planning problem followed by a velocity scheduling problem.

For path planning with uncertainty, strong assumptions are usually made about the shape of obstacles and their probability distribution to derive analytic expressions for the constraint in [2](#prob2){reference-type="ref+label" reference="prob2"} [@Zhu2019; @Park2018; @Kamel2017]. To avoid the associated conservatism and directly use the uncertainty estimates obtained from the solution of [1](#prob1){reference-type="ref+label" reference="prob1"} for path planning, we reformulate [2](#prob2){reference-type="ref+label" reference="prob2"} as a scenario problem [@Campi2009]. The path is discretized into $K\in\mathbb{N}$ poses $(\bm{p}_1, \dots, \bm{p}_K)$ and a fixed set $\mathcal{R}_0 \vcentcolon=\mathcal{R}(\bm{0})$ is defined, such that for all poses $\bm{p} \in \mathcal{T}$, the set $\mathcal{R}(\bm{p})$ can be described as a rigid motion $T^{\bm{p}}(\cdot)$ of $\mathcal{R}_0$, i.e., $\mathcal{R}(\bm{p}) = T^{\bm{p}}(\mathcal{R}_0)$. This allows us to approximate the safety constraint using random samples $\bm{x}^{(n,k)} = T^{\bm{p}_k}\big(\bm{x}_0^{(n)}\big)$, where $N_x\in\mathbb{N}$ vectors $\bm{x}_0^{(n)}$ are drawn from a uniform distribution $\mathcal{U}(\mathcal{R}_0 \oplus \mathcal{B}({\tilde{\gamma}}(\underline{v})))$. This is a common approach for reformulating robust into scenario constraints [@Campi2009]. It leads to the scenario optimization problem $$\label{eq:path_plan_problem}
\begin{align}
    \min_{(\bm{p}_1, \dots, \bm{p}_K)} \:&\sum\nolimits_{j=1}^{K} c(\bm{p}_{{j}}) \\
    \label{eq:safety_constraint}
    \text{s.t.}\quad\; &P\big(\bm{x}^{(n,k)} \in \mathcal{W}_\mathrm{free}\big) \geq 1-\delta, \\ &\forall n = 1,\dots,N_x, \: k = 1,\dots,K, \nonumber
\end{align}$$ with $\bm{x}^{(n,k)} = T^{\bm{p}_k}\big(\bm{x}_0^{(n)}\big), \: \bm{x}_0^{(n)} \sim \mathcal{U}(\mathcal{R}_0 \oplus \mathcal{B}({\tilde{\gamma}}(\underline{v})))$. While the planned path is directly affected by the choice of $\delta$ through [\[eq:safety_constraint\]](#eq:safety_constraint){reference-type="eqref" reference="eq:safety_constraint"}, reducing $\delta$ can have different impact around the obstacle, as the extent of the uncertain area usually varies along the obstacle boundary. In problem [\[eq:path_plan_problem\]](#eq:path_plan_problem){reference-type="eqref" reference="eq:path_plan_problem"}, the safety constraint is only evaluated at discrete points $\bm{p}_1,\dots,\bm{p}_k$ on the path. Still, $\delta$-safety of the continuous path can be achieved by enlarging the set ${\mathcal{R}_0  \oplus \mathcal{B}({\tilde{\gamma}}(\underline{v}))}$, accordingly. For simple calculation, enlarging its enclosing sphere by $\mathcal{B}(l/2)$, where $l$ is the distance between the positions occupied at the ends of the line segment, can be performed. Based on the solution $(\bm{p}_1^*,\ldots,\bm{p}_K^*)$ of problem [\[eq:path_plan_problem\]](#eq:path_plan_problem){reference-type="eqref" reference="eq:path_plan_problem"}, we define the continuous path $\bm{\pi}^*:[0,1] \mapsto \mathcal{T}$ by linearly interpolating between all $\bm{p}_k^*$ such that $\bm{\pi}^*(k\Delta s) = \bm{p}_{k+1}$ for $\Delta s=1/(K-1)$. Since the reliability of the scenario approximation grows with the number of random samples $N_x$ [@Campi2009], this approach provides a well-suited obstacle representation for the proposed uncertainty-aware visual perception.

## Path Planning with the SCC-RRT\* Algorithm {#subsec:rrt}

For solving the scenario optimization problem [\[eq:path_plan_problem\]](#eq:path_plan_problem){reference-type="eqref" reference="eq:path_plan_problem"}, we exemplarily employ a modified version of the popular RRT\* path planning algorithm [@Karaman2011], which we refer to as scenario chance-constrained RRT\* (SCC-RRT\*). The collision checking represents the main difference between our SCC-RRT\* algorithm and previous uncertainty-aware RRT\* variants [@Luders2013]. In order to evaluate whether a line segment $[\bm{p}_1, \bm{p}_2] \subset \mathcal{T}$ is eligible, the safety constraint [\[eq:safety_constraint\]](#eq:safety_constraint){reference-type="eqref" reference="eq:safety_constraint"} is evaluated for discrete poses ${\bm{p}^{(i)} = \bm{p}_1 + i \Delta_p \nicefrac{\bm{p}_2 - \bm{p}_1}{\|\bm{p}_2 - \bm{p}_1\|_2}}$, ${i=0,1,\dots,\left\lceil\nicefrac{\|\bm{p}_2 - \bm{p}_1\|}{\Delta_p}\right\rceil}$, where $\Delta_p \in \mathbb{R}_+$. For each $\bm{p}^{(i)}$, we draw $N_x$ samples $\bm{x}_0^{(n)},\; n=1,\dots,N_x$, uniformly from the set $(\mathcal{R}_0 \oplus \mathcal{B}({\tilde{\gamma}}(\underline{v})))$ and apply the rigid motion $T^{\bm{p}^{(i)}}(\cdot)$ to each $\bm{x}_0^{(n)}$. If all points $T^{\bm{p}^{(i)}}(\bm{x}_0^{(n)})\in \mathcal{W}_\mathrm{free}$ lie inside the free workspace $\mathcal{W}_\mathrm{free}$ with probability at least $1-\delta$, the line segment $[\bm{p}_1,\bm{p}_2]$ is considered $\delta$-safe. The quality of a path is evaluated using a line cost function. By employing the common RRT\* rewiring procedure, our SCC-RRT\* algorithm asymptotically converges to the minimum-cost path if the cost function is monotonous and bounded [@Karaman2011]. As our planning algorithm is global, the risk of getting stuck in local minima due to the unstructured nature of the occupancy estimates obtained from solving [1](#prob1){reference-type="ref+label" reference="prob1"} is avoided.

## Safe Velocity Scheduling {#subsec:trajectory_planning}

While the path obtained using [\[eq:path_plan_problem\]](#eq:path_plan_problem){reference-type="eqref" reference="eq:path_plan_problem"} admits a trajectory executed at the specified minimum velocity $\underline{v}$, a faster execution is possible when the obstacles are sufficiently far away. To find an upper bound $v^*(s)$ on the velocity for $\delta$-safety at some point $\bm{\pi}^*(s)$, we need to determine the distance between the robot and the closest point which is not $\delta$-safe. This distance can be compactly expressed as $$\label{eq:velocity_scheduling_distance}
\begin{align}
    d_{\mathrm{o}}(\bm{\pi}(s)) = \min\limits_{\bm{x}_\mathrm{r},\bm{x}_o} \: &\|\bm{x}_\mathrm{r}-\bm{x}_\mathrm{o}\|_2 \\
    \text{s.t.} \;\: &\bm{x}_\mathrm{r} \in \mathcal{R}(\bm{\pi}(s)) \\ &P(\bm{x}_\mathrm{o} \in \mathcal{W}_\mathrm{free}) < 1-\delta,
\end{align}$$ which can be effectively approximated by sampling multiple positions $\bm{x}_{\mathrm{o}}$ and merely optimizing with respect to $\bm{x}_\mathrm{r}$. Using the distance $d_{\mathrm{o}}(\bm{\pi}(s))$, we can easily determine $v^*(s)$ since ${\tilde{\gamma}}(\dot{\bm{\pi}}(s))\leq d_{\mathrm{o}}(\bm{\pi}(s))$ must hold for $\delta$-safety. Since the chain rule $\dot{\bm{\pi}}(s) = \frac{\mathop{}\!\mathrm{d}\bm{\pi}(s)}{\mathop{}\!\mathrm{d}s}\,\dot{s} = \bm{\pi}'(s)\dot{s}$ admits a parameterization of the velocity in terms of $\dot{s}$, we can obtain $v^*(s)$ by solving $$\label{eq:ds_limit}
\begin{align}
    v^*(s) = \max_{a \geq 0} \; &\bm{\pi}'(s)a \\
    \text{s.t.} \;\: &{\tilde{\gamma}}(\|\bm{\pi}'(s)\|a) \leq d_{\mathrm{o}}(\bm{\pi}(s)) \\
    &\|\bm{\pi}'(s)\|a \leq \bar{v},
\end{align}$$ where $\bar{v}$ denotes the maximum executable velocity of the robot. Unlike path planning, velocity scheduling is not directly affected by $\delta$, as [\[eq:velocity_scheduling_distance\]](#eq:velocity_scheduling_distance){reference-type="eqref" reference="eq:velocity_scheduling_distance"} is solved only for poses on the path already determined based on $\delta$. We discretize the range of $s\in[0,1]$ into $l$ steps and use a line-search to efficiently compute [\[eq:ds_limit\]](#eq:ds_limit){reference-type="eqref" reference="eq:ds_limit"} at the discretization points. Finally, numerical integration of the obtained velocity profile yields a smooth $\delta$-safe trajectory $\bm{\pi}^*(t)$ [@Bobrow1985].

# Evaluation

We evaluate the visual perception and motion planning modules separately and deploy the proposed framework for a real-world task. First, we examine the effect of data augmentation and ensembling in [5.1](#subsec:eval_aug){reference-type="ref+label" reference="subsec:eval_aug"}. As a segmentation model, we employ the DeepLabv3 architecture [@Chen17] with the ResNet50 CNN [@He16] as the backbone. In [5.2](#subsec:eval_plan){reference-type="ref+label" reference="subsec:eval_plan"}, we show the high flexibility of the proposed scenario formulation for planning in uncertain environments. Finally, in [5.3](#subsec:exp){reference-type="ref+label" reference="subsec:exp"}, the effectiveness of the safe vision-based motion planning framework is demonstrated in an experiment with a 7 DOF robotic manipulator and a hand as obstacle.

## Uncertainty Quantification in Visual Perception {#subsec:eval_aug}

:::: {#fig:dataset .figure}
:::: {#subfig:trainingset .figure}
![image](Rmer2022VisionBased_figs/training_imgs.jpg){width="\\textwidth"}\

::: caption
50 Training images
:::
::::

:::: {#subfig:testset .figure}
![image](Rmer2022VisionBased_figs/test_imgs.jpg){width="\\textwidth"}\

::: caption
50 Test images
:::
::::

::: caption
We split our available annotated samples into a training and a test set. The former contains only little variety and is thus not representative for the test set, making the training task a good example for [1](#prob1){reference-type="ref+label" reference="prob1"}.
:::
::::

In accordance with [1](#prob1){reference-type="ref+label" reference="prob1"}, we aim to evaluate our uncertainty-aware visual perception approach for a small dataset with low variety containing images of complex-shaped objects. To this end, we consider highly accurate semantic segmentation of human hands and create our own dataset for this task[^6]. Since the labelling procedure is time consuming, only 100 images are created and divided equally into a training and a testing set as depicted in Figures [3](#subfig:trainingset){reference-type="ref" reference="subfig:trainingset"} and [4](#subfig:testset){reference-type="ref" reference="subfig:testset"}. It can clearly be seen that the training set is chosen such that it exhibits only limited diversity, e.g., all images have monotonous and very similar backgrounds. In contrast, the test set includes highly diverse images with hands from multiple people in various environments. Therefore, the training set is not representative of the test images, such that the resulting segmentation task is a good instance for [1](#prob1){reference-type="ref+label" reference="prob1"}, and thus well-suited to demonstrate the effectiveness of the proposed massive augmentation procedure in adding missing variability to a dataset.

::: {#tab:aug_methods_comb}
+--------------+--------------------------------------+-------------------------+---------------------------+
| Training set | Methods                              | PA $\pm$ $1$ std $[\%]$ | mIoU $\pm$ $1$ std $[\%]$ |
+:============:+:====================================:+:=======================:+:=========================:+
| 200 images   | Cutout [@Devries2017]                | $88.2 \pm 0.9$          | $78.7 \pm 1.4$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Mixup [@Zhang2018]                   | $89.4 \pm 1.4$          | $78.3 \pm 2.0$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Flip. + $90^\circ$ Rot. [@Nanni2021] | $88.5 \pm 1.0$          | $79.4 \pm 1.5$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Flip. + Rot. + Crop. [@Uzun2021]     | $86.9 \pm 1.3$          | $76.7 \pm 1.9$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Our scheme                           | $\bm{95.4 \pm 0.7}$     | $\bm{89.1 \pm 1.4}$       |
+--------------+--------------------------------------+-------------------------+---------------------------+
| 1000 images  | Cutout [@Devries2017]                | $91.7 \pm 0.6$          | $83.6 \pm 0.8$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Mixup [@Zhang2018]                   | $88.1 \pm 0.8$          | $77.1 \pm 1.1$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Flip. + $90^\circ$ Rot. [@Nanni2021] | $88.2 \pm 1.0$          | $78.1 \pm 1.4$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Flip. + Rot. + Crop. [@Uzun2021]     | $89.2 \pm 1.1$          | $79.7 \pm 1.7$            |
|              +--------------------------------------+-------------------------+---------------------------+
|              | Our scheme                           | $\bm{96.2 \pm 0.8}$     | $\bm{91.0 \pm 1.6}$       |
+--------------+--------------------------------------+-------------------------+---------------------------+
:::

[]{#tab:aug_methods_comb label="tab:aug_methods_comb"}

::: {#tab:bs_nll_app}
+--------------+--------------------------------------+-------------------+------------------+
| Training set | Methods                              | NLL $\times 10^2$ | BS $\times 10^3$ |
+:============:+:====================================:+:=================:+:================:+
| 200 images   | Cutout [@Devries2017]                | $88.1$            | $41.8$           |
|              +--------------------------------------+-------------------+------------------+
|              | Mixup [@Zhang2018]                   | $68.3$            | $25.0$           |
|              +--------------------------------------+-------------------+------------------+
|              | Flip. + $90^\circ$ Rot. [@Nanni2021] | $91.7$            | $47.5$           |
|              +--------------------------------------+-------------------+------------------+
|              | Flip. + Rot. + Crop. [@Uzun2021]     | $97.4$            | $41.2$           |
|              +--------------------------------------+-------------------+------------------+
|              | Our scheme                           | $\bm{25.4}$       | $\bm{10.5}$      |
+--------------+--------------------------------------+-------------------+------------------+
| 1000 images  | Cutout [@Devries2017]                | $63.1$            | $32.3$           |
|              +--------------------------------------+-------------------+------------------+
|              | Mixup [@Zhang2018]                   | $87.1$            | $36.9$           |
|              +--------------------------------------+-------------------+------------------+
|              | Flip. + $90^\circ$ Rot. [@Nanni2021] | $84.1$            | $47.0$           |
|              +--------------------------------------+-------------------+------------------+
|              | Flip. + Rot. + Crop. [@Uzun2021]     | $80.2$            | $39.4$           |
|              +--------------------------------------+-------------------+------------------+
|              | Our scheme                           | $\bm{23.4}$       | $\bm{11.4}$      |
+--------------+--------------------------------------+-------------------+------------------+
:::

[]{#tab:bs_nll_app label="tab:bs_nll_app"}

We evaluate the combination of the data augmentation methods within our augmentation scheme. For this purpose, we apply our scheme and the methods proposed in [@Devries2017; @Zhang2018; @Uzun2021; @Nanni2021] to create two augmented datasets from the 50 training images: A small one containing 200 images and a large one containing 1000 images. In [1](#tab:aug_methods_comb){reference-type="ref+label" reference="tab:aug_methods_comb"}, the results for our scheme in terms of pixel accuracy (PA) and mean intersection-over-union (mIoU) [@Shelhamer17] are presented together with the results of the comparison methods. It can be seen that our scheme provides significantly stronger improvements in model performance for both degrees of dataset inflation. The best performance is achieved when the dataset is enlarged from 50 to 1000 images using our scheme, i.e., by a factor of 20, which is ten times the factor of two used in [@Uzun2021]. We also examine the impact of our data augmentation scheme on calibration and compare it to the approaches from [@Devries2017; @Zhang2018; @Uzun2021; @Nanni2021] for an inflated training set of 200 and 1000 images, respectively. To this end, we consider two common metrics, the Brier score (BS) and negative log-likelihood (NLL) [@Lakshminarayanan17]. As shown in Table [2](#tab:bs_nll_app){reference-type="ref" reference="tab:bs_nll_app"}, our augmentation scheme yields much better predictive uncertainty estimates than the comparison methods, including mixup, which is a popular method to improve calibration [@Zhang2018] . Our results show the importance of addressing the lacking variety within the training set through massive data augmentation combining different augmentation methods.

::: {#tab:bs_nll}
           M            1      2      3      4      5      6      7      8      9      10
  ------------------- ------ ------ ------ ------ ------ ------ ------ ------ ------ ------
   BS $\times 10^3$    30.8   29.7   28.1   26.9   25.1   24.3   23.9   23.3   23.6   23.4
   NLL $\times 10^2$   18.0   16.1   13.9   13.0   12.3   12.1   11.9   11.7   11.4   11.4
:::

[]{#tab:bs_nll label="tab:bs_nll"}

::: {#fig:reliability_curve .figure}
:::

Our safe planning framework builds on the assumption that for each pixel, the segmentation output can be used as an occupancy probability. To justify this assumption, we first examine calibration via the reliability diagram . For this, the confidence interval $[0.5, 1)$ is partitioned into ten equally sized bins. For each bin, the pixel accuracy is calculated and plotted against the average confidence value of the pixels within the bin. We evaluate three differently sized ensembles, $M\in\{2,5,10\}$, and the individual members of the medium-sized ensemble, which are trained with our augmented training dataset. The results depicted in Figure [6](#fig:reliability_curve){reference-type="ref" reference="fig:reliability_curve"} show that calibration improves with increasing ensemble size. Moreover, as shown in [3](#tab:bs_nll){reference-type="ref+label" reference="tab:bs_nll"}, BS and NLL significantly decrease with increasing ensemble size, which is consistent with the results reported in [@Lakshminarayanan17]. The reliability curve as well as BS and NLL indicate only small improvements for $M > 5$. Therefore, we conclude an ensemble size of $M = 5$ to maintain a good balance between computational demand and calibration suitable for the considered visual perception task.

## Uncertainty Representations for Collision Avoidance {#subsec:eval_plan}

We compare the performance of path planning with our perception-based collision avoidance with three popular methods [@Zhu2019; @Park2018; @Kamel2017] that are based on the common assumption of uncertain position $\bm{x}_\mathrm{o} \sim \mathcal{N}(\hat{\bm{x}}_\mathrm{o}, \sigma^2\bm{I}_3)$, and known geometry and orientation of the obstacles. We consider a 4D task space $\mathcal{T}$ composed of the robot position $\bm{x}\in \mathcal{W}\subset \mathbb{R}^3$ and its orientation $\phi$ around the vertical $z$-axis. The set $\mathcal{R}(\bm{p})$ is described as an ellipse parallel to the $x$-$y$-plane, we set $\underline{v}=0.01\, \nicefrac{\si{m}}{\si{s}}$, $\bar{v}=0.2\, \nicefrac{\si{m}}{\si{s}}$, ${{\tilde{\gamma}}(v)=v/\bar{v}\cdot 0.01\, \si{m}}$, and consider spheres and cuboids as obstacles. For applying our approach, we consider that the occupancy probability decreases linearly with the distance $d$ to the obstacle surface[^7], becoming zero at $d=d_\mathrm{stop}$. Since we employ the chance constraint with probability $\delta=0.05$, this leads to $\tilde{d}=0.95d_{\mathrm{stop}}$ representing the extended boundaries of the uncertain object. Due to the Gaussian distribution of the object positions, these boundaries are equivalently parameterized using $2\sigma$ in the existing approaches [@Zhu2019; @Park2018; @Kamel2017]. For comparing the different methods, we create a simple scene containing three large obstacles and a more cluttered scenario with eight small obstacles. For solving [\[eq:path_plan_problem\]](#eq:path_plan_problem){reference-type="eqref" reference="eq:path_plan_problem"}, we employ the SSC-RRT\* algorithm proposed in [4.2](#subsec:rrt){reference-type="ref+label" reference="subsec:rrt"}. The number of search tree iterations is set to $N_{\mathrm{iter}}=2000$. We aim for a path that is short in Cartesian space and also avoids unnecessary rotations. To this end, we define the line cost function for a line segment $[\bm{p}, \bm{p}']\subset \mathcal{T}$ between two poses $\bm{p} = \big[\bm{x}^\mathsf{T}, \phi\big]^\mathsf{T}$, $\bm{p}' = \big[{\bm{x}'}^\mathsf{T}, \phi'\big]^\mathsf{T}$ in the task space as $$\begin{align}
    \label{eq:eval_cost_fct}
    c_\mathrm{l}(\bm{p}, \bm{p}') = \|\bm{x}-\bm{x}'\|^2 + r(\phi - \phi')^2,
\end{align}$$ where $r>0$ determines the penalty for orientation changes.

::: {#fig:planning_comp .figure}
:::

We run the SCC-RRT\* algorithm using this cost function and $N_x=100$ for $100$ times per method and scene over a range of different values of $\tilde{d}$ and $2\sigma$, which represent different uncertainty levels in the perception. The resulting normalized average costs are illustrated in [7](#fig:planning_comp){reference-type="ref+label" reference="fig:planning_comp"}. While the behavior of the cost for the simple scenario is almost identical for our method and the approach proposed in [@Zhu2019], the cost achieved using the existing methods [@Zhu2019; @Park2018; @Kamel2017] increases significantly faster in the cluttered environment. The proposed SCC-RRT\* algorithm achieves this slower deterioration of the planning performance through the sampling-based obstacle representation, which ensures that our approach does not directly depend on the number of obstacles. This is in contrast to parametric obstacle representations in existing methods [@Zhu2019; @Park2018; @Kamel2017], where the conservatism of the uncertainty approximations for the individual obstacles accumulates, such that the path performance crucially suffers from growing uncertainties as measured by $\sigma$.

Additionally, we compare the computational efficiency of the proposed scenario approach with existing parametric approaches. For this, we create scenes with different numbers of randomly placed spherical obstacles. The average computation times for running the RRT\* algorithm 100 times with the collision checking methods [@Zhu2019; @Park2018; @Kamel2017] are recorded and shown in [8](#fig:computation_times){reference-type="ref+label" reference="fig:computation_times"}. For comparison, we also include the average computation time of our sampling-based approach for different values of $N_x$. The parametric methods exhibit a significant increase in computation time with the number of obstacles, which must all be checked for collision. The SCC-RRT\* algorithm does not suffer from this issue as it exploits a joint environment representation that is only sampled at test points instead of individual object representations. Thus, the proposed scenario approach simultaneously achieves flexibility and efficiency and is applicable to highly cluttered environments containing many obstacles.

::: {#fig:computation_times .figure}
:::

## Experimental Evaluation with a KUKA iiwa robot {#subsec:exp}

::: {#fig:experiment .figure}
![image](Rmer2022VisionBased_figs/experiment_planned.JPG){width="40%"} ![image](Rmer2022VisionBased_figs/experiment_executed.JPG){width="40%"} []{#fig:experiment label="fig:experiment"}
:::

::: {#fig:experiment_scenes .figure latex-placement="t"}
![image](Rmer2022VisionBased_figs/experiment_scenes.jpg){width="\\linewidth"} []{#fig:experiment_scenes label="fig:experiment_scenes"}
:::

In order to show the real-world applicability of our approach, we conduct an experiment with an impedance controlled KUKA iiwa robotic manipulator with seven degrees of freedom and a hand as obstacle[^8]. A Logitech C270 USB webcam positioned 0.5 m above the working area takes images of the workspace. We apply the deep ensemble trained as discussed in [5.1](#subsec:eval_aug){reference-type="ref+label" reference="subsec:eval_aug"} and augment the 2D probabilistic semantic segmentation result to 3D by assuming fixed hand height. We use the same expression for $\underline{v}$, $\bar{v}$ and $\mathcal{R}(\bm{p})$ as in Section [5.2](#subsec:eval_plan){reference-type="ref" reference="subsec:eval_plan"} and plan a $\delta$-safe path with the SCC-RRT\* algorithm with $N_\mathrm{iter}=2000$. From tracking experiments with the manipulator, we obtain an approximate tracking error bound ${{\tilde{\gamma}}(v)=v/\bar{v}\cdot 0.01\, \si{m}}$. This procedure requires test trajectories that cover a sufficiently wide range of operating conditions, which can be challenging for higher-dimensional task spaces. To obtain a motion in close proximity to the fingers, we replace the first term in the cost function [\[eq:eval_cost_fct\]](#eq:eval_cost_fct){reference-type="eqref" reference="eq:eval_cost_fct"} with a term that penalizes the area between the path and the table. The motion is executed with a maximum velocity $\bar{v}=0.2\, \nicefrac{\text{m}}{\text{s}}$, see Figure [9](#fig:experiment){reference-type="ref" reference="fig:experiment"}. As shown in Figure [10](#fig:experiment_scenes){reference-type="ref" reference="fig:experiment_scenes"} and in our supplementary video , the experiment is successfully repeated with different individuals, varying lighting conditions and backgrounds, which demonstrates the practicability and robustness of our safe perception-based planning framework. In some situations, parts of the hand are detected by only a subset of the semantic segmentation models, showing the particularly strong impact of ensembling on safety.

# Conclusion

In this letter, we present a framework for vision-based motion planning with uncertainty using semantic image segmentation. We show that combining massive data augmentation and deep ensembles yields good uncertainty quantification for semantic segmentation even for highly specific tasks lacking representative training data. This allows us to interpret the output of the semantic segmentation probabilistically and use it for motion planning with uncertainty. We avoid the conservatism of existing uncertainty-aware path planning approaches by employing a sampling-based method for collision checking that is based on scenario optimization. As a result, our planning method makes no assumptions about the obstacle geometry and can be applied in highly cluttered environments. Our framework is evaluated in simulation and experiment with a robotic manipulator. Directions for future work include using smaller semantic segmentation models, extending our method to estimate obstacle dynamics and enabling adaptive online planning based on a scenario MPC approach, so that it can be safely employed in dynamic environments.

[^1]: Manuscript received: April, 29, 2023; Revised July, 26, 2023; Accepted September, 26, 2023.

[^2]: This paper was recommended for publication by Editor J. Kober upon evaluation of the Associate Editor and Reviewers' comments. This work was supported by the European Research Council (ERC) Consolidator Grant "Safe data-driven control for human-centric systems (CO-MAN)" under grant agreement number 864686, by the Horizon 2020 research and innovation programme of the European Union under grant agreement number 871767 of the project ReHyb, and by TUM AGENDA 2030, funded by the Federal Ministry of Education and Research (BMBF) and the Free State of Bavaria under the Excellence Strategy of the Federal Government and the Länder as well as by the Hightech Agenda Bavaria.

[^3]: The authors are with the TUM School of Computation, Information and Technology, Technical University of Munich, 80333 Munich, Germany. Ralf Römer is with the Learning Systems and Robotics Lab (LSY). Armin Lederer, Samuel Tesfazgi, and Sandra Hirche are with the Chair of Information-Oriented Control (ITR). `{ralf.roemer; armin.lederer; samuel.tesfazgi; hirche}@tum.de`

[^4]: $^*$ Both authors contributed equally.

[^5]: Digital Object Identifier (DOI): see top of this page.

[^6]: The images in the dataset show only hands of co-authors, who consented to the usage and publication.

[^7]: We could just as well assume other profiles for the probabilistic segmentation around the object boundaries. However, many predictions we obtain when perceiving real objects show a roughly linear decrease.

[^8]: Approval for this type of experiments involving the close interaction between a Kuka iiwa manipulator and a human has been obtained by the ethics committee of the medical faculty of the Technical University of Munich.
