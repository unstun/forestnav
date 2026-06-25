---
citation_key: Zeng2022Informationdriven
arxiv_id: 2204.03329
arxiv_url: "https://arxiv.org/abs/2204.03329"
title: "Information-driven Path Planning for Hybrid Aerial Underwater Vehicles"
authors_short: "Zheng Zeng et al."
year: 2022
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:36:21Z
origin: ai+web
reviewed: false
---

# Information-driven Path Planning for Hybrid Aerial Underwater Vehicles

Zheng Zeng<sup>1,2</sup>, Chengke Xiong<sup>1,2</sup>, Xinyi Yuan<sup>1</sup>, Yulin Bai<sup>1</sup>, Yufei Jin<sup>1</sup>, Di Lu<sup>1,2</sup>, Lian Lian<sup>1,2</sup>

<sup>1</sup> School of Oceanography, Shanghai Jiao Tong University, Shanghai, China.

<sup>2</sup> State Key Laboratory of Ocean Engineering, Shanghai Jiao Tong University, Shanghai, China.

zheng.zeng@sjtu.edu.cn; xiongchengke@sjtu.edu.cn

Abstract: This paper presents a novel Rapidly-exploring Adaptive Sampling Tree (RAST) algorithm for the adaptive sampling mission of a hybrid aerial underwater vehicle (HAUV) in an air-sea 3D environment. This algorithm innovatively combines the tournament-based point selection sampling strategy, the information heuristic search process and the framework of Rapidly-exploring Random Tree (RRT) algorithm. Hence can guide the vehicle to the region of interest to scientists for sampling and generate a collisionfree path for maximizing information collection by the HAUV under the constraints of environmental effects of currents or wind and limited budget. The simulation results show that the fast search adaptive sampling tree algorithm has higher optimization performance, faster solution speed and better stability than the Rapidly-exploring Information Gathering Tree (RIGT) algorithm and the particle swarm optimization (PSO) algorithm.

## 1. INTRODUCTION

Efficient observation of hydrometeorological parameters at the sea-air interface to obtain high-quality, high-resolution data could provide accurate boundary conditions for numerical prediction models of the ocean and atmosphere, which is essential for the study of physical mechanisms of sea-air interactions, accurate forecasting of typhoons (hurricanes), and marine disaster prevention and mitigation [1]. For the sea-air adaptive sampling mission, the observation platforms are desired to carry various sensors to acquire the ocean physical, chemical and biological measurement data intelligently and autonomously in real-time. Recently developed observation platforms including Unmanned Aerial Vehicles (UAVs) [2], Unmanned Surface Vehicles (USVs) [3], Autonomous Underwater Vehicles (AUVs) [4], Underwater Gliders (UGs) [5], and other unmanned vehicles [6] are increasingly used by marine scientists for adaptive ocean observation and sampling. UAVs fly fast and can capture and measure changing atmospheric phenomena in the air. USVs sail fast, observe oceanic phenomena at the surface and can carry small AUVs to a designated location for deployment if needed. AUVs are mobile when fully submersed, capable of observing and sampling small-scale oceanic phenomena underwater. Underwater gliders can work continuously underwater for several months to observe large and medium scale ocean phenomena. However, the above-mentioned mobile observation platforms cannot simultaneously conduct joint sea-air observations of oceanic and atmospheric phenomena with 3D distribution and high temporal and spatial variability in specific sea areas.

In recent years, a class of highly mobile Hybrid Aerial Underwater Vehicle (HAUV) [7, 8], which can conduct air, surface and underwater surveys, has come into being. The HAUVs can carry air-sea optical observers and physicochemical sensors for air, surface, and underwater detection and data acquisition [9]. Compared with mobile observation platforms that can only operate in a single specific environmental medium, HAUVs have two modes of operation: aerial flight and underwater diving, so they can switch their modes of operation independently according to environmental information and mission requirements[10]; in addition, HAUVs have the advantages of higher mobility and lower operating costs[11] and can perform continuous, high-quality, and high-precision ocean and atmospheric characteristic parameters in the air-sea 3D environment. This reduces the total cost of sea-air stereo observation and sampling and improves the operational efficiency and the amount of actual data acquisition in a single mission.

The use of HAUVs to perform sea-air stereo adaptive observation and sampling tasks can realize the simultaneous real-time observation of hydrometeorological data at the sea-air interface and provide a new observation means for multi-scale sea-air interaction research as shown in Figure 1. An HAUV could be launched from shore or a surface vehicle where upon a path planning system could be used to generate a trajectory that lead the vehicle to a work site, perform a survey, and then return to shore or deck completely on its own. The surface vehicle will provide the HAUV with localization support, acoustic localization was used to determine the HAUV position underwater. The Blueprint SeaTrac miniature USBL could be integrated into both HAUV and surface vehicle for simultaneous localization and data exchange[12]. To fulfill this mission, it is necessary for the path planner to consider the motion characteristics, the energy consumption of operation, and the time constraints of the HAUV in both ocean and atmospheric. Furthermore, due to the cross-field nature of sea-air interface observation, it is necessary to combine the definition and analysis methods of both ocean and atmospheric phenomena to determine the type, location, and time of the most exploitable hydrometeorological parameters in a sea area and plan feasible and optimal sampling paths [4]. In practical mission scenarios, joint sea-air stereo observation and adaptive sampling are directly associated with the path planning system of the vehicle. The path planning systems should determine the target observation area accessible by the HAUV based on the sea-air environment model and guide the HAUV to navigate along the optimal sampling path to collect the parameter data desired by marine scientists

![](Zeng2022Informationdriven_figs/a39c41268204f498abe00cae97334ff2aa5b07ff20d187d11e28924f8fbc0d03.jpg)

![](Zeng2022Informationdriven_figs/4723f574f82b833173527568e3e10cac153c393df9c2c47efbd66ab7bdc5e743.jpg)  
Figure 1 Flow chart of HAUV for ocean-atmospheric adaptive sampling

Therefore, the performance of the path planning system is an important manifestation of the intelligence level of the HAUV for airsea stereo observation, which determines the sampling efficiency and observation capability of the HAUV in the joint air-sea observation mission. The existing path planning research mainly focuses on the information-driven path planning for unmanned vehicles operating in a single medium, air or underwater. There is an urgent need to develop a path planning system applicable to the sea-air 3D adaptive sampling of HAUVs. It should combine complex sea-air information with the motion performance and system constraints of HAUVs in a specific medium and adopt suitable path optimization algorithms so that the generated sampling paths can guide the HAUVs to the areas with rich environmental information for sampling.

Existing information-driven path planning algorithms include branch-and-bound method, random sampling algorithm, population intelligence optimization algorithm, etc. The random sampling algorithm and the classical RRT\* algorithm have low computationa complexity and are suitable for solving path planning problems in high-dimensional space. It can guarantee the probabilistic completeness and asymptotic optimality of the solution. A review of existing information-driven path planning algorithms is presented in Section 2. This paper will improve and expand on the RRT\* algorithm by innovatively integrating the sampling strategy based on the tournament point selection method, the information heuristic search process and the framework of the RRT\* algorithm to design an algorithm applicable to information-driven path planning for HAUVs.

The main contributions of this work are listed as follows:

We formulate the information-driven HAUV path planning problem under the constraints of environmental effects of currents or wind and limited budget.

 We present a novel RAST path planning method for HAUV that can guide the vehicle to the region of interest for sampling and generate a collision-free path for maximizing information collection.

We compared the important optimization techniques applied to HAUV path planning in several scenarios, the weaknesses and strengths of each optimization technique have been stated.

The rest of this paper is organized as follows. In Section 3, the information-driven path planning problem for a HAUV is formulated. In Section 4, we propose the RAST\* algorithm and design four different forms of the RAST\* algorithm based on the theory of this algorithm and intend to investigate which optimization method can improve the computational speed and solution accuracy of the RAST\* algorithm by introducing comparative experiments. In Section 5, the classical RIGT algorithm and PSO algorithm are used as comparison algorithms, and the performance of different sampling path optimization algorithms is compared through simulation experiments. The prospect of applying RAST\* algorithm in different scenarios is discussed. Concluding remarks are then presented in Section 6.

## 2. RELATED WORK

Information-driven path planning is one of the key technologies for adaptive sampling of unmanned aerial vehicles (UAVs). It aims to generate sampling paths that allow the UAV, within the constraints of a limited budget (e.g., energy, mission time, etc.), to maximize the amount of information observed and collected in the target area [13-15]. Commonly used information-driven path planning algorithms include branch-and-bound, population intelligence optimization algorithms and random sampling algorithms.

## 2.1 Information-driven path planning based on branch delimitation algorithm

The branch-and-bound method is widely used for solving constrained optimization problems and can efficiently search a finite number of feasible solution spaces systematically [16]. Namik et al. proposes using the branch-and-bound method to solve the optimal sampling path for a single AUV and multiple AUVs to maximize the sum of line integrals of the uncertainty values along the entire path [17]. Amarjeet et al. investigated the use of unmanned vehicles for sampling tasks with effective spatial coverage in application scenarios that require effective monitoring of spatio-temporal dynamic environments, such as water quality monitoring in rivers and lakes [18]. Jonathan et al. introduced a pilot measurement procedure in the branch-and-bound method to solve the adaptive ocean sampling path planning problem of AUV[19]. The authors verified that the branch-and-bound method with pilot measurement is more efficient than that without pilot measurement. Paul et al. explored using AUVs with multiple sensors to build water quality models to help assess important watershed environmental hazards [20]. The authors propose two information-driven path planning algorithms, branch-and-bound and cross-entropy optimization, to select the future sampling locations of the AUV under the condition of the kinematic constraints of the AUV. The effectiveness of the proposed method is verified by simulation and field experiments. The branch-and-bound method is simple in structure and fast in solving and is suitable for information-driven path planning problems in small-scale static environments.

## 2.2 Information-driven path planning based on population intelligence optimization algorithm

Population intelligence optimization algorithms such as genetic algorithms (GA), PSO algorithms, and ant colony optimization (ACO) have been applied to information-driven path planning problems in the literature. Kevin et al. used genetic algorithms to plan adaptive sampling paths for multiple underwater gliders [21, 22]. Mario et al. uses GA to search for a water-free path that maximizes the sweeping area of the lake by a manned boat to monitor the lake environment[23]. Sergey et al. proposed a fully nonlinear GA for solving the optimal sampling path of AUV. The authors verified the optimization capability of GA by comparing it with the mower method and A\* algorithm through simulation experiments [24]. Hexiong et al. integrates the fuzzy integrated evaluation method into a multi-objective PSO algorithm to solve the path planning problem of adaptive sampling with multiple AUVs in a dynamic ocean environment. This method uses sampling value and energy consumption as multi-objective cost functions [25]. Chengke et al. proposed an elite group-based PSO algorithm for planning AUV paths to maximize marine environmenta feature information collection in a static ocean environment [26]. Giancarlo et al. Colmenares used an ACO algorithm to solve a single unmanned vehicle data collection task planning problem, planning a path for the vehicle to maximize the amount of water quality sampled [27]. Chengke et al. introduced the Delaunay space partitioning strategy into an ACO to form a path planning system that can effectively guide the path planning system can effectively guide the vehicle to the area of interest to the scientists [28]. Yichen et al. used an ACO algorithm to plan the sampling path of AUV to maximize the acquisition of temperature data in the 3D environment of temperature distribution of the regional ocean model system [29]. However, only the simulation experiments of AUV in a 3D unobstructed and current-free ocean environment model were conducted. Other population intelligence optimization algorithms, including simulated annealing algorithm [30, 31], differential evolution algorithm [32], covariance matrix adaptive evolution algorithm [33, 34], etc. have also been applied to information-driven path planning problems in the literature. The population intelligence optimization algorithm uses a population search model, simple theory, and easy application; however, as the dimensionality and size of the search space increases, the convergence speed decreases sharply, and it is easy to fall into local optimal solutions.

## 2.3 Information-driven path planning based on the random sampling algorithm

One of the random sampling algorithms widely used in path planning is the Rapidly-exploring Random Tree algorithm (RRT)[35]. Geoffrey et al. proposed a fast search information gathering tree algorithm based on the RRT\* algorithm. It can plan paths tha maximize information collection for AUVs with pre-defined constraints (e.g., energy or time constraints). It is also proved that the paths obtained after optimization are asymptotically optimal [36]. Subsequently, Maani et al. proposed an incremental search information collection tree algorithm based on this algorithm that can compute the sampling paths of USVs online [37]. Rongxin et al. proposed a multidimensional fast search random tree algorithm based on mutual information for solving multiple AUVs to maximize the understanding of the region of interest while minimizing the estimation error of the optimal sampling path. The authors verified the feasibility and effectiveness of the multidimensional fast search random tree algorithm based on mutual information through pool experiments [38]. Alberto et al. proposed a two-step path planning strategy for robots to collect information about unknown physical processes efficiently. The RRT algorithm is used to determine the location points not yet visited by the robot in the first step and plan a sampling path that maximizes information collection while minimizing the path cost in the second step [39]. Chengke et al. incorporated a tournament selection method into the RRT\* algorithm and proposed an adaptive sampling-based path planning system to generate an unmanned vehicle sampling path that maximizes information collection under the influence of obstacle environments and sea currents [40]. The RRT\* algorithm has low computational complexity, which grows slowly as the size of the space increases. It is suitable for solving information-driven path planning problems in a large high-dimensional space while guaranteeing the solution's probabilistic completeness and asymptotic optimality. It can ensure the probabilistic completeness and asymptotic optimality of the solution.

Joint air-sea information-driven path planning is a high-dimensional, multi-constraint optimization problem. The computational effort and complexity of the problem will increase exponentially as the search space range increases, so the information-driven path planning module for HAUVs needs to adopt an optimization algorithm that can quickly solve high-dimensional complex problems. Synthesizing the current research status of the above three major classes of algorithms, as shown in Table 1.

TABLE 1 Parameter settings for the HAUV and all algorithms

<table><tr><td>Algorithm</td><td>Advantages</td><td>Disadvantages</td><td>Applicability</td></tr><tr><td>Branch-and-bound method</td><td>Simple structure, fast solution speed</td><td>Linear, discrete search</td><td>Suitable for small scale Static environment</td></tr><tr><td>Group intelligent optimization algorithm</td><td>Simple theory, easy to apply</td><td>Computation speed is greatly affected by space scale, easy to fall into the local optimum solution</td><td>Suitable for medium and small scale Small and medium scale environment</td></tr><tr><td>Random sampling algorithm</td><td>Low computational complexity, low speed of computation affected by spatial scale</td><td>Asymptotic optimization</td><td>Suitable for large scale High-dimensional environment</td></tr></table>

## 3. INFORMATION-DRIVEN PATH PLANNING PROBLEM FOR HAUVS IN A 3D ENVIRONMENT IN AIR AND SEA

The goal of the global information-driven path planning system for HAUVs is to find a globally optimal sampling path $\mathbb { P } ^ { * }$ from the set of feasible paths $\Psi _ { \mathbb { p } }$ that efficiently avoid obstacles $C _ { o b s }$ (e.g., ships, reefs, islands, etc.) and maximize the observation and collection of characteristic information (e.g., seawater temperature, salinity, chlorophyll fluorescence, dissolved oxygen concentration, air temperature, pressure, carbon dioxide fluxes, turbulent heat fluxes, etc.) of interest to scientists. The impact of the wind and flow fields $\mathtt { V } _ { c }$ on the vehicle should be fully considered.

Before discussing the problems studied in this paper, the following assumptions are made.

Assumptions 1: this paper primarily focuses on a high-level planning architecture with simplified dynamics enabling it to find the optimum trajectory for maximizing information collection. Previous work has been done on studying the full dynamics of the system and the control strategies that drive the vehicle to the desired planned trajectories [41].

Assumption 2: the propulsion system of the HAUV maintains a constant thrust at economic power consumption, i.e., the vehicle maintains a constant flight speed $V _ { a i r }$ in the air, and a constant operation speed $V _ { s e a }$ during the underwater navigation phase.

Assumptions 3: the Information Map (IM) of environmental features studied in this paper is given based on the actual observation needs of marine scientists, so the planning problem in this paper is based on the prior known IM.

