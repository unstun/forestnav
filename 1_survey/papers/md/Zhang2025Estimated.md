---
citation_key: Zhang2025Estimated
arxiv_id: 2508.21549
arxiv_url: https://arxiv.org/abs/2508.21549
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:31:29Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Estimated informed sampling, sampling-based planning, optimal path planning.
:::

# Introduction

planning is a fundamental challenge in robotics, aiming to devise a feasible path for a robot while avoiding collisions. This task can be framed as finding collision-free paths from a start to a goal state in state space while avoiding obstacles [@Gammell2021; @zhang2024review]. In practical applications, path planning for robot manipulators remains computationally intensive, particularly in high-dimensional spaces. The most resource-demanding aspect of this process is often the collision checking step. To address these challenges, a variety of methods have been developed, each designed to enhance the efficiency and effectiveness of robot path planning.

Popular graph-based algorithms, such as Dijkstra's [@dijkstra1959note], find the shortest path by exploring all routes in a discrete graph, while the A\* algorithm [@hart1968formal] improves efficiency with heuristic search. The Anytime Repairing A\* (ARA\*) [@likhachev2003ara] provides progressively optimal solutions, ensuring feasible paths at *anytime*. However, applying these methods to continuous spaces requires discretization, which is either sparse (yielding suboptimal paths) or dense (incurring high computational costs due to the *curse of dimensionality* [@bellman1957dynamic]). [To tackle this trade-off, sampling-based planners such as Rapidly-exploring Random Trees (RRT) [@LaValle1998], Expansive Space Trees (EST) [@Hsu2002], and Probabilistic Roadmaps (PRM) [@kavraki1998analysis] operate directly in the configuration space (*$\mathcal{C}$-space*). By sampling configurations and connecting them via local planners with collision checking, these methods efficiently solve high-dimensional planning problems without prior discretization of $\mathcal{C}$-space [@zhang2025apt].]{style="color: black"}

RRT-Connect [@kuffner2000rrt] extends RRT to efficiently find a path between two points in *$\mathcal{C}$-space* by utilizing two RRTs to connect start and goal states [@zhang2025G3t]. RRT\* [@karaman2011sampling] builds on RRT by incrementally rewiring the tree to ensure asymptotic optimality. [In the context of lazy collision checking [@strub2022adaptively], Lazy PRM [@bohlin2000path] and Lazy PRM\* [@hauser2015lazy] assume all edges are initially valid and delay the expensive collision checks until after a path is found.]{style="color: black"} This postponement of collision checks accelerates the planning process. To narrow the search domain, Informed RRT\* [@gammell2014informed] refines RRT\* by employing elliptical informed sampling rely on the current best solution cost (i.e., the *informed set*) [@gammell2014informed; @gammell2018informed], which simplifies the search and sampling set, thereby enhancing the convergence rate. The *greedy informed set* [@Phone2022greedyinformed] further improves convergence to the optimal solution by basing the informed set on the maximum admissible estimated cost of the current path. [Guided Incremental Local Densification (GuILD) [@Scalise2023] enhances path optimization by defining local subsets of problem domain via beacon selector. However, these sets can only be constructed when an initial solution has been found [@zhang2025fuzzy]. When no solution is available, the planners inefficiently re-sample and explore the entire *$\mathcal{C}$-space* [@gammell2018informed].]{style="color: black"}

