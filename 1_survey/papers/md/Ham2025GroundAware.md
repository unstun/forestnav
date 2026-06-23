---
citation_key: Ham2025GroundAware
arxiv_id: 2509.04950
arxiv_url: https://arxiv.org/abs/2509.04950
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:26:11Z
origin: ai+web
reviewed: false
---

# Introduction

Research on the design of Unmanned Ground Vehicles (UGVs)[@park2012optimal; @tang2023structure] and the locomotion capabilities of legged robots [@kim2019highly; @grandia2023perceptive; @kang2024external] has demonstrated significant advantages over conventional wheeled platforms[@biswal2021development]. Rather than merely avoiding terrain obstacles, these robots are capable of directly traversing them. Typical examples include locomotion within confined spaces such as pipes [@kim2024development], as well as overcoming complex obstacles such as high structures, low barriers, and narrow passages [@zhuang2023robot]. The maneuverability of these robots enables reconnaissance and rescue operations in environments that are challenging for human access, such as collapsed buildings and mountainous terrain.

Efficient path planning is essential for robots to operate effectively in diverse environments. Despite significant advancements in robotic hardware and control methods, limited battery capacity continues to constrain the operational time of robots. Therefore, generating an optimal path is essential for minimizing travel time. This, in turn, increases the distance that the robot can reach within the limited battery capacity.

Due to limitations in size and power consumption, mobile robots must operate with low computational complexity and memory usage to be applicable in the real-world. The processing of large-scale data for terrain analysis and optimal path computation often requires high-performance hardware, which poses challenges for deployment on systems with limited computational resources.

To address these challenges, we propose a hybrid path planning method that combines the A\* algorithm with an octree-based spatial representation. A\* is an algorithm that guarantees optimality under an admissible heuristic, while the octree is a data structure that efficiently represents three-dimensional (3D) space by recursively subdividing it into eight subregions. By integrating these two approaches, the proposed method significantly reduces the search time and memory usage of the A\* algorithm. Unlike drones, which can freely move in three-dimensional space, legged robots and UGVs are constrained to remain in contact with the ground or can only hover briefly at low altitudes. As a result, their navigable paths are more restricted compared to aerial vehicles. To account for these characteristics, we introduce a height-based penalty into the A\* algorithm's cost function, encouraging ground-level path generation. This results in a path planning method optimized for ground vehicles.