The information-driven path planning problem studied in this paper is formulated as follows: To study the characteristics of the seaair interface in a specific sea area, a HAUV carrying limited energy $E _ { m a x }$ is deployed from the deck of a research vessel. It is commanded to perform a sampling mission and at a specified mission time $T _ { m a x }$ must return or land to another base station. According to Assumption 2, the velocity of the HAUV while flying in the air is $V _ { a i r } .$ , the velocity while navigating underwater is $V _ { s e a }$ , and the global sampling path is $\mathbb { P } = \{ \mathcal { P } _ { 1 } , \mathcal { P } _ { 2 } , \ldots , \mathcal { P } _ { h } \}$ , where ℎ is the number of discrete path points. In summary, the mathematical model can be established in the following form:

$$
\begin{array}{r l} & {\mathbb {P} ^ {*} = a r g m a x f _ {\tau} (I M, V _ {a i r}, V _ {s e a}, V _ {c}, C _ {o b s}, E _ {m a x}, T _ {m a x}, \mathbb {W})} \\ & {\qquad \text {s.t.} \qquad V _ {a i r} = 0, V _ {s e a} = 0,} \\ & {\qquad \forall i \in \{1, 2, \dots , h \}, \mathcal {P} _ {i} \notin C _ {o b s}} \\ & {\qquad E \leq E _ {m a x}, T \leq T _ {m a x},} \end{array}\tag{1}
$$

Where $f _ { \tau } ( \ u )$ is the information collection function that returns the total amount of information collected along the entire path. ?? is the 3D workspace of the HAUV. E is the total energy consumption of the HAUV along the path $\mathbb { P }$ when performing the mission. T is the total time of the HAUV along the path ℙ.

## 3.1 Optimization criterion

The optimization criterion of the HAUV information-driven path planning problem is that the optimized path can maximize the information collected within a specific mission area and limited budgets. The information collection relies on the sensors onboard the HAUV, which can detect and collect data within a certain range of the current location $\mathcal { P } _ { i }$ , and build a 3D array ????????????????[] with all initial values of zero, the same size as the IM, which holds the values of collected environmental feature information. The HAUV performs the sampling task along the optimized path, constantly updating the information storage array ????????????????[]. In addition, the value of feature information of different spatial locations in the air and sea environment may be variable, introducing the weight coefficient κ into the information acquisition function. In summary, the total amount of information collected throughout the path can be expressed in the following form:

$$
\begin{array}{l} f _ {\tau} (P) = \sum_ {j = 1} ^ {J} \kappa_ {j} \cdot m e a s u r e d [ \rho_ {j} ] \\ s. t. \qquad \rho_ {j} \in W, j \in \{1, 2, 3, \ldots , J \} \end{array}\tag{2}
$$

In which, $\rho _ { \mathrm { j } }$ is the coordinate position of a raster point in the HAUV workspace. $\kappa _ { j }$ is the information value weight of raster point $\rho _ { \mathrm { j } } . J$ is the number of discrete raster points in the 3D workspace.

## 3.2 Sensor models

HAUVs can carry a variety of sensors for aerial, surface, and underwater phenomena observation and information acquisition. Different sensors may have different sensing ranges and information acquisition capabilities, recent research makes use of continuous measurements of local ocean conditions from on-board current profiling sensors mounted in HAUV, e.g., an Oculus M750D forward

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

looking sonar [42] and a StarFish sidescan sonar for information collection [43]. The Oculus M750D sensor is composed of 512 beams that allow aperture up to 120 meters in front of the HAUV. In this paper, the complexity of the sensor model is simplified. According to previous studies on various types of sensors, the ability of sensors to collect feature information decays with increasing distance [44, 45]. Therefore, the HAUV's ability to collect information about the surrounding workspace at point $\rho _ { \mathrm { j } }$ can be expressed in the following form:

