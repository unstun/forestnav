---
citation_key: Gupta2025Virtual
arxiv_id: 2511.07811
arxiv_url: "https://arxiv.org/abs/2511.07811"
title: "Virtual Traffic Lights for Multi-Robot Navigation: Decentralized Planning with Centralized Conflict Resolution"
authors_short: "Sagar Gupta et al."
year: 2025
direction_tag: H_hierarchical_planning
source: pymupdf4llm
converted_at: 2026-06-23T18:45:34Z
origin: ai+web
reviewed: false
---

# **Virtual Traffic Lights for Multi-Robot Navigation: Decentralized Planning with Centralized Conflict Resolution** 

**Sagar Gupta**[1] **, Thanh Vinh Nguyen**[1] **, Thieu Long Phan**[1] **, Vidul Attri**[1] **, Archit Gupta**[1] **, Niroshinie Fernando**[1] **, Kevin Lee**[1] **, Seng W. Loke**[1] **, Ronny Kutadinata**[2] **, Benjamin Champion**[1] **and Akansel Cosgun**[1] 1Deakin University, Australia 

> 2National Transport Research Organisation (NTRO), Australia guptasag@deakin.edu.au 

## **Abstract** 

We present a hybrid multi-robot coordination framework that combines decentralized path planning with centralized conflict resolution. In our approach, each robot autonomously plans its path and shares this information with a centralized node. The centralized system detects potential conflicts and allows only one of the conflicting robots to proceed at a time, instructing others to stop outside the conflicting area to avoid deadlocks. Unlike traditional centralized planning methods, our system does not dictate robot paths but instead provides stop commands, functioning as a virtual traffic light. In simulation experiments with multiple robots, our approach increased the success rate of robots reaching their goals while reducing deadlocks. Furthermore, we successfully validated the system in real-world experiments with two quadruped robots and separately with wheeled Duckiebots. 

## **1 Introduction** 

Coordinating multiple robots to navigate shared spaces efficiently and without collisions has many applications in robotics, video games, and traffic control. Centralized and decentralized multi-agent coordination each have distinct trade-offs. Centralized systems can achieve optimal global solutions but suffer from computational complexity and a single point of failure [Berndt _et al._ , 2021]. Decentralized systems offer greater scalability and robustness, but local decision-making can lead to suboptimal or conflicting behaviors, such as deadlocks [Yu, 2016]. 

To address these limitations, we propose a hybrid coordination framework that combines decentralized motion planning with centralized conflict resolution. Each robot operates autonomously, independently planning its path, which reduces the central computational load 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0001-09.png)


Figure 1: Our hybrid system combines decentralized planning with centralized conflict resolution. To prevent a deadlock, a central node issues a virtual red light to the quadruped on the left, allowing the other robot to pass safely through the conflict zone. Dotted lines represent each robot’s traversed path. 

as no single authority dictates detailed trajectories. The centralized system examines agent paths for conflicts; when it predicts one, it declares the area an intersection and issues a simple “Stop” command to conflicting robots, allowing only one to pass at a time. Figure 1 shows the kind of scenarios being addressed in this work. 

The coordination system is agnostic of the robots’ navigation stacks, as it operates on generic planned paths and produces commands to pause or resume navigation. This guidance facilitates cooperation among otherwise incompatible robots, making the framework suitable for real-world deployment. To demonstrate this, we have implemented the system in an identical manner across different navigation systems and communication frameworks. 

Our contributions are three-fold: 

- We propose a platform-agnostic, hybrid coordination framework that combines decentralized path planning with a lightweight, centralized conflict res- 

- olution mechanism functioning as a virtual traffic light. 

- We conduct a simulation study with 1,000 trials to quantitatively evaluate our system’s performance against a purely decentralized baseline, measuring success rate, average speed, and path replans across varying numbers of robots. 

- We validate the framework’s practical applicability and flexibility through real-world hardware demonstrations on two distinct platforms: dynamic quadruped robots and lane-following wheeled robots. 

## **2 Related Works** 

Multi-Agent Path Finding (MAPF) problems attempt to solve conflicts between a group of robots, where each robot attempts to navigate from a unique starting point to a unique destination. These solutions are optimized for a cost function like time or energy [G¨unter, 2014; Atzmon _et al._ , 2020]. MAPF is an NP-Hard problem [Surynek, 2010; Yu, 2016], which is a computational problem that is at least as difficult as the hardest problems in the NP class, for which no known efficient algorithm exists. Prior works to solve the Multi-Agent Path Finding (MAPF) problem have been categorized into decentralized, centralized, hybrid, and learning-based coordination approaches. 

