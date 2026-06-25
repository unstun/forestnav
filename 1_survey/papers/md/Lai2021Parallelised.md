---
citation_key: Lai2021Parallelised
arxiv_id: 2108.11775
arxiv_url: https://arxiv.org/abs/2108.11775
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:38:35Z
origin: ai+web
reviewed: false
---

# Introduction

This paper addresses the problem of motion planning, and bridges together two motion planning paradigms: *trajectory optimisation approaches* and *sampling-based approaches*. Trajectory optimisation views robot trajectories as solutions of an optimisation problem. The optimisation problem typically incorporates the environment occupancy, along with additionally specified requirements into a cost function. Gradients of the cost function are often assumed to be accessible, allowing for its efficient optimisation. However, trajectory optimisation approaches are known to suffer from local minima, and are generally not *anytime*. On the other hand, sampling-based planners have a complementary set of benefits. Sampling-based planners are probabilistically complete, and are able to quickly find a feasible solution and improve upon it. However, unlike trajectory optimisation approaches, sampling-based planners are unable to utilise gradient information, either from environment occupancy or from user specification.

We propose a novel motion planning framework, Parallelised Diffeomorphic Sampling-based Motion Planning (PDMP), which combines the benefits of both sampling-based and trajectory optimisation methods. PDMP is capable of finding globally optimal solutions, while benefiting from gradient information of cost functions to speed up motion planning. In broad strokes, our method leverages gradient information from specified cost functions, which can be learned from environment data or user specified, to construct differentiable bijections, or *diffeomophisms*. Like normalising flows, PDMP uses diffeomorphisms to shape a simple base sampling distribution into a sampling distribution that is more informative. However, to learn invertible transformations for normalising flows, one typically assumes that samples from a desired target distribution are accessible. This is typically not the case when learning sampling distributions: generally, we are given information about the occupancy in the environment, as well as designed costs, rather than samples from a "good" sampling distribution. We demonstrate that with relatively mild assumptions, we can obtain diffeomorphisms, from provided cost functions, that allows us to deform the sampling distribution. We provide a specific example of learning a diffeomorphism that conforms to environment occupancy.

The "morphing" of sampling distributions allows sampling-based planners, such as Rapidly-exploring Random Trees (RRTs) and its variants, to more efficiently create connections, speeding-up the planning process. Additionally, the transformation of the sampling distribution can be viewed as a parallel process, while building the expanding trees is an inherently sequential process. We integrate CPU and GPU parallelism: we use GPUs to shape the sampling distribution, which can be processed in parallel, while simultaneously using the CPU to build the expanding tree, which is a sequential process.

Concretely, our contributions are as follows: (1) We propose a method of shaping sampling distributions of sampling-based planners, such that gradient information, for example from environment occupancy gradient or user specified information can be incorporated, allowing for faster motion planning; (2) We provide an efficient implementation of our method integrated into an RRT motion-planner which leverages the parallel capabilities of GPUs. We demonstrate that the shaping of the sampling distribution can be done efficiently in parallel in a GPU, simultaneously with the sequential tree-building process resulting in no additional time cost.

We empirically evaluate PDMP on challenging planning scenarios, and find that it is able to consistently find solutions faster than existing sampling-based motion planners.

# Related Works

**Sampling-based Motion Planning:** Sampling-based planners are a class of predominant methods to compute motion trajectories for robots. They pose the motion planning problem in a probabilistic setting, where the construction of motion plans are formulated as a graph or tree building procedure. PRM [@kavraki1996_ProbRoad] was first proposed to creates a random roadmap of connectivity in the configuration space to avoid the curse of dimensionality. On the other hand, tree-based RRT [@lavalle1998_RapiRand] follows a similar idea but uses tree structures to obtaining solution quicker, which inspire a whole new class of motion planning methods [@lai2018_BalaGlob; @bry2011_RapiRand; @lee2012_SRRRSele; @lai2021_RRF]. Since sampling is one of the core component in sampling-based motion planners, there are a lot of methods that tries to improve the sampling distribution. For example, formulating a restricted distribution to improve planning time [@gammell2018_InfoSamp; @lai2020_BayeLoca]. There are also method to learn the sampling distribution from experience using neural network methods [@lai2020_LearPlan; @ichter2018_LearSamp; @sartoretti2019_PRIMPath]. However, most learning-based methods learns a skewed distribution based purely from a subset of successful motion plans configurations, which requires a mixture with uniform distribution to maintain the *probabilistic completeness* guarantee [@elbanhawi2014_SampRobo].

