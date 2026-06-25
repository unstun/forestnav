---
citation_key: Kyaw2024Greedy
arxiv_id: 2405.03411
arxiv_url: "https://arxiv.org/abs/2405.03411"
title: "Greedy Heuristics for Sampling-Based Motion Planning in High-Dimensional State Spaces"
authors_short: "Phone Thiha Kyaw et al."
year: 2024
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:23:35Z
origin: ai+web
reviewed: false
---

# Greedy Heuristics for Sampling-Based Motion Planning in High-Dimensional State Spaces

Phone Thiha Kyaw <sup>1\*</sup>, Anh Vu Le <sup>2</sup>, Rajesh Elara Mohan <sup>3</sup>, Jonathan Kelly

<sup>1</sup>Space & Terrestrial Autonomous Robotic Systems (STARS) Laboratory, University of Toronto Institute for Aerospace Studies, 4925 Duferin Sreet, Toronto, M3H 5T6, Ontario, Canada. <sup>2</sup>Advanced Intelligent Technology Research Group, Faculty of Electrical and Electronics Engineering, Ton Duc Thang University, Ho Chi Minh City, 700000, Vietnam. <sup>3</sup>ROAR Lab, Engineering Product Development, Singapore University of Technology and Design, Singapore, 487372, Singapore.

\*Corresponding author(s). E-mail(s): phone.thiha@robotics.utias.utoronto.ca; Contributing authors: leanhvu@tdtu.edu.vn; rajeshelara@sutd.edu.sg; jonathan.kelly@robotics.utias.utoronto.ca;

## Abstract

Informed sampling techniques accelerate the convergence of sampling-based motion planners by biasing sam pling toward regions of the state space that are most likely to yield better solutions. However, when the current solution path contains redundant or tortuous segments, the resulting informed subset may remain unneces sarily large, slowing convergence. Our prior work addressed this issue by introducing the greedy informed set, which reduces the sampling region based on the maximum heuristic cost along the current solution path. In this article, we formally characterize the behavior of the greedy informed set within Rapidly-exploring Random Tree (RRT\*)-like planners and analyze how greedy sampling afects exploration and asymptotic opti mality. We then present Greedy RRT\* (G-RRT\*), a bi-directional anytime variant of RRT\* that leverages the greedy informed set to focus sampling in the most promising regions of the search space. Experiments on abstract planning benchmarks, manipulation tasks from the MotionBenchMaker dataset, and a dual-arm Barrett WAM problem demonstrate that G-RRT\* rapidly finds initial solutions and converges asymptotically to optimal paths, outperforming state-of-the-art sampling-based planners.

Keywords: Sampling-based motion planning, optimal path planning, informed sampling, bidirectional search, greedy heuristics, high-dimensional planning

## 1 Introduction

Path planning is the problem of finding a collisionfree path from an initial state to a goal state while also considering specific optimization objectives, such as minimizing path length or energy use, for example (LaValle 2006). Many planning algorithms exist, including graph search, artificial potential fields, and sampling-based methods (Elbanhawi and Simic 2014). However, it remains challenging to find collision-free, optimal paths, especially in high-dimensional state spaces; the general path planning problem is known to be PSPACE-hard (Reif 1979).

Sampling-based planners, such as the probabilistic roadmap (Kavraki et al. 1996, PRM) and rapidlyexploring random tree (LaValle and Kufner Jr 2001, RRT) algorithms, tackle the complexity of highdimensional path planning by sacrificing completeness for eficiency, providing only probabilistic guarantees. The asymptotically optimal variants PRM\* and RRT\* (Karaman and Frazzoli 2011) improve solution quality over time but remain computationally expensive due to their reliance on random sampling. A substantial portion of the computational efort is often wasted exploring irrelevant portions of the state space. To improve planning performance, it is crucial to focus sampling on promising regions of the problem domain.

Existing direct informed sampling methods (Gammell et al. 2014, 2018) mitigate ineficiency by defining bounded, hyperellipsoidal sampling regions, called informed sets, based on the cost of the current solution. While this significantly reduces the size of the search space, initial feasible solutions are often highly tortuous, containing many redundant states— intermediate states that can be removed through standard path-shortening techniques without afecting feasibility. Such redundant states increase the solution cost and enlarge the informed set unnecessarily, reducing the likelihood of finding states that may be part of a better solution. To address this shortcoming, Kyaw et al. (2022) introduced a new direct informed sampling procedure that biases sampling based on heuristic information from the states that are part of the current solution, independent of their cost. These states are used to define an alternative greedy informed set that reduces the size of the informed sampling hyperellipsoid, improving both the eficiency and the convergence rate of planning. Although the greedy informed set concept was introduced in (Kyaw et al. 2022), no analysis of its properties was carried out.

![](Kyaw2024Greedy_figs/4662b794d40f710439f0b61086a5f169895a5b0f4229da0f392eac31994ce3f4.jpg)  
Fig. 1: Comparison of informed set sizes for a planning problem with a tortuous solution path (yellow) from the start (red) to the goal (green). The L<sup>2</sup> informed set (left) is defined by the current solution cost and covers a large ellipsoidal region. In contrast, the L<sup>2</sup> greedy informed set (right) is defined using the state with the maximum admissible heuristic along the current solution path, substantially reducing the ellipsoidal area.

Informed sets are only useful to reduce the size of the search space once an initial solution has been found, making rapid discovery of a feasible path crucial for overall planning eficiency. A key contribution of this work is a formal analysis of the performance and trade-ofs associated with the greedy informed set. To accelerate the search for an initial solution, bidirectional planning can be employed. Algorithms such as RRT-Connect (Kufner and LaValle 2000) grow two trees—one from the start and one from the goal—that expand toward each other, guided by a connection heuristic. Building on this idea and incorporating the greedy informed set, we propose Greedy-RRT\* (G-RRT\*), a bidirectional, asymptotically optimal sampling-based planner. G-RRT\* rapidly identifies initial solutions and exploits the greedy informed set to enhance solution quality, particularly in highdimensional spaces. In summary, we make the following contributions herein.

• We provide a formal analysis of properties of the greedy informed set and consider how possible algorithmic choices influence planning performance.

• We present Greedy-RRT\* (G-RRT\*), a bidirectional, asymptotically optimal sampling-based planning algorithm that leverages the proposed greedy heuristic.<sup>1</sup>

• We prove the completeness and asymptotic optimality of G-RRT\*, building upon existing results from the sampling-based planning literature.

• We show experimentally that greedy exploitation in large planning domains improves success and convergence rates over state-of-the-art methods, using both simulations and manipulation datasets.

The article is organized as follows. Section 2 covers related literature, while Section 3 describes our notation and problem formulation. Section 4 defines the greedy informed set, while Section 5 details the G-RRT\* algorithm. Section 6 analyzes the properties of G-RRT\*. Section 7 demonstrates the performance of G-RRT\* in simulations and through manipulation experiments. The article concludes with some discussion in Section 8.

## 2 Related Work

This section first reviews the existing literature on sampling-based planning algorithms (Section 2.1), and then discusses methods for accelerating their conver gence (Section 2.2).

## 2.1 Sampling-Based Motion Planning

Sampling-based motion planners can be broadly classified into multiple-query and single-query categories. Multiple-query planners, such as probabilistic roadmaps (Kavraki et al. 1996; Hsu et al. 1998), construct a graph of collision-free paths that can be reused for diferent start-goal pairs. In contrast, single-query planners expand a tree toward randomly sampled states to solve individual planning prob lems; rapidly-exploring random trees (LaValle and Kufner Jr 2001) are a well-known example. These sampling-based approaches are often efective in high dimensional state spaces and reduce computation by avoiding explicit obstacle representations, unlike deterministic graph-search planners. However, they typically yield only feasible (collision-free) paths and do not guarantee optimality.

Karaman and Frazzoli (2011) introduced PRM\* and RRT\*, optimal variants of PRM and RRT that guarantee asymptotic optimality. RRT\* expands a tree into free space through random sampling, but unlike RRT, it considers nearby vertices to select the best parent and incrementally rewires them to improve path quality. This rewiring enables RRT\* to converge asymptotically to the optimal solution, a key property in sampling-based motion planning.

The RRT<sup>#</sup> algorithm (Arslan and Tsiotras 2013) extends the local rewiring of RRT\* to the global level using dynamic programming, accelerating convergence by removing states that cannot improve the current solution. Karaman et al. (2011) proposed a branch-and-bound pruning scheme that deletes ver tices whose cost-to-come plus a lower bound on the cost-to-go exceeds the cost of the current best path. This pruning step eliminates vertices that are unlikely to contribute to better solutions and enhances realtime performance. Quick-RRT\* (Jeong et al. 2019) refines parent selection and rewiring by also considering ancestors of nearby vertices, up to a user-defined depth, as candidate parents. Similarly, F-RRT\* (Liao et al. 2021) enhances initial path quality and convergence by generating random parent vertices close to obstacles.

Various extensions have been proposed to accelerate the convergence of $\mathrm { R R T ^ { * } }$ , including bi-directional variants (Kufner and LaValle 2000; Klemm et al. 2015) and methods that relax optimality to nearoptimality (Dobson and Bekris 2014; Salzman and Halperin 2016). Our proposed approach similarly employs bi-directional search to rapidly generate initial solutions. However, because these methods sample uniformly across the entire state space, their convergence slows markedly in high-dimensional problems, increasing the computational efort required to find optimal solutions.

## 2.2 State Space Sampling Methods

Prior work on sampling-based planning has emphasized ways to improve the sampling process. While uniform sampling preserves global optimality, performance can often be improved by biasing samples toward regions more likely to yield better solutions. For example, Bialkowski et al. (2013) proposed a biased sampling method that records past collisions to direct future samples away from obstacles. Similarly, Kim et al. (2014) used a generalized Voronoi graph to decompose free space into spheres of varying radii, forming a dynamic sampling ‘cloud’ that evolves as the best solution is refined.

In $\mathrm { P - R R T ^ { * } }$ and $\mathrm { P Q - R R T ^ { * } }$ (Qureshi and Ayaz 2016; Li et al. 2020), random sampling is guided by artificial potential fields towards more promising state space regions (Khatib 1986), trading of exploration for exploitation. Compared with traditional rejection sampling, these free-space-biased methods quickly find improved paths and reduce the number of rejected samples, but they continue to draw samples that do not improve the current solution.

Several extensions of RRT\* have been developed to accelerate convergence. Akgun and Stilman (2011) introduced a bi-directional version of RRT\* that uses path-biased sampling and heuristic sample rejection for high-dimensional problems. Related work (Islam et al. 2012; Alterovitz et al. 2011; Faroni et al. 2024) applies similar path-biasing and refinement ideas, achieving faster convergence but often favouring locally optimal solutions over globally better ones. Techniques like rectangular rejection sampling (Ferguson and Stentz 2006; Otte and Correll 2013) can improve convergence, but their efectiveness decreases as dimensionality increases.

To address this scalability issue, Gammell et al. (2014, 2018) proposed informed sampling, implemented in Informed $\mathrm { R R T ^ { * } }$ . Once a feasible path is found, the algorithm samples only within an ndimensional hyperellipsoid—called the $L ^ { 2 }$ informed set—bounded by the current solution cost, which shrinks as better solutions are found.

