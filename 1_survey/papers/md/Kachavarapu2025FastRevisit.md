---
citation_key: Kachavarapu2025FastRevisit
arxiv_id: 2501.07343
arxiv_url: "https://arxiv.org/abs/2501.07343"
title: "Fast-Revisit Coverage Path Planning for Autonomous Mobile Patrol Robots Using Long-Range Sensor Information"
authors_short: "Srinivas Kachavarapu et al."
year: 2025
direction_tag: G_subgoal_optimization
source: pymupdf4llm
converted_at: 2026-06-23T17:58:37Z
origin: ai+web
reviewed: false
---

# Fast-Revisit Coverage Path Planning for Autonomous Mobile Patrol Robots Using Long-Range Sensor Information 

Srinivas Kachavarapu _Human-Centered Robotics Lab Ostfalia University of Applied Sciences_ Wolfenbuettel, Germany 0009-0002-4495-8539 

Tobias Doernbach Reinhard Gerndt _Human-Centered Robotics Lab Human-Centered Robotics Lab Ostfalia University of Applied Sciences Ostfalia University of Applied Sciences_ Wolfenbuettel, Germany Wolfenbuettel, Germany 0000-0001-6488-8211 0000-0001-6415-9481 

_**Abstract**_ **—The utilization of Unmanned Ground Vehicles (UGVs) for patrolling industrial sites has expanded significantly. These UGVs typically are equipped with perception systems, e.g., computer vision, with limited range due to sensor limitations or site topology. High-level control of the UGVs requires Coverage Path Planning (CPP) algorithms that navigate all relevant waypoints and promptly start the next cycle.** 

**In this paper, we propose the novel** _**Fast-Revisit Coverage Path Planning**_ **(** _**FaRe-CPP**_ **) algorithm using a greedy heuristic approach to propose waypoints for maximum coverage area and a random search-based path optimization technique to obtain a path along the proposed waypoints with minimum revisit time. We evaluated the algorithm in a simulated environment using Gazebo and a camera-equipped TurtleBot3 against a number of existing algorithms. Compared to their average path lengths and revisit times, our** _**FaRe-CPP**_ **algorithm showed a reduction of at least 21% and 33%, respectively, in these highly relevant performance indicators.** 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0001-06.png)


Fig. 1: Proposed _FaRe-CPP_ algorithm example path (red) featuring minimum revisit times and maximum sensor coverage area 

_**Index Terms**_ **—Motion and Path Planning, Reactive and SensorBased Planning, Vision-Based Navigation, Surveillance Systems, Industrial Robots** 

## I. INTRODUCTION 

Robots autonomously patrolling environments like industrial, manufacturing, construction or agricultural sites are supposed to conduct efficient surveillance by covering a maximum area in minimum time. In order to ensure this, a number of Coverage Path Planning (CPP) approaches exist that compute paths passing through all predefined or computed waypoints while covering the area of interest in the least time and with the least spatial effort. Robots rely on CPP to ensure efficient coverage, which is essential for optimal performance and safety in many applications. These algorithms can be categorized into online and offline approaches [1] where online approaches generally assume little to no prior knowledge about the environment and often use heuristics to ensure maximum coverage. Offline approaches utilize pre-recorded maps of the environment, making them well-suited for largescale areas. By leveraging hardware capabilities, all these approaches can ensure an efficient path that maximizes area 

coverage. Furthermore, CPP algorithms are categorized based on various factors, including the environment type (indoor, outdoor), dimensionality (2D occupancy maps, 3D occupancy maps), and the platform (unmanned ground (UGV) or aerial (UAV) vehicles). Additionally, multi-robot CPP approaches exist [2] which are more efficient for large areas due to task division and faster coverage, but require complex coordination and may not be applicable in all scenarios. 

Ensuring minimum revisit times of any given waypoint is crucial for certain application, for instance, safety patrol on hazardous substance sites like garbage dumps and recycling centers. Typically, in such sites, spontaneous fires are an imminent hazard because of inflammable substances or selfignition because of the heat produced during composting. Therefore, fire incidents happen frequently [3], [4] and there is great interest by waste disposal enterprises to prevent such incidents. A safety patrol robot that is able to detect fires autonomously, and potentially even applies extinguishing agents directly, calls the fire department and keeps the fire at bay until their arrival. For such kind of patrols, minimum revisit times with maximum coverage are essential to prevent 

fires from getting out of control. 

