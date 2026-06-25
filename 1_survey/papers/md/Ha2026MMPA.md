---
citation_key: Ha2026MMPA
arxiv_id: 2601.01910
arxiv_url: "https://arxiv.org/abs/2601.01910"
title: "MMP-A*: Multimodal Perception Enhanced Incremental Heuristic Search on Path Planning"
authors_short: "Minh Hieu Ha et al."
year: 2026
direction_tag: G_subgoal_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:30:37Z
origin: ai+web
reviewed: false
---

# MMP-A\*: Multimodal Perception Enhanced Incremental Heuristic Search on Path Planning

Minh Hieu Ha<sup>1,2,∗</sup> , Khanh Ly Ta<sup>2,∗</sup> , Hung Phan<sup>1</sup> , Tung Doan<sup>1</sup> , Tung Dao<sup>1</sup> , Dao Tran<sup>3</sup> , Huynh Thi Thanh Binh<sup>1</sup>

<sup>1</sup>Hanoi University of Science and Technology, Vietnam <sup>2</sup>Vingroup Big Data Research Center <sup>3</sup>FPT Software AI Center, Vietnam

## Abstract

Autonomous path planning demands a synergy of global reasoning and geometric precision, particularly in complex or cluttered environments. While classical $\mathbf { A } ^ { * }$ is favored for its optimality, it suffers from prohibitive computational and memory costs in large-scale scenarios. Recent efforts to mitigate these limitations by leveraging Large Language Models for waypoint guidance remain insufficient; operating solely on text-based reasoning without spatial grounding. These models frequently generate erroneous waypoints in topologically complex environments featuring dead-ends and lack the perceptual capacity to interpret ambiguous physical boundaries. Such inconsistencies necessitate costly corrective expansions, ultimately undermining the intended computational efficiency. We introduce MMP-A\*, a multimodal framework that synergizes the spatial grounding capabilities of Vision–Language Models with a novel adaptive decay mechanism. By anchoring high-level reasoning in physical geometry, our approach generates coherent waypoint guidance that effectively overcomes the blindness of text-only planners. The integrated decay mechanism dynamically regulates the influence of uncertain waypoints within the heuristic, ensuring geometric validity while substantially reducing memory overhead. To assess robustness, we evaluate the framework within challenging scenarios featuring severe clutter and topological complexity. Empirical results demonstrate that MMP- $\mathbf { \nabla \cdot A ^ { * } }$ yields near-optimal trajectories with significantly reduced operational costs, confirming its potential as a robust, perception-grounded paradigm for autonomous navigation.

Code is available at: https://github.com/ langkhachhoha/MMP-ASTAR

## 1 Introduction

Path planning is a core problem in robotics and autonomous navigation, requiring the computation of an optimal or nearoptimal route from start to goal while avoiding obstacles, and serving as a foundational capability for mobile robots, autonomous vehicles, industrial automation, and virtual environments where navigation efficiency directly impacts safety and scalability [Hart et al., 1968b; Abd Algfoor et al., 2015; Gonzalez´ et al., 2015]. Classical search-based methods, particularly A\* and its derivatives, are widely utilized for their theoretical guarantees of completeness and optimality under admissible heuristics [Koenig et al., 2004; Karaman and Frazzoli, 2011]. However, increasing scale and clutter trigger exponential computational costs in these algorithms. While specialized $\mathbf { A } ^ { * }$ variants offer optimizations, they often rely on specific environmental priors, rendering them brittle and unable to generalize to the arbitrary, unstructured geometries of real-world settings.

Large Language Models (LLMs) have increasingly been applied across a wide range of domains, including robotics, where they support tasks such as high-level task planning and action selection [Tariq et al., 2025; Doma et al., 2024; Joublin et al., 2024]. In particular, LLM-A\* [Meng et al., 2024] frameworks employ LLMs to generate intermediate waypoints that guide the search process toward semantically meaningful regions, significantly reducing expansion cost compared to vanilla ${ \mathrm { A } } ^ { * } .$ While this integration introduces promising global reasoning, the text-only modality of LLMs cannot encode fine-grained geometric or topological structures [Caglar et al., 2024; Wei et al., 2025; Cao et al., 2025]. Consequently, in complex environments with dense or irregular barriers, LLM-generated waypoints often become redundant, misplaced, or geometrically infeasible, leading to unstable heuristic evaluations and degraded performance, sometimes worse than A\* itself. Vision-Language Models (VLMs) partially address this issue by incorporating spatial grounding from visual inputs, enabling recognition of navigable areas and geometric relationships [Ye et al., 2025]. However, inherent limitations in longhorizon planning render both LLMs and VLMs ineffective as standalone end-to-end motion planners [Aghzal et al., 2023; Aghzal et al., 2024; Yang et al., 2025b]. This constraint necessitates a paradigm shift: rather than serving as autonomous controllers, these models may be more effectively utilized as supportive modules within a structured planning framework. The complementary strengths of LLMs and VLMs, balancing high-level semantic reasoning with precise geometric grounding, thus motivate a multimodal integration designed to unify abstract cognition with physical spatial constraints.

To this end, we propose MMP-A\*, which improves upon LLM-A\* to overcome its limitations by integrating the global reasoning of LLMs, the spatial perception of VLMs, and the deterministic guarantees of $\mathbf { A } ^ { * }$ into a unified framework. MMP-A\* operates through a three-stage pipeline: (1) an LLM first generates a coarse waypoint sequence reflecting high-level navigation intent; (2) a VLM refines these waypoints by visually analyzing the environment, pruning redundant or infeasible checkpoints; and (3) an adaptive decay mechanism dynamically regulates the influence of VLMvalidated waypoints in the heuristic function, attenuating their effect as uncertainty grows during search. This design prevents overreliance on stale or erroneous guidance while preserving the computational efficiency of waypoint-based exploration. Through this synergy of perception and reasoning, MMP-A\* achieves a robust balance between geometric fidelity, efficiency, and scalability, especially in highcomplexity maps characterized by dense barriers and intricate obstacle configurations. Our main contributions are summarized as follows:

• We propose MMP-A\*, a multimodal framework that seamlessly unifies LLM-based reasoning, VLM-driven spatial grounding, and adaptive heuristic modulation, thereby enabling computationally efficient and geometrically reliable path generation.

• We introduce an adaptive decay mechanism that dynamically modulates waypoint influence, maintaining balanced exploration–exploitation and preventing bias toward uncertain guidance.

• We conduct rigorous evaluations within highcomplexity environments characterized by dense obstacles and intricate layouts. Our findings show that MMP-A\* delivers significantly superior memory efficiency without compromising path optimality.

## 2 Related Work

Traditional Algorithms in Path Planning. Pathfinding has long been a fundamental problem in artificial intelligence, robotics, and computer graphics. The $\mathbf { A } ^ { * }$ algorithm [Hart et al., 1968a] remains foundational for combining heuristic estimation with optimality guarantees, inspiring numerous extensions to improve efficiency and adaptability. Notable A\* variants typically align with two distinct operational paradigms. In known environments, strategies such as IDA\* [Korf, 1985], RTA\*/LRTA\* [Korf, 1990], and SMA\* [Russell, 1992] address the equilibrium between computational cost, memory constraints, and responsiveness. In contrast, dynamic environments necessitate algorithms like D\* [Stentz, 1994], LPA\* [Koenig et al., 2004] or Bug1 [Lumelsky and Stepanov, 1987] which are explicitly engineered to facilitate efficient incremental replanning. To enhance scalability, hierarchical and structure-aware approaches like HPA\* [Botea et al., 2004] and JPS [Harabor and Grastien, 2011] further reduce search overhead, underscoring the enduring influence of heuristic search in modern path planning. In this context, our work specifically targets large-scale, known environments, aiming to address the scalability challenges posed by high-complexity static maps.

Large Language Models in Path Planning. LLMs have recently demonstrated impressive reasoning and generalization abilities across natural language processing and decisionmaking domains [Naveed et al., 2023; Chang et al., 2024; Ha et al., 2025]. Their capacity to decompose instructions and infer latent goals has motivated applications in highlevel planning and embodied control [Erdogan et al., 2025; Yang et al., 2025a; Zhao et al., 2023]. To address the computational complexity of path planning, works like [Meng et al., 2024] and [Tariq et al., 2025] utilize LLMs to generate highlevel waypoints, effectively pruning the search space and guiding geometric planners toward optimal solutions in largescale environments. Conversely, some approaches [Wang et al., 2024; Doma et al., 2024; Oelerich et al., 2024] focus on trajectory feasibility, employing LLMs to translate semantic instructions into dynamic cost map updates or task-space constraints, ensuring the generation of safe, collision-free paths under complex restrictions. However, LLMs still exhibit notable limitations in long-horizon planning and spatial reasoning, especially in tasks requiring continuous geometric understanding [Aghzal et al., 2023; Ilharco et al., 2020; Patel and Pavlick, 2021; Abdou et al., 2021]. To address this, we propose a hybrid framework that boosts high-level planning by coordinating LLMs with VLMs to anchor reasoning in physical space, coupled with a low-level A\* planner to deliver mathematically accurate pathfinding results.

Vision Language Models in Path Planning. VLMs have emerged as a promising solution to these spatial reasoning limitations by jointly processing visual and linguistic information [Zhang et al., 2024; Han et al., 2025; Xu et al., 2025]. Through visual grounding, VLMs directly perceive environmental geometry, allowing them to assess navigability and spatial patterns that remain opaque to text-only models. Recent frameworks utilize VLMs to ground search in visual reality, employing techniques like semantically-biased sampling [Ye et al., 2025] or visual affordance prompting [Chen et al., 2025] to steer planners toward safe, goal-relevant regions. Beyond generation, research also explores using VLMs as zero-shot reward models [Aghzal et al., 2025], evaluating trajectory compliance against complex constraints. Despite their perceptual capabilities, VLMs struggle to translate pixel-level information into continuous geometric coordinates, making visual input alone inadequate for rigorous motion planning [Baghaei et al., 2025; Colan et al., 2025].

## 3 Methodology

## 3.1 Problem Formulation

We formulate the navigation task as a path planning problem on a 2D grid map M. The map is partitioned into free space $\boldsymbol { S } _ { f r e e }$ and an obstacle set $S _ { o b s }$ , which consists of impassable barriers. For irregular or non-grid-aligned obstacles, we simplify their representation using axis-aligned orthogonal segments centered at their centroids to facilitate LLMbased symbolic reasoning (see Appendix A for more details).

