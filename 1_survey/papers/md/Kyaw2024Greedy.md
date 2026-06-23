---
citation_key: Kyaw2024Greedy
arxiv_id: 2405.03411
arxiv_url: "https://arxiv.org/abs/2405.03411"
title: "Greedy Heuristics for Sampling-Based Motion Planning in High-Dimensional State Spaces"
authors_short: "Phone Thiha Kyaw et al."
year: 2024
direction_tag: D_asymptotically_optimal_sampling
source: pymupdf4llm
converted_at: 2026-06-23T19:09:22Z
origin: ai+web
reviewed: false
---

# Greedy Heuristics for Sampling-Based Motion Planning in High-Dimensional State Spaces 

Phone Thiha Kyaw 1*, Anh Vu Le 2, Rajesh Elara Mohan 3, Jonathan Kelly 1 

> 1Space & Terrestrial Autonomous Robotic Systems (STARS) Laboratory, University of Toronto Institute for Aerospace Studies, 4925 Dufferin Sreet, Toronto, M3H 5T6, Ontario, Canada. 

> 2Advanced Intelligent Technology Research Group, Faculty of Electrical and Electronics Engineering, Ton Duc Thang University, Ho Chi Minh City, 700000, Vietnam. 

> 3ROAR Lab, Engineering Product Development, Singapore University of Technology and Design, Singapore, 487372, Singapore. 

*Corresponding author(s). E-mail(s): phone.thiha@robotics.utias.utoronto.ca; Contributing authors: leanhvu@tdtu.edu.vn; rajeshelara@sutd.edu.sg; jonathan.kelly@robotics.utias.utoronto.ca; 

## **Abstract** 

Informed sampling techniques accelerate the convergence of sampling-based motion planners by biasing sampling toward regions of the state space that are most likely to yield better solutions. However, when the current solution path contains redundant or tortuous segments, the resulting informed subset may remain unnecessarily large, slowing convergence. Our prior work addressed this issue by introducing the greedy informed set, which reduces the sampling region based on the maximum heuristic cost along the current solution path. In this article, we formally characterize the behavior of the greedy informed set within Rapidly-exploring Random Tree (RRT*)-like planners and analyze how greedy sampling affects exploration and asymptotic optimality. We then present Greedy RRT* (G-RRT*), a bi-directional anytime variant of RRT* that leverages the greedy informed set to focus sampling in the most promising regions of the search space. Experiments on abstract planning benchmarks, manipulation tasks from the MotionBenchMaker dataset, and a dual-arm Barrett WAM problem demonstrate that G-RRT* rapidly finds initial solutions and converges asymptotically to optimal paths, outperforming state-of-the-art sampling-based planners. 

**Keywords:** Sampling-based motion planning, optimal path planning, informed sampling, bidirectional search, greedy heuristics, high-dimensional planning 

## **1 Introduction** 

Path planning is the problem of finding a collisionfree path from an initial state to a goal state while also considering specific optimization objectives, such as minimizing path length or energy use, for example (LaValle 2006). Many planning algorithms exist, including graph search, artificial potential fields, and sampling-based methods (Elbanhawi and Simic 2014). However, it remains challenging to find collision-free, optimal paths, especially in high-dimensional state spaces; the general path planning problem is known to be PSPACE-hard (Reif 1979). 

Sampling-based planners, such as the probabilistic roadmap (Kavraki et al. 1996, PRM) and rapidlyexploring random tree (LaValle and Kuffner Jr 2001, RRT) algorithms, tackle the complexity of highdimensional path planning by sacrificing completeness for efficiency, providing only probabilistic guarantees. The asymptotically optimal variants PRM* and RRT* (Karaman and Frazzoli 2011) improve solution 

quality over time but remain computationally expensive due to their reliance on random sampling. A substantial portion of the computational effort is often wasted exploring irrelevant portions of the state space. To improve planning performance, it is crucial to focus sampling on promising regions of the problem domain. 

Existing direct informed sampling methods (Gammell et al. 2014, 2018) mitigate inefficiency by defining bounded, hyperellipsoidal sampling regions, called _informed sets_ , based on the cost of the current solution. While this significantly reduces the size of the search space, initial feasible solutions are often highly tortuous, containing many redundant states— intermediate states that can be removed through standard path-shortening techniques without affecting feasibility. Such redundant states increase the solution cost and enlarge the informed set unnecessarily, reducing the likelihood of finding states that may be part of a better solution. To address this shortcoming, Kyaw et al. (2022) introduced a new direct informed sampling procedure that biases sampling based on heuristic information from the states that are part of 

1 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0002-00.png)


**----- Start of picture text -----**<br>
Informed set Greedy informed set<br>Tortuous solution path<br>**----- End of picture text -----**<br>


**Fig. 1** : Comparison of informed set sizes for a planning problem with a tortuous solution path (yellow) from the start (red) to the goal (green). The _L_[2] informed set (left) is defined by the current solution cost and covers a large ellipsoidal region. In contrast, the _L_[2] _greedy informed set_ (right) is defined using the state with the maximum admissible heuristic along the current solution path, substantially reducing the ellipsoidal area. 

the current solution, independent of their cost. These states are used to define an alternative _greedy informed set_ that reduces the size of the informed sampling hyperellipsoid, improving both the efficiency and the convergence rate of planning. Although the greedy informed set concept was introduced in (Kyaw et al. 2022), no analysis of its properties was carried out. 

Informed sets are only useful to reduce the size of the search space once an initial solution has been found, making rapid discovery of a feasible path crucial for overall planning efficiency. A key contribution of this work is a formal analysis of the performance and trade-offs associated with the _greedy informed set_ . To accelerate the search for an initial solution, bidirectional planning can be employed. Algorithms such as RRT-Connect (Kuffner and LaValle 2000) grow two trees—one from the start and one from the goal—that expand toward each other, guided by a connection heuristic. Building on this idea and incorporating the greedy informed set, we propose _Greedy-RRT*_ (G-RRT*), a bidirectional, asymptotically optimal sampling-based planner. G-RRT* rapidly identifies initial solutions and exploits the greedy informed set to enhance solution quality, particularly in highdimensional spaces. In summary, we make the following contributions herein. 

- We provide a formal analysis of properties of the greedy informed set and consider how possible algorithmic choices influence planning performance. 

- We present Greedy-RRT* (G-RRT*), a bidirectional, asymptotically optimal sampling-based planning algorithm that leverages the proposed greedy heuristic.[1] 

- We prove the completeness and asymptotic optimality of G-RRT*, building upon existing results from the sampling-based planning literature. 

- We show experimentally that greedy exploitation in large planning domains improves success and convergence rates over state-of-the-art methods, using both simulations and manipulation datasets. 

> 1Information on the OMPL implementations of G-RRT* is publicly available at https://github.com/utiasSTARS/ompl. 

The article is organized as follows. Section 2 covers related literature, while Section 3 describes our notation and problem formulation. Section 4 defines the greedy informed set, while Section 5 details the G-RRT* algorithm. Section 6 analyzes the properties of G-RRT*. Section 7 demonstrates the performance of G-RRT* in simulations and through manipulation experiments. The article concludes with some discussion in Section 8. 

## **2 Related Work** 

This section first reviews the existing literature on sampling-based planning algorithms (Section 2.1), and then discusses methods for accelerating their convergence (Section 2.2). 

## **2.1 Sampling-Based Motion Planning** 

Sampling-based motion planners can be broadly classified into multiple-query and single-query categories. Multiple-query planners, such as probabilistic roadmaps (Kavraki et al. 1996; Hsu et al. 1998), construct a graph of collision-free paths that can be reused for different start-goal pairs. In contrast, single-query planners expand a tree toward randomly sampled states to solve individual planning problems; rapidly-exploring random trees (LaValle and Kuffner Jr 2001) are a well-known example. These sampling-based approaches are often effective in highdimensional state spaces and reduce computation by avoiding explicit obstacle representations, unlike deterministic graph-search planners. However, they typically yield only feasible (collision-free) paths and do not guarantee optimality. 

Karaman and Frazzoli (2011) introduced PRM* and RRT*, optimal variants of PRM and RRT that guarantee asymptotic optimality. RRT* expands a tree into free space through random sampling, but unlike RRT, it considers nearby vertices to select the best parent and incrementally rewires them to improve path quality. This rewiring enables RRT* to converge asymptotically to the optimal solution, a key property in sampling-based motion planning. 