In this paper, we present a novel Coverage Path Planning algorithm with focus on fast revisit times for a single mobile patrol robot. We name the algorithm _Fast-Revisit Coverage Path Planning_ ( _FaRe-CPP_ ). Utilizing a pre-recorded 2D occupancy grid map, our approach updates the surveilled region within the field of view of the relevant onboard sensors at each step, subsequently creating waypoints that maximize the coverage area. Initially generated with a greedy heuristic for maximum perception potential, these waypoints are optimized using the GRASP method [5] to minimize path length while preserving coverage information. Extending existing work from the literature, our approach ensures minimal revisit times as its key contribution. This is achieved by a combination of waypoint generation and optimization which results in maximum overall area coverage with no path overlap and minimal path length. 

**A Python implementation of** _**FaRe-CPP**_ with ROS[1] connectivity for rapid deployment in real-life scenarios **is publicly available on https://github.com/hcr-lab/fare-cpp** . 

## II. RELATED WORK 

## _A. Basic Coverage Path Planning Methods and Applications_ 

Coverage Path Planning (CPP) is essential for robot applications like vacuum cleaning [6], radiation monitoring [7], bridge inspection [8], emergency evacuation [3], and construction monitoring [9]. 

Earlier researchers implemented decomposition approaches for CPP, including exact cellular [10], [11], trapezoidal [12], Boustrophedon [13], and Morse-based [14] decomposition which divides free space into navigable cells, optimizing systematic path coverage through various cell partitioning and merging techniques. Miao et al. [15] propose a scalable CPP method for cleaning robots using rectangular map decomposition, simplifying the planning process for large-scale applications. These decomposition methods focus on the robot’s physical footprint rather than sensor ranges, such as camera fields of view, which are vital for scanning environments and therefore an essential part of _FaRe-CPP_ . Decomposition methods create zig-zag patterns and are less suited for patrolling robots, as they might disrupt ongoing activities. Gabriely et al. [16] discuss the Spanning Tree Covering algorithm, one of the first grid-based algorithms for CPP. 

Latest methods in Coverage Path Planning move beyond merely partitioning areas and integrate both operational aspects and sensor capabilities into the area decomposition process [8], [17]–[24]. For instance, Swain et al. [17] introduced an efficient path-planning algorithm for 2D ground area coverage using multi-UAVs, emphasizing the integration of sensor capabilities into the planning process. Mansouri et al. [18] developed a method for 2D visual area coverage and path planning that couples the robot’s path with the camera footprints like our approach, enhancing the fidelity of CPP by considering visual sensor constraints. Similarly, Ghaddar et 

> 1Robot Operating System, https://ros.org 

al. [19] presented an energy-aware grid-based CPP for UAVs, incorporating area partitioning in the presence of no-fly zones, which highlights the importance of operational constraints in path planning. Phung et al. [8] proposed an enhanced discrete particle swarm optimization algorithm for UAV vision-based surface inspection, demonstrating the benefits of considering sensor footprints for efficient inspection tasks. Kantaros et al. [23] explored distributed coverage control for concave areas, considering visibility sensing constraints, further highlighting the need to integrate sensor capabilities into the CPP process. An et al. [25] introduced the Rainbow Coverage Path Planning (RCPP) method for patrolling mobile robots with circular sensing ranges, optimizing the path to minimize overlap in sensing regions and enhance patrolling efficiency. 

However, none of the mentioned methods considers fast revisit times for time-critical patrol operations as is the focus of our approach. 

## _B. Established Practical Implementations of Coverage Path Planning_ 

Building upon the significant advancements in Coverage Path Planning techniques, certain studies have not only concentrated on theoretical models but have also ventured into practical implementations and analyses through software tools. The early work of Bormann et al. [34] provides an exploration of segmented rooms with a set of suitable map division algorithms. Following this foundational work, they presented a comprehensive survey alongside the implementation and analysis of various indoor CPP methods [35]. We are using several of the analyzed methods as baseline for our approach, as described in detail in Section IV-D. 

## _C. Coverage Path Planning for Environmental Operations_ 

Tran et al. [21], [22], [24] contributed to the dynamic and robust multi-robot coverage of both known and unknown environments through frontier-led swarming techniques. These methods underscore the importance of dynamic adaptation and sensor integration in CPP like our camera-based approach. Talavera et al. [27] developed an autonomous ground robot to support firefighters in indoor emergencies. This robot utilizes advanced CPP algorithms to navigate complex indoor environments, detect fires, and provide real-time situational awareness to firefighting teams, demonstrating the practical utility of CPP in critical firefighting applications like we target with our work. Nasirian et al. [28] addressed the challenge of effectively covering and disinfecting an environment with mobile robots using a graph-based representation like we use in our approach. Similarly, Pierson et al. [29] focused on deploying a mobile UVC disinfection robot with an optimized CPP algorithm. Perminov et al. [30] presented a genetic-based human-aware CPP algorithm for autonomous disinfection robots, achieving significant coverage efficiency. These hygiene-optimizing robot applications are similar to our firefighting approach in the sense that they profit from fast revisit times and are deployed on robots that are to treat the environment. 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0003-00.png)


