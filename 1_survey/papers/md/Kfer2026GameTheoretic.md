---
citation_key: Kfer2026GameTheoretic
arxiv_id: 2601.20054
arxiv_url: https://arxiv.org/abs/2601.20054
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:48:00Z
origin: ai+web
reviewed: false
---

# Introduction

The deployment of self-driving cars promises improvements in safety, efficiency, and comfort in day-to-day transportation, but it also introduces fundamental challenges in planning with interactions. In mixed traffic, coordination is decentralized, and vehicle interactions combine cooperative and competitive elements: all vehicles must comply with shared traffic rules to ensure safety, yet strategic behavior naturally arises in scenarios such as merging, lane changing, and overtaking. To model the pursuit of individual objectives under shared constraints, noncooperative game theory has been widely used to cast autonomous driving as a complete-information game [@game_drive; @game_lane; @game_dec]. Compared to model predictive control approaches that ignore strategic interaction, game-theoretic formulations can better capture anticipatory behavior and improve performance in interactive scenarios [@out_MPC_game; @Yan2023Decision]. A particularly useful subclass is (generalized) potential games, where unilateral incentives are aligned with a single scalar potential function, yielding algorithmic and theoretical tractability [@Bhatt_2025; @pot_ilqr; @pot_game_drive; @pot_urb]. The versatility of potential games has led to their adoption in diverse multi-agent settings [@bakolas2021TaskAssignment; @lee2021RelayPursuit; @best_response_drone; @dist_potential].

A key difficulty in multi-vehicle planning is that it is inherently hybrid: discrete decisions arise from lane selection and maneuver choices, while continuous decisions are governed by vehicle dynamics. This hybrid structure is often modeled via mixed-integer programs [@DeitsTedrake2015MIP; @EarlDAndrea2002MILP; @Mixed_Pot_game; @RichardsHow2002MILP], but such formulations can tightly couple discrete and continuous variables, limiting scalability and making it difficult to exploit problem structure in large multi-vehicle settings [@combin_drive; @PadenCYYF16].

To address these challenges, we leverage Graphs of Convex Sets (GCS) [@GCS_thesis; @GCS], which is a recently proposed optimization framework that has been successfully applied to trajectory optimization and motion planning problems with collision avoidance [@Kurtz2023GCSMotionPlanning; @GCS_traj; @GCS_SPP]. In GCS, discrete decisions are represented by a graph topology: vertices correspond to convex feasible regions (${\it e.g.}$, safe sets for each vehicle), and edges encode feasible transitions between them (${\it e.g.}$, collision-free trajectories from one feasible region to another). This representation preserves convexity within regions and along transitions, and it admits a convex relaxation that is often tight in practice [@GCS], enabling efficient computation while capturing combinatorial structure.

In this work, we present IBR-GCS, a GCS-based method for multi-vehicle highway driving that models interaction as a noncooperative game with potentially conflicting objectives while respecting traffic rules. The proposed approach, IBR-GCS, integrates combinatorial maneuver reasoning, trajectory planning, and game-theoretic interaction within a unified framework. At each iteration, vehicle $i$ constructs a strategy-dependent GCS whose vertices represent lane-specific collision-free regions over time and whose edges encode dynamically feasible, safety-preserving transitions. Given the current strategies of the other vehicles, the resulting best-response computation reduces to a shortest-path problem (SPP) in GCS, yielding a mixed-integer convex formulation with an efficient convex relaxation that is often tight in practice. We embed these updates in an Iterative Best-Response (IBR) scheme and provide conditions under which the resulting inexact best-response dynamics converge to an approximate generalized Nash equilibrium (GNE). We evaluate IBR-GCS in numerical simulations of multi-lane highway scenarios, demonstrating safe trajectories and strategically consistent behaviors.

