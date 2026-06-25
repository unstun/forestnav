---
citation_key: Jenamani2020Robotic
arxiv_id: 2006.04194
arxiv_url: https://arxiv.org/abs/2006.04194
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:45:02Z
origin: ai+web
reviewed: false
---

# Introduction

We examine the problem of using prior experience for sampling based motion planning in robots. Sampling based motion planning (SBMP) algorithms construct a graph or roadmap as a discrete representation of the state space of a robot. The vertices of this roadmap represent robot configurations and edges represent potential movements of the robot. A graph search algorithm is then used to find the path between any two vertices in the roadmap. Rapidly Exploring Random Tree (RRT)[@c17] is a tree growing variant of SBMP that creates this roadmap (tree) implicitly while planning. SBMP is state of the art in high dimensional spaces.

A defining feature of SBMP is it's reliance on the sampler. Traditionally, these samples are generated either probabilistically or deterministically[@c8] to uniformly cover the state space. Such a sampling approach allows arbitrarily accurate representations (in the limit of the number of samples approaching infinity), and thus allows theoretical guarantees on completeness. However, in environments where paths pass through narrow passages, these algorithms become computationally intractable. This is because a huge number of samples must be generated to cover these narrow passages.

:::: {.figure latex-placement="!ht"}
![](Jenamani2020Robotic_figs/herb_full.png){width="\\textwidth"}

::: caption
A $\mathbb{R}^7$ robotic arm planning problem containing a narrow passage.
:::
::::

Thus, the main challenge in sampling based algorithms is to place a small set of samples (critical samples) on certain key locations (bottleneck regions) to enable the algorithm to find a high quality path with low computation effort.

Current state of the art approaches[@c1; @c2] use learning algorithms (called learners hereon) to predict these critical samples. These samples are then connected to the nodes of a uniform sparse graph to construct a roadmap. Depending on the structure of the bottleneck regions (say in an extended narrow passage or semicircular tube like structure), the learner is required to place a small set of critical samples in accordance with the local structure at each bottleneck. The graph created by connecting these critical samples among themselves acts as a bridge for connecting the disjoint sub-graphs (connected components) present in the sparse graph. Thus, the learner needs to not only identify the bottleneck regions but also propose samples in accordance with their local structure.

This brings us to two major challenges faced by these approaches. Firstly, the learners used in these approaches are commonly fed an occupancy grid among other parameters as a representation of the workspace of a robot. There exists a trade-off between the size of the occupancy grid and, amount of data and time taken by the model to converge. In complex planning problems, the size of this occupancy grid must be large. However, this makes the convergence of the model computationally intractable. On the other hand, a decrease in the size of the occupancy grid results in low resolution and thus the learner is not able to learn the internal representation of these bottleneck regions. Thus, a large number of the generated samples are rendered useless. Secondly, most of the learners are conditioned only on the planning problem and not on the prior samples it has generated. Thus, the learner tends to repeatedly sample similar points inside a bottleneck region, leading to redundant samples.

Our key insight is to rely on the learner to identify the location of the bottleneck regions and then exploit the property of planners such as RRT to cover the local structure of these bottleneck regions. Therefore, getting a set of samples from the learner that includes a single sample in each bottleneck region is sufficient. As we expect the learner to generate a single sample per bottleneck region, we propose to convolve the occupancy grid using a kernel to create a smaller grid that contains information relevant for this generation. We use this preprocessed grid during training and for testing the learner.

We thus use the learner to get this initial set of critical samples (one per bottleneck region) and call them critical sources. We then generate our required set of critical samples from these critical sources using local sampling-based methods.

This solves the first challenge faced by current algorithms, as using a smaller grid as input to the learner makes it converge faster to generalizing well over planning problems that have similar global structure for the location of bottleneck regions but different local structures within these regions This also solves the second challenge as we condition the subsequent samples on our current set of critical samples. The job is therefore divided between the learner (generate the critical sources) and the local sampler (procure the required set of critical samples by using these critical sources to generate subsequent samples). We argue that this is similar to how we, as humans, given a planning problem, first *globally* identify the doorways present relevant to our planning problem and then *locally* explore how to navigate through these doorways.

Due to the efficient space filling nature of RRTs, we propose the algorithm: Local Critical Source RRT ([LCS$-$RRT]{.smallcaps}). This algorithm, in conjunction with a sparse graph, uses RRTs rooted at critical sources as the local sampling algorithm.

