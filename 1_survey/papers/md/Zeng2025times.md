---
citation_key: Zeng2025times
arxiv_id: 2510.02716
arxiv_url: "https://arxiv.org/abs/2510.02716"
title: "A $1000\times$ Faster LLM-enhanced Algorithm For Path Planning in Large-scale Grid Maps"
authors_short: "Junlin Zeng et al."
year: 2025
direction_tag: G_subgoal_optimization
source: pymupdf4llm
converted_at: 2026-06-23T18:36:00Z
origin: ai+web
reviewed: false
---

# **A** 1000 _×_ **Faster LLM-enhanced Algorithm For Path Planning in Large-scale Grid Maps** 

**Junlin Zeng, Xin Zhang, Xiang Zhao, Yan Pan**[*] 

National University of Defense Technology, 

Science and Technology on Information Systems Engineering Laboratory, Changsha, China _{_ zengjunlinnudt, zhangxin, zhaoxiang, panyan _}_ @nudt.edu.cn 

## **Abstract** 

Path planning in grid maps, arising from various applications, has garnered significant attention. Existing methods, such as A*, Dijkstra, and their variants, work well for smallscale maps but fail to address large-scale ones due to high search time and memory consumption. Recently, Large Language Models (LLMs) have shown remarkable performance in path planning but still suffer from spatial illusion and poor planning performance. Among all the works, LLM-A* (Meng et al. 2024) leverages LLM to generate a series of waypoints and then uses A* to plan the paths between the neighboring waypoints. In this way, the complete path is constructed. However, LLM-A* still suffers from high computational time for large-scale maps. To fill this gap, we conducted a deep investigation into LLM-A* and found its bottleneck, resulting in limited performance. Accordingly, we design an innovative LLM-enhanced algorithm, abbr. as iLLM-A*. iLLM-A* includes 3 carefully designed mechanisms, including the optimization of A*, an incremental learning method for LLM to generate high-quality waypoints, and the selection of the appropriate waypoints for A* for path planning. Finally, a comprehensive evaluation on various grid maps shows that, compared with LLM-A*, iLLM-A* **1) achieves more than** 1000 _×_ **speedup on average, and up to** 2349 _._ 5 _×_ **speedup in the extreme case, 2) saves up to** 58 _._ 6% **of the memory cost, 3) achieves both obviously shorter path length and lower path length standard deviation.** 

## **1 Introduction** 

Path planning in a grid map determines a collision-free path from a start location to a goal location, adhering to specific criteria such as minimizing distance, time, or energy (Liu et al. 2023a). This is a fundamental problem in a wide range of real-world applications, such as robot navigation (Carvalho and Aguiar 2025), automated vehicle parking (Jiang, Zhang, and Wang 2023), and player role planning in game or emulated training environments (Panov, Yakovlev, and Suvorov 2018). 

Existing algorithms such as A*, Dijkstra, and their variants are capable of finding the optimal path with the time complexity of _O_ ( _N_[4] _logN_ ) (Carlson et al. 2023), where _N_ is the edge length (grid number) of a 2D square grid map and _N_[2] is the total grid number of the map. Such algorithms 

- *Corresponding author 

work well for small-scale maps. However, in more scenarios, the need for path planning for large-scale grid maps boosts (Sun et al. 2024). An example is that, with the enhancement of robots’ capacities, their working space dramatically expands (Tang, Mao, and Ma 2025). Another example is that with the proliferation of high-resolution computer games, the game maps are increasingly complex (Lee and Lawrence 2013; Kirilenko et al. 2025). In such large-scale grid maps, the existing algorithms encounter a significant computation cost increase in both time and memory (Ou et al. 2022). In recent years, Large Language Models (LLMs) have achieved a remarkable milestone in addressing various planning tasks, inspired by their notable reasoning and planning capacities in complex contexts. Specifically, several works have utilized LLMs for path planning (Fan et al. 2025), which, however, suffer from spatial illusion (Aghzal, Plaku, and Yao 2024; Xie et al. 2024; Kwon, Di Palo, and Johns 2024) and result in unstable and limited planning performance. 

To achieve robust path planning, a state-of-the-art (SOTA) work (Meng et al. 2024) proposed LLM-A*, which combined the global insight of LLM with the robust planning capacity of A*. The basic idea of LLM-A* is that the LLM first generates a series of waypoints between the start and goal locations, then A* iteratively plans the paths between the neighbor waypoints, and finally, the whole path is constructed by connecting all the waypoints in sequence. In this way, A* does not need to explore the entire map when planning a path between each neighboring waypoints. Therefore, the overall computational and memory cost is reduced. However, when being applied for large-scale grid maps (with _N ≥_ 200), LLM-A* suffers from some critical limitations. First, the implementation of A* in LLM-A*, such as the grid cost query and collision detection, is inefficient, resulting in a long search time. Second, the global OPEN and CLOSED lists enconter high memory cost. Third, LLMs may stochastically generate some inappropriate waypoints. LLM-A* naively utilizes all waypoints for path planning, while some waypoints may be redundant and could be reduced for a better path. 

Motivated by LLM-A*, this work proposes an innovative LLM-enhanced path planning algorithm, abbr. as iLLM-A*. Specifically, iLLM-A* consists of three remarkable mechanisms. 1) **Optimization of A*** : To reduce the search time of A*, we first use a hash table to replace the linear CLOSED 


![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0002-00.png)


**----- Start of picture text -----**<br>
A* LLM-A*<br>8<br>600<br>6<br>400<br>4<br>200 2<br>0 0<br>50 100 150 200 250 300 350 50 100 150 200 250 300 350<br>Map Size (N) Map Size (N)<br>(a) Impact To Search Time            (b) Impact To Memory<br>Memory Peak (MB)<br>Search Time (seconds)<br>**----- End of picture text -----**<br>


