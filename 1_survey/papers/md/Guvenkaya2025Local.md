---
citation_key: Guvenkaya2025Local
arxiv_id: 2511.07927
arxiv_url: "https://arxiv.org/abs/2511.07927"
title: "Local Path Planning with Dynamic Obstacle Avoidance in Unstructured Environments"
authors_short: "Okan Arif Guvenkaya et al."
year: 2025
direction_tag: G_subgoal_optimization
source: pymupdf4llm
converted_at: 2026-06-23T18:45:43Z
origin: ai+web
reviewed: false
---

# **Local Path Planning with Dynamic Obstacle Avoidance in Unstructured Environments** 

Okan Arif Guvenkaya[1 ] Selim Ah.met Iz[2 ] Mustafa Unel[1 ] 1 _Faculty of Engineering and Natural Sciences, Sabanci University,_ Istanbul, Turkey _2 /nstitute of Optical Sensor Systems, German Aerospace Center (DLR),_ Berlin, Germany selim.iz@dlr.de { okanarif, munel }@sabanciuniv.edu 

_**Abstract-Obstacle**_ **avoidance and path planning are essential for guiding unmanned ground vehicles (UGVs) through envi­ ronments that are densely populated with dynamic obstacles. This paper develops a novel approach that combines tangent­ based path planning and extrapolation methods to create a new decision-making algorithm for local path planning. In the assumed scenario, a UGV has a prior knowledge of its initial and target points within the dynamic environment. A global path has already been computed, and the robot is provided with waypoints along this path. As the UGV travels between these waypoints, the algorithm aims to avoid collisions with dynamic obstacles. These obstacles follow polynomial trajectories, with their initial positions randomized in the local map and velocities randomized between O and the allowable physical velocity limit of the robot, along with some random accelerations. The developed algorithm is tested in several scenarios where many dynamic obstacles move randomly in the environment. Simulation results show the effectiveness of the proposed local path planning strategy by gradually generating a collision free path which allows the robot to navigate safely between initial and the target locations.** _**Index Terms-Dynamic**_ **Obstacle Avoidance, Extrapolation, Local Path Planning, Dynamic Environment** 

## I. INTRODUCTION 

Autonomous vehicles, a significant point of research, are in high demand for navigating human environments and perform­ ing diverse tasks like self-driving cars, delivery drones, and service robots [l ], [2]. Path planning, vital for safe navigation in complex environments, stands out as a major challenge for these systems. 

Path planning algorithms are typically classified based on several criteria, including the nature of obstacles (static or dynamic), the planning approach (global or local), and the environmental conditions (known or unknown). Global path planning proves effective in static and known environments, leveraging extensive datasets to chart a course. Conversely, local path planning becomes required in dynamic or unknown environments, where robots rely on local sensors to adapt their trajectory as the environment evolves, offering a more adapt­ able approach compared to global planning [3] [4]. Highly dynamic environments, characterized by multiple static and dynamic obstacles, pose additional complexities, amplified by factors such as the behavior of dynamic obstacles, the strategic placement of surveillance sensors, and onboard sensor ranges [5] [6] [7]. 

Path planning algorithms cover various approaches, each address distinct challenges across varied environments. Graph­ based algorithms like Dijkstra's, A*, and D* Lite excel 

in static landscapes with known obstacles, while sampling­ based methods such as Probabilistic Roadmaps (PRM) and Rapidly-exploring Random Trees (RRT) succeed in dynamic environments by probing random points. Heuristic algorithms, including Potential Fields, Genetic Algorithms, and Simulated Annealing, offer intuitive approximations for efficient path navigation, even though potentially sacrificing optimality. Fur­ thennore, hybrid algorithms, combining different techniques, provide a comprehensive toolkit for adaptable path.finding across diverse terrains [8]. 

Various studies have explored innovative approaches to path planning in dynamic environments. Conflict-based Search (CBS) in conjunction with the D* Lite algorithm demonstrates efficacy in navigating unknown dynamic environments by harmonizing individual robot path planning with colJision avoidance for multiple robots [9]. Integration of Heuris­ tic Search Based Algorithms like A* with Potential Fields presents a strategy for navigating Unmanned Surface Vehicles (USVs) through dynamic environments, combining global path planning with real-time obstacle avoidance [10). Advance­ ments such as RRT, RRT*, and Improved Bidirectional RRT* highlight efficient path planning methods for smart vehicles in dynamic settings, integrating vehicle-specific constraints and collision detection mechanisms [11). Collaboration between Ant Colony Optimization (ACO) and the Dynamic Window Approach (DWA) enables effective multi-robot navigation and obstacle avoidance within complex terrains, leveraging globally optimized paths generated by ACO and real-time obstacle avoidance by DWA [12). AdditionalJy, approaches like Maximum-Speed Aware Velocity Obstacle (MVO) ensure safe navigation in the presence of high-speed obstacles, show­ casing effectiveness in collision avoidance [l 3). Moreover, deep learning algorithms, exemplified by ANOA (Autonomous Navigation and Obstacle Avoidance) using Q-learning, offer autonomous navigation capabilities superior to conventional methods in static and dynamic environments [13). 