We propose another algorithm, Critical Source-RRT ($\textsc{CS$-$RRT}$), which forfeits the sparse graphs altogether and incrementally builds RRTs rooted at start, goal and critical sources. In addition to RRTs generating the required set of critical samples, $\textsc{CS$-$RRT}$ depends on the inherent bias of RRTs to grow towards large unsearched areas of the problem to emulate the sparse graph once the tree is out of the bottleneck region.

We thus make the following contributions:

1.  We present $\textsc{GenerateCriticalSources}$, a fast methodology that uses learning models efficiently to generate a set of critical samples, ideally one per bottleneck region (called critical sources).

2.  We present the algorithm Local Critical Source - RRT ($\textsc{LCS$-$RRT}$) which, in conjunction with a sparse graph, uses RRTs rooted at critical sources to generate the required set of critical samples which acts as a bridge between disjoint sub-graphs of the sparse graph.

3.  We present the algorithm Critical Source - RRT ($\textsc{CS$-$RRT}$) that works by incrementally building RRTs rooted at multiple key sources (start, goal and critical sources).

4.  We show that $\textsc{LCS$-$RRT}$ and $\textsc{CS$-$RRT}$ outperform the sampling based baselines on a set of $\mathbb{R}^2$ point object and $\mathbb{R}^7$ robotic arm motion planning problems, and prove their probabilistic completeness.

# Related Work

An analysis on the shortcomings of using uniform sampling in the presence of narrow passages is given by D. Hsu et. al. [@c7] . This has stimulated numerous works on using selective densification for non-uniform sampling [@c9]-[@c13].

A multitude of these works use adaptive sampling for roadmap densification by exploiting the structure of the environment. While some propose to sample around the obstacles [@c14], [@c15], others use heuristic based strategies to trace or locate key samples [@c9]. Even though these techniques generalize to a large set of problems, they suffer from placing samples in regions where a path is unlikely to traverse. Also, owing to the huge number of collision checks performed, their computation time increases rapidly with increase in dimensionality of the state space.

Recent approaches use learning models for non-uniform sampling. [@c1]-[@c6]. Some of them propose to find low dimensional structure in planning [@c1], [@c2]. In particular, generative models like conditional variational autoencoder (CVAE) [@c19] have been used to great success. We use the CVAE used in LEGO [@c1] (called [LEGO$-$CVAE]{.smallcaps} hereon) as our underlying learning model in [GenerateCriticalSources]{.smallcaps} and provide a gist of the same below. Note that, although our work uses the model used in LEGO, it can be extended to work with any other learning framework that predicts samples in bottleneck regions [@c2]-[@c5].

## LEGO: Leveraging Experience using Graph Oracles

Leveraging Experience using Graph Oracles is a framework for predicting efficient roadmaps for sampling based motion planning. During training time, LEGO processes a dense graph to identify a sparse subset of key vertices. These vertices are a diverse set of nodes lying on bottleneck regions through which a near optimal path may pass. A CVAE [@c16] conditioned on the occupancy grid of the workspace, start and goal positions is then trained on these key samples. During test time, given the occupancy grid, start and goal positions, the CVAE generates these key samples which are used in conjunction with a uniform sparse graph to generate a roadmap.

## CVAE: Conditional Variational Autoencoder

The core component of the LEGO framework is a conditional variational autoencoder (CVAE). It is an extension of traditional variational autoencoder and has been increasingly used to learn low dimensional structure in planning. The addition of conditional parameters helps embed the features of a planning problem as conditions and learn the corresponding representations.

Let $\mathcal{X}$ be the state space and $x\in \mathcal{X}$, $z\in$ $\mathbb{R} ^ L$ be the latent random variable and $y\in$ $\mathbb{R}^m$ be the conditioning variable. The framework comprises of two *deterministic mappings* - an *encoder* and a *decoder*. An encoder maps $(x, y)$ to a mean and variance value of a Gaussian $q_\phi(z| x, y)$ in latent space, such that it is "close" to a standard Gaussian $\mathcal{N}(0, I)$. The decoder maps this Gaussian and $y$ to a distribution in the output space $p_\theta(x| z, y)$. This is achieved by maximizing the following function $\mathcal{L}\left( x, y; \theta, \phi\right)$: $$\begin{equation}
\label{eq:cvae_loss}
	  -D_{KL}\left( q_\phi(z| x, y) \, || \, \mathcal{N}(0, I) \right) + \frac{1}{L} \sum_{l=1}^{L} \log p_\theta(x| y, z^{(l)})