Centralized approaches use a single supervisor which has global knowledge of the map and the states of the robots. This central node plans and coordinates the paths for the robots within the map such that each robot reaches its destination without colliding. [Matos _et al._ , 2025] utilizes a central fleet manager that plans collisionfree paths using Time Enhanced A* (TEA*). [Oleiwi _et al._ , 2015] uses a combination of Genetic Algorithms (GA) and A*, which integrates fuzzy logic for obstacle avoidance and uses a cubic spline interpolation curve to reduce energy use. [Atinc _et al._ , 2014] uses a centralized control law to navigate robots to their targets while maximizing efficiency of the path. Centralized multi-robot coordination is prevalent in industrial settings where task planning and scheduling is based on robot availability [Caloud _et al._ , 1990; Berndt _et al._ , 2021]. Decentralized coordination is used in large-scale systems with unreliable communication networks [Siefke _et al._ , 2020]. In this approach, each robot operates autonomously, making decisions based on information captured from sensors (implicit communication) or explicitly communicated information between robots [Flocchini _et al._ , 2000; Iocchi _et al._ , 2003; Jouandeau and Yan, 2012]. Deep Reinforcement Learning (DRL) can learn to coordinate robot fleets [He _et al._ , 2020; De Souza _et al._ , 2021]. Other learning-based strategies use a fuzzy inference system to refine paths generated by a global planner like D* Lite 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0002-06.png)


**----- Start of picture text -----**<br>
Coordination<br>System<br>Conflict<br>Detection<br>Virtual  Non<br>Traffic Light  Conflicting<br>Conflicting Signaller Path<br>Path<br>Stop<br>Robot (R1) Robot (R2) Robot (RN)<br>...<br>Global  Global  Global<br>Planner Planner Planner<br>Local Local Local<br>Planner Planner Planner<br>**----- End of picture text -----**<br>


Figure 2: System overview with N robots, where only robots _R_ 1 and _R_ 2 have a conflicting path. The centralized coordination system allows _R_ 1 to proceed and halts _R_ 2 until _R_ 1 has navigated through the conflicting intersection. 

[Zagradjanin _et al._ , 2021]. A common characteristic of these methods is their reliance on prior system data, such as successful runs in simpler environments, to train the coordination policy [Kulathunga, 2021]. 

Hybrid approaches often combine different algorithms, such as integrating the A* graph search with potential fields for navigation [Sang _et al._ , 2021]. [Batool _et al._ , 2024] used a simulation to show that applying a policy framework can effectively regulate robot interactions and resolve conflicts in a hospital setting, while [Jha _et al._ , 2024] adapted maritime collision regulations (COLREGs) to ground robots, where agents independently apply shared traffic rules to resolve conflicts without ambiguity. Moreover, recent work demonstrating a robot navigating intersections by adhering to actual pedestrian traffic lights [Gupta and Cosgun, 2024] highlights the potential for integrating virtual coordination systems, such as the one we are proposing, with physical infrastructure. Our work contributes to this area by proposing a hybrid framework that leverages the strengths of both centralized and decentralized systems, retaining the autonomy of decentralized path planning for individual robots while incorporating a centralized conflict resolution mechanism. 

## **3 System Overview** 

As illustrated in Figure 2, our proposed hybrid system integrates decentralized path planning with centralized conflict management. Each autonomous robot indepen- 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0003-00.png)



![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0003-01.png)



![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0003-02.png)



![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0003-03.png)


**----- Start of picture text -----**<br>
(a) t=0s (b) t=4s (c) t=8s<br>(d) t=12s (e) t=16s (f) t=20s<br>**----- End of picture text -----**<br>


Figure 3: Snapshots from a simulation run with 6 robots using the hybrid coordination system. There is a 4x4 grid of pillars depicted in black. Robots are depicted as colored circles with a white line representing their orientation. The colored dotted lines depict each robot’s global path to their goals, represented by a star of the same color. Intersections are opaque zones which are green when empty and red when occupied. 

dently computes an optimal path to its goal using an onboard planner and transmits this trajectory to a central server. The server’s role is not to plan paths but to act as a conflict mediator; it aggregates the paths from all robots to predict potential collision areas. 

Centralized coordination is done using a three-stage process: conflict detection, clustering, and prioritized resolution. 

**Conflict Detection:** The server continuously performs pairwise checks on the planned paths received from all robots. A conflict is detected if two trajectories intersect and their estimated arrival times are within a predefined threshold. The intersection is then defined by a bounding box that encompasses the overlapping path segments. 