$$
\mathcal {A} \big (\mathcal {P} _ {\mathrm{i}}, \rho_ {\mathrm{j}} \big) = \left\{ \begin{array}{c} \mathcal {A} _ {\mathrm{d} _ {\max}} \mathrm{e} ^ {- \sigma (\frac {\mathrm{d} _ {\mathrm{j}}}{\mathrm{d} _ {\max}}) ^ {2}}, \text {if} \mathrm{d} _ {\mathrm{j}} \leq \mathrm{d} _ {\max} \\ 0, \text {if} \mathrm{d} _ {\mathrm{j}} > \mathrm{d} _ {\max} \end{array} \right.\tag{3}
$$

$$
\mathrm{s.t.} \quad \mathcal {A} _ {\mathrm{d} _ {\max}} \in [ 0, 1 ]
$$

In which, ${ \mathrm { d } } _ { \mathrm { j } }$ is the Euclidean distance between the two points $\mathcal { P } _ { \mathrm { i } }$ and $\rho _ { \mathrm { j } } ; \mathcal { A } _ { \mathrm { d } _ { \mathrm { m a x } } }$ , σ and $\mathtt { d } _ { \operatorname* { m a x } }$ are the parameters of the sensor model, which control the sensing range and the sensor capability. Then, the sensor at the path point $\mathcal { P } _ { \mathrm { i } }$ can collect the amount of information at the point $\rho _ { \mathrm { j } }$ in the workspace as:

$$
\operatorname{sensor} \left(\mathcal {P} _ {\mathrm{i}}, \rho_ {\mathrm{j}}\right) = \operatorname{IM} \left(\rho_ {\mathrm{j}}\right) \cdot \mathcal {A} \left(\mathcal {P} _ {\mathrm{i}}, \rho_ {\mathrm{j}}\right)\tag{4}
$$

The HAUV navigates along a planned path, the information about environmental features is continuously collected by the sensors, which can continuously update the information storage array ????????????????[] established in subsection 3.1. If the array ????????????????[ρ<sub>j</sub>] stores the information value of the collected raster points $\rho _ { \mathrm { j } }$ is less than the information value collected by the sensor sensor $\left( \mathcal { P } _ { \mathrm { i } } , \boldsymbol { \rho } _ { \mathrm { j } } \right)$ , the array ????????????????[ρ<sub>j</sub>] is updated. Otherwise, it is not updated.

$$
m e a s u r e d [ \rho_ {j} ] = \left\{ \begin{array}{c} \text { sensor } (\mathcal {P} _ {i}, \rho_ {j}) \text { ,   if   measured } [ \rho_ {j} ] \leq \text { sensor } (\mathcal {P} _ {i}, \rho_ {j}) \\ \text { measured } [ \rho_ {j} ] \text { ,   else } \end{array} \right.\tag{5}
$$

The update detection is carried out during the sampling task until the end of the path. Finally, the information collection function Equation (1) returns the total amount of information that can be collected for the whole path.

## 3.3 Constraint conditions

Constraints on the HAUVs include the fact that the vehicles carry a limited amount of energy per mission and the possibility of prespecified mission times by marine scientists.

## 3.3.1 Energy constraints

The HAUV has three different modes of motion during the sampling mission: airborne mode, underwater navigation mode, and crossmedia mode. A complete mathematical relationship between speed and energy consumption of the HAUV in these three modes of motion is not yet available. According to the existing literature, the relationship between speed and energy consumption of unmanned vehicles (e.g., UAVs and AUVs) can be analyzed. When the economic speed is maintained, the vehicle's energy consumption per unit time can be minimized. Combining with assumption 3, this paper simplifies the mathematical model of the speed-energy consumption relationship of the HAUV, in which the power of the HAUV for economical air flight is known as $\mathrm { P _ { a i r } } { \cdot }$ And the power for economic underwater navigation is $\mathrm { P } _ { \mathrm { s e a } }$ . The total power consumption of the HAUV can be expressed as the sum of the power consumption in the flight mode $\operatorname { E } _ { \mathrm { a i r } }$ , the power consumption in the underwater navigation mode $\mathrm { E } _ { \mathrm { { s e a } } }$ and the power consumption in the cross-media transition $\mathrm { E } _ { s w i t c h }$

$$
\mathrm{E} = \mathrm {E_ {air}} + \mathrm {E_ {sea}} + \mathrm {E_ {switch}}\tag{6}
$$

$$
\mathrm {E_ {air} = P_ {air} \cdot T_ {air}}\tag{7}
$$

$$
\mathrm{E} _ {\mathrm{sea}} = \mathrm{P} _ {\mathrm{sea}} \cdot \mathrm{T} _ {\mathrm{sea}}\tag{8}
$$

$$
\mathrm{s.t.} \quad \mathrm{E} \leq \mathrm{E} _ {\max}
$$

In addition, the total energy consumed by the HAUV per mission E cannot exceed the maximum energy $\operatorname { E } _ { \operatorname* { m a x } } .$ . In equations $( 7 ) .$ , (8) $\operatorname { T } _ { \mathrm { a i r } }$ and $\mathrm { T } _ { \mathrm { s e a } }$ are the operating time of the HAUV in air flight mode and underwater navigation mode. The solution about the operating time will be explored in subsection 3.3.2. It should be noted that the time and power consumption of a single cross-media transition is simplified to a constant.

## 3.3.2 Mission time Constraints

Typically, marine scientists expect HAUV to complete sampling missions within a specified mission time. The total mission time can be expressed in the following form.

$$
\mathrm{T} = \mathrm {T_ {air}} + \mathrm {T_ {sea}} + \mathrm {T_ {switch}} = \sum_ {\mathrm{i} = 1} ^ {\mathrm{h} - 1} \frac {| \mathcal {P} _ {\mathrm{i}} - \mathcal {P} _ {\mathrm{i+1}} |}{\mathrm {V_ {abs\_i}}}\tag{9}
$$

$$
\mathrm{s.t.} \quad \mathrm{T} \leq \mathrm{T} _ {\max}, \quad \mathrm{i} \in \{1, 2, \dots , \mathrm{h} - 1 \}
$$

In which, $\mathtt { V _ { a b s \mathrm { \perp } } }$ is the actual operational velocity of the HAUV in the inertial coordinate system. The velocity of the HAUV is $\mathrm { { V _ { h a u v } } } ,$ including the $\mathrm { V _ { a i r } }$ in airborne flight mode, the $\mathrm { V } _ { \mathrm { s e a } }$ in the underwater navigation mode and the variable speed motion in the crossmedia transition mode. Considering the air-sea environment, there are wind and flow fields, the actual operating velocity $\mathsf { V } _ { \mathsf { a b s } }$ of the HAUV in the inertial coordinate system is affected by the environment. The actual operational velocity of the vehicle will be solved by the velocity vector synthesis method [46].

![](Zeng2022Informationdriven_figs/e4b65d910cae7d47d0ac498ae2f28cc8f139b1de9475b2608874ed8c98edb5cb.jpg)  
Figure 2 Schematic diagram of velocity synthesis

As shown in Figure 2, the actual operational velocity direction of the HAUV on the path segmen $\mathcal { P } _ { i } \mathcal { P } _ { i + 1 }$ should be consistent with the forward direction and the angle cosθ satisfies the following equation.

$$
\cos \theta_ {\mathrm{i}} = \frac {\mathrm{V} _ {\mathrm{c} _ {-} \mathrm{i}} \cdot \mathrm{V} _ {\mathrm{abs} _ {-} \mathrm{i}}}{\left\| \mathrm{V} _ {\mathrm{c} _ {-} \mathrm{i}} \right\| \left\| \mathrm{V} _ {\mathrm{abs} _ {-} \mathrm{i}} \right\|} = \frac {\mathrm{V} _ {\mathrm{c} _ {-} \mathrm{i}} \cdot \mathrm{a} _ {\mathrm{i}}}{\left\| \mathrm{V} _ {\mathrm{c} _ {-} \mathrm{i}} \right\|} = \frac {\mathrm{u} _ {\mathrm{c} _ {-} \mathrm{i}} \mathrm{a} _ {\mathrm{x} _ {-} \mathrm{i}} + \mathrm{v} _ {\mathrm{c} _ {-} \mathrm{i}} \mathrm{a} _ {\mathrm{y} _ {-} \mathrm{i}} + \mathrm{w} _ {\mathrm{c} _ {-} \mathrm{i}} \mathrm{a} _ {\mathrm{z} _ {-} \mathrm{i}}}{\sqrt {\mathrm{u} _ {\mathrm{c} _ {-} \mathrm{i}} ^ {2} + \mathrm{v} _ {\mathrm{c} _ {-} \mathrm{i}} ^ {2} + \mathrm{w} _ {\mathrm{c} _ {-} \mathrm{i}} ^ {2}}}\tag{10}
$$

In which, $\mathbf { a } _ { \mathrm { i } }$ is the unit vector of $\mathsf { V } _ { \mathsf { a b s \perp } }$ , that is, the unit vector of the path segment $\mathcal { P } _ { \mathrm { i } } \mathcal { P } _ { \mathrm { i } + 1 }$ whose components in the $\mathbf { X } , \mathbf { y } ,$ , and z components in the three directions are $\mathsf { a } _ { \mathbf { x } \bot } , \mathsf { a } _ { \mathbf { y } _ { - 1 } } , \mathsf { a } _ { \mathbf { z } \bot }$ .

Suppose that the path planning system has in advance the complete distribution information of the velocity field, including the velocity direction and magnitude. Then, the direction and magnitude of the velocity field $\mathrm { V _ { c , i } , }$ the direction of the actual operating velocity $\mathtt { V _ { a b s \mathrm { \perp } } }$ of the HAUV in the inertial coordinate system, and the velocity generated by the thrusters in the airframe coordinate system $\mathrm { \Delta V _ { h a u v \_ i } , }$ according to the Cosine theorem for triangles:

$$
\mathrm {V_ {c\_ i}} ^ {2} + \mathrm {V_ {abs\_ i}} ^ {2} - 2 \mathrm {V_ {c\_ i}} \mathrm {V_ {abs\_ i}} \cos \theta_ {\mathrm{i}} = \mathrm {V_ {hauv\_ i}} ^ {2}\tag{11}
$$

The actual magnitude of the operational speed of the HAUV in the inertial coordinate system $\mathsf { V } _ { \mathsf { a b s \perp } }$ can be deduced as the quadratic solution of equation (12).

$$
V _ {a b s _ {i}} ^ {2} - 2 \left(u _ {c _ {i}} a _ {x _ {i}} + v _ {c _ {i}} a _ {y _ {i}} + w _ {c _ {i}} a _ {z _ {i}}\right) V _ {a b s _ {i}} + V _ {c _ {j}} ^ {2} - V _ {h a u v _ {i}} ^ {2} = 0\tag{12}
$$

Let $\triangle { = 4 ( \mathrm { u _ { c , i } \mathrm { a _ { x , i } + \mathrm { v _ { c , i } \mathrm { a _ { y , i } + \mathrm { w _ { c , i } \mathrm { a _ { z , i } ) ^ { 2 } + 4 \mathrm { V _ { h a u v , i } ^ { 2 } - 4 \mathrm { V _ { c , j } } ^ { 2 } } } } } } } } }$ , when $\triangle { < } 0 .$ , this equation has no real number solution; when $\triangle { \geq } 0 .$ the solution of this equation can be expressed as.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

$$
V _ {\mathrm {abs\_i}} = u _ {c \_ i} a _ {x \_ i} + v _ {c \_ i} a _ {y \_ i} + w _ {c \_ i} a _ {z \_ i} \pm \frac {1}{2} \sqrt {\triangle}\tag{13}
$$

When there are two feasible solutions, the positive solution with the larger value is usually chosen as the value of $\mathsf { V } _ { \mathsf { a b s \mathrm { . i \cdot } } }$ In addition, when the value of the resulting solution is zero or negative, i.e., the value of $\mathtt { V _ { a b s \mathrm { ~ i ~ } } }$ is not positive. This indicates that the path segment $\mathcal { P } _ { \mathrm { i } } \mathcal { P } _ { \mathrm { i } + 1 }$ is not reachable. A new feasible path needs to be generated. When $\triangle { < } 0 .$ , it means the velocity component of the HAUV in the path segment $\mathcal { P } _ { \mathrm { i } } \mathcal { P } _ { \mathrm { i } + 1 }$ direction is not sufficient to counteract the velocity component of the flow or wind field in this direction, resulting in no real number solution to equation (12). Therefore, the algorithm must solve for the actual operating speed of the HAUV in each path segment, check whether the HAUV can reach each path point, and ensure that the optimized sampling paths are feasible 3. 4 Path formation and smoothing

The information-driven path planning algorithm usually outputs a set of discrete path nodes $\{ p _ { 1 } , p _ { 2 } , p _ { 3 } , \ldots \}$ . To generate a path that satisfies the kinematics and dynamics of the HAUV, this paper adopted B-spline curves for path smoothing [47, 48]. The principle of the B-spline curve is as follows. Assuming that the information-driven path planning algorithm generates six path nodes after optimization point $\{ p _ { 1 } , p _ { 2 } , p _ { 3 } , p _ { 4 } , p _ { 5 } , p _ { 6 } \}$ , where $p _ { 1 }$ is the starting point and $p _ { 6 }$ is the end point. These six path nodes are used as control points for the B-spline curve for curve fitting

$$
\mathrm{P} (S _ {\mathrm{k}}) = \sum_ {\mathrm{n=0}} ^ {\mathrm{N}} p _ {k + n} B _ {\mathrm{n,N}} (s _ {\mathrm{k}})\tag{14}
$$

$$
\mathrm{s.t.} \qquad s _ {k} \in [ 0, 1 ], k \in [ 1, 2, \dots , 6 ]
$$

Where N is the order of the B-spline curve, $\mathrm { B } _ { \mathrm { n , N } } ( s _ { \mathrm { k } } )$ is the Bernstein fundamental polynomial representing the B-spline basis function of the curve, which is defined as follows.

$$
B _ {n, N} (s _ {k}) = C _ {N} ^ {n} s _ {k} ^ {n} (1 - s _ {k}) ^ {N - n} = \frac {N !}{n ! (N - n) !} s _ {k} ^ {n} (1 - s _ {k}) ^ {N - n}, n \in \{0, 1, \dots , N \}\tag{15}
$$

When ${ \Nu } = 3 , { \sf P } ( s _ { \mathrm { \bf k } } )$ is continuously second-order derivable, i.e., the cubic B-spline curve generates a smooth path with continuous velocity and acceleration variation patterns from the start to the end of the HAUV. Therefore, the output optimized path $\mathbb { P } =$ $\{ \mathcal { P } _ { 1 } , \mathcal { P } _ { 2 } , \ldots , \mathcal { P } _ { \mathrm { h } } \}$ is continuous, smooth, and feasible.

## 3.5 Sea and air 3D environment modelling

The ocean and atmosphere environmental models can be obtained from official forecasts or built based on analytical equations.

3.5.1 Forecast-based 3D environment model for air and sea

At present, low-resolution hydrometeorological parameter data and environmental velocity field data can be obtained through ocean observation networks, satellite measurements, etc. The hydrometeorological parameter data of interest are used to construc information maps of sea-air environment characteristics and input into the path planning system of HAUVs together with wind and currents field data so that HAUV can perform the information sampling task to obtain higher resolution and finer hydrometeorological parameters in the target sea area.

The National Oceanic and Atmospheric Administration (NOAA) website provides forecast data for all types of hydrometeorological parameters. The Regional Navy Coastal Ocean Model (NCOM) datasets provide forecasts of ocean temperature, salinity, and horizontal currents at different depths with a horizontal resolution of about 3 km.

This paper downloads hydrometeorological parameters and targets from the website mentioned above. Wind and current fields in the sea area are analyzed, and information such as ocean salinity and atmospheric humidity is extracted. The data are fused to establish the forecast-based sea-air environment characteristic information map IM and the model of the sea-air environment velocity field $V _ { c } .$ Two points need to be clarified here. First, both ocean and atmospheric models only provide data on flow and wind velocities in the horizontal direction and combined with studies in the existing literature, the velocity components $w _ { c }$ of the wind and flow fields in the vertical direction are very small compared to the velocity components in the horizontal direction $u _ { c \_ i }$ and $v _ { c }$ are very small in the order of magnitude and therefore negligible[49]. Second, the forecast-based air-sea models are mainly for studies of large sea

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

areas at the several-kilometer level. In contrast, interpolation is required to generate higher resolution maps for studies of sea areas at the 100-meter level or smaller scales. In this case, instead, a mathematical type of the 3D environment of air and sea in small-scale sea areas is established based on analytical equations.

## 3.5.2 Analytic equation-based 3D environment model for air and sea

The distribution of 3D environmental feature information usually conforms to a ternary Gaussian distribution. Assuming that there are B feature information regions of interest to marine scientists in the target area, the synthesized 3D IM can be represented as a Gaussian mixture model.

$$
\mathrm{IM} = \sum_ {b = 1} ^ {\mathrm{B}} \mathbf {g} _ {b} \cdot \mathcal {N} (\boldsymbol {\mu} _ {b}, \Sigma_ {b})\tag{16}
$$

$$
\mathrm{s.t.} \qquad b \in \{1, 2, 3, \ldots , B \}
$$

Where $\mathsf { \mathbf { \mu } _ { b } } = [ \mathbf { x _ { b } } , \mathbf { y _ { b } } , \mathbf { z _ { b } } ]$ is the mean value, which represents the position of the center of the feature information b in the workspace; $\Sigma _ { \mathrm { b } }$ is a covariance matrix of size 3×3, which controls the dispersion of the feature information b in the x, y, and z directions; ${ \bf g _ { \mathrm { b } } }$ is the weight parameter, which controls the peak size of the feature information b.

In the simulation experiments of this paper, the maps of the environmental feature information based on the analytic equations are created randomly by the Gaussian mixture model. The Gaussian distribution of feature information b in 3D space is used as an example. A point in the workspace is randomly selected as the center $\mu _ { \mathrm { b } }$ of feature information b, and the randomly generated covariance matrix $\Sigma _ { \mathrm { b } }$ is constructed in the following way.

(1) First construct a random diagonal matrix $\mathcal { A } = \mathrm { d i a g } ( [ \mathcal { A } _ { \mathrm { x } } , \mathcal { A } _ { \mathrm { y } } , \mathcal { A } _ { \mathrm { z } } ] )$ , where, $\mathcal { A } _ { \mathrm { x } } , \mathcal { A } _ { \mathrm { y } } , \mathcal { A } _ { \mathrm { z } }$ is random positive;

(2) Rebate a random matrix ${ \mathcal { B } } = { \mathrm { R a n d } } ( 3 , 3 )$ , figure out the standard orthogonal group of matrix $\mathcal { B } = \mathop { \mathrm { o r t h } } ( \mathcal { B } )$ ;

(3) If the characteristic value of the matrix $\mathrm { C } = \mathcal { B } ^ { \mathrm { T } } \mathcal { A } \mathcal { B }$ is greater than or equal to 0, the matrix is a randomly generated symmetric semi-positive matrix, which can be used as a covariance matrix $\Sigma _ { \mathrm { b } }$

There is B randomly generated environmental characteristic information in the workspace. Then, the information value of any point $\rho _ { \mathrm { j } }$ can be defined as:

$$
\mathrm{I} \big (\rho_ {\mathrm{j}} \big) = \sum_ {\mathrm{b} = 1} ^ {\mathrm{B}} \frac {\mathrm{g} _ {\mathrm{b}}}{\sqrt {(2 \pi) ^ {3} | \sum_ {\mathrm{b}} |}} \mathrm{e} ^ {- \frac {1}{2} (\rho_ {\mathrm{j}} - \mu_ {\mathrm{b}}) ^ {\mathrm{T}} \sum_ {\mathrm{b}} ^ {- 1} (\rho_ {\mathrm{j}} - \mu_ {\mathrm{b}})}\tag{17}
$$

To have a unified measurement standard for different target sea areas, we used normalized processing between the $\mathrm { I _ { a i r } }$ and $\mathrm { I } _ { s e a }$ in this paper. It means the data distribution range of the feature information $\mathrm { I _ { a i r } }$ and $\mathrm { I } _ { \mathsf { s e a } }$ of all grid points in the workspace is [0, 1]. According to the result discussed in subsection 3.5.1, the 3D velocity field can be decomposed into a set of different heights and depths of the 2D horizontal speed field associated with each other. The speed field model in the 2D level can be established and superimposed in a plurality of viscous Lamb eddy [50]. According to the analysis equation of the Lamb vortex, a Lamb vortex in the horizontal direction of the vertical position can be expressed as follows

$$
V _ {c \_ x y} = f _ {c} (\mathbb {R} _ {i} ^ {0}, \eta , \zeta)\tag{18}
$$

$$
u _ {c} (\mathbb {R} _ {i}) = - \eta \frac {y - y _ {o}}{2 \pi (\mathbb {R} _ {i} - \mathbb {R} _ {i} ^ {o}) ^ {2}} [ 1 - e ^ {- (\frac {(\mathbb {R} _ {i} - \mathbb {R} _ {i} ^ {o}) ^ {2}}{\zeta^ {2}}} ]\tag{19}
$$

$$
\mathrm{v} _ {c} (\mathbb {R} _ {\mathrm{i}}) = \eta \frac {\mathrm{x} - \mathrm{x} _ {0}}{2 \pi (\mathbb {R} _ {\mathrm{i}} - \mathbb {R} _ {\mathrm{i}} ^ {0}) ^ {2}} [ 1 - \mathrm{e} ^ {- (\frac {(\mathbb {R} _ {\mathrm{i}} - \mathbb {R} _ {\mathrm{i}} ^ {0}) ^ {2}}{\zeta^ {2}}} ]\tag{20}
$$

Among them, ${ \mathbb { R } } _ { \mathrm { i } } = \mathrm { [ ^ { X } _ { y } ] } \mathrm { i n d i c a t e s }$ a 2D working space, $\mathbb { R } _ { \mathrm { i } } ^ { 0 } = \bigl [ _ { \boldsymbol { y } _ { 0 } } ^ { \mathbf { x } _ { 0 } } \bigr ]$ indicates the center position of the vortex, η represents vortex strength, ζ and indicates the radius of the vortex. If there are multiple different locations, intensity and radius of Lamb vortex in the field, the above three formulas are superimposed to solve the size and direction of the horizontal direction velocity field $\mathrm { V _ { c _ { - } x y } } .$ . The 3D ambient speed field continuously gradient in the vertical direction is created by introducing the argument $\mathbb { R } _ { \mathrm { i } } ^ { 0 } , \boldsymbol { \eta } , \boldsymbol { \zeta } .$

Figure 3 shows the maps of sea-air environment feature information generated based on the Gaussian mixture model and the velocity field generated by Lamb vortex. The size of the raster in schematic diagram is $1 0 0 { \times } 1 0 0 { \times } 1 3$ , indicates the searching area of 5km×5km×600m, and the gradient transparent red color indicates the information value of atmospheric features from 1 to 0, the gradient transparent blue color indicates the information value of ocean features from 1 to 0. The translucent dark blue plane indicates the sea level. In this paper, the wind field velocity is controlled within 5m/s, and the flow field velocity is controlled within 0.4m/s. From the top view in Fig.3b, we can see the velocity field in the vertical direction

![](Zeng2022Informationdriven_figs/993c3f0a7e64a8a939bad2185f3f4c56865f680a41faaa8c065eba6253be4972.jpg)  
a) Information on the characteristics of the sea and air 3D environment and the distribution of velocity fields

![](Zeng2022Informationdriven_figs/578a0e689d2885747a972d2845b088b5376676c9425cfd6a0f4196f20f649702.jpg)  
b) Top view  
Figure 3 Schematic diagram of the 3D marine-atmospheric environment model

## 4. INFORMATION-DRIVEN PATH PLANNING ALGORITHM DESIGN

The objective of the RAST\* algorithm is to optimize the path of the HAUV, which maximizes the collection of air-sea environmental features and autonomously allocate the tasks of the HAUV in the air and underwater to meet the constraints of limited energy and preset mission time of the vehicle, and to avoid obstacles effectively. The ${ \mathrm { R A S T } } ^ { * }$ algorithm innovatively combines the sampling strategy based on the tournament point selection method, the information heuristic search process, and the RRT\* algorithm framework to achieve an efficient search of the air-sea information map to solve the optimal sampling path quickly. Four versions of the RAST\* algorithm are designed to verify the effectiveness and superiority of the ${ \mathrm { R A S T ^ { * } } }$ algorithm and study the effects of different optimization methods on the computational speed and solution accuracy of the ${ \mathrm { R A S T ^ { * } } }$ algorithm. The deformed Rapidly-exploring Random Sampling Tree\* (RRST\*) algorithm is designed according to the different sampling strategies. The $\mathrm { R A S T ^ { * } – I / E }$ algorithm and the RAST\*-I algorithm are designed according to the information heuristic search process; the deformed Rapidly-exploring Adaptive Sampling Tree (RAST) algorithm is designed according to the presence or absence of information heuristic search and the reshaping process of parent nodes. Meanwhile, this paper also uses the classical fast search information gathering tree algorithm and the PSO algorithm as comparison algorithms. The optimization process and technical details of these six algorithms are discussed in detail in the following.

## 4.1 Rapidly-exploring Adaptive Sampling Tree Algorithm

The ${ \mathrm { R A S T ^ { * } } }$ algorithm is a sampling-based algorithm inspired by the $\mathrm { R R T ^ { * } }$ algorithm, but what differs from the $\mathrm { R R T ^ { * } }$ algorithm is the introduction of a sampling strategy based on the tournament point selection method and an information heuristic search process in the main structure of the algorithm. Based on the ${ \mathrm { R A S T } } ^ { * }$ algorithm, the sampling strategy tends to grow branches to the regions with high feature information values. The information heuristic search process searches for global sampling paths with low energy consumption during the iterative process of the algorithm, which helps to avoid the ${ \mathrm { R A S T } } ^ { * }$ algorithm from falling into local optimum solutions. These two improvements enable the ${ \mathrm { R A S T } } ^ { * }$ algorithm to generate the global optimal path for the HAUV. The pseudo-code of the RAST\* algorithm is shown in Algorithm 1, and the main flow is as follows.

First, the parameters that need to be inputted before the ${ \mathrm { R A S T } } ^ { * }$ algorithm can be executed include.

 Environment model parameters $\mathrm { P A } _ { \mathrm { e } } \colon$ information map IM, wind/currents field ${ \mathrm { V } } _ { { \mathrm { c } } } ,$ obstacle $\complement _ { \mathbf { o b s } } ;$

HAUV related parameters $\mathrm { P A } _ { \mathrm { h a u v } } \mathrm { i }$ : the aerial speed $\mathtt { V _ { a i r } }$ and the operation power $\mathrm { P _ { a i r } , }$ , underwater speed $\mathrm { V } _ { \mathrm { s e a } }$ and the operation power $\mathrm { P } _ { \mathrm { s e a } }$ , cross-media energy consumption $\mathrm { E } _ { \mathrm { s w i t c h } _ { - } 1 }$ and time $\mathrm { T } _ { \mathrm { { s w i t c h } } _ { - } 1 }$ , limited energy $\mathrm { E } _ { \mathrm { m a x } } ,$ , sensor parameters $\mathcal { A } _ { \mathrm { { d } _ { \mathrm { { m a x } } } } } , \sigma , \ \mathrm { { d } _ { \mathrm { { m a x } } } ; }$

 Task-related parameters $\mathrm { P A } _ { \mathrm { m } }$ : Task start location ${ \mathsf { q } } _ { \mathrm { i n i t } } ,$ end location $\mathbf { q } _ { \mathrm { f i n a l } } .$ , Preset mission time $\mathrm { T } _ { \mathrm { m a x } }$ ;

${ \mathrm { R A S T ^ { * } } }$ algorithm parameters $\mathrm { P A } _ { \mathrm { c d r a s t } } \mathrm { : }$ : the number of tourists M , step size $\delta ,$ neighboring radius ${ \mathrm { \Delta } } \mathrm { r } ,$ maximum iterative number $\operatorname { M a x } _ { - } \mathrm { i t } ,$ the number of iterations the result is no longer improved It\_stop.

Let Tree = (Vertex, Edge) denotes the adaptive sampling tree, Vertex is the set of tree nodes, and Edge is the set of tree branch segments formed by node connections. Best\_IG is a variable storing the optimal amount of information, Bestsol is a onedimensional array storing the optimal amount of information for each iteration.

```txt
Algorithm 1 Rapidly-exploring Adaptive Sampling Tree*

Enter: 3D environment model parameters PAe, HAUV related parameters PAhauv, task-related parameters PAm, CDRAST* algorithm parameters PArast.

1: Vertex ← {qinitm}; Edge ← ∅; Tree = (Vertex, Edge); Best_IG = 0; Bestsol(1) = 0;

2: for it = 1 to Max_it do

3: qts ← TournamentSample(IM, M);
4: qnearest ← Nearest(qts, Vertex);
5: qnew ← Steer(qnearest, qts, r);
6: if CollisionFree(Cobs, qnearest, qnew) then

7: Qm ← Near(Vertex, qnew, r);
8: cmax = 0;
9: for eachqm ∈ Qmdo

10: [IG, E, T, P] = FitnessFun(qnew, qm, qinit, qfinal, Vertex, PAhauv, PAe);

11: c1 = IG/E;

12: if c1 ≥ cmax &E ≤ Emax &T ≤ Tmax &CollisionFree(Cobs, P) then

13: cmax = c1; qmax ← qm; Pmax ← P;

14: end if

15: end for

16: if CollisionFree(Cobs, P) then

17: qnew. Parent ← qmax;
18: qnew. T ← fTime(Pmax);
19: qnew. E ← fEnergy(Pmax);
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
20:  $q_{new}$ . IG ←  $f_{Energy}(\mathbb{P}_{\text{max}})$ ;
21: Vertex ← Vertex ∪  $\{q_{new}\}$ 
22: Edge ← Edge ∪  $\{(q_{\text{max}}, q_{\text{new}})\}$ 
23: if  $q_{new}$ . IG &gt; Best_IG then
24: Best_IG =  $q_{new}$ . IG
25: end if
26: end if
27: end if
28: Bestsol(it) = Best_IG
29: if Bestsol(it) - Bestsol(it) = Best_IG
30: break:
31: end if
32: end for
33: return Tree = (Vertex, Edge);
Output: P*, M_Best_IG, Bestsol
</div>

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

```txt
Algorithm 2 Tournament point selection function
1: function TOURNAMENTSAMPLE(IM, M)
2: randomly selected M raster points {q₁, q₂, ..., qₘ} from IM;
3: qₜₛ ← q₁
4: for i=2 to M do
5: if IM(qⱼ) > IM (qₜₛ) then
6: qₜₛ ← qⱼ;
7: end if
8: end for
9: return qₜₛ;
10: end function
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 Nearest point selection function
1: function NEAREST (q$_{ts}$, Vertex)
2: vn=Length(Vertex);
3: for i =1 to vn do
4: Dis(i) = Distance(q$_{i}$, q$_{ts}$);
5: end for
6: [Dis$_{min}$, Index$_{min}$] = min (Dis);
7: return q$_{Index_{min}}$
8: end function
</div>

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4 Steering function
1: function STEER(qnearest, qts, δ)
2: D=Distance(qnearest, qts);
3: if D&gt;δ then
4:  $q_{new} = q_{nearest} + (q_{ts} - q_{nearest}) * \delta / D$ 
5: else
6:  $q_{new} \leftarrow q_{ts}$ 
7: end if
8: return  $q_{new}$ 
9: end function
</div>

The main structure of the RAST\* algorithm has four key processes as follows, and the whole process is shown in Figure 4. Sampling strategy based on tournament point selection method (Algorithm 1, line 3): the tournament point selection method replaces the original random sampling method in the RRT\* algorithm to generate sampling points. The TOURNAMENTSAMPLE() function in the steps shown in Algorithm 2 and Figure 4a. Raster point $\left\{ \varrho _ { 1 } , \varrho _ { 2 } , \ldots , \varrho _ { \mathbb { M } } \right\}$ are randomly selected from IM. Compare the feature information values corresponding to these ?? raster points and return the raster point with the largest value as the sampling point $\mathsf { q } _ { \mathrm { t } s }$

![](Zeng2022Informationdriven_figs/96b8c7d2f1ffe987e782485a4103341092d61490f4429467796347d670f9e1b0.jpg)

![](Zeng2022Informationdriven_figs/c5b77926f4edc62a860ba7c8fd3cb7064a93eff157033084441f7a61f53ec6d7.jpg)

a) Sampling-based on tournament point selection method b) Search for nearest tree nodes  
![](Zeng2022Informationdriven_figs/364b048deeec193b8c8512f39d225d3356613ea32f7b8b8204d0083fc93ab95f.jpg)  
c) Generation of new nodes