Figure 1: Search Time and Memory of LLM-A* and A* Given Different Map Size. 

list of A* to store the explored grids for fast grid query, then update the evaluation values of a small portion (instead of all of the unexplored grids) of the OPEN list, and finally use an efficient two-stage collision detection to replace the precise collision detection to reduce the detection cost. 2) **Waypoint Generating by Incremental Learning based LLM** : We implement an incremental learning-based prompt, in which the Few-shot prompt is dynamically enriched, to guide the LLM to generate higher quality waypoints. 3) **Appropriate Waypoint Selection** : To address redundant LLM-generated waypoints, we employ an experience-driven method to select the appropriate subset of waypoints from the LLMgenerated waypoints for path planning. Finally, a comprehensive evaluation on various grid maps shows that, compared to LLM-A *, iLLM-A* **1) achieves more than** 1000 _×_ **speedup on average and up to** 2349 _._ 5 _×_ **speedup in extreme cases, 2) saves up to** 58 _._ 6% **of the memory cost, 3) achieves both obviously shorter path length and lower path length standard deviation.** 

## **2 Limitation Analysis for LLM-A*** 

We first test the performance of LLM-A* in large-scale grid maps. For simplicity, the work considers a 2D square grid map with equal edges, whose edge length (grid number) is denoted as _N_ . The evaluation settings are identical to those in Sec.4 and omitted here. Fig. 1 depicts the search time and memory of A* and LLM-A* given different map sizes, where the memory is the maximum occupied memory of the algorithm. As Fig. 1 (a) shows, LLM-A* achieves a slightly shorter search time than A*. In addition, when the map scales from _N_ = 200 to _N_ = 300, the computation time of LLM-A* exponentially increases from 30 _s_ to 7 _min_ , which shows the inefficiency of LLM-A* for large-scale maps. Fig. 1 (b) illustrates that the memory shows a similar increasing trend with search time. When the map scales from _N_ = 50 to _N_ = 300, whose area increases by (300 _/_ 50)[2] = 36 _×_ , the memory increases by 84 _._ 75 _×_ (62 _._ 5 _KB_ vs. 5 _._ 17 _MB_ ). The reasons for the inefficiency of LLM-A* are analyzed as follows. 

**Limitation 1: Inefficient Implementation of A*.** The A* in LLM-A* uses two linear data structures for the OPEN and CLOSED lists, respectively. The total time 

complexity of operating the OPEN list (including inserting and sorting the explored grids into the OPEN list) is _O_ ( _NwpNopenlogNopen_ ), where _Nwp_ is the number of waypoints generated by LLM and _Nopen_ is the length of the OPEN list. The total time complexity of checking whether the grids in OPEN are in CLOSED is _O_ ( _NopenNclosed_ ). Another key operation on the OPEN list is to detect the collision of the path from the grid with the lowest cost to the next waypoint, whose total complexity is _O_ ( _NopenNclosedNob_ ). Specifically, _Nob_ is the obstacle number. In summary, the total time complexity of A* in LLM-A* is _O_ ( _NwpNopenlogNopen_ + _NopenNclosedNob_ ). In the worst case, _Nopen_ and _Nclosed_ may approach _N_[2] . Thereafter, the time complexity of LLM-A* is consistent with that of A*, as verified in Fig.1 (a). 

**Limitation 2: Global High Memory Cost.** When planning the path between any two neighboring waypoints, A* needs to maintain a global OPEN list and a CLOSED list, which results in heavy memory cost. Therefore, the memory is only slightly lighter than that of A*, which is verified in Fig.1 (b). 

**Limitation 3: Inherent Limitation of LLM.** Some waypoints generated by LLM are stochastic and cannot precisely capture the objective of path planning, which is called the space illusion (Huang et al. 2023) of LLM. The space illusion may be caused by various factors, such as the training data, the training process, and the reasoning process. In the path planning task, LLM imitates the text syntax instead of exactly learning to find the shortest collision-free path. Therefore, LLM generates some inappropriate waypoints. Valmeekam et al. (Valmeekam et al. 2023) verified the ability of LLM in task planning. The work finds that the ratio of the most advanced LLM successfully planning a mission is only 12%, which shows the limited capacity of LLM and verifies that LLM may generate some redundant waypoints in the path-planning task. 

## **3 Design of iLLM-A*** 

With the limitations of LLM-A*, this section accordingly proposes an innovative design abbr. as iLLM-A*. We next introduce its three core mechanisms: (I) Optimization of A*, (II) Waypoint Generating by Incremental Learning-Based LLM, and (III) Appropriate Waypoint Selection. 

## **3.1 Optimization of A*** 

**Optimization of The CLOSED List.** We replace the traditional linear CLOSED list structure with a hash-based set to improve efficiency. The hash function directly maps each explored grid to its storage location, and thus significantly improves the search speed of A* (Sun et al. 2009). The hash-based structure reduces the complexity of the search operation on the CLOSED list from _O_ ( _Nclosed_ ) to _O_ (1) (Sun, Koenig et al. 2007). In this way, the search cost of planning the path by A* could be dramatically reduced in large-scale maps. 

**Optimization of The OPEN List.** The A* in LLM-A* utilizes a heuristic function to estimate the cost of each grid 


![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0003-00.png)


Figure 2: Two-Stage Collision Detection. 

