---
citation_key: Soleymanzadeh2026GAIDE
arxiv_id: 2603.04463
arxiv_url: https://arxiv.org/abs/2603.04463
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:51:09Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Motion Planning, Neural Informed Sampling, Transformers, Attention Mask
:::

# Introduction

Motion planning for robotic manipulators aims to find a feasible, collision-free path that connects a start and goal configuration in a high-dimensional configuration space [@soleymanzadeh2026towards]. A broad class of algorithms has been developed to address this problem [@soleymanzadeh2026towards]. Among them, probabilistically complete sampling-based motion planners have demonstrated strong performance for robotic manipulators with high-dimensional configuration spaces due to their scalability [@lavalle2006planning].

Sampling-based motion planning algorithms construct a tree toward the planning goal by iteratively (1) sampling configurations within the configuration space, (2) steering towards these samples, and (3) collision checking such connections [@lavalle2006planning]. These planners either rely on uniform sampling [@lavalle1998rapidly] or hand-crafted informed samplers for sample generation [@strub2020adaptively]. However, uniform sampling is computationally inefficient in high-dimensional spaces, while hand-crafted informed samplers are often sensitive to initialization and difficult to design for high-dimensional configuration spaces [@soleymanzadeh2025simpnet].

:::: {#fig_1- simpt_overview .figure latex-placement="t"}
![](Soleymanzadeh2026GAIDE_figs/01OpeningImage.png){width="39%"}

::: caption
**An overview of GAIDE**: the proposed neural informed sampler constructs a graph that represents both the robotic manipulator embodiment and the spatial relationships inherent within the motion planning problem. The adjacency matrix of this graph is incorporated into a transformer-based neural sampler via attention masking to enable spatial- and embodiment-aware informed sampling. The framework is embedded within sampling-based planners as an informed sampler and demonstrates superior performance compared to benchmark neural samplers, MPNets [@qureshi2020motion] and SIMPNet [@soleymanzadeh2025simpnet].
:::
::::

:::: {#fig_2- graphconstruction .figure latex-placement="htbp"}
![](Soleymanzadeh2026GAIDE_figs/02GraphConstruction.png){width="40%"}

::: caption
**Graph Construction**: an illustration of spatial and embodiment graph. An undirected graph is constructed over the downsampled manipulator point cloud to implicitly encode the manipulator's kinematics chain, while a directed graph connects the downsampled workspace point cloud to the robot nodes to capture the inherent spatial relationships within the motion planning problem. "PCD" denotes point cloud and "PointNet++" is set abstraction layers from PointNet++ [@{qi2017pointnet++}].
:::
::::

Recent advances in neural motion planning aim to improve sampling efficiency by learning informed sampling distributions from planning datasets. These approaches train neural samplers on oracle-generated paths to bias sampling toward promising regions [@qureshi2020motion]. Despite their success, most existing neural samplers do not encode the spatial structure of the planning space or the robotic manipulator's embodiment [@zang2022robot]. To address this challenge, SIMPNet [@soleymanzadeh2025simpnet] introduced an embodiment-aware informed sampler by constructing a graph over the manipulator embodiment, and leveraging message-passing graph neural networks (GNNs) [@battaglia2018relational] for informed sampling. However, GNNs often struggle to capture the long-range interactions and dependencies inherent within motion planning due to representation oversmoothing and oversquashing in deep message-passing networks [@alon2020bottleneck].

In this work, we introduce GAIDE, a spatial- and embodiment-aware neural motion planner that encodes both kinematic and planning space structure. GAIDE constructs a unified graph that represents (1) the manipulator's kinematics structure and (2) the spatial relationship between robot and planning environment. Instead of relying on message passing, we integrate this graph into a transformer-based neural sampler by incorporating the graph adjacency matrix as an attention mask [@sferrazza2024body]. This structured attention mechanism constrains information flow according to the underlying planning structure while preserving the transformer's ability to model long-range dependencies. Embedded within a bidirectional sampling-based planner [@qureshi2020motion], GAIDE reduces planning time and enhances success rate compared to state-of-the-art planners using uniform sampling, hand-crafted informed sampling, and neural informed sampling.

The main contributions of this work are:

- We construct a graph that captures both the kinematic structure of the manipulator and the spatial structure of the planning scene. This graph is incorporated into a transformer-based neural sampler through structured attention masking, enabling spatial- and embodiment-aware informed sampling.

- We evaluate GAIDE across diverse held-out planning tasks and benchmark it against state-of-the-art sampling-based planners using uniform, heuristic-based, and neural informed sampling strategies, in terms of planning time, path cost, and success rate.

This paper is organized as follows: Section [2](#sec: relatedwork){reference-type="ref" reference="sec: relatedwork"} reviews related work in manipulator motion planning. Section [3](#sec: simpt){reference-type="ref" reference="sec: simpt"} presents the GAIDE framework. Section [4](#sec: discussions){reference-type="ref" reference="sec: discussions"} presents the evaluation results and comparisons with the benchmark planners. Section [5](#sec: conclusions){reference-type="ref" reference="sec: conclusions"} concludes the paper.

# Related Works {#sec: relatedwork}

In this section, we review prior work in robotic manipulator motion planning and highlight the key distinctions between GAIDE and existing approaches.

**Robotic manipulator motion planning.** Decades of research have led to a wide range of motion planning algorithms for robotic manipulators, most notably sampling-based [@lavalle1998rapidly; @strub2020adaptively] and trajectory optimization algorithms [@mukadam2016gaussian]. Sampling-based algorithms construct a tree connecting the start and goal configurations by uniformly or inform sampling the configuration space. Trajectory optimization algorithms subject an initial, often in-collision, path to planning constraints such as collision avoidance and path smoothness. However, the uniform [@lavalle1998rapidly] and hand-crafted informed [@strub2020adaptively] samplings of sampling-based algorithms are sample inefficient for high DOF robotic manipulators operating in cluttered workspaces [@soleymanzadeh2025simpnet]. Trajectory optimization algorithms are highly sensitive to the initial guess and may get stuck in local minima [@ichnowski2020deep]. GAIDE addresses these challenges by incorporating the kinematic and spatial structure of the planning problem to remedy the sample inefficiency of sampling-based planners with informed sample generation. In addition, GAIDE spatial-informed initial trajectories can be potentially used to warm-start trajectory optimization algorithms to reduce sensitivity to local minima.

:::: {#fig_3- simptstructure .figure latex-placement="htbp"}
![](Soleymanzadeh2026GAIDE_figs/03GAIDE.png){width="80%"}

::: caption
**GAIDE network architecture:** The framework leverages current-time-step workspace information (including the workspace and robot point clouds) together with configuration space features (current-time-step and goal configuration) to generate an informed sample that guides the robotic manipulator toward the motion planning goal. $\mathbf{q}_t,~\mathcal{P}_r$, and $\mathbf{q}_{\text{goal}}$ are the current time-step configuration, current-time step robotic manipulator point cloud, and motion planning goal configuration, respectively. $\mathbf{z}_t$, $\mathbf{z}_{\text{goal}}$, $\mathbf{z}_r$, $\mathbf{z}_w$, and $\delta \mathbf{q}_t$ are the current time-step configuration, planning goal configuration, robot point cloud, scene point cloud embeddings, and predicted joint angle, respectively. "PointNet++" denotes set abstraction layers from PoinNet++ [@{qi2017pointnet++}].
:::
::::

**Neural motion planning for robotic manipulators.** Recent advances in deep learning have enabled neural approaches for motion planning, either as end-to-end planners [@dalal2024neural; @yang2025deep; @soleymanzadeh2025perfact], or as learned components integrated into classical motion planning algorithms. Within sampling-based planners, neural networks have been used as informed samplers [@qureshi2020motion], and implicit collision checkers [@kim2022graphdistnet], while in trajectory optimization algorithms, they have been employed to encode the planning distribution to warm-start trajectory optimization [@carvalho2023motion]. However, most existing approaches struggle to capture the manipulator embodiment and spatial structure inherent within the motion planning problems. GAIDE explicitly models these structures through a graph representation and embeds them directly into the neural sampler via attention masking.

**Spatial-informed neural planning for robotic manipulators.** A growing line of work seeks to explicitly model spatial relationships within planning problems using graph representations. GNNs provide a natural framework for processing structured data and have been applied to informed sampling [@soleymanzadeh2025simpnet], edge evaluation [@yu2021reducing], and collision checking [@kim2022graphdistnet]. These methods construct graphs to encode geometric or kinematic structure and rely on message passing to propagate relational information [@battaglia2018relational]. However, GNNs often struggle to model long-term interactions and dependencies due to representation oversmoothing and overquashing in deep message passing networks [@alon2020bottleneck]. To overcome this limitation, GAIDE encodes the graph constructed based on the manipulator embodiment and planning spatial structure directly into the planning network via attention masking to enable efficient motion planning.

# Graph-based Attention Masking for Spatial- and Embodiment-aware Motion Planning (GAIDE) {#sec: simpt}

In this section, we introduce GAIDE, a neural informed sampler that encodes both the manipulator embodiment and spatial structure within planning problems to improve the performance of sampling-based motion planning algorithms for high DOF robotic manipulators. Figure [3](#fig_3- simptstructure){reference-type="ref" reference="fig_3- simptstructure"} demonstrates the structure of GAIDE.

## Motion Planning Definition

Let the configuration space of an $n$-DOF robotic manipulator be denoted as $\mathcal{C} \in \mathbb{R}^n$ spanned by its joint values. The obstacle and free configuration spaces are defined as $\mathcal{C}_{obs} \subset \mathcal{C}$ and $\mathcal{C}_{free} = \mathcal{C} \backslash \mathcal{C}_{obs}$, respectively. The goal of the motion planning problem is to find a feasible path $\sigma = [\mathbf{q}_1, \cdots, \mathbf{q}_t, \cdots, \mathbf{q}_T]$ connecting a start configuration ($\mathbf{q}_{\text{start}} \in \mathcal{C}_{free}$) and a goal configuration ($\mathbf{q}_{\text{goal}} \in \mathcal{C}_{free}$) such that: $$\begin{equation}
 \label{ppdef}
\begin{aligned}
    \sigma(0) &= \mathbf{q}_{\text{start}}, \\
    \sigma(t) &\in \mathcal{C}_{\text{free}}, \\
    \sigma(T) &= \mathbf{q}_{\text{goal}}.
\end{aligned}
\end{equation}$$

## Planning Embodiment and Spatial Graph Representation

Let $G = (V, E)$ denote a graph, where $V$ is the set of nodes, and $E$ is the set of edges. An edge $e_{ij} \in E$ connects node $v_i \in V$ and $v_j \in V$ if they are adjacent. The adjacency matrix $A \in \mathbb{R}^{n_v \times n_v}$ is defined such that $A_{ij}=1$ if $e_{ij} \in E$ and $A_{ij}=0$ if $e_{ij} \notin E$ where $n_v$ denotes the number of nodes in the graph.

::: algorithm
**Given:** Neural sampler (GAIDE): $\pi_\theta$.\
**Given:** Start and goal configurations: $\mathbf{q}_{\text{start}}$; $\mathbf{q}_{\text{goal}}$.\
**Given:** Scene point cloud, and robot point cloud sampler: *ScenePCD*, *PCDSampler*.\
$\mathbf{q}^a \leftarrow \{\mathbf{q}_{start}\}$, $\mathbf{q}^b \leftarrow \{\mathbf{q}_{goal}\}$\
$\mathbf{q}\leftarrow \emptyset$\
*Complete* $\leftarrow$ *False*
:::

**Embodiment graph representation.** Similar to [@soleymanzadeh2025simpnet], we utilize an undirected graph to model the kinematic structure of the robotic manipulator as demonstrated in Figure [2](#fig_2- graphconstruction){reference-type="ref" reference="fig_2- graphconstruction"}. We synthetically generate a manipulator point cloud by uniformly sampling on link meshes at arbitrary configurations, and apply the PointNet++ [@{qi2017pointnet++}] set abstraction layer to downsample the point cloud. In this representation, each point corresponds to a node, and edges are defined according to the manipulator's kinematic chain, such that each node is connected to its adjacent nodes along the kinematic chain of the manipulator.

**Spatial graph representation.** We utilize set abstraction layers from PointNet++ [@{qi2017pointnet++}] to downsample the workspace point cloud. We then consider each point with the downsampled workspace point cloud as a node, and construct a directed, fully connected graph that connects every workspace node to all the nodes of the manipulator, as demonstrated in Figure [2](#fig_2- graphconstruction){reference-type="ref" reference="fig_2- graphconstruction"}.

## GAIDE Structure

Given the adjacency matrix constructed in the previous section, we now describe each component of the proposed neural informed sampler.

**Embedding robot and workspace planning information.** We utilize a shared multi-layer perceptron (MLP) to encode the current and planning goal configuration as follows: $$\begin{equation}
 \label{eq - current}
\begin{aligned}
    \mathbf{z}_t = \text{MLP}_{I}(\mathbf{q}_t),
\end{aligned}
\end{equation}$$ $$\begin{equation}
 \label{eq - goal}
\begin{aligned}
    \mathbf{z}_{goal} = \text{MLP}_{I}(\mathbf{q}_{goal}),
\end{aligned}
\end{equation}$$ where $\mathbf{q}_t \in \mathbb{R}^6$, $\mathbf{q}_{goal} \in \mathbb{R}^6$, $\mathbf{z}_t \in \mathbb{R}^H$, and $\mathbf{z}_{goal} \in \mathbb{R}^H$ are current time-step configuration, goal configuration, current time-step configuration embedding, and goal configuration embedding, respectively. Also, we utilize set abstraction layer from PointNet++ [@{qi2017pointnet++}] to downsample and embed robot and workspace point clouds as follows: $$\begin{equation}
 \label{eq - pcd_robot}
\begin{aligned}
    \mathbf{z}_r = \text{SetAbstraction}(\mathcal{P}_r),
\end{aligned}
\end{equation}$$ $$\begin{equation}
 \label{eq - pcd_scene}
\begin{aligned}
    \mathbf{z}_{w} = \text{SetAbstraction}(\mathcal{P}_w),
\end{aligned}
\end{equation}$$ where $\mathcal{P}_r \in \mathbb{R}^{N_r \times 3}$, $\mathcal{P}_w \in \mathbb{R}^{N_w \times 3}$, $\mathbf{z}_r \in \mathbb{R}^{K_r \times H}$, and $\mathbf{z}_w \in \mathbb{R}^{K_w \times H}$ are robot point cloud, scene point cloud, robot point cloud embedding, and scene point cloud embedding, respectively.

**Transformer encoder.** After encoding all planning information, we calculate robot-related information as follows: $$\begin{equation}
 \label{eq - robot}
\begin{aligned}
    \mathbf{z}_{robot} = \mathbf{z}_r + \mathbf{z}_t \otimes \mathbf{1}_{K_r} + \mathbf{z}_{goal} \otimes \mathbf{1}_{K_r},
\end{aligned}
\end{equation}$$ where $\mathbf{z}_{robot} \in \mathbb{R}^{K_r \times H}$ is robot embedding. Afterwards, we apply sinusoidal positional encoding to preserve the positional information of the transformer encoder input, since transformers are inherently agnostic to the spatial locations of their inputs [@dosovitskiy2020image].

The vanilla self-attention mechanism in transformer architectures implicitly models a fully connected graph [@vaswani2017attention]. In this work, we bias the scaled dot-product attention to incorporate manipulator embodiment and planning spatial structure as follows: $$\begin{equation}
 \label{eq - robot}
\begin{aligned}
    \text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}} + B)V,
\end{aligned}
\end{equation}$$ where $Q,~K$, and $V$ are query, key, and value matrices, respectively, with $d_k$ being the dimensionality of the key vector. The matrix $B$ is defined based on the adjacency matrix of the constructed graph from the previous section as follows: $$\begin{equation}
 \label{eq - mask}
    B_{i,j} = 
    \begin{cases}
        0, & A_{i,j} = 1 \\
        -\infty, & A_{i,j} = 0
    \end{cases},
\end{equation}$$ which is equivalent to using the adjacency matrix ($A$) as a binary mask within the attention mechanism [@sferrazza2024body]. The transformer encoder interleaves layers with masked attention with layers with unmasked attention, starting with a masked attention layer as the first layer.

**Transformer decoder.** The transformer decoder follows a standard transformer architecture and is conditioned on the transformer encoder output to predict motion planning actions. It takes as input a learnable token $\mathbf{s} \in \mathbb{R}^H$ and, using the encoder output as memory, generates a delta joint angle $\mathbf{\delta q}_t \in \mathbb{R}^6$ which is then converted into joint targets, and added to the constructed planning tree toward the goal.

## Stochasticity with Dropout

We incorporate Dropout [@srivastava2014dropout] into the GAIDE framework to induce random sample generation during deployment. This randomness is a defining characteristic of classical sampling-based motion planning algorithms and underlies their probabilistic completeness [@lavalle2006planning]. By introducing stochasticity, each planning attempt by GAIDE may produce a different path between any given start and goal configuration.

:::: {#fig_4 - tasks .figure latex-placement="htbp"}
![](Soleymanzadeh2026GAIDE_figs/04PlanningTasks.png){width="\\linewidth"}

::: caption
An example of all held-out planning tasks from [@soleymanzadeh2025perfact].
:::
::::

## Bidirectional Planning Algorithm

We embed the proposed neural sampler into the bidirectional planning algorithm proposed by [@qureshi2020motion] to plan between given start and goal configurations. Algorithm [\[alg: simpt\]](#alg: simpt){reference-type="ref" reference="alg: simpt"} outlines the overall planning algorithm. For a detailed description of the underlying bidirectional planning algorithm, we refer the reader to Qureshi *et al.* [@qureshi2020motion].

# Results and Discussion {#sec: discussions}

In this section, we describe the implementation details of GAIDE and compare its performance with state-of-the-art sampling-based planning algorithms using uniform sampling, heuristic-based informed sampling, and neural informed sampling. All planning algorithms are implemented in PyTorch [@paszke2017automatic], and the evaluations are conducted on a computer running Linux OS, equipped with an NVIDIA RTX 4080 GPU.

:::: table*
::: center
[]{#tab: performance label="tab: performance"}
:::
::::

![Planning cost of GAIDE and baseline planners across all held-out planning tasks.](Soleymanzadeh2026GAIDE_figs/05PlanningCost.png){#fig_5 - planningcost width="90%"}

## Data Collection

We utilize the scene generation framework from [@soleymanzadeh2025perfact] to construct a diverse set of motion planning workspaces and planning problems. We then employ cuRobo [@sundaralingam2023curobo], a GPU-accelerated motion planner, to generate a dataset for training the proposed neural sampler.

:::: {#fig_7 - realdemo .figure latex-placement="t"}
![](Soleymanzadeh2026GAIDE_figs/07RealDemo.png){width="90%"}

::: caption
**Real-world deployment of GAIDE**. The path profile from the start configuration to the goal configuration is demonstrated in the real-world (top), and simulated scene point cloud (bottom) for each demo.
:::
::::

## GAIDE Training

We utilize the GAIDE parameterized by $\theta$ for informed sample generation within sampling-based planning algorithms. Let $\delta \mathbf{q}_{p,t} \in \mathbb{R}^6$ denote the ground-truth delta joint action at step $t$ along path $\mathbf{p}$ from the planning dataset $\mathcal{D} = \{\mathbf{p}_1, \cdots, \mathbf{p}_N\}$ where $\mathbf{p} = [\mathbf{q}_{p,0}, \cdots, \mathbf{q}_{p,t}, \cdots, \mathbf{q}_{p,T}]$. The loss function is defined as: $$\begin{equation}
 \label{eq - lossfn}
\begin{aligned}
    \mathcal{L}_{\text{GAIDE}} = \frac{1}{N_p}\sum_{p=1}^{N_p}\sum_{t=0}^{T_p - 1} \parallel \delta \mathbf{q}_{p, t} - \delta \hat{\mathbf{q}}_{p,t} \parallel^2,
\end{aligned}
\end{equation}$$ where $N_p$ is the batch size. The model is optimized using standard MSE loss for approximately 1M gradient steps, which requires wall-clock time of one day training on a single NVIDIA A100 GPU with a batch size of 256.

## Baselines and Metrics

**Baselines.** We evaluate the performance of GAIDE by comparing it with several state-of-the-art sampling-based motion planning algorithms. For planners using uniform sampling, we consider Bidirectional RRT (Bi-RRT) [@kuffner2000rrt] and RRT\* [@karaman2011sampling]. For heuristic-based informed sampling, we include Informed RRT\* (IRRT\*) [@gammell2014informed] and Batch Informed Trees (BIT\*) [@gammell2020batch]. All classical sampling-based algorithms are implemented using Open Motion Planning Library (OMPL) [@sucan2012open]. Since these planners lack internal termination conditions, we set the planning time for these planners to match the average planning time of GAIDE for each planning task. For neural informed sampling, we evaluate against MPNets [@qureshi2020motion], and SIMPNet [@soleymanzadeh2025simpnet]. These benchmark planners are selected to highlight the effectiveness of incorporating spatial structure and the manipulator's kinematic chain into neural-informed sampling framework. All neural informed samplers are embedded within the same bi-directional planner [@qureshi2020motion], and use the same workspace embedding network. All planners utilize PyBullet [@coumans2016pybullet] physics engine for collision checking.

**Metrics.** We evaluate GAIDE using three standard planning metrics: *planning time*, *planning cost* and *success rate*. *planning time* "T" denotes the average planning time the planner takes in each evaluation task. *Planning cost* "C" measures the length of the successfully planned paths within the configuration space. *Success rate* "S" represents the percentage of successfully planned paths.

## Evaluation Results

We utilize held-out planning environments proposed by [@soleymanzadeh2025perfact] to evaluate the performance of GAIDE against benchmark planners. Figure [4](#fig_4 - tasks){reference-type="ref" reference="fig_4 - tasks"} illustrate an example of these planning tasks. Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"} and Figures [5](#fig_5 - planningcost){reference-type="ref" reference="fig_5 - planningcost"} and [7](#fig_6 - average){reference-type="ref" reference="fig_6 - average"} report the performance of GAIDE in comparison with benchmark motion planners across these planning tasks.

![Average success rate and planning time comparison between GAIDE and benchmark planners across all held-out planning tasks.](Soleymanzadeh2026GAIDE_figs/06Average.png){#fig_6 - average width="\\linewidth"}

**GAIDE vs. uniform samplers.** Bi-RRT achieves the fastest planning time and the highest success rate across all planning tasks due to its bidirectional tree construction module. However, Bi-RRT terminates once an initial feasible solution is found, which results in suboptimal solutions and higher planning costs. Compared to GAIDE, Bi-RRT attains higher success rates and lower planning times as demonstrated in Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"}. However, it consistently exhibits the worst planning cost among benchmark planners (on average, Bi-RRT: [$16.2 {\pm} 7.05$]{.underline} vs. GAIDE: [$4.81 {\pm} 1.63$]{.underline}).

RRT\* is an asymptotically optimal planner that utilizes uniform sampling and graph rewiring to improve solution quality within the given planning time budget. However, both uniform sampling and graph rewiring modules are computationally expensive, which results in the lowest success rate among virtually all benchmark planner across all planning tasks, as demonstrated in Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"}. Moreover, under the planning time budget, RRT\* yields higher planning cost than GAIDE across all evaluation tasks (on average RRT\*: [$6.98 {\pm} 6.47$]{.underline} vs. GAIDE: [$4.81 {\pm} 1.63$]{.underline}).

**GAIDE vs. heuristic-based informed samplers.** Informed RRT\* (RRT\*) is also an asymptotically optimal planner that combines informed sampling with graph rewiring to improve solution quality within the given planning time budget. Although IRRT\* restricts the sampling to an informed subset after an initial feasible solution is found, the rewiring module remains computationally expensive. As a result IRRT\* exhibits the lowest success rate among virtually all benchmark planner across all planning tasks, as demonstrated in Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"}. Moreover, under the planning time budget, IRRT\* yields higher planning cost than GAIDE across all evaluation tasks (on average IRRT\*: [$10.9 {\pm} 6.98$]{.underline} vs. GAIDE: [$4.81 {\pm} 1.63$]{.underline}).

BIT\* is an asymptotically optimal planner that performs batch-wise, heuristic-guided search (informed) over a random geometric graph, which leads to high success rates and efficient planning times across all planning tasks, as demonstrated in Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"}. However, under the given planning budget, BIT\* yields higher planning cost than GAIDE across all evaluation tasks (on average: BIT\*: [$9.0 {\pm} 5.17$]{.underline} vs. GAIDE: [$4.81 {\pm} 1.63$]{.underline})

**GAIDE vs. neural informed samplers**: MPNets simply concatenates planning-related information as input to an MLP-based neural informed sampling, without explicitly encoding the spatial and kinematic structure inherent within the motion planning problems. As a result, MPNets exhibits lower success rate compared to GAIDE across all planning tasks, as demonstrated in Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"}. SIMPNet, on the other hand, encodes the kinematic structure of the robotic manipulator to establish kinematic-aware sampling. However, GNNs' struggle with encoding long-horizon interactions due to representation oversmoothing or overquashing leads to lower success rates compared to GAIDE across all planning tasks, as demonstrated in Table [\[tab: performance\]](#tab: performance){reference-type="ref" reference="tab: performance"}.

## Ablation Study

In this section, we compare GAIDE with its ablated variants to evaluate the contribution of attention masking to the performance of the neural sampler. These ablation frameworks are as follows:

**GAIDE-Vanilla Transformer.** Inspired by [@zhao2023learning], this framework features a standard encoder-decoder transformer architecture for predicting future informed samples given planning information. It processes current-time step planning information using a vanilla attention mechanism and does not incorporate the spatial and kinematic structure of the planning problem.

**GAIDE-Hard.** This framework utilizes the same attention mask as GAIDE, but applies it at every transformer encoder layer, instead of interleaving masked and standard attention layers.

As shown in Table [\[tab: ablations\]](#tab: ablations){reference-type="ref" reference="tab: ablations"}, GAIDE-V achieves lower success rates compared to GAIDE across all evaluated planning tasks. This performance drop is due to the fact that motion planning problem depends on the inherent spatial structure of the problem, and explicitly incorporating such spatial information into the motion planning framework improves planning efficiency.

However, incorporating the attention mask at every layer of the transformer encoder (i.e., GAIDE-H) leads to a deteriorated planning performance across all planning tasks, even compared to the ablation variant without attention masking (i.e., GAIDE-V), as demonstrated in Table [\[tab: ablations\]](#tab: ablations){reference-type="ref" reference="tab: ablations"}. This performance drop in terms of success rates can be attributed to the fact that the constructed attention mask restricts the transformer decoder's ability to fully attend to the workspace information embedding, causing some spatial information to be masked out at each encoder layer.

:::: table*
::: center
[]{#tab: ablations label="tab: ablations"}
:::
::::

## Real-world Deployment

To evaluate the performance of our planner on a physical robot, we conducted experiments in a real-world environment (Figure [6](#fig_7 - realdemo){reference-type="ref" reference="fig_7 - realdemo"}). The scene was represented using point cloud data acquired from a calibrated Intel RealSense D435i RGB-D camera. Collision checking was performed using a spherical approximation of the robot geometry. The transformation between the camera and the robot base was estimated using AprilTag markers. The results demonstrate that GAIDE generalizes effectively to real-world sensor data without additional training or fine-tuning.

# Conclusions {#sec: conclusions}

In this paper, we presented GAIDE, a neural informed sampler that can be embedded within sampling-based motion planners for efficient motion planning. We constructed a graph that represents the manipulator's kinematic chain and the spatial structure inherent within motion planning problems, and deployed its adjacency matrix as an attention mask to incorporate these inherent structures into the neural sampler. GAIDE was trained on optimal paths generated by an oracle planner via supervised learning, and employed dropout during inference to introduce stochasticity into the planning algorithm.

We evaluated GAIDE by embedding it into a bidirectional motion planner and comparing its performance with state-of-the-art sampling-based motion planners using uniform sampling, heuristic-based informed sampling, and neural informed sampling. The results demonstrate that GAIDE achieves superior performance compared to benchmark motion planners across all held-out evaluation tasks. Ablation studies further demonstrate that explicitly incorporating the spatial and kinematic structure of the motion planning problem into the neural sampler leads to substantial performance improvement.

[^1]: $^{1}$Davood Soleymanzadeh and Minghui Zheng are with the J. Mike Walker '66 Department of Mechanical Engineering, Texas A&M University, College Station, TX 77843, USA (`e-mail: davoodso@tamu.edu; mhzheng@tamu.edu).`

[^2]: $^{2}$Xiao Liang is with the Zachry Department of Civil and Environmental Engineering, Texas A&M University, College Station, TX 77843 USA (`e-mail: xliang@tamu.edu).`

[^3]: $^*$ Corresponding Authors.

[^4]: This work was supported by the USA National Science Foundation under Grant No. 2527316 and No. 2422826. Portions of this research were conducted with the advanced computing resources provided by Texas A&M High Performance Research Computing.
