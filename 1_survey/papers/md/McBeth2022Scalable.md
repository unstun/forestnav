---
citation_key: McBeth2022Scalable
arxiv_id: 2210.07141
arxiv_url: https://arxiv.org/abs/2210.07141
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:27:01Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

Multi-robot systems have become ubiquitous in many settings such as autonomous factories and warehouses. When the motions of two or more robots are in conflict, highly coordinated multi-robot motion planning (MRMP) is required to avoid collisions with each other and with the environment.

Existing MRMP approaches perform well in open environments but struggle with narrow passages (e.g. warehouses aisles) due to the difficulty of avoiding collisions with obstacles within tight spaces. With multi-robot teams, narrow passages may be introduced or exacerbated by inter-robot collisions, further complicating planning.

There are three classes of MRMP approaches: decoupled, which plan a path for each robot separately and offer the least amount of coordination, coupled, which plan in the *composite space*, which incorporates the degrees of freedom of all robots, and hybrid, which offer a mix of coupled and decoupled planning. Decoupled approaches (e.g., Decoupled PRM [@sl-uppccdpmrs-2002]) allow for linear scaling with the number of robots; however, they lack the coordination necessary to resolve complex inter-robot collisions. Coupled methods (e.g., Composite RRT [@l-rrtntpp-1998] and Composite PRM [@sl-uppccdpmrs-2002]) provide this coordination but consider a large search space that becomes computationally intractable for large teams. Hybrid methods (e.g., CBS-MP [@smsa-rmmpucs-21] and M\* [@wc-sefmpp-15]) leverage the scalability of decoupled methods along with an increased level of coordination. However, in environments with narrow passages where inter-robot collisions are likely, their performance is limited by the time spent resolving conflicts. In this work, we propose a coupled method that exploits topological guidance to more intelligently and efficiently search the composite space.

