---
citation_key: Li2025UnidirectionalRoadNetworkBased
arxiv_id: 2511.13048
arxiv_url: "https://arxiv.org/abs/2511.13048"
title: "Unidirectional-Road-Network-Based Global Path Planning for Cleaning Robots in Semi-Structured Environments"
authors_short: "Yong Li et al."
year: 2025
direction_tag: F_hybrid_astar
source: pymupdf4llm
converted_at: 2026-06-23T18:50:23Z
origin: ai+web
reviewed: false
---

## **Unidirectional-Road-Network-Based Global Path Planning for Cleaning Robots in Semi-Structured Environments** 

Yong Li[1,2,*] , _Member_ , _IEEE,_ and Hui Cheng[2] 

_**Abstract**_ **— Practical global path planning is critical for commercializing cleaning robots working in semi-structured environments. In the literature, global path planning methods for free space usually focus on path length and neglect the traffic rule constraints of the environments, which leads to high-frequency re-planning and increases collision risks. In contrast, those for structured environments are developed mainly by strictly complying with the road network representing the traffic rule constraints, which may result in an overlong path that hinders the overall navigation efficiency. This article proposes a general and systematic approach to improve global path planning performance in semi-structured environments. A unidirectional road network is built to represent the traffic constraints in semi-structured environments and a hybrid strategy is proposed to achieve a guaranteed planning result. Cutting across the road at the starting and the goal points are allowed to achieve a shorter path. Especially, a two-layer potential map is proposed to achieve a guaranteed performance when the starting and the goal points are in complex intersections. Comparative experiments are carried out to validate the effectiveness of the proposed method. Quantitative experimental results show that, compared with the state-of-art, the proposed method guarantees a much better balance between path length and the consistency with the road network.** 

## I. INTRODUCTION 

## _A. Motivation_ 

As a typical service robot, the cleaning robot is used to clean the solid and liquid wastes on the ground [1]. Cleaning robots in unstructured environments have been widely used, such as the household-sweeping robot [2], while the ones working in garages, construction zones, around shopping centers, and other semi-structured environments are still at an early stage [3][4]. There are still many problems to be solved, one of them is finding a practical global path. 

In addition to accomplishing the cleaning task and ensuring their own safety, robots working in semi-structured environments need to interact with vehicles, non-vehicles, pedestrians, and even other kinds of robots and autonomous vehicles. So as not to cause confusion or trouble to human drivers and other agents, they should also try to comply with the traffic rules. A practical approach is building a road network that accounts for the traffic rules so that we can plan a global path with it [5]. In the fields of autonomous driving and automated valet parking, road-network-based global path planning is already a common practice [4][6][7]. The basic flow is: (1) find the nodes pair 𝑝𝑚𝑠, 𝑝𝑚𝑔 closest to the 

> 1Guangzhou Shiyuan Electronic Technology Co., Ltd., Guangzhou 510300, China. 

> 2School of Data and Computer Science, Sun Yat-sen University, Guangzhou 510006, China. 

starting point 𝑝𝑠 and the goal point 𝑝𝑔 in the road network respectively ( 𝑝𝑚𝑠 and 𝑝𝑚𝑔 should also satisfy the angle constraint); (2) use graph search algorithm to find the path connecting 𝑝𝑚𝑠 and 𝑝𝑚𝑔 ; (3) adjust path points density and smooth the path. However, such practices may not be the best solution for robots in semi-structured environments. As Fig.1 shows, strictly following the traffic rules results in overlong paths in some situations, which results in low working efficiency for cleaning robots. 

Balancing path length and the consistency with the road network is critical for commercializing cleaning robots working in semi-structured environments and is the main focus of this article. 

## _B. Related Work_ 

Common algorithms for global path planning can be classified into four types[8]: graph-search-based planners, sampling-based methods, interpolating-curve-based and optimization-based ones. Detailed analysis and comparisons can be seen in review articles [8] and [9]. 

Currently, most of the research on global path planning is for unstructured and structured environments [7]. For the former, global path planning is viewed as a free-space-pathfinding problem. Methods in the literature are proposed mainly to shorten plan length and improve search efficiency with/without kinematics constraints [10] [11][12]. Such methods are not suitable for semi-structured environments as they do not take traffic rules and the respect for human drivers into account, which brings enormous safety risks to both the robot itself and other traffic participants. 

The global path planning methods in structured environments are usually developed based on the traffic rule constraints described by unidirectional road networks [7][13] [14]. The planning results are required to strictly comply with the traffic rules such as lane following, lane changing, merging, pulling over, and so on [15]. The robot is not allowed to cut across the road or drive reversely on highways. As shown in Fig. 1, strictly complying with the traffic rules negatively impacts the robot's work efficiency. 