![](Zeng2022Informationdriven_figs/6720e914ceed3621475acd294461a7e3096cfe09174d262051b7341f65367cc6.jpg)  
d) Information heuristic search process

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

![](Zeng2022Informationdriven_figs/b6fbf4ebc64f6607a7685c2cda2dcf5098eed30033a77c4188972dfa8d8c1dfc.jpg)  
e) Parent node reshaping

Figure 4 An illustration of RAST\*

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5 Collision detection function
1: function COLLISIONFREE( $C_{obs}$ , varargin)
2: if varargin is not part of the  $C_{obs}$  then
3: return 1
4: else
5: return 0
6: end if
7: end function
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 6 Find the set of nearby nodes function
1: function NEAR (Vertex, $q_{\text{new}}, r$)
2: $Q_m \leftarrow \emptyset$
3: vn=Length(Vertex)
4: for i = 1 to vn do
5: if Distance($q_i$, $q_{\text{new}}$) &lt; r then
6: $Q_m \leftarrow Q_m \cup q_i$
7: end if
8: end for
9: return $Q_m$
10: end function
</div>

```matlab
1: function FITNESSFUN(q_new, q_m, q_init, q_final, Vertex, PA_hauv, PA_e)
2:    P = Connection(q_new, q_m, q_init, q_final, Vertex);
3:    IG = f_τ(P);
4:    E = f_Energy(P);
5:    T = f_Time(P);
6:    return [IG, E, T, P]
7: end function
```

Search for the nearest tree node and generation of new nodes (Algorithm 1, lines 4-5): the nearest tree node is found in the set of tree nodes Vertex around the sampling point $\mathsf { q } _ { \mathrm { t } s } .$ . The search process of the nearest tree node is represented as the Nearest() function, and the specific steps are shown in Algorithm 3 and Figure 4b. Length(Vertex) function returns the number of tree nodes vn in Vertex. The Distance() function is used to solve for the Euclidean distance between two tree nodes, finding the index of the neares tree node in the set Vertex, based on the one-dimensional array Dis. Use the tree node returned by the Nearest() function as $\scriptstyle { \mathrm { q } } _ { \mathrm { n e a r e s t } } .$ Nearest() function can also be expressed in the following:

$$
\text { Nearest } (q _ {\mathrm{ts}}, \text { Vertex }) = \underset {q _ {\mathrm{i}} \in \text { Vertex }} {\arg \min} | q _ {\mathrm{ts}} - q _ {\mathrm{i}} |, \quad i = 1, 2, \dots , \mathrm{vn}\tag{21}
$$

Then, according to the steering function Steer(), grows from the tree node $\mathsf { q } _ { \mathrm { n e a r e s t } }$ to the sampling point $\mathsf { q } _ { \mathrm { t } s }$ with the tree branch whose length is $\delta$ and generate a new node $\mathsf { q } _ { \mathrm { n e w } }$ , as shown in Figure 4c. If the Euclidean distance between the two points $\{ \mathbf { q } _ { \mathrm { n e a r e s t } } , \mathbf { q } _ { \mathrm { t s } } \}$ is shorter than a step $\delta .$ Then $\mathsf { q } _ { \mathrm { t } s }$ is the new node $\mathbf { q } _ { \mathrm { n e w } } .$ . Steer() function can also be expressed in the following:

