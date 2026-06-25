---
citation_key: Wang2025Where
arxiv_id: 2505.19219
arxiv_url: https://arxiv.org/abs/2505.19219
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:30:09Z
origin: ai+web
reviewed: false
---

maketitle thanks aketitle

# Introduction {#sec:intro}

Multi-Agent Path Finding (MAPF) [@stern2019multi] is a longstanding and foundational problem in robotics and artificial intelligence, focusing on planning collision-free paths for multiple agents moving in a shared environment. Traditionally, MAPF is formulated on an undirected graph ${\cal{G}} = ({\cal{V}}, {\cal{E}})$, in which vertices ${\cal{V}}$ represent possible locations and edges ${\cal{E}}$ denote valid transitions between locations [@surynek2022problem]. A widely adopted discretization strategy places agents on a grid, enabling them to move to adjacent cells at discrete time steps. Nevertheless, continuous formulations of MAPF that allow more flexible trajectories in space and time have also been actively studied [@andreychuk2022multi; @yang2023path]. This broad problem statement has spawned numerous theoretical breakthroughs and a diverse range of algorithms over the decades.

:::: {#fig:mapf_papers .figure latex-placement="htb!"}
![Query="multi-agent pathfinding"](Wang2025Where_figs/mapf_papers_1.png){#fig:mapf_papers_1 width="\\textwidth"}

![Query="MAPF"](Wang2025Where_figs/mapf_papers_2.png){#fig:mapf_papers_2 width="\\textwidth"}

::: caption
The trends of the cumulative numbers of Google Scholar papers that contain the keyphrases "multi-agent pathfinding" and " MAPF" since January 2015, respectively. The statistics are calculated using exact match by queryingthe keyphrases in title or abstract by months. Both queries show a notable growth trend, particularly after 2020, indicating the increasing research interest and expansion.
:::
::::

MAPF sees practical deployment in an extensive set of application domains, as shown in Figure [3](#fig:mapf_papers){reference-type="ref" reference="fig:mapf_papers"}. In warehouse automation, fleets of automated guided vehicles coordinate to transport goods efficiently [@varambally2022mapf; @wang2024mapf]. In traffic management for autonomous driving, vehicles that share urban road networks must navigate safely and cooperatively [@teng2017coordinating; @ren2024multi]. In safety-critical scenarios such as air traffic control or railway scheduling, MAPF techniques contribute to conflict resolution and scheduling [@ho2020decentralized; @shrestha20216g; @li2021scalable; @chen2022multi]. Beyond these areas, MAPF is a key element in optimizing virtual character movements in video games [@rahmani2020multi; @ma2017feasibility], designing efficient airport surface operations [@morris2016planning; @von2024towards], coordinating automatic parking in vehicle infrastructure [@okoso2019multi; @okoso2022high], enabling multi-robot exploration and coordination [@tang2024large; @almadhoun2019survey], and orchestrating swarm drone fleets [@pyke2021dynamic; @tjiharjadi2022systematic]. As physical systems and robotic capabilities continue to advance, including the emergence of embodied intelligence [@paoloposition] and the low-altitude economy [@leet2024safe], the practical deployment of MAPF has grown in both scale and complexity, reinforcing MAPF's role as a crucial foundation for cooperative robotic and autonomous systems.

Despite the extensive research on MAPF, the field faces several challenges that stem from both theoretical and practical considerations. Classical approaches to MAPF, which mainly include search-based and compilation-based methods, have been the backbone of MAPF research for decades. Search-based methods often emphasize the optimality of solutions, employing traditional graph search, heuristics, and tailored techniques to minimize path collision and search overhead. Examples include the widely studied A\*-based and conflict-based search algorithms [@sharon2015conflict; @okumura2022priority]. Compilation-based methods, on the other hand, transform MAPF into other well-understood mathematical formulations (e.g., integer linear programs, satisfiability problems), thereby leveraging mature solvers [@surynek2016efficient; @surynek2022problem]. While such methods can find high-quality or even provably optimal solutions, they frequently struggle with large problem instances or dynamic environments. Real-time constraints, uncertainties in dynamics and perception, and non-stationarity can severely degrade performance when these classical methods are applied directly [@sartoretti2019primal; @alkazzi2024comprehensive].

In recent years, there has been a noticeable growth in learning-based approaches to MAPF---ranging from imitation learning and reinforcement learning (RL) to evolutionary methods and even emerging paradigms involving foundation models [@alkazzi2024comprehensive]. The motivation behind these data-driven approaches is twofold. First, learning-based methods can be more adaptable in complex or partially observable environments, where classical methods may become computationally infeasible or require excessive domain-specific heuristics. Second, they offer the potential to generalize from experience across different instances, reducing the design effort needed when facing new or changing environments. Nevertheless, these learning-based solutions typically scale to fewer agents (e.g., on the order of hundreds) [@li2022multi; @skrynnik2024learn] as compared to some of the most advanced classical methods that can handle thousands [@friedrich2024scalable; @okumura2024engineering]. This gap in scalability, along with various methodological differences, underscores the necessity of a more holistic view that integrates classical and learning insights.

A number of surveys have highlighted either the classical MAPF literature or the recent surge of learning-based approaches [@stern2019multi; @ma2022graph; @surynek2022problem; @alkazzi2024comprehensive; @chung2024learning]. However, the field currently lacks a comprehensive examination that places both paradigms side by side, evaluates their respective advantages and shortcomings, and provides guidance for combining them. In particular, the community could benefit from a detailed analysis of (i) how learning-based solutions can draw inspiration from the theoretical properties and algorithmic designs of classical MAPF and (ii) the ways in which classical methods can leverage learning components for improved scalability and robustness in real-world applications. Such an integrated view can spur new innovations, especially in learning-based MAPF, as it brings into focus opportunities for synergy, such as replacing certain heuristic modules in classical solutions with learned policies, or fusing optimization-based back-ends with representation learning.

:::: {#fig:overview .figure latex-placement="htb!"}
![](Wang2025Where_figs/overview_new.png){width="\\linewidth"}

::: caption
Structure diagram of the paper (Section 2 - Section 9).
:::
::::

Furthermore, empirical evaluations of MAPF solutions differ widely across publications, making it difficult to assess their performance in a uniform manner. While many studies employ grid-based maps with static obstacles, others look at continuous or dynamic environments, using different metrics such as makespan, sum of costs, or success rate. Additional variability arises from the choice of baseline algorithms, map size, and the number of agents. This survey aims to address these inconsistencies by providing a systematic analysis of experimental settings and evaluation metrics employed by both classical and learning-based MAPF methods. Such a comparative study can foster best practices in benchmarking and draw attention to critical gaps in real-world deployability.

In this survey, we make several key contributions:

- We offer a unified viewpoint for understanding MAPF and its wide-ranging variants, clarifying how different methods formalize and solve the same underlying challenge.

- We provide a comprehensive review of both classical approaches---including search-based and compilation-based methods and learning-based approaches, highlighting recent developments in RL, imitation learning, evolutionary algorithms, and emerging large language model techniques.

- We present an in-depth comparison between classical and learning-based MAPF, focusing on scalability, robustness, constraints, and adaptability to dynamic environments.

- We conduct a detailed analysis of experimental design across existing MAPF literature, examining map types, map sizes, number of agents, evaluation criteria, and choice of baselines, thus providing insights into generalizability and real-world applicability.

- We outline promising directions for future research, including potential for foundation models in MAPF, dynamic environment handling, hybrid classical-learning approaches, and more practical deployments beyond controlled laboratory settings.

The remainder of this survey is organized as follows, as shown in Figure [4](#fig:overview){reference-type="ref" reference="fig:overview"}. In Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}, we introduce the classical definition of MAPF and discuss various formulations, noting that a single mathematical model cannot capture the breadth of MAPF approaches. We subsequently explore in Section [3](#sec:search){reference-type="ref" reference="sec:search"} and Section [4](#sec:compilation){reference-type="ref" reference="sec:compilation"} the main categories of classical methods: search-based and compilation-based solutions. Then, in Section [5](#sec:augmenting){reference-type="ref" reference="sec:augmenting"}, [6](#sec:rl){reference-type="ref" reference="sec:rl"} and [7](#sec:others){reference-type="ref" reference="sec:others"}, we shift our focus to learning-based MAPF methods, beginning with hybrid frameworks that incorporate learned modules into otherwise classical pipelines, followed by fully data-driven RL solutions and, finally, other learning paradigms such as imitation learning, evolutionary algorithms, and emerging approaches using large language models. In Section [8](#sec:exp){reference-type="ref" reference="sec:exp"}, we provide a comparative analysis of experimental setups employed in the literature, highlighting how variations in map settings, agent populations, performance metrics, and baseline choices can influence reported outcomes. We conclude in Section [9](#sec:future){reference-type="ref" reference="sec:future"} by identifying future directions for MAPF research, such as laying the groundwork for foundation models, extending MAPF to dynamic or partially observable domains, and demonstrating early experimental results that validate these directions.

By synthesizing these diverse perspectives, we aim for this survey to serve as a comprehensive guide to both classical and learning-based MAPF. We believe that bridging these two domains ultimately benefits the broader research and industrial communities, accelerating progress toward scalable, robust, and intelligent solutions in multi-agent coordination.

# Problem Formulation {#sec:formulation}

As discussed in Section [1](#sec:intro){reference-type="ref" reference="sec:intro"}, Multi-Agent Path Finding (MAPF) broadly involves finding collision-free paths for a set of $n$ agents operating within a shared environment. The definitions in this section revolve around the mainstream MAPF formulations and several influential variants, which constitute the bulk of research addressed in this survey. Notably, many additional and more specialized MAPF variants also exist in the literature (see, e.g., [@stern2019multi] for a comprehensive overview). In the classic formulation, as shown in Figure [7](#fig:mapf){reference-type="ref" reference="fig:mapf"}, the environment is represented as an undirected graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where $\mathcal{V}$ is the set of vertices (possible locations), and $\mathcal{E}$ is the set of edges indicating valid deterministic transitions between locations [@stern2019multi; @surynek2022problem]. Each agent $i \in \{1, \dots, n\}$ is assigned a start vertex $s_i \in \mathcal{V}$ and, in many scenarios, a goal vertex $g_i \in \mathcal{V}$. Over discrete (or continuous) time steps, each agent must traverse the graph from $s_i$ to $g_i$ without colliding with other agents. A *collision* occurs if two agents occupy the same vertex at the same time or if they traverse the same edge in opposite directions at the same time. The objective is to devise a set of paths that respect these collision-free constraints while optimizing one or more cost functions defined below.

:::: {#fig:mapf .figure latex-placement="htb!"}
![](Wang2025Where_figs/mapf_a.png){#fig:mapf_1 width="\\textwidth"}

![](Wang2025Where_figs/mapf_b.png){#fig:mapf_2 width="\\textwidth"}

::: caption
Illustration of (a): a MAPF instance and (b): different types of conficts. (a): the individual paths of two agents, $a_1$ and $a_2$, along with a solution whose sum of costs (SoC) is 8. (b): (1) a vertex confict, (2) a swapping confict, and (3) a cycle confict.
:::
::::

## One-Shot and Lifelong MAPF

#### One-Shot MAPF

In a *one-shot* MAPF problem, each agent has a fixed start position $s_i$ and a fixed goal position $g_i$. Once an agent reaches its goal, it has effectively completed its mission. Two primary optimization objectives typically arise in one-shot MAPF:

1.  **Makespan Minimization.** The makespan objective minimizes the maximum arrival time among all agents. Formally, given a path $\pi_i$ for each agent $i$ and a cost function $\mathrm{Cost}(\pi_i)$ measuring the length (or time) of the path,[^3] the makespan is $$\begin{equation}
    \label{eq:makespan}
            \text{Makespan}(\{\pi_i\}_{i=1}^n) \;=\; \max_{1 \leq i \leq n} \mathrm{Cost}(\pi_i).
    \end{equation}$$ Minimizing [\[eq:makespan\]](#eq:makespan){reference-type="eqref" reference="eq:makespan"} focuses on reducing the worst-case completion time across all agents.

2.  **Sum-of-Costs (SoC).** The SoC objective aims to minimize the total cost incurred by all agents. If $\mathrm{Cost}(\pi_i)$ denotes the cost of agent $i$'s path, then $$\begin{equation}
    \label{eq:soc}
            \text{SoC}(\{\pi_i\}_{i=1}^n) \;=\; \sum_{i=1}^{n} \mathrm{Cost}(\pi_i).
    \end{equation}$$ Equivalently, one may view this as minimizing the average cost per agent. Methods optimized for SoC often strive to balance overall efficiency [@surynek2022problem].

#### Lifelong MAPF

In contrast, *lifelong* MAPF involves a sequence of tasks or an ongoing flow of tasks where agents must complete multiple goals over an extended horizon [@stern2019multi; @tang2024large]. Rather than halting once a single goal is reached, each agent is either reassigned to new tasks or continues patrolling the environment. In this setting, optimization objectives typically concern maximizing the number of completed tasks in a limited time, minimizing idle time between tasks, or balancing similar operational metrics: $$\begin{equation}
\label{eq:lifelong}
    \max_{\{\pi_i\}_{i=1}^n} \; \text{TasksCompleted}(\{\pi_i\}_{i=1}^n),
\end{equation}$$ where $\text{TasksCompleted}(\{\pi_i\}_{i=1}^n)$ indicates the cumulative total of tasks or subtasks that are successfully finished within a particular time horizon.

#### Remark 1

In one-shot MAPF problems, beyond the most common optimization objectives of makespan and sum-of-costs, there exist other task-driven optimization goals. These include minimizing the total non-waiting steps required to complete all objectives, the total number of steps before all agents settle in their target positions, and various other metrics. For a more comprehensive overview of these alternative objective functions, readers can refer to @stern2019multi.

#### Remark 2

Beyond the two most prevalent problem settings, one-shot MAPF and lifelong MAPF, numerous problem variants exist in the literature. These include anonymous MAPF (where goal locations are interchangeable among agents), colored MAPF (where agents of the same color can be assigned to any goal of the matching color), and other specializations. For a more detailed discussion of these variants, we direct readers to @stern2019multi.

#### Remark 3

The MAPF problem formulation presented in this paper implicitly assumes discrete time steps, uniform action durations (each action consumes exactly one time step), and that each agent occupies exactly one grid cell. In practical applications, these constraints are frequently relaxed. Examples include scenarios where different states and actions may consume varying amounts of time, grid cells may probabilistically contain multiple agents, and continuous-time extensions corresponding to motion planning problems. For a more thorough exploration of these generalizations, we refer readers to @stern2019multi.

## Centralized vs. Decentralized Control

#### Centralized MAPF

In a *centralized* approach, a single planning entity has access to the global state of the environment, including the positions and goals of all agents. The central planner generates collision-free paths for every agent using either search-based methods [@sharon2015conflict; @okumura2022priority] or compilation-based frameworks [@surynek2016efficient; @surynek2022problem], often yielding high-quality or even provably optimal solutions. However, centralized techniques can suffer from high computational overhead in large-scale or dynamically changing environments.

#### Decentralized MAPF

Under *decentralized* control, individual agents (or subsets of agents) plan their paths locally, possibly with partial observability or constrained communication among agents [@paoloposition; @tjiharjadi2022systematic]. Decentralized frameworks must address the challenge of coordinating agents with limited global knowledge, frequently relying on consensus strategies or local collision avoidance rules. Formally, each agent $i$ has local information $\Omega_i$, representing its (potentially partial) view of the environment. The agent's decision rule $\delta_i$ selects an action $a_i$ at each time step based on $\Omega_i$, that is, $$\begin{equation}
    a_i(t) \;=\; \delta_i\bigl(\Omega_i(t)\bigr).
\end{equation}$$ These decentralized settings better reflect realistic constraints with limited sensing or communication but may require sophisticated algorithms to handle global conflict resolution.

## Categories of MAPF Approaches

Drawing from our discussion in Section [1](#sec:intro){reference-type="ref" reference="sec:intro"}, solutions to MAPF can be broadly categorized as:

**Search-Based Methods:** Classical graph search and tree-based algorithms that explicitly enumerate or prune the space of collision-free paths. They often guarantee completeness or optimality under certain assumptions but may struggle with large-scale instances.

**Compilation-Based Methods:** Formulate MAPF as an Integer Linear Program (ILP), a Satisfiability (SAT) problem, or other well-studied optimization frameworks [@surynek2016efficient]. These methods exploit powerful generic solvers but may also face scalability issues or long solve times.

**Learning-Based Methods:** Leverage diverse machine learning paradigms, such as RL, imitation learning, and evolutionary algorithms [@alkazzi2024comprehensive; @skrynnik2024learn]. While these can more readily adapt to uncertain or partially observable environments, they frequently handle fewer agents compared to large-scale classical approaches [@friedrich2024scalable].

**Hybrid Methods:** Integrate learning components (e.g., learned heuristics or policies) into a classical MAPF pipeline to balance performance gains from learning with analytical guarantees from traditional solvers.

The chronological timeline of representative classical and learning-based algorithms are shown in Figure [8](#fig:classic_trend){reference-type="ref" reference="fig:classic_trend"} and [16](#fig:learning_trend){reference-type="ref" reference="fig:learning_trend"}.

:::: {#fig:classic_trend .figure latex-placement="htb!"}
![](Wang2025Where_figs/classic_trend.png){width="\\linewidth"}

::: caption
A chronological timeline of classical algorithms developed between 2012 and 2024, organized by core solving paradigms: CBS and its variants; SAT-based methods; SMT-based frameworks; and various other approaches.
:::
::::

# Search-Based Methodology {#sec:search}

The growing breadth of MAPF research and its expanding real-world applications underscore the enduring importance of search-based strategies, even as learning-driven approaches gain momentum. Despite the recent successes of reinforcement learning and other data-centric methods in tackling this coordination challenge, search-based algorithms maintain a unique niche thanks to their algorithmic transparency, theoretical rigor, and strong performance in a wide range of problem instances. In particular, these algorithms excel at systematically uncovering collision-free solution paths in high-dimensional, combinatorial search spaces---a common scenario in large-scale MAPF setups. The following sections delve into the most influential and widely studied search-based methodologies, starting with the foundational Conflict-Based Search (CBS) and its extensive enhancements (both optimal and suboptimal), then moving to Priority-Based Search (PBS) as a complementary framework. We also explore Large Neighborhood Search (LNS) approaches, which have gained traction in suboptimal, time-sensitive, or resource-constrained MAPF settings. By examining the theoretical underpinnings and implementation details of these methods, we aim to highlight both their individual merits and the broader methodological interplay that fuels the advancement of MAPF solutions.

## Vanilla Conflict-Based Search (CBS) {#sec:cbs}

Prior to the advent of *Conflict-Based Search* (CBS) [@sharon2015conflict], a variety of search-based algorithms were employed to tackle the MAPF problem. These methods not only addressed the problem effectively but also provided significant inspiration for CBS and its variants, including A\*, *Windowed Hierarchical Cooperative A\** (WHCA\*) [@silver2005cooperative], *Enhanced Partial Expansion A\** (EPEA\*) [@felner2012partial], M\* [@wagner2011m], *Operator Decomposition* (OD) [@standley2010finding], ODrM\* [@ferner2013odrm] and *Increasing Cost Tree Search* (ICTS) [@sharon2011pruning].

:::: {#fig:cbs .figure latex-placement="htb!"}
![](Wang2025Where_figs/cbs.png){width="\\linewidth"}

::: caption
Illustration of the CBS process on a simple two-agent instance. Left: Two related source (solid circle) and target (hollow circle) configurations overlaid on a 5$\times$`<!-- -->`{=html}5 grid with obstacles (blue squares) and two agents (green and orange circles). The underlying graph labels traversable grids A--L. Right: The CT built from the root (Con = $\{ \}$, SoC = 8), where each node box reports: Con: the set of agent--location--time constraints (e.g. $\{$[]{style="color: ACD78E"}, H, 2$\}$ forbids the green agent from H at timestep 2), SoC: the current sum-of-costs of the two individual shortest-path solutions, Sol: the ordered vertex sequences for the green and orange agents (shown in matching colors). At the root, the joint plan has a collision at (H,2) which represents the point in space-time, so CBS branches into two children that respectively prohibit either agent at that conflict. Subsequent collisions at (I,3) and (E,2) likewise generate further binary splits. Leaf nodes (shaded in light green) represent conflict-free plans whose SoC = 9, which is the optimal cost-minimal, collision-free solution found by CBS.
:::
::::

In this section, we introduce CBS, one of the most influential search-based methods for the MAPF problem. We first present a mathematical formulation of the MAPF problem tailored to CBS and its variants, followed by an overview of the CBS algorithmic framework and a pseudocode description of the basic CBS procedure. The illustration of the CBS process on a simple two-agent instance is shown in Figure [9](#fig:cbs){reference-type="ref" reference="fig:cbs"}.

### Mathematical Modeling for CBS and Its Variants

Consistent with the notations in Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}, consider an undirected graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, a set of $n$ agents $\{1,\dots,n\}$, and a discrete time horizon $T$. For each agent $i$, we denote by $s_i \in \mathcal{V}$ its start vertex and by $g_i \in \mathcal{V}$ its goal vertex. A path (or trajectory) for agent $i$ over the time horizon $T$ is a sequence of vertices $$\pi_i \;=\; \bigl(v_{i}(0),\,v_{i}(1),\dots,v_{i}(T)\bigr), \quad v_i(t)\in \mathcal{V},$$ such that $v_i(0)= s_i$ and $v_i(T)= g_i$. (If the agent is assumed to stop once reaching $g_i$, we may hold $v_i(t) = g_i$ for all remaining $t$.)

**Decision Variables.** From a constraint-based perspective, one introduces the binary variables $$x_{i,v,t} \;=\; \begin{cases}
   1, & \text{if agent $i$ is at vertex $v$ at time $t$,}\\
   0, & \text{otherwise}.
   \end{cases}$$ Hence, $\pi_i$ is represented by setting $x_{i,v,t}=1$ exactly for $v = v_i(t)$ along agent $i$'s path.

**Constraints.** The MAPF problem is characterized by twin collision-avoidance constraints: $$\label{eq:cbs:constraints}
\begin{align}
   &x_{i,v,t} + x_{j,v,t} \;\le\; 1, \ \ \forall \, t, \,\forall \, v\in \mathcal{V}, \,\forall\, i < j,\ \ \text{(vertex collision avoidance)} \label{eq:collision-vertex}\\[4pt]
   &x_{i,u,t} \,+\, x_{i,v,t+1} \;+\; x_{j,v,t} \,+\, x_{j,u,t+1} \;\le\; 3, \ \ \forall \, (u,v)\in \mathcal{E},\forall \, t, \,\forall\, i < j, \ \ \text{(edge collision avoidance)}\label{eq:collision-edge}
\end{align}$$ where [\[eq:collision-vertex\]](#eq:collision-vertex){reference-type="eqref" reference="eq:collision-vertex"} prevents multiple agents from occupying the same vertex at the same time, while [\[eq:collision-edge\]](#eq:collision-edge){reference-type="eqref" reference="eq:collision-edge"} ensures that no two agents traverse the same edge in opposite directions at the same time.[^4] Additional constraints ensure that each agent maintains a consistent path from $s_i$ to $g_i$, typically: $$\sum_{v\in \mathcal{V}} x_{i,v,t} \;=\; 1, \qquad\forall i,\;\forall 0\le t \le T,$$ and $x_{i,v_i(0),0} = 1$, $x_{i,v_i(T),T} = 1$.

**Objective.** CBS can be used to minimize different objectives. Common choices include:

- **Makespan**: $\displaystyle \min \max_{1 \leq i \leq n} \mathrm{Cost}(\pi_i)$, where $\mathrm{Cost}(\pi_i)$ typically represents the time at which agent $i$ reaches $g_i$.

- **Sum of Costs (SoC)**: $\displaystyle \min \sum_{i=1}^n \mathrm{Cost}(\pi_i)$.

The classical CBS framework is often presented for the SoC objective but can be adapted to the makespan objective.

### Algorithmic Framework and High-Level--Low-Level Search {#sec:cbs:framework}

To solve the above MAPF formulation, CBS employs a two-level search:

- *High-Level Search.* Maintains a *conflict tree* (CT), where each node contains (i) a set of constraints (i.e., forbidden vertex/time or edge/time tuples) for each agent and (ii) a set of complete paths, one per agent, that obey these constraints. Upon finding a conflict between any two paths, the high-level search *branches* into two new CT nodes, each adding a constraint to exactly one agent's path.

- *Low-Level Search.* Given the constraints for a single agent, the low-level search finds an optimal path for that agent respecting those constraints. Typically, one uses standard single-agent pathfinding algorithms (e.g., A\* or Dijkstra) in a time-expanded graph to compute the new path.

The high-level search terminates when it reaches a node in the CT whose paths are all conflict-free. The set of paths at that node is an optimal joint solution under the given objective (makespan or SoC), provided the branching and low-level searches use consistent admissible heuristics or cost functions.

To make the two-level CBS search scheme more concrete, we illustrate a small example on a $2\times 3$ grid (see Figure [10](#fig:cbs-example-grid){reference-type="ref" reference="fig:cbs-example-grid"}). The grid is indexed by $(r,c)$ with $r\in\{0,1\}$ for rows and $c\in\{0,1,2\}$ for columns. We consider two agents:

- Agent 1 starts at $s_1 = (0,0)$ and has goal $g_1 = (1,2)$.

- Agent 2 starts at $s_2 = (1,0)$ and has goal $g_2 = (0,2)$.

At each time step, the agents can either move to an adjacent cell (up, down, left, or right if valid) or remain in place if desired (cf. Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}). For simplicity of exposition, we assume both agents seek to minimize their individual path lengths (Sum of Costs).

:::: {#fig:cbs-example-grid .figure latex-placement="ht"}
  ------------------ ------------------ ------------------
   $\mathbf{(0,0)}$   $\mathbf{(0,1)}$   $\mathbf{(0,2)}$
   $\mathbf{(1,0)}$   $\mathbf{(1,1)}$   $\mathbf{(1,2)}$
  ------------------ ------------------ ------------------

::: caption
A $2\times 3$ grid environment for the CBS example. Agent 1 aims to move from $(0,0)$ to $(1,2)$; Agent 2 aims to move from $(1,0)$ to $(0,2)$.
:::
::::

We now provide a step-by-step example of how CBS resolves conflicts and arrives at a collision-free solution, using the small $2\times3$ grid from Figure [10](#fig:cbs-example-grid){reference-type="ref" reference="fig:cbs-example-grid"}. We assume both agents can move one cell per discrete time step (up, down, left, or right) or remain idle. The objective is the Sum of Costs (SoC), where each agent's cost is the earliest time step at which it reaches its goal.

1.  **Root Node (No Constraints).**

    1.  Each agent first plans a shortest path *independently*, ignoring collisions. $$\pi_1^0: (0,0)\ \to\ (0,1)\ \to\ (0,2)\ \to\ (1,2),$$ $$\pi_2^0: (1,0)\ \to\ (1,1)\ \to\ (1,2)\ \to\ (0,2).$$

    2.  The root node $N_0$ of the Conflict Tree (CT) stores:

        - *Constraint Sets:* All empty.

        - *Paths:* $\pi_1^0,\,\pi_2^0$.

        - *Cost*: $\mathrm{SoC} = \mathrm{Cost}(\pi_1^0)+\mathrm{Cost}(\pi_2^0)$. (Each path has length $3$ in this example, so $\mathrm{SoC}=6$.)

    3.  We place $N_0$ into the Open List, which is typically a priority queue ordered by SoC (or by makespan, if optimizing that objective).

2.  **Detecting a Conflict.**

    1.  We pop $N_0$ from the Open List and check the paths $\pi_1^0,\,\pi_2^0$ for collisions:

        - At $t=0$: Agent 1 is at $(0,0)$ and Agent 2 is at $(1,0)$. No conflict.

        - At $t=1$: Agent 1 is at $(0,1)$ and Agent 2 is at $(1,1)$. No conflict.

        - At $t=2$: Agent 1 is at $(0,2)$ and Agent 2 is at $(1,2)$. They occupy different cells, hence no vertex conflict yet. However, suppose we look ahead to $t=3$: Agent 1 would move to $(1,2)$, and Agent 2 would move to $(0,2)$. They attempt to *swap* positions via the edge $(0,2)\leftrightarrow(1,2)$ simultaneously. This is a classic *edge conflict* in MAPF, as they traverse the same edge in opposite directions at the same time.[^5]

    2.  Because we have found a conflict between Agents 1 and 2 at (or around) time $t=3$, we must *branch* in the Conflict Tree.

3.  **Branching into Two Child Nodes.**

    1.  At node $N_0$, we have one conflict: $\mathrm{Conflict}(1,2,t=3)$. The algorithm creates two child nodes $N_A$ and $N_B$: $$N_A:\ \text{Add constraint forbidding Agent~1’s conflicting move, replan for Agent~1 only};$$ $$N_B:\ \text{Add constraint forbidding Agent~2’s conflicting move, replan for Agent~2 only}.$$

    2.  *Constraint Sets in Each Child Node.*

        - In $N_A$, Agent 1 receives an additional constraint: $$\text{``Agent~1 may not occupy (or use edge to) }(1,2)\text{ at }t=3\text{.''}$$

        - In $N_B$, Agent 2 receives a similar constraint forbidding the move to $(0,2)$ at $t=3$.

4.  **Low-Level Replanning for a Single Agent.**

    #### Child Node $N_A$.

    1.  Agent 2's path $\pi_2^0$ remains unchanged.

    2.  Agent 1 runs a low-level path search (e.g., A\*) with the new constraint: $$\text{Cannot use edge or cell }(0,2)\leftrightarrow(1,2)\text{ at }t=3.$$

    3.  A feasible updated path might be: $$\pi_1^A:\quad
               (0,0)\xrightarrow{t=0\to1}
               (0,1)\xrightarrow{t=1\to2}
               (1,1)\xrightarrow{t=2\to3}
               (1,2).$$

    4.  In time-expanded terms:

        - $t=0$: Agent 1 at (0,0).

        - $t=1$: Move to (0,1).

        - $t=2$: Move to (1,1).

        - $t=3$: Move to (1,2) (Goal).

    5.  Check if $\pi_2^0$ and $\pi_1^A$ conflict: $$\pi_2^0: \ (1,0)\,\to\,(1,1)\,\to\,(1,2)\,\to\,(0,2).$$

        - $t=1$: Agent 1 at (0,1), Agent 2 at (1,1) (no conflict).

        - $t=2$: Agent 1 at (1,1), Agent 2 at (1,2). Different cells, no conflict.

        - $t=3$: Agent 1 at (1,2), Agent 2 at (0,2). Different cells, no conflict.

    6.  No further conflict is found. Thus $N_A$ is conflict-free.

    7.  The new SoC for $N_A$ is $\mathrm{Cost}(\pi_1^A)+\mathrm{Cost}(\pi_2^0) = 3 + 3 = 6$.[^6]

    #### Child Node $N_B$.

    1.  Agent 1's path remains $\pi_1^0$.

    2.  Agent 2 runs a low-level search forbidding $(0,2)$ at $t=3$.

    3.  A possible updated path for Agent 2 might be: $$\pi_2^B:\quad
              (1,0)\,\to\,(1,1)\,\to\,(0,1)\,\to\,(0,2).$$ Technically, Agent 2 detours or adjusts its timing to avoid reaching $(0,2)$ at $t=3$. It might arrive at $(0,2)$ at $t=4$ or pass through $(0,1)$ if timing constraints so require.

    4.  If $\pi_2^B$ and $\pi_1^0$ remain in conflict, CBS would branch again. But suppose $\pi_2^B$ yields no further collision. Then $N_B$ is also conflict-free, providing a second valid solution.

5.  **Selecting the Final Solution.**

    1.  In practice, as soon as CBS finds *any* conflict-free node in the CT, it *terminates* with that solution if the algorithm is searching in best-first order (optimal search).

    2.  In our example, both $N_A$ and $N_B$ are feasible child nodes with no further conflicts. They each yield a total SoC of 6.

    3.  CBS can return either solution:

        - **Solution 1 (from $N_A$):**\
          Agent 1's path: $$(0,0)\,\to\,(0,1)\,\to\,(1,1)\,\to\,(1,2),$$ Agent 2's path: $$(1,0)\,\to\,(1,1)\,\to\,(1,2)\,\to\,(0,2).$$

        - **Solution 2 (from $N_B$):**\
          Agent 1's path: $$(0,0)\,\to\,(0,1)\,\to\,(0,2)\,\to\,(1,2),$$ Agent 2's path: $$(1,0)\,\to\,(1,1)\,\to\,(0,1)\,\to\,(0,2).$$

    4.  Both solutions are valid and yield the same cost under typical shortest-path metrics.

**Key Takeaways.** *(i)* CBS only constrains *one* agent per conflict, creating minimal constraint sets. *(ii)* Each child node replans for a single agent at the low level, keeping other agents' paths fixed. *(iii)* The search terminates upon encountering the first conflict-free node in best-first order, guaranteeing an optimal solution for the chosen cost metric (SoC or makespan). *(iv)* In the example, once a child node's constraints eliminate conflicts, no further branching is needed. Real-world cases with more agents may generate deeper conflict trees and more branching nodes, but the same principle applies: each conflict is incrementally resolved by splitting into two child nodes, each adding a constraint to exactly one agent.

### Pseudocode for Basic CBS {#sec:cbs:algorithm}

Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"} shows a simplified pseudocode for the basic CBS procedure. Subsequent CBS variants (e.g., *Enhanced CBS*, *Meta-agent CBS*, *ICBS* [@felner2018adding]) enrich or modify this basic structure by altering the conflict prioritization strategy, introducing more advanced heuristics, or refining how constraints are defined and propagated. Nevertheless, the core two-level architecture remains the same: a high-level conflict resolution guided by branching constraints and a low-level single-agent path search.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, agents $\{1,\dots,n\}$, start vertices $\{s_i\}$, goal vertices $\{g_i\}$, objective (*SoC* or *Makespan*). Initialize the root node $N_0$ of the conflict tree (CT):

- For each agent $i$, compute an individual path $\pi_i$ from $s_i$ to $g_i$ ignoring collisions (e.g., by A\*).

- Set the *constraint set* for each agent to be empty.

Insert $N_0$ into a *priority queue* or *open list* (e.g., sorted by $\sum_i \mathrm{Cost}(\pi_i)$). $N \gets \text{pop front of open list}$ Check for conflicts among the paths $\{\pi_i\}$ stored in $N$. **return** $\{\pi_i\}$ as the optimal solution. Let $(i,j,t)$ be the first conflict detected at time $t$ between agents $i$ and $j$. $\!\!\!\!\!\!$ Create a new node $N'$ by copying $N$. Add a new constraint to agent $a$'s constraint set to *forbid* the conflicting vertex or edge at time $t$. Recompute an optimal path $\pi_a$ for agent $a$ under the updated constraint set in $N'$ (low-level A\*). Insert $N'$ into the open list, with updated total cost. **return** *No feasible solution*
:::
::::

**Algorithm Explanation.**

- *Initialization (Lines 1--2).* The root node *ignores* collisions at first. Each agent finds a shortest path $\pi_i$ from $s_i$ to $g_i$, and all constraint sets are empty. The initial cost of the root node is computed (sum of costs or makespan) over $\{\pi_i\}$.

- *Conflict Checking (Lines 4--5).* At each CT node, CBS searches for collisions among the paths. If no collision is found, a globally valid solution is reached.

- *Branching (Lines 8--18).* If a collision is detected at time $t$ between agents $i$ and $j$, the algorithm creates two new child nodes. Each child node introduces a new constraint *for only one* of the two agents, disallowing the conflict at time $t$. After adding the constraint, the algorithm re-plans *only* for that agent. If a feasible path is found, the child node is appended to the priority queue; otherwise, it is discarded.

By resolving conflicts incrementally rather than imposing all constraints upfront, CBS often explores fewer joint states than a naive multi-agent search would. The method is complete for grid-based or graph-based MAPF and, under suitable cost functions (e.g., path length), is also optimal. Subsequent sections will discuss how suboptimal or bounded-suboptimal variants of CBS trade off optimality guarantees for computational efficiency, often by imposing additional heuristics on conflict detection or node expansion order. Thus, CBS forms a core building block for the broader class of search-based MAPF algorithms, serving as a reference point for numerous enhancements and hybridizations.

Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"} provides the high-level pseudocode for the canonical CBS procedure. We augment it below with a step-by-step illustration of how conflicts are resolved in the example from Section [3.1.2](#sec:cbs:framework){reference-type="ref" reference="sec:cbs:framework"}.

**Example (continued).** In the $2\times3$ grid scenario (Figure [10](#fig:cbs-example-grid){reference-type="ref" reference="fig:cbs-example-grid"}):

- *Initialization (Lines 1--2):* - CBS first obtains two unconstrained shortest paths for Agent 1 and Agent 2. - These paths conflict at time $t=3$ in the example scenario (both trying to reach $(0,2)$ or crossing $(0,2)\leftrightarrow(1,2)$).

- *Branching (Lines 8--19):* - Suppose CBS labels the conflict as $(1,2,t=3)$ (i.e., Agents 1 and 2 are in conflict at time 3). - Child node 1 adds a constraint to Agent 1, forbidding it from occupying the conflicting vertex at time 3. Agent 1 replans a new path, e.g., by detouring via $(1,1)$. - Child node 2 adds a constraint to Agent 2 instead, causing Agent 2 to find a different route or timing that avoids the collision.

- The conflict tree grows with each detected conflict, introducing constraints and verifying whether each replan is feasible.

- When CBS encounters a node in which *no* conflict is detected, it terminates and returns the corresponding paths as an optimal joint solution.

This interplay of *high-level conflict resolution* and *low-level single-agent replanning* underlies all CBS-based methods. The branching ensures that only one agent at a time receives an additional constraint, preserving the minimal set of constraints necessary to eliminate each conflict. As a result, the algorithm often converges faster than joint multi-agent A\* in practice, while still guaranteeing completeness and optimality under the chosen objective.

## Enhancements for Optimal CBS {#sec:cbs:optimal}

Building upon the baseline CBS algorithm described in Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}, numerous enhancements have been proposed to achieve optimal (or bounded-optimal) solutions more efficiently [@sharon2015conflict; @boyarski2015icbs; @felner2018adding; @li2019improved; @li2019symmetry; @li2020new; @li2021pairwise; @zhang2022multi]. These enhancements mainly address two interwoven aspects of the CBS framework:

1.  *The high-level (HL) search*: introducing admissible heuristics, advanced conflict prioritization, and refined conflict splitting rules.

2.  *The low-level (LL) search*: augmenting single-agent pathfinding with techniques such as multi-valued decision diagrams (MDDs) and mutex propagation to prune infeasible or redundant paths quickly. An evolutionary graph of the research work conducted on CBS is shown in Figure [11](#fig:cbs_variants){reference-type="ref" reference="fig:cbs_variants"}.

:::: {#fig:cbs_variants .figure latex-placement="htb!"}
![](Wang2025Where_figs/cbs_variants.png){width="\\linewidth"}

::: caption
An evolutionary graph of the research work conducted on CBS. Starting from the vanilla CBS framework at the top, the diagram shows main development axes: optimal CBS variants (all nodes and branches outside the orange-dashed region); sub-optimal CBS variants (orange-dashed region); multi-objective CBS variants (blue-dashed region) and CBS variants in continuous space (black-dashed region).
:::
::::

#### Multi-Valued Decision Diagrams (MDDs.)

A multi-valued decision diagram, $\mathcal{MDD}_i^{\ell}$, for agent $i$, is a directed acyclic graph with $\ell+1$ levels, enumerating *all* feasible single-agent paths of length $\ell$ that satisfy the agent-specific constraints in the current CT node. Each node in $\mathcal{MDD}_i^{\ell}$ represents a vertex (location) and time-step pair $(v,t)$, and each edge encodes a valid transition (or wait action). MDDs are central to identifying whether two agents are *dependent*---if their joint MDD is empty, then they cannot be simultaneously conflict-free without additional constraints (see §[3.2.1](#sec:cbs:hl-heuristics){reference-type="ref" reference="sec:cbs:hl-heuristics"}).

Collectively, these refinements have drastically improved CBS performance, sometimes reducing the number of conflict-tree (CT) node expansions by several orders of magnitude and rendering formerly intractable MAPF instances solvable in practice.

In this subsection, we highlight four core enhancement modules for *optimal* CBS:

- *High-level admissible heuristic* (§[3.2.1](#sec:cbs:hl-heuristics){reference-type="ref" reference="sec:cbs:hl-heuristics"}): Exploit conflict graphs [@felner2018adding], pairwise dependency graphs (DGs) [@li2019improved], and their weighted variants (WDGs) to guide the high-level search.

- *Symmetry reasoning techniques* (§[3.2.2](#sec:cbs:symmetry){reference-type="ref" reference="sec:cbs:symmetry"}): Introduce additional constraints (rectangle, corridor, target constraints, *etc*.) to break symmetrical collisions early.

- *Mutex propagation* (§[3.2.3](#sec:cbs:mutex){reference-type="ref" reference="sec:cbs:mutex"}): Employ MDD-based mutual-exclusion checks to identify unreachable or conflicting states in the low-level search.

- *Disjoint splitting* (§[3.2.4](#sec:cbs:disjoint){reference-type="ref" reference="sec:cbs:disjoint"}): Alter the branching scheme so that each conflict splits into two child nodes that enforce complementary constraints, ensuring their candidate plans remain mutually exclusive.

We first provide a brief overview of these modules, then show how to integrate each into the CBS pseudocode with minimal modifications highlighted.

### High-Level Admissible Heuristics {#sec:cbs:hl-heuristics}

Standard CBS expands nodes in the conflict tree (CT) by using the sum of paths' costs (or makespan) as the priority. *High-level admissible heuristics* augment this with more informed estimates of the minimal number of conflicts to resolve. Key representative heuristics include:

- **Conflict Graph (CG) [@felner2018adding]:** Construct a graph whose vertices correspond to agents, adding an edge whenever two agents admit a *cardinal conflict*. Taking the minimum vertex cover (MVC) of this graph yields a heuristic value.

- **Pairwise Dependency Graph (DG) [@li2019improved]:** Incorporates not only cardinal conflicts but also semi-cardinal or non-cardinal ones. MDDs help identify whether two agents are *dependent*. The MVC of the DG then provides a refined heuristic estimate.

- **Weighted Pairwise Dependency Graph (WDG) [@li2019improved]:** Assign each edge a weight $\Delta_{i,j}$ measuring the difference in the pairwise SoCs for relevant conflicts. The *edge-weighted minimum vertex cover* (EWMVC) of the WDG further tightens the HL heuristic.

### Symmetry Reasoning Techniques {#sec:cbs:symmetry}

*Symmetry reasoning* adds specialized constraints whenever two agents repeatedly collide under symmetrical conditions:

- **Rectangle symmetries [@li2019symmetry]:** Two agents create a *rectangle conflict* if each uses only Manhattan-optimal paths and collides in an axis-aligned sub-grid. Extended forms (*generalized rectangle symmetry* [@li2021pairwise]) exploit intersecting MDDs to identify larger conflicting sub-lattices.

- **Target symmetries [@li2020new]:** Where an agent waits indefinitely at its goal, forcing frequent collisions with other agents passing through that cell.

- **Corridor symmetries [@li2020new]:** If two agents attempt to enter a narrow corridor (one-dimensional sub-grid) from opposite ends, they may repeatedly block each other.

By detecting these patterns, the HL search can introduce specialized constraints that eliminate *all* symmetric permutations of the same conflict at once, dramatically reducing expansions.

### Mutex Propagation {#sec:cbs:mutex}

*Mutex propagation* [@zhang2022multi] prunes infeasible or redundant portions of the MDD. Two MDD nodes $n_i$ and $n_j$ at time step $t$ are *mutex* (mutually exclusive) if no valid collision-free sub-paths can place agents $i$ and $j$ at $n_i.\text{loc}$ and $n_j.\text{loc}$ respectively at time $t$. Identifying and removing such *mutex* pairs at each level yields a more accurate approximation of feasible states for the LL search, thus guiding CBS to detect and handle collisions more effectively.

### Disjoint Splitting {#sec:cbs:disjoint}

In standard CBS, a conflict $(i, j, v, t)$ splits the CT node into two children: one forbids agent $i$ from being at $(v,t)$, the other forbids agent $j$. *Disjoint splitting* [@li2019disjoint] alters this branching so that one child *verifies* agent $i$ must occupy $(v,t)$ (an *include* constraint), while the other forbids it. A similar scheme applies to $(j, v, t)$ in the second child node. These complementary constraints ensure that the sets of candidate solutions for each child node are *disjoint*, preventing repeated exploration of the same partial paths in multiple branches.

### Pseudocode for Enhanced CBS Variants

We now present pseudocode snippets illustrating how each of these enhancement modules can be integrated into the baseline CBS of Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"} (Section [3.1.3](#sec:cbs:algorithm){reference-type="ref" reference="sec:cbs:algorithm"}). In each snippet, **additions** or **changes** compared to the baseline are enclosed in for clarity. Although each module can be combined with the others in practice, we isolate them below for clarity.

:::: algorithm
::: algorithmic
Same inputs as in Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"} (Sec. [3.1.3](#sec:cbs:algorithm){reference-type="ref" reference="sec:cbs:algorithm"}), plus function. Initialize the root node $N_0$: For each agent $i$, compute path $\pi_i$ ignoring collisions; all constraint sets are empty. Insert $N_0$ into open list, keyed by $f(N_0) = \mathrm{Cost}(\{\pi_i\}) + h(N_0)$. $N \gets$ pop node with smallest $f(N) = \mathrm{Cost}(N) + h(N)$ Check for conflicts among $\{\pi_i\}$ in $N$. $\{\pi_i\}$ (optimal solution) Let $(i, j, t)$ be the first conflict. Create $N'$ by copying $N$. Add constraint forbidding agent $a$ from the conflict at time $t$. Recompute $\pi_a$ for agent $a$ via low-level A\*. Insert $N'$ into open list with $f(N')=\mathrm{Cost}(N') + h(N')$. *No feasible solution.*
:::
::::

**Explanation (CBSH).** The main change is in lines 2 and 16, which compute and maintain an *admissible* HL heuristic, such as the MVC on a conflict graph (CG) or a pairwise dependency graph (DG/WDG). All other steps follow the baseline CBS logic.

:::: algorithm
::: algorithmic
Same inputs as in Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}, plus function. Initialize root node $N_0$ (same as baseline). Insert $N_0$ into open list. $N \gets$ *pop front of open list* Check for conflicts among $\{\pi_i\}$ in $N$. $\{\pi_i\}$ (optimal solution) Let $(i, j, t)$ be the first conflict. **Detect** Recompute $\{\pi_i\}$ for the relevant agents Insert $N$ back into open list (updated constraints) Create $N'$ by copying $N$. Add standard CBS conflict constraint for agent $a$. Recompute $\pi_a$ for agent $a$. Insert $N'$ into open list *No feasible solution.*
:::
::::

**Explanation (CBS-SR).** Compared to Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}, lines 10--13 **(*enclosed in boxes*)** introduce new logic to detect symmetry conflicts and add *symmetry-breaking constraints* (e.g., forbidding all permutations of a rectangle conflict). Only if symmetry is *not* detected does the algorithm revert to the standard CBS branching in lines 15--24.

:::: algorithm
::: algorithmic
Same inputs as in Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}, plus subroutine. Initialize root node $N_0$ with no constraints and unconstrained paths $\{\pi_i\}$. Insert $N_0$ into open list. $N \gets$ *pop front of open list* Check for conflicts among $\{\pi_i\}$ in $N$. $\{\pi_i\}$ (optimal solution) Let $(i,j,t)$ be the first conflict. Create $N'$ by copying $N$. Add constraint forbidding agent $a$ from conflict. Recompute $\pi_a$ under updated constraints. Insert $N'$ into open list *No feasible solution.*
:::
::::

**Explanation (CBS-Mutex).** Lines 2--3 and 16 **(*enclosed in boxes*)** call a `mutexCheckMDDs` routine that removes from each agent's MDD any node that is mutually exclusive with another agent's feasible states. This routine can be invoked after *any* constraint update, typically in the low-level step.

:::: algorithm
::: algorithmic
Same inputs as in Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}. Initialize $N_0$ with unconstrained paths Insert $N_0$ into open list $N \gets \emph{pop front of open list}$ Check for conflicts among $\{\pi_i\}$ in $N$ $\{\pi_i\}$ (optimal solution) Let $(i, j, v, t)$ be the first conflict Create $N'$ by copying $N$ Recompute $\pi_a$ for agent $a$ Insert $N'$ into open list *No feasible solution.*
:::
::::

**Explanation (CBS-DS).** Compared to the baseline branching (which forbids the conflict for either agent), lines 11--14 **(*enclosed in boxes*)** show a refined *disjoint* approach: one child *requires* agent $i$ (or $j$) at $(v,t)$, the other *forbids* it. Each approach leads to distinct candidate solution sets without overlap.

### Summary of Optimal CBS Variants

Each variant in Algorithms [\[alg:cbs:hl-heuristic\]](#alg:cbs:hl-heuristic){reference-type="ref" reference="alg:cbs:hl-heuristic"}--[\[alg:cbs:disjoint-splitting\]](#alg:cbs:disjoint-splitting){reference-type="ref" reference="alg:cbs:disjoint-splitting"} modifies the high-level or low-level CBS operations to reduce redundant conflict exploration, prune infeasible states via multi-agent mutex detection, or unify symmetrical collision patterns. Crucially, these modules are largely orthogonal and can be combined for further performance gains (e.g., *CBSH* plus *Symmetry Reasoning* plus *Disjoint Splitting*). Numerous implementations [@boyarski2015icbs; @felner2018adding; @li2019improved; @li2020new; @li2021pairwise; @zhang2022multi] confirm that such augmented CBS frameworks can optimally handle significantly larger MAPF instances than the plain baseline version, thus exemplifying how theoretical insights and well-designed heuristics can scale classical search-based methods in multi-agent pathfinding.

::::: table*
:::: threeparttable
::: tablenotes
1\. Conflict Graph; 2. Pairwise Dependency Graph; 3. Weighted Pairwise Dependency Graph.
:::
::::
:::::

## Suboptimal CBS Methods {#sec:cbs:suboptimal}

While optimal Conflict-Based Search (CBS) variants (Section [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"}) can guarantee the minimum possible solution cost, their computational requirements can escalate in large-scale or time-critical scenarios. To address these limitations, *suboptimal* CBS extensions relax optimality in exchange for significantly improved runtime. In what follows, we first outline the archetypal suboptimal CBS framework---**Enhanced CBS** (ECBS)---as a reference point, providing pseudocode that highlights its differences from classical CBS. We then briefly survey several notable ECBS-based extensions, including EECBS [@li2021eecbs], FECBS [@chan2022flex], and ITA-ECBS [@tang2024ita]. Each offers distinct strategies for distributing suboptimality factors ($w$), estimating costs in the high-level search, and coordinating how multiple agents share resources.

### Enhanced CBS (ECBS) {#sec:ecbs}

#### Overview and Key Ideas

ECBS [@barer2014suboptimal] introduces a suboptimality factor $w \ge 1$ into both the high-level (HL) and low-level (LL) searches of classical CBS (Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}). Specifically,

- *Low-Level Search Adjustment.* Each agent's single-agent path planner (e.g., A\*) is replaced or modified with a *bounded-suboptimal* version (often referred to as a *focal* search). For each agent $i$, the planner constructs an individual path $\pi_i$ satisfying $$\mathrm{Cost}(\pi_i) \;\le\; w \;\cdot\; \mathrm{Cost}(\pi_i^{\text{opt}}),$$ where $\mathrm{Cost}(\pi_i^{\text{opt}})$ is the agent's true single-agent optimal cost.

- *High-Level Focal Search.* At the HL level, ECBS maintains two priority queues:

  1.  **OPEN**, sorted by the sum of *lower-bound* path costs (often computed via an admissible heuristic on the single-agent path length).

  2.  **FOCAL**, containing all nodes from **OPEN** whose sum of lower-bound costs is within a multiplicative factor $w$ of the minimum in **OPEN**. The queue **FOCAL** is then sorted by a user-defined *focal heuristic* (e.g., the *sum of actual costs* or some conflict-based metric).

  The node popped from **FOCAL** (rather than **OPEN**) is the one expanded at each iteration. If a solution node $N_{\text{sol}}$ is returned, its final cost is guaranteed to be at most $w$ times the optimal cost.

In this way, ECBS systematically explores a *relaxed* search space guided by a suboptimality bound, often achieving significant speed-ups compared to optimal CBS. Algorithm [\[alg:ecbs\]](#alg:ecbs){reference-type="ref" reference="alg:ecbs"} highlights the changes from the baseline CBS pseudocode (Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"} in Section [3.1.3](#sec:cbs:algorithm){reference-type="ref" reference="sec:cbs:algorithm"}). Lines and logic added or modified for ECBS are **enclosed in** .

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, agents $\{1,\dots,n\}$, start vertices $\{s_i\}$, goal vertices $\{g_i\}$, suboptimality bound $w \ge 1$. Initialize the root node $N_0$:

- **For each agent $i$:** run a (or a focal search) to compute a path $\pi_i$ with cost at most $w \cdot \mathrm{Cost}(\pi_i^{\text{opt}})$.

- Set constraint sets to empty for all agents.

Check for conflicts among the paths $\{\pi_i\}$ in $N$. $\{\pi_i\}$ Let $(i, j, t)$ be the first detected conflict. Create $N'$ by copying $N$. Add a conflict constraint for agent $a$ at time $t$. Insert $N'$ into OPEN with key $\text{key}_\text{OPEN}(N') = L(N')$. *No feasible solution under suboptimal CBS.*
:::
::::

**Algorithm Explanation.**

- *Line 1--3.* Agents compute initial *bounded-optimal* (or *focal*) single-agent paths. A lower bound $L_i$ on each path cost is stored, summing to $L(N_0)$.

- *Lines 4--6.* ECBS manages two queues: **OPEN** (sorted by *lower-bound* sum of costs) and **FOCAL** (containing nodes whose lower-bound sum is within a factor $w$ of the smallest in **OPEN**).

- *Line 10--22.* Conflict handling proceeds similar to classical CBS, except that *bounded-suboptimal* single-agent search is used for replanning agent $a$.

- *Lines 23--25.* After generating new children, ECBS recalculates $L_{\min}$ from **OPEN**, updates the *focal threshold* $f_\text{th}$, and refills **FOCAL** accordingly.

### Variants of ECBS

#### Explicit Estimation CBS (EECBS).

EECBS [@li2021eecbs] incorporates additional heuristics in the high-level search to estimate inadmissible (but more informed) path costs. Specifically, it leverages an *online learning* approach to refine these estimates during node expansion. In practice, EECBS often reduces the search-tree size compared to vanilla ECBS, because it can more effectively prioritize nodes likely to yield feasible solutions.

#### Flexible ECBS (FECBS).

FECBS [@chan2022flex] relaxes the assumption that *one global* factor $w$ must govern suboptimality uniformly across all agents. Instead, it allows individual agents to have distinct suboptimality margins based on environmental constraints, agent importance, or resource availability. This *asymmetric suboptimality* broadens the set of solvable instances within tight time budgets, making FECBS particularly relevant to real-world settings where tasks exhibit varying priorities.

#### ITA-ECBS.

ITA-ECBS [@tang2024ita] integrates *target-assignment optimization* into the suboptimal CBS framework. Beyond searching for collision-free paths, it simultaneously refines how *goal vertices* are distributed among agents, governed by a suboptimal factor $w$. Experimental results suggest that ITA-ECBS can outperform standard ECBS-TA [@barer2014suboptimal] across a broad range of metrics, highlighting the benefits of coupling suboptimal MAPF with target allocation in a single search procedure.

### Comparison of Optimal vs. Suboptimal CBS

Table [1](#tab:cbs-opt-subopt){reference-type="ref" reference="tab:cbs-opt-subopt"} summarizes the relationship between classical *optimal* CBS algorithms (Section [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"}) and *suboptimal* CBS extensions. While optimal variants can be significantly improved with heuristics (e.g., conflict prioritization, symmetry breaking, mutex propagation), they still must expand or branch whenever needed to guarantee the minimal possible cost. By contrast, suboptimal approaches (ECBS, EECBS, FECBS, ITA-ECBS) permit bounding the solution cost by $w$ times the optimum, gaining substantial computational savings in many instances.

::: {#tab:cbs-opt-subopt}
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| **Method**                             | **Search Strategy**                                      | **Characteristics**                                                                            |
+:=======================================+:=========================================================+:===============================================================================================+
| *Optimal CBS Variants (Sec. [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"})*                                                                                            |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| Plain CBS [@sharon2015conflict]        | Standard HL + LL recursion                               | No suboptimal factor; guaranteed minimal cost.                                                 |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| CBS with HL heuristics                 | Admits conflict-based or pairwise dependency heuristics  | Reduces expansions by focusing on potential cardinal conflicts first.                          |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| CBS with Symmetry & Mutex reasoning    | Adds specialized constraints and mutual-exclusion checks | Aggressively prunes search space to handle repeated collisions.                                |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| *Suboptimal CBS Variants (Sec. [3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"})*                                                                                   |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| ECBS [@barer2014suboptimal]            | Focal search at both HL and LL with factor $w$           | Solutions cost at most $w \cdot \mathrm{Cost}(\text{opt})$, typically much faster in practice. |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| EECBS [@li2021eecbs]                   | ECBS + explicit cost estimation at HL                    | Learns better heuristics online, often fewer expansions.                                       |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| FECBS [@chan2022flex]                  | ECBS + flexible per-agent $w$                            | Adapts suboptimal factors individually, more practical under diverse agent constraints.        |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+
| ITA-ECBS [@tang2024ita]                | ECBS with integrated target assignment                   | Jointly solves target assignment + suboptimal path planning, often outperforms ECBS-TA.        |
+----------------------------------------+----------------------------------------------------------+------------------------------------------------------------------------------------------------+

: High-Level Comparison of Optimal and Suboptimal CBS Varieties
:::

From a theoretical standpoint, suboptimal CBS solutions retain *completeness* and offer bounded suboptimality, yet forego the strict cost guarantees of optimal methods. Empirically, they can tackle significantly larger or more complex MAPF scenarios within limited compute budgets, thus bridging the gap between purely optimal solutions and real-time industrial deployment.

## Priority-Based Search (PBS) {#sec:pbs}

Following our in-depth review of Conflict-Based Search (CBS) in Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}, we now turn to an alternative yet closely related search-based paradigm for MAPF known as *Priority-Based Search* (PBS). While CBS pursues a multi-agent search guided by conflicts and constraints, PBS tackles the collision-avoidance challenge by imposing a (partial) *priority ordering* on agents, such that each agent plans its path while *respecting* the fixed (i.e. *Prioritized Planning*, PP [@erdmann1987multiple]; *First Come First Served*, FCFS [@dresner2004multiagent]) or dynamically (i.e. *Safe Interval Path Planning*, SIPP [@phillips2011sipp]) assigned higher-priority agents' paths. The illustration of how agent-priority ordering affects the outcome of prioritized planning in PBS is shown in [12](#fig:pbs){reference-type="ref" reference="fig:pbs"}.

This subsection mirrors the structure of Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}: we begin by introducing the mathematical modeling that underlies PBS, then discuss the fundamental PBS algorithmic framework (comparable to "vanilla CBS"), examine notable enhancements (including dynamic priority inheritance and merging), and finally contrast PBS with CBS through a comparative lens.

:::: {#fig:pbs .figure latex-placement="htb!"}
![](Wang2025Where_figs/pbs.png){width="\\linewidth"}

::: caption
Illustration of how agent‐priority ordering affects the outcome of prioritized planning in PBS. Case 1 (top row): Map & Instance (left): a 2 $\times$ 5 grid with obstacles (blue squares), nodes labeled A--F, and two agents (green and orange) whose sources are shown by solid circles and whose targets are shown by hollow circles. Results (right): we compare two priority orders for planning---green $\prec$ orange (upper branch) versus orange $\succ$ green (lower branch). Under the green‐first ordering, we obtain conflict‐free paths shown in the figure, whereas the orange‐first ordering yields no feasible solution, demonstrating that a \"wrong\" priority can break completeness. Case 2 (bottom row): Map & Instance (left): a different 2 $\times$ 5 grid (nodes A--I), with sources and targets similarly annotated. Results (right): here both priority orders succeed, but produce markedly different path sequences.
:::
::::

### Mathematical Modeling for PBS and Its Variants {#sec:pbs:modeling}

As in the MAPF definitions of Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"} and the constraint-based formulation for CBS (Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}), we let: $$\mathcal{G} = (\mathcal{V}, \mathcal{E}), 
   \quad
   n\text{ agents } \{1,\dots,n\},
   \quad
   s_i, g_i \in \mathcal{V},$$ represent the environment and agent setup. We also adopt a discrete time horizon $T$, with agent $i$'s path $\,\pi_i = \bigl(v_i(0), v_i(1), \dots, v_i(T)\bigr)$ or, equivalently, the binary indicators $x_{i,v,t}\in\{0,1\}$ marking whether agent $i$ occupies vertex $v$ at time $t$.

Unlike CBS, which relies on conflict-tree branching when collisions are found, PBS systematically assigns each agent a *priority level*: $$\mathsf{P}:\{1,\dots,n\}\;\rightarrow\;\{1,\dots,n\},$$ such that a *lower numeric value* of $\mathsf{P}(i)$ indicates *higher* priority. The core principle then becomes: $$\text{When agent $i$ plans or updates its path, it must remain collision-free w.r.t.\ all agents $j$ for which } \mathsf{P}(j) < \mathsf{P}(i).$$ Mathematically, we incorporate constraints: $$\label{eq:pbs:constraint}
\begin{align}
   &x_{i,v,t} + x_{j,v,t} \;\le\; 1 
   \quad \text{for all }t, \,\forall v, \text{ only if } \mathsf{P}(j)<\mathsf{P}(i), \label{eq:pbs:vertex}\\[4pt]
   &x_{i,u,t} + x_{i,v,t+1} + x_{j,v,t} + x_{j,u,t+1}
     \;\le\; 3
   \quad \text{for all }(u,v), \text{ only if } \mathsf{P}(j)<\mathsf{P}(i), \label{eq:pbs:edge}
\end{align}$$ meaning that agent $i$ must avoid vertex and edge collisions with higher-priority agents but need not explicitly enforce constraints against lower-priority agents (those with $\mathsf{P}(j)>\mathsf{P}(i)$).

Consistent with Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}, we can adopt various objectives:

- **Sum of Costs (SoC).** Minimize $\sum_{i=1}^n \mathrm{Cost}(\pi_i)$, adding only the collision constraints for higher-priority agents.

- **Makespan.** Minimize $\max_{1\le i\le n}\mathrm{Cost}(\pi_i)$ under the same one-sided collision-avoidance scheme.

Alternatively, in *lifelong* settings, each agent repeatedly receives new tasks while *still* respecting the paths of currently higher-priority neighbors.

### Algorithmic Framework {#sec:pbs:framework}

#### Overview.

In *vanilla PBS*, one fixes a total ordering $$\mathsf{P}(1) < \mathsf{P}(2) < \dots < \mathsf{P}(n),$$ and iterates through agents in ascending priority. Each agent's path is found via standard single-agent pathfinding (e.g., A\*) on a time-expanded graph that marks all space-time cells occupied by *higher-priority* agents as forbidden. Because the lower-priority agents have not yet planned, they impose no constraints on the current agent's route. Hence, any collisions that might arise with same- or lower-priority agents are simply left to be resolved when those agents plan their paths (i.e., they must themselves detour around the higher-priority path). Algorithm [\[alg:pbs:vanilla\]](#alg:pbs:vanilla){reference-type="ref" reference="alg:pbs:vanilla"} outlines the process for a single pass from highest- to lowest-priority agent.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, $n$ agents each with $(s_i, g_i)$, total priority order $\mathsf{P}(1)<\dots<\mathsf{P}(n)$. For $i=1$ to $n$ (in ascending priority):

- Identify higher-priority agents $\{j \mid \mathsf{P}(j)<\mathsf{P}(i)\}$.

- Treat their chosen paths $\{\pi_j\}$ as static obstacles in time-space.

- Compute $\pi_i$ via single-agent pathfinding subject to these obstacles.

- If no path is found, **report** *infeasibility* under the current priority order.

**Return** all paths $\{\pi_1,\dots,\pi_n\}$ once computed.
:::
::::

**Comparison with CBS.** In CBS (Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}), *all* agents have partial paths that are refined by *conflict constraints* whenever collisions occur. By contrast, *vanilla PBS* never replans a *higher*-priority agent's path. Once assigned, it remains fixed; collisions *must* be handled by lower-priority agents. This approach can be implemented quickly and scales to large $n$ in many practical settings. Its main drawback is that a poor priority ordering may drastically inflate total path costs or lead to unsolvable constraints for the lower-priority agents.

#### Dynamic or Partial Orderings.

To improve beyond the naive fixed ordering, one can adopt a conflict-driven *branching on partial orders* [@ma2019searching]. Analogous to the branching in CBS, each time a collision arises between agents $i$ and $j$ of *undetermined* relative priority, the search forks into two CT nodes: one sets $i \prec j$, the other $j \prec i$. Each child node then plans or replans the relevant agent's path accordingly. The search thus explores only partial orderings that are necessary to resolve collisions, often reducing overhead compared to enumerating all $n!$ permutations.

### Illustrative Example

Consider a $2\times 3$ grid (as in Figure [10](#fig:cbs-example-grid){reference-type="ref" reference="fig:cbs-example-grid"} for CBS), with two agents: $$\text{Agent 1: }s_1=(0,0)\to g_1=(1,2), 
   \quad
   \text{Agent 2: }s_2=(1,0)\to g_2=(0,2).$$ Assume $\mathsf{P}(1)<\mathsf{P}(2)$, i.e., Agent 1 has higher priority. Then:

1.  **Plan $\pi_1$:** Agent 1 finds a direct route $(0,0)\!\to\!(0,1)\!\to\!(0,2)\!\to\!(1,2)$.

2.  **Plan $\pi_2$:** With $\pi_1$ fixed, Agent 2 sees that $(0,2)$ and $(1,2)$ are occupied or transitioning at times $t=2,3,\dots$. Hence, it must detour, e.g., $(1,0)\!\to\!(1,1)\!\to\!(1,1)\!\to\!(1,2)\!\dots$ or wait further.

If $\mathsf{P}(1)$ was chosen poorly, i.e., the direct path for Agent 1 might block Agent 2 for a long time. Still, by design, Agent 2 shoulders the entire collision-avoidance effort. This can be either advantageous (e.g., if Agent 1 is truly more critical) or suboptimal for system-level objectives.

### Enhancing PBS: Dynamic Priorities, Inheritance, and Merging

Over the years, a variety of PBS enhancements have emerged, analogous to the "optimal" and "suboptimal" CBS variants in Sections [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"} and [3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"}. Here, we focus on three main families of techniques:

**(1) Priority Inheritance with Backtracking (PIBT / winPIBT).** Originally proposed by @okumura2022priority, *PIBT* operates *one time-step at a time*. It dynamically reassigns priorities whenever a higher-priority agent becomes blocked by a lower-priority agent in the next step. The blocked low-priority agent *inherits* the higher priority and attempts to move out of the way, allowing for local deadlock resolution without globally changing the entire priority order.

- **winPIBT** [@okumura2019winpibt] generalizes this to a *$w$-step windowed* approach, planning a short horizon of $w>1$ steps for each agent at each iteration. The added foresight helps mitigate repeated short-sighted collisions.

- Both PIBT and winPIBT guarantee *eventual* goal reachability on certain classes of graphs (e.g., biconnected or cycle-rich networks), even though local re-planning can lead to suboptimal global cost.

**(2) Conflict-Driven PBS with Merging.** @ma2019searching unify the ideas of partial-order branching and *merging* proposed in the CBS context [@boyarski2022merging]. When the search detects repeated collisions between agents (or groups of agents), it merges them into a single *meta-agent*, which is then planned jointly on the time-expanded graph. This can drastically reduce repeated collisions among those agents, but it *increases* the complexity of their internal pathfinding. As in CBS merging, a careful choice of which agents to merge can yield a significant speed-up in practice.

**(3) Game-Theoretic Incentive (Mechanism Design).** @friedrich2024scalable propose a *mechanism-design* approach, ensuring that agents have no incentive to defect or misrepresent their costs. They fix the priority order (or partial order) in a manner independent of agent reports, then apply approximate MAPF algorithms (like a suboptimal PBS) to assign collision-free paths. Agents pay a *VCG-like* tax that reflects the externality they impose on others. Such strategyproof PBS frameworks can handle thousands of agents while retaining game-theoretic guarantees.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}$, $n$ agents, *initial* priority order $\mathsf{P}_0$, time horizon $T$. **Initialize:** For each agent $i$, set $\pi_i(0) = s_i$. Let $\Pi_{<t+1} = \{\pi_i(\tau)\mid \tau\le t\}$ Sort agents by current priorities, from highest to lowest. $\textbf{PlanStep}(\pi_i[t+1]\mid \Pi_{<t+1};\ \mathsf{P}, \mathcal{G})$ **priority-inherit:** $\mathsf{P}(j)\gets \mathsf{P}(i)-\epsilon$ $\textbf{ReplanStep}(j)$ *backtrack $(i,j)$* **break** $\{\pi_i(\tau)\} \quad \text{(one-step-at-a-time solution)}$
:::
::::

**Algorithm [\[alg:pbs:dynamic\]](#alg:pbs:dynamic){reference-type="ref" reference="alg:pbs:dynamic"}:** Illustrates a possible stepwise planning routine used by PIBT-like methods. In each time-step iteration, agents update their next move in priority order. If a higher-priority agent is blocked, it triggers *priority inheritance*, letting the lower-priority agent move first. Such a scheme ensures local progress in many congested environments. Notably, the final solution is not guaranteed to be *globally* cost-optimal.

### PBS Variants: Detailed Pseudocode and Comparisons with the Vanilla Algorithm

In Section [3.4.2](#sec:pbs:framework){reference-type="ref" reference="sec:pbs:framework"}, we presented the *vanilla* PBS procedure in Algorithm [\[alg:pbs:vanilla\]](#alg:pbs:vanilla){reference-type="ref" reference="alg:pbs:vanilla"}, illustrating how agents plan in ascending priority order. We also discussed three major enhanced PBS families: (i) *Priority Inheritance with Backtracking (PIBT-like)*, (ii) *Conflict-Driven PBS with Merging*, and (iii) *Mechanism-Design-based PBS*. Previously, Algorithm [\[alg:pbs:dynamic\]](#alg:pbs:dynamic){reference-type="ref" reference="alg:pbs:dynamic"} provided a stepwise *PIBT-like* approach. We now complement that with pseudocode for the other two methods, highlighting their key differences from Algorithm [\[alg:pbs:vanilla\]](#alg:pbs:vanilla){reference-type="ref" reference="alg:pbs:vanilla"} (the base version). In each pseudocode, we mark the \*modified or additional lines\* in a and provide line-by-line explanations.

#### (1) Recap: Base PBS Algorithm (Algorithm [\[alg:pbs:vanilla\]](#alg:pbs:vanilla){reference-type="ref" reference="alg:pbs:vanilla"}).

For ease of reference, we restate the base pseudocode:

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, $n$ agents each with $(s_i, g_i)$, total priority order $\mathsf{P}(1)<\cdots<\mathsf{P}(n)$. [*Single pass in ascending priority:*]{.underline} Let $\mathcal{X} \gets \{\pi_j \mid \mathsf{P}(j) < \mathsf{P}(i)\}$ $\pi_i \gets \textsc{SingleAgentPathPlanner}(s_i,\ g_i,\ \mathcal{X})$ **return** "*Infeasible under current ordering*" **return** $\{\pi_1,\ldots,\pi_n\}$
:::
::::

**Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"} Explanation (Lines 1--9):** 1) We fix a total ordering, iterating agents from highest priority ($i=1$) to lowest ($i=n$). 2) When planning agent $i$'s path, the paths for all $j$ with $\mathsf{P}(j) < \mathsf{P}(i)$ are treated as *spatio-temporal obstacles*. 3) If agent $i$ cannot find any path that avoids higher-priority obstacles, the algorithm declares failure under that ordering. 4) Otherwise, we produce a set of final paths in which each lower-priority agent yields to all higher-priority ones.

#### (2) Conflict-Driven PBS with Merging.

In *conflict-driven* PBS, the priority order is *not* fully fixed a priori. Instead, we discover necessary order constraints *on the fly*: whenever two agents $i$ and $j$ collide, we branch by forcing either $i \prec j$ or $j \prec i$. This procedure can be enriched with *merging* [@boyarski2022merging; @ma2019searching]: after repeated collisions between the same pair (or set) of agents, we merge them into a single *meta-agent*, which is then planned collectively. Algorithm [\[alg:pbs:conflict-merge\]](#alg:pbs:conflict-merge){reference-type="ref" reference="alg:pbs:conflict-merge"} shows the high-level approach; lines with a bold box are *modified/additional steps* relative to the *base PBS* logic in Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, $n$ agents each with $(s_i,g_i)$, . Initialize a node $N_0$. Insert $N_0$ into an [OpenList]{.smallcaps} or [Queue]{.smallcaps}. $N \gets$ pop front of OpenList Check collisions among $\{\pi_i\}$ in $N$. **return** $\{\pi_i\}$ as a valid plan (*partial order is fully consistent*) Let $(i,j)$ be a collision in $N$. (***Key difference from base PBS***) Recompute a joint path $\pi_{M_{ij}}$ for $M_{ij}$ avoiding collisions with other agents **Insert** $N$ back into OpenList with updated $\{\pi_{M_{ij}}, \pi_k\}$ $N' \gets$ clone of $N$ $\prec_{N'}$ by adding $i \prec j$ or $j \prec i$ Replan path(s) for whichever agent(s) must yield to the newly enforced order Insert $N'$ into OpenList **return** "*No feasible partial order found*"
:::
::::

#### Explanation of Algorithm [\[alg:pbs:conflict-merge\]](#alg:pbs:conflict-merge){reference-type="ref" reference="alg:pbs:conflict-merge"}:

1.  **Initialization (Lines 1--3).** Compare to *base PBS*, we do *not* specify a total priority from the outset. Each agent is given an unconstrained path, ignoring collisions.

2.  **Collision Check and Branching (Lines 7--10, 14--18).** On detecting a collision between agents (or meta-agents) $i$ and $j$, the algorithm can *branch* into two child nodes: one forcing $i\prec j$, the other $j\prec i$. In each child, we replan the yield-to-$\prec$ agent(s).

3.  **Merging (Lines 11--13).** If $i$ and $j$ have collided repeatedly or exceed some threshold, we *merge* them into a new meta-agent $M_{ij}$. We then re-find a single path for $M_{ij}$ (i.e., planning all agents in $M_{ij}$ simultaneously). This "solves collisions inside $M_{ij}$" cheaply but yields a bigger subproblem for $M_{ij}$'s next collisions with other agents.

4.  **Loop until solution or exhausted (Lines 4--5,19).** The partial order $\prec_N$ grows as collisions arise. Eventually, if we find a node with no collisions among the updated paths, that solution is a valid plan that respects the partial-order constraints.

**Differences from Base PBS.** Instead of committing to a single pass in ascending order, we *split* or *merge* whenever collisions appear. This approach can produce solutions that the fixed-order base PBS might fail to find easily, and can sometimes deliver better paths or prove certain cost bounds (though the latter is still typically suboptimal relative to "optimal CBS").

#### (3) Mechanism-Design-Based PBS (Strategyproof Priority Ordering).

In real-world applications involving distinct stakeholders or self-interested agents, a predetermined or conflict-driven priority might be *manipulated* by agents lying about their costs or start/goal times to gain better routes. @friedrich2024scalable propose a *mechanism design* approach, ensuring that the priority assignment is *independent of agents' reported data*. One can then apply an approximate (or even a simple single-pass) PBS routine to allocate collision-free paths, while charging each agent a *payment* reflecting the externality they impose. Algorithm [\[alg:pbs:mechanism\]](#alg:pbs:mechanism){reference-type="ref" reference="alg:pbs:mechanism"} illustrates a *high-level* procedure.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}$, $n$ agents with $(s_i,g_i)$, each agent's "(possibly reported) cost/time values" $(c_i,\dots)$, but $\mathsf{P}$ that does not depend on $c_i$. (e.g. random shuffle) **Run PBS** with the chosen $\mathsf{P}$ to generate $\{\pi_i\}$ (see Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}) Let $\mathrm{Cost}(\pi_i)$ be the (suboptimal) path cost for agent $i$, and $v_i$ the agent's reported *value* for achieving $g_i$. $W(\{\pi_i\}) \;\gets\;\sum_{i=1}^n \bigl[v_i - c_i\cdot \mathrm{Cost}(\pi_i)\bigr]^{+}$ ($[\cdot]^+$ means $\max\{0,\cdot\}$) : $W_{-i}(\{\pi_i\}) = \sum_{j\neq i} [\,v_j - c_j\,\mathrm{Cost}(\pi_j)\,]^{+}.$ $$p_i \;\;=\;\;
         \max_{\,\mathsf{P}_\text{all}\,\text{valid}} 
            \Bigl\{\,W_{-i}\bigl(\text{PBS}(\mathsf{P}_\text{all})\bigr)\!\Bigr\}
         \;\;-\;\;
         W_{-i}\bigl(\{\pi_i\}\bigr)
         \,.$$ (*like a VCG tax, subject to the range of priorities*) **return** $(\{\pi_i\},\{p_i\})$ where $p_i$ is each agent's charge.
:::
::::

#### Explanation of Algorithm [\[alg:pbs:mechanism\]](#alg:pbs:mechanism){reference-type="ref" reference="alg:pbs:mechanism"}:

- [Lines 1--2: *Exogenous Priority*]{.underline}. The priority order $\mathsf{P}$ is chosen *without* referencing $c_i,v_i$, hence an agent cannot influence its priority by lying.

- [Lines 3--4: *Suboptimal PBS*]{.underline}. We run standard or partial-order PBS as a black-box subroutine. The resulting paths can be suboptimal but feasible.

- [Lines 6--7: *Tax Payment*]{.underline}. Each agent $i$ pays a *VCG-like* tax equal to the difference between the best possible "others' welfare" if $i$ were absent and the "others' welfare" in the presence of $i$. The set of possible alternative priorities $\mathsf{P}_\text{all}$ is restricted to remain *independent* of $i$'s own data.

**Differences from Base PBS.** Although the path planning step (Line 2) can be quite similar to Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}, this approach (i) enforces that $\mathsf{P}$ not be manipulated by agent $i$, and (ii) appends a *payment* computation, ensuring the mechanism is *strategyproof*. This extra step has no direct analog in the classical (non-game-theoretic) PBS.

### Summary of Added Pseudocode and Their Key Differences

Table [2](#tab:pbs-compare-variants){reference-type="ref" reference="tab:pbs-compare-variants"} summarizes these three PBS variants (PIBT-like, conflict-driven merging, mechanism-based) in relation to *base PBS* (Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}). Each extension modifies how priorities are assigned or updated, how collisions are resolved (via branching or merging), or how final solutions incorporate incentive-aligned payments.

::: {#tab:pbs-compare-variants}
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Variant**                   **Key Modification**                                                                                 **Representative Pseudocode / Notable Differences**
  ----------------------------- ---------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Base PBS                      Single pass in ascending priority                                                                    Alg. [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}. Each agent yields to higher-priority paths. No dynamic reorder.

  *PIBT-like*                   Plan *one step at a time* in real time. Apply *priority inheritance* if blocked.                     Alg. [\[alg:pbs:dynamic\]](#alg:pbs:dynamic){reference-type="ref" reference="alg:pbs:dynamic"} replaces the single pass with a **for t=0..T** loop, re-evaluating next-step collisions. No global solution guarantee.

  *Conflict-Driven & Merging*   *Partial-order branching* for collisions. Once collisions are repeated, *merge* colliding agents.    Alg. [\[alg:pbs:conflict-merge\]](#alg:pbs:conflict-merge){reference-type="ref" reference="alg:pbs:conflict-merge"}. Instead of a single ascending order, the partial order grows with collision constraints. Merging forms meta-agents.

  *Mechanism-Design*            *Random or exogenous* priority to ensure strategyproofness. Compute *VCG-like* tax for each agent.   Alg. [\[alg:pbs:mechanism\]](#alg:pbs:mechanism){reference-type="ref" reference="alg:pbs:mechanism"}. Similar to base PBS for path planning, but no agent can influence $\mathsf{P}$ by lying. Payment stage appended.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  : Comparison of *PIBT-like*, *Conflict-Driven Merging*, and *Mechanism-Design* PBS with respect to *base PBS*.
:::

Collectively, these variants illustrate the versatility of PBS in diverse settings: from *online stepwise* planning (PIBT) to *conflict-driven merges* in offline MAPF, and even *game-theoretic* multi-agent allocations.

Thus, while the *base* (vanilla) PBS procedure (Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}) remains a minimal blueprint for priority-based collision avoidance, actual deployments often rely on these advanced extensions to handle dynamic priorities, repeated collisions, or incentive alignment. Together, they display how PBS can be tailored to balance simplicity, scalability, real-time adaptability, and strategic considerations.

### Contrasting CBS and PBS {#sec:pbs:vscbs}

Both CBS and PBS revolve around *managing collisions* among agents. Table [3](#tab:cbs-vs-pbs){reference-type="ref" reference="tab:cbs-vs-pbs"} distills their key similarities and differences:

::: {#tab:cbs-vs-pbs}
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                             **CBS** (Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"})                                                                              **PBS** (Section [3.4](#sec:pbs){reference-type="ref" reference="sec:pbs"})
  -------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Core Idea                  Two-level search (HL: constraints, LL: single-agent replan). Detect collisions among *all* agent paths, branch with constraints to fix collisions.       Implicit constraints from a *(partial) priority order.* Each agent actively avoids collisions with higher-priority agents' paths. Little/no replan of the higher-priority routes.

  Collision Handling         Upon conflict, *both* agents branch. In each child node, exactly one agent is constrained to avoid the conflict. A single final node is conflict-free.   Lower-priority agents must always detour: a conflict is effectively "won" by the higher-priority agent's path. Dynamic partial orders or inheritance can shift who is higher priority.

  Optimality                 Baseline CBS is complete and optimal for SoC or makespan if the branching is exhaustive, with variants adding heuristics for speed.                      Vanilla PBS is generally *not* guaranteed to find an optimal solution unless one enumerates or adjusts all possible priority orders. Typically yields suboptimal or incomplete results in large grids.

  Algorithmic Enhancements   **Optimal:** Admissible HL heuristics, symmetry breaking, merge-and-replan, disjoint splitting\                                                          **Static:** Single pass in total priority\
                             **Suboptimal:** ECBS, EECBS, *etc.*                                                                                                                      **Dynamic:** Conflict-driven partial orders; *priority inheritance*; merges; windowed planning\
                                                                                                                                                                                      **Mechanism design:** Strategyproof priority or partial order
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  : Comparison of Conflict-Based Search (CBS) and Priority-Based Search (PBS)
:::

**High-Level Observations.**

- *Complexity vs. Flexibility.* CBS can systematically achieve optimal solutions given enough branching, but typically sees exponential blowups for large $n$. PBS is simpler but heavily depends on a good (partial) priority assignment to produce near-optimal results.

- *Similar Enhancement Themes.* Both incorporate merging, suboptimal bounding (via focal searches or simpler heuristics), and specialized constraints for symmetrical conflicts.

- *Use Cases.* PBS is often favored in *online* or *lifelong* MAPF, where stepwise or partial-order planning (as in PIBT/winPIBT) yields quick updates in dynamic environments. CBS or suboptimal CBS may still excel in medium-scale, *offline* instances with strong demand for solution optimality or bounded suboptimality.

### Conclusion and Outlook for PBS

Priority-Based Search (PBS) stands alongside CBS as one of the fundamental search-based paradigms in multi-agent pathfinding. Its hallmark decision rule---"lower-priority agents must defer to higher-priority paths"---offers a straightforward collision-avoidance mechanism that can scale to large agent sets under real-time or constrained computation. We have seen how a simple, *static* total ordering can suffice in some applications but also how *dynamic* partial orders, *priority inheritance*, and *merging* can substantially improve PBS's completeness and solution quality.

Despite PBS's relative simplicity, it generally lacks the robust global optimality framework present in classical CBS. Nonetheless, specialized PBS extensions have bridged this gap somewhat by enumerating partial orders or integrating additional constraints in a manner reminiscent of CBS's conflict-resolution tree. Furthermore, the synergy with *mechanism design* offers a powerful route to strategyproof path assignments in open multi-robot systems.

In the subsequent sections, we explore compilation-based MAPF solvers (e.g., ILP, SAT) and learning-based methods. Both directions can be integrated with or inspired by search strategies akin to CBS or PBS, underscoring the diversity of approaches in modern MAPF research.

## Large Neighborhood Search (LNS) Methods for Suboptimal MAPF {#sec:lns}

Large Neighborhood Search (LNS) is a meta-heuristic optimization approach that has shown promise in solving suboptimal MAPF problems with potentially large numbers of agents and dynamic constraints [@li2021anytime; @li2022mapf; @lam2023exact; @tan2024benchmarking; @phan2024adaptive]. Unlike Conflict-Based Search (CBS) methods that systematically resolve collisions through high-level and low-level searches (Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}), LNS treats MAPF as a sequence of iterative refinements over a global solution, repeatedly "destroying" and "repairing" selected parts (or neighborhoods) of candidate solutions. The illustration of the core workflow in LNS is shown in Figure [13](#fig:lns){reference-type="ref" reference="fig:lns"}.

This section introduces the mathematical formulation of LNS in the MAPF setting, followed by a presentation of the baseline LNS algorithm and prominent LNS variants. We also compare how LNS complements or contrasts with both optimal and suboptimal CBS frameworks discussed in Section [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"} and Section [3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"}.

### Mathematical Formulation for LNS

We cast LNS-based MAPF using a similar problem definition as in Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}, with discrete time steps (or a permissible continuous time horizon) and a shared environment modeled by an undirected graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$. Each agent $i \in \{1,\dots,n\}$ has a start vertex $s_i$ and a goal vertex $g_i$. A candidate *global solution* is defined as a collection of single-agent paths $\{\pi_i\}_{i=1}^n$ where each $\pi_i$ is collision-free with respect to other paths.

:::: {#fig:lns .figure latex-placement="htb!"}
![](Wang2025Where_figs/lns.png){width="\\linewidth"}

::: caption
Illustration of the core workflow in LNS. Left: all agents (or path segments) are ranked by their "delay" scores---from highest (green) to lowest (pink). We select the target agent (green) and extract its current path (middle). Right: During the destroy phase (top right), a contiguous subsegment F,D is removed from the path. In the repair phase (bottom right), the best replacement vertex B (in green) is inserted at the removal point, producing the new path.
:::
::::

#### Decision Variables and Constraints.

As in Conflict-Based Search (Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}), we can define binary variables $x_{i,v,t}$ indicating whether agent $i$ is at vertex $v$ at time $t$, and impose collision-avoidance constraints: $$\begin{align}
x_{i,v,t} + x_{j,v,t} &\;\le\; 1, 
&&\forall\,t, \,\forall\,v \in \mathcal{V}, \,\forall\,i < j, \label{eq:lns-vertex}\\
x_{i,u,t} + x_{i,v,t+1} + x_{j,v,t} + x_{j,u,t+1} &\;\le\; 3,
&&\forall\, (u,v)\in\mathcal{E}, \,\forall\, t, \,\forall\,i< j, \label{eq:lns-edge}
\end{align}$$ accompanied by single-agent path consistency and start/goal constraints.

#### Objective.

Typically, LNS methods target one or more of the following objectives:

- **Makespan Minimization:** $$\min \max_{1 \leq i \leq n} \mathrm{Cost}(\pi_i),$$ where $\mathrm{Cost}(\pi_i)$ measures the time at which agent $i$ reaches $g_i$.

- **Sum of Costs (SoC):** $$\min \sum_{i=1}^{n} \mathrm{Cost}(\pi_i).$$

- **Hybrid or Weighted Metrics (e.g., Weighted SoC):** $$\min \sum_{i=1}^{n} \alpha_i \,\mathrm{Cost}(\pi_i),$$ where $\alpha_i$ sets per-agent weighting for more flexible optimization criteria.

### Algorithmic Framework and Basic LNS {#sec:lns:framework}

Large Neighborhood Search, originally popularized in vehicle routing and related combinatorial problems, proceeds by iteratively refining a *current solution* (global set of paths) via two complementary actions:

1.  **Destroy:** Select a subset of agents (or edges, time intervals, etc.) and temporarily remove or invalidate their paths, creating partial solutions with missing paths.

2.  **Repair:** Replan the removed agents' paths (using some constructive or heuristic method) in a way that hopefully reduces overall cost while maintaining collision-free feasibility.

This meta-heuristic leverages the intuition that large-scale disruptions to the current solution can escape local minima more effectively than small, incremental updates. Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"} provides a simplified pseudocode for basic LNS in the MAPF context.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}$, agents $\{1,\dots,n\}$, start $\{s_i\}$, goal $\{g_i\}$, destroy ratio $\gamma$, max iterations $K$. **Initialize** a feasible solution $\{\pi_i^{(0)}\}$ (e.g., by a greedy or search-based solver). $S \gets \{\pi_i^{(0)}\}_{i=1}^n$ $S_{\mathrm{best}} \gets S$ **Destroy Step:** $S^{\mathrm{partial}} \gets S \setminus \{\pi_i : i \in \mathcal{D}\}$ **Repair Step:** Combine paths into new solution $S^{\prime}$. $S_{\mathrm{best}} \gets S^{\prime}$ $S \gets$ [AcceptanceCriterion]{.smallcaps}$(S, S^{\prime})$ $S_{\mathrm{best}}$
:::
::::

**Algorithm Explanation.**

- *Initialization (Lines 1--3).* A feasible solution is produced via any standard method (e.g., single-agent A\* ignoring collisions, combined with a naive conflict-resolution pass). This serves as $S$, the current solution, and $S_{\mathrm{best}}$, the best solution found so far.

- *Destroy Step (Lines 6--7).* A fraction $\gamma$ of agents are randomly (or heuristically) selected, and their paths are removed from $S$. The remaining agents keep their existing paths, forming $S^{\mathrm{partial}}$.

- *Repair Step (Lines 8--9).* Each removed agent is re-inserted (planned) in a manner that aims to reduce collisions and overall cost. Any single-agent method, bounded-suboptimal pathfinding, or even an embedded MAPF solver can be used.

- *Solution Acceptance (Lines 12--13).* After constructing $S^{\prime}$, LNS updates the global best $S_{\mathrm{best}}$ if $\mathrm{Cost}(S^{\prime})$ improves upon the previous best. The routine [AcceptanceCriterion]{.smallcaps} decides whether to set $S^{\prime}$ or the old $S$ as the new *current solution* for the next iteration. Common strategies include always accept if $\mathrm{Cost}(S^{\prime}) \le \mathrm{Cost}(S)$ (greedy) or occasionally accept worse solutions to promote escaping local minima (similar to simulated annealing).

Compared to suboptimal CBS (Section [3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"}), LNS explicitly leverages large-scale partial reoptimization rather than systematic conflict splitting. As a result, LNS can quickly explore diverse regions of the solution space, especially in large instances where enumerating conflict trees becomes costly.

### Notable LNS Variants {#sec:lns:variants}

A variety of specialized LNS strategies have been proposed to address efficiency, scalability, and dynamic adaptability in MAPF. In particular, we highlight five notable LNS-based methods below, each introducing unique refinements for suboptimal MAPF. For clarity, we provide pseudocode fragments that extend or modify the baseline LNS procedure (Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"}). All indicate **additions** or **changes** compared to the baseline, facilitating direct comparison across variants.

#### Anytime LNS-based MAPF (ALNS).

@li2021anytime proposed an *anytime* LNS approach that can produce a valid solution quickly, then iteratively refine it to higher quality if time permits. It incorporates adaptive destroy-repair strategies to prioritize collisions. Algorithm [\[alg:alns\]](#alg:alns){reference-type="ref" reference="alg:alns"} highlights key modifications: an explicit `UpdateTimeBudget` routine to ensure the method returns the best solution before the time limit expires.

:::: algorithm
::: algorithmic
, destroy ratio $\gamma$, max iterations $K$. **Initialize** $S, S_{\mathrm{best}}$ as in Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"}. **return** Perform **Destroy** and **Repair** steps as in Lines 6--9 of Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"}. $S_{\mathrm{best}} \gets S^{\prime}$ $S \gets \textsc{AcceptanceCriterion}(S, S^{\prime})$ $S_{\mathrm{best}}$
:::
::::

#### MAPF-LNS2.

@li2022mapf introduced *MAPF-LNS2*, which focuses on *fast conflict resolution* by reconstructing agent paths within local neighborhoods. It often employs a more refined 'destroy' step that selectively removes only those agents heavily involved in collisions. While Algorithm [\[alg:lns2\]](#alg:lns2){reference-type="ref" reference="alg:lns2"} is structurally similar to the baseline, the crucial distinction lies in the multi-layered repair strategy (Lines 10--12) that re-inserts agents with a specialized local solver.

:::: algorithm
::: algorithmic
**Differences from Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"} are marked with boxes.** Graph $\mathcal{G}$, destroy ratio $\gamma$, , max iterations $K$. Initialize solution $S, S_{\mathrm{best}}$ as before. **Destroy Step:** $S^{\mathrm{partial}} \gets S\setminus\{\pi_i : i\in \mathcal{D}\}$ **Repair Step:** Combine new paths into $S^{\prime}$. $S_{\mathrm{best}} \gets S^{\prime}$ $S \gets \textsc{AcceptanceCriterion}(S, S^{\prime})$ $S_{\mathrm{best}}$
:::
::::

#### BCP-LNS for Exact Anytime Solutions.

@lam2023exact combined Branch-and-Cut-and-Price (BCP) methods with LNS to deliver *exact* solutions in an anytime manner. Although BCP supports an *optimal* solution guarantee, its worst-case runtime can be large. Hence, LNS heuristics are employed to prune the search space aggressively. Algorithm [\[alg:bcp-lns\]](#alg:bcp-lns){reference-type="ref" reference="alg:bcp-lns"} shows the synergy, where a partial BCP-based cut is enforced in each **Repair Step** (Line 9).

:::: algorithm
::: algorithmic
**Key additions are marked with boxes.**. Graph $\mathcal{G}$, agents, max iterations $K$. Initialize solution $S, S_{\mathrm{best}}$. **Destroy Step:** same as baseline LNS (Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"}). **Repair Step:** $S^{\prime} \gets S^{\mathrm{partial}} \cup \{\pi_i` \text{for} i\in\mathcal{D}\}$ $S_{\mathrm{best}}\gets S^{\prime}$ $S\gets \textsc{AcceptanceCriterion}(S,S^{\prime})$ $S_{\mathrm{best}}$
:::
::::

#### Benchmarking LNS (B-LNS).

@tan2024benchmarking conducted a comprehensive evaluation of multiple LNS-based algorithms on standard MAPF benchmarks. Although there is no fundamentally new pseudocode, their approach systematically compares different *destroy* heuristics (random, collision-based, region-based), *repair* strategies (standard A\*, suboptimal focus search), and acceptance criteria (greedy vs. simulated annealing). Their findings highlight how distinct LNS configurations trade off solution quality and runtime differently across problem scales.

#### Bandit-based Adaptive LNS (BA-LNS).

@phan2024adaptive introduced a *multi-armed bandit* mechanism to adaptively select among multiple destroy-repair heuristics. Agents or conflict regions are assigned to "arms," and the algorithm dynamically shifts selection probability toward heuristics producing the largest improvement over the last few iterations. Algorithm [\[alg:ba-lns\]](#alg:ba-lns){reference-type="ref" reference="alg:ba-lns"} illustrates this scheme, where [BanditSelection]{.smallcaps} maintains a reward distribution for each destroy/repair pair.

:::: algorithm
::: algorithmic
**Key differences from Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"} are marked with boxes.**. Graph $\mathcal{G}$, destroy-heuristic set $\{\mathrm{DH}_m\}$, repair-heuristic set $\{\mathrm{RH}_n\}$, max iterations $K$. Initialize $S, S_{\mathrm{best}}$, and . **Destroy Step:** **Repair Step:** Evaluate $S^{\prime}$ and compute the improvement $\Delta = \mathrm{Cost}(S) - \mathrm{Cost}(S^{\prime})$. $S_{\mathrm{best}} \gets S^{\prime}$ $S \gets \textsc{AcceptanceCriterion}(S,S^{\prime})$ $S_{\mathrm{best}}$
:::
::::

### Comparison with CBS-based Methods

Both LNS and CBS methods aim to solve MAPF in suboptimal (bounded or heuristic-driven) regimes, but they employ fundamentally different strategies:

- **Conflict Resolution vs. Destroy-Repair:** Suboptimal CBS (ECBS, EECBS, etc.) systematically resolves collisions via branching constraints and bounded-suboptimal single-agent replanning, while LNS performs large-scale partial reoptimizations on selected agents.

- **Search Granularity:** CBS-based approaches track collision conflict trees, refining partial solutions at a conflict-by-conflict level. LNS manages solutions at a more *global* scale (entire subsets of agents, or spatiotemporal neighborhoods).

- **Performance and Scalability:** Empirical benchmarks [@li2021anytime; @li2022mapf; @tan2024benchmarking; @chan2022flex] indicate that LNS can handle larger MAPF instances more gracefully, converging to feasible solutions quickly, though with fewer theoretical guarantees than standard CBS. On the other hand, suboptimal CBS methods can provide bounded suboptimality guarantees (e.g., solution cost $\leq w \cdot \mathrm{Cost}(\text{opt})$), which can be appealing in certain real-time applications.

LNS methods, particularly in the form of ALNS [@li2021anytime] and MAPF-LNS2 [@li2022mapf], demonstrate strong adaptability to dynamic environments and partial observations by re-optimizing large portions of the solution when new information arrives or constraints change. They can therefore be particularly beneficial in industrial scenarios (e.g., warehouse logistics or multi-drone coordination) where tasks evolve over time. Simultaneously, the line of BCP-LNS [@lam2023exact] highlights how coupling LNS with rigorous optimization backends can bridge the gap between heuristic speed and exactness if computational resources permit. Lastly, adaptivity via bandit-based strategies [@phan2024adaptive] offers a systematic means to tune LNS parameters online, thereby potentially outperforming static heuristics in diverse MAPF contexts.

Overall, LNS serves as a complementary approach to both optimal and suboptimal CBS, especially in large-scale or highly dynamic MAPF problems where partial reoptimization can effectively balance solution quality with rapid convergence. Future research may combine the conflict-tree perspective of CBS with the large-scale reoptimization advantages of LNS, further broadening the computational toolkit for MAPF researchers and practitioners alike.

## Lazy Constraints Addition Search (LaCAM)

In recent years, the field of MAPF has continually grappled with the trade-off between computational complexity and real-time performance while striving for high-precision solutions. On the one hand, early time-independent and offline planning methods [@okumura2021time; @okumura2021offline] enhanced solution accuracy by precomputing conflict-free paths. However, these approaches tend to incur high computational overhead, limiting their scalability and adaptability in dynamic environments. On the other hand, to meet real-time demands, researchers have introduced iterative optimization techniques [@okumura2021iterative]. Although this method offers clear advantages in terms of running time, its near real-time solution process may fall short of achieving optimal accuracy.

:::: {#fig:lacam .figure latex-placement="htb!"}
![](Wang2025Where_figs/lacam.png){width="\\linewidth"}

::: caption
Illustration of LaCAM. Top left (Map & Instance): A 3 $\times$ 3 grid (blue squares are represent obstacles) with nodes labeled A--D, and two agents ([]{style="color: ACD78E"} and []{style="color: F5B482"}) whose sources (solid circles) and targets (hollow circles) are shown. A high‐level node (rounded rectangle) holding the current global configuration of all agents (black circle). Within each high‐level node, LaCAM invokes a lazy low‐level search for one agent cluster (shown by dashed gray boxes). Successor configurations are generated by cluster‐specific constraints, indicated by labeled arrows (e.g. A$\rightarrow$A, A$\rightarrow$B, B$\rightarrow$D, B$\rightarrow$C, C$\rightarrow$B, C$\rightarrow$C) that fix one cluster's agent positions in the next configuration. Each low‐level invocation produces a minimal successor; once refined, it is merged back into the parent high‐level node and the next cluster is processed.
:::
::::

### Suboptimal Method

More recently, research has focused on system robustness and scalability in large-scale environments [@okumura2023fault; @okumura2023lacam], leading to the development of an improved method known as Lazy Constraints Addition Search (LaCAM), as shown in Figure [14](#fig:lacam){reference-type="ref" reference="fig:lacam"}. LaCAM is a step-by-step configuration search method inspired by the CBS framework. Similar to CBS, LaCAM employs a two-level architecture: the high-level search maintains a sequence of configurations, while the low-level search dynamically generates *constraints*. The primary innovation of LaCAM (Algorithm [\[alg:lacam\]](#alg:lacam){reference-type="ref" reference="alg:lacam"}) is its lazy evaluation strategy at the low-level search, which incrementally creates minimal successors only when the corresponding high-level node is explored.

:::: algorithm
::: algorithmic
MAPF instance ($\mathcal{S}$: starts, $\mathcal{G}$: goals) **Initialize:** Create root constraint $\mathcal{C}_{\text{init}} \leftarrow \langle~ parent: \bot, who: \bot, where: \bot~\rangle$; $\mathcal{N}_{\text{goal}} \leftarrow \bot$ Initialize $Open$ and $Explored$ Create initial node: $\mathcal{N}_{\text{init}} \leftarrow \langle~config: \mathcal{S},~tree: \llbracket~\mathcal{C}_{\text{init}}~\rrbracket,~neighbors: \emptyset,~parent: \bot$ $Open.\textbf{push}(\mathcal{N}_{\text{init}})$; $Explored[\mathcal{S}] \leftarrow \mathcal{N}_{\text{init}}$ $\mathcal{N} \leftarrow Open.\textbf{top}()$ $\textsc{backtrack}(\mathcal{N})$ $Open.\textbf{pop}()$; **continue** $\mathcal{C} \leftarrow \mathcal{N}.tree.\textbf{pop}()$ $\textsc{LowLevelExpansion}(\mathcal{N}, \mathcal{C})$ $Q_{\text{new}} \leftarrow \textsc{ConfigurationGenerator}(\mathcal{N}, \mathcal{C})$ **continue** $$\mathcal{N}_{\text{new}} \leftarrow \langle~config: Q_{\text{new}},~tree: \llbracket~\mathcal{C}_{\text{init}}~\rrbracket,~parent: \mathcal{N}~\rangle$$ $Open.\textbf{push}(\mathcal{N}_{\text{new}})$ $Explored[Q_{\text{new}}] \leftarrow \mathcal{N}_{\text{new}}$ `NO_SOLUTION`
:::
::::

### Eventually Optimal Method

[@okumura2023improving] aimed to achieve a more balanced trade-off between accuracy and computational complexity by integrating pre-computation with online adjustment strategies. Specifically, their method differs from LaCAM in three main aspects (Algorithm [\[alg:lacamstar\]](#alg:lacamstar){reference-type="ref" reference="alg:lacamstar"}):

1.  It continues the search even after finding the goal configuration $\mathcal{G}$.

2.  It dynamically revises parent relationships among search nodes as needed.

3.  Unlike LaCAM, which is a sub-optimal algorithm, LaCAM\* has been proven to be complete and optimal; see Theorem 1 in [@okumura2023improving] for further details.

:::: algorithm
::: algorithmic
MAPF instance ($\mathcal{S}$: starts, $\mathcal{G}$: goals), edge cost $\textbf{cost}_e$, admissible heuristic $\textbf{h}$ **Initialize:** Create root constraint $\mathcal{C}_{\text{init}} \leftarrow \langle~ parent: \bot, who: \bot, where: \bot~\rangle$; $\mathcal{N}_{\text{goal}} \leftarrow \bot$ Initialize $Open$ (priority queue ordered by $f(\mathcal{N})=\mathcal{N}.g + h(\mathcal{N})$) and $Explored$ Create initial node: $\mathcal{N}_{\text{init}} \leftarrow \langle~config: \mathcal{S},~tree: \llbracket~\mathcal{C}_{\text{init}}~\rrbracket,~neighbors: \emptyset,$$~parent: \bot,~neigh : \emptyset, ~g:0~\rangle$ $Open.\textbf{push}(\mathcal{N}_{\text{init}})$; $Explored[\mathcal{S}] \leftarrow \mathcal{N}_{\text{init}}$ $\mathcal{N} \leftarrow Open.\textbf{top}()$ $\mathcal{N}_{\text{goal}} \leftarrow \mathcal{N}$ $Open.\textbf{pop}()$; **continue** $Open.\textbf{pop}()$; **continue** $\mathcal{C} \leftarrow \mathcal{N}.tree.\textbf{pop}()$ $\textsc{LowLevelExpansion}(\mathcal{N}, \mathcal{C})$ $Q_{\text{new}} \leftarrow \textsc{ConfigurationGenerator}(\mathcal{N}, \mathcal{C})$ **continue** $\mathcal{N}.neighbors.\textbf{append}(Explored[Q_{\text{new}}])$ $\textsc{DijkstraOpen} \leftarrow \llbracket \mathcal{N} \rrbracket$ $\mathcal{N}_{\text{from}} \leftarrow \textsc{DijkstraOpen}.\textbf{pop}()$ $g \leftarrow \mathcal{N}_{\text{from}}.g + \textbf{cost}_e(\mathcal{N}_{\text{from}}, \mathcal{N}_{\text{to}})$ $\mathcal{N}_{\text{to}}.g \leftarrow g$; $\mathcal{N}_{\text{to}}.parent \leftarrow \mathcal{N}_{\text{from}}$; $\textsc{DijkstraOpen}.\textbf{push}(\mathcal{N}_{\text{to}})$ $Open.\textbf{push}(\mathcal{N}_{\text{to}})$ Create successor node: $$\mathcal{N}_{\text{new}} \leftarrow \langle~config: Q_{\text{new}},~tree: \llbracket~\mathcal{C}_{\text{init}}~\rrbracket,~neighbors: \emptyset,~parent: \mathcal{N},~g:\mathcal{N}.g + \textbf{cost}_e(\mathcal{N},Q_{\text{new}})~\rangle$$ $Open.\textbf{push}(\mathcal{N}_{\text{new}})$; $Explored[Q_{\text{new}}] \leftarrow \mathcal{N}_{\text{new}}$ $\mathcal{N}.neighbors.\textbf{append}(\mathcal{N}_{\text{new}})$ $\textsc{Backtrack}(\mathcal{N}_{\text{goal}})$ $\textsc{Backtrack}(\mathcal{N}_{\text{goal}})$ `NO_SOLUTION` `FAILURE`
:::
::::

### Engineering-Oriented Method

The latest engineering effort, [@okumura2024engineering] further validates this approach by systematically combining multiple strategies to effectively reduce computational complexity while maintaining high planning accuracy, thereby addressing the practical needs of large-scale, real-time applications. Overall, these works underscore the importance of dynamically balancing solution accuracy and complexity in the MAPF problem, and future research is likely to focus on further optimizing this trade-off using adaptive techniques.

# Compilation-Based Methodology {#sec:compilation}

Transitioning from the systematic graph-based approaches discussed in Section [3](#sec:search){reference-type="ref" reference="sec:search"}, we now turn to *compilation-based* methodologies for MAPF. Unlike search-based techniques, which explicitly enumerate collision-free paths, compilation-based methods recast MAPF constraints into a target formalism (e.g., Boolean logic, linear programming) to leverage the power of general-purpose solvers. In doing so, they help researchers sidestep the complexities of state-space exploration by delegating path planning to mature frameworks such as SAT, SMT, CSP, ASP, or MIP. This shift not only allows for well-established theoretical guarantees---arising from decades of solver development---but also provides a flexible toolset for handling heterogeneous agent capabilities and specialized constraints. In the following subsections, we review several notable families of compilation-based approaches, highlight their encoding strategies through illustrative examples and pseudocode, and analyze how each balances scalability, ease of modeling, and solution quality.

## Boolean Satisfiability (SAT) {#sec:compilation-sat}

This section presents the family of *Boolean satisfiability* (SAT) methods for Multi-Agent Path Finding (MAPF) under the sum-of-costs (SoC) objective. Building on a long line of work [@surynek2016efficient; @surynek2018sub; @surynek2017integration; @bartak2019sat; @surynek2021mutex; @surynek2022migrating; @vcapek2021dpll], SAT-based MAPF transforms the coordination of multiple agents---their collision avoidance, time discretization, and SoC minimization---into a propositional formula. A SAT solver is then invoked to find (or prove the non-existence of) collision-free paths within a specified time horizon and cost bound.

We first describe the *modeling framework* for the SoC objective in detail, with a small *toy example* illustrating how the formulation works in practice. We then present a *baseline* SAT-based algorithm, expanding on its pseudocode and design. Finally, we discuss several *notable variants* and show how each modifies the baseline procedure, highlighting their distinct pseudocode differences.

### Modeling Framework for Sum-of-Costs (SoC) {#sec:sat:modeling}

In the SAT-based paradigm, the MAPF problem is cast as a decision question: $$\textit{``Is there a set of collision-free paths for all agents such that the total SoC is at most } \xi \text{?''}$$ To attempt different SoC bounds, we usually increment $\xi$ or an equivalent parameter until we find a feasible (i.e., satisfiable) assignment. Below, we introduce the key ingredients of this formulation.

#### Graph Layout and Time Discretization.

Let $\mathcal{G}=(\mathcal{V},\mathcal{E})$ be an undirected graph. We have $n$ agents, each agent $i$ starting at $s_i \in \mathcal{V}$ and aiming to reach $g_i \in \mathcal{V}$. Time is discretized into integer steps $t=0,1,2,\dots$. A *makespan* parameter $T$ will limit the maximum number of timesteps we consider; that is, no agent schedule can exceed $t=T$.

#### States and Moves.

An agent's route is described by where it is at each timestep. The classical SAT encoding introduces:

- $\mathbf{X_{i,v,t}}$: a Boolean variable that is `true` if and only if agent $i$ is at vertex $v\in\mathcal{V}$ at time $t$.

- $\mathbf{E_{i,(u\to v),t}}$: a Boolean variable that is `true` if and only if agent $i$ moves from vertex $u$ at time $t$ to vertex $v$ at time $t+1$. Sometimes one allows $(u\to u)$ for a *wait* edge.

#### Sum-of-Costs Tracking.

In order to minimize *sum-of-costs*, we count how many time steps each agent actually uses in its path. A standard approach (see [@surynek2016efficient]) is:

- Compute each agent's shortest path length $d_i$ ignoring other agents (e.g., by BFS/Dijkstra). Let $\xi_0 = \sum_{i=1}^n d_i$. This is a natural *lower bound* on the total cost.

- Allow an extra $\Delta\ge 0$ steps beyond this bound, so any feasible solution must satisfy: $$\text{SoC} \;\; \le\;\; \xi_0 + \Delta.$$

- For each agent $i$, define a Boolean variable $C_{i,t}$ indicating that agent $i$ has *not* yet reached its goal at time $t$, or equivalently is "actively using" the time step $t$. By summing these across all $i,t$, we get the total SoC, and we constrain it to be $\le \xi_0 + \Delta$.

#### Collision Avoidance.

For a collision-free solution:

- $\sum_{i=1}^n X_{i,v,t} \;\le\;1$ for every $v\in\mathcal{V}$ and $t=0,\dots,T$, ensuring no two agents occupy the same vertex at the same time;

- Agents are similarly forbidden to swap edges in opposite directions simultaneously.

#### Flow Consistency.

If $X_{i,u,t}$ is `true`, then agent $i$ must choose exactly one valid move to a neighbor (or stay put) at time $t$: $$X_{i,u,t} \;\Longrightarrow\;
  \sum_{v : (u,v)\in\mathcal{E}\cup\{(u,u)\}} E_{i,(u\to v),t} = 1,$$ with $E_{i,(u\to v),t}$ implying $X_{i,u,t}$ and $X_{i,v,t+1}$. These constraints ensure each agent transitions consistently from one vertex to the next.

##### Toy Example.

:::::::: {#fig:toy-mapf .figure latex-placement="ht"}
::::: minipage
:::: center
::: picture
(100,45) (5,30) (5,13) (40,30) (40,13) (75,30) (75,13) (5,30) (1,0)35 (5,13)(1,0)35 (40,30)(1,0)35 (40,13)(1,0)35 (5,30) (0,-1)17 (40,30)(0,-1)17 (75,30)(0,-1)17

(2,35)(0,0)$A_0$ (37,35)(0,0)$B$ (72,35)(0,0)$C$ (2,8)(0,0)$D$ (37,8)(0,0)$E$ (72,8)(0,0)$F_0$
:::
::::
:::::

::: minipage
**Two Agents**:

- Agent 1: Start $A_0$, Goal $F_0$

- Agent 2: Start $F_0$, Goal $A_0$

All edges can be traveled in 1 time step, or an agent can wait in its current vertex.
:::

::: caption
A toy 2D grid snippet (6 vertices). Agent 1 must go from $A_0$ to $F_0$, while Agent 2 does exactly the reverse. We illustrate $(A_0\leftrightarrow B \leftrightarrow C)$ on top row and $(D\leftrightarrow E \leftrightarrow F_0)$ below. Agents can also move vertically between the top and bottom rows. Note that $A_0$ and $F_0$ are effectively diagonally across.
:::
::::::::

Consider two agents on the small environment of Figure [15](#fig:toy-mapf){reference-type="ref" reference="fig:toy-mapf"}. Agent 1 tries to go from $A_0$ to $F_0$, and agent 2 from $F_0$ to $A_0$. Let $T=4$. We introduce Boolean variables:

$$X_{1,A_0,0}, X_{1,B,0}, \dots, X_{2,E,3}, \dots$$ covering all reachable $(v,t)$ in up to 4 time steps. Then $E_{1,(A_0 \to B),0}$, $E_{2,(F_0 \to E),0}$, etc., record moves. The collision-avoidance constraints forbid $X_{1,B,t}$ and $X_{2,B,t}$ from both being `true` at the same time $t$, among others. If we also choose $\Delta=1$ on top of $\xi_0 = 4$ (assuming each agent's single-agent shortest path is 2 steps, so $\xi_0=4$), then the constraint $$\sum_{i=1}^2 \sum_{t=0}^{3} C_{i,t} \;\le\;1$$ ensures the total cost is $\le 5$. If the solver returns SAT, we decode $X_{i,v,t}$ to see the actual routes (e.g. perhaps each agent waits one step to avoid collisions). If it is UNSAT, we escalate $\Delta$ or $T$ and try again.

This toy example, though small, shows the gist: each agent's presence at each location/time is a Boolean variable, and constraints enforce legality and cost.

### Baseline SAT-Based Algorithm {#sec:baseline}

Algorithm [\[alg:sat-baseline-detailed\]](#alg:sat-baseline-detailed){reference-type="ref" reference="alg:sat-baseline-detailed"} outlines a *baseline* method, adapted from [@surynek2016efficient]. The approach systematically increments $\Delta$ from 0 upwards, setting $\xi = \sum_{i}d_i + \Delta$ and $T = \max_i d_i + \Delta$. For each candidate, we construct a formula $\Phi(\Delta)$ capturing:

- **Agent variables**: $X_{i,v,t}$, $E_{i,(u\to v),t}$, $C_{i,t}$

- **Flow/collision constraints**: ensuring valid single-agent movements and no pair collisions

- **SoC bound**: $\sum_{i,t} C_{i,t} \le \Delta$

The first $\Delta$ for which $\Phi(\Delta)$ is satisfiable yields an SoC-optimal solution.

:::: algorithm
::: algorithmic
$\mathcal{G}=(\mathcal{V},\mathcal{E})$; $n$ agents with $(s_i,g_i)$; integer $\Delta_{\max}$ (optional). **Compute** $d_i = \text{shortestPathLength}(s_i,g_i)$ for each agent $i$. $\xi_{0} \gets \sum_{i=1}^n d_i$; $\mu_{0} \gets \max_{i} d_i$. $\Delta \gets 0$. *// Extra cost budget* $\xi \;\gets\; \xi_0 + \Delta$;$T \;\gets\; \mu_0 + \Delta$. $\Phi(\Delta)\;\gets\; \emptyset$ *// Start building formula* Create variables $X_{i,v,t}$ for $t = 0,\dots,T$, $v\in\mathcal{V}$ (or pruned by reachability). Create variables $E_{i,(u\to v),t}$ for valid edges $(u,v)\in \mathcal{E}\cup\{(u,u)\}$ and $0\le t < T$. Create cost-flag variables $C_{i,t}$ for $0\le t < T$. Add **flow constraints** ensuring consistent motion from $t$ to $t+1$. Add **collision-avoidance constraints** for all pairs $(i,j)$ at each time $t$. Add **SoC bound:** $\sum_{i=1}^n \sum_{t=0}^{T-1} C_{i,t} \;\;\le\;\Delta$. **Run SAT solver** on $\Phi(\Delta)$. **Extract** assignment and decode agent paths from $X_{i,v,t}=\text{true}$.  $\le \xi$. $\Delta \gets \Delta + 1$. [NoSolutionFound]{.smallcaps} // or continue indefinitely
:::
::::

#### Implementation Notes.

- *Incremental SAT solving*: Instead of building $\Phi(\Delta)$ from scratch each time, one can reuse constraints from previous $\Delta$, adding only the new bounding or incremental changes.

- *Pruning unreachable states*: Typically, one prunes spatiotemporal states $(v,t)$ that are obviously unreachable given the agent's start and goal (the MDD idea).

- *Extraction of solution*: A [SAT]{.smallcaps} assignment sets certain $X_{i,v,t}$ to `true`. Reconstructing each agent's path is straightforward by following $E_{i,(u\to v),t}$ from $t=0$ forward.

### Notable Variants of SAT-Based MAPF {#sec:sat:variants}

While the baseline captures the essence of SAT-based MAPF, various refinements yield superior performance or functionality. We summarize five major directions here. Each variant can be thought of as branching from Algorithm [\[alg:sat-baseline-detailed\]](#alg:sat-baseline-detailed){reference-type="ref" reference="alg:sat-baseline-detailed"} with *additions or modifications*, which we highlight in pseudocode.

#### (1) MDD-SAT with Independence Detection

([@surynek2017integration]).

The idea is to *(i) build MDDs* for each agent rather than blindly enumerating all vertices at all $T$ layers and *(ii) detect large sets of agents that cannot collide*, solving them in separate, smaller SAT formulas. If collisions appear across subgroups, they either replan or merge those subgroups. Algorithm [\[alg:mdd-id\]](#alg:mdd-id){reference-type="ref" reference="alg:mdd-id"} sketches the changes from the baseline, with new/modified lines enclosed in .

:::: algorithm
::: algorithmic
$\mathcal{G}=(\mathcal{V},\mathcal{E})$, $n$ agents, start/goal $(s_i,g_i)$ **Initialize groups**: $\text{Groups}\gets\{\{1\},\dots,\{n\}\}$. $\xi \leftarrow \sum_i d_i + \Delta$; $T \leftarrow \max_i d_i + \Delta$; **break** (increase $\Delta$ and retry) **return** solution with SoC $\le\xi$.
:::
::::

#### (2) Suboptimal MDD-SAT Variants

([@surynek2018sub]).

One can trade off solution quality vs. runtime by allowing $\mathrm{SoC} \le w\cdot \mathrm{OPT}$, where $w>1$. The pseudocode mostly resembles the baseline, but we prematurely accept a solution once an SoC within $w\times \xi_0$ is found, or skip certain $\Delta$ steps. Algorithm [\[alg:suboptimal-mdd-sat\]](#alg:suboptimal-mdd-sat){reference-type="ref" reference="alg:suboptimal-mdd-sat"} highlights differences in .

:::: algorithm
::: algorithmic
$\mathcal{G}=(\mathcal{V},\mathcal{E})$, $n$ agents; factor $w\ge 1$. **Compute** $d_i$ for each agent. Let $\xi_0 = \sum_i d_i$. **Set** $\xi_{\text{max}} \leftarrow w\cdot \xi_0$ $\xi \leftarrow \xi_0 + \Delta$; $T \leftarrow \max_i d_i + \Delta$ Build (MDD-based) formula $\Phi(\Delta)$; solve via SAT **Decode solution** with SoC $\le \xi$
:::
::::

In practice, these suboptimal methods often solve large instances much faster, at the cost of a looser cost guarantee.

#### (3) Mutex Propagation {#mutex-propagation}

([@surynek2021mutex]).

Besides collision-avoidance, advanced *mutex* constraints discover deeper conflicts among partial states, forbidding them at the formula level. We incorporate a `mutexCheck` routine (enclosed in ), which after building the baseline constraints, enumerates or propagates *mutually exclusive* states. An example: if $X_{i,u,t}$ and $X_{j,v,t}$ cannot ever appear in the same valid solution due to more intricate reachability conflicts, we add a clause $\neg X_{i,u,t}\lor \neg X_{j,v,t}$ to prune that partial assignment from the solver.

:::: algorithm
::: algorithmic
**Build baseline** formula $\Phi(\Delta)$ as in Algorithm [\[alg:sat-baseline-detailed\]](#alg:sat-baseline-detailed){reference-type="ref" reference="alg:sat-baseline-detailed"}.

1.  
2.  

**Solve** the enriched formula $\Phi(\Delta)$ with a SAT solver.
:::
::::

Experiments show these mutex clauses can dramatically reduce solver overhead.

#### (4) Coupling SoC and Makespan Bounds

([@bartak2019sat]).

Instead of enumerating $\Delta$ alone, @bartak2019sat treat $(T, \xi)$ jointly. They prove that if a solution with $\mathrm{SoC}< \xi$ exists, it can be scheduled within $T \approx \mu_0 + (\xi-\xi_0)$. Hence, they systematically vary $T,\xi$ together. The pseudocode is essentially the baseline, but with a double parameter $(T,C)$ updated in tandem:

:::: algorithm
::: algorithmic
$D_{\mathrm{sum}}\gets \sum_i d_i$, $D_{\mathrm{max}}\gets \max_i d_i$ $\delta \gets 0$ $T \gets D_{\mathrm{max}} + \delta$; $C \gets D_{\mathrm{sum}} + \delta$ Build formula $\Phi(T,C)$ (ensuring each agent ends by time $T$; total cost $\le C$). **SAT-solve** $\Phi(T,C)$ **Return** solution with SoC $\le C$ $\delta \gets \delta + 1$
:::
::::

#### (5) DPLL(MAPF)

([@vcapek2021dpll]).

Finally, a more radical variant integrates MAPF conflict checks *inside* the solver's DPLL/CDCL loop, discovering collisions on partial assignments and learning conflict clauses on-the-fly. The high-level loop is still akin to the baseline, but the SAT engine's internal "*partial MAPF check*" step dynamically prunes collisions. We highlight the changed lines in , focusing on real-time clause additions:

:::: algorithm
::: algorithmic
Build initial formula $\Phi(\Delta)$ *(not necessarily all collision constraints upfront)* **Run DPLL** with partial assignments: **Backtrack** **Assign next literal** in $X_{i,v,t}$ or $E_{i,(u\to v),t}$. solution $\Delta \gets \Delta + 1$
:::
::::

#### Comparison.

1.  *MDD vs. naive expansion*: MDD-based approaches can drastically reduce the formula size, especially for large $T$, by cutting unreachable states.

2.  *Suboptimal vs. optimal:* Permitting suboptimal solutions ($w>1$) can slash runtime at the expense of cost fidelity.

3.  *Mutex propagation & ID:* Aggressively prunes obviously incompatible states/agent groups, often crucial for large instances.

4.  *Coupled bounding:* Linking $T$ and $\xi$ ensures that once satisfiable, the discovered plan is truly SoC-optimal.

5.  *On-the-fly conflict checks (DPLL(MAPF))*: Potentially reduces the solver's search depth by immediately learning collision clauses, but also requires deeper integration with the solver.

Each variant may excel in different scenarios. In dense conflict domains, *independence detection* helps isolate small colliding subsets. In large open grids, bounding $T$ and $\xi$ together can yield early detection of feasible solutions. For extremely large-scale or real-time needs, *suboptimal* strategies may be more practical.

## Satisfiability Modulo Theories (SMT)-Based Methods {#sec:smt}

Satisfiability Modulo Theories (SMT) methods constitute a second major family of *compilation-based* approaches to MAPF, complementing the search-based techniques (Section [3](#sec:search){reference-type="ref" reference="sec:search"}). As discussed in our *Problem Formulation* (Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}), MAPF demands planning collision-free paths for multiple agents on either discrete or continuous representations of the environment. SMT-based methods leverage logical satisfiability enhanced by specialized *theory* solvers (e.g., linear arithmetic, geometry) to handle key constraints such as agent motion, collision avoidance, and objective optimization [@surynek2019multi; @surynek2019multi2; @surynek2020continuous; @surynek2020multi; @surynek2021sum; @surynek2019conflict].

In essence, an SMT-based MAPF solver encodes agent paths, collision constraints, timing requirements, and objective functions as a set of logical clauses augmented with theory-specific formulas. A general SMT solver then searches for a *model* (i.e., an assignment satisfying all clauses) to produce a set of collision-free paths. If the solver finds a collision, or if a solution violates cost bounds, additional "nogood" constraints are iteratively added. These constraints refine the solution space until either a feasible MAPF plan emerges or the problem is shown to be unsatisfiable under the imposed conditions.

### General Mathematical Formulation.

Following our standard MAPF notation in Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}, let $n$ be the number of agents, and let $\mathcal{G}=(\mathcal{V},\mathcal{E})$ be an undirected graph (or a continuous embedding with discretized waypoints). For each agent $i\in\{1,\ldots,n\}$, we define:

- A path variable $\pi_i$ representing a sequence of (vertex, time) or (configuration, time) pairs.

- $\mathrm{Cost}(\pi_i)$ as the travel cost (makespan component if one-shot, or incremental cost if we are optimizing *sum of costs*).

- Additional Boolean or real-valued decision variables, such as $$\begin{aligned}
          X_{t,v}(i) & = \begin{cases}
          \text{true}, & \text{agent $i$ occupies vertex $v$ at time $t$}, \\
          \text{false}, & \text{otherwise};
          \end{cases}\\
          E_{t,u,v}(i) & = \begin{cases}
          \text{true}, & \text{agent $i$ starts traversing edge $(u,v)$ at time $t$},\\
          \text{false}, & \text{otherwise}.
          \end{cases}
      \end{aligned}$$

To accommodate the *continuous-time* setting [@surynek2019multi], some SMT formulations introduce real-valued variables for time indices (rather than enumerating integer steps). The collision-avoidance and objective constraints then become theory clauses in, e.g., linear arithmetic or geometry. In discrete-time or grid-based MAPF, simpler integer arithmetic often suffices [@surynek2022problem].

::: {#def:smt-mapf .definition}
**Definition 1** (SMT-based MAPF Encoding (Generic)). *Let $\Xi$ represent the set of all decision variables encapsulating agent positions, motions, and times. We define $F(\Xi)$ as the collection of logical clauses that enforce:*

1.  **Initial & Goal Feasibility.* Each agent $i$ starts at $s_i$ and must eventually reach $g_i$.*

2.  **Path Consistency.* An agent can only move to adjacent vertices (or valid continuous positions) with correct timing.*

3.  **Collision Avoidance.* No two agents occupy or traverse overlapping regions at the same continuous or discrete time.*

4.  **Cost (Objective) Constraints.* Either the overall makespan or sum of costs is bounded by a target value $\Lambda$. Often enforced through a lazy branch-and-bound style: if a solution contradicts known or guessed $\Lambda$, it is disallowed by extra clauses.*

*A *model* of $F(\Xi)$ that satisfies all clauses (possibly under iterative refinements) corresponds to a set of collision-free agent paths achieving or improving the optimization goal.*
:::

**Core SMT Algorithm.** Algorithm [\[alg:smt-cbs-framework\]](#alg:smt-cbs-framework){reference-type="ref" reference="alg:smt-cbs-framework"} summarizes a prototypical *SMT-based* MAPF solver, which loosely follows the "conflict-based" or "lazy" refinement paradigm proposed by [@surynek2019multi; @surynek2019multi2] and extended in subsequent works [@surynek2020continuous; @surynek2020multi; @surynek2021sum]. In the pseudocode, we assume an objective such as makespan or sum-of-costs is constrained by $\Lambda$, which is progressively tightened or relaxed during the search.

:::: algorithm
::: algorithmic
$\Sigma = (\mathcal{G}, n, \{s_i\}, \{g_i\})$, desired cost bound or optimization target $\Lambda$ A collision-free solution with cost $\leq \Lambda$, or report [Unsatisfiable]{.smallcaps} $\mathit{Constraints} \gets \varnothing \quad \triangleright \text{Initialize extra collision constraints}$ $F(\Xi,\Lambda) \gets \textsc{EncodeBaseFormulation}(\Sigma,\Lambda)$ $\textit{result} \gets \textsc{SMTSolver}(F(\Xi,\Lambda) \cup \mathit{Constraints})$ [Unsatisfiable]{.smallcaps} $\Pi \gets \textsc{extractSolution}(\textit{result})$ $\mathit{collisions} \gets \textsc{validatePaths}(\Pi)$ $\Pi$ *AddDisjunctiveConstraint*($\mathit{collision}$, $\mathit{Constraints}$)
:::
::::

**A Simple Toy Example.** Consider a small graph $\mathcal{G}=(\{v_1,v_2,v_3,v_4\}, \{(v_1,v_2),(v_2,v_3),(v_2,v_4)\})$ where two agents must swap positions: $$\begin{aligned}
    &\text{Agent~1: } s_1 = v_1, \; g_1 = v_4,\\
    &\text{Agent~2: } s_2 = v_3, \; g_2 = v_2.\\
\end{aligned}$$ In a step-based model, we introduce Boolean variables such as $X_{t,v}(1)$ and $X_{t,v}(2)$ indicating which vertex each agent occupies at each time $t$, plus potential edge-traversal variables $E_{t,u,v}(i)$. Initially, we only encode constraints ensuring each agent can follow a path from start to goal. If the solver returns a plan where both agents collide (e.g., if they try to pass through vertex $v_2$ at the same time), we detect that collision through a validation check, and add a *disjunction*: $$\neg X_{t,v_2}(1) \;\vee\;\neg X_{t,v_2}(2),$$ forcing the solver to avoid that specific simultaneous occupation in future attempts. Repeating this refinement leads to a collision-free schedule.

### SMT Variants for MAPF

While the above description outlines the fundamental use of SMT in MAPF, multiple variants have emerged to address specific objectives, environments, and agent capabilities:

**Continuous-Time & Geometric Agents.**

:   Early works, such as [@surynek2019multi; @surynek2019multi2], consider continuous trajectories and geometric overlap (e.g., circular agents in 2D). The solver lazily introduces real-valued time variables and constraints from geometry-based collision checks. These approaches are powerful in capturing uncountably many possible collision instants, although they can face high complexity in large or sparse domains.

**Makespan-Optimal vs. Sum-of-Costs.**

:   SMT encodings also differ by objective. [@surynek2019multi; @surynek2020continuous] focus on minimizing completion time (makespan), introducing incremental bounding on $\Lambda$. In contrast, [@surynek2021sum] extends these encodings to the more challenging *sum-of-costs* objective by adding designations on how waiting times or arrival times accumulate across agents. A solver iteratively refines an upper bound on $\sum_i \mathrm{Cost}(\pi_i)$ until no collision remains or the problem proves infeasible.

**Hybrid Conflict-Resolution Schemes.**

:   Works such as [@surynek2020multi] integrate *Conflict-Based Search (CBS)* with SMT solvers. Instead of classical CBS branching at collisions, the collisions are turned into disjunctive constraints fed back into an SMT loop. The approach capitalizes on the clause-learning capabilities of SMT to prune large swaths of invalid solution space.

**Scalability and Performance.**

:   As reported by [@surynek2019conflict], current SMT methods excel on small- to medium-scale problems, particularly in complex or continuous environments that break typical discrete search heuristics. However, they may struggle on extremely large and sparse domains or with thousands of agents, where simpler decentralized or priority-based methods (Section [3](#sec:search){reference-type="ref" reference="sec:search"}) can be more scalable.

**Illustrative Pseudocode for SMT Variants.** Algorithm [\[alg:smt-sum-costs\]](#alg:smt-sum-costs){reference-type="ref" reference="alg:smt-sum-costs"} outlines a *sum-of-costs* oriented version (motivated by [@surynek2021sum]) that highlights how cost bounding and collision resolution intertwine. New or modified lines from the basic template (Algorithm [\[alg:smt-cbs-framework\]](#alg:smt-cbs-framework){reference-type="ref" reference="alg:smt-cbs-framework"}) are labeled *(\*)*.

:::: algorithm
::: algorithmic
Problem $\Sigma$, initial upper bound on sum-of-costs $\Lambda$, collision constraints $\mathit{Constraints}$ $F(\Xi,\Lambda) \gets \textsc{EncodeBaseFormulation}(\Sigma,\Lambda)$ $\textit{assignment} \gets \textsc{SMTSolver}(F(\Xi,\Lambda)\,\cup\,\mathit{Constraints})$ $\Lambda \gets \Lambda + 1$ *(\*) Increase sum-of-costs bound* **continue** $\Pi \gets \textsc{extractSolution}(\textit{assignment})$ $\mathit{collisions} \gets \textsc{detectCollisions}(\Pi)$ [AddDisjunctiveConstraint]{.smallcaps}(c,$\mathit{Constraints}$) $\Pi$ *(Found feasible solution under current bound)* [AddCostNogood]{.smallcaps}($\Pi$,$\mathit{Constraints}$) *(\*) Forbid this high-cost plan*
:::
::::

### Unified Pseudocode Across SMT Variants {#unified-pseudocode-across-smt-variants .unnumbered}

While Algorithm [\[alg:smt-sum-costs\]](#alg:smt-sum-costs){reference-type="ref" reference="alg:smt-sum-costs"} focuses on the sum-of-costs objective, a variety of SMT-based MAPF methods share a common "collisions-as-constraints" logic. Below, Algorithm [\[alg:unified-smt-var\]](#alg:unified-smt-var){reference-type="ref" reference="alg:unified-smt-var"} illustrates a single compact pseudocode unifying major differences among: 1) **Makespan vs. Sum-of-Costs Objectives**, and 2) **Discrete vs. Continuous Settings**. We encode these differences through parameterized procedures or *conditional lines*, where each variant simply activates the relevant module.

:::: algorithm
::: algorithmic
Problem $\Sigma = (\mathcal{G},\,n,\,\{s_i\},\,\{g_i\})$, ObjectiveType $\in\{\textsc{Makespan}, \textsc{SumOfCosts}\}$, SettingType $\in\{\textsc{Discrete}, \textsc{Continuous}\}$, initial cost/makespan bound $\Lambda$, collision set $\mathit{Colls} \leftarrow \emptyset$ $F(\Xi,\Lambda) \gets \textsc{EncodeBase}(\Sigma,\text{ObjectiveType}, \text{SettingType}, \Lambda)$ $\textit{assignment} \gets \textsc{SMTSolver}(F(\Xi,\Lambda) \,\cup\, \textsc{CollisionConstraints}(\mathit{Colls}))$ [AdjustBound]{.smallcaps}$(\Lambda)$ **continue** $\Pi \gets \textsc{ExtractPaths}(\textit{assignment}, \text{SettingType})$ $\mathit{newColls} \gets \textsc{CheckCollisions}(\Pi, \text{SettingType})$ $\Pi$ [AddCostNogood]{.smallcaps}$(\Pi,F(\Xi,\Lambda))$ [ForbidCollisions]{.smallcaps}$(\mathit{newColls}, F(\Xi,\Lambda))$ $\mathit{Colls} \gets \mathit{Colls} \,\cup\, \mathit{newColls}$
:::
::::

#### Explanation and Comparison.

- **EncodeBase** ($\Sigma,\text{ObjectiveType},\text{SettingType}, \Lambda$): In a [Discrete]{.smallcaps} setting, this subroutine creates Boolean variables $X_{t,v}(i)$ for integer time $t$. In a [Continuous]{.smallcaps} setting, it introduces real-valued times or piecewise-linear motion segments. The objective or constraint on $\Lambda$ is likewise chosen according to [Makespan]{.smallcaps} or [SumOfCosts]{.smallcaps}.

- **CheckCollisions** ($\Pi,\text{SettingType}$): If [Discrete]{.smallcaps}, collisions are time-step conflicts. If [Continuous]{.smallcaps}, we must detect geometric overlap in real-time. Either yields a set of "collision tuples" to be forbidden next iteration.

- **AdjustBound** ($\Lambda$): For [Makespan]{.smallcaps}, we might do $\Lambda \leftarrow \Lambda + 1$. For [SumOfCosts]{.smallcaps}, incrementing can be more nuanced (e.g., bounding total arrival time).

- **AddCostNogood** ($\Pi,F$): Only relevant for sum-of-costs. If $\sum_i \mathrm{Cost}(\pi_i)$ still exceeds $\Lambda$, we forbid that specific combination of time assignments in the SMT formula. In a makespan context, no such line is needed (or it might just forbid solutions longer than $\Lambda$).

Through these modular conditions, a single loop can accommodate different SMT-based MAPF variants. For instance, [@surynek2019multi] and [@surynek2020continuous] use near-identical logic but focus on [Makespan]{.smallcaps} in continuous space; [@surynek2021sum] uses [SumOfCosts]{.smallcaps}; [@surynek2019multi2] and [@surynek2020multi] embed a Conflict-Based Search style branching into the loop, essentially refining collisions as disjunctions. Hence, Algorithm [\[alg:unified-smt-var\]](#alg:unified-smt-var){reference-type="ref" reference="alg:unified-smt-var"} encapsulates their shared pattern: obtaining a candidate plan from an SMT solver, validating it for collisions, and either finalizing the plan or refining constraints to exclude collisions or reduce cost/makespan.

### Discussion and Practical Usage.

SMT-based MAPF methods exemplify a powerful synergy between high-level collision refinement (similar to conflict-based search) and the clause-learning of SAT/SMT solvers. They are particularly appealing when:

- *Continuous time and geometry* play a central role, as direct discretization quickly becomes intractable.

- The problem dimension is moderate, allowing the solver to effectively prune the space of collisions via advanced theory constraints.

- One desires optimal or near-optimal MAPF solutions under complex constraints (e.g., sum-of-costs, multi-criteria routing).

However, these methods often face scalability issues at large agent counts or when the environment is highly sparse and can be tackled more efficiently by specialized heuristics. Still, the continuous-time and geometric formalisms that SMT can handle natively make them an invaluable tool in scenarios unsuited to purely discrete or purely search-based approaches.

In summary, SMT-based MAPF formulations unify classical path feasibility with advanced collision detection and cost-based refinement in a single constraint-solving framework. Subsequent developments have shown that each variant---whether aimed at makespan, sum-of-costs, or continuous-space coverage---substantially broadens the range of solvable MAPF challenges, addressing aspects that classical search-based or purely ILP/SAT-based methods struggle to handle alone.

## Other Compilation-Based Methods {#sec:compilation-other}

In addition to SAT (§[4.1](#sec:compilation-sat){reference-type="ref" reference="sec:compilation-sat"}) and SMT (§[4.2](#sec:smt){reference-type="ref" reference="sec:smt"}) formulations, several other *compilation-based* approaches for Multi-Agent Path Finding (MAPF) have also emerged. This section presents three major classes of such methods: (i) **Constraint Satisfaction Problem (CSP)** encodings, (ii) **Answer Set Programming (ASP)** representations, and (iii) **Mixed-Integer Programming (MIP)** formulations. Each line of work offers a unique perspective on how to encode the MAPF problem into well-established computational frameworks, providing additional flexibility or efficiency gains under certain conditions. We first detail the mathematical modeling (objective, decision variables, and constraints) for each class, then illustrate their core algorithmic pipelines with pseudocode and small toy examples. We conclude by comparing these methods along key dimensions such as scalability, solution quality, and ease of implementation.

### CSP Formulation {#sec:csp}

#### Mathematical Modeling.

In a typical CSP-based approach (see, e.g., [@wang2019new]), one treats each agent as a variable whose *domain* is the set of possible (finite-horizon) paths from $s_i$ to $g_i$. Formally, let $n$ be the number of agents, and let $X_i$ be the CSP variable for agent $i$: $$\text{Var} \;=\; \{X_1, X_2, \dots, X_n\}, 
   \quad
   \text{Dom}(X_i) \;=\; \Bigl\{\pi_i \mid \pi_i \text{ is a path from } s_i \text{ to } g_i \text{ with length} \leq T\Bigr\},$$ where $T$ is a time horizon. The CSP *constraints* enforce collision-avoidance: namely, no two chosen paths conflict. If $\pi_i(t)$ denotes the position of agent $i$ at time $t$ (along path $\pi_i$), then for any pair of agents $i,j$, the constraint $$\bigl(\pi_i(t) \neq \pi_j(t)\bigr) \;\;\wedge\;\; \bigl( (\pi_i(t) \neq \pi_j(t+1)) \vee (\pi_i(t+1) \neq \pi_j(t)) \bigr)$$ ensures that no agents share the same vertex simultaneously or pass each other on the same edge in opposite directions.

Cost objectives (e.g., makespan or sum-of-costs) can be incorporated by searching for a *smallest* $T$ such that the CSP is satisfiable, or by encoding additional constraints/variables tracking how many time steps each agent actually uses before completing its path.

#### Core Algorithm and Pseudocode.

Building on a matrix-based path-counting idea, [@wang2019new] propose a solver that repeatedly: 1) selects the most *constrained* agent (i.e., the one with the fewest feasible paths left), 2) commits to one of its available paths, 3) prunes the path set of other agents to remove newly inflicted collisions, 4) restarts if it becomes impossible to assign further agents.

A high-level sketch follows.

:::: algorithm
::: algorithmic
Graph $G=(V,E)$, agents $A=\{a_1,\dots,a_n\}$ with start/goal $(s_i,g_i)$, horizon $T$, and max restarts $R$. A conflict-free assignment of paths or report failure. $P \leftarrow \emptyset$ $\textsc{Domain}(a_i) \gets \{\text{all length-}\le T\text{ paths from }s_i \text{ to }g_i\}$ $\mathit{conflictFree} \leftarrow \text{true}$ $a^* \gets \operatorname{argmin}_{a_i\text{ unassigned}} \Bigl|\textsc{Domain}(a_i)\Bigr|$ $\mathit{conflictFree} \leftarrow \text{false}$; **break** $\pi^* \gets \textsc{PickOnePath}\bigl(\textsc{Domain}(a^*)\bigr)$ $P \leftarrow P \cup \{(a^*, \pi^*)\}$ $\textsc{UpdateDomains}\bigl(\{\textsc{Domain}(a_i)\}_{i}, \pi^*\bigr)$ $P$ [NoSolutionFound]{.smallcaps}
:::
::::

#### Toy Example and Explanation.

Consider a grid with 4 cells $\{A,B,C,D\}$ arranged in a square, and two agents $a_1$, $a_2$. Suppose $a_1$ must go from $A$ to $D$, and $a_2$ from $C$ to $B$. One enumerates all $T$-step routes for each agent (e.g., $T=3$), then forbids any assignment that yields a direct collision or an edge swap. When picking $a_1$'s path, the solver prunes $a_2$'s domain to remove collisions. This procedure continues until either a complete valid set is found or no feasible assignment remains. Such CSP views can be implemented with off-the-shelf constraint solvers, although they may require specialized heuristics to handle large instances efficiently.

#### Mathematical Note.

While classical CSPs entail purely *discrete* decision variables, one can also embed certain numeric constraints for more refined collision conditions (e.g., partial occupancy of an edge). However, most CSP-based MAPF treatments assume time-discrete steps and single-vertex occupancy constraints, preserving a purely discrete constraint satisfaction framework.

### ASP Formulation {#sec:asp}

#### Modeling and Background.

*Answer Set Programming* (ASP) is a logic-based paradigm suited for complex combinatorial search problems. The MAPF domain is encoded via sets of logical rules specifying agent positions, movement actions, collision avoidance, and cost minimization. A specialized ASP solver then finds *answer sets*---that is, consistent truth-value assignments that satisfy all rules under the stable-model semantics.

In the ASP-based MAPF approach of [@gomez2020solving; @gomez2021compact], the environment is discretized into a grid or directed graph, time steps $t \in \{0,\dots,T\}$, and Boolean predicates: $$\texttt{at}(a,x,y,t), 
   \quad
   \texttt{exec}(a,m,t),
   \quad
   \texttt{cost}(a,t,1),
   \;\dots$$ The sum-of-costs objective is encoded via integer optimization statements in ASP, and the solver incrementally explores increasing makespan values $T$ until a feasible plan emerges. Additional constraints impose that no two agents occupy or swap the same vertex.

#### Formal Encoding Highlights.

Define:

- $\texttt{move}(a,m,t)$: true if agent $a$ executes move $m$ at time $t$.

- $\texttt{reachable}(x,y,t)$: true if cell $(x,y)$ can be occupied at time $t$ by any legal path.

Collision constraints typically appear as linear rules: $$\texttt{:- at}(a,x,y,t),\;\texttt{at}(b,x,y,t),\; a \neq b.$$ ("$\texttt{:-}$" is an ASP notation for stating that this combination is forbidden.) Cost minimization can be expressed through weak constraints $\sim\!\! \texttt{cost}(a,t,1)[1@priority]$, awarding a penalty whenever $\texttt{cost}(a,t,1)$ is true. The ASP solver aims to minimize these penalty sums, effectively capturing sum-of-costs.

#### Pseudocode Structure.

Although ASP solutions are typically not written in procedural style, a top-level algorithm might look like:

:::: algorithm
::: algorithmic
$T_{\text{min}} \;\gets\max_i \bigl(d_i\bigr)$ $\Pi(T) \;\gets\;\textsc{GenerateASPEncoding}(G,A,T)$ *AS* $\gets \textsc{SolveASP}(\Pi(T))$ *BestModel* $\gets$ [GetMinCostModel]{.smallcaps}(*AS*) **return** *BestModel*
:::
::::

#### Toy Example.

Consider two agents in a $3\times2$ grid. A typical ASP snippet could define:

    time(0..T).
    agent(a1; a2).
    pos(0..2, 0..1).  % x in {0,1,2}, y in {0,1}

    at(A, X, Y, 0) :- initial(A, X, Y).
    % Agent can move to next cell if adjacent and not blocked
    at(A, X2, Y2, T+1) :- at(A, X1, Y1, T), exec(A, move(X1,Y1,X2,Y2), T).
    % Collision avoidance
    :- at(A1, X, Y, T), at(A2, X, Y, T), A1 != A2.

plus rules for cost penalties and a final directive to $\#minimize$ the total cost. The solver tries each $T$ in ascending order, stopping when a feasible (and cost-minimal) model emerges.

#### Advantages.

ASP-based encodings can be quite concise and benefit from advanced conflict-driven learning and optimization features of modern ASP solvers like `clingo`. They handle densely constrained scenarios well and allow for linear-sized encodings in terms of agents, as shown in [@gomez2020solving; @gomez2021compact].

### MIP Formulation {#sec:mip}

#### Modeling Rationale.

*Mixed-Integer Programming* (MIP) formulations encode MAPF by enumerating time-expanded flows or by representing each agent's path as a sequence of discrete decisions. The solver then uses linear constraints plus an objective function to enforce conflict-free routing and minimal cost. Advanced branch-and-cut routines prune the search, and *branch-and-price* or *branch-and-cut-and-price (BCP)* can further improve scalability. Notable examples include [@lam2022branch; @lam2023exact].

#### Decision Variables.

One canonical MIP approach introduces a large (though potentially implicit) set of path variables: $$\lambda_{p} \in \{0,1\},$$ indicating whether a particular path $p$ is used by an agent. Let $\mathcal{P}_a$ be all possible paths for agent $a$. Then,

$$\begin{equation}
\begin{aligned}
  \min \qquad & \sum_{a} \sum_{p \in \mathcal{P}_a} c_p \,\lambda_{p}, \\
  \text{s.t.}\quad & \sum_{p \in \mathcal{P}_a} \lambda_{p} = 1, \quad \forall a, \\
                   & \sum_{a} \sum_{p \in \mathcal{P}_a} x^p_v \,\lambda_{p} \;\;\le\; 1, \quad \forall v\in V,\\
                   & \text{(edge conflict constraints)},\;\; \lambda_{p} \in \{0,1\}.
\end{aligned}
\end{equation}$$ Here $c_p$ is the length (or cost) of path $p$, and $x^p_v=1$ if path $p$ visits vertex $v$. Similar definitions exist for edges. An alternative is a direct flow-based MIP with binary $x_{i,v,t}$ variables representing agent $i$'s occupancy at vertex $v$ and time $t$.

#### Core Idea: Branch-and-Cut-and-Price.

Following [@lam2022branch; @lam2023exact], one rarely enumerates all $\mathcal{P}_a$ at once. Instead:

1.  *Column generation (pricing)*: generate new path columns with negative reduced cost by solving single-agent subproblems guided by dual variables.

2.  *Cut separation*: detect collisions in the fractional solution and add linear constraints (cuts) forbidding them in the next re-optimization step.

3.  *Branching*: if the solution remains fractional, pick a branching rule (e.g., forcing an agent to use, or not use, a particular edge) and create child subproblems.

This yields a *BCP* framework that is guaranteed to converge to an optimal integral solution while handling large path sets implicitly.

#### Illustrative Pseudocode.

Algorithm [\[alg:mip\]](#alg:mip){reference-type="ref" reference="alg:mip"} outlines a simplified branch-and-cut-and-price loop.

:::: algorithm
::: algorithmic
**Initialize Master Problem**: no columns, no collision cuts. **Push**(Master Problem) into node queue. $N \gets \textbf{Pop}(\text{node queue})$ **Pricing Step:** For each agent, solve single-agent shortest path with dual-sensitive costs; add any column $p$ with negative reduced cost. **Cut Separation:** Check collisions in the fractional solution; add constraints forbidding these collisions if discovered. Re-solve the LP relaxation. **Branch:** pick a fractional condition, create 2 child nodes **Push** children into node queue
:::
::::

#### Toy Example.

Consider again a $2\times 2$ grid with two agents swapping diagonals. In a column-based MIP, each agent $a$ has a (potentially infinite) set of paths. The dual variables for vertices at each time step raise or lower path costs, guiding the solver to prefer paths that avoid collisions. Collision cuts appear if, for instance, the fractional solution attempts to use a vertex or edge simultaneously across multiple agents. While small grids are easily solved by simpler means, the power of BCP emerges in larger or more intricate domains.

## Comparative Analysis {#sec:comparative}

Compilation-based solvers for MAPF can be broadly organized according to their underlying logical or mathematical framework (e.g., CSP, SAT, SMT, ASP, MIP) and the strategies they employ for conflict resolution (e.g., complete expansion vs. incremental constraint addition). Although they share the common goal of translating MAPF into a declarative formalism handled by general-purpose solvers, subtle differences in modeling choices often lead to varying levels of scalability, solution quality, and ease of implementation. This section synthesizes insights from the preceding discussion, as well as from various recent works [@surynek2019tour; @surynek2021conceptual; @acha2021new], to provide a more unified view of the advantages and drawbacks of each approach.

From a *modeling complexity* perspective, Boolean SAT and ASP formulations often require discretizing agent positions in both space and time, resulting in large but structurally uniform propositional encodings. Works such as [@acha2021new] illustrate how specialized Boolean variables (e.g., shift-based encodings) can streamline representing collision avoidance (notably swap and follow conflicts) and enable conflict-driven clause learning. These streamlined encodings also appear in *SMT-based* approaches, which embed additional theory solvers for linear arithmetic or geometry [@surynek2019tour]. By contrast, *MIP-based* methods [@surynek2021conceptual] rely on linear constraints and integer decision variables to handle collision avoidance and objective functions. While MIP natively captures sum-of-costs or makespan objectives with linear constraints, it requires non-trivial means (often branch-and-cut or branch-and-price) to handle collisions incrementally without enumerating a prohibitive number of path variables. *CSP-based* methods occupy yet another niche, treating possible paths as the domain of agent-specific variables and pruning collisions through constraint propagation.

Regarding *scalability*, purely SAT-based or ASP-based approaches are highly effective on small and medium-size instances, particularly if the environment is dense in agents or obstacles. Their conflict-driven clause-learning (CDCL) mechanisms can prune a combinatorial search space quickly when collisions frequently arise [@acha2021new]. However, as the graph or number of agents grows larger and the state space becomes more sparse, MIP-based or hybrid approaches sometimes outperform pure SAT/ASP due to more flexible branching rules and efficient ways of generating only profitable path columns [@surynek2021conceptual]. SMT-based methods tend to excel when continuous or geometric formulations of MAPF demand sophisticated theory solvers, making them advantageous in robotic applications featuring complex dynamics [@surynek2019tour]. CSP-based designs typically scale well when agent domains (i.e., feasible paths) remain manageable, although they may require careful variable-ordering heuristics to compete with other frameworks.

A *further dimension* of comparison concerns the *degree of conflict resolution* embedded in the solver. In a one-shot encoding (as in classical SAT or MIP expansions), all potential collision constraints may be included upfront, risking very large formulas. By contrast, *incremental or lazy methods* iteratively detect actual collisions in candidate solutions and add new constraints to forbid them [@surynek2019tour; @surynek2021conceptual]. This strategy parallels the logic of Conflict-Based Search (CBS). Indeed, [@surynek2019tour] demonstrates the promise of a DPLL(MAPF) paradigm that refines constraints within the solver loop, mirroring how CBS resolves collisions one by one. Hybrids like SAT/SMT-CBS effectively unify the conflict-resolution strengths of CBS with the clause-learning prowess of SAT/SMT solvers, often achieving competitive results on a wide range of MAPF instances [@gange2019lazy].

Finally, *implementation complexity* and *practical considerations* also play decisive roles. For example, ASP encodings allow concise expression of MAPF rules at the cost of adopting APS- or MaxSAT-specific toolchains [@acha2021new], whereas MIP-based solutions can leverage extensively developed commercial solvers but must handle potential fractional assignments with custom cuts. Similarly, pure SAT approaches enjoy mature, highly optimized CDCL engines but might lack direct means for integrating advanced numeric constraints unless extended to SMT. Each framework can thus be advantageous in different industrial or research contexts, influenced by the size of the instance, the dynamic or continuous nature of the environment, desired optimality guarantees (makespan vs. sum-of-costs), and available solver technologies.

::: sidewaystable
:::

In summary, CSP, SAT, SMT, ASP, and MIP formulations for MAPF embody distinct trade-offs in how they encode agent movement, collisions, and cost functions. Recent work [@surynek2019tour; @surynek2021conceptual; @acha2021new] consolidates these approaches in an increasingly unified view, often adding conflict-refinement mechanisms that resemble CBS at a higher level (or inside the solver itself). While no single framework dominates under all conditions, these compilation-based families collectively showcase how general-purpose solvers---when armed with informed modeling choices---can handle an ever-expanding scope of MAPF problems, from classic grid-based tasks to continuous or high-dimensional coordination challenges.

# Learning-Augmented Classic Solvers {#sec:augmenting}

Building on the classical methods outlined in Sections [3](#sec:search){reference-type="ref" reference="sec:search"} and [4](#sec:compilation){reference-type="ref" reference="sec:compilation"}, a natural evolution is to incorporate learning-based components into well-established MAPF solvers. Rather than discarding decades of research on search-based and compilation-based methods, these approaches seek to *augment* classical pipelines by replacing or supporting specific modules with learned policies or heuristics. The motivation stems from the complementary strengths of each paradigm: while classical solvers offer rigid theoretical guarantees and can often handle a large number of agents, they tend to degrade in performance under real-time constraints or dynamic environments. Learning-based methods, by contrast, excel at adapting to complex, evolving scenarios and can reduce the heavy reliance on human-engineered heuristics, yet often struggle to match the scalability of purely classical techniques when the agent count or environment size becomes large.

:::: {#fig:learning_trend .figure latex-placement="htb!"}
![](Wang2025Where_figs/learning_trend.png){width="\\linewidth"}

::: caption
An evolution diagram of learning-based MAPF algorithms from 2017 to 2024, highlighting five main categories: enhanced CBS, enhanced PBS, enhanced LNS, reinforcement learning, and other learning paradigms.
:::
::::

This hybrid perspective is consistent with the broader direction introduced in Section [1](#sec:intro){reference-type="ref" reference="sec:intro"}, where data-driven methods offer the flexibility to adapt to uncertainties and partial observability, while classical solvers provide efficient frameworks for collision avoidance and optimality guarantees in static or moderately changing environments. From a theoretical standpoint, the interplay between applied optimization frameworks and learned predictors presents fertile ground for rigorous analyses: carefully designed learning modules can *guide or prune* large search spaces, improving computational tractability without sacrificing solution quality.

In the following subsections, we discuss three prominent strands of search-based MAPF solvers that have been augmented by learning-based elements. First, conflict-based methods leverage data-driven conflict resolution strategies to expedite node expansions and reduce search overhead. Second, priority-based methods can benefit from learned priority assignments or adaptive ordering schemes that dynamically resolve agent conflicts. Finally, large neighborhood search techniques incorporate customized learning heuristics to guide neighborhood selection and accelerate solution refinement. These augmented approaches illustrate an emerging shift towards *hybrid MAPF pipelines* that build on the best of both worlds, offering the promise of robust and scalable solutions in increasingly complex multi-agent settings.

## Learning-Augmented Conflict-Based Search (CBS) {#sec:cbs:learning}

Conflict-Based Search (CBS) [@sharon2015conflict] (see Section [3.1](#sec:cbs){reference-type="ref" reference="sec:cbs"}) has long been a standard bearer for solving MAPF optimally under the constraints in [\[eq:cbs:constraints\]](#eq:cbs:constraints){reference-type="eqref" reference="eq:cbs:constraints"}. However, despite notable enhancements to the baseline approach (Section [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"}), CBS can still face significant computational bottlenecks when the environment is highly dynamic or the conflict set is large. Recent work has therefore explored *learning-augmented* CBS, wherein *select modules* of the classical method---for example, node expansion, conflict selection, or heuristic evaluation---are partially *learned* rather than purely hand-coded. The central idea is to maintain CBS's original integer linear constraints and guaranteed collision-avoidance rules, while injecting data-driven insights that accelerate key search operations.

#### Mathematical Formulation.

Much like classical CBS, learning-augmented CBS retains binary variables $$x_{i,v,t} \in \{0,1\}, \quad \forall i,\,v,\,t,$$ with collision-avoidance constraints [\[eq:collision-vertex\]](#eq:collision-vertex){reference-type="eqref" reference="eq:collision-vertex"}--[\[eq:collision-edge\]](#eq:collision-edge){reference-type="eqref" reference="eq:collision-edge"}, and potentially dimensional constraints tailored to SoC or makespan objectives (see Section [3.1.2](#sec:cbs:framework){reference-type="ref" reference="sec:cbs:framework"}). To incorporate learning, one augments the baseline CBS with *auxiliary* parameters $\Theta$ that influence search decisions without altering feasibility. Thus, the feasible solution space remains governed by the same collision-free constraints, yet the *search process* can become more adaptive.

Formally, each high-level (HL) node $N$ in the conflict tree (CT) is characterized by: $$N \;=\; 
   (\{\pi_i\}_{i=1}^n,\; \{\mathrm{constraints}_i\}_{i=1}^n,\; \mathrm{cost}(N)),$$ where $\{\pi_i\}$ are single-agent paths obeying [\[eq:cbs:constraints\]](#eq:cbs:constraints){reference-type="eqref" reference="eq:cbs:constraints"}, and each $\mathrm{constraints}_i$ is a set of time-indexed vertex or edge constraints for agent $i$. In classical CBS, the node expansion order or conflict selection is often driven by manually defined heuristics (e.g., smallest sum of costs, earliest conflict). In learning-augmented CBS, we introduce a learned mapping $$\delta_\Theta: \; N \;\mapsto\; \text{(ranked node/ conflict scoring)},$$ to prioritize expansions or conflict splits based on data-driven predictions (e.g., anticipated search depth, likely feasibility, or future cost). These predictions do *not* relax any constraints but *guide* which branch of the search to explore first.

#### Key Learning-Augmented Modules.

Existing works typically introduce learning in one of the following CBS modules. Below, we highlight parallels to well-known classical refinements from Sections [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"}--[3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"}:

1.  **High-Level Node Selection.** The conflict tree is explored by popping HL nodes from a priority queue. Classical CBS often targets a minimal SoC or uses an admissible heuristic (*e.g.*, conflict-graph-based) [@felner2018adding; @li2019improved; @li2021pairwise]. Learning-augmented approaches (e.g., [@huang2021learning-aamas; @yu2023accelerating; @yao2024accelerating]) replace this manual heuristic with a policy $\delta_\Theta$ that rank-orders nodes by predicted downstream performance. Agents still replan paths via A\* at the low level (or MDD-based searches [@boyarski2015icbs; @li2019symmetry]), ensuring consistency with classical collision avoidance.

2.  **Conflict Selection & Splitting.** When a node $N$ contains multiple pairwise collisions, classical CBS typically branches on the *first detected* conflict or a *cardinal* conflict identified via conflict-graph checks [@felner2018adding; @li2019improved]. A *learning-based* approach may instead predict which collision is most "critical" to resolve, attempting to prune the search tree earlier [@huang2021learning]. Structurally, this is reminiscent of *disjoint splitting* [@li2019disjoint] or *symmetry-breaking* [@li2020new; @li2021pairwise], but with data-driven prioritization.

3.  **Adaptive Algorithm Selection.** A broader *meta-learner* may dynamically choose between different CBS variants (*e.g.*, c.f. Sections [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"}--[3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"} on optimal vs. suboptimal methods) or even between CBS and other MAPF solvers (like SAT or ILP-based methods [@surynek2022problem]). For instance, [@sigurdson2019automatic; @ren2021mapfast; @alkazzi2022mapfaster] use classifiers to identify which solver is likely fastest for a given instance. Once selected, the standard conflict-based constraints remain intact, and the learned module purely handles solver dispatch.

#### Illustrative Pseudocode.

Algorithm [\[alg:learning-cbs\]](#alg:learning-cbs){reference-type="ref" reference="alg:learning-cbs"} compares a minimal learning-augmented CBS (focusing on node selection) to the classical version in Algorithm [\[alg:cbs\]](#alg:cbs){reference-type="ref" reference="alg:cbs"}. Lines enclosed in highlight the data-driven components.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, Agents $\{1,\dots,n\}$, Start/Goal vertices $\{(s_i,g_i)\}_{i=1}^n$, $\delta_\Theta(\cdot)$. Initialize root node $N_0$:

- For each agent $i$, compute $\pi_i$ *ignoring collisions* (standard single-agent A\*).

- Set empty constraint sets for all agents (no additional constraints).

$\mathit{score}(N_0) \gets \delta_\Theta(N_0)$ $N \gets \text{pop front of queue}$ **Check for conflicts** among $\{\pi_i\}_{i=1}^n$ in $N$. $\{\pi_i\}$ (*solution found*) Let $(i, j, t)$ be the according to $\delta_\Theta(N)$ $N' \gets \text{copy of }N$ Add new constraint *forbidding* agent $a$ from $(v,t)$, the conflicting position. Replan $\pi_a$ with standard single-agent pathfinding (respecting new constraints). Insert $N'$ into the queue keyed by $\mathit{score}(N')$ $\emptyset$  (*no feasible solution*)
:::
::::

The crucial distinction is that whereas classical CBS typically expands the node with the *lowest computed cost* or the fewest conflicts, here we use a *learned* function $\delta_\Theta(\cdot)$ to guide expansions, conflict splitting, or both.

#### Comparison to Classical CBS.

Table [\[tab:cbs:compare\]](#tab:cbs:compare){reference-type="ref" reference="tab:cbs:compare"} synthesizes the main differences across four dimensions: HL node expansion, conflict selection, heuristic or priority function, and solver selection. We also reference the enhancements in Section [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"} (for optimal CBS) and Section [3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"} (for suboptimal CBS) to pinpoint how learning-driven modules map onto the older, hand-designed heuristics.

::: sidewaystable
:::

**Relation to CBS Heuristics.** As summarized in Table [\[tab:cbs:compare\]](#tab:cbs:compare){reference-type="ref" reference="tab:cbs:compare"}, classical CBS enhancements (Section [3.2](#sec:cbs:optimal){reference-type="ref" reference="sec:cbs:optimal"}) use carefully engineered heuristics (e.g., conflict-graph cardinality [@felner2018adding] or symmetry constraints [@li2020new; @li2021pairwise]) to reduce the branching factor. A learning-based approach can be viewed as "unifying" or "automating" these heuristic cues under a single parametric model that is *trained* rather than manually designed. For instance, a neural network might implicitly learn to detect frequent corridor conflicts or rectangles, approximating and even extending classical symmetry-breaking.

**Suboptimal CBS vs. Learned Guidance.** Suboptimal CBS variants like ECBS [@barer2014suboptimal], EECBS [@li2021eecbs], and FECBS [@chan2022flex] offer a guaranteed cost bound but prioritize runtime performance. Similarly, a learned node-scorer or conflict selector can be integrated into these frameworks to further accelerate expansions. For example, one can combine the suboptimal factor $w$ with a learned function $\delta_\Theta(\cdot)$, yielding a dual ranking scheme $$f(N) 
   \;=\; 
   \alpha \,\mathrm{Cost}(N) \;+\; \beta\,\delta_\Theta(N),$$ where $\mathrm{Cost}(N)$ might be the focal search cost used by ECBS, and $\delta_\Theta(N)$ is a data-driven priority. By adjusting the weights $\alpha,\beta$, one can retain partial suboptimality guarantees and benefit from learned heuristics' speedups.

#### Discussion and Outlook.

Overall, learning-augmented CBS strives to preserve the strong theoretical underpinnings of conflict-based pathfinding [@sharon2015conflict; @felner2018adding; @li2019improved], while giving the search process more data-driven adaptability. Empirical studies [@huang2021learning-aamas; @yu2023accelerating; @yao2024accelerating] indicate that learning-augmented expansions can considerably reduce runtime in complex or large-scale instances. Moreover, these approaches naturally extend to partially observable or dynamic domains (via online retraining or domain adaptation), where purely hand-designed heuristics may fail to capture all nuance.

Key open challenges include:

1.  **Scalability:** Extending these learning-augmented methods to thousands of agents (see, e.g., [@friedrich2024scalable; @okumura2024engineering]) requires highly efficient inference and robust generalization.

2.  **Guarantees under Heavy Pruning:** If the learned policy prunes nodes aggressively, suboptimal or even incomplete solutions can result. Transparent ways of bounding the search error would improve reliability.

3.  **Handling Non-Stationary Environments:** Many real-world MAPF scenarios involve dynamic obstacle layouts or uncertain agent dynamics [@ren2024multi]. Designing learning-augmented CBS pipelines resilient to such changes is an active area of research.

Nevertheless, *conflict-based modeling* remains central to many state-of-the-art MAPF solvers, and adding learned components only *augments* rather than discards these classical constraints. We thus anticipate further hybrid developments that integrate machine learning with advanced optimal or suboptimal CBS variants (or compilation-based methods) for robust, large-scale multi-agent coordination.

## Learning-Augmented Priority-Based Search (PBS) {#sec:pbs:learning}

#### Motivation and Overview.

Priority-Based Search (PBS) (Section [3.4](#sec:pbs){reference-type="ref" reference="sec:pbs"}) is a fast and popular framework for MAPF, wherein each agent plans its path under the constraint that it must respect the spatial--temporal trajectories of all higher-priority agents. While PBS can be scaled to large numbers of agents with relatively low search overhead, its performance hinges critically on the choice of *priority ordering*, as a poorly chosen order can lead to excessively long paths or even unsolvable collisions in the low-priority subset. Classical PBS relies on manual heuristics or random assignments to finalize this ordering, with no single method dominating in all scenarios.

To address this limitation, *learning-augmented* PBS approaches replace (or guide) the classic *priority assignment* module by leveraging data-driven models. These hybrid pipelines preserve the fundamental *collision constraints* (Eq. [\[eq:pbs:vertex\]](#eq:pbs:vertex){reference-type="eqref" reference="eq:pbs:vertex"}--[\[eq:pbs:edge\]](#eq:pbs:edge){reference-type="eqref" reference="eq:pbs:edge"}) and the general feasibility domain of PBS, but allow a learned predictor to rank or reorder agents in a manner that effectively reduces collisions or enhances solution quality. In addition, learning-based modules may adapt to real-time or dynamic environments where a purely static ordering would be insufficient. Conceptually, these techniques bring PBS closer to the spirit of *learning-augmented CBS* (Section [5.1](#sec:cbs:learning){reference-type="ref" reference="sec:cbs:learning"}), while retaining the simplicity and scalability that have made purely classical PBS appealing.

### Mathematical Formulation and Integration of Learning

Recall from Section [3.4.1](#sec:pbs:modeling){reference-type="ref" reference="sec:pbs:modeling"} that a classical PBS solution is governed by: $$x_{i,v,t}\in\{0,1\}, 
   \quad 
   \text{for all agents } i, \text{ vertices } v, \text{ and times } t,$$ subject to collision-avoidance constraints [\[eq:pbs:constraint\]](#eq:pbs:constraint){reference-type="eqref" reference="eq:pbs:constraint"}. What fundamentally defines a PBS instance is a *function* $$\mathsf{P}: 
      \{1,\dots, n\} 
      \;\rightarrow\; 
      \{1,\dots,n\},$$ which ranks agents from highest to lowest priority (or imposes a partial order in more advanced variants). In *learning-augmented PBS*, we introduce a *parametric* priority function $$\mathsf{P}_\Theta:\;\{1,\dots,n\}\;\mapsto\;\{1,\dots,n\},$$ where $\Theta$ denotes learnable parameters (e.g., weights of a classifier or neural policy). The search and path-finding constraints (Eqs. [\[eq:pbs:vertex\]](#eq:pbs:vertex){reference-type="ref" reference="eq:pbs:vertex"}--[\[eq:pbs:edge\]](#eq:pbs:edge){reference-type="ref" reference="eq:pbs:edge"}) remain unchanged, but instead of a fixed hand-designed $\mathsf{P}$, we compute or update $\mathsf{P}_\Theta$ from data or from online observations: $$\text{When agent $i$ plans its path, it must avoid collisions with each agent $j$ satisfying 
        } \mathsf{P}_\Theta(j) < \mathsf{P}_\Theta(i).$$ The *objective* (e.g., a sum-of-costs or makespan criterion) is also unchanged from the classical setting; the learning module aims to select a priority ordering that typically yields fewer collisions, shorter paths, or a higher success rate.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, Agents $\{1,\dots,n\}$, Start/goal pairs $\{(s_i,g_i)\}_{i=1}^n$, **learned** priority function $\mathsf{P}_\Theta$. **Initialize:**

- $r_i \gets \mathsf{P}_\Theta(i)$.

- Sort agents by $r_i$ in ascending order (lowest $r_i$ means highest priority).

Let $H_i \gets \{\pi_j \mid \mathsf{P}_\Theta(j)<\mathsf{P}_\Theta(i)\}$ paths of *higher-priority* agents Plan $\pi_i$ on a time-expanded graph where all space--time cells used by $H_i$ are forbidden. **return** "*Infeasible under current learned ordering*." **return** $\{\pi_1,\dots,\pi_n\}$ (*valid solution under* $\mathsf{P}_\Theta$)
:::
::::

**Algorithm [\[alg:learning-pbs\]](#alg:learning-pbs){reference-type="ref" reference="alg:learning-pbs"}** outlines a minimal *one-shot* integration of a learned priority function. Like the vanilla version in Algorithm [\[alg:pbs:vanilla-recap\]](#alg:pbs:vanilla-recap){reference-type="ref" reference="alg:pbs:vanilla-recap"}, we perform a single pass from highest to lowest priority. However, the order itself now comes from a predictor $\mathsf{P}_\Theta$. In principle:

1.  *Offline Training.* One can train $\Theta$ (e.g., via supervised learning or evolutionary search) on a corpus of MAPF instances, where the "label" or "reward" might measure how well an ordering reduces the sum of costs or yields fewer collisions.

2.  *Online Updating.* In dynamic environments or repeated tasks, $\mathsf{P}_\Theta$ can be re-evaluated each time new start/goal locations arrive or environmental conditions change, thereby adapting priorities in real time.

### Representative Learning Approaches

#### SVM- and Evolutionary-Based Prioritization.

@zhang2022learning propose a *support vector machine* (SVM) model to predict a promising ordering of agents, aiming to reduce collisions and hence overall solution cost. They show performance gains by incorporating *stochastic restarts* and *random rank perturbations* during planning to avoid local optima under a single ordering. Similarly, @wang2023synthesizing adopt a *genetic algorithm* (GA) to evolve priority functions, treating permutations or partial orders of agents as candidate "genomes." Offspring that yield fewer collisions or lower sum-of-costs are selected, gradually improving the learned priority scheme over multiple generations.

#### Reinforcement Learning and Attention Mechanisms.

@yang2024attention present a *hybrid* approach that couples PBS with a reinforcement learning (RL) policy. Instead of a fixed one-shot assignment, their method uses a *Synthetic Score-based Attention Network* to assign conflict-free priorities in a more dynamic fashion, learning from trial-and-error interactions in a multi-agent environment. The attention mechanism processes local agent states (positions, goals, conflicts) to generate situational *priority scores* online, which effectively reorder planning so as to reduce bottlenecks.

#### Integration with Dynamic PBS Variants.

Beyond the *vanilla* single-pass algorithm, advanced PBS frameworks (e.g., dynamic priority inheritance [@okumura2022priority], partial-order branching [@ma2019searching], or merging [@boyarski2022merging]) can similarly embed learned components. In such cases, $\mathsf{P}_\Theta$ might re-rank agents at each collision, or a *learning-based policy* might decide which agents to merge. These expansions mirror the ideas seen in learning-augmented CBS (Section [5.1](#sec:cbs:learning){reference-type="ref" reference="sec:cbs:learning"}), underscoring a broader strategy of *augmenting classical submodules*---instead of discarding them entirely.

### Discussion and Outlook

Learning-augmented PBS exemplifies the central theme of *hybridizing* classical MAPF solvers with data-driven models: it preserves the fundamental constraints of priority-based planning (Eq. [\[eq:pbs:constraint\]](#eq:pbs:constraint){reference-type="ref" reference="eq:pbs:constraint"}) while injecting a learned module $\mathsf{P}_\Theta$ to *strategically* shape the planning order. Experiments suggest that such combinations can reduce the reliance on ad-hoc heuristics, improve success rates in congested or dynamic environments, and more gracefully scale when domain parameters shift.

Important open challenges parallel those seen in learning-augmented CBS and other MAPF methods:

- **Generalization and Scalability.** Learned priority assignments may fail to extrapolate well to agent populations much larger than those seen in training or to drastically different topologies.

- **Robustness in Real-World Deployments.** In environments where sensors, communication, or agent dynamics are uncertain, how can $\mathsf{P}_\Theta$ adapt priorities online without causing deadlocks or collisions?

- **Hybrid *vs.* Fully Data-Driven.** While partial learning preserves classical PBS properties, future work may explore fully RL-based multi-agent frameworks that derive both collision-avoidance rules and priorities from large dataset pretraining, aligning with *foundation models* [@alkazzi2024comprehensive] discussed in Section [7](#sec:others){reference-type="ref" reference="sec:others"}.

Overall, learning-augmented PBS forms a promising middle ground: it capitalizes on decades of heuristic wisdom in priority-based planning, while employing machine learning to handle the notoriously difficult *priority ordering* problem. As multi-agent applications continue to grow in scale and complexity, such hybrid pipelines will likely become increasingly relevant, especially when classical PBS alone struggles to meet real-time or adaptive demands.

## Learning-Augmented Large Neighborhood Search {#sec:lns:learning}

Large Neighborhood Search (LNS) methods (Section [3.5](#sec:lns){reference-type="ref" reference="sec:lns"}) provide a suboptimal yet scalable framework for MAPF by iteratively "destroying" and "repairing" subsets of a global solution. Whereas classical LNS approaches rely on handcrafted heuristics to select which agents to remove (*destroy*) and how to replan these agents (*repair*), *learning-augmented LNS* seeks to replace or assist these modules with data-driven policies. Such hybrid designs exploit the original mathematical formulation and collision-avoidance constraints of classical LNS-based MAPF (Equations [\[eq:lns-vertex\]](#eq:lns-vertex){reference-type="eqref" reference="eq:lns-vertex"}--[\[eq:lns-edge\]](#eq:lns-edge){reference-type="eqref" reference="eq:lns-edge"}), while introducing learned components to guide destructive and reparative decisions.

#### Mathematical Model.

We recall that LNS solutions for MAPF maintain a global set of trajectories $\{\pi_i\}_{i=1}^n$, one path per agent, and impose vertex- and edge-collision constraints: $$\begin{align}
&\text{\emph{(vertex constraint)}} 
&&x_{i,v,t} + x_{j,v,t} \;\le\; 1,
\quad \forall\,t,\, \forall\,v\in \mathcal{V}, \,\forall\,i<j, \label{eq:lns-vertex-recap}\\
&\text{\emph{(edge constraint)}} 
&&x_{i,u,t} + x_{i,v,t+1} + x_{j,v,t} + x_{j,u,t+1} \;\le\; 3,\quad
\forall\,(u,v)\in \mathcal{E}, \,\forall\,t,\,\forall\,i<j,
\label{eq:lns-edge-recap}
\end{align}$$ where $x_{i,v,t}$ is a binary decision variable indicating whether agent $i$ is at vertex $v$ at time $t$. The *objective* (e.g., makespan [\[eq:makespan\]](#eq:makespan){reference-type="eqref" reference="eq:makespan"} or SoC [\[eq:soc\]](#eq:soc){reference-type="eqref" reference="eq:soc"}) and the fundamental set of collision-free feasibility constraints remain unchanged from the classical setup. In learning-augmented LNS, one introduces additional *auxiliary* variables or a learned function $\delta_\Theta$ that steers the *destroy* and *repair* steps externally to these collision-avoidance constraints: $$\delta_\Theta: (\{\pi_i\}, \mathcal{G}, \textit{other contextual data}) \;\;\mapsto\; 
   (\text{choice of agents/paths to destroy}, \text{replanning strategy}).$$ Because $\delta_\Theta$ is not part of the core feasibility constraints [\[eq:lns-vertex-recap\]](#eq:lns-vertex-recap){reference-type="eqref" reference="eq:lns-vertex-recap"}--[\[eq:lns-edge-recap\]](#eq:lns-edge-recap){reference-type="eqref" reference="eq:lns-edge-recap"}, it neither invalidates collision-free guarantees nor changes the set of admissible solutions; rather, it *guides* which partial solutions are explored and how.

#### From Classical to Learning-Augmented LNS.

The classical LNS scheme (Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"}) iterates between (i) randomly or heuristically *destroying* a subset of agent paths and (ii) *repairing* them using a local solver. In a learning-augmented approach, these two steps are partially or wholly driven by data-driven policies. Concretely:

- *Learning-Based Destroy.* Instead of removing agents uniformly at random or solely by collision frequency, one estimates which agents or spatial regions offer the greatest potential improvement if re-optimized. For instance, a learned policy $\delta_\Theta^{\text{destroy}}$ might identify "high-conflict" agents or time intervals that frequently cause deadlocks, thereby focusing the LNS loop on eliminating these problematic collisions more efficiently.

- *Learning-Based Repair.* During the *repair* step, a learned module $\delta_\Theta^{\text{repair}}$ can provide either (i) cost-effective single-agent trajectories that consider a learned heuristic beyond classical A\*, or (ii) partial multi-agent solutions via reinforcement learning. The same global feasibility constraints ([\[eq:lns-vertex-recap\]](#eq:lns-vertex-recap){reference-type="ref" reference="eq:lns-vertex-recap"})--([\[eq:lns-edge-recap\]](#eq:lns-edge-recap){reference-type="ref" reference="eq:lns-edge-recap"}) still apply; however, the planner can benefit from data-driven intuition regarding which paths are likely to reduce collisions or improve objectives.

As a result, learning-augmented LNS typically shares the *same* collision-avoidance model and objective function as classical LNS, but replaces handcrafted heuristics in the destroy-repair loop with parametric (e.g., neural) policies that can adapt to instance-specific features.

#### Example: LNS2+RL.

Recent work by @{wang2024lns2+} proposes an LNS-based solver that integrates a multi-agent reinforcement learning (MARL) module into classical LNS2 [@li2022mapf]. Initial iterations prioritize a MARL-based low-level *repair* to explore diverse path allocations, as MARL can discover geometric or collision patterns that standard shortest-path routines overlook. Later in the LNS cycles, the method switches to a priority-based re-planner (similar to suboptimal MAPF solvers in Section [4](#sec:compilation){reference-type="ref" reference="sec:compilation"} and Section [3.3](#sec:cbs:suboptimal){reference-type="ref" reference="sec:cbs:suboptimal"}), accelerating convergence by leveraging simpler heuristics in conflict-free subregions. Hence, LNS2+RL employs the same collision-prevention constraints as classical LNS2, but adaptively invokes a learned policy to *repair* agent paths early on, then falls back to more efficient classical updates once major conflicts are resolved. Empirical results indicate that this blended approach outperforms naive LNS2 or purely learning-based approaches in both solution quality and runtime, especially as the number of agents increases.

:::: algorithm
::: algorithmic
Graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, agents $\{1,\dots,n\}$, start/goal vertices $\{(s_i,g_i)\}_{i=1}^n$, destroy ratio $\gamma$, max iterations $K$, learned policy $\delta_\Theta$ for (destroy, repair). **Initialize** a feasible solution $S_0 = \{\pi_i^{(0)}\}$ using classical single-agent heuristics or a separate solver. $S_{\mathrm{current}} \gets S_0;$ $S_{\mathrm{best}} \gets S_0$ **Destroy Step:** Identify a subset of agents $\mathcal{D}$ via $\delta_\Theta^{\text{destroy}}\bigl(S_{\mathrm{current}}\bigr)$ (size $\approx \gamma n$). Remove $\pi_i$ for each $i\!\in\!\mathcal{D}$, yielding partial solution $S^{\mathrm{partial}}$. **Repair Step:** For each $i\in \mathcal{D}$, compute a new path $\hat{\pi}_i$ with $\delta_\Theta^{\text{repair}}\bigl(S^{\mathrm{partial}},\mathcal{G}\bigr)$ subject to collision constraints ([\[eq:lns-vertex-recap\]](#eq:lns-vertex-recap){reference-type="ref" reference="eq:lns-vertex-recap"})--([\[eq:lns-edge-recap\]](#eq:lns-edge-recap){reference-type="ref" reference="eq:lns-edge-recap"}). Merge these new paths into $S' = S^{\mathrm{partial}} \cup \{\hat{\pi}_i: i\in\mathcal{D}\}$. $S_{\mathrm{best}} \gets S'$ $S_{\mathrm{current}} \gets \textsc{AcceptanceCriterion}\bigl(S_{\mathrm{current}}, S'\bigr)$ $S_{\mathrm{best}}$
:::
::::

#### Illustrative Algorithm.

Algorithm [\[alg:lns-learning\]](#alg:lns-learning){reference-type="ref" reference="alg:lns-learning"} outlines a generic learning-augmented LNS procedure. Compared to the baseline procedure (Algorithm [\[alg:lns\]](#alg:lns){reference-type="ref" reference="alg:lns"}), the difference lies in Lines 5--6 (learning-based destroy) and Lines 7--8 (learning-based repair). One may also allow $\delta_\Theta$ to interact with an external classical solver, *e.g.*, switching from reinforcement learning to priority-based re-planning after a certain number of iterations.

#### Discussion and Outlook.

Learning-augmented LNS underscores the broader synergy between *classical MAPF constraints* (which guarantee collision-free doctrines) and *data-driven search guidance* (which reduces reliance on hand-engineered heuristics). By leveraging modern machine learning, one gains the ability to:

- **Adapt to Complex Environments or Partial Observability.** Learned destroy-repair policies can generalize from past experience and re-optimize quickly in changing or uncertain scenarios.

- **Reduce Search Overhead.** Targeting high-impact agents or collisions can significantly prune the solution space.

- **Maintain Transparency of Constraints.** Since the core collision-avoidance model remains identical to that in classical LNS, correctness and feasiblity are preserved.

Nevertheless, learning-augmented LNS also faces practical challenges. Data collection and policy training can be nontrivial, especially for large numbers of agents [@friedrich2024scalable; @okumura2024engineering], and guaranteeing suboptimality bounds may require careful integration of classical cost metrics [@li2022mapf; @lam2023exact]. Despite these open questions, the convergence of LNS meta-heuristics and data-driven modules represents a promising path forward, balancing adaptive intelligence with well-established optimization principles.

# Reinforcement Learning for MAPF {#sec:rl}

Reinforcement learning (RL) offers a promising framework for tackling MAPF under decentralized decision-making and partial observability. A general algorithmic flowchart for solving the MAPF problem using RL is shown in Figure [17](#fig:rl){reference-type="ref" reference="fig:rl"}. In contrast to purely classical methods, RL-based approaches allow each agent to learn collision-free navigation and coordination policies in a data-driven manner, adapting to complex or dynamic environments. Nevertheless, bridging these learning ideas with MAPF requires carefully defined states, actions, rewards, collision-avoidance mechanisms, and inter-agent communication protocols. This section provides a comprehensive presentation of how RL can model and solve MAPF, offering mathematical formulations, explanations of popular multi-agent RL (MARL) paradigms, and a critical review of remaining challenges.

## Mathematical Modeling of RL-based MAPF {#subsec:rl_modeling}

#### MDP Definition.

In an RL-based MAPF framework, agent $i$ (where $i\in\{1,\dots,n\}$) is typically governed by a Markov Decision Process (MDP) $$\bigl\langle 
    \mathcal{S}^i,\,   
    \mathcal{A}^i,\,
    p(\cdot\mid \cdot),\,
    r^i,\,
    \gamma 
\bigr\rangle,$$ where:

- $\mathcal{S}^i$ denotes the (local) state space for agent $i$, which may include partial environment observations, neighbor information, or heuristic guidance.

- $\mathcal{A}^i$ is the action space (e.g., $\{\textit{up}, \textit{down}, \textit{left}, \textit{right}, \textit{stay}\}$ in grid worlds).

- $p(\cdot\mid\cdot)$ is the transition probability function. In deterministic map-based settings, it might simplify to $s^i_{t+1}=f(s^i_t,a^i_t)$.

- $r^i:\mathcal{S}^i\times \mathcal{A}^i\rightarrow \mathbb{R}$ is an individual reward function (discussed in Section [6.4](#subsec:reward_design){reference-type="ref" reference="subsec:reward_design"}).

- $\gamma\in[0,1)$ is the discount factor for future rewards.

The goal of each agent is to learn a policy $\pi^i:\mathcal{S}^i\to \Delta(\mathcal{A}^i)$ (a probability distribution over actions) that maximizes the expected discounted return: $$\begin{equation}
\label{eq:rl-objective}
\pi^{i,*} 
~\in~
\arg \max_{\pi^i}
\mathbb{E}\biggl\{
\sum_{t=0}^\infty 
\gamma^t \, r^i\bigl(s_t^i,a_t^i\bigr)
\biggr\}.
\end{equation}$$

#### Collision-Avoidance Constraints.

Since MAPF requires collision-free paths, collisions must be integrated into the RL formulation either as *soft constraints* (negative rewards) or *hard constraints* (invalid actions). For example, an agent may receive a large penalty $-\alpha \,(<0)$ upon attempting to occupy a vertex already claimed by another agent or upon traversing an edge in an opposite direction at the same time. In large-scale MAPF instances, these collision penalties or constraints can drastically affect how the agent explores the environment during training.

:::: {#fig:rl .figure latex-placement="htb!"}
![](Wang2025Where_figs/rl.png){width="\\linewidth"}

::: caption
A general algorithmic flowchart for solving the MAPF problem using reinforcement learning. The process begins with various types of observations, including local, global, dynamic, historical, and expert-guided information. These observations are processed in the feature extraction stage, which involves convolutional layers and inter-agent communication. The extracted features are then passed to the policy network. The next steps include action execution and reward collection, followed by storing the experience in a replay buffer and generating new observations.
:::
::::

## State and Observation Spaces {#subsec:rl_state_space}

In many MAPF setups, each agent can observe only part of the environment, such as its limited field of view (FOV). Consequently, the agent's local state often contains only a subset of the global map. Table [4](#tab:rl-state-spaces){reference-type="ref" reference="tab:rl-state-spaces"} details four common categories of observation. Each category can be used individually or in combination, depending on the complexity of the environment and the level of guidance needed.

::: {#tab:rl-state-spaces}
  **Category**              **Information Examples**                                             **Remarks**
  ------------------------- -------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *Local static info*       Map obstacles, free cells in $W_{\text{FOV}}\times H_{\text{FOV}}$   Provides a local occupancy grid around the agent, enabling immediate collision detection or obstacle avoidance [@feng2024multi; @chen2023transformer].
  *Expert path guidance*    Recommended route from a classical solver (A\*, D\* Lite, etc.)      Helps agents avoid getting lost in large or complex maps by providing explicit routing suggestions; drastically reduces RL sample complexity and training time [@liu2020mapper; @tang2024ensembling].
  *Dynamic neighbor info*   Positions, velocities, or trajectories of nearby agents              Enhances multi-agent collision avoidance by providing situational awareness of other agents in dense or dynamic settings [@he2024alpha; @wang2020mobile].
  *Heuristic embedding*     Distance-to-goal, action feasibility, direction hints                Gives agents a flexible sense of goal orientation (e.g., whether moving up brings them closer to the goal), combining classical heuristics with RL's adaptive exploration [@ma2021learning; @song2023helsa; @lin2023sacha].

  : Representative State (Observation) Partitioning in RL-based MAPF. Each category of state information contributes differently to collision avoidance and goal reaching.
:::

**Additional Discussion for Table [4](#tab:rl-state-spaces){reference-type="ref" reference="tab:rl-state-spaces"}.**

- *Local static information.* This is often the minimum requirement in RL-based MAPF. Although it helps agents avoid immediate collisions, it may be insufficient for discovering long-horizon routes in large grids or environments with multiple bottlenecks.

- *Expert path guidance.* This allows each agent to receive suggestions from offline planners such as A\* or D\* Lite. By following or at least referencing these suggestions, agents reduce random exploration and can reach near-optimal routes more quickly.

- *Dynamic neighbor information.* Sharing real-time positions or velocities of other agents is crucial in high-density scenarios; it permits emergent cooperative behavior in RL, such as implicit priority or yield policies at intersections.

- *Heuristic embedding.* Instead of giving a single recommended path, some works prefer more general heuristic signals (e.g., Manhattan distance to goal). Agents then need to learn how to balance these heuristics with real-time local constraints and potential collisions.

## Action Spaces {#subsec:action_space}

On a 2D grid, an agent typically has five actions $\{\textit{up}, \textit{down}, \textit{left}, \textit{right}, \textit{stay}\}$. In continuous domains (e.g., a nonholonomic robot in a 2D plane), the agent might select continuous velocities or steering commands, requiring continuous-action RL algorithms such as DDPG or TD3. When collisions are treated as hard constraints, an action that immediately causes a collision may be invalid. Alternatively, collisions can be penalized via large negative rewards (Section [6.4](#subsec:reward_design){reference-type="ref" reference="subsec:reward_design"}), disincentivizing agents from selecting dangerous maneuvers.

## Reward Design {#subsec:reward_design}

Reward design is one of the most critical components of RL-based MAPF, balancing collision avoidance, efficiency, and multi-agent cooperation. Table [5](#tab:rl-reward-structures){reference-type="ref" reference="tab:rl-reward-structures"} lists typical reward components, each focusing on different aspects of the MAPF objective. In practice, these rewards can be combined or weighted to form a single scalar signal.

::: {#tab:rl-reward-structures}
  **Reward Type**     **Mathematical Formulation**                                                              **Explanations/References**
  ------------------- ----------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Goal-reaching       $r^i_{\text{goal}}(s_t^i,a_t^i)                                                           Rewards the agent upon reaching its designated goal $g_i$. $R_G>0$ is usually large to maximize success; a small penalty $-\varepsilon$ encourages shorter paths [@yin2024deep].
                          =                                                                                     
                          \begin{cases}                                                                         
                          +R_{G}, & \!\!\text{if }s_t^i=g_i \\                                                  
                          -\varepsilon, & \!\!\text{otherwise}                                                  
                          \end{cases}$                                                                          
  Cooperation         $r^i_{\text{coop}}(s_t^i,a_t^i)                                                           Balances individual progress $r^i_{\text{indv}}$ with a shared team incentive $r_{\text{team}}$. Encourages global success rather than local selfish behavior [@zhao2023curriculum; @tao2024poaql].
                          =                                                                                     
                          \beta_1 \,r^i_{\text{indv}} + \beta_2\, r_{\text{team}}$                              
  Expert-guided       $r^i_{\text{guide}}                                                                       Provides a positive reward $R_E>0$ for following a reference path (e.g., from A\*) to reduce trial-and-error exploration [@liu2020mapper; @wang2020mobile; @Pham2023OptimizingCM].
                          =                                                                                     
                          \begin{cases}                                                                         
                          +R_{E}, & \!\!\text{if action \(\in$expert path                                       
  Collision penalty   $r^i_{\text{collision}}(s_t^i,a_t^i)=-\alpha\,\mathbb{I}\{\text{collision at time }t\}$   Strongly penalizes collisions ($-\alpha$), deterring agents from occupying the same cell or crossing edges simultaneously [@qiu2020multi].

  : Common Reward Structures in RL-based MAPF. Multiple components are often combined to guide agents effectively in large or dynamic environments.
:::

**Additional Discussion for Table [5](#tab:rl-reward-structures){reference-type="ref" reference="tab:rl-reward-structures"}.**

- *Goal-reaching.* A common approach is to give a large positive reward only when the agent arrives at its target. Some variants also provide a small shaping reward for moving closer to the goal each step, improving learning speed but risking unintended local optima.

- *Cooperation.* A purely local or per-agent reward may lead to greedy strategies. By adding a group-oriented term $r_{\text{team}}$, methods encourage agents to coordinate, reducing deadlocks or cycles.

- *Expert-guided.* For difficult or sparse environments, referencing a path from classical planners (e.g., A\*) significantly reduces RL training time. Approaches differ in how strictly they guide: some apply partial or decreasing weighting of the expert path.

- *Collision penalty.* Typically, collisions incur a large negative reward to override other incentives. Alternatively, collisions may terminate the episode for the colliding agents, which also conveys a strong penalty signal.

## Communication Protocols in RL-based MAPF {#subsec:comm}

Communication protocols determine how partial observations are shared among agents to improve collective decision-making. Table [6](#tab:comm-rl){reference-type="ref" reference="tab:comm-rl"} summarizes representative methods. Each approach modifies the local state $s^i_t$, integrating the messages or states received from neighbors.

::: {#tab:comm-rl}
  **Type**                **Example Methods**        **Scalability**   **Further Details / References**
  ----------------------- -------------------------- ----------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *Non-communication*     Local only                 High              Each agent relies entirely on its local information; collisions are avoided via local RL rules. Feasible if agents are sparse or environments are simple [@chen2023transformer; @qiu2020multi].
  *Basic communication*   Message exchange           Moderate          Agents broadcast raw or summarized states (via GNNs) to neighbors, enabling more effective conflict resolution [@Pham2023OptimizingCM].
  *Priority-based*        Select top-$k$ neighbors   Moderate          Agents communicate only with the most relevant neighbors (e.g., highest conflict potential) to reduce bandwidth [@ye2022multi; @li2022multi].
  *Attention-based*       Graph or Transformer       Moderate          Agents weigh neighbors by attention mechanisms (e.g., BicNet, Graph Attention) to focus on the most critical relationships [@guan2022ab; @bignoli2021graph].
  *Request-response*      On-demand triggers         High              Agents broadcast or request info only when a neighbor's action might influence their decision, limiting unnecessary messages [@ma2021learning; @zhou2024dhaa].

  : Communication Mechanisms in Reinforcement Learning-based MAPF. Each approach modifies how local states $s^i_t$ are constructed, thereby affecting coordination quality.
:::

**Additional Discussion for Table [6](#tab:comm-rl){reference-type="ref" reference="tab:comm-rl"}.**

- *Non-communication.* Approaches with no inter-agent communication are typically easier to scale to many agents and ensure faster training, but they may lead to more collisions in dense areas.

- *Basic communication.* Agents may broadcast local states or partial observations to all neighbors within a certain radius. Social conventions (e.g., "move right if in conflict") can emerge, but the overhead of repeated broadcasts can be high.

- *Priority-based communication.* By allowing each agent to communicate only with those neighbors deemed "most critical," networks avoid saturating communications. Various metrics (e.g., distance, possible collisions in the next steps) can establish these priorities.

- *Attention-based communication.* Derived from modern deep learning architectures like Transformers, attention weighting helps each agent filter crucial messages. This is particularly helpful in scenarios with many neighbors.

- *Request-response communication.* Agents solicit updates from others only when critical. This specialized approach can greatly reduce bandwidth consumption while preserving coordination, though it often requires more intricate logic at each agent.

## Overview of MARL Algorithms for MAPF {#subsec:rl_algorithms}

In single-agent RL, each agent $i$ independently learns $\pi^i$ to maximize ([\[eq:rl-objective\]](#eq:rl-objective){reference-type="ref" reference="eq:rl-objective"}). However, the multi-agent setting introduces nonstationarity (since other agents are also learning) and partial observability. Below, we summarize popular multi-agent RL (MARL) paradigms and give short mathematical explanations so that MAPF practitioners can link them to classical MAPF solution concepts.

### Independent Learning

Each agent $i$ runs a single-agent RL algorithm (e.g., DQN, PPO) treating all other agents as part of the environment. Though simple to implement, independent learners may converge slowly or fail to coordinate in dense MAPF scenarios. The agent's Bellman update for action-value $Q^i$ is: $$Q^i_{t+1}(s_t^i,a_t^i)
\;\leftarrow\;
Q^i_t(s_t^i,a_t^i)
\;+\;
\eta \Bigl[
r^i_t 
  + \gamma\,\max_{a'}\,Q^i_t(s_{t+1}^i,a')
  - Q^i_t(s_t^i,a_t^i)
\Bigr].$$

### Centralized Training, Decentralized Execution (CTDE)

CTDE offers a more structured approach: $$Q_{\text{CT}}(s,a_1,\dots,a_n)
\;\; \text{with} \;\;
s = \bigl(s^1,\dots,s^n\bigr).$$ During training, a *centralized critic* has access to global states, actions, and possibly even agent IDs or goals. Once the critic $Q_{\text{CT}}$ is optimized, each agent executes a decentralized policy $\pi^i$ that conditions only on $s^i$. For instance, MADDPG uses a deterministic policy in continuous spaces: $$a^i = \mu^i_{\theta^i}(s^i),$$ while the critic $Q_{\Phi}$ is centralized: $$Q_{\Phi}(\mathbf{s},a_1,\dots,a_n)
= 
\mathbb{E}\Bigl[
r + \gamma \max_{a'} Q_{\Phi}(\mathbf{s}',a'_1,\dots,a'_n)
\Bigr].$$ This improves coordination while preserving decentralized execution essential for MAPF solutions.

### Value Decomposition Methods

For a team reward $r_{\text{team}}(\mathbf{s},\mathbf{a})$, value decomposition networks (VDN) [@sunehag2018value] and QMIX [@rashid2020monotonic] factorize the global action-value function into per-agent utilities, making the training feasible even if we have a single shared objective. For instance, VDN enforces: $$Q_{\text{VDN}}(\mathbf{s},\mathbf{a}) 
= 
\sum_i Q^i(s^i,a^i),$$ while QMIX uses a monotonic mixing network: $$Q_{\text{QMIX}}(\mathbf{s},\mathbf{a})
=
f_{\text{mix}}\bigl(Q^1,\dots,Q^n;\,\mathbf{s}\bigr)\quad\text{with monotonic partial derivatives.}$$ These methods are relevant when MAPF tasks optimize a global criterion (sum-of-costs or makespan). They can converge faster to coordinated solutions than purely independent methods.

## Representative Implementations

Various MAPF studies integrate the above MARL techniques with specialized domain knowledge, such as neighbor-based collision checks or expert guidance. For example, [@Pham2023OptimizingCM] adopt a CTDE paradigm combined with graph neural networks (GNNs) for large warehouse pathfinding. [@ma2021learning] incorporate a QMIX-based approach where agents share a team reward, encouraging them to resolve conflicts cooperatively. These examples demonstrate how general MARL architectures (e.g., independent RL, CTDE, value decomposition) can be customized and scaled for multi-agent pathfinding.

## Summary and Future Directions {#subsec:rl_summary_future}

Reinforcement learning has opened new avenues for MAPF, especially in decentralized control or partially observable, dynamic environments. However, its application is far from trivial. Table [7](#tab:rl-limitations-solutions){reference-type="ref" reference="tab:rl-limitations-solutions"} summarizes some key limitations and highlights prospective solutions from the RL/MARL community.

::: {#tab:rl-limitations-solutions}
+----------------------------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| **RL-based MAPF Challenge**      | **Current Limitation**                                            | **Possible RL/MARL Solutions**                                                            |
+:=================================+:==================================================================+:==========================================================================================+
| *Scalability to large $n$*       | Communication overhead and an exponential joint state space       | - Hierarchical RL for multi-level decisions.                                              |
|                                  |                                                                   |                                                                                           |
|                                  |                                                                   | - Graph-based message passing with priority or attention.                                 |
|                                  |                                                                   |                                                                                           |
|                                  |                                                                   | - Value decomposition for factorized learning.                                            |
+----------------------------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| *Lack of theoretical guarantees* | No formal completeness or suboptimality bounds                    | - Safe RL (e.g., barrier functions, constrained MDPs).                                    |
|                                  |                                                                   |                                                                                           |
|                                  |                                                                   | - Hybrid frameworks with classical MAPF back-ends.                                        |
+----------------------------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| *Reward shaping complexity*      | Difficult to encode global MAPF objectives into local rewards     | - CTDE with a global critic that tracks collective performance.                           |
|                                  |                                                                   |                                                                                           |
|                                  |                                                                   | - Potential-based shaping to integrate classical heuristics.                              |
+----------------------------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| *Partial observability*          | Agents are myopic, may cause collisions due to hidden areas       | - Recurrent policies or memory-based MARL.                                                |
|                                  |                                                                   |                                                                                           |
|                                  |                                                                   | - On-demand or selective communication protocols.                                         |
+----------------------------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| *Real-world complexity*          | Uncertainties in dynamics, sensor noise, or kinematic constraints | - Domain randomization or sim-to-real transfer to improve robustness.                     |
|                                  |                                                                   |                                                                                           |
|                                  |                                                                   | - Multi-fidelity simulation frameworks that gradually incorporate real-world constraints. |
+----------------------------------+-------------------------------------------------------------------+-------------------------------------------------------------------------------------------+

: Open Challenges of RL-based MAPF and Potential Research Avenues. Each challenge connects to broader RL/MARL directions, offering new opportunities for MAPF practitioners.
:::

**Additional Discussion for Table [7](#tab:rl-limitations-solutions){reference-type="ref" reference="tab:rl-limitations-solutions"}.**

- *Scalability.* Each agent's learning complexity grows quickly as $n$ increases. Approaches that factorize value or adopt hierarchical structures (e.g., assigning subgoals or clusters of agents) can help manage complexity.

- *Lack of theoretical guarantees.* Unlike classical MAPF, which can guarantee completeness or near-optimality under certain conditions, pure RL solutions lack formal proofs of collision-free motion. Integrating safe RL constraints or combining RL with classical verification tools remains an open area.

- *Reward shaping complexity.* Designing rewards that encourage local progress but also ensure global success is nontrivial. Methods like potential-based shaping or difference rewards (which remove "baseline" contributions of other agents) can better align local and global goals.

- *Partial observability.* Many realistic MAPF scenarios restrict an agent's viewpoint. Memory-augmented RL (e.g., LSTM-based policies) or advanced communication schemes can mitigate some pitfalls of partial observations, but solutions remain highly domain-specific.

- *Real-world complexity.* MAPF tasks in actual robotic deployments require robust solutions to handle agent dynamics, sensor noise, nonholonomic constraints, and cluttered or changing environments. Domain randomization and sim-to-real strategies can partially mitigate these challenges, but bridging the gap between simulation and reality is far from solved.

Overall, RL-based MAPF solutions capitalize on data-driven adaptivity, offering a unique advantage in dynamic or partially known settings. Future research can continue to refine these methods, balancing learning efficiency, communication strategies, and theoretical safety to achieve robust, scalable performance in real-world multi-agent coordination.

## Beyond Grid-World: More Advanced Environments {#subsec:advanced_envs}

While much of the existing reinforcement learning (RL) research on MAPF (see Section [6](#sec:rl){reference-type="ref" reference="sec:rl"}) focuses on two-dimensional grid worlds, real-world applications often depart markedly from this simplified model. These departures include embedding agents in 3D spaces (e.g., autonomous drones), allowing for continuous-valued states and actions, or imposing time-varying obstacles in dynamic environments. Moreover, certain real-world infrastructures---such as railway networks---require graph-based topology and additional motion constraints. This subsection reviews these non-traditional MAPF environments with an eye toward the mathematical modeling that aligns with Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}'s general MAPF framework.

### Mathematical Formulation Across Environments

To unify different environment types, we recall from Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"} that classical MAPF is modeled by a graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$. Below, we highlight the mathematical variations for each environment category. Table [\[tab:env-types\]](#tab:env-types){reference-type="ref" reference="tab:env-types"} provides a concise comparison.

::: sidewaystable
:::

#### State and Transition Functions.

For grid or 3D lattice environments, agent positions typically remain on discrete vertices, with transitions governed by adjacency. By contrast, continuous-space formulations let each agent $i$ maintain a position $\mathbf{x}_i(t)\in \Omega\subseteq \mathbb{R}^{d}$. The environment then defines transition dynamics: $$\mathbf{x}_i(t + 1)
= 
\mathbf{x}_i(t) 
\;+\; 
\Delta t \cdot \mathbf{u}_i(t),$$ or more complex non-linear motion constraints $\dot{\mathbf{x}}_{i} = f_{i}(\mathbf{x}_i,\mathbf{u}_i)$. For dynamic variants, the set of permissible states or edges can evolve each timestep. In an RL setting, each agent's local observation must capture these changes, either through dynamic occupancy grids [@xie2024improved] or sensor measurements [@qiu2020multi].

#### Action Spaces.

In discrete graphs (2D or 3D), each agent's action space $\mathcal{A}^i$ corresponds to stepping into an adjacent vertex if no collision occurs. For continuous domains, $\mathcal{A}^i$ may be a continuous set (forces, velocities, turning angles), as reported in [@liu2024multi-agent; @fan2020distributed], or discretized approximations for safe flight corridors in drone applications [@zhiyao2020deep]. Graph-based transit systems (e.g., railways) often require specialized "movement rules," disallowing direct transitions outside the track network [@mohanty2020flatland].

#### Reward and Constraints.

Regardless of dimensionality, RL-based methods frequently penalize collisions and reward reaching goals quickly. However, certain tasks (e.g., multi-train scheduling) incorporate *hard safety constraints* or even higher-level scheduling costs (e.g., lateness penalties). In dynamic environments, time-varying elements factor into collisions: $$\begin{equation}
\label{eq:dynamic-collision}
\mathbb{I}\bigl\{\mathbf{x}_i(t)\in \phi_{\text{obs}}(t)\bigr\},
\end{equation}$$ where $\phi_{\text{obs}}(t)$ denotes the region of newly introduced obstacles at time $t$. Such expansions demand specialized RL reward structures (Table [5](#tab:rl-reward-structures){reference-type="ref" reference="tab:rl-reward-structures"} in Section [6.4](#subsec:reward_design){reference-type="ref" reference="subsec:reward_design"}) and can be augmented by communication-based strategies (Table [6](#tab:comm-rl){reference-type="ref" reference="tab:comm-rl"} in Section [6.5](#subsec:comm){reference-type="ref" reference="subsec:comm"}).

#### Implications for RL.

Moving beyond grid-worlds often increases state and action dimensionality, intensifies partial observability, and requires advanced exploration or communication protocols. Effective RL policies may integrate local sensor data (continuous domains) or specialized heuristics/communication to handle dynamic graphs. Approaches such as hierarchical RL or centralized training [@Pham2023OptimizingCM] become especially relevant for environments with higher complexity.

### Case Studies of Advanced Environments

#### 3D UAV Coordination.

In [@zhiyao2020deep], the authors extend 2D PRIMAL to a 3D search space called *PRIMALc*. Agents model future conflict states by exchanging predicted actions, effectively building a communication channel. From a mathematical viewpoint, each agent $i$'s state is $\mathbf{x}_i(t)=(x_i,y_i,z_i)$, and collisions are enforced by $\|\mathbf{x}_i(t) - \mathbf{x}_j(t)\|_{2} \ge \delta$ for any $j \neq i$. Using careful reward shaping and gradient clipping stabilizes the imitation loss, yielding stable flight coordination among UAVs in a partially observable environment.

#### Continuous Robot Navigation.

@liu2024multi-agent formulate each robot's action as a continuous force vector, capturing underlying physical dynamics. Let $\mathbf{u}_i(t)\in \mathbb{R}^2$ be the planar force, and agent $i$'s dynamics follow $$m \,\ddot{\mathbf{x}}_i(t) 
= 
\mathbf{u}_i(t),$$ where $m$ is mass. Their RL training penalizes collisions and encourages minimal path length in continuous space. Similarly, @qiu2020multi [@fan2020distributed] map sensor observations to continuous velocity or steering actions and verify collision-avoidance in real or simulated prototypes.

#### Graph-Based Railway Scheduling.

In the automated train scheduling context [@mohanty2020flatland; @van2021time], trains follow track networks represented by a directed graph $\mathcal{G}=(\mathcal{V}, \mathcal{E})$. Each vertex $v \in \mathcal{V}$ can hold at most one train (or a limited capacity of trains), and each edge imposes travel-time constraints. RL-based methods must coordinate schedules at each switch junction (vertex), using a multi-agent policy that respects collision-free track occupancy.

#### Dynamic Obstacle Handling.

Dynamic MAPF (DMAPF) extends the standard setup by continuously altering obstacle configurations. @xie2024improved introduce a random process with probability $p_o$ adding or removing obstacles. In RL terms, the agent's local state includes a dynamic occupancy grid, and the RL update must incorporate time-varying feasible sets and collision checks as in Eq. [\[eq:dynamic-collision\]](#eq:dynamic-collision){reference-type="eqref" reference="eq:dynamic-collision"}. Similarly, @ou2024reinforcement propose GAR-CoNav, where graph attention networks process changing environmental features, guiding multi-agent navigation with minimal real-time collisions. Such dynamic setups highlight the demand for real-time, adaptive RL policies.

**Summary.** While discrete 2D grid worlds remain an invaluable starting point for RL-based MAPF, advanced environments---3D cells, continuous domains, specialized graphs, and dynamic obstacles---better reflect real-world scenarios but also pose higher computational complexity, stricter collision constraints, and more involved communication requirements. High-performing methods typically blend domain knowledge (e.g., sensor usage, specialized collisions checks) with advanced RL strategies (hierarchical or GNN-based).

## Beyond One-Shot Tasks: Lifelong Learning {#subsec:lifelong}

In the classical MAPF setting, each agent is assigned a single start and goal location (one-shot task). Once an agent reaches its goal, it no longer partakes in further planning, effectively halting the problem. However, many real-world applications (e.g., large-scale warehouses, delivery fleets) follow an *ongoing* or *lifelong* mode, where agents must be re-tasked repeatedly with new objectives. This difference in problem setup impacts system-level metrics such as throughput, computation frequency, and scheduling. Here, we first distinguish mathematically between one-shot and lifelong MAPF and then discuss representative RL solutions that handle repeated re-planning.

### Mathematical Formulation: One-Shot vs. Lifelong

Recall from Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"} that in a one-shot MAPF, each agent $i$ has a start vertex $s_i$ and a goal vertex $g_i$. The solution typically seeks to minimize makespan [\[eq:makespan\]](#eq:makespan){reference-type="eqref" reference="eq:makespan"} or sum-of-costs [\[eq:soc\]](#eq:soc){reference-type="eqref" reference="eq:soc"}, subject to collision-free constraints. In contrast, *lifelong MAPF (LMAPF)* assigns agent $i$ a *sequence* of goals, $\{g_{i}^1,g_{i}^2,\dots\}$, with possibly only the next target known at each step. Denote by $T_i$ the set of tasks for agent $i$, where task $j$ is $(s_{i}^j,g_{i}^j,\tau_i^j)$ specifying an origin, destination, and the time $\tau_i^j$ at which the goal is announced (if known in advance). The RL agent faces a repeated (or continual) planning scenario: $$\min_{\{\pi_i\}_{i=1}^n}
\; 
\sum_{j} \mathrm{Cost}(\pi_i^j) 
\quad
\text{subject to collision-free constraints across all tasks.}$$ Moreover, some approaches aim to maximize throughput or the average number of completed tasks per unit time: $$\begin{equation}
\label{eq:lifelong-obj}
\max_{\{\pi_i\}} 
\;\;
\frac{\sum_{i=1}^n \text{TasksCompleted}_i(\{\pi_i\})}{T_{\text{horizon}}}.
\end{equation}$$ The environment can also be partially observable or dynamic (Section [6.9](#subsec:advanced_envs){reference-type="ref" reference="subsec:advanced_envs"}). Table [8](#tab:one-shot-lifelong){reference-type="ref" reference="tab:one-shot-lifelong"} summarizes the conceptual and mathematical distinctions between one-shot and lifelong tasks.

::: {#tab:one-shot-lifelong}
                        **One-Shot MAPF**                                                  **Lifelong MAPF**
  --------------------- ------------------------------------------------------------------ -----------------------------------------------------------------------------------------------------------
  **Goal Set**          Static $\bigl(s_i \to g_i\bigr)$, single assignment                Sequential $\bigl(s_i \to g_i^1 \to g_i^2 \dots\bigr)$; possibly indefinite
  **Objective**         Minimize makespan or sum-of-costs for one final solution           Minimize cumulative cost over repeated tasks or maximize throughput
  **Policy**            Terminal once $g_i$ is reached                                     Continuous re-planning; new tasks appear dynamically
  **RL Implication**    Single-episode design; fewer exploration phases                    Multi-episode or indefinite horizon; RL must adapt to new tasks
  **Example Methods**   Conflict-based or compilation-based solutions for fixed instance   PRIMAL2 [@damani2021primal], Re-planning modules [@chen2023towards], Priority-based methods [@gao2024pce]

  : Comparison of One-Shot vs. Lifelong MAPF in Terms of Key Variables and Incentives.
:::

### Representative RL-Based Approaches

#### PRIMAL2 for Dense Warehouses.

@damani2021primal extend the PRIMAL approach to *PRIMAL2*, targeting local, fully decentralized policies for agents that repeatedly receive new tasks in constrained and partially observable environments. The RL module is structured to handle real-time pathfinding as tasks arrive, with each agent $i$ maintaining a policy $\pi^i$, refined to adapt to dynamic reassignments $(s_i^j,g_i^j)$. Training includes reshaping local observations, so that each new subtask is seamlessly integrated into the agent's partial view.

#### Re-planning Modules in Hybrid RL.

@chen2023towards propose a *Re-planning Module* that merges classical path planners with RL. Once an agent finishes a task, the module re-invokes a local or global RL-based solver to assign and plan for the next task. This pipeline ensures that partial solutions from past tasks can quickly adapt to new goals. From an MDP perspective, the state now tracks not only the agent's current position but also the *progress* (or idle time) since the last assignment.

#### Priority-Aware Communication & Lifelong Scheduling.

@gao2024pce present a *Priority-aware Communication & Experience replay* subroutine (PCE) suited for repeated tasks. In each re-planning phase, the system reassigns tasks to idle agents, and a priority-based communication ensures minimal collisions among active missions. This approach unifies ongoing scheduling decisions with standard RL updates, enabling robust performance over extended horizons.

### Challenges and Open Directions in Lifelong MAPF

Adopting a lifelong viewpoint introduces additional complexities not found in single-shot tasks:

- *Frequent Re-planning.* Agents continually switch goals, requiring fast, incremental RL updates or real-time inference.

- *Scheduling Coupling.* At high agent densities (e.g., warehouses), the scheduling of new tasks can create bottlenecks, so RL must balance finishing old tasks quickly with preparing for new ones.

- *State Explosion.* Each agent's MDP must encode which task it is pursuing, local environment states, and partial observations. This might be mitigated by hierarchical RL or modular sub-polices (one per task type).

- *Performance Metrics.* While sum-of-costs or makespan suffices for one-shot tasks, repeated assignment may require throughput ([\[eq:lifelong-obj\]](#eq:lifelong-obj){reference-type="ref" reference="eq:lifelong-obj"}) or time-averaged productivity measures akin to those used in queueing theory.

**Summary.** Switching from a one-shot perspective to lifelong MAPF captures the continuous nature of real-world operations, demanding greater adaptability from RL-based approaches. Agents must repeatedly plan while ensuring minimal collisions and high throughput. Recent works (e.g., PRIMAL2 [@damani2021primal], [@chen2023towards; @gao2024pce; @matsui2023investigation; @ma2017lifelong; @skrynnik2024learn]) exemplify how multi-agent RL can handle indefinite sequences of tasks, but the field remains open for more sophisticated scheduling policies, dynamic communication schemes, and advanced reward shaping tailored to high-throughput, multi-round settings.

::: table*
:::

# Other Learning Paradigms {#sec:others}

In addition to the reinforcement learning (RL) strategies described in Section [6](#sec:rl){reference-type="ref" reference="sec:rl"}, a variety of other learning-based paradigms have emerged for multi-agent path finding (MAPF). These paradigms treat MAPF as a sequential decision-making or prediction problem, often integrating with the classical MAPF formulation in Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"} by re-defining objectives, constraints, or feasible sets. Unlike purely RL-based methods, which directly learn a policy from trial-and-error interactions, the approaches discussed here can leverage expert demonstrations, heuristic expansions, population-based search, or hybrid search-learning loops. This section provides a structured survey of four major categories of learning paradigms: (i) Monte Carlo Tree Search, (ii) Supervised Learning, (iii) Composite Learning Strategies, and (iv) Evolutionary Methods. We highlight how each method formally maps the standard MAPF constraints (e.g., collision-avoidance) onto distinct optimization variables and search processes.

**Roadmap for this Section.** Table [\[tab:paradigm-comparison\]](#tab:paradigm-comparison){reference-type="ref" reference="tab:paradigm-comparison"} offers a broad comparison of the mathematical modeling and typical constraints across these learning paradigms. Subsequent subsections provide deeper discussion and references for each approach.

::: sidewaystable
:::

## Monte Carlo Tree Search (MCTS) {#subsec:mcts}

Monte Carlo Tree Search (MCTS) is a general-purpose sampling-based planning algorithm widely used in sequential decision making. Although it is often categorized under *model-based* reinforcement learning, MCTS can be integrated into MAPF solvers in ways that differ from typical RL pipelines. A flowchart of solving the MAPF problem using MCTS is shown in Figure [18](#fig:mcts){reference-type="ref" reference="fig:mcts"}. This subsection provides a concise mathematical view of MCTS in the context of MAPF and highlights representative works that incorporate MCTS for collision avoidance.

:::: {#fig:mcts .figure latex-placement="htb!"}
![](Wang2025Where_figs/mcts.png){width="\\linewidth"}

::: caption
A flowchart of solving the MAPF problem using Monte Carlo Tree Search (MCTS). The tree structure represents each agent's action as a separate node, reducing the branching factor in multi-agent settings. The diagram illustrates the four stages of MCTS: (a) Selection -- choosing actions based on the current state; (b) Expansion -- adding new nodes for possible actions; (c) Simulation -- simulating outcomes using a default policy; and (d) Backpropagation -- updating the tree with computed rewards. Agents and goals are shown on a grid as solid and hollow circles, respectively, with dashed-line actions excluded during selection.
:::
::::

### Mathematical Modeling of MCTS for MAPF

Recall from Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"} that each agent $i$ has a start vertex $s_i\in\mathcal{V}$ and a goal $g_i\in\mathcal{V}$. We may treat joint MAPF states $\mathbf{s}=(s^1,\dots,s^n)$ and define a tree-based search over feasible joint actions $\mathbf{a}=(a^1,\dots,a^n)$, each of which corresponds to a proposed movement in the shared graph $\mathcal{G}$. At each node in the MCTS tree: $$(\text{State})\quad \mathbf{s}_t \;\longmapsto\; (\text{Children})\quad \{\mathbf{s}_{t+1}\}$$ feasible next states are derived by applying valid joint actions. During MCTS, one typically runs four main steps:

#### 1) Selection:

Select a path from the root to a leaf by choosing actions that balance exploitation (high-value actions) and exploration (less-visited actions). A common strategy is the Upper Confidence Bound for Trees (UCT): $$\begin{equation}
\label{eq:uct}
a^* 
=\;
\arg \max_{a \in \mathcal{A}}
\Bigl[
Q(\mathbf{s},a) 
\;+\; 
c \sqrt{
\frac{\ln \bigl(\sum_{b}N(\mathbf{s},b)\bigr)}{N(\mathbf{s},a)}
}
\Bigr],
\end{equation}$$ where $Q(\mathbf{s},a)$ is the estimated action value, $N(\mathbf{s},a)$ is the visit count, and $c$ is an exploration constant.

#### 2) Expansion:

Once a leaf node is reached, new child states are added to the tree by enumerating feasible subsequent joint actions. In MAPF, expansions must check collision constraints: $$\mathbf{s}_{\text{child}} 
\;\in\;
\Bigl\{
\mathbf{s}_{\text{leaf}} + \mathbf{a} 
\;\mid\;
\text{no collision among }\{a^1,\dots,a^n\}
\Bigr\}.$$

#### 3) Simulation:

From the newly expanded node, random or heuristic-based rollouts simulate the agent movements until a terminal state is reached (e.g., all agents arrive at their goals, or a collision occurs). A scalar payoff $R_{\text{rollout}}$ is then computed, often penalizing collisions or incomplete paths.

#### 4) Backpropagation:

Propagate the rollout returns $R_{\text{rollout}}$ upwards to update $Q(\mathbf{s},a)$ along the selection path. Subsequent MCTS iterations refine these value estimates.

### Applications in MAPF

MCTS-based MAPF approaches vary by how they incorporate collision penalties and domain heuristics:

**Conflict-Avoidance with Rollout Patches.** [@skrynnik2021hybrid] employ Proximal Policy Optimization (PPO) to learn path-planning behaviors and then use MCTS expansions for collision resolution. The MCTS simulation step focuses on detecting conflicts quickly, effectively patching local collisions before committing to a joint action in the real environment. Similarly, [@pitanov2023monte] propose a specialized MCTS variant, guiding agents to avoid collisions via local partial plans.

**Decentralized MCTS.** [@skrynnik2024decentralized] adapt MCTS to a multi-agent decentralized setting in a lifelong MAPF scenario, where each agent runs a local MCTS with partial observations and limited communication. They incorporate a rolling horizon scheme: each agent simultaneously expands possible paths for a short horizon, merges local expansions with neighbor observations, and replans as needed.

**Multi-step Tree Search for Subgoal Allocation.** [@zhang2020learning] propose multi-step ahead tree search (MATS), which extends MCTS rollouts over multi-discrete state expansions. This helps in partial observability, where each agent infers likely collisions from neighbor expansions. The resulting MATS method yields robust collision avoidance in dense grid maps.

### Advantages and Limitations

MCTS ensures systematic exploration of the joint decision tree, offering interpretable expansions of feasible MAPF states. However, the branching factor can be large if each agent can move freely; classical MCTS expansions may thus become computationally expensive with many agents. Heuristic or learned rollouts are crucial to managing complexity in large-scale MAPF.

## Supervised Learning {#subsec:supervised}

Supervised learning (SL) leverages datasets of *expert demonstrations* or *labeled solutions* to train a predictive model (e.g., a neural network) that outputs recommended actions or paths for MAPF. In this sense, SL attempts to *approximate* a collision-free solver's behavior without performing an explicit search at inference time. A supervised learning framework for solving the MAPF problem is shown in Figure [19](#fig:supervised){reference-type="ref" reference="fig:supervised"}. This subsection covers two main SL-based approaches: *assisting classical solvers* and *direct solution predictions*.

:::: {#fig:supervised .figure latex-placement="htb!"}
![](Wang2025Where_figs/supervised.png){width="\\linewidth"}

::: caption
A supervised learning framework for solving the MAPF problem. The process includes four main stages: (1) Dataset generation -- using expert algorithms to compute optimal paths on a given grid; (2) Preprocessing -- extracting local observations for each agent; (3) Feature processing -- applying convolutional encoders and graph neural networks for multi-hop communication, followed by MLP-based policy output; and (4) Training -- using expert actions to supervise learning. This process is repeated across multiple agents and time steps.
:::
::::

### Mathematical Formulation of SL-based MAPF

In supervised MAPF, we typically assume a labeled dataset $\mathcal{D}=\{(\mathbf{x}_k,\mathbf{y}_k)\}_{k=1}^M$, where: $$\mathbf{x}_k \;=\; \text{map features, agent positions, obstacles, \ldots},$$ $$\mathbf{y}_k \;=\; \text{expert next actions or entire agent paths from a known solver}.$$ The learning objective is to fit model parameters $\theta$ (e.g., in a neural network) that minimize a prediction loss: $$\begin{equation}
\label{eq:SL-obj}
\theta^*
\;=\;
\arg \min_\theta
\sum_{k=1}^M
\mathcal{L}\bigl(f_\theta(\mathbf{x}_k),\, \mathbf{y}_k\bigr).
\end{equation}$$ Once trained, $f_\theta$ can produce near-instant path recommendations. Collision avoidance is implicit, learned from the collision-free labels $\mathbf{y}_k$.

### Assisting Existing Solvers

**Large Neighborhood Search (LNS) Guidance.** When integrated with LNS-based MAPF solvers (Section [3](#sec:search){reference-type="ref" reference="sec:search"}), SL can guide the selection of agent subsets to be re-optimized:

- [@huang2022anytime] train a Support Vector Machine (SVM) to rank promising subsets of agents for neighborhood destruction.

- [@yan2024neural] propose a CNN-attention architecture to guide LNS expansions.

The new selection rule replaces hand-crafted heuristics, often yielding faster or higher-quality solutions.

**Solver Selection.** [@zapata2024anytime] train an XGBoost classifier to choose the most suitable classical solver (e.g., CBS vs. priority-based methods) given input features (graph size, agent density, time limit). This meta-learning approach attempts to quickly pick an appropriate solver for each MAPF instance.

### Direct Solution Methods

**Imitation from CBS or A\*.** A popular strategy is *imitation learning* from classical MAPF solutions: $$\begin{align}
\text{Given } \{\pi^*_i\}_{i=1}^n &\;\; \text{(expert paths from CBS or A*)}, \notag \\
\theta^* 
&=\;
\arg\min_\theta
\sum_i 
\sum_{\text{states } s_t^i} 
\mathcal{L}\Bigl(
f_\theta\bigl(\mathrm{Enc}(s_t^i)\bigr),
a_t^*\Bigr),
\label{eq:il-loss}
\end{align}$$ where $a^*_t$ is the expert action label at time $t$, and $\mathrm{Enc}(s_t^i)$ denotes some encoding of the agent's local observation or map neighborhood.

Examples include:

- **CTRMs** [@okumura2022ctrms]: The authors introduce Cooperative Timed Roadmaps to focus on *critical positions* for collision-free navigation, imitating CBS solutions.

- **MAGAT** [@li2021message]: A graph-attention-based model where each agent processes messages from neighbors and imitates paths computed by Enhanced Conflict-Based Search (ECBS).

- **CNN-GNN Integrations** [@li2023multi; @bignoli2021graph]: These works embed 2D grid observations via CNN and then apply GNN layers to coordinate multi-robot collision avoidance, training the entire model to mimic an expert solver's next-step guidance.

### Pros and Cons of SL-based MAPF

Once trained, SL inference is typically very fast (sub-millisecond for moderate-scale networks), making it attractive for large or time-critical scenarios. However, generalization can degrade when new environments differ significantly from the training set. Moreover, pure SL does not guarantee *optimality* or even feasibility in out-of-distribution cases. Hence, many authors propose *hybrid* strategies (e.g., re-checking solutions with a classical solver or incorporating online collision checks) to ensure consistent results.

## Composite Learning Strategies {#subsec:composite}

:::: {#fig:composition .figure latex-placement="htb!"}
![](Wang2025Where_figs/composition.png){width="60%"}

::: caption
A set of four sub-flowcharts illustrating different hybrid approaches to solving the MAPF problem. The combinations include: (1) RL + Imitation Learning -- training by switching between expert and RL policies to generate actions; (2) RL + Curriculum Learning -- using a scheduler to gradually increase task difficulty; (3) RL + Evolutionary Algorithms -- enabling agents to imitate better-performing peers; and (4) Pure Evolutionary Algorithm -- agents execute diverse policies, replicate successful ones, and update or discard underperforming strategies.
:::
::::

Composite learning strategies integrate multiple learning paradigms---for example, combining imitation learning with RL or leveraging progressive curriculum tasks. Such hybrids often seize the advantages of each technique (e.g., fast policy convergence from imitation learning, robust exploration from RL) while mitigating their individual limitations (e.g., poor generalization of imitation learning alone). A set of four sub-flowcharts illustrating different hybrid approaches to solving the MAPF problem is shown in Figure [20](#fig:composition){reference-type="ref" reference="fig:composition"}.

### Imitation Learning (IL) + Reinforcement Learning (RL)

Imitation learning in MAPF leverages expert trajectories to *bootstrap* agent policies. Formally, agents begin by minimizing an IL loss such as [\[eq:il-loss\]](#eq:il-loss){reference-type="eqref" reference="eq:il-loss"}, then continue fine-tuning through RL to handle scenarios where the expert data are sparse or suboptimal: $$\theta_{\mathrm{combined}} 
\;=\;
\arg \min_\theta
\Bigl[
\sum_{k=1}^M \mathcal{L}\bigl(f_\theta(\mathbf{x}_k),\mathbf{y}_k\bigr) 
\;+\;
\lambda\,\mathcal{L}_{\mathrm{RL}}(\theta)
\Bigr].$$ For example:

- [@sartoretti2019primal] combine RL and IL to train a fully decentralized policy (PRIMAL).

- [@xie2024crowd] incorporate a Controlled Communication mechanism with IL to refine crowd-awareness among agents (C3PIL).

- [@liu2024multi] propose a multi-agent RL extension of Soft Actor-Critic (ISAC) and integrate IL to accelerate convergence (ISAC-IL).

### Curriculum Learning

Curriculum Learning (CL) gradually increases the difficulty or complexity of MAPF tasks during training. Starting from simpler tasks (fewer agents, smaller maps) can help each agent's policy converge to collision-free navigation strategies: $$\text{Train on }(\mathcal{V}_0,\mathcal{E}_0,\dots) \;\to\; 
(\mathcal{V}_1,\mathcal{E}_1,\dots) \;\to\; \ldots
\;\to\;
(\mathcal{V}_f,\mathcal{E}_f,\dots).$$ [@phan2024confidence] define CACTUS, a confidence-based scheme that adaptively expands difficulty as the agent's success rate increases. [@zhao2023curriculum] design a multi-phase approach, injecting more agents or higher obstacle density step by step. Empirical signals (e.g., success rate $>90\%$) trigger a progression to the next level.

### Evolutionary Methods

Evolutionary Algorithms (EAs) treat agent paths or high-level policies as *genomes* subject to evolutionary operators (selection, crossover, mutation). If $\mathbf{p}$ encodes a joint path set, the *fitness function* might be: $$\mathrm{Fitness}(\mathbf{p})
\;=\;
-\Bigl(
\underbrace{\mathrm{SoC}(\mathbf{p})}_{\text{sum-of-costs}}
\;+\;
\alpha\,\underbrace{\mathrm{Collisions}(\mathbf{p})}_{\text{collision count}}
\Bigr),$$ where collisions reflect the number of conflicting moves. In each generation, new path populations $\{\mathbf{p}^{(g+1)}\}$ evolve from $\{\mathbf{p}^{(g)}\}$:

1.  *Selection:* retain top $K$ solutions by fitness.

2.  *Crossover:* combine partial paths from two parents.

3.  *Mutation:* randomly alter portions of the path with a collision check or local re-routing.

Recent examples:

- [@liu2020mapper] propose *MAPPER*, combining distributed partially observable navigation and evolutionary RL for large-scale robotic tasks.

- [@paul2022multi] embed evolutionary game dynamics into multi-agent exploration, using replicator equations to update agent strategies.

Evolutionary search can handle complex and large state spaces, but runtime may grow with problem size unless carefully parallelized or hybridized with classical MAPF heuristics.

## Discussion

The diverse learning paradigms studied in this section---MCTS, supervised methodologies, composite learning (RL+IL, curriculum), and evolutionary searches---demonstrate varied ways to fuse data-driven or iterative optimization ideas with the classical MAPF blueprint (Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}). Table [9](#tab:paradigm-advantages){reference-type="ref" reference="tab:paradigm-advantages"} summarizes core advantages and open challenges across these paradigms.

::: {#tab:paradigm-advantages}
+-----------------------------------+----------------------------------------------------------------+----------------------------------------------------------------+
| **Paradigm**                      | **Advantages**                                                 | **Limitations / Open Challenges**                              |
+:==================================+:===============================================================+:===============================================================+
| **MCTS**                          | - Systematic search with built-in exploration                  | - Exponential branching if $n$ is large                        |
|                                   |                                                                |                                                                |
|                                   | - Flexible rollout policies, can incorporate domain heuristics | - Requires repeated rollouts at every decision step            |
+-----------------------------------+----------------------------------------------------------------+----------------------------------------------------------------+
| **Supervised Learning**           | - Fast inference once trained                                  | - No performance guarantees if test scenarios differ           |
|                                   |                                                                |                                                                |
|                                   | - Straightforward adaptation of classical solver outputs       | - Requires large labeled datasets, might not adapt online      |
+-----------------------------------+----------------------------------------------------------------+----------------------------------------------------------------+
| **Composite (IL+RL, Curriculum)** | - Synergy: IL speed + RL adaptivity                            | - Complex training pipeline                                    |
|                                   |                                                                |                                                                |
|                                   | - Progressive training can tackle large tasks                  | - Balancing multi-objective losses can be delicate             |
+-----------------------------------+----------------------------------------------------------------+----------------------------------------------------------------+
| **Evolutionary Methods**          | - Population-based search explores diverse solutions           | - Computation can become expensive                             |
|                                   |                                                                |                                                                |
|                                   | - Parallel-friendly optimization                               | - May converge slowly if mutation/crossover are not well tuned |
+-----------------------------------+----------------------------------------------------------------+----------------------------------------------------------------+

: Key Advantages and Limitations of Non-RL Learning Paradigms in MAPF. While many methods yield benefits in adaptability or solution speed, each has distinct pitfalls in terms of scalability, out-of-distribution robustness, or theoretical guarantees.
:::

Looking forward, promising future directions include:

- **Hybridizing MCTS or EAs with classical solvers,** e.g., using MCTS expansions to focus on potentially conflicting sub-regions of a graph while a compilation-based solver handles the global plan.

- **Advanced supervision from partial solutions,** rather than full demonstration traces, possibly reducing dataset requirements.

- **Aggressive curriculum or meta-learning,** where tasks automatically adjust difficulty based on the agent performance, bridging offline training and real-time deployment.

- **Evolutionary-lifelong synergy,** combining repeated assignments (Section [6.10](#subsec:lifelong){reference-type="ref" reference="subsec:lifelong"}) with evolutionary population updates to continually adapt agent routes in changing environments.

These areas underscore the broader theme of *integrating* learning modules into well-established MAPF frameworks (Sections [3](#sec:search){reference-type="ref" reference="sec:search"} and [4](#sec:compilation){reference-type="ref" reference="sec:compilation"}), aiming to achieve the best of both worlds: flexible adaptation and strong theoretical grounding.

In conclusion, the paradigms outlined here complement reinforcement learning methods (Section [6](#sec:rl){reference-type="ref" reference="sec:rl"}) and existing classical MAPF pipelines in various ways. They further illustrate the growing richness of data-driven MAPF research, where advanced machine learning techniques---ranging from tree-based rollouts to supervised and evolutionary optimization---continue to push the boundaries of scalability and robustness in multi-agent path planning.

## Towards a Tighter Integration of Classical and Learning-Based Methods

### Underutilized Classical Insights

Recent years have witnessed a surge in learning-based methods for MAPF, particularly via deep multi-agent reinforcement learning or neural search heuristics. Yet these innovations often overlook the extensive body of work developed under the classical MAPF paradigm, which includes both search-based (e.g., Conflict-Based Search, priority-based schemes, large neighborhood search) and compilation-based (e.g., SAT, SMT, and MIP) frameworks. These classical methods embody decades of specialized insights into conflict resolution, combinatorial pruning, meta-agent merging, and domain-specific constraint propagation. While contemporary learning-based approaches sometimes adopt high-level ideas or partial code reuse from these algorithms, they rarely integrate the deeper theoretical properties that have proven indispensable for producing robust, efficient, and theoretically grounded solutions.

One critical shortfall is that classical MAPF solutions have systematically studied how to detect and handle collisions under a wide range of conditions, using sophisticated notions such as corridor or rectangle conflicts, conflict prioritization, and exhaustive "include-exclude" branching strategies. Admissible and consistent heuristics---like the pairwise dependency graph (DG) or weighted DG---substantially prune the search space by exploiting structural features unique to MAPF. They also enable meta-agent merges in CBS-based methods, ensuring that agents that repeatedly conflict are planned jointly, and thus reducing the risk of recurring collisions. However, many modern machine learning planners do not fully leverage these refined conflict-handling laws. They often treat collisions as uniform penalty signals in a reward function, effectively rediscovering collision dynamics "from scratch." This leads to slow convergence during training and provides no guaranteed resolution once collisions become frequent, whereas a more direct infusion of classical conflict classification or bounding techniques could identify and prune problematic regions early, accelerating learning-based policy improvements.

Beyond collision handling, classical MAPF research has also developed systematic methods for branching and bounding solution costs. In conflict-based schemes, branching on cardinal conflicts first (i.e., collisions that increase the total solution cost if left unresolved) is known to boost convergence to an optimal or near-optimal solution. Similarly, priority-based approaches exploit partial orders on agents, reordering them dynamically when certain conflict patterns arise, so that repeated collisions do not stall planning. Moreover, advanced compilation-based solvers encode complex domain constraints into Boolean or linear formulations, enabling branch-and-cut to eliminate infeasible portions of the search space in a mathematically precise way. In principle, these bounding strategies could be embedded in a neural or reinforcement learning pipeline as "hard" constraints that forcibly prune unproductive states, or as differentiable approximations that guide a policy or Q-function away from infeasible actions. By failing to adopt such systematic bounding rules, learning-based approaches cede the algorithmic efficiency and theoretical guarantees that classical MAPF algorithms painstakingly achieve.

Classical MAPF also brings a variety of domain-specific formulations---for instance, multi-valued decision diagrams (MDDs) that restrict agent paths to only those that are cost-minimal if no collisions were present. These MDDs can be extended with advanced mutual-exclusion rules to prune large swaths of collision-prone paths. In principle, an MDD-based feasibility checker could be folded into a learning-based planner, allowing a deep policy to query whether a partial plan is viable---an operation known to dramatically reduce branching in classical MAPF. Equally significant is the concept of meta-agent merging, where a cluster of conflicting agents is treated as a single entity in the search, reflecting their interdependent joint moves. Current data-driven approaches rarely adopt such merging rules, typically treating collisions in an atomistic fashion. Incorporating meta-agent reasoning could enable a neural planner to reason directly about coordinated group moves, benefiting from the same conflict-abatement benefits that classical MAPF has long utilized.

A further benefit of classical MAPF is its nuance in handling unconventional constraints or real-world complexities. Over the years, researchers have integrated resource constraints, motion-primitive restrictions, agent heterogeneity, and multi-goal scheduling into standard MAPF formulations by carefully constructing additional constraints or objective functions. These domain-specific expansions are typically enforced with proven bounding mechanisms or exhaustive branching, which preserve completeness or suboptimality guarantees. In contrast, learning-based MAPF often tries to handle such variations by imposing a heuristic penalty or, at best, by customizing the reward function. While these approaches can work in principle, they are rarely accompanied by the deeper logical consistency checks that classical MAPF constraint reasoning would provide.

A related challenge is that many data-driven MAPF planners lack transparent performance bounds or completeness guarantees. Even suboptimal variants of classical MAPF, such as bounded suboptimal CBS or prioritized search with known approximation ratios, retain explicit guarantees on how their solutions deviate from optimum. Once these structures are ignored, the resulting learning-based method might converge to feasible paths in practice but offers no quantifiable measure of success under unforeseen circumstances or domain shifts. Although recent years have seen the emergence of "safe RL" paradigms that attempt to impose constraints during policy learning, the synergy between these paradigms and the proven bounding strategies from classical MAPF remains largely unexplored.

In light of these observations, there is vast potential for cross-pollination between learning-based MAPF and classic approaches. For instance, one could envision a "meta-CBS" search in which conflict branching relies on proven classical rules (identifying which conflict is cardinal, merging a group of interdependent agents), while the expansion or node-selection heuristics are guided by a learned model that predicts the most promising branches. Under such a framework, the rigor of collision detection and branching remains intact, but the overall search process gains speed and adaptability from the learned selection policy. Similarly, approximate versions of multi-valued decision diagrams might serve as a differentiable layer within a neural architecture, allowing the network to quickly rule out large classes of infeasible partial plans. Such hybrid strategies would incorporate the collision resolution strengths and theoretical scaffolding of classical MAPF while benefiting from the powerful function-approximation abilities of neural networks.

Ultimately, the valuable insights of classical MAPF research need not be relegated to footnotes or replaced wholesale. Instead, they can be adapted, approximated, or embedded into the emergent class of machine learning frameworks in a way that preserves both classical rigor and learning-based adaptability. This deeper fusion would not only accelerate training and improve solution quality but could also impart valuable theoretical performance bounds to systems that otherwise risk unpredictable behavior. Achieving this integration stands as an open challenge, but it promises a richer array of tools for future MAPF researchers seeking to move beyond the purely classical or purely data-driven paradigms.

## Underexplored Opportunities for Learning-Augmented Classical MAPF

Researchers have increasingly recognized the potential of learning-based MAPF methods in complex or uncertain environments. Yet the converse direction---embedding learning within *classical* MAPF solvers---remains comparatively neglected. Existing work on conflict-based search (CBS), priority-based search (PBS), or large neighborhood search (LNS) that incorporates machine learning has only begun to scratch the surface of what is theoretically and practically possible. Techniques such as learned conflict selection or agent prioritization demonstrate clear speedups and solution-quality gains, suggesting that nearly every module of a classical solver could benefit from a data-driven upgrade while retaining the solver's transparent, systematic structure.

The most direct opportunities lie in how these solvers handle branching, pruning, and constraint propagation. For instance, search-based planners typically rely on heuristic expansions or handcrafted conflict-splitting rules that may be suboptimal as problem scale grows. In CBS, conflicts encountered at the high level must be systematically resolved by branching, yet deciding *which* conflict to branch on, or *how* to split constraints among child nodes, is often determined by static policies (e.g., "choose the earliest conflict" or "choose the conflict with largest cost impact"). A learning-augmented approach could, in principle, tailor these branching decisions to the structure of actual instances. A trained classifier or regressor, leveraging historical search traces, might predict which specific conflict will yield the most branching overhead if left unresolved, thereby prioritizing it at the high level and reducing the overall size of the conflict tree. Similar logic applies to suboptimal variants of CBS, where a data-driven focal search could refine or relax bounding factors more adaptively.

Even in priority-based solvers, a machine learning model can drive dynamic reordering or grouping of agents. Classical PBS sets a static priority ordering for agents to follow, with collisions prompting merges of "meta-agents." While some work has shown that learned priority assignments reduce collisions, many deeper avenues remain open. For example, an online learned policy could detect that certain agents---due to their goals, speeds, or frequently blocked paths---are "high risk" for repeated collisions, and thus reorder them to the top of the priority queue. Another policy might guide whether two conflicting agents should be merged into a single meta-agent at all, or if a simpler local detour would suffice. By situating these data-driven heuristics within PBS's proven collision-avoidance framework, one can mitigate capacity or scheduling bottlenecks in real-time applications without discarding the solver's theoretical underpinnings.

In the realm of compilation-based MAPF, learning has a potentially even greater role. Formulations like SAT, SMT, CSP, ASP, or MIP frequently suffer from large search trees in branching, cutting, or conflict refinement. Although these solvers already incorporate sophisticated general-purpose heuristics (e.g., branching rules for SAT or MIP, conflict-driven clause learning, or cutting-plane selection), they remain blind to the domain-specific structure of MAPF problems. A synergy with machine learning might be realized by training a specialized "neural solver" or "learning-based branch-and-cut" mechanism that recognizes which integer or Boolean variables are most critical for collision resolution, which potential cuts (e.g., collision cuts in MIP or lazy constraints in LaCAM) are likely to prune large infeasible regions, and which partial solutions are promising enough to keep exploring. One possible direction is to record frequent patterns of collisions or resource conflicts across MAPF instances, then train a model to inject relevant "cuts" or constraints earlier in the solver's process---thereby dramatically shortening the convergence time. Lazy-constraint addition frameworks like LaCAM could also benefit from a learning module that predicts which constraints will actually matter, skipping many redundant checks and leaving more solver bandwidth for critical expansions.

Beyond these local improvements, a symbiosis between machine learning and classical MAPF could address high-dimensional or multi-objective variants more effectively than either approach alone. Industrial-scale MAPF problems often involve rich constraints (e.g., limited fuel, time windows, or capacity constraints for each agent), uncertain data streams (e.g., partial sensor data in real time), or hierarchical objectives (e.g., first minimize collisions, then total cost, then maximum lateness). Although classical planners can systematically incorporate these constraints once formalized, they often struggle in rapidly changing environments or when large portions of the input are noisy or approximate. Here, a learned module could filter or "translate" unstructured real-time observations---such as imperfect sensor measurements---into compact, high-level constraints that the solver can handle efficiently. In return, the solver's partial solutions, conflict clauses, or explanatory branching structures may serve as "labels" or "demonstrations" to a learning algorithm, ensuring that any learned policy adheres to collision-free or resource-feasible solutions.

Despite this broad potential, current attempts at learning-augmented classical MAPF generally limit themselves to modest instance scales or rely on ad hoc ways of inserting neural components (e.g., a single learned conflict-picker for CBS). Much of the solver's internal logic---such as advanced symmetry reasoning, disjoint splitting, or hierarchical branching---remains unaffected by learning, leaving vast spaces of synergy unexplored. In particular, there has been little effort to systematically categorize *where* and *how* data-driven modules might intervene. Such a taxonomy could map out all major stages in classical MAPF pipelines, from initial pre-processing and path generation to final conflict resolution, indicating which machine learning strategies (supervised, reinforcement, offline imitation, online adaptation) are most compatible at each stage. It would also help clarify the potential performance trade-offs, such as how real-time inference overhead from a neural network might compare with the time saved from fewer search-node expansions.

Ultimately, unlocking the full power of learning-augmented classical MAPF will require a tighter connection between the solver's inherent strengths---soundness, exhaustive branching, and interpretability---and the adaptability, pattern recognition, and data-driven generalization offered by machine learning. Achieving this synergy calls for both deeper theoretical understanding (e.g., how best to guarantee safety or completeness when deferring key decisions to a trained module) and extensive empirical evaluation (e.g., how to ensure robust performance on varied maps or dynamic tasks). By moving beyond incremental or "add-on" usage of neural networks and embracing a more integrated, principled approach, the research community can create versatile solvers that are not only guided by data but also anchored by decades of MAPF theory, ensuring both increased efficiency within known constraints and flexible adaptation to complex real-world conditions.

# Experimental Settings and Comparisons {#sec:exp}

As introduced in Section [1](#sec:intro){reference-type="ref" reference="sec:intro"}, MAPF involves devising collision-free trajectories for multiple agents within a shared environment. The mathematical formulation outlined in Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"} emphasizes representations of the environment as graphs or continuous domains, the objectives to minimize (e.g., makespan, sum-of-costs, or task completion time), and the control modes (centralized vs. decentralized). Building on those foundations, this section examines how MAPF researchers design and evaluate their experiments in practice. The discussion is organized into three main parts: (1) **Experimental environments**, which encapsulate map types and complexity; (2) **Evaluation metrics**, which capture success, safety, solution efficiency, and computation costs; (3) **Scaling factors**, including the number of agents and map sizes, as well as typical baseline selections. Throughout, mathematical abstractions are provided to solidify the connections between problem formulations (Section [2](#sec:formulation){reference-type="ref" reference="sec:formulation"}) and real-world (or simulated) experiments.

## Types of Experimental Environments {#subsec:env_types}

In MAPF experiments, the *environment* is often modeled as $\mathcal{G}=(\mathcal{V}, \mathcal{E})$ for discrete (grid) spaces or $\Omega \subseteq \mathbb{R}^d$ for continuous domains. However, the structure of $\mathcal{V}$ (or $\Omega$) can vary significantly among studies. Table [\[tab:env_comparison\]](#tab:env_comparison){reference-type="ref" reference="tab:env_comparison"} summarizes the most prevalent types of experimental environments. Where applicable, we provide an equivalent mathematical description. Classical methods and learning-based methods essentially use the same simulation environments, therefore this section does not make a distinction between them.

::: {#tab:mapf-env}
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
| **Type**           | **Map**                    | **Size**          | **Preview (map in bold)**                                                    |
+:===================+:===========================+:=================:+:============================================================================:+
| City               | Berlin_1_256               | 256 $\times$ 256  | ![image](Wang2025Where_figs/Boston_0_256.png){width="9%"}           |
|                    +----------------------------+-------------------+                                                                              |
|                    | **Boston_0_256**           | 256 $\times$ 256  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | Paris_1_256                | 256 $\times$ 256  |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
| Dragon Age Origins | brc202d                    | 481 $\times$ 530  | ![image](Wang2025Where_figs/den520d.png){width="9%"}                |
|                    +----------------------------+-------------------+                                                                              |
|                    | den312d                    | 81 $\times$ 65    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | **den520d**                | 256 $\times$ 257  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | lak303d                    | 194 $\times$ 194  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | orz900d                    | 656 $\times$ 1491 |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | ost003d                    | 194 $\times$ 194  |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
|                    | **ht_chantry**             | 141 $\times$ 162  | ![image](Wang2025Where_figs/ht_chantry.png){width="9%"}             |
|                    +----------------------------+-------------------+                                                                              |
|                    | ht_mansion_n               | 270 $\times$ 133  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | w_woundedcoast             | 578 $\times$ 642  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | lt_gallowstemplar_n        | 180 $\times$ 251  |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
| Open               | empty-8-8                  | 8 $\times$ 8      | ![image](Wang2025Where_figs/empty-32-32.png){width="9%"}            |
|                    +----------------------------+-------------------+                                                                              |
|                    | empty-16-16                | 16 $\times$ 16    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | **empty-32-32**            | 32 $\times$ 32    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | empty-48-48                | 48 $\times$ 48    |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
|                    | random-32-32-10            | 32 $\times$ 32    | ![image](Wang2025Where_figs/random-32-32-20.png){width="9%"}        |
|                    +----------------------------+-------------------+                                                                              |
|                    | **random-32-32-20**        | 32 $\times$ 32    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | random-64-64-10            | 64 $\times$ 64    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | random-64-64-20            | 64 $\times$ 64    |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
| Maze               | maze-32-32-2               | 32 $\times$ 32    | ![image](Wang2025Where_figs/maze-128-128-10.png){width="9%"}        |
|                    +----------------------------+-------------------+                                                                              |
|                    | maze-32-32-4               | 32 $\times$ 32    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | maze-128-128-1             | 128 $\times$ 128  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | maze-128-128-2             | 128 $\times$ 128  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | **maze-128-128-10**        | 128 $\times$ 128  |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
| Room               | room-32-32-4               | 32 $\times$ 32    | ![image](Wang2025Where_figs/room-64-64-8.png){width="9%"}           |
|                    +----------------------------+-------------------+                                                                              |
|                    | room-32-32-8               | 32 $\times$ 32    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | **room-64-64-8**           | 64 $\times$ 64    |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | room-64-64-16              | 64 $\times$ 64    |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+
| Warehouse          | warehouse-10-20-10-2-1     | 161 $\times$ 63   | ![image](Wang2025Where_figs/warehouse-10-20-10-2-2.png){width="9%"} |
|                    +----------------------------+-------------------+                                                                              |
|                    | **warehouse-10-20-10-2-2** | 170 $\times$ 84   |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | warehouse-20-40-10-2-1     | 321 $\times$ 123  |                                                                              |
|                    +----------------------------+-------------------+                                                                              |
|                    | warehouse-20-40-10-2-2     | 340 $\times$ 164  |                                                                              |
+--------------------+----------------------------+-------------------+------------------------------------------------------------------------------+

: Overview of MAPF Experimental Environments
:::

Table [10](#tab:mapf-env){reference-type="ref" reference="tab:mapf-env"} catalogs the most prevalent MAPF benchmark maps, organized by environment type. For each environment category, i.e., *City, Game (Dragon Age Origins, Dragon Age 2), Open, Random, Maze, Room*, and *Warehouse*, specific map instances are listed along with their dimensions. The preview column provides a visual representation of a representative map from each category, offering readers a quick visual reference of the environment's structural characteristics.

These benchmark environments vary significantly in their structural complexity, ranging from empty grids (Open) to intricate city layouts and game maps. This diversity allows researchers to evaluate algorithm performance across different scenarios with varying levels of difficulty. For instance, *Warehouse* simulates logistics settings with regular patterns of shelves and corridors, while *Maze* presents navigation challenges with narrow passages and potential deadlocks.

::: sidewaystable
:::

Table [\[tab:env_comparison\]](#tab:env_comparison){reference-type="ref" reference="tab:env_comparison"} complements Table [10](#tab:mapf-env){reference-type="ref" reference="tab:mapf-env"} by providing a mathematical formalization of each environment type along with its key characteristics and associated challenges. The mathematical representations frame these environments in terms of graph theory (for discrete spaces) or geometric spaces (for continuous domains), establishing a rigorous foundation for algorithm development and analysis. For each environment type, the table highlights the specific navigation challenges they pose, such as congestion in narrow corridors for maze environments or dynamic obstacle avoidance in time-varying settings.

#### Remarks.

*Random* environments are commonly used to train and test learning-based algorithms, gradually increasing size or obstacle density to evaluate scalability. *Mazes* focus on congestion phenomena and agent coordination in highly constrained passages. *Warehouse* and *City* maps approximate real-world logistics or urban layouts, making them a standard for industrial MAPF solutions. *Blank* maps help isolate an algorithm's inherent path-planning efficiency without the confounding presence of obstacles. *Dynamic* environments refine MAPF to dynamic MAPF (DMAPF) scenarios, highlighting the necessity of online or continual re-planning.

## Evaluation Metrics {#subsec:eval_metrics}

Evaluating MAPF algorithms requires a comprehensive set of metrics that capture different aspects of performance, efficiency, and solution quality. In this section, we categorize these metrics into distinct groups and provide detailed definitions for each. When discussing these metrics, we consider a scenario where $n$ agents operate in an environment $\mathcal{G}$ over a time horizon $T$, with $a_i(t)$ representing the action of agent $i$ at time $t$, and $s_i(t)\in\mathcal{V}$ (or $\Omega$) denoting agent $i$'s position at time $t$.

We organize our discussion of metrics into two main categories: those commonly used for evaluating classic MAPF methods (Table [\[tab:metrics_summary_classic\]](#tab:metrics_summary_classic){reference-type="ref" reference="tab:metrics_summary_classic"}) and those frequently applied to learning-based approaches (Table [\[tab:metrics_summary\]](#tab:metrics_summary){reference-type="ref" reference="tab:metrics_summary"}). While some metrics appear in both categories, their importance and implementation often differ based on the algorithmic paradigm.

### Metrics for Classic Methods

Classic MAPF methods typically prioritize completeness and optimality guarantees, with evaluation focused on solution quality, computational efficiency, and algorithmic properties. Table [\[tab:metrics_summary_classic\]](#tab:metrics_summary_classic){reference-type="ref" reference="tab:metrics_summary_classic"} presents metrics commonly used for evaluating these approaches.

The success and failure metrics for classic methods include Success Rate (SR), which measures the proportion of agents that reach their goals, and more specialized metrics like Number of Instantiated Agents (NIA) and Number of On-Time Agents (NOTA) that account for deadline constraints. These metrics are particularly important for applications with strict timing requirements, such as warehouse logistics and airport operations.

Solution efficiency metrics for classic methods are often tied to optimization objectives. Sum-of-Cost (SoC) and Sum-of-Delay (SoD) capture the cumulative time agents spend reaching their goals, with SoD specifically measuring the excess time beyond optimal paths. Makespan (MKSP) evaluates the time until the last agent reaches its goal, critical for scenarios where completion time is the primary concern. Additional metrics like Flowtime (FT) and Throughput (TP) measure different aspects of solution efficiency.

Computational metrics for classic methods include Runtime (RT) and memory usage, which are crucial for assessing algorithmic scalability. Specialized metrics like CT Node Expansions provide insight into the search process of Conflict-Based Search algorithms, helping researchers understand algorithmic behavior. Solution quality metrics such as Optimality Rate and Suboptimality Rate directly address how close solutions are to theoretical optimum, reflecting the emphasis classic methods place on optimality guarantees. Social Welfare (SW) introduces economic considerations by balancing goal values against travel costs.

The table also includes specialized metrics for resource utilization, conflict analysis, and lifelong MAPF scenarios, capturing the breadth of evaluation approaches used with classic methods.

### Metrics for Learning-based Methods

Learning-based MAPF methods typically prioritize scalability, adaptability, and real-time performance, with metrics reflecting these priorities as shown in Table [\[tab:metrics_summary\]](#tab:metrics_summary){reference-type="ref" reference="tab:metrics_summary"}.

::: sidewaystable
:::

Success and failure metrics for learning-based methods include Success Rate (SR), similar to classic methods, but also focus on Failed Agent Count (FAC) and Timeout Rate (TR). The latter metrics are particularly relevant since learning-based methods often make trade-offs between optimality and completion rate.

Collision-related metrics are especially prominent for learning-based approaches, which may not provide the same collision-avoidance guarantees as classic methods. Metrics like Collision Count (CC), Collision Times Per Step (CTPS), and Collision with Obstacles (CO) quantify safety concerns, which are crucial when deploying learning-based systems in real-world environments.

Solution efficiency metrics for learning-based methods include Makespan (MK), Flowtime (FT), and Path Length (PL), similar to classic methods. However, these metrics are often evaluated empirically rather than with formal guarantees, reflecting the different methodological approaches. Computation time metrics for learning-based methods include overall Runtime (RT) but emphasize Per-Iteration Complexity, which is critical for real-time applications. Learning-based methods frequently need to make decisions within strict time constraints, making computational efficiency per planning cycle particularly important.

**Discussion.** The evaluation metrics for classic and learning-based MAPF methods reflect fundamental differences in methodological priorities and application contexts. We can highlight several key distinctions:

- *Success & Failure* metrics are important across both paradigms, but classic methods often emphasize optimality within constraints, while learning-based methods tend to focus on robustness and completion rates in complex, uncertain environments. Classic methods typically report metrics like NIA and NOTA that incorporate strict deadlines, whereas learning-based methods more commonly report failure counts and timeout rates that acknowledge the probabilistic nature of their solutions.

- *Collision-Related* metrics are critical for both approaches but serve different purposes. For classic methods, collisions are often theoretical constraints within the planning process and may not be explicitly measured in evaluation since many algorithms guarantee collision-free paths. In contrast, learning-based methods, which may sacrifice deterministic guarantees for scalability, must carefully quantify collision rates to assess safety implications. This explains the prominence of metrics like CC, CTPS, and CO specifically for learning-based approaches.

- *Solution Efficiency* metrics like makespan [\[eq:makespan\]](#eq:makespan){reference-type="eqref" reference="eq:makespan"} and sum-of-costs [\[eq:soc\]](#eq:soc){reference-type="eqref" reference="eq:soc"} are common to both paradigms but with different emphases. Classic methods typically provide optimality bounds or guarantees with respect to these objectives, while learning-based methods report empirical performance. Additionally, classic methods often include specialized efficiency metrics (like SoD, TP, and MET) that capture nuanced aspects of performance relevant to theoretical analysis.

- *Computation Time* represents perhaps the starkest contrast between the paradigms. Classic methods like ILP-based or SAT-based approaches prioritize finding optimal solutions even at significant computational cost, with metrics focusing on total runtime and memory usage. Learning-based methods, especially those designed for real-time deployment, emphasize per-iteration efficiency and bounded-time decision making, with metrics that reflect this real-time constraint.

- *Algorithmic Process* metrics differ substantially between paradigms. Classic methods often report metrics specific to their algorithmic structure (e.g., CT Node Expansions, Mutex Propagation Time) to provide insight into internal processes. Learning-based methods typically focus less on algorithmic internals and more on end-to-end performance metrics relevant to deployment scenarios.

This comparison highlights how evaluation metrics reflect the fundamental trade-offs between these paradigms: classic methods prioritizing completeness, optimality, and theoretical guarantees versus learning-based approaches emphasizing scalability, adaptability, and real-time performance in complex environments.

While the field has produced a wide array of evaluation metrics tailored to both classic and learning-based MAPF paradigms, it is important to recognize several limitations and challenges that arise from current evaluation practices. Notably, most published works do not report or compare results across the full spectrum of metrics outlined above. Instead, each study tends to select a subset of metrics that best aligns with its methodological strengths or targeted application domain. **This selective reporting inadvertently hampers direct comparison between algorithms and often obscures the broader landscape of algorithmic trade-offs.** As a result, it becomes difficult for practitioners and researchers to draw comprehensive conclusions regarding the relative merits of different approaches.

Moreover, the divergence in metric preferences between classic and learning-based MAPF communities further exacerbates this problem. Classic methods have traditionally emphasized theoretical guarantees and optimality-focused metrics, while learning-based approaches are more likely to report empirical performance and safety-related statistics. **This division creates a barrier for cross-paradigm benchmarking and restricts the transfer of insights between the two communities.** The lack of common ground in evaluation criteria not only impedes fair assessment but also slows progress toward integrative or hybrid MAPF solutions that could leverage the advantages of both paradigms.

To address these challenges and foster the development of the MAPF field as a whole, it would be highly beneficial for the community to **converge on a more standardized and comprehensive set of evaluation protocols**. Such protocols should encourage the reporting of a broader set of metrics, encompassing both theoretical guarantees and empirical behaviors, as well as those that reflect real-world constraints and safety considerations. Efforts to develop unified benchmark suites, open-source evaluation toolkits, and consensus on metric definitions will be instrumental in enabling more meaningful and transparent comparisons between algorithms. In turn, this will facilitate clearer identification of research gaps, accelerate the adoption of MAPF solutions in practice, and promote the cross-fertilization of ideas between the classic and learning-based research communities.

## Environment Scale and Baseline Selections {#subsec:scale_baselines}

### Scaling in Map Size and Agent Number

The relationship between map size and agent population represents one of the most critical factors affecting MAPF problem difficulty. As these parameters increase, the computational complexity grows exponentially, creating significant challenges for both classical and learning-based approaches. In formal terms, consider a grid-based MAPF instance with map dimensions $H \times W$ and agent set ${1,\dots,n}$. Each experimental configuration can be represented as a triple $(H,W,n)$. Given a map $\mathcal{G}$ of size $H\times W$, the effective state space expands to $\mathcal{V}^n \equiv (H\times W)^n$ for the possible permutations of agent positions. This state space grows combinatorially as either the map dimensions $(H,W)$ or the agent count $n$ increases, representing a fundamental computational challenge in MAPF.

Figures [21](#fig:classic_map_agent){reference-type="ref" reference="fig:classic_map_agent"} and [22](#fig:map_agent){reference-type="ref" reference="fig:map_agent"} visualize the landscape of experimental configurations used across the MAPF literature. These heatmaps represent the frequency with which particular $(H\times W,n)$ pairs appear in research studies, with color intensity indicating usage frequency. Based on our survey, we can categorize MAPF problem instances into four distinct scales:

- **Small-Scale** (e.g., $H,W<10$ or $n<10$): These configurations serve primarily as algorithmic testbeds, enabling quick proofs-of-concept, debugging sessions, and theoretical validations. While limited in practical application, they allow researchers to isolate algorithmic behaviors without prohibitive computational costs.

- **Medium-Scale** ($10\leq H,W\leq 50$ or $10 \leq n \leq64$): Representing the most common configurations in academic benchmarks, these instances strike a balance between computational feasibility and real-world relevance. Many standard MAPF benchmarks like warehouse, game, and city maps fall within this category, making it the principal testing ground for comparing algorithmic approaches.

- **Large-Scale** ($H,W>50\times50$ or$64 \leq n \leq512$): As industrial applications gain prominence, this scale has become increasingly important. Configurations in this range test algorithms under conditions approximating real-world deployment scenarios, such as warehouse automation systems with hundreds of robots [@friedrich2024scalable]. At this scale, many optimal algorithms become impractical, shifting focus toward bounded-suboptimal or incomplete methods.

- **Very Large-Scale** ($n>512$ or $H,W >100\times100$): The frontier of MAPF research, these configurations push algorithms to their limits and reveal fundamental scalability bottlenecks. At this scale, decentralized approaches, hierarchical methods, and learning-based solutions often become necessary, as centralized optimal planning becomes computationally intractable.

:::: {#fig:classic_map_agent .figure latex-placement="htb!"}
![](Wang2025Where_figs/Environmental_classic_scale_heatmap2.png){width="\\linewidth"}

::: caption
Representative heatmap (schematic) depicting experimental configurations of map size vs. agent number for classical methods. The horizontal axis denotes the agent population $n$, while the vertical axis denotes the map. The color intensity indicates the frequency of usage in surveyed papers.
:::
::::

:::: {#fig:map_agent .figure latex-placement="htb!"}
![](Wang2025Where_figs/Environmental_scale_heatmap.png){width="\\linewidth"}

::: caption
Representative heatmap (schematic) depicting experimental configurations of map size vs. agent number for learning-based methods. The horizontal axis denotes the agent population $n$, while the vertical axis denotes the map dimension (e.g., $H\times W$). The color intensity indicates the frequency of usage in surveyed papers.
:::
::::

These two figures show that, classic methods demonstrate a clear dichotomy in the size of maps they tackle. On one hand, a significant portion of classic works target medium-scale problems, often with map side lengths in the range of 20 to 50. These settings are generally more tractable and allow for detailed benchmarking of algorithmic improvements. On the other hand, several studies explicitly stress-test the scalability of classic methods on very large-scale problems, with map side lengths reaching approximately 200. This dual focus demonstrates the longstanding tradition in the MAPF community to both refine algorithmic efficiency for moderate-sized environments and push the boundaries of scalability. With respect to agent count, classic methods commonly address scenarios with 64 to 1024 agents. The distribution across this range is relatively even, and more than half of the surveyed works handle settings categorized as large-scale (hundreds of agents) or very large-scale (over a thousand agents). This breadth underscores the maturity and robustness of classic algorithms in managing high agent densities, a critical requirement for real-world deployments such as warehouse automation or traffic management.

In contrast, learning-based methods, which leverage deep reinforcement learning, imitation learning, or other data-driven techniques, also display polarization in the map sizes considered. Most current research focuses on medium-scale maps (side length 10--50) and, to a lesser extent, large-scale maps (side length 80--100). However, the number of agents handled by these methods is generally much lower, typically ranging from 8 to 256 agents. The vast majority of studies remain within the bounds of large-scale or smaller problem instances. This concentration on relatively modest scales suggests that, despite strong recent advances, the application of learning-based approaches to truly large and dense MAPF scenarios remains limited in practice.

It is particularly noteworthy that **learning-based methods, despite their purported advantage of scalability, are predominantly evaluated on smaller problem instances compared to classic methods**. This observation is somewhat counterintuitive, given that a central claim of learning-based MAPF research is the potential for improved scalability through parallelism, generalization, and efficient policy learning. Several factors may contribute to this gap. Training deep models on very large maps with hundreds or thousands of agents is computationally intensive and may be hampered by sample inefficiency or instability. The community has gravitated towards established benchmarks that emphasize smaller or medium-sized problems, possibly due to the high cost of data generation and verification in larger settings. Moreover, current neural architectures may struggle with long-range coordination and global conflict resolution in massive environments, necessitating further innovation. There is also a lack of standardized metrics for large-scale MAPF that are both fair and informative across classic and learning-based methods.

To more fully realize the promise of learning-based MAPF methods and to facilitate a fair comparison with classic approaches, future research should focus on several directions. First, there is a need to scale up benchmark problems and adopt new benchmarks that reflect the scale and density of real-world applications, with larger maps and agent populations. Second, algorithmic innovation is required, particularly in the design of scalable neural architectures---such as graph neural networks, hierarchical policies, or multi-stage training---that can effectively manage global coordination among thousands of agents. Third, the development and investigation of hybrid methods that combine classic and learning-based techniques may leverage the strengths of both paradigms and enable more efficient handling of large, complex environments. Additionally, more efficient training strategies, such as curriculum learning, transfer learning, and distributed training, are essential to mitigate the computational overhead of scaling up learning-based solutions. It is also important to establish comprehensive and standardized evaluation practices that span a broad range of problem scales, ensuring meaningful and reproducible comparisons across different methodologies. Finally, theoretical analysis of the scalability and generalization limits of learning-based approaches would provide valuable insights into their potential advantages and limitations compared to classic techniques.

### Typical Baselines

In this section, we systematically analyze the selection and distribution of baselines in the MAPF literature, drawing insights from both classical and learning-based approaches.

:::: {#fig:classical_baseline_compare .figure latex-placement="htb!"}
![](Wang2025Where_figs/classical_baseline_comparisons_highlighted.png){width="\\linewidth"}

::: caption
Histogram (schematic) illustrating the frequency of classical baseline algorithms used in MAPF experiments. Horizontal axis: baseline names or abbreviations. Vertical axis: number of publications that adopt each baseline for comparison.
:::
::::

#### Baselines in Classical Methods.

A statistical overview of classical baselines is shown in Figure [23](#fig:classical_baseline_compare){reference-type="ref" reference="fig:classical_baseline_compare"}. This histogram demonstrates the frequency with which different classical algorithms are adopted as comparison baselines in MAPF experimental studies. Notably, Conflict-Based Search (CBS) overwhelmingly dominates as the baseline of choice, being cited in more publications than all other methods by a factor of two to four. Other CBS variants---such as SMT-CBS and ECBS---as well as compilation-based solvers like MDD-SAT and PP, follow at a considerable distance. The distribution exhibits a pronounced long-tail characteristic: a small number of methods are routinely compared, while the majority are only sporadically included. It is also worth noting that, in classical MAPF research, learning-based methods are rarely considered as baselines, reflecting a clear methodological divide in the literature.

:::: {#fig:baseline_compare .figure latex-placement="htb!"}
![](Wang2025Where_figs/baseline_comparisons_highlighted.png){width="\\linewidth"}

::: caption
Histogram (schematic) illustrating the frequency of various baseline algorithms used in MAPF experiments. Horizontal axis: baseline names or abbreviations (e.g., CBS, PRIMAL, DHC). Vertical axis: number of publications that adopt each baseline for comparison.
:::
::::

#### Baselines in Learning-based Methods.

Figure [24](#fig:baseline_compare){reference-type="ref" reference="fig:baseline_compare"} extends this analysis to studies proposing learning-based or hybrid MAPF solutions. Here, the long-tail pattern persists, with a few dominant methods---specifically PRIMAL and DHC---being featured in most comparisons. Methods such as SCRIMP, DCC, and PICO also appear with moderate frequency. Importantly, the set of baselines in this category spans both learning-based and classical approaches, with ODrM\* and CBS remaining the most frequently adopted classical algorithms. Among learning-based baselines, PRIMAL stands out as the method of choice, while other highly-cited baselines are predominantly communication-based or reinforcement learning (RL) algorithms. This trend underlines a growing recognition of the value of cross-paradigm comparisons within the MAPF community.

::: sidewaystable
:::

Table [\[tab:baseline_list\]](#tab:baseline_list){reference-type="ref" reference="tab:baseline_list"} provides a structured summary of representative baselines commonly used in MAPF experiments, including brief descriptions and example references.

#### Discussion and Analysis.

A closer examination of these baseline selection patterns reveals several important phenomena. Firstly, the overwhelming preference for CBS and its variants in classical MAPF research underscores its status as the de facto standard for both optimality and interpretability. However, this reliance can obscure the diversity of problem characteristics, particularly in scenarios where CBS's search-based paradigm may not scale efficiently. In contrast, learning-based and hybrid methods, such as PRIMAL and DHC, have established themselves as essential baselines in recent literature, especially for large-scale, partially observable, or dynamically changing environments. The prevalence of these methods illuminates the community's shift towards tackling real-world complexities that challenge traditional solvers.

Interestingly, **the long-tail pattern in baseline selection suggests a lack of standardization and highlights the heterogeneity of experimental settings in MAPF research.** This phenomenon is even more pronounced in learning-based studies, where the choice of baseline is influenced by the target scenario as well as by the computational resources available for large-scale training and evaluation. Moreover, the comparative analysis between independent RL and centralized training/decentralized execution (CTDE) paradigms---exemplified by MADDPG---reflects an ongoing exploration of trade-offs between scalability, coordination complexity, and solution quality. While independent RL is simple and scalable, it often underperforms in highly-coupled MAPF settings. Conversely, CTDE approaches can better capture agent interactions but at the cost of increased training complexity.

In practical terms, most publications select two to three baselines to highlight either (i) the performance gap in large-scale or online scenarios---where classical solvers may fail due to computational bottlenecks, or (ii) the near-optimality of learning-based methods on small- to medium-sized benchmarks, where exact solutions are feasible and serve as a gold standard. Despite these advances, two key limitations persist. First, the dichotomy between classical and learning-based baselines can hinder fair and comprehensive evaluation, especially as hybrid methods become more prevalent. Second, the long-tail distribution of baseline usage complicates cross-paper comparison and meta-analysis, as different studies often report results against disjoint sets of baselines.

To address these issues, future research should strive for more systematic benchmarking protocols, including the adoption of diverse and representative baseline sets across both classical and learning-based paradigms. It is essential to encourage the inclusion of strong learning-based baselines in classical research, and vice versa, to foster cross-paradigm insight. Furthermore, the development of standardized evaluation environments and open-source baseline implementations will enhance reproducibility and fairness in MAPF benchmarking, ultimately accelerating progress in the field.

## Beyond Static MAPF: Dynamic Environment {#subsec:dynamic_mapf}

Despite significant progress in classical MAPF algorithms, the extension of these approaches to dynamic environments remains an open and relatively underexplored research direction. In dynamic MAPF, the environment itself evolves over time, with obstacles appearing or disappearing as agents move or wait. This setting more accurately reflects real-world applications, such as warehouse robotics and urban mobility, where exogenous changes in the map can occur unpredictably and may substantially impact agent coordination.

To systematically assess the robustness of classical MAPF methods under such environmental shifts, we leveraged the POGEMA [@skrynnik2024pogema] benchmark[^7], which facilitates controlled experimentation with varying proportions of dynamic obstacles. Here, a dynamic environment is defined as one in which a certain fraction of obstacles---relative to the total---may appear or disappear as agents interact with the map. This experimental design enables the evaluation of MAPF solvers across a spectrum from static to highly dynamic scenarios.

:::: {#Distribution_Schematic .figure latex-placement="htb!"}
![](Wang2025Where_figs/radar_multiple.png){width=".5\\linewidth"}

::: caption
Results of the evaluation of DCC algorithm in static and dynamic envirnments
:::
::::

Our empirical analysis, summarized in Figure [25](#Distribution_Schematic){reference-type="ref" reference="Distribution_Schematic"}, compares the performance of the DCC algorithm across static and dynamic conditions using a diverse set of benchmark metrics. These metrics include: overall performance on random maps, generalization to out-of-distribution (MovingAI-tiles) maps, scalability with respect to agent count, cooperation efficiency on dense puzzle maps, congestion minimization, and single-agent pathfinding optimality.

The results indicate that classical MAPF algorithms experience a noticeable decline in overall performance as the proportion of dynamic obstacles increases. Specifically, both out-of-distribution generalization and cooperation metrics degrade in more dynamic settings, highlighting the increased difficulty of maintaining effective coordination when the environment is non-stationary. In contrast, the scalability and congestion metrics remain relatively stable, suggesting that these aspects are less sensitive to environmental dynamics, at least under the tested conditions. Notably, the pathfinding metric remains at zero across all settings, reflecting the inability of the current algorithm to find optimal solutions even in the single-agent case under dynamic constraints.

These findings underscore the urgent need for principled algorithmic advances in dynamic MAPF. Future research should prioritize the development of solvers that can adapt in real time to environmental changes, possibly by integrating online learning, predictive modeling of obstacle dynamics, or robust planning under uncertainty. Furthermore, new benchmarks and evaluation protocols---such as those enabled by POGEMA---will be essential for tracking progress and establishing reliable baselines in this challenging domain. Ultimately, bridging the gap between static and dynamic MAPF remains a critical step toward deploying multi-agent planning systems in complex, real-world environments.

# Future Work {#sec:future}

As MAPF continues to evolve in both classical and learning-based paradigms, several promising research directions are emerging to address the increasing complexity, dynamism, and heterogeneity of real-world applications. In this section, we outline key avenues for future investigation, ranging from mixed-motive and generative MAPF to language-grounded planning, collision-informed frameworks, large-scale agent coordination, neural solver integration, formal verification, and adaptation to dynamic environments. Each subsection discusses open challenges and potential methodologies, aiming to provide a roadmap for advancing the theoretical and practical boundaries of MAPF research.

## Mixed-Motive MAPF

Traditional MAPF formulations typically presume that all agents adhere to a single global objective or, at minimum, have no direct incentives to stray from the centrally prescribed collision-free plan. This assumption, though compatible with single-organization settings, is less valid when agents belong to separate stakeholders or hold private goals and constraints [@friedrich2024scalable; @he2024social]. A promising line of inquiry thus lies in mechanism design [@kollock1998social] and information design [@dughmi2016algorithmic], whereby the MAPF engine not only imposes combinatorial collision-avoidance rules but further orchestrates how agents reveal their preferences, how resource usage is priced or compensated, and how incentives unfold under partial information or strategic misreporting. In such scenarios, agents can, for instance, exaggerate the cost of diverting around congested corridors or withhold crucial timing details about resource availability. Disentangling this strategic complexity involves carefully crafting the "rules of the game" (mechanism design) alongside the "rules of communication" (information design) so that rational agents ultimately converge upon collision-free, cost-effective routes.

On the mechanism design side, one can embed proven approaches such as Vickrey--Clarke--Groves into classical methods like conflict-based or priority-based search, effectively transforming each conflict resolution or priority assignment into a small "auction," where agents bid or signal valuations of potential paths. This process relies on transfer payments or side payments to disincentivize blocking maneuvers or the withholding of crucial route information. However, layering mechanism design onto conflict-splitting or meta-agent merging poses novel algorithmic questions: each branching step could redistribute payoffs to reflect the combinatorial implications of agent conflicts, and the complexity of running repeated auctions in large MAPF instances may grow quickly unless the solver intelligently prunes or aggregates conflict sets. Bridging domain-specific heuristics (e.g., corridor constraints, target symmetries) with the incentive rules thus becomes critical for tractable deployment.

In parallel, information design tactics can address the reality that agents might not wish to share complete data on their start times, fuel costs, or future tasks. Revealing too much can expose sensitive business operations, but revealing too little can lead to wasted capacity or collisions in heavily trafficked areas. One avenue is to devise partial revelation policies, whereby high-level conflict signals (such as approximate arrival times or corridor usage) are disclosed, while private valuations or exact cost structures remain hidden. Such partial information can be channeled through multi-agent reinforcement learning modules, which learn how to integrate coarse signals into bidding or negotiation schemes without requiring every detail of an agent's internal state. This is particularly relevant in dynamic or partially observable environments, where continuous-time updates or abrupt schedule changes make full disclosure impossible or undesirable.

Learning components can further refine these mechanism- and information-aware protocols by adapting them to empirical agent behaviors in large-scale or rapidly changing contexts. A reinforcement learner, for instance, might observe trends in how certain conflict auctions are repeatedly won or lost and adjust cost functions or penalty structures so that no single agent has disproportionate power to stall or block traffic. Equilibrium-based MARL techniques can incorporate game-theoretic analyses---ensuring that collision-free outcomes remain stable against unilateral deviations---while exploiting data-driven training signals to handle highly non-stationary conditions [@yang2020learning; @lin2023information]. The interplay between classical branching heuristics, incentive-compatible pricing, and partial information sharing thus presents a rich field for new theoretical models and practical implementations. Ultimately, these research aim to produce MAPF solvers that not only rule out collisions but also account for strategic considerations and incomplete information, enabling robust and efficient multi-agent coordination where full cooperation cannot be taken for granted.

## Generative MAPF

Generative modeling offers a fundamentally different perspective on MAPF compared to classical search-based algorithms. Instead of navigating a collision-free solution space incrementally, one trains a diffusion-based or flow-based model to sample entire spatio-temporal agent trajectories simultaneously [@liang2024multi; @shaoul2025multirobot; @andreychuk2025mapf]. Diffusion models, for instance, learn to reverse a progressive noise-injection process, thus mapping random noise to structured outputs [@ho2020denoising]; in a MAPF context, each output would encode a multi-agent solution capturing both temporal dependencies (when agents move) and spatial constraints (which routes they follow). While collisions may not be strictly eliminated at generation time, the training process can steer the learned distribution toward more feasible configurations by incorporating approximate collision penalties or domain-aligned regularizations. Upon deployment, a batch of trajectories is sampled in parallel and can be quickly post-processed by classical MAPF methods such as conflict-based or acceptance--rejection checks. This two-stage pipeline rapidly explores a diverse space of solutions while preserving the guarantees of collision resolution.

Normalizing flows provide a complementary approach, in which an invertible transform maps a simple base distribution to the manifold of agent paths [@papamakarios2021normalizing]. By carefully designing coupling layers to partition or reorder spatial and temporal coordinates, one can embed approximate collision-avoidance hints directly in the architecture. Although enforcing strict feasibility within these flows is non-trivial due to highly non-linear collision constraints, such biases can reduce the burden on subsequent classical search or local repair. Moreover, controlling the likelihood of a sample allows the solver to prioritize those paths the model deems more probable under the learned distribution, potentially improving efficiency when large agent teams are present.

Another avenue of research concerns how these generative processes can adapt in real time. In-context learning [@xie2022an] and meta-learning [@finn2017model] mechanisms suggest that once a generative model has learned a broad "prior" over multi-agent trajectories (possibly from diverse environments or partial solver outputs), it can refine its sampling behavior when presented with a small set of example configurations from the current scenario. Rather than retraining from scratch, the model conditions on these examples to better accommodate new obstacles, agent dynamics, or unexpected start--goal patterns. If collisions arise even after adaptation, domain knowledge from classic MAPF remains essential for final adjustments like corridor conflict splitting or priority-based local repairs. This synergy underscores how generative modeling should not stand alone but instead integrate with core MAPF heuristics, ensuring robust feasibility checks and the ability to fine-tune solutions for complex domains.

Future investigations must probe deeper into how to embed domain constraints directly into the generative process, thereby reducing the reliance on ad hoc collision penalties and post-hoc rejigs. One possibility is to incorporate differentiable approximations of collision detection---enabling gradient-based updates that actively push sampled paths away from high-conflict regions---or to engineer flow-based layers that inherently separate agent trajectories across time steps [@christopher2024constrained]. Another research direction would explore advanced diffusion variants [@de2021diffusion], such as diffusion probabilistic fields [@zhuang2023diffusion], in which spatio-temporal dependencies are represented more flexibly and can be more directly aligned with grid- or graph-based MAPF formulations. Further, collecting training datasets that reflect diverse conflict scenarios---rather than a narrow subset of feasible solutions---will enhance the model's capacity to handle previously unseen, highly congested conditions. Ultimately, generative methods for MAPF promise to balance global exploration with established collision-avoidance paradigms, providing a rich ground for algorithmic breakthroughs that blend the creativity of deep generative sampling with the reliability of classical solver principles.

## Language-Grounded MAPF

The emergence of large language models presents novel opportunities to significantly broaden the methodological landscape of MAPF planning, both in classical and learning-based paradigms. From the perspective of classical algorithms, many established methods rely heavily on carefully tailored heuristics or branching strategies. Instead of manually designing these components, one may employ an LLM-driven meta-search process such as a FunSearch-like framework [@romera2024mathematical; @liu2024evolution] that synthesizes and refines new heuristics through evolutionary computation and language-guided reasoning. The key idea is to let the LLM propose candidate heuristic formulas or conflict-splitting schemes based on descriptive natural-language prompts, then automatically evaluate and evolve them within the MAPF setting, continually searching for high-quality or domain-specific strategies that outperform static hand-designed approaches.

In a learning-based context, LLMs can serve more directly as a policy generator by leveraging their built-in commonsense and reasoning abilities to propose agent moves or path expansions [@zeng2024perceive; @chen2024solving; @atasever2025multiagent; @seo2025llmdr]. Combined with "tool-using" functionalities, the LLM could offload subproblems---such as temporarily resolving tight collisions or revalidating partial solutions---to external classical solvers. In this way, the language model orchestrates a hybrid workflow where parts of the MAPF pipeline remain driven by exact or bounded-optimal algorithms, yet the overall agent behavior is flexibly guided by the LLM's adaptive priors, effectively lowering the barrier to tackling new or unstructured constraints. Extending this further, an agentic workflow approach would allow the LLM itself to manage parallel requests, re-planning triggers, or conflict merges and splits as circumstances evolve in real time. By respecting key MAPF constraints while drawing on the LLM's substantial capacity for semantic understanding and multi-step reasoning, the framework might scale seamlessly to more complex scenarios and dynamic constraints than purely algorithmic or purely data-driven methods could feasibly address.

The transformative potential of these LLM-integrated approaches lies in their ability to expand the boundaries of MAPF. With advanced language understanding, it becomes feasible to incorporate ambiguous or high-level directives (such as safety zones, time windows, or ethical guidelines) into a single integrated solver pipeline [@10903304]. LLMs also invite us to rethink the granularity and scope of MAPF: Instead of limiting research to discretized, grid-centric formulations, a language-grounded system could harmonize classical domain representations with higher-level, continuously updated knowledge about tasks, agent roles, and mission objectives, stepping beyond short-horizon collision avoidance toward richer multi-agent orchestration. By trusting in the surprising range of LLM capabilities and experimenting with nontrivial orchestration workflows, researchers and practitioners alike can seek to solve more ambitious MAPF tasks that were previously deemed too complex to formalize or too large to handle through conventional techniques alone. Ultimately, rather than producing standalone solutions, the richness of LLM-based MAPF encourages a more systematic synergy, emphasizing the interplay between evolutionary search, language-driven policy design, exact verification, and multi-agent adaptation to create a new generation of MAPF solvers unconstrained by traditional boundaries.

## Collision-Informed MAPF

A promising research avenue lies in reconciling the discrete foundations of classical MAPF methods with the continuous safety and collision-avoidance constraints prevalent in real-world robotics. One approach is to incorporate geometric barrier functions, partial differential equations, or other collision-informed constraints directly into the neural architecture so that collision-free behavior is maintained throughout training and inference [@raissi2019physics; @liu2024physics]. By encoding these constraints into the underlying policy or trajectory generator, it becomes feasible to guarantee adherence to physical safety margins and dynamic feasibility conditions without requiring explicit post-processing steps. This integration can be particularly powerful when paired with classic search-based planners (such as CBS or LNS), where the discrete expansions would co-exist with learned, collision-aware modules that efficiently navigate continuous dynamics or partial observability.

A second direction is to leverage specialized neural architectures that exhibit symmetry or equivariance properties consistent with MAPF tasks. Many multi-agent grid-based environments enforce uniform motion rules and relative positioning constraints that could be captured by group-equivariant neural networks or graph neural networks [@satorras2021n; @gerken2023geometric]. These architectures can be further tailored by incorporating insights from domain decomposition and agent grouping used in priority- or constraint-based algorithms. They would thereby preserve the interpretability of classical methods and simultaneously harness data-driven generalization. An additional refinement would involve neural architecture search (NAS) to automatically discover task-specific architectures that effectively balance expressive power and computational overhead, ensuring scalability to large agent counts and continuous-time maneuvers [@zoph2017neural; @elsken2019neural].

Furthermore, there is growing interest in formally verifying learned neural modules so as to provide correctness guarantees under a wide range of deployment scenarios. If the policy or planner can be represented symbolically, formal methods could systematically check whether collision-free paths are produced for all valid agent configurations and environment states within specified bounds [@sun2019formal; @ehlers2017formal; @corsi2021formal]. Although bridging neural networks with rigorous verification poses nontrivial algorithmic and computational hurdles, recent progress in combining solver-based techniques (e.g., SMT, MIP) with neural certificate generation offers a glimpse into how collision-free properties can be mathematically assured [@katz2017reluplex; @eleftheriadis2022neural]. Such integrative solutions would not only raise confidence in the deployment of learned MAPF systems but also illuminate potential failure modes that can guide subsequent network architecture revisions.

## Many-Agent Pathfinding

As agent teams grow to hundreds or even thousands of individuals, contemporary MAPF solutions struggle to balance real-time responsiveness with global collision guarantees. Traditional centralized algorithms excel in principled conflict resolution but often exhibit superlinear computation times as the agent count rises. Purely data-driven approaches, while adaptable to large heterogeneous environments, risk overlooking worst-case collisions if not carefully constrained. A productive research direction is thus to integrate classic multi-level MAPF formulations with newly emerging theoretical and learning-based insights, providing a unifying framework capable of scaling to ultra-large agent populations.

One promising avenue is to adopt a hierarchical decomposition approach at multiple levels of granularity, dividing the environment into manageable regions connected by well-defined interfaces [@zhang2021hierarchical; @lee2021parallel]. While classical corridor reasoning or disjoint splitting can handle local collisions effectively, significant open questions remain in how to maintain global consistency across inter-region boundaries. This challenge can be tackled by refining high-level conflict-detection schemes or priority-based synchronization protocols, which ensure that independently computed subsolutions do not generate collisions when merged. Crucially, learning-based modules can be incorporated to predict congestion patterns or to re-partition regions on the fly, especially under dynamic task assignments. In this scheme, each layer could exploit classical completeness and optimality checks, but rely on data-driven components for decisions such as how to group agents, when to initiate re-routing, or which regions can be safely skipped during intermediate conflict detection. Successfully merging these components requires developing robust meta-planning algorithms that preserve collision-free guarantees yet adapt to shifting agent distributions or high-density bottlenecks at runtime.

Another prospective direction involves leveraging the mean-field or other large-population theories to characterize coordination as an aggregate phenomenon, especially when detailed one-to-one interactions become computationally intractable [@yang2018mean; @park2024mean]. While mean-field approximations can mitigate dimensionality issues by focusing on ensemble behavior, a key research hurdle is to ensure the resulting macroscopic analysis remains relevant to discrete collision checks and agent-level path constraints. Coupling such theoretical frameworks with localized collision resolution demands creative approximations or hybrid models that reconcile continuous-density abstractions with discrete pathfinding. For instance, machine learning could aid in periodically mapping dense agent flows onto collision-aware graph abstractions, yielding a fluid-to-discrete handover that maintains tractable solution spaces. These research efforts could invoke domain-crossing methods from network flow theory, computational physics, or distributed control, thereby pushing MAPF toward a unified methodology that simultaneously handles micro-level path feasibility and macro-level congestion effects.

Beyond algorithmic advances, there is considerable room for cross-disciplinary systems integration and real-world validations. In large-scale robotics or warehouse logistics, where thousands of mobile units operate simultaneously, the interplay of hardware limits and safety requirements adds layers of complexity. Investigating parallel computing paradigms or distributed ledger technologies may uncover efficient ways to coordinate agent subgroups and encode conflict resolution constraints at scale. Leveraging cloud-based or high-performance computing resources might enable near real-time solutions for ultra-large MAPF instances, while novel concurrency control strategies can address synchronization overheads in a distributed environment. Integrating these systems-level solutions with hierarchical or mean-field formulations holds the potential to move from purely theoretical frameworks toward reliable, large-scale industrial deployments.

## Neural MAPF Solver

A promising extension of current compilation-based methods for MAPF lies in the integration of neural solvers that harness recent progress in deep learning for combinatorial optimization. Classical approaches that convert MAPF into SAT, SMT, CSP, ASP, or MIP formulations typically rely on general-purpose solvers with hardcoded branching heuristics and conflict resolution strategies. While such solvers have matured significantly, they often lack adaptability to domain-specific structures in MAPF, such as dynamic collision-avoidance patterns or the distinct bottlenecks introduced by dense agent populations. Neural solvers, in contrast, can learn search policies, branching rules, or cut-generation heuristics tailored to these very properties, thus offering a new level of flexibility and problem-awareness [@sun2018learning; @chen2022learning].

One key research direction is the design of differentiable solver components that incorporate learned embeddings of MAPF constraints [@ryu2019plug; @sun2021scalable]. By embedding agents' spatiotemporal interactions and collision constraints into deep neural architectures, one could enable backpropagation of solution-quality signals through the solver's decision pipeline. This approach might draw inspiration from graph neural networks or Transformer-based models, where the nodes represent time-indexed agent states and the edges capture conflict relationships. Iterative message-passing schemes could then identify tight collision sets or promising feasible transitions, guiding the solver toward near-optimal solutions more quickly than generic combinatorial methods.

Another direction is the development of neural heuristics for column generation or conflict-driven clause learning. In a MIP setting, candidate path "columns" that fail to meaningfully reduce conflicts might be pruned early by a learned ranking function, allowing the solver to focus on highly efficacious routes. In a SAT or SMT framework, learned conflict-clause generation could allow the solver to incrementally add only the most potent constraints, rather than enumerating a large swath of collisions indiscriminately. Such targeted addition would reduce solver overhead and produce solutions that reflect context-aware collision avoidance. These techniques may benefit from large-scale pretraining on diverse MAPF scenarios, enabling models to learn broad priors about collision structure and thematically consistent path flows.

A further challenge in neural solver integration is accommodating the idiosyncrasies of MAPF, such as highly heterogeneous agent goals, domain-specific resource constraints, and multi-objective cost structures. Where standard neural combinatorial optimization often focuses on uniform problem setups, MAPF tasks can vary significantly in complexity and could include partial observability or on-the-fly environment changes. Building robust neural solvers that adapt to these variations requires layering explicit MAPF constraints over trainable solver components [@bengio2021machine; @mazyavkina2021reinforcement]. Coupling domain knowledge---like joint collision checks and known bottleneck patterns---with learned strategies for branching or constraint propagation offers a fertile research path. This synergy, if pursued systematically, has the potential to move beyond single-paper demonstrations and establish a coherent body of work on neural solver design for MAPF.

Finally, an important strand of future research concerns theoretical validation and practical deployment [@martin2024learning]. Neural solvers can reduce runtime while discovering high-quality solutions that classical solvers might overlook. However, guaranteeing completeness or bounding potential suboptimality can be challenging when the solver's decision logic is partially determined by learned modules. Techniques derived from explainable AI and formal verification may be adapted to certify the correctness of neural "subroutines," ensuring that they do not violate MAPF's fundamental collision-avoidance requirements. This interplay of data-driven guidance and rigorous solver-level checks embodies a broader "AI for Science" ambition, wherein machine learning and symbolic search unite to tackle complex multi-agent coordination problems with unprecedented speed and reliability. By actively addressing these verification and validation questions, neural solvers for compilation-based MAPF could achieve both strong practical performance and robust theoretical assurances.

## Automated MAPF Proving

A promising avenue for advancing both classical and learning-based MAPF methods is the integration of automated theorem proving (ATP) frameworks, such as Lean4, with state-of-the-art machine learning techniques [@moura2021lean; @wang2024theoremllama]. Classical MAPF solvers, which strive for optimality or completeness guarantees through explicit search, stand to benefit from formal verification strategies that ensure the correctness of algorithmic steps and collision-avoidance proofs. In particular, encoding these algorithms in Lean4 could help verify key properties of conflict resolution, priority assignments, or subproblem-specific constraints, thus yielding robust correctness certificates and facilitating the discovery of overlooked corner cases. Such certified correctness has the potential to substantially accelerate the development cycle for classical methods by enabling rapid prototyping, rigorous debugging, and targeted refinements through machine-assisted proofs.

At the same time, learning-based approaches for MAPF, including deep neural planners, Large Neighborhood Search (LNS) heuristics guided by data-driven models, or reinforcement learning policies with partial observability, may similarly benefit from an ATP perspective [@zhang2025understanding; @li2025formalization]. Although most learning pipelines offer no hard completeness or optimality guarantees, it is conceivable to couple them with Lean4 reasoning modules that analyze candidate policies to ensure adherence to baseline collision-free constraints or to produce counterexamples when violations occur. This integration would require extending the expressiveness of Lean4 libraries to capture the specific temporal and spatial properties of multi-agent coordination, as well as devising pragmatic methods for encapsulating learned heuristics as logical axioms or hypotheses. By codifying the interactions between data-driven modules and the underlying MAPF rules, one could systematically identify when learned models are falling outside valid solution spaces.

Such a synthesis could also open a path for hybrid verification strategies, where a learning-based or classical solver generates candidate solutions that are then incrementally refined through symbolic reasoning. For instance, if a partial solution passes initial semantic checks in Lean4 but triggers unresolved proof obligations, a learning-based method might attempt localized corrections, or the classical solver might apply constraint-splitting techniques guided by the theorem prover's feedback. This bidirectional workflow could form a self-correcting loop, offering stronger completeness assurances while still harnessing the scalability of machine-driven exploration. Looking beyond near-term implementations, one might further explore how these formal verification pipelines can incorporate emerging advances in automated proof search, including LLM-based theorem provers or interactive proof systems that accept high-level domain insights from MAPF practitioners. By intertwining automated theorem proving, classical MAPF theory, and learning-based heuristics within a single ecosystem, future research can aspire to create rigorously verified solvers that remain adaptable to the multifaceted and ever-evolving challenges of real-world multi-agent coordination.

# Related Work {#sec:related}

Owing to the importance of MAPF in robotics, logistics, and numerous other sectors, the research community has produced an extensive array of surveys over the last few years. On the classical side of MAPF, several works have established foundational terminology, formulations, and categorizations, covering search-based, rule-based, and compilation-based algorithms for grid-based and other graph formulations [@stern2019multi; @stern2019mapfsurvey; @wu2023review; @ma2022graph; @gao2024review; @yang2023path; @salzman2020research; @tjiharjadi2022systematic; @zhou2023research]. These surveys focus on the central challenge of achieving collision-free paths for multiple agents, providing overviews of optimal and suboptimal pathways such as conflict-based search (CBS), reduction-based formulations (SAT, MILP, CSP), priority-based heuristics, and decoupling techniques. They also highlight real-world applications, enumerating key issues like scalability, dynamic constraints, and conflicting objectives.

A second category of surveys has emerged with the explicit aim of incorporating machine learning into MAPF. This line of work examines RL, imitation learning, and other learning paradigms geared toward approximate or decentralized controllers [@chung2024learning; @alkazzi2024comprehensive; @yakovlev2022planning; @yang2023path; @zhou2023research]. While such surveys effectively showcase the flexibility and adaptability of data-driven approaches, they often concentrate on a narrower set of techniques---primarily modern deep RL or policy-based algorithms---and typically offer less extensive coverage of classical techniques for large-scale problems. Problem compilation surveys form a separate, more specialized niche. These works discuss how MAPF can be encoded into Boolean satisfiability, integer linear programs, constraint satisfaction, or SMT [@surynek2022problem], underscoring how such transformations leverage efficient solver to achieve high solution quality.

More recent surveys have begun to merge perspectives by discussing beyond-classical scenarios, such as handling heterogeneous agents, tasks with temporal or resource constraints, and real-time or partially observable systems [@tjiharjadi2022systematic; @ma2022graph; @gao2024review; @yang2023path]. Some of these reviews expand the scope to include multi-agent pickup and delivery, continuous-space motion planning, and swarm robotics [@salzman2020research; @yakovlev2022planning], providing valuable insights on how MAPF can be adapted to more complex or realistic domains. Nonetheless, in many of these works, discussions of learning-based methods are presented independently from the traditional MAPF literature, offering limited guidance on how the two paradigms might reinforce each other.

In contrast to prior surveys, our paper offers a more unified treatment of MAPF. First, we bridge classical and learning-based approaches in a single cohesive framework, systematically examining the strengths and weaknesses of search-based and compilation-based methods alongside a spectrum of data-driven algorithms (including RL, imitation learning, evolutionary techniques, and large language model approaches). Second, we link the theoretical underpinnings of classical MAPF---e.g., guarantees on optimality and completeness---with the adaptivity afforded by learning-based approaches in uncertain and dynamic environments. This integration, which remains underexplored in previous reviews, underscores opportunities for synergy, such as replacing classical heuristic modules with learned policies or combining classical back-ends with representation learning for improved scalability. Third, unlike earlier works that frame empirical analyses in domain-specific terms, we provide a comparative study of experimental design across both classical and learning-based methods, shedding light on how the choice of map type, agent population, performance metrics, and baseline comparisons significantly affects reported outcomes.

Overall, we position our survey as an effort to build on and extend existing literature. We not only synthesize mature methods from decades of MAPF research but also draw attention to recent data-driven trends and novel hybrid solutions. In doing so, we aim to inspire fresh lines of inquiry that promote a holistic view of MAPF. By consolidating diverse approaches under a single umbrella and emphasizing rigorous benchmarking and real-world applicability, our survey advances the field beyond established boundaries, thereby offering practical guidance to both academic researchers and industrial practitioners.

# Conclusion

This survey has provided a comprehensive examination of Multi-Agent Path Finding, systematically bridging the traditionally separate domains of classical algorithmic approaches and modern learning-based methods. Through our analysis, several key insights have emerged that shape our understanding of the current state and future trajectory of MAPF research.

**Synthesis of Key Findings.** Our investigation reveals that MAPF has evolved far beyond its origins as a purely theoretical problem. Classical methods, exemplified by Conflict-Based Search and its variants, have achieved remarkable scalability---routinely handling thousands of agents while maintaining optimality guarantees. These approaches embody decades of algorithmic refinements, from sophisticated heuristics and symmetry reasoning to mutex propagation and disjoint splitting. Compilation-based methods have similarly matured, leveraging powerful general-purpose solvers to transform MAPF into well-studied formalisms. However, these classical approaches often struggle with real-time constraints, dynamic environments, and partial observability---precisely the scenarios where learning-based methods excel.

The emergence of data-driven approaches has introduced new possibilities for adaptive, robust multi-agent coordination. Reinforcement learning methods, particularly those employing multi-agent frameworks with communication protocols, have demonstrated the ability to discover emergent coordination strategies that classical planners might overlook. Yet our analysis also reveals a surprising paradox: despite claims of superior scalability, learning-based methods are predominantly evaluated on smaller problem instances than their classical counterparts, rarely exceeding a few hundred agents or modest grid sizes.

**The Promise of Integration.** Perhaps the most significant contribution of this survey is highlighting the vast, underexplored potential for synergy between classical and learning paradigms. Learning-augmented classical solvers represent a particularly promising direction, where data-driven components enhance specific modules (conflict selection, node prioritization, neighborhood destruction) while preserving the theoretical scaffolding that ensures completeness and bounded suboptimality. This hybrid approach exemplifies a broader principle: rather than viewing classical and learning-based methods as competing paradigms, the field benefits most when they are seen as complementary tools in a unified toolkit.

**Methodological Implications.** Our systematic analysis of experimental practices reveals critical gaps in current evaluation methodologies. The lack of standardized benchmarks, inconsistent metric reporting, and limited cross-paradigm comparisons hinder progress and make it difficult to assess the true capabilities of different approaches. We advocate for comprehensive evaluation protocols that span both theoretical guarantees and empirical performance, encompassing diverse environment types, varying agent densities, and realistic dynamic constraints. Only through such rigorous benchmarking can the community make informed decisions about which methods to deploy in specific application contexts.

**Future Outlook.** Looking ahead, MAPF research stands at an inflection point. The integration of large language models, generative approaches, and neural solver architectures promises to expand the boundaries of what is computationally feasible. Mixed-motive settings that incorporate game-theoretic considerations reflect the reality of multi-stakeholder systems. Collision-informed frameworks that embed safety constraints directly into neural architectures address critical deployment concerns. As MAPF applications extend to thousands or even millions of agents in smart cities and large-scale logistics networks, hierarchical and mean-field approaches will become essential.

**Final Remarks.** The journey from theoretical foundations to practical deployment of MAPF solutions exemplifies the evolution of AI research more broadly. What began as a discrete optimization problem on simple grids has expanded to encompass continuous domains, dynamic environments, heterogeneous agents, and complex real-world constraints. By providing this comprehensive survey that unifies classical and learning-based perspectives, we hope to accelerate progress toward robust, scalable, and intelligent multi-agent coordination systems. The future of MAPF lies not in choosing between classical rigor and learning-based flexibility, but in creatively combining their strengths to address the increasingly complex challenges of autonomous multi-agent systems in our interconnected world.

[^1]: The first two authors contribute equally.

[^2]: Corresponding authors: Xiangfeng Wang and Wenhao Li.

[^3]: In time-discretized settings, $\mathrm{Cost}(\pi_i)$ often equals the number of time steps until agent $i$ reaches $g_i$.

[^4]: One might equivalently model [\[eq:collision-edge\]](#eq:collision-edge){reference-type="eqref" reference="eq:collision-edge"} as constraints disallowing $x_{i,u,t} = x_{j,v,t}$ and $x_{i,v,t+1} = x_{j,u,t+1}$ for $(u,v)\in\mathcal{E}$. The form above simply encodes that at most three of these four binary variables can be $1$.

[^5]: A conflict could also arise if both agents tried to occupy the same cell. The resolution mechanism is similar.

[^6]: Strictly speaking, each agent took 3 moves to reach the goal. Another counting convention might yield a sum of $(3 + 3)=6$. The main point is that the total cost remains feasible.

[^7]: <https://github.com/CognitiveAISystems/pogema-benchmark>.