to the destination: _f_ ( _s_ ) = _g_ ( _s_ )+ _h_ ( _s_ )+ _cost_ ( _s, swp_ ), where _s_ is the grid, _swp_ is a waypoint, _g_ ( _s_ ) is the cost from the start, _h_ ( _s_ ) is the estimated cost to the goal, and _cost_ ( _s, swp_ ) is the estimated cost from _s_ to _swp_ . The global OPEN list stores _f_ ( _s_ ) of all explored grids. When A* in LLM-A* plans a path between two new neighbor grids, _cost_ ( _s, swp_ ) is changed and _f_ ( _s_ ) in the OPEN list should be updated. However, the update overhead is huge due to the large size of the global OPEN list. iLLM-A* leverages a similar delayed heuristic update strategy (Sun et al. 2009). Specifically, iLLMA* only updates the heuristic function in the following two cases. Case 1: only the top- _k_ (i.e., _k_ = 100) grids with the lowest estimated function in the OPEN list are updated. Case 2: when we extract a grid from the OPEN list, its heuristic function is updated if its function is outdated, and the heuristic function _f_ ( _s_ ) is estimated using the current value. 

**Collision Detection Acceleration.** The precise collision detection in LLM-A* is time-consuming. We implement a two-stage collision detection method to reduce the computation overhead. Specifically, we use an Axis-Aligned Bounding Box (AABB) (Zhu, Zhang, and Pan 2024) to define the minimal rectangle with coordinate-aligned edges completely enclosing a path segment or an obstacle. The AABB edges are parallel to the map edges. The first stage detects potential collisions by testing the overlap of the AABBs of a path segment and an obstacle. Fig.2 (a) shows an example in which the two AABBs do not overlap and the path segment would not collide with the obstacle: _AABB_ ( _seg_ ) _∩ AABB_ ( _obs_ ) = _∅_ . If the two AABBs overlap with each other: _AABB_ ( _seg_ ) _∩ AABB_ ( _obs_ ) = _∅_ , a potential collision is detected, as the two examples in Fig.2 (b). The second stage conducts the same precise collision detection with LLM-A*. Since the AABBs are parallel to the map edge and a path segment does not collide with most of the obstacles, the two-stage method is much simpler and faster than the precise collision detection in LLM-A* (Zhu, Zhang, and Pan 2024), which dramatically reduces the total computational overhead for collision detection. 

## **3.2 Waypoint Generating by Incremental Learning-Based LLM** 

The traditional static Few-shot prompts of LLM could not effectively address new environments (Song et al. 2023), 

which results in over-fixed planning strategy. To address this issue, an incremental learning mechanism using the robust Few-shot adaptation capacity of LLMs is proposed. Guided by the prompt engineering practices for Qwen models (Long et al. 2025) and the Natural Language Processing principle (Liu et al. 2023b), the prompts for iLLMA* include 3 components: Prompt Template, Incremental Learning-Based Few-shot Example Augmentation, and Task Instructions. 

**Prompt Template.** The template first establishes the LLM’s role as a path planning specialist and specifies its fundamental goal to generate an optimal path given the start location, goal locations, and obstacles. Then the template incorporates the key constraints, including obstacle avoidance, minimum required waypoint number (iLLM-A* follows LLM-A* to set this number to 5), and preferences for geometrically optimal paths. Under these constraints, the generated path is required to approximate the geometrically shortest path. Thereafter, the template standardizes the input/output to follow the JSON format. Finally, the systematic reasoning processes are specified: 1) Using A* to find the collision-free shortest path; 2) Verifying the path point count; 3) Checking that all the constraints are being satisfied. A prompt example is presented in Tab.1. 

**Incremental Learning Based Few-shot Example Augmentation.** A Few-shot example repository contains multiple validated map-waypoints pairs that serve as in-context learning references. These examples undergo incremental updates based on the performance validation outcomes from a set of training maps. 

The incremental learning is to enrich the Few-shot example repository, which enables the LLM to progressively adapt its waypoint generation strategy to diverse environmental characteristics. Given a training map, the LLM generates the waypoints using the current prompt. Then the optimized A* algorithm subsequently searches the path using the waypoints. For clarity, the path is denoted as _πLLM_ . The optimal path from the start to the goal is also planned using the optimized A* as a baseline, which is denoted _πbase_ . The path length, search time, and memory of _πLLM_ are thereafter evaluated: 


![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0003-10.png)



![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0003-11.png)



![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0003-12.png)


where _Length_ ( _π_ ) is the path length, _Time_ ( _π_ ) is the search time, and _Memory_ ( _π_ ) is the maximum occupied storage for planning the path _π_ . If the path _πLLM_ satisfies Eq.(1)(3) simultaneously, the length of the planned path is within 1 + _θlength_ of the shortest path, and its search time cost and memory cost are lower than _θtime_ and _θmemory_ of the optimized A*, respectively. In iLLM-A*, the 3 thresholds 

## **Module I: Static Prompt Template** 

**# Role** You are an expert specializing in computational geometry and path planning. **# Goal** Generate an optimal path from start point to goal point based on the given start position, goal position, and obstacle information. 

|**# Constraints**|
|---|
|Strictly adhere to the following rules:|
|1.**Obstacle Avoidance**: The path must not contact or intersect any obstacles in any form.|
|2. **Path Point Count**: The fnal path must contain at least 5 coordinate points (including start and goal points). **Inter-**|
|**polation Rules**: If the initially calculated path contains fewer than 5 points, uniformly insert additional points between|
|the longest path segments until the quantity requirement is satisfed. Inserted points should ensure path smoothness and|
|avoid unnecessary sharp angles.|
|3. **Path Optimality**: Under the premise of satisfying all above constraints, the generated path should approximate the|
|geometrically shortest path.|
|**# Input and Output Format**|
|**Input**: Start pointstart:[x, y], Goal pointgoal:[x, y], Horizontal barriershorizontal<br>~~b~~arriers:[[y,|
|x<br>~~s~~tart, x<br>~~e~~nd], ...], Vertical barriersvertical<br>~~b~~arriers:[[x, y<br>~~s~~tart, y<br>~~e~~nd], ...]|
|**Output**: Must strictly follow the JSON array format: Generated Path: [[x1, y1], [x2, y2], ...,|
|[xN, yN]]|
|**# Workfow**|
|1.**Initial Pathfnding**: Based on A* algorithm logic, identify a shortest path that avoids all obstacles.|
|2.**Verifcation**: Check the path point count. If fewer than 5 points, add intermediate points according to Core Constraint|
|3.**Final Validation**: Before output,verifythat thegeneratedpath completelysatisfes all core constraints.|



