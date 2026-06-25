---
citation_key: Choudhury2017Datadriven
arxiv_id: 1711.06391
arxiv_url: https://arxiv.org/abs/1711.06391
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:05:05Z
origin: ai+web
reviewed: false
---

# Introduction

Motion planning, the task of computing a sequence of collision-free motions for a robotic system from a start to a goal configuration, has a rich and varied history [@Lav06]. Up until now, the bulk of the prominent research has focused on the development of tractable planning algorithms with provable *worst-case performance guarantees* such as computational complexity [@canny1988complexity], probabilistic completeness [@lavalle2001randomized] or asymptotic optimality [@karaman2011sampling]. In contrast, analysis of the *expected performance* of these algorithms on real world planning problems a robot encounters has received considerably less attention, primarily due to the lack of standardized datasets or robotic platforms.

Informative path planning, the task of computing an optimal sequence of sensing locations to visit so as to maximize information gain, has also had an extensive amount of prior work on algorithms with provable worst-case performance guarantees such as computational complexities  [@singh2007efficient] and the probabilistic completeness [@hollinger2013sampling] of information theoretic planning. While these algorithms use heuristics to approximate information gain using variants of Shannon's entropy, their expected performance on real world planning problems is heavily influenced by the geometric distribution of objects encountered in the world.