\end{equation}$$ At test time, we use only the decoder to map samples from an isotropic Gaussian in the latent space to samples in the output space. The CVAE is trained by passing in a dataset $\mathcal{D}= \{ X_i, y_i \}_{i=1}^{D}$. $y_i$ is the conditional parameter vector extracted from the planning problem. In our case it's (start, goal, occupancy grid). $X_i$ is the desired set of nodes extracted from the dense graph $G_{\mathrm{dense}}$ that we want our learner to predict. Hence we train the model by maximizing the following objective. $$\begin{equation}
	\mathcal{R}(\mathcal{D}; \theta, \phi) = \frac{1}{\left|\mathcal{D} \right|} \sum_{i=1}^{\left|\mathcal{D} \right|} \sum_{j=1}^{\left|X_i \right|} \mathcal{L}\left( x_j, y_i; \theta, \phi\right)
\end{equation}$$

# Problem Formulation

Let $\mathcal{X}$ denote a $d-$dimensional configuration space. Let $\mathcal{X}_{\mathrm{obs}}$ $\subseteq$ $\mathcal{X}$ be the portion in collision and $\mathcal{X}_{\mathrm{free}}= \mathcal{X}\setminus \mathcal{X}_{\mathrm{obs}}$ denote the free space. Let a path $\xi: [0, 1] \rightarrow \mathcal{X}$ be a continuous mapping from index to configurations. A path $\xi$ is said to be collision free if $\xi(\tau) \in \mathcal{X}_{\mathrm{free}}$ for all $\tau\in [0, 1]$.

**Problem:** Given a *motion planning problem* $\Lambda= \left\lbrace x_{s}, x_{g}, \mathcal{X}_{\mathrm{free}}\right\rbrace$ where $x_{s}\in \mathcal{X}_{\mathrm{free}}$ is the start configuration and $x_{g}\in \mathcal{X}_{\mathrm{free}}$ is the goal configuration, find a *feasible* $\xi$ i.e. $\xi$ that is collision free, $\xi(0)=x_{s}$ and $\xi(1)=x_{g}$.

Given a database of prior worlds, the overall goal is to use a conjunction of a learned policy and local sampling based planners to generate a roadmap $G$ which is used by a graph search algorithm $\textsc{Alg}$ to efficiently compute a feasible path. $\textsc{Alg}$, given a graph $G$, finds and returns a feasible path $\xi$. If no feasible path exists in the graph, $\textsc{Alg}$ returns $\emptyset$. An ideal roadmap should be sparse enough for $\textsc{Alg}$ to be efficient. In addition, for problems with narrow passages (bottleneck regions), this roadmap must have a set of critical samples in the bottleneck regions to ensure existence of a feasible path.

We assume the graphs to be undirected for simplicity. However, it can easily be extended to directed graphs. The following are the additional notations used in this paper:

- $G_{\mathrm{sparse}}$ : A sparse graph embedded in the state space of the robot. It is additionally composed with the set of samples generated from the learner and local planners while constructing $G$ by $\textsc{LCS$-$RRT}$ to ensure a minimal coverage.

- $\textsc{\ensuremath{\mathcal{CS}}}$ : Set of critical sources.

# Approach

We propose to identify the location of bottleneck regions using [GenerateCriticalSources]{.smallcaps} and then use [LCS$-$RRT]{.smallcaps} or [CS$-$RRT]{.smallcaps} to navigate through these bottlenecks using local sampling based planners instead of learning their local structures.

::: algorithm
$\textsc{CandidateCS}\gets \textsc{LEGO-Global}$ $\textsc{\ensuremath{\mathcal{CS}}}\gets \emptyset$ isNear $\gets$ false isNear $\gets$ true free_count $\gets$ 0 total_count $\gets$ 0 free_count $\gets$ free_count $+$ 1 total_count $\gets$ total_count $+$ 1 $\textsc{\ensuremath{\mathcal{CS}}}\gets \textsc{\ensuremath{\mathcal{CS}}}$ $\cup$ sample
:::

## Critical Source Generation

$\textsc{GenerateCriticalSources}$ identifies the locations of bottleneck regions by generating [$\mathcal{CS}$]{.smallcaps}, a set of critical samples, one corresponding to each bottleneck region. It uses $\textsc{LEGO$-$CVAE}$ as the underlying learner. If an occupancy grid of a certain size is required to learn the locations of the bottleneck regions along with their local structures, we argue that we can preprocess this occupancy grid with a kernel to create a grid of lower dimensions that encodes only the information necessary to learn the locations of the bottleneck regions. The choice of kernel depends on the features of the environment. For example, a dilation kernel can be used in environments which contain extended narrow passages. As we do not expect $\textsc{LEGO$-$CVAE}$ to learn the local structures, there is no loss of relevant information.