The RRT[#] algorithm (Arslan and Tsiotras 2013) extends the local rewiring of RRT* to the global level using dynamic programming, accelerating convergence by removing states that cannot improve the current solution. Karaman et al. (2011) proposed a branch-and-bound pruning scheme that deletes vertices whose cost-to-come plus a lower bound on the cost-to-go exceeds the cost of the current best path. This pruning step eliminates vertices that are unlikely to contribute to better solutions and enhances realtime performance. Quick-RRT* (Jeong et al. 2019) refines parent selection and rewiring by also considering ancestors of nearby vertices, up to a user-defined depth, as candidate parents. Similarly, F-RRT* (Liao et al. 2021) enhances initial path quality and convergence by generating random parent vertices close to obstacles. 

2 

Various extensions have been proposed to accelerate the convergence of RRT*, including bi-directional variants (Kuffner and LaValle 2000; Klemm et al. 2015) and methods that relax optimality to nearoptimality (Dobson and Bekris 2014; Salzman and Halperin 2016). Our proposed approach similarly employs bi-directional search to rapidly generate initial solutions. However, because these methods sample uniformly across the entire state space, their convergence slows markedly in high-dimensional problems, increasing the computational effort required to find optimal solutions. 

## **2.2 State Space Sampling Methods** 

Prior work on sampling-based planning has emphasized ways to improve the sampling process. While uniform sampling preserves global optimality, performance can often be improved by biasing samples toward regions more likely to yield better solutions. For example, Bialkowski et al. (2013) proposed a biased sampling method that records past collisions to direct future samples away from obstacles. Similarly, Kim et al. (2014) used a generalized Voronoi graph to decompose free space into spheres of varying radii, forming a dynamic sampling ‘cloud’ that evolves as the best solution is refined. 

In P-RRT* and PQ-RRT* (Qureshi and Ayaz 2016; Li et al. 2020), random sampling is guided by artificial potential fields towards more promising state space regions (Khatib 1986), trading off exploration for exploitation. Compared with traditional rejection sampling, these free-space-biased methods quickly find improved paths and reduce the number of rejected samples, but they continue to draw samples that do not improve the current solution. 

Several extensions of RRT* have been developed to accelerate convergence. Akgun and Stilman (2011) introduced a bi-directional version of RRT* that uses path-biased sampling and heuristic sample rejection for high-dimensional problems. Related work (Islam et al. 2012; Alterovitz et al. 2011; Faroni et al. 2024) applies similar path-biasing and refinement ideas, achieving faster convergence but often favouring locally optimal solutions over globally better ones. Techniques like rectangular rejection sampling (Ferguson and Stentz 2006; Otte and Correll 2013) can improve convergence, but their effectiveness decreases as dimensionality increases. 

To address this scalability issue, Gammell et al. (2014, 2018) proposed _informed sampling_ , implemented in Informed RRT*. Once a feasible path is found, the algorithm samples only within an _n_ - dimensional hyperellipsoid—called the _L_[2] informed set—bounded by the current solution cost, which shrinks as better solutions are found. 

Although informed sampling is highly effective, early feasible paths often include redundant states, producing tortuous trajectories with many unnecessary twists and turns. These paths can yield overly 

large informed sets, which slow convergence, particularly in high-dimensional state spaces. Consequently, later studies (Kim and Song 2015; Jiang et al. 2020; Wilson et al. 2025) integrated path simplification and anytime refinement to tighten the informed set and improve solution quality, achieving state-of-the-art results on the Motion Bench Maker dataset (Chamzas et al. 2021). We pursue a different strategy: leveraging the greedy heuristic proposed in (Kyaw et al. 2022) within a bi-directional framework to prioritize sampling in regions most likely to yield improvement. By coupling greedy state-space biasing with efficient tree growth, our method accelerates convergence without sacrificing global solution optimality. 

## **3 Preliminaries** 

We begin by defining the notation used throughout the paper and introducing key planning concepts in Section 3.1. Section 3.2 then reviews the formal definitions of the feasible and optimal path-planning problems, providing a foundation for our analysis of the G-RRT* algorithm. 

## **3.1 Notation** 

Let the state space of a path planning problem be denoted by _X ⊆_ R _[n]_ , and let **x** _∈X_ denote a single state. Let _X_ obs ⊊ _X_ be the set of states in collision with obstacles, and let _X_ free = _X \ X_ obs be the set of collision-free states. A path is a continuous function _π_ : [0 _,_ 1] _→X_ , and we denote by Σ the set of all such paths. The initial and goal states are denoted by **x** _I ∈X_ free and **x** _G ∈X_ free, respectively. Each planning problem is associated with a cost function _c_ : Σ _→_ R _≥_ 0 that maps a path to a non-negative real value. Herein, we define the cost of a path as its length under the standard Euclidean metric on R _[n]_ . 

As is standard in sampling-based motion planning, we represent paths using graphs and, in particular, restrict our attention to trees, which are directed acyclic graphs. A tree is incrementally constructed by connecting states through feasible transitions that respect collision constraints. Let _T_ = ( _V, E_ ) denote such a tree, where _V_ is a set of vertices and _E ⊆ V ×V_ is a set of directed edges. Each vertex corresponds to a state **x** _∈X_ , and each edge ( **x** _a,_ **x** _b_ ) _∈ E_ represents a valid (collision-free) transition from **x** _a_ to **x** _b_ . 

With a slight abuse of notation, let _c_ ( **x** _a,_ **x** _b_ ) denote the cost of the path between two vertices **x** _a,_ **x** _b ∈ V_ in the tree _T_ . An admissible heuristic estimate of this cost is ˆ _c_ : _V ×V →_ R _≥_ 0, which satisfies 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0003-14.png)


The cost-to-come is _g_ ( **x** ) = _c_ ( **x** _I ,_ **x** ), representing the true cost of the optimal path from the initial vertex **x** _I_ to vertex **x** in the tree. Its admissible heuristic estiˆ ˆ mate is _g_ ( **x** ) = _c_ ( **x** _I ,_ **x** ). Similarly, the cost-to-go is _h_ ( **x** ) = _c_ ( **x** _,_ **x** _G_ ), the true cost of the optimal path from vertex **x** to the goal vertex **x** _G_ . Its admissible 

3 

heuristic estimate is _h_[ˆ] ( **x** ) = _c_ ˆ( **x** _,_ **x** _G_ ). The total cost of the optimal path through **x** is _f_ ( **x** ) = _g_ ( **x** )+ _h_ ( **x** ), and its admissible heuristic estimate is _f_[ˆ] ( **x** ) = _g_ ˆ( **x** )+ _h_[ˆ] ( **x** ). 

## **3.2 Feasible and Optimal Path Planning** 

A planning problem instance is defined by the state space _X_ free, an initial state **x** _I_ , and a goal state **x** _G_ , typically expressed as a tuple ( _X_ free _,_ **x** _I ,_ **x** _G_ ). In general, two types of path planning problems may be considered: the _feasible planning problem_ and the _optimal planning problem_ . We define these below. 

**Definition 1** (Feasible path planning problem) Find a path _π[′] ∈_ Σ from **x** _I_ to **x** _G_ through collision-free space such that 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0004-04.png)


There are usually many solutions to the feasible path planning problem. 

**Definition 2** (Optimal path planning problem) Find a feasible path _π[∗]_ from **x** _I_ to **x** _G_ through collision-free space that minimizes the cost functional _c_ : Σ _→_ R _≥_ 0: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0004-07.png)


A path planning algorithm is considered _robustly feasible_ if there exists a solution path with strong _δ_ - clearance, that is, remaining at least a distance _δ_ from any obstacle in R _[n]_ , for some _δ >_ 0 (Karaman and Frazzoli 2011). A solution path _π[∗]_ is _robustly optimal_ if there exists another path _π_ 0 in the same homotopy class, also with strong _δ_ -clearance, such that _c_ ( _π_ 0) = min _{c_ ( _π_ ) _| π_ is feasible _}_ . Notably, any formal guarantees provided by sampling-based algorithms are typically probabilistic in nature. An algorithm is _probabilistically complete_ if the probability of finding a feasible path (when one exists) approaches one as the number of samples tends to infinity. It is _almost-surely asymptotically optimal_ if the probability that the solution cost converges to the optimal cost approaches one as the number of samples tends to infinity. Asymptotic optimality implies probabilistic completeness. We refer interested readers to Karaman and Frazzoli (2011) for further details. 

## **4 The Greedy Informed Set** 

Informed sampling-based planners focus the search on promising regions of the state space to find better paths once an initial solution has been found. These regions correspond to the _omniscient set Xf_ , the collection of states that could yield a better solution, which is generally unknown because computing it requires solving the problem exactly (Gammell et al. 2018). Heuristic-based estimates, such as the informed 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0004-11.png)


**Fig. 2** : Illustration of the _L_[2] greedy informed set _X_ greedy in a planning problem with a path-length objective in R[2] . The greedy subset (dashed ellipse) is defined by the hypothetical minimum cost _c_ min from the initial state **x** _I_ to the goal state **x** _G_ , and by the heuristic cost of the state along the solution path with the highest admissible value _f_[ˆ] ( **x** max), used as a transverse diameter. 