Fig. 2: Fast-Revisit Coverage Path Planning ( _FaRe-CPP_ ) 

## III. PROPOSED APPROACH: FAST-REVISIT COVERAGE PATH PLANNING ( _FaRe-CPP_ ) 

In this section, we discuss in detail the methodology of our novel Fast-Revisit Coverage Path Planning ( _FaRe-CPP_ ) algorithm. Our main assumption is that the environment is represented as an occupancy map recorded using Simultaneous Localization and Mapping (SLAM) (see Section IV-A). The grid cells in the occupancy map fall into one of three categories: occupied, unoccupied, and unknown. 

In _FaRe-CPP_ , instead of considering the robot’s physical dimensions as the footprint, we utilize the field of view (FoV) of the range sensor, e.g. 2D camera, mounted on the robot as the footprint. The range within which the sensor can perceive range information is referred to as the sensor range. The grid cells within the FoV are then referred to as explored cells, and the center cell is considered the robot’s position (x, y) while the orientation ( _θ_ ) is obtained based on the direction of the robot relative to the coordinate system of the grid map. As visually summarized in Fig. 2, there are four main steps in _FaRe-CPP_ which we describe in the next subsections. 

## _A. Step 1: Waypoint Candidate Generation_ 

The algorithm begins with the waypoint generation, where the robot’s initial position is used as the first waypoint. The robot’s initial FoV is then calculated based on its orientation and sensor range. For each grid cell ( _xc, yc_ ) within the sensor range _r_ , the angle _α_ is determined using _α_ = atan2( _yc − yr, xc − xr_ ). If _α_ lies within the FoV range and is not blocked by an obstacle (checked using the Bresenham line algorithm [36]), the cell ( _xc, yc_ ) is marked as explored. 

After updating the grid cells within the FoV to the explored region, the boundary cells that separate the explored region from the unoccupied region as shown in Fig. 3 serve as waypoint candidates _Wc_ = _{wc_ 1 _, wc_ 2 _, . . . , wcn}_ . These waypoint candidates represent possible future positions for the robot from which the next actual waypoint is selected Step 2. 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0003-08.png)


Fig. 3: Explored region updated within the field of view (dark gray area) and boundary waypoint candidates _Wc_ (blue line) separating the explored from the unoccupied region 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0003-10.png)



![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0003-11.png)



![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0003-12.png)


**----- Start of picture text -----**<br>
(a) Sub grid map G ( wc 1) (b) Sub grid map G ( wc 2)<br>(c) Sub grid map G ( wc 3) (d) Sub grid map G ( wc 4)<br>**----- End of picture text -----**<br>


Fig. 4: Exemplary sub grid maps generated for four of the boundary waypoint candidates _{wc_ 1 _, wc_ 2 _, wc_ 3 _, wc_ 4 _} ∈ Wc_ from Fig. 3 

## _B. Step 2: Coverage Area Estimation per Waypoint Candidate_ 

After generating all waypoint candidates using the waypoint generation step, the coverage area _A_ ( _wc_ ) is estimated for each waypoint candidate _wc ∈ Wc_ : 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0003-16.png)


where _i_ and _j_ represent the cell indices in the sub grid map _G_ ( _wc_ ), _r_ represents the side length of each quadratic cell so that _r_[2] indicates the physical area of each cell, and _A_ ( _wc_ ) represents the explored area of each sub-grid map with the respective waypoint candidate selected as next actual waypoint. 

Separate sub grid maps _G_ ( _wc_ ) per waypoint candidate are created, and the unoccupied region is updated to the explored region like in Fig. 4 as discussed in Step 1. The coverage area for each grid map with the respective candidate as next waypoint is computed. 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0004-00.png)


Fig. 5: _FaRe-CPP_ waypoints (blue), explored region (light gray), path before Waypoint Optimization (dark gray) and final resulting path after Waypoint Optimization (red) 

## _C. Step 3: Waypoint Selection by Maximum Coverage Area_ 

After the coverage area has been computed for each waypoint candidate, the candidate with the potential of providing the maximum FoV is selected as the next waypoint _w_ with 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0004-04.png)