This preprocessed occupancy grid is then used for training and testing $\textsc{LEGO$-$CVAE}$. We call the $\textsc{LEGO$-$CVAE}$ trained with this preprocessed occupancy grid $\textsc{LEGO-Global}$ as it only learns global information of the planning problem.

We thus use $\textsc{LEGO-Global}$ for generating a set of candidate critical source samples. A sample from this set $\in \textsc{\ensuremath{\mathcal{CS}}}$ if (a) it is at least a distance $source\_sep$ away from all the critical sources generated up till now (Lines 4-8, Algorithm 1) and (b) if we connect the sample to the vertices of $G_{\mathrm{sparse}}$ that are within distance $r\_critical$ by edges, the percentage of edges not in collision with the obstacles must be smaller than a certain $threshold$ (Lines 9-17), Algorithm 1).

::: algorithm
$\textsc{\ensuremath{\mathcal{CS}}}\gets \textsc{GenerateCriticalSources}(\Lambda,G_{\mathrm{sparse}})$ $\textsc{\ensuremath{\mathcal{CS}}}\gets \textsc{\ensuremath{\mathcal{CS}}}$ $\cup$ {start,goal} $G\gets G_{\mathrm{sparse}}$ $\cup$ $\textsc{\ensuremath{\mathcal{CS}}}$ $\textsc{\ensuremath{\mathcal{T}}}= \{ \textsc{\ensuremath{\mathcal{T}}}_{1} = \{\textsc{\ensuremath{\mathcal{CS}}}_{1}\}, \cdots, \textsc{\ensuremath{\mathcal{T}}}_{N} = \{\textsc{\ensuremath{\mathcal{CS}}}_{|\textsc{\ensuremath{\mathcal{CS}}}|}\}\}$ $\textsc{\ensuremath{\mathcal{LG}}}= \{ \textsc{\ensuremath{\mathcal{LG}}}_{1} = \{\textsc{\ensuremath{\mathcal{CS}}}_{1}\}, \cdots, \textsc{\ensuremath{\mathcal{LG}}}_{N} = \{\textsc{\ensuremath{\mathcal{CS}}}_{|\textsc{\ensuremath{\mathcal{CS}}}|}\}\}$ $r \gets r\_init$ $\textsc{\ensuremath{\mathcal{LG}}}$$\gets$[ExpandLocalGraphs]{.smallcaps}($\Lambda,G,\textsc{\ensuremath{\mathcal{LG}}},\textsc{\ensuremath{\mathcal{T}}},r$) ($\textsc{\ensuremath{\mathcal{LG}}},\textsc{\ensuremath{\mathcal{T}}}$)$\gets$[DensifyLocalGraphs]{.smallcaps}($\textsc{\ensuremath{\mathcal{LG}}},\textsc{\ensuremath{\mathcal{T}}},r$) $G\gets G$ $\cup$ $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ $\xi$ = $\textsc{Alg}(G,\Lambda)$ r $\gets \lambda$ r
:::

::: algorithm
sp $\gets \emptyset$;\
sp $\gets$ sp $\cup$ {node} $\textsc{\ensuremath{\mathcal{LG}}}_{i} \gets \textsc{\ensuremath{\mathcal{LG}}}_{i}$ $\cup$ $\textsc{Subgraph}$($G$,sp) $\textsc{\ensuremath{\mathcal{LN}}}$ $\gets$ $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ - [ConnComp]{.smallcaps}($\textsc{\ensuremath{\mathcal{LG}}}_{i}$,$\textsc{\ensuremath{\mathcal{T}}}_{i}$) $\textsc{\ensuremath{\mathcal{LN}}}$ $\gets$ $\textsc{\ensuremath{\mathcal{LN}}}$ - [ConnComp]{.smallcaps}($\textsc{\ensuremath{\mathcal{LG}}}_{i}$,node) $\textsc{\ensuremath{\mathcal{LG}}}_{i} \gets \textsc{\ensuremath{\mathcal{LG}}}_{i}$ $\cup$ {edge(node,v)}
:::