This paper develops a novel local path planning algorithm tailored for highly dynamic and complex environments where the map is initially unknown. An initial global map can be constructed with the help of other robots, such as UAVs, or with alternative methods. Using this global map information, global path planning is completed with any well-known algo­ rithm, such as A* or RRT*. Afterwards, extracted waypoints are provided to the robot. The algorithm proposed in this paper focuses on traveling between waypoints. It relies on two 

1 

key environmental data which are environmental density and real-time detection of dynamic obstacles. The environmental density, which defines the density of moving obstacles across the drivable terrain, is acquired during the initial global path construction. Real-time detection of dynamic obstacles can be facilitated by UAVs or onboard sensors such as LIDAR or cameras. Utilizing the global map information, the UGV navigates using the proposed local path planning algorithm to circumvent collisions with dynamic obstacles in complex environments. The primary contribution of this paper is in­ troduction of a novel decision algorithm for local path plan­ ning, aimed at avoiding dynamic obstacles in highly dynamic environments to enhance path safety and reduce travel time. This approach draws inspiration from tangent-based methods and the dynamic window approach, supported by rigorous numerical analysis incorporating future state estimation tech­ niques for dynamic obstacles. As detailed in the methodology section, the proposed algorithm does not consider obstacles that are outside the critical area, and thus, computational cost is decreased. 

The paper is structured as follows: Section 2 provides a detailed description of the methodology used in this work. Section 3 presents and discusses some simulation results. Finally, Section 4 concludes the paper with some remarks and indicate possible future directions. 


![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0002-02.png)


Fig. 1. Environment visualisation with CoppeliaSim. 

## II. METHODOLOGY 

Continuous tracking and surveillance is one of the most essential steps of the all dynamic obstacle avoidance algorithms. This surveillance process can be done by using different types of onboard sensors or creating a collaborative system where there exist different assistant robots besides master. UAVs are widely preferred assistant robots for collaborative studies because of their wide looking angles and high degree of freedoms [14]. They can easily adopt to mosaicking whole maps [15], or help to find the proper routes even by considering the structure of the terrain [16] besides surveillance of dynamic scenes. As it can be seen in the Fig. 1, the master robot, which have a QR on top of it, tries to reach to desired location which represented by a flag, by avoiding yellow routes that represent the predicted routes of the dynamic obstacles. Additionally, the 

blue route shows the path UGV followed by avoiding from the possible collisions. 

The environment is highly dynamic and complex. The global waypoints are predetermined by one of the methods mentioned in the introduction. The robot needs to follow these waypoints sequentially. For each travel from one waypoint to another, our proposed local path planning algorithm is used. 

The initial position of the robot is (xinitiaI, Yinitial),[and the ] aimed waypoint is (x1arget, Ytarge1). The map area (Amap) can be calculated as: 


![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0002-09.png)


The velocity of the robot is _**v**_ [mis] where _**v**_ E [O, V]. _V_ is the maximum velocity limit of the robot. The existing literature offers numerous approaches to adjusting the velocity of robots, but the proposed approach introduces a new local path planning decision. This decision aims to find the optimum sensing region while maintaining a constant and high velocity for the robot to decrease travel time while ensuring high safety. [20] 

There are n dynamic obstacles, in the area where n E [O, N]. _**N**_ is the maximum possible dynamic obstacle in the map. Each dynamic obstacle can reach a maximum velocity the same as the robot, _V_ [mis]. The robot can search a closer area with the help of another helper robot, such as a UAV, or with its onboard sensors. If onboard sensors are used, then the maximum range is r����ing [m], which represents the furthest distance the sensor can read. Consequently, the sensing region of the robot forms a circle with a radius of r::ing· Otherwise, the sensing region is limited by the maximum altitude of the UAV and its camera qualifications. 

The dynamic obstacles randomly travel around the map, and they have no intention of whether to collide or not collide with the robot. They exhibit random accelerations, and they may follow higher degree polynomial trajectories. 