Table 1: Static Prompt Template for LLM Waypoint Generation. 

|**Module II: Dynamic Few-shot Examples**||**Module III: Task Instructions**||
|---|---|---|---|
|**Input**:||Generate intermediate waypoints for the following input.||
|start: [94, 321]||If input data is ambiguous or constraint conditions con-||
|goal: [706, 668]||tain logical conficts, explicitly|identify the problematic|
|horizontal<br>~~b~~arriers: [[494, 166, 634], [474, 57, 386]]||areas. Ensure the path generation is completely based on||
|vertical<br>~~b~~arriers: [[247, 182, 632], [553, 387, 775]]||the provided input data. A path|that perfectly follows all|
|**Output**:||constraints will be considered a|successful response.|
|Generated Path: [[94, 321], [217, 211], [341, 275], [464,<br>387], [588, 421], [650, 544], [706, 668]]||Start Point:_{_start_}_<br>goal:_{_goal_}_||
|[10 In-context demonstrations abbreviated]||horizontal<br>~~b~~arriers:_{_horizontal|~~b~~arriers_}_|
|||vertical<br>~~b~~arriers:_{_vertical<br>~~b~~arriers_}_||
|Table 2: Few-shot Examples for In-context Learning.||Generated Path:||



Table 3: Task-Specific Instructions and Input Template. 

_θlength_ , _θtime_ , and _θmemory_ are set to 0 _._ 1, which means that the quality of the planned path (and the corresponding waypoints) is extremely high if Eq.(1)-(3) are true. Therefore, the map and the waypoints are incorporated into the Fewshot examples. In this way, the Few-shot example repository is augmented, and the LLM could learn high-quality planning instances and improve its capacity to generate highquality waypoints for new maps. In this work, we augment the Few-shot example repository with 10 training maps and the LLM-generated waypoints. If more training maps are available, the ones from the oldest training maps are replaced. Tab.2 shows a typical Few-shot example repository. 

**Task Instructions.** This component delivers explicit instructions for current planning queries, integrating specific environmental parameters (start location, goal location, and obstacles) with the template to activate problem-specific reasoning processes. An example of task instruction is presented in Tab.3. 

## **3.3 Appropriate Waypoint Selection** 

Even with incremental learning, LLM-generated waypoints may contain redundant or deviating ones that compromise the efficiency of the A* algorithm. Inspired by the work (Karaman et al. 2011), we develop an empirically validated 

|Metrics|Method|Number of Selected Waypoints|
|---|---|---|
|||1<br>2<br>3<br>4|
|Memory Score (_↑_)|Start<br>Uniform<br>Random<br>Goal|0.973<br>**0.984**<br>0.234<br>0.406<br>0.405<br>0.778<br>0.745<br>0.338<br>0.633<br>0.711<br>0.674<br>0.223<br>0.054<br>0.233<br>0.466<br>0.261|
|Time Score (_↑_)|Start<br>Uniform<br>Random<br>Goal|0.972<br>**0.982**<br>0.221<br>0.413<br>0.420<br>0.780<br>0.743<br>0.374<br>0.354<br>0.716<br>0.662<br>0.238<br>0.323<br>0.235<br>0.477<br>0.275|
|Path Length (%,_↑_)|Start<br>Uniform<br>Random<br>Goal|107<br>106<br>107<br>107<br>**105**<br>108<br>108<br>106<br>108<br>107<br>106<br>107<br>108<br>106<br>107<br>106|



Table 4: Waypoint Selection Performance Given Different Methods. **Bold** Values Indicate The Best Performance. 

method to select the appropriate subset of waypoints. 

**Empirical Study.** Similarly to LLM-A*, we make LLM generate at least 5 waypoints, the experiments demonstrate that excessive waypoints introduce extra computational overhead. We compare 4 waypoint subset selection methods: Uniform Selection (uniformly choosing some of the waypoints, abbr. as Uniform), Start-Prioritized Selection (prioritizing the waypoints closer to the start, abbr. as Start), Goal-Prioritized Selection (prioritizing the waypoints closer to the goal, abbr. as Goal), and Random Selection (randomly choosing some of the waypoints, abbr. as Random). With these methods, we choose 1-4 waypoints and compare their performance in Tab.4, with each experimental group repeated for 30 runs. The details of the score calculation are described in the Appendix. 

**Empirical Results Analysis.** Tab.4 shows the Start method achieves the highest scores of 0.973/0.984 for memory and 0.972/0.982 for time efficiency using 1-2 waypoints, while maintaining path path within only 6% _−_ 7% to the optimal path length. The performance of all the selection methods significantly degrades given _>_ 2 waypoints. 

**Waypoint Selection.** Inspired by the empirical results above, we select the appropriate waypoints as follows: If the number of the LLM-generated waypoints is not larger than 2, all waypoints are utilized for path planning; if the number exceeds 2, the first two waypoints closest to the start location are selected. 

## **4 Evaluation** 

## **4.1 Experiment Settings** 

**Grid Map Settings.** The evaluations are conducted on different kinds of square 2D grid maps. Specifically, we leverage the LLM to generate a series of maps whose edge length _N_ are _{_ 50 _,_ 100 _,_ 150 _,_ 200 _,_ 250 _,_ 300 _,_ 350 _,_ 400 _,_ 450 _}_ . For the smallest map ( _N_ = 50), we set the obstacle number to 3. For the larger ones, the obstacle number increases linearly with the map area. For example, the obstacle number of the 