Some research has been carried out to meet the set-out requirements in semi-structured environments. Tsiakas uses a sparse road network described by OSM to guide the global path planning process, and pathfinding is achieved by the A* algorithm [16]. Klaudt combined the road network with a semantic and metric map to realize parking path planning in garages using a state-based planner [4]. The above two research work is based on the bidirectional road network. The planned global path points are usually distributed along the road center, which does not comply with the right-hand traffic (or left-hand traffic) rule, increasing the re-planning frequency and the risk of collision. Dolkov combined the free spa- 

> *Corresponding author: Yong Li (e-mail: liyong2018@zju.edu.cn). 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-00.png)


Fig. 1. Global path planning results when strictly complying with the road network that accounts for the traffic rules: (a) the starting and goal points are in the same lane and the latter is behind the former; (b) The starting and goal points are close but they are in the reverse lanes; (c) The starting and goal points are in different intersections and they are close to each other; (d) The starting and goal points are in different intersections and they are far away from each other. 

ce hybrid A* algorithm with the road network to improve the path quality in semi-structured environments [17][18]. In the nodes expansion step of the A* search, the deviation from the road network is penalized, and the road network nodes also provide a good set of macro-actions. The algorithm ensures that the planned path points are close to the road network but can not guarantee they align with the road network in direction. 

## _C. Contributions_ 

This article proposes a practical global path planning algorithm for commercial cleaning robots working in semi-structured environments. The main contributions are: 

(1) A general and systematic global path planning algorithm based on a unidirectional road network and twolayer potential map is proposed, which makes a better balance between path length and the consistency with the road network (both in distance and direction). 

(2) A scenario-based strategy is adopted to meet the set-out requirements in semi-structured environments. The robot is allowed to cut across the road at the starting and goal points, which ensures the finding of a shorter path. Besides, the road network constraints in complex intersections are described with a two-layer potential map. 

(3) Comparative experiments are carried out and quantitative performance indexes are introduced to verify the superiority of the proposed method. 

The rest of the article is organized as follows: Sec. Ⅱis about problem description, followed by Sec. Ⅲpresenting the methodology. Then comparative and field experimental results are described in Sec. Ⅳ. Conclusions are drawn in Sec. Ⅴ. 

## II. PROBLEM DESCRIPTION 

Without loss of generality, the descriptions in the rest of the article are based on a garage with the traffic rule of right-hand driving, and the research results can be easily extended to other semi-structured environments. Fig. 2 is a typical semantic map for the garage-cleaning robot. The passable areas include the passages (chocolate), the intersections (dark violet) and the parking areas (light green). The 

cleaning robot needs to complete the full coverage cleaning task in passable areas (full coverage path planning in the semi-structured environment will be carried out in our following research and this study only focuses on global path planning when the robot travels between different clean areas). Actually, appropriately cutting across the road is acceptable [19] to some extent for the following two reasons. First, when the robot executes the full coverage cleaning task, it is unavoidable that the robot cuts across the road; It is also reasonable to allow such behavior in global path planning. Second, the cleaning robot is much smaller than the vehicles. It is usually driven by differential wheels and thus has a much smaller turning radius than Ackerman-type robots. To balance safety and movement flexibility, the shortcut is only allowed at the starting and goal points in this study. 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-12.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-13.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-14.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-15.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-16.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-17.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-18.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0002-19.png)


Fig. 2. The passable areas for a garage-cleaning robot with passages in chocolate, intersections in dark violet and parking areas in light green. 

Besides, we should map the starting and goal points to the road network to find a valid path. However, finding a suitable mapping is challenging when the starting and goal points are in complex intersections even with the allowance of the shortcut. Noticeably, the road network has two kinds of restraints to the global path planning process: distance constraint and direction constraint. Considering the complexity of intersections and the fact that intersections usually have small areas, it is reasonable and practical to only consider the distance constraint in intersections. 

For a road network represented as 𝐺= 𝑉, 𝐸 with 𝑉 nodes and 𝐸 edges, our goal is to minimize the planning cost 𝐽(𝑺) as follows: 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-01.png)


