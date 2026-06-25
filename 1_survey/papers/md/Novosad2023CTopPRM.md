---
citation_key: Novosad2023CTopPRM
arxiv_id: 2305.13969
arxiv_url: https://arxiv.org/abs/2305.13969
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:55:07Z
origin: ai+web
reviewed: false
---

= 

::: IEEEkeywords
Motion and Path Planning; Planning, Scheduling and Coordination
:::

# Supplementary Material {#supplementary-material .unnumbered}

**Video:** <https://youtu.be/azNrWBU5cAk>\
**Code:** <https://github.com/ctu-mrs/CTopPRM>

# Introduction[]{#sec:intro label="sec:intro"}

planning [@lavalle2006planning] is one of the fundamental problems in robotics. It requires finding a geometrical path for a robot between given start and goal positions while avoiding collisions. However, there are several applications that would benefit from having multiple alternative paths. To address this issue, topologically distinct paths, representing the topological connectivity of a cluttered environment should be considered. Multiple paths allow the robot to select different ways how to navigate through the environment, see Fig. [1](#fig:illustration){reference-type="ref" reference="fig:illustration"}(d) with multiple distinct paths in a building-like environment.

:::: {#fig:illustration .figure latex-placement="t"}
::: caption
Illustration of the proposed CTopPRM method which starts by creating a dense Probabilistic Roadmap clustered around the start and goal positions (a). New cluster centroids are then iteratively added to promising places in the roadmap (b) to create a sparse graph (c), which is finally used to find distinct paths (d). []{#fig:illustration label="fig:illustration"}
:::
::::

Finding multiple paths with distinct topological classes can be used, for example, in optimization-based [@zhou2021raptor] or sampling-based [@penicka2022quadrotor] trajectory planners that have to consider robot dynamics. Finding multiple paths helps to find the optimal trajectory as the trajectory planning is restricted to a single topological class of a given initial path. Similarly, the paths can also be used to guide reinforcement learning methods for agile flight [@penicka2022RL]. Last but not least, finding multiple distinct paths is beneficial for guided-based planners solving high-dimensional motion planning problems [@denny2016theory; @vonasek2019iros; @denny2020dynamic; @vonasek2020searching; @belter2022walking]. These planners sample the configuration space of the robot around the guiding paths and thus increase the effectiveness of planning in environments with narrow passages. However, while online trajectory planning requires fast computation, guided-based planners and reinforcement learning methods often benefit more from acquiring a higher number of guiding paths. Therefore, when searching for multiple topologically distinct paths, a trade-off between computational time and the number of found distinct paths has to be considered. This was so far the main stumbling block of existing methods.

The majority of existing methods for planning multiple distinct paths use a graph-based roadmap representation. To discover all distinct paths, especially in challenging 3D environments, a dense roadmap is required. However, searching for multiple paths as proposed in [@fujita2003dualdijkstra] proves to be computationally expensive, even more so in a dense roadmap. Moreover, many found paths would belong to the same topological class, requiring an exhaustive filtering process. Visibility-PRM [@simeon2000visibilityprm] introduced a concept that allows the construction of a sparse roadmap, that was used by [@zhou2021raptor], [@simeon2008deformation] and [@schmitzberger2002hppr]. Yet, Visibility-PRM's reliability, i.e. the ability to consistently capture all topological classes, is limited, particularly in environments with narrow passages, which require a higher density of samples to capture paths leading through them. However, finding multiple distinct paths in the dense roadmaps is computationally very demanding.

To this end, we propose a novel sampling-based method called Clustering Topological PRM (CTopPRM), that clusters a dense roadmap, to construct a sparse graph with cluster centroids as vertices. This reduced roadmap allows fast path searching while capturing all topological classes that the initial dense roadmap had captured, including those that require traversal of narrow passages. Moreover, the algorithm enables adjusting the trade-off between computational time and number of paths found using tunable parameters. This makes it suitable for both online planning within tens of milliseconds, and for offline planning with narrow passages.

We consider the contributions of this paper to be as follows. We introduce an efficient method for identifying topologically distinct paths, with a controllable balance between computational time and the quantity of identified paths. We demonstrate that our approach, called CTopPRM, outperforms existing methods in a variety of challenging cluttered environments. In scenarios with a low number of distinct topological classes, CTopPRM is shown to successfully identify 94 % of all distinct paths while other methods find less than 80 % of paths within the same run-time. In environments with a high number of distinct topological classes, we improved the average number of topological classes detected within the same computational time between 30 % and 300 %. Finally, we release CTopPRM's source code and our implementations of related methods, along with testing environments, as an open-source package.

# Related Work[]{#sec:related label="sec:related"}

A complete solution to the problem of finding all topologically distinct paths in cluttered environments relies on combinatorial motion planning approaches. However, these methods [@rosman2017dfs; @kuderer2014onlinegeneration] use representations (e.g., Voronoi diagram) that require an explicit representation of occupied space. An optimization-based approach described in [@huang2017gaussian] proposes to use Gaussian processes to construct a factor graph representing a distribution of multiple trajectories, which are then optimized and filtered. However, the functionality of this method was verified only in 2D. Additionally, some of the trajectories found belong to the same topological class. Therefore, the resulting paths must be pruned by identifying topologically equivalent paths. Authors in [@bhattacharya2012constraints] introduce homotopy relation in the form of h-signatures, applicable in both 2D and 3D, but only with time and memory-consuming space discretization. Moreover, the discretized space often fails to capture narrow passages.

To approximate the continuous configuration space, a graph-based representation called roadmap, e.g., Probabilistic Roadmap (PRM) [@kavraki1996PRM], is commonly used. Many existing methods for finding distinct topological classes [@simeon2008deformation; @schmitzberger2002hppr; @zhou2021raptor; @penicka2022quadrotor; @zhang2019sparse; @rosmasnn2015multiple] take one of the PRM variants as a starting point. The Probabilistic Roadmap algorithm is a widely used sampling-based method for motion planning that consists of two main phases. In the construction phase, the PRM algorithm generates a set of random feasible configurations, also known as samples. These samples are then connected to each other using a local planner.

The original PRM implementation in [@kavraki1996PRM] did not allow cycles in the roadmap, which limited its connectivity, completeness and the ability to capture more than one topological class. To address this, [@karmaman2011sPRM] introduced a version called sPRM that allows cycles in the graph, and is more widely used nowadays. The author of Informed PRM [@aria2021informedprm] proposes to only sample an ellipsoid space between start and goal configurations. Method in [@kala2016hrm] aims to generate PRM that guarantees to capture all topological classes in an environment, by using an obstacle biased sampler, but relies on explicit representation of occupied space, which is unreasonable for 3D environments.

After PRM is constructed, query phase follows where a path between two samples is found using any standard graph searching algorithm such as Dijkstra's or A\*. However, these algorithms only find the shortest path in the roadmap. Method [@fujita2003dualdijkstra] proposes an approach that uses Dijkstra's algorithm to find all paths between start and goal node by finding a path to each node from start and from goal, resulting in total number of paths equal to number of nodes. Method then proceeds to prune any redundant paths, which is an exhaustive process, especially in dense graphs with a high number of nodes, which are necessary in challenging environments that contain multiple narrow passages. Depth-first search algorithm, followed by pruning of redundant paths according to equivalency relation introduced in [@bhattachacharya2010homotopyconstraints], proposed in [@rosmasnn2015multiple] is also affected by this issue. For graph search to be efficient, a sparser roadmap, with reduced number of nodes has to be constructed. Authors in [@zhang2019sparse] propose a method to delete certain edges from a dense roadmap to construct a sparse near-optimal graph. However, even though created graph is sparser, it still contains the same amount of nodes, thus still resulting in high number of redundant paths being found.

Visibility-PRM [@simeon2000visibilityprm] is a variant of PRM that constructs a sparse roadmap, while discarding some of the nodes as well, resulting in a roadmap more efficient and compact compared to traditional PRM. It does so by introducing a concept of visibility domains. Every domain is defined by a "guard\" that covers a space "visible\" to the guard. No guards are allowed to be visible to each other, thus, they are connected through additional samples called "connectors\". The method in [@schmitzberger2002hppr] extends the original Visibility-PRM by allowing creation of cycles but keeping the roadmap simply connected, making the method suitable for distinct path searching. However, it may not capture all topological classes, especially in environments containing multiple narrow passages. In this scenario a connector node has to be sampled exactly inside a narrow passage, but only after two guard nodes have already been created in specific locations.

Authors in [@simeon2008deformation] modify the original Visibility-PRM by iteratively adding a limited number of cycles, capturing new topological classes, by connecting components of visible sub-roadmap. Even though the method shows promising results, determining a visible sub-roadmap and its separate components gets progressively more computationally expensive in complex environments.

The algorithm in [@zhou2021raptor] was designed for fast trajectory re-planning, but includes the sub-task of finding topologically distinct paths. It modifies Visibility-PRM algorithm to make it computationally efficient, by discarding many generated samples. This method achieves best results in open scenarios, however is very susceptible to initial placement of new guard nodes in scenarios where visibility is limited, which affects both computational speed and functionality.

The method in [@penicka2022quadrotor] tackles minimum-time trajectory planning problem, but also proposes a solution for finding multiple paths with distinct topological classes. The algorithm starts by iteratively searching for the shortest path in a constructed PRM using Dijkstra's. For each path found, a region around the node with smallest clearance is removed from the roadmap. This process is repeated until no new path can be found. To address cases where multiple distinct paths pass through a deleted region, algorithm is called recursively. The limitation of this method is the lack of information required to optimally select a region to remove, failing to find some of the paths as a result. Recursion may also lead to combinatorial explosion, drastically increasing run-time.

The main limitation of existing methods is their inconsistency across different environments, leading to significant variations in their performance, especially in challenging environments that contain multiple narrow passages. CTopPRM is capable of efficiently reducing a dense roadmap, required to accurately represent such environment, by dividing it into clusters. This significantly reduces both number of edges and nodes, while maintaining the same connectivity of free space, as the initial roadmap. This allows it to both effectively and consistently identify a large number of topologically distinct paths, even in challenging environments.

# Problem Statement[]{#sec:problem label="sec:problem"}

The goal of this paper is to tackle the problem of finding multiple topologically distinct paths, i.e., paths between same endpoints going around an obstacle from different sides. By identifying multiple such paths, the robot has greater flexibility when planning its movements. We assume a 3D configuration space $\mathcal{C}$, where each configuration $q=(x,y,z) \in \mathcal{C}$ is the position of the robot. Let $\mathcal{C}_{\mathrm{free}} \subseteq  \mathcal{C}$ denote the set of collision-free configurations. A path $\pi(s)$ is a continuous curve that connects $q_{start} \in \mathcal{C}_{\mathrm{free}}$ and $q_{goal} \in \mathcal{C}_{\mathrm{free}}$, and is denoted as collision-free if $\pi(s) \in \mathcal{C}_{\mathrm{free}}, \forall s \in [0,1]$.

A common definition of topological equivalency is homotopy [@hatcher2002topology], where two continuous functions from one topological space to another are considered equivalent if one can be smoothly deformed into the other. This definition, applied on paths, was summarized in [@simeon2008deformation]. Homotopy of two paths $\pi(s)$ and $\pi'(s)$ in $\mathcal{C}$ is said to exist if there is a continuous map $h:[0,1]\times[0,1] \xrightarrow{} \mathcal{C}_{\mathrm{free}}$ such that $h(s,0) = \pi(s)$, $h(s,1) = \pi'(s)$ for all $s \in [0,1]$, and $h(0,t) = h(0,0)$ and $h(1,t) = h(1,0)$ for all $t \in [0,1]$.

While homotopy is a widely used concept, it has been found to be inadequate for capturing a sufficient number of useful paths in $\mathbb{R}^3$ space. To address this limitation, [@simeon2008deformation] introduced the concept of Visibility Deformation (VD) which captures more useful paths. Unlike homotopy, which preserves the topology of the paths, VD focuses on preserving certain visibility-related properties of the path, such as the ability to evade obstacles, effectively reducing dimensionality of deformation between the paths. However, the approach is still computationally expensive. Therefore, [@zhou2021raptor] proposes an extension to VD called Uniform Visibility Deformation (UVD), which is more efficient.

::: definition
****Definition** 1**. *Two paths $\pi(s)$, $\pi'(s)$ parameterized by $s\in[0,1]$ and satisfying $\pi(0) = \pi'(0)$, $\pi(1) = \pi'(1)$, belong to the same uniform visibility deformation class, if for all s, the line-segment from $\pi(s)$ to $\pi'(s)$ is collision-free.*
:::

In this paper, we tackle the problem of finding a set $\Pi$ of distinct topological paths that belong to different UVD classes, using a combination of motion planning methods, as well as clustering and graph-based search algorithms.

# Clustering Topological PRM[]{#sec:method label="sec:method"}

:::: {#fig:blender .figure latex-placement="htbp"}
  ------------------------------------------------ --------------------------------------------- ---------------------------------------------
    ![image](Novosad2023CTopPRM_figs/alg1.png){width="33%"}     ![image](Novosad2023CTopPRM_figs/alg2.png){width="33%"}   ![image](Novosad2023CTopPRM_figs/alg3.png){width="33%"}
   \(a\) roadmap clustered with initial centroids          \(b\) fully clustered roadmap              \(c\) connections between clusters
    ![image](Novosad2023CTopPRM_figs/alg4.png){width="33%"}     ![image](Novosad2023CTopPRM_figs/alg5.png){width="33%"}   ![image](Novosad2023CTopPRM_figs/alg6.png){width="33%"}
            \(d\) one of the found paths                \(e\) shortening of the found path               \(f\) filtered distinct paths
  ------------------------------------------------ --------------------------------------------- ---------------------------------------------

::: caption
Visualization of individual stages of the algorithm. Generated PRM is first divided into two clusters with $q_{start}$ and $q_{goal}$ as centroids (a). Minimum and maximum connections, marked by green and red line, are compared and new centroids (light yellow in (a)) are iteratively created at one of the maximum connections until roadmap is fully clustered (b). Connections between cluster centroids are found and a low-order, sparse graph (c) is constructed and then searched for distinct paths (d). Each found path is then shortened (e), where red path is shortened into the green. Finally, redundant path are filtered out (f).
:::
::::

The proposed method we named Clustering Topological PRM (CTopPRM) finds distinct topological paths using a hierarchical approach that starts by constructing a dense roadmap using Informed-PRM [@aria2021informedprm]. The nodes in the roadmap are divided into two initial clusters (that are defined by $q_{start}$ and $q_{goal}$), and more clusters are iteratively identified. In each iteration, new cluster centroid is created between two neighbouring clusters. Cluster centroids are then used as vertices of new sparse roadmap, which is then searched for paths with diverse uniform visibility deformation classes. Finally, found paths are shortened and filtered. The algorithm uses Euclidean Signed Distance Field (ESDF) for collision checking. The method is summarized in Algorithm [\[alg:alg1\]](#alg:alg1){reference-type="ref" reference="alg:alg1"} and its visualization is shown in Figure [2](#fig:blender){reference-type="ref" reference="fig:blender"}.

::: algorithm
($V$, $E$), $l$ $\xleftarrow{}$ **Informed-PRM**($q_{start}$, $q_{goal}$) *//* [@aria2021informedprm] $C_V$ $\xleftarrow{}$ {$q_{start}$, $q_{goal}$} can_add $\xleftarrow{}$ true $C_E$ $\xleftarrow{}$**findClusterEdges($C_V$, $E_C$)** $\Pi^d$ $\xleftarrow{}$ **findDistinctPaths**($C_V$, $C_E$, $\kappa_p\cdot l$) $\Pi$ $\xleftarrow{}$ **filterPaths**($\Pi^d$)
:::

Algorithm [\[alg:alg1\]](#alg:alg1){reference-type="ref" reference="alg:alg1"} starts with **Informed-PRM** constructing a graph ($V$, $E$) with vertices $V$ and edges $E$. This graph is then divided into clusters by **clusterGraph** method, transforming the roadmap into a forest ($V$, $E_C$). Method **addCentroids** defines a node as a new cluster centroid. Roadmap is then clustered again. This process is iteratively repeated until a suitable new centroid candidate was not found, or a predefined maximum number of clusters M is reached resulting in a fully clustered roadmap shown in Figure [2](#fig:blender){reference-type="ref" reference="fig:blender"}(b). Then, a low-order graph is created with cluster centroids as vertices. Edges connecting them are found using the **findClusterEdges** method, which transforms saved shortest paths between each pair of neighbouring clusters into edges, finalizing the construction of the low-order graph, shown in Figure [2](#fig:blender){reference-type="ref" reference="fig:blender"}(c). Method **findDistinctPaths** searches this graph for a set of distinct paths $\Pi^d$, which are then shortened, akin to the approach in [@zhou2021raptor] and [@penicka2022quadrotor], and filtered by method **filterPaths**. Each part of the CTopPRM algorithm is explained in more detail in the following subsections.

## Dense Probabilistic Roadmap Construction {#subsection:PRM}

The goal of this step of the CTopPRM algorithm is to densely represent free-space $\mathcal{C}_{\mathrm{free}}$ which is realized using Informed-PRM [@aria2021informedprm]. Each vertex is connected to its k-nearest neighbours using a straight-line, if possible. The shortest path in the constructed roadmap is then found using Dijkstra; let $l$ denote its length.

## Graph clustering {#subsection:clustering}

The **clusterGraph** method described in Algorithm [\[alg:alg2\]](#alg:alg2){reference-type="ref" reference="alg:alg2"} divides roadmap into clusters with shortest-path tree [@dijkstra1959note] structure, with each cluster centroid being root of each shortest-path tree. All clusters together form a shortest-path forest [@dial1969SPforest]. In a shortest-path forest, each tree represents the shortest paths from all nodes to their closest root.

::: algorithm
heap $\xleftarrow{} V\cup C_V$
:::

The division of the roadmap into clusters is implemented using a min-heap, making the time complexity $\mathcal{O}(E \log V)$. The initial cluster centroids are $q_{start}$ and $q_{goal}$. Each cluster is expanded from its centroid, creating connections to minimize the total cost of a path from each vertex to the nearest cluster centroid, summarized by Lines [\[alg2:begin\]](#alg2:begin){reference-type="ref" reference="alg2:begin"}-[\[alg2:end\]](#alg2:end){reference-type="ref" reference="alg2:end"} of Algorithm [\[alg:alg2\]](#alg:alg2){reference-type="ref" reference="alg:alg2"}. If two neighbouring vertices belong to different clusters, total cost of path connecting two cluster centroids over these two vertices is calculated, as shown in Line [\[alg2:cost\]](#alg2:cost){reference-type="ref" reference="alg2:cost"}. For each pair of neighbouring clusters i and j, the method maintains paths $P_{\mathrm{min}}^{ij}$ and $P_{\mathrm{max}}^{ij}$ that represent the shortest and the longest paths connecting the two clusters, respectively, with a prospect they might represent different UVD classes. Edges that do not belong to either cluster, but are a part of these paths are called minimum and maximum cluster connection, and they are crucial for selecting new cluster centroids in the steps to follow. An example of these connections is shown in Figure [2](#fig:blender){reference-type="ref" reference="fig:blender"}(a), where green line represents minimum and red line represents maximum cluster connection.

## Adding new centroids {#subsection:centroid}

The motivation behind division of PRM into multiple clusters is to create an easily searchable graph with cluster centroids as vertices which will have significantly less vertices than the dense roadmap. To capture all UVD classes, while minimizing order of the graph, vertices have to be placed methodically. CTopPRM's approach to create new cluster centroids is depicted in Algorithm [\[alg:alg3\]](#alg:alg3){reference-type="ref" reference="alg:alg3"}.

It starts by comparing connections $P_{\mathrm{min}}^{ij}$ and $P_{\mathrm{max}}^{ij}$ for each pair of connected clusters. The method **Deformable** in Line [\[alg3:deformable\]](#alg3:deformable){reference-type="ref" reference="alg3:deformable"} of Algorithm [\[alg:alg3\]](#alg:alg3){reference-type="ref" reference="alg:alg3"} then checks if these two paths belong to the same UVD class. Each path is discretized to $n = \lceil P_{\mathrm{max}}^{ij}.length / \Delta d \rceil$ steps. Each line-segment between the points $P_{\mathrm{max}}^{ij}[k]$ and $P_{\mathrm{min}}^{ij}[k]$, $k=0,\ldots, n$, is tested for collisions with the resolution $\Delta d$. If they are not deformable, creating a new centroid at the border of these two clusters is beneficial in capturing more UVD classes, as there are two distinct paths connecting two existing cluster centroids. The ratio of their lengths is then calculated and saved. The connection with the highest ratio is selected and one of the two neighbouring nodes belonging to its maximum connection (endpoints of the red line in Fig. [2](#fig:blender){reference-type="ref" reference="fig:blender"}(a)), is determined as a new centroid (light yellow in Fig. [2](#fig:blender){reference-type="ref" reference="fig:blender"}(a)). By adding a new centroid at the maximum connection, a new topologically unique path between given cluster centroids is created, allowing detour through the newly defined centroid, usually resulting in at least one new path between start and goal nodes. If $P_{\mathrm{min}}^{ij}$ and $P_{\mathrm{max}}^{ij}$ are deformable into each other for all neighbouring clusters, thus a suitable new candidate for the centroid cannot be identified, then the *can_add* variable remains set to *false*, indicating termination of iteration in Alg. [\[alg:alg1\]](#alg:alg1){reference-type="ref" reference="alg:alg1"}.

::: algorithm
can_add $\xleftarrow{}$ false ratio $\xleftarrow{} \emptyset$ new_centroid $\xleftarrow{}$ **getCentroid**(**max**(ratio)) $C_V \xleftarrow{} C_V \cup$ new_centroid
:::

## Path finding and filtering {#subsection:filtering}

The method **findDistinctPaths** in Line [\[alg1:find\]](#alg1:find){reference-type="ref" reference="alg1:find"} of Algorithm [\[alg:alg1\]](#alg:alg1){reference-type="ref" reference="alg:alg1"} searches the graph using Depth-first search (DFS) algorithm with visited list similar to [@rosman2017dfs]. In this depth-limited depth-first search, the expansion on the actual node is terminated if the current path length is greater than $\kappa_{p}$ times the length of best solution $l$.

To accommodate future applications, e.g., for planning high-speed UAV trajectories along the paths, CTopPRM uses a series of methods, included in **filterPaths** function in Line [\[alg1:filter\]](#alg1:filter){reference-type="ref" reference="alg1:filter"} of Algorithm [\[alg:alg1\]](#alg:alg1){reference-type="ref" reference="alg:alg1"}, to augment and filter found paths. Method similar to shortening in [@zhou2021raptor] and [@penicka2022quadrotor] is used first to shorten found paths in forward and backward pass. Any shortened paths longer than a threshold defined as length of the shortest found path multiplied by the parameter $\kappa_{s}$ are then pruned away. Doing this filters out any paths that include sub-optimal movement, e.g. looping around obstacles. Finally, one last UVD equivalency check is performed on shortened paths to filter out any paths belonging to the same UVD class. The final output of the CTopPRM (Algorithm [\[alg:alg1\]](#alg:alg1){reference-type="ref" reference="alg:alg1"}) is a set of paths representing different UVD classes.

## Discussion {#subsection:filtering}

The CTopPRM uses the probabilistically complete Informed-PRM [@aria2021informedprm] that, for an infinite number of samples, ensures finding a path between start and goal if it exists. Thus, it can capture for an infinite number of samples all distinct topological paths. At the same time, if the number of cluster centroids grows, the probability of finding all distinct paths approaches certainty, as eventually all PRM samples would be searched by the DFS. Yet, for practical purposes, a more efficient approach is favored in the CTopPRM over probabilistic completeness due to application constraints.

# Results[]{#sec:results label="sec:results"}

:::: {#fig:scenarios .figure latex-placement="ht"}
:::: {#fig:windows .figure}
::: caption
windows 1-3-1 scenario (from [@vonasek2019guidingpaths])
:::
::::

![poles](Novosad2023CTopPRM_figs/forestb.png){#fig:poles width="\\textwidth"}

:::: {#fig:building .figure}
![image](Novosad2023CTopPRM_figs/side_view.png){width="\\textwidth"} ![image](Novosad2023CTopPRM_figs/top_view.png){width="\\textwidth"}

::: caption
building
:::
::::

::: caption
Maps of the environments used for evaluating CTopPRM and related algorithms with paths found by CTopPRM.
:::
::::

The performance of the CTopPRM is evaluated in three different environments shown in Figure [6](#fig:scenarios){reference-type="ref" reference="fig:scenarios"}. The purpose of having multiple thematically different environments is to evaluate robustness of our and related methods. The most important evaluation metric is the number of UVD classes each method is able to find in form of a path within such a UVD class. We also consider computational time and quality of found paths, represented by their respective lengths.

::: {#tab:parameters}
+:-----------:+-------------:+:---------:+:---------:+:---------:+
|             |              | windows   | poles     | building  |
+-------------+--------------+-----------+-----------+-----------+
|             | map size     | 27x26.7x8 | 10x10x2.8 | 30x20x6.3 |
+-------------+--------------+-----------+-----------+-----------+
| All methods | clearance    | 0.3       | 0.3       | 0.2       |
|             +--------------+-----------+-----------+-----------+
|             | $\Delta d$   | 0.1       | 0.2       | 0.2       |
|             +--------------+-----------+-----------+-----------+
|             | PRM samples  | 500       | 300       | 1000      |
|             +--------------+-----------+-----------+-----------+
|             | $\kappa_{s}$ | 1.5       | 1.2       | 1.5       |
+-------------+--------------+-----------+-----------+-----------+
| CTopPRM     | M            | 9         | 20        | 20        |
|             +--------------+-----------+-----------+-----------+
|             | $\kappa_{p}$ | 1.8       | 1.6       | 1.8       |
|             +--------------+-----------+-----------+-----------+
|             | k            | 14        | 14        | 14        |
+-------------+--------------+-----------+-----------+-----------+

: Algorithm parameters & map size
:::

CTopPRM is implemented in C++, and experiments are run on AMD Ryzen 7 6800HS CPU. Values of parameters used in the test is shown in Table [1](#tab:parameters){reference-type="ref" reference="tab:parameters"}.

The computational time of all methods examined in this study is primarily influenced by three key parameters: $\Delta d$ --- the resolution of collision detection, the number of samples used to build the dense roadmap and k --- the number of neighbours each node is connected to during the construction of the roadmap. In all conducted experiments, k was set to 14, a value determined experimentally to achieve a balance between computational time and adequate coverage of the free space. The size of the spherical robot is specified by the clearance parameter. CTopPRM algorithm includes two more parameters: M (maximum number of clusters) and $\kappa_{p}$ (DFS termination condition). Both parameters affect the trade-off in performance of the method, reducing computational time, but at a cost of quality and quantity of found paths.

We evaluate the performance of CTopPRM by comparing it with three other methods that tackle the same challenge. These include the method we call RAPTOR from [@zhou2021raptor], which solves the sub-task of identifying distinct topological paths, the Distinct Path Search algorithm proposed in [@penicka2022quadrotor], referred to as B. spheres, and an approach based on [@simeon2008deformation] called P-D-PRM, adapted slightly to ensure reasonable run-time.

## Windows environment {#subsection:windows}

:::: table*
::: tabular
r\|c\|c\|ccc\|c\|ccc\|c\|ccc\|c\|ccc & & & & &\
env. & **GT** & c.t.\[ms\] & $\pi_1$\[%\] & $\pi_2$\[%\] & $\pi_3$\[%\] & c.t.\[ms\] & $\pi_1$\[%\] & $\pi_2$\[%\] & $\pi_3$\[%\] & c.t.\[ms\] & $\pi_1$\[%\] & $\pi_2$\[%\] & $\pi_3$\[%\] & c.t.\[ms\] & $\pi_1$\[%\] & $\pi_2$\[%\] & $\pi_3$\[%\]\
-2-0 &2 &41 &**100** &**100** &- &75 &80 &64 &- &**36** &99 &94 &- &39 &54 &46 &-\
1-2-0 &2 &54 &**99** &**100** &- &65 &51 &42 &- &55 &89 &94 &- &**52** &35 &24 &-\
1-2-1 &2 &51 &**99** &**99** &- &**35** &4 &7 &- &51 &95 &58 &- &43 &9 &8 &-\
1s-2-1s &2 &48 &**98** &**97** &- &42 &40 &26 &- &86 &87 &91 &- &**40** &42 &9 &-\
-3-0 &3 &70 &94 &**100** &**96** &148 &94 &**100** &92 &53 &**98** &98 &93 &**49** &86 &98 &81\
1-3-0 &3 &51 &**100** &**71** &**70** &101 &**100** &0 &0 &41 &95 &2 &3 &**38** &**100** &0 &0\
1-3-1 &3 &47 &**100** &**89** &**89** &43 &41 &12 &10 &51 &90 &78 &52 &**41** &41 &9 &5\
1s-3-1s &3 &54 &**100** &**99** &**81** &46 &86 &16 &14 &85 &88 &89 &68 &**21** &89 &9 &7\
:::
::::

The first set of experiments is performed in environments called windows which contain a small number of narrow passages (windows) placed on one to three parallel walls, making maximum number of distinct UVD classes, ground truth (GT), easily determinable. Name of the maps in Table [\[tab:windows\]](#tab:windows){reference-type="ref" reference="tab:windows"} indicates number of windows on each wall. For example, scenario 1-3-1 shown in Figure [3](#fig:windows){reference-type="ref" reference="fig:windows"} contains one window on the first wall, three on the second and one on the third. Zero indicates a given wall is missing and 's' for 'side' indicates that a specific window is not in the middle of the wall. These scenarios are tested in $\mathbb{R}^2$ space with a circular robot. Each algorithm is evaluated on 100 runs in every scenario.

Figure [7](#fig:graphs){reference-type="ref" reference="fig:graphs"} presents the performance comparison of all algorithms in the 1-3-1 scenario. Our method outperformed other methods by finding all three distinct paths more reliably in this particular scenario. We report computational time and success rate of each algorithm in finding every single distinct path that exists in a given scenario.

The results of this experiment are shown in Table [\[tab:windows\]](#tab:windows){reference-type="ref" reference="tab:windows"}. They indicate that CTopPRM algorithm manages to find all but one path, across all testing scenarios, with highest success rate. Additionally, CTopPRM finds most paths with a success rate close to 100 %, with lowest success rate being 70 %, proving its effectiveness and reliability, both absolutely and relatively to other methods.

:::: {#fig:graphs .figure latex-placement="!htb"}
::: caption
Number of paths found in 1-3-1 scenario with highlighted ground-truth (GT) (Fig. [3](#fig:windows){reference-type="ref" reference="fig:windows"}).
:::
::::

All the methods performed better in simpler scenarios where only one window is required to be passed (0-2-0 and 0-3-0), and their performance deteriorates as the number of narrow passages increases. Visibility-based methods P-D-PRM and RAPTOR demonstrate the most significant decline in performance, with success rates dropping below 10% for multiple paths in different scenarios.

Interesting results arise from scenario 1-3-0 where P-D-PRM and RAPTOR find the shortest path $\pi_1$ in every run, due to $q_{goal}$ being visible from $q_{start}$, but fail to ever identify any of the remaining paths $\pi_2$ and $\pi_3$. Due to the layout of the map, we can assume that Visibility-PRM blocks itself off by placing a guard node in an unfavorable position. Additionally, B.spheres method, which otherwise shows more competitive results, is also able to detect these paths with less than 10 % success rate. Contrarily, CTopPRM detects both paths in 70 % of runs. While this result significantly surpasses other methods, it is the most challenging map for the CTopPRM. This is primarily due to the CTopPRM's limitation in capturing UVD classes not included in the initial PRM, which depends on the number of random samples. This weakness is magnified in this test case where closely spaced walls and large free space result in fewer nodes being generated in critical areas. Moreover, for the tests in Table [\[tab:windows\]](#tab:windows){reference-type="ref" reference="tab:windows"}, the algorithm was always terminated only if all connections between clusters were deformable. Therefore, Table [\[tab:windows\]](#tab:windows){reference-type="ref" reference="tab:windows"} accurately represents the probability of CTopPRM failing to capture a UVD class. Despite this limitation, CTopPRM clearly outperforms other methods, showcasing its robustness in challenging scenarios.

The run-time of all methods depends not only on the size of the input roadmap, but also on number of paths identified, as most of computational time is taken by filtering process described in Section [4.5](#subsection:filtering){reference-type="ref" reference="subsection:filtering"}. This is why scenario 0-3-0 is interesting to us, since all tested methods identify similar amount of paths.

:::: {#fig:samples .figure latex-placement="!htb"}
![](Novosad2023CTopPRM_figs/samples_comparison.png){width="\\columnwidth"}

::: caption
The performance with the increasing number of random samples.
:::
::::

As already mentioned, the performance of the methods depends on the number of random samples used to create the initial roadmap. We show the performance with the increasing number of random samples in Figure [8](#fig:samples){reference-type="ref" reference="fig:samples"}. They indicate that with the lower number of samples, the methods B. spheres and CTopPRM manage to find more paths, but are clearly slower than both P-D-PRM and RAPTOR. Additionally, it is important to note that P-D-PRM finds significantly fewer paths than the other methods, because it consists of two phases, which have to share the total amount of samples. With a growing number of samples, the performance of all algorithms in terms of the number of paths found converges towards three, which is the ground truth in this scenario. However, unlike B. spheres and CTopPRM, which record just a minor increase in computational time, both P-D-PRM and RAPTOR become significantly slower.

Overall, CTopPRM shows computational speed competitive with other related methods, while clearly outclassing them in terms of path detection success rate. Therefore, CTopPRM proves to be the most efficient and effective in scenarios with smaller number of distinct UVD classes.

## Complex environments {#subsection:complex}

:::: table*
::: tabular
r\|c\|cccc\|cccc\|cccc\|cccc & & & & &\
map & $n$ & c.t.\[ms\] & best & average & n-shortest & c.t.\[ms\] & best & average & n-shortest & c.t.\[ms\] & best & average & n-shortest & c.t.\[ms\] & best & average & n-shortest\
&400 &19 &**19** &**15.16**$\pm$`<!-- -->`{=html}3.76 &7.83 &14 &**19** &13.71$\pm$`<!-- -->`{=html}3.03 &**7.75** &**10** &11 &7.47$\pm$`<!-- -->`{=html}1.48 &7.87 &55 &**19** &14.11$\pm$`<!-- -->`{=html}1.82 &7.80\
poles&400 &16 &**6** &**4.80**$\pm$`<!-- -->`{=html}0.96 &**7.79** &20 &5 &3.61$\pm$`<!-- -->`{=html}0.94 &N/A &**14** &**6** &3.42$\pm$`<!-- -->`{=html}1.05 &N/A &135 &**6** &4.42$\pm$`<!-- -->`{=html}1.08 &**7.79**\
&400 &13 &**11** &**7.85**$\pm$`<!-- -->`{=html}1.71 &**7.52** &**7** &9 &7.28$\pm$`<!-- -->`{=html}1.44 &7.54 &13 &8 &4.06$\pm$`<!-- -->`{=html}1.08 &7.60 &27 &8 &7.18$\pm$`<!-- -->`{=html}0.84 &**7.52**\
&300 &142 &**25** &**7.78**$\pm$`<!-- -->`{=html}4.43 &**39.49** &**29** &2 &0.41$\pm$`<!-- -->`{=html}0.58 &N/A &93 &7 &3.24$\pm$`<!-- -->`{=html}1.18 &46.95 &39 &1 &0.16$\pm$`<!-- -->`{=html}0.37 &N/A\
building&300 &151 &**36** &**8.74**$\pm$`<!-- -->`{=html}5.79 &**35.93** &**21** &1 &0.01$\pm$`<!-- -->`{=html}0.10 &N/A &114 &10 &2.85$\pm$`<!-- -->`{=html}2.02 &N/A &35 &0 &0.00$\pm$`<!-- -->`{=html}0.00 &N/A\
&300 &124 &**11** &**4.77**$\pm$`<!-- -->`{=html}1.74 &**33.16** &**29** &1 &0.06$\pm$`<!-- -->`{=html}0.24 &N/A &122 &7 &2.26$\pm$`<!-- -->`{=html}1.17 &N/A &42 &1 &0.02$\pm$`<!-- -->`{=html}0.14 &N/A\
:::
::::

The second set of experiments was conducted in complex environments, containing a high number of distinct UVD classes. The first, called "poles\" and depicted in Figure [4](#fig:poles){reference-type="ref" reference="fig:poles"}, resembles a small forest-like area, while the second, shown in Figure [5](#fig:building){reference-type="ref" reference="fig:building"} and called "building\", requires a robot to traverse a closed, multi-level building area through doors and windows. For each of these environments, we tested the performance of the methods in three different scenarios with different start and goal configurations ($q_{start}$ and $q_{goal}$). Each method was tested in 100 runs in each scenario. The poles scenarios are tested in $\mathbb{R}^2$ space with a circular robot and building scenarios are tested in $\mathbb{R}^3$ space with a spherical robot.

Table [\[tab:all\]](#tab:all){reference-type="ref" reference="tab:all"} summarizes performance of the methods in terms of computational time, the quantity of found paths represented by the highest number of paths found in a single run (best) and average number of found paths across all 100 runs. The quality of paths is evaluated as an average length of n-shortest paths found over all 100 runs, where $n$ is indicated in the table. This metric is supposed to show if a method is able to consistently find $k$ shortest paths in each scenario.

The results show that CTopPRM performs the best in terms of quantity of paths found, identifying the most paths in a single run in every scenario, as well as significantly outscoring other methods in average number of paths found in all scenarios. Additionally, CTopPRM also outperforms other methods in terms of quality of found paths in all but one scenario in poles environment, where it records a score just 1% worse than RAPTOR. CTopPRM is also the only method to find at least $n$ paths across 100 runs in every single scenario. Failure to do so is denoted by N/A in Table [\[tab:all\]](#tab:all){reference-type="ref" reference="tab:all"}.

P-D-PRM and RAPTOR achieve results comparable to CTopPRM in poles environment. Yet, they fail to identify a single path in majority of runs in building environment. P-D-PRM is even unable to detect a single path across all 100 runs for a whole scenario. This is caused by the increased visibility in poles environment, allowing long connections for Visibility-PRM based methods. Contrarily, building environment consists of multiple narrow passages, which was shown in Section [5.1](#subsection:windows){reference-type="ref" reference="subsection:windows"} to be unfavourable. CTopPRM delivers consistent results in all environments, verifying its robustness.

The distribution of CTopPRM's computational time was studied in the poles environment. Experimental results indicate that Informed-PRM's construction takes 6.31 ms, clustering lasts 1.72 ms, path search is 0.09 ms, and path filtering 6.23 ms. Path searching and filtering process exhibit a significant standard deviation (0.09 ms and 2.62 ms, respectively), influenced by the quantity of discovered paths.

In overall, CTopPRM algorithm outperformed other methods in vast majority of scenarios in computational time, quality and quantity of found paths. It also has the best trade-off between computational time and number of paths found.

# Conclusions[]{#sec:conclusion label="sec:conclusion"}

This paper introduced a new sampling-based method named CTopPRM for finding multiple paths with distinct UVD classes in cluttered environments. The CTopPRM clusters initially sampled dense roadmap in order to efficiently simplify the search of multiple distinct paths. Through testing in a variety of environments, we demonstrated that CTopPRM is both efficient and robust. In majority of test cases, it surpassed other related methods in number of found distinct paths, and their length, during similar computational time. We improved the average number of topological classes detected within the same run-time by 30 - 300 % , depending on the scenario Additionally , the CTopPRM allows controlling the balance between computational time , quantity and quality of found paths , making it highly adaptable for online planning As future work , we aim to extend CTopPRM to enable fast trajectory re - planning , and to deploy it online on unmanned aerial vehicles ( UAVs ) to test high - speed flight in partially unknown environments 

[^1]: Manuscript received: May 25, 2023; Revised August 8, 2023; Accepted September 6, 2023.

[^2]: This paper was recommended for publication by Editor Chao-Bo Yan upon evaluation of the Associate Editor and Reviewers' comments.

[^3]: The authors are with the Multi-robot Systems Group, Faculty of Electrical Engineering, Czech Technical University in Prague, Czech Republic (<http://mrs.felk.cvut.cz/>). This work has been supported by the Czech Science Foundation (GAČR) under research project No. 22-24425S, by European Union's Horizon 2020 research and innovation programme AERIAL-CORE under grant agreement no. 871479, and by CTU grant no SGS23/177/OHK3/3T/13.

[^4]: Digital Object Identifier (DOI): 10.1109/LRA.2023.3315539.