|Metrics|Method|Map Size (_N_)|
|---|---|---|
|||200<br>250<br>300<br>350<br>400<br>450|
|Path Length (%)|iLLM-A*<br>w/o LLM<br>w/o IncL<br>w/o WDS<br>w/o Opt-A*|102.83 109.46 105.29 106.17 107.00 109.40<br>100.00 100.00 100.00 100.00 100.00 100.00<br>102.83 113.86 106.57 107.40 114.80 115.04<br>109.03 115.10 104.50 105.00 108.25 108.52<br>108.74 106.30 105.66 107.35 117.20<br>—|
|Search Time (s)|iLLM-A*<br>w/o LLM<br>w/o IncL<br>w/o WDS<br>w/o Opt-A*|**0.11**<br>**0.21**<br>**0.33**<br>**0.41**<br>**0.39**<br>**0.79**<br>0.50<br>0.66<br>1.62<br>2.83<br>3.75<br>9.05<br>0.12<br>0.21<br>0.33<br>0.47<br>0.59<br>0.96<br>0.13<br>0.39<br>1.50<br>3.04<br>2.49<br>4.33<br>27.04 54.17 173.54 278.96 381.96<br>—|
|Memory (MB)|iLLM-A*<br>w/o LLM<br>w/o IncL<br>w/o WDS<br>w/o Opt-A*|**1.02**<br>**1.57**<br>**2.14**<br>**2.23**<br>**2.54**<br>**3.62**<br>3.35<br>3.61<br>8.69<br>13.37 14.10 28.67<br>1.21<br>1.74<br>2.41<br>2.73<br>2.79<br>3.98<br>1.34<br>1.93<br>5.23<br>6.52<br>5.47<br>6.13<br>1.06<br>1.63<br>2.14<br>2.28<br>2.62<br>—|



Table 5: Ablation Study on Large-scale Maps. ”—” indicates Search Time _>_ 10 _min_ . 

map with _N_ = 450 is 3 _×_ (450 _/_ 50)[2] = 243. The width of the obstacle equals 1 grid, and the length of the obstacle is randomly distributed between 10 and 50 grids. The obstacles are randomly distributed in the map, which is randomly parallel to the vertical or horizontal edge of the map. To evaluate the robustness of iLLM-A* in diverse maps, we insert two new kinds of giant obstacles in the maps, which will be described in details in Sec.4.5. The numerical results are the average of 30 runs. 

**Baselines.** The evaluation includes 3 baselines: 

- **LLM-A*** : LLM-A* (Meng et al. 2024) represents the 

- SOTA method wherein the LLM generates intermediate waypoints to guide A* to search. 

- **A*** : The original A* algorithm employed in LLM-A*. 

- **Opt-A*** : The optimized A* in iLLM-A*. 

**Evaluation Metrics.** We compare iLLM-A* on 3 metrics. 

- **Path Length (%).** Since A* and Opt-A* could find the 

- shortest path, we normalized the length of the shortest path as 100%. The planned path by LLM-A* and iLLMA* should not be shorter than 100%. 

- **Search Time (s/seconds).** This is the time consumed by an algorithm for planning the path. 

- **Memory (MB).** This is the maximum storage needed for an algorithm when planning the path. 

**Environment.** We implement iLLM-A* and the baselines in Python on a server equipped with Intel Xeon Silver 4216 CPU, NVIDIA V100 GPU, and 128 GB RAM running Ubuntu with CUDA 550. Qwen2.5-32B is used as the LLM. 

|Map Size (_N_)|Performance Metrics|Performance Metrics|Performance Metrics|
|---|---|---|---|
||Search Time(s) _↓_|Memory (MB) _↓_|Path Length(%) _↓_|
||A*<br>Opt-A* LLM-A* iLLM-A*|A*<br>Opt-A* LLM-A* iLLM-A*|A*<br>Opt-A* LLM-A*<br>iLLM-A*|
|50<br>100<br>150<br>200<br>250<br>300<br>350<br>400<br>450|0.06<br>0.002<br>0.08<br>**0.001**<br>1.11<br>0.07<br>0.91<br>**0.04**<br>27.24<br>0.20<br>16.52<br>**0.11**<br>89.71<br>0.50<br>34.65<br>**0.11**<br>245.46<br>0.66<br>229.15<br>**0.21**<br>—<br>1.62<br>438.86<br>**0.33**<br>—<br>2.83<br>—<br>**0.41**<br>—<br>3.75<br>—<br>**0.39**<br>—<br>9.05<br>—<br>**0.79**|0.067<br>0.075<br>0.061<br>**0.059**<br>1.22<br>1.84<br>1.13<br>**0.64**<br>1.79<br>2.22<br>1.96<br>**0.98**<br>3.32<br>3.35<br>2.43<br>**1.02**<br>3.42<br>3.61<br>2.75<br>**1.57**<br>—<br>8.69<br>5.17<br>**2.14**<br>—<br>13.37<br>—<br>**2.23**<br>—<br>14.10<br>—<br>**2.54**<br>—<br>28.67<br>—<br>**3.62**|100.00<br>100.00<br>110.47<br>100.01<br>100.00<br>100.00<br>101.69<br>101.03<br>100.00<br>100.00<br>106.86<br>108.5<br>100.00<br>100.00<br>112.3<br>103.26<br>100.00<br>100.00<br>108.22<br>108.63<br>—<br>100.00<br>104.04<br>105.93<br>—<br>100.00<br>—<br>106.17<br>—<br>100.00<br>—<br>107.37<br>—<br>100.00<br>—<br>108.00|



Table 6: Performance Given Different Map Sizes. ”—” Indicates Search Time _>_ 10 _min_ . 


![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0006-02.png)


Figure 3: CDF of Path Length For LLM-A* and iLLM-A*. 

