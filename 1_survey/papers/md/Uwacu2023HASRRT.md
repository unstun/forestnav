---
citation_key: Uwacu2023HASRRT
arxiv_id: 2309.10801
arxiv_url: https://arxiv.org/abs/2309.10801
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:06:04Z
origin: ai+web
reviewed: false
---

Uwacu *et al.*: HAS-RRT: RRT-based Motion Planning using Topological Guidance

# Introduction {#sec:introduction}

Motion planning algorithms have applications in many fields, from robotics [@englot2012AAAI] to microbiology [@baghvsl-urfpdl]. Exact motion planning is PSPACE-hard and intractable, as deterministic algorithms are exponential in the number of degrees of freedom of the robot  [@r-cpmpg-79]. We can use sampling-based planners to approximate the robot's high dimensional planning space (the configuration space, or $\mathcal{C}$) [@lk-rrtpp-00; @kslo-prpp-96].

:::: {#fig:roadmaps .figure latex-placement="t"}
![Basic RRT [@lk-rrtpp-00]](Figures/tree_rrt.png){#fig:tree-rrt width="100%"}

![DR-RRT [@dsba-drbrrt-16]](Figures/tree_drrrt.png){#fig:tree-drrrt width="100%"}

![EET [@Rickert_balancingexploration]](Figures/tree_eet.png){#fig:tree-eet width="100%"}

![HAS-RRT](Uwacu2023HASRRT_figs/tree_hasrrt.png){#fig:tree-hasrrt width="100%"}

::: caption
Trees from RRT variants in a narrow passage problem. HAS-RRT  shows a better balance of exploring the open space and narrow passage.
:::
::::

Narrow passages in $\mathcal{C}$ are a challenge for sampling-based algorithms. The probability of randomly discovering those narrow passages is very low, hence the necessity to find ways to provide guidance to the planning process. Initial methods including OBPRM [@abdjv-obprm-98], OBRRT [@rtla-obrrt-06], and MAPRM [@was-maprm-99] attempt to address the narrow passage problem by biasing the sampling process using an approximation of the obstacle space (the portion of $\mathcal{C}$ occupied by obstacles) as guidance. However, these methods can be slow in dense or cluttered environments because they require lots of calls to a collision checker. We can identify narrow passages with the help of information about the connectivity of the workspace. Such information can be encoded in a graph called a workspace skeleton and used to guide the exploration of the configuration space. The Dynamic Region-biased RRT [@dsba-drbrrt-16] algorithm is a skeleton-based sampling strategy that showed that the workspace skeleton can be a reliable guide. However, it does not take full advantage of the guidance that a workspace skeleton can provide. DR-RRT takes small steps along the workspace skeleton, which can be slow and unnecessary (see Figure [10](#fig:dynamicregion:example){reference-type="ref" reference="fig:dynamicregion:example"}) .

This work presents the Hierarchical Annotated Skeleton RRT (HAS-RRT) method to quickly find workspace-guided paths in a single-query environment. Similar to [@dsba-drbrrt-16], HAS-RRT  uses the workspace skeleton to search for paths. However, HAS-RRT  initially relies on the connectivity of the workspace to make large steps in its exploration and only retracts to focused local exploration when necessary. This approach makes HAS-RRT more robust to poor-quality skeletons than previous methods. such as environment clearance or priority through certain passages , the strategy can be adapted to fit different motion planning applications. When the workspace skeleton contains workspace paths that can be extended to $\mathcal{C}$ paths, HAS-RRT exploits the guidance fully, and when the skeleton is not perfectly indicative of the motion planning solution, the method can use directional hints from such a skeleton and find a solution with additional exploration more gracefully than the other methods. This work most applies to robots whose workspace and configuration space are closely related, such as mobile robots.

Our results show how the HAS-RRT method achieves improved run time, efficiency, and scalability compared to the basic RRT strategy [@lk-rrtpp-00], the Exploration-Exploitation tree (EET) strategy [@Rickert_balancingexploration], and the Dynamic Region RRT (DR-RRT) strategy [@dsba-drbrrt-16]. Our runtime improves by at least 59% and as much as 91% on average compared to DR-RRT in each of our test environments. In addition, as shown in Figure [5](#fig:roadmaps){reference-type="ref" reference="fig:roadmaps"}, HAS-RRT yields a sparser tree with exploration focused on critical regions of $\mathcal{C}$ compared to those strategies.

Specifically, our contributions include:

- A novel workspace guidance algorithm, Hierarchical Annotated-Skeleton Guided RRT, which can rapidly discover paths indicated by a workspace skeleton.

- An empirical validation that demonstrates HAS-RRT's reliable efficiency in run time and path quality across various environments and highlights it as the best strategy for workspace-guided planning.

- A study that shows how HAS-RRT reacts to varying levels of guidance and shows that with extremely poor guidance, HAS-RRT's behavior is similar to that of RRT. Previous work using workspace skeletons does not include an analysis of performance under varying qualities of guidance.

# Preliminaries and Previous Work {#sec:prev-work}

Section [2.1](#sec:mp-prelims){reference-type="ref" reference="sec:mp-prelims"} provides an overview of the motion planning problem and some basic algorithms used to solve it. Section [2.2](#sec:bkgd-workspace){reference-type="ref" reference="sec:bkgd-workspace"} covers different types of workspace guidance, including the workspace skeleton, and relevant previous methods which use workspace guidance.

:::: {#fig:dynamicregion:example .figure}
![](Uwacu2023HASRRT_figs/DynamicRegionRRTExample-3.png){#fig:dbrrt-step1 width="100%"}

![](Uwacu2023HASRRT_figs/DynamicRegionRRTExample-4.png){#fig:dbrrt-step2 width="100%"}

![](Uwacu2023HASRRT_figs/DynamicRegionRRTExample-5.png){#fig:dbrrt-step3 width="100%"}

![](Uwacu2023HASRRT_figs/DynamicRegionRRTExample-6.png){#fig:dbrrt-step4 width="100%"}

::: caption
Example execution of Dynamic Region-biased RRT: (a) Query Skeleton (magenta) computed from a query $\{q_s, q_g\}$; (b) initial region (green) placed at the source vertex of the Query Skeleton; (c) region-biased RRT growth (blue); and (d) multiple active regions (green) guiding the tree (blue) among multiple embedded arcs of the Query Skeleton (magenta) is shown.
:::
::::

## Motion Planning Preliminaries and Sampling-based Planning {#sec:mp-prelims}

A robot's pose is described by its configuration, and the set of all possible configurations within an environment is called the *configuration space*, or $\mathcal{C}$. The dimension of $\mathcal{C}$ is the same as the number of degrees of freedom of the robot. $\mathcal{C}$ is partitioned into $\mathcal{C}_{free}$ (the set of valid configurations, or the free space) and $\mathcal{C}_{obst}$ (the set of invalid configurations, or the obstacle space).

Given a start configuration $q_{start}$ and a goal configuration $q_{goal}$, the goal of a motion planning problem is to find a path from $q_{start}$ to $q_{goal}$ which lies entirely in $\mathcal{C}_{free}$. In other words, the goal is to find a path $p:[0, 1]\rightarrow \mathcal{C}$, where $p(0) = q_{start}$ and $p(1) = q_{goal}$. This is called a *query*.

Sampling-based planning algorithms approximate $\mathcal{C}$, since it is difficult to calculate exactly. These methods randomly generate configurations in $\mathcal{C}$ and connect them to build a representational graph. Examples of such methods include probabilistic roadmaps (PRM) [@kslo-prpp-96] , which constructs a graph, and rapidly exploring random trees (RRT) [@lk-rrtpp-00], which constructs a tree. Graph-based methods can be reused for multiple queries, while tree-based methods must be used for one query at a time. In this work, we focus on RRT and some of its variations to study problems related to accessibility.

RRT algorithms are generally used to solve single-query motion planning problems. The tree starts at the start configuration, $q_{start}$. In each algorithm iteration, a random direction, $q_{rand}$, is sampled, and its nearest neighbor $q_{near}$ in the tree is identified. An extension from $q_{near}$ to $q_{rand}$ is attempted to expand the tree. After enough iterations, the tree reaches the goal, and the query is solved.

Since the direction to expand the tree is randomly selected, the basic RRT algorithm is probabilistically complete. This means that that if a solution exists, the probability of finding it increases as more time and resources are spent growing the tree [@lk-rrtpp-00]. This, however, also implies that the algorithm struggles in more constrained environments. For example, if an environment has many dead ends, the basic RRT algorithm may waste time exploring unnecessary directions.

## Workspace-Guided Planning {#sec:bkgd-workspace}

Information about the workspace can be used to bias sampling towards $\mathcal{C}_{free}$ for more optimal paths or faster search time. Many methods use the workspace to guide planning, and here we describe a few.

Some methods perform a preliminary search of the workspace before sampling. The Exploration-Exploitation Trees (EET) algorithm [@Rickert_balancingexploration] first explores the workspace by randomly growing a tree of spheres from the start position to the goal. This is called the 'Wavefront' expansion tree, and with it, EET grows an RRT in $\mathcal{C}$, exploiting the pre-explored sphere regions. If exploitation fails in difficult regions, the planner gradually shifts its behavior to exploration with regular sampling-based planning. The wavefront exploration process is highly sensitive to the positioning of the start and goal configurations and the variability of region sizes in the environment. In addition, the information about the workspace is acquired by using clearance-based spheres that are randomly expanded to cover the free workspace. In environments with narrow passages, this process often takes too long.

Workspace Decomposition Strategies [@kh-wisprp-04; @bo-uwignsprp-04; @kh-wco-06] steer sampling in the free workspace. For example, SyCLoP [@pkv-mpdsclp-10] uses an RRT to sample frontier decomposition regions. The decomposition of the workspace is limited as a guide, however, because it does not contain information about the topology of the workspace.

Some methods attempt to use the medial axis, the set of all points equidistant to at least 2 obstacles, to help guide sampling. MAPRM and aMAPRM [@hk-fuwmapp-00; @yb-asdppbama-04] generate all their PRM samples along the medial axis. MARRT [@dgta-marrt-14] attempts to do the same, but with an RRT tree expansion.

A workspace skeleton has been shown to provide better guidance for sampling. A workspace skeleton is a graph that denotes the connectivity of the workspace [@blk-tcsrp-2012]. The vertices of the skeleton denote regions in the workspace, and the edges denote connectivity between them. A skeleton can be computed geometrically or provided by a user. Examples of workspace skeletons can be found in Figure [25](#fig:envs){reference-type="ref" reference="fig:envs"}

Workspace skeletons are more effective when $\mathcal{C}$ is a subset of the workspace. When sampling along a workspace skeleton, a sample directly corresponds to a point in $\mathcal{C}$. When $\mathcal{C}$ does not correspond to the workspace (e.g. manipulator robots, where $\mathcal{C}$ has much different topology from the workspace), it can be difficult to find a transformation from a sample taken in the workspace to a point in the free configuration space. EET [@Rickert_balancingexploration] addresses this by corresponding a point in the the workspace to the location of the end effector, however, this approach does not guarantee finding a path if one exists.

A precursor of the work presented in this paper is the Dynamic Region-biased RRT[@dsba-drbrrt-16], detailed in Figure [10](#fig:dynamicregion:example){reference-type="ref" reference="fig:dynamicregion:example"}. The workspace has obstacles and a Reeb graph [@dn-eacrg-09] skeleton. To speed up the process, the workspace skeleton has been pruned and directed to only have parts connecting the current start to the current goal. A sampling region is instantiated close to $q_{start}$ and expanded along the nearest skeleton edge until it reaches the next skeleton vertex and splits into several regions, one for each adjacent edge. The process ends when one of the regions is close enough to the goal to solve the query.

Dynamic Region-biased RRT  is efficient because the tree is guided through the connected free space, simplifying the narrow passage problem and preventing the tree from being stagnant. However, Dynamic Region-biased RRT  does unnecessary exploration by expanding the dynamic region in small steps along the skeleton edge.

Other similar methods which use a workspace skeleton include Dynamic Region Sampling with PRM[@suda-tgrcdrs-20] and Hierarchical Annotated-Skeleton guided PRM[@uyma-hpasg-22], both of which use the workspace skeleton as guidance for building and querying a probabilistic roadmap. While RRT-based methods such as Dynamic Region-biased RRT prune and direct the portions of the workspace skeleton related to a query, these PRM-based methods use the whole skeleton to build a roadmap.

Mathematically, we define the workspace skeleton as a graph $G_s = (V_s, E_s)$ that lies in the 2D or 3D workspace $\mathbb{R}^2$ or $\mathbb{R}^3$. Each edge $e$ has a set of intermediates $e_i$, which are points along the edge. The workspace skeleton is a representation of the obstacle-free workspace. However, because we often calculate the skeleton with computational geometry methods that create approximations, there are no guarantees that the skeleton lies fully in the obstacle-free workspace.

# Hierarchical Annotated Skeleton RRT {#sec:method}

In Section [3.1](#sec:hasrrt){reference-type="ref" reference="sec:hasrrt"} we describe the Hierarchical Annotated-Skeleton Guided RRT method and how it works. In Section [3.2](#sec:adaptingskeletonquality){reference-type="ref" reference="sec:adaptingskeletonquality"} we discuss the parts of the HAS-RRT algorithm that allow it to adapt to the quality of the workspace skeleton.

:::: {#fig:HASRRT .figure latex-placement="h!"}
![](Uwacu2023HASRRT_figs/fig3a.png){#fig:meth1-step1 width="100%"}

![](Uwacu2023HASRRT_figs/fig3b.png){#fig:meth1-step2 width="100%"}

![](Uwacu2023HASRRT_figs/fig3c.png){#fig:meth1-step3 width="100%"}

![](Uwacu2023HASRRT_figs/fig3d.png){#fig:meth1-step4 width="100%"}

![](Uwacu2023HASRRT_figs/fig3e.png){#fig:meth1-step5 width="100%"}

![](Uwacu2023HASRRT_figs/fig3f.png){#fig:meth1-step6 width="100%"}

![](Uwacu2023HASRRT_figs/fig3g.png){#fig:meth1-step7 width="100%"}

![](Uwacu2023HASRRT_figs/fig3h.png){#fig:meth1-step8 width="100%"}

::: caption
Example execution of the Hierarchical skeleton-guided RRT: (a) Query Skeleton (purple) computed from a query $q_s$, $q_g$; (b) initial region (green) placed at the source vertex of the Query Skeleton; (c) a full extension to the end of the skeleton edge; (d) region splits into two regions at the adjacent edges; (e) an invalid extension is attempted; (f) after a failed extension, a local expansion is attempted; (g) the weight of the failed region is adjusted to bias the tree to alternative path options; (h) the tree after a few iterations.
:::
::::

## The Algorithm {#sec:hasrrt}

The Hierarchical Annotated-Skeleton Guided RRT (HAS-RRT) algorithm (Figure [19](#fig:HASRRT){reference-type="ref" reference="fig:HASRRT"} and Algorithm [\[alg:fullalg\]](#alg:fullalg){reference-type="ref" reference="alg:fullalg"}) improves upon the previous approach of DR-RRT by combining exploitation of the skeleton's guidance with local exploration to better adapt to the nature of the surrounding environment. Using the connectivity mapped by the workplace skeleton, HAS-RRT aims to use longer edge extensions and smaller local extensions when the environment is has more obstacles or the skeleton is less reliable. This allows the algorithm to prioritize paths directly denoted by the skeleton and add exploration only as necessary.

The inputs to the algorithm are the 3D workspace, the start configuration $q_{start}$, the goal configuration $q_{goal}$, and a workspace skeleton $G_s$.

:::: algorithm
::: algorithmic
Environment $env$, Start $s$, Goal $g$, Annotated Skeleton $aws$ []{#alg:directskeleton label="alg:directskeleton"} []{#alg:inittree label="alg:inittree"} []{#alg:initregion label="alg:initregion"} []{#alg:selectregion label="alg:selectregion"} []{#alg:sample label="alg:sample"} []{#alg:attemptextension label="alg:attemptextension"} []{#alg:advanceregion label="alg:advanceregion"} []{#alg:incrementsuccess label="alg:incrementsuccess"} []{#alg:extensionfailed label="alg:extensionfailed"} []{#alg:retractregion label="alg:retractregion"} []{#alg:updateweight label="alg:updateweight"}
:::
::::

First, the skeleton is directed and pruned to show only the workspace paths relevant to the given query. This process is the same as that of [@dsba-drbrrt-16]. The directed skeleton encodes information about the exploration direction should be prioritized as shown in Figure [11](#fig:meth1-step1){reference-type="ref" reference="fig:meth1-step1"}. Since the edges that are deleted during the pruning process do not connect those positions in workspace, they could not connect them in the configuration space either [@suda-tgrcdrs-20]. Thus, this step effectively reduces the amount of exploration done by the planner without the possibility of accidentally removing valid solutions.

*Initializing the tree* (Lines [\[alg:inittree\]](#alg:inittree){reference-type="ref" reference="alg:inittree"} and [\[alg:initregion\]](#alg:initregion){reference-type="ref" reference="alg:initregion"} in Algorithm [\[alg:fullalg\]](#alg:fullalg){reference-type="ref" reference="alg:fullalg"}): We define a sampling region as a sphere in the $\mathcal{C}$ of radius $r$ (determined through user-selected hyperparameters), anchored to an intermediate $e_i$. An active sampling region $s$ is initialized at the skeleton vertex nearest to $q_{start}$ in the workspace. The tree is initialized with the start configuration $q_{start}$ and grown until it reaches the first sampling region. Figure [12](#fig:meth1-step2){reference-type="ref" reference="fig:meth1-step2"} illustrates the initial region with a tree of size 3.

*Expanding the tree* (Lines [\[alg:selectregion\]](#alg:selectregion){reference-type="ref" reference="alg:selectregion"} to [\[alg:updateweight\]](#alg:updateweight){reference-type="ref" reference="alg:updateweight"} in Algorithm [\[alg:fullalg\]](#alg:fullalg){reference-type="ref" reference="alg:fullalg"}): These steps constitute the main loop that terminates when the query is solved or the algorithm runs out of resources. First, an active region is selected (see Section [3.2](#sec:adaptingskeletonquality){reference-type="ref" reference="sec:adaptingskeletonquality"} for region selection details), and the planner samples inside for a direction to expand the tree toward. Once a valid $q_{rand}$ is sampled, an extension attempt is performed to expand the tree (Line [\[alg:attemptextension\]](#alg:attemptextension){reference-type="ref" reference="alg:attemptextension"} of Algorithm [\[alg:fullalg\]](#alg:fullalg){reference-type="ref" reference="alg:fullalg"}). The successful extension adds a new vertex to the tree and pushes the region that gave $q_{rand}$ to the end of its current skeleton edge. The region's weight is also updated by incrementing its success record to increase its chances of being selected in the next iterations. Then, new regions are created at the start of all outgoing new skeleton edges. A successful direct extension to the end of a skeleton edge and its branching into two regions for each adjacent edge are shown in Figures [13](#fig:meth1-step3){reference-type="ref" reference="fig:meth1-step3"} and [14](#fig:meth1-step4){reference-type="ref" reference="fig:meth1-step4"}.

*Retracting a sampling region* (Lines [\[alg:extensionfailed\]](#alg:extensionfailed){reference-type="ref" reference="alg:extensionfailed"}-[\[alg:retractregion\]](#alg:retractregion){reference-type="ref" reference="alg:retractregion"} in Algorithm [\[alg:fullalg\]](#alg:fullalg){reference-type="ref" reference="alg:fullalg"}): If the extension does not reach the region where $q_{rand}$ was sampled, as shown in Figure [15](#fig:meth1-step5){reference-type="ref" reference="fig:meth1-step5"}, the region is pulled back toward $q_{near}$. The current implementation pulls the region halfway between $q_{rand}$ and $q_{near}$ as shown in Algorithm [\[alg:retract-region\]](#alg:retract-region){reference-type="ref" reference="alg:retract-region"} and Figure [16](#fig:meth1-step6){reference-type="ref" reference="fig:meth1-step6"}. In addition, the region's weight is updated by incrementing its failure record to decrease its chances of being selected in the next iterations, as shown in Figure [17](#fig:meth1-step7){reference-type="ref" reference="fig:meth1-step7"}.

:::: algorithm
::: algorithmic
Region $r$, Current annotated skeleton $ask$, $q_{near}$, $q_{new}$
:::
::::

*Region Selection.* The planner chooses the next region using a probability distribution based on prior extension success, the directed skeleton, and the explore/exploit bias.

A candidate region $r$ is selected with probability $p_r$ calculated as follows, where $e$ is the explore bias hyperparameter and $R$ is the set of all regions: $$p_r = \frac{e}{|R|+1} + (1-e)\frac{w_r}{\sum_{r'\in R}w_{r'}}$$

A region's weight $w_r$ is the percentage of successful extensions within that region. To maintain probabilistic completeness, the whole environment also constitutes one region in case the workspace skeleton does not cover parts of the environment that comprise the motion planning solution. The environment is chosen with probability $\frac{e}{|R|+1}$. When the whole environment is selected a sample is chosen randomly within the environment, and the planner behaves like a regular RRT.

## Adapting to Skeleton Quality - Method {#sec:adaptingskeletonquality}

Strategies guided by the workspace skeleton are affected by the quality of the skeleton. In DR-RRT  when a skeleton edge does not provide reliable guidance, the sampling region on the edge leads to repeated sampling failure, which lowers its weight and eventually pushes the algorithm to follow other directions if available or degrade to random sampling of the whole environment. With HAS-RRT  the effects of poor guidance are mitigated by three things. First, the skeleton annotations help prioritize edges that lead to the desired solution, making it less likely to encounter bad guidance. Second, when a direct extension along the skeleton edge fails, the algorithm's retraction mechanism keeps the exploration of an alternative focused on adjusting the extension at the point of failure instead of directly reverting to random sampling. Third, if the guidance provided by the skeleton is so poor that the algorithm experiences increasingly more failures than successes by using the skeleton, the target selection behavior reverts back to that of RRT, allowing for randomized exploration of the environment.

Prior extension success denotes extending to a sample within a region $r$. If the skeleton is reliable, then $r$ on a skeleton vertex $v$ is centered properly in $\mathcal{C}_{free}$. Thus, the algorithm is more likely to have repeated success extending into $r$ again. The directed skeleton ensures that the algorithm continues progressing toward its goal. If a particular skeleton vertex is not accurately placed in the free workspace, the samples in the corresponding $\mathcal{C}$ may not be valid as often. Thus, the success rate in $r$ goes down, making the region less desirable to expand into. Future region selections will prioritize other regions with higher success rates over $r$.

# Validation {#sec:validation}

:::: {#fig:envs .figure latex-placement="t"}
![2D narrow passage and Medial Axis skeleton. We use a small 3-DOF rectangular prism robot. The robot at its widest is 60% of narrow passage's width. ](Uwacu2023HASRRT_figs/simple_passage.png){#fig:envs-simplepassage width="100%"}

![Grid tunnels and skeleton constructed with method from Section [4.2](#sec:skeleton-construction){reference-type="ref" reference="sec:skeleton-construction"}. We use a small 6-DOF L-shaped robot. The L shape is approximately 8% of a block's width.](Figures/grid_env.png){#fig:envs-gridtunnels width="100%"}

![Extended Z-shaped tunnels and a curated mean curvature skeleton. We use a cube-shaped robot that cannot rotate (3-DOF). The robot's width is approximately 10% of the tunnel's width.](Uwacu2023HASRRT_figs/z_tunnel.png){#fig:envs-extendedz width="100%"}

![Grid Mining, with shafts (grey) and drifts (green), and skeleton constructed with method from Section [4.2](#sec:skeleton-construction){reference-type="ref" reference="sec:skeleton-construction"}. We use a small 6-DOF L-shaped robot. The L shape is approximately 8% of one block's width.](Figures/gridmine_env.png){#fig:envs-gridmine width="100%"}

![8x8 3D grid maze and curated mean curvature skeleton. We use a stick shaped robot that can rotate around any axis 6-DOF. The length and depth of the stick are approximately 2% and 9% of the environment's length, respectively.](Uwacu2023HASRRT_figs/gridmaze.png){#fig:envs-gridmaze width="100%"}

::: caption
Tested environments. Workspace skeletons are shown in green.
:::
::::

[]{#sec:setup label="sec:setup"} We compare HAS-RRT with three other methods: Basic RRT[@lk-rrtpp-00], EET[@Rickert_balancingexploration], and DR-RRT[@dsba-drbrrt-16]. DR-RRT and EET use workspace guidance to help with sampling. These methods were chosen due to their ability to grow an RRT with additional environmental guidance. We compare with RRT because it is a baseline method.

The results below show the robustness of HAS-RRT to all environments. In each environment, one of the other planning strategies' performance is comparable to that of HAS-RRT  but only HAS-RRT consistently yields good solutions in less time than the others. In addition, HAS-RRT is independent of parameter tuning, an added value that makes it a good choice for a non-expert user.

We evaluate the method in five maze/tunnel environments shown and described in Figure [25](#fig:envs){reference-type="ref" reference="fig:envs"}. In Section [4.1](#sec:experimental-setup){reference-type="ref" reference="sec:experimental-setup"} and [4.2](#sec:skeleton-construction){reference-type="ref" reference="sec:skeleton-construction"} we describe our experimental setup and our novel modular way to construct a workspace skeleton for two of our environments. In Section [4.3](#sec:discussion){reference-type="ref" reference="sec:discussion"} we discuss the results of our experiments. Finally, in Section [4.4](#sec:ablation-study){reference-type="ref" reference="sec:ablation-study"} we analyze the performance of HAS-RRT with varying qualities of guidance to demonstrate how HAS-RRT behaves with poor guidance.

## Experimental Setup {#sec:experimental-setup}

In each environment, a query was set to evaluate the ability of the RRT  variant to solve an accessibility problem in that environment. We pre-computed different types of skeletons and annotated them with clearance for all the problems. The results do not report the time to compute a workspace skeleton since they are incurred only once. However, the time to prune and direct the skeleton is reported in the run time. Each algorithm was given the same amount of time to solve the queries, ranging from 20 seconds to 300, depending on the problem's difficulty. We report the time to solve the query and path cost. For robotics environments, we use path length as a proxy for path cost. For all planners and in all environments, we use Euclidean distance as a distance metric, and our local planner always moves in a straight line towards its goal.

The experiments were executed on a Google Cloud Compute e2-standard-4 computer with 4vCPUs and 16GB of RAM, running Ubuntu 20.04. All methods were implemented in our C++ Parasol Planning Library (PPL) [@PPL]. Validation was done with PQP-SOLID collision detection [@lglm-pqp-99]. Hyperparameters were chosen through experimentation.

## Skeleton Construction and Annotation {#sec:skeleton-construction}

:::: {#fig:blocks .figure latex-placement="h!"}
![Two separate blocks, blue with two entryways and pink with three entryways. Two separate skeletons. ](Uwacu2023HASRRT_figs/blocks_individual.png){#fig:blocks_separate width="65%"}

![Blue (solid) and pink (outlined) blocks, combined, with pruned skeleton. ](Uwacu2023HASRRT_figs/blocks_combined.png){#fig:blocks_combined width="40%"}

::: caption
Block environment and skeleton construction.
:::
::::

The workspace skeleton is constructed differently depending on the environment. For example, a medial-axis skeleton can easily be constructed for a 2-dimensional environment like the 2D narrow passage in Figure [20](#fig:envs-simplepassage){reference-type="ref" reference="fig:envs-simplepassage"}. In 3D cases like the extended Z tunnel and the grid maze, structures like the mean curvature skeleton [@blk-tcsrp-2012] can be used to show the connectivity of the workspace. In such environments, however, the default graph may contain long curved edges that do not indicate the changes in the topology of the workspace. For example, a tunnel with a $90^{\circ}$ turn may be represented by a long curved edge with no indication of the change in direction.

In some cases, instead of constructing an environment and computing a skeleton afterward, we simultaneously build an environment and skeleton. For simplicity, we create an environment with $90^{\circ}$ angles using cubic structures as building blocks. Considering orientation, there are $2^6$ ways to construct a cube with varying tunnels leading outwards. After designing the blocks, a skeleton is constructed for each block based on the tunnel openings, as shown in Figure [26](#fig:blocks_separate){reference-type="ref" reference="fig:blocks_separate"}. When blocks are paired, their respective skeletons are joined to make a connected graph representing the new topology (Figure [27](#fig:blocks_combined){reference-type="ref" reference="fig:blocks_combined"}).

## Discussion {#sec:discussion}

:::: table*
::: adjustbox
width=

+-------------------+-----+------------------------------------+------------------------------------------+---------------------------------------+
| Environment       |     | Number of vertices                 | Collision Detection Calls                | Completed seeds ($\%$)                |
+:==================+:====+=======:+=======:+=======:+========:+========:+=========:+========:+==========:+========:+========:+========:+========:+
| 3-14              |     | RRT    | EET    | DR-RRT | HAS-RRT | RRT     | EET      | DR-RRT  | HAS-RRT   | RRT     | EET     | DR-RRT  | HAS-RRT |
+-------------------+-----+--------+--------+--------+---------+---------+----------+---------+-----------+---------+---------+---------+---------+
| Simple Passage    | avg | 462    | 660    | 59     | **20**  | 6138    | 6020     | 725     | **393**   | 100%    | 63%     | 100%    | 100%    |
|                   +-----+--------+--------+--------+---------+---------+----------+---------+-----------+         |         |         |         |
|                   | std | 425    | 833    | 14     | 4       | 4418    | 6506     | 142     | 56        |         |         |         |         |
+-------------------+-----+--------+--------+--------+---------+---------+----------+---------+-----------+---------+---------+---------+---------+
| Grid Tunnels      | avg | 86     | **16** | 438    | 19      | 5383    | **1359** | 8000    | 1496      | 100%    | 97%     | 100%    | 100%    |
|                   +-----+--------+--------+--------+---------+---------+----------+---------+-----------+         |         |         |         |
|                   | std | 61     | 3      | 78     | 2       | 2866    | 353      | 1103    | 305       |         |         |         |         |
+-------------------+-----+--------+--------+--------+---------+---------+----------+---------+-----------+---------+---------+---------+---------+
| Extended Z Tunnel | avg | 592    | **51** | 498    | 55      | 15922   | 3922     | 7288    | **1977**  | 100%    | 94%     | 100%    | 100%    |
|                   +-----+--------+--------+--------+---------+---------+----------+---------+-----------+         |         |         |         |
|                   | std | 199    | 13     | 60     | 7       | 4163    | 559      | 686     | 136       |         |         |         |         |
+-------------------+-----+--------+--------+--------+---------+---------+----------+---------+-----------+---------+---------+---------+---------+
| Grid Mining       | avg | 634    | **78** | 1701   | 130     | 52102   | 8682     | 29114   | **5750**  | 31%     | 80%     | 100%    | 100%    |
|                   +-----+--------+--------+--------+---------+---------+----------+---------+-----------+         |         |         |         |
|                   | std | 136    | 40     | 113    | 2       | 9345    | 1519     | 1488    | 155       |         |         |         |         |
+-------------------+-----+--------+--------+--------+---------+---------+----------+---------+-----------+---------+---------+---------+---------+
| Grid Maze         | avg | NaN    | NaN    | 3570   | **892** | NaN     | NaN      | 69675   | **26124** | NaN     | NaN     | 97%     | 100%    |
|                   +-----+--------+--------+--------+---------+---------+----------+---------+-----------+         |         |         |         |
|                   | std | NaN    | NaN    | 183    | 197     | NaN     | NaN      | 3565    | 4979      |         |         |         |         |
+-------------------+-----+--------+--------+--------+---------+---------+----------+---------+-----------+---------+---------+---------+---------+
:::
::::

:::: {#fig:results .figure latex-placement="h!"}
![Run time in seconds, for all seeds. ](Uwacu2023HASRRT_figs/2024_12_runtime.png){#fig:results-runtime width="100%"}

![Path cost (path edge weights) for only seeds that found a path.](Uwacu2023HASRRT_figs/2024_12_PC.png){#fig:results-pathcost width="100%"}

::: caption
Run time and path cost comparisons for the tested robotics environments.'x' marks represent seeds that failed to find a solution.
:::
::::

The experimental results in Figure [31](#fig:results){reference-type="ref" reference="fig:results"} and Table [\[tab:results\]](#tab:results){reference-type="ref" reference="tab:results"} show the importance of using a workspace skeleton to guide planning and the significant advantage of using hierarchical planning with guidance. The comparative results show that DR-RRT takes longer than HAS-RRT and is not consistently faster than basic RRT or EET. In addition, although EET returns paths with the lowest cost, its success rate is worse than others in most environments, and it is sensitive to parameter tuning.

In the Simple Passage, Extended Z Tunnel, and Grid Mining environments, HAS-RRT outperformed the other guided strategies because of the long extensions it takes through the narrow passage using skeleton guidance. DR-RRT locally explores each edge, increasing its sampling failures in the narrow passage. EET takes longer for the wavefront expansion to discover and explore the narrow passage randomly, but the resulting guidance yields a better path cost. These examples highlight one of the main strengths of HAS-RRT: prioritizing paths indicated by the workspace guidance and only sampling if a naive extension fails. By following the guidance of a good skeleton, the runtime of HAS-RRT is greatly minimized while maintaining a competitive path cost.

In the grid tunnel environment, HAS-RRT runs faster than DR-RRT and EET. EET performs faster than DR-RRT because the wavefront expansion is easier to build in this environment.

The grid mine environment shows the scalability of HAS-RRT. In this more complex environment, Basic RRT only solved 31% of the 35 random seeds. HAS-RRT even performs better than DR-RRT, because it simply follows the guidance from the long skeleton edges rather than fully exploring each edge.

The grid maze environment is notoriously difficult and was only successfully solved by DR-RRT and HAS-RRT (of the 35 seeds). This environment has curved edges (as shown in Figure [24](#fig:envs-gridmaze){reference-type="ref" reference="fig:envs-gridmaze"}), even though the environment's tunnels are straight. From this, we can see two more strengths of HAS-RRT: While HAS-RRT works best with straight-edged workspace skeletons, it performs well on other types of skeletons due to the method's exploration when necessary. Additionally, as evidenced by HAS-RRT's lower path cost and faster runtime compared to DR-RRT, HAS-RRT still uses more information from the skeleton than its competitors.

EET's path costs are comparable and competitive to HAS-RRT because the Wavefront expansion guarantees any path to be centered in an environment. However, EET's runtime is much higher than the other methods because the wavefront expansion is built probabilistically and thus must be recomputed for each seed. Additional investigation shows that building the wavefront expansion takes up most of the runtime: build times for the Generated Grid environment averaged 66.49% of the total runtime and for the Extended Z Tunnel averaged 85.75%. The other two environments averaged similarly.

## Adapting to Skeleton Quality - Study {#sec:ablation-study}

We also investigate HAS-RRT's capability to consistently find optimal paths with an unreliable skeleton. We ran HAS-RRT on the Grid Tunnels environment with increasingly unreliable skeletons and compare runtime and path cost. Since the skeleton generated using the process from Section [4.2](#sec:skeleton-construction){reference-type="ref" reference="sec:skeleton-construction"} is medially centered in the Grid Tunnels, it can be easily modified and its reliability can be easily quantified.

We used the same query used in the experiments from Section [4](#sec:validation){reference-type="ref" reference="sec:validation"}. Each vertex of the skeleton not corresponding to the query start and goal positions are shifted by a distance $d$ in a random direction and are guaranteed to be within the free workspace (see Figure [35](#fig:perturbed_skeleton_comparison){reference-type="ref" reference="fig:perturbed_skeleton_comparison"}). We increase the maximum radius of a sampling region from the previous set of experiments to accommodate the poorer-quality skeletons. Each experiment is run with 10 seeds.

The results for these experiments are shown in Figure [32](#fig:perturbed_results){reference-type="ref" reference="fig:perturbed_results"}. The HAS-RRT results are shown in increasing order of $d$ from the second to tenth columns. Smaller values of $d$ have results that match those in Section [4.3](#sec:discussion){reference-type="ref" reference="sec:discussion"}, where HAS-RRT's performance is faster than both DR-RRT and RRT. As $d$ increases, the quality of the skeleton worsens, and the algorithm must adapt accordingly. Its behavior begins to change into that of DR-RRT and RRT, depending on the sampling success rate for each individual seed. At $d=5$ and $d=6$, HAS-RRT's chosen sampling distribution is the whole environment on average $51.6\%$ and $93.7\%$ percent of the time, respectively. This shows that even in extreme cases, HAS-RRT behaves approximately the same way RRT would.

For three seeds in the $d=5$ experiment, the runtime is much higher than the remainder of the experiments. This is because while HAS-RRT readily assumes that skeleton edges can be unreliable, it is more sensitive to skeleton vertices being unreliable. For these three seeds, HAS-RRT had difficulty finding a valid configuration at a region constructed at one of the skeleton's vertices.

:::: {#fig:perturbed_results .figure latex-placement="t"}
![](Uwacu2023HASRRT_figs/ab_result.png){width="100%"}

::: caption
Runtimes for DR-RRT, HAS-RRT for ten different perturbed skeletons, and RRT. Only runtimes for seeds which found paths are shown.
:::
::::

:::: {#fig:perturbed_skeleton_comparison .figure latex-placement="t"}
![$d=0$](Uwacu2023HASRRT_figs/o_0.0.jpg){#fig:skeleton_0 width="\\textwidth"}

![$d=3.5$](Uwacu2023HASRRT_figs/o_3.5.jpg){#fig:skeleton_35 width="\\textwidth"}

::: caption
Perturbed skeletons. Valid regions for the grid environment are shown in grey, and the skeleton is shown in black.
:::
::::

# Conclusion {#sec:conclusion}

In this work we introduce Hierarchical Annotated-Skeleton Guided RRT (HAS-RRT), which leverages guidance from a workspace skeleton to efficiently guide the RRT's expansion process. By strategically prioritizing paths available within the workspace, HAS-RRT can find comparable-cost paths faster than similar methods. We also perform an in-depth analysis on the performance of HAS-RRT with varying qualities of guidance, showing that the method is robust to and can perform efficiently with both minor and major inaccuracies with the provided guidance. Our experimental findings underscore the value of incorporating workspace information into motion planning problems where relevant.

[^1]: Manuscript received: September 15, 2024; Revised December 25, 2024; Accepted March 25, 2025.

[^2]: This paper was recommended for publication by Editor Aniket Bera upon evaluation of the Associate Editor and Reviewers' comments. This work was supported in part by the U.S. National Science Foundation's "Expeditions: Mind in Vitro: Computing with Living Neurons\" under award No. IIS-2123781, and by the IBM-Illinois Discovery Accelerator Institute and the Center for Networked Intelligent Components and Environments (C-NICE) at the University of Illinois. Yammanuru was supported in part by an NSF GRFP. Morales was supported in part by Asociación Mexicana de Cultura A.C.

[^3]: $^*$ Equal contribution.

[^4]: $^{1}$Department of Computer Science at Mt. Holyoke College, South Hadley, MA, USA `duwacu@ mtholyoke.edu`

[^5]: $^{2}$ Department of Computer Science at the University of Illinois at Urbana-Champaign, Urbana, IL, USA `(ananyay2, kn19, sc83, moralesa, namato)@illinois.edu`

[^6]: $^{3}$ Department of Computer Science at Instituto Tecnológico Autónomo de México (ITAM), Mexico City, México.
