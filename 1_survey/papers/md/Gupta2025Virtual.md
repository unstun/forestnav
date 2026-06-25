---
citation_key: Gupta2025Virtual
arxiv_id: 2511.07811
arxiv_url: "https://arxiv.org/abs/2511.07811"
title: "Virtual Traffic Lights for Multi-Robot Navigation: Decentralized Planning with Centralized Conflict Resolution"
authors_short: "Sagar Gupta et al."
year: 2025
direction_tag: H_hierarchical_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:17:49Z
origin: ai+web
reviewed: false
---

# Virtual Trafic Lights for Multi-Robot Navigation: Decentralized Planning with Centralized Conflict Resolution

Sagar Gupta<sup>1</sup>, Thanh Vinh Nguyen<sup>1</sup>, Thieu Long Phan<sup>1</sup>, Vidul Attri<sup>1</sup>, Archit Gupta<sup>1</sup>, Niroshinie Fernando<sup>1</sup>, Kevin Lee<sup>1</sup>, Seng W. Loke<sup>1</sup>, Ronny Kutadinata<sup>2</sup>,

Benjamin Champion<sup>1</sup> and Akansel Cosgun<sup>1</sup>

<sup>1</sup>Deakin University, Australia

<sup>2</sup>National Transport Research Organisation (NTRO), Australia guptasag@deakin.edu.au

## Abstract

We present a hybrid multi-robot coordination framework that combines decentralized path planning with centralized conflict resolution. In our approach, each robot autonomously plans its path and shares this information with a centralized node. The centralized system detects potential conflicts and allows only one of the conflicting robots to proceed at a time, instructing others to stop outside the conflicting area to avoid deadlocks. Unlike traditional centralized planning methods, our system does not dictate robot paths but instead provides stop commands, functioning as a virtual trafic light. In simulation experiments with multiple robots, our approach increased the success rate of robots reaching their goals while reducing deadlocks. Furthermore, we successfully validated the system in real-world experiments with two quadruped robots and separately with wheeled Duckiebots.

## 1 Introduction

Coordinating multiple robots to navigate shared spaces eficiently and without collisions has many applications in robotics, video games, and trafic control. Centralized and decentralized multi-agent coordination each have distinct trade-ofs. Centralized systems can achieve optimal global solutions but sufer from computational complexity and a single point of failure [Berndt et al., 2021]. Decentralized systems ofer greater scalability and robustness, but local decision-making can lead to suboptimal or conflicting behaviors, such as deadlocks [Yu, 2016].

To address these limitations, we propose a hybrid coordination framework that combines decentralized motion planning with centralized conflict resolution. Each robot operates autonomously, independently planning its path, which reduces the central computational load as no single authority dictates detailed trajectories. The centralized system examines agent paths for conflicts; when it predicts one, it declares the area an intersection and issues a simple “Stop” command to conflicting robots, allowing only one to pass at a time. Figure 1 shows the kind of scenarios being addressed in this work.

![](Gupta2025Virtual_figs/6bc472e3e4139bfd4cba131082507e7cbf8a1837454b1e942ac3f50a0f8077dd.jpg)  
Figure 1: Our hybrid system combines decentralized planning with centralized conflict resolution. To prevent a deadlock, a central node issues a virtual red light to the quadruped on the left, allowing the other robot to pass safely through the conflict zone. Dotted lines represent each robot’s traversed path.

The coordination system is agnostic of the robots’ navigation stacks, as it operates on generic planned paths and produces commands to pause or resume navigation. This guidance facilitates cooperation among otherwise incompatible robots, making the framework suitable for real-world deployment. To demonstrate this, we have implemented the system in an identical manner across diferent navigation systems and communication frameworks.

Our contributions are three-fold:

• We propose a platform-agnostic, hybrid coordination framework that combines decentralized path planning with a lightweight, centralized conflict resolution mechanism functioning as a virtual trafic light.

• We conduct a simulation study with 1,000 trials to quantitatively evaluate our system’s performance against a purely decentralized baseline, measuring success rate, average speed, and path replans across varying numbers of robots.

• We validate the framework’s practical applicability and flexibility through real-world hardware demonstrations on two distinct platforms: dynamic quadruped robots and lane-following wheeled robots.

## 2 Related Works