The remainder of the paper is organized as follows. Section [2](#sec_preliminaries){reference-type="ref" reference="sec_preliminaries"} reviews graphs of convex sets and generalized potential games. Section [3](#sec_problem_formulation){reference-type="ref" reference="sec_problem_formulation"} formalizes the multi-vehicle driving game and states the key assumptions. Section [4](#sec_approach){reference-type="ref" reference="sec_approach"} presents IBR-GCS, including the strategy-dependent GCS construction, the iterative best-response algorithm, and the accompanying error analysis. Section [5](#sec_simulation_results){reference-type="ref" reference="sec_simulation_results"} presents simulation results. Finally, Section [6](#sec_conclusion){reference-type="ref" reference="sec_conclusion"} discusses conclusions.

# Preliminaries {#sec_preliminaries}

This section reviews GCS and generalized potential games, which form the basis for the proposed approach.

## Shortest Path Problem in Graphs of Convex Sets {#sec_gcs}

The GCS framework provides a graph-based representation for optimization problems that combine continuous decision variables with a combinatorial structure. The framework was originally introduced for trajectory optimization and motion planning with obstacle avoidance. A detailed formulation can be found in [@GCS_thesis; @GCS].

::: definition
A graph of convex sets is a directed graph $\mathcal{G}=(\mathcal{V}, \mathcal{E})$ with vertex set $\mathcal{V}$ and edge set $\mathcal{E}$, where each vertex $V \in \mathcal{V}$ is associated with a convex set $\mathcal{X}_V \subset \mathbb{R}^n$, and each directed edge $e = (U,W) \in \mathcal{E}$ represents an admissible one-step move from vertex $U$ to vertex $W$ (${\it i.e.}$, between the sets $\mathcal{X}_U$ and $\mathcal{X}_W$).
:::

In the relevant literature, vertices typically correspond to convex feasible regions that are subsets of the state or trajectory space, while edges encode admissible transitions between regions, such as continuity, dynamical feasibility, or safety constraints [@Kurtz2023GCSMotionPlanning; @GCS_traj].

Each vertex $V\in\mathcal{V}$ is associated with a continuous decision variable $x_V \in \mathcal{X}_V$. For each edge $e =(U,W) \in \mathcal{E}$, convex constraints may couple $(x_U,  x_W)$ via $(x_U, x_W) \in \mathcal{X}_e$, where $\mathcal{X}_e \subset \mathbb{R}^n \times \mathbb{R}^n$ is a convex set. Each edge may also be assigned a convex nonnegative cost function $c_e: \mathcal{X}_e \to \mathbb{R}_{\ge 0}$. Additionally, vertices may be assigned convex nonnegative costs $c_V: \mathcal{X}_V \to \mathbb{R}_{\ge 0}$.

We recall the definition of a path in a graph of convex sets.

::: definition
Given a source vertex $V_0$ and a target vertex $V_K \neq V_0$, a path is a sequence of vertices $(V_0, \dots, V_K)$ and directed edges such that $(V_{k-1}, V_k) \in \mathcal{E}$ for all $k=1,\dots,K$.
:::

To find a minimum-cost path through $\mathcal{G}$, we introduce binary decision variables $z_e \in \{0,1\}$ for all $e \in \mathcal{E}$ to indicate whether an edge $e$ is selected, and vertex-selection variables $y_V \in [0,1]$ for all $V \in \mathcal{V}$ (equal to $1$ for vertices $V$ on the selected path and $0$ otherwise under the flow constraints below). For each vertex $V \in \mathcal{V}$, let $\mathcal{E}^{\mathrm{in}}_V \coloneqq \{(U, V) \in \mathcal{E}\}$ and $\mathcal{E}^{\mathrm{out}}_V \coloneqq \{(V, W) \in \mathcal{E}\}$ denote its sets of incoming and outgoing edges, respectively. A standard mixed-integer formulation of the GCS shortest path problem is as follows: $$\label{eq_gcs_shortest_path}
\begin{align}
& \mathop{\mathrm{\mathrm{minimize}}}_{\substack{\{x_V, y_V\}_{V \in \mathcal{V}},\\ \{z_e\}_{e \in \mathcal{E}},\\}}
&& \sum_{e=(U,W) \in \mathcal{E}} z_e\, c_e(x_U, x_W) + \sum_{V\in\mathcal{V}} y_V\, c_V(x_V) \label{eq_gcs_shortest_path_obj} \\
& \mathop{\mathrm{\mathrm{subject~to}}}
&& \sum_{e \in \mathcal{E}^{\mathrm{in}}_V} z_e + \delta_{V,V_{0}} = \sum_{e \in \mathcal{E}^{\mathrm{out}}_V} z_e + \delta_{V,V_{K}}, && \forall V \in \mathcal{V}, \label{eq_gcs_shortest_path_flow} \\
&&& y_V = \delta_{V,V_0} + \sum_{e\in\mathcal{E}^{\mathrm{in}}_V} z_e, && \forall V\in\mathcal{V}, \label{eq_gcs_shortest_path_ydef}\\
&&& x_V \in \mathcal{X}_V, && \forall V \in \mathcal{V}, \label{eq_gcs_shortest_path_feas} \\
&&& z_e = 1 \ \Rightarrow\ (x_U,x_W)\in\mathcal{X}_e, && \forall e=(U,W)\in\mathcal{E}, \label{eq_gcs_shortest_path_edgefeas} \\
&&& z_e \in \{0,1\}, && \forall e \in \mathcal{E}, \label{eq_gcs_shortest_path_binary}\\
&&& 0 \le y_V \le 1, && \forall V\in\mathcal{V}. \label{eq_gcs_shortest_path_ybox}
\end{align}$$ Here, $\delta_{V, W}$ denotes the Kronecker delta, where $\delta_{V, W}=1$, if $V = W$, and $\delta_{V, W}=0$, otherwise. In [\[eq_gcs_shortest_path_flow\]](#eq_gcs_shortest_path_flow){reference-type="eqref" reference="eq_gcs_shortest_path_flow"}, the terms $\delta_{V, V_0}$ and $\delta_{V, V_K}$ therefore create the required unit flow imbalance at the source vertex $V_0$ and target vertex $V_K$. In contrast to the classical SPP [@short_path], the GCS SPP is NP-hard in general, ${\it cf.}$ [@GCS Theorem 3.1].

### Convex Relaxation

A standard convex relaxation replaces [\[eq_gcs_shortest_path_binary\]](#eq_gcs_shortest_path_binary){reference-type="eqref" reference="eq_gcs_shortest_path_binary"} with the box constraint $0 \le z_e \le 1$ and converts the implications in [\[eq_gcs_shortest_path_edgefeas\]](#eq_gcs_shortest_path_edgefeas){reference-type="eqref" reference="eq_gcs_shortest_path_edgefeas"} into a convex perspective (or conic) formulation; see [@GCS_thesis; @GCS] for canonical constructions. This relaxation can be tight in many motion-planning instances, but in general it may be loose [@GCS_thesis Proposition 8.1]. Existing formal tightness guarantees are limited to restrictive settings [@GCS_thesis Proposition 8.2]. In this paper, we empirically observe tightness in our setting (${\it cf.}$ Section [5](#sec_simulation_results){reference-type="ref" reference="sec_simulation_results"}), but we do not claim a general tightness guarantee.

## Generalized Potential Games {#sec_potential_games}

We consider a game with $N$ vehicles, indexed by $\mathcal{N} \coloneqq \{1, \ldots, N\}$. Vehicle $i \in \mathcal{N}$ chooses a strategy $\theta_{i}$, which in our driving setting represents a finite-horizon motion plan (trajectory and lane-change actions) and will later be encoded as a path through a vehicle-specific graph of convex sets. Vehicle $i$ incurs a cost $J_{i} (\theta_{i}, \theta_{-i})$, where $\theta_{-i} \coloneqq (\theta_1, \dots, \theta_{i-1}, \theta_{i+1}, \dots, \theta_N)$ denotes the strategies of all other vehicles. In our setting, feasibility depends on other vehicles through coupled constraints, so we use a *generalized* strategy set of the form $$\begin{align}
\label{generalized_strategy_set}
\Theta_{i} (\theta_{-i}) \coloneqq \{\theta_i \mid (\theta_i,\theta_{-i}) \in \Theta\},
\end{align}$$ where $\Theta$ is the joint feasible set. Each vehicle's cost is a function $J_i : \Theta \to \mathbb{R}$, evaluated on feasible joint strategies $\theta=(\theta_i, \theta_{-i}) \in \Theta$.

Collecting the vehicles, costs, and coupled feasibility constraints yields a game in which each vehicle solves an optimization problem whose feasible set depends on the other vehicles' strategies.

::: definition
[]{#def_game label="def_game"} The game is denoted by $G$ and is specified by the following set of coupled optimization problems: $$\begin{equation}
 \label{eq_game_def}
G \coloneqq \left\{
\begin{aligned}
\mathop{\mathrm{\mathrm{minimize}}}_{\theta_i}\quad & J_i(\theta_i,\theta_{-i})\\
\mathop{\mathrm{\mathrm{subject~to}}}\quad & \theta_i \in \Theta_i(\theta_{-i}),
\end{aligned}
\right. \qquad \forall i \in \mathcal{N}.
\end{equation}$$
:::

A central solution concept for games of this form is the Generalized Nash Equilibrium (GNE), in which no vehicle can unilaterally reduce its cost while satisfying the feasibility constraints imposed by the other vehicles' strategies.

::: definition
[]{#def_GNE label="def_GNE"} A strategy profile $\theta^\star \in \Theta$ is a GNE of $G$ if, for every vehicle $i \in \mathcal{N}$, $$\begin{equation}
 \label{eq_GNE_def}
J_i(\theta_i^\star, \theta_{-i}^\star) \le J_i(\theta_i,\theta_{-i}^\star),
\qquad \forall \theta_i \in \Theta_i(\theta_{-i}^\star).
\end{equation}$$
:::

To analyze the existence of equilibria and the behavior of best-response dynamics, it is often useful to identify games whose incentives can be summarized by a single scalar function. This motivates the notion of a generalized potential game, which extends exact potential games to settings with coupled feasibility constraints [@pot].

::: definition
[]{#def_GPG label="def_GPG"} The game $G$ is a generalized potential game if there exists a function $\Phi:\Theta \to \mathbb{R}$ such that for all $i \in \mathcal{N}$ and all $\theta_{-i}$ for which $\Theta_i(\theta_{-i})\neq\emptyset$, it holds for all $\theta_i,\theta_i'\in \Theta_i(\theta_{-i})$ that $$\begin{equation}
\label{eq_GPG_def}
J_i(\theta_i',\theta_{-i}) - J_i(\theta_i,\theta_{-i}) = \Phi(\theta_i',\theta_{-i}) - \Phi(\theta_i,\theta_{-i}).
\end{equation}$$ The function $\Phi$ is called a *generalized potential*.
:::

We next introduce the iterative best-response (IBR) dynamics that will be used in Section [4](#sec_approach){reference-type="ref" reference="sec_approach"}. Given $\theta_{-i}$, the set of best responses for each vehicle $i \in \mathcal{N}$, denoted $\mathrm{BR}_i(\theta_{-i})$, is given by $$\begin{equation}
\label{eq_best_response}
\mathrm{BR}_i(\theta_{-i}) \coloneqq \mathop{\mathrm{\mathrm{argmin}}}_{\theta_i \in \Theta_i(\theta_{-i})} J_i(\theta_i,\theta_{-i}).
\end{equation}$$ Starting from an initial feasible profile $\theta^{0} \in \Theta$, IBR updates vehicles sequentially. We define $$\begin{equation}
\label{eq_theta_intermediate}
\theta^{k,i} \coloneqq (\theta_1^{k+1}, \ldots, \theta_i^{k+1}, \theta_{i+1}^{k}, \ldots, \theta_N^{k}),
\qquad i = 1,\ldots,N,
\end{equation}$$ for the intermediate profile after vehicles $1, \ldots, i$ have been updated during iteration $k$. With this, the update rule is $$\begin{equation}
 \label{eq_IBR_update}
\theta_i^{k+1} \in \mathrm{BR}_i(\theta_{-i}^{k,i-1}), \qquad i=1, \ldots, N, \quad k \ge 0,
\end{equation}$$ with $\theta^{k,0}=\theta^{k}$ at the beginning of iteration $k$ and $\theta^{k,N}=\theta^{k+1}$ at the end of iteration $k$. In a generalized potential game, any exact best-response update is a descent step for the potential function $\Phi$. A standard result is given below, ${\it cf.}$ [@pot].

::: proposition
[]{#prop_potential_descent label="prop_potential_descent"} Suppose $G$ is a generalized potential game with generalized potential $\Phi$ (Definition [\[def_GPG\]](#def_GPG){reference-type="ref" reference="def_GPG"}). If, at some intermediate profile $\theta^{k,i-1}$, vehicle $i \in \mathcal{N}$ performs an exact best-response update [\[eq_best_response\]](#eq_best_response){reference-type="eqref" reference="eq_best_response"}, then $$\begin{align*}
\Phi(\theta^{k,i}) \le \Phi(\theta^{k,i-1}).
\end{align*}$$ Consequently, if all vehicles update with exact best responses, the sequence $\{\Phi(\theta^k)\}_{k\ge 0}$ is monotonically non-increasing along IBR, and therefore convergent, if $\Phi$ is bounded below on $\Theta$.
:::

# Problem Formulation {#sec_problem_formulation}

We consider a multi-vehicle highway driving scenario with $N$ vehicles indexed by $\mathcal{N}\coloneqq\{1,\ldots,N\}$ operating on a set of straight lanes $\mathcal{L}\subset \mathbb{N}$, as illustrated in Fig. [1](#fig_vehicles){reference-type="ref" reference="fig_vehicles"}. Planning is performed over a finite-horizon $\mathcal{T}\coloneqq\{0,\ldots,T-1\}$ with a discretization step $\Delta t \in \mathbb{R}_{> 0}$ and transition index set $\mathcal{T}^{-}\coloneqq\{0,\ldots,T-2\}$. Vehicle $i\in\mathcal{N}$ has longitudinal position $s_i(t)$, speed $v_i(t)$, acceleration $a_i(t)$, lane index $z_i(t)\in\mathcal{L}$, and blinker (lane-change action) $b_i(t)\in\mathcal{B}\coloneqq\{-1,0,1\}$, where $b_i(t)=-1$ indicates a lane change to the right, $b_i(t)=0$ indicates staying in lane, and $b_i(t)=1$ indicates a lane change to the left.

:::::: {#fig_vehicles .figure latex-placement="H"}
::: minipage
![](Kfer2026GameTheoretic_figs/fig_vars.png){width="\\linewidth"}
:::

::: minipage
![](Kfer2026GameTheoretic_figs/fig_dist.png){width="\\linewidth"}
:::

::: caption
Vehicles operating on a highway with vehicle-specific variables (left) and longitudinal distance (right).
:::
::::::

### Dynamics and bounds:

The motion of vehicle $i\in\mathcal{N}$ is modeled by the discrete-time dynamics: $$\begin{equation}
\label{eq_dynamics}
\begin{aligned}
s_i(t{+}1) &= s_i(t) + \Delta t\, v_i(t),\\
v_i(t{+}1) &= v_i(t) + \Delta t\, a_i(t),
\end{aligned}
\qquad \forall t \in \mathcal{T}^{-}.
\end{equation}$$ We enforce state bounds: $$\begin{equation}
\label{eq_state_bounds}
s_i(t)\in[\,\underline{s},\ \overline{s}\,], \qquad
v_i(t)\in[\,\underline{v}_i,\ \overline{v}_i\,], \qquad \forall t\in\mathcal{T},
\end{equation}$$ where $\underline{s}$ and $\overline{s}$ denote the endpoints of the road segment and $\underline{v}_i,\overline{v}_i$ are the minimum and maximum allowable speeds for vehicle $i$. Acceleration is bounded by actuation limits $$\begin{equation}
\label{eq_actuation_bounds}
a_i(t)\in[\,\underline{a}_i,\ \overline{a}_i\,], \qquad \forall t\in\mathcal{T}^{-},
\end{equation}$$ with $\underline{a}_i,\overline{a}_i$ denoting the minimum and maximum admissible accelerations of vehicle $i$.

### Lane evolution:

Lane changes are restricted to adjacent lanes and are commanded by the blinker: $$\begin{equation}
\label{eq_lane_evolution}
z_i(t{+}1)= z_i(t)+b_i(t),\qquad
b_i(t)\in\mathcal{B},\qquad
z_i(t{+}1)\in\mathcal{L},\qquad \forall t\in\mathcal{T}^{-}.
\end{equation}$$

### Relative coordinates:

For any pair of vehicles $i,j\in\mathcal{N}$, define the longitudinal and lateral offsets: $$\begin{equation}
\label{eq_relative_coords}
d_{i,j}(t)\coloneqq s_j(t)-s_i(t), \qquad
z_{i,j}(t)\coloneqq z_j(t)-z_i(t),
\end{equation}$$ as shown in Fig. [1](#fig_vehicles){reference-type="ref" reference="fig_vehicles"}. The longitudinal offset, in view of [\[eq_dynamics\]](#eq_dynamics){reference-type="eqref" reference="eq_dynamics"}, evolves as: $$\begin{equation}
\label{eq_relative_dynamics}
d_{i,j}(t{+}1)=d_{i,j}(t)+\Delta t\bigl(v_j(t)-v_i(t)\bigr), \qquad \forall t\in\mathcal{T}^{-}.
\end{equation}$$

### Safety rules:

To prevent collisions, we impose longitudinal safety for vehicles in the same lane and lateral safety for vehicles in adjacent lanes.

#### Rule 1 (Longitudinal safety in the same lane).

If $z_{i,j}(t)=0$, then vehicles must maintain a minimum longitudinal separation, ${\it i.e.}$, $$\begin{equation}
\label{eq_rule1}
|d_{i,j}(t)| \ge d_i^{\mathrm{s}}, \qquad \forall t\in\mathcal{T},
\end{equation}$$ where $d_i^{\mathrm{s}}>0$ is the required safety gap for vehicle $i$.

#### Rule 2 (Lateral safety across adjacent lanes).

If vehicles are side-by-side in adjacent lanes, ${\it i.e.}$, $$\begin{equation}
\label{eq_rule2_condition}
|d_{i,j}(t)| \le d_i^{\mathrm{s}}, \qquad |z_{i,j}(t)|=1, \qquad \forall t\in\mathcal{T},
\end{equation}$$ then simultaneous swaps into each other's lanes are forbidden: $$\begin{equation}
\label{eq_rule2}
z_i(t{+}1)\neq z_j(t), \qquad z_j(t{+}1)\neq z_i(t), \qquad \forall t\in\mathcal{T}^{-}.
\end{equation}$$

### Preferences and objectives:

Each vehicle $i\in\mathcal{N}$ is assigned a desired cruising speed $v_i^{\mathrm{des}}\in[\,\underline{v}_i,\ \overline{v}_i\,]$ and a desired lane $\ell_i^{\mathrm{des}}\in\mathcal{L}$. We also fix weights $w_{i,v},w_{i,\ell},w_{i,a},w_{i,b}\in\mathbb{R}_{> 0}$ that trade off speed tracking, lane preference, control effort, and lane-change usage, respectively. These parameters are used to define the edge and terminal costs in the GCS construction in Section [4](#sec_approach){reference-type="ref" reference="sec_approach"}.

## Individual vehicle strategy and optimization problem {#subsec:single_vehicle}

A vehicle $i$'s finite-horizon strategy is the collection of its state and input trajectories, $$\begin{equation}
\label{eq:theta_i_def}
\theta_i \coloneqq \Big( \{ s_i(t), v_i(t), z_i(t) \}_{t\in\mathcal{T}},\ \{ a_i(t), b_i(t) \}_{t \in \mathcal{T}^{-}} \Big),
\end{equation}$$ and we write $\theta \coloneqq( \theta_1, \ldots, \theta_N)$ for the joint strategy profile. Given initial conditions $\{s_i(0), v_i(0), z_i(0) \}_{i \in \mathcal{N}}$, each vehicle $i \in \mathcal{N}$ seeks a feasible strategy that respects the shared safety rules while optimizing its own preferences (${\it e.g.}$, tracking a desired speed $v_i^{\mathrm{des}}$ and lane $\ell_i^{\mathrm{des}}$, as introduced earlier). We formalize through the following assumption.

::: {#assum_separable_cost .assumption}
**Assumption 1** (Separable objectives). *Vehicle objectives are separable across vehicles, ${\it i.e.}$, $J_i(\theta_i) = J_i(\theta_i,\theta_{-i})$, and interaction between vehicles occurs only through the coupled feasibility constraints (Rules 1--2).*
:::

Assumption [1](#assum_separable_cost){reference-type="ref" reference="assum_separable_cost"} captures the modeling choice that vehicles do not directly penalize (or reward) other vehicles in their objectives; rather, strategic coupling arises solely because each vehicle's feasible set depends on the others through shared safety rules. Formally, vehicle $i$ solves: $$\begin{equation}
 \label{eq_single_vehicle}
\begin{aligned}
&\mathop{\mathrm{\mathrm{minimize}}}_{\theta_i}\quad && J_i(\theta_i)\\
&\mathop{\mathrm{\mathrm{subject~to}}}\quad
&& s_i(0),\,v_i(0),\,z_i(0)\ \text{given},\\
&&& \text{\cref{eq_dynamics,eq_state_bounds,eq_actuation_bounds,eq_lane_evolution}},\\
&&& \eqref{eq_rule1},\ \eqref{eq_rule2}, \qquad & \forall j \in\mathcal{N}\setminus\{i\}.
\end{aligned}
\end{equation}$$ The constraints in Equations [\[eq_dynamics,eq_state_bounds,eq_actuation_bounds,eq_lane_evolution\]](#eq_dynamics,eq_state_bounds,eq_actuation_bounds,eq_lane_evolution){reference-type="ref+label" reference="eq_dynamics,eq_state_bounds,eq_actuation_bounds,eq_lane_evolution"} enforce discrete-time longitudinal dynamics [\[eq_dynamics\]](#eq_dynamics){reference-type="eqref" reference="eq_dynamics"}, bounded roadway and speed domains [\[eq_state_bounds\]](#eq_state_bounds){reference-type="eqref" reference="eq_state_bounds"}, actuation limits [\[eq_actuation_bounds\]](#eq_actuation_bounds){reference-type="eqref" reference="eq_actuation_bounds"}, and lane-change feasibility [\[eq_lane_evolution\]](#eq_lane_evolution){reference-type="eqref" reference="eq_lane_evolution"}. Vehicle interactions enter only through the coupled collision-avoidance Rules 1 and 2: [\[eq_rule1\]](#eq_rule1){reference-type="eqref" reference="eq_rule1"} enforces longitudinal separation between vehicles in the same lane, while [\[eq_rule2\]](#eq_rule2){reference-type="eqref" reference="eq_rule2"} prevents simultaneous lane swaps when vehicles are side-by-side in adjacent lanes.

To connect each vehicle's optimization problem in [\[eq_single_vehicle\]](#eq_single_vehicle){reference-type="eqref" reference="eq_single_vehicle"} with the GCS construction in Section [4](#sec_approach){reference-type="ref" reference="sec_approach"}, we impose the following mild modeling assumptions.

::: {#assum_convex_cost .assumption}
**Assumption 2** (Convexity of continuous costs). *For each vehicle $i\in\mathcal{N}$ and for any fixed lane and blinker sequences $(z_i,b_i)$, the objective $J_i(\theta_i)$ is proper, closed, and convex in the continuous variables $\{s_i(t), v_i(t)\}_{t \in \mathcal{T}}$ and $\{a_i(t)\}_{t \in \mathcal{T}^{-}}$, and takes values in $\mathbb{R}_{\ge 0}$.*
:::

Assumption [2](#assum_convex_cost){reference-type="ref" reference="assum_convex_cost"} ensures that once the discrete lane/blinker sequence is fixed, the remaining optimization over continuous variables is a convex program. This property is essential for modeling each maneuver option as a convex set (vertex) and each time-adjacent transition as a convex constraint (edge) in a GCS.

#### Example objective function.

A concrete cost function consistent with the preferences and assumptions introduced earlier, and used later in Section [4](#sec_approach){reference-type="ref" reference="sec_approach"}, is the following cost function: $$\begin{equation}
\label{eq_Ji_example}
\begin{aligned}
J_i(\theta_i)
\coloneqq &\sum_{t \in \mathcal{T}^{-}} \Bigl[
w_{i,v}\bigl(v_i(t{+}1)-v_i^{\mathrm{des}}\bigr)^2
+ w_{i,\ell}\bigl(z_i(t{+}1)-\ell_i^{\mathrm{des}}\bigr)^2 \\
&\hspace{3.2em}
+\, w_{i,a}\,a_i(t)^2
+ w_{i,b}\,b_i(t)^2
\Bigr]
+ w_{i,v}\bigl(v_i(T{-}1)-v_i^{\mathrm{des}}\bigr)^2 ,
\end{aligned}
\end{equation}$$ which penalizes deviations from the desired speed and lane, as well as acceleration and lane changes. For any fixed lane and blinker sequences $(z_i,b_i)$, the cost in [\[eq_Ji_example\]](#eq_Ji_example){reference-type="eqref" reference="eq_Ji_example"} is convex in the continuous variables $(s_i,v_i,a_i)$.

Let $\Theta$ denote the joint feasible set of all strategy profiles $\theta$ satisfying the dynamics, bounds, lane evolution, and safety rules for every vehicle. Under Assumption [1](#assum_separable_cost){reference-type="ref" reference="assum_separable_cost"}, the induced game admits a generalized potential formulation (Definition [\[def_GPG\]](#def_GPG){reference-type="ref" reference="def_GPG"}) with potential: $$\begin{equation}
\label{eq_potential}
\Phi(\theta)\coloneqq \sum_{i\in\mathcal{N}} J_i(\theta_i).
\end{equation}$$

::: problem
[]{#prob_multi_vehicle label="prob_multi_vehicle"} Given initial conditions $\{s_i(0),v_i(0),z_i(0)\}_{i\in\mathcal{N}}$ and vehicle preferences (${\it e.g.}$, $v_i^{\mathrm{des}}$ and $\ell_i^{\mathrm{des}}$), find a feasible joint strategy profile $\theta^\star\in\Theta$ such that no vehicle can unilaterally decrease its cost while respecting the coupled feasibility constraints, ${\it i.e.}$, $\theta^\star$ is a generalized Nash equilibrium of the induced game.
:::

# Iterative Best Response Graphs of Convex Sets {#sec_approach}

We address Problem [\[prob_multi_vehicle\]](#prob_multi_vehicle){reference-type="ref" reference="prob_multi_vehicle"} using IBR. At each iteration, vehicles update their strategies sequentially by solving a single-vehicle motion planning problem while treating the trajectories of all other vehicles as fixed.

For vehicle $i \in \mathcal{N}$, we construct a directed graph of convex sets $\mathcal{G}_{i} = (\mathcal{V}_i, \mathcal{E}_i)$ tailored to the current best-response subproblem. Vertices represent collision-free convex regions at each time step, and directed edges represent dynamically feasible transitions between time-adjacent vertices.

:::::: {#fig_safe_gaps_graph .figure latex-placement="H"}
::: minipage
![](Kfer2026GameTheoretic_figs/safe_gaps.png){width="\\linewidth"}
:::

::: minipage
![](Kfer2026GameTheoretic_figs/graph.png){width="\\linewidth"}
:::

::: caption
Time expanded graph.
:::
::::::

## Vertex Construction {#sec_vertex}

Fix an IBR iteration and treat the other vehicles' trajectories as known. For each lane $\ell \in \mathcal{L}$ and time step $t \in \mathcal{T}$, define the unsafe longitudinal interval around each vehicle $j \neq i$ that is in lane $\ell$ at time step $t \in \mathcal{T}$: $$\begin{align}
\mathcal{K}_{i}^{j}(\ell,t) \coloneqq \bigl(\, s_j(t) - d_i^{\mathrm{s}},\ s_j(t) + d_i^{\mathrm{s}} \,\bigr).
\end{align}$$ Let the union of unsafe intervals in lane $\ell$ at time step $t \in \mathcal{T}$ be $$\begin{align}
\mathcal{F}_{i}(\ell,t) \coloneqq \bigcup_{\substack{j\in\mathcal{N}\setminus\{i\}\\ z_j(t)=\ell}} \mathcal{K}_{i}^{j}(\ell,t).
\end{align}$$ Over a bounded road segment $[\,\underline{s},\ \overline{s}\,]$, the collision-free set is $$\begin{align}
\mathcal{S}_{i}(\ell,t) \coloneqq [\,\underline{s},\ \overline{s}\,] \setminus \mathcal{F}_{i}(\ell,t).
\end{align}$$ Since $\mathcal{F}_{i}(\ell,t)$ is a finite union of open intervals, $\mathcal{S}_{i}(\ell, t)$ can be expressed as a finite union of disjoint closed intervals (safe gaps) $$\begin{align}
\mathcal{S}_{i}(\ell,t) = \bigcup_{g \in \mathcal{H}_{i}(t, \ell)} \mathcal{I}_{i}(t,\ell,g),
\end{align}$$ where $\mathcal{H}_{i}(t,\ell)$ is the finite index set of connected components of $\mathcal{S}_{i}(\ell, t)$ and $\{ \mathcal{I}_{i}(t,\ell,g) \}_{g \in \mathcal{H}_{i} (t, \ell) }$ denotes the corresponding family of pairwise-disjoint closed intervals. Equivalently, each $g \in \mathcal{H}_{i} (t, \ell)$ labels one collision-free longitudinal "gap" in lane $\ell \in \mathcal{L}$ at time step $t \in \mathcal{T}$ between consecutive unsafe regions induced by other vehicles.

Each safe interval $\mathcal{I}_{i}(t,\ell,g)$, as illustrated in Fig. [\[fig_safe_gaps\]](#fig_safe_gaps){reference-type="ref" reference="fig_safe_gaps"}, induces a vertex $V_i(t,\ell,g)\in\mathcal{V}_i$ whose continuous state variable is $$\begin{align}
x_{V_i(t,\ell,g)} \coloneqq
\begin{bmatrix}
s_{V_i(t,\ell,g)}\\
v_{V_i(t,\ell,g)}
\end{bmatrix} \in\mathbb{R}^2,
\end{align}$$ and whose convex constraints are $$\begin{equation}
\label{eq_vertex_constraints}
s_{V_i(t,\ell,g)} \in \mathcal{I}_{i}(t,\ell,g),
\qquad
v_{V_i(t,\ell,g)} \in [\,\underline{v}_i,\ \overline{v}_i\,].
\end{equation}$$ The discrete lane choice is encoded by the vertex lane index $\ell \in \mathcal{L}$.

#### Initial condition.

To impose initial state conditions of vehicle $i$, choose any $g_0 \in \mathcal{H}_{i}\big(0,z_i(0)\big)$ such that $s_i(0)\in \mathcal{I}_{i}(0,z_i(0),g_0)$ (ties may be broken arbitrarily), and enforce $$\begin{equation}
\label{eq_initial_condition_vertex}
x_{V_i(0,z_i(0),g_0)}=
\begin{bmatrix}
s_i(0)\\
v_i(0)
\end{bmatrix}.
\end{equation}$$ This fixes a valid source vertex consistent with the initial state.

## Edge Construction {#sec_edge}

Directed edges connect time-adjacent vertices: $$\begin{align}
e = \bigl(V_i(t,\ell,g),\ V_i(t+1,\ell',g')\bigr),
\qquad t\in\mathcal{T}^{-},
\end{align}$$ as shown in Fig. [2](#fig_safe_gaps_graph){reference-type="ref" reference="fig_safe_gaps_graph"}. Only edges between adjacent lanes are permitted, ${\it i.e.}$, $|\ell'-\ell|\le 1$. Each edge enforces dynamic feasibility of the form [\[eq_dynamics\]](#eq_dynamics){reference-type="eqref" reference="eq_dynamics"} with a decision variable $a_i(t) \in [\,\underline{a}_i,\ \overline{a}_i\,]$ satisfying [\[eq_actuation_bounds\]](#eq_actuation_bounds){reference-type="eqref" reference="eq_actuation_bounds"} and consistent state variables at times $t$ and $t+1$. The lane-change action on the edge is $b_i(t)=\ell'-\ell\in\{-1,0,1\}$, consistent with [\[eq_lane_evolution\]](#eq_lane_evolution){reference-type="eqref" reference="eq_lane_evolution"}. Lateral safety (Rule 2) is enforced by excluding lane-change edges that would violate [\[eq_rule2\]](#eq_rule2){reference-type="eqref" reference="eq_rule2"} given the fixed trajectories and lane-change actions of other vehicles. Each edge $e=\bigl(V_i(t,\ell,g),\,V_i(t+1,\ell',g')\bigr)$ is assigned a convex quadratic edge cost $c_e(\cdot)$ that depends on the decision variables on that edge, namely the successor velocity $v_{V_i(t+1,\ell',g')}$ and the control $a_i(t)$ (with $b_i(t)=\ell'-\ell$): $$\begin{multline}
\label{eq_edge_cost}
c_e \bigl(x_{V_i(t,\ell,g)},x_{V_i(t+1,\ell',g')},a_i(t)\bigr) =
w_{i,v}\!\left(v_{V_i(t+1,\ell',g')}-v_i^{\mathrm{des}}\right)^{2}
+ w_{i,\ell}\!\left(\ell'-\ell_i^{\mathrm{des}}\right)^{2} \\
+
w_{i,a}\,a_i(t)^{2}
+ w_{i,b}\,b_i(t)^{2},
\end{multline}$$ where $w_{i,v}, w_{i,\ell}, w_{i,a}, w_{i,b}\in\mathbb{R}_{>0}$ are weights. A terminal penalty may be included as a vertex cost at $t=T-1$, ${\it e.g.}$, $$\begin{equation}
c_V \left( x_{V_i(T-1,\ell,g)} \right) = w_{i,v} \left( v_{V_i(T-1,\ell,g)}-v_i^{\mathrm{des}} \right)^2.
\end{equation}$$

Equipped with this construction, vehicle $i \in \mathcal{N}$'s single-vehicle planning problem [\[eq_single_vehicle\]](#eq_single_vehicle){reference-type="eqref" reference="eq_single_vehicle"} can be cast as a GCS shortest path problem on $\mathcal{G}_i$.

::: proposition
[]{#prop_single_vehicle_tight label="prop_single_vehicle_tight"} Fix the trajectories of all vehicles $j\neq i$ and construct $\mathcal{G}_i$ accordingly. If the convex relaxation of the induced GCS shortest path problem is tight, ${\it i.e.}$, it admits an optimal solution with $z_e \in \{0,1\}$, then solving the relaxed problem yields a globally optimal solution of vehicle $i$'s mixed-integer best-response subproblem on $\mathcal{G}_i$. Consequently, under tightness, the resulting update is an *exact* best response, so each IBR step is a potential-descent step in the sense of Proposition [\[prop_potential_descent\]](#prop_potential_descent){reference-type="ref" reference="prop_potential_descent"}.
:::

::: remark
If the relaxation is not tight, the computed update can be interpreted as an approximate best response. Section [4.4](#sec_error){reference-type="ref" reference="sec_error"} quantifies the effect of such inexactness.
:::

## Iterative Best-Response on Graphs of Convex Sets Algorithm {#sec_IBR}

We solve the multi-vehicle game in Problem [\[prob_multi_vehicle\]](#prob_multi_vehicle){reference-type="ref" reference="prob_multi_vehicle"} using an IBR scheme, summarized in Algorithm [\[alg_ibr\]](#alg_ibr){reference-type="ref" reference="alg_ibr"}.

::: algorithm
Set $k\gets 0$ and compute $\Phi(\theta^{0})$
:::

The algorithm proceeds in *sweeps* indexed by $k$: during sweep $k$, vehicles update sequentially, and each vehicle $i$ computes a best response to the most recent strategies of the other vehicles, denoted $\theta_{-i}^{k,i-1}$. Concretely, at its update, vehicle $i$ constructs a GCS instance $\mathcal{G}_i^k$ that encodes collision-free regions and feasible transitions given $\theta_{-i}^{k,i-1}$, solves the resulting single-vehicle GCS SPP, and records the resulting strategy $\theta_i^{k+1}$ (lines [\[alg_construct\]](#alg_construct){reference-type="ref" reference="alg_construct"}--[\[alg_update\]](#alg_update){reference-type="ref" reference="alg_update"} of Algorithm [\[alg_ibr\]](#alg_ibr){reference-type="ref" reference="alg_ibr"}). After all vehicles have updated, the sweep terminates, and the algorithm produces the next joint strategy profile $\theta^{k+1}$ (line [\[alg_end_of_sweep\]](#alg_end_of_sweep){reference-type="ref" reference="alg_end_of_sweep"}).

Under exact best-response updates in a generalized potential game (see Section [2.2](#sec_potential_games){reference-type="ref" reference="sec_potential_games"}), Proposition [\[prop_potential_descent\]](#prop_potential_descent){reference-type="ref" reference="prop_potential_descent"} implies that the generalized potential is monotonically nonincreasing along the intermediate profiles $\theta^{k,i}$, and hence along the sweep iterates $\theta^{k}$. In our implementation, each best response is computed by solving a convex relaxation of the underlying GCS mixed-integer problem. Consequently, the update may be inexact and should be interpreted as an approximate best response. The resulting equilibrium error and its relationship to the per-update suboptimality are quantified in Section [4.4](#sec_error){reference-type="ref" reference="sec_error"}. We terminate IBR when the decrease in the potential across a sweep is below a specified tolerance (lines [\[alg_end_of_sweep\]](#alg_end_of_sweep){reference-type="ref" reference="alg_end_of_sweep"}--[\[alg_term\]](#alg_term){reference-type="ref" reference="alg_term"}).

## Error Quantification {#sec_error}

This section quantifies the extent to which inexact best-response updates degrade the limiting quality of the strategy profiles produced by the IBR procedure. Since each vehicle solves a relaxed GCS problem in practice, the resulting update may not be an exact best response to the other vehicles' fixed strategies. We therefore measure the suboptimality of each update relative to the true best-response problem and translate this into an approximate equilibrium guarantee.

We recall the definitions of the joint feasible set $\Theta$, the individual feasible sets $\Theta_i(\theta_{-i})$, and the intermediate profiles $\theta^{k,i}$ introduced in Equations [\[generalized_strategy_set\]](#generalized_strategy_set){reference-type="eqref" reference="generalized_strategy_set"} and [\[eq_theta_intermediate\]](#eq_theta_intermediate){reference-type="eqref" reference="eq_theta_intermediate"}. We note that for the remainder of this section, we revert to the cost function notation used prior to Assumption [1](#assum_separable_cost){reference-type="ref" reference="assum_separable_cost"}, ${\it i.e.}$, $J_i(\theta_i,\theta_{-i}) = J_i(\theta_i)$.

#### Approximate best responses.

At each update, vehicle $i \in \mathcal{N}$ aims to minimize its cost over the feasible set induced by the current strategies of the other vehicles. We measure the quality of the computed update by comparing its cost to the optimal value of this best-response problem.

::: definition
[]{#def_ABR label="def_ABR"} At sweep $k$ and vehicle $i \in \mathcal{N}$, we say the computed update $\theta_i^{k+1}$ has best-response error at most $\epsilon_i^k\ge 0$ if $$\begin{equation}
\label{ineq_ABR}
J_i(\theta_i^{k+1}, \theta_{-i}^{k,i-1}) \le \inf_{\theta_i \in \Theta_i(\theta_{-i}^{k,i-1})} J_i(\theta_i, \theta_{-i}^{k,i-1}) +\epsilon_i^k.
\end{equation}$$
:::

#### Approximate equilibrium.

A natural benchmark for IBR is a generalized Nash equilibrium (Definition [\[def_GNE\]](#def_GNE){reference-type="ref" reference="def_GNE"}), in which no vehicle can reduce its cost through a feasible unilateral deviation. Since we allow inexact best responses, we use the standard relaxation of this notion, ${\it cf.}$ [@shoham2008multiagent Definition 3.4.7].

::: definition
[]{#def_epsGNE label="def_epsGNE"} A strategy profile $\theta\in\Theta$ is an $\epsilon$-GNE if $$\begin{align}
J_i(\theta_i,\theta_{-i}) \le \inf_{\hat{\theta}_i\in\Theta_i(\theta_{-i})} J_i(\hat{\theta}_i,\theta_{-i}) + \epsilon, \qquad \forall i \in \mathcal{N}.
\end{align}$$
:::

To connect update-level errors to equilibrium quality, we introduce each vehicle's *regret*, ${\it i.e.}$, the gap between its current cost and its best feasible unilateral deviation.

$$\begin{align}
r_i(\theta) \coloneqq J_i(\theta_i, \theta_{-i}) - \inf_{\hat{\theta}_i \in \Theta_i(\theta_{-i})} J_i(\hat{\theta}_i, \theta_{-i}) \ge 0.
\end{align}$$

Our analysis is based on two standard technical assumptions. The first prevents the potential from decreasing without bound, while the second postulates that the inexactness of each best-response computation is uniformly bounded.

::: {#assum_bounded .assumption}
**Assumption 3**. *The potential function $\Phi$ is bounded below on $\Theta$, and $\Theta$ is nonempty and compact.*
:::

::: {#assum_bderror .assumption}
**Assumption 4**. *The IBR iterates satisfy [\[ineq_ABR\]](#ineq_ABR){reference-type="eqref" reference="ineq_ABR"} with errors uniformly bounded by $\epsilon_i^k \le \bar{\epsilon} < \infty$ for all $i \in \mathcal{N}$ and all $k\ge 0$.*
:::

Assumption [3](#assum_bounded){reference-type="ref" reference="assum_bounded"} is standard in our setting, as physical constraints and finite discrete decisions ensure the feasible strategy space is a nonempty compact set over which the nonnegative potential function is bounded below. However, Assumption [4](#assum_bderror){reference-type="ref" reference="assum_bderror"} is stronger and generally difficult to verify, requiring a uniform bound of the suboptimality of the GCS convex relaxation that is often observed in motion-planning problems (see Remark [\[rem_tightness_empirical\]](#rem_tightness_empirical){reference-type="ref" reference="rem_tightness_empirical"}), but is difficult to guarantee theoretically (${\it cf.}$, [@GCS_thesis Proposition 8.1]).

The following result states that if each IBR update is an $\epsilon$-approximate best response with a uniform error bound, then the iterates asymptotically lie in an approximate equilibrium set: no vehicle can improve by more than $\bar\epsilon$ in the limit.

::: theorem
[]{#thm_approximateGNE label="thm_approximateGNE"} Suppose $G$ is a generalized potential game with potential $\Phi$ (Definition [\[def_GPG\]](#def_GPG){reference-type="ref" reference="def_GPG"}). Under Assumptions [3](#assum_bounded){reference-type="ref" reference="assum_bounded"}--[4](#assum_bderror){reference-type="ref" reference="assum_bderror"}, $$\begin{align*}
\limsup_{k\to\infty}\ \max_{i \in \mathcal{N}} r_i(\theta^k)\ \le\ \bar{\epsilon}.
\end{align*}$$ In particular, the iterates asymptotically lie in the $\bar\epsilon$-GNE set (Definition [\[def_epsGNE\]](#def_epsGNE){reference-type="ref" reference="def_epsGNE"}).
:::

::: proof
*Proof.* Fix a sweep index $k$ and consider the update of vehicle $i\in\mathcal{N}$ from the intermediate profile $\theta^{k,i-1}$ to $\theta^{k,i}$. Since $\Phi$ is a generalized potential (Definition [\[def_GPG\]](#def_GPG){reference-type="ref" reference="def_GPG"}), changes in vehicle $i$'s cost match changes in $\Phi$ under feasible unilateral deviations. Combining this property with the approximate best-response condition [\[ineq_ABR\]](#ineq_ABR){reference-type="eqref" reference="ineq_ABR"} yields $$\begin{align}
\Phi(\theta^{k,i-1})-\Phi(\theta^{k,i})
&= J_i(\theta_i^{k,i-1},\theta_{-i}^{k,i-1}) - J_i(\theta_i^{k,i},\theta_{-i}^{k,i-1}) \nonumber\\
&\ge r_i(\theta^{k,i-1}) - \epsilon_i^k
\ \ge\ r_i(\theta^{k,i-1}) - \bar{\epsilon}.
\label{ineq_improv}
\end{align}$$

We proceed by contradiction. Suppose there exists $\eta>0$ and an infinite subsequence of sweeps $\{k_m\}_{m \in \mathbb{N}}$ such that, for each $m \in \mathbb{N}$, there exists an index $i_m \in \mathcal{N}$ with $$\begin{equation}
\label{ineq_contradiction}
r_{i_m}(\theta^{k_m,i_m-1}) \ge \bar{\epsilon} + \eta.
\end{equation}$$ Applying [\[ineq_improv\]](#ineq_improv){reference-type="eqref" reference="ineq_improv"} at the update of vehicle $i_m$ during sweep $k_m$ gives $$\begin{align}
\Phi(\theta^{k_m,i_m-1})-\Phi(\theta^{k_m,i_m}) \ge r_{i_m}(\theta^{k_m,i_m-1})-\bar{\epsilon} \ge \eta.
\end{align}$$ In particular, since $\theta^{k_m,i_m}$ occurs within sweep $k_m$, we have $\Phi(\theta^{k_m+1})\le \Phi(\theta^{k_m})-\eta$. Iterating along the subsequence implies $\Phi(\theta^{k_m}) \to -\infty$ as $m\to\infty$, contradicting the boundedness of $\Phi$ below on $\Theta$ (Assumption [3](#assum_bounded){reference-type="ref" reference="assum_bounded"}). Therefore, $$\begin{align}
\limsup_{k\to\infty}\max_{i\in\mathcal{N}} r_i(\theta^k)\le \bar{\epsilon},
\end{align}$$ which proves the claim. $\square$ ◻
:::

::: remark
As noted earlier, GCS relaxations are often tight in practice (${\it i.e.}$, $\epsilon_i^k=0$), but they can be arbitrarily loose in special cases [@GCS_thesis Proposition 8.1], in which case Assumption [4](#assum_bderror){reference-type="ref" reference="assum_bderror"} may fail. For instance, this may happen when the costs and edge weights are symmetric [@GCS_thesis; @GCS]. In such cases, the result above should be interpreted as a conditional guarantee: whenever the per-update best-response error remains uniformly bounded, the IBR iterates converge to a correspondingly bounded approximate equilibrium set.
:::

# Simulation Results {#sec_simulation_results}

The performance of the proposed method is illustrated in a representative driving scenario. The parameters for the driving problem are $N = 6$, $|\mathcal{L}| = 4$, $T = 30$, and discretization step of $\Delta t = \SI{0.3}{\second}$. The scenario is set up with two vehicles merging from a terminating lane into a three-lane highway, where four other vehicles operate. The algorithm converges in 2 iterations, with the resulting equilibrium visualized in Fig. [3](#fig_scenario_snapshots){reference-type="ref" reference="fig_scenario_snapshots"}. All simulations were performed using the `GCSOPT` library [@gcsopt] on a laptop with a AMD Ryzen 7 5800U (8-core, 16-thread) CPU and solved using the MOSEK 11.0.29 solver [@mosek], leading to a total wall-clock time of $\SI{297.24}{\second}$ for this scenario. The resulting strategies $\theta^{\star}$ drive each vehicle $i \in \mathcal{N}$ safely over the chosen time horizon $\mathcal{T}$ to a target lane $\ell_i^\text{des}$, while tracking a desired velocity $v_i^\text{des}$. In doing so, the vehicles perform multi-layered overtaking maneuvers while accelerating and ensuring both lateral and longitudinal safety.

:::: {#fig_scenario_snapshots .figure latex-placement="H"}
![](Kfer2026GameTheoretic_figs/overlaid_trajectories.png){width="\\textwidth"}

::: caption
Trajectories of six vehicles on a highway with one merging lane. The initial and final positions of each vehicle are shown without transparency, while positions at every third time step are shown with transparency.
:::
::::

Additionally, multiple randomized simulations with $N=4$, $|\mathcal{L}| = 3$, $T=30$, and $\Delta t = \SI{0.3}{\second}$ were conducted, with parameters sampled from the following uniform distributions: $$\begin{align*}
&v_i^\text{des} \sim \mathcal{U}\ (\tfrac{80}{3.6}, \tfrac{160}{3.6}),  
&&\ell_i^\text{des} \sim \mathcal{U}(\{1,\dots,|\mathcal{L}|\}),
& w_{i,v} \sim \mathcal{U}(0.1,1.0), \\
&w_{i,\ell} \sim \mathcal{U}(5,25), 
&&w_{i,b} \sim \mathcal{U}(5,10),
&w_{i,a} \sim \mathcal{U}(0.1,0.5).
\end{align*}$$ Initial states and lane configurations were randomly sampled according to: $$\begin{align*}
&s_i^{0} \sim \mathcal{U}\ ({0.0}, {200}),
&&v_i^{0} \sim \mathcal{U}\ (\tfrac{60}{3.6}, \tfrac{130}{3.6}),
&\ell_i^{0} \sim \mathcal{U}(\{1,2,3\}),
\end{align*}$$ until a collision-free arrangement was obtained. Figure [4](#fig_Pot_fctn){reference-type="ref" reference="fig_Pot_fctn"} illustrates the evolution of the potential function $\Phi(\theta^k)$ over the iterations $k$. As predicted, the potential function values are decreasing, with a strictly positive decrease. Consequently, each iteration of the algorithm moves the system closer to a $\epsilon$-GNE, providing empirical validation of the proposed approach, IBR-GCS.

:::: {#fig_Pot_fctn .figure latex-placement="H"}
![](Kfer2026GameTheoretic_figs/convergence_violin.png){width="\\textwidth"}

::: caption
Distributions of potential function evolution over iterations for 100 randomized simulation setups with the mean in orange. As shown, the potential function is always smaller at iteration $k$ than at $k-1$.
:::
::::

::: remark
[]{#rem_tightness_empirical label="rem_tightness_empirical"} In all our simulations, the convex relaxation was observed to be very tight, enabling us to solve complex driving scenarios to globally optimal solutions. While our work provides no theoretical tightness guarantee, these empirical observations suggest that additional structure may be present and motivate future work aimed at establishing formal tightness guarantees.
:::

# Conclusion {#sec_conclusion}

This paper presented IBR-GCS, a graphs of convex sets (GCS) formulation for multi-vehicle highway autonomous driving with strategic interaction. For each vehicle, collision-free maneuver options and dynamically feasible transitions are encoded as a shortest-path problem (SPP) on a vehicle-specific GCS. This representation separates continuous trajectory optimization (handled within convex vertex/edge constraints and costs) from discrete maneuver selection (encoded in the graph topology) and admits a convex relaxation that is often tight. Since each vehicle's feasible maneuver graph depends on the current strategies of the other vehicles, a single centralized GCS is not naturally available; instead, IBR-GCS employs an iterative best-response (IBR) procedure in which vehicles repeatedly solve their individual GCS subproblems while holding the strategies of the other vehicles fixed.

From a game-theoretic perspective, the coupled feasibility constraints induce a generalized Nash game with a generalized potential structure that can be exploited to interpret IBR as an (approximate) descent method on a global potential function. Under exact best responses, the potential is monotonically non-increasing (Proposition [\[prop_potential_descent\]](#prop_potential_descent){reference-type="ref" reference="prop_potential_descent"}). When best responses are computed inexactly (${\it e.g.}$, due to relaxation looseness), our error analysis provides conditions under which the iterates converge to a neighborhood of the generalized Nash equilibrium set, with a bound on the maximum unilateral improvement available to any vehicle (Theorem [\[thm_approximateGNE\]](#thm_approximateGNE){reference-type="ref" reference="thm_approximateGNE"}).

Several practical considerations affect performance and the particular equilibrium reached. For example, the limiting equilibrium point can depend on initialization and on the vehicle update order. In the current implementation, each vehicle reconstructs its GCS at every update, even though successive graphs often change only locally as other vehicles move. An important direction for future work is to warm-start and reuse graph structure across sweeps (${\it e.g.}$, caching safe-gap decompositions and updating only affected vertices/edges), which could substantially reduce per-iteration overhead. Another direction is to incorporate randomized or priority-based update schedules to mitigate order sensitivity, and to refine termination criteria based on per-vehicle regret (Section [4.4](#sec_error){reference-type="ref" reference="sec_error"}) rather than only on potential decrease.

Finally, while convex relaxations are frequently tight in practice, relaxation looseness can degrade best-response accuracy. Developing tighter relaxations and problem-specific certificates of tightness for driving instances remains an important avenue for future work.

# Acknowledgement {#acknowledgement .unnumbered}

This work was supported in part by the National Science Foundation under Grants 2211548 and 2336840.

# Notation {#sec_notation}

Table [1](#tab_notation){reference-type="ref" reference="tab_notation"} summarizes the notation used throughout the paper.

::: {#tab_notation}
  **Symbol**                                                     **Description**
  -------------------------------------------------------------- -------------------------------------------------------------------------------------------
  **Symbol**                                                     **Description**
                                                                 
                                                                 
  $\mathcal{X}$                                                  Calligraphic font, ${\it e.g.}$, $\mathcal{N}$, $\mathcal{L}$ (set-valued objects).
  $\mathbb{R}$                                                   Real numbers.
  $\underline{(\cdot)}$, $\overline{(\cdot)}$                    Lower/upper bounds (${\it e.g.}$, $\underline{a}_i$, $\overline{a}_i$).
  $\mathrm{des}$                                                 "Desired" superscript, ${\it e.g.}$, $v_i^{\mathrm{des}}$, $\ell_i^{\mathrm{des}}$.
  $\mathrm{s}$                                                   "Safety" superscript, ${\it e.g.}$, $d_i^{\mathrm{s}}$.
  $\delta_{i,j}$                                                 Kronecker delta (1 if $i=j$, 0 otherwise).
                                                                 
  $\mathcal{G}=(\mathcal{V},\mathcal{E})$                        Graph of convex sets with vertices $\mathcal{V}$ and directed edges $\mathcal{E}$.
  $V\in\mathcal{V}$                                              A vertex of the GCS graph.
  $e=(U,W)\in\mathcal{E}$                                        A directed edge from vertex $U$ to vertex $W$.
  $\mathcal{E}_V^{\mathrm{in}},\ \mathcal{E}_V^{\mathrm{out}}$   Incoming/outgoing edge sets at vertex $V$.
  $\mathcal{X}_V\subset\mathbb{R}^n$                             Convex set associated with vertex $V$.
  $\mathcal{X}_e\subset\mathbb{R}^n\times\mathbb{R}^n$           Convex set encoding feasibility/coupling across edge $e=(U,W)$.
  $x_V\in\mathcal{X}_V$                                          Continuous decision variable at vertex $V$.
  $z_e\in\{0,1\}$                                                Binary edge-selection variable for edge $e$.
  $y_V$                                                          Induced vertex-selection variable (vertex is on the selected path).
  $c_e(\cdot)$                                                   Convex nonnegative edge cost.
  $c_V(\cdot)$                                                   Optional convex nonnegative vertex cost.
  $V_0,\ V_K$                                                    Source and target vertices for the shortest path problem.
                                                                 
  $N$                                                            Number of agents.
  $\mathcal{N}=\{1,\dots,N\}$                                    Set of agent indices.
  $\theta_i$                                                     Strategy of agent $i$.
  $\theta_{-i}$                                                  Joint strategy of all agents except $i$.
  $\theta=(\theta_i,\theta_{-i})$                                Joint strategy profile.
  $\Theta$                                                       Joint feasible set (captures coupled/shared constraints).
  $\Theta_i(\theta_{-i})$                                        Feasible strategy set of agent $i$ given $\theta_{-i}$.
  $J_i(\theta_i,\theta_{-i})$                                    Cost incurred by agent $i$ at joint strategy $(\theta_i,\theta_{-i})$.
  $G$                                                            The generalized game defined by the coupled optimization problems.
  $\theta^\star$                                                 A generalized Nash equilibrium (GNE) strategy profile.
  $\Phi:\Theta\to\mathbb{R}$                                     Generalized potential function.
  $\mathrm{BR}_i(\theta_{-i})$                                   Best-response mapping of agent $i$.
                                                                 
  $k$                                                            IBR iteration (sweep) index.
  $\theta^k$                                                     Joint strategy at the start of sweep $k$.
  $\theta^{k,i}$                                                 Intermediate joint strategy after agents $1,\dots,i$ updated in sweep $k$.
  $\epsilon_i^k$                                                 Best-response suboptimality for agent $i$ at sweep $k$.
  $\bar{\epsilon}$                                               Uniform bound on best-response errors.
  $r_i(\theta)$                                                  Regret of agent $i$ at profile $\theta$
  $\epsilon$                                                     Tolerance used in termination criteria.
                                                                 
  $\mathcal{L}$                                                  Set of lane indices.
  $\mathcal{T}=\{0,\dots,T-1\}$                                  Discrete planning horizon (time indices).
  $\Delta t$                                                     Time step duration.
  $s_i(t)$                                                       Longitudinal position of vehicle $i \in \mathcal{N}$ at time $t$.
  $v_i(t)$                                                       Longitudinal speed of vehicle $i \in \mathcal{N}$ at time $t$.
  $a_i(t)$                                                       Longitudinal acceleration of vehicle $i \in \mathcal{N}$ at time $t$.
  $z_i(t)\in\mathcal{L}$                                         Lane index of vehicle $i \in \mathcal{N}$ at time $t$.
  $\mathcal{B}=\{-1,0,1\}$                                       Blinker command set (right, stay, left).
  $b_i(t)\in\mathcal{B}$                                         Blinker (lane-change command) of vehicle $i \in \mathcal{N}$ at time $t$.
  $\underline{a}_i,\ \overline{a}_i$                             Acceleration bounds for vehicle $i \in \mathcal{N}$.
  $\underline{v}_i,\ \overline{v}_i$                             Speed bounds for vehicle $i \in \mathcal{N}$.
  $\underline{s},\ \overline{s}$                                 Road segment bounds in longitudinal coordinate.
  $d_{i,j}(t)=s_j(t)-s_i(t)$                                     Longitudinal separation between vehicles $i$ and $j$.
  $z_{i,j}(t)=z_j(t)-z_i(t)$                                     Relative lane offset between vehicles $i$ and $j$.
  $d_i^{\mathrm{s}}$                                             Safety distance (longitudinal gap) for vehicle $i \in \mathcal{N}$.
                                                                 
  $\mathcal{G}_i=(\mathcal{V}_i,\mathcal{E}_i)$                  Vehicle-$i$ GCS graph used in its best-response subproblem.
  $\ell\in\mathcal{L}$                                           Lane index in the construction.
  $g$                                                            Safe-gap index within a lane at a given time.
  $\mathcal{K}_i^{j}(\ell,t)$                                    Unsafe longitudinal interval around vehicle $j$ in lane $\ell$ at time $t$.
  $\mathcal{F}_i(\ell,t)$                                        Union of unsafe intervals in lane $\ell$ at time $t$.
  $\mathcal{S}_i(\ell,t)$                                        Collision-free longitudinal set in lane $\ell$ at time $t$.
  $\mathcal{H}_i(\ell,t)$                                        Finite index set of collision-free gaps in lane $\ell$ at time $t$.
  $\mathcal{I}_i^{\ell,g}(t)$                                    The $g$-th collision-free longitudinal interval in lane $\ell$ at time $t$.
  $V_i(t,\ell,g)$                                                Vertex corresponding to $(t,\ell,g)$ in $\mathcal{G}_i$.
  $x_i(t)=\begin{bmatrix}s_i(t)\\ v_i(t)\end{bmatrix}$           Continuous state used in vertices of $\mathcal{G}_i$.
  $e=\bigl(V_i(t,\ell,g),V_i(t+1,\ell',g')\bigr)$                Directed edge representing a feasible transition between time-adjacent vertices.
                                                                 
  $v_i^{\mathrm{des}}$                                           Desired speed of vehicle $i \in \mathcal{N}$.
  $\ell_i^{\mathrm{des}}$                                        Desired lane of vehicle $i \in \mathcal{N}$.
  $w_{i,v}, w_{i,\ell}, w_{i,a}, w_{i,b}$                        Cost weights for speed tracking, lane preference, acceleration effort, and blinker usage.

  : Summary of notation.
:::