![](Ha2026MMPA_figs/d5665b4f71e689597608e39558440ee638995364ec42d5d1ecf7ca741d734999.jpg)  
Figure 1: Overall framework of MMP-A\*: The proposed planner operates in three stages: (1) the LLM analyzes the map and generates coarse waypoint suggestions; (2) the VLM refines these by visually filtering redundant or invalid checkpoints; and (3) the refined waypoints guide the $\hat { \mathbf { A } } ^ { * }$ search through an adaptive fading-checkpoint heuristic, producing valid and efficient paths in complex environments.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 MMP-A* Algorithm with Adaptive Decay
1: Require: START state $s_0$, GOAL state $s_g$, OBSTACLE set $\mathcal{S}_{obs}$, heuristic function $h()$, cost function $g()$, $llm()$, $vlm()$, adaptive decay factor $\alpha \in (0,1)$
2: $\mathcal{O}_{open} \leftarrow \{s_0\}$, $\mathcal{C}_{close} \leftarrow \{\}$, TARGET list $\mathcal{T} \leftarrow vlm(llm(s_0,s_g,\mathcal{O}))$, TARGET state $t \leftarrow \mathcal{T}_{start}$, $g(s_0) \leftarrow 0$, $f(s_0) \leftarrow h(s_0)$, $k \leftarrow 0$
3: while $\mathcal{O}_{open} \neq \emptyset$ do
4:    $s_a \leftarrow \arg \min_{s \in \mathcal{O}_{open}} f(s)$
5:    if $s_a = s_g$ then
6:    return reconstruct_path($s_a$)
7:    Remove $s_a$ from $\mathcal{O}_{open}$
8:    Add $s_a$ to $\mathcal{C}_{close}$
9:    for all neighbors $s_n$ of $s_a$ do
10:    if $s_n = t$ and $s_g \neq t$ then
11:    $t \leftarrow \mathcal{T}_{next}$ ▷ Move to next waypoint
12:    $k \leftarrow k + 1$ ▷ Increment decay step
13:    Update $f$-cost of states in $\mathcal{O}_{open}$
14:    if $s_n \in (\mathcal{C}_{close} \cup \mathcal{S}_{obs})$ then
15:    continue
16:    Tentative cost $g_{tent} \leftarrow g(s_a) + \text{cost}(s_a, s_n)$
17:    if $s_n \notin \mathcal{O}_{open}$ or $g_{tent} &lt; g(s_n)$ then
18:    Update path to $s_n$ to go through $s_a$
19:    $g(s_n) \leftarrow g_{tent}$
20:    $f(s_n) \leftarrow g(s_n) + h_A^*(s_n) + \alpha^k \cdot \text{cost}(t, s_n)$
21:    if $s_n \notin \mathcal{O}_{open}$ then
22:    Add $s_n$ to $\mathcal{O}_{open}$
23: return failure
</div>

The robot is initialized at a starting state $s _ { 0 }$ and aims to reach a goal state $s _ { g } .$ . We adopt an 8-connected grid topology (Moore neighborhood), allowing the robot to transition to any adjacent cell $s ^ { \prime } \in \mathcal { S } _ { f r e e }$ . The transition cost is defined as the Euclidean distance: 1 for cardinal and $\sqrt { 2 }$ for diagonal movements. The objective is to generate a sequence of states $P = \{ s _ { 0 } , s _ { 1 } , . . . , s _ { g } \}$ such that every state in $P$ avoids $S _ { o b s } .$ ensuring a collision-free trajectory from source to destination.

To solve the formulation, we establish the classical $\mathbf { A } ^ { * }$ algorithm as the foundational planner. Unlike blind search methods, $\mathbf { A } ^ { * }$ directs the exploration by minimizing a heuristic-guided cost function $f ( s )$ for every visited node s:

$$
f (s) = g (s) + h _ {A ^ {*}} (s)\tag{1}
$$

Here, $g ( s )$ represents the accumulated exact cost from $s _ { 0 }$ to current node $s ,$ while $h _ { A ^ { * } } ( s )$ is a heuristic function estimating the remaining cost from s to $s _ { g } .$

The algorithm maintains a priority queue $\left( \mathcal { O } _ { \mathrm { o p e n } } \right)$ containing candidate nodes sorted by their f-values. At each iteration, the planner extracts the node with the minimal $f ( s )$ expands its valid neighbors in $S _ { \mathrm { f r e e } } ,$ and relaxes their costs if a more efficient path is discovered. Expanded nodes are retired to a CLOSED set $( \mathcal { C } _ { \mathrm { c l o s e } } )$ to prevent redundant processing. The search terminates when $s _ { g }$ is selected for expansion, at which point the optimal trajectory is reconstructed by backtracking parent pointers. Crucially, the optimality of the solution is guaranteed provided that $h _ { A ^ { * } } ( s )$ is admissible (i.e., it never overestimates the true remaining distance).

## 3.2 Overview

Figure 1 and Algorithm 1 illustrates the overall workflow of the proposed ${ \bf M } { \bf \bar { M } } { \bf P } { - } { \bf A } ^ { * }$ , which improves upon ${ \mathrm { L L M } } { \cdot } { \mathrm { A } } ^ { * }$ to resolve its scalability constraints and enhance adaptability in complex scenarios. The planner operates in three sequential stages that couple linguistic reasoning with visual spatial grounding. First, the LLM analyzes the global map and proposes a set of coarse waypoints representing high-level intent and directional guidance (Section 3.3). Second, the VLM refines these suggestions by examining the visual map, removing waypoints that lie in blocked regions or near walls, thus ensuring geometric feasibility and free-space alignment (Section 3.4). Finally, the refined waypoints are injected into the $\mathbf { A } ^ { * }$ search as a multimodal prior within an adaptive fadingcheckpoint heuristic (Section 3.5). This integration enables the search to leverage early linguistic cues for fast exploration while progressively decaying their influence to guarantee admissibility and optimal convergence.

## 3.3 LLM-Guided Waypoint Generation

In this phase, the LLM processes a textual encoding of the environment map to propose a high-level navigational strategy.

The model is tasked with generating a target list $T ,$ comprising coarse-grained waypoints that bridge the start state $s _ { 0 }$ and the goal state $s _ { g } ,$ thereby leveraging the LLM’s global reasoning capabilities. To ensure the structural integrity of the proposed path, two fundamental constraints are enforced:

1. Endpoint Consistency: The target set must strictly delimit the trajectory. Formally, we require $\{ s _ { 0 } , s _ { g } \} \subseteq T$ If the model fails to generate these boundary states, they are explicitly appended to the set.

2. Feasibility Verification: Every generated waypoint $t \in$ $T$ is validated against the environmental constraints. Any waypoint localized within an obstacle region $( \mathrm { i . e . } ,$ $t \in \boldsymbol { S } _ { o b s } )$ is identified as invalid and pruned from the list prior to subsequent processing.

Despite these structural safeguards, the LLM operates on abstract textual data and lacks intrinsic spatial grounding. Consequently, the generated waypoints may exhibit geometric inaccuracies. Critically, as the environment scales or obstacle density increases, the textual representation becomes unwieldy, leading to prohibitive computational costs and context-length bottlenecks. These limitations necessitate the subsequent stage, which employs visual perception to robustly validate and optimize the waypoint candidates.

## 3.4 VLM-Based Visual Refinement

To mitigate spatial hallucinations from the text-based phase, we introduce a VLM refinement stage that validates the coarse list $T .$ The model is prompted with two aligned visual inputs: (i) a raw occupancy grid marking barriers and $\{ s _ { 0 } , s _ { g } \}$ , and (ii) a visualization layer overlaying LLMproposed waypoints onto the grid. Our prompt engineering operationalizes the concept of a valid checkpoint as a node that maintains safety margins from walls and avoids congestion. The refinement workflow proceeds as follows:

1. Global Scene Understanding: The VLM scans the raw grid to map the global structure of the maze, assessing the spatial relationship between obstacles and the potential path from $s _ { 0 }$ to $s _ { g }$

2. Feasibility Filtering: The model scrutinizes each candidate in $\dot { T }$ against the visual evidence. Waypoints located in open, strategic positions are preserved. In contrast, those identified in blocked regions, dead-ends, or geometrically constrained passages are flagged as hazardous or redundant and are subsequently discarded to ensure a robust search space.

We prioritize visual verification over direct generation to exploit the resolution independence of the top-down view. Unlike coordinate-based generation, which struggles with the combinatorial explosion of large grids, a visual approach allows us to abstract the map into a fixed-size image. This ensures that the VLM’s ability to interpret global topology remains robust regardless of the map’s actual scale.

## 3.5 Adaptive Heuristic Search Integration

The original $\mathrm { L L M } { \cdot } \mathrm { A } { \ast }$ approach relies on waypoints generated by an LLM to guide the $\mathbf { A } ^ { * }$ search, which significantly enhances computational efficiency. However, this mechanism introduces a strong dependency on the correctness of the waypoints: when a waypoint is misplaced or misleading, the heuristic estimation

$$
h _ {L L M - A ^ {*}} (n) = h _ {A ^ {*}} (n) + c o s t (n, t _ {k})\tag{2}
$$

becomes unstable. Here $c o s t ( n , t _ { k } )$ measures the cost from the current node n to the current waypoint $t _ { k }$ . Consequently, the search tends to diverge toward suboptimal areas, greatly increasing computation and slowing convergence. This limitation arises from the static treatment of LLM-generated waypoints, where the algorithm maintains excessive confidence in each waypoint regardless of its reliability. To address this issue, we introduce an adaptive decay factor α to dynamically reduce the influence of LLM-generated waypoints over time. Specifically, the heuristic function is reformulated as

$$
h _ {M M P - A ^ {*}} (n) = h _ {A ^ {*}} (n) + \alpha^ {k} c o s t (n, t _ {k}),\tag{3}
$$

where $\alpha \in ( 0 , 1 )$ decays exponentially with each waypoint switch (k denotes the index of the current waypoint).

As the search progresses toward the goal, the influence of intermediate waypoints gradually diminishes, making the heuristic increasingly focused on the actual target. This adaptive strategy mitigates the bias introduced by unreliable LLM waypoints, improving both the stability of heuristic estimation and the overall efficiency of the search process.

## 3.6 Theoretical Analysis

We analyze the theoretical properties of the adaptive decay heuristic employed in ${ \bf M P - A } ^ { * }$

