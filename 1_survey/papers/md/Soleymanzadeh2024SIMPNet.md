---
citation_key: Soleymanzadeh2024SIMPNet
arxiv_id: 2408.12831
arxiv_url: https://arxiv.org/abs/2408.12831
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:15:49Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Neural Motion Planning, UR5e Robotic Manipulator, SIMPNet, Graph Neural Networks (GNNs), Attention Mechanism
:::

# Introduction {#sec: intro}

planning is a critical component within the robotic autonomy stack, enabling robotic manipulators to achieve task-specific goals [@orthey2023sampling; @McMahon_2022; @tamizi2023review]. For a robotic manipulator, this process involves finding a feasible collision-free path between a pre-defined start and goal within its configuration space. Over the past few years, a diverse collection of motion planning algorithms has been developed to address the motion planning problem. These planning paradigms fall into three categories: resolution complete graph-based algorithms [@hart1968formal], probabilistic complete sampling-based algorithms [@lavalle1998rapidly], and optimization-based algorithms [@ratliff2009chomp]. Among motion planning paradigms, sampling-based motion planners are effective for robotic manipulators operating in complex environments, allowing them to navigate safely and efficiently [@lavalle2006planning].

Sampling-based motion planners rely on three algorithmic primitives: sampling within high-dimensional configuration spaces, steering towards these sampled configurations, and checking collisions for such connections [@lavalle1998rapidly]. These planners iteratively build a tree by connecting collision-free samples drawn from their underlying sampling distribution. For example, Rapidly-Exploring Random Trees (RRTs) [@lavalle1998rapidly] uniformly sample the configuration space, a method that becomes computationally intensive within high-dimensional configuration spaces. To address this, more recent advanced sampling-based motion planners utilize hand-crafted heuristics to modify the sampling distribution, biasing it towards areas that likely reduce planning cost and increase success likelihood [@gammell2014informed]. However, challenges like developing an initial path to guide these heuristics and the inherent complexity of high-dimensional configuration spaces can hinder the effectiveness of these planners [@qureshi2018deeply].