The sub-grid map of this waypoint is then used in the next iteration where new waypoint candidates are generated. 

The _FaRe-CPP_ algorithm repeats Steps 1–3 until the stopping criterion is met. This is the case when no more waypoint candidates are available, a predefined minimum coverage area _A_ min has been exceeded, or the rate of increase in the coverage area across iterations[∆] _[A][i]_ is less than a threshold _ϵ_ : _Ai_ 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0004-07.png)


Our waypoint selection strategy ensures that at every iteration, we select a waypoint globally from all possible candidates. By evaluating coverage potential over the entire set of waypoint candidates, we prevent the risk of the algorithm converging to a suboptimal local minimum. 

## _D. Step 4: Waypoint Optimization_ 

So far, the _FaRe-CPP_ algorithm focuses on incrementally expanding the coverage area by selecting waypoints that maximize the coverage area at each iteration, rather than minimizing the overall path length. As a result, the waypoints are not arranged in an optimal sequence, leading to inefficient, overlapping, or zigzagging paths. This disorganization is since the waypoints are obtained in The waypoint generation step purely based on coverage needs, not on path efficiency. To balance extensive coverage with path efficiency, we employ the Greedy Randomized Adaptive Search Procedure (GRASP) [5]. GRASP operates in two phases: 1.) initial greedy randomized construction, which builds a path by selecting from top candidates, introducing randomness to avoid local optima, 

followed by 2.) local search, which refines the path using the 2-opt swap strategy to minimize cumulative distance. 

To avoid computational complexity, the environment map is also not considered during waypoint optimization. The optimization focuses only on ordering the waypoints, while path planning that takes the environment into account is done in the next step. GRASP optimizes the waypoints such that the global path that passes through the waypoints bears the least cumulative distance, as shown in Fig. 5. However, due to the introduction of randomness in the greedy construction phase and the iterative nature of the 2-opt swap strategy, there is some variability in the resulting global path. While the global path is optimized, the exact distance can vary slightly across different runs due to the stochastic elements of the algorithm. Despite this, GRASP consistently arranges waypoints with reduced cumulative distance and improved efficiency. 

## _E. Path Planning and Following_ 

After generating and optimizing waypoints, they are used to plan a global path. In this case, the A* algorithm [37] is employed to find a path that passes through these waypoints. A* is a graph-based search algorithm that finds the shortest path from a start point to a goal, considering the cost of movement between points. The result is a global path that connects the waypoints while maintaining alignment with the range sensors field of view. This path, which forms a closed loop through all waypoints, can be utilized by and path following approach to locomote the robot accordingly. In the implementation of our example scenario as used in the following experimental evaluation, we use the Dynamic Window Approach (DWA) from the ROS navigation stack for local path planning. 

## IV. EVALUATION 

## _A. Experimental Setup_ 

We conducted all experiments in a simulation environment using ROS Noetic, Gazebo, and a camera-equipped TurtleBot3. We first created an occupancy grid map using the SLAM technique with the GMapping package [38]. We selected two environments from AWS RoboMaker: The House world[2] for comparison with algorithms designed for smaller environments and the Warehouse world[3] for larger environments like warehouses or recycling centers. 

The occupancy grid map of the House environment has dimensions of 500x500 grid cells with a resolution of 0 _._ 05 m _/_ cell, resulting in an unoccupied coverage area of 157 m[2] , whereas the Warehouse environment has 380x640 grid cells with a resolution of 0 _._ 05 m _/_ cell and an unoccupied coverage area of 232 m[2] . 

## _B. Evaluation Metrics_ 

We evaluated the performance of _FaRe-CPP_ on the generated grid map using several key metrics, chosen to compre- 

> 2https://github.com/aws-robotics/aws-robomaker-small-house-world 

> 3https://github.com/belal-ibrahim/dynamic logistics warehouse 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0005-00.png)


Fig. 6: _FaRe-CPP_ on Warehouse environment – waypoints (blue), explored region (light gray), path before Waypoint Optimization (dark gray) and final resulting path after Waypoint Optimization (red) 

hensively assess the algorithm’s efficiency and effectiveness in selected environments: 

- **Path Length** _lp_ : This metric measures the total distance traveled by the robot in a closed loop, starting and ending at the first waypoint. It provides insight into the efficiency of the generated path, with shorter paths being more optimal with respect to minimum revisit times. 

- **Total Cumulative Rotation** _θ_ total: This is calculated based on the robot’s orientation changes at each waypoint. While maintaining maximum coverage, this should be minimized in order to achieve fast revisit times. 