::: algorithm
$\textsc{\ensuremath{\mathcal{LN}}}$$\gets$$\textsc{\ensuremath{\mathcal{LG}}}_{i}$ -$\textsc{ConnComp}$($\textsc{\ensuremath{\mathcal{LG}}}_{i}$,$\textsc{\ensuremath{\mathcal{T}}}_{i}$) rn $\gets$ [RandomNode]{.smallcaps}($\textsc{\ensuremath{\mathcal{CS}}}_{i}$,$r$) nn $\gets$ [NearestVertex]{.smallcaps}($\textsc{\ensuremath{\mathcal{T}}}_{i}$,rn) rn'$\gets$ [Interpolate]{.smallcaps}(nn, rn, step_size) $\textsc{\ensuremath{\mathcal{T}}}_{i} \gets \textsc{\ensuremath{\mathcal{T}}}_{i}$ $\cup$ {rn',edge(rn',nn)} $\textsc{\ensuremath{\mathcal{LG}}}_{i} \gets \textsc{\ensuremath{\mathcal{LG}}}_{i}$ $\cup$ {rn',edge(rn',nn)} $\textsc{\ensuremath{\mathcal{LN}}}$$\gets$ $\textsc{\ensuremath{\mathcal{LN}}}$ - $\textsc{ConnComp}$($\textsc{\ensuremath{\mathcal{LG}}}_{i}$,n) $\textsc{\ensuremath{\mathcal{LG}}}_{i} \gets \textsc{\ensuremath{\mathcal{LG}}}_{i}$ $\cup$ {edge(rn',n)}
:::

## Local Critical Source - RRT

Local Critical Source - RRT (LCS-RRT) uses [GenerateCriticalSources]{.smallcaps} to get [$\mathcal{CS}$]{.smallcaps} and adds the start and goal vertices to it. It builds $G$, which contains $G_{\mathrm{sparse}}$ and $\textsc{\ensuremath{\mathcal{CS}}}$. For each $\textsc{\ensuremath{\mathcal{CS}}}_{i}$, the algorithm maintains two graphs: a tree $\textsc{\ensuremath{\mathcal{T}}}_{i}$ and a local graph $\textsc{\ensuremath{\mathcal{LG}}}_{i}$. $\textsc{\ensuremath{\mathcal{T}}}_{i}$ is RRT rooted at $\textsc{\ensuremath{\mathcal{CS}}}_{i}$. $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ consists of edges and vertices of $G$ within distance $r$ from $\textsc{\ensuremath{\mathcal{CS}}}_{i}$. The goal of the algorithm is to make $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ completely connected by adding edges between the vertices of $\textsc{\ensuremath{\mathcal{T}}}_{i}$ and the vertices of $\textsc{\ensuremath{\mathcal{LG}}}$ not belonging to the connected component of $\textsc{\ensuremath{\mathcal{CS}}}_{i}$.

Initially, for each $\textsc{\ensuremath{\mathcal{CS}}}_{i}$, both $\textsc{\ensuremath{\mathcal{T}}}_{i}$ and $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ contain only $\textsc{\ensuremath{\mathcal{CS}}}_{i}$. In an iteration of the outer while loop of LCS-RRT (Line 7, Algorithm 2), $\textsc{ExpandLocalGraphs}$ expands each $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ to radius $r$. After expansion, these $\textsc{\ensuremath{\mathcal{LG}}}{i}$ consist of the subgraph of $G$ within a radius $r$ of $\textsc{\ensuremath{\mathcal{CS}}}_{i}$ (Line 6, Algorithm 2a). $\textsc{ExpandLocalGraphs}$ and $\textsc{DensifyLocalGraphs}$ both maintain $\textsc{\ensuremath{\mathcal{LN}}}$, a set of vertices of the $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ that does not belong to the connected component of $\textsc{\ensuremath{\mathcal{CS}}}_{i}$. Wherever possible, the nodes of $\textsc{\ensuremath{\mathcal{T}}}_{i}$, are connected to $\textsc{\ensuremath{\mathcal{LN}}}$ by collision free edges and $\textsc{\ensuremath{\mathcal{LN}}}$ is updated (Lines 8-12, Algorithm 2a). $\textsc{DensifyLocalGraphs}$ densifies the local graph by growing its $\textsc{\ensuremath{\mathcal{T}}}_{i}$ and adding edges between its $\textsc{\ensuremath{\mathcal{T}}}_{i}$ and the vertices of the set $\textsc{\ensuremath{\mathcal{LN}}}$ until either the $\textsc{\ensuremath{\mathcal{LG}}}_{i}$ is completely connected or M (hyperparameter) iterations have taken place, whichever is earlier. To grow its $\textsc{\ensuremath{\mathcal{T}}}_{i}$, $\textsc{DensifyLocalGraphs}$ samples a random node within a radius $r$ of $\textsc{\ensuremath{\mathcal{CS}}}_{i}$, interpolates it to within a distance of step_size of the vertex nearest to this node in its $\textsc{\ensuremath{\mathcal{T}}}_{i}$ and, if possible, joins them with an edge in a similar fashion to RRT growth (and therefore the name) (Lines 5-10 Algorithm 2a). It then tries to connect this new node of $\textsc{\ensuremath{\mathcal{T}}}_{i}$ with the vertices of $\textsc{\ensuremath{\mathcal{LN}}}$ and wherever a connection is possible, $\textsc{\ensuremath{\mathcal{LN}}}$ is updated (Lines 12-15 Algorithm 2b). After densification, $\textsc{\ensuremath{\mathcal{LG}}}$ is added to $G$ and $\textsc{Alg}$ is run on G (Lines 10-12 Algorithm 2). If successful, the feasible $\xi$ is returned. Else, the radius $r$ is increased by a factor $\lambda$ and the process is repeated again and so on.