Multi-Agent Path Finding (MAPF) problems attempt to solve conflicts between a group of robots, where each robot attempts to navigate from a unique starting point to a unique destination. These solutions are optimized for a cost function like time or energy [G¨unter, 2014; Atzmon et al., 2020]. MAPF is an NP-Hard problem [Surynek, 2010; Yu, 2016], which is a computational problem that is at least as dificult as the hardest problems in the NP class, for which no known eficient algorithm exists. Prior works to solve the Multi-Agent Path Finding (MAPF) problem have been categorized into decentralized, centralized, hybrid, and learning-based coordination approaches.

Centralized approaches use a single supervisor which has global knowledge of the map and the states of the robots. This central node plans and coordinates the paths for the robots within the map such that each robot reaches its destination without colliding. [Matos et al., 2025] utilizes a central fleet manager that plans collisionfree paths using Time Enhanced $\mathrm { A } ^ { * }$ (TEA\*). [Oleiwi et al., 2015] uses a combination of Genetic Algorithms (GA) and $\mathrm { A ^ { * } }$ , which integrates fuzzy logic for obstacle avoidance and uses a cubic spline interpolation curve to reduce energy use. [Atinc et al., 2014] uses a centralized control law to navigate robots to their targets while maximizing eficiency of the path. Centralized multi-robot coordination is prevalent in industrial settings where task planning and scheduling is based on robot availability [Caloud et al., 1990; Berndt et al., 2021]. Decentralized coordination is used in large-scale systems with unreliable communication networks [Siefke et al., 2020]. In this approach, each robot operates autonomously, making decisions based on information captured from sensors (implicit communication) or explicitly communicated information between robots [Flocchini et al., 2000; Iocchi et al., 2003; Jouandeau and Yan, 2012]. Deep Reinforcement Learning (DRL) can learn to coordinate robot fleets [He et al., 2020; De Souza et al., 2021]. Other learning-based strategies use a fuzzy inference system to refine paths generated by a global planner like $\mathrm { D ^ { * } }$ Lite [Zagradjanin et al., 2021]. A common characteristic of these methods is their reliance on prior system data, such as successful runs in simpler environments, to train the coordination policy [Kulathunga, 2021].

![](Gupta2025Virtual_figs/2610b32ffd2033ebadf77ae2ef2e1e0a2ed398172ccb0ba14e104902f3c7048e.jpg)  
Figure 2: System overview with N robots, where only robots $R _ { 1 }$ and $R _ { 2 }$ have a conflicting path. The centralized coordination system allows $R _ { 1 }$ to proceed and halts $R _ { 2 }$ until $R _ { 1 }$ has navigated through the conflicting intersection.

Hybrid approaches often combine diferent algorithms, such as integrating the $\mathrm { A ^ { * } }$ graph search with potential fields for navigation [Sang et al., 2021]. [Batool et al., 2024] used a simulation to show that applying a policy framework can efectively regulate robot interactions and resolve conflicts in a hospital setting, while [Jha et al., 2024] adapted maritime collision regulations (COL-REGs) to ground robots, where agents independently apply shared trafic rules to resolve conflicts without ambiguity. Moreover, recent work demonstrating a robot navigating intersections by adhering to actual pedestrian trafic lights [Gupta and Cosgun, 2024] highlights the potential for integrating virtual coordination systems, such as the one we are proposing, with physical infrastructure. Our work contributes to this area by proposing a hybrid framework that leverages the strengths of both centralized and decentralized systems, retaining the autonomy of decentralized path planning for individual robots while incorporating a centralized conflict resolution mechanism.

## 3 System Overview

As illustrated in Figure 2, our proposed hybrid system integrates decentralized path planning with centralized conflict management. Each autonomous robot independently computes an optimal path to its goal using an onboard planner and transmits this trajectory to a central server. The server’s role is not to plan paths but to act as a conflict mediator; it aggregates the paths from all robots to predict potential collision areas.

![](Gupta2025Virtual_figs/2d406e0cd16d3b6a0b1ec10e2332c49633dd476255e68c17fbc55647785bdaef.jpg)  
(a) t=0s

![](Gupta2025Virtual_figs/88b64a3dc972873965404697f1edc885f2f61230f106fe27c8f2c1016db769d6.jpg)  
(b) t=4s

![](Gupta2025Virtual_figs/756fd20bc330d11f6d52e9acc3a86e174c06b10648e39f1a4cd6a34255b9d7da.jpg)  
(c) t=8s

![](Gupta2025Virtual_figs/9282f80e2e194db80fb9e81688b79d643ee9445dfcdb18ea76eaa42d95b5d422.jpg)  
(d) t=12s

![](Gupta2025Virtual_figs/d18be4d836b7454e9cf9dadb2171c7811f7df79da697ab7fa379e0de07cc7463.jpg)  
(e) t=16s