where 𝑺= 𝑠𝑖, 𝑖= 1,2,. . . , 𝑛 is the global path with 𝑠𝑖 = 𝑥𝑖, 𝑦𝑖, 𝜃𝑖 the _i_ th global path point, 𝑓𝑙(𝑺) the path length cost, 𝑓𝑑(𝑠𝑖, 𝐺) and 𝑓𝜃(𝑠𝑖, 𝐺 ) the cost of the distance and angle between 𝑠𝑖 and 𝐺, respectively. This article tries to minimize 𝐽(𝑺) with hybrid strategies rather than giving an analytic solution. 

III. METHODOLOGY 

## _A. Unidirectional road network_ 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-05.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-06.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-07.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-08.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-09.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-10.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-11.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-12.png)


Fig. 3. A typical semantic map for the garage-cleaning robot with the unidirectional road network in chocolate, intersection areas in dark violet and parking areas in light green. The arrows of the lanes indicate their direction. 

The road network can be designed according to the actual situation of the environment with considering the set-out requirements. For example, the unidirectional road network for the garage of Guangzhou Shiyuan Electronic Technology Co., Ltd. is designed as Fig. 3 shows. The road network is composed of unidirectional lanes 𝐿= 𝐿𝑖, 𝑖= 1,2,. . . , 𝑛 and each lane 𝐿𝑖 has two nodes 𝑝𝑖 = 𝑝𝑖𝑠, 𝑝𝑖𝑒 (fewer nodes improve the speed of road network construction and 𝑓𝑟𝑜𝑚 pathfinding process). The predecessor lanes 𝐿𝑖 and the successor lanes 𝐿𝑡𝑜𝑖 of 𝐿𝑖 can be expressed as: 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-15.png)


where 𝜃∗ is the angle of node ∗ ( ∗= 𝑝𝑗𝑒, 𝑝𝑖𝑠, 𝑝𝑗𝑠 𝑎𝑛𝑑𝑝𝑖𝑒 ), 𝛼𝑚𝑖𝑛 the angle threshold and 𝑑𝑚𝑖𝑛 the distance threshold. Besides, the procedure for finding the reverse lanes 𝐿𝑟𝑒𝑣𝑒𝑟𝑠𝑒𝑖 of 𝐿𝑖 can be seen in Algorithm 1. For every node in 𝐿𝑖 , the algorithm tries to find its closest lane 𝐿𝑗 in 𝐿 with 𝐿𝑗 no a predecessor/successor lane nor an intersection lane of 𝐿𝑖. The founded lane and 𝐿𝑖 are reverse lanes of each other. The nodes of 𝐿 are also the nodes 𝑉 of road network _G_ . the edges 𝑉 of _G_ are represented as unidirectional edges. The predeces𝑓𝑟𝑜𝑚 𝑡𝑜 sor node 𝑝𝑖𝑒 of 𝑝𝑖𝑒 is 𝑝𝑖𝑠 while the successor node 𝑝𝑖𝑠 of 

𝑓𝑟𝑜𝑚 𝑝𝑖𝑠 is 𝑝𝑖𝑒 . The predecessor nodes 𝑝𝑖𝑠 of 𝑝𝑖𝑠 and successor nodes 𝑝𝑡𝑜𝑖𝑒 of 𝑝𝑖𝑒 are respectively represented as: 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-18.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-19.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-20.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0003-21.png)


Based on the above nodes and edges, the unidirectional road network 𝐺= 𝑉, 𝐸 can be built. 

## _B. Search strategy_ 

> **Case1** ： **path planning with starting and goal points in passages or parking areas.** When the starting and goal points are in passages or parking areas, the complete planning procedure is shown in Algorithm 2. In this study, the starting and goal points are mapped not only to the closet lane but also to the reverse lanes of their closet lane. For the planned path, the mapping rules are designed to ensure no sharp turns around the matched starting points or the matched goal ones. 

_1) Starting point mapping_ : For starting point 𝑝𝑠, donate its closest lane as 𝐿𝑐 and 𝐿𝑐's reverse lane is 𝐿𝑟𝑒𝑣𝑒𝑟𝑠𝑒𝑐 . The set of 𝐿𝑐 and 𝐿𝑟𝑒𝑣𝑒𝑟𝑠𝑒𝑐 is represented as 𝛹= 𝐿𝑐 ∪𝐿𝑟𝑒𝑣𝑒𝑟𝑠𝑒𝑐 . For ∀𝛹𝑘 ∈𝛹, 𝑘= 1,2,. . . , 𝑚 with 𝛹𝑘 composed of 𝑝𝑘𝑠 and 𝑝𝑘𝑒, the relative spatial relationship between 𝑝𝑠 and 𝛹𝑘 can be seen in Fig. 4 with 𝑝𝑠1, 𝑝𝑠2 𝑎𝑛𝑑𝑝𝑠3 three possible locations of 𝑝𝑠. For easy of notation, let 𝐏𝟎 = 𝑝�������𝑘𝑠𝑝⃑𝑠, 𝐏𝟏 = �������[𝑝] 𝑘𝑒[𝑝] ⃑𝑠, 𝐏 