set _X_ ˆ _f_[,][are][commonly][used][to][approximate] _[X][f]_[.][The] informed set is an admissible over-approximation of the omniscient set, defining a subset of _X_ free where samples are likely to improve the current solution, provided the heuristic never overestimates the true cost. However, in problems with many homotopy classes or in high-dimensional spaces, the heuristic used in _Xf_ ˆ often provides very little information, resulting in an overly large informed set. Consequently, the probability of drawing a random sample from _Xf_ ˆ[that][also] belongs to _Xf_ is low. 

The _greedy informed set_ , introduced by Kyaw et al. (2022), addresses this limitation by eliminating direct dependence on the current solution cost. Instead, it constructs a smaller hyperellipsoid from the states along the current solution path, which is bounded above by the admissible informed set. This section formally defines the greedy informed set and examines how heuristic exploitation in greedy informed sampling influences optimality. We consider only holonomic planning problems in R _[n]_ with a path-length objective under the Euclidean norm (i.e., where all degrees of freedom are directly controllable and the cost depends solely on geometric path length). For any state **x** _∈_ R _[n]_ , let _f_[ˆ] ( **x** ) denote the standard _L_[2] informed heuristic, which provides an admissible lower bound on the cost of any path from the initial state **x** _I_ to the goal state **x** _G_ passing through **x** , 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0004-15.png)


**Definition 3** ( _L_[2] greedy informed set) Let **x** max denote the state along the current solution path _π_ with the maximum admissible heuristic cost, defined by _f_[ˆ] ( _·_ ) in (4), 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0004-17.png)


The _L_[2] _greedy informed set_ , _X_ greedy, is the subset of collision-free states, _X_ free, consisting of all **x** whose heuristic costs are less than or equal to that of the greedily chosen state **x** max along the current solution path (Figure 2), 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0004-19.png)


The greedy informed set is bounded above by the informed set, i.e., _X_ greedy _⊆X_ ˆ _f_[,][and][consequently] yields smaller ellipsoidal regions than the original informed set, especially in high-dimensional problems 

4 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0005-00.png)


**Fig. 3** : Illustration of the current solution path _π_ and another path _π[∗]_ within the same homotopy class, sharing the same initial and goal states, **x** _I_ and **x** _G_ . The greedy informed set _X_ greedy (dashed gray ellipse) is constructed using the maximum heuristic cost along _π_ . The path _π[∗]_ intersects the boundary of _X_ greedy at **x** _a_ and **x** _b_ and passes through a state **x** _c_ that lies outside this set. 

Suppose that _π[∗]_ contains a state **x** _c_ not in _X_ greedy, _∃_ **x** _c ∈ π[∗]_ s.t. **x** _c ∈X/_ greedy _._ (8) 

Since **x** _I ,_ **x** _G ∈X_ greedy, _π[∗]_ must exit the hyperellipsoid at some point and later re-enter it. Consequently, there exist at least two intersection points **x** _a_ and **x** _b_ between _π[∗]_ and the boundary of _X_ greedy. 

Because _π_ and _π[∗]_ are homotopic, they can be continuously deformed into one another without intersecting obstacles while keeping endpoints fixed (Hatcher 2002). The same holds for their subpaths _πab_ and _πabc[∗]_[.][The][cost] of the direct (geodesic) subpath between **x** _a_ and **x** _b_ is strictly less than that of the detour passing through **x** _c_ : 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0005-05.png)


with complex solution paths. Consequently, sampling from this smaller subset increases the likelihood of finding states that also belong to the omniscient set. However, because the greedy informed set is constructed using knowledge from the current solution path—similar to path-biasing methods—an algorithm relying on it may in some cases bias the search toward locally optimal solutions, as the set might exclude portions of the omniscient set. Therefore, continued exploration of other homotopy classes, that is, sampling from the informed set, remains essential for planners utilizing the greedy informed set to preserve asymptotic optimality guarantees. 

Sampling from informed sets is a necessary condition for asymptotic optimality in sampling-based motion planning, since states along the optimal path always lie within these sets (Gammell et al. 2018). The greedy informed set may also contain states from the optimal path, but only if the current solution path and the true optimal path belong to the same homotopy class. In the following, we draw on basic concepts from homotopy theory (Hatcher 2002) to establish the conditions under which an algorithm sampling from the greedy informed set can still converge to the optimal solution (Theorem 1), and to discuss cases where this property may fail to hold (Remark 1). 

**Theorem 1** (Inclusion of the optimal path in the greedy informed set) _Let f_[ˆ] ( _·_ ) _be the L_[2] _heuristic defined in (4). Let π be the current solution path and π[∗] the optimal path between the same initial and goal states_ **x** _I and_ **x** _G. If π and π[∗] lie within the same homotopy class, then every state_ **x** _[∗] ∈ π[∗] satisfies_ 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0005-09.png)


_Consequently, π[∗] ⊆X_ greedy _._ 

_Proof_ Consider the example shown in Figure 3. Let _π_ denote the current solution path in _X_ free from **x** _I_ to **x** _G_ , and let **x** _a_ and **x** _b_ be two states along _π_ with the same maximum heuristic cost, _f_[ˆ] ( **x** _a_ ) = _f_[ˆ] ( **x** _b_ ) = _f_[ˆ] ( **x** max). Let the path _π_ be constructed such that every state **x** _[′]_ on the subpath between **x** _a_ and **x** _b_ also satisfies _f_[ˆ] ( **x** _[′]_ ) = _f_[ˆ] ( **x** max): _∀_ **x** _[′] ∈Z, f_[ˆ] ( **x** _[′]_ ) = _f_[ˆ] ( **x** max) _,_ 

where _Z_ := _{_ **x** _[′] ∈ π[′] | π[′]_ (0) = **x** _a, π[′]_ ( _b_ ) = **x** _b, π[′] ⊂ π}_ . By Definition 3, _X_ greedy is constructed using **x** max of _π_ . We show that the optimal path _π[∗]_ also lies within _X_ greedy if _π_ and _π[∗]_ belong to the same homotopy class. 

By definition, every subpath of an optimal path must also be optimal (Cormen et al. 2022); hence, (9) contradicts the optimality of _π[∗]_ . Therefore, the assumption in (8) is false, and _π[∗] ⊆X_ greedy. □ 

While Theorem 1 establishes that the optimal path _π[∗]_ lies within the greedy informed set _X_ greedy when it shares the same homotopy class as the current solution path _π_ , this guarantee no longer holds when the two paths are homotopically distinct. In such cases, _X_ greedy may fail to include _π[∗]_ , motivating an examination of scenarios where this exclusion occurs. 

**Remark 1** (Non-inclusion of the optimal path in the greedy informed set) _The greedy informed set X_ greedy _does not necessarily contain the optimal path π[∗] if the current solution path and the optimal path lie in different homotopy classes._ 

Remark 1 follows directly from Theorem 1 and can be illustrated with a simple counterexample. Consider a planning problem in a maze-like environment with many homotopy classes between the initial and goal states (Figure 4). Let _π_ be a feasible path that passes through a narrow corridor and requires several sharp turns to navigate around obstacles. In contrast, let _π[∗]_ denote an optimal path in a different homotopy class that avoids the corridor by circumventing the obstacles entirely. By construction, the greedy informed set _X_ greedy is concentrated around the current solution path _π_ , primarily near the narrow passage. 

Since _π_ and _π[∗]_ belong to different homotopy classes, the path _π_ cannot be continuously deformed into _π[∗]_ without intersecting obstacles. Theorem 1 establishes that if _πi_ and _π[∗]_ are homotopic, then _π[∗]_ lies in _X_ greedy. However, in this case, _X_ greedy is restricted to the vicinity of the narrow passage and therefore does not contain _π[∗]_ , which circumvents the obstacles. Thus, in environments of this type, where the current feasible path and the optimal path belong to different homotopy classes, the greedy informed set _X_ greedy may fail to include the optimal path. 

This counterexample highlights an important limitation of relying solely on _X_ greedy. When the optimal path lies in a different homotopy class from the current solution path, sampling exclusively from _X_ greedy can lead to suboptimal performance. Understanding this behaviour is crucial when choosing how frequently 

5 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0006-00.png)


**Fig. 4** : Illustration of the suboptimality of the greedy informed set in an example planning scenario. The greedy informed set _X_ greedy, constructed from the current tortuous solution path _π_ , is shown as a dashed ellipse and the optimal path _π[∗]_ as a dotted line. In this case, _X_ greedy fails to include some states that could improve the current solution cost (i.e., those leading towards _π[∗]_ and lying outside of the hyperellipsoid) due to the nature of its greedy exploitation. 