$$
\mathrm{Steer} (q _ {\mathrm{nearest}}, q _ {\mathrm{ts}}, \delta) = \left\{ \begin{array}{c c} q _ {\mathrm{nearest}} + \frac {\delta}{| q _ {\mathrm{ts}} - q _ {\mathrm{nearest}} |} \cdot (q _ {\mathrm{ts}} - q _ {\mathrm{nearest}}), & \delta \leq | q _ {\mathrm{ts}} - q _ {\mathrm{nearest}} | \\ q _ {\mathrm{ts}}, & \delta \geq | q _ {\mathrm{ts}} - q _ {\mathrm{nearest}} | \end{array} \right.\tag{22}
$$

Information heuristic search process (Algorithm 1, lines 7-15): after checking that nodes q , q are not in the obstacle space. find the tree node whose distance between node $\mathsf { q } _ { \mathrm { n e w } }$ and itself is less than r in the set of tree nodes Vertex according to the Near() function and store it in the set of neighbors $\mathbf { Q _ { m } }$ . The Near() function can also be expressed in the following:

$$
\text { Nearest } (q _ {\mathrm{ts}}, \text { Vertex }, r) = q _ {\mathrm{i}} \in \text { Vertex: } | q _ {\mathrm{ts}} - q _ {\mathrm{i}} |, \quad i = 1, 2, \dots , v n\tag{23}
$$

Using Connection() for each node in the neighborhood set $\mathrm { Q } _ { \mathrm { m } }$ . First retraces the parent node of ${ \bf q } _ { \mathrm { m } }$ until it returns to the starting point ${ \bf q } _ { \mathrm { i n i t } }$ and then use a B-spline curve to fit the path segmentation from the starting point ${ \bf q } _ { \mathrm { m } }$ through the tree nodes to $\mathsf { q } _ { \mathrm { n e w } }$ and finally to the $\mathtt { q } _ { \mathtt { f i n a l } }$ , until it forms the curvature continuous sampling path ℙ. According to Equations (1), (6) and (9), the total amount of collected information, the total energy consumption and the total time consumption of path ℙ can be solved. By cycling the path that satisfies the constraints of energy, mission time and no collision along with the most amount of information collected per unit power consumption is found as $\mathbb { P } _ { \operatorname* { m a x } }$ , and the neighboring nodes that constitute this path are recorded $\mathbf { q } _ { \mathrm { m a x } } ,$ as shown in Figure 4d.

Remodelling of the parent node and update of the optimal solution (Algorithm 1, lines 16-31): after checking that all discrete points in the path $\mathbb { P } _ { \operatorname* { m a x } }$ are not within the obstacle space, the $\mathbf { q } _ { \mathrm { m a x } }$ will be recorded as the parent of $\mathbf { q } _ { \mathrm { n e w } }$ , storing the total amount of collected information, total energy consumption and total time consumption of the path $\mathbb { P }$ constructed by node $\mathsf { q } _ { \mathrm { n e w } } .$ , and add nodes $\mathsf { q } _ { \mathrm { n e w } }$ to the set of tree nodes Vertex, segment $( \mathtt { q } _ { \mathrm { m a x } } , \mathtt { q } _ { \mathrm { n e w } } )$ will be added in the tree branch set Edge as shown in Figure $4 \mathrm { e } .$ If the amount of collected information by the path generated in this iteration is greater than that of the previous iteration, then update the variable Best\_IG as the optimal solution for this iteration. Otherwise do not update. After that, Best\_IG is added to the array Bestsol. The algorithm keeps iterating in a loop until the optimal solution has no improvement after It\_stop iterations. Otherwise, it iterates until the maximum number of iterations Max\_it and outputting the path $\mathbb { P } ^ { * }$ , the optimal solution Best\_IG and the array of optimal solutions Bestsol generated by each iteration

It is important to note here that the path planning problem studied in this paper has a large number of constraints. According to the characteristics of the HAUV model, if the mission start and end points are particularly far apart, there may be a situation where the HAUV is unreachable under the constraints of limited energy and mission time. In this case, the RAST\* algorithm method may not be able to generate a feasible solution after It\_stop iterations, and output Best\_IG=0. The optimized path $\mathbb { p } ^ { * }$ is empty. In this case, the mission start and end positions need to be set again reasonably.

## 4.1.1 Different improved forms of the $\mathrm { R A S T ^ { * } }$ algorithm

The ${ \mathrm { R A S T } } ^ { * }$ algorithm uses $\mathtt { c } _ { \mathrm { m a x } }$ as the heuristic factor (line 11 of Algorithm 1). $\mathtt { c } _ { \mathrm { m a x } }$ is the amount of information collected by the path per unit power consumption to judge which node in the neighborhood set $\mathrm { Q } _ { \mathrm { m } }$ will be selected as the parent node of $\mathbf { q } _ { \mathrm { n e w } } .$ Hence, this algorithm is named as ${ \mathrm { R A S T } } ^ { * }$ -I/E algorithm in this paper. The corresponding counterpart is the $\mathrm { R A S T ^ { * } { - } I }$ algorithm, it heuristic factor $\mathtt { C } _ { \mathrm { m a x } }$ is the total amount of information collected throughout the path to judge which node in the neighborhood set $\mathrm { Q } _ { \mathrm { m } }$ will be selected as be the parent node of $\mathsf { q } _ { \mathrm { n e w } }$ . That is, the $\mathrm { R A S T ^ { * } { - } I }$ algorithm directly uses the target value as the value of th $\mathbf { c } _ { \mathrm { m a x } } .$ In theory, if the total amount of collected information is set as a heuristic factor and the power consumption as a constraint throughout the path, the initial search process may focus on acquiring more information in the short term without limiting power consumption. As a result, in the subsequent iterations, the tree nodes will not be able to grow to the region with high feature information value due to the lack of energy. Thus the $\mathrm { R A S T ^ { * } { - } I }$ algorithm tends to fall into local optimal solutions. The subsequent simulation experiments will compare the $\mathrm { R A S T ^ { * } – I / E }$ algorithm with the $\mathrm { R A S T ^ { * } { - } I }$ algorithm to analyze the information heuristic search process and analyze the influence of the selection of the heuristic factor $\mathtt { C } _ { \mathrm { m a x } }$ on the final results.

The framework of the RAST algorithm is consistent with that of the RRT algorithm. There is no heuristic search and parent node reshaping process in the optimization process and the tree node $\mathsf { q } _ { \mathrm { n e a r e s t } }$ is directly used as the parent node of $\mathbf { q } _ { \mathrm { n e w } }$ , it means tha lines 7-20 of Algorithm 1 are not executed. Although the RAST algorithm introduces a sampling strategy based on the tournament point selection method, leading the adaptive sampling tree to grow to regions with higher values, the RAST algorithm lacks inspiration It does not re-evaluate the fitness of the tree nodes with the newly generated nodes, so only feasible solutions can be obtained after optimization. The optimality of the RAST algorithm is the same as that of the RRT algorithm. Subsequent simulation experiments will compare the RAST\*-I/E algorithm with the RAST algorithm to analyze the necessity and importance of applying the information heuristic search and the reshaping process of the parent nodes.

In addition, the ${ \mathrm { R R S T } } ^ { * }$ algorithm is designed in this paper depending on the sampling strategy. The sampling strategy of the RRST\* algorithm is the same random sampling strategy as the RRT\* algorithm, i.e., a point is randomly selected as the sampling point $\mathsf { q } _ { \mathrm { t } s }$ (line 3 of Algorithm 1), $\mathrm { i . e . M = 1 ; }$ the rest of the ${ \mathrm { R R S T } } ^ { * }$ algorithm procedure is the same as the $\mathrm { R A S T ^ { * } – I / E }$ algorithm. Theoretically, the advantage of the ${ \mathrm { R R S T } } ^ { * }$ algorithm is that it maintains the randomness of the algorithm and can search and grow branches randomly. Hence, the ${ \mathrm { R R S T } } ^ { * }$ algorithm explores the whole space more comprehensively. However, due to the stochastic nature of the ${ \mathrm { R R S T } } ^ { * }$ algorithm, it requires more iterations to converge, leading to a longer computation time than the RAST\*-I/E algorithm. Subsequent simulations experiments will also compare the RAST\*-I/E algorithm and the RRST\* algorithm to analyze the effect of different sampling strategies on the optimization results and efficiency.

## 4.1.2 Complexity analysis of the RAST\* algorithm

Let n be the total number of iterations of the RAST\* algorithm, and the main loop of the ${ \mathrm { R A S T ^ { * } } }$ algorithm contains the iterations of the nearest tree node search process and the heuristic search process. The number of iterations of the Nearest() function in the nearest tree node search process is the number of iterations available so far. The number of iterations of the Near() function in the information heuristic search process is also the number of iterations available so far. Then, the time complexity of the processes is represented by the Nearest() function, so the time complexity of the ${ \mathrm { R A S T } } ^ { * }$ algorithm and its deformation algorithm is O(n), the time complexity is ${ \mathrm { O } } ( { \mathrm { n } } ^ { 2 } )$ . However, according to existing studies in the literature[35], it is shown that the time complexity of the processes represented by the Nearest() function and the Near() function processes can be reduced to O(logn) by certain methods, i.e., by reducing the number of loops. The nearest tree node position and the set of neighbors can be solved accurately while reducing the number of cycles. Therefore, the RAST\* algorithm also can reduce the time complexity to O(nlogn).

The space complexity of the RAST\* algorithm is defined as the amount of memory in the storage space for the adaptive sampling tree Tree=(Vertex, Edge), i.e., the size of the Tree set, i.e., Size(Vertex) + Size(Edge). In this paper, the size of the Edge set does no exceed the total number of iterations of the ${ \mathrm { R A S T ^ { * } } }$ algorithm, and the size of the Vertex set does not exceed the total number of iterations of the RAST\* algorithm plus one because the initialization of the Vertex set already stores the starting point $\mathsf { q } _ { \mathrm { t } s }$ . In summary, the RAST\* algorithm has a maximum space complexity of O(n+n+1), i.e., O(n).

## 4.2 Rapidly-exploring information gathering tree algorithm

The RIGT algorithm is a sampling-based motion planning algorithm first proposed by Geoffrey A. Hollinger et al. for the information driven path planning problem[36]. The advantages of the RIGT algorithm have been analyzed in the literature as it can quickly search the entire workspace and reduce the number of branches and nodes in the tree collection by continuously growing and pruning the tree collection, reducing the number of paths stored in the tree collection. The specific flow of the RIGT algorithm is shown in Algorithm 8.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

```txt
Algorithm 8 Rapidly-exploring Information Gathering Tree*

Enter: 3D environment model parameters PAe, HAUV related parameters PAhauv, task-related parameters PAm, RIGT* algorithm parameters PArigt.

1: Vertex ← {qinit}; Edge ← ∅; Tree = (Vertex, Edge); Vclosed ← ∅ BestIG = 0; Bestsol(1) = 0;

2: for it = 1 to Max_it do

3: qrand ← RandomSample(IM, M);
4: qnearest ← Nearest(qrand, Vertex);
5: qfeasible ← Steer(qnearest, qrand, δ);
6: Qm ← Near(Vertex, qnew, r);
7: for eachqm ∈ Qmdo

8: qnew ← Steer(qm, qfeasible, δ);
9: if CollisionFree(Cobs, qnearest, qnew)then

10: [qnew.IG, qnew.E, qnew, T, P] = FitnessFun(qnew, qm, qinit, qfinal, Vertex, PAhauv, PAe);
11: if PRUNE(qnew)then

12: Deleteqnew

13: else

14: Vertex ← Vertex ∪ {qnew}

15: Edge ← Edge ∪ {qmax, qnew};
16: if E > Emax|T ≤ Tmax then

17: Vclosed ← Vclosed ∪ {qnew}

18: else if qnew.IG > BestIG then

19: Best_IG = qnew.IG

20: end if

21: end if

22: end if

23: end for

24: Bestsol(it) = Best_IG

25: if Bestsol(it) - Bestsol(it - It_stop) = Best_IG

26: break:

27: end if

28: end for

29: return Tree = (Vertex, Edge);

Output: P*, Best_IG, Bestsol
```

Unlike the RAST\* algorithm, the RIGT algorithm is a random sampling strategy, so the parameters of the RIGT algorithm $\mathrm { P A } _ { \mathrm { r i g t } }$ include only the step size ??, the neighborhood radius r, the maximum number of iterations Max\_it, and the optimization terminated if solution no longer improved after It\_stop iterations.

The basic idea of the RIGT algorithm is as follows.

1. Random sampling and nearest point search process: randomly generate sampling points $\mathbf { q } _ { \mathrm { r a n d } }$ in the workspace and select the nearest sampling point q nearest tree node $\mathbf { q } _ { \mathrm { r a n d } }$ . The branch grows with the length of ??. Then it forms a new node q (Algorithm 8, lines 3-5).

2. Neighborhood access and tree set update process: find the set of neighbors $\mathbf { Q _ { m } } .$ , for each of the tree nodes in the set of neighbors q grows branches of length up to $\delta$ to the new node $\mathbf { q } _ { \mathrm { n e w } } .$ . If neither this branch nor the new node is in the obstacle space and does not need to be cropped, they are put into the sets Edge and Vertex, respectively. Otherwise, delete the new node $\mathrm { q } _ { \mathrm { n e w } } ;$ when the new node $\mathsf { q } _ { \mathrm { n e w } }$ corresponds to a full path whose total energy consumption exceeds the maximum energy or total time

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

consumption exceeds the specified mission time, the new node $\mathsf { q } _ { \mathrm { n e w } }$ will be placed in the forbidden set $\mathrm { V _ { c l o s e d } }$ . The tree nodes in this set no longer grow branches (Algorithm 8, lines 6-17).

3. Update the optimal solution process: update the optimal solution Best\_IG and the array of optimal solutions generated after each iteration Bestsol (Algorithm 8, lines 18-27).

4. Output results: After the main loop terminates, the optimal path $\mathbb { P } ^ { * }$ , the optimal solution ???????? ${ \mathbf { } } J G .$ , and the array of optimal solutions ?????????????? generated by each iteration is output.

The rules for whether the newly generated node $\mathsf { q } _ { \mathrm { n e w } }$ by the RIGT algorithm in step 3 is cropped are defined in the literature as follows[36]. A node $\mathbf { q } _ { \mathrm { n e w } }$ and its associated node ${ \bf q } _ { \mathrm { m } }$ , if $\mathrm { q _ { n e w } . \mathrm { I G < q _ { m } . \mathrm { I G } , q _ { n e w } . \mathrm { E > q _ { m } . \mathrm { E , q _ { n e w } . \mathrm { T > q _ { m } . \mathrm { T } } } } } }$ , the nodes $\mathbf { q } _ { \mathrm { n e w } }$ are trimmed.

## 4.3 PSO algorithm

The core idea of the PSO algorithm is as follows, K particles are randomly generated as populations at initialization, and each particle represents a feasible solution. Let $\mathbf { p _ { k } }$ and $\mathtt { v _ { k } }$ be the position and velocity of the k-th particle, respectively, and the PSO algorithm satisfies the following velocity and position update equations for the kth particle at the i-th iteration.

$$
\mathbf {v} _ {\mathrm{k}} ^ {\mathrm{i+1}} = \mathbf {w} ^ {\mathrm{i}} \cdot \mathbf {v} _ {\mathrm{k}} ^ {\mathrm{i}} + c 1 \cdot \mathrm{Rand} _ {1} ^ {\mathrm{i}} \cdot (\mathbf {p} _ {\mathrm {gbest_ {k}}} ^ {\mathrm{i}} - \mathbf {p} _ {\mathrm{k}} ^ {\mathrm{i}}) + c 2 \cdot \mathrm{Rand} _ {2} ^ {\mathrm{i}} \cdot (\mathbf {p} _ {\mathrm{gbest}} ^ {\mathrm{i}} - \mathbf {p} _ {\mathrm{k}} ^ {\mathrm{i}})\tag{24}
$$

$$
\mathbf {p} _ {\mathrm{k}} ^ {\mathrm{i+1}} = \mathbf {p} _ {\mathrm{k}} ^ {\mathrm{i}} \cdot \mathbf {v} _ {\mathrm{k}} ^ {\mathrm{i+1}}\tag{25}
$$

$\mathrm { w } ^ { \mathrm { i } }$ is the weight parameter at the itch iteration, c1 and c2 are the learning factors. Rand<sup>i</sup> , Rand<sup>i</sup> is [0,1] random number in the interval, $\mathsf { p } _ { \mathsf { p b e s t } _ { \mathbf { k } } } ^ { \mathrm { i } }$ is the kth particle optimal position at the i-th iteration, $\mathsf { p } _ { \mathsf { g b e s t } } ^ { \mathrm { i } }$ is the population optimal position at the i-th iteration It should be noted here that the weight parameter decays with an increasing number of iterations, satisfying the following equation:

$$
\mathbf {w} ^ {\mathrm{i+1}} = \mathbf {w} ^ {\mathrm{i}} \cdot \mathbf {w} _ {\mathrm{damp}}\tag{26}
$$

Where, $\mathbf { W _ { d a m p } }$ is the decay rate of the weight parameter for each iteration. In the PSO algorithm, it is necessary to limit the maximum velocity of each particle in x, y, and z directions $\mathrm { v } _ { \mathrm { p } s 0 } ^ { \mathrm { m a x } }$ , to avoid too large a step; also, it is necessary to constrain that the updated position of each particle cannot overflow the workspace.

```txt
Algorithm 9 PSO algorithm
Enter: Environment model parameters PAe, HAUV related parameters PAhauv, task-related parameters PAm, PSO algorithm parameters PApso.
1: Initialize the position p0 and velocity v0 of each particle to ensure that each particle generates a feasible solution IG0pbest.
2: IGgbest = max(IG0gbest);
3: for i = 1 to Max_it do
4: for k = 1 to K do
5 Solving for Npso control points in particle k according to Equation. (24) and (25), the vk and pk;
6: The path nodes from the starting point through the control points to the endpoint are fitted with a B-spline curve to form path P
7: IGk = fI(P);
8: Ek = fEnergy(P);
9: Tk = fTime(P)
10: if IGk > IGpbest_k & Ek > Emax & Tk > Tmax then;
11: pgbest = pk; IGpbest = IGk;
12: else
13: pgbest = pgbest; IGpbest = IGk;
14: end if
15: if IGpbest = IGgbest then
16: pgbest = pgbest_k; IGgbest = IGpbest;
17: else
18: pgbest = pgbest
```

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
19: end if
20: end for
21:  $w^{i} = w^{i-1} \cdot w_{damp}$ 
22: Bestsol(i) = IG $_{gbest}$ 
23: if Bestsol(i) - Bestsol(i - It $_{stop}$ ) = 0 then
24: break:
25: end if
26: end for
Output: P*, IG $_{gbest}$ , Bestsol
</div>

The PSO algorithm flow is shown in Algorithm 9, and the required input PSO algorithm parameters $\mathrm { P A } _ { \mathrm { p s o } }$ include the learning factors c1, c2, initial weight coefficients $\mathrm { w } ^ { 0 }$ , the weight decay rate $\mathbf { W _ { d a m p } } ,$ , maximum particle velocity $\mathrm { v } _ { \mathrm { p } s 0 } ^ { \mathrm { m a x } }$ population size K, number of control points $\Nu _ { \mathrm { p s o } }$ , the maximum number of iterations It\_stop, the number of iterations the result is no longer improved Max\_it. The PSO algorithm updates the position and velocity of each control point according to Equations (24) and (25).

## 5 SIMULATION EXPERIMENT RESULTS AND ANALYSIS

In this section, the RAST\*-I/E algorithm, RAST\*-I algorithm, RAST algorithm, RRST\* algorithm, RRST algorithm and PSO algorithm designed in subsection four are compared in five simulation cases under various scenarios.

## 5.1 Simulation experiment setup

All simulation experiments in this section were performed on a host computer with Windows 10 operating system, Intel(R) Core(TM) i7-6700HQ CPU @ 3.40 GHz and 16.0 GB of RAM. The parameter settings of the HAUV and all algorithms in the simulation experiments are shown in Table 2. The parameters of the HAUV in this paper are based on the values of the HAUV "Nezha"[51] The optimal power of the HAUV for air flight $\mathrm { P _ { a i r } }$ , the optimal power for underwater navigation $\mathrm { P } _ { \mathrm { s e a } }$ and single energy consumption for cross-media motion mode $\mathrm { E } _ { \mathrm { s w i t c h } _ { - } 1 } ,$ all three parameters are related to the HAUV with finite energy $\operatorname { E } _ { \operatorname* { m a x } } .$ . In this paper, $\operatorname { E } _ { \operatorname* { m a x } }$ is used as a criterion to inver $\mathrm { P _ { a i r } , ~ } \mathrm { P _ { s e a } }$ and $\mathrm { E } _ { \mathrm { s w i t c h \_ i } }$ relative to the scale factor of $\operatorname { E } _ { \operatorname* { m a x } }$ , thus determining the relative values of these three parameters. In addition, the basic parameter settings of all algorithms in this paper are based on the summary of existing research literature. The step size σ and the neighborhood radius r of the RAST\* algorithm are based on the size of the environmental raster map. In particular, it should be noted that the results of this paper set It\_stop is set to 200 times to speed up the solution of th algorithm.

This section focuses on the simulation experiments of the information-driven path planning problem for a single HAUV. The following five scenarios are designed.

Scenario 1: Path planning for a HAUV with limited energy.

Scenario 2: Path planning for a HAUV under the dual constraints of limited energy and mission time.

Scenario 3: Path planning for a HAUV under dual constraints of limited energy and tight mission time.

Scenario 4: Path planning for a HAUV with a higher weight of information on ocean features than on atmosphere.

Scenario 5: Path planning for a HAUV with higher weight of information on the atmospheric than the ocean.

The air and underwater environmental information weights are the same in Scenarios 1-3, and these simulations mainly demonstrate the performance of these six algorithms under different constraints. In Scenarios 4-5, different weights are set in the information collection function for the aerial and underwater features, and the simulations compare the optimization performance of these six algorithms.

TABLE 2 Parameter settings for the HAUV and all algorithms

<table><tr><td></td><td>parameters</td><td>notation</td><td>value</td></tr><tr><td rowspan="3">HAUV</td><td>air speed</td><td> $V_{air}$ </td><td>10(m/s)</td></tr><tr><td>power for air flight</td><td> $P_{air}$ </td><td> $\frac{1}{900}E_{max}$ </td></tr><tr><td>underwater speed</td><td> $V_{sea}$ </td><td>0.5(m/s)</td></tr></table>

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

<table><tr><td rowspan="7"></td><td>power for underwater navigation</td><td> $P_{sea}$ </td><td> $\frac{1}{28800}E_{max}$ </td></tr><tr><td>power consumption in cross-media</td><td> $E_{switch\_1}$ </td><td> $\frac{1}{30}E_{max}$ </td></tr><tr><td>time consumption for cross-media</td><td> $T_{switch\_1}$ </td><td>20(s)</td></tr><tr><td>limited energy</td><td> $E_{max}$ </td><td>One standard unit</td></tr><tr><td>sensor perception factor</td><td> $\mathcal{A}_{d_{max}}$ </td><td>1</td></tr><tr><td>sensor distance attenuation coefficient</td><td>σ</td><td>1</td></tr><tr><td>sensing range</td><td> $d_{max}$ </td><td>100(m)</td></tr><tr><td rowspan="5">RAST*Algorithm</td><td>Number of tournament selection</td><td>M</td><td>10</td></tr><tr><td>Step length</td><td>δ</td><td>5</td></tr><tr><td>Neighborhood radius</td><td>r</td><td>10</td></tr><tr><td>Maximum number of iterations</td><td> $V_{sea}$ </td><td>5000</td></tr><tr><td>Number of times the result is no longer improved</td><td>It_stop</td><td>200</td></tr><tr><td rowspan="7">PSO Algorithm</td><td>Learning factor</td><td>c1</td><td>1</td></tr><tr><td>Learning factor</td><td>c2</td><td>1</td></tr><tr><td>Initial weighting factor</td><td> $ω^0$ </td><td>1</td></tr><tr><td>Decay rate of weights</td><td> $ω_{damp}$ </td><td>0.99</td></tr><tr><td>Maximum particle velocity</td><td> $v_{pso}^{max}$ </td><td>[5,5.1]</td></tr><tr><td>Population size</td><td>K</td><td>50</td></tr><tr><td>Number of control points</td><td> $N_{pso}$ </td><td>5</td></tr></table>

The environmental model used in the above five scenarios is a 100×100×13 raster map, representing a mission area of 5km×5km×600m. Each raster point in the raster map contains environmental feature information and velocity field data. The distribution of the values of all raster points in the workspace is [0,1]. To evaluate the algorithm's performance, several runs of experiments are performed for each algorithm, and the following performance indicators are introduced to measure and evaluate the strengths and weaknesses of the algorithm in terms of computational accuracy and efficiency.

(1) The average information collection $\mathrm { { I } _ { m e a n } , \mathrm { { I } _ { m e a n } } }$ satisfies the following equation:

$$
\mathrm{I} _ {\mathrm{mean}} = \frac {1}{\mathbb {N}} \sum_ {\mathrm{i=1}} ^ {\mathbb {N}} \mathrm{I} _ {\mathrm{i}}\tag{27}
$$

ℕ is the number of samples, i.e., the times of experiment replications.

(2) The standard deviation of the information collection $\mathrm { I } _ { \mathrm { s t d } } , \mathrm { I } _ { \mathrm { s t d } }$ satisfies the following equation.

$$
\mathrm {I_ {std}} = \sqrt {\frac {1}{\mathbb {N} - 1} \sum_ {\mathrm{i} = 1} ^ {\mathbb {N}} | \mathrm {I_ {i}} - \mathrm {I_ {mean}} | ^ {2}}\tag{28}
$$

(3) The average number of iterations.

(4) The average computation time.

5.2 Information-driven path planning for HAUV under different constraints

In this subsection, we analyze the optimization performance of the above six algorithms to solve the HAUV information-driven path planning problem under different constraints when the information weights of the sea and air environment features are the same.

## 5.2.1 Scenario 1: Path planning for a HAUV with limited energy

First, consider a HAUV carrying a finite energy $\operatorname { E } _ { \operatorname* { m a x } } .$ , assume that the starting position of the HAUV is $\mathbf { q } _ { \mathrm { i n i t } } { = } \left( 1 \mathrm { k m } , 3 . 7 5 \mathrm { k m } , 0 \mathrm { m } \right)$ and the mission end position is $\mathsf { q } _ { \mathrm { f i n a l } } \mathrm { = \ ( 4 k m , 3 . 7 5 k m , 0 m ) }$ and the mission time is set to $\mathrm { T } _ { \mathrm { m a x } } { = } \mathrm { i n f } .$ , the mission area is based on the analytic equation, and there exists a submerged obstacle space similar to the continental slope. In this parameter setting, each algorithm is repeated ten times to verify the algorithms' stability, average optimization performance, and average computational speed.

![](Zeng2022Informationdriven_figs/24728c68d181ab4e31fc30373fd9e984550c66c1ed8ec857d9ab884c82696558.jpg)  
(a)

![](Zeng2022Informationdriven_figs/ff895d48a8a21c2b630f5b9c5b6e8692ba676f24e9baffbd4ccd259b576b5dd2.jpg)  
(b)

![](Zeng2022Informationdriven_figs/d90deb9fb36ba6b016586b7333687fc214ff600dc383d2298396ba1cf2e5d5ec.jpg)  
(b)

![](Zeng2022Informationdriven_figs/75c299a0abf8c04307094a54758ff85a77a6ff9150482b9046a75e806fb60bef.jpg)  
(d)

![](Zeng2022Informationdriven_figs/f8b34da5d5caab3c18be0c674ce2d98835ab78322c615753a95de0f5ee2a0b6c.jpg)  
(e)

![](Zeng2022Informationdriven_figs/370f4260b76553412305b157000a35c387e6b70ca7bfaa9962b2dcb2565ca74f.jpg)  
(f)

![](Zeng2022Informationdriven_figs/8fcc9d26c3317f9df009718c1cff8bcc5e19e14f01be6533daf2bd890ddad3e7.jpg)  
(g)

![](Zeng2022Informationdriven_figs/d673c86ac1a6d83ac78329cc5a07a19f3b7bdfb4e585cdc174d89293398e20c6.jpg)  
(h)  
Figure 5 Scenario 1: Informative path, convergence curve and error bar produced by the path planners

TABLE 3 Scenario 1: Comparison of the optimal results of the simulation experiment algorithm

<table><tr><td>Algorithm</td><td>Amount of information collected</td><td>Iteration times</td><td>Energy (Emax)</td><td>consumption</td><td>Task execution time (h)</td></tr><tr><td>RAST*-I/E</td><td>1190.87</td><td>1912</td><td>0.99</td><td></td><td>7.41</td></tr><tr><td>RAST*-I</td><td>1023.72</td><td>1062</td><td>1.00</td><td></td><td>6.56</td></tr><tr><td>RAST</td><td>520.96</td><td>757</td><td>0.71</td><td></td><td>5.17</td></tr></table>

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

<table><tr><td>RRST*</td><td>934.25</td><td>2145</td><td>0.99</td><td>6.97</td></tr><tr><td>RIGT</td><td>795.79</td><td>1909</td><td>0.99</td><td>4.58</td></tr><tr><td>PSO</td><td>1080.51</td><td>946</td><td>1.00</td><td>7.48</td></tr></table>

TABLE 4 Scenario 1: Algorithm performance comparison

<table><tr><td>Algorithm</td><td>Average message size</td><td>Standard deviation</td><td>Average number of iterations</td><td>Average computation time (s)</td></tr><tr><td>RAST*-I/E</td><td>1077.20</td><td>84.01</td><td>1401</td><td>52</td></tr><tr><td>RAST*-I</td><td>963.08</td><td>58.07</td><td>951</td><td>30</td></tr><tr><td>RAST</td><td>485.21</td><td>28.79</td><td>611</td><td>3</td></tr><tr><td>RRST*</td><td>734.70</td><td>171.23</td><td>1294</td><td>43</td></tr><tr><td>RIGT</td><td>656.06</td><td>121.73</td><td>1360</td><td>34</td></tr><tr><td>PSO</td><td>912.47</td><td>108.99</td><td>828</td><td>46</td></tr></table>

Figure 5 show the HAUV sampling path, the distribution and convergence curve of environmental feature information collected along this path, and the error plot of information collection for ten repetitions of each algorithm. In the figure, the obstacle space is represented by a grey surface, the starting point is a yellow dot, and the endpoint is a green dot. The RAST\*-I/E algorithm, RAST\*- I algorithm, RAST algorithm, RRST\*, RIGT, and PSO algorithms are orange, blue, red-brown, purple, lime green, and yellow-brown, respectively. From the graph of the optimized sampling paths of each algorithm, it can be seen that there is no limit on the RIGT algorithm performing aerial sampling in the pre-task period. The main reason is that the sampling volume per unit energy consumption of the HAUV for underwater sampling is much higher than that for aerial sampling. In the absence of a mission time constraint, a global algorithm would choose to slowly collect the amount of information in the environment for a longer period to save the energy of the HAUV. However, the RIGT algorithm is relatively weak in global optimization, and the algorithm does not learn the experience of increasing the amount of information collected by extending the sampling time through iterations. Hence, the optimized path information collection is less.

The convergence curves in Figure 5g show that the RAST\*-I/E algorithm has the most information collection. The three algorithms with relatively slow convergence are the RAST\*-I/E algorithm, the RRST\* algorithm, and the RIGT algorithm, which require a relatively large number of iterations to find the asymptotically optimal solution. Figure 5h shows the deviation of the results for each algorithm for ten repeated experiments. The two algorithms with larger deviation are RRST\* algorithm and RIGT algorithm, which can also be seen from the standard deviation in Table 4. The reason may be that these two algorithms' sampling strategies are random, lacking good environmental information to guide the algorithm, which may repeatedly search near a local solution so that the results are no longer improved in a certain iterative process.

From the results recorded in Table 3, we can find that, except for the RAST algorithm, the optimized paths of the other five algorithm almost exhaust the energy, meaning energy usage is maximized. The main reason is that, although the tournament-based poin selection method can guide the adaptive sampling tree to grow toward regions with high values, the algorithm structure does not have the process of initiation search and parent node reshaping. The algorithm lacks initiation and does not re-evaluate the adaptability of the tree nodes to the newly generated nodes. The simulation results show that the computation time of the RAST algorithm is significantly better than the rest of the algorithms. Still, it can only solve the feasible path, not the global optimal path, and thus the RAST algorithm has the lowest optimization performance.

From Tables 3 and 4, we can also obtain that the three algorithms with the best optimization performance are the RAST\*-I/E algorithm, the RAST\*-I algorithm and the PSO algorithm. All three algorithms have an optimal information collection of more than 1000. However, it can also be seen in Figure 5 that the paths generated by the RAST\*-I/E algorithm are sampled back and forth underwater. In contrast, the paths generated by the PSO algorithm generates paths with a shape of S, and ultimately the PSO algorithm does not collect as much information as the RAST\*-I/E algorithm

Comparing the simulation results of RAST\*-I/E algorithm and the RAST\*-I algorithm, the RAST\*-I/E algorithm has slightly higher optimization performance than the RAST\*-I algorithm but slightly lower optimization speed. The only difference between these two algorithms is the heuristic factor in the information heuristic search process. The heuristic factor of the RAST\*-I/E algorithm adopts

![](Zeng2022Informationdriven_figs/b93b8178f8b3f16586f1fb46c6bddf0be828725b1f90f36913ef243ae2a1541c.jpg)

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

the information collection amount per unit energy consumption of the path. In contrast, the heuristic factor of the $\mathrm { R A S T ^ { * } { - } I }$ algorithm adopts the information collection amount directly, which means that the information heuristic search process of the RAST\*-I algorithm does not consider the power consumption of the HAUV. On the other hand, the $\mathrm { R A S T ^ { * } – I / E }$ algorithm considers the power consumption of the HAUV, and the iterative search process is oriented toward collecting more information with less energy, but this increases the number of iterations. Therefore, the $\mathrm { R A S T ^ { * } – I / E }$ algorithm is not as fast as the $\mathrm { R A S T ^ { * } { - } I }$ algorithm, but its optimization performance is better.

## 5.2.2 Algorithm 2: Path planning for a HAUV under the constraints of limited energy and mission time

In a real mission, marine scientists usually specify the mission time so that information can be obtained on time, which also facilitates the recovery of the HAUV. The environmental characteristics of the target area are downloaded from the official NOAA website for a small area in the Gulf of Mexico. Since the raster scale of the data provided by the official NOAA website is too large, this section scales the dataset to store the same feature information in a square environment of 50m in length, width and height for each raster. The dataset is normalized to $\mathrm { I _ { a i r } , I _ { s e a } } ~ \in ~ [ 0 , 1 ]$ . Set the HAUV's starting position as $\mathbf { q } _ { \mathrm { i n i t } } { = } ( 0 . 5 \mathrm { k m } , 2 . 5 \mathrm { k m } , 0 \mathrm { m } )$ and the mission end position as $\mathtt { q _ { i n i t } } { = } ( 4 . 5 \mathrm { k m } , 2 . 5 \mathrm { k m } , 0 \mathrm { m } )$ , the mission time is $\mathrm { T } _ { \mathrm { m a x } } = 3 \mathrm { h }$

From Figure 6, it can be seen that the RAST\*-I/E algorithm has the least remaining red and blue areas compared to other algorithms. It means that the RAST\*-I/E algorithm captures the most information, which is quantitatively shown in Figure $6 \mathrm { g }$ and Table 5. Combining Figure 6h and Table 6, it can be found that the three algorithms with the best optimization performance are still the $\mathrm { R A S T ^ { * } – I / E }$ algorithm, $\mathrm { R A S T ^ { * } { - } I }$ algorithm and PSO algorithm.

The optimal results in Table 5 show that the path generated by the $\mathrm { R A S T ^ { * } – I / E }$ algorithm and the $\mathrm { R A S T ^ { * } { - } I }$ algorithm used almost all the power and mission time. The $\mathrm { R R S T ^ { * } }$ , RIGT and PSO algorithms reach the boundary of one single constraint and have a fair search capability, while the RAST algorithm still only generates feasible solutions. The performance metrics in Table 6 still reflect a similar situation to Scenario 1, i.e., the random sampling strategy makes the ${ \mathrm { R R S T } } ^ { * }$ algorithm and the RIGT algorithm require more iterations to find the global solution. The RAST\*-I/E algorithm performs better under multiple constraints than one single constraint

![](Zeng2022Informationdriven_figs/be8a3d7fd9a4f65933af8823eedb803b376be197ddb8a94e0fc40da2a5078a8c.jpg)

![](Zeng2022Informationdriven_figs/8b4bfed947202c2075cdb9abb529cef1e444405e11172981cd741d44b7c3f8aa.jpg)

![](Zeng2022Informationdriven_figs/d321bb9637522eaea2bbd253aadce5341c7bcb346235c05a79ada073a4c48217.jpg)  
(b)

(a)  
![](Zeng2022Informationdriven_figs/477baedbc292b54df679a578ec52f086b284544c99d81ab9047b598e29882a41.jpg)  
(b)

![](Zeng2022Informationdriven_figs/6811960db6c809c863043ffe0546e1a6d9c762063fd1a2fd9e6459da5c94184a.jpg)

![](Zeng2022Informationdriven_figs/bdb9682e8c6636497d71f38fdc6af0927d55e7b69c5f20b0b02c00db87a45451.jpg)  
(e)

(d)  
![](Zeng2022Informationdriven_figs/ba53382ba22209b6d56849c75d0301e50f0bf950126ee97abd84736d96eb076b.jpg)  
(f)

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

![](Zeng2022Informationdriven_figs/2bca8f2b8b4e6d0f4d7a792a400b7b45e56e52711606cfa8b875cbf5a0c96fd8.jpg)  
(g)

![](Zeng2022Informationdriven_figs/dd163380a8bf8332b62d1da92fc07e1b554354133b3f5658bc5b29e11eee8848.jpg)  
(h)  
Figure 6 Scenario 2: Informative path, convergence curve and error bar produced by the path planners

TABLE 5 Scenario 2: Comparison of the optimal results of the simulation experiment algorithm

<table><tr><td>Algorithm</td><td>Amount of information collected</td><td>Iteration times</td><td>Energy (Emax)</td><td>consumption</td><td>Task execution time (h)</td></tr><tr><td>RAST*-I/E</td><td>836.08</td><td>1070</td><td>0.99</td><td></td><td>2.99</td></tr><tr><td>RAST*-I</td><td>749.42</td><td>1508</td><td>1.00</td><td></td><td>2.99</td></tr><tr><td>RAST</td><td>381.63</td><td>413</td><td>0.88</td><td></td><td>1.46</td></tr><tr><td>RRST*</td><td>611.68</td><td>1428</td><td>0.89</td><td></td><td>2.97</td></tr><tr><td>RIGT</td><td>566.38</td><td>1939</td><td>0.97</td><td></td><td>2.89</td></tr><tr><td>PSO</td><td>739.35</td><td>1054</td><td>1.00</td><td></td><td>2.88</td></tr></table>

TABLE 6 Scenario 2: Repeated experimental algorithm performance metrics comparison

<table><tr><td>Algorithm</td><td>Average message size</td><td>Standard deviation</td><td>Average number of iterations</td><td>Average computation time (s)</td></tr><tr><td>RAST*-I/E</td><td>760.21</td><td>44.73</td><td>760</td><td>41</td></tr><tr><td>RAST*-I</td><td>672.20</td><td>59.80</td><td>766</td><td>43</td></tr><tr><td>RAST</td><td>321.70</td><td>39.59</td><td>549</td><td>3</td></tr><tr><td>RRST*</td><td>438.34</td><td>132.26</td><td>837</td><td>21</td></tr><tr><td>RIGT</td><td>426.40</td><td>74.17</td><td>977</td><td>25</td></tr><tr><td>PSO</td><td>659.49</td><td>84.57</td><td>616</td><td>45</td></tr></table>

5.2.3 Scenario 3: Path planning for a HAUV under the constraints of limited energy and tight mission time While the mission time studied in Scenario 2 is more relaxed, this scenario will conduct experiments for path planning of a HAUV under a tighter mission time. It is assumed that the HAUV needs to be recovered at this location after one hour. As shown in Figure 7, the areas with high information values of the atmosphere are distributed in the range of [3km, 5km] on the x-axis. The areas with high information values of oceanic features are distributed in the range of [1km, 3km] on the x-axis. Due to the tight mission time, the HAUV prefers to collect atmospheric feature information, but it is constrained by the limited energy to perform only aerial sampling. The optimized path maximizes atmospheric and oceanic information collection under double constraints. The convergence curves in Figure $7 \mathrm { g }$ show that the RRST\* algorithm based on the random sampling strategy and the RIGT algorithm has the highest convergence. The RIGT algorithm converges the slowest. The information acquisition error in Figure 7h shows that the optimization capability of the algorithms in this example can be roughly divided into three echelons. The first echelon is the RAST\*-I/E algorithm, the second echelon is the RAST\*-I algorithm, RRST\* algorithm and PSO algorithm, and the third echelon is the RAST algorithm and RIGT algorithm.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

![](Zeng2022Informationdriven_figs/a6c0cef9ffef18fd8e43294d2951562e43414d9e8b161718e8d336c318ea9cf4.jpg)  
(a)

![](Zeng2022Informationdriven_figs/444c66f50c0290dedbee627e072d9ded4ce947d0066dd4b9a67853f13bb0f175.jpg)  
(b)

![](Zeng2022Informationdriven_figs/6c7004e98657dd0152459c98acb7d07a1087778f261cb9cd0437115f21e317eb.jpg)  
(c)

![](Zeng2022Informationdriven_figs/b0928dee92974a40ebcf78867455b517b74154db2897ed5beda714eec4108479.jpg)

![](Zeng2022Informationdriven_figs/c9662b0cb7a666731cd72ccd4e1a591aaa7456e95f912164ff57b1467deecc58.jpg)  
(e)

(d)  
![](Zeng2022Informationdriven_figs/8a92d980c88e5933201ff2a58362cff05d31e036f9c6275a2aa1d4ac4ad71259.jpg)  
(f)

![](Zeng2022Informationdriven_figs/a462dbac6e3b4b984eaa83f91734f09517e01f8ac6aec0215621e014ebe8aae5.jpg)  
(g)

![](Zeng2022Informationdriven_figs/6f65bfb2c5341e06d7899fcaff010ce6c1ec84778d2b50084b6a64e1656038d0.jpg)  
(h)

Figure 7 Scenario 3: Informative path, convergence curve and error bar produced by the path planners  
TABLE 7 Scenario 3: Comparison of the optimal results of the simulation experiment algorithm

<table><tr><td>Algorithm</td><td>Amount of information collected</td><td>Iteration times</td><td>Energy (Emax)</td><td>consumption</td><td>Task execution time (h)</td></tr><tr><td>RAST*-I/E</td><td>684.52</td><td>1027</td><td>1.00</td><td></td><td>0.94</td></tr><tr><td>RAST*-I</td><td>589.14</td><td>600</td><td>0.99</td><td></td><td>0.99</td></tr><tr><td>RAST</td><td>342.72</td><td>606</td><td>0.72</td><td></td><td>0.74</td></tr><tr><td>RRST*</td><td>608.90</td><td>1542</td><td>0.99</td><td></td><td>0.94</td></tr><tr><td>RIGT</td><td>405.55</td><td>1619</td><td>0.96</td><td></td><td>0.89</td></tr><tr><td>PSO</td><td>608.15</td><td>1014</td><td>0.99</td><td></td><td>1.00</td></tr></table>

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

TABLE 8 Scenario 3: Repeated experimental algorithm performance metrics comparison

<table><tr><td>Algorithm</td><td>Average message size</td><td>Standard deviation</td><td>Average iterations</td><td>number</td><td>of</td><td>Average computation time (s)</td></tr><tr><td>RAST*-I/E</td><td>620.33</td><td>48.60</td><td>999</td><td></td><td>45</td><td></td></tr><tr><td>RAST*-I</td><td>511.98</td><td>41.10</td><td>831</td><td></td><td>32</td><td></td></tr><tr><td>RAST</td><td>231.18</td><td>18.43</td><td>564</td><td></td><td>2</td><td></td></tr><tr><td>RRST*</td><td>513.00</td><td>63.02</td><td>1351</td><td></td><td>41</td><td></td></tr><tr><td>RIGT</td><td>234.90</td><td>87.40</td><td>695</td><td></td><td>26</td><td></td></tr><tr><td>PSO</td><td>521.01</td><td>60.59</td><td>750</td><td></td><td>63</td><td></td></tr></table>

From Table 7, we can calculate that the optimal result of the $\mathrm { R A S T ^ { * } – I / E }$ algorithm has 12% higher information collection than the RRST\* algorithm. The reason is that the $\mathrm { R A S T ^ { * } – I / E }$ algorithm introduces the tournament point selection method into the sampling strategy. Therefore, more sampling points fall in the regions where feature information is gathered. From Table 8, it can be calculated that the average information collection of the optimized results of the RAST\*-I/E algorithm is 19% higher than that of the second. The simulation results of this example fully verify the optimization performance and stability of the RAST\*-I/E. However, the speed of the RAST\*-I/E algorithm is only moderate. In addition, the average computation time of the PSO algorithm in Table 8 is higher than that of the remaining five algorithms, mainly because the process of finding feasible solutions for the initial particle swarm is uncertain.

## 5.3 Information-driven path planning for a HAUV with weighted environmental feature information

This subsection analytically investigates the performance of the above six algorithms for solving the HAUV in different weights of information on the sea and air environment.

5.3.1 Algorithm 4: Path planning for a HAUV with higher weight of ocean feature information than the atmosphere It is assumed that marine scientists are more interested in information of the ocean, assigning a weighting factor of ocean feature information weighting factor $\kappa _ { s e a } = 3$ and the weighting factor of atmospheric feature information $\kappa _ { a i r } = 1$

![](Zeng2022Informationdriven_figs/ec30aca73a51693ac7007b495dd893ad2508828d56734b706d079d1722e1e79b.jpg)

![](Zeng2022Informationdriven_figs/009e8ce96a5be9327b8e765327ccb63eeeb41b9ef8929ea361ed6c4469508e50.jpg)

(a)  
![](Zeng2022Informationdriven_figs/2794c42f6dc1265529b65e92a5034e51e25d15485cca4484bf8a821b87d62458.jpg)  
(c)

(b)  
![](Zeng2022Informationdriven_figs/84d9ebe3fa95ec7312a54b78ae48f6b5b57b8c89dd27d231914b61a5f68af38a.jpg)  
(d)

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

![](Zeng2022Informationdriven_figs/caa517b3219c311374659fd795b3e21ce68cfc2d6118b383a4ee73c1dcd5dc6e.jpg)  
(e)

![](Zeng2022Informationdriven_figs/88c14f2f63d48e3c373c9f245258f8f336a119245c7c07f19097baf8c8602445.jpg)  
(f)

![](Zeng2022Informationdriven_figs/e4cadd0d39b9cd44f5d7be087da3b49a618bfbdc9f8644091bb22051cdc04ea3.jpg)  
(g)

![](Zeng2022Informationdriven_figs/8c53c5099f89b933f3a22b75a3cf0b3430a5496b24ec46749acef1df3e3d42ee.jpg)  
(h)  
Figure 8 Scenario 4: Informative path, convergence curve and error bar produced by the path planners

TABLE 9 Scenario 4: Comparison of the optimal results of the simulation experiment algorithm

<table><tr><td>Algorithm</td><td>Amount of information collected</td><td>Iteration times</td><td>Energy (Emax)</td><td>consumption</td><td>Task execution time (h)</td></tr><tr><td>RAST*-I/E</td><td>2914.08</td><td>745</td><td>1.00</td><td></td><td>7.47</td></tr><tr><td>RAST*-I</td><td>2234.58</td><td>1148</td><td>1.00</td><td></td><td>6.21</td></tr><tr><td>RAST</td><td>1288.18</td><td>458</td><td>0.94</td><td></td><td>4.09</td></tr><tr><td>RRST*</td><td>1875.60</td><td>959</td><td>0.90</td><td></td><td>6.67</td></tr><tr><td>RIGT</td><td>2331.55</td><td>2493</td><td>1.00</td><td></td><td>6.89</td></tr><tr><td>PSO</td><td>2641.41</td><td>915</td><td>1.00</td><td></td><td>7.48</td></tr></table>

TABLE 10 Scenario 4: Repeated experimental algorithm performance metrics comparison

<table><tr><td>Algorithm</td><td>Average message size</td><td>Standard deviation</td><td>Average number of iterations</td><td>Average computation time (s)</td></tr><tr><td>RAST*-I/E</td><td>2841.31</td><td>87.36</td><td>1008</td><td>54</td></tr><tr><td>RAST*-I</td><td>2147.38</td><td>74.94</td><td>866</td><td>46</td></tr><tr><td>RAST</td><td>1132.68</td><td>86.04</td><td>528</td><td>2</td></tr><tr><td>RRST*</td><td>1648.89</td><td>139.46</td><td>987</td><td>45</td></tr><tr><td>RIGT</td><td>1686.39</td><td>416.07</td><td>1532</td><td>69</td></tr><tr><td>PSO</td><td>2569.83</td><td>40.51</td><td>947</td><td>94</td></tr></table>

As shown in Figure 8, each algorithm crosses the obstacle space and travels to the region where environmental feature information is gathered. Due to the high weight of ocean information, algorithms with high optimization capabilities focus on collecting underwater information. This conclusion is corroborated in figure 8, where only the RAST algorithm activates the cross-media motion mode for the HAUV. However, the optimized path does not capture more environmental information, so the RAST algorithm is still not able to search for the global solution. From Figure 8g and Figure 8h, it can be seen that the optimization speed and stability of the RIGT algorithm is poor. From Table 9, we can find that the $\mathrm { R A S T ^ { * } – I / E }$ algorithm, $\mathrm { R A S T ^ { * } { - } I }$ algorithm, RIGT algorithm, and PSO algorithm all make full use of the limited power of the HAUV before returning to the base. Hence, the optimal results of all four algorithms exceed 2000. From Table $^ { 1 0 , }$ the three algorithms with the best optimization performance are still $\mathrm { R A S T ^ { * } \mathrm { - I / E , R A S T ^ { * } \mathrm { - I } } } .$ and PSO. The optimization performance of the $\mathrm { R A S T ^ { * } – I / E }$ algorithm is 10.6% higher than that of the PSO algorithm.

5.3.2 Scenario 5: Path planning for a HAUV with a higher weighting of atmospheric feature information than the ocean Assuming that marine scientists are more interested in atmospheric information, a weighting factor $\kappa _ { \mathrm { a i r } } = 3$ is assigned to atmospheric information and a weighting factor $\kappa _ { \mathsf { s e a } } { = } 1$ to oceanic information.

From the paths of each algorithm shown in Figure 9, it can be found that, except for the RAST algorithm, all the other five algorithms only perform aerial sampling before heading to the endpoint, which is due to the high weight of atmospheric feature information.

According to the convergence curves Figure ${ 9 } \mathrm { g } ,$ it is found that the PSO algorithm and RAST\*-I/E algorithm generate the path with maximum information collection. In Tables 11 and 12, the optimal results and the performance indexes show that both algorithms perform well in repeated experiments. The optimization performance of the PSO algorithm is slightly higher than that of the RAST\*- I/E algorithm, and the number of iterations is reduced by nearly two times, which highlights that the PSO algorithm is indeed an excellent global optimization algorithm. However, the standard deviation of the PSO algorithm in repeated runs is higher than that of the $\mathrm { R A S T ^ { * } – I / E }$ algorithm, indicating that the PSO algorithm is not as stable as the $\mathrm { R A S T ^ { * } – I / E }$ algorithm. Moreover, the average computation time of the PSO algorithm is slightly longer than that of th $\mathrm { R A S T ^ { * } – I / E }$ algorithm, indicating that a large amount of time is wasted in finding the initial feasible solution. Still, once the initial feasible solution of the particle swarm is generated, the convergence speed of the algorithm's main loop can be accelerated, thus reducing the number of iterations. In summary, for this scenario, if a high stability algorithm is needed, this paper recommends the RAST\*-I/E algorithm; if a fast convergence algorithm is required, this paper recommends the PSO algorithm

![](Zeng2022Informationdriven_figs/91f89a2e5c5d927318f6727c100de3ba63671078d8f79ffe7662f6b0d6274067.jpg)

![](Zeng2022Informationdriven_figs/e8768579a9abe6f6f55070587d77a4f6043068ed71c41c33698b4ec6e8c5a5e4.jpg)  
(b)

(a)  
![](Zeng2022Informationdriven_figs/ad0f213c433bb550e3f7d5a5320e2186c9d38dc8d4bc0f533a22782f74c46f2e.jpg)  
(c)

![](Zeng2022Informationdriven_figs/76ccfb2509b2fffe2ae591fa5ec9653022408f414f20f0f7113956b7967ff196.jpg)

![](Zeng2022Informationdriven_figs/7d5e31f2a11c2d648b927d6e0c399e770d2190c4f31315d5d1eaf90e0d2f9197.jpg)  
(e)

(d)  
![](Zeng2022Informationdriven_figs/3941cb01f5fb8d0f46c7c9dbbda04d3774d4dd8db5b28cd4d0af006e36123f2b.jpg)  
(f)

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

![](Zeng2022Informationdriven_figs/019399734d98f2b180ebe8b61b0430e4b03a8b780a0446f3296fc55bc88551c9.jpg)  
(g)

![](Zeng2022Informationdriven_figs/8f467534049fe3a42830fee8a072f3f58a522f9ae50af456efe07591de5e371b.jpg)  
(h)  
Figure 9 Scenario 5: Informative path, convergence curve and error bar produced by the path planners

TABLE 11 Scenario 5: Comparison of the optimal results of the simulation experiment algorithm

<table><tr><td>Algorithm</td><td>Amount of information collected</td><td>Iteration times</td><td>Energy (Emax)</td><td>consumption</td><td>Task execution time (h)</td></tr><tr><td>RAST*-I/E</td><td>2229.48</td><td>1354</td><td>1.00</td><td></td><td>0.24</td></tr><tr><td>RAST*-I</td><td>1992.40</td><td>1347</td><td>1.00</td><td></td><td>0.24</td></tr><tr><td>RAST</td><td>1221.39</td><td>810</td><td>0.85</td><td></td><td>1.80</td></tr><tr><td>RRST*</td><td>1687.20</td><td>1059</td><td>0.94</td><td></td><td>0.23</td></tr><tr><td>RIGT</td><td>1893.54</td><td>628</td><td>1.00</td><td></td><td>0.33</td></tr><tr><td>PSO</td><td>2270.10</td><td>458</td><td>1.00</td><td></td><td>0.24</td></tr></table>

TABLE 12 Scenario 5: Repeated experimental algorithm performance metrics comparison

<table><tr><td>Algorithm</td><td>Average message size</td><td>Standard deviation</td><td>Average number of iterations</td><td>Average computation time (s)</td></tr><tr><td>RAST*-I/E</td><td>2088.10</td><td>98.65</td><td>1193</td><td>62</td></tr><tr><td>RAST*-I</td><td>1839.98</td><td>100.79</td><td>993</td><td>44</td></tr><tr><td>RAST</td><td>1085.83</td><td>72.46</td><td>414</td><td>1</td></tr><tr><td>RRST*</td><td>1341.29</td><td>254.53</td><td>543</td><td>23</td></tr><tr><td>RIGT</td><td>1255.39</td><td>249.53</td><td>607</td><td>26</td></tr><tr><td>PSO</td><td>2034.48</td><td>191.10</td><td>583</td><td>71</td></tr></table>

## 5.4 Robustness Analysis

To verify the robustness of these six algorithms, this subsection will conduct simulation experiments to evaluate three scenarios from single constraint condition, double constraint condition, and the sea-air environment with different weights, respectively. Each scenario is simulated 100 times, i.e., 100 different maps of sea-air environments and velocity fields are randomly generated, and the task start and end positions are randomly selected. The specific settings of the three mission scenarios are as follows.

\- Scenario 1: the HAUV carries a limited energy $E _ { m a x } ,$ but has no limits for the mission time.

\- Scenario 2: the HAUV carries a limited energy $E _ { m a x }$ with a mission time of a random number in the interval [1h, 3h].

\- Scenario 3: the HAUV carries a limited energy $E _ { m a x }$ with a mission time of $T _ { m a x } { = 3 \mathrm { h } }$ and atmospheric and oceanic information weights $\kappa _ { a i r }$ and $\kappa _ { s e a }$ are random integers in the interval [1,5].

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

![](Zeng2022Informationdriven_figs/dd8be76635893ec23443b7ecaa77c1bc90be38cae4c9139b5e0a89a0e0e0a341.jpg)  
(a) Mission Scenario 1

![](Zeng2022Informationdriven_figs/da537965785072b04f74800f87175d1ce408f4fbdd1b0c2538d95f8b0bc3ca10.jpg)

(b) Mission Scenario 2  
![](Zeng2022Informationdriven_figs/6e4eaf41590cd5fcd230f7ad1e54c46133419277ca016cd17c4b4cffae7b70ca.jpg)  
(c) Mission Scenario 3  
Figure 10 Robustness assessment results

The robustness experiments are judged by which algorithm can collect more information with the same setting. The algorithm with the highest number of winning results among 100 randomized simulations for each scenario is considered the most robust and more suitable for practical applications in such scenarios.

The results are shown in Figs. 10. The $\mathrm { R A S T ^ { * } – I / E }$ algorithm wins over the other five algorithms by an absolute margin, indicating that the paths optimized by the $\mathrm { R A S T ^ { * } – I / E }$ algorithm are more likely to capture more information, confirming the superiority of the $\mathrm { R A S T ^ { * } – I / E }$ algorithm in solving the HAUV information-driven path planning problem. On the other hand, as an excellent classical global optimization algorithm, the PSO algorithm is slightly less robust than the $\mathrm { R A S T ^ { * } – I / E }$ algorithm proposed in this paper in terms of adaptability and optimization capability.

## 6 SUMMARY

This paper presents a new RAST\*-I/E algorithm for information-driven path planning problems of HAUV. This ${ \mathrm { R A S T } } ^ { * } .$ -I/E algorithm innovatively combines the sampling strategy based on the tournament point selection method, information heuristic search processand the framework of $\mathrm { R R T ^ { * } }$ algorithm. In order to compare the effectiveness of the newly designed structure in the $\mathrm { R A S T ^ { * } – I / E }$ algorithm, the $\mathrm { R A S T ^ { * } { - } I }$ algorithm with the heuristic factor of total information is designed according to the information heuristic search process; the ${ \mathrm { R R S T } } ^ { * }$ algorithm based on the random sampling strategy is designed according to the sampling strategy; and the RAST without the information heuristic search and parent node reshaping process is designed according to the presence or absence of this process algorithm without this process according to the presence or absence of information heuristic search and parent node reshaping process. Moreover, the classical RIGT algorithm and the PSO algorithm are designed as the comparison algorithm. The simulation experiments were conducted to compare the above six algorithms' optimization performance, speed, and stability through five cases. The sampling strategy of the $\mathrm { R A S T ^ { * } – I / E }$ algorithm based on the tournament point selection method guides the adaptive sampling tree to explore the regions where information with higher values are located. The information heuristic search process is the key to preventing the algorithm from falling into local optimal paths. The RAST\*-I/E algorithm combines the advantages of tournament point selection, information heuristic search, and RRT\* algorithm to efficiently search the air-sea environment. Therefore, the obtained sampling path can collect the most information, which ensures the accuracy and robustness of the algorithm.

## ACKNOWLEDGMENTS

This Research is supported in part by the National Natural Science Foundation of China under grant 41706108 and in part by the Science and Technology Commission of Shanghai Municipality Project 20dz1206600 and in part by the Natural Science Foundation of Shanghai under Grant 20ZR1424800 and in partly by the Shanghai Jiao Tong University Scientific and Technological Innovation Funds under Grant 2019QYB04

## REFERENCES

[1] L. R. Centurioni et al., "Global in-situ observations of essential climate and ocean variables at the air-sea interface," Frontiers in Marine Science, Review vol. 6, no. JUL, 2019, Art no. 419, doi: 10.3389/fmars.2019.00419.

[2] J. Elston, B. Argrow, M. Stachura, D. Weibel, D. Lawrence, and D. Pope, "Overview of small fixed-wing unmanned aircraft for meteorological sampling," Journal of Atmospheric and Oceanic Technology, Article vol. 32, no. 1, pp. 97-115, 2015, doi: 10.1175/JTECH-D-13-00236.1.

[3] J. Meng, Y. Liu, R. Bucknall, W. Guo, and Z. Ji, "Anisotropic GPMP2: A Fast Continuous-Time Gaussian Processes Based Motion Planner for Unmanned Surface Vehicles in Environments With Ocean Currents," IEEE Transactions on Automation Science and Engineering, Article 2022, doi: 10.1109/TASE.2021.3139163.

[4] Z. Zeng, L. Lian, K. Sammut, F. He, Y. Tang, and A. Lammas, "A survey on path planning for persistent autonomy of autonomous underwater vehicles," Ocean Engineering, Review vol. 110, pp. 303-313, 2015, doi: 10.1016/j.oceaneng.2015.10.007.

[5] M. Yang, Y. Wang, Y. Liang, and C. Wang, "A New Approach to System Design Optimization of Underwater Gliders," IEEE/ASME Transactions on Mechatronics, Article 2022, doi: 10.1109/TMECH.2022.3143125.

[6] Z. Zeng, K. Sammut, L. Lian, A. Lammas, F. He, and Y. Tang, "Rendezvous Path Planning for Multiple Autonomous Marine Vehicles," IEEE Journal of Oceanic Engineering, Article vol. 43, no. 3, pp. 640-664, 2018, doi: 10.1109/JOE.2017.2723058.

[7] C. Lyu et al., "Toward a gliding hybrid aerial underwater vehicle: Design, fabrication, and experiments," Journal of Field Robotics, Article 2022, doi: 10.1002/rob.22063.

[8] D. Lu et al., "Design, fabrication, and characterization of a multimodal hybrid aerial underwater vehicle," Ocean Engineering, Article vol. 219, 2021, Art no. 108324, doi: 10.1016/j.oceaneng.2020.108324.

[9] X. Liang, C. Liu, and Z. Zeng, "Multi-domain informative coverage path planning for a hybrid aerial underwater vehicle in dynamic environments," Machines, Article vol. 9, no. 11, 2021, Art no. 278, doi: 10.3390/machines9110278.

[10] Z. Zeng, C. Lyu, Y. Bi, Y. Jin, D. Lu, and L. Lian, "Review of hybrid aerial underwater vehicle: Cross-domain mobility and transitions control," Ocean Engineering, Review vol. 248, 2022, Art no. 110840, doi: 10.1016/j.oceaneng.2022.110840.

[11] R. Hu et al., "Modeling, characterization and control of a piston-driven buoyancy system for a hybrid aerial underwater vehicle," Applied Ocean Research, Article vol. 120, 2022, Art no. 102925, doi: 10.1016/j.apor.2021.102925

[12] A. Vasilijević, N. Đ, F. Mandić, N. Mišković, and Z. Vukić, "Coordinated Navigation of Surface and Underwater Marine Robotic Vehicles for Ocean Sampling and Environmental Monitoring," IEEE/ASME Transactions on Mechatronics, vol. 22, no. 3, pp. 1174-1184, 2017, doi: 10.1109/TMECH.2017.2684423.

[13] J. Binney, A. Krause, and G. S. Sukhatme, "Informative path planning for an autonomous underwater vehicle," in 2010 IEEE International Conference on Robotics and Automation, 2010: IEEE, pp. 4791-4796.

[14] T. Somers and G. A. Hollinger, "Human–robot planning and learning for marine data collection," Autonomous Robots, vol. 40, no. 7, pp. 1123-1137, 2016.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

[15] T. O. Fossum et al., "Information‐driven robotic sampling in the coastal ocean," Journal of Field Robotics, vol. 35, no. 7, pp. 1101-1121, 2018.

[16] E. L. Johnson, G. L. Nemhauser, and M. W. Savelsbergh, "Progress in linear programming-based algorithms for integer programming: An exposition," Informs journal on computing, vol. 12, no. 1, pp. 2-23, 2000.

[17] N. K. Yilmaz, C. Evangelinos, P. F. Lermusiaux, and N. M. Patrikalakis, "Path planning of autonomous underwater vehicles for adaptive sampling using mixed integer linear programming," IEEE Journal of Oceanic Engineering, vol. 33, no. 4, pp. 522-537, 2008.

[18] A. Singh, A. Krause, C. Guestrin, and W. J. Kaiser, "Efficient informative sensing using multiple robots," Journal of Artificial Intelligence Research, vol. 34, pp. 707-755, 2009.

[19] J. Binney and G. S. Sukhatme, "Branch and bound for informative path planning," in 2012 IEEE international conference on robotics and automation, 2012: IEEE, pp. 2147-2154.

[20] P. Stankiewicz, Y. T. Tan, and M. Kobilarov, "Adaptive sampling with an autonomous underwater vehicle in static marine environments," Journal of Field Robotics, vol. 38, no. 4, pp. 572-597, 2021.

[21] K. D. Heaney, G. Gawarkiewicz, T. F. Duda, and P. F. Lermusiaux, "Nonlinear optimization of autonomous undersea vehicle sampling strategies for oceanographic data‐assimilation," Journal of Field Robotics, vol. 24, no. 6, pp. 437-448, 2007.

[22] K. D. Heaney, P. F. Lermusiaux, T. F. Duda, and P. J. Haley, "Validation of genetic algorithm-based optimal sampling for ocean data assimilation," Ocean Dynamics, vol. 66, no. 10, pp. 1209-1229, 2016.

[23] M. Arzamendia, D. Gregor, D. G. Reina, and S. L. Toral, "An evolutionary approach to constrained path planning of an autonomous surface vehicle for maximizing the covered area of Ypacarai Lake," Soft Computing, vol. 23, no. 5, pp. 1723- 1734, 2019.

[24] S. Frolov, B. Garau, and J. Bellingham, "Can we do better than the grid survey: Optimal synoptic surveys in presence of variable uncertainty and decorrelation scales," Journal of Geophysical Research: Oceans, vol. 119, no. 8, pp. 5071-5090, 2014.

[25] H. Zhou, Z. Zeng, and L. Lian, "Adaptive re-planning of AUVs for environmental sampling missions: A fuzzy decision support system based on multi-objective particle swarm optimization," International Journal of Fuzzy Systems, vol. 20, no. 2, pp. 650-671, 2018.

[26] C. Xiong, D. Lu, Z. Zeng, L. Lian, and C. Yu, "Path planning of multiple unmanned marine vehicles for adaptive ocean sampling using elite group-based evolutionary algorithms," Journal of Intelligent & Robotic Systems, vol. 99, no. 3, pp. 875-889, 2020.

[27] G. Colmenares, F. Halal, and M. B. Zaremba, "Ant colony optimization for data acquisition mission planning," Management and Production Engineering Review, vol. 5, 2014.

[28] C. Xiong, Z. Zeng, and L. Lian, "Path Planning of Multi-Modal Underwater Vehicle for Adaptive Sampling Using Delaunay Spatial Partition-Ant Colony Optimization," in 2018 OCEANS-MTS/IEEE Kobe Techno-Oceans (OTO), 2018: IEEE, pp. 1-8.

[29] Y. Hu, D. Wang, J. Li, Y. Wang, and H. Shen, "Adaptive Environmental Sampling for Underwater Vehicles Based on Ant Colony Optimization Algorithm," in Global Oceans 2020: Singapore–US Gulf Coast, 2020: IEEE, pp. 1-9.

[30] R. P. Anderson, G. S. Dinolov, D. Milutinović, and A. M. Moore, "Maximally-informative regional ocean modeling system (ROMS) navigation of an AUV in uncertain ocean currents," in Dynamic Systems and Control Conference, 2012, vol. 45318: American Society of Mechanical Engineers, pp. 291-297.

[31] G. Ferri, M. Cococcioni, and A. Alvarez, "Mission planning and decision support for underwater glider networks: A sampling on-demand approach," Sensors, vol. 16, no. 1, p. 28, 2016.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

[32] A. Zamuda, J. D. H. Sosa, and L. Adler, "Constrained differential evolution optimization for underwater glider path planning in sub-mesoscale eddy sampling," Applied Soft Computing, vol. 42, pp. 93-118, 2016.

[33] G. Hitz, E. Galceran, M. È. Garneau, F. Pomerleau, and R. Siegwart, "Adaptive continuous‐space informative path planning for online environmental monitoring," Journal of Field Robotics, vol. 34, no. 8, pp. 1427-1449, 2017.

[34] M. Popovic, G. Hitz, J. Nieto, I. Sa, R. Siegwart, and E. Galceran, "Online informative path planning for active classification using uavs," arXiv preprint arXiv:1609.08446, 2016.

[35] S. Karaman and E. Frazzoli, "Sampling-based algorithms for optimal motion planning," The international journal of robotics research, vol. 30, no. 7, pp. 846-894, 2011.

[36] G. A. Hollinger and G. S. Sukhatme, "Sampling-based robotic information gathering algorithms," The International Journal of Robotics Research, vol. 33, no. 9, pp. 1271-1287, 2014.

[37] M. Ghaffari Jadidi, J. Valls Miro, and G. Dissanayake, "Sampling-based incremental information gathering with applications to robotic exploration and environmental monitoring," The International Journal of Robotics Research, vol. 38, no. 6, pp. 658-685, 2019.

[38] R. Cui, Y. Li, and W. Yan, "Mutual information-based multi-AUV path planning for scalar field sampling using multidimensional RRT," IEEE Transactions on Systems, Man, and Cybernetics: Systems, vol. 46, no. 7, pp. 993-1004, 2015.

[39] A. Viseras, D. Shutin, and L. Merino, "Robotic active information gathering for spatial field reconstruction with rapidly exploring random trees and online learning of Gaussian processes," Sensors, vol. 19, no. 5, p. 1016, 2019.

[40] C. Xiong, H. Zhou, D. Lu, Z. Zeng, L. Lian, and C. Yu, "Rapidly-exploring adaptive sampling Tree\*: A sample-based path-planning algorithm for unmanned marine vehicles information gathering in variable ocean environments," Sensors, vol. 20, no. 9, p. 2515, 2020.

[41] D. Lu, Y. Guo, C. Xiong, Z. Zeng, and L. Lian, "Takeoff and Landing Control of a Hybrid Aerial Underwater Vehicle on Disturbed Water's Surface," IEEE Journal of Oceanic Engineering, Article 2021, doi: 10.1109/JOE.2021.3124515.

[42] J. McConnell, F. Chen, and B. Englot, "Overhead Image Factors for Underwater Sonar-Based SLAM," IEEE Robotics and Automation Letters, vol. 7, no. 2, pp. 4901-4908, 2022, doi: 10.1109/LRA.2022.3154048.

[43] G. Bruzzone, G. Bruzzone, M. Bibuli, and M. Caccia, "Autonomous mine hunting mission for the Charlie USV," in OCEANS 2011 IEEE - Spain, 6-9 June 2011 2011, pp. 1-6, doi: 10.1109/Oceans-Spain.2011.6003469.

[44] S. K. Gan and S. Sukkarieh, "Multi-UAV target search using explicit decentralized gradient-based negotiation," in 2011 IEEE International Conference on Robotics and Automation, 2011: IEEE, pp. 751-756.

[45] P. Lanillos, S. K. Gan, E. Besada-Portas, G. Pajares, and S. Sukkarieh, "Multi-UAV target search using decentralized gradient-based negotiation with expected observation," Information Sciences, vol. 282, pp. 92-110, 2014.

[46] D. Zhu, H. Huang, and S. X. Yang, "Dynamic task assignment and path planning of multi-AUV system based on an improved self-organizing map and velocity synthesis method in three-dimensional underwater workspace," IEEE Transactions on Cybernetics, vol. 43, no. 2, pp. 504-514, 2013.

[47] C. YongBo, M. YueSong, Y. JianQiao, S. XiaoLong, and X. Nuo, "Three-dimensional unmanned aerial vehicle path planning using modified wolf pack search algorithm," Neurocomputing, vol. 266, pp. 445-457, 2017.

[48] Y. Zeng and R. Zhang, "Energy-efficient UAV communication with trajectory optimization," IEEE Transactions on Wireless Communications, vol. 16, no. 6, pp. 3747-3760, 2017.

[49] A. Zamuda and J. D. H. Sosa, "Differential evolution and underwater glider path planning applied to the short-term opportunistic sampling of dynamic mesoscale ocean structures," Applied Soft Computing, vol. 24, pp. 95-108, 2014.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

[50] B. Garau, A. Alvarez, and G. Oliver, "AUV navigation through turbulent ocean environments supported by onboard H ADCP," in Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006., 2006: IEEE, pp. 3556-3561.

[51] D. Lu, C. Xiong, Z. Zeng, and L. Lian, "Adaptive dynamic surface control for a hybrid aerial underwater vehicle with parametric dynamics and uncertainties," IEEE Journal of Oceanic Engineering, vol. 45, no. 3, pp. 740-758, 2019.