Proposition 3.1 (Bounded Suboptimality). Let $h _ { A ^ { * } } ( n )$ be an admissible heuristic and define

$$
h _ {M M P - A ^ {*}} (n) = h _ {A ^ {*}} (n) + \alpha^ {k} \cdot c (n, t _ {k}), \quad \alpha \in (0, 1),
$$

where $t _ { k }$ denotes the current waypoint and $c ( n , t _ { k } )$ is the estimated cost from node n to $t _ { k } .$ . Assume that there exists a finite constant $D _ { \mathrm { m a x } }$ such that $c ( n , t _ { k } ) \leq D _ { \mathrm { m a x } }$ for all n and $k , e . g .$ ., the maximum shortest-path distance in the finite grid. Then, for any finite $k ,$

$$
h _ {M M P - A ^ {*}} (n) \leq h ^ {*} (n) + \alpha^ {k} D _ {\mathrm{max}},
$$

where $h ^ { * } ( n )$ denotes the true optimal cost-to-go. Consequently, the heuristic exhibits bounded additive suboptimality with an error term $\alpha ^ { k } D _ { \mathrm { m a x } }$

Proof Sketch. By admissibility of $h _ { A ^ { * } }$ ∗, we have $h _ { A ^ { * } } ( n ) \leq$ $h ^ { * } ( n )$ Since the waypoint-dependent term $c ( n , t _ { k } )$ is bounded by $D _ { \mathrm { m a x } }$ and scaled by $\hat { \alpha } ^ { k }$ , the heuristic introduces a bounded additive overestimation that decays exponentially with the waypoint index. □

Proposition 3.2 (Pointwise Convergence). For any node n,

$$
\lim _ {k \to \infty} h _ {M M P - A ^ {*}} (n) = h _ {A ^ {*}} (n).
$$

Proof Sketch. Since $\alpha \in ( 0 , 1 )$ , the decay factor satisfies $\begin{array} { r } { \operatorname* { l i m } _ { k \to \infty } \alpha ^ { k } = 0 } \end{array}$ . As a result, the waypoint guidance term vanishes asymptotically, and the heuristic converges pointwise to the admissible base heuristic $h _ { A ^ { * } }$ □

Proposition 3.3 (Robustness against Long-Horizon Spatial Hallucinations). In large-scale environments where the sequence length k is significant, VLM reliability typically degrades, leading to high-error waypoints (hallucinations). Under the LLM-A\* formulation $( \alpha = 1 )$ , a misleading waypoint $t _ { k }$ imposes a persistent heuristic penalty $c ( n , t _ { k } )$ , forcing the planner to detour towards the erroneous location regardless of the path length. In contrast, MMP-A\* attenuates this risk via the decay factor $\alpha ^ { k }$ . For large k, the influence of the misleading waypoint vanishes:

$$
\lim _ {k \to \infty} \alpha^ {k} \cdot c (n, t _ {k}) = 0.
$$

This property ensures that as the problem scale increases, MMP- ${ \bf \nabla } \cdot { \bf A ^ { * } }$ automatically decouples from potentially unreliable VLM guidance and reverts to the admissible goaldirected behavior of $h _ { A ^ { * } } ( n )$ , effectively bypassing misleading traps that would otherwise entrap a LLM-A\* planner.

## 4 Experiments

## 4.1 Dataset

We validate our framework using a suite of 200 highcomplexity maps (100×60) that exhibits significantly greater topological intricacy than the sparse environments typical of prior LLM-A\* research. By incorporating labyrinthine corridors and deceptive dead-ends, these topologies are explicitly designed to induce local optima, effectively neutralizing greedy heuristics and necessitating robust global reasoning. To ensure a holistic assessment across diverse navigational scenarios, we implement a dual-faceted evaluation protocol:

1. Scalability is examined by expanding map dimensions from 30×50 to 240×400 under strict topological invariance, explicitly isolating algorithmic efficiency from environmental structure.

2. Environmental Complexity is modulated via obstacle density, culminating in Level 5, a rigorous benchmark featuring approximate 12 intertwined barrier clusters and deep dead-ends designed to challenge multimodal reasoning.

3. Irregular Obstacles introduces undefined hazard zones that do not fit standard grid lines. This evaluates visual perception in scenarios where text-based descriptions become inefficient or impractical.

Figure 3 illustrates samples from our curated datasets. For a detailed specification of these parameters and generation protocols, please refer to Appendix D.

## 4.2 Experimental Setup

Models and Parameters. We evaluate ${ \bf M } { \bf M } { \bf P } { - } { \bf A } ^ { * }$ using representative models including GPT-4o-mini, Llama-3.3- 70B, Qwen2.5-7B, and DeepSeek-V3 for reasoning, alongside Llama-4-Maverick, Gemma-3n, and Qwen2.5-VL for perception. We focus our evaluation on $\mathbf { A } ^ { * }$ and LLM-$\mathbf { A } ^ { * }$ as primary baselines to isolate and validate the specific efficiency gains of the VLM-integrated methodology. Implementation-wise, we adopt standard few-shot, Chain-of-Thought, and Recursive Path Evaluation (RePE) strategies with a fixed heuristic decay factor $\alpha = 0 . 7$ (see Appendix B and C for full prompt details).

Experiment Metrics and Objectives. Our evaluation focuses on efficiency and scalability by benchmarking MMP-$\mathbf { A } ^ { * }$ against $\mathbf { A } ^ { * }$ and ${ \mathrm { L L M } } { \cdot } { \mathrm { A } } ^ { * }$ . We assess computational cost and memory usage via Operation and Storage Ratios, computed as the geometric mean of performance ratios between ${ \bf M } { \bf M } { \bf P } { - } { \bf A } ^ { * }$ and the $\mathbf { A } ^ { * }$ baseline $\bf ( \frac { M M P - A ^ { * } } { A ^ { * } } )$ , where lower values indicate superior resource efficiency. Path optimality is evaluated via Relative Path Length, while system reliability is measured by the Valid Path Ratio, representing the proportion of successfully generated collision-free trajectories. Comprehensive results are summarized in Table 1. Figure 8 in Appendix visualizes representative sample results, demonstrating how MMP-A\* allows the planner to bypass misleading waypoints and yield smoother trajectories.

## 4.3 Experimental Results

Overall Quantitative Results. The comprehensive evaluation in Table 1–2 reveals that purely generative models fail to capture topological constraints of complex environments, yielding Valid Path Ratios below 10% and trajectories inflated by up to 30% due to geometric hallucinations. While integrating language guidance with search via LLM-A\* resolves the validity issue, it inadvertently incurs a substantial computational penalty, with operation ratios surging to 191.6% in some configurations as the search algorithm is forced to explore misleading regions suggested by noisy heuristics. In stark contrast, our proposed $\mathrm { { \dot { M } M P  – A } ^ { * } }$ achieves a superior balance of efficiency and optimality across all model backbones. By leveraging VLM-based visual pruning to eliminate infeasible waypoints before the search commences and employing an adaptive heuristic decay, ${ \bf M } { \bf M } { \bf P } { - } { \bf A } ^ { * }$ not only guarantees 100% validity but also drastically reduces resource consumption, bringing operation and storage costs down to $8 1 . 0 \%$ and $7 6 . 0 \%$ respectively while maintaining path lengths within 2% of the optimal solution. We discuss the comparative efficiency of LLM–VLM models and their limitations in Appendix $\dot { \mathrm { E } } .$

Complex Environments Analysis The robustness of this improvement becomes clearer in Table 4 and Figure 4a, where we stress-test the system under increasingly complex maze environments. As obstacle density grows, $\mathrm { L L M - A } ^ { * }$ exhibits unstable behavior, often consuming two to three times more operations than the baseline due to misleading guidance from noisy checkpoints. In contrast, $\mathbf { M M P - A } ^ { * }$ maintains steady performance across all difficulty levels. For instance, with the DeepSeek-V3 and Qwen2.5-VL pairing, the operation ratio remains between 45–97% and the storage ratio between 53–86% from Level 1 to Level 5, consistently outperforming both $\mathbf { A } ^ { * }$ and LLM-A\*. The relative path length stays close to optimal, indicating that the efficiency gain arises from reduced exploration rather than from sacrificing solution quality. These results show that visual pruning is especially useful in cluttered or irregular environments, as it stops the search from following dead-end or wall-hugging paths suggested by the LLM.

Scalability Analysis. Table 5 and Figure 4b further investigates scalability across grid sizes ranging from 30×50 to $2 4 0 \times 4 0 0$ As observed, ${ \mathrm { L L M } } { \cdot } { \mathrm { A } } ^ { * }$ becomes increasingly unstable at larger scales, sometimes performing worse than vanilla $\mathbf { A } ^ { * }$ due to accumulated waypoint noise over longer planning horizons. Conversely, MMP-A\* demonstrates consistent and even improving efficiency with scale. Using the GPT-4o-mini and Gemma-3n-E4B pairing, operation ratios rise only slightly from about 63% to 77%, while storage ratios decline from 73% to 59% as the map enlarges, all while preserving near-optimal path lengths. This stable scaling behavior confirms that our multimodal filtering and fading-heuristic design not only improves small-scale navigation but also generalizes to large, complex search spaces.