|Method<br>iLLM-A*<br>LLM-A*|MapSize (N)|
|---|---|
||50<br>100<br>150<br>200<br>250<br>300|
||**0.00**<br>**0.27**<br>**0.64**<br>**4.82**<br>**0.46**<br>**1.20**<br>0.63<br>1.67<br>3.06<br>7.97<br>5.56<br>3.46|




![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0006-05.png)


Figure 4: Basic Concept of the Two New Kinds of Obstacles. 

Table 7: Path Length Std on Different Map Sizes (%) _↓_ . 

## **4.2 Ablation Study** 

Tab.5 shows the Path Length, Search Time, and Memory of the variants on different map sizes. iLLM-A* outperforms all variants. Without LLM, the Search Time is obviously longer than that of iLLM-A* (e.g. 9 _._ 05 _s_ vs. 0 _._ 79 _s_ for the map with _N_ = 450). Without IncL, the average Path Length is 3 _._ 2% longer than that of iLLM-A*. Meanwhile, the maximum Path Length in the variant without Incl is 115 _._ 05%, which is much worse than that of iLLM-A*. Without WDS, both the performance on Search Time and Memory are obviously worse than that of iLLM-A*. Without Opt-A*, the Search Time is 270 _×_ to 1000 _×_ longer than that of iLLMA*. The ablation study shows the effectiveness of each designed mechanism in iLLM-A*. 

## **4.3 Overall Performance Comparison** 

Tab.6 demonstrates the comprehensive performance given different map sizes. iLLM-A* significantly outperforms all baselines in Search Time and Memory while maintaining acceptable path length. 

**Search Time Comparison.** iLLM-A* achieves substantial improvements in runtime performance with order-ofmagnitude speedups. Specifically, for maps with _N_ = 250 and _N_ = 300, iLLM-A* achieves 1091 _×_ (0 _._ 21 _s_ vs. 229 _._ 15 _s_ ) and 1330 _×_ (0 _._ 33 _s_ vs. 438 _._ 86 _s_ ) faster than LLM-A*, respectively. Besides, iLLM-A* achieves 11 _._ 5 _×_ (0 _._ 79 _s_ vs.9 _._ 05 _s_ ) speedup compared with Opt-A* given the map with _N_ = 450. 

**Memory Comparison.** The occupied memory of iLLM-A* is only 3.62 MB vs. 28.67 MB of Opt-A* on the map with _N_ = 450, representing 87 _._ 4% of memory reduction. iLLMA* saves 58 _._ 6% of the memory compared to LLM-A* on the map with _N_ = 300. This efficiency stems from our waypoint selection method that effectively reduces the exploration space of A*. 

**Path Length Comparison.** On average, the mean path length of LLM-A* and iLLM-A* is 107 _._ 94% and 104 _._ 39% given _N_ = 50 _,_ 100 _,_ 150 _,_ 200 _,_ 250 _,_ 300. Namely, iLLM-A* reduces the gap to the optimal path length by[7] _[.]_[94] 7 _.[−]_ 94[4] _[.]_[39] = 44 _._ 7% compared with LLM-A*, which means the path length of iLLM-A* is much closer to the optimal path. This is because the incremental learning and waypoint selection mechanisms generates higher-quality waypoints. 

|Map Size (_N_)|Performance Metrics|Performance Metrics|Performance Metrics|
|---|---|---|---|
||Search Time(s) _↓_|Memory (MB) _↓_|Path Length(%) _↓_|
||A*<br>Opt-A* LLM-A* iLLM-A*|A*<br>Opt-A* LLM-A* iLLM-A*|A*<br>Opt-A* LLM-A*<br>iLLM-A*|
|50<br>100<br>150<br>200<br>250<br>300<br>350<br>400<br>450|0.51<br>0.01<br>0.04<br>**0.002**<br>4.86<br>0.05<br>3.05<br>**0.01**<br>29.35<br>0.18<br>19.30<br>**0.10**<br>152.01<br>0.75<br>145.92<br>**0.12**<br>170.48<br>0.585<br>375.92<br>**0.16**<br>—<br>1.40<br>—<br>**0.37**<br>—<br>2.637<br>—<br>**0.842**<br>—<br>5.477<br>—<br>**0.605**<br>—<br>8.733<br>—<br>**0.800**|0.078<br>0.15<br>0.14<br>**0.07**<br>0.75<br>0.85<br>0.44<br>**0.30**<br>1.78<br>2.23<br>2.74<br>**1.11**<br>3.81<br>3.15<br>3.18<br>**1.34**<br>3.94<br>3.67<br>3.87<br>**1.56**<br>—<br>8.16<br>—<br>**2.45**<br>—<br>13.35<br>—<br>**3.23**<br>—<br>17.36<br>—<br>**3.28**<br>—<br>28.69<br>—<br>**3.37**|100.00<br>100.00<br>102.20<br>101.29<br>100.00<br>100.00<br>107.22<br>103.75<br>100.00<br>100.00<br>107.33<br>105.83<br>100.00<br>100.00<br>105.85<br>104.80<br>100.00<br>100.00<br>104.74<br>109.28<br>—<br>100.00<br>—<br>104.82<br>—<br>100.00<br>—<br>107.91<br>—<br>100.00<br>—<br>102.83<br>—<br>100.00<br>—<br>109.42|



Table 8: Performance For The Map With One Intermediate Cross-shaped Obstacle. 