For simplicity of discussion, let's assume that the robot and dynamic obstacles are circular in shape, with radii of Trobor and robstacle respectively. 

The complexity of the dynamic environment is correlated with the obstacle density (Pobsrac1e) in the drivable area, which is calculated as follows. 


![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0002-15.png)


## A. _Proposed Dynamic Obstacle Avoidance Approach via Ex­ trapolation_ 

In the algorithm, several key terms are defined, crucial for navigation and obstacle avoidance. Their visual representation can be seen in Fig. 2. The critical area is an imaginary circular zone around the robot, monitored by its sensors, with a radius (rca) ranging from Trobot to r:��ino' The dynamic obstacle safe zone, an imaginary circular area earound dynamic obstacles, determines the minimum safe distance for the center of the robot to approach them. It is defined by robstacle plus a safe zone distance (d,2), yielding the obstacle safe zone 

2 


![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0003-00.png)



![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0003-07.png)



![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0004-00.png)


## 


![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0005-00.png)



![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0005-06.png)


## 


![](1_survey/papers/md/Guvenkaya2025Local_figs/Guvenkaya2025Local.pdf-0005-14.png)


critical area increases the likelihood of the most critical obstacle changing frequently, causing the algorithm to react to different obstacles at each frame. This leads to noisy and fluctuating inputs, resulting in poor navigation. Thus, a 2-meter radius performs worse in low-density environments compared to a 6-meter radius but performs better in high­ density environments. 

Overall, a critical area radius of 3 meters offers balanced performance across most density levels, making it a good choice. 

## IV. CONCLUSlON 

A new approach was developed for local path planning by combining tangent-based methods and extrapolation. With the help of initial global map information obtained from UAYs or other methods, the global path is determined before­ hand. The algorithm navigates a UGV between predetermined waypoints while avoiding collisions with dynamic obstacles in unstructured and complex environments. Throughout the robot's motion, detections can be performed via a helper VAY or alternative methods such as onboard sensors. The algorithm aims to enhance navigation safety and reduce travel time through these local paths when a UGY moves through scenarios that are highly complex and dynamic. The perfor­ mance of the local path planning algorithm is related to the critical area, which represents the field that the robot must take into account for dynamic obstacles to ensure the algorithm functions effectively. Numerous highly dynamic environments were created, and simulations were run with different critical area radii. The success ratios were extracted and analyzed for each to determine the optimum one. 

As part of future work, the hyperparameters of the al­ gorithm, the velocity of the robot, and the radius of the critical area can be optimized using various learning methods. Additionally, the algorithm can be extended to operate in three­ dimensional space, making it applicable for use in UAYs or submarines, thus supporting projects in 3D environments. 

## REFERENCES 