<table><tr><td>Methodology</td><td>LLM Model</td><td>VLM Model</td><td>Operation Ratio ↓ (%)</td><td>Storage Ratio ↓ (%)</td><td>Relative Path Length ↓ (%)</td><td>Valid Path Ratio ↑ (%)</td></tr><tr><td>A*</td><td></td><td></td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td rowspan="4">LLM-A*</td><td>DeepSeek-V3</td><td></td><td>125.2</td><td>114.6</td><td>103.4</td><td>100</td></tr><tr><td>Llama-3.3-70B</td><td></td><td>112.1</td><td>103.1</td><td>103.3</td><td>100</td></tr><tr><td>Qwen2.5-7B</td><td></td><td>191.6</td><td>141.4</td><td>102.5</td><td>100</td></tr><tr><td>GPT-4o-mini</td><td></td><td>115.3</td><td>104.6</td><td>103.5</td><td>100</td></tr><tr><td rowspan="12">MMP-A*</td><td rowspan="3">DeepSeek-V3</td><td>Gemma-3n-E4B</td><td>91.1</td><td>86.0</td><td>101.9</td><td>100</td></tr><tr><td>Llama 4 Maverick</td><td>93.9</td><td>87.8</td><td>101.6</td><td>100</td></tr><tr><td>Qwen2.5-VL</td><td>84.9</td><td>80.6</td><td>102.2</td><td>100</td></tr><tr><td rowspan="3">Llama-3.3-70B</td><td>Gemma-3n-E4B</td><td>88.5</td><td>81.5</td><td>102.0</td><td>100</td></tr><tr><td>Llama 4 Maverick</td><td>97.0</td><td>91.0</td><td>101.8</td><td>100</td></tr><tr><td>Qwen2.5-VL</td><td>81.0</td><td>76.0</td><td>102.3</td><td>100</td></tr><tr><td rowspan="3">Qwen2.5-7B</td><td>Gemma-3n-E4B</td><td>150.4</td><td>106.3</td><td>101.9</td><td>100</td></tr><tr><td>Llama 4 Maverick</td><td>181.0</td><td>129.8</td><td>101.5</td><td>100</td></tr><tr><td>Qwen2.5-VL</td><td>162.8</td><td>114.8</td><td>102.2</td><td>100</td></tr><tr><td rowspan="3">GPT-4o-mini</td><td>Gemma-3n-E4B</td><td>82.4</td><td>76.5</td><td>102.2</td><td>100</td></tr><tr><td>Llama 4 Maverick</td><td>97.4</td><td>88.3</td><td>101.6</td><td>100</td></tr><tr><td>Qwen2.5-VL</td><td>81.0</td><td>76.4</td><td>102.3</td><td>100</td></tr></table>

Table 1: Quantitative comparison between baseline A\*, LLM-A\* and our multimodal framework MMP-A\*

<table><tr><td>Methodology</td><td>LLM Model</td><td>VLM Model</td><td>Rel. Path ↓</td><td>Valid ↑</td></tr><tr><td>A*</td><td></td><td></td><td>100</td><td>100</td></tr><tr><td rowspan="4">LLM</td><td>DeepSeek-V3</td><td></td><td>116.8</td><td>7.0</td></tr><tr><td>Llama-3.3-70B</td><td></td><td>123.5</td><td>8.6</td></tr><tr><td>Qwen2.5-7B</td><td></td><td>130.4</td><td>4.5</td></tr><tr><td>GPT-4o-mini</td><td></td><td>112.0</td><td>7.5</td></tr><tr><td rowspan="3">VLM</td><td></td><td>Gemma-3n-E4B</td><td>114.3</td><td>6.0</td></tr><tr><td></td><td>Llama 4 Maverick</td><td>122.4</td><td>6.5</td></tr><tr><td></td><td>Qwen2.5-VL</td><td>119.5</td><td>8.0</td></tr><tr><td rowspan="12">LLM + VLM</td><td rowspan="3">DeepSeek-V3</td><td>Gemma-3n-E4B</td><td>110.0</td><td>8.0</td></tr><tr><td>Llama 4 Maverick</td><td>110.6</td><td>9.0</td></tr><tr><td>Qwen2.5-VL</td><td>107.9</td><td>9.5</td></tr><tr><td rowspan="3">Llama-3.3-70B</td><td>Gemma-3n-E4B</td><td>101.3</td><td>5.1</td></tr><tr><td>Llama 4 Maverick</td><td>114.9</td><td>9.7</td></tr><tr><td>Qwen2.5-VL</td><td>105.7</td><td>6.1</td></tr><tr><td rowspan="3">Qwen2.5-7B</td><td>Gemma-3n-E4B</td><td>112.6</td><td>4.0</td></tr><tr><td>Llama 4 Maverick</td><td>118.0</td><td>5.0</td></tr><tr><td>Qwen2.5-VL</td><td>109.1</td><td>3.5</td></tr><tr><td rowspan="3">GPT-4o-mini</td><td>Gemma-3n-E4B</td><td>100.9</td><td>5.5</td></tr><tr><td>Llama 4 Maverick</td><td>104.2</td><td>6.0</td></tr><tr><td>Qwen2.5-VL</td><td>103.3</td><td>6.0</td></tr></table>

Table 2: Comparison between A\* and GenAI-based methods

<table><tr><td>Methodology</td><td>Operation ↓</td><td>Storage ↓</td><td>Rel. Path ↓</td></tr><tr><td>A*</td><td>100</td><td>100</td><td>100</td></tr><tr><td>LLM-A*</td><td>123.7</td><td>113.1</td><td>103.2</td></tr><tr><td>MMP-A*</td><td>88.9</td><td>82.1</td><td>102.1</td></tr></table>

Table 3: Comparison of A\*, LLM-A\*, and MMP-A\* performance.

General Applicability beyond Grid Constraints. While specialized $\mathbf { A } ^ { * }$ variants offer runtime acceleration, they remain confined to rigid grid structures, and LLM-A\* struggles to textually describe amorphous hazards (e.g., irregular hazardous regions), MMP-A\* achieves robust generalization through direct visual perception. By treating the environment as a visual scene rather than a coordinate list, our VLM-based approach intuitively interprets arbitrary obstacle shapes that defy rigid geometric definitions. This versatility leads to superior efficiency (Table 3), with MMP-A\* achieving an operation score of 88.9, effectively navigating complex scenarios where traditional grid-centric assumptions break down.

## 4.4 Ablation Study

Alpha-Decay Sensitivity Analysis. As shown in Table 11 in Appendix and Figure 2, incorporating adaptive decay slightly increases the operation and storage ratios, by about 5–10%, since the planner performs extra expansions to refine its heuristic. Nevertheless, it remains markedly more efficient than vanilla A\*, while consistently producing smoother and shorter paths. This small overhead is offset by a 1–2% reduction in relative path length, confirming that adaptive decay effectively stabilizes the search by gradually lowering reliance on uncertain early waypoints. When varying the decay coefficient α, we observe a clear efficiency–optimality tradeoff: higher α values reduce operation cost but yield longer paths due to stronger waypoint bias, whereas lower α values encourage broader exploration and shorter trajectories at slightly higher cost. Overall, moderate α values achieve the best balance, preserving efficiency gains while maintaining near-optimal path quality.

Runtime–performance trade-off. We analyze the runtime cost, inclusive of API latency, across varying environmental complexities. MMP-A\* effectively amortizes reasoning overheads in large-scale settings, achieving runtime parity or even acceleration compared to LLM-A\* while delivering superior memory efficiency. For a detailed discussion, please refer to Appendix F.

Prompt Engineering Strategy. We evaluated three prompting schemes to analyze their influence on waypoint

<table><tr><td rowspan="2">Methodology</td><td rowspan="2">Base Model</td><td colspan="3">Level 1</td><td colspan="3">Level 2</td><td colspan="3">Level 3</td><td colspan="3">Level 4</td><td colspan="3">Level 5</td></tr><tr><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td></tr><tr><td>A*</td><td>-</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td rowspan="4">LLM-A*</td><td>DeepSeek-V3</td><td>52.1</td><td>59.3</td><td>103.6</td><td>70.9</td><td>72.6</td><td>104.0</td><td>130.5</td><td>103.0</td><td>105.5</td><td>110.0</td><td>96.8</td><td>103.7</td><td>124.1</td><td>109.6</td><td>103.1</td></tr><tr><td>Llama-3.3-70B</td><td>86.6</td><td>62.5</td><td>103.5</td><td>68.7</td><td>72.2</td><td>103.3</td><td>119.8</td><td>88.7</td><td>104.8</td><td>99.4</td><td>94.3</td><td>104.7</td><td>112.2</td><td>103.7</td><td>102.7</td></tr><tr><td>Qwen2.5-7B</td><td>300.0</td><td>128.1</td><td>103.8</td><td>130.6</td><td>116.5</td><td>102.6</td><td>300.2</td><td>139.1</td><td>104.1</td><td>149.7</td><td>125.2</td><td>103.7</td><td>121.6</td><td>112.0</td><td>102.8</td></tr><tr><td>GPT-4o-mini</td><td>74.6</td><td>75.8</td><td>103.3</td><td>88.9</td><td>83.1</td><td>102.8</td><td>129.8</td><td>82.7</td><td>105.6</td><td>99.3</td><td>93.6</td><td>104.3</td><td>111.5</td><td>104.7</td><td>102.8</td></tr><tr><td rowspan="4">MMP-A*</td><td>DeepSeek-V3 + Qwen2.5-VL</td><td>45.4</td><td>53.1</td><td>102.3</td><td>61.7</td><td>65.2</td><td>103.0</td><td>81.8</td><td>78.4</td><td>102.9</td><td>78.2</td><td>73.9</td><td>102.9</td><td>96.8</td><td>86.2</td><td>102.1</td></tr><tr><td>Llama-3.3-70B + Qwen2.5-VL</td><td>65.9</td><td>56.8</td><td>102.5</td><td>66.4</td><td>68.8</td><td>102.6</td><td>83.3</td><td>70.3</td><td>104.0</td><td>75.5</td><td>75.8</td><td>103.3</td><td>90.5</td><td>80.8</td><td>102.1</td></tr><tr><td>Qwen2.5-7B + Qwen2.5-VL</td><td>269.8</td><td>102.7</td><td>101.9</td><td>80.9</td><td>78.7</td><td>102.1</td><td>221.2</td><td>114.2</td><td>103.2</td><td>111.2</td><td>98.4</td><td>102.8</td><td>111.8</td><td>99.1</td><td>102.4</td></tr><tr><td>GPT-4o-mini + Qwen2.5-VL</td><td>49.5</td><td>60.0</td><td>101.7</td><td>44.3</td><td>52.3</td><td>101.9</td><td>93.9</td><td>74.3</td><td>103.0</td><td>71.6</td><td>71.0</td><td>102.2</td><td>88.9</td><td>84.7</td><td>101.9</td></tr></table>

Table 4: Complex Environment Experiment