��������⃑ 𝑚𝑎𝑡𝑐ℎ = 𝑝𝑘𝑠𝑝𝑘𝑒 . The matching point[𝑝] 𝑘 can be expressed as follows: 

- 𝑚𝑎𝑡𝑐ℎ 

- if 𝐏𝟎𝐏< 0 (corresponding to 𝑝𝑠1 in Fig.4(a)), 𝑝𝑘 = 𝑝𝑘𝑠. 

- if 𝐏𝟎𝐏> 0&𝐏𝐏𝟏 < 0 (corresponding to 𝑝𝑠2 in Fig. 4(a)), 𝑝𝑚𝑎𝑡𝑐ℎ𝑘 = 𝑝𝑘𝑠 + 𝐏𝟎𝐏𝐏 𝐏 2. 

- 𝑚𝑎𝑡𝑐ℎ 

- if 𝐏𝐏𝟏 > 0 (corresponding to 𝑝𝑠3 in Fig. 4(a)), 𝑝𝑘 = {𝑝𝑢𝑠 ∈𝐿𝑢, 𝐿𝑢 ∈𝛹𝑡𝑜𝑘 }. 

Then the set of the matched starting points is represented as 𝑷𝑚𝑎𝑡𝑐ℎ𝑠𝑡𝑎𝑟𝑡 = {𝑝𝑚𝑎𝑡𝑐ℎ𝑘 , 𝑘= 1,2, . .. , 𝑚}. _2) Goal point mapping:_ Similarly, as shown in Fig.4(b), the matching point 𝑝𝑚𝑎𝑡𝑐ℎ𝑘 for the goal point 𝑝𝑔 can be represented as follows: 

- if 𝐏𝟎𝐏< 0 (corresponding to 𝑝𝑒1 in Fig.4(b)), 𝑚𝑎𝑡𝑐ℎ 𝑓𝑟𝑜𝑚 

- 𝑝𝑘 = {𝑝𝑣𝑠 ∈𝐿𝑣, 𝐿𝑣 ∈𝛹𝑘 }. 

- if 𝐏𝟎𝐏> 0&𝐏𝐏𝟏 < 0 (corresponding to 𝑝𝑒2 in Fig. 4(b)), 𝑝𝑚𝑎𝑡𝑐ℎ𝑘 = 𝑝𝑘𝑠 + 𝐏𝟎𝐏𝐏 𝐏 2. 

- if 𝐏𝐏𝟏 > 0(corresponding to 𝑝𝑒3in Fig. 4(b)), 𝑝𝑚𝑎𝑡𝑐ℎ𝑘 = 𝑝𝑘𝑒. 

Then the set of the matched goal points is represented as 𝑷𝑚𝑎𝑡𝑐ℎ𝑔𝑜𝑎𝑙 . 𝑷𝑚𝑎𝑡𝑐ℎ𝑠𝑡𝑎𝑟𝑡 and 𝑷𝑚𝑎𝑡𝑐ℎ𝑔𝑜𝑎𝑙 serve as the start and goal candidates in the path searching process. 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0004-05.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0004-06.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0004-07.png)


Fig. 4. (a) starting point mapping: 𝑝𝑠1,𝑝𝑠2and𝑝𝑠3represent three probable positions of starting point 𝑝𝑠 , 𝛹𝑘 the closest lane to 𝑝𝑠, 𝛹𝑓𝑟𝑜𝑚𝑘 and 𝛹𝑡𝑜𝑘 the predecessor and successor lane of 𝛹𝑘, respectively. The ends of the arrows represent the mapping results; (b) goal point mapping: 𝑝𝑒1,𝑝𝑒2,𝑝𝑒3 are three probable positions of goal point 𝑝𝑔,𝛹𝑘 the closest lane to 𝑝𝑔, 𝛹𝑓𝑟𝑜𝑚𝑘 and 𝛹𝑡𝑜𝑘 the predecessor and successor lane of 𝛹𝑘 , respectively. The ends of the arrows represent the mapping results. _3) Path searching:_ For every 𝑝𝑚𝑎𝑡𝑐ℎ𝑠 in 𝑷𝑚𝑎𝑡𝑐ℎ𝑠𝑡𝑎𝑟𝑡 and 𝑝𝑚𝑎𝑡𝑐ℎ𝑔 in 𝑷𝑚𝑎𝑡𝑐ℎ𝑔𝑜𝑎𝑙 , the Dijkstra algorithm is adopted to find a 

