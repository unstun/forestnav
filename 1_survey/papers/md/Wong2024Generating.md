---
citation_key: Wong2024Generating
arxiv_id: 2410.20635
arxiv_url: https://arxiv.org/abs/2410.20635
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:44:26Z
origin: ai+web
reviewed: false
---

Wong *et al.*: Generating and Optimizing Topological Distinct Guesses

::: IEEEkeywords
Mobile Manipulation, Motion and Path Planning, Constrained Motion Planning, Optimization and Optimal Control
:::

# Introduction

path planning for mobile manipulators is commonly done by formulating and solving a nonlinear program (NLP) using gradient-based optimization approaches. One major challenge with this approach is that often the constraints introduced to the planning problem, such as obstacle avoidance, end effector path constraints, cause the NLP to be highly nonconvex. This causes gradient based optimization approaches to only solve them to local optimality. While solving nonconvex NLPs to global optimality in general is NP-hard, one potential mitigation is to generate multiple distinct local optima and choose the best among them. This increases the likelihood of actually finding the global optimum. In the sequel, we denote the optimum among multiple distinct local optima a *multi-local optimum*.

The challenge of obtaining a multi-locally optimal path is computing multiple distinct local optima since most research has only been conducted on finding a single local optimum [@zucker2013chomp],[@schulman2014motion]. Using the observation that the local optimum returned by gradient-based optimization approaches usually stays within the same homotopy class as the provided initial guess [@Lav06], we propose a pipeline that first discovers homotopically distinct paths and then uses them as initial guesses for an NLP. This allows for generating multiple distinct local optima, and subsequently finding the *multi-local optimum*.