<table><tr><td rowspan="2">Methodology</td><td rowspan="2">Base Model</td><td colspan="3">Level 1 (30×50)</td><td colspan="3">Level 2 (60×100)</td><td colspan="3">Level 3 (120×200)</td><td colspan="3">Level 4 (180×300)</td><td colspan="3">Level 5 (240×400)</td></tr><tr><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td><td>Op</td><td>Stor</td><td>Rel</td></tr><tr><td>A*</td><td>-</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr><tr><td>LLM-A*</td><td>GPT-4o-mini</td><td>85.5</td><td>88.5</td><td>101.5</td><td>97.2</td><td>91.3</td><td>103.4</td><td>102.8</td><td>92.9</td><td>104.8</td><td>106.1</td><td>93.7</td><td>103.7</td><td>100.7</td><td>83.1</td><td>104.1</td></tr><tr><td>MMP-A*</td><td>GPT-4o-mini + Gemma-3n-E4B</td><td>63.1</td><td>73.4</td><td>100.9</td><td>80.5</td><td>76.9</td><td>101.8</td><td>89.9</td><td>79.8</td><td>102.2</td><td>89.4</td><td>75.4</td><td>102.6</td><td>76.6</td><td>59.3</td><td>102.5</td></tr></table>

Table 5: Scale Robustness Experiment  
![](Ha2026MMPA_figs/e7327c7ecd0fc3b27ac06da0b261594ee69d1b4509432694b00481c09ed847f0.jpg)  
Figure 2: Alpha-Decay Sensitivity Analysis. Operation ratio (bars) and relative path length (lines) of LLM-A\* and MMP-A\* under varying decay coefficients α.

![](Ha2026MMPA_figs/5e430038a9f0e14b7a1d2e2ee6680cc6bc180ba8fa906f2e9e093b9cd0e50e5f.jpg)  
Figure 3: Visualization of the experimental setup. The bottom row depicts the core dataset featuring dense, maze-like topologies. The top row illustrates the generality assessment subset, where irregular, amorphous barriers (shaded red) are superimposed to rigorously evaluate the framework’s visual generalization capabilities against non-geometric obstacles.

generation and search efficiency. As summarized in Table 10 and Figure 10 in Appendix, CoT prompts generally yield better reasoning consistency but incur higher computational cost, with operation ratios often 10–20% above Few-Shot setups. RePE introduces recursive self-evaluation, which improves local waypoint precision and slightly reduces path length (about 0.5–1.0%), though at the expense of additional memory usage. Among these, Few-Shot remains the most lightweight and stable baseline, while RePE offers the best trade-off between cost and accuracy when integrated with MMP-A\*.

![](Ha2026MMPA_figs/6528f6feba4e4edf41a075d545ef3993f274e0a3e8b7710e98bfe3d1e7bcf458.jpg)  
Figure 4: (a) Complex Environment Experiment: Operation and storage ratios across increasing map complexity levels. (b) Scale Robustness Experiment: Growth factors of operations and storages across varying map sizes.

## 5 Conclusion

In this work, we proposed MMP-A\*, a multimodal perception–enhanced pathfinding framework that tightly integrates LLM reasoning, VLM visual filtering, and adaptive heuristic decay into classical A\* search. The method demonstrates particular strength in complex and cluttered environments, where pure language-guided or traditional heuristic planners often fail. Through extensive experiments, ${ \bf M P - A } ^ { * }$ consistently maintains 100% path validity while achieving lower operation and storage costs, especially under high obstacle density and large-scale maps. The adaptive decay mechanism further stabilizes performance by balancing exploration and guidance, allowing the planner to refine its trajectory as search progresses. These results suggest that MMP-A\* is especially well-suited for dynamic or visually ambiguous navigation tasks, where multimodal understanding and adaptive reasoning are essential for robust and efficient planning.

## References

[Abd Algfoor et al., 2015] Zeyad Abd Algfoor, Mohd Shahrizal Sunar, and Hoshang Kolivand. A comprehensive study on pathfinding techniques for robotics and video games. International Journal of Computer Games Technology, 2015(1):736138, 2015.

[Abdou et al., 2021] Mostafa Abdou, Artur Kulmizev, Daniel Hershcovich, Stella Frank, Ellie Pavlick, and Anders Søgaard. Can language models encode perceptual structure without grounding? a case study in color. arXiv preprint arXiv:2109.06129, 2021.

[Aghzal et al., 2023] Mohamed Aghzal, Erion Plaku, and Ziyu Yao. Can large language models be good path planners? a benchmark and investigation on spatial-temporal reasoning. arXiv preprint arXiv:2310.03249, 2023.

[Aghzal et al., 2024] Mohamed Aghzal, Erion Plaku, and Ziyu Yao. Look further ahead: Testing the limits of gpt-4 in path planning. In 2024 IEEE 20th International Conference on Automation Science and Engineering (CASE), pages 1020–1027. IEEE, 2024.

[Aghzal et al., 2025] Mohamed Aghzal, Xiang Yue, Erion Plaku, and Ziyu Yao. Evaluating vision-language models as evaluators in path planning. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 6886–6897, 2025.

[Baghaei et al., 2025] Kourosh T Baghaei, Dieter Pfoser, and Antonios Anastasopoulos. Follow the beaten path: The role of route patterns on vision-language navigation agents generalization abilities. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pages 7986–8005, 2025.

[Botea et al., 2004] Adi Botea, Martin Muller, and Jonathan¨ Schaeffer. Near optimal hierarchical path-finding. Journal of Game Development, 1(1):7–28, 2004.

[Caglar et al., 2024] Turgay Caglar, Sirine Belhaj, Tathagata Chakraborty, Michael Katz, and Sarath Sreedharan. Can llms fix issues with reasoning models? towards more likely models for ai planning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages 20061–20069, 2024.

[Cao et al., 2025] Pengfei Cao, Tianyi Men, Wencan Liu, Jingwen Zhang, Xuzhao Li, Xixun Lin, Dianbo Sui, Yanan Cao, Kang Liu, and Jun Zhao. Large language models for planning: A comprehensive and systematic survey. arXiv preprint arXiv:2505.19683, 2025.

[Chang et al., 2024] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, et al. A survey on evaluation of large language models. ACM transactions on intelligent systems and technology, 15(3):1–45, 2024.

[Chen et al., 2025] Jiaqi Chen, Bingqian Lin, Xinmin Liu, Lin Ma, Xiaodan Liang, and Kwan-Yee K Wong. Affordances-oriented planning using foundation models

for continuous vision-language navigation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 23568–23576, 2025.

[Colan et al., 2025] Jacinto Colan, Ana Davila, and Yasuhisa Hasegawa. Assessing the value of visual input: A benchmark of multimodal large language models for robotic path planning. arXiv preprint arXiv:2507.12391, 2025.

[Doma et al., 2024] Pranav Doma, Aliasghar Arab, and Xuesu Xiao. Llm-enhanced path planning: Safe and efficient autonomous navigation with instructional inputs. arXiv preprint arXiv:2412.02655, 2024.

[Erdogan et al., 2025] Lutfi Eren Erdogan, Nicholas Lee, Sehoon Kim, Suhong Moon, Hiroki Furuta, Gopala Anumanchipalli, Kurt Keutzer, and Amir Gholami. Plan-andact: Improving planning of agents for long-horizon tasks. arXiv preprint arXiv:2503.09572, 2025.

[Gonzalez´ et al., 2015] David Gonzalez, Joshu´ e P´ erez, Vi-´ cente Milanes, and Fawzi Nashashibi. A review of motion´ planning techniques for automated vehicles. IEEE Transactions on intelligent transportation systems, 17(4):1135– 1145, 2015.

[Ha et al., 2025] Minh Hieu Ha, Hung Phan, Tung Duy Doan, Tung Dao, Dao Tran, and Huynh Thi Thanh Binh. Pareto-grid-guided large language models for fast and high-quality heuristics design in multi-objective combinatorial optimization. arXiv preprint arXiv:2507.20923, 2025.

[Han et al., 2025] Xiaofeng Han, Shunpeng Chen, Zenghuang Fu, Zhe Feng, Lue Fan, Dong An, Changwei Wang, Li Guo, Weiliang Meng, Xiaopeng Zhang, et al. Multimodal fusion and vision-language models: A survey for robot vision. Information Fusion, page 103652, 2025.

[Harabor and Grastien, 2011] Daniel Harabor and Alban Grastien. Online graph pruning for pathfinding on grid maps. In Proceedings of the AAAI conference on artificial intelligence, volume 25, pages 1114–1119, 2011.

[Hart et al., 1968a] Peter Hart, Nils Nilsson, and Bertram Raphael. A formal basis for the heuristic determination of minimum cost paths. IEEE Transactions on Systems Science and Cybernetics, 4(2):100–107, 1968.

[Hart et al., 1968b] Peter E Hart, Nils J Nilsson, and Bertram Raphael. A formal basis for the heuristic determination of minimum cost paths. IEEE transactions on Systems Science and Cybernetics, 4(2):100–107, 1968.

[Ilharco et al., 2020] Gabriel Ilharco, Rowan Zellers, Ali Farhadi, and Hannaneh Hajishirzi. Probing contextual language models for common ground with visual representations. arXiv preprint arXiv:2005.00619, 2020.

[Joublin et al., 2024] Frank Joublin, Antonello Ceravola, Pavel Smirnov, Felix Ocker, Joerg Deigmoeller, Anna Belardinelli, Chao Wang, Stephan Hasler, Daniel Tanneberg, and Michael Gienger. Copal: corrective planning of robot actions with large language models. In 2024 ieee international conference on robotics and automation (ICRA), pages 8664–8670. IEEE, 2024.

[Karaman and Frazzoli, 2011] Sertac Karaman and Emilio Frazzoli. Sampling-based algorithms for optimal motion planning. The International Journal of Robotics Research, 30(7):846–894, 2011.

[Koenig et al., 2004] Sven Koenig, Maxim Likhachev, and David Furcy. Lifelong planning a. Artificial Intelligence, 155(1-2):93–146, 2004.

[Korf, 1985] Richard E Korf. Depth-first iterativedeepening: An optimal admissible tree search. Artificial Intelligence, 27(1):97–109, 1985.

[Korf, 1990] Richard E Korf. Real-time heuristic search. Artificial Intelligence, 42(2-3):189–211, 1990.

[Lumelsky and Stepanov, 1987] Vladimir J Lumelsky and Alexander A Stepanov. Path-planning strategies for a point mobile automaton moving amidst unknown obstacles of arbitrary shape. Algorithmica, 2(1):403–430, 1987.

[Meng et al., 2024] Silin Meng, Yiwei Wang, Cheng-Fu Yang, Nanyun Peng, and Kai-Wei Chang. Llm-a\*: Large language model enhanced incremental heuristic search on path planning. arXiv preprint arXiv:2407.02511, 2024.