valid path. Appending the starting point 𝑝𝑠 and the goal point 𝑝𝑔 to the front and back of the Dijkstra path, respectively, then we can get the total path ℶ that connects 𝑝𝑠 and 𝑝𝑔 . Looping through 𝑷𝑚𝑎𝑡𝑐ℎ𝑠𝑡𝑎𝑟𝑡 and 𝑷𝑚𝑎𝑡𝑐ℎ𝑔𝑜𝑎𝑙 then we can get the shorted path 𝜒. A branch-and-bound method is adopted in the cycles to improve the computation efficiency: If the length of current ℶ is shorter than the shortest path 𝜒 ever, the total search cost of the Dijkstra process in this cycle will be used as the upper bound cost for Dijkstra in the following cycles. 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0004-10.png)


> **Case2** ： **path planning with starting and goal points in intersections.** The procedure in Case 1 can not guarantee the quality of the generated path in Case 2 due to the complexity of intersection areas. In this article, a hybrid strategy is proposed: the sub-paths inside the intersections are obtained based on a two-layer potential map, while those outside the intersections are gained with a strategy similar to that in Case 1. Detailed procedures can be seen in Algorithm 3. 

_1) path planning outside the intersections:_ For 𝑝𝑠 and 𝑝𝑔, without loss of generality, assume they locate in intersections 𝑆𝑚 and 𝑆𝑛 (𝑚≠𝑛), respectively. The set of intersected points of 𝑆𝑚/𝑆𝑛 and _G_ is represented as 𝑷𝑖𝑛𝑡𝑒𝑟𝑠𝑠𝑡𝑎𝑟𝑡 / 𝑷𝑖𝑛𝑡𝑒𝑟𝑠𝑔𝑜𝑎𝑙 . Similar to the procedure in Case 1, the shortest path χ(𝑝𝑠𝑡, 𝑝𝑔𝑡) can be obtained with starting point candidates 𝑷𝑖𝑛𝑡𝑒𝑟𝑠𝑠𝑡𝑎𝑟𝑡 and goal point candidates 𝑷𝑖𝑛𝑡𝑒𝑟𝑠𝑔𝑜𝑎𝑙 . The front and back points of χ(𝑝𝑠𝑡, 𝑝𝑔𝑡) are represented as 𝑝𝑠𝑡and 𝑝𝑔𝑡, respectively. 

_2) path planning within the intersections:_ In this step, sub-paths χ(𝑝𝑠, 𝑝𝑠𝑡) and χ(𝑝𝑔𝑡, 𝑝𝑔) are obtained so that we can get the complete path χ(𝑝𝑠, 𝑝𝑔) from 𝑝𝑠 to 𝑝𝑔. A two-layer potential map is proposed to represent the distance constraints of the road network. As can be seen in Fig.5, the first layer is a traditional static map 𝑚𝑠𝑡𝑎𝑡𝑖𝑐 with the obstacles inflated. The second layer 𝑚𝑠𝑒𝑚𝑎𝑛𝑡𝑖𝑐 is built based on the semantic information in Fig.3. A Gaussian potential field is generated within the passable area with the lanes reference (similar approaches can be seen in [20] and [21]). For every point 𝑥𝑖 in the passable area 𝑈𝑝, if the distance between 𝑥𝑖 a- 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0005-00.png)


Fig. 5. Part of the two-layer potential map used for path planning when the starting and goal points are in intersections: (a) static metric map with obstacles inflated; (b) road network Gaussian likelihood potential maps; (c) the combined map. 

nd the road network _G_ is 𝑑𝑥𝑖, its potential value 𝑝(𝑥𝑖) can be computed as: 

𝑝(𝑥𝑖) = 𝑝0 1 −𝑒𝑥𝑝( −𝑑2𝒙𝑖 2𝜎[2] ) , 𝑥𝑖 ∈𝑈𝑝 (4) where 𝑝0 is the maximal potential, 𝜎 the standard deviation. The potential value for points on the road boundary is 𝑝0 and that for points outside passable areas is 0. Combining 𝑚𝑠𝑡𝑎𝑡𝑖𝑐 and 𝑚𝑠𝑒𝑚𝑎𝑛𝑡𝑖𝑐 with the adoption of a larger potential value in each grid cell, we can get the map 𝑚 used for path planning. A traditional Dijkstra planner is then adopted to get χ(𝑝𝑠, 𝑝𝑠𝑡) and χ(𝑝𝑔𝑡, 𝑝𝑔). 