contains all robots whose paths are directly or indirectly in conflict. For example, if _R_ 1 conflicts with _R_ 2, and _R_ 2 conflicts with _R_ 3, all three robots are grouped into a single conflict cluster. 

**Resolution:** For each conflict zone, resolution occurs at every simulation step. Robots within the zone’s larger “stop area” are sorted by proximity to its center to create a priority queue. The system iteratively evaluates this queue, starting with the highest-priority robot. For each subsequent candidate, it checks if its future path conflicts with the paths of all higher-priority robots already cleared to proceed in the current timestep. A “STOP” command is issued if a conflict is detected. Otherwise, the robot can proceed, allowing multiple non-colliding robots to traverse the intersection simultaneously. 

**Conflict Clustering:** When conflicts are detected, the server groups the involved robots into clusters. A cluster 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0004-00.png)


**----- Start of picture text -----**<br>
Success Rate vs. Number of Robots<br>100<br>95<br>90<br>85<br>80<br>Simulation Type<br>75 Decentralized<br>Hybrid (Ours)<br>70<br>1 2 3 4 5 6 7 8 9 10<br>Number of robots<br>% of robots that reached their goal<br>**----- End of picture text -----**<br>


Figure 4: Average success rate (percentage of robots reaching their goal within a 135s timeout) for the Hybrid and Decentralized systems versus the number of robots. Each point is the mean over 500 trials; shaded regions represent the 95% confidence interval. 

## **4 Simulation-based Validation 4.1 Simulation Setup** 

We validated our framework through 1,000 simulations in a Python environment. The world was a 50 _×_ 50 unit space containing a 4 _×_ 4 grid of static pillar obstacles. Each robot, modeled with a 3-unit diameter, utilized an A* global planner and a Dynamic Window Approach (DWA) local planner. To ensure meaningful navigation, robots in each run were assigned random start and goal positions, with the goal constrained to be at least 75% of the map’s width away from the start. We evaluated system performance under three distinct experimental conditions: 

1. **Proposed Hybrid System:** Both the central coordinator and the local DWA collision avoidance were active. Figure 3 provides a visual representation of a simulation run with six robots under the Hybrid configuration. 

2. **Decentralized Baseline:** The central coordinator was disabled. Robots relied exclusively on their local DWA planners, using simulated LIDAR data to avoid collisions with one another. 

For each configuration, we varied the number of robots from one to ten, running 50 trials per count for a total of 1,000 simulations. Performance was quantified using success rate, total collisions, average speed, and the average number of replans. The success rate is the percentage of robots reaching their goal within a 135-second timeout, a window derived from the maximum potential travel time. The average speed is measured in pixels moved per simulation step. Replans are triggered using a dynamic patience level, varying for each robot from being stuck for 3 to 6 seconds. 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0004-07.png)


**----- Start of picture text -----**<br>
Speed vs. Number of Robots<br>0.20<br>0.18<br>0.16<br>0.14<br>Simulation Type<br>Decentralized<br>0.12<br>Hybrid (Ours)<br>1 2 3 4 5 6 7 8 9 10<br>Number of robots<br>Avg speed of robots<br>**----- End of picture text -----**<br>


Figure 5: Average speed for Hybrid and Decentralized systems versus the number of robots. Speed is measured in (pixels/step) _×_ 100, averaged from the start of a run until a robot reaches its goal or times out. Each point is the mean over 500 trials; shaded regions represent the 95% confidence interval. 

## **4.2 Results** 

The quantitative results from our 1,000 simulation runs are visualized in the figures below, comparing success rate (Figure 4), average speed (Figure 5), and path replans (Figure 6). In addition to these metrics, we monitored collisions between robots and static objects in the environment, and recorded no collisions over 1,000 runs. 

Across all multi-robot scenarios (2 to 10 robots), the Hybrid system consistently achieved a higher success rate than the purely Decentralized baseline. The gap in the success rate increased with the number of robots. The Hybrid system’s success rate was 96% compared to the Decentralized system’s 81% with 8 robots, which was the widest difference across the runs. While the success rate for both systems generally decreased with more robots, the Hybrid system’s rate remained at or above 90% until the 9-robot mark. The Decentralized system’s rate dropped to as low as 81% until the 9-robot mark. The Hybrid system was faster with fewer than five robots. The average number of global path replans was lower for the Hybrid system. At eight robots, the Decentralized system required four times as many replans as the Hybrid system. 

## **4.3 Discussion of Results** 

The observed results reveal a clear trade-off between proactive coordination and reactive avoidance. The Hybrid system’s success rate is a direct result of its ability to prevent deadlocks. By commanding robots to wait outside a conflict zone, the central coordinator ensures the intersection remains clear for a prioritized robot to pass through. In the purely Decentralized system, robots 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0005-00.png)