[Naveed et al., 2023] Humza Naveed, Asad Ullah Khan, Shi Qiu, Muhammad Saqib, Saeed Anwar, Muhammad Usman, Nick Barnes, and Ajmal Mian. A comprehensive overview of large language models. arXiv preprint arXiv:2307.06435, 2023.

[Oelerich et al., 2024] Thies Oelerich, Christian Hartl-Nesic, and Andreas Kugi. Language-guided manipulator motion planning with bounded task space. In 8th Annual Conference on Robot Learning, 2024.

[Patel and Pavlick, 2021] Roma Patel and Ellie Pavlick. Mapping language models to grounded conceptual spaces. In International Conference on Learning Representations, 2021.

[Russell, 1992] Stuart J Russell. Memory-bounded heuristic search. Artificial Intelligence, 49(1-3):5–27, 1992.

[Stentz, 1994] Anthony Stentz. Optimal and efficient path planning for partially-known environments. In Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), pages 3310–3317, 1994.

[Tariq et al., 2025] Muhammad Taha Tariq, Yasir Hussain, and Congqing Wang. Robust mobile robot path planning via llm-based dynamic waypoint generation. Expert Systems with Applications, 282:127600, 2025.

[Wang et al., 2024] Shu Wang, Muzhi Han, Ziyuan Jiao, Zeyu Zhang, Ying Nian Wu, Song-Chun Zhu, and Hangxin Liu. Llmˆ 3: Large language model-based task and motion planning with motion failure reasoning. In 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 12086–12092. IEEE, 2024.

[Wei et al., 2025] Hui Wei, Zihao Zhang, Shenghua He, Tian Xia, Shijia Pan, and Fei Liu. Plangenllms: A modern survey of llm planning capabilities. arXiv preprint arXiv:2502.11221, 2025.

[Xu et al., 2025] Guowei Xu, Peng Jin, Ziang Wu, Hao Li, Yibing Song, Lichao Sun, and Li Yuan. Llava-cot: Let vision language models reason step-by-step. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 2087–2098, 2025.

[Yang et al., 2025a] Dejie Yang, Zijing Zhao, and Yang Liu. Planllm: Video procedure planning with refinable large language models. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 9166–9174, 2025.

[Yang et al., 2025b] Zhutian Yang, Caelan Garrett, Dieter Fox, Tomas Lozano-P´ erez, and Leslie Pack Kaelbling.´ Guiding long-horizon task and motion planning with vision language models. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pages 16847– 16853. IEEE, 2025.

[Ye et al., 2025] Jianlin Ye, Savvas Papaioannou, and Panayiotis Kolios. Vlm-rrt: Vision language model guided rrt search for autonomous uav navigation. In 2025 International Conference on Unmanned Aircraft Systems (ICUAS), pages 633–640. IEEE, 2025.

[Zhang et al., 2024] Jingyi Zhang, Jiaxing Huang, Sheng Jin, and Shijian Lu. Vision-language models for vision tasks: A survey. IEEE transactions on pattern analysis and machine intelligence, 46(8):5625–5644, 2024.

[Zhao et al., 2023] Zirui Zhao, Wee Sun Lee, and David Hsu. Large language models as commonsense knowledge for large-scale task planning. Advances in neural information processing systems, 36:31967–31987, 2023.

## A Selection of Symbolic Obstacle Representations

The efficacy of LLM-based path planning is heavily dependent on how spatial constraints are encoded into text. We evaluate the trade-offs between two primary symbolic strategies: Boundary Enclosure and our proposed Orthogonal Centroid Segments, as can be seen in Figure 5. Traditional boundary enclosure, which involves listing the coordinates of all boundary cells or multiple bounding boxes to encapsulate an irregular shape, proves highly ineffective for LLMs. As the map resolution increases or obstacle geometry becomes more complex, this method leads to a token explosion, often exceeding the model’s context window and increasing inference latency. Furthermore, the high density of numerical coordinates creates significant spatial noise, causing the LLM to suffer from reasoning fatigue and hallucinations, where it fails to identify navigable gaps or misinterprets the overall topology of the environment.

In contrast, our MMP-A\* framework adopts a skeletonized representation by approximating each irregular barrier B with two axis-aligned orthogonal segments of unit width intersecting at the centroid $( x _ { c } , y _ { c } )$ This approach ensures a constant token footprint regardless of the obstacle’s actual area or geometric complexity, allowing the system to scale efficiently to large-scale maps. By reducing a complex “blob” to two fundamental linear constraints, we enable the LLM to perform simplified logical checks $( \mathbf { e . g . } , x > x _ { c } \ \mathrm { o r } \ y < y _ { c } )$ more reliably. This provides the LLM with clear ”topological hints” to understand which regions are impassable without overwhelming its processing capacity.

While this simplified representation does not capture every geometric nuance of an irregular obstacle, it is sufficient for the LLM’s role as a high-level strategic planner. The inherent loss of detail is strategically compensated for in the subsequent VLM refinement stage. Unlike the LLM, the VLM operates on the original, un-abstracted map M, where it perceives the precise boundaries of all barriers. The VLM refines the high-level waypoints generated by the LLM to ensure they are collision-free relative to the true obstacle geometry. This hierarchical division of labor allows the LLM to focus on global path topology while the VLM handles local geometric precision and safety assurance.

## B Prompts in LLMs

This appendix outlines the prompting techniques used in our MMP-A\* algorithm to generate paths between start and goal points while navigating around obstacles. We employed different prompting strategies to evaluate their effectiveness in guiding the model. Below are the details of each technique along with the templates used.

## B.1 Standard 5-Shot Demonstration

In the standard 5-shot demonstration in Table 6, the model is provided with five examples (or demonstrations) to guide the generation of the path. Each example includes start and goal points, along with horizontal and vertical barriers. The model is prompted to generate a path by following the pattern observed in the examples.

## B.2 Chain of Thought (CoT) Prompting

The chain of thought prompting technique in Table 7 provides a sequence of reasoning steps that the model follows to arrive at the final path. This technique includes a detailed thought process and evaluation for each step, helping the model to understand the rationale behind the path generation.

## B.3 Recursive Path Evaluation (RePE)

In the recursive path evaluation technique shown Table 8, the model iteratively evaluates the path at each step and makes decisions based on previous iterations. This process involves selecting points, evaluating their effectiveness, and adjusting the path as necessary to avoid obstacles and reach the goal.

## C Prompt in VLM

This appendix outlines the visual–language prompting strategy employed in our MMP-A\* framework to evaluate the spatial validity of LLM-generated waypoints. While the LLM module proposes candidate checkpoints in textual form, the VLM serves as a perception-based verifier that inspects corresponding maze images to filter out invalid, wall-touching, or redundant waypoints. This process ensures that only geometrically feasible and visually consistent landmarks remain before the A\* search begins, thereby improving path reliability and reducing unnecessary node expansions.

Specifically, the VLM receives two paired images: the first is a clean map with start and goal points, and the second contains the same map annotated with candidate waypoints along a suggested blue route. The prompt, shown in Table 9, instructs the model to reason over the obstacle layout, assess visibility and clearance, and output a structured JSON object that lists only the selected waypoints to keep.

## D Details of Dataset Construction

The dataset for A\* path planning is generated using a custom Python script, leveraging several key packages for randomization, geometric manipulation, visualization, and data management. The process involves the following steps:

1. Initialization: The script initializes with specified map dimensions (x and y boundaries) and parameters (number of barriers and obstacles) for the number of unique environments and start-goal pairs.

2. Environment Creation: For each map configuration, do the following:

• Random obstacles, horizontal barriers, and vertical barriers are generated within defined x and y ranges. For irregular barriers, we manually designed non-standard geometries by delineating their boundaries with dashed, semi-transparent red contours. A reference grid was then superimposed over these shapes to precisely determine their centroids $( x _ { c } , y _ { c } )$ This manual annotation process ensures that each irregular obstacle is accurately mapped to its simplified symbolic representation, providing a consistent ground truth for the LLM’s axis-aligned orthogonal segment approximation.

![](Ha2026MMPA_figs/9e776fae5b1f7d660ee18b7fc90e774e65401fe6cabb3ce5cb8f24ad07a2c750.jpg)

![](Ha2026MMPA_figs/7b624c93f384f5b94c020369141166481b778fdcc55581178f76509794aaca4d.jpg)

![](Ha2026MMPA_figs/d7d1f337f72f987ecd58c2a7833156496fff15069e847632fbbf030c0c56f026.jpg)

Figure 5: Comparison of symbolic representation strategies for irregular obstacles. From left to right: raw geometric data of an impassable barrier $B \in S _ { o b s } ;$ our proposed skeletonized representation using axis-aligned segments for a constant token footprint and efficient LLM reasoning; and conventional boundary-based encoding which suffers from token explosion and high spatial noise.  
![](Ha2026MMPA_figs/a05e9e17f15abb94cfce8805c1ef9c279ac9bcd42c627065c3658943fc990262.jpg)  
Table 6: The template of the prompt used for MMP-A\* with 5-shot demonstration.

• Start and goal points are randomly placed on the map, ensuring they do not intersect with any obstacles. Valid pairs form non-intersecting line segments.

3. Data Storage: The generated environments, including the obstacles and start-goal pairs, are stored in JSON format.

4. Query Generation: Natural language queries are appended to each start-goal pair. These queries describe the task of finding a path that avoids the obstacles, which is supported as text input for LLMs.

5. Visualization: The environments are visualized using matplotlib, displaying the grid, obstacles, and paths. The plots are supported to be saved as image files for reference and stream in a show..

To systematically evaluate both scalability and environmental complexity, we constructed a hierarchical dataset divided into five levels of difficulty, as shown in Fig 7. Each level corresponds to a distinct grid resolution and barrier configuration, enabling progressive testing of MMP-A\* under increasing spatial and structural challenges.

Scalability setup. The environment sizes range from small 30×50 maps in Level 1 up to large 240×400 maps in Level 5. For each level, we proportionally scale the map dimensions while preserving the relative topology of obstacles and corridors. This ensures that the navigational patterns remain consistent across scales, allowing controlled analysis of algorithmic efficiency and memory growth as problem size increases.

Complexity setup. The structural complexity is defined by the number and arrangement of barrier columns and rows. The benchmark Level 5 map contains approximately twelve primary obstacles (both horizontal and vertical), forming multiple intertwined corridors and dead-end traps. Lower levels progressively reduce the number of barriers by 2–3 per level, producing simpler configurations while maintaining the same relative spatial layout. This hierarchical design creates a smooth transition from sparse to cluttered environments, enabling evaluation of robustness, operation ratio, and path validity across a controlled complexity spectrum.