It can be seen from the above procedure in Case 2 that a piece-wise planning strategy is adopted: the starting point 𝑝𝑠𝑡 and the goal point 𝑝𝑔𝑡 for the planning within the intersections are the outcomes of the planning outside the intersections; we end up with a path that may not be optimal. Considering the computation burden and the fact that the intersections often have a small area, the above sub-optimal strategy is acceptable. 

It should be noted that this article only describes the path planning strategy in two typical situations, where both the starting and goal points are in the passage/parking area or in different intersections. There are much more combinations such as: the starting point in passage/parking area while the goal point in intersections, the goal point in passage/parking area while the starting point in intersections, or the starting and goal points in the same intersection. Due to space limitations, we will not elaborate on them case by case. Noticeably, they can be easily handled with the basic ideas in Case1&2. 

## IV. EXPERIMENTS 

## _A. Comparative experiments_ 

To verify the effectiveness of the proposed method, comparative experiments are carried out. The computing unit used in the experiments is an industrial computer with CPU i7-10700@2.9Hz×16 and RAM of 16 GB. The size of the map used in the experiment is 75 _m_ * 128 _m_ . The following four methods are compared: 

_**Hybrid-A*-in-SS**_ : Hybrid A* in semi-structured environments [18], is considered the state-of-the-art. The cost coefficient 𝐶𝐺 (the deviation from the road network) is set to be 1. 

_**Dijkstra**_ : The widely used Dijkstra algorithm in free space. The map resolution is 0.05m. 

_**Dijkstra-in-SS** :_ Dijkstra in semi-structured environments. In the nodes-expansion step of Dijkstra, the cost representing the distance between the current node and the road network is considered. 

_**Ours** :_ the method proposed in this article. 

To quantify the performance of different planners, the following performance indexes are used: 

- 100 

- 𝑡= 1 100 ∑i=0 𝑡𝑖 , the average planning time for 100 consecutive planning cycles, is used to evaluate the computation efficiency; 

- 𝑙 the path length, is used to evaluate the distance cost; 

- 𝑛 

- 𝑑𝑒 = 1 𝑛 ∑𝑖=0 𝑑𝑖 with 𝑑𝑖 = 𝐏𝟎 × 𝐏/ 𝐏 (𝐏𝟎 = ������𝑝𝑗𝑠𝑝⃑𝑖 , 𝐏= 𝑝�������𝑗𝑠𝑝𝑗𝑒⃑ ) the distance between the path point 𝑝𝑖 and its closest lane 𝐿𝑗 ( 𝐿𝑗 is composed of points 𝑝𝑗𝑠 and 𝑝𝑗𝑒), is used to evaluate the distance deviation from the road network; 

- 𝑛 

- 𝜃𝑒 = 1 𝑛 ∑𝑖=0 ∆𝜃𝑖 with ∆𝜃𝑖 = 𝜃𝑝𝑖 −𝜃𝑝𝑗𝑠the relative angle between the path point 𝑝𝑖 and its closest lane 𝐿𝑗 (𝐿𝑗 is composed of points 𝑝𝑗𝑠 and 𝑝𝑗𝑒), is used to evaluate the direction deviation from the road network _._ 

|TABLE I.<br>PERFORMANCE INDEXES IN EXPERIMENT1|TABLE I.<br>PERFORMANCE INDEXES IN EXPERIMENT1|TABLE I.<br>PERFORMANCE INDEXES IN EXPERIMENT1|TABLE I.<br>PERFORMANCE INDEXES IN EXPERIMENT1|TABLE I.<br>PERFORMANCE INDEXES IN EXPERIMENT1|
|---|---|---|---|---|
||HybridA*-in-SS|Dijkstra|Dijkstra-in-SS|Ours|
|𝑡(s)|11.279|0.405|0.409|**0.009**|
|𝑙(m)|132.514|**127.172**|131.158|137.599|
|𝑑𝑒(m)|0.039|0.625|0.085|**0.028**|
|𝜃𝑒(rad)|1.997|2.876|2.004|**0.095**|