*Probabilistic Completeness:* Let us consider the local graph $\textsc{\ensuremath{\mathcal{LG}}}_{s}$ at start node $\textsc{\ensuremath{\mathcal{CS}}}_{s}$ at infinite time. As time approaches infinity, so does the radius $r$. Thus, the goal node is present in the $\textsc{\ensuremath{\mathcal{LG}}}_{s}$. As we try to connect $\textsc{\ensuremath{\mathcal{CS}}}_{s}$ to all nodes not present in the connected component of $\textsc{\ensuremath{\mathcal{CS}}}_{s}$ using $\textsc{\ensuremath{\mathcal{T}}}_{s}$, we are at the least running a RRT from start node to goal node. Thus, due to the probabilistic completeness of RRT, $\textsc{LCS$-$RRT}$ is probabilistically complete.

## Critical Source - RRT

Critical Source - RRT (CS-RRT) uses [GenerateCriticalSources]{.smallcaps} to get $\textsc{\ensuremath{\mathcal{CS}}}$ and adds them to $G$. It then adds start and goal vertices to $G$. These nodes subsequently act as the roots of the RRTs we will grow. In each iteration of the outer while loop (Line 3, Algorithm 3), the algorithm iterates through the connected components present in $G$ i.e. the RRTs in a round robin manner. In lines 5-10, the algorithm samples a random node, interpolates it to within a distance of $step\_size$ of the vertex nearest to this node in its RRT and loops until it is possible to join them with an edge. This is similar to how a RRT grows (and therefore the name). In lines 11-13 it then tries to connect the new_node of its tree to the nearest vertices of the other trees that lie within a distance of $step\_size$. If a connection is possible, an edge is inserted into the graph (line 14). Insertion of this edge results in merger of the two trees the nodes belonged to. The algorithm returns a feasible path when the start and goal nodes belong to the same connected component of $G$ (Lines 15-17).

*Probabilistic Completeness:* As $\textsc{CS$-$RRT}$ grows RRTs rooted at start and goal nodes along with the critical sources to connect the start and goal nodes, it runs a RRT-Connect at the least. Thus, due to the probabilistic completeness of RRT-Connect, $\textsc{CS$-$RRT}$ is probabilistically complete.