- **Revisit Time** _t_ revisit: Revisit time measures the duration required for the robot to complete its patrol loop and return to the starting point for subsequent patrols. It is determined as _t_ revisit = _v_ linear _lp_[+] _v_ angular _θ_ total[with] _[v]_[linear][as] the actual linear and _v_ angular as the actual angular robot velocity. 

- **Coverage Area** : Percentage of the environment’s floor plan covered by the sensor’s field of view. 

- **Computation Time** : Total time to compute the final resulting path. 

## _C. Results_ 

As range sensors, we employ wide-angle cameras with FoVs of 90 _[◦]_ and 120 _[◦]_ on the Warehouse map, each with a 5-meter sensor radius. We use this radius as a conservative estimate to prove our algorithm’s utility because typical low-cost sensors as used on patrol robots have a 5 m to 10 m range. Table I shows that the 120 _[◦]_ FoV outperforms the 90 _[◦]_ FoV, with shorter computation time (149 s vs. 178 s), better coverage (96 % vs. 94 %), and reduced cumulative rotation. These results demonstrate the effectiveness of _FaRe-CPP_ in large environments like the Warehouse, see Fig. 6. The algorithm achieves high coverage and minimizes cumulative rotation, contributing to efficient sensor usage. Importantly, the similar revisit times (421 s for 90 _[◦]_ FoV and 419 s for 120 _[◦]_ FoV) indicate that _FaRe-CPP_ maintains consistent performance without 

TABLE I: _FaRe-CPP_ quantitative results with FoV (90 _[◦]_ ,120 _[◦]_ ) 