**Experiment 1** : **both the starting and goal points are in the passage** _._ As can be seen in Fig.6 and Table 1, The traditional _Dijkstra_ algorithm has the shortest path. Due to the neglect of the road network constraints, it has the worst performance in 𝑑𝑒 and 𝜃𝑒. Compared with _Dijkstra_ , _Hybrid-A*-in-SS_ and _Dijkstra-in-SS_ both have improved performance in 𝑑𝑒 due to the introduction of the road-network-distance-derivation penalty. However, they can not guarantee a small 𝜃𝑒 in nature. The path length of the proposed method is 3.8% longer than that of the _Hybrid-A*-in-SS_ mainly due to the shortcut at the goal point. However, the proposed method has better performance in the consistency with the road network, especially in terms of the direction deviation 𝜃𝑒 , which significantly improves the navigation safety of the robot. Besides, due to the adoption of the sparse unidirectional road network in Sec. Ⅲ. A, our method has better performance in planning time than those grid-map-based planners. 

**Experiment 2** : **the starting and goal points are in different intersections.** Experimental results and performance indexes for Experiment 2 are shown in Fig. 7 and Table 2, respectively. Compared with other planners, our method has similar performance in path length but with shorter planning 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0006-00.png)



![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0006-01.png)


Fig. 6. Planning results in Experiment 1 with 𝜃𝑒 representing the angle error between the path point and its closest lane. 


![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0006-03.png)


Fig. 7. Planning results in Experiment 2 with 𝜃𝑒 representing the angle error between the path point and its closest lane. 

TABLE II. PERFORMANCE INDEXES IN EXPERIMENT 2 

||HybridA*-in-SS|Dijkstra|Dijkstra-in-SS|Ours|
|---|---|---|---|---|
|𝑡(s)|8.534|0.349|0.351|**0.101**|
|𝑙(m)|91.7328|**88.023**|88.479|91.280|
|𝑑𝑒(m)|0.035|0.606|0.063|**0.027**|
|𝜃𝑒(rad)|2.542|2.725|3.029|**0.220**|




![](1_survey/papers/md/Li2025UnidirectionalRoadNetworkBased_figs/Li2025UnidirectionalRoadNetworkBased.pdf-0006-07.png)


Fig. 8. An instance of the field experiment with the proposed global path planner in the garage of Guangzhou Shiyuan Electronic Technology Co., Ltd. 

time. Due to the adoption of the two-layer-map based hybrid planning strategy in Algorithm 2, compared with _Hybrid-A*in-SS_ , 22.86% and 91.35% improvement in 𝑑𝑒 and 𝜃𝑒 can be obtained, respectively. It means that with the proposed method, a much better balance between path length and the 

consistency with the road network has been achieved, which is vital for path planning in semi-structured environments. 

## _B. Experiments with robots_ 

Field experiments are carried out in the garage shown in Fig.8(a) with the semantic map in Fig.8(b). The starting and goal points in Fig.8(c) are the same as those in Experiment 1. The robot used in the experiment is a commercial garagecleaning robot produced by Guangzhou Shiyuan Electronic Technology Co., Ltd. with RK3399 the computation unit. The global path planner proposed in this article provides a reference line to the local path planner module, which is a lightweight state lattice planner. The video of the experiment is submitted as a supplementary material. 

## V. CONCLUSION 

This article proposes a general and systematic global path planning method for robots in semi-structured environments. Comparative experimental results show that it achieves a much better balance between path length and the consistency with the road network, which distinguishes our work from the ones in the literature. The proposed method has been widely used in the commercial garage-cleaning robot produced by Guangzhou Shiyuan Electronic Technology Co., Ltd. 

Our research focuses on solving the critical motion planning problems that prevent the commercializing robots in semi-structured environments. Research on full coverage path planning and local path planning for robots in semistructured environments will be carried out in the future. 

## REFERENCES 

- [1] R. Bormann, F. Jordan, J. Hampp and M. Hägele, "Indoor Coverage Path Planning: Survey, Implementation, Analysis," in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2018, pp. 1718-1725. 

- [2] L. Sui and L. Lin, "Design of Household Cleaning Robot Based on Low-cost 2D LIDAR SLAM," in _2020 International Symposium on Autonomous Systems (ISAS)_ .IEEE, 2020, pp. 223-227. 

- [3] A. C. Magalhães, M. Prado, V. Grassi and D. F. Wolf, "Autonomous vehicle navigation in semi-structured urban environment", _IFAC Proceedings Volumes_ , vol. 46, no. 10, pp. 42-47, 2013. 

- [4] S. Klaudt, A. Zlocki and L. Eckstein, "A-priori map information and path planning for automated valet-parking," in _2017 IEEE Intelligent Vehicles Symposium (IV)_ .IEEE, 2017, pp. 1770-1775. 