|Map Size (_N_)|Performance Metrics|Performance Metrics|Performance Metrics|
|---|---|---|---|
||Search Time(s) _↓_|Memory (MB) _↓_|Path Length(%) _↓_|
||A*<br>Opt-A* LLM-A* iLLM-A*|A*<br>Opt-A*<br>LLM-A*<br>iLLM-A*|A*<br>Opt-A* LLM-A*<br>iLLM-A*|
|50<br>100<br>150<br>200<br>250<br>300<br>350<br>400<br>450|0.77<br>0.012<br>0.19<br>**0.003**<br>6.44<br>0.07<br>5.34<br>**0.027**<br>31.55<br>0.22<br>25.31<br>**0.11**<br>134.49<br>0.61<br>125.43<br>**0.13**<br>217.65<br>0.585<br>436.23<br>**0.27**<br>523.43<br>1.91<br>—<br>**0.27**<br>—<br>2.96<br>—<br>**0.50**<br>—<br>5.477<br>—<br>**0.58**<br>—<br>8.733<br>—<br>**0.76**|0.33<br>0.39<br>0.24<br>**0.15**<br>0.84<br>0.94<br>0.87<br>**0.56**<br>1.79<br>2.22<br>1.78<br>**1.05**<br>3.51<br>3.89<br>3.28<br>**1.12**<br>3.75<br>4.08<br>5.14<br>**2.11**<br>7.25<br>9.08<br>—<br>**2.08**<br>—<br>13.40<br>—<br>**2.38**<br>—<br>17.36<br>—<br>**2.64**<br>—<br>28.69<br>—<br>**2.89**|100.00<br>100.00<br>108.78<br>**100.00**<br>100.00<br>100.00<br>100.65<br>**100.83**<br>100.00<br>100.00<br>110.06<br>**107.67**<br>100.00<br>100.00<br>104.95<br>**109.11**<br>100.00<br>100.00<br>106.86<br>**108.41**<br>100.00<br>100.00<br>—<br>**103.20**<br>—<br>100.00<br>—<br>**105.22**<br>—<br>100.00<br>—<br>**107.75**<br>—<br>100.00<br>—<br>**108.54**|



Table 9: Performance For The Maps with Long Bar-shaped Obstacles. 

## **4.4 Stability Analysis** 

Given the maps with _N_ = 50 _,_ 100 _,_ 150 _,_ 200 _,_ 250 _,_ 300, the Cumulative Distribution Function (CDF) of the Path Length of LLM-A* and iLLM-A* is shown in Fig.3. All Path Lengths of iLLM-A* are shorter than 110%, while about 30% of the Path Lengths of LLM-A* are longer than 110%. To further verify the stability of iLLM-A*, Tab.7 illustrates the Path Length std in different sizes of maps. Clearly, the standard deviation of the Path Length of iLLM-A* is much smaller than that of LLM-A* for all map sizes, which shows that the length of the paths planned by iLLM-A* is more consistent and stable to the optimal path. 

## **4.5 Scalability Analysis** 

To show the robustness of iLLM-A*, we insert two new kinds of giant obstacles in the maps, as illustrated in Fig.4. Specifically, one giant cross-shaped obstacle lies in the intermediate region between the start of the goal, which forces the feasible paths to detour far from the straight line connecting the start and goal. The other kind of obstacle includes 3 long bar-shaped obstacles parallel to an edge, which force the feasible paths to detour multiple times. The length of the obstacles is randomly distributed within 50%-60% of the edge length. 

Tab.8 shows that iLLM-A* achieves near-linear scalabil- 

ity for the map with one intermediate giant obstacle, with search times scaling linearly with the map size, ranging from 0 _._ 002 _s_ to 0 _._ 800 _s_ across all map sizes. In contrast, LLM-A* cannot complete the planning tasks on the map with _N ≥_ 300. Specifically, given _N_ = 250, the Search Time of LLM-A* is 2349 _._ 5 _×_ longer than that of iLLM-A* (375 _._ 92 _s_ vs. 0 _._ 16 _s_ ). The Path Length consistently remains within 100% and 109 _._ 42%. The Memory of iLLM-A* is also only about half of that of LLM-A*. The results for maps with long bar-shaped obstacles are similar and are illustrated in Tab.9. For maps with _N_ = 200 _,_ 250, the search time of LLM-A* is about 1000 _×_ longer than that of iLLM-A*. The results are consistent with those in Tab.6, which shows the robustness of iLLM-A* in diverse maps, even with unseen giant obstacles in the Few-shot examples. 

## **5 Conclusion** 

In this paper, we present an innovative LLM-enhanced algorithm for path planning in large-scale grid maps. We first use both test and theoretical analysis to reveal the limitations of the SOTA LLM-enhanced algorithm. Then we propose the innovative design consisting of 3 core mechanisms to address these limitations: Optimization of A*, Waypoint Generating By Incremental Learning LLM, and Appropriate Waypoint Selection. Finally, a comprehensive evaluation on 

various grid maps shows that, compared with SOTA method, iLLM-A* **1) achieves more than** 1000 _×_ **speedup on average, 2) saves up to** 58 _._ 6% **of the memory cost, 3) achieves both obviously shorter path length and lower path length standard deviation.** 

## **References** 

Aghzal, M.; Plaku, E.; and Yao, Z. 2024. Can Large Language Models be Good Path Planners? A Benchmark and Investigation on Spatial-temporal Reasoning. In _ICLR 2024 Workshop on Large Language Model (LLM) Agents_ . 

Carlson, M.; Moghadam, S. K.; Harabor, D. D.; Stuckey, P. J.; and Ebrahimi, M. 2023. Optimal pathfinding on weighted grid maps. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 37, 12373–12380. 

Carvalho, J. P.; and Aguiar, A. P. 2025. Deep reinforcement learning for zero-shot coverage path planning with mobile robots. _IEEE/CAA Journal of Automatica Sinica_ . 

Fan, H.; Liu, X.; Fuh, J. Y. H.; Lu, W. F.; and Li, B. 2025. Embodied intelligence in manufacturing: leveraging large language models for autonomous industrial robotics. _Journal of Intelligent Manufacturing_ , 36(2): 1141–1157. 