:::: {#fig_1- simpnet-example .figure latex-placement="t"}
![](Soleymanzadeh2024SIMPNet_figs/00.png){width="3 in"}

::: caption
An example of SIMPNet planning in a complex environment. The proposed sampling heuristic (Figure [2](#fig_2- simpnet-framework){reference-type="ref" reference="fig_2- simpnet-framework"}) within the SIMPNet framework leverages graph and graph neural network frameworks to retain the spatial relationships within the configuration space and the kinematic chain of the robotic manipulator. This approach allows for informed sampling within the framework of sampling-based motion planning algorithms. $q_t$, and $\mathbf{x}_t$ are current joint angle and Cartesian 3D workspace position respectively. $q_g$, and $\mathbf{x}_g$ are the goal joint angle and Cartesian 3D workspace position respectively. $\mathbf{f}_i$ denotes node features, $\mathbf{v}_t$ denotes the concatenation of all nodes' features, and $\mathbf{o}_t$ denotes environment embedding. $\mathbf{q}_{t+1}$ is the next time step sampled manipulator's configuration.
:::
::::

Recently, learning-based motion planning methods have been developed to improve the sampling heuristic of traditional sampling-based planners. These methods use networks trained on successful paths to capture the similarity between planning problems and encode the underlying structure of the configuration space. As a result, they generate an informed sample based on the learned sampling heuristic [@johnson2023learning; @qureshi2020motion]. However, many of these learning-based planners do not fully account for the spatial relations within the configuration space and workspaces, or the sequential structure inherent within the motion planning problem [@zang2022robot].

We introduce SIMPNet, a novel motion planner that features a stochastic neural sampling heuristic based on a message-passing neural network architecture [@gilmer2017neural]. This approach enables SIMPNet to learn motion policies and generate samples that are informed by the spatial relationships within the configuration space. By integrating relational information from the robotic manipulator's kinematic structure into a graph and applying a cross-attention mechanism [@vaswani2017attention] to merge workspace embeddings with configuration space, SIMPNet facilitates spatially-aware sampling. Combined with a bi-directional planning algorithm [@qureshi2019motion], this method reduces planning time and enhances the success rate, thus outperforming existing motion planning algorithms like MPNet [@qureshi2019motion].

The contributions of this work include:

- We construct a graph that implicitly represents the kinematic chain of the robotic manipulator, providing a spatial representation of its movements within the configuration space. We use a message-passing neural network structure [@gilmer2017neural], to perform message-passing on the constructed graph. This process ensures the sampling heuristic within the SIMPNet framework is spatially aware of the configuration space, thereby facilitating informed sample generation.

- We integrate a cross-attention mechanism into our sampling heuristic, which effectively incorporates workspace embeddings into the configuration space [@zhang2022learning]. The cross-attention module addresses challenges posed by the differing dimensionalities of the configuration space and workspace, allowing for efficient integration of information between these two environments.

- We evaluate the performance of SIMPNet across various workspaces, empirically demonstrating that it outperforms other benchmark motion planning algorithms in terms of planning time and success rate.

The paper is structured as follows. Section [2](#sec: related work){reference-type="ref" reference="sec: related work"} reviews related work in sampling-based motion planning. Section [3](#sec: GNN-based planning){reference-type="ref" reference="sec: GNN-based planning"} introduces the SIMPNet structure. Section [4](#sec: results and discussion){reference-type="ref" reference="sec: results and discussion"} presents a performance evaluation of our proposed planner, and compares it against benchmark motion planners. Finally, section [5](#sec: conclusion){reference-type="ref" reference="sec: conclusion"} concludes the paper.

# Related Work {#sec: related work}

This section briefly reviews recent literature on sampling-based motion planning for robotic manipulators. We begin by discussing sampling-based motion planners and then explore how deep learning, particularly graph neural networks, is being applied to enhance these motion planning algorithms.

**Sampling-based motion planning (SBMP)**: Sampling-based motion planners, such as RRTs [@lavalle1998rapidly] and Probabilistic Roadmap (PRM) [@amato1996randomized], have emerged as a practical solution for motion planning of robotic manipulators. SBMP algorithms are probabilistic complete, meaning the probability of finding a feasible path, if one exists, approaches one as the number of samples increases to infinity [@lavalle2006planning]. SMBP algorithms use sampling techniques to generate rapidly-exploring trees (single-query rapidly-exploring trees) [@lavalle1998rapidly; @karaman2011sampling; @kuffner2000rrt] or roadmaps (multi-query probabilistic roadmaps) [@karaman2011sampling; @amato1996randomized; @bohlin2000path] within the manipulator's configuration space. These planners operate directly within the continuous configuration space without requiring precise models of collision and collision-free spaces [@lavalle2006planning]. Multi-query probabilistic roadmaps construct a graph that can be used for planning between various start and goal configurations. However, this can be achieved by solving a series of single query problems for different start and goal configurations [@karaman2011sampling].

RRTs [@lavalle1998rapidly] sample the configuration space uniformly to construct a tree between the start and goal configuration for path planning. However, RRTs struggle to find the optimal path. RRT\* (i.e., optimal RRT), an extension of RRTs, aims to achieve asymptotic optimality [@karaman2011sampling]. RRT\* employs rewiring steps within the constructed tree to find a sub-optimal path, necessitating more samples. As the manipulator's degrees of freedom (DOF) increase, so does the computational complexity. RRTs and RRT\* utilize a uniform sampling heuristic to construct a tree implicitly representing the configuration space. However, this uniform sampling heuristic struggles to scale to high-dimensional configuration spaces, leading to higher computational complexity and longer planning time. More advanced SBMPs such as Informed-RRT\* [@gammell2014informed] and Batch-Informed Trees (BIT\*) [@gammell2015batch] employ informed sampling heuristics that focus on areas likely to contain optimal paths, thereby reducing computational complexity and planning time. These hand-crafted sampling heuristics decrease the planner's computation complexity and planning time by directing sampling towards regions with potential optimal paths. Nevertheless, crafting these informed sampling heuristics is not trivial, particularly for high-dimensional configuration spaces [@qureshi2020motion]. The major drawbacks of SBMPs are sample inefficiency and expensive collision checking [@yu2024efficient].

**Neural-based SBMPs**: Neural-based SBMPs utilize deep learning frameworks - known for fast inference, inductive bias, and the capability to encode the multi-modal structure within datasets - to replace or enhance algorithmic primitives of SBMPs. For the sampling heuristic, deep learning modules have been utilized to either implicitly learn the heuristic for generating informed samples, or explicitly generate samples. Deep generative models [@sohn2015learning; @van2017neural; @tolstikhin2017wasserstein; @rezende2015variational] are particularly popular for learning the underlying sampling heuristic for a specific motion planning problem [@johnson2023learning; @zhuang2024transformer; @xia2022graph; @ichter2018learning; @ichter2019robot; @lai2021plannerflows]. Additionally, the rapid inference capabilities of multi-layer perceptrons (MLPs) are employed as explicit informed sampling heuristic in motion planning [@qureshi2018deeply; @qureshi2019motion; @qureshi2020neural; @qureshi2020motion]. For the collision-checking, various deep learning frameworks predict whether nodes and edges in the planning tree are collision-free [@chase2020neural; @koptev2022neural; @quintero2023stochastic; @bhardwaj2021leveraging]. However, many of these planners struggle to adequately account for the spatial and temporal dependencies inherent in motion planning problems.

**Graph neural networks (GNNs)-based SBMPs**: GNNs-based SBMPs leverage graphs, which are powerful for representing both structured and unstructured data, and for encoding temporal and spatial relationships within them [@pistilli2023graph]. Graph neural networks (GNNs), which operate on graphs, offer a structured representation that effectively encodes spatial correlations within a dataset [@battaglia2018relational]. This capability is useful for encoding spatial dependencies within a robotic manipulator's configuration space. Researchers [@yu2021reducing; @zhang2022learning] have utilized GNNs to enhance edge evaluation in planning trees, thereby reducing the need for expensive edge evaluation and collision checks. However, a major drawback of these approaches is that the initial geometric graphs are often generated randomly, without consideration for the underlying structure of the configuration space.

In contrast to these works, our framework, SIMPNet, uses a stochastic neural network built on a message-passing neural network framework, serving as a spatially informed sample generator. The aim of SIMPNet's sampling primitive is to learn an informed sampling heuristic from a set of observed sub-optimal paths. This innovative learning approach is designed to improve the success rate and reduce the planning time required by the motion planning algorithm.

# Spatial-Informed Motion Planning Network (SIMPNet) {#sec: GNN-based planning}

We introduce an informed sampling heuristic within the SIMPNet framework that uses current timestep planning information from configuration space and workspace to generate the next timestep configuration in a motion planning problem. This framework integrates workspace encoding into the configuration space using an attention mechanism, while the message-passing module encodes the spatial correlations within the configuration space to facilitate spatially-aware sampling. Figure [2](#fig_2- simpnet-framework){reference-type="ref" reference="fig_2- simpnet-framework"} illustrates the schematic of the proposed sampling heuristic within the SIMPNet structure. In this section, we first define the motion planning problem. Next, we describe how to construct a graph to encode the spatial correlations. Finally, we describe each component of the SIMPNet in detail.

:::: {#fig_2- simpnet-framework .figure latex-placement="htbp"}
![](Soleymanzadeh2024SIMPNet_figs/02.png){width="\\textwidth"}

::: caption
Schematic of spatial-informed sampling heuristic within SIMPNet. Utilizing the current time step planning information from the workspace and configuration space, this sampling heuristic generates the next time step configuration, moving towards the goal of the motion planning problem. $q_t$, and $\mathbf{x}_t$ are the current joint angle and Cartesian 3D workspace position respectively. $q_g$, and $\mathbf{x}_g$ are the goal joint angle and Cartesian 3D workspace position respectively. $\mathbf{o}_t$, and $\mathbf{q}_{t+1}$ are the environment embedding, and the next time step sampled manipulator's configuration respectively.
:::
::::

## Motion Planning Definition

Let $\mathcal{C} \in \mathbb{R}^n$ represent the configuration space of a robotic manipulator where $n$ denotes the robot's degree of freedom (DOF). The configuration space comprises two spaces: the obstacle space ($\mathcal{C}_{obs} \subset \mathcal{C}$), and the free space ($\mathcal{C}_{free}=\mathcal{C}\backslash \mathcal{C}_{obs}$). Given a start configuration ($\mathbf{q}_{start} \in \mathcal{C}_{free}$), and a goal configuration ($\mathbf{q}_{goal} \in \mathcal{C}_{free}$), the motion planning problem involves finding a feasible path ($\mathbf{q}=\{\mathbf{q}_{start}, \cdots, \mathbf{q}_{goal}\}$) between the start and goal configuration such that the entire path lies within the free configuration space.

## Robotic Manipulator's Graph Representation

We model the kinematic structure of the robotic manipulator using an undirected graph. In the graph, $G = (V, E, F)$, $V$ represents the set of nodes, $E$ the set of edges, and $F$ the node features. An edge $e_{ij} \in E$ connects node $v_i \in V$ and $v_j \in V$, if they are connected. Each node feature vector $\mathbf{f}_i \in F$ is a $d$-dimensional vector ($\in \mathbb{R}^d$) associated with the corresponding node $v_i$. The neighborhood of a node $v_i$, denoted as $\mathcal{N}(i) = \{j|e_{ij} \in E\}$, represents the nodes directly connected to the given node $v_i$.

In our model, the joints of the robotic manipulator are represented as nodes in a graph, where the edges represent the topological and kinematic relationships between these nodes. The edges are explicitly defined based on the kinematic structure of the manipulator, with each node connected to the subsequent nodes following the kinematic chain of the robotic manipulator from the base joint toward the end-effector. The node features are selected to encapsulate relevant information, including the spatial information of both workspace and configuration space, kinematic information of the manipulator, and essential elements of motion planning as follows: $$\begin{equation}
 \label{eq - node_features}
\begin{split}
    \mathbf{f}_i = [&\mathbf{x}_t, \mathbf{x}_{goal}, |\mathbf{x}_{goal} - \mathbf{x}_t|, \left\lVert\mathbf{x}_{goal} - \mathbf{x}_t\right\rVert_2, q_t, q_{goal}, \\
    & |q_t - q_{goal}|]
\end{split}
\end{equation}$$ where $\mathbf{x}_t$, $\mathbf{x}_{goal}$ are the current and goal positions in Cartesian 3D coordinates for each node, derived using forward kinematics (FK). Similarly, $q_t$, and $q_{goal}$ denote the current and target joint angles respectively. Figure [3](#fig_3- cobot-graph){reference-type="ref" reference="fig_3- cobot-graph"} illustrates the graph representation of our robotic manipulator.

:::: {#fig_3- cobot-graph .figure latex-placement="htbp"}
![](Soleymanzadeh2024SIMPNet_figs/01.png){width="3in"}

::: caption
Illustration of the constructed graph for the 6-DoF UR5e robotic manipulator. This graph represents the relational geometry and kinematics chain of the robotic manipulator. Each joint is considered a node, and edges are defined to reflect the kinematic connections between joints, mapping the robotic manipulator's structure into the graph.
:::
::::

## SIMPNet Sampling Heuristic Components

Building on the graph constructed in the previous section, we now detail each component of the proposed sampling heuristic.

**Embedding Workspace and Node Features**: Node features, as defined in eq. [\[eq - node_features\]](#eq - node_features){reference-type="ref" reference="eq - node_features"}, are concatenated to form a single embedding vector that implicitly represents the configuration space at time step $t$. Dimensions (length, height, width) and 3D coordinates of each obstacle's center are similarly concatenated to create the environment embedding at the same time step. Two distinct deep multi-layer perceptrons (MLPs) then transform the configuration space and the workspace embeddings into same-size embedding vectors as follows: $$\begin{equation}
 \label{eq - taskspace}
\begin{aligned}
    \mathbf{v} = MLP_{I}\big(\parallel_{i=1}^{n_v}\mathbf{f}_i \parallel\big)
\end{aligned}
\end{equation}$$ $$\begin{equation}
 \label{eq -workspace}
\begin{aligned}
    \mathbf{o} = MLP_{II}\big(\parallel_{j=1}^{n_o}[x_i, y_i, z_i, L_i, W_i, H_i] \parallel \big)
\end{aligned}
\end{equation}$$ where $\mathbf{f}_i$ represents the feature of $i$-th node as defined in eq. [\[eq - node_features\]](#eq - node_features){reference-type="ref" reference="eq - node_features"}. $n_v$ denotes the total number of nodes in the graph. $(x_i, y_i, z_i)$ and $(L_i, W_i, H_i)$ denote the Cartesian coordinate, and the dimensions (length, width, height) of the $j$-th obstacle within the workspace, respectively. The $\parallel$ operator represents the concatenation operator.

**Integrating Workspace embedding into Configuration Space**: We utilize a cross-attention mechanism to integrate workspace embeddings, i.e., obstacles, into the configuration space. The attention mechanism, a key component of the Transformer model, helps encode inter-dependencies among elements [@vaswani2017attention]. The formulation of the attention mechanism is as follows: $$\begin{equation}
 \label{eq - attention-mechanism}
\begin{aligned}
    \text{Attention}(\mathbf{q}, \mathbf{k}, \mathbf{v}) = \text{softmax}(\frac{\mathbf{q}\mathbf{k}^T}{\sqrt{d_k}})\mathbf{v}
\end{aligned}
\end{equation}$$ where $\mathbf{q}$, $\mathbf{k}$, and $\mathbf{v}$ are query, key, and value vectors respectively, with $d_k$ indicating the dimensionality of the key vector. This attention mechanism integrates workspace embeddings into the configuration space in our research. $$\begin{equation}
 \label{eq -cross-attention}
\begin{aligned}
    \mathbf{v} = \text{Cross-attention}(\mathbf{q}_v, \mathbf{k}_o, \mathbf{v}_o) + \mathbf{v}
\end{aligned}
\end{equation}$$ where $\mathbf{q}_v$, $\mathbf{k}_o$, and $\mathbf{v}_o$ are query, key and value vectors respectively. These vectors are derived using one-layer MLPs, as follows: $$\begin{equation}
 \label{eq -query-key-value}
\begin{aligned}
    \mathbf{q}_v &= \text{MLP}_{\text{query}}(\mathbf{v}) \\ 
    \mathbf{k}_o &= \text{MLP}_{\text{key}}(\mathbf{o}) \\
    \mathbf{v}_o &= \text{MLP}_{\text{value}}(\mathbf{o}) \\
\end{aligned}
\end{equation}$$

**Kinematics Aware Message Passing**: Following the integration of workspace information into the configuration space, and the construction of the graph, we aggregate node features to predict node-level (joint-level) properties [@battaglia2018relational]. To this end, we utilize a message-passing neural network (MPNN) [@gilmer2017neural] which consists of three steps for performing message passing to produce a new graph with the same structure and connectivity but updated node features. The message-passing operator within the MPNN framework is as follows: $$\begin{equation}
 \label{eq - mpnn}
\begin{aligned}
    \mathbf{f}_i^{(k)} = \phi^v\left[\mathbf{f}_i^{(k-1)}, \oplus_{j \in \mathcal{N}(i)} \phi^e \left[\mathbf{f}_i^{(k-1)}, \mathbf{f}_j^{(k-1)}\right] \right]
\end{aligned}
\end{equation}$$ where $\phi^e$ and $\phi^v$ are multilayer perceptron (MLP)-based update functions, and $\oplus$ denotes a permutation invariant operator (e.g., sum, mean, max). $\mathcal{N}(i)$ denotes the neighborhood of the given node [@fey2019fast]. Within the SIMPNet framework, one layer of message passing is performed using eq. [\[eq - mpnn\]](#eq - mpnn){reference-type="ref" reference="eq - mpnn"}, considering $sum$ as the $\oplus$ operator, as follows: $$\begin{equation}
 \label{eq - simpnetmpnn}
\begin{aligned}
    \mathbf{f}_i = \phi^v\left[\mathbf{f}_i, \sum_{j \in \mathcal{N}(i)} \phi^e \left[\mathbf{f}_i, \mathbf{f}_j\right] \right]
\end{aligned}
\end{equation}$$

**Final Embedding Layer**: Finally, another deep neural network is utilized to map the output of the message passing layer to a single number representing the next timestep joint angle within the framework of sampling-based motion planning algorithms as follows. $$\begin{equation}
 \label{eq -final-embedding}
\begin{aligned}
   \mathbf{q}_{t+1} = MLP_{III}(\mathbf{f}_i)
\end{aligned}
\end{equation}$$ where $\mathbf{q}_{t+1}$ is the next time step stochastically generated joint angle within the framework of sampling-based motion planning algorithms.

## Bi-directional Planning Algorithm

We embed our proposed sampling heuristic into the bi-directional planning algorithm proposed by [@qureshi2019motion] to have our proposed planning algorithm. Algorithm [\[alg:simpnet\]](#alg:simpnet){reference-type="ref" reference="alg:simpnet"} shows SIMPNet algorithm. Interested readers are welcome to check the work by Qureshi et al. [@qureshi2019motion] for a detailed description of the utilized bi-directional planning algorithm.

::: algorithm
$\mathbf{q}^a \leftarrow \{\mathbf{q}_{start}\}$, $\mathbf{q}^b \leftarrow \{\mathbf{q}_{goal}\}$\
$\mathbf{q}\leftarrow \emptyset$\
*Complete* $\leftarrow$ *False*
:::

# Results and Discussion {#sec: results and discussion}

In this section, we detail the implementation of our planner and compare its performance with state-of-the-art motion planning algorithms. The framework is developed using the PyTorch framework [@paszke2017automatic], and the simulations were conducted on a computer running Linux OS, equipped with a 2.6 GHz Intel i7-1355U CPU, and a 16 GB RAM.

## Data Collection

We simulated the planning environment using MoveIt! [@coleman2014reducing], and collected data using RRT\* from Open Motion Planning Library (OMPL) [@sucan2012open]. Two types of planning environments, complex and simple, were considered. For each environment, 10 different workspaces were considered. Figure [5](#fig_4- envs){reference-type="ref" reference="fig_4- envs"} displays examples of these environments. In each workspace, 1000 collision-free paths are collected for training. For testing, 200 start-goal configurations are generated for each of the complex and simple environments. Collision checking was performed utilizing Flexible Collision Library (FCL) [@pan2012fcl] within the MoveIt! framework.

:::: {#fig_4- simpnetvsrrt .figure latex-placement="htbp"}
![](Soleymanzadeh2024SIMPNet_figs/04.png){width="\\linewidth"}

::: caption
Comparison of planned paths by SIMPNet and some baseline planners in a complex environment: Bi-RRT (Bi-directional RRT), IRRT\* (Informed-RRT\*), and MPNet (Motion Planning Networks) [@qureshi2019motion]. RRT completes the path in $32$ seconds with a planning cost of $9.32$. Bi-RRT plans in $9.44$ seconds with a planning cost of $9.02$. IRRT\* takes $500$ seconds, achieving a cost of $4.01$. MPNet completes the path in $218$ seconds with a planning cost of $11.3$. SIMPNet plans the path in $5.81$ seconds with a planning cost of $8.08$. Please note that the planning cost for a path $\{\mathbf{q}_1, \mathbf{q}_2, ..., \mathbf{q}_n\}$ is calculated as $\sum_{i=0}^{n-1}||\mathbf{q}_{i+1} - \mathbf{q}_i||_2$, where $\mathbf{q}_i$ represents the robotic manipulator's configuration state, and the shortest path in the configuration space doesn't necessarily translate into the workspace.
:::
::::

:::: {#fig_4- envs .figure latex-placement="htbp"}
![](Soleymanzadeh2024SIMPNet_figs/03.png){width="3.0 in"}

::: caption
Type of workspaces used for training and evaluation of SIMPNet.
:::
::::

## Baselines and Metrics

**Algorithms and Baselines.** We assessed the performance of SIMPNet by comparing it with several state-of-the-art motion planning algorithms. We chose Bi-directional RRT [@kuffner2000rrt] and Informed-RRT\* [@gammell2014informed], as baseline sampling-based motion planners. Bi-directional RRT utilizes a uniform sampling heuristic, and Informed-RRT\* employs a hand-crafted sampling heuristic for sampling within the robotic manipulator's configuration space. In addition, we chose two recent deep learning-based sampling heuristics called MPNet [@qureshi2019motion], and KG-Planner [@liu2024kg]. Given that KG-Planner is a deterministic motion planner with limited application in simple environments, for fair comparison we made its structure stochastic. All deep learning-based sampling heuristics used the same workspace embedding network and number of replanning attempts. Also, a Python implementation of all the planners was leveraged for comparison purposes. Figure [4](#fig_4- simpnetvsrrt){reference-type="ref" reference="fig_4- simpnetvsrrt"} shows the performance of SIMPNet compared to other baseline motion planners, in a planning instance in a complex environment.

**Metrics.** We employed three commonly used metrics for evaluating the performance of SIMPNet against baseline motion planners: *planning time*, *planning cost*, and *success rate*. *Planning time* "T" refers to the average planning time the planner takes in each environment. *Planning cost* "C" measures the length of the successfully planned paths in the configuration space. *Success rate* "Success" represents the percentage of successfully planned paths.

## Randomness via Dropout

We incorporate Dropout [@srivastava2014dropout] within the structure of the sampling heuristic of SIMPNet, and also applied it to two deep learning-based motion planning baselines for sample generation [@qureshi2020motion]. This introduction of randomness implies that each planning attempt by these planners could result in a different path between any given start and goal configuration. This property, the defining feature of classical sampling-based motion planning algorithms, contributes to the generalizability of these sampling heuristics to unseen environments.

## SIMPNet Performance in a Simple Environment

We evaluate the performance of SIMPNet, and all the baselines in a simple environment (see an example of a simple environment in figure [5](#fig_4- envs){reference-type="ref" reference="fig_4- envs"}). Since classical planners used in this study (e.g., Bi-RRT and Informed-RRT\*) lack inherent termination conditions, we set the planning time for these planners to match the average planning time of our proposed planner. Table [\[tab: simpnet-performance\]](#tab: simpnet-performance){reference-type="ref" reference="tab: simpnet-performance"} shows the performance metrics of all the planners in the simple environment.

:::: table*
::: center
[]{#tab: simpnet-performance label="tab: simpnet-performance"}

+----------------------------+---------------------------------------------------------------------------------------------------------------------------+---+---------------------------------------------------------------------------------------------------------------------------+---+
|                            | Simple Environment                                                                                                        |   | Complex Environment                                                                                                       |   |
+:===========================+:=================:+:==============:+:======================:+:=================:+:==============:+:======================:+:=:+:=================:+:==============:+:======================:+:=================:+:==============:+:======================:+:=:+
| 2-7                        | Seen                                                        | Unseen                                                      |   | Seen                                                        | Unseen                                                      |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
| 2-4                        | T $[s]\downarrow$ | C $\downarrow$ | Success $[\%]\uparrow$ | T $[s]\downarrow$ | C $\downarrow$ | Success $[\%]\uparrow$ |   | T $[s]\downarrow$ | C $\downarrow$ | Success $[\%]\uparrow$ | T $[s]\downarrow$ | C $\downarrow$ | Success $[\%]\uparrow$ |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
| Bi-RRT                     | 1.13              | 8.81           | **96%**                | 1.18              | 9.16           | **98%**                |   | **4.13**          | 9.2            | **82%**                | **3.65**          | 9.2            | **68%**                |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
| IRRT\*                     | 1.15              | **5.37**       | 88%                    | 1.10              | **5.16**       | 89%                    |   | 14.03             | 4.78           | 44%                    | 7.48              | 4.82           | 34%                    |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
| MPNet [@qureshi2019motion] | 0.92              | 5.78           | 94%                    | 1.13              | 5.57           | **98%**                |   | 17                | **4.72**       | 54%                    | 20                | **4.67**       | 41%                    |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
| KG-Planner [@liu2024kg]    | 0.79              | 5.79           | 94%                    | 1.02              | 5.71           | 98%                    |   | 4.49              | 5.76           | 60%                    | 8.37              | 6.32           | 55%                    |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
| SIMPNet                    | **0.5**           | 5.68           | 94%                    | **0.53**          | 5.44           | 97%                    |   | 14                | 6.42           | 81%                    | 7.45              | 7.13           | 65%                    |   |
+----------------------------+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+-------------------+----------------+------------------------+-------------------+----------------+------------------------+---+
:::
::::

The results show that Bi-RRT has the highest success rate among all the planners. Its inherent bi-directional heuristic contributes to its efficiency, making it fast. However, this planner compromises planning cost for higher planning time and success rate [@gammell2015batch]. Informed-RRT\* rewires the constructed graph during planning to find the sub-optimal path, resulting in the lowest planning cost among the utilized planners, while trading off success rate and planning time. Among the deep learning-based planners, the proposed planner performs comparably similarly to others. Also, the use of Dropout during planning, helps all the deep learning-based planners generalize effectively to unseen environments.

## SIMPNet Performance in a Complex Environment

We evaluate the performance of SIMPNet, and all the baselines in a complex environment (see an example of a complex environment in figure [5](#fig_4- envs){reference-type="ref" reference="fig_4- envs"}). We also set the planning time of Bi-RRT and Informed-RRT\* as the average planning time of the SIMPNet algorithm. Table [\[tab: simpnet-performance\]](#tab: simpnet-performance){reference-type="ref" reference="tab: simpnet-performance"} summarizes the performance of all the planners in a complex environment. In this environment, Bi-RRT maintains the highest success rate and planning time across seen and unseen environments, benefiting from its bi-directional module. However, it does so at the expense of increased planning costs. Similarly, Informed-RRT\*, with its inherent rewiring heuristic, achieves the lowest planning cost, while trading off success rate and planning time.

SIMPNet achieves a higher success rate and lower planning time compared to other baseline deep learning-based planners. This performance can be attributed to the proposed approach of encoding the kinematic chain of the robotic manipulator as a graph. Also, unlike other baseline deep learning-based planners that directly incorporate the configuration space and workspace into the sampling heuristic network, SIMPNet employs a cross-attention mechanism to link these two fundamentally different environments efficiently.

## Ablation Study: Forward Kinematics Relaxed-SIMPNet (RelaxedFK-SIMPNet)

Although the original graph was constructed to implicitly represent the kinematic structure of the robotic manipulator in the configuration space, node features also contain some information from the workspace, such as joint positions, and goal positions. However, using forward kinematics in the planning and replanning phase of the proposed planner results in a trade-off between planning time and success rate. Here we are considering constructing a modified graph based solely on information from the configuration space. The newly constructed graph retains the same nodes and edges as the original graph but features the following node attributes. $$\begin{equation}
 \label{eq - node_featuresnofk}
\begin{aligned}
    \mathbf{f}_i = [q_t, q_{goal}, |q_t - q_{goal}|]
\end{aligned}
\end{equation}$$ where $q_t$, and $q_{goal}$ are current time-step and goal joint angles within the configuration space, respectively. The performance of RelaxedFK is compared against SIMPNet across all the environments. Table [1](#tab: planning performance - ablation-simpnetvsrelaxedFKsimpnet){reference-type="ref" reference="tab: planning performance - ablation-simpnetvsrelaxedFKsimpnet"} showcases the performance metrics of these planners.

::: {#tab: planning performance - ablation-simpnetvsrelaxedFKsimpnet}
+------------------+--------------------------------------------+--------------------------------------------+
|                  | Simple Environment                         | Complex Environment                        |
+:=======+:========+:==================+:=======================+:==================+:=======================+
|        | Planner | T $[s]\downarrow$ | Success $[\%]\uparrow$ | T $[s]\downarrow$ | Success $[\%]\uparrow$ |
+--------+---------+-------------------+------------------------+-------------------+------------------------+
| Seen   | SMP     | **0.5**           | 94%                    | 14                | **81%**                |
|        +---------+-------------------+------------------------+-------------------+------------------------+
|        | RFK-SMP | 0.86              | **96%**                | **1.76**          | 62%                    |
+--------+---------+-------------------+------------------------+-------------------+------------------------+
| Unseen | SMP     | **0.53**          | 97%                    | 7.45              | **65%**                |
|        +---------+-------------------+------------------------+-------------------+------------------------+
|        | RFK-SMP | 0.72              | **98%**                | **6.02**          | 61%                    |
+--------+---------+-------------------+------------------------+-------------------+------------------------+

: Comparison of planning performance between SIMPNet and RelaxedFK-SIMPNet across all environments. "SMP" denotes SIMPNet, "RFK-SMP" denotes RelaxedFK-SIMPNet.
:::

The results suggest that RelaxedFK-SIMPNet trades off success rate for reduced planning time. This property is desirable in simple planning environments, as it is highly probable that the proposed planner can find a path without incorporating forward kinematics information. However, for complex environments, the results indicate that including forward kinematics enhances the success rate of the motion planner.

# Conclusion and Future Work {#sec: conclusion}

In this paper, we introduced SIMPNet, a bi-directional motion planner that utilizes an informed deep learning-based sampling heuristic. We constructed a graph representing the kinematic chain of the robotic manipulator within the configuration space and employed a cross-attention mechanism to integrate information from the 3D workspace to the robotic manipulator's 6D configuration space. The proposed sampling heuristic within SIMPNet was trained via supervised learning on optimal paths generated by an oracle planner. Additionally, We used Dropout within during inference to introduce stochastic behavior in the SIMPNet architecture.

Our results highlight the advantage of using graphs and graph neural networks. These tools are highly effective for retaining and leveraging spatial relationships inherent in the configuration space and kinematic structure of the robotic manipulators. This capability enhances informed sampling within the sampling-based motion planning algorithms. Additionally, the attention mechanism was effectively employed to integrate workspace information into the configuration space, facilitating highly informed sample generation.

One direction for improving the performance of the proposed planner involves improving the underlying dataset. The current dataset can be improved by including high-quality, representative data regarding the boundary of obstacles within the workspace, which could further improve the effectiveness of the proposed sampling heuristic. One potential solution could involve leveraging the exploration characteristics of reinforcement learning frameworks, combined with the exploitation characteristics of the proposed sampling heuristic, to address this challenge [@cheng2020learning].

[^1]: This work was supported by USA National Science Foundation under Grant 2026533/2422826 and Grant 2132923/2422640. (*Corresponding authors: Minghui Zheng; Xiao Liang.*)

[^2]: Davood Soleymanzadeh and Minghui Zheng are with the J. Mike Walker '66 Department of Mechanical Engineering, Texas A&M University, College Station, TX 77843, USA (e-mail: davoodso@tamu.edu; mhzheng@tamu.edu).

[^3]: Xiao Liang is with the Zachry Department of Civil and Environmental Engineering, Texas A&M University, College Station, TX 77843 USA (e-mail: xliang@tamu.edu).

[^4]: Supplementary materials are available via this [link](https://zh.engr.tamu.edu/wp-content/uploads/sites/310/2024/08/SIMPNet-Demo.mp4).