the planner should sample from _X_ greedy, as the impact of this choice depends on the distribution of homotopy classes and the type of planning problem being addressed. A practical way to mitigate this issue is to also sample from the informed set with some probability (Section 5), thereby balancing exploration and exploitation within the planner. 

## **5 Greedy RRT* (G-RRT*)** 

Greedy RRT* is an almost surely asymptotically optimal path planning algorithm that builds on RRT* and its bi-directional variants (Klemm et al. 2015; Mashayekhi et al. 2020). It maintains two rapidly growing trees—one rooted at the start and the other at the goal—to explore the state space, and employs a greedy connection heuristic to guide them toward each other, similar to RRT-Connect (Kuffner and LaValle 2000). As an RRT*-like algorithm, it incrementally rewires the growing trees to preserve asymptotic optimality. However, rather than sampling randomly throughout the state space, G-RRT* focuses the search on promising regions, once an initial solution is found. Specifically, it employs a greedy version of the informed set introduced in Section 4 to exploit knowledge of the existing solution path and focus subsequent sampling (Figure 5). The complete algorithm is presented in Algorithm blocks 1–5, with modifications to the bi-directional versions of RRT and RRT* highlighted in red. 

## **5.1 Greedy Informed Sampling** 

G-RRT* finds better paths by simultaneously growing two trees, _Ta_ = ( _Va, Ea_ ) from the start and _Tb_ = ( _Vb, Eb_ ) from the goal, consisting of the vertices _Va ∪ Vb_ and edges _Ea ∪ Eb_ , each expanding toward randomly sampled states in the free space. Each tree incrementally rewires nearby vertices to minimize their cost-to-come. Once an initial solution is found, G-RRT* exploits heuristic information from the current solution to bias sampling toward a progressively shrinking hyperellipsoidal region called the greedy informed set. It also samples from the informed subset to maintain exploration and ensure asymptotic optimality. Specifically, the balance between exploration 

**Algorithm 1:** Greedy RRT* ( **x** _I ,_ **x** _G_ ) 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0006-08.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0006-09.png)


**Algorithm 3:** Sample ( **x** _I ,_ **x** _G, c_ max) 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0006-11.png)


and exploitation is controlled by a parameter _ϵ ∈_ [0 _,_ 1], called the _greedy biasing ratio_ . With probability _ϵ_ , the algorithm samples from the greedy informed set to exploit the current best path; with probability 1 _− ϵ_ , it samples from the broader informed subset to encourage exploration and retain asymptotic optimality. Thus, finding a good balance between uniform sampling for exploration and path-biased sampling for exploitation is necessary for G-RRT* to rapidly reduce the search space and achieve faster convergence toward globally optimal solutions. 

6 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0007-00.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0007-01.png)


**----- Start of picture text -----**<br>
(a) (b) (c) (d)<br>**----- End of picture text -----**<br>


**Fig. 5** : Illustrations of the progress of bi-directional sampling-based search performed by the G-RRT* algorithm. The initial and goal states are shown as large black dots, sampled states as small black dots, and the start and goal trees in blue and orange, respectively. The current solution path is highlighted in yellow, and the _L_[2] greedy informed set—the set of states that could yield better solutions—is shown with gray dashed lines. G-RRT* grows two trees rooted at the start and goal (a), where expansion is guided by a greedy connection heuristic that guides the two trees towards each other, producing an initial solution (b). Subsequent sampling is then focused within the greedy informed set to incrementally refine the path (c–d), almost-surely asymptotically converging to the optimal solution. 

## **Algorithm 4:** Extend* ( _T_ = ( _V, E_ ) _,_ **x** ) 

|**A**|**lgorithm 4:** Extend* (_T_ =(_V, E_)_,_**x**)|
|---|---|
|**1 **|**x**nearest _←_Nearest (_T_ = (_V, E_)_,_**x**);|
|**2 **|**x**new _←_Steer (**x**nearest_,_**x**);|
|**3 **|**if** _g_(**x**nearest)+_c_(**x**nearest_,_**x**new)+ˆ_h_(**x**new)_< ci_ **then**|
|**4**|**if** ObstacleFree (**x**nearest_,_**x**new) **then**|
|**5**|_V ←V ∪{_**x**new_}_;|
|**6**|_X_near _←_Near (_T_ = (_V, E_)_,_**x**new_, r_rewire);|
|**7**|**x**min _←_**x**nearest;|
|**8**|**foreach x**near _∈X_near **do**|
|**9**|_c_near _←g_(**x**near) +_c_(**x**near_,_**x**new);|
|**10**|**if** _c_near _< g_(**x**min) +_c_(**x**min_,_**x**new) **then**|
|**11**|**if** ObstacleFree (**x**near_,_**x**new) **then**|
|**12**|**x**min _←_**x**near;|
|**13**|_E ←E ∪{_**x**min_,_**x**new_}_;|
|**14**|**foreach x**near _∈X_near **do**|
|**15**|**if** _g_(**x**new) +_c_(**x**new_,_**x**near)_< g_(**x**near)|
||**then**|
|**16**|**if** ObstacleFree (**x**new_,_**x**near) **then**|
|**17**|**x**parent _←_Parent (**x**near);|
|**18**|_E ←E \ {_(**x**parent_,_**x**near)_}_;|
|**19**|_E ←E ∪{_(**x**new_,_**x**near)_}_;|
|**20**|**if x**new =**x then**|
|**21**|**return** REACHED_,_**x**new;|
|**22**|**else**|
|**23**|**return** ADVANCED_,_**x**new;|
|**24 **|**return** TRAPPED_,_**x**new;|



**Algorithm 5:** Connect* ( _T_ = ( _V, E_ ) _,_ **x** ) 

**1 repeat 2** status _,_ **x** new _←_ Extend* ( _T_ = ( _V, E_ ) _,_ **x** ); **3 until** status _̸_ = ADVANCED; 

nearest vertex to a new vertex is validated only if it can improve the current best solution cost. This gating step also helps G-RRT* to reduce overlap between the two trees, limiting the number of added vertices. G-RRT* prunes the trees as in Gammell et al. (2018), removing vertices whose heuristic values exceed the greedy best heuristic cost. Additionally, because obtaining an initial solution as quickly as possible is important, rewiring is delayed until an initial solution is found. The remaining planning time is then used to rewire to improve solution quality. 

## **6 Analysis** 

This section analyzes the theoretical guarantees of G- RRT*, first establishing its probabilistic completeness in Section 6.1 and then proving asymptotic optimality in Sections 6.2. 

## **6.1 Probabilistic Completeness** 

Since G-RRT* adopts the same tree extension and connection strategy as RRT-Connect, its probabilistic completeness follows directly from the arguments established in Theorem 1 of Kuffner and LaValle (2000). G-RRT* grows two rapidly expanding trees, each of which inherits the probabilistic completeness property of the classical RRT. During the alternating extension process, new vertices are added to the sets _Va_ and _Vb_ of the start and goal trees, respectively, such that the combined set _Vk_ = _Va ∪ Vb_ becomes dense in _X_ free as the number of iterations _k →∞_ . Because the greedy connection heuristic generates all the standard RRT vertices, along with additional ones, it aids in covering _X_ free and therefore does not affect the completeness guarantee. 

## **5.2 Implementation Details** 

G-RRT* employs a balanced search strategy (Kuffner and LaValle 2005) to keep both trees approximately equal in size while maintaining their rapidly exploring behaviour. Since collision checking is computationally expensive in practice, G-RRT* also uses admissible heuristics to gate the vertex extension process (highlighted as red in Algorithm 4). An edge from the 

## **6.2 Asymptotic Optimality** 

G-RRT* uses the greedy informed set _X_ greedy, introduced in Section 4, to focus the search on a subset of the state space. This subset is bounded above by the informed subset, that is, _X_ greedy _⊆X_ ˆ _f_[.][Focus-] ing the search in this way increases the likelihood of sampling states that lie within the omniscent set. 

7 

However, not all states in _X_ greedy are guaranteed to be in the omniscient set (see Figure 4). As a result, some states that could yield better solutions may lie outside the homotopy regions covered by _X_ greedy (Remark 1). Nevertheless, because G-RRT* samples from both _X_ greedy and _Xf_ ˆ[according][to][the][greedy] biasing ratio _ϵ_ (Section 5.1), setting _ϵ <_ 1 is a sufficient condition for preserving asymptotic optimality. 

**Theorem 2** (Worst-case sample complexity for probabilistic optimality) _When sampling with a greedy biasing ratio ϵ, the worst-case number of samples required to achieve_ 1 _probabilistic optimality increases by a factor of_ 1 _−ϵ[relative] to sampling only from the informed set._ 