Although informed sampling is highly efective, early feasible paths often include redundant states, producing tortuous trajectories with many unnecessary twists and turns. These paths can yield overly large informed sets, which slow convergence, particularly in high-dimensional state spaces. Consequently, later studies (Kim and Song 2015; Jiang et al. 2020; Wilson et al. 2025) integrated path simplification and anytime refinement to tighten the informed set and improve solution quality, achieving state-of-the-art results on the Motion Bench Maker dataset (Chamzas et al. 2021). We pursue a diferent strategy: leveraging the greedy heuristic proposed in (Kyaw et al. 2022) within a bi-directional framework to prioritize sampling in regions most likely to yield improvement. By coupling greedy state-space biasing with eficient tree growth, our method accelerates convergence without sacrificing global solution optimality.

## 3 Preliminaries

We begin by defining the notation used throughout the paper and introducing key planning concepts in Section 3.1. Section 3.2 then reviews the formal definitions of the feasible and optimal path-planning problems, providing a foundation for our analysis of the G-RRT\* algorithm.

## 3.1 Notation

Let the state space of a path planning problem be denoted by $\mathcal { X } \subseteq \mathbb { R } ^ { n }$ , and let $\mathbf { x } \in \mathcal { X }$ denote a single state. Let $\mathcal { X } _ { \mathrm { o b s } } \subset \mathcal { X }$ be the set of states in collision with obstacles, and let $\chi _ { \mathrm { f r e e } } = \chi \setminus \chi _ { \mathrm { o b s } }$ be the set of collision-free states. A path is a continuous function $\pi : [ 0 , 1 ] \to \mathcal { X } .$ , and we denote by Σ the set of all such paths. The initial and goal states are denoted by $\mathbf { x } _ { I } \in \mathcal { X } _ { \mathrm { f r e e } }$ and $\mathbf { x } _ { G } \in \mathcal { X } _ { \mathrm { f r e e } }$ , respectively. Each planning problem is associated with a cost function $c : \Sigma $ $\mathbb { R } { \geq } 0$ that maps a path to a non-negative real value. Herein, we define the cost of a path as its length under the standard Euclidean metric on <sup>Rn</sup>.

As is standard in sampling-based motion planning, we represent paths using graphs and, in particular, restrict our attention to trees, which are directed acyclic graphs. A tree is incrementally constructed by connecting states through feasible transitions that respect collision constraints. Let $\tau = ( V , E )$ denote such a tree, where V is a set of vertices and $E \subseteq V \times V$ is a set of directed edges. Each vertex corresponds to a state $\mathbf { x } \in \mathcal { X }$ , and each edge $\left( \mathbf { x } _ { a } , \mathbf { x } _ { b } \right) \in E$ represents a valid (collision-free) transition from $\mathbf { x } _ { a }$ to x<sub>b</sub>.

With a slight abuse of notation, let $c ( \mathbf { x } _ { a } , \mathbf { x } _ { b } )$ denote the cost of the path between two vertices $\mathbf { x } _ { a } , \mathbf { x } _ { b } \in \textit { V }$ in the tree . An admissible heuristic estimate of this cost is cˆ : $V \times V \to \mathbb { R } _ { \geq 0 }$ , which satisfies

$$
\forall \mathbf {x} _ {a}, \mathbf {x} _ {b} \in V, \quad \hat {c} (\mathbf {x} _ {a}, \mathbf {x} _ {b}) \leq c (\mathbf {x} _ {a}, \mathbf {x} _ {b}).\tag{1}
$$

The cost-to-come is $g ( \mathbf { x } ) = c ( \mathbf { x } _ { I } , \mathbf { x } )$ , representing the true cost of the optimal path from the initial vertex x to vertex x in the tree. Its admissible heuristic estimate is $\hat { g } ( \mathbf { x } ) \overset { } { = } \hat { c } ( \mathbf { x } _ { I } , \mathbf { x } )$ . Similarly, the cost-to-go is $h ( { \bf x } ) = c ( { \bf x } , { \bf x } _ { G } )$ , the true cost of the optimal path from vertex x to the goal vertex $\mathbf { x } _ { G }$ . Its admissible heuristic estimate is $\hat { h } ( \mathbf { x } ) = \hat { c } ( \mathbf { x } , \mathbf { x } _ { G } )$ . The total cost of the optimal path through x is $f ( \mathbf { x } ) = g ( \mathbf { x } ) + h ( \mathbf { x } )$ , and its admissible heuristic estimate is ${ \hat { f } } ( \mathbf { x } ) = { \hat { g } } ( \mathbf { x } ) + { \hat { h } } ( \mathbf { x } )$

## 3.2 Feasible and Optimal Path Planning

A planning problem instance is defined by the state space $\mathcal { X } _ { \mathrm { f r e e } } ,$ an initial state $\mathbf { x } _ { I } .$ , and a goal state $\mathbf { x } _ { G } .$ , typically expressed as a tuple $\left( \mathcal { X } _ { \mathrm { f r e e } } , \mathbf { x } _ { I } , \mathbf { x } _ { G } \right)$ . In general, two types of path planning problems may be considered: the feasible planning problem and the optimal planning problem. We define these below.

Definition 1 (Feasible path planning problem) Find a path $\pi ^ { \prime } \in \Sigma$ from $\mathbf { x } _ { I }$ to $\mathbf { x } _ { G }$ through collision-free space such that

$$
\begin{array}{r} \pi^ {\prime} \in \{\pi \in \Sigma | \pi (0) = \mathbf {x} _ {I}, \pi (1) = \mathbf {x} _ {G}, \\ \forall s \in [ 0, 1 ], \pi (s) \in \mathcal {X} _ {\mathrm{free}} \}. \end{array}\tag{2}
$$

There are usually many solutions to the feasible path planning problem.

Definition 2 (Optimal path planning problem) Find a feasible path $\pi ^ { * }$ from $\mathbf { x } _ { I }$ to $\mathbf { x } _ { G }$ through collision-free space that minimizes the cost functional $c : \Sigma  \mathbb { R } _ { > 0 } \colon$

$$
\begin{array}{r} \pi^ {*} = \underset {\pi \in \Sigma} {\arg \min} \{c (\pi) \mid \pi (0) = \mathbf {x} _ {I}, \pi (1) = \mathbf {x} _ {G}, \\ \forall s \in [ 0, 1 ], \pi (s) \in \mathcal {X} _ {\mathrm{free}} \}. \end{array}\tag{3}
$$