|LE I:_FaRe-CPP_quantitative|results wit|h FoV (90_◦_,1|
|---|---|---|
|**Metric**|**FoV(**90_◦_**)**|**FoV(**120_◦_**)**|
|Path Length (m)|100.95|102.15|
|Total Cumulative Rotation (rad)|43.98|40.84|
|Revisit Time (s)|421|419|
|Coverage Area (%)|94|96|
|Computation Time (s)|178|149|



unnecessary re-exploration, making it well-suited for largescale applications where extensive coverage and minimized redundancy are critical. 

## _D. Comparison with Existing Algorithms_ 

We evaluate the effectiveness of our proposed _FaRe-CPP_ algorithm through qualitative comparisons (Fig. 7) and quantitative metrics (Table II) against existing camera foot print-based methods. As baselines, we utilize the algorithms evaluated in Bormann et al. [35] as implemented in their publicly available framework[4] , which represent the state of the art in coverage path planning. For consistency and fairness, we adopt the sensor parameters specified in their work: an RGB-D sensor mounted at 65 cm height, facing downward, with a trapezoidal field of view (FoV) with a 70 cm (closest edge, 15 cm from the robot center) to 1.3 m (farthest edge, 1.15 m from the robot center). This setup yields a horizontal FoV of 58 _._ 4 _[◦]_ , a vertical FoV of 47 _._ 4 _[◦]_ , and a sensor range of 1.3 m. In addition, we evaluate the optimal parameter set for our approach, which assumes a sensor parallel to the floor, producing a conical FoV constrained by a horizontal field of view and sensing range of 1.3 m . To enable a direct comparison, we evaluate _FaRe-CPP_ under these two configurations: (1) with parameters matching Bormann et al.’s [35] setup, and (2) optimized for long-range efficiency, our primary objective. 

As the results show in Fig. 7, _FaRe-CPP_ achieves more efficient coverage in both configurations with fewer overlaps and a more streamlined path compared to the other methods. Table II quantitatively supports these findings, which shows averages for 10 comparison runs. _FaRe-CPP_ exhibits the shortest path length, lowest total cumulative rotation, and fastest revisit time while maintaining a high coverage area percentage. 

In total, compared to the average of the baseline approaches, our algorithm achieves a reduction in path length of 21% for similar and 42% for long range-optimized parameter settings. This results in a reduced revisit time of 33% for similar and 57% for long range-optimized parameter settings. These metrics highlight the performance of _FaRe-CPP_ in achieving near-optimal coverage with fast revisit times for subsequent patrolling, which is an essential requirement for the targeted use cases. 

With respect to computing time, _FaRe-CPP_ currently lags behind other algorithms except for Grid TSP. To ensure consistent comparison, all methods use the same GRASP-based waypoint optimization, implemented uniformly in Python. The 

> 4https://github.com/ipa320/ipa coverage planning 


![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0006-00.png)



![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0006-01.png)



![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0006-02.png)



![](1_survey/papers/md/Kachavarapu2025FastRevisit_figs/Kachavarapu2025FastRevisit.pdf-0006-03.png)


**----- Start of picture text -----**<br>
(a) Grid-based TSP [35] (b) Boustrophedon [13] (c) Neural Network-based [39]<br>(d) Convex SPP [40] (e) Contour Line [35] (f) Grid local Energy [41]<br>(g) Proposed FaRe-CPP (h) Proposed FaRe-CPP<br>(Bormann et al. [35] parameters) (optimized for long-range efficiency)<br>**----- End of picture text -----**<br>


Fig. 7: Qualitative results for paths generated by existing approaches and _FaRe-CPP_ – waypoints (blue), path before Waypoint Optimization (gray) and final resulting path after Waypoint Optimization (red) 

TABLE II: Quantitative average results for 10 comparison runs between existing approaches and _FaRe-CPP_ 

|**Algorithm**|**Comp. Time (s)**|**Path Length (m)**|**Total Rotation (rad)**|**Coverage Area (%)**|**Revisit Time (s)**|
|---|---|---|---|---|---|
|Grid TSP [35]|148|297.45|544|**97**|2037|
|Boustrophedon [13]|4|209.79|302|76|1280|
|Neural Network [39]|8|293.69|795|92|2507|
|Convex SPP [40]|17|**171.60**|347|92|1239|
|Grid Local Energy [41]|**1.7**|261.34|322|95|1490|
|Contour Line [35]|71|283.74|574|**97**|2049|
|**Proposed** **_FaRe-CPP_**<br>(Bormann et al. [35] parameters)|274 _±_ 5.89|199.65_±_ 5.06|**272** _±_ **13.63**|92 _±_ 0|**1188**_±_ **28.35**|
|**Proposed** **_FaRe-CPP_**<br>(optimized for long-range effciency)|109 _±_ 3.26|**148.00** _±_ **3.63**|**141** _±_ **5.91**|95 _±_ 0|**764** _±_ **15.29**|



difference lies in waypoint generation, which is implemented in Python for _FaRe-CPP_ and in C++ for the baselines. However, since this stage is heuristic and has minimal effect on final path quality, the impact is limited to computation time, not algorithmic efficiency. 

_FaRe-CPP_ performs well in coverage efficiency as well as path optimization and the main issue of the application problem at hand is closed-loop revisit time after initial deployment. Since no near-realtime reprocessing of the path is required after the robot started to patrol, any reprocessing can 

happen during deployment while the robot is on patrol. Initial computation, in contrast, plays a comparably minor role since the main focus of our approach is to achieve fast revisit times. 

We provide the experimental results described in this section as generated with the current version of _FaRe-CPP_ together with the code on https://github.com/hcr-lab/FaRe-CPP/tree/ main/experiments. 

## V. CONCLUSION 

The proposed _FaRe-CPP_ coverage path planning algorithm achieves near-complete coverage of the environment with short 

paths and low total cumulative rotation, resulting in fast revisit times. Our approach effectively first generates waypoints that yield the maximum visual coverage, and subsequently optimizes the waypoints using the Greedy Randomized Adaptive Search Procedure (GRASP). 

We evaluated our approach in a simulation environment, demonstrating that our algorithm outperforms existing approaches by achieving optimal coverage areas with shorter path lengths, lower cumulative rotation, and faster revisit times. Compared to the average path lengths and revisit times of existing approaches, _FaRe-CPP_ showed a reduction of at least 21% and 33%, respectively, in these highly relevant performance indicators. 

However, so far _FaRe-CPP_ is limited to scenarios with static obstacles and consistent coverage parameters since the path is being generated offline. In future work, we aim to expand _FaRe-CPP_ to be able to deal with dynamic environments with online obstacle avoidance and varying coverage requirements. This will help to further improve the robustness and adaptability of _FaRe-CPP_ in real-world scenarios. 

## REFERENCES 

- [1] E. Galceran and M. Carreras, “A survey on coverage path planning for robotics,” _Robotics and Autonomous Systems_ , vol. 61, no. 12, pp. 1258– 1276, 2013. 

- [2] R. Almadhoun, T. Taha, L. Seneviratne, and Y. Zweiri, “A survey on multi-robot coverage path planning for model reconstruction and mapping,” _SN Applied Sciences_ , vol. 1, p. 847, 2019. 

- [3] A. Bahamid, A. Ibrahim, A. Ibrahim, I. Zahurin, and A. Wahid, “Intelligent robot-assisted evacuation: a review,” _Journal of Physics: Conference Series_ , vol. 1706, no. 1, 2020. 

- [4] A. Dhiman, N. Shah, P. Adhikari, S. Kumbhar, I. Dhanjal, and N. Mehendale, “Firefighting robot with deep learning and machine vision,” _Neural Computing and Applications_ , vol. 34, pp. 2831–2839, 2021. 

- [5] T. Feo and M. Resende, “Greedy randomized adaptive search procedures,” _Journal of Global Optimization_ , vol. 6, no. 2, pp. 109–133, Mar. 1995. 

- [6] F. Yasutomi, M. Yamada, and K. Tsukamoto, “Cleaning robot control,” in _International Conference on Robotics and Automation_ , 1988, pp. 1839–1841. 

- [7] N. Abd Rahman, K. Sahari, N. Hamid, and Y. Hou, “A coverage path planning approach for autonomous radiation mapping with a mobile robot,” _International Journal of Advanced Robotic Systems_ , vol. 19, no. 4, 2022. 

- [8] M. Phung, C. Quach, T. Dinh, and Q. Ha, “Enhanced discrete particle swarm optimization path planning for UAV vision-based surface inspection,” _Automation in Construction_ , vol. 81, pp. 25–33, 2017. 

- [9] K. Becker, M. Oehler, and O. von Stryk, “3D coverage path planning for efficient construction progress monitoring,” in _IEEE International Symposium on Safety, Security, and Rescue Robotics (SSRR)_ , 2022. 

- [10] E. Acar, H. Choset, A. Rizzi, P. Atkar, and D. Hull, “Morse decompositions for coverage tasks,” _International Journal of Robotics Research_ , vol. 21, no. 4, pp. 331–344, 2002. 

- [11] Y. Li, H. Chen, M. Joo Er, and X. Wang, “Coverage path planning for UAVs based on enhanced exact cellular decomposition method,” _Mechatronics_ , vol. 21, no. 5, pp. 876–885, 2011, Special Issue on Development of Autonomous Unmanned Aerial Vehicles. 

- [12] T. Oksanen and A. Visala, “Coverage path planning algorithms for agricultural field machines,” _Journal of Field Robotics_ , vol. 26, no. 5, pp. 651–668, 2009. 

- [13] H. Choset and P. Pignon, “Coverage path planning: The boustrophedon cellular decomposition,” in _Field and Service Robotics_ , A. Zelinsky, Ed. London: Springer London, 1998, pp. 203–209. 

- [14] E. Acar and H. Choset, “Sensor-based coverage of unknown environments: Incremental construction of morse decompositions,” _International Journal of Robotics Research_ , vol. 21, no. 4, pp. 345–366, 2002. 

- [15] X. Miao, J. Lee, and B.-Y. Kang, “Scalable coverage path planning for cleaning robots using rectangular map decomposition on large environments,” _IEEE Access_ , vol. 6, pp. 38 200–38 215, 2018. 

- [16] Y. Gabriely and E. Rimon, “Spanning-tree-based coverage of continuous areas by a mobile robot,” _Annals of Mathematics and Artificial Intelligence_ , vol. 31, no. 1, pp. 77–98, 2001. 

- [17] S. Swain, P. Khilar, and B. Senapati, “An efficient path planning algorithm for 2D ground area coverage using multi-UAV,” _Wireless Personal Communication_ , vol. 132, no. 1, pp. 361–407, Aug. 2023. 

- [18] S. Mansouri, C. Kanellakis, G. Georgoulas, D. Kominiak, T. Gustafsson, and G. Nikolakopoulos, “2D visual area coverage and path planning coupled with camera footprints,” _Control Engineering Practice_ , vol. 75, pp. 1–16, 2018. 

- [19] A. Ghaddar, A. Merei, and E. Natalizio, “PPS: Energy-aware grid-based coverage path planning for UAVs using area partitioning in the presence of NFZs,” _Sensors_ , vol. 20, p. 3742, 2020. 

- [20] N. Baras and M. Dasygenis, “UGV coverage path planning: An energyefficient approach through turn reduction,” _Electronics_ , vol. 12, p. 2959, 2023. 

- [21] V. Tran, M. Garratt, K. Kasmarik, and S. Anavatti, “Dynamic frontierled swarming: Multi-robot repeated coverage in dynamic environments,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 10, no. 3, pp. 646–661, Mar. 2023. 

- [22] V. Tran, M. Garratt, K. Kasmarik, S. Anavatti, and S. Abpeikar, “Frontier-led swarming: Robust multi-robot coverage of unknown environments,” _Swarm and Evolutionary Computation_ , vol. 75, p. 101171, 2022. 

- [23] Y. Kantaros, M. Thanou, and A. Tzes, “Distributed coverage control for concave areas by a heterogeneous robotswarm with visibility sensing constraints,” _Automatica_ , vol. 53, pp. 195–207, 2015. 

- [24] V. Tran, A. Perera, M. Garratt, K. Kasmarik, and S. Anavatti, “Coverage path planning with budget constraints for multiple unmanned ground vehicles,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 24, no. 11, pp. 12 506–12 522, 2023. 

- [25] V. An, Z. Qu, and R. Roberts, “A rainbow coverage path planning for a patrolling mobile robot with circular sensing range,” _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , vol. 48, no. 8, pp. 1238– 1254, 2018. 

- [26] A. Jonnarth, J. Zhao, and M. Felsberg, “Learning coverage paths in unknown environments with deep reinforcement learning,” _arXiv preprint_ , 2023. [Online]. Available: https://arxiv.org/abs/2306.16978 

- [27] N. Fern´andez Talavera, J. Rold´an-G´omez, F. Mart´ın, and M. RodriguezSanchez, “An autonomous ground robot to support firefighters’ interventions in indoor emergencies,” _Journal of Field Robotics_ , vol. 40, no. 3, pp. 451–473, May 2023. 

- [28] B. Nasirian, M. Mehrandezh, and F. Janabi-Sharifi, “Efficient coverage path planning for mobile disinfecting robots using a graph-based representation of environment,” _Frontiers in Robotics and AI_ , vol. 8, 2021. 

- [29] A. Pierson, J. Romanishin, H. Hansen, L. Yanez, and D. Rus, “Designing and deploying a mobile UVC disinfection robot,” in _International Conference on Intelligent Robots and Systems_ , 2021. 

- [30] S. Perminov, I. Kalinov, and D. Tsetserukou, “GHACPP: Geneticbased human-aware coverage path planning algorithm for autonomous disinfection robot,” in _International Conference on Systems, Man, and Cybernetics_ , 2023. 

- [31] Z. Chen, H. Wang, K. Chen, C. Song, X. Zhang, B. Wang, and J. C. Cheng, “Improved coverage path planning for indoor robots based on bim and robotic configurations,” _Automation in Construction_ , vol. 144, p. 105160, 2024. 

- [32] Z. Chen, K. Chen, C. Song, X. Zhang, J. Cheng, and D. Li, “Global path planning based on BIM and physics engine for UGVs in indoor environments,” _Automation in Construction_ , vol. 139, p. 104263, 2022. 

- [33] J.-K. Lee, A. Naser, O. Ennasr, A. Soylemezoglu, and G. Glaspell, “Unmanned ground vehicle (UGV) full coverage planning with negative obstacles,” Engineer Research and Development Center (U.S.), Tech. Rep. ERDC TR-23-13, 2023. 

- [34] R. Bormann, F. Jordan, W. Li, J. Hampp, and M. Haegele, “Room segmentation: Survey, implementation, and analysis,” in _International Conference on Robotics and Automation_ , 2016. 

- [35] R. Bormann, F. Jordan, J. Hampp, and M. Haegele, “Indoor coverage path planning: Survey, implementation, analysis,” in _International Conference on Robotics and Automation_ , 2018. 

- [36] J. Bresenham, “Algorithm for computer control of a digital plotter,” _IBM Systems journal_ , vol. 4, no. 1, pp. 25–30, 1965. 

- [37] P. Hart, N. Nilsson, and B. Raphael, “A formal basis for the heuristic determination of minimum cost paths,” _IEEE Transactions on Systems Science and Cybernetics_ , vol. 4, no. 2, pp. 100–107, 1968. 

- [38] G. Grisetti, C. Stachniss, and W. Burgard, “Improved techniques for grid mapping with rao-blackwellized particle filters,” _IEEE Transactions on Robotics_ , vol. 23, no. 1, pp. 34–46, 2007. 

- [39] S. Yang and C. Luo, “A neural network approach to complete coverage path planning,” _IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)_ , vol. 34, no. 1, 2004. 

- [40] M. Arain, M. Cirillo, V. Bennetts, E. Schaffernicht, M. Trincavelli, and A. Lilienthal, “Efficient measurement planning for remote gas sensing with mobile robots,” in _International Conference on Robotics and Automation_ , 2015. 

- [41] R. Bormann, J. Hampp, and M. H¨agele, “New brooms sweep clean - an autonomous robotic cleaning assistant for professional office cleaning,” in _International Conference on Robotics and Automation_ , 2015. 