**----- Start of picture text -----**<br>
Replans vs. Number of Robots<br>80 Simulation Type<br>Decentralized<br>60 Hybrid (Ours)<br>40<br>20<br>0<br>1 2 3 4 5 6 7 8 9 10<br>Number of robots<br>Avg replans per simulation run<br>**----- End of picture text -----**<br>


Figure 6: Average total path replans per simulation run for the Hybrid and Decentralized systems versus the number of robots. Each data point is the mean over 500 trials, and the shaded regions indicate the 95% confidence interval. 

frequently converge and create gridlock, which is quantified by the high number of replans. These deadlocks cause individual robots to become stuck, ultimately leading them to time out before reaching their goal, which lowers the success rate. Since decentralized robots are moving until they get stuck, their average speed for successful runs is higher in dense scenarios. The Hybrid system’s robots are often stationary, which lowers their average speed but produces a higher rate of task completion. It should be noted that the Hybrid system’s effectiveness becomes erratic with 9-10 robots. This uncertainty in performance is statistically represented by the widening confidence interval, which indicates a drop in predictability. The underlying cause for this is that at such high densities, the conflict clustering algorithm begins to merge multiple smaller conflicts into a single, massive, map-spanning intersection. This phenomenon makes the “stop” command less efficient, as robots may be halted far from the actual point of conflict, leading to the high variance in outcomes. 

## **5 Real World Demonstration** 

We validated our framework’s applicability through two distinct physical demonstrations, showcasing its flexibility in managing both dynamic and pre-defined conflict zones. We have made available a video of our demonstrations.[1] 

The first demonstration, shown in Figure 1, involved two Unitree GO1 quadruped robots in a 5 _×_ 10 _m_ laboratory space. Each robot, equipped with a 2D LiDAR, ran ROS 2 and the Nav2 stack on an onboard computer for autonomous mapping and navigation. The robots 

> 1Demonstration video: `https://youtu.be/h2lHliLEdd8` 


![](1_survey/papers/md/Gupta2025Virtual_figs/Gupta2025Virtual.pdf-0005-07.png)


Figure 7: The hybrid system manages a pre-defined intersection with four Duckiebots on a first-come, firstserved basis, with arrows indicating turn intentions. The first robot to arrive (red arrow) passes straight, followed in sequence by the blue and yellow robots. The last to arrive (green arrow) is cleared to make its left turn only after the intersection is vacant. 

planned their paths independently and communicated their poses to an external PC running the central coordinator. We created conflict scenarios by assigning start and goal points that resulted in intersecting paths, which allowed the coordinator to dynamically identify and manage the conflict zone. 

The second demonstration, shown in Figure 7, utilized three Duckiebots doing factory-configured lane-following on a small-scale road network with fixed intersections. A top-down camera system localized the robots using ArUco markers, feeding their positions directly to the central coordinator. In this structured environment, the coordinator’s role was to manage access to these predefined intersections, granting passage to one robot at a time based on a first-come, first-served policy. This showcased the system’s adaptability to scenarios where conflict zones are static and known in advance, and global path information from the robots is not required. 

## **6 Conclusion** 

We presented a hybrid coordination framework that combines decentralized path planning with centralized, conflict resolution, functioning as a virtual traffic light. The system is independent of the planners deployed by independent agents. Simulation results demonstrated that this approach increases goal success rates and reduces path replans by preventing deadlocks when compared to a purely decentralized system, especially in moderately dense scenarios. The framework was also validated in real-world demonstrations with two differ- 

ent robot platforms. Future work will focus on enhancing the central coordinator’s conflict mitigation strategies. We plan to enable it to request specific robots to replan their paths, which could improve traffic flow. We also intend to scale up our real-world hardware demonstrations with a larger number of robots. Finally, we aim to extend the simulation framework to 3D environments to evaluate its performance for more applications and a deeper validation. Beyond these directions, our Duckietown experiments also serve as a proof of concept that the same approach could be applied to intersection management for autonomous cars. 

## **References** 

- [Atinc _et al._ , 2014] G. M. Atinc, D. M. Stipanovic, and P. G. Voulgaris. Supervised coverage control of multi agent systems. _Automatica_ , 2014. 

- [Atzmon _et al._ , 2020] Dor Atzmon, Roni Stern, Ariel Felner, Glenn Wagner, and Neng-Fa Zhou. Robust multi-agent path finding and executing. _Journal of Artificial Intelligence Research_ , 2020. 