Section [2](#sRELATEDWORKS){reference-type="ref" reference="sRELATEDWORKS"} provides an overview of related works. Section [3](#sPATHPLANNING){reference-type="ref" reference="sPATHPLANNING"} describes a grid map compression method using an octree structure and introduces an optimal path planning approach based on A\* for ground vehicles that leverages obstacles, culminating in the proposed Octree-A\* hybrid method. Section [4](#sBENCHMARK){reference-type="ref" reference="sBENCHMARK"}e presents a performance comparison between the standard A\* algorithm and the proposed hybrid algorithm. Finally, Section [5](#sCONCLUSION){reference-type="ref" reference="sCONCLUSION"} concludes the study.

# Related Works {#sRELATEDWORKS}

Various approaches to path planning have been extensively studied. Dijkstra's algorithm can find the optimal path but suffers from high computational time. To address this limitation, the A\* algorithm was introduced to reduce computation time. However, if the heuristic function used in A is not admissible, the optimality of the resulting path cannot be guaranteed[@candra2020dijkstra]. An improved A\* algorithm, which restricts the search to obstacle intersections along a straight line between the start and goal nodes, reduces the average path length by 3%. Nevertheless, the computation time increases by a factor of four, limiting its applicability in real-time environments[@ju2020path]. While A\* guarantees optimality under an admissible heuristic, it incurs high computational costs in high-dimensional and unstructured environments.

Rapidly-exploring Random Tree Star (RRT\*) is a sampling-based algorithm that incrementally builds a search tree by randomly sampling the space. It addresses the limitation of the original RRT algorithm, which does not guarantee an optimal solution, and is suitable for use in high-dimensional environments [@karaman2011sampling; @solovey2020revisiting]. Despite its asymptotic optimality as the number of samples increases, RRT\* often yields suboptimal paths in practice due to limited computational resources. In addition, its performance degrades in environments with narrow passages, and its non-deterministic nature requires further consideration of reliability [@braun2019comparison; @belaid2022narrow]. Recent modifications of RRT\* [@huang2024adaptive; @tu2024improved] showed improved success rates in narrow passage scenarios, addressing limitations of the original method. However, these approaches did not guarantee complete search success.

Although numerous studies have been conducted on path planning in 3D space, most of them focus on underwater environments [@yan2022three; @li2023three] or unmanned aerial vehicles (UAVs) [@kiani2021adapted]. In contrast, robots such as quadrupeds and UGVs typically perform path planning on two-dimensional (2D) surfaces [@zhang2021efficient]. Both 2D and 3D path planning commonly utilize algorithms such as RRT and A\*.

In many studies [@xu2025path; @liu2024safe], path planning is performed under the assumption that the terrain is continuous, where the robot must either navigate over traversable terrain or avoid untraversable obstacles, often by jumping. For instance, the study by [@zhe2019path] employs an ADFA\* algorithm using a simple grid map, focusing solely on 2D motion.

Other works [@li2022quadruped; @li2020grid] construct grid maps using 3D laser radar data and address the challenge of dynamic obstacles in 2D space. Similarly, studies such as [@zhang2021efficient; @liu2020research] demonstrate locomotion involving stepping over obstacles or navigating complex 2D terrain. In [@hoeller2024anymal], terrain information is captured using a scan-dot representation to enable local path planning.

:::: algorithm
::: algorithmic
$(x_i, y_i, z_i)$, $\mathcal{N}_{R}$, $s$ $\mathcal{N}_{L}$, $(x, y, z) \in \mathcal{N}_{L}$ $(x,y,z) \gets (x_i, y_i, z_i)$ $s \gets s / 2$ $\mathcal{i}$$\gets \textbf{ComputeChildIndex}(x,y,z,s)$ $\mathcal{N} \gets \mathcal{N}_{\text{child}}[i]$ $(x, y, z) \gets (x \bmod s,\ y \bmod s,\ z \bmod s)$ $\mathcal{N}_L \gets  \mathcal{N}$
:::
::::

# Path Planning {#sPATHPLANNING}

In this Section, we introduce the Octree-A\* hybrid path planning method. A uniform grid map is first compressed using an octree structure, and then a cost function of A\* is proposed to constrain the path to be generated only over valid surface regions, including traversable obstacles. Finally, the integration of the octree representation with the A\* algorithm is presented.

## Octree Structure

The octree is primarily a compression algorithm applied to densely sampled surface geometry and has the advantage of being lossless [@schnabel2006octree]. It is a hierarchical tree-based data structure for partitioning 3D space, where each node is recursively subdivided into eight cubic child nodes starting from a root node representing a larger region.

Construction of nodes in the octree follows the procedure described below. First, the grid map is uniformly divided into eight nodes. Each node is then checked for the presence of obstacles. If any obstacle is present within a node, it is further subdivided into eight child nodes. If no obstacle is present---i.e.,the node contains only empty space, start, or goal---it is not further subdivided. A leaf node represents a terminal region in the space that is no longer subdivided. Each newly generated child node is recursively processed until it becomes a leaf node or no obstacles are present within the node. If a child node is identical to a uniform node, it is not further subdivided.

:::: algorithm
::: algorithmic
$\mathcal{N}_{L}$, $(x, y, z) \in \mathcal{N}_{L}$ $\mathcal{O}$ $\mathcal{O} \gets \emptyset$ $ds \gets s/2 \in \mathcal{N}_{L}$ $\mathcal{M}$ $\gets \textbf{ComputeAdjacents}(x,y,z,ds+r)$ $\mathcal{N}$ $\gets \textbf{Algorithm~\ref{aLeafNode}}(m)$ $\mathcal{O} \gets \mathcal{O} \cup \{\mathcal{N}\}$
:::
::::

## A\* Algorithm

:::: {#fAstar .figure latex-placement="t!"}
::: caption
Results of the modified 3D A\* algorithm executed on a uniform grid, showing the generated path. Gray represents obstacles, red and black indicate the planned path, yellow denotes the start node, and green denotes the goal node.
:::
::::

To ensure successful path planning and produce shorter trajectories, A\* algorithm was utilized. Unlike UAVs and manipulators, ground vehicles are subject to the constraint of moving on the ground surface. The modified cost function applies the above constraint as a soft constraint within the node exploration process. The cost function is defined as follows: $$\begin{equation}
    \min_{n \in N} \quad g(n) + h(n) + \alpha r(n)
    \label{eCostfunction}
\end{equation}$$ where $N$ is the set of neighbor nodes, $n \in N$ is a candidate node, $g(n)$ is the accumulated cost from the start node to node $n$, and $h(n)$ is the heuristic cost defined as the Manhattan distance between node $n$ and the goal node, $\alpha$ is positive scalar penalty weight, and $r(n)$ is a penalty term defined as the vertical distance from the center of node $n$ to the nearest surface. The penalty term is designed to achieve two objectives. First, it increases the cost of nodes that are distant from the surface, discouraging the selection of nodes that are not on the ground. Second, it prevents path generation toward heights that are beyond the robot's traversable capability, effectively discouraging upward movement from the current position when such movement is infeasible.

## Octree-A\* Algorithm

::: {#tBenchmark}
+:-----------:+:-----:+:----:+:-----:+:-----:+:----:+
|             | S1    | S2   | S1    | S2    |      |
+-------------+-------+------+-------+-------+------+
|             | A\*          | Octree-A\*    | Unit |
+-------------+-------+------+-------+-------+------+
| Path length | 121.5 | 125  | 122   | 124   | m    |
+-------------+-------+------+-------+-------+------+
| Comp. time  | 927.7 | 7495 | 68.4  | 661   | ms   |
+-------------+-------+------+-------+-------+------+
| Memory      | 8192  | 8192 | 367.4 | 608.7 | kB   |
+-------------+-------+------+-------+-------+------+
|             |       |      |       |       |      |
+-------------+-------+------+-------+-------+------+

: Comparison of A\* and Octree-A\* performance in two benchmark scenarios.
:::

To integrate the octree with the A\*, several challenges must be addressed. In contrast to uniform grids, leaf nodes in an octree have irregular neighbor configurations, where both the number and size of neighboring nodes may differ. Therefore, applying the A\* to octree-based grid, it is essential to identify both the neighboring nodes and their corresponding sizes.

An octree node $\mathcal{N}$ consists of a leaf indicator, a state, and a set of child nodes. The state can encode whether the node is empty, occupied, or corresponds to a start or goal. The pseudocode of the method for finding the leaf node $\mathcal{N}_{L}$ that contains a given 3D coordinate $(x_i, y_i, z_i)$ is described in Algorithm [\[aLeafNode\]](#aLeafNode){reference-type="ref" reference="aLeafNode"}. The procedure recursively traverses the octree beginning at the root node $\mathcal{N}_R$ with side length $s$. If the node is not a leaf node, update $s$ to represent the side length of its child nodes. Among the eight child nodes, identify the index $\mathcal{i}$ such that the coordinate $(x, y, z)$ lies within child node $\mathcal{N}_{\text{child}}[i]$, and update node accordingly. Then, update $(x, y, z)$ to the center coordinates within the selected child node using modulo operation. The algorithm returns the leaf node when a leaf node is reached.

Algorithm [\[aGetNeighbors\]](#aGetNeighbors){reference-type="ref" reference="aGetNeighbors"} presents the procedure for identifying neighbor leaf nodes of a given leaf node. The set $\mathcal{O}$ is initialized to store valid neighboring leaf nodes, and the variable $ds$ is assigned half the side length of the input leaf node. The ComputeAdjacents function computes the nearest coordinates in each feasible direction using the center coordinate of the current leaf node, $ds$, and the minimum grid resolution $r$. The resulting coordinates are stored in the set $\mathcal{M}$. For each element in $\mathcal{M}$, Algorithm [\[aLeafNode\]](#aLeafNode){reference-type="ref" reference="aLeafNode"} is used to identify the leaf node that contains the corresponding coordinate. Each leaf node is checked using the isValid function, and only those without obstacles are pushed into the $\mathcal{O}$. As a result, $\mathcal{O}$ contains only the coordinates of candidate nodes, which can be directly used in the A\*.

:::: {#fOctree .figure latex-placement="t!"}
::: caption
Results of the octree applied to each scenario. Red outlines indicate the edges of leaf nodes, while gray, yellow, and green follow the same color scheme as in Fig. [1](#fAstar){reference-type="ref" reference="fAstar"}.
:::
::::

:::: {#fOcastar .figure latex-placement="t!"}
::: caption
Illustration of the Octree-A\*. The color scheme is identical to that used in Fig. [1](#fAstar){reference-type="ref" reference="fAstar"}.
:::
::::

# Benchmark {#sBENCHMARK}

Simulations were conducted on Intel i7-9700 CPU running Ubuntu 22.04 operating system. The algorithms were implemented in C++ and executed using a compiler compliant with the C++17 standard. Two simulation scenarios were conducted. The first scenario represents a condition where an optimal path can be generated without leveraging obstacles. In contrast, the second scenario requires obstacle leveraging---i.e., the path can only be generated by traversing over obstacles. Each uniform grid cell has a size of 0.5m$\times$`<!-- -->`{=html}0.5m$\times$`<!-- -->`{=html}0.5cm, and the map consists of 128$\times$`<!-- -->`{=html}128$\times$`<!-- -->`{=html}128 grid cells. For both A\* and Octree-A\*, the $g(n)$ is computed by accumulating the distances between the midpoints of adjacent nodes.

Fig. [1](#fAstar){reference-type="ref" reference="fAstar"} illustrates the path computed by the modified 3D A\* algorithm on a uniform grid. In the path visualization, red segments indicate traversal along the ground surface, while black segments represent portions of the path over obstacle surfaces. In both scenarios, the paths satisfy the constraint of moving along the surface while maintaining optimality. In particular, Fig. [\[fAstar2\]](#fAstar2){reference-type="ref" reference="fAstar2"} shows that the path is generated only over obstacles that are feasible to leverage. Fig. [2](#fOctree){reference-type="ref" reference="fOctree"} visualizes the size and distribution of leaf nodes for each scenario. Scenario 1 contains 47 obstacles, whereas Scenario 2 contains 78. As shown in the figure, a lower number of obstacles results in fewer leaf nodes with larger average side lengths. The visualization of the modified A\* applied to leaf nodes is shown in Fig. [3](#fOcastar){reference-type="ref" reference="fOcastar"}. Although the generated paths differ from those on the uniform grid, they satisfy all constraints and successfully achieve optimality. Table [1](#tBenchmark){reference-type="ref" reference="tBenchmark"} presents the quantitative benchmark results of A\* and Octree-A\*.

Compared to uniform nodes, applying leaf nodes resulted in a 0.41% increase in path length for Scenario 1 and a 0.80% decrease for Scenario 2 indicating that the path lengths generated by both node types are comparable. The computation time of Octree-A\* is the combined time of both octree generation and A\* path planning. The Octree-A\* significantly reduced computation time by 92.63% and 91.18% in Scenarios 1 and 2, respectively. Memory usage was reduced by 95.50% and 92.73% in Scenarios 1 and 2, respectively, with higher compression observed in environments containing fewer obstacles.

# CONCLUSION {#sCONCLUSION}

In this paper, we studied the 3D optimal path planning method for ground vehicles that generates paths by leveraging obstacles when beneficial. The cost function was modified with a penalty to enforce surface-level path generation and to restrict traversal to only feasible obstacles. With the octree structure, memory consumption dropped to under 10% while computation time was reduced by a factor greater than 10. The improvements in performance were achieved without compromising the characteristics of A\*. Since all path lengths were computed by connecting the center points of nodes, the trajectories may not be shortest for ground vehicles. By applying post-processing such as spline curves, shorter and smoother paths may be obtained.

::: thebibliography
10

W.-S. Park, M.-S. Park, and H.-W. Yang, "The optimal design scheme of an sugv for surveillance and reconnaissance missions in urban and rough terrain," *International Journal of Control, Automation and Systems*, vol. 10, pp. 992--999, 2012.

Y. Tang, X. Xu, L. Zhang, G. Chen, K. Luo, and L. Yan, "Structure design and configuration optimization of the reconfigurable deformed tracked wheel based on terramechanics characteristics," *Journal of Intelligent & Robotic Systems*, vol. 108, no. 1, p. 7, 2023.

D. Kim, J. Di Carlo, B. Katz, G. Bledt, and S. Kim, "Highly dynamic quadruped locomotion via whole-body impulse control and model predictive control," *arXiv preprint arXiv:1909.06586*, 2019.

R. Grandia, F. Jenelten, S. Yang, F. Farshidian, and M. Hutter, "Perceptive locomotion through nonlinear model-predictive control," *IEEE Transactions on Robotics*, vol. 39, no. 5, pp. 3402--3421, 2023.

J. Kang, H.-B. Kim, B.-I. Ham, and K.-S. Kim, "External force adaptive control in legged robots through footstep optimization and disturbance feedback," *IEEE Access*, 2024.

P. Biswal and P. K. Mohanty, "Development of quadruped walking robots: A review," *Ain Shams Engineering Journal*, vol. 12, no. 2, pp. 2017--2031, 2021.

H.-B. Kim, C. Kim, B.-I. Ham, J. Kang, M. Choi, K.-H. Choi, and K.-S. Kim, "Development of remote piping inspection system with dual-mode locomotion quadruped robot," in *International Conference on Robot Intelligence Technology and Applications*, pp. 307--319, Springer, 2024.

Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, "Robot parkour learning," *arXiv preprint arXiv:2309.05665*, 2023.

A. Candra, M. A. Budiman, and K. Hartanto, "Dijkstra's and a-star in finding the shortest path: a tutorial," in *2020 International Conference on Data Science, Artificial Intelligence, and Business Analytics (DATABIA)*, pp. 28--32, IEEE, 2020.

C. Ju, Q. Luo, and X. Yan, "Path planning using an improved a-star algorithm," in *2020 11th international conference on prognostics and system health management (PHM-2020 Jinan)*, pp. 23--26, IEEE, 2020.

S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," *The international journal of robotics research*, vol. 30, no. 7, pp. 846--894, 2011.

K. Solovey, L. Janson, E. Schmerling, E. Frazzoli, and M. Pavone, "Revisiting the asymptotic optimality of rrt," in *2020 IEEE international conference on robotics and automation (ICRA)*, pp. 2189--2195, IEEE, 2020.

J. Braun, T. Brito, J. Lima, P. G. d. Costa, P. Costa, and A. Y. Nakano, "A comparison of a\* and rrt\* algorithms with dynamic and real time constraint scenarios for mobile robots," in *9th International Conference on Simulation and Modeling Methodologies, Technologies and Applications, SIMULTECH 2019*, pp. 398--405, Scitepress, 2019.

A. Belaid, B. Mendil, and A. Djenadi, "Narrow passage rrt\*: a new variant of rrt," *International journal of computational vision and robotics*, vol. 12, no. 1, pp. 85--100, 2022.

Y. Huang and H.-H. Lee, "Adaptive informed rrt\*: Asymptotically optimal path planning with elliptical sampling pools in narrow passages," *International Journal of Control, Automation and Systems*, vol. 22, no. 1, pp. 241--251, 2024.

H. Tu, Y. Deng, Q. Li, M. Song, and X. Zheng, "Improved rrt global path planning algorithm based on bridge test," *Robotics and Autonomous Systems*, vol. 171, p. 104570, 2024.

Z. Yan, J. Zhang, J. Zeng, and J. Tang, "Three-dimensional path planning for autonomous underwater vehicles based on a whale optimization algorithm," *Ocean engineering*, vol. 250, p. 111070, 2022.

X. Li and S. Yu, "Three-dimensional path planning for auvs in ocean currents environment based on an improved compression factor particle swarm optimization algorithm," *Ocean Engineering*, vol. 280, p. 114610, 2023.

F. Kiani, A. Seyyedabbasi, R. Aliyev, M. U. Gulle, H. Basyildiz, and M. A. Shah, "Adapted-rrt: novel hybrid method to solve three-dimensional path planning problem using sampling and metaheuristic-based algorithms," *Neural Computing and Applications*, vol. 33, no. 22, pp. 15569--15599, 2021.

Z. Zhang, J. Yan, X. Kong, G. Zhai, and Y. Liu, "Efficient motion planning based on kinodynamic model for quadruped robots following persons in confined spaces," *IEEE/ASME Transactions on Mechatronics*, vol. 26, no. 4, pp. 1997--2006, 2021.

X. Xu, P. Li, J. Zhou, and W. Deng, "Path planning of quadrupedal robot based on improved rrt-connect algorithm," *Sensors*, vol. 25, no. 8, p. 2558, 2025.

H. Liu and Q. Yuan, "Safe and robust motion planning for autonomous navigation of quadruped robots in cluttered environments," *IEEE Access*, 2024.

L. Zhe, L. Yibin, R. Xuewen, and Z. Hui, "Path planning based on adfa\* algorithm for quadruped robot," *IEEE Access*, vol. 7, pp. 111095--111101, 2019.

Z. Li, B. Li, Q. Liang, W. Liu, L. Hou, and X. Rong, "A quadruped robot obstacle avoidance and personnel following strategy based on ultra-wideband and three-dimensional laser radar," *International Journal of Advanced Robotic Systems*, vol. 19, no. 4, p. 17298806221114705, 2022.

Z. Li, Y. Li, X. Rong, and H. Zhang, "Grid map construction and terrain prediction for quadruped robot based on c-terrain path," *IEEE Access*, vol. 8, pp. 56572--56580, 2020.

Y. Liu, L. Jiang, F. Zou, B. Xing, Z. Wang, and B. Su, "Research on path planning of quadruped robot based on globally mapping localization," in *2020 3rd International Conference on Unmanned Systems (ICUS)*, pp. 346--351, IEEE, 2020.

D. Hoeller, N. Rudin, D. Sako, and M. Hutter, "Anymal parkour: Learning agile navigation for quadrupedal robots," *Science Robotics*, vol. 9, no. 88, p. eadi7566, 2024.

R. Schnabel and R. Klein, "Octree-based point-cloud compression.," *PBG@ SIGGRAPH*, vol. 3, no. 3, 2006.
:::