![](Gupta2025Virtual_figs/0ef92af22160429330363eb71518dc5846ca67e5c193af7e570561d81c722669.jpg)  
(f) t=20s  
Figure 3: Snapshots from a simulation run with 6 robots using the hybrid coordination system. There is a 4x4 grid of pillars depicted in black. Robots are depicted as colored circles with a white line representing their orientation. The colored dotted lines depict each robot’s global path to their goals, represented by a star of the same color. Intersections are opaque zones which are green when empty and red when occupied.

Centralized coordination is done using a three-stage process: conflict detection, clustering, and prioritized resolution.

Conflict Detection: The server continuously performs pairwise checks on the planned paths received from all robots. A conflict is detected if two trajectories intersect and their estimated arrival times are within a predefined threshold. The intersection is then defined by a bounding box that encompasses the overlapping path segments.

Conflict Clustering: When conflicts are detected, the server groups the involved robots into clusters. A cluster contains all robots whose paths are directly or indirectly in conflict. For example, if $R _ { 1 }$ conflicts with $R _ { 2 } ,$ and $R _ { 2 }$ conflicts with $R _ { 3 }$ , all three robots are grouped into a single conflict cluster.

Resolution: For each conflict zone, resolution occurs at every simulation step. Robots within the zone’s larger “stop area” are sorted by proximity to its center to create a priority queue. The system iteratively evaluates this queue, starting with the highest-priority robot. For each subsequent candidate, it checks if its future path conflicts with the paths of all higher-priority robots already cleared to proceed in the current timestep. A “STOP” command is issued if a conflict is detected. Otherwise, the robot can proceed, allowing multiple non-colliding robots to traverse the intersection simultaneously.

![](Gupta2025Virtual_figs/ebbe21c77bdfc0084d0e73a73529f64eed4cc498f908f82166391758ad209e01.jpg)  
Figure 4: Average success rate (percentage of robots reaching their goal within a 135s timeout) for the Hybrid and Decentralized systems versus the number of robots. Each point is the mean over 500 trials; shaded regions represent the 95% confidence interval.

## 4 Simulation-based Validation

## 4.1 Simulation Setup

We validated our framework through 1,000 simulations in a Python environment. The world was a 50 × 50 unit space containing a 4 × 4 grid of static pillar obstacles. Each robot, modeled with a 3-unit diameter, utilized an A\* global planner and a Dynamic Window Approach (DWA) local planner. To ensure meaningful navigation, robots in each run were assigned random start and goal positions, with the goal constrained to be at least 75% of the map’s width away from the start. We evaluated system performance under three distinct experimental conditions:

1. Proposed Hybrid System: Both the central coordinator and the local DWA collision avoidance were active. Figure 3 provides a visual representation of a simulation run with six robots under the Hybrid configuration.

2. Decentralized Baseline: The central coordinator was disabled. Robots relied exclusively on their local DWA planners, using simulated LIDAR data to avoid collisions with one another.

For each configuration, we varied the number of robots from one to ten, running 50 trials per count for a total of 1,000 simulations. Performance was quantified using success rate, total collisions, average speed, and the average number of replans. The success rate is the percentage of robots reaching their goal within a 135-second timeout, a window derived from the maximum potential travel time. The average speed is measured in pixels moved per simulation step. Replans are triggered using a dynamic patience level, varying for each robot from being stuck for 3 to 6 seconds.

Figure 5: Average speed for Hybrid and Decentralized systems versus the number of robots. Speed is measured in (pixels/step) × 100, averaged from the start of a run until a robot reaches its goal or times out. Each point is the mean over 500 trials; shaded regions represent the 95% confidence interval.  
![](Gupta2025Virtual_figs/362be26b1ece3c1b98043b41469e47acd1362fd8963924ab659b5501acff426e.jpg)

## 4.2 Results

The quantitative results from our 1,000 simulation runs are visualized in the figures below, comparing success rate (Figure 4), average speed (Figure 5), and path re plans (Figure 6). In addition to these metrics, we monitored collisions between robots and static objects in the environment, and recorded no collisions over 1,000 runs.

Across all multi-robot scenarios (2 to 10 robots), the Hybrid system consistently achieved a higher success rate than the purely Decentralized baseline. The gap in the success rate increased with the number of robots. The Hybrid system’s success rate was 96% compared to the Decentralized system’s 81% with 8 robots, which was the widest diference across the runs. While the success rate for both systems generally decreased with more robots, the Hybrid system’s rate remained at or above 90% until the 9-robot mark. The Decentralized system’s rate dropped to as low as 81% until the 9-robot mark. The Hybrid system was faster with fewer than five robots. The average number of global path replans was lower for the Hybrid system. At eight robots, the Decentralized system required four times as many replans as the Hybrid system.