:::: {#fig:marquee .figure latex-placement="!t"}
![](Choudhury2017Datadriven_figs/marquee.png){width="\\textwidth"}

::: caption
Sequential decision making in informative path planning and search based planning. The implicit structure of the environment affects the performance of policies in both tasks. (a) The effectiveness of a policy to gather information depends on the distribution of worlds. (left) When the distribution corresponds to a scene containing ladders, the learnt policy executes a helical motion around parts of the ladder already observed as it is unlikely that there is information elsewhere. (right) When the distribution corresponds to a scene from a construction site, the learnt policy executes a large sweeping motion as information is likely to be dispersed. (b) A learnt heuristic policy adapts to different obstacle configurations to minimize search effort. All schematics show the evolution of a search algorithm as the expansion of a search wavefront (expanded(white), invalid(black), unexpanded(grey)) from start (green) to goal (blue). A commonly used inflated Euclidean heuristic cannot adapt to different environments, e.g it gets stuck in bugtraps. On the other hand, the learnt policy is able to infer the presence of a bug trap when trained on such a distribution and switch to greedy behaviour when trained on other distributions. []{#fig:marquee label="fig:marquee"}
:::
::::

A unifying theme for both these problem domains is that as robots break out of contrived laboratory settings and operate in the real world, the scenarios encountered by them vary widely and have a significant impact on performance. Hence, a key requirement for autonomous systems is a *robust planning module* that maintains *consistent performance* across the diverse range of scenarios it is likely to encounter. To do so, planning modules must possess the ability to leverage information about the implicit structure of the world in which the robot operates and adapt the planning strategy accordingly. Moreover, this must occur in a pure *data-driven fashion* without the need for human intervention. Fortunately, recent advances in affordable sensors and actuators have enabled mass deployment of robots that navigate, interact and collect real data. This motivates us to examine the following question:

::: displayquote
How can we design planning algorithms that, subject to on-board computation and sensing constraints, maximize their expected performance on the actual distribution of problems that a robot encounters?
:::

## Motivation

We look at two domains - informative path planning and search based planning. We briefly delve into these motivations and make the case for data-driven approaches in both.

### Informative Path Planning

We consider the following information gathering problem - given a hidden world map, sampled from a prior distribution, the goal is to successively visit sensing locations such that the amount of relevant information uncovered is maximized while not exceeding a specified fuel budget. This problem fundamentally recurs in mobile robot applications such as autonomous mapping of environments using ground and aerial robots [@Charrow-RSS-15; @heng2015efficient], monitoring of water bodies [@hollinger2013sampling] and inspecting models for 3D reconstruction [@isler2016information; @hollinger2011active].

The nature of "interesting" objects in an environment and their spatial distribution influence the optimal trajectory a robot might take to explore the environment. As a result, it is important that a robot learns about the type of environment it is exploring as it acquires more information and adapts its exploration trajectories accordingly.

To illustrate our point, we sketch out two extreme examples of environments for a particular mapping problem, shown in Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"}(a). Consider a robot equipped with a sensor (RGBD camera) that needs to generate a map of an unknown environment. It is given a prior distribution about the geometry of the world, but has no other information. This geometry could include very diverse settings. First it can include a world where there is only one ladder, but the form of the ladder must be explored, which is a very dense setting. Second, it could include a sparse setting with spatially distributed objects, such as a construction site.

The important task for the robot is to now try to infer which type of environment it is in based on the history of measurements, and thus plan an efficient trajectory. At every time step, the robot visits a sensing location and receives a sensor measurement (e.g. depth image) that has some amount of information utility (e.g. surface coverage of objects with point cloud). As opposed to naive lawnmower-coverage patterns, it will be more efficient if the robot could use a policy that maps the history of locations visited and measurements received to decide which location to visit next such that it maximizes the amount of information gathered in the finite amount of battery time available.

The ability of such a learnt policy to gather information efficiently depends on the prior distribution of worlds in which the robot has been shown how to navigate optimally. Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"}(a) (left) shows an efficient learnt policy for inspecting a ladder, which executes a helical motion around parts of the ladder already observed to efficiently uncover new parts without searching naively. This is efficient because given the prior distribution the robot learns that information is likely to be geometrically concentrated in a particular volume given its initial observations of parts of the ladder. Similarly Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"}(a) (right) shows an effective policy for exploring construction sites by executing large sweeping motions. Here again the robot learns from prior experience that wide, sweeping motions are efficient since it has learnt that information is likely to be dispersed in such scenarios. We wish to arrive at an efficient procedure for training such a policy.

### Search Based Planning

Search based motion planning offers a comprehensive framework for reasoning about a vast number of motion planning algorithms [@Lav06]. In this framework, an algorithm grows a *search tree* of feasible robot motions from a start configuration towards a goal [@pearl1984heuristics]. This is done in an incremental fashion by first selecting a leaf node of the tree, *expanding* this node by computing outgoing edges, checking each edge for validity and finally updating the tree with potentially new leaf nodes. It is useful to visualize this search process as a *wavefront of expanded nodes* that grows from the start outwards till it finds the goal as illustrated in Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"}(b).

This paper addresses a class of robotic motion planning problems where edge evaluation dominates the search effort, such as for robots with complex geometries like robot arms [@dellin2016guided] or for robots with limited onboard computation like UAVs [@cover2013sparse]. In order to ensure real-time performance, algorithms must prioritize minimizing the search effort, i.e. keeping the volume of the search wavefront as small as possible while it grows towards the goal. This is typically achieved by heuristics, which guide the search towards promising areas by selecting which nodes to expand. As shown in Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"}, this acts as a force stretching the search wavefront towards the goal.

A good heuristic must balance the bi-objective criteria of finding a good solution and minimizing the search effort. The bulk of the prior work has focused on the former objective of guaranteeing that the search returns a near-optimal solution [@pearl1984heuristics]. These approaches define a heuristic function as a *distance metric* that estimates the cost-to-go value of a node [@pohl1970first]. However, estimation of this distance metric is difficult as it is a complex function of robot geometry, dynamics and obstacle configuration. Commonly used heuristics such as the euclidean distance do not adapt to different robot configurations or different environments. On the other hand, by trying to compute a more accurate distance the heuristic should not end up doing more computation than the original search. While state-of-the-art methods propose different relaxation-based [@likhachev2009planning; @dolgov2008practical] and learning-based approaches [@paden2017verification] to estimate the distance metric they run into a much more fundamental limitation - *a small estimation error can lead to a large search wavefront*. Minimizing the estimation error does not necessarily minimize search effort.

Instead, we focus on the latter objective of designing heuristics that explicitly reduce search effort in the interest of real-time performance. Our key insight is that *heuristics should adapt during search* - as the search progresses, they should actively infer the structure of the valid configuration space, and focus the search on potentially good areas. Moreover, we want to learn this behaviour from data - changing the data distribution should change the heuristic automatically. Consider the example shown in Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"}(b). When a heuristic is trained on a world with 'bug traps', it learns to recognize when the search is trapped and circumvent it. On the other hand, when it is trained on a world with narrow gaps, it learns a greedy behaviour that drives the search to the goal.

## Key Idea

It is natural to think of both these problems as a Partially Observable Markov Decision Process (POMDP). However the POMDP is defined on a belief over possible world maps, which is very large in size rendering even the most efficient of online POMDP solvers impractical.

Our key insight is that if the policies could fully observe and process the world map during decision making, they could quite easily disambiguate good actions from bad ones. This motivates us to frame the problem of learning a planning policy as a novel data-driven imitation [@ross2014reinforcement] of a *clairvoyant oracle*. During the training process, the oracle has full knowledge about the world map (hence clairvoyant) and selects actions that maximize cumulative rewards. The policy is then trained to imitate these actions as best as it can using partial knowledge from the current history of actions and observations. As a result of our novel formulation, we are able to sidestep a number of challenging issues in POMDPs like explicitly computing posterior distribution over worlds and planning in belief space.

We empirically show that training such policies using imitation learning of clairvoyant oracles leads to much faster convergence and robustness to poor local minima than training policies via model free policy improvement. We leverage the fact that such oracles can be efficiently computed for our domains once the source of uncertainty is removed. We show in our analysis that imitation of such clairvoyant oracles during training is equivalent to being competitive with a *hallucinating oracle* at test time, i.e. an oracle that implicitly maintains a posterior over world maps and selects the best action at every time step. This offers some valuable insight behind the success of this approach as well as instances where such an approach would lead to a near-optimal policy.

## Contributions

Our contributions are as follows:

1.  We motivate the need to learn a planning policy that adapts to the environment in which the robot operates. We examine two domains - informative path planning and search based planning. We examine both problems through the lens of sequential decision making under uncertainty (Section [2](#sec:background){reference-type="ref" reference="sec:background"}).

2.  We present a novel mapping of both these problems to a common POMDP framework (Section [3](#sec:problem_formulation){reference-type="ref" reference="sec:problem_formulation"}).

3.  We propose a novel framework for training such POMDP policies via imitation learning of a clairvoyant oracle. We analyze the implications of imitating such an oracle (Section [4](#sec:imitation_learning){reference-type="ref" reference="sec:imitation_learning"}).

4.  We present training procedures that deal with the non i.i.d distribution of states induced by the policy itself along with performance guarantees. We present concrete instances of the algorithm for both problem domains. We also show that for a certain class of informative path planning problems, policies trained in this fashion possess near-optimality properties (Section [5](#sec:approach){reference-type="ref" reference="sec:approach"}).

5.  We extensively evaluate the approach on both problem domains. In each domain, we evaluate on a spectrum of environments and show that policies outperform state-of-the-art approaches by exhibiting adaptive behaviours. We also demonstrate the impact of this framework on real world problems by presenting flight test results from a UAV (Section [6](#sec:res_ipp){reference-type="ref" reference="sec:res_ipp"} and Section [7](#sec:res_search){reference-type="ref" reference="sec:res_search"}).

This paper is an unification of previous works on adaptive information gathering [@choudhury2017adaptive; @choudhury2016learning] and learning heuristic search [@bhardwaj2017heuristic]. We present a unified framework for reasoning about both problems. We compare and contrast training procedures due to both domains. We present new results in learning heuristics on 4D planning problems and present flight test results from a UAV. We present new results on comparing the imitation learning with policy search and comparing sample efficiency of [AggreVaTe]{.smallcaps} and [ForwardTraining]{.smallcaps}. We present more details on implementation and analysis of results. We provide comprehensive discussions on shortcomings of this approach and directions for future work in Section [8](#sec:discussion){reference-type="ref" reference="sec:discussion"}.

# Background {#sec:background}

## Informative Path Planning {#sec:background:ipp}

We now present a framework for informative path planning where the objective is to visit maximally informative sensing locations subjected to time and travel constraints. We use this framework to pose the problem of computing a information gathering policy for a given distribution over worlds and briefly discuss prior work on this topic.

### Framework {#sec:background:ipp:framework}

We now introduce a framework and set of notations to express the IPP problems of interest. The specific implementation details of the problem are described in detail in Section [6.1](#sec:res_ipp:problem){reference-type="ref" reference="sec:res_ipp:problem"}.

We have a robot that is constrained to move on a graph $\mathcal{G}= (\mathcal{V}, \mathcal{E})$ where $\mathcal{V}$ is the set of nodes corresponding to all sensing locations. The start node is $v_s$. Let $\xi= \left(v_{1}, v_{2}, \ldots, v_{p}\right)$ be a sequence of connected nodes (a path) such that $v_1 = v_s$. Let $\Xi$ be the set of all such paths.

Let $\phi\in \mathcal{M}$ be the world map in which the robot operates. The world map is usually represented in practice as a binary grid map where grid cells are either occupied or free. We assume that the world map is fixed during an episode.

Let $y\in \mathcal{Y}$ be a measurement received by the robot. Let $\mathcal{H}{}: \mathcal{V}\times \mathcal{M}\to \mathcal{Y}$ be a measurement function. When the robot is at node $v$ in a world map $\phi$, the measurement $y$ received by the robot is $y= \mathcal{H}\left(v, \phi\right)$. The measurement function is defined by a sensor model, e.g. a range limited sensor. A measurement is obtained by projecting the sensor model on the sensing node $v$ and ray-casting to determine the surfaces of the underlying world $\phi$ that intersect with the sensor rays.

The objective of the robot is to move on the graph and maximize utility. Let $\mathcal{F}{}: 2^\mathcal{V}\times \mathcal{M}\to \mathbb{R}_{\geq 0}$ be a utility function. For a path $\xi$ and a world map $\phi$, $\mathcal{F}\left(\xi, \phi\right)$ assigns a utility to executing the path on the world. The utility of a measurement from a node is usually the amount of surface of the world covered by it. In such an instance, the function does not depend on the sequence of vertices in the path, i.e. is a set function. For simplicity, we assume that the measurement and utility function is deterministic. However, this assumption can easily be relaxed in our approach and is discussed in Section. [8.4](#sec:discussion:noisy){reference-type="ref" reference="sec:discussion:noisy"}.

As the robot moves on the graph, the travel cost is captured by the cost function $\mathcal{T}{}: \Xi\times \mathcal{M}\to \mathbb{R}_{\geq 0}$. For a path $\xi$ and a world map $\phi$, $\mathcal{T}\left(\xi, \phi\right)$ assigns a travel cost for executing the path on the world. In a practical setting, the total number of timesteps is bounded by $T$ and the travel cost is bounded by $B$. Fig. [2](#fig:problem){reference-type="ref" reference="fig:problem"} shows an illustration of the framework.

:::: {#fig:problem .figure latex-placement="t!"}
![](Choudhury2017Datadriven_figs/problem_formulation_pic.png){width="\\columnwidth"}

::: caption
The informative path planning problem. Given a world map $\phi$, the robot plans a path $\xi$ which visits a node $v_i \in \mathcal{V}$ and receives measurement $y_i$, such that utility (information gathered) $\mathcal{F}\left(\xi, \phi\right)$ is maximized. Here the utility is the cardinality of all the cells uncovered (green), which is a union of the cells uncovered at each location (and hence a set cover function) []{#fig:problem label="fig:problem"}
:::
::::

We are now ready to define the informative path planning problems. There are two axes of variations

1.  Constraint on the motion of the robot

2.  Observability of the world map

The first axis arises from whether the robot is subject to any travel constraints. For problems such as sensor placement, the agent is free to select any sequence of nodes and the travel cost between nodes is $0$. For such situations, the graph is also fully connected to permit any sequence. For problems involving physical movements, the agent is constrained by a budget on the travel cost. Additionally the graph may also not be fully connected.

The second axis arises from different task specifications which result in the world map being observable or being hidden. We categorize the problems on this axis to aid future discussions on imitating clairvoyant oracles in Section [5](#sec:approach){reference-type="ref" reference="sec:approach"}.

### Problems with Known World Maps {#sec:background:ipp:problem_known}

For the first two variants, the world map $\phi$ is known and can be evaluated while computing a path $\xi$.

::: {#prob:known:unc .problem}
**Problem 1** ([Known-Unc]{.smallcaps}: Known World Map; Unconstrained Travel Cost). *Given a world map $\phi$, a fully connected graph $\mathcal{G}$ and a time horizon $T$, find a path $\xi$ that maximizes utility $$\begin{equation}
\begin{aligned}
\mathop{\mathrm{arg\,max}}\limits_{\xi\in \Xi} \quad & \mathcal{F}\left(\xi, \phi\right) \\
\mathop{\mathrm{\;\; \mbox{s.t.} \;\;}}& \left|\xi\right| \leq T+1
\end{aligned}
\end{equation}$$*
:::

In the case where the utility function is a set function, Problem [1](#prob:known:unc){reference-type="ref" reference="prob:known:unc"} is a set function maximization problem which in general can be NP-Hard [@krause2012submodular]). Such problems occur commonly in the sensor placement problem [@krause2008efficient]. However, in many instances the utility function can be shown to posses the powerful property of *monotone submodularity*. This property implies the following

1.  *Monotonic improvement*: The value of the utility can only increase on adding nodes, i.e. $$\begin{equation*}
    	\mathcal{F}\left( \mathcal{V}_1 \cup \mathcal{V}_2 , \phi\right) \geq \mathcal{F}\left( \mathcal{V}_1 , \phi\right)
    \end{equation*}$$ for all $\mathcal{V}_1, \mathcal{V}_2 \subseteq \mathcal{V}$

2.  *Diminishing returns*: The gain in adding a set of nodes diminshes $$\begin{equation*}
    \begin{aligned}
    	\mathcal{F}\left( \mathcal{V}_1 \cup \mathcal{V}_3 , \phi\right) - \mathcal{F}\left(\mathcal{V}_3 , \phi\right) \leq & \mathcal{F}\left( \mathcal{V}_1 \cup \mathcal{V}_2 , \phi\right) \\ 
    	& - \mathcal{F}\left(\mathcal{V}_2 , \phi\right)
    \end{aligned}
    \end{equation*}$$ for all $\mathcal{V}_1, \mathcal{V}_2, \mathcal{V}_3 \subseteq \mathcal{V}$ where $\mathcal{V}_2 \subseteq \mathcal{V}_3$.

For such functions, it has been shown that a greedy algorithm achieves near-optimality [@krause2008efficient; @Krause:2007:NOS:1619797.1619913].

::: {#prob:known:cons .problem}
**Problem 2** ([Known-Con]{.smallcaps}: Known World Map; Constrained Travel Cost). *Given a world map $\phi$, a time horizon $T$ and a travel cost budget $B$, find a path $\xi$ that maximizes utility $$\begin{equation}
\begin{aligned}
\mathop{\mathrm{arg\,max}}\limits_{\xi\in \Xi} \quad & \mathcal{F}\left(\xi, \phi\right) \\
\mathop{\mathrm{\;\; \mbox{s.t.} \;\;}}& \mathcal{T}\left(\xi, \phi\right) \leq B\\
                                      &  \left|\xi\right| \leq T+1
\end{aligned}
\end{equation}$$*
:::

Problem [2](#prob:known:cons){reference-type="ref" reference="prob:known:cons"} introduces a routing constraint (due to $\mathcal{T}$) for which greedy approaches can perform arbitrarily poorly. Such problems occur when a physical system has to travel between nodes. @chekuri2005recursive [@singh2007efficient] propose a quasi-polynomial time recursive greedy approach to solving this problem. @iyer2013submodular solve a related problem (submodular knapsack constraints) using an iterative greedy approach which is generalized by @zhang2016submodular. @yu2014correlated propose a mixed integer approach to solve a related correlated orienteering problem. @hollinger2013sampling propose a sampling based approach. @arora2017rapidly use an efficient TSP with a random sampling approach.

### Problems with Hidden World Maps {#sec:background:ipp:problem_hidden}

We now consider the setting where the world map $\phi$ is hidden. Given a prior distribution $P(\phi)$, it can be inferred only via the measurements $y_i$ received as the robot visits nodes $v_i$. Hence, instead of solving for a fixed path, we compute a policy that maps history of measurements received and nodes visited to decide which node to visit.

::: {#prob:hidden:unc .problem}
**Problem 3** ([Hidden-Unc]{.smallcaps}: Hidden World Map; Unconstrained Travel Cost). *Given a distribution of world maps, $P(\phi)$, a fully connected graph $\mathcal{G}$, a time horizon $T$, find a policy that at time $t$, maps the history of nodes visited $\{ v_i \}_{i=1}^{t}$ and measurements received $\{ y_i \}_{i=1}^{t}$ to compute the next node $v_{t+1}$ to visit at time $t+1$, such that the expected utility is maximized.*
:::

Such a problem occurs for sensor placement where sensors can optionally fail [@golovin2011adaptive]. Due to the hidden world map $\phi$, it is not straight forward to apply the approaches of Problem [Known-Unc]{.smallcaps}- we have to reason both about $P(\phi\; | \; \{ v_i \}_{i=1}^{t} , \{ y_i \}_{i=1}^{t})$ and how the function will evolve. However, in some instances the utility function $\mathcal{F}$ has an additional property of *adaptive submodularity* [@golovin2011adaptive]. This is an extension of the submodularity property where the gain of the function is measured in expectation over the conditional distribution over world maps $P(\phi\; | \; \{ v_i \}_{i=1}^{t} , \{ y_i \}_{i=1}^{t})$. Under such situations, applying greedy strategies to Problem [3](#prob:hidden:unc){reference-type="ref" reference="prob:hidden:unc"} has near-optimality guarantees [@golovin2010near; @Javdani_2013_7419; @Javdani_2014_7555; @AAAI159841; @DBLP:journals/corr/ChenHK16a] ). However, these strategies require explicitly sampling from the posterior distribution over $\phi$ which make it intractable to apply for our setting.

::: {#prob:hidden:cons .problem}
**Problem 4** ([Hidden-Con]{.smallcaps}: Hidden World Map; Constrained Travel Cost). *Given a distribution of world maps, $P(\phi)$, a time horizon $T$, and a travel cost budget $B$, find a policy that at time $t$, maps the history of nodes visited $\{ v_i \}_{i=1}^{t}$ and measurements received $\{ y_i \}_{i=1}^{t}$ to compute the next node $v_{t+1}$ to visit at time $t+1$, such that the expected utility is maximized.*
:::

Such problems crop up in a wide number of areas such as sensor planning for 3D surface reconstruction [@isler2016information] and indoor mapping with UAVs [@Charrow-RSS-15; @nelson2015information]. Problem [4](#prob:hidden:cons){reference-type="ref" reference="prob:hidden:cons"} does not enjoy the adaptive submodularity property due to the introduction of travel constraints. @hollinger2011active [@hollinger2012active] propose a heuristic based approach to select a subset of informative nodes and perform minimum cost tours. @Singh:2009:NAI:1661445.1661741 replan every step using a non-adaptive information path planning algorithm. Inspired by adaptive TSP approaches by @gupta2010approximation, @lim2016adaptive [@NIPS2015_6005] propose recursive coverage algorithms to learn policy trees. However such methods cannot scale well to large state and observation spaces. @heng2015efficient make a modular approximation of the objective function. @isler2016information survey a broad number of myopic information gain based heuristics that work well in practice but have no formal guarantees.

## Search Based Planning {#sec:background:search}

We now present a framework for search based planning where the objective is to find a feasible path from start to goal while minimizing search effort. We use this framework to pose the problem of learning the optimal heuristic for a given distribution over worlds and briefly discuss prior work on this topic.

### Framework {#sec:background:search:framework}

We consider the problem of search on a graph, $\mathcal{G}= \left( \mathcal{V}, \mathcal{E}\right)$, where vertices $\mathcal{V}$ represent robot configurations and edges $\mathcal{E}$ represent potentially valid movements of the robot between these configurations. Given a pair of start and goal vertices, $\left( v_s, v_g\right) \in \mathcal{V}$, the objective is to compute a path $\xi\subseteq \mathcal{E}$ - a connected sequence of valid edges. The implicit graph $\mathcal{G}$ can be compactly represented by $\left( v_s, v_g\right)$ and a successor function $\mathtt{Succ}(v)$ which returns a list of outgoing edges and child vertices for a vertex $v\in \mathcal{V}$. Hence a graph $\mathcal{G}$ is constructed during search by repeatedly *expanding* vertices using $\mathtt{Succ}(v)$. Let $\phi\in \mathcal{M}$ be a representation of the world that is used to ascertain the validity of an edge. An edge $e\in \mathcal{E}$ is checked for validity by invoking an evaluation function $\mathtt{Eval}(e, \phi)$ which is an expensive operation and may require complex geometric intersection operations [@dellin2016unifying].

Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"} defines a general search based planning algorithm $\mathtt{Search}$ which takes as input the tuple $\langle v_s, v_g, \mathtt{Succ}, \mathtt{Eval}, \phi, \mathtt{Select}\rangle$ and returns a valid path $\xi$. To ensure systematic search, the algorithm maintains the following lists - an open list $\mathcal{O}\subset \mathcal{V}$ of candidate vertices to be expanded and a closed list $\mathcal{C}\subset \mathcal{V}$ of vertices which have already been expanded. It also retains an additional invalid list $\mathcal{I}\subset \mathcal{E}$ of edges found to be in collision. These $3$ lists together represent the complete information available to the algorithm at any given point of time. At a given iteration, the algorithm uses this information to select a vertex $v\in \mathcal{O}$ to expand by invoking $\mathtt{Select}(\mathcal{O})$. It then expands $v$ by invoking $\mathtt{Succ}(v)$ and checking validity of edges using $\mathtt{Eval}(e, \phi)$ to get a set of valid successor vertices $\mathcal{V}_\mathrm{succ}$ as well as invalid edges $\mathcal{E}_\mathrm{inv}$. The lists are then updated and the process repeated till the goal vertex $v_g$ is uncovered. Fig. [3](#fig:search_problem){reference-type="ref" reference="fig:search_problem"} illustrates this framework.

:::: {#fig:search_problem .figure latex-placement="!t"}
![](Choudhury2017Datadriven_figs/sail_problem.png){width="\\columnwidth"}

::: caption
The search based planning problem. Given a world map $\phi$, the agent has to guide a search tree from start $v_s$ to goal $v_g$ by expanding vertices. At any given iteration, the open list $\mathcal{O}$ represents the set of candidate vertices that can be expanded. The closed list $\mathcal{C}$ represents the set of vertices already expanded. The invalid list represents the set of edges that were found to be in collision with the world. The status of every other vertex is unknown. The search continues till the goal belongs to the open list, i.e. a feasible path to goal has been found. []{#fig:search_problem label="fig:search_problem"}
:::
::::

### The Optimal Heuristic Problem

In this work, we focus on the *feasible path problem* and ignore the optimality of the path. Although this is a restrictive setting, quickly finding the feasible path is a very important problem in robotics. Efficient feasible path planners such as RRT-Connect [@kuffner2000rrt] has proven highly effective in high dimensional motion planning applications such as robotic arm planning [@Lav06] and mobile robot planning [@laumond1998guidelines]. Hence we ignore the traversal cost of an edge and deal with unweighted graphs. We defer discussions on how to relax this restriction to Section [8.2](#sec:discussion:anytime_search){reference-type="ref" reference="sec:discussion:anytime_search"}.

We view a heuristic policy as a *selection function* (Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}, Line [\[alg:search:select\]](#alg:search:select){reference-type="ref" reference="alg:search:select"}) that selects a vertex $v$ from the open list $\mathcal{O}$. The objective of the policy is to minimize the number of expansions until the search terminates. Note that the evolution of the open list $\mathcal{O}$ depends on the underlying world map $\phi$ which is hidden. Given a prior distribution over world maps $P(\phi)$, it can be inferred only via the outcome of the expansion operation $\left( \mathcal{V}_\mathrm{succ}, \mathcal{E}_\mathrm{inv}\right)$. The history of outcomes is captured by the state of the search, i.e. the combination of the 3 lists $\{ \mathcal{O}, \mathcal{C}, \mathcal{I}\}$.

::: {#prob:opt_heur .problem}
**Problem 5** ([Opt-Heur]{.smallcaps}). *Given a distribution of world maps, $P(\phi)$, find a heuristic policy that at time $t$, maps the state of the search $\{ \mathcal{O}_t, \mathcal{C}_t, \mathcal{I}_t\}$ to select a vertex $v_t \in \mathcal{O}_t$ to expand, such that the expected number of expansions till termination is minimized.*
:::

:::: algorithm
::: algorithmic
$\mathcal{O}\gets v_s,\; \mathcal{C}\gets \emptyset,\; \mathcal{I}\gets \emptyset$ $v\gets \mathtt{Select}(\mathcal{O})$ []{#alg:search:select label="alg:search:select"} $\left( \mathcal{V}_\mathrm{succ}, \mathcal{E}_\mathrm{inv}\right) \gets \mathtt{Expand}(v, \mathtt{Succ}, \mathtt{Eval}, \phi)$ $\mathcal{O}\gets \mathcal{O}\cup \mathcal{V}_\mathrm{succ}, \; \mathcal{C}\gets \mathcal{C}\cup v, \; \mathcal{I}\gets \mathcal{I}\cup \mathcal{E}_\mathrm{inv}$ **Return** $\mathtt{Path}\left( v_s, v_g\right)$
:::
::::

The problem of heuristic design has a lot of historical significance. A common theme is "Optimism Under Uncertainty". A spectrum of techniques exist to manually design good heuristics by relaxing the problem to obtain guarantees with respect to optimality and search effort [@pearl1984heuristics]. To get practical performance, these heuristics are inflated, as has been the case in the applications in mobile robot planning [@likhachev2009planning]. However, being optimistic under uncertainty is not a foolproof approach and could be disastrous in terms of search efforts depending on the environment (See Fig 2.5, @Lav06).

Learning heuristics falls under machine learning for general purpose planning [@jimenez2012review]. @yoon2006learning propose using regression to learn residuals over FF-Heuristic [@hoffmann2001ff]. @xu2007discriminative [@xu2010iterative; @xu2009learning] improve upon this in a beam-search framework. @arfaee2011learning iteratively improve heuristics. @us2013learning learn combination of heuristic to estimate cost-to-go. Kendall rank coefficient is used to learn open list ranking [@wilt2015building; @garrettlearning]. @thayer2011learning learn heuristics online during search. @paden2017verification learn admissible heuristics as S.O.S problems. However, these methods do not address minimization of search effort and also ignore the non i.i.d nature of the problem.

## Partially Observable Markov Decision Process

POMDPs [@kaelbling1998planning] provide a rich framework for sequential decision making under uncertainty. However, solving a POMDP is often intractable - finite horizon POMDPs are PSPACE-complete [@papadimitriou1987complexity] and infinite horizon POMDPs are undecidable [@madani2003undecidability]. Despite this challenge, the field has forged on and produced a vast amount of work by investigating effective approximations and analyzing the structure of the optimal solution. We refer the reader to [@ross2008online] for a concise survey of modern approaches.

There are two main approaches to POMDP planning: offline policy computation and online search. In offline planning, the agent computes before hand a policy by considering all possible scenarios and executes the policy based on the observation received. Athough offline methods have shown success in planning near-optimal policies in several domains [@smith2012point; @kurniawati2008sarsop; @spaan2005perseus], they are difficult to scale up due to the exponential number of future scenarios that must be considered.

Online methods interleave planning and execution. The agent plans with the current belief, executes the action and updates the belief. Monte-carlo sampling methods explicitly maintain probability over states and plan via monte carlo roll-outs [@mcallester1999approximate; @asmuth2011approaching]. This limits scalability since belief update can take time. In contrast, POMCP [@silver2010monte] maintains a set of particles to represent belief and employ UCT methods to plan with these particles. This allows the method to scale up for larger state spaces.

However, the disadvantage of purely online methods is that they require a lot of search effort online and can lead to poor performance due to evaluation on a small number of particles. [@somani2013despot] present a state-of-the-art algorithm DESPOT that combines the best aspects of many algorithms. First it uses determinized sampling techniques to ensure that the branching factor of the tree is bounded [@ng2000pegasus; @kearns2000approximate]. Secondly, it uses offline precomputed policies to roll-out from a vertex, thus lower bounding its value. Finally, it tries to regularize the search by weighing the utility of a node to be robust against the fact that a finite number of samples is being used.

The methods we have talked about explicitly models the belief. For large scale POMDPs, this might be an issue. Model free approaches and representation learning offer attractive alternatives. Model free policy improvement has been successfully used to solve POMDPs [@liu2013online; @li2009multi]. Predictive state representations  [@littman2002predictive; @boots2011closing] that minimize prediction loss of future observations offer more compact representations than maintaining belief. There also has been a lot of success in employing deep learning to learn powerful representations [@hausknecht2015deep; @karkus2017qmdp].

## Reinforcement Learning and Imitation Learning {#sec:background:il}

Reinforcement Learning (RL) [@sutton1998reinforcement] especially deep RL has dramatically advanced the capabilities of sequential decision making in high dimensional spaces such as controls [@duan2016benchmarking], video games [@silver2016mastering] and strategy games [@silver2016mastering]. Several conventional supervised learning tasks are now being solved using deep RL to achieve higher performance [@ranzato2015sequence; @li2016deep]. In sequential decision making, the prediction of a learner is dependent on the history of previous outcomes. Deep RL algorithms are able to train such predictors by reasoning about the future accumulated cost in a principle manner.

We refer the reader to [@kober2013reinforcement] for a concise survey on RL and to [@arulkumaran2017brief] for a survey on deep RL. Training such policies can be classified into two approaches - either *value function-based approach*, where a value function for an action is learnt, or *policy search*, where a policy is directly learnt. The value function methods can themselves be categorized in two categories - *model-free* algorithms and *model-based* algorithms.

Model-free methods are computationally cheap but ignore the dynamics of the world thus requiring a lot of samples. Q-learning [@watkins1992q] is a representative algorithm for estimating the long-term expected return for executing an action from a given state. When the number of state action pairs are too large in number to track each uniquely, a function approximator is required to estimate the value. Deep Q-learning [@mnih-dqn-2015; @wang2016dueling] addresses such a need by employing a neural-network as a function approximator and learning these network weights. However, the process of using the same network to generate both target values and update Q-values results in oscillations. Hence a number of remedies are required to maintain stability such as having a buffer of experience, a separate target network and an adaptive learning rate. These are indicative of the underlying sample inefficiency problem of a model-free approach.

Model-based methods such as R-Max [@brafman2002r] learn a model of the world which is then used to plan for actions. While such methods are sample efficient, they require a lot of exploration to learn the model. Even in the case when the model of the environment is known, solving for the optimal policy might be computationally expensive for large spaces. Policy search approaches are commonly used where its easier to parameterize a policy than learn a value function [@peters2006policy], however such approaches are sensitive to initialization and can lead to poor local minima.

In contrast with RL methods, imitation learning (IL) algorithms [@daume2009search; @venkatraman2014data; @chang2015learning; @ross2014reinforcement] reduce the sequential prediction problem to supervised learning by leveraging the fact that, for many tasks, at training time we usually have a (near) optimal cost-to-go oracle. This oracle can either come from a human expert guiding the robot [@abbeel2004apprenticeship] or from ground truth data as in natural language processing [@chang2015learning]. The existence of such oracles can be exploited to alleviate learning by trial and error - imitation of an oracle can significantly speed up learning. A traditional approach to using such oracles is to learn a policy or value function from a pre-collected dataset of oracle demonstrations [@ratliff2009learning; @ziebart2008maximum; @finn2016guided]. A problem with these methods is that they require training and test data to be sampled from the same distribtution which is difficult in practice. In contrast, interactive approaches to data collection and training has been shown to overcome stability issues and works well empirically [@ross2011reduction; @ross2014reinforcement; @sun2017deeply]. Furthermore, these approaches lead to strong performance through a reduction to no-regret online learning.

Recent approaches have also employed imitation of clairvoyant oracles, that has access to more information than the learner during training, to improve reinforcement learning as they offer better sample efficiency and safety. @zhang2016mpcgps [@kahn2016plato] train policies that map current observation to action by extending guided policy search [@levine2013guided] for imitation of model predictive control oracles. @tamar2016hindsight consider a cost-shaping approach for short horizon MPC by offline imitation of long horizon MPC which is closest to our work. @gupta2017cmp develop a holistic mapping and planner framework trained using feedback from optimal plans on a graph.

[@sun2017deeply] also theoretically analyze the question of why imitation learning aids in reinforcement learning. They develop a comprehensive theoretical study of IL on discrete MDPs and construct scenarios to show that IL acheives better sample efficiency than any RL algorithm. Concretely, they conclude that one can expect atleast a polynomial gap ad a possible exponential gap in regret between IL and RL when one has access to unbiased estimates of the optimal policy during training.

# Problem Formulation {#sec:problem_formulation}

## POMDPs

A discrete-time finite horizon POMDP is defined by the tuple $(\mathcal{S}, \mathcal{A}, \Omega, R, \mathcal{O}, Z, T)$ where

- $\mathcal{S}$ is a set of states

- $\mathcal{A}$ is a set of actions

- $\Omega$ is a set of state transition probabilities

- $R: \mathcal{S}\times \mathcal{A}$ is the reward function

- $\mathcal{O}$ is the set of observations

- $Z$ is a set of conditional observation probabilities

- $T$ is the time horizon

At each time period, the environment is in some state $s\in \mathcal{S}$ which cannot be directly observed. The initial state is sampled from a distribution $P(s)$. The agent takes an action $a\in \mathcal{A}$ which causes the environment to transition to state $s' \in \mathcal{S}$ with probability $\Omega{}\left(s, a, s'\right) = P(s_{t+1} = s' | s_t = s, a_t = a)$. The agent receives a reward $R{}\left(s, a\right)$. On reaching the new state $s'$, it receives an observation $o\in \mathcal{O}$ according to the probability $Z{}\left(s', a, o\right) = P(o_{t+1} = o| s_{t+1} = s', a_t = a)$.

A *history* $\psi\in \Psi$ is a sequence of actions and observations $\psi_t = \{ <o_1>, <a_1, o_2>, \dots, <a_{t-1}, o_t> \}$. Note that the initial history $\psi_t = <o_1>$ is simply the observation at the initial timestep. The history $\psi_t$ captures all information required to express the belief over state. The belief $P(s_{t+1} | \psi_{t+1})$ can be computed recursively applying Bayes' rule $$\begin{equation*}
\eta \;Z{}\left(s_{t+1}, a_t, o_{t+1}\right) \sum\limits_{s_t \in \mathcal{S}} \Omega{}\left(s_t, a_t, s_{t+1}\right) P(s_t | \psi_t)
\end{equation*}$$ where $\eta$ is a normalization constant.

The history can then also be used to compute an update $P(\psi_{t+1} | \psi_t, a_t)$: $$\begin{equation*}
 \sum\limits_{s_t \in \mathcal{S}} \sum\limits_{s_{t+1} \in \mathcal{S}}  P(s_t | \psi_t) \Omega{}\left(s_t, a_t, s_{t+1}\right) Z{}\left(s_{t+1}, a_t, o_{t+1}\right)
\end{equation*}$$

The agent's action selection behaviour can be explained by a policy $\pi(\psi_t) \in \Pi$ that maps history $\psi_t$ to action $a_t$.

Let the state and history distribution induced by a policy $\pi$ after $t$ timesteps be $P(s, \psi| \pi, t)$. The value of a policy $\pi$ is the expected cumulative reward for executing $\pi$ for $T$ timesteps on the induced state and history distribution $$\begin{equation}
	J\left(\pi\right) = \sum\limits_{t=1}^{T} \mathbb{E}_{s_t, \psi_t \sim P(s, \psi| \pi, t)}\left[R{}\left(s_t, \pi(\psi_t)\right)\right]
\end{equation}$$

The optimal policy maximizes the expected cumulative reward, i.e $\pi^* \in \mathop{\mathrm{arg\,max}}\limits_{\pi\in \Pi} J\left(\pi\right)$.

Given a starting history $\psi$, let $P(s', \psi' | \psi, \pi, i)$ be the induced state history distribution after $i$ timesteps. The value of executing a policy $\pi$ for $t$ time steps from a history $\psi$ is the expected cumulative reward: $$\begin{equation}
\tilde{V}^{\pi}_{t}(\psi) = \sum\limits_{i=1}^{t} 
\mathbb{E}_{s_i, \psi_i \sim P(s', \psi' | \psi, \pi, i)}\left[R{}\left(s_i, \pi(\psi_i)\right)\right]
\end{equation}$$

The state-action value function $\tilde{Q}^{\pi}_{t}(\psi_t, a_t)$ is defined as the expected sum of one-step-reward and value-to-go: $$\begin{equation}
\begin{aligned}
\label{eq:pomdp:q}
\tilde{Q}^{\pi}_{t}(\psi, a) =& \mathbb{E}_{s\sim P(s| \psi)}\left[R{}\left(s, a\right)\right] + \\
                        &\mathbb{E}_{\psi' \sim P(\psi' | \psi, a)}\left[\tilde{V}^{\pi}_{t-1}(\psi')\right]
\end{aligned}
\end{equation}$$

## Mapping Informative Path Planning to POMDPs {#sec:problem_formulation:ipp_mapping}

We now map IPP problems [Hidden-Unc]{.smallcaps} and [Hidden-Con]{.smallcaps} to a POMDP. The state is defined to contain all information that is required to define the reward, observation and transition functions. Let the state be the set of nodes visited and the underlying world, $s_t = \{ v_1, \dots, v_t, \phi\}$. At the start of an episode, a world is sampled from a prior distribution $\phi\sim P(\phi)$ along with a graph $\mathcal{G}\sim P(\mathcal{G})$. The initial state is assigned by setting $s_1 = \{ v_1, \phi\}$. Note that the state $s_t$ is partially observable due to the hidden world map $\phi$.

We define the action $a_t = v_{t+1}$ to be the next node to visit. We are now ready to map the utility and travel cost to the reward function definition. Given the agent is in state $s_t$ and has executed $a_t$, we can extract the path $\xi= \left(v_{1}, v_{2}, \ldots, v_{t+1}\right)$ and the underlying world $\phi$. Hence we can compute the utility function $\mathcal{F}\left(\xi, \phi\right)$. We can also compute the travel cost function $\mathcal{T}\left(\xi, \phi\right)$.

Before we define the reward function, we note that for Problem [Hidden-Con]{.smallcaps} not all actions are feasible at all times due to connectivity of the graph and constraints due to travel cost. Hence we can define a feasible set of actions $\mathcal{A}_{\mathrm{feas}}\left(s\right) \subset \mathcal{A}$ for a state as follows $$\begin{equation}
   \mathcal{A}_{\mathrm{feas}}\left(s\right) = \left\lbrace a\;\;\middle|\;\;a\in \mathcal{A}, (v_t, v_{t+1}) \in \mathcal{E}, \mathcal{T}\left(\xi, \phi\right) \leq B\right\rbrace
\end{equation}$$ For Problem [Hidden-Unc]{.smallcaps}, let $\mathcal{A}_{\mathrm{feas}}\left(s\right) = \mathcal{A}$.

Since the objective is to maximize the cumulative reward function, we define the reward to be proportional to the marginal utility of visiting a node. Given a node $v\in \mathcal{V}$, a path $\xi$ and world $\phi$, the marginal gain of the utility function $\mathcal{F}$ is $\Delta_\mathcal{F}\left(v\mid \xi, \phi\right) = \mathcal{F}\left(\xi\cup \{ v\}, \phi\right) - \mathcal{F}\left(\xi, \phi\right)$. The one-step-reward function, $R{}\left(s, a\right)$, is defined as the marginal gain of the utility function. Additionally, the reward is set to $-\infty$ whenever an infeasible action is selected. Hence: $$\begin{equation}
	R{}\left(s, a\right) = .
	\begin{cases}
	\Delta_\mathcal{F}\left(a\mid \xi, \phi\right) &\text{if $a\in \mathcal{A}_{\mathrm{feas}}\left(s\right)$} \\
	-\infty & \text{otherwise}
	\end{cases}
\end{equation}$$

The state transition function, $\Omega{}\left(s, a, s'\right)$, is defined as the deterministic function which sets $v_{t+1} = a_t$. We define the observation to be the measurement $o_t = y_t$ and the observation model $Z$ to be a deterministic function $o_{t} = \mathcal{H}\left(v_t, \phi\right)$.

Note that the history $\psi_t$, the sequence of actions and observations, is captured in the sequence of nodes visited $\{v_i\}_{i=1}^t$ and measurements received $\{y_i\}_{i=1}^t$. In our implementation, we encode this information in an occupancy map as described later in Section [6.1](#sec:res_ipp:problem){reference-type="ref" reference="sec:res_ipp:problem"}. The information gathering policy $\pi(\psi_t)$ maps this history to an action $a_t$, the sensing location to visit.

## Mapping Search Based Planning to POMDPs

We now map the problem of computing a heuristic policy to a POMDP setting. Let the state be the open list and the underlying world, $s_t = \{ \mathcal{O}_t, \phi\}$. At the start of an episode, a world is sampled from a prior distribution $\phi\sim P(\phi)$ along with a start state $v_s$. The initial state is assigned by setting $s_1 = \{ v_s, \phi\}$. Note that the state $s_t$ is partially observable due to the hidden world map $\phi$.

We define the action $a_t$ as the vertex $v\in \mathcal{O}_t$ that is to be expanded by the search. The state transition function, $\Omega{}\left(s, a, s'\right)$, is defined as the deterministic function which sets $\mathcal{O}_{t+1}$ by querying $\mathtt{Expand}(v, \mathtt{Succ}, \mathtt{Eval}, \phi)$. The one-step-reward function, $R{}\left(s, a\right)$, is defined as $-1$ for every $\left( s_t, a_t\right)$ until the goal is added to the open list. Additionally, the reward is set to $-\infty$ whenever an infeasible action is selected. Hence: $$\begin{equation}
	R{}\left(s, a\right) = .
	\begin{cases}
	-\infty & \text{if $a\notin \mathcal{O}$} \\
	0 &\text{if $v_g\in \mathcal{O}$} \\
	-1 & \text{otherwise}
	\end{cases}
\end{equation}$$

We define the observation to be the successor nodes and invalid edges, i.e. $o_t = \{ \mathcal{V}_\mathrm{succ}, \mathcal{E}_\mathrm{inv}\}$ and the observation model $Z$ to be a deterministic function $\left( \mathcal{V}_\mathrm{succ}, \mathcal{E}_\mathrm{inv}\right) = \mathtt{Expand}(v, \mathtt{Succ}, \mathtt{Eval}, \phi)$.

Note that the history, the sequence of actions and observations, is contained in the information present in the concatenation of all lists, i.e $\psi_t = \{ \mathcal{O}, \mathcal{C}, \mathcal{I}\}$. The heuristic is a policy $\pi(\psi_t)$ that maps this history to an action $a_t$, the vertex to expand.

Note that it is more natural to think of this problem as minimizing a one-step-cost than maximizing a reward. Hence when we subsequently refer to this problem instance, we refer to the cost $c(s, a) = -R{}\left(s, a\right)$ and the cost-to-go $\tilde{Q}^{\pi}_{t}(\psi, a)$. This only results in a change from maximization to minimization.

## What makes these POMDPs intractable? {#sec:problem:hardness}

A natural question to ask if these problems can be solved by state-of-the-art POMDP solvers such as POMCP [@silver2010monte] or DESPOT [@somani2013despot]. While such solvers are very effective at scaling up and solving large scale POMDPs, there are a few reasons why there are not immediately applicable to our problem.

Firstly, these methods require a lot of online effort. In the case of search based planning, the effort required to plan in belief space defeats the purpose of a heuristic all together. In the case of informative path planning, the observation space is very large and belief updates would be time consuming.

Secondly, since both methods employ a particle filter based approach to tracking plausible world maps, they both are susceptible to a realizability problem. Its unlikely that there will be a world map particle that will explain all observations. That being said, the world maps can explain local correlations in observations. For example, when planning indoors the world maps can explain correlations in observations made at intersection of corridors. Hence, we would like to generalize across these local submaps.

# Imitation of Clairvoyant Oracles {#sec:imitation_learning}

A possible approach is to employ model free Q-learning [@mnih-dqn-2015] by featurizing the history $\psi_t$ and collecting on-policy data. However, given the size of $\Psi$, this may require a large number of samples. Another strategy is to parameterize the policy class and employ policy improvement [@peters2006policy] techniques. However, such techniques when applied to POMDP settings may lead to poor local minima due to poor initialization. We discussed in Section [2.4](#sec:background:il){reference-type="ref" reference="sec:background:il"} how imitation learning offers a more effective strategy than reinforcement learning in scenarios where there exist good policies for the original problem, however these policies cannot be executed online (e.g due to computational complexity) hence requiring imitation via an offline training phase. In this section, we extend this principle and show how imitation of *clairvoyant oracles* enables efficient learning of POMDP policies.

## Imitation Learning

We now formally define imitation learning as applied to our setting. Given a policy $\pi$, we define the distribution of histories $P(\psi| \pi)$ induced by it (termed as *roll-in*). Let $\mathcal{L}{}\left( \psi, \pi\right)$ be a loss function that captures how well policy $\pi$ imitates an oracle. Our goal is to find a policy $\hat{\pi}$ which minimizes the expected loss as follows.

$$\begin{equation}
\label{eq:imitation_learning}
\hat{\pi}= \mathop{\mathrm{arg\,min}}\limits_{\pi\in \Pi} \mathbb{E}_{ 
\psi\sim P(\psi| \pi)}\left[\mathcal{L}{}\left( \psi, \pi\right)\right]
\end{equation}$$

This is a non-i.i.d supervised learning problem. @ross2011reduction propose [ForwardTraining]{.smallcaps} to train a non-stationary policy (one policy $\hat{\pi}_t$ for each timestep), where each policy $\hat{\pi}_t$ can be trained on distributions induced by previous policies ($\hat{\pi}_1, \dots, \hat{\pi}_{t-1}$). While this solves the problem exactly, it is impractical given a different policy is needed for each timestep. For training a single policy, @ross2011reduction show how such problems can be reduced to no-regret online learning using dataset aggregation ([DAgger]{.smallcaps}). The loss function they consider $\mathcal{L}$ is a mis-classification loss with respect to what the expert demonstrated. @ross2014reinforcement extend the approach to the reinforcement learning setting where $\mathcal{L}$ is the reward-to-go of an oracle reference policy by aggregating *values* to imitate ([AggreVaTe]{.smallcaps}).

## Solving POMDP via Imitation of a Clairvoyant Oracle

To examine the applicability of imitation learning in the POMDP framework, we compare the loss function ([\[eq:imitation_learning\]](#eq:imitation_learning){reference-type="ref" reference="eq:imitation_learning"}) to the action value function ([\[eq:pomdp:q\]](#eq:pomdp:q){reference-type="ref" reference="eq:pomdp:q"}). We see that a good candidate loss function $\mathcal{L}{}\left( \psi, \pi\right)$ should incentivize maximization of $\tilde{Q}^{\pi}_{T-t+1}(\psi, \pi(\psi))$. A suitable approximation of the optimal value function $\tilde{Q}^{\pi^*}_{T-t+1}$ that can be computed at train time would suffice. However, we cannot resort to oracles that explicitly reasoning about the belief over states $P(s_t | \psi_t)$, let alone planning in this belief space due to tractability issues.

In this work, we leverage the fact that for our problem domains, we have access to the true state $s_t$ at train time. This allows us to define oracles that are *clairvoyant* - that can observe the state at training time and plan actions using this information.

::: definition
**Definition 1** (Clairvoyant Oracle). *A clairvoyant oracle $\pi_{\mathrm{OR}}(s)$ is a policy that maps state $s$ to action $a$ with an aim to maximize the cumulative reward of the underlying MDP $(\mathcal{S}, \mathcal{A}, \Omega, R, T)$.*
:::

The oracle policy defines an equivalent action value function *defined on the state* as follows

$$\begin{equation}
\label{eq:qvaloracle}
Q^{\pi_{\mathrm{OR}}}_{t}(s, a) = R{}\left(s, a\right) + \mathbb{E}_{s' \sim P(s' \mid s, a)}\left[
V^{\pi_{\mathrm{OR}}}_{t-1}(s')\right]
\end{equation}$$

Our approach is to imitate the oracle during training. This implies that we train a policy $\hat{\pi}$ by solving the following optimization problem

$$\begin{equation}
\label{eq:imitateClairvoyantOracle}
\hat{\pi}= \mathop{\mathrm{arg\,max}}\limits_{\pi\in \Pi} \mathbb{E}_{
\substack{t\sim U(1:T), \\
s_t, \psi_t \sim P(s, \psi| \pi, t)}}\left[Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, \pi(\psi_t))\right]
\end{equation}$$

While we will define training procedures to concretely realize ([\[eq:imitateClairvoyantOracle\]](#eq:imitateClairvoyantOracle){reference-type="ref" reference="eq:imitateClairvoyantOracle"}) later in Section [5](#sec:approach){reference-type="ref" reference="sec:approach"}, we offer some intuition behind this approach. Since the oracle $\pi_{\mathrm{OR}}$ knows the state $s$, it has appropriate information to assign a value to an action $a$. The policy $\hat{\pi}$ attempts to imitate this action from the partial information content present in its history $\psi$. Due to this realization error, the policy $\hat{\pi}$ visits a different state, updates the history, and queries the oracle for the best action. Hence while the learnt policy can make mistakes in the beginning of an episode, with time it gets better at imitating the oracle.

## Analysis using a Hallucinating Oracle {#sec:pomdp_imitate:hallucinating}

The learnt policy imitates a clairvoyant oracle that has access to more information (state $s$ compared to history $\psi$). This results in a large realizability error which is due to two terms - firstly the information mismatch between $s$ and $\psi$, and secondly the expressiveness of feature space. This realizability error can be hard to bound making it difficult to apply the performance guarantee analysis of [@ross2014reinforcement]. It is also not desirable to obtain a performance bound with respect to the *clairvoyant oracle* $J\left(\pi_{\mathrm{OR}}\right)$.

To alleviate the information mismatch, we take an alternate approach to analyzing the learner by introducing a purely hypothetical construct - a *hallucinating oracle*.

::: {#def:halluc .definition}
**Definition 2** (Hallucinating Oracle). *A hallucinating oracle $\tilde{\pi}_{\mathrm{OR}}$ computes the instantaneous posterior distribution over state $P(s| \psi)$ and returns the expected clairvoyant oracle action value. $$\begin{equation}
\label{eq:hallucinating_oracle}
\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi, a) =  \mathbb{E}_{s\sim P(s| \psi)}\left[Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s, a)\right]
\end{equation}$$*
:::

We show that by imitating a clairvoyant oracle, the learner effectively imitates the corresponding hallucinating oracle

::: {#lemma:hallucinating .lemma}
**Lemma 1**. *The **offline** imitation of **clairvoyant** oracle ([\[eq:imitateClairvoyantOracle\]](#eq:imitateClairvoyantOracle){reference-type="ref" reference="eq:imitateClairvoyantOracle"}) is equivalent to **online** imitation of a **hallucinating** oracle as shown*

*$$\begin{equation*}
\hat{\pi}= \mathop{\mathrm{arg\,max}}\limits_{\pi\in \Pi} \mathbb{E}_{
\substack{
t\sim U(1:T), \\
\psi_t \sim P(\psi| \pi, t)}}\left[\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \pi(\psi_t))\right]
\end{equation*}$$*
:::

::: proof
*Proof.* Refer to Appendix [10](#appendix:lemma_hallucinating){reference-type="ref" reference="appendix:lemma_hallucinating"}. ◻
:::

Note that a hallucinating oracle uses the same information content as the learnt policy. Hence the realization error is purely due to the expressiveness of the feature space. The empirical risk of imitating the hallucinating oracle will be significantly lower than the risk of imitating the clairvoyant oracle.

Lemma [1](#lemma:hallucinating){reference-type="ref" reference="lemma:hallucinating"} now allows us to express the performance of the learner with respect to a hallucinating oracle. This brings us to the key question - how good is a hallucinating oracle? Upon examining ([\[eq:hallucinating_oracle\]](#eq:hallucinating_oracle){reference-type="ref" reference="eq:hallucinating_oracle"}) we see that this oracle is equivalent to the well known QMDP policy first proposed by [@Littman95learningpolicies]. The QMDP policy ignores observations and finds the $Q_{\mathrm{MDP}}(s, a)$ values of the underlying MDP. It then estimates the action value by taking an expectation on the current belief over states $P(s| \psi)$. This estimate amounts to assuming that any uncertainty in the agent's current belief state will be gone after the next action. Thus, the action where long-term reward from all states (weighed by the probability) is largest will be the one chosen.

[@Littman95learningpolicies] points out that policies based on this approach are remarkably effective. This has been verified by other works such as @Koval-RSS-14 and @javdani2015shared. This naturally leads to the question of why we cannot directly apply QMDP to our problem. The QMDP approach requires explicitly sampling from the posterior over states online - a step that we cannot tractably compute as discussed in Section [3.4](#sec:problem:hardness){reference-type="ref" reference="sec:problem:hardness"}. However, by imitating clairvoyant oracles, we implicitly obtain such a behaviour.

Imitation of clairvoyant oracles has been shown to be effective in other domains such as receding horizon control via imitating MPC methods that have full information [@kahn2016plato]. [@sun2017deeply] show how the partially observable acrobot can be solved by imitation of oracles having full state. [@karkus2017qmdp] introduce imitation of QMDP in a deep learning architecture to train POMDP policies end to end.

The connection with a hallucinating oracle also provides valuable insight into potential failure situations. [@Littman95learningpolicies] point out that policies based on this approach will not take actions to gain information. We discuss such situations in Section [8.1](#sec:discussion:success_failures){reference-type="ref" reference="sec:discussion:success_failures"}.

# Approach {#sec:approach}

## Algorithms

:::: {#fig:ft_aggrevate .figure latex-placement="t"}
![](Choudhury2017Datadriven_figs/ft_aggrevate_overview.png){width="\\textwidth"}

::: caption
Overview of the two approaches for training policies. (a) [ForwardTraining]{.smallcaps} is used to train a non-stationary policy, i.e a sequence of policies $\hat{\pi}^1, \ldots, \hat{\pi}^{T}$ at each time-step. To train a policy at time-step $t$, a state $s$ is sampled from initial distribution $P(s)$. The policies $\hat{\pi}^1, \ldots, \hat{\pi}^{t-1}$ are then used to roll-in to get $(s_t, \psi_t)$. The oracle is queried to get $Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, a_t)$ which is then used to update the dataset and train policy $\hat{\pi}^t$. (b) [AggreVaTe]{.smallcaps} is used to train a stationary policy. The training process is iterative where dataset collection is interleaved with learning. At iteration $i$, a mixture policy $\pi_{\mathrm{mix},i}$ is used to roll-in to get $(s_t, \psi_t)$. The oracle is queried to get $Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, a_t)$. The data is then aggregated to the whole dataset which is used to update the entire policy $\hat{\pi}^{i}$. []{#fig:ft_aggrevate label="fig:ft_aggrevate"}
:::
::::

We introduced imitation learning and its applicability to POMDPs in Section [4](#sec:imitation_learning){reference-type="ref" reference="sec:imitation_learning"}. We now present a set of algorithms to concretely realize the process. The overall idea is as follows - we are training a policy $\hat{\pi}(\psi)$ that maps features extracted from the history $\psi$ to an action $a$. The training objective is to imitate a clairvoyant oracle that has access to the corresponding full state $s$. In order to define concrete algorithms, we need to reason about two classes of policies - non-stationary and stationary.

### Non-stationary policy

For the non-stationary case, we have a policy for each timestep $\hat{\pi}^1, \ldots, \hat{\pi}^{T}$. The motivation for adopting such a policy class is that the problems arising from the non i.i.d distribution immediately disappears. Such a policy class can be trained using the [ForwardTraining]{.smallcaps} algorithm [@ross2011reduction] which sequentially trains each policy on the distribution of features induced from the previous set of policies. Hence the training problem for each policy at timestep $t$ is reduced to supervised learning.

:::: algorithm
::: algorithmic
[]{#alg:FT:init label="alg:FT:init"} Initialize $\mathcal{D}_t \gets \emptyset$. Sample initial state $s_1$ from dataset $P(s)$ Execute policy $\hat{\pi}^1, \ldots, \hat{\pi}^{t-1}$ to reach $\left( s_t, \psi_t\right)$.[]{#alg:FT:rollin label="alg:FT:rollin"} Execute any action $a_t \in \mathcal{A}$. Collect value to go $Q_j^{\pi_{\mathrm{OR}}} =  Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, a_t)$ []{#alg:FT:oracle label="alg:FT:oracle"} $\mathcal{D}_t \gets \mathcal{D}_t \cup \{\psi_t, a_t, Q_j^{\pi_{\mathrm{OR}}}\}$ Train cost-sensitive classifier $\hat{\pi}^t$ on $\mathcal{D}_t$ **Return** Set of policies for each time step $\hat{\pi}^1, \ldots, \hat{\pi}^{T}$ .
:::
::::

Alg. [\[alg:FT\]](#alg:FT){reference-type="ref" reference="alg:FT"} describes the [ForwardTraining]{.smallcaps} procedure to train the non-stationary policy. The policies are trained in a sequential manner. At each time-step $t$, the previously trained policies $\hat{\pi}^1, \ldots, \hat{\pi}^{t-1}$ are used to create a dataset of $\psi_t$ by rolling-in (Lines [\[alg:FT:init\]](#alg:FT:init){reference-type="ref" reference="alg:FT:init"}--[\[alg:FT:rollin\]](#alg:FT:rollin){reference-type="ref" reference="alg:FT:rollin"}). For each such datapoint $\psi_t$, there is a corresponding state $s_t$. A random action $a_t$ is sampled and the oracle is queried for the cost-to-go $Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, a_t)$ (Line [\[alg:FT:oracle\]](#alg:FT:oracle){reference-type="ref" reference="alg:FT:oracle"}). This is then added to the dataset $\mathcal{D}_t$ which is used to train the policy $\hat{\pi}^t$. This is illustrated in Fig. [4](#fig:ft_aggrevate){reference-type="ref" reference="fig:ft_aggrevate"}.

We can state the following property about the training process

::: {#theorem:ft .theorem}
**Theorem 1**. *[ForwardTraining]{.smallcaps} has the following guarantee $$\begin{equation*}
\begin{aligned}
  J\left(\hat{\pi}\right) \geq J\left(\tilde{\pi}_{\mathrm{OR}}\right) -2 T \sqrt{\mathcal{A}\; \varepsilon_{\mathrm{class}}} + T\varepsilon_{\mathrm{or}}
\end{aligned}
\end{equation*}$$ where $\varepsilon_{\mathrm{class}}$ is the regression error of the learner and $\varepsilon_{\mathrm{or}}$ is the local oracle suboptimality.*
:::

::: proof
*Proof.* Refer to Appendix [11](#appendix:theorem_ft){reference-type="ref" reference="appendix:theorem_ft"}. ◻
:::

However, there are several drawbacks to using a non-stationary policy. Firstly, it is impractical to have a different policy for each time-step as it scales with $T$. While this might be a reasonable approach when $T$ is small (e.g. sequence classification problems [@cohen2005stacked]), in our applications $T$ can be fairly large. Secondly, and more importantly, each policy operates on data for only that time-step, thus preventing generalizations across timesteps. Each policy sees only $\frac{\mathcal{D}}{T}$ fraction of the training data. This leads to a high empirical risk.

### Stationary policy

A single stationary policy $\hat{\pi}$ enjoys the benefit of learning on data across all timesteps. However, the non i.i.d data distribution implies the procedure of data collection and training cannot be decoupled - the learner must be involved in the data collection process. @ross2014reinforcement show that such policies can be trained by reducing the propblem to a no-regret online learning setting. They present an algorithm, [AggreVaTe]{.smallcaps} that trains the policy in an interactive fashion where data is collected by a mixture policy of the learner and the oracle, the data is then *aggregated* and the learner is trained on this aggregated data. This process is repeated.

:::: algorithm
::: algorithmic
Initialize $\mathcal{D}\gets \emptyset$, $\hat{\pi}_1$ to any policy in $\Pi$ []{#alg:qvalAgg:init label="alg:qvalAgg:init"} Initialize sub-dataset $\mathcal{D}_i \gets \emptyset$ []{#alg:qvalAgg:initSub label="alg:qvalAgg:initSub"} Let roll-in policy be $\pi_{\mathrm{mix},i} = \beta_{i} \pi_{\mathrm{OR}}+ (1-\beta_{i}) \hat{\pi}_{i-1}$ []{#alg:qvalAgg:mixPol label="alg:qvalAgg:mixPol"} Collect $m$ data points as follows: Sample initial state $s_1$ from dataset $P(s)$ []{#alg:qvalAgg:sampleWorld label="alg:qvalAgg:sampleWorld"} Sample uniformly $t \in \{1,2,\dots,T\}$ []{#alg:qvalAgg:sampleTime label="alg:qvalAgg:sampleTime"} Execute $\pi_{\mathrm{mix},i}$ up to time $t-1$ to reach $\left( s_t, \psi_t\right)$ []{#alg:qvalAgg:rollin label="alg:qvalAgg:rollin"} Execute any action $a_t \in \mathcal{A}$ []{#alg:qvalAgg:takeAction label="alg:qvalAgg:takeAction"} Collect value-to-go $Q_j^{\pi_{\mathrm{OR}}} =  {Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, a_t)}$ []{#alg:qvalAgg:collectVal label="alg:qvalAgg:collectVal"} $\mathcal{D}_i \gets \mathcal{D}_i \cup \{\psi_t, a_t, t, Q_j^{\pi_{\mathrm{OR}}}\}$ []{#alg:qvalAgg:aggrSubData label="alg:qvalAgg:aggrSubData"} Aggregate datasets: $\mathcal{D}\gets \mathcal{D}\bigcup \mathcal{D}_i$ []{#alg:qvalAgg:aggrData label="alg:qvalAgg:aggrData"} Train cost-sensitive classifier $\hat{\pi}_{i+1}$ on $\mathcal{D}$ []{#alg:qvalAgg:updateLearner label="alg:qvalAgg:updateLearner"} **Return** best $\hat{\pi}_i$ on validation
:::
::::

Alg. [\[alg:Agg\]](#alg:Agg){reference-type="ref" reference="alg:Agg"} describes the [AggreVaTe]{.smallcaps} procedure to train the stationary policy. To overcome the non i.i.d distribution issue, the algorithm interleaves data-collection with learning and iteratively trains a set of policies $\left(\hat{\pi}_{1}, \hat{\pi}_{2}, \ldots, \hat{\pi}_{N}\right)$. Note that these iterations are not to be confused with time steps - they are simply learning iterations. A policy $\hat{\pi}_i$ is valid for all timesteps. At iteration $i$, data is collected by rolling-in with a mixture of the learner and the oracle policy (Lines [\[alg:qvalAgg:init\]](#alg:qvalAgg:init){reference-type="ref" reference="alg:qvalAgg:init"}--[\[alg:qvalAgg:rollin\]](#alg:qvalAgg:rollin){reference-type="ref" reference="alg:qvalAgg:rollin"}). The mixing fraction is chosen to be $\beta_{i} = (1 - \alpha)^{i-1}$. Mixing implies flipping a coin with bias $\beta_{i}$ and executing the oracle if heads comes up. A random action $a_t$ is sampled and the oracle is queried for the cost-to-go $Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, a_t)$ (Line [\[alg:qvalAgg:collectVal\]](#alg:qvalAgg:collectVal){reference-type="ref" reference="alg:qvalAgg:collectVal"}).

The key step is to ensure that *data is aggregated*. The motivation for doing so arises from the fact that we want the learner to do well on the distribution it induces. [@ross2014reinforcement] show that this can be posed as the mixture of learners $\left(\hat{\pi}_{1}, \hat{\pi}_{2}, \ldots, \hat{\pi}_{N}\right)$ doing well on the induced loss sequences $l_i(\pi)$ at every iteration. If we were to treat each iteration as a game in an online adversarial learning setting, this would be equivalent to having bounded regret with respect to the best policy in hindsight on the loss sequence $\left(l_{1}, l_{2}, \ldots, l_{N}\right)$. The strategy of dataset aggregation is an instance of follow the leader and hence has bounded regret. Hence, data is appended to the original dataset and used to train an updated learner $\hat{\pi}_{i+1}$ (Lines [\[alg:qvalAgg:aggrData\]](#alg:qvalAgg:aggrData){reference-type="ref" reference="alg:qvalAgg:aggrData"}--[\[alg:qvalAgg:updateLearner\]](#alg:qvalAgg:updateLearner){reference-type="ref" reference="alg:qvalAgg:updateLearner"}).

[AggreVaTe]{.smallcaps} can be shown to have the following guarantee

::: {#theorem:aggrevate .theorem}
**Theorem 2**. *$N$ iterations of [AggreVaTe]{.smallcaps}, collecting $m$ regression examples per iteration guarantees that with probability at least $1-\delta$ $$\begin{equation*}
\begin{aligned}
  J\left(\hat{\pi}\right) \geq & J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
  & - 2 T \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) } \\
  & - \mathcal{O}\left(\frac{R \; T \log T}{N}\right) + T\varepsilon_{\mathrm{or}}\\
\end{aligned}
\end{equation*}$$ where $\varepsilon_{\mathrm{class}}$ is the empirical regression regret of the best regressor in the regression class on the aggregated dataset, $\varepsilon_{\mathrm{reg}}$ is the empirical online learning average regret on the sequence of training examples, $R$ is the range of oracle action value and $\varepsilon_{\mathrm{or}}$ is the local oracle suboptimality.*
:::

::: proof
*Proof.* Refer to Appendix [12](#appendix:theorem_aggrevate){reference-type="ref" reference="appendix:theorem_aggrevate"}. ◻
:::

## Application to Informative Path Planning {#sec:approach:ipp}

:::: {#fig:algorithm_qvalagg .figure latex-placement="!htp"}
![](Choudhury2017Datadriven_figs/algorithm_qvalagg.png){width="\\textwidth"}

::: caption
An overview of [QvalAgg]{.smallcaps} in IPP where a learner $\hat{\pi}$ is trained to imitate a clairvoyant oracle $\pi_{\mathrm{OR}}$. There are 4 key steps. Step 1: A world map $\phi$ is sampled from database representing $P(\phi)$. Step 2: A mixture policy $\pi_{\mathrm{mix},}$ of the learner and oracle is used to roll-in on $\phi$ to a timestep $t$ to get history $\psi_t$. Step 3: A random action $a_t$ is chosen and $(\psi_t, a_t)$ is featurized as $f_t$. Step 4: A clairvoyant oracle $\pi_{\mathrm{OR}}$ is given full access to world map $\phi$ to compute the cumulative reward to go $Q^{\pi_{\mathrm{OR}}}$. The pair $(f_t, Q^{\pi_{\mathrm{OR}}})$ is added to data to update the learner. This process is repeated to train a sequence of learners.
:::
::::

We now consider the applicability of Alg. [\[alg:FT\]](#alg:FT){reference-type="ref" reference="alg:FT"} and Alg. [\[alg:Agg\]](#alg:Agg){reference-type="ref" reference="alg:Agg"} for learning a policy to plan informative paths. We refer to the mapping of the IPP problem to a POMDP defined in Section [3.2](#sec:problem_formulation:ipp_mapping){reference-type="ref" reference="sec:problem_formulation:ipp_mapping"}. We first need to define a clairvoyant oracle in this context. Recall that the state $s_t = \{v_1, \dots, v_t, \phi\}$ is the set of nodes visited and the underlying world. A clairvoyant oracle takes a state action pair $(s_t, a_t)$ as input and computes a value. Depending on whether we are solving Problem [Hidden-Unc]{.smallcaps} or [Hidden-Con]{.smallcaps}, we explore two different kinds of oracles:

1.  *Clairvoyant One-step-reward*

2.  *Clairvoyant Reward-to-go*

### Solving [Hidden-Unc]{.smallcaps} by Imitating Clairvoyant One-step-reward {#sec:approach:ipp:one_step_reward}

We first define a Clairvoyant One-step-reward oracle in the IPP framework.

::: {#def:clair_onestep_rew .definition}
**Definition 3** (Clairvoyant One-step-reward). *A Clairvoyant One-step-reward returns an action value $Q^{\pi_{\mathrm{OR}}}_{t}(s, a) = R{}\left(s, a\right)$ that considers only the one-step-reward. In the context of [Hidden-Unc]{.smallcaps}, it uses the world map $\phi$, the curent path $\{v_1, \dots, v_t\}$, the next node to visit $v_{t+1} = a_t$ to compute the value $Q^\mathrm{OR}(\phi, \{v_1, \dots, v_t\}, v_{t+1})$ as the marginal gain in utility, i.e. $$\begin{equation*}
  \Delta_\mathcal{F}\left(v_{t+1} \mid \{v_1, \dots, v_t\}  , \phi\right)
\end{equation*}$$*
:::

To motive the use of Clairvoyant One-step-reward, we refer to the discussion on the structure of the Problem [Hidden-Unc]{.smallcaps} in Section [2.1.3](#sec:background:ipp:problem_hidden){reference-type="ref" reference="sec:background:ipp:problem_hidden"}. We assume that the utility function is *adaptive monotone submodular* - it has the property of montonicity and diminishing returns under the belief over world maps. This property implies the following

1.  *Adaptive Monotonicity*: The expected value of the utility can only increase on adding a node, i.e. $$\begin{equation*}
      \mathbb{E}_{\phi\sim P(\phi| \psi)}\left[ \Delta_\mathcal{F}\left(v\mid \mathcal{V}_\psi, \phi\right) \right]  \geq 0
    \end{equation*}$$ for all $v\in \mathcal{V}$, where $\psi= \{ v_i \}_{i=1}^p, \{ y_i \}_{i=1}^p$, and $\mathcal{V}_\psi= \{v_i \}_{i=1}^p$.

2.  *Adaptive Submodularity*: The expected gain in adding a node diminshes as more nodes are visited, i.e. $$\begin{equation*}
    \begin{aligned}
      \mathbb{E}_{\phi\sim P(\phi| \psi)}\left[ \Delta_\mathcal{F}\left(v\mid \mathcal{V}_\psi, \phi\right) \right] \geq \\
      \mathbb{E}_{\phi\sim P(\phi| \psi' )}\left[ \Delta_\mathcal{F}\left(v\mid \mathcal{V}_{\psi'} , \phi\right) \right] 
    \end{aligned}
    \end{equation*}$$ for all $v\in \mathcal{V}$, where $\psi\subseteq \psi'$ (history $\psi$ is contained in history $\psi'$)

For such functions, [@golovin2011adaptive] show that greedily selecting vertices to visit is near-optimal. We use this property to show that the Clairvoyant One-step-reward induces a one-step-oracle which is equivalent to the greedy policy and hence near optimal. This implies the following Lemma

::: {#theorem:hidden_unc .theorem}
**Theorem 3**. *$N$ iterations of [AggreVaTe]{.smallcaps} with Clairvoyant one-step-reward collecting $m$ regression examples per iteration guarantees that with probability at least $1-\delta$ $$\begin{equation*}
\begin{aligned}
  J\left(\hat{\pi}\right) \geq & \left(1 - \frac{1}{e}\right)J\left(\pi^*\right) \\
  & - 2 T \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) } \\
  & - \mathcal{O}\left(\frac{R \; T \log T}{N}\right)\\
\end{aligned}
\end{equation*}$$ where $\varepsilon_{\mathrm{class}}$ is the empirical regression regret of the best regressor in the regression class on the aggregated dataset, $\varepsilon_{\mathrm{reg}}$ is the empirical online learning average regret on the sequence of training examples, $R$ is the maximum range of one-step-reward.*
:::

::: proof
*Proof.* Refer to Appendix [13](#appendix:theorem_hiddenunc){reference-type="ref" reference="appendix:theorem_hiddenunc"}. ◻
:::

We will shown in Section [6](#sec:res_ipp){reference-type="ref" reference="sec:res_ipp"} that such policies are remarkably effective. An added benefit of imitating the Clairvoyant One-step-reward is that the empirical classification loss $\varepsilon_{\mathrm{class}}$ is lower since only the expected one-step-reward of an action needs to be learnt.

### Solving [Hidden-Con]{.smallcaps} by Imitating Clairvoyant Reward-to-go

Unforutunately, Problem [Hidden-Con]{.smallcaps} does not posses the adaptive-submodular property of [Hidden-Unc]{.smallcaps} due to the introduction of the travel cost. Hence imitating the one-step-reward is no longer appropriate. We define the Clairvoyant Reward-to-go oracle for this problem class

::: definition
**Definition 4** (Clairvoyant Reward-to-go). *A Clairvoyant Reward-to-go returns an action value $Q^{\pi_{\mathrm{OR}}}_{t}(s, a)$ that corresponds to the cumulative reward obtained by executing $a$ and then following the oracle policy $\pi_{\mathrm{OR}}$. In the context of [Hidden-Con]{.smallcaps}, it uses the world map $\phi$, the curent path $\{v_1, \dots, v_t\}$, the next node to visit $v_{t+1} = a_t$ to solve the problem [Known-Con]{.smallcaps} and compute a future sequence of nodes $\{v_{t+2}, \dots, v_T\}$. This provides the value $Q^\mathrm{OR}(\phi, \{v_1, \dots, v_t\}, v_{t+1})$ as the marginal gain $$\begin{equation*}
  \Delta_\mathcal{F}\left(\{v_{t+1}, \dots, v_T\} \mid \{v_1, \dots, v_t\}  , \phi\right)
\end{equation*}$$ The correspoding oracle policy $\pi_{\mathrm{OR}}$ is obtained by following the computed path.*
:::

Note that solving [Known-Con]{.smallcaps} is NP-Hard and even the best approximation algorithms require some computation time. Hence the calls to the oracle must be minimized.

### Training and Testing Procedure

We now present concrete algorithms to realize the training procedure. Given the two axes of variation - problem and policy type - we have four possible algorithms

1.  [RewardFT]{.smallcaps}: Imitate one-step-reward using non-stationary policy by [ForwardTraining]{.smallcaps}(Alg. [\[alg:FT\]](#alg:FT){reference-type="ref" reference="alg:FT"})

2.  [QvalFT]{.smallcaps}: Imitate reward-to-go using non-stationary policy by [ForwardTraining]{.smallcaps}(Alg. [\[alg:FT\]](#alg:FT){reference-type="ref" reference="alg:FT"})

3.  [RewardAgg]{.smallcaps}: Imitate one-step-reward using stationary policy by [AggreVaTe]{.smallcaps}(Alg. [\[alg:Agg\]](#alg:Agg){reference-type="ref" reference="alg:Agg"})

4.  [QvalAgg]{.smallcaps}: Imitate reward-to-go using stationary policy by [AggreVaTe]{.smallcaps}(Alg. [\[alg:Agg\]](#alg:Agg){reference-type="ref" reference="alg:Agg"})

Table. [\[tab:alg:mapping\]](#tab:alg:mapping){reference-type="ref" reference="tab:alg:mapping"} shows the algorithm mapping.

::: tabulary
0.8L\|CC & [Hidden-Unc]{.smallcaps}& [Hidden-Con]{.smallcaps}\
Non-stationary policy & [RewardFT]{.smallcaps}& [QvalFT]{.smallcaps}\
Stationary policy & [RewardAgg]{.smallcaps}& [QvalAgg]{.smallcaps}\
:::

[]{#tab:alg:mapping label="tab:alg:mapping"}

:::: algorithm
::: algorithmic
Initialize $\mathcal{D}\gets \emptyset$, $\hat{\pi}_1$ to any policy in $\Pi$ Initialize sub-dataset $\mathcal{D}_i \gets \emptyset$ Let roll-in policy be $\pi_{\mathrm{mix},i} = \beta_{i} \pi_{\mathrm{OR}}+ (1-\beta_{i}) \hat{\pi}_i$ Collect $m$ data points as follows: Sample world $\phi$ from dataset $P(s)$ Sample start node $v_s$ for $P(v_s)$ Sample uniformly $t \in \{1,2,\dots,T\}$ Execute $\pi_{\mathrm{mix},i}$ up to time $t-1$

to get path $\{v_1, \dots, v_t\}$ and history ${\psi_t}$ Sample a random action $a_t \in \mathcal{A}$

as the next vertex to visit $v_{t+1} = a_t$ Invoke Clairvoyant Reward-to-go oracle

to get $Q_j^{\pi_{\mathrm{OR}}} = Q^\mathrm{OR}\{\phi, \{v_1, \dots, v_t\}, v_{t+1}\}$. $\mathcal{D}_i \gets \mathcal{D}_i \cup \{\psi_t, a_t, t, Q_j^{\pi_{\mathrm{OR}}}\}$ Aggregate datasets: $\mathcal{D}\gets \mathcal{D}\bigcup \mathcal{D}_i$ Train cost-sensitive classifier $\hat{\pi}_{i+1}$ on $\mathcal{D}$ **Return** best $\hat{\pi}_i$ on validation
:::
::::

For completeness, we concretely define the training procedure for [QvalAgg]{.smallcaps} in Alg. [\[alg:qvalAgg\]](#alg:qvalAgg){reference-type="ref" reference="alg:qvalAgg"}. The procedure for the remaining three algorithms can be inferred from this. The algorithm iteratively trains a sequence of policies $\left(\hat{\pi}_{1}, \hat{\pi}_{2}, \ldots, \hat{\pi}_{N}\right)$. At every iteration $i$, the algorithm conducts $m$ episodes. In every episode a different world map $\phi$ and start vertex $(v_s)$ is sampled from a database. The roll-in is conducted with a mixture policy $\pi_{\mathrm{mix},i}$ which blends the learner's current policy, $\hat{\pi}_{i-1}$ and the oracle's policy, $\pi_{\mathrm{OR}}$ using blending parameter $\beta_{i}$. The blending is done in an episodic fashion, with probability $\beta_{i}$ the Clairvoyant Reward-to-go oracle is invoked to compute a path which is followed. With probability $1 - \beta_{i}$, the learner is invoked for the whole episode. In a given episode, the roll-in is conducted to a timestep $t$ which is uniformly sampled. At the end of the roll-in, we have a path $\{v_1, \dots, v_t\}$ and a history ${\psi_t}$. A random action $a_t \in \mathcal{A}$ is sampled which defines the next vertex to visit $v_{t+1} = a_t$. The Clairvoyant Reward-to-go oracle is invoked with the world $\phi$ and the path already travelled $\{v_1, \dots, v_t\}, v_{t+1}\}$. It then invokes a solver to [Hidden-Con]{.smallcaps} to complete the path and return the reward to go $Q_j^{\pi_{\mathrm{OR}}}$ . This history action pair $(\psi_t, a_t)$ is projected to a feature space along with label $Q_j^{\pi_{\mathrm{OR}}}$. The data is aggregated to the dataset which is eventually used to train policy $\hat{\pi}_{i+1}$. Fig. [5](#fig:algorithm_qvalagg){reference-type="ref" reference="fig:algorithm_qvalagg"} illustrates this approach.

## Application to Search Based Planning

:::: {#fig:algorithm_sail .figure latex-placement="!htp"}
![](Choudhury2017Datadriven_figs/algorithm_sail.png){width="\\textwidth"}

::: caption
An overview of [SaIL]{.smallcaps} in search based planning where a learner $\hat{\pi}$ is trained to imitate a clairvoyant oracle $\pi_{\mathrm{OR}}$. There are 4 key steps. Step 1: A world map $\phi$ is sampled from database representing $P(\phi)$ along with start goal pair $\left( v_s, v_g\right)$. Step 2: A mixture policy $\pi_{\mathrm{mix},}$ of the learner and oracle is used to roll-in on $\phi$ to a timestep $t$ to get history $\psi_t$ which is the combination of open list, closed list and invalid edges. Step 3: A random vertex $a_t$ from the open list is chosen and $(\psi_t, a_t)$ is featurized as $f_t$. Step 4: A clairvoyant oracle $\pi_{\mathrm{OR}}$ is given full access to world map $\phi$ to compute the cumulative cost to go $Q^{\pi_{\mathrm{OR}}}$. The pair $(f_t, Q^{\pi_{\mathrm{OR}}})$ is added to data to update the learner. This process is repeated to train a sequence of learners.
:::
::::

We now consider the applicability of Alg. [\[alg:Agg\]](#alg:Agg){reference-type="ref" reference="alg:Agg"} for heuristic learning in search based planning. Unlike the IPP problem domain, there is no incentive to use a non-stationary policy or imitate Clairvoyant One-step-rewards. Hence we only consider training a stationary policy imitating Clairvoyant Reward-to-go.

We first need to define a clairvoyant oracle for this problem. Given access to the world map $\phi$, the oracle has to solve for the optimal number of expansions to reach the goal. This allows us to define a *clairvoyant oracle planner* that employs a *backward* Dijkstra's algorithm, which given a world $\phi$ and a goal vertex $v_g$ plans for the optimal path from every $v\in \mathcal{V}$ using dynamic programming.

::: {#def:clairvoyant_oracle .definition}
**Definition 5** (Clairvoyant Oracle Planner). *Given full access to the state $s$, which contains the open list $\mathcal{O}$ and world $\phi$, and a goal $v_g$, the oracle planner encodes the cost-to-go from any vertex $v\in \mathcal{V}$ as the function $Q^{\pi_{\mathrm{OR}}}_{t}(s, a)$ which implicitly defines an oracle policy, $\pi_{\mathrm{OR}}(s) \; = \; \mathop{\mathrm{arg\,min}}\limits_{v\in\mathcal{O}} \; Q^{\pi_{\mathrm{OR}}}_{t}(s, a)$.*
:::

The clairvoyant oracle planner provides a look-up table $Q^{\textsc{OR}}\left( \phi, v\right)$ for the optimal cost-to-go from any vertex irrespective of the current state of the search.

A key distinction between this oracle and the one defined for an IPP problem in Section [5.2](#sec:approach:ipp){reference-type="ref" reference="sec:approach:ipp"} is that we are able to efficiently get the cost-to-go value for all states by dynamic programming - we do not need to repeatedly invoke the oracle. We exploit this fact by extracting multiple labels from an episode even though the oracle is invoked only once. Additionally, this allows us a better roll-in procedure where the oracle and learner are interleaved. We adapt the [AggreVaTe]{.smallcaps} framework to present an algorithm, *Search as Imitation Learning* ([SaIL]{.smallcaps}).

:::: algorithm
::: algorithmic
Initialize $\mathcal{D}\gets \emptyset$, $\hat{\pi}_1$ to any policy in $\Pi$ []{#lst:line: label="lst:line:"} Initialize sub dataset $\mathcal{D}_i \gets \emptyset$ Collect $mk$ data points as follows: Sample world map $\phi\sim P(\phi)$ Sample $\left( v_s, v_g\right) \sim P(v_s, v_g)$ Invoke clairvoyant oracle planner

to compute $Q^{\pi_{\mathrm{OR}}}_{}(\phi, v) \; \forall \; v\in \mathcal{V}$ Sample uniformly $k$ timesteps $\left\lbrace t_{1}, t_{2}, \ldots, t_{k}\right\rbrace$

where each $t_{i} \in \ \left\lbrace 1, \ldots ,T\right\rbrace$ Rollout search with

$\pi_{\mathrm{mix},i} = \beta_{i} \pi_{\mathrm{OR}}+ (1-\beta_{i}) \hat{\pi}_i$ At each $t\in\left\lbrace t_{1}, t_{2}, \ldots, t_{k}\right\rbrace$ pick a random

action $a_t$ to get corresponding $\left( \psi_t, v\right)$ Query oracle for $Q^{\textsc{OR}}\left( \phi, a_t\right)$ $\mathcal{D}_i \gets \mathcal{D}_i \cup \{\psi_t, a_t, t, Q^{\textsc{OR}}\left( \phi, a_t\right) \}$ Aggregate datasets: $\mathcal{D}\gets \mathcal{D}\bigcup \mathcal{D}_i$ Train cost-sensitive classifier $\hat{\pi}_{i+1}$ on $\mathcal{D}$ **Return** best $\hat{\pi}_i$ on validation
:::
::::

Alg. [\[alg:sail_alg\]](#alg:sail_alg){reference-type="ref" reference="alg:sail_alg"}, describes the $\textsc{SaIL}$ framework which iteratively trains a sequence of policies $\left(\hat{\pi}_{1}, \hat{\pi}_{2}, \ldots, \hat{\pi}_{N}\right)$. For training the learner, we collect a dataset $\mathcal{D}$ as follows - At every iteration *i*, the agent executed *m* different searches (Alg. [\[alg:search\]](#alg:search){reference-type="ref" reference="alg:search"}). For every search, a different world $\phi$ and the pair $(v_s, v_g)$ is sampled from a database. The agent then rolls-out a search with a mixture policy $\pi_{\mathrm{mix},i}$ which blends the learner's current policy, $\hat{\pi}_{i}$ and the oracle's policy, $\pi_{\mathrm{OR}}$ using blending parameter $\beta_{i}$. During the search execution, at every timestep in a set of $k$ uniformly sampled timesteps, we select a random action from the set of feasible actions and collect a datapoint $\{\psi_t, a_t, t, Q^{\textsc{OR}}\left( \phi, a_t\right) \}$. The policy $\pi_{\mathrm{mix},i}$ is rolled out till the end of the episode and all the collected data is aggregated with dataset $\mathcal{D}$. At the end of N iterations, the algorithm returns the best performing policy on a set of held-out validation environment or alternatively, a mixture of $\left(\hat{\pi}_{1}, \hat{\pi}_{2}, \ldots, \hat{\pi}_{N}\right)$. Fig. [6](#fig:algorithm_sail){reference-type="ref" reference="fig:algorithm_sail"} illustrates the [SaIL]{.smallcaps} framework.

Note that while the oracle is invoked once per $\phi$, we obtain $k$ datapoints - this is critical for speeding up training. We also note that even though the time complexity of $\mathtt{Select}$ is $O \left(|\mathcal{O}_{t}|\right)$ at timestep $t$, $\textsc{SaIL}$ can have better overall complexity if it can achieve a squared reduction in number of expansions compared to uninformed search as discussed more in Appendix [16](#appendix:sail_complexity){reference-type="ref" reference="appendix:sail_complexity"}.

# Experiments on Informative Path Planning {#sec:res_ipp}

In this section, we extensively evaluate our approach on a set of 2D and 3D informative path planning problems across a spectrum of synthetic and real world environments. We examine a class of informative path planning problem where a robot, equipped with a range limited sensor, possibly constrained by time and fuel resources, is tasked with 3D reconstruction of structures in the world. We choose a variety of environments to highlight the importance of adaptive behaviours for information gathering. Our implementation is open sourced for both MATLAB and C++ (<https://bitbucket.org/sanjiban/matlab_learning_info_gain>).

## Problem Details {#sec:res_ipp:problem}

We consider both 2D and 3D informative path planning problems. The world map $\phi$ is represented as a 2D or 3D binary grid, i.e. a grid cell is either occupied or free. The candidate set of sensing locations $\mathcal{V}$ is generated by uniformly randomly sampling nodes in the configuration space of the robot. For 2D problems, the configuration space of the robot is $SE(2)$, for 3D it is $SE(3)$. We assume for simplicity that the robot can teleport between any two nodes $v_i$ and $v_j$ and the cost of travel is the 2D/3D euclidean straight-line distance $\mathcal{T}(\{ v_i, v_j \}, \phi) = \left|\left| v_i - v_j \right|\right|_{2}$. It would be straightforward to incorporate practical constraints such as collision avoidance by only allowing motion between vertices that are known to collision free and computing travel cost to be the arc length distance of a collision free path.

We assume that the robot is equipped with a field-of-vision (FOV) and range limited sensor. When a robot visits a node $v$ in a world map $\phi$, the measurement received by the robot, $y= \mathcal{H}\left(v, \phi\right)$, is computed by ray-casting the sensor on the world and obtaining a scan line (2D) or a depth-image (3D).

The utility function $\mathcal{F}$ is selected to be the fractional coverage function (similar to [@isler2016information]) which is defined as follows. Let the robot traverse a path $\xi= \left(v_{1}, v_{2}, \ldots, v_{p}\right)$ in a world $\phi$. For each node $v_i \in \xi$ we have a corresponding measurement $y_i$. Let the coverage map $C_i$ be a binary grid whose cells are $1$ iff the corresponding cell in $\phi$ is occupied and $y_i$ contains a point in that cell. The total coverage map of a path $\xi$ is a union of all coverage maps $C = \bigcup\limits_{i = 1}^{p} C_i$. Then the utility function is the ratio of the total coverage and the total occcupied cells in the world map, i.e. $\mathcal{F}(\xi, \phi) = \frac{\left|\left| C \right|\right|_{1}}{\left|\left| \phi \right|\right|_{1}}$.

While we assume the objective of the robot is to 'uncover' every cell of the hidden world map, this framework can also allow a more task specific objective. For example, if the objective is to perform surface reconstruction of a specific object (and not of every surface in the world map), the utility function can be modified to only cover gridcells belonging to that object. The quality of an observation can also be included in the utility, i.e. measurements at close range can be weighted more than measurements taken from far away.

The values of total time step $T$ and travel budget $B$ vary with problem instances and are specified along with the results.

The history of events $\psi_t$ is represented as an occupancy grid $\mathcal{X}$ where each grid cell $x\in \mathcal{X}$ corresponds to an occupancy value $P_o\left(x\right) \in [0, 1]$. Every time a new measurement is received, $\mathcal{X}$ is updated by ray-casting and applying Bayes' rule [@thrun2005probabilistic]. The policy $\pi(\psi_t)$ takes as input the occupancy grid and selects an action $a_{t+1}$ that corresponds to the next node $v$ to be visited.

## Baseline: Information Theoretic Heuristics {#sec:res_ipp:baseline}

@isler2016information propose a set of information theoretic heuristics that quantify the information gain of obtaining a measurement for the task of volumetric reconstruction which include visibility likelihood and the likelihood of seeing new parts of the object. These heuristics are variants of Shannon's entropy where cells are weighted by an importance function. All of the heuristics are myopic, i.e. given the current occupancy grid, each candidate node is evaluated and the best node is selected as the next action. We briefly describe these heuristics and ask the reader to refer to @isler2016information for further details.

To evaluate a node $v$, a set of rays $\mathcal{R}(v)$ are cast from the node using the specifications of the sensor model. A ray $r\in \mathcal{R}$ corresponds to a set of grid cells in the occupancy grid $\mathcal{X}{}\left(r\right)$. Given a grid cell $x$, the probability of it being occupied is $P_o\left(x\right)$ and being free is $\bar{P}_o\left(x\right)$. This can be used to compute various information gain metrics according to different heuristics. Let $\mathcal{I}_{}\left(x\right)$ be the information stored in the grid cell $x$. Then the information gain for a node is given by $$\begin{equation}
  \mathcal{I}\mathcal{G}_{}\left(v\right) = \sum\limits_{\forall r\in \mathcal{R}(v)} \sum\limits_{\forall x\in \mathcal{X}{}\left(r\right)} \mathcal{I}_{}\left(x\right)
\end{equation}$$

Depending on the type of information gain $\mathcal{I}$, there can be several information gain functions

1.  Average Entropy: $\mathcal{I}\mathcal{G}_{o}\left(v\right)$

    This corresponds to the entropy $$\begin{equation}
      \mathcal{I}_{o}\left(x\right) = -P_o\left(x\right) \log P_o\left(x\right) - \bar{P}_o\left(x\right) \log \bar{P}_o\left(x\right)
    \end{equation}$$

2.  Occlusion Aware Entropy: $\mathcal{I}\mathcal{G}_{v}\left(v\right)$

    This corresponds to considering the visibility likelihood of a grid cell $$\begin{equation}
      \mathcal{I}_{v}\left(x\right) = P_v(x) \mathcal{I}_{o}\left(x\right)
    \end{equation}$$ where $P_v(x)$ is the likelihood of the ray $r$ leading to the $x$ being free.

3.  Unobserved Voxel: $\mathcal{I}\mathcal{G}_{u}\left(v\right)$

    This corresponds to only considering unknown grid cells $$\begin{equation}
      \mathcal{I}_{u}\left(x\right) = \begin{cases}
    1 &\text{if $x$ is unknown}\\
    0 &\text{otherwise}
    \end{cases}
    \end{equation}$$

4.  Unobserved Entropy: $\mathcal{I}\mathcal{G}_{k}\left(v\right)$

    This is the composition of unobserved voxel with occlusion aware entropy $$\begin{equation}
      \mathcal{I}_{k}\left(x\right) = \mathcal{I}_{u}\left(x\right) \mathcal{I}_{v}\left(x\right)
    \end{equation}$$

5.  Rear Side Voxel: $\mathcal{I}\mathcal{G}_{b}\left(v\right)$

    Let $RS$ be the set of *rear-side* grid-cells defined as occluded, unknown gird cells adjacent on the ray to an occupied grid cell. Then $$\begin{equation}
      \mathcal{I}_{b}\left(x\right) = \begin{cases}
    1 &\text{if $x\in RS$}\\
    0 &\text{otherwise}
    \end{cases}
    \end{equation}$$

6.  Rear Side Entropy: $\mathcal{I}\mathcal{G}_{n}\left(v\right)$

    This is the composition of rear side voxel with occlusion aware entropy $$\begin{equation}
      \mathcal{I}_{n}\left(x\right) = \mathcal{I}_{b}\left(x\right) \mathcal{I}_{v}\left(x\right)
    \end{equation}$$

The heuristics are used in a greedy fashion as follows. Given the robot has already visited nodes $v_1, \dots, v_{t-1}$, it decides to visit node $v_t$ according to the following rule

$$\begin{equation}
  v_t = \mathop{\mathrm{arg\,max}}\limits_{v_t \in \mathcal{V}} \frac{ \mathcal{I}\mathcal{G}_{}\left(v_t\right) }{ \sum_{v\in \mathcal{V}} \mathcal{I}\mathcal{G}_{}\left(v\right) } - 
  \lambda \frac{ \left|\left|  v_t - v_{t-1} \right|\right|_{2} }{ \sum_{v\in \mathcal{V}} \left|\left|  v- v_{t-1} \right|\right|_{2} }
\end{equation}$$

When applied to the Problem [Hidden-Unc]{.smallcaps}, we de-activate the penalization and set $\lambda = 0$.

## Imitation Learning Details

### Feature Extraction and Learner

The policy maps the history $\psi$ to an action $a$ by learning a function approximation for the action value function $\hat{Q}(\psi, a)$. The tuple $\left(a, \psi\right)$ is mapped to a vector of features $f=  \begin{bmatrix}f{}_{\mathrm{IG}}^T & f{}_{\mathrm{mot}}^T \end{bmatrix}^T$. The first set of features $f{}_{\mathrm{IG}}\in \mathbb{R}^6$ are the information gain heuristics defined in Section [6.2](#sec:res_ipp:baseline){reference-type="ref" reference="sec:res_ipp:baseline"}. These heuristics are computed using the occupancy map corresponding to history $\psi$ and the candidate node corresponding to action $a$. There are several reasons for using these heuristics as the feature vector. They allow generalization across different instance of the world map. They also allow for fare comparison against the heuristics as baseline approaches - the learner learns a trade-off between heuristics.

$f{}_{\mathrm{mot}}\in \mathbb{R}^7$ encodes the distance already travelled by the robot $(\mathbb{R}^1)$, the relative translation $(\mathbb{R}^3)$ and rotation $(\mathbb{R}^3)$ to visit the candidate node from the current node. These set of features capture the travel cost trade-off for visiting a node.

We use random forest regression as a function approximator [@liaw2002classification].

### Dataset Creation

The 2D world maps are created by randomly distributing geometric objects such as rectangles and circles according to hand design parametric distribution. The 3D world maps are created using the ROS-Gazebo simulator and randomly distributing 3D object meshes. Depending on the environment (such as construction site or office-desk), different collection of objects and parametric distributions are selected.

For the experiment on a real dataset, we used registered RGBD data collected by [@sturm12iros]. The original dataset is a set of registered point cloud along with the measurement pose. This dataset can be used to create the world map $\phi$. The set of poses are used to create a fully connected graph $\mathcal{V}$. The algorithm is then restricted to choosing a subset of these poses to maximize the utility. Every time the algorithm visits a node $v_i$, the corresponding measurement $y_i$ is returned. We found that this setup allowed us to easily evaluate information gathering algorithms on real data in a completely decoupled manner from the data collection process.

This process of dataset creation motivates the applicability of our method in practical settings. Given a new environment, we can envision collecting a dataset open-loop, either via manual operation or via some base exploration policy. We can then learn an efficient policy on this dataset and subsequently used the learnt policy for future operations. The generalization capability of the learner allows performance to be transferred to environments with similar object configurations.

:::: {#fig:results:extra .figure latex-placement="t"}
![](Choudhury2017Datadriven_figs/extra_results.png){width="\\textwidth"}

::: caption
Results for Problems [Hidden-Unc]{.smallcaps} and [Hidden-Con]{.smallcaps} on a spectrum of 2D and 3D exploration problems. The train size is $100$ and test size is $10$. Numbers are the confidence bounds (for 95% CI) of cumulative reward at the final time step. Algorithm with the highest median performance is emphasized in bold.
:::
::::

### Clairvoyant Oracle

For algorithms [RewardAgg]{.smallcaps} and [RewardFT]{.smallcaps}, the clairvoyant oracle is simply the one-step-reward function, i.e. the marginal utility of visiting a node given the history of nodes visited. An important implementation detail is that when using the one-step-reward oracle, the call to the oracle is inexpensive. Hence, instead of sampling a random action and obtaining its value, all actions can be queried. This dramatically improves the convergence due to the increase in data size.

For [QvalAgg]{.smallcaps} and [QvalFT]{.smallcaps}, the clairvoyant oracle needs to solve the submodular routing problem (Problem [Known-Con]{.smallcaps}). We use the Generalized Cost Benefit (GCB) [@zhang2016submodular] algorithm - an efficient greedy algorithm with bi-criterion approximation guarantees. The core idea of the algorithms is very simple: at iteration $i$ select a node $v_i$ that maximizes the ratio of the marginal gain in utility and the marginal gain in travel cost

$$\begin{equation}
  \label{eq:gcb}
  v_i = \mathop{\mathrm{arg\,max}}\limits_{v\in \mathcal{V}} 
  \frac{ \mathcal{F}\left( v_i \cup \{ v_j \}_{j=1}^{i-1} , \phi\right) - \mathcal{F}\left( \{ v_j \}_{j=1}^{i-1} , \phi\right) }      
       { \mathcal{T}\left( v_i \cup \{ v_j \}_{j=1}^{i-1} , \phi\right)    - \mathcal{T}\left( \{ v_j \}_{j=1}^{i-1} , \phi\right)  }
\end{equation}$$

Once a vertex $v_i$ is selected, a TSP solver is invoked to find the minimum cost route through nodes $v_1, \dots, v_i$ and the vertices are re-ordered accordingly. The process is repeated till the travel budget constraints are met. Note that computing the denominator exactly in ([\[eq:gcb\]](#eq:gcb){reference-type="ref" reference="eq:gcb"}) might be expensive since it involves a call to a TSP solver. We can instead approximate it by the distance to the node $v_i$ from the last node in the route $v_{i-1}$.

:::: {#fig:results:matlab_unc .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/matlab_2d_unc.png){width="\\textwidth"}

::: caption
Case study of Problem [Hidden-Unc]{.smallcaps} using [RewardAgg]{.smallcaps}, [RewardFT]{.smallcaps} and baseline heuristics. Two different datasets of 2D exploration are considered - (a) dataset 1 (parallel lines) and (b) dataset 2 (distributed blocks). Problem details are: $T=30, |\mathcal{A}|=300$, $100$ train and $100$ test maps. A sample test instance is shown along with a plot of cumulative reward with time steps for different policies is shown in (c) and (d). The error bars show $95\%$ confidence intervals. (e) and (f) show snapshots of the execution at time steps $7, 15$ and $30$. []{#fig:results:matlab_unc label="fig:results:matlab_unc"}
:::
::::

:::: {#fig:results:matlab_con .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/matlab_2d_con.png){width="\\textwidth"}

::: caption
Case study of Problem [Hidden-Unc]{.smallcaps} using[QvalAgg]{.smallcaps} with baseline heuristics on a 2D exploration problem on 2 different datasets - dataset 1 (concentrated information) and dataset 2 (distributed information). The problem details are: $T=30, B=2500, |\mathcal{A}|=300$, $100$ train and $100$ test maps. A sample test instance is shown along with a plot of cumulative reward with time steps for different policies is shown in (c) and (d) The error bars show $95\%$ confidence intervals Snapshots of execution of [QvalAgg]{.smallcaps}, Rear Side Voxel and Average Entropy are shown for (e) dataset 1 and (f) dataset 2. The snapshots show the evidence grid at time steps $7, 15$ and $30$. []{#fig:results:matlab_con label="fig:results:matlab_con"}
:::
::::

:::: {#fig:results:cpp .figure latex-placement="t"}
![](Choudhury2017Datadriven_figs/cpp_results.png){width="\\textwidth"}

::: caption
Comparison of [QvalAgg]{.smallcaps} with baseline heuristics on a 3D exploration problem where training is done on simulated world maps and testing is done on a real dataset of an office workspace. The problem details are: $T=10$, $B=12$, $|\mathcal{A}|=50$. (a) Samples from $100$ simulated worlds resembling an office workspace created in Gazebo. (b) Real dataset collected by [@sturm12iros] using a RGBD camera. (c) Plot of cumulative reward with time steps for [QvalAgg]{.smallcaps} and baseline heuristics on the real dataset. (d) The 3D model of the real office workspace formed by cumulating measurements from all poses. (e) Snapshots of execution of Occlusion Aware heuristic at time steps $1,3, 5, 9$. (f) Snapshots of execution of [QvalAgg]{.smallcaps} heuristic at time steps $1,3, 5, 9$. []{#fig:results:cpp label="fig:results:cpp"}
:::
::::

:::: {#fig:result:agg .figure latex-placement="t"}
![](Choudhury2017Datadriven_figs/cem_vs_agg.png){width="\\textwidth"}

::: caption
(a) Comparison of [RewardAgg]{.smallcaps} with CEM policy search. Both algorithms are given access to the same amount of data. The final policy from CEM and the best validation policy of [RewardAgg]{.smallcaps} are then executed on a test dataset. [RewardAgg]{.smallcaps} outperforms CEM not only overall but pointwise at each timestep. (b) Comparison of [RewardAgg]{.smallcaps} with [ForwardTraining]{.smallcaps}. Each policy in [ForwardTraining]{.smallcaps} is trained with a dataset size of $500$. [RewardAgg]{.smallcaps} is trained with $100$ samples per iteration for 10 iteration. The performance of both policies on test dataset is shown. [RewardAgg]{.smallcaps} surpasses [ForwardTraining]{.smallcaps} at the $4^{th}$ iteration and never drops below. At iteration 5 the single policy of [RewardAgg]{.smallcaps} has the same dataset size as each policy of the $10$ policies of [ForwardTraining]{.smallcaps}. However the single policy still outperforms the nonstationary policy. []{#fig:result:agg label="fig:result:agg"}
:::
::::

## Analysis of Results

Fig. [7](#fig:results:extra){reference-type="ref" reference="fig:results:extra"} shows the utility of all algorithms on various synthetic datasets. The two numbers are lower and upper $95\%$ confidence intervals of the episodic utility of each algorithm. The best performance on each dataset is highlighted. For Problem [Hidden-Unc]{.smallcaps}, [RewardAgg]{.smallcaps} is employed along with baseline heuristics. For Problem [Hidden-Con]{.smallcaps}, [QvalAgg]{.smallcaps} is employed with baseline heuristic augmented with motion penalization. The train size is $100$ and test size is $10$. We present a set of observations to interpret these results.

::: observation
**O 1**. *The learnt policy from [RewardAgg]{.smallcaps}/ [QvalAgg]{.smallcaps} has a consistently competitive performance across all datasets.*
:::

Fig. [7](#fig:results:extra){reference-type="ref" reference="fig:results:extra"} shows the performance of all algorithms on a set of 2D and 3D datasets. We see that out of the $10$ datasets, the learners perform better than any heuristic on $8$. On $2$ of the datasets, the Average Entropy heuristic outperforms the learner by a small margin. On examining the datasets, we see that the unknown space exploration behaviour of Average Entropy results in good performance in environments that either lack spatial correlation or contain objects distributed in the environment.

::: observation
**O 2**. *The performance of heuristics vary widely across datasets, however, the performance of the learner is robust.*
:::

We can see that the relative ranking of Average Entropy and Rear Side Voxel interchanges from Dataset 1 to 2. This motivates the need for adaptive policies that assign different utility to unknown cells conditioned on the environment in which the robot is operating. The learner's policy on the other hand adapts to different environments and hence maintains a consistently good performance. Interestingly, it also outperforms the heuristic pointwise across datasets, which is indicative of the fact that the adaptation happens during exploration as well.

::: observation
**O 3**. *The performance margin of [RewardAgg]{.smallcaps} in Problem [Hidden-Unc]{.smallcaps} as compared to heuristics is much larger than that of [QvalAgg]{.smallcaps} in Problem [Hidden-Con]{.smallcaps}*
:::

This is seen to be especially true in Dataset 1, 2 and 4. As conjectured in Section [5.2.1](#sec:approach:ipp:one_step_reward){reference-type="ref" reference="sec:approach:ipp:one_step_reward"}, this can be attributed to two reasons. Firstly, the near-optimality guarantee in Theorem [3](#theorem:hidden_unc){reference-type="ref" reference="theorem:hidden_unc"} of imitating a Clairvoyant one-step-reward bounds the performance of the learner. Secondly, the empirical regression regret of imitating one step reward values will be much lower than trying to estimate the action values using features from the history $\psi_t$, i.e. it is easier to predict the immediate utility of going to a sensing location than trying to predict the future utility.

::: observation
**O 4**. *The performance of Average Entropy in the Poisson Forest dataset is at par with the learner.*
:::

The Poisson Forest dataset is created by sampling circles in the environment from a spatial Poisson distribution where the density of the forest is specified. The lack of spatial correlation, implies it is equally likely to find objects anywhere in the world - an assumption that Average Entropy optimizes.

## Case study A: Adaptation to Different Environments

We created a set of 2D exploration problems to gain a better understanding of the learnt policies and baseline heuristics. We did this both for Problem [Hidden-Unc]{.smallcaps}(Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"}) and [Hidden-Con]{.smallcaps}(Fig. [9](#fig:results:matlab_con){reference-type="ref" reference="fig:results:matlab_con"}). The dataset comprises of 2D binary world maps, uniformly distributed nodes and a simulated laser. The problem details are $T=30$ and $|\mathcal{A}|=300$. The cost budget for [Hidden-Con]{.smallcaps} is $B= 2500$. The train size is $100$, test size is $100$. [RewardAgg]{.smallcaps} and [QvalAgg]{.smallcaps} is executed for $10$ iterations.

### Dataset 1: Parallel Lines

We first examined Problem [Hidden-Unc]{.smallcaps}. Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (a) shows a dataset created by applying random affine transformations to a pair of parallel lines. This dataset is representative of information being concentrated in an area in the environment, e.g. powerline inspection. Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (c) shows a comparison of [RewardAgg]{.smallcaps}, [RewardFT]{.smallcaps} with baseline heuristics. While Rear Side Voxel outperforms Average Entropy, [RewardAgg]{.smallcaps} outperforms both. Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (e) shows progress of each. Average Entropy explores the whole world without focusing, Rear Side Voxel exploits early while [RewardAgg]{.smallcaps} trades off exploration and exploitation.

The same trend can be observed in Problem [Hidden-Con]{.smallcaps}. Fig. [9](#fig:results:matlab_con){reference-type="ref" reference="fig:results:matlab_con"} (c) shows a comparison of [QvalAgg]{.smallcaps} with baseline heuristics. The heuristic Rear Side Voxel performs the best, while [QvalAgg]{.smallcaps} is able to match the heuristic. Fig. [9](#fig:results:matlab_con){reference-type="ref" reference="fig:results:matlab_con"} (e) shows progress of [QvalAgg]{.smallcaps} along with two relevant heuristics - Rear Side Voxel and Average Entropy. Rear Side Voxel takes small steps focusing on exploiting viewpoints along the already observed area. Average Entropy aggressively visits the unexplored area which is mainly free space. [QvalAgg]{.smallcaps} initially explores the world but on seeing parts of the lines reverts to exploiting the area around it.

### Dataset 2: Distributed Blocks

We first examined Problem [Hidden-Unc]{.smallcaps}. Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (b) shows a dataset created by randomly distributing rectangular blocks around the periphery of the map. This dataset is representative of information being distributed around. Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (d) shows that Rear Side Voxel saturates early, Average Entropy eventually overtaking it while [RewardAgg]{.smallcaps} outperforms all. Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (f) shows that Rear Side Voxel gets stuck exploiting an island of information. Average Entropy takes broader sweeps of the area thus gaining more information about the world. [QvalAgg]{.smallcaps} shows a non-trivial behavior exploiting one island before moving to another.

The same trend can be observed in Problem [Hidden-Con]{.smallcaps}. Fig. [9](#fig:results:matlab_con){reference-type="ref" reference="fig:results:matlab_con"} (d) shows that the heuristic Average Entropy performs the best, while [QvalAgg]{.smallcaps} is able to match the heuristic. Rear Side Voxel saturates early on and performs worse. Fig. [9](#fig:results:matlab_con){reference-type="ref" reference="fig:results:matlab_con"} (f) shows a similar trend as Fig. [8](#fig:results:matlab_unc){reference-type="ref" reference="fig:results:matlab_unc"} (f).

## Case study B: Train on Synthetic, Test on Real

To show the practical impact of our framework, we show a scenario where a policy is trained on synthetic data and tested on a real dataset. Fig. [10](#fig:results:cpp){reference-type="ref" reference="fig:results:cpp"} (a) shows some sample worlds created in Gazebo to represent an office desk environment on which [QvalAgg]{.smallcaps} is trained. Fig. [10](#fig:results:cpp){reference-type="ref" reference="fig:results:cpp"} (b) shows a dataset of an office desk collected by TUM Computer Vision Group [@sturm12iros]. The dataset is parsed to create a pair of pose and registered point cloud which can then be used to evaluate different algorithms. Fig. [10](#fig:results:cpp){reference-type="ref" reference="fig:results:cpp"} (c) shows that [QvalAgg]{.smallcaps} outperforms all heuristics. Fig. [10](#fig:results:cpp){reference-type="ref" reference="fig:results:cpp"} (f) shows how [QvalAgg]{.smallcaps} learns a desk exploring policy by circumnavigating around the desk. This shows the powerful generalization capabilities of the approach. In contrast, the best heuristic Occlusion Aware gets stuck in a local minima(Fig. [10](#fig:results:cpp){reference-type="ref" reference="fig:results:cpp"} (e))

## Case study C: Policy Search vs Imitation Learning

We compared our approach to a baseline approach of policy search. We picked the problem setting [Hidden-Unc]{.smallcaps}, the dataset 'Concentrated Parallel Lines' and the trained policy using [RewardAgg]{.smallcaps}. We created a parametrized policy which was linear on the space of the information gain heuristics. The policy, parameterized by $\theta \in \mathbb{R}^6$, assigns at time $t$ to each vertex $v$, picks the action with the highest score as follows $$\begin{equation*}
  \mathop{\mathrm{arg\,max}}\limits_{v_t \in \mathcal{V}} \theta^T  \mathcal{I}\mathcal{G}_{}\left(v_t\right)
\end{equation*}$$ We train such a policy using a black-box sample efficient policy search method, Covariance Matrix Adaptation Evolution Strategy (CMAES) [@hansen2016cma]. CMAES is allowed $1000$ roll-outs, the same number of calls to oracle as [RewardAgg]{.smallcaps}(Note that CMAES actually has access to more information as they are full rollouts compared to single reward calls in [RewardAgg]{.smallcaps}). Fig. [11](#fig:result:agg){reference-type="ref" reference="fig:result:agg"}(a) shows comparison between the final policy trained by CMAES and the best policy on validation trained by [RewardAgg]{.smallcaps} on a held out test dataset. We see that [RewardAgg]{.smallcaps} outperforms CMAES not only on the cumulative reward by also at each time step. This confirms our hypothesis that model free policy improvement is slow to converge on account of sample inefficiency. It should be noted that the CMAES policy outperforms all the baseline heuristics as expected.

## Case study D: [ForwardTraining]{.smallcaps} vs [AggreVaTe]{.smallcaps}

We compared the training framework of [ForwardTraining]{.smallcaps}, which trains a different policy for every time-step with [AggreVaTe]{.smallcaps} that trains a single policy across all time steps. We wished to examine the following question - 'How much data does a the single [AggreVaTe]{.smallcaps} policy need to be competitive with [ForwardTraining]{.smallcaps}?'. We picked the problem setting [Hidden-Unc]{.smallcaps} and the dataset 'Concentrated Parallel Lines'. We trained [ForwardTraining]{.smallcaps} where each policy $\pi_t$ is given $500$ datapoints (hence for episode length $T=30$, a total of $15,000$ datapoints are used). We trained [RewardAgg]{.smallcaps} where each iteration has $100$ datapoints, and the the number of iterations is $10$. Hence the [RewardAgg]{.smallcaps} policy matches the same datasize as [ForwardTraining]{.smallcaps} at iteration $5$. Fig. [11](#fig:result:agg){reference-type="ref" reference="fig:result:agg"}(b) shows a comparison between [ForwardTraining]{.smallcaps} and [RewardAgg]{.smallcaps}. We see that [RewardAgg]{.smallcaps} outperforms [ForwardTraining]{.smallcaps} by iteration $4$, following which the performance converges and oscillates at values above [ForwardTraining]{.smallcaps}. Interestingly, at iteration $5$ [RewardAgg]{.smallcaps} outperforms [ForwardTraining]{.smallcaps} even though each policy in [ForwardTraining]{.smallcaps} has access to the same dataset size as [RewardAgg]{.smallcaps}. We conjecture that this might be because of the generalization effect across time-steps - [ForwardTraining]{.smallcaps} might be over-fitting as it reasons about timesteps individually.

# Experiments on Search Based Planning {#sec:res_search}

In this section, we extensively evaluate our approach on a set of search based planning problems for 2D planning on synthetic problems and more realistic 4D nonholonomic path planning problems encountered by UAVs flying at various speed regimes. We choose a wide variety of world distributions ranging from simple and intuitive environments, chosen to highlight the importance of exploiting environment structure in motion planning, to complex, heterogenous environments for analyzing scalability and robustness. We also present closed loop results on a UAV flying outdoors at high speeds.

Additionally, we have developed a simple and intuitive Python based planning pipeline to serve as a backend for the Gym environment. The planning environment exposes search as a policy and makes it easy to incorporate standard machine learning libraries [@2016arXiv160502688short; @DBLP:journals/corr/AbadiABBCCCDDDG16] with custom planning graphs that requires only environment images as input. We use this planning pipeline to conduct all our experiments. Source code and instructions can be found via our project page at this link: <https://goo.gl/YXkQAC>

## Problem Details {#sec:res_search:problem}

We first describe the 2D navigation task. Here, the world map $\phi$ is a 2D binary map. The graph $\mathcal{G}$ is a discrete lattice of size $200\times200$ where each node is connected to the $8$ neighbours. The robot has to plan from bottom-left to top-right of the lattice. Note that while the grid size for these problems are small, the edge evaluation for such a graph could be arbitrarily expensive in practice. For example, consider the problem of planning 2D routes for aircrafts. It is plausible to envision that the lattice resolution is $100m$ and the $200 \times 200$ lattice covers an area of $20km$. Evaluation of each edge of such a lattice requires collision checking with other dynamically moving aircrats, no-fly-zones and risk of flying over urban areas. This implies that a real time traffic control can only search a small fraction of the lattice.

We now describe a more realistic 4D nonholonomic path planning problem on a state lattice for problems encountered by UAVs. The term *nonholonomic path planning* [@laumond1998guidelines] refers to the fact that certain class of dynamical systems are constrained in the range of feasible motions the robot can execute [@KelNag03]. It is a common practice to approximate UAVs moving at high speeds as curvature constrained systems with unicycle dynamics [@dugar2017smooth; @dugar2017kappaite; @Choudhury_2014_7588]. We consider the problem of path planning for such systems by planning on a state-lattice [@pivtoraiko2009differentially]. We consider two classes of UAVs : an autonomous helicopter moving at speeds of $30 m/s$ and a quadrotor (DJI M100) flying at $5 m/s$.

The autonomous helicopter has a minimum radius of $50m$ and plans on a state-lattice $\mathcal{G}$ of resolution $25m$. The average degree of a node is $21$. The distance between start and goal is $600m$. The world $\phi$ is represented as a 3D binary grid map and a set of 3D no-fly-zones (represented as polygons with a height range). An edge evaluation requires that every state on an edge is at a clearance distnce from all obstacles. Expansion of each node takes $~1 ms$ on average. The robot is required to plan within a time budget of $500 ms$ thus corresponding to maximum of $500$ expansions.

The quadrotor has a minimum radius of $12.5m$ and plans on a state-lattice $\mathcal{G}$ of resolution $12.5m$. The average degree of a node is $9$. The distance between start and goal is $300 m$. The world is represented as a 3D binary grid map and a set of 3D no-fly-zones. Expansion of each node takes $~1 ms$ on average. The robot is required to plan within a time budget of $1000 ms$ thus corresponding to a maximum of $1000$ expansions.

## Baseline Approaches For Search Based Planning {#sec:res_search:baseline}

### Motion Planning Baselines

For 2D navigation, we compare against greedy best-first search with 2 commonly used heuristics - the euclidean distance ($h_{\textsc{EUC}}$) and the manhattan distance ($h_{\textsc{MAN}}$). We also use A\* algorithm as a baseline with $h_{\textsc{EUC}}$ heuristic. Additionally, we compare against the MHA\* algorithm [@aine2016multi] which has been proven to be an effective way of combining multiple, often unrelated, heuristics providing bounds on solution quality [@phillips2015efficient]. We use a simplified version which expands three different heuristics in a round-robin fashion - $\left[h_{\textsc{EUC}}, h_{\textsc{MAN}}, d_{OBS}\right]$, where $d_{OBS}$ is the euclidean distance to closest, *known* obstacle cell in $\mathcal{I}$.

For 4D nonholonomic planning problems, we use the Dubins distance [@dubins1957curves] as a heuristic.

### Machine Learning Baselines

We consider two learning baselines (a) Supervised Learning (SL) with data from roll-outs with $\pi_\mathrm{OR}$ and (b) Reinforcement Learning using evolutionary strategies (CEM) and Q-Learning (QL) with function approximation. These methods are explained in detail in Appendix [14](#appendix:ml_baseline_search){reference-type="ref" reference="appendix:ml_baseline_search"}.

## Imitation Learning Details {#sec:res_search:learning}

### Feature Extraction and Learner {#sec:res_search:learning:feature}

The policy maps the history $\psi$ to an action $a$ by learning a function approximation for the action value function $\hat{Q}(\psi, a)$. The tuple $\left(a, \psi\right)$ is mapped to a vector of features $f$. Here the history $\psi$ is represented as a concatenation of all lists, i.e $\psi_t = \{ \mathcal{O}, \mathcal{C}, \mathcal{I}\}$. The action $a$ is the vertex $v$ to expand.

We now describe the feature extraction for 2D navigation problems. Although technically, the features for a vertex $v$ should depend on the parent edge $e$ that leads to the vertex, we ignore this in practice and consider a vertex in isolation to calculate features. It is important to note that the features used must be easy to calculate (no high computational burden) and should only require information uncovered by search until that point in time(else it would count as extra expansions). We define the feature vector to be a concatenation of the two vectors i.e, $f= \left[f_{S}, f_{E}\right]$. *Search Based Features:* $f_{S}\left( v, \psi\right)$. These features depend on the state of the search only and does not probe the environment

1.  $(x_{v}, y_{v})$ - location of node in coordinate axis of occupancy map.

2.  $(x_{v_g}, y_{v_g})$ - location of goal in coordinate axis of occupancy map.

3.  $g_{v}$ - cost(number of expansions) of shortest path to start.

4.  $h_{\textsc{EUC}}$ - Euclidean distance to goal.

5.  $h_{\textsc{MAN}}$ - Euclidean distance to goal.

6.  $d_{TREE}$ - Depth of $v$ in the search tree so far.

*Environment Based Features:* $f_{E}\left( v, s\right)$. These features depend upon the environment uncovered so far, more specifically the vertices in $\mathcal{I}$.\

1.  $x_{OBS}, y_{OBS}, d_{OBSX}$ - coordinates and distance of closest node in $\mathcal{I}$ to $v$

2.  $x_{OBSX}, y_{OBSX}, d_{OBSX}$ - coordinates and distance of closest node in $\mathcal{I}$ to $v$ in terms of x-coordinate.

3.  $x_{OBSY}, y_{OBSY}, d_{OBSY}$ - coordinates and distance of closest node in $\mathcal{I}$ to $v$ in terms of y-coordinate

We discuss more about alternate representations and feature extraction ideas in Appendix [15](#appendix:representation_search){reference-type="ref" reference="appendix:representation_search"}.

For the 4D planning problems, we use a slightly altered feature representation which is $8$-dimensional.

1.  Normalized Euclidean distance to start.

2.  Normalized Euclidean distance to goal.

3.  Dot product between start, vertex and goal.

4.  Normalized Eubins distance to start.

5.  Normalized Eubins distance to goal.

6.  Normalized heading of vertex.

7.  Normalized distance of vertex from closest obstacle.

8.  Dot product between distance to obstacle and heading of vertex.

Such a feature representation is chosen as these terms are easy to compute and are informative in estimating the utility of expanding a vertex.

The learner is represented using a feed-forward neural network with two fully connected hidden layers containing \[100, 50\] units and ReLu activation. The model takes as input a feature vector $f\in \mathcal{F}$ for the pair $(v, s)$ and outputs a scalar cost-to-go estimate. The network is optimized using RMSProp [@rmsprop]. A mini-batch size of 64 and a base learning rate of 0.01 is used. The network architecture and hyper-parameters are kept constant across all environments. For experiments with the UAV, we use a random forest regression [@liaw2002classification].

:::: {#fig:results_table .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/results_table.png){width="\\textwidth"}

::: caption
[]{#fig:results_table label="fig:results_table"} Normalized cost of baselines on different environments (best in bold). The cost corresponds to average expansions on a test set of planning problems normalized between \[200, 5000\] (max possible: 40000). Planning parameters are - map size: $200\times200$,$T_{train}=1100$, $T_{test}=20000$. Data sizes are: train($200$), test($100$), validation($70$). [NONAME]{.smallcaps}parameters are - $k: 50, \beta_{0} = 0.7$. [NONAME]{.smallcaps}, CEM and QL are run for $N: 15$ iterations. SL uses $m:600$.
:::
::::

:::: {#fig:benchmark_results .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/benchmark_results.png){width="\\textwidth"}

::: caption
[]{#fig:benchmark_results label="fig:benchmark_results"} Evolution of search frontier (expanded(blue), invalid(black), unexpanded(white)) of [SaIL]{.smallcaps} compared with final snapshot of supervised learning (SL) and $h_{\textsc{EUC}}$ across all environments. [SaIL]{.smallcaps} expands far less states.
:::
::::

:::: {#fig:explanatory_result .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/explanatory_result.png){width="\\textwidth"}

::: caption
[]{#fig:explanatory_result label="fig:explanatory_result"} (a) [SaIL]{.smallcaps} learns to adapt to different environment distributions by directing search to areas where it expects to find gaps. Note [SaIL]{.smallcaps} does not have information about the entire environment, only the explored part. (b) On the 'Forest' dataset, [SaIL]{.smallcaps} converges faster that CEM and QL to a good policy. [SaIL]{.smallcaps} also converges consistently to a good policy across environments 'Gaps', 'Gaps+Forest', 'Maze.'
:::
::::

## Case Study B: Helicopter Path Planning

:::: {#fig:helicopter_results .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/helicopter_results.png){width="\\textwidth"}

::: caption
[]{#fig:helicopter_results label="fig:helicopter_results"} Experiments on path planning for an autonomous helicopter in a canyon environment. The environment is motivated from planning challenges as described in [@Choudhury_2014_7588]. (a) Dataset of canyon-like environments generated by a parametric distribution. (b) The search tree from A\* with Dubins distance heuristic on a test environment. The start point is shown by the axes. The expanded edges are shown in yellow. The planned path is shown in green. A\* expands $2531$ vertices and takes $7000 ms$. (c) The search tree for greedy search with Dubins distance heuristic. It expands $142$ vertices and takes $500 ms$. Note that most of the wasted expansions are where the tree tries to search through the canyon wall (d) [SaIL]{.smallcaps} expands only $18$ vertices and takes $100 ms$. It hugs the canyon wall till it reaches the goal.
:::
::::

:::: {#fig:uav_results_sail .figure latex-placement="!htbp"}
![](Choudhury2017Datadriven_figs/uav_results_sail.png){width="\\textwidth"}

::: caption
[]{#fig:uav_results_sail label="fig:uav_results_sail"} Experiments on path planning for a real quadrotor flying at high speed $5 m/s$ while avoiding no fly zones that represent a maze like scenario. (a) A dataset of mazes created from a parametric distribution (b) The search graph of A\* on the environment. It expands $1910$ states in the $1000 ms$ time budget without finding a path (c) The greedy search with Dubins distance expands $661$ vertices and takes $400 ms$. The remaining time is used to relax the path shown in green. (d) [SaIL]{.smallcaps} outperforms both and finds a path by expanding only $180$ vertices in $120 ms$. (e) The DJI M100 used for our experiments (f) An experiment where [SaIL]{.smallcaps} is running onboard the robot. A set of no fly zones is created and the robot has to fly through it. The robot view and onboard imagery is shown (g) A time lapse of the search tree as the robot replans while performing the mission. We can see that the search tree remains sparse through out and [SaIL]{.smallcaps} is always able to find a path.
:::
::::

### Dataset Creation

The 2D world maps are created by randomly distributing geometric objects such as rectangles and circles according to hand design parametric distribution. Each environment class is representative of challenging artifacts in motion planning such as narrow corridors, local minimas, single homotopies. Hetergenous environments are created to show that the heuristic can deal with such problems as well.

For the experiment with a real robot, a dataset of mazes was created and a real life maze was simulated using no-fly-zones.

### Clairoyant Oracle

We use the backward Djikstra algorithm as the clairvoyant oracle. It is executed till it expands to all states, or till it reaches a cost-to-go limit. We note that using such an oracle for higher dimensions might be infeasible in higher dimensions and discuss remedies in Section [8](#sec:discussion){reference-type="ref" reference="sec:discussion"}.

### Practical Algorithm Implementation

Since the size of the action space changes as more states are expanded, the [SaIL]{.smallcaps} algorithm requires a forward pass through the model for every action individually unlike the usual practice of using a network that outputs cost-to-go estimate for all actions in one pass as in [@mnih-dqn-2015]. This can get computationally demanding as the search progresses ($\mathcal{O}\left(N\right)$ in actions). Instead, we use a *priority queue* as $\mathcal{O}$ which sorts vertices in increasing order of the cost-to-go estimates as is usually done in search based motion planning. The vertex on the top of the list is then expanded. We use two priority queues, sorted by the learner and oracle's cost-to-go estimates respectively. This allows us to take actions in $\mathcal{O}\left(1\right)$ but forces us to freeze the *Q*-value for a vertex to whenever it is inserted in $\mathcal{O}$. Despite this artificial restriction over the policy class $\Pi$, we are able to learn efficient policies in practice. However, we wish to relax this requirement in future work. We also analyze the time complexity in Appendix [16](#appendix:sail_complexity){reference-type="ref" reference="appendix:sail_complexity"}.

## Analysis of Results

Fig. [12](#fig:results_table){reference-type="ref" reference="fig:results_table"} shows the normalized evaluation cost of all algorithms on various datasets. Snapshots of planning with different heuristics are shown in Fig. [13](#fig:benchmark_results){reference-type="ref" reference="fig:benchmark_results"} and Fig. [14](#fig:explanatory_result){reference-type="ref" reference="fig:explanatory_result"} (a). Convergence of different learning algorithms are shown in Fig. [14](#fig:explanatory_result){reference-type="ref" reference="fig:explanatory_result"} (b). We present a set of key observations to summarize these results.

::: observation
**O 5**. *[SaIL]{.smallcaps} has a consistently competitive performance across all datasets.*
:::

Fig. [12](#fig:results_table){reference-type="ref" reference="fig:results_table"} shows that [SaIL]{.smallcaps} learns a better search policy than any other baseline across all but one environments. It maintains performance from homogenous to heterogenous environments.

::: observation
**O 6**. *[SaIL]{.smallcaps} has faster convergence than all learning baselines.*
:::

Fig. [14](#fig:explanatory_result){reference-type="ref" reference="fig:explanatory_result"} (b) shows that on the 'Forest' dataset, [SaIL]{.smallcaps} converges by $6^\text{th}$ iteration, while CEM takes $12$ and QL does not converge. [SaIL]{.smallcaps} also converges quickly (by the $8^\text{th}$ iteration) across datasets.

::: observation
**O 7**. *[SaIL]{.smallcaps} is able to detect and escape local minima.*
:::

A classic case in motion planning is the bugtrap (Fig. [1](#fig:marquee){reference-type="ref" reference="fig:marquee"} (b) ) which traps a greedy search in a local minimum. Fig. [13](#fig:benchmark_results){reference-type="ref" reference="fig:benchmark_results"} (a) and Fig. [13](#fig:benchmark_results){reference-type="ref" reference="fig:benchmark_results"} (f) shows that when trained on such distributions, [SaIL]{.smallcaps} is able to detect these artifacts and smartly escape them by exploring in different directions.

::: observation
**O 8**. *[SaIL]{.smallcaps} is able to exploit the relative configuration of obstacles and environment structure.*
:::

In a maze world with rectilinear hallways (Fig. [13](#fig:benchmark_results){reference-type="ref" reference="fig:benchmark_results"} (e)), [SaIL]{.smallcaps} learns to quickly find a wall and then concentrate the search along the axes. In Fig. [13](#fig:benchmark_results){reference-type="ref" reference="fig:benchmark_results"} (d), [SaIL]{.smallcaps} focuses only on regions where there is a high probability of a gap and skids along obstacles otherwise.

## Case Study A: Adaptive behaviour of [SaIL]{.smallcaps}

We take a closer look at the behaviour of [SaIL]{.smallcaps} in response to a change in the distribution of worlds that it is being trained on $P(\phi)$. Consider the scenario illustrated in Fig. [14](#fig:explanatory_result){reference-type="ref" reference="fig:explanatory_result"} (a). We create two datasets. Both datasets have a wall in the middle of the environment, with a gap in the wall. For dataset $1$, the gap can occur uniformly randomly along the y-axis. For dataset $2$, the gap either occurs with $70\%$ probability at the bottom and $30\%$ probability at the top.

For dataset $1$, [SaIL]{.smallcaps} learns to approach the centre of the environment first and then search along the wall till it finds a gap. This is in response to the fact that the gap can occur anywhere and hence this is a cost efficient strategy. Contrast this to a greedy search that get stuck expanding states near the top of the wall.

For dataset $2$, [SaIL]{.smallcaps} learns to approach the bottom of the environment first and then search along the wall. This is in response to the gaps occuring at the bottom of the wall. The greedy search is non responsive to the change in distribution and gets stuck expanding states near the top again.

An important application of heuristic learning is to speed up high dimension search. An application of particular relevance to us is an autonomous helicopter [@Choudhury_2014_7588]. A class of environment in which the helicopter has to plan in is a canyon like environment. Since the system moves at a speed of $30 m/s$, it has to produce a plan in real-time (within $200 ms$) otherwise it risks reaching states from which collision is inevitable.

We use [SaIL]{.smallcaps} to learn a heuristic that guides search in such environments. We collect a dataset by generating canyons using a parametric distribution as showing in Fig. [15](#fig:helicopter_results){reference-type="ref" reference="fig:helicopter_results"} (a). A lattice, with the specifications described in Section [7.1](#sec:res_search:problem){reference-type="ref" reference="sec:res_search:problem"} is created. As a baseline, we run A\* with Dubins distance as the heuristic on this problem. As shown in Fig. [15](#fig:helicopter_results){reference-type="ref" reference="fig:helicopter_results"} (b), this ends up expanding a large number of vertices ($2531$). This is because the Dubins distance is not the optimal cost to do. The under-estimation of this heuristic results in a large number of vertices being expanded and hence a long planning time ($7000 ms$).

We also run a greedy search using the Dubins distance as a heuristic. We see that for these kind of environments, greedy search performs pretty good - the number of vertices expanded is $142$ and planning time is $500 ms$. However, the greedy search expends search effort trying to search for a tunnel through the canyon.

[SaIL]{.smallcaps} has much better performance than either of these baselines. It is able to learn a heuristic that expands only $18$ vertices with a search time of $100 ms$. The features used by [SaIL]{.smallcaps} are minimialistic and are enlisted in Section [7.3.1](#sec:res_search:learning:feature){reference-type="ref" reference="sec:res_search:learning:feature"}. Among those features are the Dubins distance to the goal and the direction vector to the nearest obstacle. By examining the search tree produced by [SaIL]{.smallcaps}, we observe that it learns a trade-off between following the Dubins distance heuristic and not expanding states that are pointing into the canyon wall (as such states would not result in a feasible path eventually).

## Case Study C: Quadrotor Path Planning

We also applied this approach to a real quadrotor which has to navigate in an environment at high speed $5 m/s$ while avoiding no fly zones. No fly zones can result from areas that a UAV cannot fly over because of risks to property or from other vehicles in the area. These no fly zones can be arbitrary in complexity thus creating artifacts such as a maze as shown in Fig [16](#fig:uav_results_sail){reference-type="ref" reference="fig:uav_results_sail"}.

We create a dataset of such mazes by means of a parametric distribution as shown in Fig [16](#fig:uav_results_sail){reference-type="ref" reference="fig:uav_results_sail"} (a). We give a time budget of $1000 ms$ for planners to solve the problem. A\* with Dubins heuristic is unable to solve the problem in the time limit as shown in Fig [16](#fig:uav_results_sail){reference-type="ref" reference="fig:uav_results_sail"} (b). This is because the Dubins distance vastly under-estimates the distance to the goal in this environment. A\* expands $1910$ states before being terminated.

Greedy search with Dubins heuristic is able to find a path after $661$ expansions within the time budget (in $400 ms$). The remaining time is spent relaxing the path found. The greedy behaviour is beneficial in this environment because it results in a wall following like behaviour. However the algorithm wastes search effort expanding states perpendicular to the wall which would lead to inevitable collision.

[SaIL]{.smallcaps} outperforms both algorithms by finding a path in $180$ expansions (in $120 ms$). The remaining time is spent relaxing the path. As can be seen for the search graph, it focuses on expanding paths perpendicular to the wall. It learns to not expand vertices that point into the wall since the oracle shows the cost to go of such nodes to be $\infty$.

We also evaluated [SaIL]{.smallcaps} on board a DJI M100 quadrotor equipped with a TX2 computer. We created a synthetic maze with no fly zones and commanded the robot to fly through it (Fig [16](#fig:uav_results_sail){reference-type="ref" reference="fig:uav_results_sail"} (e-f) ). [SaIL]{.smallcaps} is able to find a path expanding a sparse number of vertices. As the robot follows the path, the algorithm is able to consistently replan and find a path consistently without expanding too many states (Fig [16](#fig:uav_results_sail){reference-type="ref" reference="fig:uav_results_sail"} (g) ).

# Discussion and Future Work {#sec:discussion}

We presented a novel data-driven imitation learning framework to learning planning policies. Our approach trains a policy to imitate a clairvoyant oracle that has full information about the world and can compute optimal planning decisions. We examined two problem domains - informative path planning and search based planning. We evaluated our approach in both these domains and showed that the learnt policy can outperform state-of-the-art approaches. We now discuss a set of relevant questions and directions for future work.

## When does this framework lead to good policies? What are some failure cases? {#sec:discussion:success_failures}

:::: {#fig:clairvoyant_failure_case .figure latex-placement="t"}
![](Choudhury2017Datadriven_figs/clairvoyant_failure_case.png){width="\\textwidth"}

::: caption
The robot in a dark room problem. The robot is uncertain about the location of a door and the only way to collapse that uncertainty is to pull a light switch. (a) A clairvoyant oracle is not incentivized to flip the switch and hence the robot does not learn to collapse uncertainty (b) The optimal POMDP policy would be to flip the switch and then head for the door.
:::
::::

MDP framework provides an elegant way of posing problems where the complete state of the problem space is known. The value of an action for a given state in an MDP is given by equation [\[eq:hallucinating_oracle_repeat\]](#eq:hallucinating_oracle_repeat){reference-type="ref" reference="eq:hallucinating_oracle_repeat"}. $$\begin{equation}
\label{eq:hallucinating_oracle_repeat}
Q^{\pi}_{t}(s, a) = R{}\left(s, a\right) + \mathbb{E}_{s' \sim P(s' \mid s, a)}\left[
V^{\pi}_{t-1}(s')\right]
\end{equation}$$ $$\begin{equation}
	V^{\pi}_{t}(s) = \sum\limits_{i=t}^{T} \mathbb{E}_{s_t \sim P(s_{i}| \pi, i,s)}\left[R{}\left(s_i, \pi(s_i)\right)\right]
\end{equation}$$

The optimal MDP policy maximizes the expected cumulative reward, i.e $\pi^*(s_t) \in \mathop{\mathrm{arg\,max}}\limits_{\pi\in \Pi} V^{\pi}_{t}(s_t)$.

However there are 2 major challenges that POMDP solvers face-

- Computing the expectation over the state space. Since the state space of most of the problems worth solving is large, computing an expectation over such state space needs a large number, making it expensive to evaluate online.

- Keep track of evolving uncertainty about the state space over the planning horizon.

Our approach solves the first challenge through data driven techniques - the MDP solvers are used over sampled MDP problems to train a policy on the expected distribution of problems. The hallucinating oracle is similar in nature to a QMDP algorithm [@Littman95learningpolicies], an effective approximate solution to POMDPs, which takes the best action on the current posterior. However, while QMDP requires maintaining an explicit posterior, our framework does not. QMDP has been shown to be very successful where explicit information gathering behaviour is not required [@Koval-RSS-14; @javdani2015shared] - the belief collapses irrespective of the action. Hence this optimization assumes a fixed belief and does not account for evolving belief over time, (which is challenge 2 for POMDP's). This implies there is no motivation for the MDP solver and hence the learnt policy to change the belief.

These kind of methods work quite well in POMDP problems where the required changes in belief can be attained by actions that are rewarding as well. This is very apt in the problem we address - as the set of actions are constrained to candidate nodes in the open list, no single action is very informative. It suffices to expand the best node under the current belief and continue to update the belief as the open list evolves. And there exists no action that is not rewarding while reducing the uncertainty. We note that this is not true for all learning in planning paradigms. For example, when learning to collision check [@choudhury2017active], a policy that actively reduces uncertainty about the world is effective.

To illustrate the failure case, we present a simple scenario as shown in Fig [17](#fig:clairvoyant_failure_case){reference-type="ref" reference="fig:clairvoyant_failure_case"}. We have a 'trapped robot' whose task is to escape from a room, i.e. it gets a reward for escaping and penalization for staying in the room. The room is dark, i.e. the robot cannot observe the location of the door. It can performa actions such as moving in the room. It can also perform an action of flicking on the light switch. On performing such an action, it receives an observation containing the location of the door. An optimal POMDP policy would always choose this action, collapse uncertainty about the door location and subsequently head straight for the door. However, imitation of clairvoyant oracles do not provide such behaviours. The oracle, at training, always guides the robot towards the door to maximize reward and is not incentivized to flip the light switch. The policy learns a blind search pattern which takes a long time to find the door.

For such POMDP problems, one way forward would be to incentivize the oracle at train time to reduce the uncertainty as suggested by the POMDP-lite approach [@chen2016pomdp]. While POMDP-lite quantifies uncertainty reduction as L1-norm of the belief change, this can be hard to compute for the space of world maps. Using approximations to this belief change would be an interesting direction of future work.

## How can we incorporate solution cost in addition to search effort in this framework? {#sec:discussion:anytime_search}

While our framework ignores the cost of a solution, we note that finding feasible solutions quickly is the core motivation of a number of high dimensional planning problems which have historically resorted to sampling based approaches [@kuffner2000rrt]. Hence, one can apply our framework to such problems to produce potentially faster solutions. We also note that when planning on locally connected lattices for geometric planning problems, minimizing the number of expansions generally leads to near-optimal solutions (unit cost for each valid edge).

However, if we really cared about near optimal solutions, the framework of Multi-heuristic A\* (MHA\*) [@aine2016multi] can be easily adopted. In such a framework, any heuristic function [@narayanan2015improved] can be used in tandem with an anchored search which uses an inflated admissible heuristic. Hence we can simply replace our $\mathtt{Search}$ function with MHA\*.

The bi-objective criteria of solution cost and search effort is best reasoned about in the paradigm of *anytime planning*. In this paradigm, an algorithm traces out the *pareto-frontier* [@choudhury2016pareto] - finds a feasible solution quickly and iteratively improves it. In this paradigm, [SaIL]{.smallcaps} trains a heuristic that displays a behaviour we would expect in the first iteration. A direction of future work would be to learn *anytime heuristics* that minimize search effort initially to and solution cost eventually.

## Can we generalize this framework to sampling based planners?

The [SaIL]{.smallcaps} framework defines $\mathtt{Search}$ in a very general way - the underlying implicit graph can also be a tree and the expansion operation can be a local steering operation akin to the framework of EST [@hsu1999placing]. The oracle design is an open question - a plausible oracle is growing a backward tree from the goal and using a k-NN value function approximator. Another paradigm to consider is when the $\mathtt{Expand}$ operation is a call to a *sampler*. For example, the framework in Randomized A\* (RA\*) [@diankov2007randomized] proceeds by selecting a node of the search tree using some criteria and sampling around it.

Recently, [@ichter2017learning] proposed a framework for learning sampling distributions from optimal paths during training by using a conditional variational auto-encoder (CVAE). However, in this framework sampling and planning are decoupled, i.e. the sampling policy learns a good stationary distribution from which samples are generated and provided to the planner. Hence the planner does not adapt during the planning cycle. Such a stationary distribution can be very hard to learn as directly predicting the optimal path requires conditioning on a lot of information about the environment.

[SaIL]{.smallcaps} can be extended to learn sampling policies that address this problem. The CVAE can condition on the state of the search (similar to the feature vector used by [SaIL]{.smallcaps}). The labels can be obtained by a backward tree from the goal grown during training. The iterative learning process of [SaIL]{.smallcaps} will ensure that the CVAE is trained on the distribution of search state actually encountered rather than simply using the optimal path.

## Incorporating noise in transition and observation for IPP problems {#sec:discussion:noisy}

The informative path planning problem that we defined in Section [2.1.1](#sec:background:ipp:framework){reference-type="ref" reference="sec:background:ipp:framework"} and subsequently mapped to a POMDP in Section [3.2](#sec:problem_formulation:ipp_mapping){reference-type="ref" reference="sec:problem_formulation:ipp_mapping"} consider a deterministic measurement and utility function. This can always be relaxed in an ad-hoc way: the occupancy map used to represent $\psi_t$ is essentially a Bayes' filter and can handle noisy observations, and the policy can also handle motion uncertainty since during the training phase, data collected in the initial stages is from random motions of the learner.

However, if one is to formally incorporate noise, the mapping needs to be re-examined. The crucial change arises from the fact that the utility function $\mathcal{F}$ is no longer dependent only on the sequence of vertices visited $\{ v_i \}_{i=1}^t$ and the world $\phi$. It also depends on the actual observations received $\{ y_i \}_{i=1}^t$, i.e. the utility function needs to be redefined to have the following arguments $\mathcal{F}\left(\{ v_i, y_i \}_{i=1}^t, \phi\right)$.

To provide a concrete example, we re-examine our application of 3D reconstruction of objects in the environment presented in Section. [6.1](#sec:res_ipp:problem){reference-type="ref" reference="sec:res_ipp:problem"}. We had assumed that each vertex $v_i$ in a path $\xi$ is associated with a unique measurement $y_i$. The union of all measurements defined the coverage map $C$ which in turn defined the utility. Since this unique measurement assumption is no longer true, the coverage map has to explicitly consider the actual measurements received. This results in a utility function $\mathcal{F}\left(\{ v_i, y_i \}_{i=1}^t, \phi\right)$ that depends on measurements as well.

Keeping this important change in mind, we redefine the mapping to POMDP. The state is defined to contain all information that is required to define the reward, observation and transition functions. Let the state be the set of nodes visited *and measurements received* as well as the underlying world, $s_t = \{ \{ v_i, y_i \}_{i=1}^t, \phi\}$. At the start of an episode, a world is sampled from a prior distribution $\phi\sim P(\phi)$ along with a graph $\mathcal{G}\sim P(\mathcal{G})$. The initial state is assigned by setting $s_1 = \{ v_1, y_1, \phi\}$. Note that the state $s_t$ is partially observable due to the hidden world map $\phi$.

We define the action $a_t$ to be the next *desired node* to visit. The reward function is now defined as a function of the state $s_t$ only as the marginal gain in utility on receiving $\{v_t, y_t\}$. The marginal gain of the utility function $\mathcal{F}$ is $\Delta_\mathcal{F}\left(\{ v_t, y_t \} \mid \{ v_t, y_t \}_{i=1}^{t-1}, \phi\right) = \mathcal{F}\left( \{ v_i, y_i \}_{i=1}^t , \phi\right) - \mathcal{F}\left( \{ v_i, y_i \}_{i=1}^{t-1} , \phi\right)$. Additionally, the reward is set to $-\infty$ whenever the cost budget is violated, i.e. $R{}\left(s, a\right) =$ $$\begin{equation}
	\begin{cases}
	\Delta_\mathcal{F}\left(\{ v_t, y_t \} \mid \{ v_t, y_t \}_{i=1}^{t-1}, \phi\right) &\text{if $\mathcal{T}\left(\{ v_i\}_{i=1}^t, \phi\right) \leq B$} \\
	-\infty & \text{otherwise}
	\end{cases}
\end{equation}$$

The state transition function, $\Omega{}\left(s, a, s'\right)$, is defined by the execution model $P(v_{t+1} | a_t, \phi)$ and the measurement model $P(y_{t+1} | v_{t+1}, \phi)$. Given state $s_t$, the observation is now deterministic because it is contained in the state, i.e. $o_t = y_t$.

# Acknowledgement

We would like to thank Silvio Maeta, Vishal Dugar and Brian McAllister for help with flight test results on the UAV. We would like to thank Shushman Choudhury for insightful discussions and feedback on the paper. We would like to acknowledge the support from ONR grant N000141310821 and NASA contract NNX17CS56C.

:::::::::::::::::::: appendices
# Proof of Lemma 1 {#appendix:lemma_hallucinating}

::: lemma*
**Lemma 1**. *The **offline** imitation of **clairvoyant** oracle ([\[eq:imitateClairvoyantOracle\]](#eq:imitateClairvoyantOracle){reference-type="ref" reference="eq:imitateClairvoyantOracle"}) is equivalent to sampling **online** a world from the posterior distribution and executing a **hallucinating** oracle as shown*

*$$\begin{equation*}
\hat{\pi}= \mathop{\mathrm{arg\,max}}\limits_{\pi\in \Pi} \mathbb{E}_{
\substack{
t\sim U(1:T), \\
\psi_t \sim P(\psi| \pi, t)}}\left[\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \pi(\psi_t))\right]
\end{equation*}$$*
:::

::: proof
*Proof.* We will define two loss functions on the policy. Let $\mathcal{L}_1 (\pi)$ be the loss function corresponding to clairvoyant oracle, i.e.

$$\begin{equation}
	\mathcal{L}_1 (\pi) = \mathbb{E}_{\substack{t\sim U(1:T), \\
s_t, \psi_t \sim P(s, \psi| \pi, t)}}\left[ Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, \pi(\psi_t)) \right]
\end{equation}$$

Let $\mathcal{L}_2 (\pi)$ be the loss function corresponding to the hallucinating oracle, i.e. $$\begin{equation}
\label{eq:loss2}
	\mathcal{L}_2 (\pi) = \mathbb{E}_{
\substack{
t\sim U(1:T), \\
\psi_t \sim P(\psi| \pi, t)}}\left[\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \pi(\psi_t))\right]
\end{equation}$$

Substituting ([\[eq:hallucinating_oracle\]](#eq:hallucinating_oracle){reference-type="ref" reference="eq:hallucinating_oracle"}) in ([\[eq:loss2\]](#eq:loss2){reference-type="ref" reference="eq:loss2"}) we have

$$\begin{equation*}
\begin{aligned}
&\mathbb{E}_{
\substack{
t\sim U(1:T), \\
\psi_t \sim P(\psi| \pi, t)}}\left[\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \pi(\psi_t))\right] \\
&= \mathbb{E}_{
\substack{
t\sim U(1:T), \\
\psi_t \sim P(\psi| \pi, t)}}\left[ \mathbb{E}_{s_t \sim P(s_t | \psi_t)}\left[Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, \pi(\psi_t))\right]  \right] \\
&= \mathbb{E}_{t\sim U(1:T)}\left[ \sum\limits_{\psi_t, s_t} P(\psi_t | \pi, t) P(s_t | \psi_t) Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, \pi(\psi_t))  \right] \\
&= \mathbb{E}_{t\sim U(1:T)}\left[ \sum\limits_{\psi_t, s_t} P(s_t, \psi_t | \pi, t) Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, \pi(\psi_t))  \right] \\
&= \mathbb{E}_{\substack{t\sim U(1:T), \\
s_t, \psi_t \sim P(s, \psi| \pi, t)}}\left[ Q^{\pi_{\mathrm{OR}}}_{T-t+1}(s_t, \pi(\psi_t)) \right]
\end{aligned}
\end{equation*}$$

Hence $\mathcal{L}_1 (\pi) = \mathcal{L}_2 (\pi)$. ◻
:::

# Proof of Theorem 1 {#appendix:theorem_ft}

We begin with a statement of the *performance difference lemma* that is useful to bound the change in total reward-to-go. This general result bounds the difference in performance of any two policies.

::: {#lemma:pd .lemma}
**Lemma 2**. *Let $\pi$ and $\pi'$ be any two policies and denote $\tilde{V}_t'$ and $\tilde{Q}_t'$ be the t-step value function and action value function of policy $\pi'$ respectively, then: $$\begin{equation*}
\begin{aligned}
	&J\left(\pi\right) - J\left(\pi'\right) \\
	& = \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \pi, t)}\left[ \tilde{Q}^{\pi'}_{T-t+1}(\psi_t, \pi(\psi_t)) - \tilde{V}^{\pi'}_{T-t+1}(\psi_t) \right]
\end{aligned}
\end{equation*}$$*
:::

::: proof
*Proof.* Let $\pi_t$ be the policy that executes $\pi$ in first t timesteps and then switches to $\pi'$ fromt $t+1$ to $T$. We then have $J\left(\pi\right) = J\left(\pi_T\right)$ and $J\left(\pi'\right)=J\left(\pi_0\right)$. Thus: $$\begin{equation*}
\begin{aligned}
	&J\left(\pi\right) - J\left(\pi'\right) \\
	& = \sum\limits_{t=1}^T \left[ J\left(\pi_t\right) - J\left(\pi_{t-1}\right) \right] \\
	& = \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \pi, t)}\left[ \tilde{Q}^{\pi'}_{T-t+1}(\psi_t, \pi(\psi_t)) - \tilde{V}^{\pi'}_{T-t+1}(\psi_t) \right]
\end{aligned}
\end{equation*}$$ ◻
:::

We now state the theorem and the proof

::: theorem*
**Theorem 1**. *[ForwardTraining]{.smallcaps} has the following guarantee $$\begin{equation*}
\begin{aligned}
  J\left(\hat{\pi}\right) \geq J\left(\tilde{\pi}_{\mathrm{OR}}\right) -2 T \sqrt{\mathcal{A}\; \varepsilon_{\mathrm{class}}} + T\varepsilon_{\mathrm{or}}
\end{aligned}
\end{equation*}$$ where $\varepsilon_{\mathrm{class}}$ is the regression error of the learner, $\varepsilon_{\mathrm{or}}$ is the local oracle suboptimality.*
:::

::: proof
*Proof.* In [ForwardTraining]{.smallcaps}, the distribution of history $P(\psi| \hat{\pi}, t)$ is generated by the learner directly. Let the cost sensitive classification error $\varepsilon_{\mathrm{cs}}$ be the expected difference in action value selected by the policy and the best action, $\varepsilon_{\mathrm{cs}}=$ $$\begin{equation*}
\begin{aligned}
& \mathbb{E}_{\substack{t\sim U(1:T), \\
\psi_t \sim P(\psi| \hat{\pi}, t)}}\left[\max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) -\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}(\psi)) \right]
\end{aligned}
\end{equation*}$$

We also define the local oracle suboptimality $\varepsilon_{\mathrm{or}}$ being the minimum gap between oracle value and the best action value averaged over all time-steps, i.e. $\varepsilon_{\mathrm{or}}=$ $$\begin{equation*}
\mathbb{E}_{t\sim U(1:T)}\left[\min_{\psi_t} \left( \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right)\right]
\end{equation*}$$ This can be non-zero when the oracle is sub-optimal with respect to itself at any time-step. This is true in this setting as there is no guarantee that the hallucinating oracle will pick a locally optimal actions with respect to its own value function. This is true even if the clairvoyant oracle was locally optimal as in the case of search based planning.

Applying Lemma [2](#lemma:pd){reference-type="ref" reference="lemma:pd"} with $\pi= \hat{\pi}$, $\pi' = \tilde{\pi}_{\mathrm{OR}}$, we have $$\begin{equation*}
\begin{aligned}
	&J\left(\hat{\pi}\right) - J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
	& = \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}, t)}\left[ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}(\psi_t)) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right] \\
	& = \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}, t)} [ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}(\psi_t)) \\
	& - \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) ]  \\
	& + \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}, t)}\left[ \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right] \\
	& \geq -T \varepsilon_{\mathrm{cs}}+ \\
	& \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}, t)}\left[ \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right] \\
	& \geq -T \varepsilon_{\mathrm{cs}}+ T\varepsilon_{\mathrm{or}}
\end{aligned}
\end{equation*}$$

Hence we have the performance bound $$\begin{equation*}
J\left(\hat{\pi}\right) \geq J\left(\tilde{\pi}_{\mathrm{OR}}\right) -T \varepsilon_{\mathrm{cs}}+ T\varepsilon_{\mathrm{or}}
\end{equation*}$$

Interestingly, note that if $\varepsilon_{\mathrm{or}}\geq \varepsilon_{\mathrm{cs}}$, we would be guaranteed to do *better* than the hallucinating oracle.

Since we reduce cost sensitive classification to regression by uniformly sampling actions, we can express $\varepsilon_{\mathrm{cs}}$ in terms of the regression error $\varepsilon_{\mathrm{class}}$ using the reduction bound from ([@langford2005sensitive])

$$\begin{equation*}
	\varepsilon_{\mathrm{cs}}\leq 2 \sqrt{\mathcal{A}\;\varepsilon_{\mathrm{class}}}
\end{equation*}$$

Hence we have the performance bound $$\begin{equation*}
J\left(\hat{\pi}\right) \geq J\left(\tilde{\pi}_{\mathrm{OR}}\right) -2 T \sqrt{\mathcal{A}\; \varepsilon_{\mathrm{class}}} + T\varepsilon_{\mathrm{or}}
\end{equation*}$$ ◻
:::

# Proof of Theorem 2 {#appendix:theorem_aggrevate}

We follow the analysis of [@ross2014reinforcement] with two main difference:

1.  [@ross2014reinforcement] examine an MDP on states, we translate that to an MDP on history

2.  [@ross2014reinforcement] consider one step cost minimization, we consider one step reward maximization

We borrow a couple important Lemmas from [@ross2014reinforcement].

::: {#lemma:dist_mismatch .lemma}
**Lemma 3**. *Let $P$ and $Q$ be any two distributions over $x$, let $f(x)$ be a bounded function with range $r$. We then have $$\begin{equation*}
	\left| \mathbb{E}_{x \sim P}\left[f(x)\right] - \mathbb{E}_{x \sim Q}\left[f(x)\right]  \right| \leq \frac{r}{2} \left|\left| P-Q \right|\right|_{1}
\end{equation*}$$*
:::

::: {#lemma:mix_divergence .lemma}
**Lemma 4**. *Let $P(\psi| \pi_{\mathrm{mix},i})$ be the distribution of history encountered by the mixture policy over all time steps and $P(\psi| \hat{\pi}_i)$ be the distribution encountered by the learner. We have $$\begin{equation*}
	\left|\left|  P(\psi| \pi_{\mathrm{mix},i}) - P(\psi| \hat{\pi}_i)  \right|\right|_{1} \leq 2 \min (1, T \beta_{i})
\end{equation*}$$*
:::

We now state the theorem we wish to prove

::: theorem*
**Theorem 2**. *$N$ iterations of [AggreVaTe]{.smallcaps}, collecting $m$ regression examples per iteration guarantees that with probability at least $1-\delta$ $$\begin{equation*}
\begin{aligned}
	J\left(\hat{\pi}\right) \geq & J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
	& - 2 T \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) } \\
	& - \mathcal{O}\left(\frac{R \; T \log T}{N}\right) + T\varepsilon_{\mathrm{or}}\\
\end{aligned}
\end{equation*}$$ where $\varepsilon_{\mathrm{class}}$ is the empirical regression regret of the best regressor in the regression class on the aggregated dataset, $\varepsilon_{\mathrm{reg}}$ is the empirical online learning average regret on the sequence of training examples, $R$ is the range of oracle action value and $\varepsilon_{\mathrm{or}}$ is the local oracle suboptimality.*
:::

::: proof
*Proof.* We first define the local oracle suboptimality $\varepsilon_{\mathrm{or}}$ as in Appendix [11](#appendix:theorem_ft){reference-type="ref" reference="appendix:theorem_ft"} $$\begin{equation*}
\varepsilon_{\mathrm{or}}=  \mathbb{E}_{t\sim U(1:T)}\left[\min_{\psi_t} \left( \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right)\right]
\end{equation*}$$

We define the average cost sensitive classification error $\varepsilon_{\mathrm{cs}}$ $$\begin{equation*}
\begin{aligned}
& \varepsilon_{\mathrm{cs}}= \frac{1}{N} \sum_{i=1} ^ N\\
& \mathbb{E}_{\substack{t\sim U(1:T), \\
\psi_t \sim P(\psi| \pi_{\mathrm{mix},i}, t)}}\left[\max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) -\tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}(\psi)) \right]
\end{aligned}
\end{equation*}$$

Applying the performance difference lemma in Lemma [2](#lemma:pd){reference-type="ref" reference="lemma:pd"} with $\pi= \hat{\pi}_i$, $\pi' = \tilde{\pi}_{\mathrm{OR}}$, we have

$$\begin{equation*}
\begin{aligned}
	&J\left(\hat{\pi}_i\right) - J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
	& = \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}_i, t)}\left[ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}_i(\psi_t)) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right] \\
	& = \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}_i, t)} [ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}_i(\psi_t))  \\
	& - \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) ] \\
	& + \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}_i, t)}\left[ \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) - \tilde{V}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t) \right] \\
	& \geq \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \hat{\pi}_i, t)} [ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}_i(\psi_t)) \\
	& - \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) ] \\
	& + T\varepsilon_{\mathrm{or}}\\
\end{aligned}
\end{equation*}$$

We define the range $R$ of the maximum difference between the best and worst action value function of the oracle.

$$\begin{equation*}
R = \max_{t, \psi_t} \left| \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a)  - \min_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a)    \right|
\end{equation*}$$

We can then apply Lemma [3](#lemma:dist_mismatch){reference-type="ref" reference="lemma:dist_mismatch"} and Lemma [4](#lemma:mix_divergence){reference-type="ref" reference="lemma:mix_divergence"} with $P(\psi| \hat{\pi}_i, t)$ and $P(\psi| \pi_{\mathrm{mix},i}, t)$ to get $$\begin{equation*}
\begin{aligned}
	&J\left(\hat{\pi}_i\right) - J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
	& \geq \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \pi_{\mathrm{mix},i}, t)}[ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}_i(\psi_t)) \\ 
	& - \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) ] \\
	& - \frac{R}{2} \sum\limits_{t=1}^T \left|\left| P(\psi| \pi_{\mathrm{mix},i}, t) - P(\psi| \hat{\pi}_i, t) \right|\right|_{1} + T\varepsilon_{\mathrm{or}}\\
	& \geq \sum\limits_{t=1}^T \mathbb{E}_{\psi_t \sim P(\psi| \pi_{\mathrm{mix},i}, t)}[ \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, \hat{\pi}_i(\psi_t)) \\
	& - \max_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) ] \\
	& - R \;T \;\min (1, T \beta_{i}) + T\varepsilon_{\mathrm{or}}\\
\end{aligned}
\end{equation*}$$

If we now wish to bound the performance of the average learner over $N$ iterations $$\begin{equation*}
\begin{aligned}
	&J\left(\hat{\pi}_{\mathrm{avg}}\right) - J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
	& = \frac{1}{N} \sum_{i=1}^N \left| J\left(\hat{\pi}_i\right) - J\left(\tilde{\pi}_{\mathrm{OR}}\right)  \right| \\
	& \geq - T \varepsilon_{\mathrm{cs}}-  \frac{R \; T}{N} \sum_{i=1}^N \min (1, T \beta_{i}) + T\varepsilon_{\mathrm{or}}\\
	& \geq - T \varepsilon_{\mathrm{cs}}-   \frac{R \; T}{N} \frac{ \log(T) + 2}{\alpha}  + T\varepsilon_{\mathrm{or}}\\
\end{aligned}
\end{equation*}$$

where the last inequality follows from [@ross2014reinforcement] after setting $\beta_{i} = (1 - \alpha)^{i-1}$.

To bound $\varepsilon_{\mathrm{cs}}$, we need to define two terms: $\varepsilon_{\mathrm{class}}$, the empirical regression regret of the best regressor in the regression class on the aggregated dataset, and $\varepsilon_{\mathrm{reg}}$ the empirical online learning average regret on the sequence of training examples. We then use the following result from [@ross2014reinforcement] $$\begin{equation*}
\varepsilon_{\mathrm{cs}}\leq 2 \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) }
\end{equation*}$$ with probability $1-\delta$.

Also note that the performance of the best policy in the sequence $\hat{\pi}$ is better than the average learner, i.e. $J\left(\hat{\pi}\right) \geq J\left(\hat{\pi}_{\mathrm{avg}}\right)$.

This results in the following bound for [AggreVaTe]{.smallcaps} with probability $1-\delta$ $$\begin{equation*}
\begin{aligned}
	J\left(\hat{\pi}\right) \geq & J\left(\tilde{\pi}_{\mathrm{OR}}\right) \\
	& - 2 T \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) } \\
	& - \mathcal{O}\left(\frac{R \; T \log T}{N}\right) + T\varepsilon_{\mathrm{or}}\\
\end{aligned}
\end{equation*}$$ ◻
:::

# Proof of Theorem 3 {#appendix:theorem_hiddenunc}

::: theorem*
**Theorem 3**. *$N$ iterations of [AggreVaTe]{.smallcaps} with Clairvoyant one-step-reward collecting $m$ regression examples per iteration guarantees that with probability at least $1-\delta$ $$\begin{equation*}
\begin{aligned}
  J\left(\hat{\pi}\right) \geq & \left(1 - \frac{1}{e}\right)J\left(\pi^*\right) \\
  & - 2 T \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) } \\
  & - \mathcal{O}\left(\frac{R \; T \log T}{N}\right)\\
\end{aligned}
\end{equation*}$$ where $\varepsilon_{\mathrm{class}}$ is the empirical regression regret of the best regressor in the regression class on the aggregated dataset, $\varepsilon_{\mathrm{reg}}$ is the empirical online learning average regret on the sequence of training examples, $R$ is the maximum range of one-step-reward.*
:::

:::: proof
*Proof.* We use an important result from [@golovin2011adaptive] about the near-optimality properties of greedy maximization of an adaptive montonone and adaptive submodular set function. We define a greedy policy

The greedy algorithm selects a node to visit that has the highest expected marginal gain under the conditional distribution of world maps given the history. If the history of vertices visited and measurements received are where $\psi= \{ v_i \}_{i=1}^t, \{ y_i \}_{i=1}^t$, the greedy algorithm $\pi_{\mathrm{GR}}(\psi_t)$ selects node to visit $v_{t+1}$ with the highest expected marginal gain $$\begin{equation}
\label{eq:adaptive_greedy}
v_{t+1} = \mathop{\mathrm{arg\,max}}\limits_{v\in \mathcal{V}} \mathbb{E}_{\phi\sim P(\phi| \psi_t)}\left[\Delta_\mathcal{F}\left(v| \{ v_i \}_{i=1}^t , \phi\right)\right]
\end{equation}$$

[@golovin2011adaptive] show that the greedy algorithm $\pi_{\mathrm{GR}}$ has the following guarantee

::: {#lemma:adapt_sub .lemma}
**Lemma 5**. *If $\mathcal{F}$ is adaptive monotone and adaptive submodular with respect to $P(\phi)$ and $\pi_{\mathrm{GR}}$ is a greedy policy, then for all policies $\pi^*$ we have $$\begin{equation*}
	\mathbb{E}_{\phi\sim P(\phi)}\left[\mathcal{F}\left(\pi_{\mathrm{GR}}, \phi\right)\right] \geq \left( 1 - \frac{1}{e} \right) \mathbb{E}_{\phi\sim P(\phi)}\left[\mathcal{F}\left(\pi^*, \phi\right)\right]
\end{equation*}$$*
:::

We note that for the Clairvoyant one-step-reward oracle is defined such that $$\begin{equation}
\begin{aligned}
&\tilde{\pi}_{\mathrm{OR}}(\psi_t) = \mathop{\mathrm{arg\,max}}\limits_{a\in \mathcal{A}} \tilde{Q}^{\tilde{\pi}_{\mathrm{OR}}}_{T-t+1}(\psi_t, a) \\
&	= \mathop{\mathrm{arg\,max}}\limits_{v_{t+1} \in \mathcal{V}} \mathbb{E}_{\phi\sim P(\phi| \psi)}\left[  \Delta_\mathcal{F}\left(v_{t+1} | \{ v_i \}_{i=1}^t , \phi\right) \right]
\end{aligned}
\end{equation}$$ where the second inequality uses Definition [3](#def:clair_onestep_rew){reference-type="ref" reference="def:clair_onestep_rew"} along with Definition [2](#def:halluc){reference-type="ref" reference="def:halluc"}. Hence $\tilde{\pi}_{\mathrm{OR}}= \pi_{\mathrm{GR}}$. Also the local suboptimality is $\varepsilon_{\mathrm{or}}= 0$ since the oracle selects actions that maximize one-step-reward. Finally the range $R$ is that of the one step reward.

Hence applying these terms along with Lemma [5](#lemma:adapt_sub){reference-type="ref" reference="lemma:adapt_sub"} in Theorem [2](#theorem:aggrevate){reference-type="ref" reference="theorem:aggrevate"}, we have $$\begin{equation*}
\begin{aligned}
  J\left(\hat{\pi}\right) \geq & \left(1 - \frac{1}{e}\right)J\left(\pi^*\right) \\
  & - 2 T \sqrt{\left|\mathcal{A} \right| \left( \varepsilon_{\mathrm{class}}+ \varepsilon_{\mathrm{reg}}+ \mathcal{O}\left(\sqrt{\nicefrac{\log \nicefrac{1}{\delta}}{N m}}\right) \right) } \\
  & - \mathcal{O}\left(\frac{R \; T \log T}{N}\right)\\
\end{aligned}
\end{equation*}$$ ◻
::::

# Machine Learning Baselines for Search Based Planning {#appendix:ml_baseline_search}

## Supervised Learning (Behavior Cloning)

The supervised learning algorithm is identical to [SaIL]{.smallcaps} with the key difference that roll-outs are made with $\pi_{\mathrm{OR}}$ and not $\pi_{\mathrm{mix},i}$. This is equivalent to setting the mixing parameter $\beta= 1$ across all environments. For completeness, we present the algorithm below in Alg. [\[alg:supervised_learning\]](#alg:supervised_learning){reference-type="ref" reference="alg:supervised_learning"}

:::: algorithm
::: algorithmic
Initialize $\mathcal{D}\leftarrow \emptyset$ Collect datapoints as follows: Initialize sub-dataset $\mathcal{D}_{i} \leftarrow \emptyset$ Sample $\phi\sim P(\phi)$ Sample $\left( v_s, v_g\right) \sim P(v_s)$ Invoke clairvoyant oracle planner

to compute $Q^{\textsc{OR}}\left( v, \phi\right) \forall v\in \mathcal{V}$ Rollout a new search with $\pi_\mathrm{OR}$ At each timestep $t$ pick a random action $a_t$

to get corresponding $\left( v, s_t\right)$ Query oracle for $Q^{\textsc{OR}}\left( v, \phi\right)$ $\mathcal{D}_i \gets \mathcal{D}_{i} \cup \left< v, s_t, Q^{\textsc{OR}}\left( v, \phi\right) \right>$ Continue roll-out with $\pi_{\mathrm{OR}}$ till end of episode. Append to c.s classification data $\mathcal{D}\leftarrow \mathcal{D}\cup \mathcal{D}_{i}$ Train on $\mathcal{D}$ to get $\hat{\pi}$ **Return** $\hat{\pi}$
:::
::::

We use $m = 600$ for all the environments. The network architecture and hyper-parameters used are the same as [SaIL]{.smallcaps}.

## Q Learning with Function Approximation

We use an episodic implementation of the Q-learning algorithm which collects data in an iteration-wise manner similar to [SaIL]{.smallcaps}. The learner is trained on the aggregated dataset across all iterations by regressing to the TD-error. The aggregated dataset $\mathcal{D}$ effectively acts as an experience replay buffer to which helps in stabilizing learning when using neural network function approximation as has been suggested in recent work [@mnih-dqn-2015]. However,we do not use a target network or any other extensions over the original qlearning algorithm in our baselines [@DBLP:journals/corr/HasseltGS15; @DBLP:journals/corr/SchaulQAS15]. We also use only a single observation to take decisions and not a history length of past $h$ observations for a fair comparison with [SaIL]{.smallcaps} which also uses a single observation. Alg. [\[alg:q_learning\]](#alg:q_learning){reference-type="ref" reference="alg:q_learning"} describes the training procedure for the Q-learning baseline.

:::: algorithm
::: algorithmic
Initialize $\mathcal{D}\leftarrow \emptyset,\; \hat{\pi}_{1}$ to any policy in $\Pi$ Initialize sub-dataset $\mathcal{D}_{i} \leftarrow \emptyset$ Let mixture policy be

$\pi_{\mathrm{mix},i} = \epsilon  \text{-greedy on} \;  \hat{\pi}_{i} \; \text{with} \; \epsilon_{i}$ Collect *mk* datapoints as follows: Sample $\phi\sim P(\phi)$ Sample $\left( v_s, v_g\right) \sim P(v_s)$ Sample uniformly *k* timesteps $\left\lbrace t_{1}, t_{2}, \ldots, t_{k}\right\rbrace$

where each $t_{i} \in \ \left\lbrace 1, \ldots ,T\right\rbrace$ Rollout a new search with $\pi_{\mathrm{mix},i}$ At each $t\in\left\lbrace t_{1}, t_{2}, \ldots, t_{k}\right\rbrace$,

$\mathcal{D}_i \gets \mathcal{D}_{i} \cup \left< v, s_t, C, v_{t+1} \right>$ Continue roll-out with $\pi_{\mathrm{mix},i}$ till end of episode. Append to dataset $\mathcal{D}\leftarrow \mathcal{D}\cup \mathcal{D}_{i}$ Train learner by minimizing T.D error on $\mathcal{D}$

to get $\hat{\pi}_{i+1}$ **Return** Best $\hat{\pi}$ on validation
:::
::::

$C$ is the one step cost which is 1 for every expansion till goal is added to the open list. We use $k = 100$ and $\epsilon_{0} = 0.9$. Epsilon is decayed after every iteration in an exponential manner. Network architecture and params are kept the same as [SaIL]{.smallcaps}.

## Cross Entropy Method (C.E.M)

We use C.E.M as a derivative free optimization method for training [@goodfellow2016deep]. At each iteration of the algorithm we sample $\mathrm{batch_{size}} = 40$ set of parameters from a Gaussian Distribution. Each parameter is used to roll-out a policy on 5 environments each and the total cost is collected. The total cost (number of expansions) is used as the fitness function and the the best performing, $n_{elite} = 20\%$ of the parameters are selected. These elite parameters are then used to create a new Gaussian distribution (using sample mean and standard deviation) for the next iteration. At the end of all iterations, the best performing policy on a set of held-out states is returned. For this baseline, we use a simpler neural network architecture with one hidden layer of 100 units and ReLu activation.

# Representation for Search Based Planning {#appendix:representation_search}

In order to overcome the changing sizes of the observation and action spaces in our setting, we use insight from motion planning literature and represent an entire search state in terms of closest nodes in $\mathcal{O}$ to a set of pre-defined *attractor states* and *attractor paths*. Attractor states are manually defined states that can be thought of as landmarks trying to pull the search cloud in different directions. Such states can be useful in pulling the search out of local minima such as a bugtrap or they could be strategic orientations of the robot or an object the robot is trying to manipulate that lead to faster solutions [@aine2016multi]. Attractor paths on the other hand are solutions to a small subset of environments from the training dataset. In many episodic tasks, where the structure of the environment does not change drastically between planning iterations, such *path-reuse* can be very useful in finding solutions faster [@phillips2012graphs]. The planning algorithm is built into the environment, and the agent only receives as an observation the nodes in the open list closest to each attractor paths/states. At each iteration then, the action that the agent performs is to select a node from the observation to expand.

Although this is a generic framework that can be applied to many different problems, we chose not to use it for this work. The reason for this choice was that in this paper, our aim was to build the foundation for learning graph search heuristics as sequential decision making problem and clearly demonstrate the efficacy of the imitation learning paradigm in this domain. We found that using attractor paths/states would distract from the effectiveness of $\textsc{SaIL}$ and also make learning easier for other baseline methods.

In our final experiments, we instead featurize every pair $\left( v, s\right)$ using simple information based on the search tree and the environment uncovered up until that point.

# Analyzing the time complexity of [SaIL]{.smallcaps} {#appendix:sail_complexity}

The computational bottleneck in [SaIL]{.smallcaps} is the $\mathtt{Select}$ function which requires estimating the Q-value for every node in the open list $\mathcal{O}$. Contrast this with something like Dijkstra's algorithm which selects a node to expand in very little time, but wastes a lot of computation in excessively expanding nodes and evaluating edges. In order to analyze the usefulness of [SaIL]{.smallcaps} in terms of computational gains, we make the following assumptions. Firstly, we assume that the computational cost of calculating the Q-value of a single node(including feature calculation and forward pass through function approximator) is equal to the computational cost of $\mathtt{Expand}$ function (involves checking all edges coming out of a node for collision and calculating edge costs). This is in reality a very conservative approximation as in many high-dimensional planning problems, collision checking is way more computationally demanding as it requires expensive geometric intersection computations. We also ignore the computational cost of re-ordering the priority-queue whenever a node is popped which means Dijkstra's algorithm can select a node to expand in $O(1)$. Given a graph with cardinality $k$, we obtain the following time complexities for algSail and Dijkstra's algorithm.

## [SaIL]{.smallcaps} test time complexity: {#sail-test-time-complexity .unnumbered}

Assume [SaIL]{.smallcaps} did $A$ expansions before it found a solution starting from an empty $\mathcal{O}$. Also assume that states are never removed from $\mathcal{O}$. Total $\mathtt{Select}$ complexity: $O\left(k + 2k + 3k + \ldots + Ak\right) = O\left(kA^{2}\right)$ Total expansion complexity: $O(\sum_{i=1}^{A} k) = O(Ak)$ From this we get total complexity of [SaIL]{.smallcaps} to be $O\left(kA^{2}\right)$.

## Dijkstra's test time complexity: {#dijkstras-test-time-complexity .unnumbered}

Assume Dijkstra's algorithm does $B$ expansions before finding a path. As mentioned earlier, we assume that priority-queue reordering can be achieved in constant time. Total $\mathtt{Select}$ complexity: $O(1)$ Total expansion complexity: $O\left(kB\right)$ From this we obtain total complexity for Dijkstra's algorithm to be $O\left(kB\right)$.

From the above analysis, for [SaIL]{.smallcaps} to have lesser overall computational complexity than uninformed search we require the following condition to be satisfied: $$\begin{equation}
	A^{2} < B
\end{equation}$$ Thus, [SaIL]{.smallcaps} must obtain a squared reduction in total number of expansions for it to be computationally better than uninformed search. We argue that this strengthens the case for using [SaIL]{.smallcaps} in higher dimensional search graphs as in uninformed search expands a very large number of nodes as the total number of graph nodes increases.
::::::::::::::::::::