:::: {#fig: elipseEIS .figure latex-placement="t!"}
::: caption
Illustration of the $L^2$ estimated informed set, it's determined by the start, goal states, and two key costs: the theoretical minimum cost $s_\textnormal{min}$ and the current expand *estimate initial solution* cost $\Tilde{s}_\textnormal{est}$.
:::
::::

In this article, we propose a novel sampling-based planner, Multi-Informed Trees (MIT\*), which is multi-informed by the prior admissible cost during the initial pathfinding and the current best cost during the optimization. The prior admissible cost is calculated from the lazy reverse search to construct an *estimated informed set* (Fig. [1](#fig: elipseEIS){reference-type="ref" reference="fig: elipseEIS"}). By combining prior costs with a reliability expansion factor, MIT\* explores within an ellipsoidal subset of the planning domain, thereby guiding the search while no initial solution has been established yet. Furthermore, MIT\* employs an adaptive sampler that adjusts its strategy based on the exploration process, which densifies distribution around obstacles. MIT\* improves reverse search by adjusting resolution based on edge length to enhance computational efficiency while maintaining search effectiveness.

[MIT\* outperforms state-of-the-art (SOTA) methods in initial solution time, initial solution cost (e.g., path length), and final solution cost (i.e., optimized path) across generalized simulation benchmarks and various real-world experiments.]{style="color: black"}

The contributions of this work are summarized as follows:

1.  *Estimated informed set:* Constructs a set before finding the initial path, using prior costs and expansion factors to effectively guide the exploration and sampling process.

2.  *Adaptive sampling strategy:* Integrates dynamic sampling adjustments to improve distribution around obstacles and in narrow corridors based on the exploration process.

3.  *Real-world application in robotic manipulation:* MIT\* was evaluated in versatile real-world tasks and achieved the highest success rate across multiple trials.

The rest of this article is organized as follows. Section [3](#sec:prob){reference-type="ref" reference="sec:prob"} introduces the problem definition. In Section [4](#sec:method){reference-type="ref" reference="sec:method"}, the MIT\* algorithm with the proof of asymptotic optimality, is presented in detail. Simulation and experimental results are discussed in Section [5](#sec:Expri){reference-type="ref" reference="sec:Expri"}. Finally, Section [6](#sec:conclu){reference-type="ref" reference="sec:conclu"} concludes this article.

# Related Work

In sampling-based motion planning, a common drawback is the slow convergence to an optimal solution. This section introduces popular methods to expedite path optimization.

## Informed Optimal Path Planning

Recently, researchers have proposed various heuristics to improve the convergence of sampling-based algorithms to an optimal path [@zhang2025dit; @wang2023; @ZHANG2025git]. Batch Informed Trees (BIT\*) [@gammell2020batch] builds on Informed RRT\* by constructing an implicit *random geometric graph* (RGG) [@penrose2003random] and performing a step-wise search similar to Lifelong Planning A\* (LPA\*) [@koenig2004lifelong]. BIT\* focuses on almost-surely asymptotic optimality by refining the RGG through batch processing [@Zhang2024adaptive], aggregating multiple state batches to form a denser graph over time, which reduces computational overhead while improving solution quality. Advanced BIT\* (ABIT\*) [@strub2020advanced] introduces inflation and truncation factors to balance exploration and exploitation in the denser RGG approximation, enhancing its effectiveness in complex environments. [Energy-efficient BIT\* for reconfigurable robots (EBITR\*) [@Phone2022greedyinformed] utilizes a greedy informed set, based solely on the maximum heuristic cost of the current solution's state. Adaptively Informed Trees (AIT\*) [@strub2022adaptively; @strub2020adaptively] use adaptive heuristics and an asymmetrical search strategy, incorporating sparse collision checks during the reverse search phase to improve precision by continuously updating the heuristic based on the evolving approximation. BiAIT\* [@Li2024] employs symmetrical bidirectional search for both heuristic and space searching. Effort Informed Trees (EIT\*) [@strub2022adaptively], a SOTA planner, utilize admissible cost (i.e., the lower bound on the true value) and effort heuristics (e.g., *the number of collision checks*) to optimize objectives with obstacle clearance [@Zhang2024Elliptical].]{style="color: black"}

Despite these advancements, these planners typically rely on uniform sampling strategies, which may struggle with critical zones such as narrow passages. Uniform sampling often has a lower probability of sampling in such challenging regions, potentially impacting the efficiency and effectiveness of pathfinding in complex, high-dimensional spaces.

::: {style="color: black"}
## Non-uniform Sampling Methods
:::

[Improved sampling strategies are crucial for navigating complex environments. Learning-based sampling [@Ichter2018] distribution from demonstrations using a conditional variational autoencoder, Neural RRT\* [@Wang2020] trains a neural network to perform nonuniform sampling, leading to more efficient tree expansion.]{style="color: black"} Techniques like Obstacle-based PRM (OBPRM) [@amato1998obprm] enhance sampling distribution near obstacles by generating samples close to obstacle surfaces through perturbation, which improves path discovery in constrained regions. Gaussian sampling [@boor1999gaussian] biases samples toward obstacle boundaries, increasing the likelihood of finding paths through tight spaces by placing one sample inside and another outside an obstacle's influence. Bridge test sampling [@hsu2003bridge] connects pairs of samples with a *bridge* to detect narrow passages, concentrating sampling efforts on critical pathways in cluttered environments. However, OBPRM may result in uneven sample distribution, Gaussian sampling assumes that data follows a normal distribution, and Bridge Test samplers focus only on the midpoint, potentially missing key samples along the edge.

In contrast to previous work, we utilize prior knowledge from lazy search attempts (i.e., prior admissible costs) to define the estimated informed set. Moreover, we implement an adaptive sampler that adjusts its sampling strategy dynamically and increases sampling density in critical zones.

# Preliminaries {#sec:prob}

[In this section, we first formulate the optimal path planning and then provide notations for the MIT\* algorithm (Alg. [\[alg: mit\]](#alg: mit){reference-type="ref" reference="alg: mit"}).]{style="color: black"}

## Problem Formulation

*Definition 1 (Optimal Planning):* Define a planning problem with the state space $X \subseteq \mathbb{R}^n$. Let $X_{\textnormal{obs}} \subset X$ represent states in collision with obstacles, and $X_{\textnormal{free}} = \textnormal{cl}(X \setminus X_{\textnormal{obs}})$ denote the resulting permissible states, where $\textnormal{cl}(\cdot)$ represents the *closure* of a set. The initial state is denoted by $\mathbf{x}_{\textnormal{start}} \in X_{\textnormal{free}}$, and the set of desired final states is $X_{\textnormal{goal}} \subset X_{\textnormal{free}}$. A sequence of states $\sigma: [0, 1] \mapsto X$ forms a continuous map (i.e., a collision-free path), and $\Sigma$ represents the set of all nontrivial paths [@karaman2011sampling].

[The optimal solution, represented as $\sigma^*$, corresponds to the path that minimizes a selected cost function $c: \Sigma \mapsto \mathbb{R}_{\geq 0}$. This path connects the initial state $\mathbf{x}_{\textnormal{start}}$ to any goal state $\mathbf{x}_{\textnormal{goal}} \in X_{\textnormal{goal}}$ through the free space: $$\begin{equation}
\begin{split}
    \sigma^* &= \arg \min_{\sigma \in \Sigma} \left\{ c(\sigma) \,\middle|\, \sigma(0) = \mathbf{x}_{\textnormal{start}}, \sigma(1) \in \mathbf{x}_{\textnormal{goal}}, \right. \\
    &\qquad\qquad \left. \forall t \in [0, 1], \sigma(t) \in X_{\textnormal{free}} \right\}.
\end{split}
\end{equation}$$ where $\mathbb{R}_{\geq 0}$ denotes the non-negative real numbers. The cost of the optimal path is $c^*$, and $t$ represents the continuous time parameter over the path $\sigma$. Considering set of states, $X_{\textnormal{samples}} \subset X$, as a graph where a transition function determines edges, we can describe its properties using a probabilistic model implicit in dense RGGs when these states are randomly sampled, i.e., $X_{\textnormal{samples}} = \{ \mathbf{x} \sim X_\textnormal{free} \}$, as discussed in [@penrose2003random].]{style="color: black"}

*Definition 2 (Potential subsets of problem domain):* Let $g(\mathbf{x}_\textnormal{})$ denote the cost of the optimal path from the start to a state $\mathbf{x}_\textnormal{} \in X_{\textnormal{free}}$, where the optimal *cost-to-come* is defined as: $$\begin{equation}
g(\mathbf{x}_\textnormal{}) := \min_{\sigma \in \Sigma} \{c(\sigma) \mid \sigma(0) = \mathbf{x}_\textnormal{start}, \sigma(1) = \mathbf{x}_\textnormal{}\},
\end{equation}$$ Let $h(\mathbf{x}_\textnormal{})$ denote the cost of the optimal path from $\mathbf{x}_\textnormal{}$ to the goal region, where the optimal *cost-to-go* is defined as: $$\begin{equation}
h(\mathbf{x}_\textnormal{}) := \min_{\sigma \in \Sigma} \{c(\sigma) \mid \sigma(0) = \mathbf{x}_\textnormal{}, \sigma(1) \in X_{\textnormal{goal}}\},
\end{equation}$$ [The cost of the optimal path from $\mathbf{x}_\textnormal{start}$ to $X_{\textnormal{goal}}$, constrained to pass through $\mathbf{x}_\textnormal{}$, is given by $f(\mathbf{x}_\textnormal{}) := g(\mathbf{x}_\textnormal{}) + h(\mathbf{x}_\textnormal{})$. This defines the states within the subsets that can potentially yield a solution better than the current solution $c_i$ as: $$\begin{equation}
{X}_\textnormal{subset} := \{ \mathbf{x}_\textnormal{} \in X_{\textnormal{free}} \mid f(\mathbf{x}_\textnormal{}) < c_i \}.
\end{equation}$$ The defined set ${X}_\textnormal{subset} \subseteq X$ represents a subset of the problem domain and depends on the cost (Fig. [1](#fig: elipseEIS){reference-type="ref" reference="fig: elipseEIS"}), as discussed in [@gammell2018informed].]{style="color: black"}

## Notation

 []{#subsec: notation label="subsec: notation"} The state space is defined as $X \subseteq \mathbb{R}^n$ with the initial state $\mathbf{x}_{\textnormal{init}} \in X$ and target states $X_{\textnormal{goal}} \subset X$. Sampled states are noted as $X_{\textnormal{sampled}}$. Forward and reverse trees are represented as $\mathcal{T_F} = (V_\mathcal{F}, E_\mathcal{F})$ and $\mathcal{T_R} = (V_\mathcal{R}, E_\mathcal{R})$, respectively. The nodes $V_\mathcal{F}$ and $V_\mathcal{R}$ correspond to valid states. Edges $E_\mathcal{F} \subset V_\mathcal{F} \times V_\mathcal{F}$ in the forward tree link validly connected states, while edges $E_\mathcal{R} \subset V_\mathcal{R} \times V_\mathcal{R}$ in the reverse tree may traverse invalid areas. Each edge $(\mathbf{x}_s, \mathbf{x}_t)$ connects source state $\mathbf{x}_s$ to target state $\mathbf{x}_t$.

The function $c: X \times X \rightarrow [0, \infty)$ denotes the actual cost (path length) of connecting two states, and $\hat{c}: X \times X \rightarrow [0, \infty)$ provides an approximation ensuring $\hat{c}(\mathbf{x}_i, \mathbf{x}_j) \leq c(\mathbf{x}_i, \mathbf{x}_j)$. The estimated costs from the initial state to any state are given by $\hat{g}(\mathbf{x}):= \hat{c}(\mathbf{x}_{\textnormal{start}}, \mathbf{x})$. The admissible cost heuristics to reach the goal are denoted by $\hat{h}(\mathbf{x}):= \min_{\mathbf{x}_{\textnormal{goal}} \in X_{\textnormal{goal}}} \hat{c}(\mathbf{x}, \mathbf{x}_{\textnormal{goal}})$. The forward tree cost from the initial state to a given state is $g_\mathcal{F}: X \rightarrow [0, \infty)$. The path cost from start to goal via a state is $\hat{f}(\mathbf{x}) := \hat{g}(\mathbf{x}) + \hat{h}(\mathbf{x})$. The informed set $X_{\hat{f}} := \{\mathbf{x} \in X | \hat{f}(\mathbf{x}) < c_\textnormal{curr} \}$ contains states that can improve the cost of the current solution, denotes as $c_\textnormal{curr}$.

Let $A$ be a set and $B, C$ be subsets of $A$. The notation $B \stackrel{+}{\leftarrow} C$ denotes $B \leftarrow B \cup C$ and $B \stackrel{-}{\leftarrow} C$ denotes $B \leftarrow B \setminus C$.

*MIT\* specific notation:* The admissible initial solution is denoted by ${\hat{\sigma}_\textnormal{adms}}$ and its cost by $\hat{s}_\textnormal{adms}: X \rightarrow [0, \infty)$. The estimated initial solution is denoted by ${\Tilde{\sigma}_\textnormal{est}}$ and its cost by $\Tilde{s}_\textnormal{est}$. The estimated informed set is denoted as $X_{\Tilde{\sigma}}$. The reliability parameter of $\hat{s}_\textnormal{adms}$ is $\gamma \in (0,1)$. The expand factor of $X_{\Tilde{\sigma}}$ is $e_{\gamma}$. The number of sparse checks per edge in iteration $k$ is $\Theta_\textnormal{sparse,$k$}$. The resolution of sparse checks for edges is $\Delta_\textnormal{sparse,$k$}$.

# Multi-Informed Trees (MIT\*) {#sec:method}

:::: {#fig:generalConcept .figure latex-placement="t!"}
![](Zhang2025Estimated_figs/sampler.png){width="90%"}

::: caption
The path planning process of MIT\* begins with initial sampling in the entire *$\mathcal{C}$-space* and selecting an adaptive sampler case. If no initial path/lazy path is found, re-sampling occurs in the entire *$\mathcal{C}$-space* (i.e., case 1). If a lazy path is found but invalid, sampling is conducted within the estimated informed set, expanding it when the lazy path cannot be improved (i.e., cases 2, 3). Upon finding a valid path, the informed set is calculated and optimized until the planner's termination condition is met (i.e., case 4).
:::
::::

In this section, we first introduce the concept of obstacle-based adaptive sampling. Next, we illustrate the estimated informed set. Then, we propose a sparse collision check based on the edge length. Finally, we analyze the probabilistic completeness and asymptotic optimality of MIT\*.

::: algorithm
[]{#alg: mit label="alg: mit"} [$X_{\textnormal{sampled}} \gets \{\mathbf{x}_\textnormal{start},\mathbf{x}_{\textnormal{goal}}\}$]{style="color: purple"}, $E_\mathcal{F} \gets \emptyset$, $\mathcal{T_F} = (V_\mathcal{F}, E_\mathcal{F})$\
$\Tilde{s}_\textnormal{est}\gets \infty$, $\gamma \gets \infty$, $e_{\gamma} \gets \infty$
:::

## Obstacle-Based Adaptive Sampler {#subsec: obs_sampler.}

::: algorithm
*$\mathbf{x}_\textnormal{pre} = \vec{0}, \mathbf{x}_\textnormal{temp} = \vec{0}, \mathbf{x}_\textnormal{crit} = \vec{0}$*\
\
:::

[The sampling strategy of the adaptive sampler is categorized into distinct scenarios. During sampling, the uniform sampler (Alg. [\[Alg:Sampler\]](#Alg:Sampler){reference-type="ref" reference="Alg:Sampler"}, line 3-10) is employed to generate the preliminary sampled state, denoted as $\mathbf{x}_{\textnormal{pre}}$, and for conducting the initial validity assessment.]{style="color: black"} The Gaussian distribution-generated temporary state (Alg. [\[Alg:Sampler\]](#Alg:Sampler){reference-type="ref" reference="Alg:Sampler"}, line 8) is denoted as $\mathbf{x}_{\textnormal{temp}}$. The state within the critical zone is denoted as $\mathbf{x}_{\textnormal{crit}}$. [The adaptive sampling process for valid and invalid states with obstacles-based sampled states distribution is detailed in Fig. [3](#fig:adaptiveSampler){reference-type="ref" reference="fig:adaptiveSampler"}.]{style="color: black"}

- *${\mathbf{x}_\textnormal{pre,val}}$:* Upon validation of preliminary samples ${\mathbf{x}_\textnormal{pre}}$, it is incorporated into the resultant sample set ${X}_\textnormal{sampled}$.

- *${\mathbf{x}_\textnormal{pre,inv}}$:* For an invalid ${\mathbf{x}_\textnormal{pre}}$, a Gaussian distribution is utilized to procure a temporary sampled state ${\mathbf{x}_\textnormal{temp}}$, positioned at a $\delta$ distance from ${\mathbf{x}_\textnormal{pre,inv}}$.

- *${\mathbf{x}_\textnormal{temp,val}}$:* If ${\mathbf{x}_\textnormal{temp}}$ is valid, it is added to set ${X}_\textnormal{sampled}$ to increase the density of samples close to obstacles.

- *${\mathbf{x}_\textnormal{temp,inv}}$:* When ${\mathbf{x}_\textnormal{temp}}$ is invalid, a binary search is conducted to locate a state ${\mathbf{x}_\textnormal{crit}}$ situated between ${\mathbf{x}_\textnormal{pre}}$ and ${\mathbf{x}_\textnormal{temp}}$, essentially on the edge (${\mathbf{x}_\textnormal{pre}}$, ${\mathbf{x}_\textnormal{temp}}$).

- *${\mathbf{x}_\textnormal{crit,val}}$:* Upon validation of ${\mathbf{x}_\textnormal{crit}}$, the first valid ${\mathbf{x}_\textnormal{crit}}$ is appended to set ${X}_\textnormal{sampled}$ to enhance the density of states in critical zones (e.g., narrow corridors, wall gaps).

- *${\mathbf{x}_\textnormal{crit,inv}}$:* If no viable area exists between ${\mathbf{x}_\textnormal{pre}}$ and ${\mathbf{x}_\textnormal{temp}}$, all ${\mathbf{x}_\textnormal{crit}}$ are invalid, the re-sampling process is recommenced.

:::: {#fig:adaptiveSampler .figure latex-placement="t!"}
![](Zhang2025Estimated_figs/sampler_progress_nolable.png){width="99%"}

::: caption
Four snapshots illustrate how the obstacle-based adaptive sampler adjusts its strategy. (a) depicts uniform sampling in the *$\mathcal{C}$-space* to generate valid/invalid preliminary sampled states (i.e., ${\mathbf{x}_\textnormal{pre,val}}$ and ${\mathbf{x}_\textnormal{pre,inv}}$), with the red dashed ellipsoid highlighting a critical zone which is often difficult to sample. (b) and (c) shows the sampler encountering ${\mathbf{x}_\textnormal{pre,inv}}$ when using uniform sampling; it employs a Gaussian distribution at distance $\delta$ to find temporary valid/invalid samples (i.e., ${\mathbf{x}_\textnormal{temp,val}}$ and ${\mathbf{x}_\textnormal{temp,inv}}$) around obstacles ($X_{\textnormal{obs}}$). (d) demonstrate that if the ${\mathbf{x}_\textnormal{temp,inv}}$ fall within $X_{\textnormal{obs}}$, the sampler tests along the connecting bridge between ${\mathbf{x}_\textnormal{pre,inv}}$ and ${\mathbf{x}_\textnormal{temp,inv}}$ to sample key points ${\mathbf{x}_\textnormal{crit,val}}$ in critical zone.
:::
::::

For the analysis of sample distributions in confined settings. We define the sampling distribution in the critical zone as a weighted mixture of probability functions $\pi_\textnormal{adapt}$. Let ${\Phi}_\textnormal{}(\cdot)$ be the probability density of any state $\mathbf{x}_\textnormal{} \in X_\textnormal{}$, thus: $$\begin{equation}
{\Phi}_\textnormal{}(\mathbf{x}_\textnormal{}):=
    \begin{cases}
        1 & \textnormal{if } \mathbf{x}_\textnormal{} \in {X}_\textnormal{obs}  \\
        0 & \textnormal{if }  \mathbf{x}_\textnormal{} \not\in {X}_\textnormal{obs}
    \end{cases} 
    \hspace{10pt}\textnormal{with}\hspace{10pt}\texttt{Vol}({X}_\textnormal{obs}) = 1,
\end{equation}$$ here, $\texttt{Vol}(\cdot)$ is the *$\mathcal{C}$-space* volume function. [The conditional probability density function of ${\mathbf{x}_\textnormal{temp}}$ given ${\mathbf{x}_\textnormal{pre}}$ is defined as: $$\begin{equation}
{\Phi}_\textnormal{}(\mathbf{x}_\textnormal{temp}|\mathbf{x}_\textnormal{pre}):=\rho_\textnormal{gau}(\mathbf{x}_\textnormal{temp})\mathcal{B}(\mathbf{x}_\textnormal{temp})/\Psi_\textnormal{const},
\label{eq:ftemp}
\end{equation}$$ where $\rho_\textnormal{gau}(\mathbf{x}_\textnormal{})$ is the density function of Gaussian distribution around ${\mathbf{x}_\textnormal{pre}}$, and $\mathcal{B}(\mathbf{x}_\textnormal{})$ is a binary function that $\mathcal{B}(\mathbf{x}_\textnormal{}) = 1$ when $\mathbf{x}_\textnormal{} \in X_\textnormal{obs}$, and 0 otherwise. $$\begin{equation}
\Psi_\textnormal{const} :=  \int_{X}{\rho_\textnormal{gau}(\mathbf{x}_\textnormal{temp})\mathcal{B}(\mathbf{x}_\textnormal{temp})}d\mathbf{x}_\textnormal{temp},
\end{equation}$$ where $\Psi_\textnormal{const} \in \mathbb{R}$ is a normalizing constant. Thus we have the probability $\pi_\textnormal{adapt}$ created by the adaptive sampler as: $$\begin{equation}
\pi_\textnormal{adapt}(\mathbf{x}_\textnormal{crit}) :=  \int_{X}{{\Phi}_\textnormal{}(\mathbf{x}_\textnormal{temp}|\mathbf{x}_\textnormal{pre}){\Phi}_\textnormal{}(\mathbf{x}_\textnormal{pre})}d\mathbf{x}_\textnormal{pre}.
\label{eq:piAdaptive}
\end{equation}$$ since ${\mathbf{x}_\textnormal{crit}}$ represents the sample points between line segment $\overline{\mathbf{x}_\textnormal{pre}\mathbf{x}_\textnormal{temp}}$, therefore the ${\mathbf{x}_\textnormal{temp}}$ can be defined as: $$\begin{equation}
\mathbf{x}_\textnormal{temp} := {\xi}_\textnormal{}\cdot\mathbf{x}_\textnormal{crit} - \mathbf{x}_\textnormal{pre},   \label{eq:xtemp}
\end{equation}$$ where $\xi \in \mathbb{R}^{+}$ is defined as the position of the ${\mathbf{x}_\textnormal{crit}}$, with its maximum value equal to the resolution of the state space. By substituting ${\Phi}_\textnormal{}(\mathbf{x}_\textnormal{temp}|\mathbf{x}_\textnormal{pre})$, ${\Phi}_\textnormal{}(\mathbf{x}_\textnormal{pre})$ and $\mathbf{x}_\textnormal{temp}$, we have: $$\begin{multline}
\pi_\textnormal{adapt}(\mathbf{x}_\textnormal{crit}) := \\
\int_{X \cap {X}_\textnormal{obs}}{\frac{\rho_\textnormal{gau}({\xi}_\textnormal{}\mathbf{x}_\textnormal{crit} - \mathbf{x}_\textnormal{pre})\mathcal{B}({\xi}_\textnormal{}\mathbf{x}_\textnormal{crit} - \mathbf{x}_\textnormal{pre})}{\Psi_\textnormal{const}}}d\mathbf{x}_\textnormal{pre}.
\end{multline}$$ where ${\Phi}_\textnormal{}(\mathbf{x}_\textnormal{pre}) = 1$ (preliminary invalid samples). The $\rho_\textnormal{gau}(\mathbf{x}_\textnormal{})$ is large if ${\mathbf{x}_\textnormal{temp}}$ lies close to ${\mathbf{x}_\textnormal{pre}}$, and the integrand in Eq. [\[eq:piAdaptive\]](#eq:piAdaptive){reference-type="ref" reference="eq:piAdaptive"} is non-zero only if ${\mathbf{x}_\textnormal{temp}}$ is invalid. Therefore, for a point ${\mathbf{x}_\textnormal{crit}}$ in critical zones, the probability density $\pi_\textnormal{adapt}$ is higher. ]{style="color: black"}

## Estimated Informed Set {#subsec: EIS.}

::: algorithm
:::

To expedite the search process, MIT\* introduces the concept of the admissible initial solution (${\hat{\sigma}_\textnormal{adms}}$), which is constructed based on the $\mathcal{T_F}$ that have undergone a full collision check and failed (Alg. [\[alg: mit\]](#alg: mit){reference-type="ref" reference="alg: mit"}, line 9). In this case, the forward tree is connected with the reverse tree by the edge that failed to pass the full collision check. Although this is a failed search attempt, its cost, denoted as ${\hat{s}_\textnormal{adms}}$, can still serve as a valuable heuristic for our path planning problem. A comprehensive definition of the cost of ${\hat{\sigma}_\textnormal{adms}}$ is provided as follows: $$\begin{equation}
\hat{s}_\textnormal{adms}:= g_{\mathcal{F}}(\mathbf{x}_s) + \hat{c}(\mathbf{x}_s,\mathbf{x}_t) + \hat{h}(\mathbf{x}_t),
\end{equation}$$ where $g_{\mathcal{F}}$ is the actual cost to come, $\hat{c}(\mathbf{x}_s,\mathbf{x}_t)$ is the edge cost, and $\hat{h}(\mathbf{x}_t)$ is the admissible cost to reach the goal. Traditional informed set construction delays sampling by requiring the exact solution cost. The ${\hat{\sigma}_\textnormal{adms}}$ approach enables an estimated informed set to guide sampling before the initial solution is found. However, directly using ${\hat{\sigma}_\textnormal{adms}}$ can overly restrict the estimated informed set, risking the omission of the exact solution. [We define the estimated initial solution ${\Tilde{\sigma}_\textnormal{est}}$, which is calculated using an expansion factor $e_{\gamma} > 1$ to expand the sampling range, and a reliability parameter $\gamma$ to determine ${\hat{s}_\textnormal{adms}}$, where: $$\begin{equation}
\label{eq:realiability}
\gamma := \frac{g_{\mathcal{F}}(\mathbf{x}_s)}{g_{\mathcal{F}}(\mathbf{x}_s) + \hat{c}(\mathbf{x}_s, \mathbf{x}_t) + \hat{h}(\mathbf{x}_t)} = \frac{g_{\mathcal{F}}(\mathbf{x}_s)}{\hat{s}_\textnormal{adms}}.
\end{equation}$$ The expansion factor is then computed as: $$\begin{equation}
\label{eq:expandFactor}
e_{\gamma} := \sqrt{1 + (1 - \gamma)^2},
\end{equation}$$ which serves to adjust the extent of the sampling range based on the reliability of the initial estimate. The optimal of $e_{\gamma}$ could be a potential direction for future work. ]{style="color: black"} This yields a hypothetical path ${\Tilde{\sigma}_\textnormal{est}}$, whose cost is denoted as ${\Tilde{s}_\textnormal{est}}$ and can be calculated as follows: $$\begin{equation}
{\Tilde{s}_\textnormal{est}:= \hat{s}_\textnormal{adms}\cdot e_{\gamma},}
\label{eq:cehis}
\end{equation}$$ with ${\Tilde{s}_\textnormal{est}}$, we can formulate the estimated informed set with the detailed definition provided in Fig. [2](#fig:generalConcept){reference-type="ref" reference="fig:generalConcept"} and Alg. [\[alg: updateEIS\]](#alg: updateEIS){reference-type="ref" reference="alg: updateEIS"}.

An estimated informed set, $X_{\Tilde{\sigma}}$, represents all states within ${{X}_\textnormal{free}}$, where any state $\mathbf{x} \in X_{\Tilde{\sigma}}$ can potentially be part of a path that has a lower cost than the cost of the current ${\Tilde{\sigma}_\textnormal{est}}$. This set can be mathematically described by the equation: $$\begin{equation}
    X_{\Tilde{\sigma}}:= \{ \mathbf{x} \in {X}_\textnormal{free} \mid \Tilde{f}(\mathbf{x}) < \Tilde{s}_\textnormal{est}\},
\end{equation}$$ where $\Tilde{f}(\mathbf{x}) := \Tilde{g}(\mathbf{x}) + \Tilde{h}(\mathbf{x})$ combines the cost to reach state $\mathbf{x}$ from the start $\Tilde{g}(\mathbf{x})$ and the cost from state $\mathbf{x}$ to the goal $\Tilde{h}(\mathbf{x})$. For problems where the objective is to minimize path length, the estimated informed set typically takes the shape of an $n$-dimensional prolate hyperspheroid or an ellipsoid that is elongated along one axis, which encompasses all points that can result in a path length less than ${\Tilde{s}_\textnormal{est}}$. The $n$-dimensional hyperellipsoid is defined by the initial position ${\mathbf{x}_\textnormal{start}}$ and terminal position ${\mathbf{x}_\textnormal{goal}}$, alongside two critical metrics: the cost of the ${\Tilde{\sigma}_\textnormal{est}}$ so far, ${\Tilde{s}_\textnormal{est}}$ and conjugate diameters of $\sqrt{\Tilde{s}_\textnormal{est}^2 - s_\textnormal{min}^2}$, where the minimal possible cost ${s_\textnormal{min}}$ comes from: $$\begin{equation}
    s_\textnormal{min}:= \| \mathbf{x}_\textnormal{goal} - \mathbf{x}_\textnormal{start}\|_2,
\end{equation}$$ here, the eccentricity of the ellipse is given by ratio $s_\textnormal{min}/\Tilde{s}_\textnormal{est}$. The estimated informed set is the intersection of the free space, ${{X}_\textnormal{free}}$, and an $n$-dimensional Hyper-Ellipsoid (${{X}_\textnormal{HES}}$) which symmetric about its transverse axis: $$\begin{equation}
    X_{\Tilde{\sigma}}= {X}_\textnormal{free} \cap {X}_\textnormal{HES},
\end{equation}$$ where $$\begin{equation}
{X}_\textnormal{HES} := \{\mathbf{x}_\textnormal{} \in \mathbb{R}^n \mid \|\mathbf{x}_\textnormal{} - \mathbf{x}_\textnormal{start}\|_2 + \|\mathbf{x}_\textnormal{goal} - \mathbf{x}_\textnormal{}\|_2 < \Tilde{s}_\textnormal{est}
\} .
\end{equation}$$

The estimated informed set ${X_{\Tilde{\sigma}}}$ in $\mathbb{R}^2$ can be directly defined using the $L^2$ norm (i.e., Euclidean distance): $$\begin{equation}
    X_{\Tilde{\sigma}}:= \{ \mathbf{x}_\textnormal{} \in {X}_\textnormal{free} \mid \|\mathbf{x}_\textnormal{} - \mathbf{x}_\textnormal{start}\|_2 + \|\mathbf{x}_\textnormal{goal} - \mathbf{x}_\textnormal{}\|_2 < \Tilde{s}_\textnormal{est}\},
\end{equation}$$

::: algorithm
:::

[To extend EIS into multiple goals scenarios based on informed set [@gammell2018informed], goal region $X_\textnormal{goal}:=\left\{\mathbf{x}_\textnormal{goal,o}\right\}_{o=1}^m$ set is the union of the individual estimated informed sets: $$\begin{equation}
X_{\Tilde{\sigma}}=\bigcup_{o=1}^mX_{\Tilde{\sigma},o},
\end{equation}$$ where $m$ is the number of goals in the problem domain, therefore the $o$-th EIS $X_{\Tilde{\sigma},o}$ can be described as: $$\begin{equation}
    X_{\Tilde{\sigma},o}:= \{ \mathbf{x}_\textnormal{} \in {X}_\textnormal{free} \mid \|\mathbf{x}_\textnormal{} - \mathbf{x}_\textnormal{start}\|_2 + \|\mathbf{x}_\textnormal{goal,o} - \mathbf{x}_\textnormal{}\|_2 < \Tilde{s}_\textnormal{est,o} \},
\end{equation}$$]{style="color: black"} The direct method to generate distributed samples via adaptive sampler in the estimated informed set is defined from direct sampling in subset [@gammell2014informed]. We define the $n$-dimensional hyper ellipsoid that contains an estimated informed set as: $$\begin{equation}
    {X}_\textnormal{HES} := \{ \mathbf{x}_\textnormal{} \in \mathbb{R}^n \mid (\mathbf{x}_\textnormal{} -\mathbf{x}_\textnormal{center})^T\mathbf{R}_\textnormal{}\mathbf{P}_\textnormal{}^{-1}\mathbf{R}_\textnormal{}^T(\mathbf{x}_\textnormal{} -\mathbf{x}_\textnormal{center}) < 1\},
\end{equation}$$ where $$\begin{equation}
    \mathbf{x}_\textnormal{center} := \frac{\mathbf{x}_\textnormal{start}+\mathbf{x}_\textnormal{goal}}{2},
\end{equation}$$ $$\begin{equation}
    \mathbf{P}_\textnormal{} := diag\left(\frac{\Tilde{s}_\textnormal{est}^2}{4},\frac{\Tilde{s}_\textnormal{est}^2-s_\textnormal{min}^2}{4},...,\frac{\Tilde{s}_\textnormal{est}^2-s_\textnormal{min}^2}{4}\right),
\end{equation}$$ where $\mathbf{P}_\textnormal{} \in \mathbb{R}^{n\cross n}$ is the positive symmetric matrix, and the rotation matrix ${\mathbf{R}_\textnormal{}}$ can be obtained by *minimizing a cost function* that measures the alignment error between the rotated hyperellipsoid's major axis and the first axis of the world frame. The cost function is typically defined as: $$\begin{equation}
    {J}_\textnormal{}(\mathbf{R}_\textnormal{}) := \|\mathbf{R}_\textnormal{}\mathbf{k}_\textnormal{1}-\mathbf{I}_\textnormal{1}\|^2,
\end{equation}$$ where $\mathbf{k}_\textnormal{1} \in \mathbb{R}^{n \cross 1}$ (Alg. [\[alg:sampleEIS\]](#alg:sampleEIS){reference-type="ref" reference="alg:sampleEIS"}, line 6) is the major axis of the rotated hyperellipsoid and $\mathbf{I}_\textnormal{1}\in \mathbb{R}^{n \cross 1}$ is the first column of the identity matrix, which represents the first axis of the world frame. Thus we can retrieve rotation matrix ${\mathbf{R}_\textnormal{}}$: $$\begin{equation}
    \mathbf{R}_\textnormal{} := \mathbf{U}_\textnormal{}\mathbf{\Lambda}_\textnormal{}\mathbf{V}_\textnormal{}^T,
\end{equation}$$ where diagonal matrix $\mathbf{\Lambda}_\textnormal{} \in \mathbb{R}^{n\cross n}$ is: $$\begin{equation}
    \mathbf{\Lambda}_\textnormal{}:=
    \begin{cases}
    \mathbf{I}_\textnormal{} & \textnormal{if } det(\mathbf{U}_\textnormal{}\mathbf{V}_\textnormal{}^T) = 1, \\
    diag(1,1,...,-1) & \textnormal{if }  det(\mathbf{U}_\textnormal{}\mathbf{V}_\textnormal{}^T) = -1.
    \end{cases},
\end{equation}$$ where $det(\cdot)$ is the matrix determinant. The unitary matrices $\mathbf{U}_\textnormal{} \in \mathbb{R}^{n\cross n}$ and $\mathbf{V}_\textnormal{} \in \mathbb{R}^{n\cross n}$ are defined by the singular value decomposition $\texttt{SVD}(\cdot)$, such as $\mathbf{U}_\textnormal{}\mathbf{\Sigma}_\textnormal{}\mathbf{V}_\textnormal{}^T \equiv \mathbf{B}_\textnormal{}$, and $\mathbf{B}_\textnormal{} \in \mathbb{R}^{n\cross n}$ is calculated by the outer product of axes: $$\begin{equation}
    \label{eq:MatrixB}
    \mathbf{B}_\textnormal{} := \mathbf{k}_\textnormal{1}\mathbf{I}_\textnormal{1}^T = ((\mathbf{x}_\textnormal{goal} - \mathbf{x}_\textnormal{start})/s_\textnormal{min})\mathbf{I}_\textnormal{1}^T.
\end{equation}$$ with predefined matrices, we can generate samples directly by transforming samples $\mathbf{x}_\textnormal{ball} \in {X}_\textnormal{ball}$ into a $\mathbf{x}_\textnormal{hes} \in {X}_\textnormal{HES}$. The ${{X}_\textnormal{ball}}$ is defined as: $$\begin{equation}
    {X}_\textnormal{ball} := \{ \mathbf{x}_\textnormal{} \in \mathbb{R}^n \mid \|\mathbf{x}_\textnormal{} \|_2 < 1\},
\end{equation}$$ and the transform is given by: $$\begin{equation}
    \mathbf{x}_\textnormal{hes} = \mathbf{R}_\textnormal{}\mathbf{L}_\textnormal{}\mathbf{x}_\textnormal{ball} + \mathbf{x}_\textnormal{center},
\end{equation}$$ where $\mathbf{L}_\textnormal{} \in \mathbb{R}^{n\cross n}$ is the lower-triangular Cholesky decomposition of the ${\mathbf{P}_\textnormal{}}$ such that: $$\begin{equation}
    \mathbf{L}_\textnormal{}\mathbf{L}_\textnormal{}^T\equiv\mathbf{P}_\textnormal{},
\end{equation}$$ the ${\mathbf{L}_\textnormal{}}$ can be written as: $$\begin{equation}
    \mathbf{L}_\textnormal{} := diag\left(\frac{\Tilde{s}_\textnormal{est}}{2},\frac{\sqrt{\Tilde{s}_\textnormal{est}^2-s_\textnormal{min}^2}}{2},...,\frac{\sqrt{\Tilde{s}_\textnormal{est}^2-s_\textnormal{min}^2}}{2}\right).
\end{equation}$$

This section defines the ${X_{\Tilde{\sigma}}}$ which re-projects *$\mathcal{C}$-space* set to the estimated hyperellipsoid set, and the pseudocode of direct sampling within the estimated informed set is given in Alg. [\[alg:sampleEIS\]](#alg:sampleEIS){reference-type="ref" reference="alg:sampleEIS"}.

## Length-related Adaptive Sparse Collision Check {#subsec: approx.}

Traditional sparse collision-checking methods are inefficient due to the fixed number of checks, $\Theta_\textnormal{sparse,$k$} \in \mathbb{N}^+$, to all edges. These methods eventually adapt, but their initial check level is not robust (i.e., only one check per edge), leading to inaccuracies. In contrast, MIT\* introduces a *length-related adaptive sparse collision-checking* strategy. MIT\* starts with an initial resolution, $\Delta_{\textnormal{sparse,ini}}$ (e.g., $5 \times 10^{-6}$ in simulation benchmark), and adjusts it according to the edge length, adapting the resolution for sparse collision checks as follows: [$$\begin{align}
    \Delta_{\textnormal{sparse,$k$}} &:= \Omega \cdot \Delta_{\textnormal{sparse,ini}}, \\
    \Theta_\textnormal{sparse,$k$} &:= \lfloor \frac{\| \mathbf{x}_\textnormal{s} - \mathbf{x}_\textnormal{t}\|_2}{\Delta_{\textnormal{sparse,$k$}}} + 1\rfloor.
\end{align}$$ here, $\lfloor \cdot \rfloor$ is the floor function for integers, $\Delta_{\textnormal{sparse,$k$}}$ is the next sparse-check resolution, $\Omega \in (0, 1)$ is the tuning parameter. ]{style="color: black"} The number of edge collision checks $\Theta_\textnormal{sparse,k}$ in $\mathcal{T_R}$ increases when the edge length is longer. This approach enables MIT\* to perform effective initial collision checks and adjust resolution, making the reverse search more reliable and problem-specific.

## Probabilistic Completeness and Asymptotic Optimality

Most sampling-based path planning algorithms have been proven to be probabilistically complete and asymptotically optimal, and MIT\* can also guarantee these two properties. As the number of iterations $k$ approaches infinity, the entire space will be explored, satisfying the following condition: $$\begin{equation}
\lim_{k \to \infty} \mathbb{P} (\{V_\mathcal{F}\cup V_\mathcal{R}\} \cap X_{\textnormal{goal}}) \neq \emptyset) = 1,
\end{equation}$$ which means that if there is a feasible path, it must be found by the MIT\*. Therefore, the probabilistic completeness of MIT\* is guaranteed.

The MIT\* implements the same Choose Parent and Rewire strategies as the EIT\*. It means that if the rewiring radius $r(q)$ in Choose Parent and Rewire processes satisfies: $$\begin{equation}
\label{eqn:radius r}
    r(q) > \eta \left(2 \left(1 + \frac{1}{n}\right){\left(\frac{\lambda(X_{\Tilde{\sigma}}\cup X_{\hat{f}})}{\zeta_n}\right) \left( \frac{\log(q)}{q}\right)}\right)^{\frac{1}{n}},
\end{equation}$$ here, $q$ denotes the number of sampled states in the sets, $\eta > 1$ is a tuning parameter, $n$ is the dimensionality of the workspace. The term $\lambda(X_{\Tilde{\sigma}}\cup X_{\hat{f}})$ represents the Lebesgue measure of the union of the estimated informed set ${X_{\Tilde{\sigma}}}$, and the informed set $X_{\hat{f}}$, where ${X_{\Tilde{\sigma}}}$ is used in *initial pathfinding* phase and $X_{\hat{f}}$ is used for *path optimization* phase. $\zeta_n$ is the volume of the unit ball in the current workspace. In reference to Lemma 56, 71, and 72 in [@karaman2011sampling], the following equation holds: $$\begin{equation}
\mathbb{P} (\limsup_{q \to \infty} \min_{\sigma\in\Sigma_q} \left\{ c(\sigma) \right\} = c^*) = 1.
\end{equation}$$ where $q$ is the number of samples, $\Sigma_q \subset \Sigma$ is the set of valid paths from the start to the goal found by the planner from those samples, $c: \Sigma \rightarrow [0, \infty)$ is the cost function, and $c^*$ is the optimal solution cost. It indicates that the MIT\* can find an optimal path, if it exists, as the number of iterations go to infinity. Therefore, the asymptotic optimality is guaranteed.

# Experimental Results {#sec:Expri}

:::: {#fig: testEnv .figure latex-placement="t!"}
::: caption
The 2D representation of the simulated planning problems in Section [5](#sec:Expri){reference-type="ref" reference="sec:Expri"}. The state space, denoted as $X \subset \mathbb{R}^n$, is constrained within a hypercube with one width for both problem instances. Specifically, we conducted ten distinct instantiations of the random rectangles experiment and the outcomes are showcased in Fig. [5](#fig: result){reference-type="ref" reference="fig: result"}.
:::
::::

:::: {#fig: result .figure latex-placement="t!"}
::: caption
Detailed experimental results from Section [5.1](#subsec:experi){reference-type="ref" reference="subsec:experi"} are summarized. Fig. (a)-(c) show flanking gap outcomes in $\mathbb{R}^4$, $\mathbb{R}^8$, and $\mathbb{R}^{16}$, respectively. Panel (d)-(f) displays ten random rectangle experiments in $\mathbb{R}^4$, $\mathbb{R}^8$ and $\mathbb{R}^{16}$. Fig. (g)-(i) present dividing walls outcomes in $\mathbb{R}^4$, $\mathbb{R}^8$, and $\mathbb{R}^{16}$. Fig. (j)-(l) present non-convex simulation for goal enclosure test outcomes in $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^{8}$. In the cost plots, boxes represent solution cost and time, with lines indicating cost progression for an almost surely optimal planner (unsuccessful runs have infinite cost). Error bars provide nonparametric 99% confidence intervals for solution cost and time.
:::
::::

:::: {#fig: Realresult .figure latex-placement="t!"}
::: caption
Detailed experimental results from Section [5.2](#subsec:realExpri){reference-type="ref" reference="subsec:realExpri"} are summarized above. Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}a illustrates the *beer barrel*, highlighting the start and goal configurations, solution cost, and success rate. Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}b depicts the *industry shelf*, showing the initial and final positions for container extraction and placement. Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}c presents the *kitchen*, focusing on the DARKO robot's performance. In the cost box plots, boxes represent solution costs per planner, while lines show mean cost progression for an optimal planner (with unsuccessful runs assigned an infinite cost).
:::
::::

In this article, we utilize the Planner-Arena benchmark database [@moll2015benchmarking], the Planner Developer Tools (PDT) [@gammell2022planner], and MoveIt [@gorner2019moveit] to benchmark proposed motion planner behaviors. [MIT\* was tested against SOTA algorithms in both simulated random scenarios (Fig. [4](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}, resolution $5 \times 10^{-6}$) and real-world manipulation problems (Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}, resolution $5 \times 10^{-3}$).]{style="color: black"} The comparison involved several versions of RRT-Connect, Informed RRT\*, BIT\*, ABIT\*, AIT\*, and EIT\* sourced from the Open Motion Planning Library (OMPL) [@sucan2012open]. [The construction time costs of the *$\mathcal{C}$-space* (Table [\[tab:benchmark\]](#tab:benchmark){reference-type="ref" reference="tab:benchmark"}) across different dimensions are evaluated using the space information constructor of OMPL. The experimental results demonstrate that the *$\mathcal{C}$-space* construction time remains a minor component of the overall planning process and does not constitute a computational bottleneck.]{style="color: black"} The evaluations are implemented on a computer with an Intel i7 3.90 GHz processor and 32GB of LPDDR3 3200 MHz memory. These comparisons were carried out in simulated environments ranging from $\mathbb{R}^2$ to $\mathbb{R}^{16}$. The primary objective for the planners was to minimize path length (cost). The RGG constant $\eta$ was uniformly set to 1.001, and the rewire factor was set to 1.2 for all planners. [Gaussian standard deviation $\delta$ is default set to 10% of the maximum extent of *$\mathcal{C}$-space*.]{style="color: black"}

For RRT-based algorithms, a 5% goal bias was used, with maximum edge lengths of 0.3, 0.5, 1.25, and 3.0 in $\mathbb{R}^2$, $\mathbb{R}^4$, $\mathbb{R}^8$, $\mathbb{R}^{16}$. All batch-sorted planners sampled 100 states per batch, and informed planners defined the informed set $X_{\hat{f}}$ using the current best costs. MIT\* leveraged prior admissible costs to guide the search using an *estimated informed set* $X_{\Tilde{\sigma}}$ before discovering the initial solution. It then used an adaptive sampler to target critical areas in confined spaces. [The implementation of MIT\* planner into OMPL framework is available at: ]{style="color: black"}[[https://github.com/Liding-Zhang/ompl_release]{style="color: black"}](https://github.com/Liding-Zhang/ompl_release).

## Simulation Experimental Tasks {#subsec:experi}

The planners were tested across four distinct benchmarks in four domains: $\mathbb{R}^2$, $\mathbb{R}^4$, $\mathbb{R}^8$, and $\mathbb{R}^{16}$. [In the first scenario, a constrained flanking gap (FG) environment with a narrow gap was simulated, offering one general direction for optimal path (Fig. [4](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}a).]{style="color: black"} Each planner ran 100 times with varying random seeds, and the computation times for optimal planners are labeled. Figs. [5](#fig: result){reference-type="ref" reference="fig: result"}a, [5](#fig: result){reference-type="ref" reference="fig: result"}b and [5](#fig: result){reference-type="ref" reference="fig: result"}c show that MIT\* quickly finds the initial solution in different dimensions with minimal time.

[In the second scenario, random widths were assigned to *axis-aligned hyperrectangles*, creating non-convex regions within the *$\mathcal{C}$-space* (Fig. [4](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}b). Ten random rectangle (RR) problems were generated for each *$\mathcal{C}$-space* dimension, with 100 trials per planner. Figs. [5](#fig: result){reference-type="ref" reference="fig: result"}d, [5](#fig: result){reference-type="ref" reference="fig: result"}e and [5](#fig: result){reference-type="ref" reference="fig: result"}f show that MIT\* achieved the highest success rates within a limited time]{style="color: black"}.

[The third test simulated a constrained dividing wall (DW) environment with multiple narrow gaps, allowing all planners to search optimal paths in various non-trivial directions (Fig. [4](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}c).]{style="color: black"} Each planner ran 100 times with different random seeds, and maximal computation times for optimal planners are shown in the labels. Figs. [5](#fig: result){reference-type="ref" reference="fig: result"}g, [5](#fig: result){reference-type="ref" reference="fig: result"}h and [5](#fig: result){reference-type="ref" reference="fig: result"}i indicate that MIT\* outperforms the SOTA planner in both finding the initial solution and converging to the optimal solution.

[The last test problem featured a hollow, non-convex C-shaped obstacle surrounding the goal state. In this configuration, even in higher dimensions, the goal could only be accessed through the face of the hyper-obstacle farthest from the start state (Fig. [4](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}d). This setup presents a challenge for sampling-based planners, as many invalid edges near the reverse search tree often require repair. Effective coverage of narrow channels is crucial, and strategies such as biased or adaptive sampling may be necessary to improve efficiency. A direct path planner would result in collisions, resulting in the planner rerouting around obstacles. As shown in Figs. [5](#fig: result){reference-type="ref" reference="fig: result"}j, [5](#fig: result){reference-type="ref" reference="fig: result"}k and [5](#fig: result){reference-type="ref" reference="fig: result"}l, MIT\* outperforms SOTA planners by quickly finding an initial solution and converging to the optimal one.]{style="color: black"}

[]{#tab:benchmark label="tab:benchmark"}

:::: {#fig: dynamicResult .figure latex-placement="t!"}
::: caption
[Detailed planner performance in dynamic experimental scenarios from Section [5.3](#subsec:dynamicExpri){reference-type="ref" reference="subsec:dynamicExpri"} are summarized above. Fig. [7](#fig: dynamicResult){reference-type="ref" reference="fig: dynamicResult"}a and b illustrates the robotic arm's start and goal configurations, along with the motion directions (i.e., horizontal and vertical) of the dynamic obstacles (red arrows). The robotic arm repeatedly travels between the start and goal configurations within the scenes, performing real-time re-planning (MaxTime 0.1s) to evaluate its dynamic obstacle avoidance capabilities (with unsuccessful runs assigned an infinite cost).]{style="color: black"}
:::
::::

[As shown in Table [\[tab:benchmark\]](#tab:benchmark){reference-type="ref" reference="tab:benchmark"}, MIT\* consistently outperforms SOTA in initial median time ($t^\textit{med}_\textit{init}$) across various scenarios. For instance, in the $\textnormal{FG}-\mathbb{R}^{16}$ scenario, MIT\* achieves a $t^\textit{med}_\textit{init}$ of 0.0083s, which is 35.65% faster than EIT\*. Similarly, in the $\textnormal{RR}-\mathbb{R}^{16}$ scenario, MIT\* reduces $t^\textit{med}_\textit{init}$ by 32.04%. In more confined settings, such as $\textnormal{DW}-\mathbb{R}^{16}$ and $\textnormal{GE}-\mathbb{R}^{8}$, the level of improvement is even more substantial, with MIT\* achieving a 41.15% and 86.95% reduction, respectively.]{style="color: black"}

Overall, the table highlights the superior efficiency of MIT\* in reducing initial median times and enhancing the effectiveness of path planning algorithms.

## Real-world Path Planning Tasks {#subsec:realExpri}

[We compare MIT\* with SOTA optimal path planners via the base-manipulator robot (DARKO) to evaluate performance in converging to the optimal solution and success rate over 30 runs (Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}). The *Beer Barrel*-ENV includes simple cup holder obstacles, while the *Shelf*-ENV and *Kitchen*-ENV feature navigating through cluttered, narrow spaces. Each scenario requires finding a collision-free path from start to goal.]{style="color: black"}

### **Beer barrel cup placement task**

Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}a illustrates the start and goal configurations for the cup placement task. In this scenario, a single robotic manipulator is used to grab a beer cup and position it under the beer tap of a keg, all while avoiding obstacles. All planners were given 1.0 seconds to address the beer barrel cup placement problem. Over the course of 30 trials, MIT\* achieved a 93.33% success rate with a median solution cost of 13.2741. EIT\* had a success rate of 76.67% with a median solution cost of 16.8917. AIT\* was 63.33% successful, with a median solution cost of 18.6277.

### **Industry shelf container rearrangement task**

The initial and final configurations for the shelf task are shown in Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}b. The robot grasps an industry-standard (*tolerance* $\leq$ 5mm) container from a lower position and positions it on the upper layer between two larger containers. The challenge lies in precisely inserting the container into narrow spaces, making the planning of a collision-free path particularly difficult. Each planner was allocated 1.5 seconds to solve the constrained lift-up and insertion problem within a limited space. Across 30 trials, MIT\* achieved an 80% success rate with a median solution cost of 9.7145. EIT\* had a 60% success rate with a median solution cost of 11.1054. AIT\* managed a 53.33% success rate with a median solution cost of 12.7851.

### **Kitchen model pan cooking task**

The DARKO robot was positioned in front of a kitchen model for the third task. The start and goal configurations are shown in Fig. [6](#fig: Realresult){reference-type="ref" reference="fig: Realresult"}c. This task is challenging because the manipulator must maneuver the pan within a cluttered oven while avoiding collisions with both the base robot and the kitchen shelves. Each planner was given 5.0 seconds to solve the kitchen pan reallocation problem. Over 30 trials, MIT\* achieved a 36.67% success rate with a median solution cost of 15.9380. EIT\* had a success rate of 26.67% and a median solution cost of 21.2667. AIT\* recorded a 20% success rate with a median solution cost of 23.5611.

In short, compared with the AIT\* and the EIT\*, the MIT\* achieves the best performance in finding the initial solution and converging to the optimal solution.

::: {style="color: black"}
## Dynamic Experimental Re-planning Tasks {#subsec:dynamicExpri}

We evaluate MIT\* with SOTA optimal path planners using the robot arm to benchmark its performance in terms of the optimal solution costs and success rate over 30 runs (Fig. [7](#fig: dynamicResult){reference-type="ref" reference="fig: dynamicResult"}). The *Horizontal-movement*-ENV scenario involves manipulating blocks while avoiding a single dynamic obstacle, whereas the *Vertical-movement*-ENV scenario features navigation through two vertically moving dynamic obstacles traveling in opposite directions. Each scenario requires computing a collision-free path from the start to the goal configuration.

### **Horizontal-movement block task**

Fig. [7](#fig: dynamicResult){reference-type="ref" reference="fig: dynamicResult"}a illustrates the start and goal configurations for the horizontal movable block task. In this scenario, a single robotic manipulator is used to grab a table block and navigate between the start and goal positions five times, all while avoiding obstacles. All planners were allocated 0.1 seconds to solve the problem. Across 30 trials, for forward planning from the start to the goal configuration, AIT\* achieved an average cost of 8.8167 with a 93.33% success rate, while EIT\* achieved 6.7306 with a 90% success rate. Our proposed MIT\* attained an average cost of 5.5329 with a 96.67% success rate, representing a 17.78% cost improvement over the best-performing baseline planner.

### **Two vertical-movement blocks task**

As illustrated in Fig. [7](#fig: dynamicResult){reference-type="ref" reference="fig: dynamicResult"}b, the task starts from the right part of the table and ends at the left. Two dynamic obstacles move repeatedly, one from top to bottom and the other from bottom to top. The robot arm needs to pick up a block from the start and place it at the goal, repeating this process five times. Avoiding collisions with two opposite moving obstacles, constrained narrow space, and limited planning time make the planning problem challenging. Each planner was allocated 0.1 seconds of re-planning time to solve the back-and-forth problem within a limited space. Across 30 trials, AIT\* achieved an 86.67% success rate with a median solution cost of 10.2138, while EIT\* reached a 90% success rate with a median cost of 9.6934. Our proposed MIT\* attained a 93.33% success rate and a median cost of 7.8718, resulting overall in an 18.79% cost improvement.
:::

[In summary, MIT\* quickly re-planning and converges to high-quality paths, it effectively supports robotic task execution in constrained and dynamic environments.]{style="color: black"}

## Discussion

### Comparison with SOTA Planners

To evaluate the performance of MIT\*, we compared it with SOTA planners using success rate and solution cost metrics across three real-world and nine simulation tasks. MIT\* demonstrated superior performance in all scenarios. In real-world tasks, MIT\* achieved notable improvements: in the *Beer Barrel*-ENV, it reduced solution cost by 21.55% and improved success rate by 16.67% over EIT\*. Compared to AIT\*, MIT\* lowered cost by 28.73% and raised success rate by 30%. In the *Shelf*-ENV, MIT\* reduced cost by 12.55% and improved success rate by 20% compared to EIT\*, and reduced cost by 24.02% with a 26.67% higher success rate than AIT\*. In the *Kitchen*-ENV, MIT\* outperformed EIT\* by reducing cost by 25% and increasing success rate by 10%, and compared to AIT\*, MIT\* lowered cost by 32.74% while increasing success rate by 16.67%.

[Through simulations and real-world experiments, MIT\* is shown to explore and converge more efficiently under the guidance of EIS and an adaptive sampler for dynamic settings, enabling the rapid discovery of feasible solutions.]{style="color: black"}

::: {style="color: black"}
### Ablation Study for Contributions {#subsec:ablation}

To evaluate the individual contributions of the proposed planner, we performed an ablation study focusing on the adaptive sampler (MIT\*-AS), estimated informed set (MIT\*-EIS), and length-related sparse collision checking (MIT\*-SC) in two representative scenarios (Fig. [8](#fig: ablaResult){reference-type="ref" reference="fig: ablaResult"}): goal enclosure (GE)-$\mathbb{R}^{2}$ and dividing walls (DW)-$\mathbb{R}^{4}$. In the GE scenario, which lacks narrow passages, the adaptive sampler was less effective as the bridge sampling component was underutilized, resulting in inferior performance compared to MIT\*-EIS, which could initially prune the search space. Sparse collision checking offered limited improvement here, slightly reducing path cost but increasing initial solution time due to additional collision checks. In contrast, in the DW scenario, which features numerous narrow passages, the adaptive sampler demonstrated certain advantages, as both the bridge test and Gaussian sampling were effective, outperforming MIT\*-EIS. Sparse collision checking showed benefits in this scenario by improving reverse search precision and reducing the need for costly restarts. Overall, MIT\*, integrating all contributions, delivered better performance, highlighting the synergistic nature of the proposed methods.
:::

:::: {#fig: ablaResult .figure latex-placement="t!"}
::: caption
Detailed ablation study results from Section [5.4.2](#subsec:ablation){reference-type="ref" reference="subsec:ablation"} are summarized. Cost plots show solution cost and time, with lines for optimal cost progression and error bars for 99% confidence intervals.
:::
::::

### Limitations and Future Work

While MIT\* demonstrates superior performance, it also has some limitations. The proposed EIS may be overly conservative in environments with irregular cost landscapes or poorly aligned heuristics. In such cases, the repeated enlargement of the EIS could introduce computational overhead, potentially negating the method's advantages. Although we utilized a dynamic adjustment mechanism to iteratively refine the EIS, its effectiveness relies on the complexity of the problem and the quality of the initial solution cost. Furthermore, the current objective of our approach is to optimize path costs in Euclidean space. This limits the EIS's applicability to other cost metrics and non-Euclidean spaces, where the EIS may not effectively constrain the search space. Expanding the EIS to include broader optimal objectives (e.g., obstacle clearance, energy efficiency, etc.) and dynamic scenarios (i.e., via local motion planners) is crucial for future works to enhance robustness. [In future work, we will integrate our planner with an RGB-D/LiDAR perception stack that continuously refreshes an occupancy or signed-distance map, enabling closed-loop planning around non-convex and dynamic obstacles.]{style="color: black"}

# Conclusion {#sec:conclu}

In this article, we proposed Multi-Informed Trees (MIT\*), a sampling-based planner that is multi-informed by prior admissible cost (i.e., estimated informed set) and current solution cost (i.e., informed set). The novel estimated informed set can improve early-stage exploration, the adaptive sampling strategy can refine distribution in critical regions, and length-related adaptive sparse collision checks for edges can optimize lazy reverse search. Then, the probabilistic completeness and asymptotic optimality were guaranteed. Through simulation across dimensions and real-world experiments, we demonstrated that our algorithm shows faster initial path convergence and shorter path length over the SOTA algorithms in a robust manner. Moreover, real-world tasks can further demonstrate the effectiveness of our method in practical applications.

::: IEEEbiography
Liding Zhang is currently a Ph.D. candidate at the School of Computation, Information and Technology (CIT) chair of informatics 6, Technical University of Munich, Germany. He received the B.Sc. degree in mechanical engineering from the Rhine-Waal University of Applied Sciences, Germany, in 2020 and the M.Sc. degree in mechanical engineering and automation from the Technical University of Clausthal, Germany, in 2022.\
His current research interests include robotic task and motion planning, multi-robot collaborations.
:::

::: IEEEbiography
Kuanqi Cai is currently a research associate at the Munich Institute of Robotics and Machine Intelligence (MIRMI), Technical University of Munich. He worked as a research assistant at The Chinese University of Hong Kong, Hong Kong, from 2019 to 2020. Following that, he served as a visiting student researcher at the Southern University of Science and Technology. In 2021, he was a Robotics Student Fellow at ETH Zurich. In 2022, he was employed at The Chinese University of Hong Kong (Shenzhen Research Institute). He obtained his B.E. degree from Hainan University in 2018 and his M.E. degree from Harbin Institute of Technology in 2021. His current research interests include motion planning and human-robot interaction.
:::

::: IEEEbiography
Yu Zhang received the M.Eng. degree from the School of Intelligence Science and Technology, University of Science and Technology Beijing, Beijing, China, in 2022. He is currently working toward the Ph.D. degree in computer science as a member of the Informatics 6, Technical University of Munich, Munich, Germany.\
His current research interests include optimization and control in robotics, machine learning, adaptive and learning control.
:::

::: IEEEbiography
Zhenshan Bing (Member, IEEE) received the B.S. degree in mechanical design, manufacturing, and automation and the M.Eng. degree in mechanical engineering from Harbin Institute of Technology, China, in 2013 and 2015, respectively, and the Ph.D. degree in computer science from the Technical University University of Munich, Germany, in 2019.\
From 2019 to 2024, he was a Post-Doctoral Researcher with the Department of Informatics, Technical University of Munich. He is currently an Associate Professor with the School of Intelligence Science and Technology, Nanjing University, Suzhou. His research interests include bio-inspired robotics and embodied intelligence control algorithms.
:::

::: IEEEbiography
Chaoqun Wang (Member, IEEE) received the B.E. degree in automation from Shandong University, Jinan, China, in 2014, and the Ph.D. degree in robot and artificial intelligence from the Department of Electronic Engineering, The Chinese University of Hong Kong, Hong Kong, in 2019. During his Ph.D. study, he spent six months with the University of British Columbia, Vancouver, BC, Canada, as a Visiting Scholar. He was a Postdoctoral Fellow with the Department of Electronic Engineering, The Chinese University of Hong Kong, from 2019 to 2020. He is currently a Professor with the School of Control Science and Engineering, Shandong University. His current research interests include autonomous vehicles, active and autonomous exploration, and path planning.
:::

::: IEEEbiography
Fan Wu (Member, IEEE) received the B.Sc. degree in mathematics from the University of Science and Technology Beijing, Beijing, China, in 2012, and the M.Sc. degree in financial mathematics from King's College London, London, U.K. Since 2016, he has been working toward the Ph.D. degree in robotics from King's College London, U.K. He is currently a postdoctoral researcher with the Munich Institute of Robotics and Machine Intelligence (MIRMI), Technical University of Munich, Germany. His research interests span the topics in compliant robotics, optimal control and reinforcement learning.
:::

::: IEEEbiography
Sami Haddadin (IEEE Fellow) received the Dipl.-Ing. degree in electrical engineering in 2005, the M.Sc. degree in computer science in 2009 from the Technical University of Munich (TUM), Munich, Germany, the Honours degree in technology management in 2007 from Ludwig Maximilian University, Munich, Germany, and TUM, and the Ph.D. degree in safety in robotics from RWTH Aachen University, Aachen, Germany, in 2011. He is currently a Full Professor and the Chair with Robotics and Systems Intelligence, TUM, and the Founding Director of the Munich Institute of Robotics and Machine Intelligence (MIRMI), Munich. Dr. Haddadin was the recipient of numerous awards for his scientific work, including the George Giralt Ph.D. Award (2012), IEEE RAS Early Career Award (2015), the German President's Award for Innovation in Science and Technology (2017), and the Leibniz Prize (2019).
:::

::: IEEEbiography
Alois Knoll (IEEE Fellow) received his diploma (M.Sc.) degree in Electrical/Communications Engineering from the University of Stuttgart, Germany, in 1985 and his Ph.D. (summa cum laude) in Computer Science from Technical University of Berlin, Germany, in 1988. He served on the faculty of the Computer Science department at TU Berlin until 1993. He joined the University of Bielefeld, Germany as a full professor and served as the director of the Technical Informatics research group until 2001. Since 2001, he has been a professor at the Department of Informatics, Technical University of Munich (TUM), Germany . He was also on the board of directors of the Central Institute of Medical Technology at TUM (IMETUM). His research interests include cognitive, medical and sensor-based robotics, multi-agent systems, data fusion, adaptive systems, multimedia information retrieval, model-driven development of embedded systems with applications to automotive software and electric transportation, as well as simulation systems for robotics and traffic.
:::

[^1]: $^{1}$L. Zhang, Y. Zhang, Z. Bing, and A. Knoll are with the Chair of Robotics, Artificial Intelligence and Real-time Systems, TUM School of Computation, Information and Technology (CIT), Technical University of Munich, 85748 Garching bei Munich, Germany. `liding.zhang@tum.de`

[^2]: $^{2}$K. Cai, F. Wu, S. Haddadin is with the Chair of Robotics and Systems Intelligence, Munich Institute of Robotics and Machine Intelligence (MIRMI), Technical University of Munich, 80992 Munich, Germany.

[^3]: $^{3}$Zhenshan Bing is also with the State Key Laboratory for Novel Software Technology and the School of Science and Technology, Nanjing University (Suzhou Campus), China.

[^4]: $^{4}$C. Wang is with the School of Control Science and Engineering, Shandong University, 250100 Shandong, China.\
    *(Corresponding authors: Zhenshan Bing; Kuanqi Cai.)*