_Proof_ Let _P_ ( **x** rand _∈Xf_ ) represent the probability of sampling a state from the omniscient set. According to Lemma 5 from Gammell et al. (2018), sampling states from the omniscient set is a necessary condition for improving the current solution in RRT*-like algorithms. Let _P_ ( **x** rand _∈ X_ ˆ _f_[)][represent][the][probability][of][sampling][a][state][from][the] informed set. Since the informed set _Xf_ ˆ[is a superset of the] omniscient set _Xf_ (Gammell et al. 2018), sampling from _X_ ˆ _f_[is][also][a][necessary][condition][for][probabilistic][optimal-] ity, and the probability of doing so is bounded below by the probability of sampling from _Xf_ : 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-03.png)


Thus, the expected number of samples required to improve the current solution to a holonomic problem depends on the probability of sampling the informed set, and is given by: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-05.png)


Recall that with probability 1 _− ϵ_ , we sample from the informed set, and with probability _ϵ_ , we sample from the greedy informed set. Therefore, the overall probability of sampling from _Xf_ ˆ[in][any][given][iteration][is][reduced,] since we do not always sample from _X_ ˆ[Specifically,][the] _f_[.] new probability _P_ new( **x** rand _∈X_ ˆ _f_[)][of][selecting][a][random] sample from _Xf_ ˆ[is:] 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-07.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-08.png)


Comparing (10) and (12): 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-10.png)


Therefore, in the worst case where the greedy informed set does not include states from the optimal solution, the number of samples required for asymptotic optimality increases by a factor of 1 _−_ 1 _ϵ_[compared to only sampling from] _[ X] f_[ ˆ][.] □ 

**Theorem 3** (Expected sample complexity under mixed greedy sampling) _Let the planner sample from the informed set with probability_ 1 _− ϵ and from the greedy_ 

_informed set with probability ϵ. Let γ ∈_ [0 _,_ 1] _denote the fraction of the omniscient set that is contained within the greedy informed set (i.e., the recall of X_ greedy _with respect to Xf ), and let ρ denote the ratio of the volume of the omniscient set to the volume of the informed set. Then the expected number of samples required for probabilistic optimality satisfies_ 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-14.png)


_In particular, E_ [ _n_ new] _< E_ [ _n_ ] _if and only if γ > ρ._ 

_Proof_ Let _λ_ denote the Lebesgue measure on R _[n]_ . Under uniform sampling of the greedy informed set, and following Definition 9 in Gammell et al. (2018), we define _γ_ as the _recall_ of _X_ greedy with respect to the omniscient set: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-17.png)


Similarly, let _ρ_ denote the ratio of the Lebesgue measures of the greedy informed set and the informed set: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-19.png)


We can bound the Lebesgue measure of _X_ ˆ _f_[by the measure] of a prolate hyperspheroid as 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-21.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-22.png)


Similarly, the Lebesgue measure of _X_ greedy is bounded by 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-24.png)


Using (17) and (19), _ρ_ admits the closed form 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-26.png)


Let _P_ ( **x** rand _∈Xf_ ) denote the probability of sampling a state from the omniscient set. According to Lemma 5 from Gammell et al. (2018), sampling states from the omniscient set is a necessary condition for improving the current solution in RRT*-like algorithms. Recall that with probability _ϵ_ , we sample from the greedy informed set, and with probability 1 _− ϵ_ , we sample from the informed set. Therefore, the new probability _P_ new of selecting a random sample from either set that can guarantee improvement is: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-28.png)


Under uniform sampling, each conditional probability can be expressed as a ratio of relative measures. Specifically, 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-30.png)


Since _Xf_ ˆ _[⊇X][f]_[,][as][noted][in][Gammell][et][al.][(2018),][(23)] simplifies to: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0008-32.png)


8 

Expressing (24) in terms of _γ_ and _ρ_ gives: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0009-01.png)


Thus, the expected number of samples required to improve the current solution to a holonomic problem depends on the probability of sampling the informed set as well as on overlap measures between the two sets _Xf_ and _X_ greedy: 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0009-03.png)


In particular, setting _γ_ = 0 in (27) recovers the worst-case factor 1 _/_ (1 _− ϵ_ ), while setting _γ_ = 1 and _ϵ_ = 1 (sampling only from _X_ greedy) yields the best-case factor 1 _/ρ_ . 

## **7 Experiments** 

We evaluated the performance of G-RRT* by comparing it with several state-of-the-art sampling-based planners on abstract problems in R[4] , R[8] , and R[16] (Section 7.1), as well as on robotic manipulation problems in R[7] , R[8] , and R[14] (Section 7.2). The former problems test the planner’s ability to find high-quality solutions in challenging, high-dimensional spaces, whereas the latter assesses performance on realistic robotic tasks. We compared G-RRT* with the Open Motion Planning Library (Sucan et al. 2012, OMPL) implementations of RRT-Connect, RRT*, RRT*-Connect (Klemm et al. 2015), BIT* (Gammell et al. 2020), AIT* (Strub and Gammell 2022), and AORRTC (Wilson et al. 2025). We also included a variant of G-RRT* without the greedy heuristic (denoted by the _†_ symbol) to highlight convergence differences between the informed set and the greedyinformed set. All experiments were conducted using the Planner Developer Tools (Gammell et al. 2022, PDT) and Robowflex (Kingston and Kavraki 2022)[2] . 

All planners were evaluated with the optimization objective of minimizing path length in R _[n]_ . Each planner used the default edge length specified by OMPL, computed as a fixed fraction of the maximum possible distance between any two states in the space. An RGG constant of _η_ = 1 _._ 001 was applied to all planners, and the Euclidean distance (i.e., _L_[2] norm) for path length was used as the admissible cost heuristic. BIT*-based planners used a batch size of 100, and G-RRT* employed a greedy bias ratio of _ϵ_ = 0 _._ 9 to encourage exploitation across all experiments. Notably, AORRTC internally applies path simplification—specifically, randomized shortcutting (Geraerts and Overmars 2007; Hauser and Ng-Thow-Hing 2010) and B-spline smoothing (Pan et al. 2012)—as part of its planning process to improve 

> 2Simulations were performed in an Ubuntu 20.04 Docker container on an Intel Core i7-10875H CPU with 40 GB of RAM; all planners were implemented in C++. 

solution quality. To ensure a fair comparison, and because all reported times and costs for AORRTC include this simplification, we applied the same procedure to all planners as a post-processing step _only_ : (i) after an initial solution had been found, and (ii) for the final solution at the end of the planning time limit. The costs of these post-processed, simplified paths are reported separately.[3] 

## **7.1 Abstract Planning Problems** 

The planners were tested on three simulated planning problems in R[4] , R[8] , and R[16] . To provide some intuition, these problems are illustrated in two dimensions in Figure 6. The R[2] versions are shown only for visualization purposes, since they are too simple to differentiate planner performance in a meaningful way. The higher-dimensional problem instances were created by extending the same obstacle layouts uniformly along each additional dimension. The first problem consists of many axis-aligned hypercubes, with the start and goal located at [ _−_ 0 _._ 25 _,_ 0 _, . . . ,_ 0] _[⊤]_ and [0 _._ 25 _,_ 0 _, . . . ,_ 0] _[⊤]_ , respectively (Figure 6a). The second problem contains a wall with a narrow passage gap, such that only two homotopy classes in all dimensions (Figure 6b), with start and goal at [ _−_ 0 _._ 3 _,_ 0 _, . . . ,_ 0] _[⊤]_ and [0 _._ 3 _,_ 0 _, . . . ,_ 0] _[⊤]_ . The final problem includes two hollow, axis-aligned hypercubes with an opening, enclosing the start and goal, located at [ _−_ 0 _._ 3 _,_ 0 _, . . . ,_ 0] _[⊤]_ and [0 _._ 3 _,_ 0 _, . . . ,_ 0] _[⊤]_ , respectively (Figure 6c). 

Each planner was allocated a planning time proportional to the difficulty of the problem and the dimensionality of the state space. We ran 100 trials for the first two problems and 50 for the last, each initialized with a different pseudorandom seed. During each trial, solution costs were recorded at fixed time intervals (10 _[−]_[4] s) by a separate monitoring thread. If no solution was found at a given time, the cost was assigned an infinite value. We then reported the median costs to mitigate any bias from unsolved trials. Figure 7 shows each planner’s median solution cost and success rate over computation time. To ensure a fair comparison with AORRTC, we also applied path simplification to all of the initial and final solutions, as summarized in Table 1. 