A path planning algorithm is considered robustly feasible if there exists a solution path with strong $\delta -$ clearance, that is, remaining at least a distance δ from any obstacle in $\mathbb { R } ^ { n }$ , for some $\delta > 0$ (Karaman and Frazzoli 2011). A solution path $\pi ^ { * }$ is robustly optimal if there exists another path $\pi _ { 0 }$ in the same homotopy class, also with strong δ-clearance, such that $c ( \pi _ { 0 } ) = \operatorname* { m i n } \{ c ( \pi ) \ |$ π is feasible . Notably, any formal guarantees provided by sampling-based algorithms are typically probabilistic in nature. An algorithm is probabilistically complete if the probability of finding a feasible path (when one exists) approaches one as the number of samples tends to infinity. It is almost-surely asymptotically optimal if the probability that the solution cost converges to the optimal cost approaches one as the number of samples tends to infinity. Asymptotic optimality implies probabilistic completeness. We refer interested readers to Karaman and Frazzoli (2011) for further details.

## 4 The Greedy Informed Set

Informed sampling-based planners focus the search on promising regions of the state space to find better paths once an initial solution has been found. These regions correspond to the omniscient set $\chi _ { f }$ the collection of states that could yield a better solution, which is generally unknown because computing it requires solving the problem exactly (Gammell et al. 2018). Heuristic-based estimates, such as the informed set $\boldsymbol { \mathcal { X } } _ { \hat { f } } .$ , are commonly used to approximate $\chi _ { f }$ . The informed set is an admissible over-approximation of the omniscient set, defining a subset of $\chi _ { \mathrm { f r e e } }$ where samples are likely to improve the current solution, provided the heuristic never overestimates the true cost. However, in problems with many homotopy classes or in high-dimensional spaces, the heuristic used in $\boldsymbol { \mathcal { X } } _ { \hat { f } }$ often provides very little information, resulting in an overly large informed set. Consequently, the probabil ity of drawing a random sample from $\mathcal { X } _ { \widehat { f } }$ that also belongs to $\chi _ { f }$ is low.

![](Kyaw2024Greedy_figs/97ecfb12452e7fdbb33c1f51f0c452dbaac8f5371d2eed5a08a1fc53300fb1a1.jpg)  
Fig. 2: Illustration of the $L ^ { 2 }$ greedy informed set $\boldsymbol { \mathcal { X } } _ { \mathrm { g r e e d y } }$ in a planning problem with a path-length objective in $\mathbb { R } ^ { 2 } .$ The greedy subset (dashed ellipse) is defined by the hypothetical minimum cost c<sub>min</sub> from the initial state x to the goal state x , and by the heuristic cost of the state along the solution path with the highest admissible value $\hat { f } ( \mathbf { x } _ { \mathrm { m a x } } )$ , used as a transverse diameter.

The greedy informed $s e t ,$ introduced by Kyaw et al. (2022), addresses this limitation by eliminating direct dependence on the current solution cost. Instead, it constructs a smaller hyperellipsoid from the states along the current solution path, which is bounded above by the admissible informed set. This section formally defines the greedy informed set and exam ines how heuristic exploitation in greedy informed sampling influences optimality. We consider only holo nomic planning problems in $\mathbb { R } ^ { n }$ with a path-length objective under the Euclidean norm $( { \mathrm { i . e . } }$ , where all degrees of freedom are directly controllable and the cost depends solely on geometric path length). For any state $\mathbf { x } \in \mathbb { R } ^ { n }$ , let $\hat { f } ( \mathbf { x } )$ denote the standard $L ^ { 2 }$ informed heuristic, which provides an admissible lower bound on the cost of any path from the initial state $\mathbf { x } _ { I }$ to the goal state $\mathbf { x } _ { G }$ passing through $\mathbf { x } ,$

$$
\hat {f} (\mathbf {x}) = \left\| \mathbf {x} - \mathbf {x} _ {I} \right\| _ {2} + \left\| \mathbf {x} - \mathbf {x} _ {G} \right\| _ {2}.\tag{4}
$$

Definition 3 $( L ^ { 2 }$ greedy informed set) Let $\mathbf { x } _ { \mathrm { m a x } }$ denote the state along the current solution path π with the maximum admissible heuristic cost, defined by ${ \hat { f } } ( \cdot )$ in (4),

$$
\mathbf {x} _ {\max} := \underset {\mathbf {x} \in \pi} {\arg \max} \Bigl \{\hat {f} (\mathbf {x}) \Bigr \}.\tag{5}
$$

The $L ^ { 2 }$ greedy informed set, $\chi _ { \mathrm { g r e e d y } } .$ , is the subset of collision-free states, $\chi _ { \mathrm { f r e e } } ,$ , consisting of all x whose heuristic costs are less than or equal to that of the greedily chosen state x<sub>max</sub> along the current solution path (Figure 2),

$$
\mathcal {X} _ {\mathrm{greedy}} = \Bigl \{\mathbf {x} \in \mathcal {X} _ {\mathrm{free}} \mid \hat {f} (\mathbf {x}) \leq \hat {f} (\mathbf {x} _ {\mathrm{max}}) \Bigr \}.\tag{6}
$$

The greedy informed set is bounded above by the informed set, i.e., $\mathcal X _ { \mathrm { g r e e d y } } \subseteq \mathcal X _ { \hat { f } } .$ , and consequently yields smaller ellipsoidal regions than the original informed set, especially in high-dimensional problems with complex solution paths. Consequently, sampling from this smaller subset increases the likelihood of finding states that also belong to the omniscient set. However, because the greedy informed set is constructed using knowledge from the current solution path—similar to path-biasing methods—an algorithm relying on it may in some cases bias the search toward locally optimal solutions, as the set might exclude portions of the omniscient set. Therefore, continued exploration of other homotopy classes, that is, sampling from the informed set, remains essential for planners utilizing the greedy informed set to preserve asymptotic optimality guarantees.

![](Kyaw2024Greedy_figs/b9e172704994e363e00551ae95e1b9b3afd4e3dc038be4c77076d8186d1010b7.jpg)  
Fig. 3: Illustration of the current solution path π and another path $\pi ^ { * }$ within the same homotopy class, sharing the same initial and goal states, x<sub>I</sub> and $\mathbf { x } _ { G }$ . The greedy informed set $\mathcal { X } _ { \mathrm { g r e e d y } }$ (dashed gray ellipse) is constructed using the maximum heuristic cost along π. The path $\pi ^ { * }$ intersects the boundary of $\mathcal { X } _ { \mathrm { g r e e d y } }$ at $\mathbf { x } _ { a }$ and x<sub>b</sub> and passes through a state $\mathbf { x } _ { c }$ that lies outside this set.

Sampling from informed sets is a necessary condition for asymptotic optimality in sampling-based motion planning, since states along the optimal path always lie within these sets (Gammell et al. 2018). The greedy informed set may also contain states from the optimal path, but only if the current solution path and the true optimal path belong to the same homotopy class. In the following, we draw on basic concepts from homotopy theory (Hatcher 2002) to establish the conditions under which an algorithm sampling from the greedy informed set can still converge to the optimal solution (Theorem 1), and to discuss cases where this property may fail to hold (Remark 1).

Theorem 1 (Inclusion of the optimal path in the greedy informed set) Let ${ \hat { f } } ( \cdot )$ be the $L ^ { \dot { 2 } }$ heuristic defined in $( 4 )$ Let π be the current solution path and $\pi ^ { * }$ the optimal path between the same initial and goal states x and $\mathbf { x } _ { G } , \ I f \ \pi$ and $\pi ^ { * }$ lie within the same homotopy class, then every state $\mathbf { x } ^ { * } \in \pi ^ { * }$ satisfies

$$
\hat {f} (\mathbf {x} ^ {*}) \leq \hat {f} (\mathbf {x} _ {\max}).\tag{7}
$$

Consequently, $\pi ^ { * } \subseteq { \mathcal { X } } _ { \mathrm { g r e e d y } } .$

Proof Consider the example shown in Figure 3. Let π denote the current solution path in $\mathcal { X } _ { \mathrm { f r e e } }$ from $\mathbf { x } _ { I }$ to $\mathbf { x } _ { G } ,$ and let $\mathbf { x } _ { a }$ and $\mathbf { x } _ { b }$ be two states along π with the same maximum heuristic cost, ${ \hat { f } } ( \mathbf { x } _ { a } ) = { \hat { f } } ( \mathbf { x } _ { b } ) = { \hat { f } } ( \mathbf { x } _ { \mathrm { m a x } } )$ . Let the path π be constructed such that every state $\mathbf { x } ^ { \prime }$ on the subpath between $\mathbf { x } _ { a }$ and $\mathbf { x } _ { b }$ also satisfies $\hat { f } ( \mathbf { x } ^ { \prime } ) = \hat { f } ( \mathbf { x } _ { \mathrm { m a x } } ) \colon$

$$
\forall \mathbf {x} ^ {\prime} \in \mathcal {Z}, \hat {f} (\mathbf {x} ^ {\prime}) = \hat {f} (\mathbf {x} _ {\max}),
$$

where ${ \mathcal { Z } } : = \{ \mathbf { x } ^ { \prime } \in \pi ^ { \prime } \mid \pi ^ { \prime } ( 0 ) = \mathbf { x } _ { a } , \pi ^ { \prime } ( b ) = \mathbf { x } _ { b } , \pi ^ { \prime } \subset \pi \}$ . By Definition $3 , \mathcal { X } _ { \mathrm { g r e e d y } }$ is constructed using x of π. We show that the optimal path $\pi ^ { * }$ also lies within $\chi _ { \mathrm { g r e e d y } }$ if π and $\pi ^ { * }$ belong to the same homotopy class.

Suppose that $\pi ^ { * }$ contains a state $\mathbf { x } _ { c }$ not in $\chi _ { \mathrm { g r e e d y } } .$

$$
\exists \mathbf {x} _ {c} \in \pi^ {*} \text {   s.t.   } \mathbf {x} _ {c} \notin \mathcal {X} _ {\text { greedy }}.\tag{8}
$$

Since $\mathbf { x } _ { I } , \mathbf { x } _ { G } \in \mathcal { X } _ { \mathrm { g r e e d y } } , \pi ^ { * }$ must exit the hyperellipsoid at some point and later re-enter it. Consequently, there exist at least two intersection points $\mathbf { x } _ { a }$ and $\mathbf { x } _ { b }$ between $\pi ^ { * }$ and the boundary of $\chi _ { \mathrm { g r e e d y } }$

Because π and $\pi ^ { * }$ are homotopic, they can be continuously deformed into one another without intersecting obstacles while keeping endpoints fixed (Hatcher 2002). The same holds for their subpaths $\pi _ { a b }$ and $\pi _ { a b c } ^ { * } .$ The cost of the direct (geodesic) subpath between $\mathbf { x } _ { a }$ and $\mathbf { x } _ { b }$ is strictly less than that of the detour passing through $\mathbf { x } _ { c } \mathbf { : }$

$$
c (\pi_ {a b}) <   c (\pi_ {a b c} ^ {*}).\tag{9}
$$

By definition, every subpath of an optimal path must also be optimal (Cormen et al. 2022); hence, (9) contradicts the optimality of $\pi ^ { * }$ . Therefore, the assumption in (8) is false, and $\pi ^ { * } \subseteq \mathcal { X } _ { \mathrm { g r e e d y } }$ □

While Theorem 1 establishes that the optimal path $\pi ^ { * }$ lies within the greedy informed set $\chi _ { \mathrm { g } }$ reedy when it shares the same homotopy class as the cur rent solution path $\pi ,$ this guarantee no longer holds when the two paths are homotopically distinct. In such cases, $\chi _ { \mathrm { g r e e d y } }$ may fail to include $\pi ^ { * }$ , motivating an examination of scenarios where this exclusion occurs.

Remark 1 (Non-inclusion of the optimal path in the greedy informed set) The greedy informed set $\chi _ { \mathrm { g r e e d y } }$ does not necessarily contain the optimal path $\pi ^ { * }$ if the current solution path and the optimal path lie in diferent homotopy classes.

Remark 1 follows directly from Theorem 1 and can be illustrated with a simple counterexample. Consider a planning problem in a maze-like environment with many homotopy classes between the initial and goal states $( { \mathrm { F i g u r e ~ 4 } } )$ . Let $\pi$ be a feasible path that passes through a narrow corridor and requires several sharp turns to navigate around obstacles. In contrast, let $\pi ^ { * }$ denote an optimal path in a diferent homotopy class that avoids the corridor by circumventing the obstacles entirely. By construction, the greedy informed set $\chi _ { \mathrm { g r e e d y } }$ is concentrated around the current solution path $\pi ,$ , primarily near the narrow passage.

Since π and $\pi ^ { * }$ belong to diferent homotopy classes, the path π cannot be continuously deformed into $\pi ^ { * }$ without intersecting obstacles. Theorem 1 establishes that if $\pi _ { i }$ and $\pi ^ { * }$ are homotopic, then $\pi ^ { * }$ lies in $\chi _ { \mathrm { g r e e d y } }$ . However, in this case, $\chi _ { \mathrm { g r e e d y } }$ is restricted to the vicinity of the narrow passage and therefore does not contain $\pi ^ { * }$ , which circumvents the obstacles. Thus, in environments of this type, where the current feasible path and the optimal path belong to diferent homotopy classes, the greedy informed set $\chi _ { \mathrm { g r e e d y } }$ may fail to include the optimal path.

This counterexample highlights an important limitation of relying solely on $\chi _ { \mathrm { g r e e d y } }$ . When the optimal path lies in a diferent homotopy class from the current solution path, sampling exclusively from $\chi _ { \mathrm { g r e e d y } }$ can lead to suboptimal performance. Understanding this behaviour is crucial when choosing how frequently the planner should sample from $\chi _ { \mathrm { g r e e d y } }$ , as the impact of this choice depends on the distribution of homotopy classes and the type of planning problem being addressed. A practical way to mitigate this issue is to also sample from the informed set with some probability (Section 5), thereby balancing exploration and exploitation within the planner.

![](Kyaw2024Greedy_figs/406abd674c885e28505d885b5cb0c6b933ffb61c8e999241a5e2a1859bb9835b.jpg)  
Fig. 4: Illustration of the suboptimality of the greedy informed set in an example planning scenario. The greedy informed set <sub>Xgreedy</sub>, constructed from the current tortuous solution path π, is shown as a dashed ellipse and the optimal path $\pi ^ { * }$ as a dotted line. In this case, $\mathcal { X } _ { \mathrm { g r e e d y } }$ fails to include some states that could improve the current solution cost (i.e., those leading towards π<sup>∗</sup> and lying outside of the hyperellipsoid) due to the nature of its greedy exploitation.

## 5 Greedy RRT\* (G-RRT\*)

Greedy RRT\* is an almost surely asymptotically optimal path planning algorithm that builds on RRT\* and its bi-directional variants (Klemm et al. 2015; Mashayekhi et al. 2020). It maintains two rapidly growing trees—one rooted at the start and the other at the goal—to explore the state space, and employs a greedy connection heuristic to guide them toward each other, similar to RRT-Connect (Kufner and LaValle 2000). As an RRT\*-like algorithm, it incrementally rewires the growing trees to preserve asymptotic optimality. However, rather than sampling randomly throughout the state space, $\mathrm { G - R R T ^ { * } }$ focuses the search on promising regions, once an initial solution is found. Specifically, it employs a greedy version of the informed set introduced in Section 4 to exploit knowledge of the existing solution path and focus subsequent sampling (Figure 5). The complete algorithm is presented in Algorithm blocks 1–5, with modifications to the bi-directional versions of RRT and RRT\* highlighted in red.

## 5.1 Greedy Informed Sampling

G-RRT\* finds better paths by simultaneously growing two trees, ${ \mathcal T } _ { a } ~ = ~ \left( V _ { a } , E _ { a } \right)$ from the start and $\mathcal { T } _ { b } = ( V _ { b } , E _ { b } )$ from the goal, consisting of the vertices $V _ { a } \cup V _ { b }$ and edges $E _ { a } \cup E _ { b }$ , each expanding toward randomly sampled states in the free space. Each tree incrementally rewires nearby vertices to minimize their cost-to-come. Once an initial solution is found, G-RRT\* exploits heuristic information from the current solution to bias sampling toward a progressively shrinking hyperellipsoidal region called the greedy informed set. It also samples from the informed subset to maintain exploration and ensure asymptotic optimality. Specifically, the balance between exploration and exploitation is controlled by a parameter $\epsilon \in [ 0 , 1 ]$ called the greedy biasing ratio. With probability $\epsilon ,$ the algorithm samples from the greedy informed set to exploit the current best path; with probability $1 - \epsilon ,$ it samples from the broader informed subset to encourage exploration and retain asymptotic opti mality. Thus, finding a good balance between uniform sampling for exploration and path-biased sampling for exploitation is necessary for G-RRT\* to rapidly reduce the search space and achieve faster convergence toward globally optimal solutions.

```matlab
Algorithm 1: Greedy RRT* (xI, xG)

1 Va ← {xI}; Ea ← ∅; Ta = (Va, Eb);
2 Vb ← {xG}; Eb ← ∅; Tb = (Vb, Eb);
3 Esol'n ← ∅;
4 for i = 1, ..., n do
5    ci ← ComputeBestCost (Esol'n);
6    xrand ← Sample (xI, xG, ci);
7    status, xa ← Extend* (Ta = (Va, Ea), xrand);
8    if status ≠ TRAPPED then
9    status, xb ← Connect* (Tb = (Vb, Eb), xa);
10    if status = REACHED then
11    Esol'n ← Esol'n ∪ {xa, xb};
12    Swap (Ta = (Va, Ea), Tb = (Vb, Eb));
13 return T = (Va ∪ Vb, Ea ∪ Eb);
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: ComputeBestCost
$(E_{\text{sol'n}} = \{(\mathbf{x}_a, \mathbf{x}_b) \mid \mathbf{x}_a \in V_a, \mathbf{x}_b \in V_b\})$

1 $c_i \leftarrow \infty;$

2 if $|E_{\text{sol'n}}| &gt; 0$ then

3 $c_i \leftarrow \min_{(\mathbf{x}_a, \mathbf{x}_b) \in E_{\text{sol'n}}} \{g_a(\mathbf{x}_a) + c(\mathbf{x}_a, \mathbf{x}_b) + g_b(\mathbf{x}_b)\};$

4 if $\epsilon &gt; U([0,1])$ then

5 if $c_i &lt; c_{\text{min}}$ then

6 $c_{\text{min}} \leftarrow c_i;$

7 $c_{\text{max}} \leftarrow \max_{\substack{(\mathbf{x}_a, \mathbf{x}_b) \in E_{\text{sol'n}} \\ \mathbf{x} \in \{\mathbf{x}_a, \mathbf{x}_b\} \\ k \geq 0}} \hat{f}\big(\text{Parent}^k(\mathbf{x})\big);$

8 $c_i \leftarrow c_{\text{max}};$

9 else

10 $c_{\text{min}} \leftarrow c_i;$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: Sample ( $x_{I}, x_{G}, c_{max}$ )

1 repeat
2 if  $c_{max} &lt; \infty$  then
3  $x_{rand} \leftarrow$ 
    SampleHyperEllipsoid ( $x_{I}, x_{G}, c_{max}$ );
4 if  $x_{rand} \in X \cap X_{PHS}$  then
5 return  $x_{rand}$ ;
6 else
7  $x_{rand} \leftarrow$  SampleUniform (X);
8 return  $x_{rand}$ ;
9 until  $x_{rand}$  satisfies bounds;
</div>

![](Kyaw2024Greedy_figs/9909122afa091cfb5922475cd6749f97b116728d04bcf866620f5d5d8d2d742e.jpg)  
(a)

![](Kyaw2024Greedy_figs/8e5c27f568a5c8c0c591e4886c5e98ae65aa3b3783ec0849f922a8370b43bbc6.jpg)  
(b)

![](Kyaw2024Greedy_figs/8ed8d76a80998759b5b534b5bd5f3390282019c78cfd42ea52de07529b18c455.jpg)  
(c)

![](Kyaw2024Greedy_figs/6d50574e569bca3a38b118d374bd5f16b1d1e02dc64bdd220307b919b176de67.jpg)  
(d)

Fig. 5: Illustrations of the progress of bi-directional sampling-based search performed by the G-RRT\* algorithm. The initial and goal states are shown as large black dots, sampled states as small black dots, and the start and goal trees in blue and orange, respectively. The current solution path is highlighted in yellow, and the $L ^ { 2 }$ greedy informed set—the set of states that could yield better solutions—is shown with gray dashed lines. G-RRT\* grows two trees rooted at the start and goal (a), where expansion is guided by a greedy connection heuristic that guides the two trees towards each other, producing an initial solution (b). Subsequent sampling is then focused within the greedy informed set to incrementally refine the path (c–d), almost-surely asymptotically converging to the optimal solution.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4: Extend* (T = (V, E), x)

1  $x_{nearest} \leftarrow Nearest(T = (V, E), x)$ ;
2  $x_{new} \leftarrow Steer(x_{nearest}, x)$ ;
3 if  $g(x_{nearest}) + c(x_{nearest}, x_{new}) + \hat{h}(x_{new}) &lt; c_i$  then
4    if ObstacleFree( $x_{nearest}, x_{new}$ ) then
5    $V \leftarrow V \cup \{x_{new}\}$ ;
6    $X_{near} \leftarrow Near(T = (V, E), x_{new}, r_{rewire})$ ;
7    $x_{min} \leftarrow x_{nearest}$ ;
8    foreach  $x_{near} \in X_{near}$  do
9    $c_{near} \leftarrow g(x_{near}) + c(x_{near}, x_{new})$ ;
10    if  $c_{near} &lt; g(x_{min}) + c(x_{min}, x_{new})$  then
11    if ObstacleFree( $x_{near}, x_{new}$ ) then
12    $x_{min} \leftarrow x_{near}$ ;
13    $E \leftarrow E \cup \{x_{min}, x_{new}\}$ ;
14    foreach  $x_{near} \in X_{near}$  do
15    if  $g(x_{new}) + c(x_{new}, x_{near}) &lt; g(x_{near})$ 
16    then
17    if ObstacleFree( $x_{new}, x_{near}$ ) then
18    $x_{parent} \leftarrow Parent(x_{near})$ ;
19    $E \leftarrow E \setminus \{(x_{parent}, x_{near})\}$ ;
20    $E \leftarrow E \cup \{(x_{new}, x_{near})\}$ ;
21    if  $x_{new} = x$  then
22    return REACHED,  $x_{new}$ ;
23    else
24 return ADVANCED,  $x_{new}$ ;
</div>

```txt
Algorithm 5: Connect* (T = (V, E), x)
1 repeat
2 | status, x_new ← Extend* (T = (V, E), x);
3 until status ≠ ADVANCED;
```

## 5.2 Implementation Details

G-RRT\* employs a balanced search strategy (Kufner and LaValle 2005) to keep both trees approximately equal in size while maintaining their rapidly exploring behaviour. Since collision checking is computationally expensive in practice, G-RRT\* also uses admissible heuristics to gate the vertex extension process (highlighted as red in Algorithm 4). An edge from the nearest vertex to a new vertex is validated only if it can improve the current best solution cost. This gating step also helps G-RRT\* to reduce overlap between the two trees, limiting the number of added vertices. G-RRT\* prunes the trees as in Gammell et al. (2018), removing vertices whose heuristic values exceed the greedy best heuristic cost. Additionally, because obtaining an initial solution as quickly as possible is important, rewiring is delayed until an initial solution is found. The remaining planning time is then used to rewire to improve solution quality.

## 6 Analysis

This section analyzes the theoretical guarantees of G-RRT\*, first establishing its probabilistic completeness in Section 6.1 and then proving asymptotic optimality in Sections 6.2.

## 6.1 Probabilistic Completeness

Since G-RRT\* adopts the same tree extension and connection strategy as RRT-Connect, its probabilistic completeness follows directly from the arguments established in Theorem 1 of Kufner and LaValle (2000). G-RRT\* grows two rapidly expanding trees, each of which inherits the probabilistic completeness property of the classical RRT. During the alternating extension process, new vertices are added to the sets $V _ { a }$ and $V _ { b }$ of the start and goal trees, respectively, such that the combined set $V _ { k } ~ = ~ V _ { a } \cup V _ { b }$ becomes dense in $\chi _ { \mathrm { f r e e } }$ as the number of iterations $k  \infty$ Because the greedy connection heuristic generates all the standard RRT vertices, along with additional ones, it aids in covering $\chi _ { \mathrm { f r e e } }$ and therefore does not afect the completeness guarantee.

## 6.2 Asymptotic Optimality

G-RRT\* uses the greedy informed set $\chi _ { \mathrm { g r e e d y } }$ , introduced in Section 4, to focus the search on a subset of the state space. This subset is bounded above by the informed subset, that is, $\mathcal { X } _ { \mathrm { g r e e d y } } \ \subseteq \ \mathcal { X } _ { \hat { f } }$ . Focusing the search in this way increases the likelihood of sampling states that lie within the omniscent set.

However, not all states in $\chi _ { \mathrm { g r e e d y } }$ are guaranteed to be in the omniscient set (see Figure 4). As a result, some states that could yield better solutions may lie outside the homotopy regions covered by $\chi _ { \mathrm { g r e e d y } }$ (Remark 1). Nevertheless, because $\mathrm { G } \mathrm { - R R T ^ { \ast } }$ samples from both $\chi _ { \mathrm { g r e e d y } }$ and $\mathcal { X } _ { \widehat { f } }$ according to the greedy biasing ratio ϵ (Section 5.1), setting $\epsilon < 1$ is a suficient condition for preserving asymptotic optimality.

Theorem 2 (Worst-case sample complexity for probabilistic optimality) When sampling with a greedy biasing ratio ϵ, the worst-case number of samples required to achieve probabilistic optimality increases by a factor of $\scriptstyle { \frac { 1 } { 1 - \epsilon } }$ relative to sampling only from the informed set.

Proof Let $P ( \mathbf { x } _ { \mathrm { r a n d } } \in \mathcal { X } _ { f } )$ represent the probability of sampling a state from the omniscient set. According to Lemma 5 from Gammell et al. (2018), sampling states from the omniscient set is a necessary condition for improving the current solution in RRT\*-like algorithms. Let $P ( \mathbf { x } _ { \mathrm { r a n d } } \in$ $\boldsymbol { \chi } _ { \hat { f } } )$ represent the probability of sampling a state from the informed set. Since the informed set $\boldsymbol { \mathcal { X } } _ { \hat { \boldsymbol { f } } }$ is a superset of the omniscient set $\chi _ { f }$ (Gammell et al. 2018), sampling from $\boldsymbol { \mathcal { X } } _ { \hat { \boldsymbol { f } } }$ is also a necessary condition for probabilistic optimality, and the probability of doing so is bounded below by the probability of sampling from $\chi _ { f }$

$$
P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {f}) \leq P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}})
$$

Thus, the expected number of samples required to improve the current solution to a holonomic problem depends on the probability of sampling the informed set, and is given by:

$$
E [ n ] = \frac {1}{P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}})}\tag{10}
$$

Recall that with probability $1 - \epsilon ,$ we sample from the informed set, and with probability $\epsilon ,$ we sample from the greedy informed set. Therefore, the overall probability of sampling from $\boldsymbol { \mathcal { X } } _ { \hat { \boldsymbol { f } } }$ in any given iteration is reduced, since we do not always sample from $\boldsymbol { \mathcal { X } } _ { \hat { \boldsymbol { f } } } .$ . Specifically, the new probability $P _ { \mathrm { n e w } } ( \mathbf { x } _ { \mathrm { r a n d } } \in \mathcal { X } _ { \hat { f } } )$ ) of selecting a random sample from $\boldsymbol { \mathcal { X } } _ { \hat { f } }$ is:

$$
P _ {\mathrm{new}} (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}}) = (1 - \epsilon) \cdot P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}})\tag{11}
$$

Substituting (11) into (10), the expected number of samples required to sample from $\boldsymbol { \mathcal { X } } _ { \hat { f } }$ now becomes:

$$
E [ n _ {\mathrm{new}} ] = \frac {1}{(1 - \epsilon) \cdot P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}})}\tag{12}
$$

Comparing (10) and (12):

$$
\frac {E [ n _ {\mathrm{new}} ]}{E [ n ]} = \frac {\overline {{(1 - \epsilon) \cdot P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}})}}}{\frac {1}{P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {\hat {f}})}} = \frac {1}{1 - \epsilon}\tag{13}
$$

Therefo $\therefore \mathbf { e } ,$ in the worst case where the greedy informed set does not include states from the optimal solution, the number of samples required for asymptotic optimality increases by a factor of $\frac { 1 } { 1 - \epsilon }$ compared to only sampling from $\chi _ { \hat { f } } . \quad \sqcup$

Theorem 3 (Expected sample complexity under mixed greedy sampling) Let the planner sample from the informed set with probability 1 − ϵ and from the greedy informed set with probability ϵ. Let $\gamma \in [ 0 , 1 ]$ denote the fraction of the omniscient set that is contained within the greedy informed set $( i . e . ,$ the recall of $\chi _ { \mathrm { g r e e d y } }$ with respect to $\begin{array} { r } { \ X _ { f } ) , } \end{array}$ and let $\rho$ denote the ratio of the volume of the omniscient set to the volume of the informed set. Then the expected number of samples required for probabilistic optimality satisfies

$$
\frac {E [ n _ {\mathrm{new}} ]}{E [ n ]} = \frac {1}{1 - \epsilon + \epsilon \gamma / \rho}.\tag{14}
$$

In particular, $E [ n \mathrm { e w } ] < E [ n ]$ if and only $i f \gamma > \rho .$

Proof Let λ denote the Lebesgue measure on $\mathbb { R } ^ { n }$ . Under uniform sampling of the greedy informed set, and following Definition 9 in Gammell et al. (2018), we define $\gamma$ as the recall of $\chi _ { \mathrm { g r e e d y } }$ with respect to the omniscient set:

$$
\gamma = \operatorname{Recall} \left(\mathcal {X} _ {\text { greedy }}\right) = \frac {\lambda \left(\mathcal {X} _ {f} \cap \mathcal {X} _ {\text { greedy }}\right)}{\lambda \left(\mathcal {X} _ {f}\right)} \in [ 0, 1 ].\tag{15}
$$

Similarly, let $\rho$ denote the ratio of the Lebesgue measures of the greedy informed set and the informed set:

$$
\rho = \frac {\lambda (\mathcal {X} _ {\text { greedy }})}{\lambda (\mathcal {X} _ {\hat {f}})} \in (0, 1 ].\tag{16}
$$

We can bound the Lebesgue measure of $\boldsymbol { \mathcal { X } } _ { \hat { f } }$ by the measure of a prolate hyperspheroid as

$$
\lambda \big (\mathcal {X} _ {\hat {f}} \big) \leq \lambda \big (\mathcal {X} _ {\mathrm{PHS}} \big) = \frac {\zeta_ {n}}{2 ^ {n}} c _ {i} \big (c _ {i} ^ {2} - c _ {\mathrm{min}} ^ {2} \big) ^ {\frac {n - 1}{2}}.\tag{17}
$$

Here $\zeta _ { n }$ is the Lebesgue measure of the unit n-ball,

$$
\zeta_ {n} = \frac {\pi^ {n / 2}}{\Gamma \left(\frac {n}{2} + 1\right)}.\tag{18}
$$

Similarly, the Lebesgue measure of $\chi _ { \mathrm { g r e e d y } }$ is bounded by

$$
\begin{array}{r l} & {\lambda \big (\mathcal {X} _ {\mathrm{greedy}} \big) \leq \lambda \big (\mathcal {X} _ {\mathrm{PHS}} \big)} \\ & {\quad = \frac {\zeta_ {n}}{2 ^ {n}} \hat {f} (\mathbf {x} _ {\max}) \big (\hat {f} (\mathbf {x} _ {\max}) ^ {2} - c _ {\min} ^ {2} \big) ^ {\frac {n - 1}{2}}} \end{array}\tag{19}
$$

Using (17) and (19), ρ admits the closed form

$$
\rho = \frac {\hat {f} (\mathbf {x} _ {\max})}{c _ {i}} \left(\frac {\hat {f} (\mathbf {x} _ {\max}) ^ {2} - c _ {\min} ^ {2}}{c _ {i} ^ {2} - c _ {\min} ^ {2}}\right) ^ {\frac {n - 1}{2}}.\tag{20}
$$

Let $P ( \mathbf { x } _ { \mathrm { r a n d } } \in \mathcal { X } _ { f } )$ denote the probability of sampling a state from the omniscient set. According to Lemma 5 from Gammell et al. (2018), sampling states from the omniscient set is a necessary condition for improving the current solution in $\mathrm { R R T ^ { * } } .$ -like algorithms. Recall that with probability $\epsilon ,$ we sample from the greedy informed set, and with prob ability $1 - \epsilon ,$ we sample from the informed set. Therefore, the new probability $P _ { \mathrm { n e w } }$ of selecting a random sample from either set that can guarantee improvement is:

$$
P _ {\mathrm{new}} = \epsilon \cdot P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {f} | \mathbf {x} _ {\mathrm{rand}} \sim \mathcal {U} (\mathcal {X} _ {\mathrm{greedy}}))\tag{21}
$$

$$
+ (1 - \epsilon) \cdot P (\mathbf {x} _ {\mathrm{rand}} \in \mathcal {X} _ {f} \mid \mathbf {x} _ {\mathrm{rand}} \sim \mathcal {U} (\mathcal {X} _ {\hat {f}}))\tag{22}
$$

Under uniform sampling, each conditional probability can be expressed as a ratio of relative measures. Specifically,

$$
P _ {\text { new }} = \epsilon \cdot \frac {\lambda (\mathcal {X} _ {f} \cap \mathcal {X} _ {\text { greedy }})}{\lambda (\mathcal {X} _ {\text { greedy }})} + (1 - \epsilon) \cdot \frac {\lambda (\mathcal {X} _ {f} \cap \mathcal {X} _ {\hat {f}})}{\lambda (\mathcal {X} _ {\hat {f}})}\tag{23}
$$

Since $\boldsymbol { \mathcal { X } } _ { \boldsymbol { \hat { f } } } \supseteq \boldsymbol { \mathcal { X } } _ { \boldsymbol { f } } ,$ , as noted in Gammell et al. (2018), (23) simplifies to:

$$
P _ {\mathrm{new}} = \epsilon \cdot \frac {\lambda (\mathcal {X} _ {f} \cap \mathcal {X} _ {\mathrm{greedy}})}{\lambda (\mathcal {X} _ {\mathrm{greedy}})} + (1 - \epsilon) \cdot \frac {\lambda (\mathcal {X} _ {f})}{\lambda (\mathcal {X} _ {\hat {f}})}\tag{24}
$$

Expressing (24) in terms of $\gamma$ and $\rho$ gives:

$$
P _ {\mathrm{new}} = \epsilon \cdot \left(\gamma / \rho \frac {\lambda (\mathcal {X} _ {f})}{\lambda (\mathcal {X} _ {\hat {f}})}\right) + (1 - \epsilon) \cdot \frac {\lambda (\mathcal {X} _ {f})}{\lambda (\mathcal {X} _ {\hat {f}})}\tag{25}
$$

$$
= [ (1 - \epsilon) + \epsilon (\gamma / \rho) ] \cdot \frac {\lambda (\mathcal {X} _ {f})}{\lambda (\mathcal {X} _ {\hat {f}})}\tag{26}
$$

Thus, the expected number of samples required to improve the current solution to a holonomic problem depends on the probability of sampling the informed set as well as on overlap measures between the two sets $\chi _ { f }$ and $\chi _ { \mathrm { g r e e d y } } \mathrm { . }$

$$
\frac {E [ n _ {\mathrm{new}} ]}{E [ n ]} = \frac {1}{[ (1 - \epsilon) + \epsilon (\gamma / \rho) ]}.\tag{27}
$$

□

In particular, setting $\gamma = 0$ in (27) recovers the worst-case factor $1 / ( 1 - \epsilon )$ , while setting $\gamma = 1$ and $\epsilon = 1$ (sampling only from $\chi _ { \mathrm { g r e e d y } } )$ ) yields the best-case factor $1 / \rho .$

## 7 Experiments

We evaluated the performance of G-RRT\* by comparing it with several state-of-the-art sampling-based planners on abstract problems in $\mathbb { R } ^ { 4 } , \ \mathbb { R } ^ { \bar { 8 } } .$ , and $\mathbb { R } ^ { 1 6 }$ (Section 7.1), as well as on robotic manipulation problems in $\mathbb { R } ^ { 7 } , \ \mathbb { R } ^ { 8 }$ , and $\mathbb { R } ^ { 1 4 }$ (Section 7.2). The former problems test the planner’s ability to find high-quality solutions in challenging, high-dimensional spaces, whereas the latter assesses performance on realistic robotic tasks. We compared $\mathrm { G } \mathrm { - R R T ^ { \ast } }$ with the Open Motion Planning Library (Sucan et al. 2012, OMPL) implementations of RRT-Connect, RRT\*, RRT\*-Connect (Klemm et al. 2015), BIT\* (Gammell et al. 2020), AIT\* (Strub and Gammell 2022), and AORRTC (Wilson et al. 2025). We also included a variant of G-RRT\* without the greedy heuristic (denoted by the  symbol) to highlight convergence diferences between the informed set and the greedyinformed set. All experiments were conducted using the Planner Developer Tools (Gammell et al. 2022, PDT) and Robowflex (Kingston and Kavraki 2022)<sup>2</sup>.

All planners were evaluated with the optimization objective of minimizing path length in $\mathbb { R } ^ { n }$ . Each planner used the default edge length specified by OMPL, computed as a fixed fraction of the maximum possible distance between any two states in the space. An RGG constant of $\eta ~ = ~ 1 . 0 0 1$ was applied to all planners, and the Euclidean distance $( \mathrm { i . e . , } L ^ { 2 }$ norm) for path length was used as the admissible cost heuristic. BIT\*-based planners used a batch size of 100, and G-RRT\* employed a greedy bias ratio of $\epsilon \ : \ : = \ : \ : 0 . 9$ to encourage exploitation across all experiments. Notably, AORRTC internally applies path simplification—specifically, randomized shortcutting (Geraerts and Overmars 2007; Hauser and $\mathrm { N g \mathrm { . } }$ -Thow-Hing 2010) and B-spline smoothing (Pan et al. 2012)—as part of its planning process to improve solution quality. To ensure a fair comparison, and because all reported times and costs for AORRTC include this simplification, we applied the same procedure to all planners as a post-processing step only: (i) after an initial solution had been found, and (ii) for the final solution at the end of the planning time limit. The costs of these post-processed, simplified paths are reported separately.<sup>3</sup>

## 7.1 Abstract Planning Problems

The planners were tested on three simulated planning problems in $\mathbb { R } ^ { 4 } , \mathbb { R } ^ { 8 }$ , and $\mathbb { R } ^ { 1 6 }$ . To provide some intuition, these problems are illustrated in two dimensions in Figure 6. The $\mathbb { R } ^ { 2 }$ versions are shown only for visu alization purposes, since they are too simple to diferentiate planner performance in a meaningful way. The higher-dimensional problem instances were created by extending the same obstacle layouts uniformly along each additional dimension. The first problem consists of many axis-aligned hypercubes, with the start and goal located at $[ - 0 . 2 5 , 0 , \ldots , 0 ] ^ { \top }$ and $[ 0 . 2 5 , 0 , \ldots , 0 ] ^ { \top }$ respectively (Figure 6a). The second problem contains a wall with a narrow passage gap, such that only two homotopy classes in all dimensions (Figure 6b), with start and goal at $[ - 0 . 3 , 0 , \ldots , 0 ] ^ { \top }$ and $[ 0 . 3 , 0 , \ldots , 0 ] ^ { \top }$ The final problem includes two hollow, axis-aligned hypercubes with an opening, enclosing the start and goal, located at $[ - 0 . 3 , 0 , \ldots , 0 ] ^ { \top }$ and $[ 0 . 3 , 0 , \ldots , 0 ] ^ { \top }$ respectively (Figure 6c).

Each planner was allocated a planning time proportional to the dificulty of the problem and the dimensionality of the state space. We ran 100 trials for the first two problems and 50 for the last, each initialized with a diferent pseudorandom seed. During each trial, solution costs were recorded at fixed time intervals $( 1 0 ^ { - 4 } \ \mathrm { s } )$ by a separate monitoring thread. If no solution was found at a given time, the cost was assigned an infinite value. We then reported the median costs to mitigate any bias from unsolved trials. Figure 7 shows each planner’s median solution cost and success rate over computation time. To ensure a fair comparison with AORRTC, we also applied path simplification to all of the initial and final solutions, as summarized in Table 1.

The results highlight the importance of maintaining two rapidly growing trees to quickly find initial solutions in high-dimensional problems. G-RRT\* discovers initial solutions as fast as RRT-Connect across all tested problems. Unlike RRT-Connect, G-RRT\* is an anytime algorithm that converges asymptotically to optimal solutions. From Figure 7, we observe that AORRTC reports lower median solution costs than G-RRT\* because its paths are already simplified. However, G-RRT\* reaches the same final solution costs as AORRTC, and does so faster than AOR-RTC and all other asymptotically optimal planners,

![](Kyaw2024Greedy_figs/789016bb8406e1679fe5053253e7027166f54dd05da79f9b02421600b1c2aa98.jpg)  
(a)

![](Kyaw2024Greedy_figs/19f11e0a5aa314d03c40d82f494700890de8627d33a31b0b46181452965c94f7.jpg)  
(b)

![](Kyaw2024Greedy_figs/fc3f30477509559de3f74b01d18dc632f9b03bb1df490cb1d3792ca98fcbdcbb.jpg)  
(c)  
Fig. 6: Two-dimensional illustrations of the abstract planning problems examined in Section 7.1. These include complex planning problems containing (a) many homotopy classes, (b) narrow passage gap environment, and (c) double enclosures, with a problem domain of size l = 1. The $\mathbf { x } _ { I }$ and x represent the initial and goal states, respectively.

![](Kyaw2024Greedy_figs/fcaa371ec1b6f508a1707a49126e9a46e640d678144175c882704ee0f3a64ffd.jpg)

![](Kyaw2024Greedy_figs/e5204e3ce39f7ec2c51acb704885f331f626d725c2aec8730521cccfc5e2e1d1.jpg)

![](Kyaw2024Greedy_figs/c7c6a8a6b7ad04fd6e0cdc65a1f176026416bc4e0afdf2dd80a4d4e65fa9508a.jpg)

![](Kyaw2024Greedy_figs/26b005552335cfe76d13d01611f84fee5ce23ae584161ac434ee93bcf6ac0006.jpg)

![](Kyaw2024Greedy_figs/3612b95f4ef73cf2d33a1e24df0acd091154097deaf238cff2845b593a49ca85.jpg)

![](Kyaw2024Greedy_figs/6c8550b65608a1ee2e25b78fdc1de31b19c8abfaf89a8ca1a5fb8f3a4fb1ba4b.jpg)

$$
\begin{array}{c c c c c c c c c} \hline \text {■RRT - C} & \text {■RRT*} & \text {■RRT*-C} & \text {■BIT*} & \text {■AIT*} & \text {■AORRTC} & \text {■G - RRT*†} & \text {■G - RRT*} \\ \hline \end{array}
$$

Fig. 7: Planner performance versus runtime on the abstract planning problems described in Section 7.1. The success plots show the percentage of successful runs over time, while the cost plots present the median solution cost versus runtime for each planner. Error bars and shaded regions denote non-parametric 99% confidence intervals on the median. The top and middle rows show the many-homotopy-class and narrow passage-gap experiments for $\mathbb { R } ^ { 8 }$ (left) and $\mathbb { R } ^ { 1 6 }$ (right), respectively, while the bottom row shows the double-enclosure experiment for <sup>R4</sup> (left) and $\mathbb { R } ^ { 8 }$ (right). Reported times and costs for AORRTC include path simplification, i.e., randomized shortcutting and B-spline smoothing.

even without path simplification. These results demonstrate the efectiveness of greedy informed sampling. Moreover, as shown in Table 1, when the same simplification process is applied uniformly to all planners, their initial solution costs become similar; yet G-RRT\* consistently yields lower final solution costs for most problems. Simplification improves path quality only locally, G-RRT\* achieves global improvement through RRT\*-style rewiring combined with its greedy biasing strategy.

Some of the most constrained problems further illustrate the strengths of G-RRT\*. In the narrow passage gap problem, all asymptotically optimal planners struggle to find a path through the passage, yet G-$\mathrm { R R T ^ { * } }$ is the only one that consistently succeeds within the available time budget. This demonstrates the efec tiveness of the greedy informed set relative to the informed sets used in $\mathrm { { \dot { G } { - } R R T ^ { * } } ^ { \dagger } }$ and AORRTC.

In the more dificult bug trap scenario involving double enclosures symmetric about the start and goal, all planners struggled as dimensionality increased. Only G-RRT\*, G-RRT\*<sup>†</sup>, RRT-Connect, and AOR-RTC solved more than half of the trials, emphasizing the importance of maintaining two greedily connecting trees in domains with several biased Voronoi regions (Yershova et al. 2005). Nevertheless, after simplification, G-RRT\* achieves lower median costs than competing planners, confirming its ability to find higher-quality solutions within the allotted planning time.

Table 1: Initial and final median solution costs for each planner on the abstract planning problems described in Section 7.1. Costs are shown after randomized shortcutting and B-spline smoothing. Lower values indicate better performance, with the best cost in bold and the second best underlined.

<table><tr><td rowspan="3"></td><td colspan="4">many homotopy classes</td><td colspan="4">narrow passage gap</td><td colspan="4">double enclosure</td></tr><tr><td colspan="2"> $\mathbb{R}^8$ </td><td colspan="2"> $\mathbb{R}^{16}$ </td><td colspan="2"> $\mathbb{R}^8$ </td><td colspan="2"> $\mathbb{R}^{16}$ </td><td colspan="2"> $\mathbb{R}^4$ </td><td colspan="2"> $\mathbb{R}^8$ </td></tr><tr><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td></tr><tr><td>RRT-C</td><td>0.511</td><td>0.511</td><td>0.694</td><td>0.694</td><td>1.384</td><td>1.384</td><td>2.075</td><td>2.075</td><td>1.547</td><td>1.547</td><td>1.806</td><td>1.806</td></tr><tr><td>RRT*</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td><td>1.412</td><td>1.304</td><td>∞</td><td>∞</td><td>1.552</td><td>1.500</td><td>∞</td><td>∞</td></tr><tr><td>RRT*-C</td><td>0.494</td><td>0.479</td><td>0.564</td><td>0.525</td><td>1.384</td><td>1.302</td><td>1.862</td><td>1.749</td><td>1.491</td><td>1.479</td><td>∞</td><td>∞</td></tr><tr><td>BIT*</td><td>0.495</td><td>0.447</td><td>0.595</td><td>0.463</td><td>1.315</td><td>0.982</td><td>1.871</td><td>1.431</td><td>1.485</td><td>1.452</td><td>∞</td><td>∞</td></tr><tr><td>AIT*</td><td>0.491</td><td>0.448</td><td>0.584</td><td>0.467</td><td>1.307</td><td>1.032</td><td>1.838</td><td>1.563</td><td>1.480</td><td>1.457</td><td>∞</td><td>∞</td></tr><tr><td>AORRTC</td><td>0.497</td><td>0.443</td><td>0.549</td><td>0.450</td><td>1.385</td><td>0.661</td><td>1.829</td><td>1.346</td><td>1.567</td><td>1.464</td><td>1.803</td><td>1.724</td></tr><tr><td>G-RRT*†</td><td>0.505</td><td>0.447</td><td>0.588</td><td>0.454</td><td>1.392</td><td>0.771</td><td>1.861</td><td>1.033</td><td>1.568</td><td>1.465</td><td>1.833</td><td>1.703</td></tr><tr><td>G-RRT*</td><td>0.508</td><td>0.443</td><td>0.573</td><td>0.451</td><td>1.369</td><td>0.655</td><td>1.828</td><td>1.019</td><td>1.536</td><td>1.451</td><td>1.784</td><td>1.643</td></tr></table>

![](Kyaw2024Greedy_figs/985e9b8c7ead99a39bf988627e9dd211107423e60098df69c79e8ecd71fcbdbf.jpg)  
(a) Start configuration

![](Kyaw2024Greedy_figs/a2a2ea3a156d78166bdc166b55173a0b4d066cd695b454c301e6d55da73278d5.jpg)  
(b) Goal configuration  
Fig. 8: A dual-arm manipulation problem for the Barrett WAM Arm in <sup>R14</sup>. Starting with (a) both arms pointing in the same direction (a), they must be moved to (b) extend in opposite directions without hitting the cage.

## 7.2 Manipulation Problems

The planners were also evaluated on manipulation tasks from the MotionBenchMaker dataset (Chamzas et al. 2021), using the Panda $\left( \mathbb { R } ^ { 7 } \right)$ and Fetch $\left( \mathbb { R } ^ { 8 } \right)$ robot platforms. The dataset provides a standardized set of seven manipulation benchmarks across multiple robot models, each containing 100 planning problems with varying start and goal configurations and workspace obstacles. For each robot, we selected four environments of increasing dificulty—bookshelf thin, table pick, box, and cage—ranging from relatively open reaching motions to tightly constrained scenarios (Figure 9). In addition, the planners were evaluated on a more challenging, higher-dimensional dual-arm manipulation task involving two Barrett WAM arms with a combined 14 degrees of freedom $\left( \mathbb { R } ^ { 1 4 } \right)$ in the Open Robotics Automation Virtual Environment (Diankov 2010), as shown in Figure 8. The objective is to move the arms from an initial configuration, where they point in the forward direction, to a goal configuration where they are extended outward in opposite directions, without colliding with the surrounding cage. OpenRAVE was configured to use the Flexible Collision Library (Pan et al. 2012, FCL) with a collision-checking resolution of $1 0 ^ { - 2 }$ Performance results for all planners, optimizing path length in <sup>Rn</sup>, are presented in Figures 10 and 11, with post-simplification statistics summarized in Table 2.

The observed performance trends closely match those of the abstract problems discussed in Section 7.1. G-RRT\* finds initial solutions as quickly as RRT-Connect and then uses the remaining planning time to converge toward optimality. In most planning problems from the MotionBenchMaker dataset, G-RRT\* achieves final solution costs comparable to those of AORRTC, but does so without requiring any path simplification—indicating faster convergence relative to the other asymptotically optimal planners. In very constrained problems such as bookshelf thin and cage for Fetch, however, all planners struggle to find feasible paths within the time limit. As a result, G-RRT\* spends less time rewiring, leading to slightly higher solution costs than AOR-RTC. Notably, for the dual-arm problem, G-RRT\* not only finds solutions faster but also produces the lowest final costs after simplification, highlighting the benefit of the greedy heuristic for high-dimensional planning problems.

## 8 Conclusion

In this paper, we build on our earlier introduction of the greedy informed set (Kyaw et al. 2022), and provide the first formal analysis of its behaviour within sampling-based planners. We show that the greedy informed set contains all states along the optimal path whenever the current and optimal solutions share the same homotopy class. Conversely, when the two paths belong to diferent homotopy classes, exclusively relying on the greedy informed set can prevent convergence to the global optimum. These findings highlight the need to appropriately balance greedy exploitation with broader exploration through the full informed set to preserve asymptotic optimality. To this end, we present G-RRT\*, an algorithm that uses bidirectional search to quickly find initial solutions and then leverages the greedy informed set to focus the subsequent search, while preserving asymptotic optimality guarantees.

![](Kyaw2024Greedy_figs/6f3d5b3a4df33c1715592e2a8c2dda9fb9002ce3b3daf5f36dc6e8c71f4276a6.jpg)  
Fig. 9: Manipulation problems from the MotionBenchMaker dataset used in our experiments (see Section 7.2). Each row shows a diferent robot platform (Panda or Fetch) evaluated on four benchmark tasks: bookshelf thin, table pick, box, and cage.

Table 2: Initial and final median solution costs for each planner on the manipulation problems described in Section 7.2. Costs are shown after randomized shortcutting and B-spline smoothing. Lower values indicate better performance, with the best cost in bold and the second-bes underlined.

<table><tr><td rowspan="2" colspan="2"></td><td colspan="2">bookshelf thin</td><td colspan="2">table pick</td><td colspan="2">box</td><td colspan="2">cage</td></tr><tr><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td><td> $c_{init}$ </td><td> $c_{final}$ </td></tr><tr><td rowspan="8">Panda ( $\mathbb{R}^7$ )</td><td>RRT-C</td><td>4.617</td><td>4.617</td><td>4.651</td><td>4.651</td><td>5.414</td><td>5.414</td><td>8.028</td><td>8.028</td></tr><tr><td>RRT*</td><td>4.996</td><td>4.915</td><td>4.534</td><td>4.532</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td></tr><tr><td>RRT*-C</td><td>4.565</td><td>4.436</td><td>4.553</td><td>4.457</td><td>4.812</td><td>4.411</td><td>7.591</td><td>7.408</td></tr><tr><td>BIT*</td><td>4.501</td><td>4.402</td><td>4.527</td><td>4.497</td><td>4.851</td><td>4.318</td><td>∞</td><td>∞</td></tr><tr><td>AIT*</td><td>4.543</td><td>4.523</td><td>4.683</td><td>4.564</td><td>4.919</td><td>4.569</td><td>∞</td><td>∞</td></tr><tr><td>AORRTC</td><td>4.471</td><td>4.315</td><td>4.553</td><td>4.342</td><td>5.202</td><td>4.149</td><td>7.876</td><td>5.189</td></tr><tr><td>G-RRT*†</td><td>4.565</td><td>4.251</td><td>4.571</td><td>4.326</td><td>5.099</td><td>3.800</td><td>8.014</td><td>7.116</td></tr><tr><td>G-RRT*</td><td>4.564</td><td>4.229</td><td>4.564</td><td>4.315</td><td>5.031</td><td>3.778</td><td>8.014</td><td>5.258</td></tr><tr><td rowspan="8">Fetch ( $\mathbb{R}^8$ )</td><td>RRT-C</td><td>11.872</td><td>11.872</td><td>9.207</td><td>9.207</td><td>10.804</td><td>10.804</td><td>14.646</td><td>14.646</td></tr><tr><td>RRT*</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td><td>∞</td></tr><tr><td>RRT*-C</td><td>∞</td><td>∞</td><td>8.072</td><td>6.713</td><td>9.609</td><td>7.895</td><td>12.691</td><td>12.379</td></tr><tr><td>BIT*</td><td>∞</td><td>∞</td><td>7.544</td><td>6.657</td><td>8.782</td><td>7.703</td><td>∞</td><td>∞</td></tr><tr><td>AIT*</td><td>∞</td><td>∞</td><td>7.323</td><td>6.578</td><td>8.650</td><td>7.778</td><td>∞</td><td>∞</td></tr><tr><td>AORRTC</td><td>11.312</td><td>8.526</td><td>8.900</td><td>6.001</td><td>10.593</td><td>7.046</td><td>13.934</td><td>7.826</td></tr><tr><td>G-RRT*†</td><td>11.353</td><td>9.871</td><td>8.846</td><td>5.690</td><td>10.596</td><td>7.023</td><td>14.358</td><td>12.145</td></tr><tr><td>G-RRT*</td><td>11.237</td><td>9.523</td><td>8.703</td><td>5.576</td><td>10.347</td><td>6.827</td><td>14.230</td><td>11.898</td></tr></table>

<table><tr><td rowspan="2"></td><td colspan="2"> $dual-arm (\mathbb{R}^{14})$ </td></tr><tr><td> $c_{init}$ </td><td> $c_{final}$ </td></tr><tr><td>RRT-C</td><td>11.864</td><td>11.864</td></tr><tr><td>RRT*</td><td>∞</td><td>∞</td></tr><tr><td>RRT*-C</td><td>11.562</td><td>10.017</td></tr><tr><td>BIT*</td><td>12.890</td><td>8.618</td></tr><tr><td>AIT*</td><td>12.017</td><td>8.708</td></tr><tr><td>AORRTC</td><td>12.162</td><td>7.028</td></tr><tr><td>G-RRT*†</td><td>11.801</td><td>9.003</td></tr><tr><td>G-RRT*</td><td>11.988</td><td>6.707</td></tr></table>

We evaluate G-RRT\* on both abstract planning problems and manipulation tasks across a range of dimensions. Our results show that G-RRT\* finds initial solutions as quickly as RRT-Connect and then uses the remaining planning time to improve them, converging faster than all other asymptotically optimal planners. It achieves these gains without relying on path simplification, unlike AORRTC, and applying simplification as a post-processing step yields even lower solution costs. Overall, the experiments demonstrate that incorporating greedy informed sampling can substantially accelerate convergence to highquality solutions in informed planners.

There are several promising directions for future work. Because G-RRT\* currently draws a single sample per iteration, extending greedy informed sampling to batched updates, as in BIT\*, could further improve performance. Additionally, we are investigating ways to define and exploit promising regions of the state space; focusing sampling on these regions may improve both the eficiency and convergence rate of sampling-based motion planners for high-dimensional problems.

Acknowledgements. The authors would like to thank Yunfan Lu for dedicating time to assist with the proofs in this manuscript.

## References

Akgun, B. and M. Stilman 2011. Sampling heuristics for optimal motion planning in high dimensions. In 2011 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 2640–2645.

![](Kyaw2024Greedy_figs/3cf2079e2d500c1ecf0dd9dd288dee088b9d1ec5acf1d66dccc677d98a77fdf8.jpg)  
(a) bookshelf (Panda)

![](Kyaw2024Greedy_figs/33cf9be8743c6c4ba6a61ff18950d7c62342fb3bcfdd27e85e2da5a5ea67ca54.jpg)  
(c) box (Panda)

![](Kyaw2024Greedy_figs/21198a4e5e49f5c4e43d5b3b6ffba9c12017569f6c2b5e6492b4f3eed71c1c04.jpg)  
(b) table (Panda)

![](Kyaw2024Greedy_figs/1ee5db8f25aeeba901a1c02a26b6f3595a0bf14bf4e149e244a23eaa14bb3149.jpg)  
(d) cage (Panda)

![](Kyaw2024Greedy_figs/b290b282dc6c2eec02c1a8ba423b81e8afc65c272ed4532bd29f10a1522a99f3.jpg)  
(e) bookshelf (Fetch)

![](Kyaw2024Greedy_figs/f9ddbaeab6cf2fd51b6c774eaa81824aede915c2c7bcbdf36c4713a89ef085b6.jpg)  
(f) table (Fetch)

![](Kyaw2024Greedy_figs/ad5fa3271e335d78207545a882446ab62da5cce83c22450452f3766aef84df96.jpg)  
(g) box (Fetch)

![](Kyaw2024Greedy_figs/395c101d1cf8f47d0c6fe2201ffd6af8e9d5e8995d4d4692542b1a0e78235ddb.jpg)  
(h) cage (Fetch)

$$
\boxed { \begin{array}{c} \text {■RRT - C■RRT*■RRT* - C■BIT*■AIT*■AORRTC■G - RRT*†■G - RRT*} \\ \hline \end{array} }
$$

Fig. 10: Planner performance versus running time on the Panda $( \mathbb { R } ^ { 7 } )$ and Fetch (<sup>R8</sup>) problems from the MotionBenchMaker dataset (see Section 7.2 and Figure 9). The success plots show the percentage of successful runs over time, while the cost plots present the median solution cost versus runtime for each planner. Error bars and shaded regions denote non-parametric 99% confidence intervals on the median. Reported times and costs for RRT-Connect and AORRTC include path simplification, i.e., randomized shortcutting and B-spline smoothing.

Alterovitz, R., S. Patil, and A. Derbakova 2011. Rapidly-Exploring Roadmaps: Weighing exploration vs. refinement in optimal motion planning. In 2011 IEEE International Conference on Robotics and Automation (ICRA), pp. 3706–3712.

Arslan, O. and P. Tsiotras 2013. Use of relaxation methods in sampling-based algorithms for optimal motion planning. In 2013 IEEE International Conference on Robotics and Automation (ICRA), pp. 2421–2428.

Bialkowski, J., M. Otte, and E. Frazzoli 2013. Freeconfiguration biased sampling for motion planning. In 2013 IEEE/RSJ International Conference on

Intelligent Robots and Systems (IROS), pp. 1272– 1279.

Chamzas, C., C. Quintero-Pena, Z. Kingston, A. Orthey, D. Rakita, M. Gleicher, M. Toussaint, and L.E. Kavraki. 2021. MotionBenchMaker: A tool to generate and benchmark motion planning datasets. IEEE Robotics and Automation Letters 7 (2): 882–889.

Cormen, T.H., C.E. Leiserson, R.L. Rivest, and C. Stein. 2022. Introduction to Algorithms. MIT Press.

Diankov, R. 2010. Automated construction of robotic manipulation programs. PhD Thesis, Robotics

RRT-C RRT\* RRT\*-C BIT\* AIT\* AORRTC G-RRT\*† G-RRT\*  
![](Kyaw2024Greedy_figs/1c7d8d9c71dac37aa9abda98cddef3bfbe7897eea3f61819e3dbf7f92e27c7ea.jpg)  
Fig. 11: Planner performance versus runtime on the dual-arm problem described in Section 7.2 (see Figure 8). The success plots show the percentage of successful runs over time, and the cost plots present the median solution cost versus runtime for each planner. Error bars and shaded regions denote non-parametric 99% confidence intervals on the median. Each planner was run for 50 trials with a runtime limit of $1 0 0 \mathrm { ~ s ~ i n ~ } \mathbb { R } ^ { 1 4 }$ . Reported times and costs for AORRTC include path simplification, i.e., randomized shortcutting and B-spline smoothing.

Institute, Carnegie Mellon University, Pittsburgh, PA.

Dobson, A. and K.E. Bekris. 2014. Sparse roadmap spanners for asymptotically near-optimal motion planning. The International Journal of Robotics Research 33 (1): 18–47.

Elbanhawi, M. and M. Simic. 2014. Sampling-based robot motion planning: A review. IEEE Access 2: 56–77.

Faroni, M., N. Pedrocchi, and M. Beschi. 2024. Adaptive hybrid local-global sampling for fast informed sampling-based optimal path planning. Autonomous Robots 48 (2): 6.

Ferguson, D. and A. Stentz 2006. Anytime RRTs. In 2006 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 5369–5375.

Gammell, J.D., T.D. Barfoot, and S.S. Srinivasa. 2018. Informed sampling for asymptotically optimal path planning. IEEE Transactions on Robotics 34 (4): 966–984.

Gammell, J.D., T.D. Barfoot, and S.S. Srinivasa. 2020. Batch Informed Trees (BIT\*): Informed asymptotically optimal anytime search. The International Journal of Robotics Research 39 (5): 543–567.

Gammell, J.D., S.S. Srinivasa, and T.D. Barfoot 2014. Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic. In 2014 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 2997–3004.

Gammell, J.D., M.P. Strub, and V.N. Hartmann 2022. Planner Developer Tools (PDT): Reproducible experiments and statistical analysis for developing and testing motion planners. In Proceedings of the Workshop on Evaluating Motion Planning Performance (EMPP), 2022 IEEE/RSJ

International Conference on Intelligent Robots and Systems (IROS).

Geraerts, R. and M.H. Overmars. 2007. Creating high-quality paths for motion planning. The International Journal of Robotics Research 26 (8): 845–863.

Hatcher, A. 2002. Algebraic topology. Cambridge University Press.

Hauser, K. and V. Ng-Thow-Hing 2010. Fast smoothing of manipulator trajectories using opti mal bounded-acceleration shortcuts. In 2010 IEEE International Conference on Robotics and Automation (ICRA), pp. 2493–2498.

Hsu, D., L.E. Kavraki, J.C. Latombe, R. Motwani, S. Sorkin, et al. 1998. On finding narrow passages with probabilistic roadmap planners. In Robotics: The Algorithmic Perspective: 1998 Workshop on the Algorithmic Foundations of Robotics (WAFR), pp. 141–154.

Islam, F., J. Nasir, U. Malik, Y. Ayaz, and O. Hasan 2012. RRT\*-Smart: Rapid convergence implementation of RRT\* towards optimal solution. In 2012 IEEE International Conference on Mechatronics and Automation (ICMA), pp. 1651–1656.

Jeong, I.B., S.J. Lee, and J.H. Kim. 2019. Quick-RRT\*: Triangular inequality-based implementation of RRT\* with improved initial solution and convergence rate. Expert Systems with Applications 123: 82–90.

Jiang, H., Q. Chen, Y. Zheng, and Z. Xu 2020. Informed RRT\* with adjoining obstacle process for robot path planning. In 2020 IEEE 20th International Conference on Communication Technology (ICCT), pp. 1471–1477.

Karaman, S. and E. Frazzoli. 2011. Sampling-based algorithms for optimal motion planning. The International Journal of Robotics Research 30 (7): 846–894.

Karaman, S., M.R. Walter, A. Perez, E. Frazzoli, and S. Teller 2011. Anytime motion planning using the RRT. In 2011 IEEE International Conference on Robotics and Automation (ICRA), pp. 1478–1483.

Kavraki, L.E., P. Svestka, J.C. Latombe, and M.H. Overmars. 1996. Probabilistic roadmaps for path planning in high-dimensional configuration spaces. IEEE Transactions on Robotics and Automation 12 (4): 566–580.

Khatib, O. 1986. Real-time obstacle avoidance for manipulators and mobile robots. The International Journal of Robotics Research 5 (1): 90–98.

Kim, D., J. Lee, and S.e. Yoon 2014. Cloud RRT\*: Sampling cloud based RRT\*. In 2014 IEEE International Conference on Robotics and Automation (ICRA), pp. 2519–2526.

Kim, M.C. and J.B. Song 2015. Informed RRT\* towards optimality by reducing size of hyperellipsoid. In 2015 IEEE International Conference on Advanced Intelligent Mechatronics (AIM), pp. 244–248.

Kingston, Z. and L.E. Kavraki 2022. Robowflex: Robot motion planning with MoveIt made easy. In 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 3108–3114.

Klemm, S., J. Oberl¨ander, A. Hermann, A. Roennau, T. Schamm, J.M. Zollner, and R. Dillmann 2015. RRT\*-Connect: Faster, asymptotically optimal motion planning. In 2015 IEEE International Conference on Robotics and Biomimetics (ROBIO), pp. 1670–1677.

Kufner, J. and S. LaValle. 2005. An eficient approach to path planning using balanced bidirectional RRT search. Robotics Institute, Carnegie Mellon University, Pittsburgh, PA, USA. Technical Report CMU-RI-TR-05-34 .

Kufner, J.J. and S.M. LaValle 2000. RRT-Connect: An eficient approach to single-query path planning. In Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No. 00CH37065), Volume 2, pp. 995–1001.

Kyaw, P.T., A.V. Le, P. Veerajagadheswar, M.R. Elara, T.T. Thu, N.H.K. Nhan, P. Van Duc, and M.B. Vu. 2022. Energy-eficient path planning of reconfigurable robots in complex environments. IEEE Transactions on Robotics 38 (4): 2481–2494.

LaValle, S.M. 2006. Planning algorithms. Cambridge University Press.

LaValle, S.M. and J.J. Kufner Jr. 2001. Randomized kinodynamic planning. The International Journal of Robotics Research 20 (5): 378–400.

Li, Y., W. Wei, Y. Gao, D. Wang, and Z. Fan. 2020. PQ-RRT\*: An improved path planning algorithm for mobile robots. Expert systems with applications 152: 113425.

Liao, B., F. Wan, Y. Hua, R. Ma, S. Zhu, and X. Qing. 2021. F-RRT\*: An improved path planning algorithm with improved initial solution and convergence rate. Expert Systems with Applications 184: 115457.

Mashayekhi, R., M.Y.I. Idris, M.H. Anisi, I. Ahmedy, and I. Ali. 2020. Informed RRT\*-Connect: An asymptotically optimal single-query path planning

method. IEEE Access 8: 19842–19852.

Otte, M. and N. Correll. 2013. C-FOREST: Parallel shortest path planning with superlinear speedup. IEEE Transactions on Robotics 29 (3): 798–806.

Pan, J., S. Chitta, and D. Manocha 2012. FCL: A general purpose library for collision and proximity queries. In 2012 IEEE International Conference on Robotics and Automation (ICRA), pp. 3859–3866.

Pan, J., L. Zhang, and D. Manocha. 2012. Collisionfree and smooth trajectory computation in cluttered environments. The International Journal of Robotics Research 31 (10): 1155–1175.

Qureshi, A.H. and Y. Ayaz. 2016. Potential functions based sampling heuristic for optimal path planning. Autonomous Robots 40: 1079–1093.

Reif, J.H. 1979. Complexity of the mover’s problem and generalizations. In 20th Annual Symposium on Foundations of Computer Science (SFCS 1979), pp. 421–427.

Salzman, O. and D. Halperin. 2016. Asymptotically near-optimal RRT for fast, high-quality motion planning. IEEE Transactions on Robotics 32 (3): 473–483.

Strub, M.P. and J.D. Gammell. 2022. Adaptively Informed Trees (AIT\*) and Efort Informed Trees (EIT\*): Asymmetric bidirectional sampling-based path planning. The International Journal of Robotics Research 41 (4): 390–417.

Sucan, I.A., M. Moll, and L.E. Kavraki. 2012. The open motion planning library. IEEE Robotics & Automation Magazine 19 (4): 72–82.

Wilson, T.S., W. Thomason, Z. Kingston, and J.D. Gammell. 2025. AORRTC: Almost-surely asymptotically optimal planning with RRT-Connect. IEEE Robotics and Automation Letters 10 (12): 13375–13382.

Yershova, A., L. Jaillet, T. Sim´eon, and S.M. LaValle 2005. Dynamic-Domain RRTs: Eficient exploration by controlling the sampling domain. In Proceedings of the 2005 IEEE International Conference on Robotics and Automation (ICRA), pp. 3856–3861.