## 4.3 Discussion of Results

The observed results reveal a clear trade-of between proactive coordination and reactive avoidance. The Hybrid system’s success rate is a direct result of its ability to prevent deadlocks. By commanding robots to wait outside a conflict zone, the central coordinator ensures the intersection remains clear for a prioritized robot to pass through. In the purely Decentralized system, robots frequently converge and create gridlock, which is quantified by the high number of replans. These deadlocks cause individual robots to become stuck, ultimately leading them to time out before reaching their goal, which lowers the success rate. Since decentralized robots are moving until they get stuck, their average speed for successful runs is higher in dense scenarios. The Hybrid system’s robots are often stationary, which lowers their average speed but produces a higher rate of task completion. It should be noted that the Hybrid system’s efectiveness becomes erratic with 9-10 robots. This uncertainty in performance is statistically represented by the widening confidence interval, which indicates a drop in predictability. The underlying cause for this is that at such high densities, the conflict clustering algorithm begins to merge multiple smaller conflicts into a single, massive, map-spanning intersection. This phenomenon makes the “stop” command less eficient, as robots may be halted far from the actual point of conflict, leading to the high variance in outcomes.

Replans vs. Number of Robots  
![](Gupta2025Virtual_figs/c8f1cff060489deea3cf276e1fc258147b50ad37bdc6a34643b735a1cf10d322.jpg)  
Figure 6: Average total path replans per simulation run for the Hybrid and Decentralized systems versus the number of robots. Each data point is the mean over 500 trials, and the shaded regions indicate the 95% confidence interval.

## 5 Real World Demonstration

We validated our framework’s applicability through two distinct physical demonstrations, showcasing its flexibility in managing both dynamic and pre-defined conflict zones. We have made available a video of our demonstrations.<sup>1</sup>

The first demonstration, shown in Figure 1, involved two Unitree GO1 quadruped robots in a 5 × 10m laboratory space. Each robot, equipped with a 2D LiDAR, ran ROS 2 and the Nav2 stack on an onboard computer for autonomous mapping and navigation. The robots planned their paths independently and communicated their poses to an external PC running the central coordinator. We created conflict scenarios by assigning start and goal points that resulted in intersecting paths, which allowed the coordinator to dynamically identify and manage the conflict zone.

![](Gupta2025Virtual_figs/61ec758958eb8077d4814ae1433b814b53b2550fdcb11b9fd2a35c664f039c3e.jpg)  
Figure 7: The hybrid system manages a pre-defined intersection with four Duckiebots on a first-come, firstserved basis, with arrows indicating turn intentions. The first robot to arrive (red arrow) passes straight, followed in sequence by the blue and yellow robots. The last to arrive (green arrow) is cleared to make its left turn only after the intersection is vacant.

The second demonstration, shown in Figure 7, utilized three Duckiebots doing factory-configured lane-following on a small-scale road network with fixed intersections. A top-down camera system localized the robots using ArUco markers, feeding their positions directly to the central coordinator. In this structured environment, the coordinator’s role was to manage access to these predefined intersections, granting passage to one robot at a time based on a first-come, first-served policy. This showcased the system’s adaptability to scenarios where conflict zones are static and known in advance, and global path information from the robots is not required.

## 6 Conclusion

We presented a hybrid coordination framework that combines decentralized path planning with centralized, conflict resolution, functioning as a virtual trafic light. The system is independent of the planners deployed by independent agents. Simulation results demonstrated that this approach increases goal success rates and reduces path replans by preventing deadlocks when compared to a purely decentralized system, especially in moderately dense scenarios. The framework was also validated in real-world demonstrations with two diferent robot platforms. Future work will focus on enhancing the central coordinator’s conflict mitigation strategies. We plan to enable it to request specific robots to replan their paths, which could improve trafic flow. We also intend to scale up our real-world hardware demonstrations with a larger number of robots. Finally, we aim to extend the simulation framework to 3D environments to evaluate its performance for more applications and a deeper validation. Beyond these directions, our Duckietown experiments also serve as a proof of concept that the same approach could be applied to intersection management for autonomous cars.

## References

[Atinc et al., 2014] G. M. Atinc, D. M. Stipanovic, and P. G. Voulgaris. Supervised coverage control of multi agent systems. Automatica, 2014.