![We demonstrate our method on a variety of physical and simulated environments. Video: <https://youtu.be/xP7mSWxdYfs>](McBeth2022Scalable_figs/phsical-inlet.png){#fig:physical-inlet width="48%"}

Guided planning methods leverage external information to efficiently find paths.

Topology-guided methods [@dsba-drbrrt-16; @suda-tgrcdrs-20; @rsb-beaeisbmp-2014] exploit representations of the environment to direct motion planning through narrow passages. Topological skeletons are embedded graphs encoding the environment. Prior work [@dsba-drbrrt-16; @suda-tgrcdrs-20] has explored guiding planning around a skeleton.

In this work, we extend topological skeleton guidance to multi-robot systems to provide the level of coordination required for large teams in environments with narrow passages. We present *Composite Dynamic Region-biased Rapidly-exploring Random Trees* (CDR-RRT), a coupled MRMP approach that leverages knowledge of the workspace topology, leading to improved planning times while retaining probabilistic completeness. We demonstrate significantly improved scalability compared to existing state-of-the-art methods, successfully finding paths for teams of size up to 25 times larger in complex environments where inter-robot collisions are likely. Our contributions include:

- The development of novel composite-space analogs of workspace skeletons and sampling regions.

- A scalable, probabilistically complete MRMP method that leverages topological guidance to address problems that require high levels of coordination.

- An experimental validation in a variety of congested and open environments with scaling robot team sizes.

# PRELIMINARIES AND RELATED WORK

In this section, we discuss the motion planning problem and research in both the multi-robot motion planning and guided motion planning domains.

## Motion Planning Preliminaries

A robot's *degrees of freedom* (dofs) include its position and orientation in the *workspace*, the 2D or 3D space within which the robot physically exists, as well as other configurable values such as joint angles. A *configuration* is a set of values describing the robot's dofs. The *configuration space* ($\mathcal{C}_{space}$) is the set of all robot configurations [@lw-apcfpapo-79]. The *free space* ($\mathcal{C}_{free}$) is the subset of $\mathcal{C}_{space}$ that only contains valid configurations (e.g. configurations not in collision with obstacles). The *obstacle space* ($\mathcal{C}_{obst}$) contains all configurations that are not valid. Given a start configuration, $q_{start}$, and a goal configuration, $q_{goal}$, the *motion planning problem* strives to find a path from $q_{start}$ to $q_{goal}$ through $\mathcal{C}_{free}$.

Searching the entire $\mathcal{C}_{space}$ is intractable [@ss-otpmpiigtfctporam-83; @c-crmp-88], resulting in the emergence of sampling-based motion planning algorithms [@kslo-prpp-96; @l-rrtntpp-1998]. These algorithms forego completeness guarantees in favor of faster planning and *probabilistic completeness*, meaning that the probability of finding a solution, if one exists, converges to 1 in the upper limit of planning time. Unfortunately, these randomized sampling techniques suffer in constrained environments [@hlk-pfprp-06], where they face the *narrow passage problem*. This refers to the difficulty of sampling valid configurations within narrow corridors that by volume make up a small proportion of the freespace.

The underlying sampling-based motion planning algorithm that forms the basis of our method is Rapidly-exploring Random Trees (RRT) [@l-rrtntpp-1998]. This method iteratively grows a tree, $T$, from $q_{start}$ to $q_{goal}$. During each iteration, a random configuration $q_{rand}$ is sampled. We then find $q_{near}$, the configuration in $T$ closest to $q_{rand}$. $T$ is then extended a maximum distance $\Delta$ from $q_{near}$ in the direction of $q_{rand}$. RRTs exhibit a Voronoi bias that results in the rapid exploration of the $\mathcal{C}_{space}$ and makes RRTs an efficient way to handle single-query motion planning problems. RRT variants have been developed to improve performance in the presence of narrow passages [@rtla-obrrt-06; @yjsl-ddreecsd-05].

## Multi-robot Motion Planning

Multi-robot motion planning consists of finding valid paths for a set of robots between their respective starts and goals.

The composite space is the Cartesian product of each of the $n$ individual robots' $\mathcal{C}_{spaces}$: $C_{composite} = C_1 \times C_2 \times ... \times C_n$ where $C_i$ represents the $\mathcal{C}_{space}$ of robot $i$. A composite configuration consists of values for each robot's dofs. The composite free space is made up of all valid configurations such that no robot is in collision with another robot. The MRMP problem can be formulated as finding a continuous path through the composite free space.

Table [\[tab:overview\]](#tab:overview){reference-type="ref" reference="tab:overview"} compares select MRMP approaches. Decoupled approaches such as Decoupled PRM [@sl-uppccdpmrs-2002] plan individual robot paths in their own decoupled $\mathcal{C}_{spaces}$ and thus do not offer completeness or optimality guarantees. The lack of coordination degrades their performance in narrow passages, where inter-robot collisions may not be possible to avoid along the individual paths only using velocity tuning.

Coupled methods such as Composite PRM [@sl-uppccdpmrs-2002] and Composite RRT [@l-rrtntpp-1998] plan directly within the composite $\mathcal{C}_{space}$. Other composite methods (e.g., MRdRRT [@ssh-faniaehdrfeoirimm-16]) build individual robot roadmaps, then search an implicit composite roadmap. These methods maintain the probabilistic completeness of the single-robot methods they use. However, due to the decoupled individual roadmap construction, they lack the level of coordination required to efficiently find paths in congested environments with narrow passages.

Hybrid methods such as CBS-MP [@smsa-rmmpucs-21], MAPF/C [@hpksga-tpqs-2018], and M\* [@wc-sefmpp-15] seek to leverage the strengths of both coupled and decoupled methods. For example, CBS-MP [@smsa-rmmpucs-21] plans individual robot paths in their decoupled $\mathcal{C}_{spaces}$ and then reconciles the paths in the composite $\mathcal{C}_{space}$. In the worst case, these methods will explore the whole composite $\mathcal{C}_{space}$, but on average, the runtimes are comparable to decoupled methods while providing varying levels of probabilistic completeness and representation optimality guarantees. These methods are generally not well suited for environments with narrow passages due to the computational effort expended transitioning the planner from decoupled to the high level of coordination required. Here, we propose a method for composite-space RRT construction while leveraging topological guidance to improve performance in environments with narrow passages.

## Guided Motion Planning

Topological guidance has not been well explored in the composite space; however, some hybrid methods have explored using topological information to construct decoupled roadmaps. Ryan [@r-cbmrpp-2010] decomposes the workspace into halls, represented by singly-linked chains of vertices, and open spaces, represented by fully-connected subgraphs. Yu et al. [@Yu2018] propose a method for roadmap construction via overlaying a lattice structure onto the workspace. They show that this method leads to efficient path planning for large groups of robots in relatively open environments.

Several single-robot motion planning strategies have been proposed to adapt planning to the workspace. The Feature Sensitive Motion Planning Strategy [@mtpra-mlafsmp-04] attempts to subdivide the environment into homogeneous workspace regions that are planned in individually, adapting roadmap construction to local features. The individual roadmaps are merged into a complete roadmap of the planning space. This strategy allows the planner to use resources efficiently.

Workspace Decomposition Strategies [@kh-wisprp-04; @bo-uwignsprp-04; @kh-wco-06] help concentrate planning in narrow areas of the workspace. SyClop [@pkv-mpdsclp-10] uses an RRT to sample frontier decomposition regions. A User-Guided Planning Strategy [@dsja-arbsfcrc-14] allows the user to define and manipulate workspace sampling regions that the planner explores in real-time. The planner relies on the user's intuition to identify narrow passages and find paths faster.

Skeleton-based strategies leverage the topology of the workspace using an embedded graph (Fig. [\[fig:init-skel\]](#fig:init-skel){reference-type="ref" reference="fig:init-skel"}) that is homotopy equivalent to the workspace. All points in the workspace can be smoothly collapsed to the skeleton [@blk-tcsrp-2012]. Skeleton edges describe contiguous volumes of the free workspace (e.g., tunnels or rooms) and vertices represent connections between these volumes. Given the environment, the skeleton is precomputed and may be used for multiple queries and different types of robots. Examples include medial axis skeletons [@Blum_1967_6755] in 2D and mean curvature skeletons [@t-mcs-12] in 3D. Skeletons are generally quick to compute. The medial axis skeleton, for example, can be computed in $O(n \log n)$ time where $n$ is the number of obstacle edges [@l-matoaps-1982].

Dynamic Region Sampling with PRM (DR-PRM) [@suda-tgrcdrs-20], initiates local components at the vertices of a skeleton, expands them along adjacent edges, then merges them to form a complete roadmap. Hierarchical Annotated Skeleton Planning [@uyma-hpwakg-2022] extends DR-PRM by relaxing its reliance on skeleton edges over time. We describe the single-query counterpart of DR-PRM, Dynamic Region-biased RRT (DR-RRT), in detail in Section [2.4](#sec:dr-rrt){reference-type="ref" reference="sec:dr-rrt"} since we extend our method from it. These methods show the advantage of using workspace information to guide planning in $\mathcal{C}_{space}$ when they are closely related; however, they are constrained to single-robot settings.

## Dynamic Region-biased RRT {#sec:dr-rrt}

DR-RRT [@dsba-drbrrt-16] (Alg. [\[alg:dynamicregions\]](#alg:dynamicregions){reference-type="ref" reference="alg:dynamicregions"}) grows an RRT while constraining sampling within regions that advance along a skeleton.

### Query Skeleton

Algorithm [\[alg:dynamicregions\]](#alg:dynamicregions){reference-type="ref" reference="alg:dynamicregions"} creates two skeletons: one for the entire workspace (line [\[alg:init-skel\]](#alg:init-skel){reference-type="ref" reference="alg:init-skel"}), and the *query skeleton* (Fig. [\[fig:query-skel\]](#fig:query-skel){reference-type="ref" reference="fig:query-skel"}; line [\[alg:query-skel\]](#alg:query-skel){reference-type="ref" reference="alg:query-skel"}), which retains only edges that are along a path from the start to the goal in the workspace.

:::: {#fig:dr-rrt-skeletons .figure}
::: caption
An example workspace skeleton (a) and query skeleton (b). The query skeleton is a directed and pruned skeleton that only contains edges along a path from $q_{start}$ to $q_{goal}$.
:::
::::

:::: algorithm
::: algorithmic
Environment $e$ and a Query $\{q_s, q_g\}$

Tree $T$ $W \gets \textsc{ComputeWorkspaceSkeleton}(e)$ []{#alg:init-skel label="alg:init-skel"} $S \gets \textsc{ComputeQuerySkeleton}(W, q_s, q_g)$ []{#alg:query-skel label="alg:query-skel"} $T \gets (\emptyset, \emptyset)$ $R \gets \textsc{InitialRegions}(S, q_s)$ []{#alg:init-regions label="alg:init-regions"} $\textsc{RegionBiasedRRTGrowth}(T, S, R)$ $T$
:::
::::

:::: algorithm
::: algorithmic
Tree $T$, Query Skeleton $S$, Regions $R$, region radius $\eta$, maximum for failed extension attempts $\tau$ $r \gets \textsc{SelectRegion}(R)$ []{#alg:select-region label="alg:select-region"} $q_{rand} \gets r.\textsc{GetRandomCfg}()$ $q_{near} \gets \textsc{NearestNeighbor}(T, q_{rand})$ []{#alg:qrand label="alg:qrand"} $q_{new} \gets \textsc{Extend}(q_{near}, q_{rand}, \Delta)$ []{#alg:qnew label="alg:qnew"} []{#alg:success-rate label="alg:success-rate"} $r.\textsc{IncrementSuccesses()}$ $r.\textsc{IncrementFailures()}$ []{#alg:end-success-rate label="alg:end-success-rate"} []{#alg:for-advance label="alg:for-advance"} $r.\textsc{AdvanceAlongSkeletonEdge}()$ []{#alg:end-for-advance label="alg:end-for-advance"} []{#alg:delete-end label="alg:delete-end"} $R \gets R \setminus \{r\}$ []{#alg:end-delete-end label="alg:end-delete-end"} []{#alg:fail-start label="alg:fail-start"} $R \gets R \setminus \{r\}$ []{#alg:fail-end label="alg:fail-end"} []{#alg:new-regions label="alg:new-regions"} $R \gets R \cup \textsc{NewRegion(v)}$ $S.\textsc{MarkExplored}(v)$ []{#alg:end-new-regions label="alg:end-new-regions"}
:::
::::

### Sampling Regions

Sampling regions will advance along the edges of the query skeleton, using the skeleton, a solution in the workspace, to guide construction of an RRT, a solution in the $\mathcal{C}_{space}$. A *region* is a bounded volume in the workspace, e.g., a bounding sphere. Construction of the RRT begins by initializing the first region centered on the skeleton vertex closest to $q_{start}$ (line [\[alg:init-regions\]](#alg:init-regions){reference-type="ref" reference="alg:init-regions"}). During each iteration, Algorithm [\[alg:rbrrtg\]](#alg:rbrrtg){reference-type="ref" reference="alg:rbrrtg"} selects a region to guide sampling (line [\[alg:select-region\]](#alg:select-region){reference-type="ref" reference="alg:select-region"}). The probability of selecting a region is proportional to its *extension success rate*. To maintain probabilistic completeness, with a small probability, the entire environment is chosen (see Sec. [3.5](#sec:theory){reference-type="ref" reference="sec:theory"}). A random configuration $q_{rand}$ is selected from this region to grow the tree toward (line [\[alg:qrand\]](#alg:qrand){reference-type="ref" reference="alg:qrand"}). The algorithm then proceeds as a general RRT by attempting to extend the tree to $q_{new}$ (line [\[alg:qnew\]](#alg:qnew){reference-type="ref" reference="alg:qnew"}). The extension success rate is updated based on the outcome of this attempt (lines [\[alg:success-rate\]](#alg:success-rate){reference-type="ref" reference="alg:success-rate"}-[\[alg:end-success-rate\]](#alg:end-success-rate){reference-type="ref" reference="alg:end-success-rate"}).

### Region Advancement

Once a configuration has been added to the tree, all regions that are in contact with $q_{new}$ are advanced forward along their skeleton edges until they leave $q_{new}$ behind (Alg. [\[alg:rbrrtg\]](#alg:rbrrtg){reference-type="ref" reference="alg:rbrrtg"}, lines [\[alg:for-advance\]](#alg:for-advance){reference-type="ref" reference="alg:for-advance"}-[\[alg:end-for-advance\]](#alg:end-for-advance){reference-type="ref" reference="alg:end-for-advance"}). Any region that reaches the end of its edge or exceeds the maximum number of extension failures is deleted (lines [\[alg:delete-end\]](#alg:delete-end){reference-type="ref" reference="alg:delete-end"}-[\[alg:fail-end\]](#alg:fail-end){reference-type="ref" reference="alg:fail-end"}). Then, new regions are created on each unexplored skeleton vertex that is within a small distance of $q_{new}$ (lines [\[alg:new-regions\]](#alg:new-regions){reference-type="ref" reference="alg:new-regions"}-[\[alg:end-new-regions\]](#alg:end-new-regions){reference-type="ref" reference="alg:end-new-regions"}). This cycle of region selection, tree extension, region advancement, and region creation continues until the tree extends to $q_{goal}$.

# COMPOSITE DYNAMIC REGION-BIASED RRT

In this paper, we extend DR-RRT to multi-robot systems to propose a new method, Composite Dynamic Region-biased RRT (CDR-RRT). We limit the exploration of the composite space to areas that are likely to yield a solution because of the exponential size of the search space.

We do this by developing composite analogs for workspace skeletons and regions that allow for coupled multi-robot motion planning while leveraging topological guidance as in DR-RRT. We leverage lazy construction of the composite skeleton as we exploit a greedy heuristic to search the composite space.

## Composite Skeleton {#sec:comp-skel}

:::: {#fig:composite-edge .figure latex-placement="t"}
::: caption
An example of a composite edge and a composite region. Each of the three robots has its own workspace skeleton. Obstacles are gray, and the workspace skeletons are purple. Three skeleton edges that comprise a composite edge are shown in blue. All possible combinations of such edges make up the composite skeleton. Three individual regions that make up a composite region along this composite edge are shown in green.
:::
::::

:::: algorithm
::: algorithmic
Tree $T$, Composite Skeleton $S$, Region $r$, Failed Vertex and Edge Constraints $C$, Maximum for Failed Extension Attempts $\tau$ $Bound \gets \textsc{SelectRegionOrWholeEnvironment}()$[]{#alg:bounds label="alg:bounds"} $q_{rand} \gets r.\textsc{GetRandomCompositeCfg}(Bound)$ $q_{near} \gets \textsc{NearestNeighbor}(T, q_{rand})$ $q_{new} \gets \textsc{Extend}(q_{near}, q_{rand}, \Delta)$ $r.\textsc{IncrementSuccesses()}$ $r.\textsc{IncrementFailures()}$ $r.\textsc{AdvanceAlongCompositeSkeletonEdge}()$[]{#alg:end-adv-siblings label="alg:end-adv-siblings"} []{#alg:delete-comp-region label="alg:delete-comp-region"} $V_t \gets r.\textsc{CompositeTargetVertex()}$ $r \gets S.\textsc{GrowCompositeSkeleton}(V_t, C)$ []{#alg:delete-grow-skel label="alg:delete-grow-skel"} []{#alg:priority-queue label="alg:priority-queue"} $C \gets C \cup \{r.\textsc{Edge\}}$ $V_s \gets r.\textsc{CompositeSourceVertex}()$ $C \gets C \cup \{V_s\}$ $V_s \gets V_s.\textsc{GetPredecessor}()$ $r \gets S.\textsc{GrowCompositeSkeleton}(V_s, C)$ []{#alg:replace-region label="alg:replace-region"}
:::
::::

As the composite space is the Cartesian product of each robot's $\mathcal{C}_{space}$, the composite skeleton (Fig. [3](#fig:composite-edge){reference-type="ref" reference="fig:composite-edge"}) is the Cartesian product of the workspace skeleton for each of the $n$ robots. It consists of composite vertices and edges which respectively represent a set of $n$ vertices or edges in the workspace skeleton where each of the $n$ robots lies. We avoid the exponential expansion associated with the computation of the full composite skeleton graph by using local, on-demand construction. A composite region is made up of $n$ individual sampling regions, one in each robot's workspace.

Computing a composite query skeleton, which is a directed and pruned version of the composite skeleton, requires an explicit computation of the composite skeleton.

Instead, we heuristically construct and search the composite skeleton one edge at a time and only consider edges likely to be along a feasible low-cost path from $q_{start}$ to $q_{goal}$. We discuss our heuristic to capture these edges in Section [3.3](#section:cbs-heur){reference-type="ref" reference="section:cbs-heur"}.

## Guided Composite RRT Construction

:::: algorithm
::: algorithmic
Composite Skeleton $S$, Composite Source Vertex $V$, Failed Vertex and Edge Constraints $C$ $V \gets V.\textsc{GetPredecessor}()$ []{#alg:predecessor label="alg:predecessor"} $Paths \gets \textsc{MAPFSolution}(V, C)$ []{#alg:mapf label="alg:mapf"} $E \gets \textsc{ExtractFirstCompositeEdge}(Paths)$ []{#alg:extract label="alg:extract"} $S.\textsc{AddEdge}(E)$ $\textsc{NewRegion}(E)$ []{#alg:newregion label="alg:newregion"}
:::
::::

To begin RRT construction, we compute the first composite skeleton edge to explore. Section [3.3](#section:cbs-heur){reference-type="ref" reference="section:cbs-heur"} discusses the construction of composite skeleton edges by growing the composite skeleton from a source composite vertex. CDR-RRT then proceeds as DR-RRT by iteratively performing region-biased sampling, RRT growth, region advancement and deletion, and new region creation until $q_{goal}$ is reached.

During each iteration of CDR-RRT, Algorithm [\[alg:crbrrtg\]](#alg:crbrrtg){reference-type="ref" reference="alg:crbrrtg"} selects a composite region $r$. After sampling from $r$ and extending the tree, we advance $r$ forward until it leaves $q_{new}$ behind (line [\[alg:end-adv-siblings\]](#alg:end-adv-siblings){reference-type="ref" reference="alg:end-adv-siblings"}). In DR-RRT [@dsba-drbrrt-16], as individual regions advance along skeleton edges, they are centered on intermediate points along the edges. Correspondingly, we create composite intermediates along composite skeleton edges. In composite region advancement, as shown in Fig. [4](#fig:adv){reference-type="ref" reference="fig:adv"}, all individual regions are advanced forward the minimum amount of intermediates such that the composite region is no longer touching $q_{new}$.

When a composite region reaches the target vertex at the end of its edge, we add an outgoing edge to the composite skeleton from this vertex and spawn a new region (Alg. [\[alg:growskeleton\]](#alg:growskeleton){reference-type="ref" reference="alg:growskeleton"}). When a region surpasses $\tau$ failed extension attempts, it is deleted and replaced with a new region (line [\[alg:replace-region\]](#alg:replace-region){reference-type="ref" reference="alg:replace-region"}).

:::: {#fig:adv .figure latex-placement="t"}
![](McBeth2022Scalable_figs/double_region_advancement.png)

::: caption
An example of composite region advancement for two point robots in a 1D environment. The individual robots' skeletons are shown on the axes and the composite skeleton between them. Each individual roadmap is shown in blue and the composite roadmap is in purple. Edge intermediates are shown as tick marks along the skeletons. Both individual regions advance at the same rate with respect to their individual intermediates until the composite region leaves $q_{new}$ behind at the position shown in dark green.
:::
::::

## Multi-agent Pathfinding Heuristic {#section:cbs-heur}

We use a multi-agent pathfinding (MAPF) heuristic to identify the next edge to explore given a source composite vertex, $V$ (Alg. [\[alg:growskeleton\]](#alg:growskeleton){reference-type="ref" reference="alg:growskeleton"}). MAPF is the discrete state space equivalent of the MRMP problem. We use MAPF to generate a path for each robot through the workspace skeleton from $V$ to the vertex closest to each robot's goal (line [\[alg:mapf\]](#alg:mapf){reference-type="ref" reference="alg:mapf"}). We ensure that these individual paths are feasible by accounting for potential collisions between robots. We define the capacity of an individual skeleton edge as the minimum width between obstacles along the edge. If the total width of the robots traversing that edge exceeds the capacity, a conflict has occurred. These conflicts are resolved by the MAPF algorithm.

:::: {#fig:mapf-replan .figure latex-placement="t"}
::: caption
An example of the MAPF replanning process. (a) If a composite skeleton edge (in red) cannot be traversed, we impose a constraint that future MAPF solutions cannot contain that edge and replan the paths from the last vertex reached. (b) If the maximum number of failed outgoing edges from a vertex is exceeded, a constraint is imposed that future MAPF solutions cannot contain that vertex, and paths are replanned from its predecessor.
:::
::::

We extract composite skeleton edges from the produced MAPF solution (Alg. [\[alg:growskeleton\]](#alg:growskeleton){reference-type="ref" reference="alg:growskeleton"}, line [\[alg:extract\]](#alg:extract){reference-type="ref" reference="alg:extract"}) and iteratively create a region to traverse each edge. If a region exceeds the maximum number of extension failures traversing an edge, we consider that edge failed and impose a constraint that no further MAPF solutions can contain that composite skeleton edge (Fig. [\[fig:failed_comp_edge\]](#fig:failed_comp_edge){reference-type="ref" reference="fig:failed_comp_edge"}). We also increment the number of failed growth attempts that each source composite skeleton vertex has seen. To avoid spending excess computation exploring a region of the composite skeleton that is unlikely to produce a path, if a vertex exceeds the maximum number of growth failures, we backtrack to its predecessor vertex (Fig. [\[fig:failed_comp_vertex\]](#fig:failed_comp_vertex){reference-type="ref" reference="fig:failed_comp_vertex"}; line [\[alg:predecessor\]](#alg:predecessor){reference-type="ref" reference="alg:predecessor"}).

## Implementation Details

To generate MAPF solutions, we adapt Conflict-Based Search (CBS) [@ssfs-cbsfomap-15] and Priority-Based Search (PBS) [@ma2019searching]. Both use a hierarchical approach with a low-level search to find individual paths for each agent and a high-level search to resolve conflicts between paths. CBS finds optimal paths with respect to the makespan while PBS has been shown to achieve improved performance in scenarios where the optimal path for one robot blocks the path for other robots.

The size of the full composite skeleton is exponential in the number of robots, so we optimize memory usage by leveraging local construction of the composite skeleton. We can also remove composite vertices and edges when they are no longer useful. A composite edge is no longer useful when the composite region that traverses it has reached the end and been deleted. A composite vertex is no longer useful when all of its incoming and outgoing edges are no longer useful.

:::: {#fig:warehouse .figure}
\

::: caption
The Cross (a) and Flow (b) scenarios feature a single hallway through which all robots must pass. In Cross, the robots on either side must swap places. In Flow, all robots must move from one side of the hallway to the other. In the Inlet (c) scenario, the robots must swap places. One robot must move into the inlet to allow the other to pass. The track environment (d) features a ring through which robots must move. The robots on top and bottom must swap places by moving in the same direction to avoid collision. The Warehouse scenario (e) has three variants of aisle widths (1, 2, and 4 meters; the 1m variant is shown). The robots on top and bottom must swap places with the robot with which they are aligned vertically.
:::
::::

:::: {#fig:cross .figure}
::: caption
In the Open Cross (a) environment, the red robots must move from left to right and the blue robots from top to bottom. In the Maze Cross (b) environment, robots starting on the left and right must swap places by moving through the 3D tunnel structure.
:::
::::

:::: {#fig:coord-graphs .figure latex-placement="t!"}
::: caption
Running time and path cost results for the Hallway (a), Inlet (b), and Track (c) environments.
:::
::::

:::: {#fig:warehouse-both-graph .figure latex-placement="t!"}
![](McBeth2022Scalable_figs/Store.png){width=".49\\textwidth"}

::: caption
Running time and path cost results for the Warehouse scenarios.
:::
::::

:::: {#fig:track-cdr-rrt-graph .figure latex-placement="t!"}
![](McBeth2022Scalable_figs/Track-CDR-RRT-heur.png){width="49%"}

::: caption
Running time results for up to 100 robots for CDR-RRT on the Track Environment including heuristic evaluation times.
:::
::::

:::: {#fig:cross-results .figure}
::: caption
Results for the Open Cross (a) and Maze Cross (b) environments for all methods. Those that were unable to find a solution within the time limit are omitted. We demonstrate improved scalability as compared to the other methods by consistently achieving low planning times even as the number of robots increases. On the larger (4 and 6-robot) scenarios with narrow passages, CDR-RRT achieves the lowest running time.
:::
::::

## Theoretical Analysis {#sec:theory}

*Theorem:* CDR-RRT is probabilistically complete.

*Proof:* During each iteration of CDR-RRT, there is a probability $\epsilon > 0$ of sampling from the entire environment rather than within a region (Alg. [\[alg:crbrrtg\]](#alg:crbrrtg){reference-type="ref" reference="alg:crbrrtg"}, line [\[alg:bounds\]](#alg:bounds){reference-type="ref" reference="alg:bounds"}). Sampling from the entire environment guarantees probabilistic completeness, ensuring that a valid path from $q_{start}$ to $q_{goal}$ will be found, if one exists, even if all regions are unable to produce valid configurations. As $\epsilon$ increases to 1 or as the size of regions is increased to encompass the entire workspace, knowledge of the workspace topology is utilized less and the method eventually reduces to Composite RRT.

# VALIDATION

We run scaling MRMP queries in environments designed to highlight the strengths and weaknesses of our approach. We consider both environments with different narrow passage widths and open environments to measure how CDR-RRT compares to other state-of-the-art methods when the workspace is and is not informative. We measure each algorithm's performance in scenarios that require various levels of coordination during planning to demonstrate our improved performance when high coordination is required.

## Experimental Setup

We compare to several state-of-the-art MRMP methods (Table [\[tab:overview\]](#tab:overview){reference-type="ref" reference="tab:overview"}). We use CBS-MP [@smsa-rmmpucs-21] with DR-PRM [@suda-tgrcdrs-20] to construct the individual roadmaps as a comparison against a hybrid method with workspace guidance. We use the implementation of MAPF/C described in [@hpksga-tpqs-2018] with SPARS [@db-spsanomp-13] roadmap generation. Although MRdRRT [@ssh-faniaehdrfeoirimm-16] was designed primarily for manipulators, we compare to it since its use of a tensor-product roadmap to conduct an RRT-style search of the composite space is similar to our composite skeleton guidance. We pre-compute medial-axis skeletons for 2D environments and mean curvature skeletons for 3D environments.

All methods were implemented in C++ in the Parasol Planning Library. The experiments were run in simulation with holonomic mobile robots using a desktop computer with an Intel Core i9-10900KF CPU at 3.7 GHz and 128 GB of RAM. Each method is given 600 seconds to find a plan or is considered unsuccessful. We report planning times and average path costs given by the makespan.

## Environments

In this section, we describe our experimental environments and explain why these scenarios highlight the advantages and disadvantages of our approach relative to other methods.

### Corridors (Fig. [\[fig:hall-cross\]](#fig:hall-cross){reference-type="ref" reference="fig:hall-cross"}-[\[fig:track\]](#fig:track){reference-type="ref" reference="fig:track"})

We consider the Hallway environment featuring a single tunnel within which only one robot may fit vertically, preventing robots from passing each other. We consider two variants of this scenario, one in which two groups of robots start on opposite ends of the tunnel and swap places (*Cross*, Fig. [\[fig:hall-cross\]](#fig:hall-cross){reference-type="ref" reference="fig:hall-cross"}) and one in which all robots start on one side and must move to the other (*Flow*, Fig. [\[fig:hall-flow\]](#fig:hall-flow){reference-type="ref" reference="fig:hall-flow"}). In the Inlet scenario (Fig. [\[fig:inlet\]](#fig:inlet){reference-type="ref" reference="fig:inlet"}), we show how each method performs when one robot must explicitly move out of the other's way, requiring a high level of coordination. Similarly, in the Track scenario (Fig. [\[fig:track\]](#fig:track){reference-type="ref" reference="fig:track"}), we show how each method performs when all robots must move in the same direction around an obstacle, again requiring a high level of coordination, but for larger robot groups.

### Warehouse (Fig. [\[fig:short-warehouse\]](#fig:short-warehouse){reference-type="ref" reference="fig:short-warehouse"})

The Warehouse scenario is designed to imitate the motions required to fetch or place items on shelves in a warehouse. The topology creates several parallel narrow passages, and queries are selected such that conflicting choices of aisles are likely, thus requiring coordination during planning to avoid inter-robot collisions. It includes a width-wise aisle cutting through the middle of the length-wise aisles creating entry/exit points that can be used to avoid collisions. We scale the number of aisles with the number of robots. We consider three variants with progressively doubled aisle widths.

### Open Cross (Fig. [\[fig:open-cross\]](#fig:open-cross){reference-type="ref" reference="fig:open-cross"})

We evaluate our approach on a classic open MRMP scenario [@smsa-rmmpucs-21] to demonstrate how our method compares when the workspace is not informative, limiting the benefit of topological skeleton guidance.

### Maze Cross (Fig. [\[fig:3d_maze\]](#fig:3d_maze){reference-type="ref" reference="fig:3d_maze"})

In this 3D environment with a narrow maze tunnel, the number of degrees of freedom of each mobile robot is doubled relative to a 2D workspace, resulting in a very large composite space.

## Narrow Passages

The Hallway, Inlet, and Track scenario results are given in Fig. [8](#fig:coord-graphs){reference-type="ref" reference="fig:coord-graphs"}. In the Hallway scenario, CDR-RRT's use of skeleton guidance allows it to find considerably lower cost paths than other methods in both variants of the problem, especially with the larger 4 and 6-robot groups. Composite RRT was able to solve the 6-robot scenarios but with significantly decreased success rates and higher path costs. MRdRRT and MAPF/C were unable to find solutions within the time limit.

Considering the Inlet scenario, runtimes for CDR-RRT, Composite RRT, Composite PRM, and MAPF/C were similar; however, the solution quality varies greatly between the methods. CDR-RRT has an average path cost of 15.35s, while Composite RRT, Composite PRM, and MAPF/C have average path costs of 22.31s, 22.13s, and 25.30s respectively. By sampling along skeleton edges, CDR-RRT finds more direct, lower-cost paths. CBS-MP and MRdRRT were unable to find solutions. We also demonstrate our method on physical robots (Fig. [1](#fig:physical-inlet){reference-type="ref" reference="fig:physical-inlet"}). We use Turtlebot3s and integrate ROS with our planning library to follow paths generated by CDR-RRT.

In the Track environment, only CDR-RRT is able to find a solution to the 6-robot scenario due to the difficulty of sampling paths where each robot moves in the same direction. CDR-RRT's use of a MAPF heuristic to find feasible paths over the composite skeleton allows it to efficiently recognize the robots must move either clockwise or counterclockwise. None of the other methods was able to achieve over a 7% success rate on the 4-robot scenario. Decoupled PRM was unable to find a solution for any scenario.

The Warehouse scenarios demonstrate each method's performance in with varying widths of narrow passages (results in Fig. [9](#fig:warehouse-both-graph){reference-type="ref" reference="fig:warehouse-both-graph"}). CDR-RRT achieves the lowest planning time on all scenarios and its use of skeleton guidance allows it to scale to the more complex 4 and 6-robot scenarios, where the performance of other methods significantly degrades. Decoupled PRM was unable to complete any scenario.

## Scalability

We ran up to 100-robot Track scenarios with an 1800-second time limit for CDR-RRT to measure its performance on larger problems. Fig. [10](#fig:track-cdr-rrt-graph){reference-type="ref" reference="fig:track-cdr-rrt-graph"} shows that CDR-RRT is able to efficiently find paths for very large robot teams when a high level of coordination is required. We also show that CDR-RRT's MAPF heuristic evaluation maintains scalability.

## Robot Crossings

The Open Cross and Maze Cross environments evaluate each method's performance in different robot cross scenarios, in which topological guidance provides varying levels of benefit. The Open Cross environment results are in Fig. [\[fig:open-graph\]](#fig:open-graph){reference-type="ref" reference="fig:open-graph"}. When the topology is not useful, workspace guidance still biases robot paths along skeleton edges, which, in an environment without obstacles, increases the potential for collision relative to Composite RRT and Composite PRM. As a result, CDR-RRT has a higher average planning time than Composite RRT and Composite PRM. This shows that composite skeleton guidance is most effective when there are narrow passages that robots must pass through.

In the Maze Cross scenarios (Fig. [\[fig:maze-graph\]](#fig:maze-graph){reference-type="ref" reference="fig:maze-graph"}), CDR-RRT and CBS-MP are the only methods able to plan for 4 robots. Only CDR-RRT is able to plan for 6 robots with 100% success within the time limit (CBS-MP - 33%). Decoupled PRM failed to solve the 2-robot scenario. In 3D environments, the size of the composite $\mathcal{C}_{space}$ increases significantly, boosting the impact of composite skeleton guidance.

# CONCLUSION AND FUTURE WORK

We present Composite Dynamic Region-biased Rapidly-exploring Random Trees, a scalable workspace-guided multi-robot motion planning approach. We validate our method on a variety of environments, with and without narrow passages, to demonstrate its strengths and weaknesses. We show improved performance in constricted environments. Future work will explore the use of composite skeleton guidance for PRM-based roadmap construction, expanding its utility to multi-query scenarios, as well as extending skeleton guidance to non-holonomic robot teams.

[^1]: $^{1}$Courtney McBeth, James Motes, Marco Morales, and Nancy M. Amato are with the Parasol Lab, Department of Computer Science, University of Illinois Urbana-Champaign, Champaign, IL 61820 USA `{cmcbeth2, jmotes2, moralesa, namato}@illinois.edu`

[^2]: $^{2}$Diane Uwacu is with the Texas A&M University Department of Computer Science and Engineering, College Station, TX 77840 USA `duwacu@tamu.edu`

[^3]: This work was supported in part by Foxconn Interconnect Technology (FIT) and the Center for Networked Intelligent Components and Environments (C-NICE) at UIUC.
