---
citation_key: Kusnur2020Searchbased
arxiv_id: 2011.07383
arxiv_url: https://arxiv.org/abs/2011.07383
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:53:07Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Path planning for traditional robotic coverage is the task of determining a collision-free robot trajectory that observes all points of interest in a given environment [@galceran2013survey]. Numerous real-world tasks including environmental exploration, traffic monitoring, and post-disaster assessment can be cast as coverage problems [@nedjati2016complete; @smith2011persistent; @srinivasan2004airborne; @teixeira2018autonomous]. Robots employed for such coverage tasks are often equipped with limited-range sensors to observe the environment and can exercise active control over them. An important problem is to plan robot and sensor trajectories that maximize coverage or information gain in these tasks. Planning in real time for kinodynamically constrained robots is in itself a computationally expensive problem due to the many degrees of freedom in a kinodynamic state. Additionally planning trajectories for sensors onboard these robots further increases the computational complexity of this task.

In this paper, we consider the specific problem of planning trajectories for an unmanned aerial vehicle (UAV) and its onboard sensor covering cells of a discrete maprepresenting a known, deterministic environmentto achieve efficient 2D area coverage while navigating to an assigned goal. We assume that the UAV flies at a fixed altitude, and that the yaw angle of a pan-only camera onboard the UAV can be controlled, thereby controlling the camera's projected footprint on the ground. In turn, we include the robot's $x$ and $y$ coordinates on the map, heading angle $\theta$, velocity $v$, timestamp $t$, and sensor angle $\psi$ in our state spacemaking it *at least* a 6-degree-of-freedom (6-DoF) planning problem (we describe in Sec. [3](#sec:problem-and-notation){reference-type="ref" reference="sec:problem-and-notation"} how this can amount to planning in more than 6 DoFs).

We tackle this problem using a search-based approach. To the best of our knowledge, no previous work applies search-based planning to compute trajectories for a kinodynamically constrained robot and an onboard directional sensor to maximize coverage. We propose two approaches to do so, each with a different way to improve the solution.

:::: {#fig:toy-example .figure latex-placement="t"}
![](Kusnur2020Searchbased_figs/combined-itsa+history.png){width="\\columnwidth"}

::: caption
We present two algorithms for search-based planning for active sensing. (A) [SPlaSH]{.smallcaps} tries to minimize sensor footprint overlaps along the robot trajectory. For the last state in the figure, it would prefer the solid blue sensor footprint over the dashed blue so as to avoid the overlap denoted by the red area. (B) [SPLIT]{.smallcaps} iteratively refines an initial trajectory $\pi_i$ to maximize the area covered by the sensor to come up with the final trajectory $\pi_f$.
:::
::::

A key challenge in planning non-myopic sensor trajectories that maximize coverage is that in general, for a given robot trajectory, the optimal sensor configuration at a given point in the trajectory depends on all previous sensor measurements (the full *sensor history*) before it. One can appreciate this in 2D environments by thinking of sensor footprint overlapsto compute an optimal sensor configuration at a given location, a planner must take into account all overlaps with previously planned sensor footprints in the plan being considered. However, including the full sensor history in a state makes the search computationally intractable. Our first approach, **S**ensor **Pla**nning with **S**ensor **H**istory ([SPlaSH]{.smallcaps}), first computes a robot trajectory. It then searches for sensor plans for this fixed robot trajectory while maintaining a *partial* sensor history during searchthis prevents covering areas already sensed before in the trajectory, up to the size of the maintined sensor history. Even for a fixed robot trajectory, the space of sensor trajectories exponentially increases in dimensionality as we account for larger sensor histories (this might not be trivial to see, and so we detail how this occurs in Sec. [4](#sec:approach-one){reference-type="ref" reference="sec:approach-one"}). Our results show that in most planning problems considering 2D sensor footprint overlaps, only a partial history of sensor footprints actually affect computing the next optimal sensor configuration.

The basis of our second approach is the empirical observation that approximate search algorithms like Weighted A\* [(WA\*)]{.smallcaps} [@pohl1970heuristic] overlook better solutions that are actually "close" to the computed solution in the space of solution paths [@furcy2006itsa]. In our second approach, **S**ensor **P**lanning with **L**ocal **I**terative **T**unneling ([SPLIT]{.smallcaps}), we *split* the process into two steps:

- We first quickly compute suboptimal robot and sensor trajectories in *decoupled* robot- and sensor-state spaces (**initialization**).

- We then use this solution as initialization to a local-search routine that iteratively improves this solution in the *joint* robot- and sensor-state space until time runs out (**refinement**).

We adapt Iterative Tunneling Search with [A\*]{.smallcaps} ([ITSA\*]{.smallcaps}) [@furcy2006itsa] to our problem for the refinement step. This is detailed in Sec. [5](#sec:approach-two){reference-type="ref" reference="sec:approach-two"}.

The illustation in Fig. [1](#fig:toy-example){reference-type="ref" reference="fig:toy-example"} depicts both of our approaches on a toy example. Our approaches can be contextualized within several related works on sensor management and informative path planning, as we do in Sec. [2](#sec:related-work){reference-type="ref" reference="sec:related-work"}. In Sec. [3](#sec:problem-and-notation){reference-type="ref" reference="sec:problem-and-notation"}, we describe our problem and notation in detail. In sections [4](#sec:approach-one){reference-type="ref" reference="sec:approach-one"} and [5](#sec:approach-two){reference-type="ref" reference="sec:approach-two"}, we describe and provide pseudocode for both of our approaches. In Sec. [6](#sec:results){reference-type="ref" reference="sec:results"}, we evaluate our approaches and show their benefits in the context of a previously established planning framework for persistent coverage with multiple UAVs [@kusnur2019planning], where individual UAVs are tasked with generating collision-free trajectories that maximize information gain while navigating to an assigned goal. Note that our contribution lies in planning robot and sensor trajectories for a single UAV navigating to a goal (we do not attempt to solve the problem of coordinating UAV plans for coverage).

# Related Work {#sec:related-work}

Hero and Cochran present an extensive survey on sensor management [@hero2011sensor]. Gutpta et al. state general challenges and computational complexity of optimal sensor selection in detail in [@gupta2006stochastic]this is on similar lines as the computational challenge of maintaining a sensor history (see Fig [4](#fig:history){reference-type="ref" reference="fig:history"}, explained later). In general, optimal coverage has been addressed in various settings including mobile sensors and autonomous robots. Robotic sensing systems have used with both fixed sensors [@huang2017visual; @furgale2010visual] as well as sensors that execute pre-computed patterns [@scherer2012autonomous]. The problem of optimal mobile sensor location with unbounded ranges has been tackled as Voronoi space partitioning in [@du1999centroidal]. Many approaches have also been targeted to specific applications, such as active perception work  [@mori1990active; @costante2016perception]. The measurement control problem, also essentially a sensor scheduling problem, was shown to be solved by tree-search in general [@meier1967optimal]. To deal with computational intractability, several greedy solutions have been proposed [@gupta2006stochastic; @oshman1994optimal; @mukai1996active; @chung2004decentralized; @kagami2006sensor]. Further, Finite-horizon model predictive control provide improvement over myopic techniques but suffer from high run-times in large state spaces and provide no performance guarantees beyond the horizon depth [@bourgault2003coordinated; @ryan2010particle]. Arora et al. propose a data-driven approaches to sensor trajectory generation that map calculated features to sensory actions [@arora2015pasp].

Several recent works that fall under *informative path planning* are closely related to our work. Perhaps the most closely related is a recent line of work on active information acquisition, although with *fixed* sensors onboard robots: Atanasov et al. propose a non-greedy, value-iteration based offline solution with applications to gas distribution mapping and target localization [@atanasov2014information]. Schlotfeldt et al. then reformulate the problem as a deterministic planning problem and apply [A\*]{.smallcaps} search with the first consistent heuristic for information acquisition, with applications to active mapping [@schlotfeldt2019maximum]. Kantaros et al. then propose a probabilistically complete and asymptotically optimal sampling-based approach to this problem, along with strategies to bias exploration toward informative regions [@kantaros2019asymptotically]. Lu et al. propose a potential-function based method for integrated planning and control of robotic sensors deployed to classify multiple targets in an obstacle-populated environment [@lu2014information].

There are also lines of work that formulate information gathering as an Orienteering Problem. Of particular interest are [@vavna2015dubins; @faigl2017solution; @pvenivcka2019physical; @pvenivcka2019data] because of a similarity in their approaches with our initialize-and-refine approach in [SPLIT]{.smallcaps} (detailed further in Sec. [5](#sec:approach-two){reference-type="ref" reference="sec:approach-two"}). However these approaches focus on computing informative *tours*unlike our goal-directed setting, and perform local refinement over heading angles constrained by Dubin's-car dynamicsunlike our approach that refines sensor angles that observe the environment.

# Problem Formulation and Notation {#sec:problem-and-notation}

## Persistent coverage framework

We contextualize and evaluate our approaches within the persistent-coverage framework established in previous work [@kusnur2019planning]. This is a centralized framework that continuously computes goal locations to which UAVs should fly and kinodynamically feasible, globally deconflicting plans for them to do so, in a *prioritized planning* setting [@erdmann1987multiple]. While it is a multi-UAV system, we plan for UAVs independentlyplans between UAVs are not explictly coordinated in [@kusnur2019planning] and is out of the scope of this paper. Our specific contribution lies in planning robot and sensor trajectories for a single UAV navigating to a goal. The framework in [@kusnur2019planning] assumes a circular sensor footprint directly underneath the UAV. In this paper, we extend the system to incorporate a rectangular footprint offset from the UAVconsequently, different sensor headings correspond to the UAV observing different areas of the environment around it.

**Map.** The environment map $\ensuremath{\mathcal{M}}$ consists of a priority map $\ensuremath{\mathcal{M}^{\mathrm{C}}}$ and a no-coverage map $\ensuremath{\mathcal{M}^{\mathrm{NC}}}$. The UAV must attempt to cover each cell $c_{i,j}$ at row $i$ and column $j$ of $\ensuremath{\mathcal{M}^{\mathrm{C}}}$. Such a cell is associated with two values: its lifetime $l(i,j)$ and age $a(i,j)$the age of a cell is the time passed since the cell was last covered by a UAV, and its lifetime is a desired bound on its age. At any point of time t, $\ensuremath{\mathcal{M}^{\mathrm{C}}}$ holds the quantity $p(i,j) = l(i,j) - a(i,j)$ for each cell $c_{i,j}$. $\ensuremath{\mathcal{M}^{\mathrm{C}}}$ *decays* with time, meaning $p(i,j)$ for each cell $c_{i,j}$ reduces by one every second, thus making $c_{i,j}$ more *urgent*. Cells part of $\ensuremath{\mathcal{M}^{\mathrm{NC}}}$ do not need to be covered.

**Sensor.** In our setting, the sensor is a pan-only camera with one controllable DoF (yaw), which controls a downward-looking rectangular footprint of fixed and limited field-of-view. The area of the footprint is discretized into cells on the map according to an underlying resolution. We assume no noise in the footprint observed by the sensor.

**Robot.** The UAV is a kinodynamically constrained system, accounting for the robot's $x$ and $y$ coordinates, heading angle $\theta$, velocity $v$, and timestamp $t$. The UAV is said to be at a cell $c_{i,j}$ if the projection of its reference point onto the $xy$-plane lies in cell $c_{i,j}$. A cell is said to be covered by the UAV if any point on the cell is contained in the rectangular projection of the sensor footprint on the $xy$-plane.

## Problem formulation and definitions {#problem}

We represent this planning problem as a search over a finite, discrete search space. Here, we define the configuration spaces of the robot (UAV) and sensor, and three state spaces that are relevant to our approaches. Each state space is associated with a set of transitions, and they together define three separate search spaces.

:::: {#fig:transitions .figure latex-placement="t"}
![](Kusnur2020Searchbased_figs/transitions_new.png){width=".9\\columnwidth"}

::: caption
An example of the successor-generation functions for the three search spaces described in Sec. [3](#sec:problem-and-notation){reference-type="ref" reference="sec:problem-and-notation"}.
:::
::::

### Robot state space {#def:robot-space}

A feasible robot configuration is represented by $\ensuremath{c^\mathsf{R}}= (x, y, \theta, v, t)$ where $x$ and $y$ are the robot's $2D$ coordinates, $\theta$ is the UAV's heading, and $t$ is the global timestamp at which this configuration is achieved (the timestamp $t$ is part of $\ensuremath{c^\mathsf{R}}$ as we plan spatiotemporally collision-free trajectories for multiple robots in this framework). These five degrees of freedom together define the $5D$ robot state space $\ensuremath{\mathbb{E_\mathsf{R}}}$. A set of kinodynamically feasible motion primitives computed offline define a state lattice [@pivtoraiko2005generating] via a set of transitions $$\ensuremath{\mathbb{T}_\mathsf{R}}= \{ (\ensuremath{c^\mathsf{R}}_i, \ensuremath{c^\mathsf{R}}_j)\ |\ \ensuremath{c^\mathsf{R}}_i, \ensuremath{c^\mathsf{R}}_j \in \ensuremath{\mathbb{E_\mathsf{R}}}\}$$ This defines a search space represented by a graph $\ensuremath{\mathbb{G}_\mathsf{R}}$ with nodes $\ensuremath{\mathbb{E_\mathsf{R}}}$ and edges $\ensuremath{\mathbb{T}_\mathsf{R}}$. A robot trajectory $\ensuremath{\pi_\mathsf{R}}$ is a sequence of feasible robot configurations.

### Sensor state space {#def:sensor-space}

A sensor configuration is defined with respect to a corresponding robot configuration $\ensuremath{c^\mathsf{R}}$ as a tuple $\ensuremath{c^\mathsf{S}}= (t, \psi, \ensuremath{H^{\psi}})$, where $t$ is the timestamp in $\ensuremath{c^\mathsf{R}}$, $\psi$ is the sensor's heading angle in the global frame, and $\ensuremath{H^{\psi}}$ is a list denoting the history of sensor angles assigned at all timestamps earlier than $t$. These state variables collectively define the sensor state space $\ensuremath{\mathbb{E_\mathsf{S}}}$, with dimensionality $(1 + |\ensuremath{H^{\psi}}|)$[^2]. The set of feasible sensor motions define a set of transitions $$\ensuremath{\mathbb{T}_\mathsf{S}}= \{ (\ensuremath{c^\mathsf{S}}_i, \ensuremath{c^\mathsf{S}}_j)\ |\ \ensuremath{c^\mathsf{S}}_i, \ensuremath{c^\mathsf{S}}_j \in \ensuremath{\mathbb{E_\mathsf{S}}}\}$$ This defines a search space represented by a graph $\ensuremath{\mathbb{G}_\mathsf{S}}$ with nodes $\ensuremath{\mathbb{E_\mathsf{S}}}$ and edges $\ensuremath{\mathbb{T}_\mathsf{S}}$. A sensor trajectory $\ensuremath{\pi_\mathsf{S}}$ is a sequence of sensor configurations.

### Joint state space {#def:joint-space}

A feasible *joint-state* configuration $\ensuremath{c^\mathsf{J}}$ is a concatenation of a feasible robot configuration and sensor configuration $\langle \ensuremath{c^\mathsf{R}}, \ensuremath{c^\mathsf{S}}\rangle$. These state variables collectively define the joint state space $\ensuremath{\mathbb{E_\mathsf{J}}}$ of dimensionality $(6 + |\ensuremath{H^{\psi}}|)$. The set of feasible transitions in $\ensuremath{\mathbb{E_\mathsf{J}}}$ is a combination of feasible transitions in $\ensuremath{\mathbb{E_\mathsf{R}}}$ and $\ensuremath{\mathbb{E_\mathsf{S}}}$ $$\ensuremath{\mathbb{T}_\mathsf{J}}= \{ (\ensuremath{c^\mathsf{J}}_i, \ensuremath{c^\mathsf{J}}_j)\ |\ \ensuremath{c^\mathsf{J}}_i, \ensuremath{c^\mathsf{J}}_j \in \ensuremath{\mathbb{E_\mathsf{J}}}\}$$ This defines a search space represented by a graph $\ensuremath{\mathbb{G}_\mathsf{J}}$ with nodes $\ensuremath{\mathbb{E_\mathsf{J}}}$ and edges $\ensuremath{\mathbb{T}_\mathsf{J}}$. Note that since the state-lattice discretization in $\ensuremath{\mathbb{E_\mathsf{R}}}$ can be different from that in $\ensuremath{\mathbb{E_\mathsf{S}}}$, the transition set $\ensuremath{\mathbb{T}_\mathsf{J}}$ consists of actions that change robot and sensor states at their respective state discretizations.

Given these search spaces, we define the routine [Successors]{.smallcaps}$(s, \ensuremath{\mathbb{T}_\mathsf{R}})$ to be the successor-generation routine for a state $s$ that returns successor states in $\ensuremath{\mathbb{E_\mathsf{R}}}$. Similarly, we have the routines [Successors]{.smallcaps}$(s, \ensuremath{\mathbb{T}_\mathsf{S}})$ and [Successors]{.smallcaps}$(s, \ensuremath{\mathbb{T}_\mathsf{J}})$. Fig. [2](#fig:transitions){reference-type="ref" reference="fig:transitions"} illustrates these three types of successors, although with much smaller branching factors for $\mathbb{T}_\mathsf{R}$ and $\mathbb{T}_\mathsf{J}$. Specifically, in $\mathbb{T}_\mathsf{J}$ for example, we generate $3$ sensor-space successors for points at every 1s of a $4$-second long motion primitive. We have $12$ motion primitives per robot state on average, making the branching factor in the joint space $12 \times 4 \times 3 = 144$ on average. We also denote running algorithm [X]{.smallcaps} searching for a path from $\ensuremath{s_\mathit{start}}$ to $\ensuremath{s_\mathit{goal}}$ in search space $\mathbb{G}$ by [X]{.smallcaps}($s_\mathit{start}$, $s_\mathit{goal}$ $|$ $\mathbb{G}$). For example, [A\*($s_\mathit{start}$, $s_\mathit{goal}$$|$ $\mathbb{G}_\mathsf{J}$)]{.smallcaps} denotes running [A\*]{.smallcaps} search in the search space determined by $\mathbb{G}_\mathsf{J}$(meaning state transitions are determined by $\mathbb{T}_\mathsf{J}$).

## Cost Function {#sec:cost-function}

We now define the cost function associated with a transition from state $s$ to $s'$. We use two costsone associated with sensor coverage at $s'$ where $s' \in \ensuremath{\mathbb{E_\mathsf{S}}}$ or $\ensuremath{\mathbb{E_\mathsf{J}}}$, and the other associated with the UAV's motion primitive from $s$ to $s'$ where $s, s' \in \ensuremath{\mathbb{E_\mathsf{R}}}$ or $\ensuremath{\mathbb{E_\mathsf{J}}}$.

**Motion primitive cost.** Each motion primitive is a sequence of states forward-simulated from the corresponding robot state at $s,\ s_{robot} = (x, y, \theta, v, t)$, following double-integrator dynamics. The cost of the primitive is equal to the time taken for the UAV to execute it. More details about the motion primitives can be found in [@kusnur2019planning].

**Sensor coverage cost.** For the corresponding sensor state at $s'$, $s'_{sensor} = (t, \psi, H^\psi)$, the variables $x, y, \theta, \psi$ together define a 2D specific footprint of cells $\mathcal{F}$. Let a given footprint $\mathcal{F}$ cover $|\mathcal{F}|$ discrete cells in the map $\mathcal{M}$. Let the number of these cells lying in a coverage zone be given by $N_{\mathcal{C}}$ and those lying in a no-coverage zone be $N_{\mathcal{NC}}$: $$N_\mathcal{C} = \sum\limits_{i \in \mathcal{F}} \mathds{1}\left[i \in \ensuremath{\mathcal{M}^{\mathrm{C}}}\right] \ \text{and}\  N_\mathcal{NC} = \sum\limits_{i \in \mathcal{F}} \mathds{1}\left[i \in \ensuremath{\mathcal{M}^{\mathrm{NC}}}\right]$$

### No sensor history

If we ignore the sensor history, the cost of a footprint is given by the sum of priorities of all coverage cells in $\mathcal{F}$, and an additive penalty $\lambda$ scaled by the fraction of no-coverage cells in $\mathcal{F}$: $$\begin{equation}
\label{eqn:cost-without-history}
\mathsf{cost}_{0}(\mathcal{F}) =
    \overbrace {
    %   \Biggl(
            % \sum_{ \substack{ i \in \mathcal{F} \\ i \in \mathcal{C} } } p_i
            \sum_{ i \in \mathcal{F} \land \mathcal{C} } p_i
    %   \Biggr)
    }^\text{criticality measure}
        +\
    \overbrace {
        \mathbf{\lambda}
        \times
        % \Biggl(
            \frac{ N_{\mathcal{NC}} }{ | \mathcal{F} | }
        % \Biggr)
    }^{\substack{\text{penalize} \\ \text{no-coverage cells}}}
\end{equation}$$

### With sensor history

We define the following sensor coverage cost for this footprint $\mathcal{F}$ (where '$\mathds{1}$' represents the indicator function):

$$\begin{equation}
\label{eqn:cost-with-history}
    \mathsf{cost}_{H}(\mathcal{F}) =
        \overbrace {
%       \Biggl(
            % \sum_{ \substack{ i \in \mathcal{F} \\ i \in \mathcal{C} } }
            \sum_{ i \in \mathcal{F} \land \mathcal{C} }
                \underbrace { \mathds{1}[ i \notin \mathcal{H}^\psi ] \times p_i }_\text{not in history} +
                \underbrace { \mathds{1}[ i \in \mathcal{H}^\psi ] \times l_i }_\text{in history}
%       \Biggr)
        }^\text{criticality measure}
                +\
            \overbrace {
                \mathbf{\lambda} \times  \frac{ N_{\mathcal{NC}} }{ | \mathcal{F} | } }^{\substack{\text{penalize} \\ \text{no-coverage cells}}}
\end{equation}$$ This cost function is illustrated in Fig. [3](#fig:cost-function){reference-type="ref" reference="fig:cost-function"}. Note that Eq. [\[eqn:cost-with-history\]](#eqn:cost-with-history){reference-type="ref" reference="eqn:cost-with-history"} reduces to Eq. [\[eqn:cost-without-history\]](#eqn:cost-without-history){reference-type="ref" reference="eqn:cost-without-history"} when no history is considered.

:::: {#fig:cost-function .figure latex-placement="t"}
![](Kusnur2020Searchbased_figs/costs.png){width="\\columnwidth"}

::: caption
Pictorial explanation of our cost function $\mathsf{cost}_{H}(\mathcal{F})$ from Eq. [\[eqn:cost-with-history\]](#eqn:cost-with-history){reference-type="ref" reference="eqn:cost-with-history"}. We consider history size, $H = 2$ in this example. For the last UAV state on the green trajectory $\ensuremath{\pi_\mathsf{R}}$, the sensor footprint is shaded in three colours. The blue area is the overlap with previous footprints in $\ensuremath{\pi_\mathsf{R}}$, while the red and dark green areas do not overlap. For Eq. [\[eqn:cost-with-history\]](#eqn:cost-with-history){reference-type="ref" reference="eqn:cost-with-history"}, the blue area is *in history*, the red area is *not in history*, and the dark green area is *penalize no-coverage cells*. Note that for footprints too far in the past, even if there was an overlap, it has no effect.
:::
::::

# **S**ensor **Pla**nning with **S**ensor **H**istory ([SPlaSH]{.smallcaps}) {#sec:approach-one}

In this section, we describe out first approach, [SPlaSH]{.smallcaps}. [SPlaSH]{.smallcaps} first quickly computes a suboptimal robot trajectory using Multi-Heuristic [A\*]{.smallcaps} ([MHA\*]{.smallcaps}) search in $\mathbb{G}_\mathsf{R}$. This search is performed with the motion primitive cost function (Sec. [3.3](#sec:cost-function){reference-type="ref" reference="sec:cost-function"}). Then, it computes a sensor trajectory using (uninformed-)[A\*]{.smallcaps} search in $\mathbb{G}_\mathsf{S}$ for a given history $\mathsf{H}$. This search is performed with the sensor coverage cost function $\mathsf{cost}_{H} (\mathcal{F})$ (Sec. [3.3](#sec:cost-function){reference-type="ref" reference="sec:cost-function"}).

[MHA\*]{.smallcaps} is a variant of A\* that can use multiple arbitrarily inadmissible heuristics. We omit details for brevity and refer the reader to the paper for details [@aine2016multi]. We use (1) a Euclidean distance heuristic, (2) a Dubin's path length heuristic, and (3) a Dijkstra's shortest path length heuristic.

Note that here and henceforth in this paper, when we mention [A\*]{.smallcaps}, we are talking about *uninformed* [A\*]{.smallcaps} (without a heuristic). We set aside formulating with a consistent heuristic for sensor coverage in our setting for future work. However, both [SPlaSH]{.smallcaps} and [SPLIT]{.smallcaps} both work unchanged with the addition of a heuristic. The pseudocode for [SPlaSH]{.smallcaps} can be found in Alg. [\[alg:decoupled\]](#alg:decoupled){reference-type="ref" reference="alg:decoupled"}.

:::: {#fig:history .figure latex-placement="t"}
![](Kusnur2020Searchbased_figs/dijkstra.png){width="\\columnwidth"}

::: caption
Graph representation for sensor planning for history size $H = 0$ (*above*) and $H = 1$ (*below*). Each level $l$ in the graph corresponds to a state in the UAV trajectory $\ensuremath{\pi_\mathsf{R}}$. The search space size increases with increasing history sizes. Thus, duplicates (highlighted by coloured arrows and nodes) appear less frequently with increasing history sizes making the search for an optimal $\ensuremath{\pi_\mathsf{S}}$ more expensive.
:::
::::

:::: algorithm
**Input:** $s_\mathit{start}$, $s_\mathit{goal}$, $\mathsf{H}$\
**Output:** $\pi_f$ (final trajectory in joint space)

::: algorithmic
$\pi_\mathit{robot} \gets$ [MHA\*($s_\mathit{start}$, $s_\mathit{goal}$$|$ $\mathbb{G}_\mathsf{R}$)]{.smallcaps} $\pi_\mathit{sensor} \gets$ [A\*]{.smallcaps}($s_\mathit{start}$, $s_\mathit{goal}$$|$ $\mathbb{G}_\mathsf{S}$) with $\mathsf{H}$ states in sensor history $\pi_\mathit{joint} \gets$ concatenate $\pi_\mathit{robot}$ and $\pi_\mathit{sensor}$ $\pi_\mathit{joint}$
:::
::::

The most important aspect of [SPlaSH]{.smallcaps} is accounting for sensor history in Line 3. Fig. [4](#fig:history){reference-type="ref" reference="fig:history"} illustrates the effect of history values $H = 0$ and $H = 1$ on the search graph $\ensuremath{\mathbb{G}_\mathsf{S}}$ for a given initial sensor heading $\psi_0$. Each level in Fig. [4](#fig:history){reference-type="ref" reference="fig:history"} corresponds to a waypoint along the robot trajectory $\ensuremath{\pi_\mathsf{R}}$. The figure denotes state $\ensuremath{c^\mathsf{S}}= (t, \psi, \ensuremath{H^{\psi}})$ as a tuple where $\ensuremath{H^{\psi}}$ is the last $H$ elements in the tuple. For any state $\ensuremath{c^\mathsf{S}}$, the sensor angle can either be changed by one step (increment or decrement), or it may remain the same.

The effect of $H$ values is illustrated by the coloured arrows and vertices in the graphtwo arrows of the same color end up at a unique state in the graph. The key idea is as follows: For $H = 0$, ending up at $\psi_0$ on level $2$ is considered the same state, whether you come from $\psi_0$ or $\psi_{-1}$ or $\psi_{1}$we only care about the *current* sensor angle. But for $H = 1$, ending up at $\psi_0$ on level $2$ is considered a different state in all these three cases because we maintain $1$ historical sensor angle. This can be incorporated by defining the state as $\ensuremath{c^\mathsf{S}}= (t, \psi, \ensuremath{H^{\psi}})$. Observe that states are replicated in this way a lot more frequently for $H = 0$ than for $H = 1$, meaning the graph for $H = 0$ has much (in fact, exponentially) lesser states than that for $H = 1$.

# **S**ensor **P**lanning with **L**ocal **I**terative **T**unneling ([SPLIT]{.smallcaps}) {#sec:approach-two}

:::: algorithm
**Input:** $s_\mathit{start}$, $s_\mathit{goal}$, $\mathsf{T}_{\mathsf{overall}}$ (time limit)\
**Output:** $\pi_f$ (final trajectory in joint space)

::: algorithmic
$\pi_i \gets$ [SPlaSH]{.smallcaps}$(\ensuremath{s_\mathit{start}}, \ensuremath{s_\mathit{goal}}, \mathsf{H}=0)$ $\mathsf{t}_\text{\textsc{SPlaSH}{}} \gets$ time taken for [SPlaSH]{.smallcaps} to terminate $\pi_f \gets$ [LocalIterativeTunneling]{.smallcaps}($\pi, \mathsf{T}_\mathsf{overall} - \mathsf{t}_\text{\textsc{SPlaSH}{}}$) $\pi_f$

$\ensuremath{s_\mathit{start}}\gets$ first state in $\pi$ $\ensuremath{s_\mathit{goal}}\gets$ last state in $\pi$ $g(\ensuremath{s_\mathit{goal}}) = \infty$; $g(\ensuremath{s_\mathit{start}}) = 0$ $bp(\ensuremath{s_\mathit{start}}) = bp(\ensuremath{s_\mathit{goal}}) =$ `NULL` Insert $\ensuremath{s_\mathit{start}}$ into `OPEN` with [key]{.smallcaps}$(\ensuremath{s_\mathit{start}})$ $s \gets$ `OPEN`.[min()]{.smallcaps} Backtrack from $s$ to obtain solution $\pi_f$ **break** $g(s') = g(s) + c(s, s')$ $bp(s') = s$ $\pi_f$

$g(s) + h(s)$
:::
::::

[SPlaSH]{.smallcaps} takes into account sensor history and incentivizes the search to compute plans where overlaps are minimized. However, it operates with a fixed, suboptimal robot trajectory that optimizes only motion primitive cost. Recall that it is empirically observed that approximate search algorithms tend to overlook better solutions that are actually "close" to the computed solution in the space of solution paths [@furcy2006itsa]. The final solution that [SPlaSH]{.smallcaps} gives ussay $\pi$is most likely suboptimal with respect to the coverage cost in the space of joint-space solutions. **S**ensor **P**lanning with **L**ocal **I**terative **T**unneling ([SPLIT]{.smallcaps}) locally refines $\pi$ by performing searches in small search spaces around $\pi$ in the joint space, increasing in size with each iteration. We call these search spaces *tunnels*, and this is an application of the ITSA\* algorithm [@furcy2006itsa].

We provide pseudocode for [SPLIT]{.smallcaps} in Alg. [\[alg:hybrid\]](#alg:hybrid){reference-type="ref" reference="alg:hybrid"}. Lines in [blue]{style="color: blue"} indicate the differences from standard [A\*]{.smallcaps} search. Line 2 obtains the initial solution from [SPlaSH]{.smallcaps}. Then, [LocalIterativeTunneling]{.smallcaps} refines this solution locally by performing [A\*]{.smallcaps} searches in iterative tunnels. The "level" of a state $s$ corresponds to the distance from the initial path $\pi_i$ to $s$ computed as the smallest number of edges on a path from any state on $\pi_i$ to $s$ [@furcy2006itsa]. In the beginning, every state on the initial plan $\pi_i$ is stored in memory with level $0$.

The refinement process is essentially [A\*]{.smallcaps} being performed repeatedly, with the addition of lines $25$$27$. The level of any newly generated state is set to one more than the level of its parent. Only a state whose level is lesser than the current iteration number is inserted into the OPEN list. This is what creates tunnels increasing in size per iteration. [LocalIterativeTunneling]{.smallcaps}and consequently, [SPLIT]{.smallcaps}terminates when the time available for local refinement runs out.

# Experimental Results {#sec:results}

We evaluate our approaches by running them over $200$ randomly generated start-goal pairs over several maps. We pick maps as seen in the persistent coverage framework described in [@kusnur2019planning] (Sec. [3](#sec:problem-and-notation){reference-type="ref" reference="sec:problem-and-notation"}) ($10$ start-goal pairs per map for $20$ maps). The maps are generated by letting the map in the framework decay for several minutes while one UAV with a fixed sensor covers it persistently. We pick versions of the map at different points in time, which gives us maps with complex coverage zones.

**Evaluation.** We use the following set of facts to compare any two trajectories: Let a given trajectory in the joint space cover $N$ cells that lie in coverage zones. Let the quantity $\sum_{i} p_i$ denote the sum of priorities of all such cells. The quantity $\bar{P} = \frac{\sum_{i} p_i}{N}$ denotes the average of the priority values of all such cells. We value two things: covering a large number of cells, and covering important cells (those with a low priority value). Thus, a large value of $N$ and low values of $\sum_{i} p_i$ and $\bar{P}$ are desirable for a given plan. For any two plans having the same value of $\bar{P}$, we prefer the one with the larger number of covered cells. If a plan has a low value of $N$ as well as a large value of $\bar{P}$, it is undesirable.

Since [SPlaSH]{.smallcaps} penalizes footprint overlaps, we see an increase in the number of cells covered as a larger sensor history is maintained (see Fig. [5](#fig:splash-results){reference-type="ref" reference="fig:splash-results"}). We also see that maintaining a sensor history of size $5$ gives us no more value than size $3$ in practical settings. Also notice that $\bar{P}$ stays fairly unchanged over several trajectories. This can be attributed to the maps have many different priority values for cells and no single, contiguous coverage zonemaintaining sensor history would lead to covering more cells, but the average priority over these cells would be approximately the same.

Since [SPLIT]{.smallcaps} refines the trajectory locally to optimize coverage cost, we see an increase in information gain, or a decrease in $\sum_{i} p_i$, with each iteration (see Fig. [6](#fig:split-results){reference-type="ref" reference="fig:split-results"}). We also see decreasing path costs (g-value of the goal) with each iteration. If we consider a timeout of $\sim 5$s for real-time planning purposes, we see that $2$ or $3$ iterations are feasible. Note that its performance largely depends on the immediate area around the initial plan which will be explored in the iterative tunnels. If this immediate area has only a few more important cells to cover, the refined plan will largely stay the same.

:::: {#fig:splash-results .figure latex-placement="t"}
![](Kusnur2020Searchbased_figs/decoupled_results.png){width="\\columnwidth"}

::: caption
Results of running [SPlaSH]{.smallcaps} for sensor histories of size $0, 3, 5$.
:::
::::

:::: {#fig:split-results .figure latex-placement="t"}
![](Kusnur2020Searchbased_figs/iterative_tunneling_results.png){width="\\columnwidth"}

::: caption
Results of running [SPLIT]{.smallcaps} timed out at $30$s.
:::
::::

A natural baseline is to search directly in the joint space of robot and sensor variables. This requires a cost function that is a linear combination of the motion primitive and sensor coverage cost. Running [MHA\*]{.smallcaps} on these start-goal pairs with such a cost function yielded an average planning time of $8.44\ \pm\ 6.40$ssignificantly larger than running [SPlaSH]{.smallcaps} with a sensor history of size $3$ or [SPLIT]{.smallcaps} for $2$ or $3$ iterations. (We set a timeout of $20$s while obtaining this value, so this is a conservative estimate and true value is in fact larger.)

Note that iteration $4$ onward [SPLIT]{.smallcaps} takes a lot of time to convergethis is not useful for real-time planning problems. However, we include them in the results to demonstrate that the solution can still improve after the third iteration (and that a local minimum is not reached within $3$ iterations).

# Conclusion and Future Work {#conclusion}

We present two search-based approaches for generating robot and sensor trajectories in goal-directed 2D coverage tasks, namely **S**ensor **Pla**nning with **S**ensor **H**istory ([SPlaSH]{.smallcaps}) and **S**ensor **P**lanning with **L**ocal **I**terative **T**unneling ([SPLIT]{.smallcaps}). [SPlaSH]{.smallcaps} solves for robot and sensor trajectories independently in decoupled state spaces while maintaining a history of sensor headings during the search. [SPLIT]{.smallcaps} is a two-step approach that first quickly computes a solution in decoupled state spaces and then refines it by searching its local neighborhood in the joint space for a better solution. We show that both these approaches are practical alternatives to running standard search-based planning in the full joint space of robot and sensor state variables.

A limitation of [ITSA\*]{.smallcaps}, and consequently of [SPLIT]{.smallcaps}, is that the [A\*]{.smallcaps} searches do not reuse any search efforts between subsequent iterations, and so each iteration takes longer than the last. Reusing search efforts between iterations will lead to considerable speed-ups, leading to faster refinement of the trajectory. Further, we do not look into maintaining sensor histories within [SPLIT]{.smallcaps}. It can be useful to adaptively increase the size of the sensor history maintained with increasing iterations in [SPLIT]{.smallcaps}. We set aside these two limitations as opportunities for future work.

[^1]: All authors are with the Robotics Institute, Carnegie Mellon University, Pittsburgh, USA `{tkusnur, dsaxena, maxim}@cs.cmu.edu`.

[^2]: Note that $t$ is a known variable and no search is performed over it, and thus it does not contribute to the dimensionality of $c^\mathsf{S}$.