::: algorithm
$G\gets \textsc{GenerateCriticalSources}(\Lambda,G_{\mathrm{sparse}})$ $G\gets G$ $\cup$ {start,goal} rn $\gets$ [RandomNode]{.smallcaps} nn $\gets$ [NearestVertex]{.smallcaps}($G_{i}$,rn) rn'$\gets$ [Interpolate]{.smallcaps}(nn, rn, $step\_size$) $G\gets$ $\cup$ {rn',edge(rn',nn)} onn $\gets$ [NearestVertex]{.smallcaps}($G_{j}$,rn') $G\gets G$ $\cup$ {edge(rn',onn)} $\xi$ = $\textsc{Alg}(G,\Lambda)$
:::

# Experiments

In this section, we compare the performance of LCS-RRT and CS-RRT to sampling based algorithms in multiple domains. We evaluate our algorithms against RRT-Connect[@c18], a variation of RRT that incrementally builds two trees rooted at the start and goal nodes. Additionally, we compare our algorithms with LEGO, a state-of-the-art learning based sampling algorithm.

:::: {.figure latex-placement="!ht"}
![](Jenamani2020Robotic_figs/LEGO_cvae_500.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/LEGO_global_30.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/lego_cvae_30.png){width="\\textwidth"}

::: caption
\(a\) [LEGO$-$CVAE]{.smallcaps} fails to cover the local structure of the bottleneck regions even with a large number of samples. (b) [LEGO-Global]{.smallcaps} is able and (c) [LEGO$-$CVAE]{.smallcaps} is unable to place at least one sample per bottleneck region with a small number of samples. Trained with a preprocessed grid, [LEGO-Global]{.smallcaps} is robust to fine changes in local structures.
:::
::::

As LEGO is a graph based approach while others are tree based approaches, we adapted LEGO to an anytime algorithm with incremental densification for testing purposes. We have tuned the parameters of RRT-Connect and LEGO to ensure their best performance.

#### Evaluation Procedure

For a given planning problem, we run each algorithm with a fixed timeout. For a given problem domain, each of the learning models used by these algorithms are trained on similar number of planning problems. We evaluate the performance of these algorithms on the metric of time taken to find a feasible path.

#### Problem Domains

We evaluate our algorithms on $\mathbb{R}^2$ and $\mathbb{R}^7$ problem domains. The $\mathbb{R}^2$ problems have random rectilinear walls with extruded narrow passages that have varying local structures (Fig 3). The $\mathbb{R}^7$ problem is a robotic-arm manipulation problem in a cluttered environment.

#### Experiment Details

We compare the algorithms $\textsc{LCS$-$RRT}$, $\textsc{CS$-$RRT}$, LEGO and RRT-Connect on a testset of 100 planning problems. For the $\mathbb{R}^2$ problems, each learning model is trained on 4000 planning problems for around 30 minutes. The planning timeout for the algorithms is 5 seconds. The size of occupancy grid used by $\textsc{LEGO$-$CVAE}$ is 50X50. The kernel used by $\textsc{LEGO-Global}$ for preproccessing is of size 5X5 (with stride value 5) resulting in an updated occupancy grid of size 10X10 (Fig 5). For the $\mathbb{R}^7$ problems, each learning model is trained on 4000 training problems for 2 hours and the planning timeout for the algorithms is 12 seconds. The code is open sourced and can be found at <https://github.com/RKJenamani/CS-RRT>.

**Observation 1.** *[LCS$-$RRT]{.smallcaps} and [CS$-$RRT]{.smallcaps} outperform the sampling based baselines LEGO and RRT-Connect.*\
Fig 4 shows the performance of $\textsc{CS$-$RRT}$, $\textsc{LCS$-$RRT}$, LEGO and RRT-Connect on $\mathbb{R}^2$ and $\mathbb{R}^7$ problem domains. $\textsc{LCS$-$RRT}$ performs better than $\textsc{CS$-$RRT}$ in $\mathbb{R}^2$. However in $\mathbb{R}^7$, where the size of $G_{\mathrm{sparse}}$ becomes large to ensure coverage of the high dimensional space and collision checking is computationally expensive, $\textsc{CS$-$RRT}$ performs better.\
**Observation 2.** *[LEGO$-$CVAE]{.smallcaps} is unable to cover the local structure of the bottleneck regions even with a large number of samples. Also, with a few number of samples, [LEGO-Global]{.smallcaps} is able to place a sample at each bottleneck region while [LEGO$-$CVAE]{.smallcaps} is not (Fig 2)*.

:::: {#fig:envs .figure latex-placement="!ht"}
![](Jenamani2020Robotic_figs/lego_global_run.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/critical_sources_run.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/csrrt_run.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/lcsrrt_run.png){width="\\textwidth"}

::: caption
\(a\) Samples predicted by [LEGO-Global]{.smallcaps}(green) on the $\mathbb{R}^2$ environment. (b) Critical Sources (Pink) selected by [GenerateCriticalSources]{.smallcaps}. (c) Path (Red) found by [CS$-$RRT]{.smallcaps}(d) Path (Red) found by [LCS$-$RRT]{.smallcaps}
:::
::::

:::: {.figure latex-placement="!ht"}
![](Jenamani2020Robotic_figs/2d.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/7d.png){width="\\textwidth"}

::: caption
Comparison of CS-RRT, LCS-RRT, RRT-Connect and LEGO for (a) $\mathbb{R}^2$ and (b) $\mathbb{R}^7$ problem domains
:::
::::

:::: {.figure latex-placement="!ht"}
![](Jenamani2020Robotic_figs/50_50.png){width="\\textwidth"}

![](Jenamani2020Robotic_figs/10_10.png){width="\\textwidth"}

::: caption
Convolving with a kernel of size 5X5 on (a) an occupancy grid of size 50 by 50, we are able to extract (b) a 10 by 10 occupancy grid with global features. This approach is similar to the method of dilation used in image processing.
:::
::::

# Conclusion

We show the feasibility of using local sampling algorithms aided by a learning model to rapidly find a feasible path in complex environments containing extended bottleneck regions. These algorithms share the responsibility of generating key samples between the learner and the local sampler. This lets the learning model converge faster to generalizing well over planning problems that have similar global structure for the location of bottleneck regions but different local structures within these regions. As we require the learner to only identify the location of bottleneck regions, we introduce the idea of using a kernel to preprocess the occupancy grids for better learning. In future works, we would like to analyse the relationship between a workspace and the kernel suitable to it. We intend to explore the integration of other sampling based methods to make the approach asymptotically optimal. We would also like to test our algorithms on environments where extended bottleneck regions arise due to differential constraints.

::: thebibliography
99

R. Kumar, A. Mandalika, S. Choudhury, and S. S. Srinivasa, "LEGO: Leveraging experience in roadmap generation for sampling-based planning", in IROS 2019. B. Ichter, J. Harrison, and M. Pavone, "Learning sampling distributions for robot motion planning", in ICRA 2018. B. Ichter, E. Schmerling, T.-W. E. Lee, and A. Faust, \"Learned Critical Probabilistic Roadmaps for Robotic Motion Planning\", arXiv preprint arXiv:1910.03701, 2019. C. Chamzas, A. Shrivastava, Lydia E. Kavraki, \"Using Local Experiences for Global Motion Planning\", in ICRA 2019. Daniel Molina, Kislay Kumar, Siddharth Srivastava, "Learn and Link: Learning Critical Regions for Efficient Planning," in ICRA 2020. S.R. Koukuntla, M. Bhat, S. Aggarwal, R. K. Jenamani, and J. Mukhopadhyay, \"Deep Learning rooted Potential piloted RRT\* for expeditious Path Planning\", in CACRE 2019. D. Hsu, J.-C. Latombe, and R. Motwani, \"Path planning in expansive configuration spaces\", in International Journal Computational Geometry and Applications, 4:495--512, 1999. L. Janson, B. Ichter, and M. Pavone, \"Deterministic sampling-based motion planning: Optimality, complexity, and performance\", arXiv preprint arXiv:1505.00023, 2015. Christopher Holleman and Lydia E. Kavraki, \"A framework for using the workspace medial axis in PRM planners\", in ICRA 2000. D. Hsu, G. Sánchez-Ante, and Z. Sun, \"Hybrid prm sampling with a cost-sensitive adaptive strategy\", in ICRA 2005. Brendan Burns and Oliver Brock, \"Sampling-based motion planning using predictive models\", in ICRA 2005. D. Hsu, J. Latombe, and H. Kurniawati, \"On the probabilistic foundations of probabilistic roadmap planning\", in IJRR 2006. H. Kurniawati and D. Hsu, \"Workspace-based connectivity oracle: An adaptive sampling strategy for prm planning\" in Algorithmic Foundation of Robotics VII, pages 35--51. Springer, 2008. Valérie Boor, Mark H. Overmars, and A. Frank Van Der Stappen, \"The gaussian sampling strategy for probabilistic roadmap planners\" in ICRA 1999. D. Hsu, T. Jiang, J. Reif, and Z. Sun, \"The bridge test for sampling narrow passages with probabilistic roadmap planners\", in ICRA 2003. Diederik P. Kingma and Max Welling, \"Auto-encoding variational bayes\", arXiv preprint arXiv:1312.6114, 2013 S. M. LaValle, \"Rapidly-exploring random trees: A new tool for path planning\". TR 98-11, Computer Science Dept., Iowa State Univ. \<http://janowiec.cs.iastate.edu/papers/rrt.ps\>, Oct. 1998. J. Kuffner and S. M. LaValle, \"RRT-connect: An efficient approach to single-query path planning", in ICRA 2000. Carl Doersch, \"Tutorial on variational autoencoders\", arXiv preprint arXiv:1606.05908, 2016.
:::

[^1]: \*All four authors contributed equally to this research.

[^2]: $^{1}$Indian Institute of Technology Kharagpur { rkj, vernwalrahul, parthmall, kushal.k }@iitkgp.ac.in