```txt
Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end]. Conclude your response with the generated path in the format “Generated Path: [[x1, y1], [x2, y2], ...]”.  
Start Point: [5, 5]  
Goal Point: [20, 20]  
Horizontal Barriers: [[10, 0, 25], [15, 30, 50]]  
Vertical Barriers: [[25, 10, 22]]  
Thought: Identify a path from [5, 5] to [20, 20] while avoiding the horizontal barrier at y=10 spanning x=0 to x=25 by moving upwards and right, then bypass the vertical barrier at x=25 spanning y=10 to y=22, and finally move directly to [20, 20].  
Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]]  
[3 in-context demonstrations abbreviated]  
Start Point: {start}  
Goal Point: {goal}  
Horizontal Barriers: {horizontal_barriers}  
Vertical Barriers: {vertical_barriers}  
Generated Path: Model Generated Answer Goes Here
```

Table 7: Prompt template for MMP-A\* using 3-shot Chain-of-Thought (CoT) reasoning.  
![](Ha2026MMPA_figs/1da243bd3676da1d5f7d3316a9dc0a2773bccff53cbdd5703a32c825dc19740b.jpg)  
Figure 6: Runtime Performance Trade-Off Between LLM-A\* and MMP-A\*. As environment complexity and map resolution increase, MMP-A\* not only sustains superior optimality rates but also exhibits a decreasing runtime trend, becoming comparable to and even surpassing the runtime of classical A\* at the highest complexity and resolution levels.

Such construction allows the dataset to simultaneously stress-test both computational scalability and topological reasoning. In particular, Level 5 serves as the canonical benchmark environment, capturing the full navigational difficulty expected in real-world cluttered maps.

## E Comparative Efficiency of LLM–VLM Models and Limitation

Although MMP-A\* consistently enhances efficiency and stability, its overall performance remains sensitive to the intrinsic reasoning capability of the underlying language model. As shown in Figure 9, configurations using QWEN as the LLM consistently exhibit the weakest results across all metrics, including the highest operation and memory ratios. This is primarily because Qwen often generates misleading or dead-end waypoints that terminate within narrow or blocked corridors. Once these erroneous checkpoints are provided, the accompanying VLM cannot fully recover, the visual module can only validate or prune existing candidates, not generate alternative waypoints, thus propagating early errors through the search process.

```txt
Identify a path between the start and goal points to navigate around obstacles and find the shortest path to the goal. Horizontal barriers are represented as [y, x_start, x_end], and vertical barriers are represented as [x, y_start, y_end]. Conclude your response with the generated path in the format “Generated Path: [[x1, y1], [x2, y2], ...]”. Start Point: [5, 5] Goal Point: [20, 20] Horizontal Barriers: [[10, 0, 25], [15, 30, 50]] Vertical Barriers: [[25, 10, 22]] - First Iteration on [5, 5] Thought: The horizontal barrier at y=10 spanning x=0 to x=25 blocks the direct path. Move to the upper-right corner of the barrier. Selected Point: [26, 9] Evaluation: The point [26, 9] bypasses the horizontal barrier efficiently. - Second Iteration on [26, 9] Thought: The vertical barrier at x=25 blocks direct motion to [20, 20]; move around it. Selected Point: [25, 23] Evaluation: The new point successfully avoids the barrier. - Third Iteration on [25, 23] Thought: No further obstacles to the goal. Selected Point: [20, 20] Generated Path: [[5, 5], [26, 9], [25, 23], [20, 20]] [3 in-context demonstrations abbreviated] Start Point: {start} Goal Point: {goal} Horizontal Barriers: {horizontal_barriers} Vertical Barriers: {vertical_barriers} Generated Path: Model Generated Answer Goes Here
```  
Table 8: Prompt template for MMP-A\* using 3-shot Recursive Path Evaluation (RePE) reasoning.

This limitation arises not from perceptual failure of the VLM but from the upstream linguistic bias of the LLM, which shapes the initial search manifold. The effectiveness of MMP-A\* therefore depends on the LLM’s ability to propose spatially coherent and semantically meaningful waypoint candidates, allowing the VLM to refine rather than rescue the trajectory.

## F Runtime Performance Trade-Off Analysis

Figure 11 compares the runtime and operation performance of LLM-A\* and MMP-A\* across two settings: Complex Environment (GPT-4o-mini + Qwen-VL) and Scale Robustness (GPT-4o-mini + Gemma).

As resolution and complexity increase, LLM-A\* becomes progressively slower, primarily because it generates redundant or poorly aligned waypoints; these noisy suggestions misguide the search, inflate the A\* exploration space, and cause the number of expansions to grow disproportionately with map difficulty. In contrast, MMP-A\* exploits structured waypoint reasoning and multimodal filtering to impose a coherent global guidance signal, pruning large portions of the search space and enabling its runtime to converge toward, and at higher difficulty levels even surpass the baseline runtime of classical A\*. Although MMP-A\* incurs a small overhead on simple, low-resolution maps due to LLM/VLM calls, this cost is effectively amortized in complex and large-scale environments, where guided reasoning sharply compresses the search space. This trend aligns well with real-world robotic navigation, where maps are typically high-resolution and structurally complex, making MMP-A\* a practically attractive choice that reconciles multimodal reasoning with stringent runtime constraints.

<table><tr><td>You are presented with two visual representations of the same maze environment. The obstacles are defined by two distinct visual cues: standard black grid walls and irregular red regions delineated by dashed contours:1. First image: Shows the clean map with start point (blue square) and goal point (green square).2. Second image: Shows the same map with num-waypoints waypoints (yellow stars) placed along a blue path.Waypoints are indexed 1..num-waypoints; goal is id num-waypoints + 1.What is a ”waypoint” and its role (read carefully):A waypoint (yellow star) is a navigation landmark, a coarse checkpoint placed in clearly open space that helps the robot orient its heading and follow a feasible route.It is NOT a precise docking coordinate. Waypoints indicate:- Turning points (where the robot must change direction)- Corridor transitions (entering or leaving a corridor)- Decision junctions (where multiple passages meet)A valid waypoint MUST be centered in open space with visible clearance from walls. Waypoints in dead-ends, touching/near walls, or inside narrow squeezes are invalid and must be discarded.Because the robot travels in straight-line segments between consecutive waypoints, every such segment in the final path must be visibly open and free of contact with barriers.Important:The second image (with yellow stars) is onlya suggested route, it is NOT guaranteed to be a valid robot path. You must infer safety from the barrier layout (do not assume the blue path is correct).IMPORTANT RULES:This is for a physical robot. The robot cannot touch, graze, or squeeze between walls. Be conservative: if a straight segment is ambiguous or appears to touch walls, treat it as blocked.Do NOT create any new waypoints. Choose only from the existing numbered candidate waypoints shown in the second image. Do NOT output internal chain-of-thought. Output only the structured JSON described below using factual, image-tied statements.</td></tr><tr><td>TASK (two stages, output combined):First, inspect the clean map (first image) globally and identify which corridors or directions from start toward goal are visibly open or blocked.Then, using that global view, evaluate each original waypoint in order and decide whether it is essential as a navigation marker:Keep a waypoint if it lies in open space and is necessary as a turning point, corridor transition, or decision marker so that start → selected-waypoint-1 → ... → goal can be realized by clearly open straight segments.Discard a waypoint if it lies in a blocked, narrow, redundant, or dead-end location that would force the robot into unsafe or blocked segments.</td></tr><tr><td>OUTPUT (strict JSON only; nothing else):“selected-waypoints”: [ list of integer waypoint IDs to KEEP in traversal order, e.g. [2, 5] ], must contain only integers between 1 and num-waypoints. If no original waypoint is needed, return an empty list.“final-reasoning”: “(a) explicitly describe the overall feasible route(s) observed on the clean map before considering waypoints, and (b) explain for each chosen waypoint why it is necessary and for discarded waypoints why they were removed. Keep statements factual and tied to visible barriers/corridors, must be factual and image-referential”</td></tr></table>

Table 9: Prompt template used in MMP-A\* for filtering spatially valid waypoints from paired maze images.

<table><tr><td>Methodology</td><td>Base Model</td><td>Prompt Approach</td><td>Operation Ratio ↓ (%)</td><td>Storage Ratio ↓ (%)</td><td>Relative Path Length ↓ (%)</td></tr><tr><td>A*</td><td>-</td><td>-</td><td>100</td><td>100</td><td>100</td></tr><tr><td rowspan="12">LLM-A*</td><td rowspan="3">DeepSeek-V3</td><td>Few-Shot</td><td>109.6</td><td>93.5</td><td>103.1</td></tr><tr><td>CoT</td><td>131.6</td><td>106.6</td><td>102.7</td></tr><tr><td>RePE</td><td>125.2</td><td>114.6</td><td>103.4</td></tr><tr><td rowspan="3">Llama-3.3-70B</td><td>Few-Shot</td><td>100.0</td><td>94.9</td><td>103.2</td></tr><tr><td>CoT</td><td>110.2</td><td>102.5</td><td>102.7</td></tr><tr><td>RePE</td><td>112.1</td><td>103.1</td><td>103.3</td></tr><tr><td rowspan="3">Qwen2.5-7B</td><td>Few-Shot</td><td>173.7</td><td>133.5</td><td>103.0</td></tr><tr><td>CoT</td><td>144.4</td><td>106.3</td><td>104.0</td></tr><tr><td>RePE</td><td>191.6</td><td>141.4</td><td>102.5</td></tr><tr><td rowspan="3">GPT-4o-mini</td><td>Few-Shot</td><td>127.1</td><td>119.7</td><td>103.1</td></tr><tr><td>CoT</td><td>117.7</td><td>105.1</td><td>103.2</td></tr><tr><td>RePE</td><td>115.3</td><td>104.6</td><td>103.5</td></tr><tr><td rowspan="12">MMP-A*</td><td rowspan="3">DeepSeek-V3 + Gemma-3n-E4B</td><td>Few-Shot</td><td>73.0</td><td>72.6</td><td>102.2</td></tr><tr><td>CoT</td><td>79.5</td><td>77.0</td><td>102.4</td></tr><tr><td>RePE</td><td>91.1</td><td>86.0</td><td>101.9</td></tr><tr><td rowspan="3">Llama-3.3-70B + Gemma-3n-E4B</td><td>Few-Shot</td><td>72.4</td><td>71.7</td><td>102.1</td></tr><tr><td>CoT</td><td>91.4</td><td>85.9</td><td>101.8</td></tr><tr><td>RePE</td><td>88.5</td><td>81.5</td><td>102.0</td></tr><tr><td rowspan="3">Qwen2.5-7B + Gemma-3n-E4B</td><td>Few-Shot</td><td>137.6</td><td>102.2</td><td>102.2</td></tr><tr><td>CoT</td><td>111.0</td><td>91.3</td><td>102.8</td></tr><tr><td>RePE</td><td>150.4</td><td>106.3</td><td>101.9</td></tr><tr><td rowspan="3">GPT-4o-mini + Gemma-3n-E4B</td><td>Few-Shot</td><td>93.2</td><td>86.4</td><td>101.5</td></tr><tr><td>CoT</td><td>89.5</td><td>82.5</td><td>101.6</td></tr><tr><td>RePE</td><td>82.4</td><td>76.5</td><td>102.2</td></tr></table>