The results highlight the importance of maintaining two rapidly growing trees to quickly find initial solutions in high-dimensional problems. G-RRT* discovers initial solutions as fast as RRT-Connect across all tested problems. Unlike RRT-Connect, G-RRT* is an anytime algorithm that converges asymptotically to optimal solutions. From Figure 7, we observe that AORRTC reports lower median solution costs than G-RRT* because its paths are already simplified. However, G-RRT* reaches the same final solution costs as AORRTC, and does so faster than AORRTC and all other asymptotically optimal planners, 

> 3Simplification was evaluated only in separate post-processing experiments and did not affect convergence; the simplified paths were not reused during planning. 

9 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0010-00.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0010-01.png)


**----- Start of picture text -----**<br>
(a) (b) (c)<br>**----- End of picture text -----**<br>


**Fig. 6** : Two-dimensional illustrations of the abstract planning problems examined in Section 7.1. These include complex planning problems containing (a) many homotopy classes, (b) narrow passage gap environment, and (c) double enclosures, with a problem domain of size _l_ = 1. The **x** _I_ and **x** _G_ represent the initial and goal states, respectively. 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0010-03.png)


**----- Start of picture text -----**<br>
100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>1 . 2<br>2<br>1<br>0 . 8<br>0 . 6 1<br>0 . 4<br>10 [−] [2] 10 [−] [1] 10 [0] 10 [−] [2] 10 [−] [1] 10 [0] 10 [1]<br>Computation time [s] Computation time [s]<br>100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>4 4<br>3<br>2<br>2<br>10 [−] [2] 10 [−] [1] 10 [0] 10 [−] [2] 10 [−] [1] 10 [0] 10 [1]<br>Computation time [s] Computation time [s]<br>100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>4 8<br>3 6<br>4<br>2<br>2<br>10 [−] [1] 10 [0] 10 [1] 10 [1] 10 [2]<br>Computation time [s] Computation time [s]<br>RRT-C RRT* RRT*-C BIT* AIT* AORRTC G-RRT* [†] G-RRT*<br>[%] [%]<br>Success Success<br>Cost Cost<br>[%] [%]<br>Success Success<br>Cost Cost<br>[%] [%]<br>Success Success<br>Cost Cost<br>**----- End of picture text -----**<br>


**Fig. 7** : Planner performance versus runtime on the abstract planning problems described in Section 7.1. The success plots show the percentage of successful runs over time, while the cost plots present the median solution cost versus runtime for each planner. Error bars and shaded regions denote non-parametric 99% confidence intervals on the median. The top and middle rows show the many-homotopy-class and narrowpassage-gap experiments for R[8] (left) and R[16] (right), respectively, while the bottom row shows the double-enclosure experiment for R[4] (left) and R[8] (right). Reported times and costs for AORRTC include path simplification, i.e., randomized shortcutting and B-spline smoothing. 

even _without_ path simplification. These results demonstrate the effectiveness of greedy informed sampling. Moreover, as shown in Table 1, when the same simplification process is applied uniformly to all planners, their initial solution costs become similar; yet G-RRT* consistently yields lower final solution costs for most problems. Simplification improves path quality only locally, G-RRT* achieves global improvement through RRT*-style rewiring combined with its greedy biasing strategy. 

Some of the most constrained problems further illustrate the strengths of G-RRT*. In the narrow passage gap problem, all asymptotically optimal planners struggle to find a path through the passage, yet G- RRT* is the only one that consistently succeeds within the available time budget. This demonstrates the effectiveness of the greedy informed set relative to the informed sets used in G-RRT* _[†]_ and AORRTC. 

In the more difficult _bug trap_ scenario involving double enclosures symmetric about the start and goal, 

10 

**Table 1** : Initial and final median solution costs for each planner on the abstract planning problems described in Section 7.1. Costs are shown after randomized shortcutting and B-spline smoothing. Lower values indicate better performance, with the best cost in **bold** and the secondbest underlined. 

||**many homotopy classes**<br>R8<br>R16<br>_c_init<br>_c_fnal<br>_c_init<br>_c_fnal|**many homotopy classes**<br>R8<br>R16<br>_c_init<br>_c_fnal<br>_c_init<br>_c_fnal|**narrow pa**<br>R8<br>_c_init<br>_c_fnal|**ssage gap**<br>R16<br>_c_init<br>_c_fnal|**double enclosure**<br>R4<br>R8<br>_c_init<br>_c_fnal<br>_c_init<br>_c_fnal|**double enclosure**<br>R4<br>R8<br>_c_init<br>_c_fnal<br>_c_init<br>_c_fnal|
|---|---|---|---|---|---|---|
|RRT-C|0.511<br>0.511|0.694<br>0.694|1.384<br>1.384|2.075<br>2.075|1.547<br>1.547|1.806<br>1.806|
|RRT*|_∞_<br>_∞_|_∞_<br>_∞_|1.412<br>1.304|_∞_<br>_∞_|1.552<br>1.500|_∞_<br>_∞_|
|RRT*-C|0.494<br>0.479|0.564<br>0.525|1.384<br>1.302|1.862<br>1.749|1.491<br>1.479|_∞_<br>_∞_|
|BIT*|0.495<br>0.447|0.595<br>0.463|1.315<br>0.982|1.871<br>1.431|1.485<br>1.452|_∞_<br>_∞_|
|AIT*|**0.491**<br>0.448|0.584<br>0.467|**1.307**<br>1.032|1.838<br>1.563|**1.480**<br>1.457|_∞_<br>_∞_|
|AORRTC|0.497<br>**0.443**|**0.549**<br>**0.450**|1.385<br>0.661|1.829<br>1.346|1.567<br>1.464|1.803<br>1.724|
|G-RRT*_†_|0.505<br>0.447|0.588<br>0.454|1.392<br>0.771|1.861<br>1.033|1.568<br>1.465|1.833<br>1.703|
|G-RRT*|0.508<br>**0.443**|0.573<br>0.451|1.369<br>**0.655**|**1.828**<br>**1.019**|1.536<br>**1.451**|**1.784**<br>**1.643**|




![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0011-02.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0011-03.png)



![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0011-04.png)


**----- Start of picture text -----**<br>
(a) Start configuration (b) Goal configuration<br>**----- End of picture text -----**<br>


**Fig. 8** : A dual-arm manipulation problem for the Barrett WAM Arm in R[14] . Starting with (a) both arms pointing in the same direction (a), they must be moved to (b) extend in opposite directions without hitting the cage. 

all planners struggled as dimensionality increased. Only G-RRT*, G-RRT* _[†]_ , RRT-Connect, and AORRTC solved more than half of the trials, emphasizing the importance of maintaining two greedily connecting trees in domains with several biased Voronoi regions (Yershova et al. 2005). Nevertheless, after simplification, G-RRT* achieves lower median costs than competing planners, confirming its ability to find higher-quality solutions within the allotted planning time. 

## **7.2 Manipulation Problems** 

The planners were also evaluated on manipulation tasks from the MotionBenchMaker dataset (Chamzas et al. 2021), using the Panda (R[7] ) and Fetch (R[8] ) robot platforms. The dataset provides a standardized set of seven manipulation benchmarks across multiple robot models, each containing 100 planning problems with varying start and goal configurations and workspace obstacles. For each robot, we selected four environments of increasing difficulty— _bookshelf thin_ , _table pick_ , _box_ , and _cage_ —ranging from relatively open reaching motions to tightly constrained scenarios (Figure 9). In addition, the planners were evaluated on a more challenging, higher-dimensional dual-arm manipulation task involving two Barrett WAM arms with a combined 14 degrees of freedom (R[14] ) in the Open Robotics Automation Virtual Environment (Diankov 2010), as shown in Figure 8. The objective is to move the arms from an initial configuration, where they point in the forward direction, 

to a goal configuration where they are extended outward in opposite directions, without colliding with the surrounding cage. OpenRAVE was configured to use the Flexible Collision Library (Pan et al. 2012, FCL) with a collision-checking resolution of 10 _[−]_[2] . Performance results for all planners, optimizing path length in R _[n]_ , are presented in Figures 10 and 11, with post-simplification statistics summarized in Table 2. 

The observed performance trends closely match those of the abstract problems discussed in Section 7.1. G-RRT* finds initial solutions as quickly as RRT-Connect and then uses the remaining planning time to converge toward optimality. In most planning problems from the MotionBenchMaker dataset, G-RRT* achieves final solution costs comparable to those of AORRTC, but does so _without_ requiring any path simplification—indicating faster convergence relative to the other asymptotically optimal planners. In very constrained problems such as _bookshelf thin_ and _cage_ for Fetch, however, all planners struggle to find feasible paths within the time limit. As a result, G-RRT* spends less time rewiring, leading to slightly higher solution costs than AORRTC. Notably, for the dual-arm problem, G-RRT* not only finds solutions faster but also produces the lowest final costs after simplification, highlighting the benefit of the greedy heuristic for high-dimensional planning problems. 

