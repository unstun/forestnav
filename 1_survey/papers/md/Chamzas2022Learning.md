---
citation_key: Chamzas2022Learning
arxiv_id: 2204.08550
arxiv_url: https://arxiv.org/abs/2204.08550
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:21:48Z
origin: ai+web
reviewed: false
---

# Introduction

Motion planning is used in real-time autonomous vehicles [@Kuwata2009], manipulators in dynamic environments [@Murray2016], and as a subroutine in planners for complex missions (e.g. task and motion planning [@Dantam2018]), all of which rely heavily on efficiency. However, motion planning is still challenging, especially for high-dimensional systems [@Canny1988]. Sampling-based planners [@kavraki1996; @Hsu1999; @LaValle2000] are a class of motion planning algorithms that have found widespread adoption in the planning community. Although significant progress has been made over the years, planning is still computationally expensive [@Salzman2019], hindering the adoption of robotic solutions. Thus, to endow robots with real-time capabilities, faster motion planning algorithms are necessary.

:::: {#fig:intro .figure latex-placement="ht!"}
![](Chamzas2022Learning_figs/intro.png){width="90%"}

::: caption
Three example problems $M_0, M_1, M_2$ where the robot is tasked with picking one object from a shelf starting from the same tuck (home) configuration (not shown for visual clarity). The motion planning problems $M_0$ and $M_1$ have similar solution paths even though their workspaces are visually different. On the other hand, visually similar workspaces such as $M_1$ and $M_2$ can have different solution paths for subtle reasons (e.g. slightly different goals, obstacle arrangements, and robot base orientation).
:::
::::

A promising avenue is to guide planning by leveraging the past experiences of a robot. Several methods have shown that storing and retrieving experiences [@Jetchev2013; @Coleman2015thunder] can significantly improve motion planners' efficiency. These methods have focused on what to store and how to adapt/repair it for the current situation, but not on how to retrieve the most relevant experiences, defaulting to simple similarity functions. In other words, little emphasis has been placed on finding suitable functions that quantify the similarity of motion planning problems, limiting the generalizability of retrieval-based methods outside their training dataset.

In this context, for similar motion planning problems or subproblems, the solution path of one can be used to expedite the search when solving the other. Capturing this notion of similarity is the core investigation of this work. Designing a good similarity function is very challenging for motion planning problems. For example, in [1](#fig:intro){reference-type="ref+label" reference="fig:intro"} two visually dissimilar workspaces $M_0$, $M_1$ have similar solution paths while visually similar workspaces $M_1$ and $M_2$ have different solution paths. A good similarity function should capture the commonalities between $M_0$ and $M_1$ while still distinguishing between $M_1$ and $M_2$. These problems are part of the "Tall-Shelf" dataset described in [5](#sec:exp){reference-type="ref+label" reference="sec:exp"}.

To address this problem we propose **F**ast retr**I**eval of **R**elevant **E**xperiences ([fire]{.smallcaps}). As detailed in [4](#sec:meth){reference-type="ref+label" reference="sec:meth"}, [fire]{.smallcaps} extracts suitable local representations, called local primitives, from previous problems. [fire]{.smallcaps} finds pairs of similar and dissimilar local primitives using a self-supervised method. With these pairs, a similarity function is learned which can be used to retrieve relevant experiences and guide a motion planner. We demonstrate the effectiveness of [fire]{.smallcaps} with an 8-[dof]{.smallcaps} mobile manipulator in five categories of diverse problems with sensed environments as shown ([1](#fig:intro){reference-type="ref+label" reference="fig:intro"}). Through our experiments ([5](#sec:exp){reference-type="ref+label" reference="sec:exp"}) we show that [fire]{.smallcaps} generalizes better outside its training dataset even with less data, and is faster in terms of planning time than prior work. The implementation of [fire]{.smallcaps} and the generated datasets are open-source [^2].

Overall, the main contributions of this work lie in 1) defining suitable local representations of motion planning problems, 2) learning a similarity function over them, and 3) applying it in the motion planning problem through our new framework. Although [fire]{.smallcaps} is tailored to retrieval frameworks that use local features and biased sampling distributions [@Chamzas2019; @Chamzas2021] we believe it could be easily adapted to work with other retrieval-based methods [@Lien2009; @Tang2019; @Merkt2020].

# Problem Description and Notation {#sec:form}

*Feasible Path Planning*: Consider a robot in a workspace $\mathcal{W}$. A configuration of the robot $x$ is a point in the configuration space ($\mathcal{C}$-space), $x \in \ensuremath{\mathcal{C}}$. Obstacles in the workspace induce $\mathcal{C}$-space obstacles $X_\text{obs}\subset \ensuremath{\mathcal{C}}$. The set of configurations that are not in collision is denoted by $X_\text{free}= \ensuremath{\mathcal{C}}- X_\text{obs}$. We are interested in finding a path $p$, from $\ensuremath{x_\textsc{start}}\in X_\text{free}$ to $\ensuremath{x_\textsc{goal}}\in X_\text{free}$, as a continuous map with $\ensuremath{p}(0) = \ensuremath{x_\textsc{start}},~\ensuremath{p}(1) = \ensuremath{x_\textsc{goal}}$ such that for all $t \in \ensuremath{[0, 1]}$, $\ensuremath{p}(t) \in X_\text{free}$. We denote the motion planning problem by $\ensuremath{\mathcal{M}}=(\ensuremath{x_\textsc{start}}, \ensuremath{x_\textsc{goal}}, \ensuremath{\mathcal{W}})$.

