---
citation_key: Zhang2023Flexible
arxiv_id: 2310.12828
arxiv_url: https://arxiv.org/abs/2310.12828
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:08:49Z
origin: ai+web
reviewed: false
---

# Introduction

Path planning is essential in robotics, autonomous driving, game design, and related fields. Early methods like Dijkstra's algorithm [@dijkstra1959note] found the shortest path in a graph, while A\*[@hart1968formal] integrated graph and heuristic search for faster pathfinding. Anytime Repairing A\* (ARA\*)[@likhachev2003ara] offers progressive solutions during execution, catering to real-time scenarios with its *Anytime* feature. Its *Repairing* aspect also refines solutions by adjusting search parameters and balancing speed and quality.

Using graph-based planning in continuous state spaces is challenging due to the need for suitable discretization, known as *prior discretization*. Coarse resolution boosts efficiency but may yield suboptimal paths. Finer resolution improves path quality [@bertsekas1975convergence] but demands exponentially more computation, especially in high-dimensional environments, which are known as *the curse of dimensionality* [@bellman1957dynamic]. To tackle this issue, sampling-based planning methods like Rapidly-exploring Random Trees (RRT)[@lavalle2001randomized] and Probabilistic Roadmaps (PRM)[@kavraki1996probabilistic] construct feasible paths by randomly sampling vertices in the *configuration space* (*$\mathcal{C}$-space*) and connects samples using local planners with collision checks. These approaches are suitable for high-dimensional and narrow environments.