## **8 Conclusion** 

In this paper, we build on our earlier introduction of the greedy informed set (Kyaw et al. 2022), and provide the first formal analysis of its behaviour within sampling-based planners. We show that the greedy informed set contains all states along the optimal path whenever the current and optimal solutions share the same homotopy class. Conversely, when the two paths belong to different homotopy classes, exclusively relying on the greedy informed set can prevent convergence to the global optimum. These findings highlight the need to appropriately balance greedy exploitation with broader exploration through the full informed set to preserve asymptotic optimality. To this end, 

11 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0012-00.png)


**Fig. 9** : Manipulation problems from the MotionBenchMaker dataset used in our experiments (see Section 7.2). Each row shows a different robot platform (Panda or Fetch) evaluated on four benchmark tasks: _bookshelf thin_ , _table pick_ , _box_ , and _cage_ . 

**Table 2** : Initial and final median solution costs for each planner on the manipulation problems described in Section 7.2. Costs are shown after randomized shortcutting and B-spline smoothing. Lower values indicate better performance, with the best cost in **bold** and the second-best underlined. 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0012-03.png)


**----- Start of picture text -----**<br>
bookshelf thin table pick box cage dual-arm (R [14] )<br>c init c final c init c final c init c final c init c final c init c final<br>RRT-C 4.617 4.617 4.651 4.651 5.414 5.414 8.028 8.028 RRT-C 11.864 11.864<br>RRT* 4.996 4.915 4.534 4.532 ∞ ∞ ∞ ∞ RRT* ∞ ∞<br>RRT*-C 4.565 4.436 4.553 4.457 4.812 4.411 7.591 7.408 RRT*-C 11.562 10.017<br>BIT* 4.501 4.402 4.527 4.497 4.851 4.318 ∞ ∞ BIT* 12.890 8.618<br>AIT* 4.543 4.523 4.683 4.564 4.919 4.569 ∞ ∞ AIT* 12.017 8.708<br>AORRTC 4.471 4.315 4.553 4.342 5.202 4.149 7.876 5.189 AORRTC 12.162 7.028<br>G-RRT* [†] 4.565 4.251 4.571 4.326 5.099 3.800 8.014 7.116 G-RRT* [†] 11.801 9.003<br>G-RRT* 11.988 6.707<br>G-RRT* 4.564 4.229 4.564 4.315 5.031 3.778 8.014 5.258<br>RRT-C 11.872 11.872 9.207 9.207 10.804 10.804 14.646 14.646<br>RRT* ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞<br>RRT*-C ∞ ∞ 8.072 6.713 9.609 7.895 12.691 12.379<br>BIT* ∞ ∞ 7.544 6.657 8.782 7.703 ∞ ∞<br>AIT* ∞ ∞ 7.323 6.578 8.650 7.778 ∞ ∞<br>AORRTC 11.312 8.526 8.900 6.001 10.593 7.046 13.934 7.826<br>G-RRT* [†] 11.353 9.871 8.846 5.690 10.596 7.023 14.358 12.145<br>G-RRT* 11.237 9.523 8.703 5.576 10.347 6.827 14.230 11.898<br>)<br>7(R<br>Panda<br>)<br>8(R<br>Fetch<br>**----- End of picture text -----**<br>


we present G-RRT*, an algorithm that uses bidirectional search to quickly find initial solutions and then leverages the greedy informed set to focus the subsequent search, while preserving asymptotic optimality guarantees. 

We evaluate G-RRT* on both abstract planning problems and manipulation tasks across a range of dimensions. Our results show that G-RRT* finds initial solutions as quickly as RRT-Connect and then uses the remaining planning time to improve them, converging faster than all other asymptotically optimal planners. It achieves these gains _without_ relying on path simplification, unlike AORRTC, and applying simplification as a post-processing step yields even lower solution costs. Overall, the experiments demonstrate that incorporating greedy informed sampling can substantially accelerate convergence to highquality solutions in informed planners. 

There are several promising directions for future work. Because G-RRT* currently draws a single sample per iteration, extending greedy informed sampling to batched updates, as in BIT*, could further improve performance. Additionally, we are investigating ways to define and exploit promising regions of the state space; focusing sampling on these regions may improve both the efficiency and convergence rate of sampling-based motion planners for high-dimensional problems. 

**Acknowledgements.** The authors would like to thank Yunfan Lu for dedicating time to assist with the proofs in this manuscript. 

## **References** 

- Akgun, B. and M. Stilman 2011. Sampling heuristics for optimal motion planning in high dimensions. In _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 2640–2645. 

12 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0013-00.png)


**----- Start of picture text -----**<br>
100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>30<br>10 20<br>10<br>5<br>10 [−] [1] 10 [0] 10 [−] [1] 10 [0]<br>Computation time [s] Computation time [s]<br>(a) bookshelf (Panda) (b) table (Panda)<br>100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>30<br>40<br>20<br>20<br>10<br>0<br>10 [−] [1] 10 [0] 10 [−] [1] 10 [0] 10 [1]<br>Computation time [s] Computation time [s]<br>(c) box (Panda) (d) cage (Panda)<br>100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>40<br>20<br>20<br>10<br>10 [−] [1] 10 [0] 10 [1] 10 [−] [1] 10 [0] 10 [1]<br>Computation time [s] Computation time [s]<br>(e) bookshelf (Fetch) (f) table (Fetch)<br>100 100<br>75 75<br>50 50<br>25 25<br>0 0<br>40<br>40<br>20 20<br>10 [−] [1] 10 [0] 10 [1] 10 [−] [1] 10 [0] 10 [1]<br>Computation time [s] Computation time [s]<br>(g) box (Fetch) (h) cage (Fetch)<br>RRT-C RRT* RRT*-C BIT* AIT* AORRTC G-RRT* [†] G-RRT*<br>[%] [%]<br>Success Success<br>Cost Cost<br>[%] [%]<br>Success Success<br>Cost Cost<br>[%] [%]<br>Success Success<br>Cost Cost<br>[%] [%]<br>Success Success<br>Cost Cost<br>**----- End of picture text -----**<br>


**Fig. 10** : Planner performance versus running time on the Panda (R[7] ) and Fetch (R[8] ) problems from the MotionBenchMaker dataset (see Section 7.2 and Figure 9). The success plots show the percentage of successful runs over time, while the cost plots present the median solution cost versus runtime for each planner. Error bars and shaded regions denote non-parametric 99% confidence intervals on the median. Reported times and costs for RRT-Connect and AORRTC include path simplification, i.e., randomized shortcutting and B-spline smoothing. 

- Alterovitz, R., S. Patil, and A. Derbakova 2011. Rapidly-Exploring Roadmaps: Weighing exploration vs. refinement in optimal motion planning. In _2011 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 3706–3712. 

- Arslan, O. and P. Tsiotras 2013. Use of relaxation methods in sampling-based algorithms for optimal motion planning. In _2013 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2421–2428. 

- Bialkowski, J., M. Otte, and E. Frazzoli 2013. Freeconfiguration biased sampling for motion planning. In _2013 IEEE/RSJ International Conference on_ 

_Intelligent Robots and Systems (IROS)_ , pp. 1272– 1279. 

- Chamzas, C., C. Quintero-Pena, Z. Kingston, A. Orthey, D. Rakita, M. Gleicher, M. Toussaint, and L.E. Kavraki. 2021. MotionBenchMaker: A tool to generate and benchmark motion planning datasets. _IEEE Robotics and Automation Letters 7_ (2): 882–889. 

- Cormen, T.H., C.E. Leiserson, R.L. Rivest, and C. Stein. 2022. _Introduction to Algorithms_ . MIT Press. 

- Diankov, R. 2010. Automated construction of robotic manipulation programs. _PhD Thesis, Robotics_ 

13 


![](1_survey/papers/md/Kyaw2024Greedy_figs/Kyaw2024Greedy.pdf-0014-00.png)


**----- Start of picture text -----**<br>
100<br>75<br>50<br>25<br>0<br>60<br>40<br>20<br>10 [−] [1] 10 [0] 10 [1] 10 [2]<br>Computation time [s]<br>RRT-C RRT* RRT*-C BIT* AIT* AORRTC G-RRT* [†] G-RRT*<br>[%]<br>Success<br>Cost<br>**----- End of picture text -----**<br>


**Fig. 11** : Planner performance versus runtime on the dual-arm problem described in Section 7.2 (see Figure 8). The success plots show the percentage of successful runs over time, and the cost plots present the median solution cost versus runtime for each planner. Error bars and shaded regions denote non-parametric 99% confidence intervals on the median. Each planner was run for 50 trials with a runtime limit of 100 s in R[14] . Reported times and costs for AORRTC include path simplification, i.e., randomized shortcutting and B-spline smoothing. 