- [5] F. Poggenhans et al., "Lanelet2: A high-definition map framework for the future of automated driving," in _2018 21st International Conference on Intelligent Transportation Systems (ITSC)_ .IEEE, 2018, pp. 1672-1679. 

- [6] K. Tsiakas, I. Kostavelis, A. Gasteratos and D. Tzovaras, "Autonomous Vehicle Navigation in Semi-structured Environments Based on Sparse Waypoints and LiDAR Road-tracking," in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ .IEEE, 2021, pp. 1244-1250. 

- [7] Hatem Darweesh, Eijiro Takeuchi, Kazuya Takeda, Yoshiki Ninomiya, Adi Sujiwo, Y. Morales, et al., "Open Source Integrated Planner for Autonomous Navigation in Highly Dynamic Environments", _Journal of Robotics and Mechatronics_ , vol. 29, pp. 668-684, 2017. 

- [8] D. González, J. Pérez, V. Milanés and F. Nashashibi, "A review of motion planning techniques for automated vehicles", _IEEE Transactions on Intelligent Transportation Systems_ , vol. 17, no. 4, pp. 1135-1145, 2016. 

- [9] H. Banzhaf, D. Nienhüser, S. Knoop and J. M. Zöllner, "The future of parking: A survey on automated valet parking with an outlook on high density parking," in _2017 IEEE Intelligent Vehicles Symposium (IV)_ .IEEE, 2017, pp. 1827-1834. 

- [10] S. Klemm et al., "RRT-Connect: Faster, asymptotically optimal motion planning," in _2015 IEEE International Conference on Robotics and Biomimetics (ROBIO)_ .IEEE, 2015, pp. 1670-1677. 

- [11] D. M. Saxena, T. Kusnur and M. Likhachev, "AMRA*: Anytime Multi-Resolution Multi-Heuristic A*," in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 3371-3377. 

- [12] D. Khalidi, D. Gujarathi and I. Saha, "T: A Heuristic Search Based Path Planning Algorithm for Temporal Logic Specifications," in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2020, pp. 8476-8482. 

- [13] J. Kim, K. Jo, K. Chu and M. Sunwoo, "Road-model-based and graph-structure-based hierarchical path-planning approach for autonomous vehicles", _Proceedings of the Institution of Mechanical Engineers Part D: Journal of Automobile Engineering_ , vol. 228, no. 8, pp. 909-928, 2014. 

- [14] W. Cheng, T. Gao, Z. Liu, S. Li, N. Li and C. Lu, "A Distributed Motion Planning Method based on Routing and Local Dynamic Programming," in 2020 3rd International Conference on Unmanned Systems (ICUS).IEEE, 2020, pp. 418-422. 

- [15] C. Urmson, J. Anhalt, D. Bagnell, C. Baker, R. Bittner, MN Clark, J. Dolan, D. Duggins, T. Galatali, C. Geyer et al., "Autonomous driving in urban environments: Boss and the Urban Challenge", _Journal of Field Robotics_ , vol. 25, no. 8, 2008. 

- [16] K. Tsiakas, I. Kostavelis, A. Gasteratos and D. Tzovaras, "Autonomous Vehicle Navigation in Semi-structured Environments Based on Sparse Waypoints and LiDAR Road-tracking," in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ .IEEE, 2021, pp. 1244-1250. 

- [17] D. Dolgov and S. Thrun, "Autonomous driving in semi-structured environments: Mapping and planning," in 2009 IEEE International Conference on Robotics and Automation _(ICRA)._ IEEE, 2009, pp. 3407-3414. 

- [18] D. Dolgov, S. Thrun, M. Montemerlo, and J. Diebel, “Path planning for autonomous vehicles in unknown semi-structured environments,” _The international journal of robotics research_ , vol. 29, no. 5, pp. 485– 501, 2010. 

- [19] F. Yang, D. -H. Lee, J. Keller and S. Scherer, "Graph-based Topological Exploration Planning in Large-scale 3D Environments," in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ .IEEE, 2021, pp. 12730-12736. 

- [20] K. Narula, S. Worrall and E. Nebot, "Two-Level Hierarchical Planning in a Known Semi-Structured Environment," in _2020 IEEE 23rd International Conference on Intelligent Transportation Systems (ITSC)_ .IEEE, 2020, pp. 1-6. 

- [21] D. Kim, H. Kim and K. Huh, "Trajectory Planning for Autonomous Highway Driving Using the Adaptive Potential Field," in _2018 21st International Conference on Intelligent Transportation Systems (ITSC)_ .IEEE, 2018, pp. 1069-1074. 