::::: {#fig:intro .figure}
::: center
![](Wong2024Generating_figs/video_screenshot.png){width="\\columnwidth"}
:::

::: caption
Mobile manipulator executing three homotopically distinct locally optimal paths given a desired end effector path. Blue shows the desired end effector path, green and red shows the computed elbow and base paths respectively.
:::
:::::

We apply our pipeline to the path planning of mobile manipulators consisting of a 6-revolute (6R) elbow manipulator attached to a nonholonomic differential drive base. We further require that the end effector follows a predetermined path. Such end-effector path constraints arise naturally in applications such as painting, welding or wiping a table.

The contribution of this paper is the development of a path planning pipeline for mobile manipulators under end effector path constraints and produces a *multi-locally optimal* solution. To this end, we propose a method for generating a low dimensional configuration graph to be used with the Neighborhood Augmented Graph Search (NAGS) algorithm [@sahin2023topogeometrically]. Additionally, we propose several modifications to the NAGS algorithm that enhances its accuracy. Furthermore, an NLP is formulated to produce distinct locally optimal paths from the guesses provided by the modified NAGS algorithm. Finally, the effectiveness of the pipeline is demonstrated with simulation results along with a comparison study with existing methodologies.

The remainder is organized as follows. In Section [2](#sec:related_work){reference-type="ref" reference="sec:related_work"}, related work is reviewed, and in Section [3](#sec:problem){reference-type="ref" reference="sec:problem"}, the problem under consideration is stated. Section [4](#sec:methodology){reference-type="ref" reference="sec:methodology"} presents the proposed planning pipeline in detail, and Section [5](#sec:results){reference-type="ref" reference="sec:results"} presents some experimental results demonstrating the efficacy of our pipeline. Section [6](#sec:conclusion){reference-type="ref" reference="sec:conclusion"} offers a conclusion with some discussion.

# Related Work {#sec:related_work}

## Constrained Motion Planning

Motion planning in high dimensional space such as mobile manipulators under end effector constraints has been well studied. Many current methods build upon the rapidly exploring random tree (RRT) [@lavalle1998rapidly] and encode the constraints geometrically during tree construction [@oriolo2005motion; @berenson2011constrained; @kim2016tangent; @jaillet2012path]. These have been generalized and incorporated into the Implicit Manifold Configuration Space (IMACS) framework [@kingston2019exploring], decoupling the planning algorithm from the constraint adherence. These sampling approaches can often be postprocessed to produce a locally optimal path. However, the randomized nature of RRT-based algorithms implies that there is relatively little control over the characteristics of the paths returned, e.g. the topological properties.

## Optimal Path Planning

Trajectory optimization is a commonly used technique in optimal path planning. This involves formulating the path-finding problem as a mathematical program with costs and constraints, which is then solved with an optimizer. This field is well studied with many successful algorithms such as CHOMP [@zucker2013chomp] and TrajOpt [@schulman2014motion]. Both of these approaches use a direct transcription based technique [@underactuated], which involves discretizing the trajectory into a fixed number of discrete samples. These approaches generally scale well with the number of decision variables and constraints. However, the presence of nonconvex constraints and cost functions leads to results that are locally, not globally optimal, and heavily dependent on the initial guess provided.

## Topological Path Planning

Topological path planning focuses on finding and quantifying paths based on their topological features. Often, the feature of interest is a path's homotopy class ($\mathcal{H}$-class) within a robot's configuration space. Paths of different $\mathcal{H}$-class cannot be smoothly deformed into each other without colliding with obstacles (Fig. [2](#fig:homotopies){reference-type="ref" reference="fig:homotopies"}). Many probabilistic methods for finding homotopically distinct paths have been proposed [@pokorny2016high; @bhattacharya2012topological; @jaillet2008path]. However, they generally scale poorly to high dimensions.

:::: {#fig:1d_configuration_graph .figure latex-placement="tbp"}
![](Wong2024Generating_figs/homotopies.png){#fig:homotopies width="0.95\\columnwidth"}

 

![](Wong2024Generating_figs/1d_configuration_graph_combined.png){#fig:1d_configuration_graph width="\\textwidth"}

::: caption
\(a\) Given the grey obstacle, $p_1$ and $p_2$ belong to the same $\mathcal{H}$-class (homotopically equivalent) while $p_2$, $p_3$, $p_4$ each belong to a different $\mathcal{H}$-class (homotopically distinct). (b) Illustration of a 2D cross section ($y$ axis omitted) of the configuration graph.
:::
::::

As such, using a lower dimensional or simpler topological path planning setup for coarse global planning followed by optimal path planning approaches for local refinement is a common approach to combine the best of both worlds. This pipeline is effective in generating optimal trajectories for mobile ground robots [@rosmann2017integrated; @he2022homotopy], quadrotors [@zhou2021raptor] and manipulators [@rice2020multi; @saleem2021search].

For applying this topological and optimal path planning pipeline to mobile manipulators, a major problem is the determination of the $\mathcal{H}$-class, which is very challenging for high-dimensional configuration spaces [@sahin2023topogeometrically]. A novel Neighborhood Augmented Graph Search (NAGS) algorithm [@sahin2023topogeometrically] has recently been proposed that allows finding topologically distinct paths in higher dimensions. In our work, we leverage a modified version of NAGS to identify homotopically distinct paths and use optimal path planning for the local refinement.

# Problem Formulation {#sec:problem}

The path planning problem concerns a 6-degree-of-freedom (DoF) fully actuated elbow manipulator attached to a nonholonomic differential drive mobile base. The manipulator is assumed to have a 3DoF spherical wrist that handle any end effector orientation constraints. This is the case for most mobile manipulators available today. As such, we refer to the wrist as the end effector and only consider its position.

The base is characterized by its position $x_b = [x, y]^T \in \mathbb{R}^2$ and orientation $\theta \in S^1$. The base motion is governed by $$\begin{equation}
\dot x_b = \begin{bmatrix}\cos \theta \\ \sin \theta \end{bmatrix} u_1, \quad \dot \theta = u_2
\label{eq:base_dynamics}
\end{equation}$$ where $u_1, u_2 \in \mathbb{R}$ are control inputs.

As opposed to the more common approach of describing the arm in joint angle coordinates, we instead choose to express the arm in maximal coordinates [@underactuated]. In maximal coordinates, links are described by their position in space. This allows for a more natural incorporation of the end effector constraint that we will exploit in Section [4.1](#sec:graph){reference-type="ref" reference="sec:graph"}. Define $x_{b\perp} = [x_b, 0]^T = [x, y, 0]^T$. Given the base position $x_b$, the arm can be characterized by its elbow position $x_w \in \mathbb{R}^3$ and end effector position $x_e \in \mathbb{R}^3$, both in world cartesian coordinates. Let $l_1$ be the upperarm length and $l_2$ be the forearm length. The elbow and end effector positions are subject to the following kinematic constraints: $$\begin{align}
\begin{split}
    \lVert x_w - x_{b\perp} \rVert _2 &= l_1 \\
    \lVert x_w - x_e \rVert _2 &= l_2 \\
    \exists a, b \in \mathbb{R} : x_w - x_{b\perp} &= a (x_e - x_{b\perp}) + \begin{bmatrix}0 & 0 & b\end{bmatrix}^T
    \label{eq:kinematics}
\end{split}
\end{align}$$ The last constraint states that base, elbow and end effector positions projected to the $xy$-plane are collinear. This reflects the fact that the upperarm and elbow cannot roll. The dynamics of the arm is given by $$\begin{equation}
\dot x_w = u_3, \quad \dot x_e = u_4
\label{eq:arm_dynamics}
\end{equation}$$ where $u_3, u_4 \in \mathbb{R}^3$ are control inputs, subject to the constraints in Eq. ([\[eq:kinematics\]](#eq:kinematics){reference-type="ref" reference="eq:kinematics"}). The robot configuration $q$ is then fully defined by $$q = \begin{bmatrix}x_b^T & \theta & x_w^T & x_e^T \end{bmatrix}^T$$ subject to the aforementioned constraints. Note that this approach of using maximal coordinates to encode end effector constraints is not specific to the 6-DoF elbow manipulator and can be applied to arms with different kinematics by adjusting Eq. ([\[eq:kinematics\]](#eq:kinematics){reference-type="ref" reference="eq:kinematics"}) and ([\[eq:arm_dynamics\]](#eq:arm_dynamics){reference-type="ref" reference="eq:arm_dynamics"}), correspondingly [@brudigam2024variational].

Obstacles are assumed to be defined via an obstacle function $\text{obs}(q)$ which returns *True* if and only if the given robot configuration $q$ is colliding with an obstacle.

A desired end effector path is given in the form of a function $x_e(k)$ with $k \in [0, 1]$ being the normalized path parameter. The planning problem, then is to find a feasible path, satisfying the kinematic and end effector path constraints, and which does not collide with obstacles, minimizing $$\begin{equation}
\int_0^1 \lVert \mathbf{u}(t) \rVert_2 dt
\label{eq:cost}
\end{equation}$$

# Methodology {#sec:methodology}

The proposed planning pipeline consists of four main steps, illustrated in Fig. [5](#fig:pipeline){reference-type="ref" reference="fig:pipeline"} and Algorithm [\[alg:pipeline\]](#alg:pipeline){reference-type="ref" reference="alg:pipeline"}.

::::: {#fig:pipeline .figure latex-placement="tbp"}
::: center
![](Wong2024Generating_figs/pipeline.png){width="\\linewidth"}
:::

::: caption
The planning pipeline
:::
:::::

1.  First (line 2), we generate the collision-free configuration space graph (CG) representing the valid robot configurations and transitions.

2.  Then (line 3), we apply a modified NAGS algorithm, adapted from [@sahin2023topogeometrically], which takes as input the CG and finds a pre-specified number of homotopically distinct paths within the graph.

3.  Next (line 4-5), the homotopically distinct paths are used as initial guesses and the trajectory optimization problem is solved for each guess.

4.  Finally (line 6-7), we compare the optimized paths from the different initial guesses and choose the best path.

:::: algorithm
::: algorithmic
$x_e$: $[0, 1] \to \mathbb{R}^3$: Desired end effector path $n$: Number of distinct local optima to evaluate $dt$: Optimization timestep interval $T$: Number of optimization timesteps $Q^\star = \{q(t_0), q(t_1)$, $\dots, q(t_T)\}$, $t_0 = 0$, $t_T = 1$ $G = (V, E) := \text{ConfigurationGraphGeneration($x_e$)}$ $\begin{bmatrix}
    (x_{b1}, x_{w1}, t_1) \\
    (x_{b2}, x_{w2}, t_2) \\
    \vdots \\
    (x_{bn}, x_{wn}, t_n) \\
\end{bmatrix} := \text{modifiedNAGS}(G, n)$ $(\text{cost}_i, Q_i^\star) := \text{TrajOpt}
    (x_{bi}, x_{wi}, t_i, dt, T)$ $i^\star := \arg \min_i (\text{cost}_i)$ $Q^\star_{i^\star}$
:::
::::

## Configuration Graph Generation {#sec:graph}

The goal of this step is to transform the constrained high-dimensional continuous space of collision-free robot configurations into an unconstrained low-dimensional discrete graph for the subsequent NAGS algorithm. The base heading and nonholonomic constraints are ignored at this stage. The dimensionality reduction is achieved by a change of coordinates from $[x_b, x_w, x_e]^T \in \mathbb{R}^2 \times \mathbb{R}^3 \times \mathbb{R}^3$ to $[x_b, k, w]^T \in \mathbb{R}^2 \times [0, 1] \times \{0, 1\}$ by noticing that $x_e$ is fully defined by the path parameter $k$ and that given $x_b$ and $x_e$, there only exists two feasible elbow positions: elbow up and elbow down, represented by $w=1$ and $w=0$ respectively, with $w \in \{0, 1\}$. This is a direct results from Eq. ([\[eq:kinematics\]](#eq:kinematics){reference-type="ref" reference="eq:kinematics"}). This parametrization reduces the configuration space dimensionality allowing for a simpler configuration graph and thus better runtime performance. In the remainder of this section, we abuse notation and use $[x, y, k, w]^T$ and $[x_b, x_w, x_e]^T$ interchangeably with the understanding that the former can always be mapped to the latter via standard IK procedures [@siciliano2008springer].

The configuration graph (CG) is given by $G = (V, E)$ where $V$ is the set of vertices and $E$ is the set of undirected edges. Beginning with $V$, vertices are defined via a discretization of the configuration space $(x, y, t, w) \in \mathbb{R}^2 \times [0, 1] \times \{0, 1\}$ by predefined discretization intervals $\Delta x, \Delta y, \Delta t$. We define the discretized bounded configuration space as $$\begin{align*}
C &:= \{x_{\text{min}}, x_{\text{min}} + \Delta x, \dots, x_{\text{max}}\} \\
&\times
\{y_{\text{min}}, y_{\text{min}} + \Delta y, \dots, y_{\text{max}}\} \\
&\times \{t : 0, \Delta t, \dots, 1\} \times \{0, 1\}
\end{align*}$$ Define $C_{\text{free}} \subseteq C$ to be the configurations not in collision with obstacles. Furthermore, given the upperarm link length $l_1$ and forearm link length $l_2$, the distance between the base and end effector cannot be greater than the full arm length ($l_1 + l_2$), thus we define $$\begin{align*}
    C_\text{kinematic} = \{(x, y, t, w) : \lVert [x, y, 0]^T - x_e(t) \rVert _2 \leq l_1 + l_2\}
\end{align*}$$ The set of vertices is then given by $V = C_{\text{free}} \cap C_\text{kinematic}$.

The vertices within an elbow configuration $w$ are connected by collision-free edges in a grid-like fashion with diagonals for coordinates $x, y, t$. Transitions between elbow configurations $w$ can only occur at the joint singularity, when $\lVert [x, y, 0]^T - x_e(t) \rVert_2 = l_1 + l_2$. A simplified example is illustrated in Fig. [4](#fig:1d_configuration_graph){reference-type="ref" reference="fig:1d_configuration_graph"}. The edge cost is defined as the Euclidean distance between vertices in the $(x, y, t)$ coordinates.

The construction of a configuration graph for general mobile manipulators follows similarly by solving for each joint's possible cartesian positions given $x_b$ and $x_e$, according to their kinematic constraints in Eq. ([\[eq:kinematics\]](#eq:kinematics){reference-type="ref" reference="eq:kinematics"}).

## Modified Neighborhood Augmented Graph Search {#sec:NAGS}

The next step is to generate topologically distinct guesses. Our approach is based on a modified version of the NAGS algorithm [@sahin2023topogeometrically Algorithm 1]. The original algorithm along with our modifications colored in blue, orange and magenta, is presented in Algorithm [\[alg:modified_NAGS2\]](#alg:modified_NAGS2){reference-type="ref" reference="alg:modified_NAGS2"}.

:::: algorithm
::: algorithmic
$q_s \in V$: Start configuration $q_g \in V$: Goal configuration $\mathcal{N}_G$: Neighbor/successor function for graph $G$ $\mathcal{C}_G: V \times V \to \mathbb{R}^+$: Cost function $n_\text{req}$: Required number of homotopically distinct paths [\@computePS: $V \times (V_N, E_N)$: parent set computation]{style="color: blue"} $G_N$: Graph with costs and parent set for every vertex $V_N := \{ v_s \}$, $E_N := \emptyset$ $v_s := (q_s, \{ q_s \})$, $g(v_s) := 0$ $Q := \{ v_s \}$, $v := v_s$ $n := 0$ $v := (q, U) = \arg \min_{v' \in Q} g(v')$ $Q = Q - v$ $V_N = V_N \cup \{ v \}$ $E_N = E_N \cup \{ (v, v.\text{came\_from})\}$ ~~$U' = \text{computePNS}(v, (V_N, E_N))$~~ $U' = \text{computePS}(v, (V_N, E_N))$ ~~**for all $q' \in \mathcal{N}_G(v)$ do**~~ $v' := (q', U')$ $g' = g(v) + C_G(q, q')$ $w = v'$ $E_N = E_N \cup \{ (v, w) \}$ $g(w) = g'$ $w.\text{came\_from} = v$ $w.U = U'$ $v' := (q', U')$ ~~$V_N = V_N \cup \{ v' \}$~~ ~~$E_N = E_N \cup \{ (v, v') \}$~~ $g(v') = g'$ $v'.\text{came\_from} = v$ $Q = Q \cup \{ v' \}$ $n = n+1$ $G_N = (V_N, E_N)$
:::
::::

The main idea behind the original NAGS algorithm is to include approximations of the path tangents to vertices in Dijkstra's Algorithm [@dijkstra1959note]. This is done by using a vertex's path neighborhood set (PNS)[@sahin2023topogeometrically Algorithm 3], which is computed by running a reverse A\* search [@hart1968formal] on the graph for a fixed search depth $r$ from the current vertex back to the starting vertex. Since homotopically distinct paths terminating at the same vertex should have distinct path tangents, vertices are considered distinct if their PNS do not intersect. Note the distinction between CG vertex (vertices in the CG) and NAG vertex (vertices that are incrementally added to the NAG during the Dijkstra search). Each NAG vertex corresponds to one CG vertex; however, multiple NAG vertices may correspond to the same CG vertex. Two NAG vertices $v_1$ and $v_2$ are said to be *coincident* if they correspond to the same CG vertex. The equivalence ($\equiv$) of two coincident NAG vertices $v_1, v_2$ are thus defined as follows [@sahin2023topogeometrically Definition 4] $$v_1 \equiv v_2 \iff v_1\texttt{.cg} = v_2\texttt{.cg} \land v_1\texttt{.pns} \cap v_2 \texttt{.pns} \ne \emptyset$$ where $v\texttt{.cg}$ and $v\texttt{.pns}$ retrieves NAG vertex $v$'s corresponding CG vertex and PNS, respectively. We improve upon the original NAGS algorithm to address several shortcomings:

### Tiny obstacles {#sec:tiny_obstacles}

:::: {#fig:modified_nags_motivation_r .figure latex-placement="tb"}
![](Wong2024Generating_figs/modified_nags_motivation_r1_1.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r1_2.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r1_3.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r1_4.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r1_5.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r1_6.png){#fig:modified_nags_motivation_r1_final width="0.9\\columnwidth"}

![](Wong2024Generating_figs/modified_nags_motivation_r2_1.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r2_2.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r2_3.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r2_4.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r2_5.png){width="0.9\\columnwidth"}

 

![](Wong2024Generating_figs/modified_nags_motivation_r2_6.png){#fig:modified_nags_motivation_r2_final width="0.9\\columnwidth"}

::: caption
Top row: (a) shows a simple CG with the green start vertex and yellow goal vertex. The edge weight corresponds to the length depicted. Note that this CG only has one homotopically unique path from start to goal. (b)-(f) corresponds to the successive iterations as the NAG grows using $r = 1$. The subscript indicates the PNS of the NAG vertex. Notice in (f) that since NAG vertex $D_C$ and $D_A$ have disjoint PNS, NAGS incorrectly identifies them as homotopically distinct. Bottom row: (g) shows a simple CG with an obstacle in the middle. Notice that there are two homotopically distinct paths from the start to goal. (h)-(l) corresponds successive iterations with $r = 2$. Notice in (l) that the NAG vertices $D_{BA}$ and $D_{CA}$ have overlapping PNS, thus NAGS incorrectly identifies them as homotopically equivalent.
:::
::::

The original NAGS algorithm suffers from the inability to distinguish homotopically distinct paths around tiny obstacles regardless of the value of $r$ chosen. This is exemplified in Fig. [8](#fig:modified_nags_motivation_r){reference-type="ref" reference="fig:modified_nags_motivation_r"}. Notice that regardless of the value of $r$, the original NAGS algorithm is not able to correctly identify the homotopically distinct paths in the top and bottom cases simultaneously. This stems from the fact that the continuous path tangent is poorly represented in a discrete graph structure. As such, the overlap in the path tangent, approximated by the overlap of the PNS, is easily over- or underestimated, causing the incorrect identification of homotopically distinct paths.

:::: {#fig:nags_progression .figure latex-placement="tb"}
![](Wong2024Generating_figs/nags_progression1.png){width="\\columnwidth"}

 

![](Wong2024Generating_figs/nags_progression2.png){width="\\columnwidth"}

 

![](Wong2024Generating_figs/nags_progression4.png){width="\\columnwidth"}

 

![](Wong2024Generating_figs/nags_progression5.png){width="\\columnwidth"}

::: caption
Successive iterations of the NAG. Notice that obstacles cause the yellow wavefront to split and then merge.
:::
::::

:::: {#fig:nags_ps_progression .figure latex-placement="tb"}
![](Wong2024Generating_figs/nags_ps_progression_noobs0.png){width="0.6\\columnwidth"}

 

![](Wong2024Generating_figs/nags_ps_progression_noobs1.png){width="0.6\\columnwidth"}

 

![](Wong2024Generating_figs/nags_ps_progression_noobs2.png){width="0.6\\columnwidth"}

 

![](Wong2024Generating_figs/nags_ps_progression_noobs3.png){width="0.6\\columnwidth"}

![](Wong2024Generating_figs/nags_ps_progression_obs0.png){width="0.6\\columnwidth"}

 

![](Wong2024Generating_figs/nags_ps_progression_obs1.png){width="0.6\\columnwidth"}

 

![](Wong2024Generating_figs/nags_ps_progression_obs2.png){width="0.6\\columnwidth"}

 

![](Wong2024Generating_figs/nags_ps_progression_obs3.png){width="0.6\\columnwidth"}

::: caption
Top row: (a) shows a CG with the blue start vertex. (b)-(d) shows the successive iterations of the NAG. Yellow vertices are those in the open set (wavefront) while green vertices have already been visited. Consider the NAG vertex circled in red. The red edge connects the circled vertex to its parents. Bottom row: (e) shows a CG with an obstacle. (f)-(h) shows successive iterations of the NAG.
:::
::::

Instead of a static approximation of the path tangent, we improve performance by using a dynamic local description of the wavefront of the open set instead (Fig. [9](#fig:nags_progression){reference-type="ref" reference="fig:nags_progression"}). The following observation can be made upon careful inspection of the wavefront as it visits a vertex. Given the current state of the NAG $G_N = (V_N, E_N)$, define the parent set $\mathcal{P}(v)$ of NAG vertex $v$ as $$\begin{align*}
\mathcal{P}(v) := \{v' : \exists (v, v') \in E_N \}
\end{align*}$$ We observe that in the absence of obstacles, the parent set (PS) of a vertex starts on the shortest path and grows to adjacent vertices. In the presence of obstacles, this rule is broken. The PS no longer grows to adjacent vertices. This is demonstrated in Fig. [10](#fig:nags_ps_progression){reference-type="ref" reference="fig:nags_ps_progression"}. In effect, the PS acts as a local description of the wavefront.

This motivates the use of the PS to detect whether two paths are homotopically distinct or not. Two PS $\mathcal{P}_1, \mathcal{P}_2$ are said to be *adjacent* if the following holds: $$\text{adj}_{E_N}(\mathcal{P}_1, \mathcal{P}_2) \iff \exists v_1 \in \mathcal{P}_1, v_2 \in \mathcal{P}_2 : (v_1, v_2) \in E_N$$ We then redefine the equivalence relation ($\equiv$) as follows:

::: {#def:equivalence .definition}
**Definition 1** (Equivalence between NAG vertices). *For coincident NAG vertices $v_1$ and $v_2$ and NAG $G_N = (V_N, E_N)$, $$v_1 \equiv v_2 \iff
v_1\texttt{.cg} = v_2\texttt{.cg} \land \text{adj}_{E_N}(\mathcal{P}(v_1), \mathcal{P}(v_2))$$ where $v\texttt{.cg}$ retrieves the corresponding CG vertex of $v$.*
:::

To illustrate the effect of using PS, consider the example in Fig. [6](#fig:modified_nags_motivation_r1_final){reference-type="ref" reference="fig:modified_nags_motivation_r1_final"} again. Using PS, $\mathcal{P}(D_C) = \{C_A\}, \mathcal{P}(D_A) = \{A\}$. Since $C_A$ is adjacent $A$, $D_C \equiv D_A$ and they are considered homotopically identical. For Fig. [7](#fig:modified_nags_motivation_r2_final){reference-type="ref" reference="fig:modified_nags_motivation_r2_final"}, $\mathcal{P}(D_{CA}) = \{C_A\}, \mathcal{P}(D_{BA}) = \{B_A\}$. Since $C_A$ and $B_A$ are not adjacent, the two NAG vertices will be considered distinct, correctly identifying the two homotopically distinct paths.

### Non-uniform discretization

In the original NAGS algorithm, $r$ must be fine tuned to account for potentially large differences in edge weights. The PS modification mentioned in Section [4.2.1](#sec:tiny_obstacles){reference-type="ref" reference="sec:tiny_obstacles"} itself does not alleviate this issue. One example is illustrated in Fig. [13](#fig:bad_example1){reference-type="ref" reference="fig:bad_example1"}. This is due to the fact that the original NAGS algorithm adds a vertex to the NAG based on the parent of that vertex. We thus apply the changes in line 9-10 and line 25-26 of Algorithm [\[alg:modified_NAGS2\]](#alg:modified_NAGS2){reference-type="ref" reference="alg:modified_NAGS2"}. These modifications ensure that vertices are added to the NAG in the order of the cost to the vertex itself, rather than the parent. The effect of these modifications is that $F_E$ will be added to the NAG before $F_B$. Since $F_E$ and $F_H$ are equivalent, the edge $(E_G, F_H)$ is inserted, causing the PS of $F_H$ to expand to $E_G$. Then, $\mathcal{P}(F_H) = \{H_G, E_G\}$ will be adjacent to $\mathcal{P}(F_B) = \{B_D\}$ and thus $F_B \equiv F_H$.

:::: {#fig:bad_example1 .figure latex-placement="tb"}
![CG](Wong2024Generating_figs/bad_example1_cg.png){#fig:bad_example1_cg width="\\columnwidth"}

![Start](Wong2024Generating_figs/bad_example1_1.png){width="0.9\\columnwidth"}

![Visit G](Wong2024Generating_figs/bad_example1_2.png){width="\\columnwidth"}

![Visit D](Wong2024Generating_figs/bad_example1_3.png){width="\\columnwidth"}

![Visit H](Wong2024Generating_figs/bad_example1_4.png){width="\\columnwidth"}

![Visit A](Wong2024Generating_figs/bad_example1_5.png){width="\\columnwidth"}

![Visit B](Wong2024Generating_figs/bad_example1_6.png){#fig:bad_example1_6 width="\\columnwidth"}

 

::: caption
\(a\) Non-uniformly discretized CG with $GH<GD + DB<GE$. Note that there is only 1 homotopically unique path between $G$ and $F$. (b)-(g) Progression of the NAGS algorithm using PS. Subscript indicates the parent of the vertex. In (g), $\mathcal{P}(F_B) = \{B_D\}$, $\mathcal{P}(F_H) = \{H_G\}$. Since $\mathcal{P}(F_B)$ is not adjacent to $\mathcal{P}(F_H)$, we have $F_B \not\equiv F_H$. Hence the algorithm incorrectly determines that there are two homotopically distinct paths from $G$ to $F$.
:::
::::

### Ambiguous visiting order

:::: {#fig:bad_example2 .figure latex-placement="tb"}
![CG](Wong2024Generating_figs/bad_example2_cg.png){#fig:bad_example2_cg width="0.95\\columnwidth"}

![Start](Wong2024Generating_figs/bad_example2_1.png){width="0.95\\columnwidth"}

![Visit A](Wong2024Generating_figs/bad_example2_2.png){width="0.95\\columnwidth"}

![Visit B](Wong2024Generating_figs/bad_example2_3.png){width="0.95\\columnwidth"}

![Visit D](Wong2024Generating_figs/bad_example2_4.png){#fig:bad_example2_4 width="0.95\\columnwidth"}

::: caption
\(a\) CG with uniform edge lengths. Note that there is only 1 homotopically unique path between $A$ and $C$. (b)-(e) Progression of the NAGS algorithm using PS. Subscript indicates the parent of the vertex. Dotted vertices represent vertices in the heap. Notice that the order for visiting $B_D$, $D_B$, $C_B$, $C_D$ is undefined as they all have the same path cost. Furthermore, whether or not $C_B \equiv C_D$ depends on the order in which the four vertices are visited. If $C_B$ and $C_D$ are visited before $B_D$ or $D_B$, then $C_B \not\equiv C_D$.
:::
::::

Similar to the above, the order in which vertices are visited impacts both PS and PNS calculation. This is illustrated in Fig. [16](#fig:bad_example2){reference-type="ref" reference="fig:bad_example2"}. To tackle the nondeterministic visiting order of paths of the same length, we prioritize processing equivalent vertices first (line 13-14) before processing nonequivalent vertices (line 23). This prevents equivalent vertices being incorrectly considered distinct due to visiting order.

### Sufficient Condition Sketch

We provide a more general sufficient condition for detecting homotopically distinct paths, only requiring obstacles that cause the removal of edges/vertices in the CG.

::: proposition
**Proposition 1**. *Two locally shortest (geodesic) paths, $p_1$ and $p_2$, from the CG vertex $v_s$ to $v_g$ that encloses an obstacle will generate distinct NAG vertices.*
:::

*Proof Sketch:*

Note that each obstacle causes the removal of edges/vertices in the configuration graph, creating a chordless cycle $R_0$. A chordless cycle is a cycle of length at least four in which no two vertices are joined by an edge outside of the cycle itself. Define $R_k$ to be the set of vertices adjacent to but not contained in $R_{k-1}$.

Let $\{n_1, \dots, n_j\}$ be the NAG vertices of $p_1$ and $\{m_1, \dots, m_h\}$ be the NAG vertices of $p_2$. Suppose path lengths $l(p_2) \ge l(p_1)$. Note that $n_1$ and $m_1$ both correspond to the same CG vertex $v_s$ and $n_1 \equiv m_1$ while $n_j$ and $m_h$ both correspond to $v_g$, but it is yet to be determined whether they are equivalent or not.

The inductive proof proceeds as follows:

1.  Base condition: Consider $v_g \in R_0$. In order for $p_1$ and $p_2$ to enclose $R_0$ and be geodesics, we must have $n_{j-1}, m_{h-1} \in R_0$. Since $R_0$ is a chordless cycle, there is no edge between $n_{j-1}$ and $m_{h-1}$. $\mathcal{P}(n_j) = \{n_{j-1}\}$ is not adjacent $\mathcal{P}(m_h) = \{m_{h-1}\}$. Hence $n_j \not\equiv m_h$.

2.  Inductive step: Assume the proposition is true $\forall v_g' \in R_{k-1}$. We wish to show it to be true for $v_g \in R_k$. Suppose the contrary, that for some $v_g \in R_k$, $n_j \equiv m_k$. This requires that $\mathcal{P}(m_{h}) = \{m_{h-1}\}$ be adjacent to $\mathcal{P}(n_{j}) = \{n_{j-1}\}$. We consider two cases for $m_{h-1}$

    1.  $m_{h-1} \in R_k \cup R_{k+1}$: This cannot be the case if $p_1$, $p_2$ enclose the obstacle, $l(p_2) \ge l(p_1)$ and they are locally shortest paths. This can be seen since there must exist some point $m_a \in p_2 \cap R_0$ and the subpath $(m_a, \dots, m_{h-1})$ is locally shortest.

    2.  $m_{h-1} \in R_{k-1}$: Then there exist some $v_g' = m_{h-1} \in R_{k-1}$ such that $p_1'$ and $p_2'$ are equivalent, contradicting the induction hypothesis.

    Hence the proposition must be true for $v_g \in R_k$.

Thus we show the proposition to be true for pairs of locally shortest paths. $\square$

The generalization to all possible pairs of paths from $v_s$ to $v_g$ follows based on two facts: 1) If two NAG vertices $n_{j-1}$, $m_{h-1}$ are adjacent, then a path via $n_{j-1}$ to $m_{h-1}$ must have been deemed homotopically equivalent to a path via $m_{h-2}$ to $m_{h-1}$ in earlier iterations. 2) Dijkstra's algorithm always finds shorter paths first. Thus, homotopic equivalence is determined by the locally shortest path.

## Trajectory Optimization {#sec:traj_opt}

The goal of this step is to use the results from the previous section to refine the path, considering all constraints of the original planning problem. In addition to including the base heading and the nonholonomic constraints, a finer time discretization is used to ensure that constraints are satisfied more precisely.

The trajectory optimization problem is given as

::: mini!
\|s\| \_k=0\^T u_1\[k\] \_2\^2 + u_2\[k\] \_2\^2 + x_w\[k\] \_2\^2 []{#opt:obj label="opt:obj"}
:::

The objective ([\[opt:obj\]](#opt:obj){reference-type="ref" reference="opt:obj"}) is to minimize the discretized cost in Eq. ([\[eq:cost\]](#eq:cost){reference-type="ref" reference="eq:cost"}). This is subject to ([\[opt:const_l1\]](#opt:const_l1){reference-type="ref" reference="opt:const_l1"})-([\[opt:elbow_kinematics\]](#opt:elbow_kinematics){reference-type="ref" reference="opt:elbow_kinematics"}) which enforce the kinematic constraints in Eq. ([\[eq:kinematics\]](#eq:kinematics){reference-type="ref" reference="eq:kinematics"}), and ([\[opt:nonholonomic\]](#opt:nonholonomic){reference-type="ref" reference="opt:nonholonomic"})-([\[opt:elbow_vel\]](#opt:elbow_vel){reference-type="ref" reference="opt:elbow_vel"}) which enforce the dynamic constraints in Eq. ([\[eq:base_dynamics\]](#eq:base_dynamics){reference-type="ref" reference="eq:base_dynamics"}) and ([\[eq:arm_dynamics\]](#eq:arm_dynamics){reference-type="ref" reference="eq:arm_dynamics"}). Finally, ([\[opt:no_col\]](#opt:no_col){reference-type="ref" reference="opt:no_col"}) enforces collision avoidance at each timestep.

## Evaluate Local Optima

The final step is to compare and select the least cost path among the locally optimal paths from the previous step. Formally, given the locally optimal trajectories $Q_i^\star$ and associated $\text{cost}_i$ for $i \in \{1, \dots, n\}$, index $i^\star$ of the trajectory with the least cost is given by $$i^\star := \arg \min_i(\text{cost}_i)$$ The *multi-locally optimal* path is then $Q^\star_{i^\star}$ which is the optimal path among the local optima $\{Q_1^\star, \dots, Q_n^\star\}$.

# Results {#sec:results}

:::: table*
::: center
+--------------------------+-----------------------------------------------------------------------+--------------------------------------------------------+
| Method                   | Planning Problem 1 (n=4)                                              | Planning Problem 2 (n=3)                               |
+:=========================+:===========+:======================+:=================================+:===========+:=================+:=======================+
| 2-7                      | Runtime(s) | NLP success rate      | Final cost                       | Runtime(s) | NLP success rate | Final cost             |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
| CG+Modified NAGS (n)     | 1.02+0.49  | 1.0 / 1.0 / 1.0 / 1.0 | **2.33** / 6.02 / 6.09 / 6.05    | 0.90+2.35  | 1.0 / 1.0 / 1.0  | **2.32** / 2.98 / 2.99 |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
| IMACS-KPIECE (1)         | 1.79       | 0.3                   | 14.37                            | timeout    | \*               | \*                     |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
| IMACS-KPIECE (n)         | 29.9       | 0.6 / 0.2 / 0.2 / 0.1 | 10.57 / **5.75** / 25.64 / 10.03 | timeout    | \* / \* / \*     | \* / \* / \*           |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
| IMACS-RRTConnect (1)     | 37.3       | 0.3                   | 4.62                             | timeout    | \*               | \*                     |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
| IMACS-RRTConnect (n)     | timeout    | \* / \* / \* / \*     | \* / \* / \* / \*                | timeout    | \* / \* / \*     | \* / \* / \*           |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
| Simple Interpolation (1) | 0.01       | 0.0                   | \*                               | 0.01       | 0                | \*                     |
+--------------------------+------------+-----------------------+----------------------------------+------------+------------------+------------------------+
:::
::::

In this Section, we compare our method for generating topologically distinct initial guesses against sampling-based approaches and simple interpolation. For all planning problems, we generate the CG by discretizing the end effector path at 0.05m intervals. Base positions are discretized at a resolution of 0.1m. Edges in the CG are further subsampled at 0.01m for collision checking. The results of both modified NAGS and sampling-based methods are all used as initial guesses for the NLP specified in Section [4.3](#sec:traj_opt){reference-type="ref" reference="sec:traj_opt"}. The optimization problem is formulated in Drake [@drake] and solved with SNOPT [@gill2005snopt] using discretization $T = 200$ and timestep $dt = 0.2$. All final costs represent optimized costs in Eq. ([\[opt:obj\]](#opt:obj){reference-type="ref" reference="opt:obj"}) after using the initial guess to solve the NLP. Runtime only includes the time taken to generate the the initial guesses and does not include the time for solving the NLP . The code for the implementation and comparison, as well as interactive recordings of the results can be found at <https://github.com/rcywongaa/topologically_distinct_guesses>. We investigate three planning scenarios.

## Two Sphere Obstacles with Straight Line Path Constraint {#sec:planning_problem1}

Planning Problem 1 involves finding the optimal path for a simple two-link mobile manipulator in the presence of two spherical obstacles, subject to an end effector constraint in the form of a straight line.

Our algorithm is compared against two constrained sampling-based approaches: the IMACS-RRTConnect [@kuffner2000rrt] algorithm (emulates CBIRRT2 [@berenson2011constrained], TB-RRT [@kim2016tangent], AtlasRRT [@jaillet2012path]) and the IMACS-KPIECE [@csucan2009kinodynamic] algorithm which shows superior results in high dimensional constrained configuration space [@kingston2019exploring]. The path tolerance was set to 0.05m.

The sampling-based planners are compared in singleshot mode (1), where only one path is generated and evaluated, and multishot mode (n), where the planner keeps generating paths until at least one path belonging to each of the $n$ homotopic classes is generated. Both modes are subject to a 5 minute timeout. The sampling-based approaches were set up using OMPL [@sucan2012the-open-motion-planning-library] and MoveIt2 [@chitta2012moveit][@coleman2014reducing]. Additionally, a simple IK-based interpolation method is also compared.

The results are summarized in Table [\[table:performance_comparisons\]](#table:performance_comparisons){reference-type="ref" reference="table:performance_comparisons"}, averaged over 10 trials. It can be seen that our algorithm can generate topologically distinct initial guesses more quickly as indicated by the lower runtime, as well as produce guesses of higher quality, as indicated by the higher NLP success rate and lower final cost. Examples from modified NAGS and IMACS-KPIECE are shown in Fig. [18](#fig:NAG){reference-type="ref" reference="fig:NAG"} and Fig. [19](#fig:OMPL){reference-type="ref" reference="fig:OMPL"} respectively.

Note that the nonholonomic constraints of the mobile manipulator are only enforced in the NLP, further introducing more local optima to the optimization landscape. This highlights the importance of providing high-quality guesses to the optimizer and explains the apparent differences in final cost of trajectories belonging to the same $\mathcal{H}$-classes. Since the NAGS algorithm produces shortest paths within the $\mathcal{H}$-class, it naturally constitutes an initial guess that is closer to the global optimum, even with the added nonholonomic constraints. Additionally worth pointing out, the single-shot performance of IMACS-KPIECE is comparable to that of our CG+Modified NAGS pipeline, while its multi-shot performance is significantly worse. This indicates that the slowdown stems from the absence of homotopy awareness in IMACS-KPIECE. Since the discovery of homotopically distinct paths is inherently probabilistic, this largely explains the increased planning time.

## Simulated Bar Table Cleaning

Planning Problem 2 involves a more realistic table cleaning scenario in which a mobile manipulator in the form of a Kinova Gen3 robot arm attached to a Turtlebot 4 is tasked with cleaning a counter table with a sine wave motion while avoiding collisions. The sampling-based planners are set up and evaluated in the same fashion as in Section [5.1](#sec:planning_problem1){reference-type="ref" reference="sec:planning_problem1"} and the results are summarized in Table [\[table:performance_comparisons\]](#table:performance_comparisons){reference-type="ref" reference="table:performance_comparisons"}, also averaged over 10 trials. The final results are shown in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"}. Particularly, note that the highly nonconvex table and chair means that conventional approaches of projecting obstacles to the ground plane and splitting base and arm motion planning would yield poor results since naive projection would either severely overestimate or underestimate the size of the obstacles. Indeed, if we project the table and chair to the ground plane and consider the mobile base inflation radius, the path where the base moves between the table and the chair would not be feasible. This planning problem also highlights the limitation of sampling based planners which struggle with narrow passages generated by the large obstacle and end effector constraints [@kingston2019exploring].

:::: {#fig:randomized_tests .figure latex-placement="tpb"}
![](Wong2024Generating_figs/varying_obstacle_radii.png){width="\\columnwidth"}

 

![](Wong2024Generating_figs/varying_num_obstacles.png){width="\\columnwidth"}

::: caption
Effect of varying number of obstacles and obstacle radius on number of paths found in 10s. Note that paths found by IMACS-KPIECE may not be homotopically distinct. (a) uses 4 obstacles. (b) uses obstacles of radii 0.15m.
:::
::::

## Randomized Tests

This test studies the effect of the number and size of the obstacles on the performance of our modified NAGS algorithm. The setup is similar to Planning Problem 1 with a varying number and radii of spherical obstacles. In this experiment, we focus on comparing against IMACS-KPIECE since it has been shown to be superior in performance in Planning Problem 1. Since it is difficult to predetermine the number of $\mathcal{H}$-classes in a randomized setting, we instead impose a 10s time limit for both modified NAGS and IMACS-KPIECE to generate as many paths as possible (homotopically distinct or not). The experiment is conducted with randomized obstacle positions averaged over 50 trials per setting. The results are shown in Fig. [17](#fig:randomized_tests){reference-type="ref" reference="fig:randomized_tests"}. It can be seen that modified NAGS outperforms IMACS-KPIECE in situations with a small number of large obstacles. Large obstacles are favorable since they lead to fewer vertices in the CG, and thus to a faster search. For a high number of obstacles, the number of homotopically distinct paths of a certain length grows rapidly. This causes the open set to grow quickly, which impacts the performance. Furthermore, since each obstacle creates infinitely many homotopically distinct paths corresponding to increasing winding numbers, there is no upper bound to the size of the open set.

Using 4 obstacles of radius of 0.15, we repeat the experiment with the trajectory optimization step included. We additionally randomize the initial and goal headings. The respective multi-locally optimal paths are then compared. Across 50 trials, modified NAGS and IMACS-KPIECE produced at least one admissible initial guesses for 88% and 60% of the trials, respectively, where an initial guess is admissible if it allows the NLP to be solved. On average, the multi-locally optimal paths generated by the NAGS algorithm were 30.6% shorter than those generated by IMACS-KPIECE. Furthermore, 34% of the multi-locally optimal paths from modified NAGS were *not* from the first (shortest) path returned. Since the first path returned by modified NAGS is equivalent to the result of running standard Dijkstra's Algorithm [@dijkstra1959note], this also shows that modified NAGS produced better initial guesses than standard Dijkstra in those cases.

:::: {#fig:NAG .figure latex-placement="tpb"}
![$\mathcal{H}$-class 1](Wong2024Generating_figs/nag_1.png){width="\\columnwidth"}

 

![$\mathcal{H}$-class 2](Wong2024Generating_figs/nag_2.png){width="\\columnwidth"}

 

![$\mathcal{H}$-class 3](Wong2024Generating_figs/nag_3.png){width="\\columnwidth"}

 

![$\mathcal{H}$-class 4](Wong2024Generating_figs/nag_4.png){width="\\columnwidth"}

::: caption
Results of NAGS belonging to different $\mathcal{H}$-classes for Planning Problem 1
:::
::::

:::: {#fig:OMPL .figure latex-placement="tpb"}
![$\mathcal{H}$-class 1](Wong2024Generating_figs/ompl_1.png){width="\\columnwidth"}

 

![$\mathcal{H}$-class 2](Wong2024Generating_figs/ompl_2.png){width="\\columnwidth"}

 

![$\mathcal{H}$-class 3](Wong2024Generating_figs/ompl_3.png){width="\\columnwidth"}

 

![$\mathcal{H}$-class 4](Wong2024Generating_figs/ompl_4.png){width="\\columnwidth"}

::: caption
Results of IMACS-KPIECE belonging to different $\mathcal{H}$-classes for Planning Problem 1
:::
::::

# Conclusion & Discussions {#sec:conclusion}

This paper presents a pipeline for mobile manipulator path planning under end effector path constraints that achieve multi-local optimality. Several modifications were proposed to the core NAGS algorithm enabling it to reliably distinguish homotopically distinct paths. Our algorithm performs particularly well in scenarios where kinematic structure and constraints reduce the dimensionality of the problem, and where a small number of large obstacles lead to a more compact configuration graph. In such cases, the algorithm's ability to handle large obstacles becomes especially beneficial, as these environments often introduce challenging local optima that our approach is well-equipped to address. This can be seen as a complement to sampling-based approaches, which generally work well in the absence of constraints and with smaller, more numerous obstacles. Future work may investigate ways to alleviate the curse of dimensionality when applying our algorithm to mobile manipulators with many DoFs.

[^1]: Manuscript received: April, 25, 2025; Revised August, 23, 2025; Accepted September, 27, 2025.

[^2]: This paper was recommended for publication by Editor Aniket Bera upon evaluation of the Associate Editor and Reviewers' comments.

[^3]: This work was supported by the Swedish Research Council, the Knut and Alice Wallenberg Foundation, and the Swedish Foundation for Strategic Research.

[^4]: The authors are with the Division of Decision and Control Systems, School of EECS, Royal Institute of Technology (KTH), 100 44 Stockholm, Sweden `[rcywong,sewlia,wiltz,dimos]@kth.se`

[^5]: Digital Object Identifier (DOI): see top of this page.