*"Challenging Regions" and "Critical Samples"*: In this work, we are concerned with planning for high-dimensional robotic manipulators, and focus on sampling-based motion planners. A common theme in learning-based approaches is to produce configurations in $\mathcal{C}$-space regions with low visibility [@Hsu2003], which are the main bottleneck for sampling-based motion planners [@Hsu2006]. We denote these "challenging regions", and configurations inside them "critical samples."

*Retrieval-Based Learning for Motion Planning*: Given a dataset $\ensuremath{\mathcal{DS}}=\{\ensuremath{\mathcal{M}}^i:\ensuremath{p}^i\}^N_{i=1}$ of past problems $\mathcal{M}$ and their feasible paths $p$, retrieval-based methods extract information from $\mathcal{DS}$ and store it in a database denoted $\mathcal{DB}$. In this context, $\mathcal{DB}$ is a structure that contains $\langle key:value \rangle$ entries, with the experiences (values) being "critical samples." The indices (keys) of the database are local primitives denoted by $\ensuremath{\ell}\in \ensuremath{\mathcal{L}}$, where $\mathcal{L}$ is the space of local primitives. Each local primitive includes local workspace information [@Chamzas2021] along with $x_\textsc{start}$, $x_\textsc{goal}$ information (as defined in [4.1](#sec:lp){reference-type="ref+label" reference="sec:lp"}). This work aims to learn a suitable similarity function $\textsc{sim}:\ensuremath{\mathcal{L}}\times\ensuremath{\mathcal{L}}\rightarrow \{0,1\}$ over the local primitives in order to retrieve relevant "critical samples" for a given problem $\mathcal{M}$.

# Related work {#sec:related}

Over the years many techniques have been proposed to guide sampling-based motion planners. Many examples use heuristics to bias sampling, such as Bridge sampling [@Hsu2006], Gaussian sampling [@Boor1999], Medial-Axis sampling [@Lien2003], and workspace-based sampling [@Kurniawati2008]. However, these predefined heuristics may or may not apply in different situations.

Thus, a growing number of works attempt to learn how to guide planning by utilizing past solutions to motion planning problems. One set of methods learns interesting regions in $\mathcal{W}$ [@Zucker2008; @Molina2020Link] but requires an inverse kinematics solver to infer samples in "challenging regions". A similar class of methods directly computes relevant configurations in $\mathcal{C}$ from a motion planning problem $\mathcal{M}$ using a neural network. For example, some methods train a conditional variational autoencoder to reconstruct samples from previous paths [@Ichter2018] or "challenging regions" [@Ichter2020LocalCrit; @Kumar2019; @Jenamani2020LocalCrit]. The authors of [@Patil2019PredictionOB; @Terasawa20203d] use a [3d]{.smallcaps} CNN to sample in "challenging regions", while [@Qureshi2020motion; @Tamar2019; @Chen2020] use neural networks as motion planners.

Although these methods have shown some promising results, mapping $\mathcal{M}$ to paths or "challenging regions" in $\mathcal{C}$ is hard in high-dimensional problems. Motion planning is sensitive to input; small changes in $\ensuremath{\mathcal{W}}$, $\ensuremath{x_\textsc{start}}$, or $\ensuremath{x_\textsc{goal}}$ can drastically alter the resulting solution [@Tang2019; @Chamzas2021; @Farber2003]. Furthermore, this mapping is usually multi-modal, since a motion planning problem may have multiple solution paths or multiple disjoint "challenging regions" [@Merkt2020; @Rice2020Multihomotopy].

For these reasons, some approaches have adopted retrieval-based methods, also known as library- [@Stolle2007Transfer] or memory-based [@Lembono2020] methods. Such methods typically store in memory a database $\ensuremath{\mathcal{DB}}$ and retrieve relevant information in the form of paths [@Berenson2012lightning; @Pairet2021] or sampling distributions [@Chamzas2019; @Finney2007Partial] based on a similarity function over $\mathcal{M}$. These methods naturally apply to multi-modal problems, since for similar or identical $\mathcal{M}$ multiple outputs can be retrieved. Another advantage of these methods is that they are incremental since new experiences can simply be added to the database $\mathcal{DB}$. The main challenge lies in constructing a good similarity function over $\mathcal{M}$.

Defining a similarity function is challenging because $\mathcal{M}$ contains heterogeneous parameters; $\ensuremath{x_\textsc{start}}, \ensuremath{x_\textsc{goal}}\in \ensuremath{\mathcal{C}}$ while $\ensuremath{\mathcal{W}}$ is a 3D representation. Some approaches do not use a similarity function but learn problem invariants [@Iversen2016Kernel; @Lehner2017], others construct the similarity only over $\ensuremath{x_\textsc{start}}$ and $\ensuremath{x_\textsc{goal}}$ [@Coleman2015thunder; @Berenson2012lightning], and some construct it only over $\mathcal{W}$ [@Lien2009; @Chamzas2021]. In [@Chamzas2021] a hand-crafted similarity function over local workspaces is defined, while [@Lien2009] defines workspace similarity based on geometric deformation of obstacles. Most similarly to our work, [@Jetchev2013] learned a similarity function over $\ensuremath{x_\textsc{start}}$, $\ensuremath{x_\textsc{goal}}$, and $\mathcal{W}$ using a weighted combination of global workspace features. In contrast, our work uses local features and leverages latent space representations obtained from neural networks.

Learning similarity functions [@hoffer2015deep] in the latent space has been successfully employed in computer-vision tasks, such as image classification [@vinyals2016matching] and 3D object classification [@zeng20163dmatch]. Our work is inspired by these methods, and applies similar metric learning methods to the motion planning problem.

# Methodology {#sec:meth}

![ **a)** The blue dots depict the 10 projections defined on the arm and gripper of the Fetch robot. Each blue dot is one projection point $\pi(x)_p \in \mathbb{R}^{3}$ of $x \in \ensuremath{\mathcal{C}}$. Specifically, each robotic link of the arm+gripper was used as a projection, as described in its `urdf`. **b)** Examples of local occupancy grids and their position in space derived from the sensed scene ($\ensuremath{lw}= (b, \ensuremath{v}$)). Note that only non-empty local occupancy grids are generated. ](Chamzas2022Learning_figs/proj_octo.png){#fig:proj_octo width="80%"}

We propose [fire]{.smallcaps}, a framework that learns a similarity function to retrieve relevant experiences from a database in the form of "critical samples". In [4.1](#sec:lp){reference-type="ref+label" reference="sec:lp"} we formulate the local primitives which are the input to the similarity function, and we extract them from past problems in [4.2](#sec:cr){reference-type="ref+label" reference="sec:cr"}. Then, we describe how to generate similar and dissimilar local primitives ([4.3](#sec:gen){reference-type="ref+label" reference="sec:gen"}). In [4.4](#sec:learn){reference-type="ref+label" reference="sec:learn"}, we train a Siamese network by minimizing the contrastive loss of the local primitive pairs and realize the similarity function in the learned latent space. Finally, [4.5](#sec:ret){reference-type="ref+label" reference="sec:ret"} explains how the similarity function can guide a sampling-based planner.

## Local primitives {#sec:lp}

First, we define a set of projections ${\pi}(x): \ensuremath{\mathcal{C}}\rightarrow \mathbb{R}^3$ used to extract and compare local primitives. Each configuration $x$ is projected to multiple points in $\mathcal{W}$ and stacked as a vector $${\Pi}(x)= [{\pi}_1(x), {\pi}_{2}(x), \ldots,  {\pi}_{P}(x)] \in \mathbb{R}^{3\times P}$$ where $P$ is the number of projections. [2](#fig:proj_octo){reference-type="ref+label" reference="fig:proj_octo"}a) shows the 10 projections on the Fetch which we used. Specifically, we used the link frames of the arm+gripper from the Fetch [@Wise2016] `urdf`. Projections have often been used to guide motion planners [@Orthey2018quotient] and specifying them is often a research problem in itself, albeit outside the scope of this work.

Now we define the local primitives $\ell$, which include a local [3d]{.smallcaps} occupancy grid and its position $lw$[@Chamzas2021] along with some auxiliary $\mathcal{C}$-space information $x_\textsc{target}$ and $x_\textsc{proj}$:

$$\begin{align*}
    \ensuremath{\ell}=  [\ensuremath{lw}, \ensuremath{x_\textsc{target}}, \ensuremath{x_\textsc{proj}}]
\end{align*}$$

More specifically, $\ensuremath{lw}= (b, \ensuremath{v})$ where $b \in \{0,1\}^{64}$ is a 64-bit binary vector that represents a (4x4x4) local occupancy grid and $\ensuremath{v}\in \mathbb{R}^3$ is the center position of the grid. Examples of $lw$ are shown in [2](#fig:proj_octo){reference-type="ref+label" reference="fig:proj_octo"}b. The variable $\ensuremath{x_\textsc{target}}\in \ensuremath{\mathcal{C}}$ is either $x_\textsc{start}$ or $x_\textsc{goal}$, depending on the situation as explained in [\[alg:1\]](#alg:1){reference-type="ref+label" reference="alg:1"} and [4.5](#sec:ret){reference-type="ref+label" reference="sec:ret"}. Finally, we calculate $x_\textsc{proj}$ from $x_\textsc{target}$ and the center position $v$ of $lw$. We project $x_\textsc{target}$ to $P$ points in the workspace ${\Pi}(\ensuremath{x_\textsc{target}})  \in \mathbb{R}^{3\times P}$ and then aggregate all the distances between the $P$ points and $v$ to calculate $x_\textsc{proj}$: $$\begin{align*}
     \ensuremath{x_\textsc{proj}}= [\left\lVert\ensuremath{v}- {\pi}_1(\ensuremath{x_\textsc{target}})\right\rVert, \ldots , \left\lVert\ensuremath{v}- {\pi}_P(\ensuremath{x_\textsc{target}})\right\rVert]  \in \mathbb{R}^{P}
\end{align*}$$ The variable $x_\textsc{proj}$ serves as an interleaved representation of $x_\textsc{target}$ and $lw$ and was empirically validated to improve the latent space structure.

## Creating the experience database {#sec:cr}

[\[alg:1\]](#alg:1){reference-type="ref+label" reference="alg:1"} describes how to create the experience database $\mathcal{DB}$ from $\ensuremath{\mathcal{DS}}=\{(\ensuremath{x_\textsc{start}}, \ensuremath{x_\textsc{goal}}, W)^i:\ensuremath{p}^i\}^N_{i=1}$ by associating each local primitive with a configuration from a solution path.

First, the paths are shortcutted [@Raveh2011] to remove redundant nodes not in "challenging regions"([\[alg:1:short\]](#alg:1:short){reference-type="ref+label" reference="alg:1:short"} in [\[alg:1\]](#alg:1){reference-type="ref+label" reference="alg:1"}) and keep only "critical samples". Finding "critical samples" is still an open research problem [@Ichter2020LocalCrit; @Molina2020Link; @Chamzas2021] but this simple shortcutting heuristic has been used previously in [@Chamzas2019; @Iversen2016Kernel].

Next, `TARGET` ([\[alg:1:target\]](#alg:1:target){reference-type="ref+label" reference="alg:1:target"} in [\[alg:1\]](#alg:1){reference-type="ref+label" reference="alg:1"}) samples near $x_\textsc{start}$ and $x_\textsc{goal}$ and chooses the one which yielded the most in-collision samples with the workspace. This aims to create the same local representation for motion plans with the same solution path but swapped $x_\textsc{start}$ and $x_\textsc{goal}$. Consider for example the task in [1](#fig:intro){reference-type="ref+label" reference="fig:intro"}, where the robot plans from the home ($x_\textsc{start}$) to a grasp configuration ($x_\textsc{goal}$). The same solution path applies for planning between the grasp configuration ($x_\textsc{start}$) back to the tuck configuration ($x_\textsc{goal}$). Thus, to ensure that both plans have the same local representations `TARGET` should choose the same configuration as $x_\textsc{target}$(e.g. the grasp configuration). We then decompose the workspace to local occupancy grids ([\[alg:1:decompose\]](#alg:1:decompose){reference-type="ref+label" reference="alg:1:decompose"} in [\[alg:1\]](#alg:1){reference-type="ref+label" reference="alg:1"}) by traversing the octomap tree similarly to [@Chamzas2021].

::: algorithm
Shortcut $\ensuremath{p}^{\prime} = \SHORT(\ensuremath{p})$\
[]{#alg:1:short label="alg:1:short"} Find target $x_\textsc{target}$$\gets$ ($x_\textsc{goal}$, $x_\textsc{start}$)\
[]{#alg:1:target label="alg:1:target"} Decompose $\ensuremath{\mathcal{W}}$ to $\mathcal{LW} \gets \{\ensuremath{lw}_{1}, \ldots, \ensuremath{lw}_{M}\}$ []{#alg:1:decompose label="alg:1:decompose"}\
[]{#alg:1:contains label="alg:1:contains"} $\ensuremath{x_\textsc{proj}}\gets |\ensuremath{\tilde{\ensuremath{v}}}- {\Pi}(\ensuremath{x_\textsc{target}})|$\
$\ensuremath{\ell}\gets [\ensuremath{lw}, \ensuremath{x_\textsc{target}},\ensuremath{x_\textsc{proj}}]$\
$x^{n} \gets \NEXT(x,\ensuremath{p})$\
$x^{p} \gets \PREVIOUS(x,\ensuremath{p})$\
Insert $\langle \ensuremath{\ell}: x^{p}, x,  x^{n} \rangle$ in $\mathcal{DB}$[]{#alg:1:store label="alg:1:store"} $\mathcal{DB}$
:::

Afterward, we iterate over the configurations in each path, the local occupancy grids, and the projections. The subroutine `CONTAINS` associates each configuration with its relevant regions in the workspace. `CONTAINS` checks for every projection ${\pi}(x)_p \in \mathbb{R}^{3}$ of the configuration $x$ if it is contained in the bounding box of an occupancy grid; if so we store the local primitive $\ell$ along with the critical $x$, the previous waypoint configuration $x^p$, and the next waypoint configuration $x^n$ in $\mathcal{DB}$. The previous and next configurations are only used to help us create similar pairs as described in [\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"} and are not part of the retrieved experience.

## Creating a dataset of similar pairs {#sec:gen}

[\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"} describes a novel method to create a dataset of similar pairs of local primitives over which to learn the similarity function. This is the key problem investigated in this paper.

Given a database $\mathcal{DB}$, we iterate over all pairs of local primitives and perform the following checks. First, the subroutine `SAME_PROJ` checks if the two local primitives were generated by the same projection ([\[alg:2:proj\]](#alg:2:proj){reference-type="ref+label" reference="alg:2:proj"} in [\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"}). Then we check whether the centers $v$ of the local occupancy grids are close enough in $\mathcal{W}$([\[alg:2:check1\]](#alg:2:check1){reference-type="ref+label" reference="alg:2:check1"} in [\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"}) and whether the stored configurations are also close enough in $\mathcal{C}$-space([\[alg:2:check2\]](#alg:2:check2){reference-type="ref+label" reference="alg:2:check2"} in [\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"}). The variable $lw_{side}$ is the length of the side of the local occupancy bounding box $lw$.

Finally ([\[alg:2:check2\]](#alg:2:check2){reference-type="ref+label" reference="alg:2:check2"} in [\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"}) we sample up to N times $x^{near}_{j} \sim  \mathcal{N}(x_j, \sigma^2)$ until a configuration $x^{near}_{j}$ is found which passes the `VALID` check. The `VALID` subroutine checks if $x^{near}_{j}$ can connect through a collision-free edge (in the full workspace $\mathcal{W}$ of $\ensuremath{\ell}_i$) with the next $x^n_{i}$ and previous $x^p_{i}$ configuration of the local primitive $\ensuremath{\ell}_i$. If such a configuration is found then we consider $\langle \ensuremath{\ell}_i,\ensuremath{\ell}_j \rangle$ similar and add them to $\mathcal{S}$. This procedure aims to discover local primitives whose "critical samples" are good substitutes for one another by emulating how "critical samples" are used to bias sampling during planning ([4.5](#sec:ret){reference-type="ref+label" reference="sec:ret"}). To generate dissimilar pairs we randomly choose local primitives from $\mathcal{DB}$ and generate an equal number of dissimilar pairs. We denote the set that includes these dissimilar pairs $\mathcal{NS}$.

::: algorithm
[]{#alg:2:proj label="alg:2:proj"}

[]{#alg:2:check1 label="alg:2:check1"}

[]{#alg:2:check2 label="alg:2:check2"} []{#alg:2:check3 label="alg:2:check3"} $x^{near}_{j} \sim  \mathcal{N}(x_j, \sigma^2)$\
$\mathcal{S}$$\gets \langle \ensuremath{\ell}_j, \ensuremath{\ell}_i \rangle$\
\

$\mathcal{S}$
:::

Note that [\[alg:2\]](#alg:2){reference-type="ref+label" reference="alg:2"} needs the "critical samples" extracted from solution paths to find similar local primitives, and cannot be used as a similarity function when solving a new motion planning problem where only $W, \ensuremath{x_\textsc{goal}}, \ensuremath{x_\textsc{start}}$ is available.

## Learning the similarity function {#sec:learn}

The learned similarity function is realized in the latent space of a Siamese network. A Siamese network [@chicco2020siamese] is comprised of two identical encoder networks as shown in [3](#fig:siamese){reference-type="ref+label" reference="fig:siamese"}. Each encoder maps $\ell$ to a latent variable $z \in \mathbb{R}^{8}$. The overall network is relatively small with around 3500 parameters, and was trained with the contrastive loss [@hadsell2006dimensionality]: $$\begin{equation*}
\label{eq:contrastive}
\mathcal{L}(\ensuremath{\ell}_i, \ensuremath{\ell}_j) =
\begin{cases}
    \max (0,d_m - \left\lVert z_i-z_j\right\rVert^2) & \text{if }   \langle \ensuremath{\ell}_j, \ensuremath{\ell}_i \rangle \in \ensuremath{\mathcal{NS}}\\
            ||z_i - z_j||^2 & \text{if } \langle \ensuremath{\ell}_j, \ensuremath{\ell}_i \rangle \in \ensuremath{\mathcal{S}}
\end{cases}
\end{equation*}$$

This loss tries to bring local primitives that belong in $\mathcal{S}$ (similar) as close as possible in the latent space $Z$, while local primitives that belong in $\mathcal{NS}$(dissimilar) must have at least a margin distance $d_m=0.5$. After having structured the latent space $Z$ the similarity function is defined as follows:

$$\begin{equation*}
\label{eq:simfun}
\textsc{sim}(\ensuremath{\ell}_i, \ensuremath{\ell}_j) =
\begin{cases}
    1 & \text{if} \left\lVert z_i-z_j\right\rVert^2< R\\
    0 & \text{ otherwise} 
\end{cases}
\end{equation*}$$

where $R=0.2d_m$ is the retrieval radius. A lower retrieval radius than the margin distance $d_m$ must be used to avoid retrieving dissimilar pairs. After structuring the latent space $Z$ all the local primitives in $\mathcal{DB}$ are projected to $Z$ and added in a K-D tree [@bentley1975multidimensional] structure for fast retrieval. Finding similar local primitives with [sim]{.smallcaps} is equivalent [@balcan2008theory] to retrieving all the neighbors within radius $R$ in the latent space $Z$.

![The Siamese network architecture used. The activation function for all the layers was ReLU. *Conv3D* denotes a 3D convolutional layer, *MaxPool* takes the maximum value out of every subgrid, and *FC* denotes a fully connected layer. The parameters of each layer are shown in the figure. ](figures/siamese.svg){#fig:siamese width="90%"}

## Retrieving relevant experiences {#sec:ret}

When solving a new problem $\mathcal{M}$=($x_\textsc{start}$,$x_\textsc{goal}$, $\mathcal{W}$) the new local primitives are created with the following procedure. First, we extract the local occupancy grids from $\mathcal{W}$. Then, for each local occupancy grid $lw$ we generate two local primitives: one with $\ensuremath{x_\textsc{target}}=\ensuremath{x_\textsc{start}}$ and one with $\ensuremath{x_\textsc{target}}=\ensuremath{x_\textsc{goal}}$. The value of $\ensuremath{x_\textsc{proj}}$ is calculated from $x_\textsc{target}$ and $\ell$ as explained in [\[alg:1\]](#alg:1){reference-type="ref+label" reference="alg:1"}. Each created local primitive is projected to $Z$ and its neighbors within radius $R$ are retrieved, effectively obtaining their associated "critical samples" from $\mathcal{DB}$. Finally, similarly to [@Chamzas2021], we aggregate all the $K$ "critical samples" and convert them to a Gaussian Mixture Model ([gmm]{.smallcaps}): $$P(x|\ensuremath{\mathcal{M}}) = \frac{1}{K} \sum^{K}_{i=0} \mathcal{N}(x_i, \sigma^2)$$

The [gmm]{.smallcaps} can be used to bias the sampling of any sampling-based planner. To keep the probabilistic completeness guarantees of sampling-based planners we sample from $P(x|\ensuremath{\mathcal{M}})$ with probability $0< \lambda <1$ and from a standard uniform distribution with probability $(1-\lambda)$. If the planner uses a local expansion strategy like [est]{.smallcaps} [@Hsu1999] we simply sample from the mixtures that are within the local sampling radius.

# Experiments {#sec:exp}

![**a)** An example problem from the "Small-Shelf" dataset. We generate different problems by uniformly sampling the robot pose, the position of the obstacles, and the height of the shelf. This is similar to the "Small-Shelf" used in [@Chamzas2021] but the shelf is shorter, making it more challenging due to the narrow area the robot has to traverse. **b)** Planning time (including retrieval) with different underlying planners for 100 test examples from the "Small-Shelf" dataset. The timeout was set to 180 seconds.](figures/results_small.svg){#fig:small width="\\linewidth"}

We demonstrate the effectiveness of the learned similarity function on five generated datasets with [MotionBenchMaker]{.smallcaps} [@Chamzas2022]. Each dataset contains an 8-[dof]{.smallcaps}(arm+torso) Fetch robot [@Wise2016] with a workspace represented by an octomap [@Hornung2013], performing a pick task as shown in [4](#fig:small){reference-type="ref+label" reference="fig:small"}a. We consider this a realistic representation since point clouds can easily be obtained from a simple depth camera. The five datasets generated were "Small-Shelf"([4](#fig:small){reference-type="ref+label" reference="fig:small"}a), "Tall-Shelf"([5](#fig:envs){reference-type="ref+label" reference="fig:envs"}a), "Thin-Shelf"([5](#fig:envs){reference-type="ref+label" reference="fig:envs"}b), "Table"([5](#fig:envs){reference-type="ref+label" reference="fig:envs"}c), and "Cage"([7](#fig:cage){reference-type="ref+label" reference="fig:cage"}a). As shown in the figures, the starting configuration $x_\textsc{start}$ for all datasets was a home (tuck) position, except for "Table" where $x_\textsc{start}$ is a random configuration under the table. The goal configuration $x_\textsc{goal}$ is an inverse kinematics (IK) solution placing the end-effector in a grasping pose relative to an object. For the "Shelf" datasets, one object per shelf is grasped and it is always the one furthest back. For "Table" and "Cage" the grasped object is shown in the figures. We generate different motion planning problems similarly to [@Chamzas2021] by uniformly sampling poses for the robot base and scene objects. Note that such variation generates highly diverse planning problems since even small changes in the positions of the obstacles relative to the robot drastically affect $X_\text{obs}$ and the resulting $x_\textsc{goal}$.

![The three datasets used to test the evaluated methods. Different problems are generated similarly to [4](#fig:small){reference-type="ref+label" reference="fig:small"}. **a)** An example environment from the "Tall-Shelf" dataset. The "Tall-Shelf" is created by stacking the "Small-Shelf" three times. **b)** An example environment from the "Thin-Shelf" dataset. This is also a bookcase like "Small-Shelf" and "Tall-Shelf", but the shelves are shorter and there is a divider, making it a much more challenging problem. **c)** An example environment from the "Table" dataset, which includes a table with several objects and is very different from the other datasets.](figures/all_environments.pdf){#fig:envs width="\\linewidth"}

![ Planning time (including retrieval) when testing in the three datasets shown in [5](#fig:envs){reference-type="ref+label" reference="fig:envs"}. All of the methods are only trained with the "Small-Shelf" dataset. The timeout was set to 180 seconds. ](figures/results_test.svg){#fig:test width="\\linewidth"}

All evaluated methods produce biased samples in $\mathcal{C}$ which can guide any sampling-based motion planner. We evaluated these methods within [rrt]{.smallcaps}-connect ([rrtc]{.smallcaps}) [@Kuffner2000] and bidirectional [est]{.smallcaps} ([biest]{.smallcaps}) [@Hsu1999], implemented in the Open Motion Planning Library ([ompl]{.smallcaps}) [@Sucan2012]. Additionally, we considered two versions of each planner: one with default [ompl]{.smallcaps} parameters ([rrtc-default]{.smallcaps} and [biest-default]{.smallcaps}) and one with a tuned range parameter ([rrtc-tuned]{.smallcaps} and [biest-tuned]{.smallcaps}) found by a parameter sweep over a diverse set of problems. In our experiments we compare [fire]{.smallcaps} with the following methods:

- [uniform]{.smallcaps}: Default uniform sampling of the $\mathcal{C}$-space.

- [mpnet-smp]{.smallcaps} [@Qureshi2020motion]: This is the sampling-biasing version of Motion Planning Networks. Given a training dataset of [3d]{.smallcaps} point cloud workspaces, $x_\textsc{start}$, $x_\textsc{goal}$, and solution paths, [mpnet-smp]{.smallcaps} learns to iteratively produce samples that mimic the solution paths. We adapted the provided implementation and tuned its hyperparameters to achieve the best performance for the given problems.

- [flame]{.smallcaps} [@Chamzas2021]: This framework is similar to [fire]{.smallcaps} and also retrieves "critical samples" from a $\mathcal{DB}$. However, the local primitives are simpler, including only workspace information ($lw$) and not considering $x_\textsc{goal}$ or $x_\textsc{start}$. The similarity function considers $\ensuremath{lw}_i$ similar to $\ensuremath{lw}_j$ if they have the same position and binary representation.

- [static]{.smallcaps} [@Iversen2016Kernel; @Lehner2017]: These methods generate a static sampling distribution by extracting key configurations from past trajectories. They do not rely on a similarity function but instead attempt to capture the problem's invariants. We emulate the static sampling idea of these methods by retrieving all the $\mathcal{C}$-space samples we have stored in $\mathcal{DB}$.

We consider these methods representative of the works discussed in [3](#sec:related){reference-type="ref+label" reference="sec:related"}, with [mpnet-smp]{.smallcaps} being a non-retrieval method that directly maps $\mathcal{M}$ to $\mathcal{C}$-space samples using a neural network, [flame]{.smallcaps} a retrieval-based method with a hand-crafted similarity function, and [static]{.smallcaps} a method that learns problem invariants.

We evaluate the performance of [fire]{.smallcaps} and the generalization of the learned similarity function when both the training and testing examples come from the same dataset ([5.1](#sec:small){reference-type="ref+label" reference="sec:small"}), and also when the testing dataset is increasingly different from the training dataset ([5.2](#sec:test){reference-type="ref+label" reference="sec:test"}). Finally, we evaluate [fire]{.smallcaps} when retrieving experiences it was not trained on, and while the $\mathcal{DB}$ includes unrelated experiences ([5.3](#sec:cage){reference-type="ref+label" reference="sec:cage"}). For our experiments we used Robowflex with MoveIt [@Moveit; @Robowflex] and the [ompl]{.smallcaps} benchmarking tools [@Moll2015]. The sampling parameters for [fire]{.smallcaps} were the same as [@Chamzas2021] ($\sigma^2 =0.2, \lambda =0.5$).

## Generalizing in similar problems {#sec:small}

### Learning (Training)

In this experiment, [mpnet-smp]{.smallcaps}, [flame]{.smallcaps}, and [fire]{.smallcaps} were trained in problems that come from the "Small-Shelf" dataset. [fire]{.smallcaps} and [flame]{.smallcaps} were given enough training examples for their performance to converge in the "Small-Shelf" dataset. By convergence, we mean that the average planning time did not improve after doubling the number of experiences in $\mathcal{DB}$. Specifically, [fire]{.smallcaps} was trained with a total of 500 training examples. From these 500 examples, 200 were used to learn the similarity function and all of the 500 examples were added to $\mathcal{DB}$. Training the Siamese network of [fire]{.smallcaps} took around 1 hour for 200 epochs. [flame]{.smallcaps} was trained with 1000 examples which were added to $\mathcal{DB}$ as described in [@Chamzas2021]. Since it was difficult to profile the convergence of [mpnet-smp]{.smallcaps}($\approx$`<!-- -->`{=html}1 day of training time) we provided it 5000 training examples to ensure that it has enough data. This is of a similar order to [@Qureshi2020motion] (10000).

### Evaluation (Testing)

The methods were tested in a different set of 100 problems that also come from "Small-Shelf". As seen in [4](#fig:small){reference-type="ref+label" reference="fig:small"}b, [fire]{.smallcaps} outperformed all other methods in all four different settings in terms of planning time. We do include the retrieval time in the total planning time for [flame]{.smallcaps} and [fire]{.smallcaps} but it was negligible in all cases ($0.01-0.1$ seconds). We also notice that the tuning of the underlying planner and the use of experiences interact synergistically, with the best performance being achieved by [fire]{.smallcaps} with [rrtc-tuned]{.smallcaps}.

## Generalizing in increasingly different problems {#sec:test}

### Learning (Training)

We do not perform any additional training in these experiments and simply use the methods trained on "Small-Shelf" from [5.1](#sec:small){reference-type="ref+label" reference="sec:small"}.

### Evaluation (Testing)

In these experiments, the methods were tested on three datasets that are increasingly different from "Small-Shelf" as shown in [5](#fig:envs){reference-type="ref+label" reference="fig:envs"}. The "Tall-Shelf" is created by stacking the "Small-Shelf" three times. The "Thin-Shelf" is also a bookcase but is different from "Tall-Shelf" and "Small-Shelf" because there is a divider and the distance between the shelves has changed. Finally, "Table" is significantly different from "Small-Shelf" regarding $\mathcal{W}$. We used 100 testing examples for each of these three datasets. As shown in [6](#fig:test){reference-type="ref+label" reference="fig:test"}, [mpnet-smp]{.smallcaps} could not outperform [uniform]{.smallcaps} in "Tall-Shelf" and "Table" except for [rrtc-default]{.smallcaps}, while in "Thin-Shelf" it was not able to improve upon [uniform]{.smallcaps} given the time limits. In some cases [mpnet-smp]{.smallcaps} performed worse than [uniform]{.smallcaps}; we attribute this behavior to the testing examples being outside the training dataset of [mpnet-smp]{.smallcaps}. [flame]{.smallcaps} did offer some improvement for the "Tall-Shelf" environment but could not transfer to "Thin-Shelf" or "Table". Also, in some cases [flame]{.smallcaps} performed worse than [uniform]{.smallcaps}; this is attributed to the retrieval of very few critical samples leading to poor biased sampling (if nothing is retrieved it defaults to [uniform]{.smallcaps}). On the other hand, [fire]{.smallcaps} outperformed all other methods even in "Thin-Shelf" and "Table", demonstrating that the learned similarity function generalizes to problems that are significantly different than those in the training dataset. We also note that "Table" has a different $x_\textsc{start}$ configuration than the training dataset "Small-Shelf". This demonstrates the usefulness of independently considering $x_\textsc{start}$ and $x_\textsc{goal}$ in the local primitives defined by [fire]{.smallcaps}.

![ **a)** An example problem from the "Cage" dataset. **b)** Planning time for 100 test examples from the "Cage" dataset using the [rrtc-tuned]{.smallcaps} planner. The timeout was set to 60 seconds. The x-axis shows the number of experiences that exist in $\mathcal{DB}$ from "Small-Shelf" and from "Cage". Note that "Small-Shelf" and "Cage" have very different solution paths. In other words, the experiences from "Small-Shelf" do not transfer to "Cage". ](figures/results_cage.svg){#fig:cage width="\\linewidth"}

## Robustness to irrelevant experiences {#sec:cage}

### Learning (Training)

In this experiment, we do not retrain [fire]{.smallcaps}'s similarity function and use the one obtained from training on "Small-Shelf" from [5.1](#sec:small){reference-type="ref+label" reference="sec:small"}. However, now we add to $\mathcal{DB}$ example problems from both "Cage" and "Small-Shelf". Note that the problems from "Cage" and "Small-Shelf" are highly dissimilar in terms of solution paths. Thus, when solving a problem from "Cage" a good similarity function should not retrieve experiences generated from "Small-Shelf". The x-axis in [7](#fig:cage){reference-type="ref+label" reference="fig:cage"}b shows the ratio of example problems from "Cage" and "Small-Shelf". For example, $500/0$ denotes an experience database $\mathcal{DB}$ that has 500 examples from "Cage" and 0 examples from "Small-Shelf".

### Evaluation (Testing)

In this experiment, we tested on 100 example problems from the "Cage" dataset using [rrtc-tuned]{.smallcaps} as the underlying planner. We compared with [static]{.smallcaps} to illustrate how irrelevant experiences from "Small-Shelf" affect performance. The results in [7](#fig:cage){reference-type="ref+label" reference="fig:cage"}b show that although [static]{.smallcaps} significantly outperforms [uniform]{.smallcaps}, its performance degrades as we add irrelevant experiences in the training dataset. On the other hand, [fire]{.smallcaps} is robust to the irrelevant experiences from "Small-Shelf" added to $\mathcal{DB}$ since it maintains its good performance even with the $500/4500$ ratio. [fire]{.smallcaps}'s similarity function was only trained on "Small-Shelf" while $\mathcal{DB}$ includes experiences from "Cage". This demonstrates that the learned latent space can successfully structure local primitives it was not trained on.

# Conclusion {#sec:discussion}

In this work, we have proposed [fire]{.smallcaps}, a framework that learns a similarity function for motion planning problems with sensed environments. Using the learned similarity function, [fire]{.smallcaps} retrieves relevant experiences from a database in the form of "critical samples" that can informatively guide any sampling-based motion planner. Through our experiments, we demonstrated the generalization of [fire]{.smallcaps} outside its training dataset. Furthermore, [fire]{.smallcaps} can also learn incrementally without retraining by simply adding experiences in $\mathcal{DB}$, and can discriminate between relevant and irrelevant experiences.

In the future, we would like to improve [fire]{.smallcaps} by bounding its memory requirements and treating biased samples differently from uniform samples [@Molina2020Link; @Ichter2020LocalCrit]. Additionally, we would like to investigate how the same ideas apply to other problems that include motion planning such as task and motion planning or kinodynamic planning.

[^1]: All authors are affiliated with the Department of Computer Science, Rice University, Houston TX, USA `{chamzas, aedan, anshumali, kavraki}@rice.edu`. This work was supported in part by NSF 1718478, NSF-GRFP 1842494 and Rice University Funds.

[^2]: <https://github.com/KavrakiLab/pyre>