:::: {#fig: darko_setup .figure latex-placement="t"}
::: caption
FIT\* on mobile manipulator robot during a real-time pull-out and place task in supermarket cell (Section [6.2](#subsec:realExpri){reference-type="ref" reference="subsec:realExpri"}).
:::
::::

Efficient pathfinding with high-dimensional *$\mathcal{C}$-space* in an incremental planner hinges on balancing exploration and exploitation. Batch Informed Trees (BIT\*)[@gammell2015batch; @gammell2020batch] compactly groups states into an implicit *random geometric graph* (RGG)[@penrose2003random], employing step-wise search akin to Lifelong Planning A\* (LPA\*)[@koenig2004lifelong] based on expected solution quality. Advanced BIT\* (ABIT\*)[@strub2020advanced] uses inflation and truncation factors to balance the exploration and exploitation of an increasingly dense RGG approximation. Adaptively Informed Trees (AIT\*)[@strub2022adaptively; @strub2020adaptively] utilized an asymmetrical search method with sparse collision checks in the reverse search. Effort Informed Trees (EIT\*)[@strub2022adaptively], a state-of-the-art planner uses admissible cost (i.e., lower bound on the true value) and effort heuristics to enhance its capability to tackle intricate scenarios, particularly in objectives with obstacle clearance, which is not estimable with the Euclidean distance heuristic. However, these planners lack adaptability in selecting an optimal batch size during the planning process. Optimizing batch size is advisable, considering variations among robots, scenarios, dimensions, and state spaces. Fewer samples might lower the probability of sampling vertices in narrow corridors. After the informed set (Fig. [2](#fig: elipse){reference-type="ref" reference="fig: elipse"}) contracts, more samples might lead to a more time-consuming edge check. This limitation hampers overall planning efficiency[@gammell2020batch].

This paper presents Flexible Informed Trees (FIT\*), which integrates the strengths of both *search strategies* and *approximation techniques*. FIT\* aims to integrate adaptive batch-size features to tackle wall gap challenges and efficient planning. By employing decay-based sigmoid functions to leverage the decay factor for dynamic batch size adjustments, a smoothing operation is integrated to prevent large differences in resizing steps while maintaining optimality. This integration enhances the efficiency of the approximation process.

The practical efficacy of FIT\* has been thoroughly demonstrated through real-world applications, as depicted in Fig. [1](#fig: darko_setup){reference-type="ref" reference="fig: darko_setup"} and [5](#fig:simulation){reference-type="ref" reference="fig:simulation"}. We evaluated autonomous mobile manipulator navigation performance. Its adaptability in dynamically adjusting batch sizes during optimization demonstrated notable enhancements in computational time efficiency and solution quality. FIT\* addresses the limitations of existing informed heuristic sampling-based algorithms by computing appropriate batch size during path optimization. FIT\* proposed a potential research direction, especially in dealing with densely populated settings. The effectiveness of FIT\* underlines its potential in autonomous robotics and path planning.

The contributions of this work are summarized as follows:

- *Efficient initial pathfinding*: FIT\*'s dense sampling strategy in the initial pathfinding phase tackles difficult-to-sample regions problem, reducing the initial pathfinding time in various test environments up to approx. 24%.

- *Batch sampling frequency*: The sparse sampling strategy in the path-optimized phase benefits the search process by frequently sampling points in the informed set. Leads to a higher probability of sampling *key* points.

- *Adaptability to confined environments*: FIT\* was tested in real-world applications, including mobile manipulator pull-out and place tasks in narrow spaces. FIT\* showed a 27.78% solution cost reduction in experiments.

# Related Work

In sampling-based motion planning, two distinct strategies are introduced for sampling vertices in the *$\mathcal{C}$-space*: *Dense sampling* and *Sparse sampling* (Fig. [3](#fig: BatchSize){reference-type="ref" reference="fig: BatchSize"}). Dense sampling entails generating more samples per batch, thereby increasing the likelihood of including critical vertices within narrow corridors (key sample areas). However, dense sampling demands more time for constructing the RGG, elongating the duration required for edge checking. On the contrary, sparse sampling involves generating fewer samples per batch, thereby expediting the construction of RGG and reducing the time needed for edge checking. Nonetheless, this approach entails a trade-off, as it diminishes the likelihood of sampling vertices within key sample areas. Despite this trade-off, sparse sampling accelerates the edge-checking process, facilitating a quicker transition to subsequent sampling iterations.

:::: {#fig: elipse .figure latex-placement="t!"}
::: caption
The 2D representation of hyperellipsoid, its shape is determined by the start, goal states, and two key costs: the theoretical minimum cost $l_\text{min}$ and the current best solution cost $l_\text{curr}$. The eccentricity of the hyperellipsoid is given by the ratio $l_\text{min}/l_\text{curr}$ [@gammell2014informed].
:::
::::

Effective motion planning involves striking a balance between *exploration* and *exploitation*. Overemphasizing exploration wastes time mapping the environment without progressing toward the goal, while excessive exploitation may overlook superior solutions [@karaman2011sampling]. Exploring/Exploiting Trees (EET) [@rickert2008balancing] aim to strike this balance by integrating gradient information. RRT-Connect extends RRT to efficiently find a path between two points in $\mathcal{C}$-space by utilizing two RRTs to connect start and goal states. RRT\* [@karaman2011sampling] enhances efficiency and optimality by incrementally constructing a tree from an initial state. Informed-RRT[@gammell2014informed] and Smart-RRT [@nasir2013rrt], extensions of RRT, use heuristics or informed sampling (Fig. [2](#fig: elipse){reference-type="ref" reference="fig: elipse"}) to guide state space exploration, biasing sampling towards regions likely to contain the optimal path. Lazy-PRM [@bohlin2000path] improves roadmap construction by deferring collision checking until necessary.

BIT\* is a sampling-based planner designed to achieve almost-surely asymptotic optimality. It utilizes a *batch processing approach*, takes numerous state batches and approximates as a progressively denser edge-implicit RGG. It optimizes the tree structure iteratively to minimize computational overhead. EIT\* and AIT\* consist of forward edge build and reverse search to employ distinct heuristic approaches for pathfinding. AIT\* excels in precision by updating its heuristic with high accuracy to match the ongoing approximation. EIT\* is built on BIT\* and uses effort as an additional heuristic function to estimate the collision check of the edges. In contrast, EIT\* focuses on optimizing the pathfinding process by utilizing the count (e.g. *number of collision checks*) as an effort estimate heuristic, leading to efficient path discovery. Through iterative optimization, they approximate a near-optimal path, effectively balancing exploration and exploitation for efficient robot navigation.

## Ellipsoid in high-dimensional space

An ellipsoid in an $n$-dimensional Euclidean space $\mathbb{R}^n$ is defined as the locus of all points $\mathbf{x}$ that satisfy the equation: $$\begin{equation}
    \left( \frac{x_1}{v_1} \right)^2 + \left( \frac{x_2}{v_2} \right)^2 + \cdots + \left( \frac{x_n}{v_n} \right)^2 = 1,
\end{equation}$$ Where $\mathbf{x} = (x_1, x_2, \ldots, x_n)$ represents the coordinates of a point on the ellipsoid, and $\mathbf{v} = (v_1, v_2, \ldots, v_n)$ is a given vector in $\mathbb{R}^n$. The components of the vector $\mathbf{v}$ correspond to the lengths of the semi-axes of the ellipsoid along each coordinate axis in $\mathbb{R}^n$[@han2018eca].

Open Motion Planning Library (OMPL) [@sucan2012open], is a widely used open-source database designed to address motion planning challenges in robotics and related fields. It provides a comprehensive framework and a suite of tools to assist researchers and developers in developing efficient motion planning algorithms. We integrated the proposed algorithm, Flexible Informed Trees (FIT\*), into the OMPL framework and Planner-Arena benchmark database [@moll2015benchmarking], along with Planner Developer Tools (PDT) [@gammell2022planner].

# Problem Formulation

We define the problem of optimal planning in a manner associated with the definition provided in [@karaman2011sampling].

*Problem Definition 1 (Optimal Planning):* Consider a planning problem with the state space $X \subseteq \mathbb{R}^n$. Let $X_{\text{obs}} \subset X$ represent states in collision with obstacles, and $X_{\text{free}} = cl(X \setminus X_{\text{obs}})$ denote the resulting permissible states, where $cl(\cdot)$ represents the *closure* of a set. The initial state is denoted by $\mathbf{x}_{\text{start}} \in X_{\text{free}}$, and the set of desired final states is $X_{\text{goal}} \subset X_{\text{free}}$. A sequence of states $\sigma: [0, 1] \mapsto X$ forms a continuous map (i.e., a collision-free, feasible path), and $\Sigma$ represents the set of all nontrivial paths.

The optimal solution, represented as $\sigma^*$, corresponds to the path that minimizes a selected cost function $s: \Sigma \mapsto \mathbb{R}_{\geq 0}$. This path connects the initial state $\mathbf{x}_{\text{start}}$ to any goal state $\mathbf{x}_{\text{goal}} \in X_{\text{goal}}$ through the free space: $$\begin{equation}
\begin{split}
    \sigma^* &= \arg \min_{\sigma \in \Sigma} \left\{ s(\sigma) \middle| \sigma(0) = \mathbf{x}_{\text{start}}, \sigma(1) \in \mathbf{x}_{\text{goal}}, \right. \\
    &\qquad\qquad \left. \forall t \in [0, 1], \sigma(t) \in X_{\text{free}} \right\},
\end{split}
\end{equation}$$

:::: {#fig: BatchSize .figure latex-placement="t!"}
::: caption
Four snapshots of how EIT\* and FIT\* place their sampling strategy. FIT\* employs an adaptive batch size (1 to 199) strategy. EIT\* maintains a constant batch size (100) across all sample batches. The approach contains a combination of sparse and dense sampling, where more samples are utilized to expedite tree construction (c) compared to (a). Subsequently, FIT\* reduces the samples per batch, resulting in less time-consuming edge checking and an increased frequency of batch updating (d) compared to (b).
:::
::::

Where $\mathbb{R}_{\geq 0}$ denotes non-negative real numbers. The cost of the optimal path is $s^*$.

Considering a discrete set of states, $X_{\text{samples}} \subset X$, as a graph where edges are determined algorithmically by a transition function, we can describe its properties using a probabilistic model implicit dense RGGs when these states are randomly sampled, i.e., $X_{\text{samples}} = \{ \mathbf{x} \sim \mathcal{U}(X) \}$, as discussed in [@penrose2003random].

The characteristics of the anytime almost-surely sampling-based planner with the definition are provided in [@gammell2018informed].

*Problem Definition 2 (Almost-sure asymptotic optimality):* A planner is considered almost-surely asymptotically optimal as the number of samples tends to *infinity* which covers the entire general *$\mathcal{C}$-space*. In this scenario, if an optimum solution exists (as definition 1 optimal planning), the probability of the planner asymptotically converging to the optimal solution equals one when sample size $q$ goes infinite.

$$\begin{equation}
     P \left( \limsup_{q \to \infty} c(\sigma_q) = c(\sigma^*) \right) = 1.
\end{equation}$$ where $q$ represents the number of samples a planner has sampled, $\sigma_q$ signifies the path derived by the planner from those batch of samples, $\sigma^*$ stands for the optimal solution to the planning problem, and $c(\cdot)$ denotes the path's cost at the informed batch. After discovering an initial solution, the planner utilizes the remaining computational time to optimize the path quality of the existing solution.

# Flexible Informed Trees (FIT\*)

FIT\* builds on EIT\* and follows the asymmetric bidirectional search process with adaptive batch-size tunning (Alg. [\[biSearch\]](#biSearch){reference-type="ref" reference="biSearch"}). Moreover, FIT\* dynamically adjusts batch sizes based on the state space's geometry, fine-tuning the sampling density according to the dimension of *$\mathcal{C}$-space* and hypervolume of the $n$-dimensional hyperellipsoid. This difference in sampling strategy leads to distinct efficiencies and computational performance within planning algorithms.

::: algorithm
:::

## Notation

 []{#subsec: notation label="subsec: notation"} The state space of the planning problem is denoted by $X \subseteq \mathbb{R}^n$, where $n \in \mathbb{N}$. The start point is represented by $\mathbf{x}_{\text{start}} \in X$, and the goals are denoted by $X_{\text{goal}} \subset X$. The sampled states are denoted by $X_{\text{sampled}}$. The forward and reverse search trees are represented by $\mathcal{F} = (V_\mathcal{F}, E_\mathcal{F})$ and $\mathcal{R} = (V_\mathcal{R}, E_\mathcal{R})$, respectively. The vertices in these trees, denoted by $V_\mathcal{F}$ and $V_\mathcal{R}$, are associated with valid states. The edges in the forward tree, $E_\mathcal{F} \subset V_\mathcal{F} \times V_\mathcal{F}$, represent valid connections between states, while the edges in the reverse tree, $E_\mathcal{R} \subset V_\mathcal{R} \times V_\mathcal{R}$, may traverse invalid regions of the problem domain. An edge comprises a source state, $\mathbf{x}_s$, and a target state, $\mathbf{x}_t$, denoted as $(\mathbf{x}_s, \mathbf{x}_t)$. $\mathcal{Q_F}$ and $\mathcal{Q_R}$ designate the edge-queue for the forward search and reverse search, respectively. The true connection cost between two states in *$\mathcal{C}$-space* is represented by the function $c: X \times X \rightarrow [0, \infty)$.

For sets $A, B,$ and $C$ with $B, C$ being subsets of $A$, the notation $B \stackrel{+}{\leftarrow} C$ denotes $B \leftarrow B \cup C$, and $B \stackrel{-}{\leftarrow} C$ denotes $B \leftarrow B \setminus C$.

*FIT\*-specific Notation:* Incorporating attenuation introduces a decay factor $\Psi_\text{decay}$, with specified minimal $m_\text{min}:= 1$ and maximal $m_\text{max}$ sample numbers per batch. The initial batch sizes, denoted as $\mathcal{M}_\text{initial}$, and the current count of states sampled per batch represented as $\mathcal{M}(\Psi_\text{current})$. The Lebesgue measure within an $n$-dimensional hyperellipsoid is denoted by $\zeta_n$. Non-negative scalar $\xi_n$ represents the raw ratio of the initial hypervolume of the $n$-dimensional hyperellipsoid $\mathcal{V}_\text{initial}$ to the current hypervolume $\mathcal{V}_\text{current}$. A nature logarithmic tuning parameter $\Lambda_\text{tuning}$ regulates the rate at which the ratio decreases. $\mathcal{O}_\text{smooth}$ represents a smoothed value after the attenuation of the initial and optimal state.

::: algorithm
*$c_\text{current} \leftarrow \infty; \Psi_\text{decay} \leftarrow \infty; \Lambda_\text{tuning} \leftarrow \text{initialized}$*\
*$\mathcal{M}_\text{initial} \leftarrow \mathcal{M}(\Psi_\text{current}); \mathcal{V}_\text{current}\leftarrow \mathcal{V}_\text{initial};\xi_\text{initial}:= 1$*\
*$X_\text{sampled} \leftarrow X_\text{goal} \cup \{ \mathbf{x}_\text{start} \}$*\
*$V_\mathcal{F}, E_\mathcal{F}, \mathcal{Q_F} \leftarrow \text{\expand}(\mathbf{x}_\text{start})$*\
*$V_\mathcal{R}, V_{\mathcal{R},\text{closed}}, E_\mathcal{R}, \mathcal{Q_R} \leftarrow \text{\expand}(X_\text{goal})$*\
*$\text{Initialize and update the Inflation Factor and Sparse Resolution}$*\
:::

## Approximation {#subsec: approx.}

FIT\* employs informed sampling strategies [@gammell2018informed] to concentrate its RGG approximation on the pertinent region of the state space and dynamically adjusts the connection radius as more states are sampled. The radius ($r$) is updated according to the approach proposed in [@karaman2011sampling], utilizing the measure of the informed set as introduced in [@gammell2018informed]. $$\begin{equation}
\label{eqn:radius r}
    r(q) = \eta \left(2 \left(1 + \frac{1}{n}\right){\left(\frac{\lambda(X_{\hat{f}})}{\zeta_n}\right) \left( \frac{\log(q)}{q}\right)}\right)^{\frac{1}{n}},
\end{equation}$$ Here, $q$ denotes the number of sampled states in the informed set, $\eta >$ 1 is a tuning parameter, $\lambda(\cdot)$ denotes the Lebesgue measure, and $n$ represents the dimension of the state space.

::: algorithm
*$m_\text{min}:= 1, m_\text{max} := 2m_\text{current} - m_\text{min}$*\

*$c_\text{last} \leftarrow$ ($c_\text{current}$)*\

*$\mathcal{V}_\text{current} \stackrel{+}{\leftarrow} \ellipseVolumCal(c_\text{current})$*\
*$\xi_n \leftarrow \updateRawRatio(\mathcal{V}_\text{current},\mathcal{V}_\text{initial})$*\
*$\mathcal{O}_\text{smooth} \leftarrow \sigmoidFunction(\xi_n)$*\
*$\Psi_\text{decay} \leftarrow \updateDecayFactor(\mathcal{O}_\text{smooth}, \Lambda_\text{tuning})$*\
*$\mathcal{M}(\Psi_\text{current}):= m_\text{min}+\Psi_\text{decay}(m_\text{max}-m_\text{min})$*\
:::

:::: {#fig: decay_method .figure latex-placement="t!"}
::: caption
This graph shows the decay-based method comparison, where the maximal batch size is 199, and the minimal batch size is 1; more specific illustrations are given in section [4.3](#subsec: adaBachSize){reference-type="ref" reference="subsec: adaBachSize"}.
:::
::::

:::: {#fig:simulation .figure latex-placement="t!"}
::: caption
Illustrates the simulation (a) and the real-world scenarios of DARKO robot for the intralogistics task, (b) shows the start configuration of the arm in position to pick up the red cube from the metal sheet table, (c) shows the transition configuration position of the task, (d) shows the goal configuration of the arm in position to place a cube in the box.
:::
::::

## Adaptive Batch-Size {#subsec: adaBachSize}

FIT\* dynamically adjusts the number of samples in batch size. Specifically, it leverages the sigmoid function in conjunction with logarithmic (*sigmoid-log*, FIT\*-SL). As observed in Table [\[tab: decay_method\]](#tab: decay_method){reference-type="ref" reference="tab: decay_method"}, where $t^\textit{min}_\textit{init}$ represents the minimal initial planning time over 100 runs, and $c^\textit{max}_\textit{init}$ represents the maximal initial cost of the planning problem, respectively. The $c$ and $t$ of unsuccessful attempts are represented as infinity.

[]{#tab: decay_method label="tab: decay_method"}

Within the FIT\*'s flexible batch size context (Alg. [\[FIT_algori\]](#FIT_algori){reference-type="ref" reference="FIT_algori"} and [\[adaptiveBatch\]](#adaptiveBatch){reference-type="ref" reference="adaptiveBatch"}), our comparison focused on exploring various decay methods to comprehend their distinct impacts (Table [\[tab: decay_method\]](#tab: decay_method){reference-type="ref" reference="tab: decay_method"} and Fig. [4](#fig: decay_method){reference-type="ref" reference="fig: decay_method"}). These decay methods encompassed *linear* decay (FIT\*-L), *brachistochrone* curve-based decay (FIT\*-B), decay functions following an *parabola* pattern (FIT\*-P), and decay based on the *iteration count* (FIT\*-I). Each method was thoroughly examined 100 runs to assess its effectiveness in shaping the decay factor $\Psi_\text{decay}$. Through experimentation, it is concluded that FIT\*-SL stands out as the most efficient approach, demonstrating the quickest *median time* and shortest *median cost* for the initial solution. It strikes a balance between adaptability to denser sampling in the initial pathfinding phase and sparse sampling during the optimization phase of $\mathcal{C}$-space.

# Formal Analysis

 []{#sec: formalAnalysis label="sec: formalAnalysis"} In this paper, we refer to Definition 24 from [@karaman2011sampling] to establish the concept of almost-sure asymptotic optimality.

## Almost-Sure Asymptotically Optimal Path

The FIT\* algorithm utilizes an RGG approximation similar to EIT\*, with the underlying graph likely to contain an asymptotically optimal path. The graph search in FIT\* shows asymptotic resolution optimality. Given EIT\*'s status as an almost-surely asymptotically optimal algorithm [@gammell2022planner], it indicates that this RGG approximation includes an asymptotically optimal path. Therefore, the adaptive batch size computation affects the number of edge collision checks and does not seem to impact almost-sure asymptotic optimality.

:::: {#fig: testEnv .figure latex-placement="t!"}
::: caption
The 2D representation of the simulated planning problems in Section [6](#sec:Expri){reference-type="ref" reference="sec:Expri"}. The state space, denoted as $X \subset \mathbb{R}^n$, is constrained within a hypercube with one width for both problem instances. Specifically, we conducted ten distinct instantiations of the random rectangles experiment and the outcomes are showcased in Fig. [7](#fig: result){reference-type="ref" reference="fig: result"}.
:::
::::

## Statistical Formulation and Hypotheses

The sampling-based planner FIT\* dynamically adjusts batch sizes, increasing samples in the initial solution stage for faster convergence to a feasible path. Conversely, reducing samples per batch expedites optimization by minimizing edge checks, accelerating the batch sample update frequency, and reducing computational time. The *adaptiveBatchSize* function $\mathcal{M}(\Psi)$ is the major influence, considering the integration of the decay factor. It reflects how the expansion and contraction of the hyperellipsoids in different dimensions affects the appropriate batch size, aligning with the exploration requirements. $$\begin{equation}
        \mathcal{M}(\Psi) := m_\text{min} + (m_\text{max}-m_\text{min}) \times \Psi_\text{decay},
\end{equation}$$

:::: {#fig: result .figure latex-placement="t!"}
::: caption
Detailed experimental results from Section [6.1](#subsec:experi){reference-type="ref" reference="subsec:experi"} are presented above. Fig. (a), (c) and (e) depict test benchmark wall gap outcomes in $\mathbb{R}^2$, $\mathbb{R}^4$ and $\mathbb{R}^8$, respectively. Panel (b) showcases ten random rectangle experiments in $\mathbb{R}^2$, while panels (d) and (f) demonstrate in $\mathbb{R}^4$ and $\mathbb{R}^8$. In the cost plots, boxes represent solution cost and time, with lines showing cost progression for an almost surely optimal planner (unsuccessful runs have infinite cost). Error bars provide nonparametric 99% confidence intervals for solution cost and time.
:::
::::

Natural logarithm smoothly diminishes the decay rate, averting sudden drops for stable model optimization. The decay factor $\Psi_\text{decay}$ is determined through the division operation involving the logarithmic function. This relationship emphasizes how the dimensions of the hyperellipsoid influence the exploration of the state space in a logarithmic manner. $$\begin{equation}
\label{fuc:decay}
        \Psi_\text{decay} = \frac{\ln(1+\Lambda \times \mathcal{O}_\text{smooth})}{\ln{(1+\Lambda)}},
\end{equation}$$

The sigmoid smoothing technology of the raw ratio $\mathcal{O}_\text{smooth}$ ensures a gradual transition between batch sizes, mirroring how the hyperellipsoids's hypervolume changes smoothly with varying semi-axes lengths. This smoothing function allows for a more continuous adjustment of the batch size.

$$\begin{equation}
\label{fuc:smooth}
        \mathcal{O}_\text{smooth} = \frac{1}{1+ e^ {-10 \times {(\xi_n} -0.5)}},
\end{equation}$$ where $e$ is Euler's number $e = \sum_{i=0}^\infty \frac{1}{n!}$

Decay tuning parameter $\Lambda_\text{tuning}$ is correlated on the problem's dimensionality $n_\text{dimension}$ along with the $m_\text{min}$ and $m_\text{max}$ samples. This tuning parameter is a composite representation that makes the batch size related to *$\mathcal{C}$-space* dimensional information and becomes more problem-specific during adaptation.

$$\begin{equation}
        \Lambda_\text{tuning} = \frac{\mathcal{M}(\Psi_\text{max})+\mathcal{M}(\Psi_\text{min})}{n_\text{dimension}},
\end{equation}$$

The adjustment of batch size responds to the current raw ratio $\xi_n$, aligning with the optimization phase of the problem. This ratio is affected by the contraction (i.e., solution cost update) of the hypervolume of the current $n$-dimensional hyperellipsoids, this raw ratio is represented as:

$$\begin{equation}
        \xi_n = \frac{\mathcal{V}_\text{current}}{\mathcal{V}_\text{initial}}.
\end{equation}$$

Given the continuous improvement of the solution cost, the hypervolume shrinks accordingly, $\mathcal{V}_\text{current}$ consistently remains less than or equal to $\mathcal{V}_\text{initial}$. Consequently, the current raw ratio of the process $\xi_n$ resides within the interval $(0,1]$.

# Experimental Results {#sec:Expri}

FIT\* was tested against existing algorithms in both simulated random scenarios (Fig. [6](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}) and real-world manipulation problems (Fig. [5](#fig:simulation){reference-type="ref" reference="fig:simulation"}). The comparison involved several versions of RRT-Connect, Informed RRT\*, BIT\*, AIT\*, ABIT\*, and EIT\* sourced from the Open Motion Planning Library (OMPL) [@sucan2012open]. The evaluations are implemented on a computer with an Intel i7 3.90 GHz processor and 32GB of LPDDR3 3200 MHz memory. These comparisons were carried out in simulated environments ranging from $\mathbb{R}^2$ to $\mathbb{R}^8$. The primary objective for the planners was to minimize path length. The RGG constant $\eta$ was uniformly set to 1.1, and the rewire factor was set to 1.001 for all planners.

In the case of RRT-based algorithms, a goal bias of 5% was employed, and the maximum edge lengths were appropriately determined based on the dimensionality of the space. Meanwhile, BIT\*, AIT\*, ABIT\*, and EIT\* maintained a fixed sampling of 100 states per batch, regardless of the dimensionality of the state space. These planners also had graph pruning deactivated and utilized the Euclidean distance and effort as heuristic functions. FIT\*'s adaptive batch size technology dynamically adjusts the batch size, displaying a range from 1 to 199 batch sizes (Fig. [4](#fig: decay_method){reference-type="ref" reference="fig: decay_method"}). The specific number of samples at anytime is determined by the planner's adaptive mechanisms, ensuring quantities that are optimized for each solution cost update and batch re-sampling process.

## Experimental Tasks {#subsec:experi}

The planners were subjected to testing across three distinct problem domains: $\mathbb{R}^2$, $\mathbb{R}^4$, and $\mathbb{R}^8$. In the first scenario, a constrained environment resembling a wall with a narrow gap was simulated, allowing valid paths in two general directions for non-intersecting solutions (Fig. [6](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}a). The path planning objective is to optimize the initial and final path length rapidly. Each planner underwent 100 runs, and the computation time for each asymptotically optimal planner is demonstrated in the labels, with varying random seeds. The overall success rates and median path lengths for all planners are depicted in Fig. [7](#fig: result){reference-type="ref" reference="fig: result"}a, [7](#fig: result){reference-type="ref" reference="fig: result"}c, and [7](#fig: result){reference-type="ref" reference="fig: result"}e. In the second test scenario, random widths were assigned to *axis-aligned hyperrectangles*, generated arbitrarily within the *$\mathcal{C}$-space* (Fig. [6](#fig: testEnv){reference-type="ref" reference="fig: testEnv"}b). Random rectangle problems were created for each dimension of the *$\mathcal{C}$-space*, and each planner underwent 100 runs for every instance. Fig. [7](#fig: result){reference-type="ref" reference="fig: result"}b, [7](#fig: result){reference-type="ref" reference="fig: result"}d, and [7](#fig: result){reference-type="ref" reference="fig: result"}f illustrate the overall success rates and median path costs within the computation time for all the planners.

FIT\* employs an adaptive batch size feature, enhancing convergence time in the initial pathfinding phase by up to 24% and achieving faster solutions with lower initial costs.

## Path Planning for DARKO {#subsec:realExpri}

FIT\* demonstrated its effective adaptive batch size techniques during a field test as part of the inventory management (Fig. [1](#fig: darko_setup){reference-type="ref" reference="fig: darko_setup"} and Fig. [5](#fig:simulation){reference-type="ref" reference="fig:simulation"}). DARKO is a mobile manipulation robotic platform (8-DoF) created by combining Robotnik base robot and Franka Emika Panda manipulator, addressing intralogistics challenges. The intricacy of the narrow space presents challenging planning problems, primarily due to the computationally expensive state evaluations required. All planners had 1.0 seconds to address this confined, limited space pull-out and place problem. Over 15 trials, FIT\* was 100% successful with a median solution cost of 19.1021. EIT\* was also 100% successful but had a median solution cost of 22.6917. AIT\* was 86.7% successful with a median solution cost of 26.4482, and ABIT\* was 80% successful with a median solution cost of 25.6341. In contrast to other planners that rely on occupied space, FIT\* showcased efficiency by saving working space and completing the task with the shortest optimal path length. The detailed behavior of DARKO can be viewed in the accompanying video.

# Discussion & Conclusion

This paper introduces FIT\*, an adaptive batch size method planner correlated to the *$\mathcal{C}$-space*'s dimensionality and the hypervolume of the $n$-dimensional hyperellipsoid. In the initial solution finding phase, increased samples per batch accelerate initial solution discovery (higher probability to sample in the key area), while in the optimal phase, fewer samples per batch reduce collision checking time, enhancing sampling efficiency across batches. The adaptability of FIT\* was exemplified in a real-world scenario with the DARKO robot. FIT\*'s adaptive strategies ensured rapid initial solutions. This illustrates FIT\*'s practical applicability and industry problem-solving capacity.

In conclusion, FIT\* employs a flexible approach by dynamically optimizing batch sizes based on the sigmoid-log function to leverage a decay factor related to the $n$-dimensional hyperellipsoid. The adaptive batch size method showcases its potential by modifying the number of samples per batch and batch update frequency to optimize the planner's initial and optimization phases. This feature positions FIT\* as a promising solution in the field of path planning.

[^1]: $^{1}$L. Zhang, Z. Bing, K. Chen, L. Chen, K. Cai, Y. Zhang, F. Wu, S. Haddadin and A. Knoll are with the Department of Informatics, Technical University of Munich, Germany. `liding.zhang@tum.de`

[^2]: $^{2}$P. Krumbholz, Z. Yuan are with the Department of Technology & Innovation, KION Group Linde Material Handling GmbH, Germany.