- [Batool _et al._ , 2024] Amna Batool, Seng W. Loke, Niroshinie Fernando, and Jonathan Kua. Policy-based management of human-device and device-device interactions in IoT collectives: A simulation-based study. In _2024 IEEE Smart World Congress_ , 2024. 

- [Berndt _et al._ , 2021] Michael Berndt, Dennis Krummacker, Christian Fischer, and Hans D Schotten. Centralized robotic fleet coordination and control. In _Mobile Communication-technologies and applications_ , 2021. 

- [Caloud _et al._ , 1990] Philippe Caloud, J-C Wonyun Choi, C Latombe, and M Pape, Yim. Indoor automation with many mobile robots. In _International Workshop on Intelligent Robots and Systems, Towards a New Frontier of Applications_ , 1990. 

- [De Souza _et al._ , 2021] Cristino De Souza, Rhys Newbury, Akansel Cosgun, Pedro Castillo, Boris Vidolov, and Dana Kuli´c. Decentralized multi-agent pursuit using deep reinforcement learning. _Robotics and Automation Letters_ , 2021. 

- [Flocchini _et al._ , 2000] Paola Flocchini, Giuseppe Prencipe, Nicola Santoro, and Peter Widmayer. Distributed coordination of a set of autonomous mobile robots. In _Intelligent Vehicles Symposium, Proceedings_ , 2000. 

- [G¨unter, 2014] Ullrich G¨unter. _The history of automated guided vehicle systems_ . 2014. 

- [Gupta and Cosgun, 2024] Sagar Gupta and Akansel Cosgun. Audio-visual traffic light state detection for urban robots. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 12509–12514, 2024. 

- [He _et al._ , 2020] Junyan He, Hanlin Niu, Joaquin Carrasco, Barry Lennox, and Farshad Arvin. Voronoibased multi-robot autonomous exploration in unknown environments via deep reinforcement learning. _Transactions on Vehicular Technology_ , 2020. 

- [Iocchi _et al._ , 2003] Luca Iocchi, Daniele Nardi, Michele Piaggio, and Antonio Sgorbissa. Distributed coordination in heterogeneous multi-robot systems. _Autonomous Robots_ , 2003. 

- [Jha _et al._ , 2024] Eshant Jha, Abhilash Somayajula, Don Gideon, Sayooj P Raveendran, and Bijo Sebastian. COLREGs inspired decentralised path planning for multi-agent system. In _2024 IEEE International Conference on Artificial Intelligence in Engineering and Technology_ , 2024. 

- [Jouandeau and Yan, 2012] Nicolas Jouandeau and Zheng Yan. Decentralized waypoint-based multirobot coordination. In _International Conference on Cyber Technology in Automation, Control and Intelligent Systems, Bangkok, Thailand_ , 2012. 

- [Kulathunga, 2021] Gayanga Kulathunga. A reinforcement learning based path planning approach in 3d environment, 2021. 

- [Matos _et al._ , 2025] Diogo Miguel Matos, Pedro Costa, H´eber Sobreira, Antonio Valente, and Jos´e Lima. Efficient multi-robot path planning in real environments: a centralized coordination system. _International Journal of Intelligent Robotics and Applications_ , 2025. 

- [Oleiwi _et al._ , 2015] B. K. Oleiwi, R. Al-Jarrah, H. Roth, and B. I. Kazem. Integrated motion planing and control for multi objectives optimization and multi robots navigation. In _2nd IFAC Conference on Embedded Systems, Computer Intelligence and Telematics_ , 2015. 

- [Sang _et al._ , 2021] Hongke Sang, Yingtang You, Xiujun Sun, Yang Zhou, and Fang Liu. The hybrid path planning algorithm based on improved A* and artificial potential field for unmanned surface vehicle formations. _Ocean Engineering_ , 2021. 

- [Siefke _et al._ , 2020] Lars Siefke, Volker Sommer, Benedikt Wudka, and Christian Thomas. Robotic systems of systems based on a decentralized serviceoriented architecture. _Robotics_ , 2020. 

- [Surynek, 2010] Petr Surynek. An optimization variant of multi-robot path planning is intractable. In _Proceedings of the National Conference on Artificial Intelligence_ , 2010. 

- [Yu, 2016] Jingjin Yu. Intractability of optimal multirobot path planning on planar graphs. _IEEE Robotics and Automation Letters_ , 2016. 

- [Zagradjanin _et al._ , 2021] Nenad Zagradjanin, Aleksandar Rodic, Dragan Pamucar, and Branimir Pavkovic. Cloud-based multi-robot path planning in complex and crowded environment using fuzzy logic and online learning. _Information Technology and Control_ , 2021. 