- [IJ L. Claussmann, M. Revilloud, D. Gruyer and S. Glaser, "A Review of Motion Planning for Highway Autonomous Driving," in CEEE Trans­ actions on Intelligent Transportation Systems, vol. 21, ao. 5, pp. I 8261848, May 2020 

- [2J M. Missura and M. Bennewitz, "Predictive Collision Avoidance for the Dynamic Window Approach,"' 2019 International Conference on Robotics and Automation (ICRA), Montreal, QC, Canada, 2019, pp. 8620-8626 

- [3] A. Shareef and S. AI-Darraji, "Dynamic Multi-Threaded Path Planning Based on Grasshopper Optimization Algorithm," 2022 lraqi International Conference on Communication and Information Technologies (IICCIT), Basrah, Iraq, 2022 

- [4J 0. Elmakis, T. Shaked and A. Degani, "Vision-Based UAV-UGV Collab­ oration for Autonomous Construction Site Preparation," in IEEE Access, vol. I 0, pp. 51209-51220, 2022 

- [SJ S. A. IZ and M. Unel, "Vision-Based System Identification of a Quadrotor," 2023 8th International Conference on Image, Vision and Computing (ICJVC), Dalian, China, 2023, pp. 584-590, doi: l0.1I09/ICIVC58118.2023.10270807. keywords: Uncertainty;Computational modeling;Machine vision;Fault detec­ tion;Aerodynamics;Mathematical models;Numerical models;system identification;quadrotor modeling;onboard sensing system;vision-based localization 

- [6J Katikaridis, Dimitrios, Vasileios Moysiadis, Naoum Tsolak:is, Patrizia Busato, Dimitrios Kateris, Simon Pearson, Claus Gr!l!n S!l!rensen, and Dionysis Bochtis. "UAV-supported route planning for UGVs in semi­ deterministic agricultural environments." Agronomy 12, no. 8 (2022) 

- [7) L. Kastner et al., "Arena-Rosnav: Towards Deployment of Deep­ Reinforcement-Learning-Based Obstacle Avoidance into Conventional Autonomous Navigation Systems," 2021 CEEE/RSJ International Confer­ ence on Intelligent Robots and Systems (JROS), Prague, Czech Republic, 2021 

- [8] Ahn, Jisoo, Sewoong Jung, Hansom Kim, Ho-Jin Hwang, and Hong­ Bae Jun. "A study on unmanned combat vehicle path planning for collision avoidance with enemy forces in dynamic situations." Journal of Computational Design and Engineering I 0, no. 6 (2023): 2251-2270. 

- [9] Jin, Jianzhi, Yin Zhang, Zhuping Zhou, Mengyuan Jin, Xiaolian Yang, and Fang Hu. "Conflict-based search with D* lite algorithm for robot path planning in unknown dynamic environments." Computers and Electrical Engineering I 05 (2023) 

- [ !OJ D. Wang, H. Chen, S. Lao and S. Drew, "Efficient Path Planning and Dynamic Obstacle Avoidance in Edge for Safe Navigation of USV," in IEEE Internet of Things Journal 

- [11) Ge, Qingying, Aijuan Li, Shaohua Li, Haiping Du, Xin Huang, and Chuanhu Niu. "Improved Bidirectional RRT* Path Planning Method for Smart Vehicle." Mathematical Problems in Engineering 2021 (202 J ): 1-14. 

- [12) Wang, Qian, Junli Li, Liwei Yang, Zhen Yang, Ping Li, and Guofeng Xia. "Distributed Multi-Mobile Robot Path Planning and Obstacle Avoidance Based on ACO-DWA in Unknown Complex Terrain." Elec­ tronics JI, no. 14 (2022) 

- [13) T. Xu, S. Zhang, Z. Jiang, Z. Liu and H. Cheng, "Collision Avoidance of High-Speed Obstacles for Mobile Robots via Maximum-Speed Aware Velocity Obstacle Method," in IEEE Access, vol. 8, pp. 138493-138507, 2020 

- [14J S. A. lz, 2023, "Vision-based Navigation of Heterogeneous Robots" [Master's Thesis, Sabanci University], Sabanci University Research Database, https://research.sabanciuniv.edu/id/eprint/47449/ 

- [ISJ S. A. Jz and M. Unel, "Aerial Image Stitching Using JMU Data from a UAV," 2023 8th International Conference on Image, Vision and Computing (ICIVC), Dalian, China, 2023, pp. 513-5 I 8, doi: I O.J I09/ICIYC58 l l 8.2023. l0269879. keywords: Pose estimation;Autonomous aerial vehicles;Distortion;Cameras;Robustness;Satellite images;lmage 

   - stitching;Image Stitching;IMU;Unmanned Aerial Vehicle {UAV);Camera Calibration 

- [16J S. A. lz and M. Unel, "An Image-Based Path Planning Algorithm Using a UAV Equipped with Stereo Vision," IECON 2022 - 48th Annual Conference of the IEEE Industrial Electronics Society, Brussels, Belgium, 2022, pp. 1-6, doi: I0.1109/IECON49645.2022.9968613. keywords: Surface reconstruction;Three-dimensional displays;Service robots;Heuristic algorithrns;Probabilistic logic;Mathematical models;Trajectory;Path Planning;Stereo Depth Reconstruction;Computer Vision;ArUco marker;Mobile Robotics;Heterogeneous Robot Collaboration; V-REP 

- [17J Yalcin, Hulya, Mustafa Unel, and William Wolovich. "lmplicitization of parametric curves by matrix annihilation." International Journal of Computer Vision 54 (2003): 105-115. 

- [18J Choi, Jaewan, Geonhee Lee, and Chibum Lee. "Reinforcement learning­ based dynamic obstacle avoidance and integration of path planning." Intelligent Service Robotics 14 (2021): 663-677. 

- [19) Wu, Xing, Haolei Chen, Changgu Chen, Mingyu Zhong, Shaorong Xie, Yike Guo, and Hamido Fujita. ''The autonomous navigation and obstacle avoidance for USVs with ANOA deep reinforcement learning method." Knowledge-Based Systems 196 (2020) 

- [20) Li, Changwu, and Danhong Zhang. "A Global Dynamic Path Planning Algorithm Based on Optimized A* Algorithm and Improved Dynamic Window Method." ln 2021 33rd Chinese Control and Decision Confer­ ence (CCDC), pp. 7515-7519. IEEE, 2021. 

6 