Table 10: Quantitative results of different prompting strategies under LLM-A\* and MMP-A\*. The few-shot, chain-of-thought (CoT), and recursive path evaluation (RePE) settings are compared across multiple base models.

<table><tr><td rowspan="2">Method</td><td rowspan="2">LLM</td><td rowspan="2">VLM</td><td colspan="3">Operation Ratio ↓</td><td colspan="3">Storage Ratio ↓</td><td colspan="3">Rel. Path Length ↓</td></tr><tr><td>w/ Adap.</td><td>w/o Adap.</td><td>Δ</td><td>w/ Adap.</td><td>w/o Adap.</td><td>Δ</td><td>w/ Adap.</td><td>w/o Adap.</td><td>Δ</td></tr><tr><td rowspan="4">LLM-A*</td><td>DeepSeek-V3</td><td>-</td><td>135.8</td><td>125.2</td><td>+10.6</td><td>118.6</td><td>114.6</td><td>+4.0</td><td>100.9</td><td>103.4</td><td>-2.5</td></tr><tr><td>Llama-3.3-70B</td><td>-</td><td>128.5</td><td>112.1</td><td>+16.4</td><td>112.9</td><td>103.1</td><td>+9.8</td><td>101.0</td><td>103.3</td><td>-2.3</td></tr><tr><td>Qwen2.5-7B</td><td>-</td><td>182.0</td><td>191.6</td><td>-9.6</td><td>133.9</td><td>141.4</td><td>-7.5</td><td>101.2</td><td>102.5</td><td>-1.3</td></tr><tr><td>GPT-4o-mini</td><td>-</td><td>136.0</td><td>115.3</td><td>+20.7</td><td>114.5</td><td>104.6</td><td>+9.9</td><td>100.9</td><td>103.5</td><td>-2.6</td></tr><tr><td rowspan="12">MMP-A*</td><td rowspan="3">DeepSeek-V3</td><td>Gemma-3n-E4B</td><td>91.1</td><td>82.3</td><td>+8.8</td><td>86.0</td><td>81.0</td><td>+5.0</td><td>101.9</td><td>103.9</td><td>-2.0</td></tr><tr><td>Llama 4 Maverick</td><td>93.9</td><td>84.8</td><td>+9.1</td><td>87.8</td><td>82.0</td><td>+5.8</td><td>101.6</td><td>103.9</td><td>-2.3</td></tr><tr><td>Qwen2.5-VL</td><td>84.9</td><td>78.7</td><td>+6.2</td><td>80.6</td><td>76.9</td><td>+3.7</td><td>102.2</td><td>103.6</td><td>-1.4</td></tr><tr><td rowspan="3">Llama-3.3-70B</td><td>Gemma-3n-E4B</td><td>88.5</td><td>78.8</td><td>+9.7</td><td>81.5</td><td>75.9</td><td>+5.6</td><td>102.0</td><td>103.6</td><td>-1.6</td></tr><tr><td>Llama 4 Maverick</td><td>97.0</td><td>86.1</td><td>+10.9</td><td>91.0</td><td>83.6</td><td>+7.4</td><td>101.8</td><td>103.6</td><td>-1.8</td></tr><tr><td>Qwen2.5-VL</td><td>81.0</td><td>72.2</td><td>+8.8</td><td>76.0</td><td>70.7</td><td>+5.3</td><td>102.3</td><td>104.1</td><td>-1.8</td></tr><tr><td rowspan="3">Qwen2.5-7B</td><td>Gemma-3n-E4B</td><td>150.4</td><td>141.3</td><td>+9.1</td><td>106.3</td><td>103.7</td><td>+2.6</td><td>101.9</td><td>103.4</td><td>-1.5</td></tr><tr><td>Llama 4 Maverick</td><td>181.0</td><td>177.4</td><td>+3.6</td><td>129.8</td><td>128.3</td><td>+1.5</td><td>101.5</td><td>102.9</td><td>-1.4</td></tr><tr><td>Qwen2.5-VL</td><td>162.8</td><td>156.4</td><td>+6.4</td><td>114.8</td><td>111.9</td><td>+2.9</td><td>102.2</td><td>103.7</td><td>-1.5</td></tr><tr><td rowspan="3">GPT-4o-mini</td><td>Gemma-3n-E4B</td><td>82.4</td><td>70.6</td><td>+11.8</td><td>76.5</td><td>69.3</td><td>+7.2</td><td>102.2</td><td>104.4</td><td>-2.2</td></tr><tr><td>Llama 4 Maverick</td><td>97.4</td><td>87.0</td><td>+10.4</td><td>88.3</td><td>82.6</td><td>+5.7</td><td>101.6</td><td>103.9</td><td>-2.3</td></tr><tr><td>Qwen2.5-VL</td><td>81.0</td><td>74.1</td><td>+6.9</td><td>76.4</td><td>72.5</td><td>+3.9</td><td>102.3</td><td>103.7</td><td>-1.4</td></tr></table>

Table 11: Comparison of LLM-A\* and MMP-A\* with and without adaptive decay across LLM–VLM pairs.

![](Ha2026MMPA_figs/90d7ab82cff714b12a0b3ef2cf142e4435046471cf72a6b64152e0ccbe16d949.jpg)  
Figure 7: Hierarchical maze dataset for evaluating scalability and complexity in MMP-A\*. Map sizes increase from 30 × 50 to $2 4 0 \times 4 0 0$ , while barrier count rises from sparse layouts to ∼12 obstacles in Level 5. Each level preserves the relative spatial structure, enabling controlled analysis from simple to highly cluttered environments.

![](Ha2026MMPA_figs/32be31edb0438f72974e451bb32d14f64a329ad46fa0665d266ea4ab3f8bf434.jpg)

![](Ha2026MMPA_figs/ae0199ad48b9326becd1503211a39d05b96fe2b44d910af14c5924ef58e56782.jpg)

![](Ha2026MMPA_figs/fc21ab170e473f54ba93c0ec15bb3f72906eaf9d0c7046a4afde6affbd93f12f.jpg)

![](Ha2026MMPA_figs/e02a613f795dfe90e413ba1854febc574b7385d6f626fc365e94dea2c5f6af1f.jpg)

![](Ha2026MMPA_figs/2cf72f709e5b346f51af0c3cb90869fc39c0c2315be4436e9b66826b4829b77b.jpg)

![](Ha2026MMPA_figs/abe039a401f5e6a51138582ede01f1204e6ac2cf7690af0ac6eadbfa17ce0a77.jpg)

![](Ha2026MMPA_figs/80c7a220b6b32a6a998748084df5b7c063c5cecb4c2c547fb90c8a9bc1ac87c4.jpg)

![](Ha2026MMPA_figs/4870425e286a21ece563b211fece0181dceb596eac4b6abf620284abb2f6f0cf.jpg)

![](Ha2026MMPA_figs/d7225d2a40ac39ff4476a39b80db8894f7eb510782419ae1b1c151186be4e4d6.jpg)

![](Ha2026MMPA_figs/d63c76aff525a981b28ea4f91e540f03beab89d855d43383ebeb51604d39c75c.jpg)

![](Ha2026MMPA_figs/7edd95b47651b7164faf9792f5b5eda1a75a5616b247cdd4f97c1e7b15eb1146.jpg)

![](Ha2026MMPA_figs/5fc9ebd8f7990090b3acb141aa85056de763b14ab719a673b2361c1869238892.jpg)  
Figure 8: Visual comparison of search behaviors across different planners. LLM-A\* suffers from redundant expansions due to unreliable waypoint guidance, while MMP-A\* refines these checkpoints through visual filtering and adaptive decay, achieving smoother, obstacle-aware trajectories with the fewest search operations and balanced efficiency–optimality trade-off.

![](Ha2026MMPA_figs/3f21df0c23382700327cd5537bb4fbd14fccb19dc5437a3bd9a97b425506352a.jpg)

![](Ha2026MMPA_figs/4b8fac2686a91a0c599b4aa9db355f7fa7b7e9138e4f1eb56bc6ec1a249f9fd1.jpg)

![](Ha2026MMPA_figs/58718bf2920e4b9940c2de884096bf38cfc688a0337480f18f80e414cc970193.jpg)  
Figure 9: Comparative Efficiency of LLM–VLM Models Across Operations, Memory, and Path Quality

![](Ha2026MMPA_figs/ee998942e36595df7c49d2aad19e3d75d1bc993429550b7aa9f32a323519de9f.jpg)  
Figure 10: Comparative Efficiency of LLM–VLM Models Across Operations, Memory, and Path Quality

![](Ha2026MMPA_figs/ccc5bc1d3ead3c9e8f72d7d20bde3b9823ac7f4d61ff9a06b845ea268684d0cc.jpg)

![](Ha2026MMPA_figs/1ae0b0b29f30b0dca3a33214bdbe91e7af19d7bce1c95cadd8c261707f50a6ea.jpg)  
Figure 11: Runtime Performance Trade-Off Between $\mathbf { L L M { \cdot } } \mathbf { A } ^ { \ast }$ and $\mathbf { M } \mathbf { M } \mathbf { P } { \cdot } \mathbf { A } ^ { * } ,$ . As environment complexity and map resolution increase, MMP-A\* not only sustains superior optimality rates but also exhibits a decreasing runtime trend, becoming comparable to and even surpassing the runtime of classical $\mathbf { A } ^ { * }$ at the highest complexity and resolution levels.