Huang, L.; Yu, W.; Ma, W.; Zhong, W.; Feng, Z.; Wang, H.; Chen, Q.; Peng, W.; Feng, X.; Qin, B.; and Liu, T. 2023. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. _ACM Transactions on Information Systems_ , 43: 1 – 55. 

Jiang, Z.; Zhang, X.; and Wang, P. 2023. Grid-map-based path planning and task assignment for multi-type AGVs in a distribution warehouse. _Mathematics_ , 11(13): 2802. 

Karaman, S.; Walter, M. R.; Perez, A.; Frazzoli, E.; and Teller, S. 2011. Anytime motion planning using the RRT. In _2011 IEEE international conference on robotics and automation_ , 1478–1483. ieee. 

Kirilenko, D.; Andreychuk, A.; Panov, A. I.; and Yakovlev, K. 2025. Generative models for grid-based and image-based pathfinding. _Artificial Intelligence_ , 338: 104238. 

Kwon, T.; Di Palo, N.; and Johns, E. 2024. Language models as zero-shot trajectory generators. _IEEE Robotics and Automation Letters_ , 9(7): 6728–6735. 

Lee, W.; and Lawrence, R. 2013. Fast grid-based path finding for video games. In _Canadian Conference on Artificial Intelligence_ , 100–111. Springer. 

Meng, S.; Wang, Y.; Yang, C.-F.; Peng, N.; and Chang, K.W. 2024. LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning. _Findings of EMNLP_ . 

Ou, Y.; Fan, Y.; Zhang, X.; Lin, Y.; and Yang, W. 2022. Improved A* path planning method based on the grid map. _Sensors_ , 22(16): 6198. 

Panov, A. I.; Yakovlev, K. S.; and Suvorov, R. 2018. Grid path planning with deep reinforcement learning: Preliminary results. _Procedia computer science_ , 123: 347–353. 

Song, C. H.; Wu, J.; Washington, C.; Sadler, B. M.; Chao, W.-L.; and Su, Y. 2023. Llm-planner: Few-shot grounded planning for embodied agents with large language models. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 2998–3009. 

Sun, X.; Koenig, S.; et al. 2007. The Fringe-Saving A* Search Algorithm-A Feasibility Study. In _IJCAI_ , volume 7, 2391–2397. 

Sun, X.; Yeoh, W.; Chen, P.-A.; and Koenig, S. 2009. Simple optimization techniques for A*-based search. In _Proceedings of The 8th International Conference on Autonomous Agents and Multiagent Systems-Volume 2_ , 931–936. 

Sun, Y.; Tong, X.; Lei, Y.; Guo, C.; Lei, Y.; Song, H.; An, Z.; Tang, J.; and Wu, Y. 2024. A multi-scale path-planning method for large-scale scenes based on a framed scaleelastic grid map. _International Journal of Digital Earth_ , 17(1): 2383852. 

Tang, J.; Mao, Z.; and Ma, H. 2025. Large-scale multirobot coverage path planning on grids with path deconfliction. _IEEE Transactions on Robotics_ . 

Valmeekam, K.; Marquez, M.; Sreedharan, S.; and Kambhampati, S. 2023. On the planning abilities of large language models-a critical investigation. _Advances in Neural Information Processing Systems_ , 36: 75993–76005. Xie, J.; Zhang, K.; Chen, J.; Zhu, T.; Lou, R.; Tian, Y.; Xiao, Y.; and Su, Y. 2024. TravelPlanner: a benchmark for real-world planning with language agents. In _Proceedings of the 41st International Conference on Machine Learning_ , ICML’24. JMLR.org. 

Zhu, A.; Zhang, Z.; and Pan, W. 2024. Developing a fast and accurate collision detection strategy for crane-lift path planning in high-rise modular integrated construction. _Advanced Engineering Informatics_ , 61: 102509. 

Liu, L.; Wang, X.; Yang, X.; Liu, H.; Li, J.; and Wang, P. 2023a. Path planning techniques for mobile robots: Review and prospect. _Expert Systems with Applications_ , 227: 120254. 

Liu, P.; Yuan, W.; Fu, J.; Jiang, Z.; Hayashi, H.; and Neubig, G. 2023b. Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing. _ACM computing surveys_ , 55(9): 1–35. 

Long, D. X.; Dinh, D.; Nguyen, N.-H.; Kawaguchi, K.; Chen, N. F.; Joty, S.; and Kan, M.-Y. 2025. What Makes a Good Natural Language Prompt? _arXiv preprint arXiv:2506.06950_ . 

## **A Appendix: Metric Computation and Normalization** 

The experimental evaluation implements a two-stage metric computation process involving raw data aggregation and normalization-based scoring procedures. 

**Raw Metric Aggregation** : The system calculates the arithmetic mean of the three performance metrics across 30 trials for each strategy-count-map combination. 

**Normalization for Cost-Type Metrics** : Search time and memory constitute cost-type indicators where lower values demonstrate superior performance. The normalization process applies the following mathematical transformation for each map scale: 


![](1_survey/papers/md/Zeng2025times_figs/Zeng2025times.pdf-0009-04.png)


where _xcurrent_ represents the mean performance value for the specific strategy-count combination, _xmax_ denotes the maximum value across all strategies for the given map scale, and _xmin_ represents the corresponding minimum value. This transformation maps performance values to a [0,1] scale where values approaching 1.0 indicate optimal performance characteristics. 

**Final Score Calculation** : The system computes the final score for each cost-type metric by averaging the normalized scores across all map scales, ensuring balanced representation across different complexity levels. 

**Path Length Evaluation** : The path length assessment calculates the Path Length as a percentage of the optimal A* solution for each individual trial, subsequently computing the mean Path Length across all trials and map scales for each strategy-count combination. Values approaching 100% indicate superior path quality performance. 