_Institute, Carnegie Mellon University, Pittsburgh, PA_ . 

- Dobson, A. and K.E. Bekris. 2014. Sparse roadmap spanners for asymptotically near-optimal motion planning. _The International Journal of Robotics Research 33_ (1): 18–47. 

- Elbanhawi, M. and M. Simic. 2014. Sampling-based robot motion planning: A review. _IEEE Access_ 2: 56–77. 

- Faroni, M., N. Pedrocchi, and M. Beschi. 2024. Adaptive hybrid local-global sampling for fast informed sampling-based optimal path planning. _Autonomous Robots 48_ (2): 6. 

- Ferguson, D. and A. Stentz 2006. Anytime RRTs. In _2006 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 5369–5375. 

- Gammell, J.D., T.D. Barfoot, and S.S. Srinivasa. 2018. Informed sampling for asymptotically optimal path planning. _IEEE Transactions on Robotics 34_ (4): 966–984. 

- Gammell, J.D., T.D. Barfoot, and S.S. Srinivasa. 2020. Batch Informed Trees (BIT*): Informed asymptotically optimal anytime search. _The International Journal of Robotics Research 39_ (5): 543–567. 

- Gammell, J.D., S.S. Srinivasa, and T.D. Barfoot 2014. Informed RRT*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic. In _2014 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 2997–3004. 

- Gammell, J.D., M.P. Strub, and V.N. Hartmann 2022. Planner Developer Tools (PDT): Reproducible experiments and statistical analysis for developing and testing motion planners. In _Proceedings of the Workshop on Evaluating Motion Planning Performance (EMPP), 2022 IEEE/RSJ_ 

_International Conference on Intelligent Robots and Systems (IROS)_ . 

- Geraerts, R. and M.H. Overmars. 2007. Creating high-quality paths for motion planning. _The International Journal of Robotics Research 26_ (8): 845–863. 

- Hatcher, A. 2002. _Algebraic topology_ . Cambridge University Press. 

- Hauser, K. and V. Ng-Thow-Hing 2010. Fast smoothing of manipulator trajectories using optimal bounded-acceleration shortcuts. In _2010 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2493–2498. 

- Hsu, D., L.E. Kavraki, J.C. Latombe, R. Motwani, S. Sorkin, et al. 1998. On finding narrow passages with probabilistic roadmap planners. In _Robotics: The Algorithmic Perspective: 1998 Workshop on the Algorithmic Foundations of Robotics (WAFR)_ , pp. 141–154. 

- Islam, F., J. Nasir, U. Malik, Y. Ayaz, and O. Hasan 2012. RRT*-Smart: Rapid convergence implementation of RRT* towards optimal solution. In _2012 IEEE International Conference on Mechatronics and Automation (ICMA)_ , pp. 1651–1656. 

- Jeong, I.B., S.J. Lee, and J.H. Kim. 2019. QuickRRT*: Triangular inequality-based implementation of RRT* with improved initial solution and convergence rate. _Expert Systems with Applications_ 123: 82–90. 

- Jiang, H., Q. Chen, Y. Zheng, and Z. Xu 2020. Informed RRT* with adjoining obstacle process for robot path planning. In _2020 IEEE 20th International Conference on Communication Technology (ICCT)_ , pp. 1471–1477. 

- Karaman, S. and E. Frazzoli. 2011. Sampling-based algorithms for optimal motion planning. _The International Journal of Robotics Research 30_ (7): 846–894. 

- Karaman, S., M.R. Walter, A. Perez, E. Frazzoli, and S. Teller 2011. Anytime motion planning using the RRT. In _2011 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1478–1483. 

- Kavraki, L.E., P. Svestka, J.C. Latombe, and M.H. Overmars. 1996. Probabilistic roadmaps for path planning in high-dimensional configuration spaces. _IEEE Transactions on Robotics and Automation 12_ (4): 566–580. 

- Khatib, O. 1986. Real-time obstacle avoidance for manipulators and mobile robots. _The International Journal of Robotics Research 5_ (1): 90–98. 

14 

- Kim, D., J. Lee, and S.e. Yoon 2014. Cloud RRT*: Sampling cloud based RRT*. In _2014 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2519–2526. 

- Kim, M.C. and J.B. Song 2015. Informed RRT* towards optimality by reducing size of hyperellipsoid. In _2015 IEEE International Conference on Advanced Intelligent Mechatronics (AIM)_ , pp. 244–248. 

- Kingston, Z. and L.E. Kavraki 2022. Robowflex: Robot motion planning with MoveIt made easy. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 3108–3114. 

- Klemm, S., J. Oberl¨ander, A. Hermann, A. Roennau, T. Schamm, J.M. Zollner, and R. Dillmann 2015. RRT*-Connect: Faster, asymptotically optimal motion planning. In _2015 IEEE International Conference on Robotics and Biomimetics (ROBIO)_ , pp. 1670–1677. 

- Kuffner, J. and S. LaValle. 2005. An efficient approach to path planning using balanced bidirectional RRT search. _Robotics Institute, Carnegie Mellon University, Pittsburgh, PA, USA. Technical Report CMU-RI-TR-05-34_ . 

- Kuffner, J.J. and S.M. LaValle 2000. RRT-Connect: An efficient approach to single-query path planning. In _Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No. 00CH37065)_ , Volume 2, pp. 995–1001. 

- Kyaw, P.T., A.V. Le, P. Veerajagadheswar, M.R. Elara, T.T. Thu, N.H.K. Nhan, P. Van Duc, and M.B. Vu. 2022. Energy-efficient path planning of reconfigurable robots in complex environments. _IEEE Transactions on Robotics 38_ (4): 2481–2494. 

- LaValle, S.M. 2006. _Planning algorithms_ . Cambridge University Press. 

- LaValle, S.M. and J.J. Kuffner Jr. 2001. Randomized kinodynamic planning. _The International Journal of Robotics Research 20_ (5): 378–400. 

- Li, Y., W. Wei, Y. Gao, D. Wang, and Z. Fan. 2020. PQ-RRT*: An improved path planning algorithm for mobile robots. _Expert systems with applications_ 152: 113425. 

## method. _IEEE Access_ 8: 19842–19852. 

   - Otte, M. and N. Correll. 2013. C-FOREST: Parallel shortest path planning with superlinear speedup. _IEEE Transactions on Robotics 29_ (3): 798–806. 

   - Pan, J., S. Chitta, and D. Manocha 2012. FCL: A general purpose library for collision and proximity queries. In _2012 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 3859–3866. 

   - Pan, J., L. Zhang, and D. Manocha. 2012. Collisionfree and smooth trajectory computation in cluttered environments. _The International Journal of Robotics Research 31_ (10): 1155–1175. 

   - Qureshi, A.H. and Y. Ayaz. 2016. Potential functions based sampling heuristic for optimal path planning. _Autonomous Robots_ 40: 1079–1093. 

   - Reif, J.H. 1979. Complexity of the mover’s problem and generalizations. In _20th Annual Symposium on Foundations of Computer Science (SFCS 1979)_ , pp. 421–427. 

   - Salzman, O. and D. Halperin. 2016. Asymptotically near-optimal RRT for fast, high-quality motion planning. _IEEE Transactions on Robotics 32_ (3): 473–483. 

   - Strub, M.P. and J.D. Gammell. 2022. Adaptively Informed Trees (AIT*) and Effort Informed Trees (EIT*): Asymmetric bidirectional sampling-based path planning. _The International Journal of Robotics Research 41_ (4): 390–417. 

   - Sucan, I.A., M. Moll, and L.E. Kavraki. 2012. The open motion planning library. _IEEE Robotics & Automation Magazine 19_ (4): 72–82. 

   - Wilson, T.S., W. Thomason, Z. Kingston, and J.D. Gammell. 2025. AORRTC: Almost-surely asymptotically optimal planning with RRT-Connect. _IEEE Robotics and Automation Letters 10_ (12): 13375–13382. 

   - Yershova, A., L. Jaillet, T. Sim´eon, and S.M. LaValle 2005. Dynamic-Domain RRTs: Efficient exploration by controlling the sampling domain. In _Proceedings of the 2005 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 3856–3861. 

- Liao, B., F. Wan, Y. Hua, R. Ma, S. Zhu, and X. Qing. 2021. F-RRT*: An improved path planning algorithm with improved initial solution and convergence rate. _Expert Systems with Applications_ 184: 115457. 

- Mashayekhi, R., M.Y.I. Idris, M.H. Anisi, I. Ahmedy, and I. Ali. 2020. Informed RRT*-Connect: An asymptotically optimal single-query path planning 

15 