**Gradient-based Cost Optimisation in Motion Planning:** Outside of sampling-based motion planner, many other paradigms of motion planning make use of gradient information of some defined cost function. Trajectory optimisation approaches, such as CHOMP [@ratliff2009_CHOMGrad], STOMP[@kalakrishnan2011_STOMStoc] and TrajOpt [@schulman2014_MotiPlan], and potential field approaches [@hwang1992_PoteFiel] are prominent examples of this. These approaches find a single solution by descending in the direction of lower cost, guided by the negative gradient. Likewise, our approach transform a distribution such that samples have lower cost by descending based on negative gradients.

**Diffeomorphisms and Normalising Flows:** The transforming of distributions via invertible and differentiable mappings is known as *normalising flows* [@rezende2015_VariInfe]. These invertible and differentiable mappings are known as "flows" [@rezende2015_VariInfe] or more generally as "diffeomorphisms" [@flowsJMLR; @Lee2002IntroductionTS]. Normalising flows are typically learned using invertible structures [@ardizzone2019analyzing; @NEURIPS2019_7ac71d43], with data drawn from the desired target distribution. We take a different approach, and develop invertible mappings from cost gradients, which can be hand specified or learned from other sources of data, such as occupancy information (outlined in [3](#Continuous_map){reference-type="ref+label" reference="Continuous_map"}).

# Parallelised Diffeomorphic Sampling-based Motion Planning {#Continuous_map}

We shall detail the proposed Parallelised Diffeomorphic Sampling-based Motion Planning (PDMP) framework. In [3.1](#learningRep){reference-type="ref+label" reference="learningRep"}, we begin by introducing neural network representations of occupancy, which allows for fast batched querying of coordinates via the GPU. This occupancy representation will be used to construct diffeomorphisms which transforms a sampling distribution, such that samples have lower likelihood of being in occupied space. Details on constructing this diffeomorphism, along with those from an arbitrary cost function, are elaborated in [3.2](#Cost_inf){reference-type="ref+label" reference="Cost_inf"}. Finally, in [3.3](#parallel){reference-type="ref+label" reference="parallel"}, we expand on how we can leverage both the GPU, for the highly parallelisable transformation of samples, and the CPU, for the inherently sequential tree-building process, to achieve improved performance with the same time budget, for tree-building sampling-based motion planning methods.

## Learning Continuous Occupancy Representations with Neural Networks {#learningRep}

::: wrapfigure
R0.24

::: figure
![image](Lai2021Parallelised_figs/occuppied.png){width="\\linewidth"} ![image](Lai2021Parallelised_figs/close_rw.png){width="\\linewidth"}
:::

![](Lai2021Parallelised_figs/occmap_color-bar.png){width="\\linewidth"}
:::

Occupancy in an environment have traditionally been represented by occupancy grid maps, which discretise the world into grid-cells and compute occupancy independently for each cell. Recent advancements in machine learning have brought continuous analogues of occupancy maps [@HilbertMaps], and continuous distance-based methods [@Park2019DeepSDFLC]. Here we present a straightforward approach of learning the occupancy via a neural network, which is fast to query, fast to obtain derivatives with respect to inputs, and inherently parallelised. These properties are beneficial for querying of large batches of coordinates.

We are assumed to have a dataset of $n$ pairs, containing coordinates and a binary value, which indicates whether the coordinate is occupied, i.e. $\mathcal{D}=\{(\mathbf{x}_{i},y_{i})\}_{i=1}^{n}$, where $y_{i}\in\{0,1\}$ for $i=1,\ldots,n$. A dataset of this format can be obtained from depth sensors. Our aim is now to learn a mapping $f_{map}$ between a coordinate of interest $\mathbf{x}$ and the probability of being occupied at $\mathbf{x}$, $f_{map}(\mathbf{x})=p(\mathbf{y}=1\vert\mathbf{x})$. We shall model $f_{map}$ as a fully-connected neural network, with $tanh$ activation functions between hidden layers, and a $sigmoid$ activation layer at the output. The resulting setup is a binary classification problem, which can be learned via a binary cross entropy loss with gradient descent optimisers. Derivatives of the neural network can be obtained efficiently, via batched computation on a GPU.

## Cost-informed Diffeomorphisms for Sampling Distributions {#Cost_inf}

In this section we elaborate on building differentiable bijections, or diffeomorphisms, to transform a base distribution such that the "morphed" target distribution density is concentrated at where a provided cost function is low. That is, samples from the target distribution are more likely than the base distribution to be sampled from regions with low cost. Diffeomorphisms ensure that the transformed sampling distribution will have the same topology as the base distribution. For example, if the base distribution has infinite support, then the transformed sampling distribution also has infinite support, and will not have "holes" where there is no probability density.

**Constructing Diffeomorphisms via integral curves:** Diffeomorphisms can be generated by taking integral curves on the vector field defined by the negative gradients of the cost function. We consider an $n$-dimensional state vector $\mathbf{y}\in\mathbb{R}^{n}$ to be an initial time, provided a cost $f_{c}:\mathbb{R}^{n}\rightarrow\mathbb{R}$, an integral curve for some time $t\in\mathbb{R}$, can be written as an initial value problem (IVP): $$\begin{align}
    \phi(\mathbf{y}):=\mathbf{y}-\int_{0}^{t}\nabla_{\mathbf{y}(s)}f_{c}(\mathbf{y}(s))\mathrm{d}s=\mathbf{z}, && \mathbf{y}(0)=\mathbf{y}, \label{diffeo}
\end{align}$$ where $\mathbf{z}\in\mathbb{R}^{n}$ results from the Picard--Lindelöf theorem [@Coddington1955TheoryOO] (existence and uniqueness of IVPs), which states that if $\nabla_{\mathbf{y}(s)}f_{c}$ is Lipschitz continuous with respect to $\mathbf{y}(s)$, then the solution of the IVP exists and is unique. We shall restrict our discussion to cost functions with Lipschitz derivatives, this includes the continuous occupancy representations introduced in [3.1](#learningRep){reference-type="ref+label" reference="learningRep"}. Then, $\phi(\mathbf{y})$ is a diffeomorphism, and the inverse is given by: $$\begin{align}
    \phi^{-1}(\mathbf{z}):=\mathbf{z}+\int_{0}^{t}\nabla_{\mathbf{z}(s)}f_{c}(\mathbf{z}(s))\mathrm{d}\mathbf{s}=\mathbf{y}, && \mathbf{z}(0)=\mathbf{z}.
\end{align}$$ Therefore, we can use numerical integration techniques, such as Euler's method, to solve the IVP to evaluate the diffeomorphism efficiently.

**Bringing Diffeomorphisms into Configuration Space:** Motion-planning in robotics typically requires plans to be made in the *configuration space* (C-space) of the robot. On the other hand, costs to shape robot behaviour can be, and is often, defined in the Cartesian task space. For example, collision checking requires information about the task space geometry of the robot to determine whether it overlaps with objects in the environment. We assume that the sampling distribution is defined in the C-space of the robot, and diffeomorphisms need to operate in the C-space. We shall in particular discuss robot manipulators, where the states in the C-space are joint angles. We denote the C-space as $\mathcal{Q}\in\mathbb{R}^{n}$, where there are $n$ joints. Joint configurations, $\mathbf{q}\in\mathcal{Q}$, are elements of the C-space, while Cartesian coordinates in task space are denoted as $\mathbf{x}\in\mathbb{R}^{3}$. We outline how to *pull* a cost gradient defined in the task space to the C-space, and construct a diffeomorphism there.

We start by defining $b$ body points on the robot, each with a forward kinematics function mapping configurations to the Cartesian coordinates at the body point, $\psi_{i}:\mathcal{Q}\rightarrow\mathbb{R}^{3}$, for each $i=1,\ldots,b$. This allows us to make use of the Jacobian of the forward kinematics functions with respect to the joint configurations. The Jacobian of the $i^{th}$ kinematics function is denoted as $J_{\psi}^{i}(\cdot)=\frac{\mathrm{d}\psi_{i}}{\mathrm{d}\mathbf{q}}(\cdot)$. A cost potential $f_{c}$ which operates on the body points, such as the occupancy cost potential discussed above, can be *pulled* into the C-space: $$\begin{equation}
    \nabla_{\mathbf{q}}f_{c}=\sum_{i=1}^{b}J_{\psi}^{i}(\mathbf{q})\nabla_{\mathbf{x}}f_{c},
\end{equation}$$ we can then define a diffeomorphism, via solving the IVP as in [\[diffeo\]](#diffeo){reference-type="ref+label" reference="diffeo"}, in the C-space of the robot.

**Drawing Samples from the Morphed Target Distribution:** We can draw samples from the morphed distribution by drawing samples from the known base distribution, then passing the points through the diffeomorphism $\phi$. Unlike normalising flows for density estimation, which are computationally burdened by having to compute the determinant of the Jacobian of $\phi$, we only require the mapping of sampled points, which can be done efficiently, and does not require the Jacobian of $\phi$. Furthermore, we note that morphing the sampled points from the base distribution to the transformed distribution can be done in parallel if the cost gradients can be parallelised. In particular, occupancy gradients as introduced in [3.1](#learningRep){reference-type="ref+label" reference="learningRep"} can be batch computed on a GPU efficiently. In the following sections, we shall elaborate on how to exploit the parallel nature of the morphing sampled points.

## Parallelised Diffeomorphic Transform of Sampling Distribution {#parallel}

Rapidly-exploring random trees (RRTs), its variants, along with its graph-based counter parts are some of the most widely-used motion planning algorithms. In this section, we develop the Parallelised Diffeomorphic Sampling-based Motion Planning (PDMP) algorithm to transform the sampling distribution while constructing trees, efficiently integrating CPU and GPU parallelism. We elaborate on the *diffeomorphic sampler*, which can be largely parallelised, and the *motion planner main thread*, which consists of sequential operations. An overview flow-diagram is shown in [\[rrt_building\]](#rrt_building){reference-type="ref+label" reference="rrt_building"}.

**Motion Planner Main Thread** Building random trees is inherently a sequential process -- sampling a random configuration, searching for nearest neighbour in the k-d tree, collision-checking of potential tree edges, connecting the candidate node , and rewiring of other existing nodes. This process requires knowledge of nodes that are currently connected by the tree, and valid nodes are connected to the tree as soon as they are found. Such a sequential process is repeated within a loop until the time budget exhausted. We will denote this sequential process as the *Motion Planner* because most of the works are to be done within the same thread. Similar to existing methods, we conduct the tree-building on the CPU. However, we proceed with optimising the sampled points in background threads that are parallelised in GPUs.

When the planning request is first received, the *main thread* spawns a background *boostrap thread* that prepares all necessary house keeping works such as constructing a concurrent queue $S$. Then, the *main thread* will proceed with the rest of the typical tree-building procedures, following the traditional RRT-variant literature. The main modification in this sequenital process lies in the sampling step. Typically, RRT samples from some distribution (e.g. uniform distribution $q_\text{rand}\sim\mathcal{U}(0,1)$) within the same thread. Instead, in our PDMP framework we draw samples from the previously constructed concurrent queue $S$, which is one of the only communication contacts in between the *main thread* and the *diffeomorphic sampler thread*, to avoid any other synchronisation overhead (the other communication happens when the *main thread* requests the background *diffeomorphic sampler* to exits due to time budget being exhausted). This concurrent bucket is filled by our *diffeomorphic sampler thread*. In the event the planner attempts to draw from an empty bucket, sample points are immediately drawn from a simple prior distribution $\mathbf{q}\sim\mathcal{Q}_{prior}$, reverting back to a standard sampling-based planner. Therefore, the main thread does not need to do a blocking-wait on the background thread; which implies that, in the rare event of degraded GPUs performance, PDMP will only be reverting back to the typical planner performance.

::: shapedFig
![image](Lai2021Parallelised_figs/flow-diagram5.png){width="\\textwidth"} Flow diagram of the parallelised operations in PDMP.[]{#rrt_building label="rrt_building"} **Diffeomorphic Sampler** The diffeomorphic sampler leverages parallelism on the GPU to provide more informed samples. When the *bootstrap thread* is created, it first spawns multiple background threads that are equal to the target computer's parallelisation power (e.g. the number of CPUs or hyper-threads). Each background thread is in-charge of generating sample points from the morphed distribution in a mini-batch fashion. In contrast to CPUs, we can use the GPU to sample a large batch from a prior distribution. These backgroud threads within *diffeomorphic sampler* in [\[rrt_building\]](#rrt_building){reference-type="ref+label" reference="rrt_building"} will also collect the necessary kinematic Jacobians into batches for forward pass in the GPUs. The batch of samples is then passed through the diffeomorphism to obtain the informed samples. The pass through the diffeomoprhism can be done efficiently when leveraging the parallel computing capabilities of the GPUs, if the gradients of the cost potential can be done in batch. This is often the case if the cost gradients can be expressed analytically. This is particularly the case, if given by the derivative of a neural network.
:::

## Probabilistic Completeness

We shall demonstrate that drawing sample points from the transformed distribution maintains the probabilistic-completeness of the popular RRT-based sampling-based method.

We shall begin by considering the support of the prior distribution and the transformed distribution. Let $P_y$ be the prior probability measure on space $Y$, with the diffeomorphism $F:Y\rightarrow Z$. Let $P_z(\mathbf{z}):=P_y(F^{-1}(\mathbf{z}))$, with $\mathbf{z}\in Z$

::: definition
**Definition 1** (Support of probability measure). *Let $P_{y}$ be a measure on a topological space Y, then the support of $P_{y}$ is the set, $suppP_{y}:=\{\mathbf{y}\in Y\lvert P_y(\mathbf{y})>0\}$,*
:::

Intuitively, the support of a probability distribution is the set of possible values of a random variable having non-zeros probability density. We shall study how the support of the prior and the transformed distribution change depending on $F$. In particular we consider when the support of the prior and transformed distributions are equal.

::: {#supportLemme .lemma}
**Lemma 1** ([@Cornish2020RelaxingBC] Equation 4). *The support of the prior and transformed probability measure are equal, i.e. $suppP_{y}=suppP_{z}$, if $Y$ and $Z$ are *homeomorphic* i.e., isomorphic as topological spaces.*
:::

As $F:Y\rightarrow Z$ is a *diffeomorphism*, that is a differentiable homeomophism, $suppP_{y}=suppP_{z}$.

::: theorem
**Theorem 1** (Probabilistic Completeness). *If a RRT-algorithm, drawing samples from random variable $\mathbf{y}$, is probabilistic complete, then the RRT-algorithm drawing samples from $f(\mathbf{y})$, where $f$ is a diffeomorphism, is also probabilistic complete.*
:::

::: proof
*Proof.* As random variables $\mathbf{y}$ and $f(\mathbf{y})$ are linked by diffeomorphism $f$, by [1](#supportLemme){reference-type="ref+label" reference="supportLemme"}, they have the same support. Clearly, as the sampling time $t\rightarrow +\infty$, the set of created vertices with the sampling distribution $\mathbf{y}$, $V(\mathbf{y})$, and set of created vertices with the sampling distribution $f(\mathbf{y})$, $V(f(\mathbf{y}))$, are equal. Then by Theorem 23 from [@Karaman], the probabilistic completeness follows directly from the probabilistic completeness of RRT with sampling distribution $\mathbf{y}$. ◻
:::

We shall note that the above theorem proves that, for samples that are drawn from the morphed distribution, there are non-zero probability regions that they will cover *everywhere* in the space. However, certain parts of the space can be stretched arbitrarily thin such that it might reduce the quality of the planner (although still remaining complete). One can deploy a strategy such as sampling with epsilon-bias towards a uniform distribution to circumvent the possibility of a highly skewed distribution. The following experiments utilise a purely morphed distribution and do not employ such a strategy.

# Experimental Results

We empirically analyse our proposed Parallel Diffeomorphic Sampling-based Motion Planning (PDMP) method. In the following sections, we investigate the performance of finding valid motion plans, with gradients from a cost potential occupancy representations, under time constraints. For our simulated environments, we construct three challenging environments, as illustrated in [\[fig:sim-env\]](#fig:sim-env){reference-type="ref+label" reference="fig:sim-env"}. *Divider*: consists of a large divider on a cluttered table, planning to reach the other sides of the divider; *Cupboard*: consists of a cupboard where the arm move in-between different shelves; *Lab-setup*: where the arm pickup an object and place it at the bottom of a cluttered scene.

::: minipage
:::

::: minipage
![image](Lai2021Parallelised_figs/pct.png){width="\\linewidth"}
:::

## Qualitative Evaluation on Informed Distribution

We hypothesise that after morphing our sampling distribution with a cost potential from our continuous occupancy representation, we can significantly improve the performance of the sampling-based planning strategies. In [\[table:samp-dist-total-pts-and-feasible-pts\]](#table:samp-dist-total-pts-and-feasible-pts){reference-type="ref+label" reference="table:samp-dist-total-pts-and-feasible-pts"} we evaluate the effect of PDMP on the sampling distribution, both quantitatively and in terms of feasibility. The results for PDMP in [\[table:samp-dist-total-pts-and-feasible-pts\]](#table:samp-dist-total-pts-and-feasible-pts){reference-type="ref+label" reference="table:samp-dist-total-pts-and-feasible-pts"} are broken down into samples that are contributed by the original uninformed prior distribution (top half) and by the informed diffeomorphic distribution (bottom half). The are no relative differences between the original and PDMP distribution in *total samples*, this means that PDMP does not slow down the drawing of random samples. Instead, the morphed samples are more beneficial to the planning problem as they are more likely to be feasible in free space, as shown by the higher *total feasible* percentage in the PDMP section.

:::::: {#fig:real-robot .figure latex-placement="t"}
::: minipage
:::

::: minipage
![image](Lai2021Parallelised_figs/env1.png){width=".28\\linewidth"} ![image](Lai2021Parallelised_figs/env2.png){width=".28\\linewidth"} ![image](Lai2021Parallelised_figs/env3.png){width=".28\\linewidth"}
:::

::: caption
Sequence of trajectory in the real-world experiments with the Jaco arm: (Top) *Divider*; (Bottom) *Lab-setup*. []{#fig:real-robot label="fig:real-robot"}
:::
::::::

## Higher Success Rates with Informed Sampling Distributions

We examine our hypothesis by testing various sampling-based motion planners (SBPs) within our PDMP framework. We investigate three SBPs---RRT\* [@karaman2010_IncrSamp], RRT\*-connect [@Klemm2015], Lazy-PRM\* [@Bohlin2000], and a trajectory optimisation-based planner STOMP [@kalakrishnan2011_STOMStoc]. For the SBPs, we compare the effect of morphing the sampling distribution provided by our approach to standard uninformed sampling.

We provide a time-budget of 20 seconds for each planner, and calculate the percentage of tries, over 30 runs, that result in a successful plan at different times until the budget of 20s was entirely used. The results are illustrated in [2](#fig:success-rate){reference-type="ref+label" reference="fig:success-rate"}. We see that for each of the three sampling-based planning methods, incorporation within the PDMP framework to morph the sampling distribution improves the success rate. This is most evident when using RRTs within PDMP, since it allows us to produce more successful samples which in-turn speed up the tree-building process. We replicate the *divider* and *Lab-setup* environment ([1](#fig:real-robot){reference-type="ref+label" reference="fig:real-robot"}) in the real-world with a 6-DOF Jaco manipulator. The planning is illustrated by videos included in the supplementary materials.

[\[table:planners-result\]](#table:planners-result){reference-type="ref+Label" reference="table:planners-result"} illustrates numerical results of two important attributes in motion planning---the *time-to-solution* and the *success percentage*. Overall, PDMP allows each motion planners to utilise sampled configurations that are more likely to be feasible (see [\[table:samp-dist-total-pts-and-feasible-pts\]](#table:samp-dist-total-pts-and-feasible-pts){reference-type="ref+label" reference="table:samp-dist-total-pts-and-feasible-pts"}), which in turn allow PDMP planners to achieve shorter *time-to-solution* when compared to their original counterpart in [\[table:planners-result\]](#table:planners-result){reference-type="ref+label" reference="table:planners-result"}. Therefore, they are also more likely to successfully obtain a solution trajectory within the allocated time budget.

In the *divider* environment, we see that the success rate of PDMP-RRT\* reaches $80\%$ at around 7 seconds of planning, and almost has a perfect success rate by the end of the 20s budget. On the other hand, vanilla RRT\* with a uniform sampling distribution has a success rate of under $50\%$ when the time budget is used up. The same trends are observed with the other variants. Overall, the RRT\*-connect within PDMP and with a uniform sampling distribution outperforms the other variants. Even still, when using RRT-connect within the PDMP, we observe higher success rates when the planning time is low (under 3 seconds), indicating that PDMP significantly improves time-to-solution. The time-to-solution of STOMP tends to spread out among all three environments, which is likely due to its stochastic nature. The performance of STOMP does not seem to be degraded by the complexity of the environment, which suggests that the cost information was able to guide STOMP to obtain a solution trajectory. Our PDMP framework provides clear imporvements to the success rates of both RRT and RRT-connect methods. Additionally, we observe that at the end of the 20s time budget, PDMP variants outperform their counterparts which sample from an uninformed sampling distribution. Lastly, Lazy-PRM\* performs poorly on most environments as it is a multi-query planner, and was not able to obtain any valid solution in *Cupboard* within the allocated time budget.

## Influence of CPU-GPU Parallelisation

Our PDMP method parallelises over the CPU and GPU, by allocating the GPU to filling up a bucket for which samples are drawn, and dedicating the CPU to the planning process, which typically involves building a tree. If the bucket is empty when a sample is needed for the sequential planning process on the CPU, a sample is drawn from an uninformed prior distribution. Therefore, obtaining informed samples come at almost no additional cost: in the worst-case scenario, if the planning process faster than drawing samples from the morphed distribution, PDMP falls back to a vanilla sampling based algorithm, drawing samples from a uninformed distribution.

Intuitively, the more samples obtained from the bucket used in the planning process, the more informed our used samples are. We investigate the number of sample points drawn from the bucket, which are from the "morphed" distribution, and the percentage of samples from the uninformed prior as planning time progresses. This is shown in [\[fig:pct-of-morphed\]](#fig:pct-of-morphed){reference-type="ref+label" reference="fig:pct-of-morphed"}. We observe at the beginning, as the bucket has not yet been filled with samples from the morphed sampling distribution, samples from the uninformed prior are used. However, the GPU is able to quickly fill up the bucket with samples from the morphed distribution, and the number of uninformed samples beyond 0.2s is largely negligible. By 1 second of sampling time, the cumulative "morphed" sample points significantly exceeds the cumulative uninformed samples. This indicates that at any reasonable amount of planning time, the process of drawing samples from an informed distribution is much faster than the main planning process.

:::: {#fig:success-rate .figure latex-placement="t"}
![](Lai2021Parallelised_figs/success_rate.png){width="\\linewidth"}

::: caption
The success rate of the planning algorithm variants, over 30 runs. We observe that PDMP enables all flavours of sampling-based motion planning algorithms to have improved success rates, particularly at lower planning times.
:::
::::

# Conclusions

In this paper a novel method combining cost gradients from optimisation-based motion planning with probabilistic-complete sampling-base motion planning methods is proposed. Parallelised Diffeomorphic Sampling-based Motion Planning is a motion-planning framework which utilises *diffeomorphisms* generated from gradients of defined cost to morph the sampling distribution for sampling-based motion-planning methods. We demonstrate how such diffeomorphisms can be created from learned models of environment occupancy to encode obstacle avoidance behaviour, or user specified biases. Additionally, an implementation which parallelises this process across the GPU and CPU is provided, showing that sampling from the more informed distribution can be achieved at no additional run-time cost. We empirically demonstrate that our method is capable of significantly improving the success rate of finding solutions in challenging planning environments.