[Atzmon et al., 2020] Dor Atzmon, Roni Stern, Ariel Felner, Glenn Wagner, and Neng-Fa Zhou. Robust multi-agent path finding and executing. Journal of Artificial Intelligence Research, 2020.

[Batool et al., 2024] Amna Batool, Seng W. Loke, Niroshinie Fernando, and Jonathan Kua. Policy-based management of human-device and device-device interactions in IoT collectives: A simulation-based study. In 2024 IEEE Smart World Congress, 2024.

[Berndt et al., 2021] Michael Berndt, Dennis Krummacker, Christian Fischer, and Hans D Schotten. Centralized robotic fleet coordination and control. In Mobile Communication-technologies and applications, 2021.

[Caloud et al., 1990] Philippe Caloud, J-C Wonyun Choi, C Latombe, and M Pape, Yim. Indoor automation with many mobile robots. In International Workshop on Intelligent Robots and Systems, Towards a New Frontier of Applications, 1990.

[De Souza et al., 2021] Cristino De Souza, Rhys Newbury, Akansel Cosgun, Pedro Castillo, Boris Vidolov, and Dana Kuli´c. Decentralized multi-agent pursuit using deep reinforcement learning. Robotics and Automation Letters, 2021.

[Flocchini et al., 2000] Paola Flocchini, Giuseppe Prencipe, Nicola Santoro, and Peter Widmayer. Distributed coordination of a set of autonomous mobile robots. In Intelligent Vehicles Symposium, Proceedings, 2000.

[G¨unter, 2014] Ullrich G¨unter. The history of automated guided vehicle systems. 2014.

[Gupta and Cosgun, 2024] Sagar Gupta and Akansel Cosgun. Audio-visual trafic light state detection for urban robots. In 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 12509–12514, 2024.

[He et al., 2020] Junyan He, Hanlin Niu, Joaquin Carrasco, Barry Lennox, and Farshad Arvin. Voronoibased multi-robot autonomous exploration in unknown environments via deep reinforcement learning. Transactions on Vehicular Technology, 2020.

[Iocchi et al., 2003] Luca Iocchi, Daniele Nardi, Michele Piaggio, and Antonio Sgorbissa. Distributed coordination in heterogeneous multi-robot systems. Autonomous Robots, 2003.

[Jha et al., 2024] Eshant Jha, Abhilash Somayajula, Don Gideon, Sayooj P Raveendran, and Bijo Sebastian. COLREGs inspired decentralised path planning for multi-agent system. In 2024 IEEE International Conference on Artificial Intelligence in Engineering and Technology, 2024.

[Jouandeau and Yan, 2012] Nicolas Jouandeau and Zheng Yan. Decentralized waypoint-based multirobot coordination. In International Conference on Cyber Technology in Automation, Control and Intelligent Systems, Bangkok, Thailand, 2012.

[Kulathunga, 2021] Gayanga Kulathunga. A reinforcement learning based path planning approach in 3d environment, 2021.

[Matos et al., 2025] Diogo Miguel Matos, Pedro Costa, H´eber Sobreira, Antonio Valente, and Jos´e Lima. Eficient multi-robot path planning in real environments: a centralized coordination system. International Journal of Intelligent Robotics and Applications, 2025.

[Oleiwi et al., 2015] B. K. Oleiwi, R. Al-Jarrah, H. Roth, and B. I. Kazem. Integrated motion planing and control for multi objectives optimization and multi robots navigation. In 2nd IFAC Conference on Embedded Systems, Computer Intelligence and Telematics, 2015.

[Sang et al., 2021] Hongke Sang, Yingtang You, Xiujun Sun, Yang Zhou, and Fang Liu. The hybrid path planning algorithm based on improved A\* and artificial potential field for unmanned surface vehicle formations. Ocean Engineering, 2021.

[Siefke et al., 2020] Lars Siefke, Volker Sommer, Benedikt Wudka, and Christian Thomas. Robotic systems of systems based on a decentralized serviceoriented architecture. Robotics, 2020.

[Surynek, 2010] Petr Surynek. An optimization variant of multi-robot path planning is intractable. In Proceedings of the National Conference on Artificial Intelligence, 2010.

[Yu, 2016] Jingjin Yu. Intractability of optimal multirobot path planning on planar graphs. IEEE Robotics and Automation Letters, 2016.

[Zagradjanin et al., 2021] Nenad Zagradjanin, Aleksandar Rodic, Dragan Pamucar, and Branimir Pavkovic. Cloud-based multi-robot path planning in complex and crowded environment using fuzzy logic and online learning. Information Technology and Control, 2021.