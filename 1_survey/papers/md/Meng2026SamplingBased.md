---
citation_key: Meng2026SamplingBased
arxiv_id: 2603.03514
arxiv_url: https://arxiv.org/abs/2603.03514
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:20:51Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

:::: {#fig:illustration_figure .figure latex-placement="!ht"}
![](Meng2026SamplingBased_figs/illustration.png){width="0.95\\columnwidth"}

::: caption
An illustration of our perception-aware motion planner that leverages a scene graph embedded with perception costs to generate a trajectory from a start to a goal, while monitoring three objects of interest. The screen of the monitor is the preferable viewpoint in this scenario.
:::
::::

robot systems have become more prevalent in a variety of human-centered environments, such as workplaces [@bolu2021adaptive], hospitals [@qian2025astrid], urban areas [@liao2023kitti] and homes [@shafiullah2023bringing]. A key challenge in such environments is that the robot often has to plan a collision-free trajectory to finish its own tasks, while monitoring other humans or objects of interest along the trajectory. For example, a household robot may need to deliver an item while keeping a person's face or gestures in view, or a museum patrol robot may navigate around visitors while maintaining visibility of multiple paintings or sculptures. Such perception constraints are essential for monitoring the surrounding objects [@falanga2018_pampc; @masnavi2024differentiable], improving the robot's state estimation [@ichter2020_perception; @bartolomei2020_perception], enabling safe navigation [@loquercio2021_learning; @song2023_learning], and mapping and exploration of the environment [@placed2023active_slam_survey]. Therefore, we aim to address the problem of motion planning under perception constraints in this paper.

A common example of perception-aware constraints in motion planning is object tracking and monitoring, where the robot maintains visibility of a single object [@falanga2018_pampc; @masnavi2024differentiable; @meng2025lookleapplanningsimultaneous] or multiple objects [@tordesillas2022_panther; @zhang2024perception], that can be either static [@falanga2018_pampc; @meng2025lookleapplanningsimultaneous] or dynamic [@masnavi2024differentiable; @tordesillas2022_panther; @zhang2024perception] in the environment. Accurate tracking of multiple objects in the environment is particularly useful for collision avoidance, especially with aggressive quadrotor flights [@falanga2018_pampc; @loquercio2021_learning; @song2023_learning], or in cluttered and dynamic environments [@tordesillas2022_panther; @singla2021_memory; @masnavi2024differentiable]. Besides objects, several works aim to maintain visibility of visual features for accurate state estimation [@ichter2020_perception; @bartolomei2020_perception], such as visual-inertial odometry (VIO) [@mourikis2007multi], which is crucial for robot operations in the wild. Another exciting research direction is active mapping or exploration [@placed2023active_slam_survey], where the robot trajectory is planned to explore the unmapped regions of the environment [@bircher2016receding; @zhang2020fsmi; @asgharivaskasi2023semantic], either by choosing the next best goal state [@bircher2016receding] or by maximizing the information gain of future sensor observations [@zhang2020fsmi; @asgharivaskasi2023semantic].

The perception-aware constraints are commonly integrated as a cost, heuristic, or reward function in a motion planning problem, which is in turn, solved by an optimization solver [@falanga2018_pampc; @tordesillas2022_panther], a search-based [@bartolomei2020_perception] or sampling-based planner [@ichter2020_perception; @costante2016perception; @meng2025lookleapplanningsimultaneous], or by reinforcement learning [@singla2021_memory; @song2023_learning]. Although successful in navigation with mobile robots, existing work on perception-aware motion planning largely focuses on settings with simplified robot models or with limited degrees of freedom ([df]{.smallcaps}). Closely related to our approach, PS-PRM [@meng2025lookleapplanningsimultaneous] considers a perception-aware motion planning problem for a high-[df]{.smallcaps} robot but only monitors a known single object. Extending from monitoring a single object to multiple objects is nontrivial, as the planner must determine how to prioritize and achieve the correct viewpoints of the objects along the trajectory to maximize the overall user-defined perception score. Our work departs significantly from prior work on planning under perception constraints by developing a perception-aware sampling-based motion planner for high-[df]{.smallcaps} robots, e.g., mobile manipulators, that allows the robot to monitor multiple static objects of interest, stored in a scene graph built from sensor observations, while satisfying the kinematic constraints on the robot configuration.

Recently, metric-semantic maps [@alatise2020review], such as scene graphs [@chang2021comprehensive], have emerged as powerful representations that unify geometric, semantic, and topological information for large-scale environments. Scene graphs organize semantic and metric information in a hierarchical structure, capturing relationships across abstraction layers. Scene graphs have been used for task planning and high-level reasoning, in combination with language models, e.g., SayPlan [@rana2023sayplan] and AutoGPT+P [@{birr2024autogpt+}], or semantic instructions, e.g., GRID [@ni2024grid] and ConceptGraphs [@gu2024conceptgraphs], or for explorations, e.g., RoboEXP [@jiang2024roboexp].

As low-level motion planning requires geometric information and kinematic constraints to ensure the feasibility of a motion plan, recent work has explored the use of scene graphs for both task and motion planning [@ray2024task; @dai2024optimal; @viswanathan2025spade] in a hierarchical manner. A "coarse\" task plan is generated at the higher abstraction levels, such as buildings, rooms, or objects, and is then used to guide a local geometric planner at the occupancy level [@ray2024task; @viswanathan2025spade], or to generate a heuristic function for a multi-heuristic A\* geometric planner [@dai2024optimal]. However, these works focus on low-dimensional robot systems, e.g., robot or camera poses, without considering kinematic constraints.

Instead, we develop a sampling-based perception-aware probabilistic roadmap (PRM) planner for high-[df]{.smallcaps} robots, that integrates the robot's kinematic, geometric, and perception constraints, e.g., multi-object monitoring. The perception constraints are embedded with each object of interest in a scene graph as a perception cost function, which is used to inform the construction of a PRM. Given a robot configuration, the perception cost function describes the perception score of all objects of interest, that can be predefined or approximated by a neural network, pretrained to fit the confidence score of an object detection algorithm such as YOLOE [@wang2025yoloe]. For example, a high perception score or low perception cost is given if the camera pose, calculated via forward kinematics, leads to a clear view of multiple objects or humans in the camera image. We develop a perception-aware PRM graph construction by biasedly sampling robot configurations with low perception cost, i.e., high perception score. Given a start and a goal, an A\* search algorithm with our consistent heuristic design returns a robot path on the PRM that balances between the motion cost, representing the path's length or energy, and the perception cost, representing how well the robot can monitor the objects of interest along the path. We extensively validate our approach in both simulation and real-robot experiments. In summary, we propose a **M**ulti-**O**bject **P**erception-aware **S**cene-graph-based **P**robabilistic **R**oad**M**ap ([MOPS-PRM]{.smallcaps}) that:

- augments each object of interest in a scene graph with a learned perception costmap, specifying the preferable configuration regions for multi-object monitoring.

- constructs a perception-informed PRM on the configuration space of a high-[df]{.smallcaps} robot by selectively sampling nodes with low perception cost.

- generates a perception-aware trajectory with an A\* search on the perception-aware PRM.

![This figure presents the pipeline of our planner. The planner takes the scene graph as input, combining geometric and object-level information with a neural perception cost function to perform multi-object constrained sampling. Sampling is performed (see [3.2](#sec:method_multiobject){reference-type="ref+label" reference="sec:method_multiobject"}) to construct a PRM, which is searched using A\* to generate a trajectory that effectively accomplishes perception tasks involving multiple objects along the path.](figures/flowchart.png){#fig:approach_diagram width="\\textwidth"}

# Problem Statement {#sec:problem_statement}

We consider a robot with configuration $\mathbf{q} \in \mathcal{C} = \mathcal{C}_{\rm free} \cup \mathcal{C}_{\rm occupied} \subseteq \mathbb{R}^n$, where $n$ denotes the total number of degrees of freedom, including both the robot's base and its joints, and $\mbox{\ensuremath{\mathcal{C}_{\rm free}}}$ and ${\cal C}_{\rm occupied}$ are the free and occupied spaces, respectively. The robot operates in a workspace $\mbox{\ensuremath{\mathcal{W}}}\subseteq \mathbb{R}^3$ and is equipped with an onboard steerable RGB-D camera, controlled via the robot joints to observe the environment.

The goal of motion planning is to find a collision-free path $\boldsymbol{\pi}: [0, 1] \rightarrow \mbox{\ensuremath{\mathcal{C}_{\rm free}}}$, from the start configuration $\boldsymbol{\pi}(0) = \mbox{\ensuremath{q_{\rm start}}}$ to a goal region $\boldsymbol{\pi}(1) \in \mbox{\ensuremath{\mathcal{C}_{\rm goal}}}$. Along a path $\boldsymbol{\pi}$, the robot also aims to monitor a set ${\cal O}$ of $N$ objects of interest.

A motion cost $c_m(\boldsymbol{\pi})$, defined over the space of all possible paths $\Pi$, assigns a non-negative real number to each path $c_m: \Pi \rightarrow \mathbb{R}_{ \geq 0}$, e.g., its length, energy or control effort. To model the object monitoring constraints, we introduce a perception cost function $f: \mbox{\ensuremath{\mathcal{C}_{\rm free}}}\times {\cal O}\rightarrow \mathbb{R}_{\geq 0}
\label{eq:perception_function}$ that assigns each pair of configuration $\mathbf{q}\in \mbox{\ensuremath{\mathcal{C}_{\rm free}}}$ and object $o \in {\cal O}$ a scalar value, measuring the quality of the observation of $o$ by the onboard camera when the robot is at configuration $\mathbf{q}$. A lower perception quality implies a higher perception cost. We next define the overall perception cost at a configuration $\mathbf{q}$ as the weighted sum of the object-wise cost: $$\begin{equation}
p(\mathbf{q}) = \sum_{o \in {\cal O}} w_o \, f(\mathbf{q}, o),
\label{eq:perception_config}
\end{equation}$$ where the weight $w_o$ is a user-defined importance of monitoring object $o$. The cumulative perception cost of a path is: $$\begin{equation}
c_p(\boldsymbol{\pi}) = \int_0^1 p(\boldsymbol{\pi}(t)) \, dt,
\label{eq:perception_path}
\end{equation}$$ which aggregates the perception cost along the path $\boldsymbol{\pi}$. Our goal is to find the optimal path $\boldsymbol{\pi}^*$ that minimizes the weighted combination of motion and perception cost, *i.e.*, $$\begin{equation}
\begin{aligned}
    &\boldsymbol{\pi}^* = {\mathop{\mathrm{arg\,min}}}_{\boldsymbol{\pi}\in \Pi} \; c_m(\boldsymbol{\pi}) + \alpha c_p(\boldsymbol{\pi}), \\
    \text{s.t.} \quad &\boldsymbol{\pi}(t) \in \mbox{\ensuremath{\mathcal{C}_{\rm free}}}\quad\forall t\in [0,1],\\
    &\boldsymbol{\pi}(0) = q_{\rm start}, \boldsymbol{\pi}(1) \in \mbox{\ensuremath{\mathcal{C}_{\rm goal}}},
\end{aligned}
\label{eq:optimal_path}
\end{equation}$$ where the weighting factor $\alpha \geq 0$ controls the trade-off between motion and perception cost.

# Perception-aware Planner with Multi-Object Monitoring using Scene Graphs

An overview of [MOPS-PRM]{.smallcaps} is provided in [3.1](#sec:method_planner){reference-type="ref+label" reference="sec:method_planner"} with details on how we develop our perception-informed PRM construction [3.2](#sec:method_multiobject){reference-type="ref+label" reference="sec:method_multiobject"}, and how we augment a scene graph with the perception cost in [3.3](#sec:method_scenegraph){reference-type="ref+label" reference="sec:method_scenegraph"}.

## MOPS-PRM Planning {#sec:method_planner}

While finding the optimal trajectory in [\[eq:optimal_path\]](#eq:optimal_path){reference-type="ref+label" reference="eq:optimal_path"} is challenging due to the high-dimensional configuration space of high-[df]{.smallcaps} robots, our approach instead constructs a probabilistic roadmap (PRM) in the free space $\mathcal{C}_{\rm free}$ and searches for an optimal path $\boldsymbol{\pi}$ on the PRM from the start to the goal.

We define the PRM $G=(V,E)$, where $V$ is the set of $P$ collision-free configurations and $E$ the set of edges connecting them. The edges in $E$ are checked for collisions with obstacles by a validity checker, e.g., [@thomason2024vamp], during our PRM construction. The nodes are generated by a "perception-aware\" sampling scheme ([3.2](#sec:method_multiobject){reference-type="ref+label" reference="sec:method_multiobject"}), connected to their $k$-nearest neighbors and checked for collision, creating a set of PRM edges (see lines 14-19 of [\[alg:prm_pseudocode\]](#alg:prm_pseudocode){reference-type="ref+label" reference="alg:prm_pseudocode"}). Each edge $(\mathbf{q}_u, \mathbf{q}_v)$ is represented by a local motion $\boldsymbol{\pi}_{uv}(t), \; \boldsymbol{\pi}_{uv}(0) = \mathbf{q}_u, \; \boldsymbol{\pi}_{uv}(1) = \mathbf{q}_v$, which depends on the kinematic constraints of the robot, e.g., a Reeds-Shepp curve for the base of a non-holonomic mobile manipulator. Each edge $(\mathbf{q}_u, \mathbf{q}_v)$ is assigned a cost: $$\begin{equation}
c(\mathbf{q}_u, \mathbf{q}_v) = c_m(\boldsymbol{\pi}_{uv})+ \alpha \cdot c_p(\boldsymbol{\pi}_{uv}),
\label{eq:edge_cost}
\end{equation}$$ where $c_m(\boldsymbol{\pi}_{uv})$ is the edge's motion cost, e.g., the length or total control efforts of $\boldsymbol{\pi}_{uv}$, and $c_p(\boldsymbol{\pi}_{uv})$ is the edge's perception cost from Eq. [\[eq:perception_path\]](#eq:perception_path){reference-type="eqref" reference="eq:perception_path"}: $$\begin{equation}
     c_p(\boldsymbol{\pi}_{uv}) = \int_0^1 \sum_{o \in {\cal O}} w_o \, f(\boldsymbol{\pi}(t), o)\, dt.
\end{equation}$$ However, the perception cost $f(\mathbf{q}, o)$ for each pair $(\mathbf{q}, o)$ is typically unknown in advance for an arbitrary configuration $\mathbf{q}$. Therefore, we approximate the perception cost by a neural costmap $f_{\boldsymbol{\theta}}(\mathbf{q}, o)$ with parameter $\boldsymbol{\theta}$, trained on supervised data from an object detector and augmented to each object $o\in{\cal O}$ in a scene graph (see [3.3](#sec:method_scenegraph){reference-type="ref+label" reference="sec:method_scenegraph"}). As a result, the edge's perception cost is approximated as: $$\begin{equation}
    \label{eq:edge_perception_approx}
     c_p(\boldsymbol{\pi}_{uv}) \approx \sum_{k = 0}^{K-1} \sum_{o \in {\cal O}} w_o \, f_{\boldsymbol{\theta}}(\boldsymbol{\pi}(t_k), o)\,  \delta t, 
     \quad K \geq 2,
\end{equation}$$ where $t_0, t_1, \ldots, t_K$ are discrete times sampled along the edge with time steps $\delta t = \tfrac{1}{K}$.

After the PRM is constructed, [MOPS-PRM]{.smallcaps} connects the start and goal to the roadmap and applies an A\* search [@hart1968formal] with a consistent heuristic to find a path from $\mbox{\ensuremath{q_{\rm start}}}$ to $\mbox{\ensuremath{\mathcal{C}_{\rm goal}}}$ for the robot to follow. Following [@meng2025lookleapplanningsimultaneous], we define a consistent "hop\"-based heuristic function that lower-bounds the remaining path cost to the goal: $$\begin{equation}
h(\mathbf{q}) \;=\; H_{\min} \cdot c^{\min},
\label{eq:heuristic_def}
\end{equation}$$ where $H_{\min}(\mathbf{q})$ denotes the hop distance, i.e., the minimum number of edges required to reach the goal from the configuration $\mathbf{q}$ obtained via a shortest-path search, and $c^{\min}$ represents the minimum edge cost over the entire roadmap: $$\begin{equation}
\label{eq:min_edge_def}
c^{\min} = \min_{(u,v)\in E} c(\mathbf{q}_u, \mathbf{q}_v).
\end{equation}$$

For any $(u,v)\in E$, a feasible path from $u$ to the goal is to take $(u,v)$ and then follow a shortest path from $v$ to the goal. Thus, we have: $H_{\min}(\mathbf{q}_u) \le 1 + H_{\min}(\mathbf{q}_v)$.

Therefore, our heuristic function $h(\cdot)$ is consistent: $$\begin{align*}
h(\mathbf{q}_u) 
     &\le (1+H_{\min}(\mathbf{q}_v))\cdot c^{\min}\\
     &\le c(\mathbf{q}_u,\mathbf{q}_v) + h(\mathbf{q}_v).
        &&\text{by \cref{eq:min_edge_def,eq:heuristic_def}}
\end{align*}$$

This formulation only requires nonnegativity of edge costs, without assuming a specific form such as Euclidean distance for motion cost. It applies broadly, e.g., when $c_m$ is defined as the trajectory length, energy, or control effort, and $c_p$ is a non-negative cost derived from neural perception scores. The weight $\alpha$ controls the tradeoff between the motion and perception costs, e.g., the higher the weight $\alpha$ is, the longer path the A\* search might return and vice versa.

The solution returned solves [\[eq:optimal_path\]](#eq:optimal_path){reference-type="ref+label" reference="eq:optimal_path"} only for trajectories that lie on the PRM. However, as the number of nodes increases, the solution asymptotically converges to the true optimal trajectory. [MOPS-PRM]{.smallcaps} is illustrated in [\[alg:prm_pseudocode\]](#alg:prm_pseudocode){reference-type="ref+label" reference="alg:prm_pseudocode"} with implementation details provided in [4.1](#sec:implementation){reference-type="ref+label" reference="sec:implementation"}.

::: algorithm
$V,E \leftarrow \emptyset$
:::

## Perception-aware Sampling {#sec:method_multiobject}

An important subroutine in [MOPS-PRM]{.smallcaps} is to sample a set of nodes for roadmap construction. As the configuration space is high-dimensional, it is beneficial to bias the sampling process towards regions with low perception cost. Given a sampled configuration $\mathbf{q}_0 \in \mbox{\ensuremath{\mathcal{C}_{\rm free}}}$, we would like to find a nearby $\mathbf{q}^*$ that minimizes the perception cost: $$\begin{equation}
\label{eq:ideal_proj}
\mathbf{q}^* = {\mathop{\mathrm{arg\,min}}}_{\mathbf{q}\in {\cal C}_{free}} \; 
\Big( p(\mathbf{q}) + \lambda \|\mathbf{q}- \mathbf{q}_0\|_2^2 \Big),
\end{equation}$$ where $p(\mathbf{q})$ is the perception cost in [\[eq:perception_config\]](#eq:perception_config){reference-type="ref+label" reference="eq:perception_config"} and the distance $\|\mathbf{q}- \mathbf{q}_0\|_2^2$ is a regularization term with coefficient $\lambda$ to penalize large deviation from $\mathbf{q}_0$. However, solving [\[eq:ideal_proj\]](#eq:ideal_proj){reference-type="ref+label" reference="eq:ideal_proj"} exactly is challenging for our PRM construction, as the perception cost is approximated by: $$\begin{equation}
 \label{eq:approx_perception_cost}
    p(\mathbf{q})~\approx~\sum_{o \in {\cal O}} w_o \, f_{\boldsymbol{\theta}}(\mathbf{q}, o),
\end{equation}$$ with a nonlinear neural costmap $f_{\boldsymbol{\theta}}(\mathbf{q}, o)$. Instead, we introduce a perception-aware local sampling scheme that empirically approximates $\mathbf{q}^*$ in two stages, as outlined in [\[alg:prm_pseudocode\]](#alg:prm_pseudocode){reference-type="ref+label" reference="alg:prm_pseudocode"}. The first stage (lines 1--7 of [\[alg:prm_pseudocode\]](#alg:prm_pseudocode){reference-type="ref+label" reference="alg:prm_pseudocode"}) projects the sampled configuration $\mathbf{q}_0$ on a constrained manifold, where the camera pose points toward the objects. The second stage (lines 8--12) performs local sampling around each projection and selects the configuration with the lowest perception cost.

In the first stage, given the sample $\mathbf{q}_0$, we calculate the camera pose via forward kinematics, and generate viewpoint candidates by projecting the camera optical axis toward a set ${\cal X}_{\cal O}$ of $\big(N~+~\tbinom{N}{2}~+~1\big)$ desired centroids, consisting of the centroid of each object $o \in {\cal O}$, the centroid of each object pair, and the centroid of all objects collectively. This captures common cases where potentially the best viewpoint either focuses on observing a single object, all objects, or the transition between a pair of objects.

After experimentation, we observed that lower perception costs are obtained when the camera's optical axis is aligned with the object centroid (as illustrated in the "Multi-Object Constrained Sampling" block in [2](#fig:approach_diagram){reference-type="ref+label" reference="fig:approach_diagram"}). Let $\mathbf{m}(\mathbf{q}) \in \mathbb{R}^3$ denote the camera center, $\mathbf{z}(\mathbf{q}) \in \mathbb{S}^2$ the unit optical axis, and $\mathbf{x}_c \in \mathbb{R}^3$ the 3-D coordinates of the desired centroid $c \in \mathcal{X}_{\mathcal{O}}$. We define the lateral (image-plane) projection residual as $$\begin{equation}
\boldsymbol{\phi}(\mathbf{q},c) := 
\big(\mathbf{I}_3 - \mathbf{z}(\mathbf{q})\mathbf{z}(\mathbf{q})^\top\big)\,
\big(\mathbf{x}_c - \mathbf{m}(\mathbf{q})\big) \in \mathbb{R}^3,
\end{equation}$$ where $\mathbf{I}_3$ is the $3\times 3$ identity matrix [@ma2004invitation]. The matrix $\mathbf{P}(\mathbf{q}) = \mathbf{I}_3 - \mathbf{z}(\mathbf{q})\mathbf{z}(\mathbf{q})^\top$ is the orthogonal projector onto the tangent plane of $\mathbb{S}^2$ at $\mathbf{z}(\mathbf{q})$, i.e., $\mathbf{z}(\mathbf{q})^\top \boldsymbol{\phi}(\mathbf{q},c)=0$ and the residual $\boldsymbol{\phi}(\mathbf{q},c)$ has only two degrees of freedom corresponding to the lateral error in the image plane. We then project $\mathbf{q}_0$ onto a configuration, whose camera pose aligns with the centroid $c \in {\cal X}_{\cal O}$ by solving: $$\begin{equation}
\label{eq:projection_argmin}
\begin{aligned}
\mathbf{q}_0^{c} &= \mathop{\mathrm{arg\,min}}_{\mathbf{q}\in\mathbb{R}^k}\;
 \|\boldsymbol{\phi}(\mathbf{q},c)\|^2 + \lambda \|\mathbf{q}- \mathbf{q}_0\|^2_2 \\[2pt]
\text{s.t.}\quad
& \mathbf{q}\in {\cal C}_{\mathrm{free}},\; \|\mathbf{q}- \mathbf{q}_0\|_2 \le \rho,
\end{aligned}
\end{equation}$$ where $\lambda \ge 0$ is a regularization weight that encourages the solution to be close to $\mathbf{q}_0$, and $\rho > 0$ is an optional trust-region radius restricting the projection to a ball around $\mathbf{q}_0$. The parameters $\lambda$ and $\rho$ allow us to balance between the PRM coverage of the configuration space and biased sampling towards regions with low perception cost. For a large $\lambda$/small $\rho$, the projected point $\mathbf{q}_0^c$ stays close to the uniformly sampled $\mathbf{q}_0$, encouraging more even coverage of the configuration space. For a small $\lambda$/large $\rho$, the projected point $\mathbf{q}_0^c$ tends to be biased towards regions with low perception cost. The projection problem [\[eq:projection_argmin\]](#eq:projection_argmin){reference-type="ref+label" reference="eq:projection_argmin"} can be solved efficiently via gradient descent, e.g., using an L-BFGS-B solver [@zhu1997lbfgsb]. If the optimization does not converge within the iteration limit, we discard the sample $\mathbf{q}_0$ and obtain a new one.

In the second stage, we sample $M$ configurations $\{\mathbf{q}_{0(i)}^{c}\}_{i = 1}^M$ around each projected $\mathbf{q}_0^c$ by adding a zero-mean Gaussian noise $\mathbf{n}\sim {\cal N}(\bf0, \boldsymbol{\Sigma})$ so that the corresponding camera's field of view (FOV) will still capture the centroid $c \in {\cal X}_{\cal O}$. This process generates a set of $\big(N~+~\tbinom{N}{2}~+~1\big)(M+1)$ candidates: ${\cal C}_{\mathbf{q}_0}~=~
\left\{ \bigcup_{c\in {\cal X}_{\cal O}} \{\mathbf{q}_{0(i)}^{c}\}_{i = 1}^M \cup \{\mathbf{q}_0^c\}\right\}$. The perception cost of all candidates in ${\cal C}_{\mathbf{q}_0}$ is calculated via [\[eq:approx_perception_cost\]](#eq:approx_perception_cost){reference-type="ref+label" reference="eq:approx_perception_cost"} efficiently in parallel using the neural costmap $f_{\boldsymbol{\theta}}(\mathbf{q}, o)$ (see [3.3](#sec:method_scenegraph){reference-type="ref+label" reference="sec:method_scenegraph"}). The candidate with the lowest perception cost: $\mathbf{q}_{\mathrm{node}} = \mathop{\mathrm{arg\,min}}_{\mathbf{q}\in {\cal C}_{\mathbf{q}_0}} p(\mathbf{q})$, is added to our perception-aware PRM (lines 12-13 in [\[alg:prm_pseudocode\]](#alg:prm_pseudocode){reference-type="ref+label" reference="alg:prm_pseudocode"} and "Local Sampling" block in [2](#fig:approach_diagram){reference-type="ref+label" reference="fig:approach_diagram"}).

## Embedding Perception Costs in Scene Graphs {#sec:method_scenegraph}

Many perception constraints can be characterized by a scalar score $s$, such as the confidence value output $s \in [0,1]$ of an object detection model, *i.e.*, YOLOE [@wang2025yoloe], which can be converted to a perception cost $l$, e.g., $\ell = 1 - s$ or $\ell = 1/s$. To efficiently query the cost during PRM construction, we train a neural network $f_{\boldsymbol{\theta}}(q,o)$ that predicts the perception cost of a pair of configuration $\mathbf{q}\in \mbox{\ensuremath{\mathcal{C}_{\rm free}}}$ and object $o \in {\cal O}$. The network $f_{\boldsymbol{\theta}}(q,o)$ is pre-trained on a wide range of common objects, e.g., representative objects in a home or a hospital, and can be used across different environments. We consider the robot's forward kinematics as a non-trainable first layer of the neural network, calculating the camera pose from the configuration $\mathbf{q}$. The input of the second layer is the relative pose between the robot's onboard camera and the object $o$, together with an encoding of the object's semantic class, such as *monitor* or *human*. This is followed by a neural network, such as a multi-layer perceptron (MLP), that outputs an estimate of the perception cost $f(\mathbf{q}, o)$.

The training dataset ${\cal D}~=~\{(\mathbf{q}_i, o_i, s_i)\}_{i = 1}^D$ is generated using a task-specific perception model, which provides the perception score $s_i$ for each robot-object pair $(q_i, o_i)$. The neural costmap $f_{\boldsymbol{\theta}}$ is trained via supervised learning to fit the dataset ${\cal D}$, enabling batched parallel evaluation of perception costs. In practice, not all objects in the scene graph are assigned a perception costmap; only those important to monitor are given this attribute.

# Experimental Results {#sec:experiment}

In our experiments, we verify the effectiveness of our multi-object perception-aware scene-graph-based PRM with simulated and real-robot experiments using the Hello Robot's Stretch $2$ [@kemp2022design] and Isaac Sim [@nvidia2022isaacsim] for simulation and visualization. The Stretch 2 is a high-[df]{.smallcaps} mobile manipulator: in our experiments, we control its differential-drive, non-holonomic base (3 DoF) together with the pan--tilt joints of the onboard camera, introducing nontrivial kinematic constraints, leading to a challenging perception-aware planning problem. All experiments were conducted on an Intel i7-12700K CPU and an NVIDIA GeForce RTX4090 GPU.

## Implementation Details {#sec:implementation}

While [MOPS-PRM]{.smallcaps} planner can admit different motion and perception costs, and different forms of scene graphs, we present the specific implementation choices that we used.

The motion cost $c_m(\boldsymbol{\pi})$ of a path $\boldsymbol{\pi}$ is computed as the sum of the Euclidean distances of all individual edges along the path. For the A\* heuristic in [\[eq:heuristic_def\]](#eq:heuristic_def){reference-type="ref+label" reference="eq:heuristic_def"}, we use the Euclidean distance between the current configuration $\mathbf{q}$ and the goal as the motion component. Meanwhile, the perception cost label $\ell$, used to train our neural costmap in [3.3](#sec:method_scenegraph){reference-type="ref+label" reference="sec:method_scenegraph"}, is chosen as a quadratic function $(1-s)^2$, where $s$ is the confidence score provided by the object detector YOLOE [@wang2025yoloe]. We chose this perception cost to emphasize on higher confidence scores, guiding the planner to favor views that yield more reliable detections. As the motion cost and the perception cost have different units and ranges, we normalize both costs to the range $[0,1]$ using their minimum and maximum values over the entire roadmap, easing parameter tuning for the weight $\alpha$.

For perception-aware sampling in [3.2](#sec:method_multiobject){reference-type="ref+label" reference="sec:method_multiobject"}, an L-BFGS-B  solver [@zhu1997lbfgsb] is used to solve [\[{eq:projection_argmin}\]](#{eq:projection_argmin}){reference-type="ref+label" reference="{eq:projection_argmin}"} with parameters $\rho =0.05$, $\lambda = 0.3$, and the maximum iterations set to 100. For the local sampling function in the second stage, we choose $M=5$ and use a Gaussian noise $\mathbf{n}\sim {\cal N}(\bf0, \mathbf{I})$. For the PRM nearest-neighbor selection in line 14 of [\[alg:prm_pseudocode\]](#alg:prm_pseudocode){reference-type="ref+label" reference="alg:prm_pseudocode"}, the number of neighbors is set to be 5, empirically balancing graph connectivity and computational efficiency.

:::: {#fig:simulation_experiment .figure latex-placement="t"}
![](Meng2026SamplingBased_figs/Simulation-MOPSPRM.png){width="\\columnwidth"}

::: caption
In our simulated benchmarks, the robot moves from a start to a goal in an office environment while monitoring the four screens of the monitors placed on the table. The robot takes the longer path to observe the monitors, where the arrows illustrate the camera orientations. The bottom plot shows the camera pan-tilt joint angles along the trajectory.
:::
::::

:::: {#fig:real_robot_dynamic .figure latex-placement="t"}
![](Meng2026SamplingBased_figs/real-robot-experiment.png){width="\\textwidth"}

::: caption
In this real-robot experiment, the robot plans two different paths with the same start (shown in red) and goal (shown in green) based on a user-specified importance of the two paintings: the yellow path prioritizes painting 1, while the blue path prioritizes painting 2. Both paths start by observing a human with a monitor and end by looking at another human sitting at the table while the middle sections of the paths differ as they prioritize observing different paintings.
:::
::::

::: table*
[]{#tab:planning-results label="tab:planning-results"}
:::

We build our scene graph from camera images using the Khronos framework [@schmid2024khronos]. At the lowest layer, the scene graph contains a semantically annotated mesh of the environment geometry, representing obstacles in the environment, which we convert into a parallelization-friendly CAPT point cloud [@ramsey2024collision], allowing us to perform collision checking efficiently using fine-grained parallelism.

The neural cost function in [3.3](#sec:method_scenegraph){reference-type="ref+label" reference="sec:method_scenegraph"} is implemented as a multilayer perceptron (MLP) [@rumelhart1986learning] with five fully connected layers of 256 units and ReLU activations. For the training dataset, we uniformly sample $50000$ robot-independent camera poses in Isaac Sim that keep the object in view. These viewpoints are not tied to a specific robot configuration and can be used with any high-[df]{.smallcaps} platform via forward kinematics. We then render the corresponding images and evaluate perception costs using the YOLOE [@wang2025yoloe] model. The neural cost function is trained on these perception costs across diverse objects and humans from the COCO dataset [@lin2014microsoft], ensuring applicability to both real and simulated experiments.

## Multi-Object Detection in a Simulated Office {#sec:experiment_simulation}

We evaluate our approach in a simulated environment containing objects commonly found in an office, such as tables, chairs, humans, and monitors (an example is shown in  [3](#fig:simulation_experiment){reference-type="ref+label" reference="fig:simulation_experiment"}). This setting reflects typical scenarios faced by robotic assistants in office environments, where the robot must perform navigation or delivery tasks while monitoring multiple task-relevant objects, such as screens or humans. The task is to plan collision-free motions from a start to a goal while ensuring that the robot maintains visibility of monitors placed around the environment. To generate test cases, we sample $100$ motion planning problems by selecting random collision-free start and goal configurations on opposite sides of the room, ensuring that the robot must traverse the environment while balancing motion and perception costs. As illustrated in [3](#fig:simulation_experiment){reference-type="ref+label" reference="fig:simulation_experiment"}, we place the objects of interest in physically plausible locations (e.g., resting on a surface rather than floating in the air) to create realistic and meaningful scenarios for evaluation.

We compare [MOPS-PRM]{.smallcaps} against three baselines: "Closest-Object Low-[df]{.smallcaps}", "Closest-Object", and "Lowest-Cost-Object". At a configuration $\mathbf{q}$, "Closest-Object Low-[df]{.smallcaps}" and "Closest-Object" always monitor the nearest object by projecting the camera view toward it, while "Lowest-Cost-Object" selects the object with the lowest perception cost as evaluated by the same neural cost function used in [MOPS-PRM]{.smallcaps}. In "Closest-Object Low-[df]{.smallcaps}", planning is restricted to the non-holonomic base with all other joints fixed, resembling perception-aware planning for aerial or ground robots. A comparison on the movement of camera joints is included in [3](#fig:simulation_experiment){reference-type="ref+label" reference="fig:simulation_experiment"}, with sample paths from the same environment. Both "Closest-Object Low-[df]{.smallcaps}" and "Closest-Object" define the perception cost as the distance to the selected object, whereas "Lowest-Cost-Object" instead uses the neural cost function of [MOPS-PRM]{.smallcaps}. We set time limits for PRM construction, adapted from OMPL [@sucan2012open], to ensure similar number of nodes across all methods: 5 seconds for "Closest-Object Low-[df]{.smallcaps}" and "Closest-Object", and 30 seconds for "Lowest-Cost-Object" and [MOPS-PRM]{.smallcaps}.

Perception performance is evaluated using YOLOE [@wang2025yoloe] for object detection and Deep SORT [@Wojke2017simple] for tracking, whose "track rate\" metric describes the benefits of continuously monitoring multiple objects beyond detection. One key metric is the average number of objects detected per frame, $\overline{D}$, which measures frame-to-frame visual coverage by averaging the number of detected objects across all frames along a trajectory. Detection confidence is measured in two forms: the average confidence $\overline{C}$, computed as the mean confidence score $s_i$ over all successful detections in the set $S$, and the scaled average confidence $\overline{C}_\mathrm{sc} = \overline{D}\,\overline{C}$, which emphasizes the ability to maintain both high-confidence detections and consistent multi-object coverage along the trajectory.

[\[tab:planning-results\]](#tab:planning-results){reference-type="ref+label" reference="tab:planning-results"} summarizes the results across the 100 planning problems. Both "Closest-Object Low-[df]{.smallcaps}" and "Closest-Object" incur lower computational overhead, as reflected in their significantly faster PRM construction and planning times. However, their strict focus on the nearest object leads to reduced coverage, evident from a lower average number of objects detected per frame $\overline{D}$. Their confidence metrics also lag behind, since they do not account for accurate perception cost estimates from each robot configuration. Meanwhile, the 'Lowest-Cost-Object'' baseline achieves confidence scores comparable to [MOPS-PRM]{.smallcaps} by leveraging the neural cost function, but its inability to consider multiple objects simultaneously results in our method achieving more than $\sim 36\%$ improvement in the average number of detected objects per frame and a $\sim 17\%$ higher track rate. For this "track rate" metric, [MOPS-PRM]{.smallcaps} achieves the highest performance clearly surpassing all baselines. This highlights the advantage of continuously monitoring multiple objects beyond mere single-frame detection. While the baselines may achieve slightly shorter planning times or path lengths by focusing on an object at a time, [MOPS-PRM]{.smallcaps} explicitly accounts for multi-object monitoring, and hence, substantially improves perception performance.

[5](#fig:prm_statistics_plot){reference-type="ref+label" reference="fig:prm_statistics_plot"} illustrates how our planner's performance scales with the PRM size and the number of objects. With the number of objects fixed at $5$, increasing the PRM size increases roadmap construction time, while planning time remains low, typically around or below one second. The average number of detections per frame also increases, indicating that a denser roadmap supports more stable perception quality. When the PRM size is fixed at roughly 300 nodes, adding more objects drives up construction time and modestly increases planning time. At the same time, perception performance improves as the number of PRM nodes or objects increases, as reflected in higher average detections per frame. While the PRM construction is time-consuming, it only occurs once, and can be reused multiple times for path generation.

The results suggest that our approach remains practical as the problem size increases, with most of the overhead concentrated in the one-time construction stage.

## Real Robot Experiments {#sec:experiment_real}

As shown in [4](#fig:real_robot_dynamic){reference-type="ref+label" reference="fig:real_robot_dynamic"}, the robot is placed in an indoor environment and is tasked to move from a starting position shown in red to the corner of the room shown in green. To reach this goal, the robot must pass through a narrow passage created by an intervening chair, resulting in a challenging scenario with multi-modal solutions and high collision risks.

Unlike the simulation experiments, this setup introduces a different challenge, since the objects are farther apart and facing different directions. While monitoring multiple objects simultaneously, the robot must transition its focus between different objects of interest while maintaining smooth motion and maximizing perception scores along the trajectory.

The robot is tasked to consider the monitor near its starting position and a person near the end position, while detecting one of two objects, either a robot painting (painting 1) or a landscape painting (painting 2) placed on a cabinet, as shown in [4](#fig:real_robot_dynamic){reference-type="ref+label" reference="fig:real_robot_dynamic"}. The priority of monitoring each object is encoded by user-defined weights, as described in [3.1](#sec:method_planner){reference-type="ref+label" reference="sec:method_planner"}.

[4](#fig:real_robot_dynamic){reference-type="ref+label" reference="fig:real_robot_dynamic"} illustrates how [MOPS-PRM]{.smallcaps} generates trajectories based on which painting is prioritized. The two resulting paths are shown in yellow and blue, each highlighting a representative robot configuration along the path corresponding to the case where the respective painting is given higher weight. Averaged over 100 runs, our planner takes around 1.64 seconds to generate each plan and takes around 30.0 seconds to build the PRM. The path length for this experiment, measured as the Euclidean distance at all 5-[df]{.smallcaps} edges of the path, is around 19.13 for the yellow path and around 18.10 for the blue path. The average number of objects detected in each frame is around 0.84 on the yellow path and 0.81 on the blue path. This experiment demonstrates the planner's ability to monitor multiple objects while respecting the assigned weights of each object of interest.

:::: {#fig:prm_statistics_plot .figure latex-placement="t"}
![](Meng2026SamplingBased_figs/prm_plot.png){width="\\columnwidth"}

::: caption
Performance of [MOPS-PRM]{.smallcaps} under varying number of objects and PRM sizes. In the first column, the number of objects is fixed at five. In the second, PRM size is approximately 300 nodes. We report the planning and PRM construction times, and the average number of detections per frame.
:::
::::

# Discussion {#sec:conclusion}

We develop [MOPS-PRM]{.smallcaps}, a roadmap-based perception-aware motion planner for high-[df]{.smallcaps} robots tasked with multi-object monitoring. Perception awareness is modeled via a costmap anchored to objects of interest in a scene graph, guiding the perception-aware PRM construction and A\* search to produce paths that balance motion efficiency with perception quality. This enables applications such as museum patrol, patient monitoring, or industrial inspection where robots must move efficiently while maintaining visibility of key objects. As scene graphs have shown tremendous potential for task and motion planning in semantically rich environments, our work serves as a first step towards perception-aware task and motion planning for high-[df]{.smallcaps} robots, and can be further extended to leverage the scene graph's topology for perception-aware task-level reasoning. Besides, we also aim to extend the framework to include tree-based planners (e.g., RRT variants), handle map uncertainty for more robust planning, explore perception-aware motion planning in dynamic and interactive environments, and handle previously unseen objects, e.g., by incorporating open-set object detection [@liu2024grounding].

[^1]: $^{1}$Qingxi Meng, Emiliano Flores, and Thai Duong are with Department of Computer Science, Rice University, Houston, TX 77005 USA `qm15@rice.edu`

[^2]: $^{2}$Vaibhav Unhelkar and Lydia E. Kavraki are with the Department of Computer Science, Rice University, Houston, TX 77005 USA, and also with Ken Kennedy Institute, Rice University, Houston, TX 77005 USA. `vaibhav.unhelkar@rice.edu; kavraki@rice.edu`

[^3]: $^{*}$ Equal contribution.
