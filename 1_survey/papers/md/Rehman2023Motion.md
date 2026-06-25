---
citation_key: Rehman2023Motion
arxiv_id: 2310.14339
arxiv_url: "https://arxiv.org/abs/2310.14339"
title: "Motion Planning for Autonomous Ground Vehicles Using Artificial Potential Fields: A Review"
authors_short: "Aziz ur Rehman et al."
year: 2023
direction_tag: R_surveys
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:33:51Z
origin: ai+web
reviewed: false
---

# Motion Planning for Autonomous Ground Vehicles Using Artificial Potential Fields: A Review

Aziz ur Rehman<sup>a,</sup> <sup>\*</sup>, Ahsan Tanveer<sup>a,</sup> <sup>\*</sup>, M. Touseef Ashraf<sup>a</sup>, Umer Khan<sup>a</sup>

<sup>a</sup> Department of Mechanical and Aerospace Engineering, Institute of Avionics and Aeronautics, Air University, Islamabad 44000, Pakistan

<sup>\*</sup> Corresponding author: Aziz ur Rehman; Ahsan Tanveer, Email: azizkhokhar11@gmail.com; ahsan.tanveer@mail.au.edu.pk

## K E Y W O R D S

Autonomous Vehicle Motion Planning Artificial Potential Field Path Planning

## A B S T R A C T

Autonomous ground vehicle systems have found extensive potential and practical applications in the modern world. The development of an autonomous ground vehicle poses a significant challenge, particularly in identifying the best path plan, based on defined performance metrics such as safety margin, shortest time, and energy consumption. Various techniques for motion planning have been proposed by researchers, one of which is the use of artificial potential fields. Several authors in the past two decades have proposed various modified versions of the artificial potential field algorithms. The variations of traditional APF approach have given answer to prior shortcomings. This gives potential rise to a strategic survey on the improved versions of this algorithm. This study presents a review of motion planning for autonomous ground vehicles using artificial potential fields. Each article is evaluated based on criteria that involve, the environment type, which may be either static or dynamic, the evaluation scenario, which may be real-time or simulated, and the method used for improving the search performance of the algorithm. All the customized designs of planning models are analysed and evaluated. At the end, the results of the review are discussed and future works are proposed.

## 1. Introduction

Autonomous Ground Vehicles or AGVs are autonomously navigated vehicles that rely on advanced sensors, cameras, and software tools to navigate and operate independently. AGVs are landbased counterparts to autonomous aerial vehicles (AAVs), [1] and autonomous underwater vehicles (AUVs) [2]. A variety of dull, dirty, and dangerous activities are nowadays being performed through the use of AGV robots. Their applications can be found in agriculture and pest control, security and surveillance, exploration and navigation, reconnaissance, and scouting operations. The integration of autonomy in AGVs make them capable of making independent decisions and taking actions based on the surrounding environment information. The simplified system layer of an autonomous ground vehicle system is shown in Figure 1.

![](Rehman2023Motion_figs/9e978627b15a3cb03356dfb7a8286ca53732af59b378d16bb365bba7615ffff1.jpg)  
Figure 1. Layers of an Autonomous System.

The optimized navigation of an AGV, while avoiding obstacles in the static and dynamic environment, requires the use of optimized path and motion planning algorithms. The algorithm determines a feasible path from a start position to a goal (target) position and optimize the plan along some defined criteria. These criteria or performance measures of the algorithm include time and distance minimization, safety, comfort, and controlling effort, which are used to help identify the best feasible path.

Motion planning of UGVs is a challenging task. it is hard to solve it in a single integrated process. For this reason, motion planning is solved by dividing the whole problem into multiple layers of abstraction. At the top-level layer, the planner handles long-term planning. In this layer, the planner defines the problem over the entire map of the driving scenario, that is from the current location in the environment, through the road network to the target location. This can be termed global path planning. Next is the behavioural planner of the vehicle and is responsible for safe behavioural actions and execution of manoeuvres along the path given by the top-level layer. These behavioural actions may include lane changing, lane keeping, parking, or intersection crossing. At the end layer, the local planning is executed. This layer performs immediate or reactive planning to dynamic obstacles discovered along the global path, as well as define the motion and velocity profile, that is smooth, safe, efficient, and satisfies the constraints of the vehicle and the environment.

Path planning can be divided into static path planning and dynamic path planning from the perspective of whether the environment obstacles are moving or not. It is noted that for global path planning, the environment is generally assumed to be static. This layer of planning is performed before the robots begin to navigate hence offline, while that is not the case for local planning. During the local planning phase, the planner executes reactive planning and hence online, while traversing on the global path based on the data from the on-board sensors. This assumes incomplete knowledge of the environment, hence optimal for navigation in dynamic environments. Figure 2 best illustrates the scenario for the local (online) and global (offline) planning for the AGV robot.

![](Rehman2023Motion_figs/63a29df312d0975147efb574299ddf97fbb1835d8dec73d89c3027feae0721a6.jpg)  
Figure 2. Scenario for Local and Global Path Planning [3].

The advancements in the development of autonomy in AGVs have led to highly accurate 3-D environmental models. However, for practical application, the autonomous vehicle has to navigate a safe and optimized path plan. It is hard to solve the path planning problem, which is generally considered a non-deterministic polynomial-time (‘‘NP”) problem, considering more complications, such as the increase in the degree of freedom (DOF) of the system in a 3-D environment. Additionally, the problem formulation of the AGV system involves constraints like non-holonomic motion constraints or dynamic constraints, which increase the complexity of the problem [3]. In other cases, the computational efficiency and the compatibility of the motion plan with the assumptions required for optimal control, to make the path traceable are also a significant challenge [4].

A variety of different surveys have been presented, such as in [3], a systematic survey of path planning was presented, which classified a variety of planning techniques as classical and heuristic techniques. In [4], a survey of planning and control was presented, giving attention to tailoring and integration the two designs. While, different papers have classified the planning techniques according to the nature of their review, such as traditional and machine learning algorithms [5]. A more complete classification of path and motion planners was presented in [6]. Going deeper into the study, there have been a growing number of surveys on motion planners. However, a review of modified and improved versions of one particular algorithm are undiscovered. Limited research has been found, such as Short et al. [7] gave a review of sampling-based planners. Similarly, just recently in 2023, Paliwal [8] published a survey of improved versions of the A-star family of motion planners, which are similar in standings to the artificial potential field algorithms.

In this review, we have selected to review versions of artificial potential field (APF) as the planning algorithm for autonomous ground vehicles. There have been a variety of different improved versions of APF planning algorithm. Such variations in the traditional APF algorithms have given answer to prior shortcomings. Ultimately, this gives potential importance to a strategic survey on versions of this algorithm. Every article in this survey is evaluated based on criteria that involve, the environment type, which may be either static or dynamic, the evaluation scenario, which may be real-time or simulated, and the method used for improving the search performance and optimization of the APF path plan. This paper presents a review that lists different variants of the APF motion planning approach and discusses results.

The paper is organized as follows: Section 2 provides a comprehensive overview of the structure of the APF algorithm; Section 3 will cover review and analysis of the different variants of the APF motion planning for AGVs; In Section 4, results of the literature will be discussed; At the end, in section $^ { 5 , }$ a conclusion and future recommendations will be drawn out from the paper.

## 2. Artificial Potential Field

Artificial potential field, abbreviated as APF was first proposed by Khatib et al. [9]. It is a wellrecognized grid-based motion planning approach that is used nowadays as a reactive planner for obstacle avoidance. It can be used for planning in both offline and online maps, in other words, for both global and local planning.

The basis of the APF method in motion planning follows the natural characteristic of an electrostatic potential. The interaction of the electrostatic particles in physics is given as

$$
F = \frac {- k q _ {1} q _ {2}}{r ^ {2}}
$$

where <sub>??</sub> is the interactions constant, $q _ { 1 }$ and $q _ { 2 }$ are the electric charges of the particles, and <sub>??</sub> is the distance between these particles. If the charge of the two particles is the same, it repels, Conversely, if the charges are opposite, they attract. Such is the formulation of the APF problem. Both, the goal point and the obstacles, and in some cases the road boundaries exert force fields on the ego vehicle. The goal exerts a force of attraction $F _ { a t t }$ while the obstacle and road boundaries exert a repulsive force $F _ { r e p }$ . The attraction force is also termed as the gravity force. This means that the traditional APF is a combination of two different potential functions. If we consider the position of a robot at a particular time (t) to be $\boldsymbol { q } ~ = ~ [ x y ] ^ { T }$ then the force of attraction $F _ { a t t }$ can be modelled as

$$
F _ {a t t} (q) = - \nabla V _ {a t t} (q)
$$

where

$$
V _ {a t t} (q) = \frac {1}{2} \xi p ^ {2} \bigl (q, q _ {g o a l} \bigr)
$$

Here $V _ { a t t } ( q )$ is the attractive potential, $\xi$ is the gain parameter which has a position value, while, $p ( q , q _ { g o a l } )$ is the distance between the position of the ego vehicle q and the goal location $\begin{array} { r } { q _ { g o a l } . } \end{array}$ Mathematically $p \big ( q , q _ { g o a l } \big ) = | | q _ { g o a l } - q | |$ which defines that the value converges to zero as the ego vehicle moves towards the target location.

Similarly, the repulsive force of attraction $F _ { r e p }$ , which is from the obstacle is modeled as

$$
F _ {r e p} (q) = - \nabla V _ {r e p} (q)
$$

Where,

$$
V _ {r e p} (q) = \left\{ \begin{array}{l l} \frac {\eta}{\sqrt {\rho (q , q _ {a b s})}} & \quad i f \rho (q, q _ {a b s}) \leq \rho_ {o} \\ 0 & \quad i f \rho (q, q _ {a b s}) \geq \rho_ {o} \end{array} \right.
$$

Here $\eta$ is the repulsive gain parameter, $V _ { r e p } ( q )$ is the repulsive potential, while $\rho ( q , q _ { a b s } )$ is the distance between the obstacle and the ego vehicle position. The c-obstacle of the ego vehicle dimension is represented by the variable $\rho _ { o }$ which is a positive number. The resultant force of the attractive and repulsive forces is represented as,

$$
F _ {t o t a l} = F _ {a t t} + F _ {r e p}
$$

This resultant force $F _ { t o t a l }$ is a vector quantity, which represents the direction of movement of the ego vehicle [10]. An illustration of this resultant force is shown in Figure 3. The resultant force provides the reference for the AGV local path generation and control. The deployment of electrostatic potential for path generation can also serve as a reactive planner for obstacle avoidance, hence suitable for local path planning in undiscovered surroundings.

![](Rehman2023Motion_figs/d20ee35ffd8be853c9b9a4770ffebdbaea49a768c19a99eaada443221df7ae00.jpg)  
Figure 3. Illustration of the resultant force that is generated on the AGV [3].

## 2.1 Shortcomings of unmodified Traditional APFs in AGV motion planning

The use of artificial potential fields for local path planning has received much attention because of its simplicity and low computation cost for obstacle avoidance in real time. However, as this technique was applied in complex environments with dense obstacles and in real time experiments, it covered some shortcomings.

One of the drawbacks of the APF method in motion planning is the problem of local minima. This is due to the robot detecting its current location as the goal point because the attractive potential and repulsive potential have become equal. The AGV is then trapped before reaching the goal location, which is the global minima. The problem of local minima is inevitable because the robot has only local information of its current surroundings, and the issue can only be detected if the robot has information of the whole environment. The planner also has navigation issues and falls into traps for narrow passages in environments.

Autonomous ground vehicles are non-holonomic, however, the APF assumes the robot to be point mass. It means that the APF gives the resulting forces which may be in any direction, rejecting the possible constrained movement of the robot. Another inherent issue of the classical APF is the goal nonreachable with obstacles nearby (GNRON) problem In some cases, Oscillations also occur in path generation, which are not acceptable to be neglected in real-time [10].

The solution to these drawbacks has been an active area of research for the past decades. Different researchers have proposed different improvements in the traditional APF method for motion planning and real-time obstacle avoidance. Our study gives a review of the different solutions to the shortcomings associated and gives a literature on improved and modified APF motion planning models.

## 3. Literature Review

There have been a variety of methods to improve the performance of traditional artificial potential field motion planning with real-time obstacle avoidance. Some of these methods include modification in the repulsive or attractive functions, and addition of some other potential fields such as road boundary repulsive fields, or escaping potential functions. Other methods involve the inclusion of a virtual obstacle or goal that provides the force required to escape the local minima and solution of the GNRON problem. A variety of methods also involve the use of APF combined with other planning algorithms. In this strategic review of the improved artificial potential field algorithms, 32 articles were reviewed. The aims of the review were to analyse the various methods employed to enhance the APF motion planner, as well as its integration with other techniques. The assessment also has considered environmental conditions (static or dynamic) and the specific scenarios of experimentation or simulation. A brief explanation of the articles reviewed is below

A solution for the local minima problem was presented using additional components and external forces fields in the repulsive potential field function of the APF motion planner [10, 11]. The modified APF was then able to overcome the local minima and proceed towards the global minima, which represented the goal location. In [12], the formulation of attractive and repulsive functions in APF were modified for planning. In [13, 14], the issue of the local minima was solved by an appropriate steering angle, and by setting a step function for jumping out of the local minima. In [15], for collision avoidance of AV, an improved APF was proposed with the modification of the road potential field, attractive and repulsive fields. In addition to these modifications, the influence of obstacles on the collision areas was redesigned and safety factors were introduced. In [16], a boundary repulsion potential field was introduced for limiting the range of vehicle motion. Moreover, optimization of the repulsive potential function, and distance factor between the target and the vehicle was also introduced for GNRON issues.

Duan et al. [17], suggested an improved APF which utilized a virtual escaping potential field function. This function served as a trigger and influencing factor for situations where the ego vehicle gets stuck and falls into the local minimal location. In [18], a potential function that used the distance between the robot and the goal point for solving the issues related to the local minimum was proposed. In [14], a safety distance and correction factor was introduced for solving the GNRON problem.

Also, Szczepanski et al. [19] proposed the use of augmented reality for detecting the local minimum during navigation. The proposed planner detects if there is a local minimum in the plan currently traversing through the LIDAR. In case there is a local minimum, the planner activates a trigger to generate a virtual wall and initiate a bypassing procedure. Haoyang Li [20], on the other hand used LIDAR to obtain the distance of the ego vehicle from the target location, which he used to identify whether the planner was stuck in a local minima. If the planner is stuck, his modified APF initiates the correction procedure for the robot to separate itself from the equilibrium state.

In [21], improved APF method was proposed in response to the shortcomings faced in traditional APF methods, where different terms were added, which included a distance correction factor, repulsive fields of the dynamic road environments, the velocity, and the accelerations of the vehicle. The invasive weed algorithm was also then integrated to further improve APF motion planning and obstacle avoidance.

Zhang et al. [22] proposed an APF planner, where the repulsive function was modified and he also introduced the selection of a new virtual goal point in case the planning gets stuck. In [23], Szczepanski et al. proposed to place an additional virtual obstacle called top quark in critical areas of the environment, which provided a supplementary repulsive force at critical areas of the environment for energy-efficient APF motion planning. In addition, while considering the stagnation-free path of the planner, a temporary goal point was also selected. This approach was very useful in allowing the planner to reduce the travel length, and the traversing time, increasing the smoothness of the trajectory, and evasion of the local minima. H. Wang et al. [24] suggested a modified APF approach for local minimum problem in patrol swarms. He proposed the adjustment of weights of the attractive and repulsive forces to ensure the local minimum trap evasion.

Similarly, Songtao Xie et al. [25] proposed modified APF methods for distributed motion planning, the velocity difference potential field (VDPF) and acceleration difference potential field (ADPF). The authors used multiple field functions for the algorithm which include the attractive quadratic potential field between the ego vehicle and the virtual goal, the repulsive potential field from the humanoperated vehicles, the repulsive potential field from the automated vehicles, and finally the repulsive potential field generated from to road boundaries.

In [13], a road boundary potential field function was added to a traditional APF for improved intelligent vehicle motion planning with obstacle avoidance. Furthermore, in this topic of research, Lazarowska [26] proposed a discrete APF planning method, where the path planning of a differentially driven mobile robot was generated by taking into account different parameters which include the dynamic obstacles, path length, and run time of the problem.

Hongcai Li et al. [27] proposed a DynEFWA (dynamic enhanced firework algorithm) APF approach for motion planning. He introduced the modification of the repulsive and attractive functions on the basis of the shapes of obstacle and the driving characteristics constraints of the vehicle, such as the brake distances and lateral distances of the external vehicles. The authors proposed to use fireworks algorithm for further cost optimization of the DynEFWA-APF path planned.

In addition to the APF algorithm, the A-star algorithm is a graph traversal and path search algorithm that is widely due to shortest optimal path generation and performance efficiency. The A-star algorithm uses heuristics functions guide its search and find the path between multiple nodes on a graph with the smallest cost. Although the A-star algorithm obtains a relatively short path, it is unable to handle dynamic characteristics of environment, the artificial potential field method however can handle dynamic obstacles but the generated path is much longer than the A-star algorithm. Hence in [28, 29], a fusion of Astar algorithm with APF was proposed for optimized motion planning. Similarly, Guodong Du et al. [30] introduced a hierarchal approach to obtain optimal motion planning. He proposed the incorporation of APF with the global reference path that was generated using modified A-star and weighted regression for optimal sequences of motion planning.

In addition to the heuristic nature of the A-star algorithm, bacteria evolutionary algorithm (BEA) is also a nature inspired approach, based on the evolutionary process of bacterial gene recombination. In [31], utilizing the advantages and trimming down disadvantages in traditional APFs, bacterial evolutionary algorithm was proposed for combination for flexible path planning.

Probabilistic roadmap (PRM), which is a graph search-based algorithms is useful for finding best possible paths in grid maps. PRM objects and generates nodes in the free and occupied spaces of the environment and creates a connection between them. While, cost functions are also designed that help in identifying the best possible path for obstacle avoidance. In [32], APF was used for improving the locations of the PRM nodes, while the A-star algorithms was used for the finding the shortest plan.

Similar to the bacterial evolutionary algorithm, chaotic optimization algorithm is also an optimization algorithm, which uses chaotic maps, influenced by the properties of ergodicity and randomness, to enhance search optimization and performance. In [33], a combination of chaotic optimization algorithm with the APF for optimal planning was proposed for motion planning. This approach also introduced adaptation of potential function as objective function and proposed use of robot direction of movement as the control variable.

In [34], an adaptive approach to artificial potential field combined with ant colony optimization for motion planning and optimal obstacle evasion was considered based on the relative position and velocity of the robot to the obstacles.

Genetic algorithm is also a heuristic algorithm, which is based on the Darwinians theory of natural evolution. This algorithm was proposed by Feng Liu et al. [35] for optimisation of the gravity and repulsive functions in the APF algorithm. The optimization algorithm used cost functions to find the lowest possible potential energy location, which is at the goal location, and for determination of the step size and movement of direction for the robot. He also used virtual target points for escaping local minima.

Particle swarm optimization algorithm, which is inspired by the collective behaviour of living organisms, such as birds or fishes, was introduced for obtaining optimum values of APF factors in [36]. This approach iteratively enhanced the APF until the shortest path was obtained, which was then smoothened using the spline equation.

Rapidly exploring random trees is sampling based motion planning approach that searches through non-convex dimensional spaces by randomly building a space-filling tree. In [37], a hybrid motion planning algorithm was proposed utilizing a combination of informed rapidly exploring random trees-star (informed-RRT\*) with APF.

Chen Zheyi and Xu Bing [38] suggested using fuzzy control method for improving the adaptability of APF path planning. Additionally, by adding an angle repulsive function to increase the repulsion as the distance between the target point and AGV increases and in other cases a dragging force effect as the distance decreases, for counteracting strong gravitational forces. In [39], the fuzzy algorithm was proposed as an alternative planner for a vehicle, when in local minimum location in the APF path plan. The planner used fuzzy algorithm when in local minimum, and switched back to the APF when the robot moved away from that location.

Simulated annealing is a probabilistic method for path planning, which was proposed in combination with APF for solving problem of local minima and oscillations in the motion plan [40]. Additionally, an escape module was developed for local minimum with a modified resultant force for optimal global planning solution.

In [41], an innovative approach to APF motion planning was proposed. The proposed APF method utilized machine learning for training a model according to different driver characteristics. This model was then used for designing different repulsive field functions according to their respective driver characteristics and road environments. The resulting planner demonstrated adaptability to different surrounding vehicle environments and showed behaviour akin to that of a human-like driver.

## 4. Discussion of the literature

A strategy review of methods used for solving the problems associated with APF motion planners was presented. In this strategic review of the improved artificial potential field algorithms, 32 articles were reviewed. It was observed that although a number of articles [10, 11, 16, 22-25] have proposed modifications in the repulsive and attractive functions, added additional boundary or repulsive functions, used virtual obstacle and goal points, these approaches are not applicable in dynamic or realworld experiments. It was also observed that the majority of the articles have based their research on simulated scenarios, without real-world implementations [10, 11, 17, 18, 20, 22, 25, 41]. A number of authors focused on solving the problems related to local minima and GNRON [10, 18], where they have assumed static obstacles. However, these issues can also arise when the AGV traverses in realtime with dynamic obstacles. Although the APF has solved a variety of issues, Triharminto et al. [10] discussed that oscillations were still occurring in the path plan. Due to this reason, [27, 29, 31, 36] proposed APF combined with other planning algorithms and obtained good results [42].

## 5. Conclusion

Autonomous systems are an increasing area of research and hold significant promise. An autonomous ground vehicle system is a unification of different architectural designs, one of which is motion planning. This paper presents a strategic review of the modification and improvements involved in autonomous motion planning using artificial potential fields. Different approaches were reviewed for solving the motion planning issues, which involve the use of additional repulsive functions, correction factors, virtual obstacle and goal points, and combination with other algorithms. Several articles were found that had designed modified APF integrated with optimal control designs, where the vehicles were modelled according to the kinematic and dynamic constraints of the vehicle for obstacle avoidance. However, they were neglected in this research as those articles were more in correlation with optimal control. Hence, this can be proposed as future work.

Appendix A

<table><tr><td>Sr. No.</td><td>Title</td><td>Modification to APF</td><td>Environment (static or dynamic)</td><td>Evaluation (simulation or Realtime)</td></tr><tr><td>1</td><td>A novel of repulsive function on artificial potential field for robot path planning</td><td>Modified the repulsive force</td><td>Static</td><td>Simulation</td></tr><tr><td>2</td><td>Active obstacle avoidance method of autonomous vehicle based on improved artificial potential field</td><td>Added a virtual escaping force</td><td>Dynamic</td><td>Simulation</td></tr><tr><td>3</td><td>Distributed motion planning for safe autonomous vehicle overtaking via artificial potential field</td><td>Modified the resultant force</td><td>Dynamic</td><td>Simulation</td></tr><tr><td>4</td><td>Autonomous vehicle path planning based on driver characteristics identification and improved artificial potential field</td><td>Modified the repulsive field function to a ML trained driver characteristics model</td><td>Dynamic</td><td>Simulation</td></tr><tr><td>5</td><td>Efficient local path planning algorithm using artificial potential field supported by augmented reality</td><td>Used lidar data to detect local minima and modified the APF to bypass it.</td><td>Static</td><td>Simulation and real time</td></tr><tr><td>6</td><td>Energy efficient local path planning algorithm based on predictive artificial potential field</td><td>Added virtual temporary obstacles and goal points at critical areas</td><td>Static</td><td>Real time</td></tr><tr><td>7</td><td>Robotic path planning strategy based on improved artificial potential field</td><td>Used lidar to sense the distance b/w the vehicle and the target, which helped in identifying whether the robot is trapped or not and perform evasion</td><td>Static</td><td>Simulation</td></tr><tr><td>8</td><td>Trajectory generation and tracking control of an autonomous vehicle based on artificial potential field and optimized backstepping controller</td><td>Modified the repulsive force</td><td>Static</td><td>Simulation</td></tr><tr><td>9</td><td>Path planning based on improved artificial potential field method</td><td>Modified the repulsive force and added a virtual goal in case of a local minima trap</td><td>Static</td><td>Simulation</td></tr><tr><td>10</td><td>A new method for robot path planning based artificial potential field</td><td>Used potential field filling for GNRON problem and regression search for optimization of path</td><td>Static</td><td>Simulation</td></tr><tr><td>11</td><td>Research on active obstacle avoidance of intelligent vehicles based on improved artificial potential field method</td><td>Modified the repulsive force, and added a step function for jumping out of the local minima trap</td><td>Static and dynamic</td><td>Simulations and real time</td></tr><tr><td>12</td><td>Hybrid ant colony and immune network algorithm based on improved APF for optimal motion planning</td><td>Combined the use of APF with ant colony network algorithm</td><td>Static and dynamic</td><td>Simulations and real time</td></tr><tr><td>13</td><td>APF-IRRT*: an improved informed rapidly-exploring random trees-star algorithm by introducing artificial potential field method for mobile robot path planning</td><td>Combined the use of APF with improved rapidly exploring random trees-star algorithm</td><td>Static and dynamic</td><td>Simulations and real time</td></tr><tr><td>14</td><td>Unmanned vehicle route planning based on improved artificial potential field method</td><td>Added steering angle for solving local minima problem. Also added a safety distance and a correction factor for GNRON problem</td><td>Static</td><td>Simulation</td></tr><tr><td>15</td><td>Path planning using artificial potential field method and a-star fusion algorithm</td><td>Fusion of A-star and APF algorithms</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>16</td><td>Discrete artificial potential field approach to mobile robot path planning</td><td>Customized APF approach to a 2D discrete configuration space. Additionally, used Path Optimization algorithm to improve smoothness and length of path</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>17</td><td>An optimization-based path planning approach for autonomous vehicles using the DynEFWA-artificial potential field</td><td>Constraints of vehicle dynamics, driver characteristics and shapes of obstacles were taken into consideration. Also, used fireworks algorithm for path cost optimization</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>18</td><td>Collision avoidance method of autonomous vehicle based on improved artificial potential field algorithm</td><td>Introduced safety distance and road potential field in the modified APF and redesigned the influence range of obstacles based on the collision areas and corresponding safety distance</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>19</td><td>Research on automatic driving trajectory planning and tracking control based on improvement of the artificial potential field method</td><td>Added distance correction factor, with the addition of dynamic road repulsive field, velocity repulsive field, and acceleration repulsive field. Used invasive weed algorithm for improved motion planning</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>20</td><td>Dynamic path planning of mobile robot based on artificial potential field</td><td>APF combined with simulated annealing algorithm to solve local minimum and oscillation problems, additionally an escape module with modified resultant force was also designed</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>21</td><td>Research on intelligent vehicle path planning based on improved artificial potential field method</td><td>Added distance correction factor. Also added the use of boundary repulsive potential field, and further optimized the repulsive potential field of obstacle's</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>22</td><td>AGV path planning based on improved artificial potential field method</td><td>Angle function was added to classical APF, while fuzzy control idea for used for further enhancing the stability of the motion plan</td><td>Static</td><td>Simulation</td></tr><tr><td>23</td><td>Path planning for mobile robots using bacterial potential field for avoiding static and dynamic obstacles</td><td>APF combined with bacterial evolutionary algorithm (BEA) for an enhanced flexible path planner</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>24</td><td>Real time robot path planning method based on improved artificial potential field method</td><td>Modification and addition of attractive and repulsive forces</td><td>Static</td><td>Simulations and real time</td></tr><tr><td>25</td><td>Intelligent vehicle path planning based on improved artificial potential field algorithm</td><td>Used distance correction factor and global minimum regulatory factor. Also, proposed use of fuzzy algorithm for planning in local minimum location</td><td>Static</td><td>Simulation</td></tr><tr><td>26</td><td>Improved potential field method path planning based on genetic algorithm</td><td>Used genetic algorithm (GA) to optimize the combined potential field function of gravity and repulsion in the APF</td><td>Static</td><td>Simulation</td></tr><tr><td>27</td><td>Hierarchical motion planning and tracking for autonomous vehicles using global heuristic-based potential field and reinforcement learning-based predictive control</td><td>Used modified A-star algorithm and locally weighted regression smoothing incorporated with APF to generate the real-time optimal motion sequences</td><td>Static and dynamic</td><td>Simulation and real time</td></tr><tr><td>28</td><td>Path planning for robot based on chaotic artificial potential field method</td><td>Proposed combination of improved APF with chaotic optimization algorithm</td><td>Static</td><td>Simulation</td></tr><tr><td>29</td><td>An improved artificial potential field escape method with weight adjustment</td><td>Suggested modified APF approach by increasing the influence of gravity while reducing the influence of repulsion</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>30</td><td>Development of modified path planning algorithm using artificial potential field (APF) based on PSO for factors optimization</td><td>Combined use particle swarm optimization (PSO) to find optimum of APF factor for shortest path. Also spline equation used for path smoothing</td><td>Static</td><td>Simulation</td></tr><tr><td>31</td><td>Research on path-planning algorithm integrating optimization a-star algorithm and artificial potential field method</td><td>Proposed a fusion-based path finding approach based on optimized A-star algorithm, the APF and the least squares method</td><td>Static and dynamic</td><td>Simulation</td></tr><tr><td>32</td><td>Development of A* algorithm for robot path planning based on modified probabilistic roadmap and artificial potential field</td><td>Combined use of APF with probabilistic roadmap (PRM) for enhancing the location of the nodes. While, A-star was used to find shortest path within the constructed map</td><td>Static</td><td>Simulation</td></tr></table>

## 6. Reference

[1] A. Tanveer and S. M. Ahmad, "Mathematical Modelling and Fluidic Thrust Vectoring Control of a Delta Wing UAV," Aerospace, vol. 10, no. 6, p. 563, 2023. [Online]. Available: https://www.mdpi.com/2226-4310/10/6/563.

[2] A. Tanveer and S. M. Ahmad, "Cross-Coupled Dynamics and MPA-Optimized Robust MIMO Control for a Compact Unmanned Underwater Vehicle," Journal of Marine Science and Engineering, vol. 11, no. 7, doi: 10.3390/jmse11071411.

[3] A. Loganathan and N. S. Ahmad, "A systematic review on recent advances in autonomous mobile robot navigation," Engineering Science and Technology, an International Journal, vol. 40, p. 101343, 2023/04/01/ 2023, doi: https://doi.org/10.1016/j.jestch.2023.101343.

[4] B. Paden, M. Čáp, S. Z. Yong, D. Yershov, and E. Frazzoli, "A Survey of Motion Planning and Control Techniques for Self-Driving Urban Vehicles," IEEE Transactions on Intelligent Vehicles, vol. 1, no. 1, pp. 33-55, 2016, doi: 10.1109/TIV.2016.2578706.

[5] C. Zhou, B. Huang, and P. Fränti, "A review of motion planning algorithms for intelligent robots," Journal of Intelligent Manufacturing, vol. 33, no. 2, pp. 387-424, 2022.

[6] J. R. Sánchez-Ibáñez, C. J. Pérez-del-Pulgar, and A. García-Cerezo, "Path Planning for Autonomous Mobile Robots: A Review," Sensors, vol. 21, no. 23, doi: 10.3390/s21237898.

[7] A. Short, Z. Pan, N. Larkin, and S. v. Duin, "Recent progress on sampling based dynamic motion planning algorithms," in 2016 IEEE International Conference on Advanced Intelligent Mechatronics (AIM), 12-15 July 2016 2016, pp. 1305-1311, doi: 10.1109/AIM.2016.7576950.

[8] P. Paliwal, "A Survey of A-Star Algorithm Family for Motion Planning of Autonomous Vehicles," in 2023 IEEE International Students' Conference on Electrical, Electronics and Computer Science (SCEECS), 18-19 Feb. 2023 2023, pp. 1-6, doi: 10.1109/SCEECS57921.2023.10063063.

[9] O. Khatib, "Real-Time Obstacle Avoidance for Manipulators and Mobile Robots," The International Journal of Robotics Research, vol. 5, no. 1, pp. 90-98, 1986/03/01 1986, doi: 10.1177/027836498600500106.

[10] H. Triharminto, O. Wahyunggoro, T. Adji, A. Cahyadi, and I. Ardiyanto, "A Novel of Repulsive Function on Artificial Potential Field for Robot Path Planning," International Journal of Electrical and Computer Engineering (IJECE), vol. 6, p. 3262, 12/01 2016, doi: 10.11591/ijece.v6i6.pp3262-3275.

[11] A. D. Sabiha, M. A. Kamel, E. Said, and W. M. Hussein, "Trajectory Generation and Tracking Control of an Autonomous Vehicle Based on Artificial Potential Field and optimized Backstepping Controller," in 2020 12th International Conference on Electrical Engineering (ICEENG), 7-9 July 2020 2020, pp. 423-428, doi: 10.1109/ICEENG45378.2020.9171708.

[12] P. Yan, Z. Yan, H. Zheng, and J. Guo, "Real Time Robot Path Planning Method Based on Improved Artificial Potential Field Method," in 2018 37th Chinese Control Conference (CCC), 25-27 July 2018 2018, pp. 4814-4820, doi: 10.23919/ChiCC.2018.8482571.

[13] J. Tian et al., "Research on Active Obstacle Avoidance of Intelligent Vehicles Based on Improved Artificial Potential Field Method," World Electric Vehicle Journal, vol. 13, no. 6, doi: 10.3390/wevj13060097.

[14] M. Zha, Z. Wang, J. Feng, and X. Cao, "Unmanned Vehicle Route Planning Based on Improved Artificial Potential Field Method," Journal of Physics: Conference Series, vol. 1453, no. 1, p. 012059, 2020/01/01 2020, doi: 10.1088/1742-6596/1453/1/012059.

[15] S. Feng, Y. Qian, and Y. Wang, "Collision avoidance method of autonomous vehicle based on improved artificial potential field algorithm," Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering, vol. 235, no. 14, pp. 3416-3430, 2021/12/01 2021, doi: 10.1177/09544070211014319.

[16] L. Zang, Z. Wang, Z. Zhang, Y. Li, and T. Shi, Research on Intelligent Vehicle Path Planning Based on Improved Artificial Potential Field Method. 2022.

[17] Y. Duan, C. Yang, J. Zhu, Y. Meng, and X. Liu, "Active obstacle avoidance method of autonomous vehicle based on improved artificial potential field," International Journal of Advanced Robotic Systems, vol. 19, no. 4, p. 17298806221115984, 2022/07/01 2022, doi: 10.1177/17298806221115984.

[18] X. Yang, W. Yang, H. Zhang, H. Chang, C. Y. Chen, and S. Zhang, "A new method for robot path planning based artificial potential field," in 2016 IEEE 11th Conference on Industrial Electronics and Applications (ICIEA), 5-7 June 2016 2016, pp. 1294-1299, doi: 10.1109/ICIEA.2016.7603784.

[19] R. Szczepanski, A. Bereit, and T. Tarczewski, "Efficient Local Path Planning Algorithm Using Artificial Potential Field Supported by Augmented Reality," Energies, vol. 14, no. 20, doi: 10.3390/en14206642.

[20] H. Li, "Robotic Path Planning Strategy Based on Improved Artificial Potential Field," in 2020 International Conference on Artificial Intelligence and Computer Engineering (ICAICE), 23-25 Oct. 2020 2020, pp. 67-71, doi: 10.1109/ICAICE51518.2020.00019.

[21] Y. Li, W. Yang, X. Zhang, X. Kang, and M. Li, "Research on Automatic Driving Trajectory Planning and Tracking Control Based on Improvement of the Artificial Potential Field Method," Sustainability, vol. 14, no. 19, doi: 10.3390/su141912131.

[22] H. Zhang, M. Li, and Z. Wu, "Path Planning based on Improved Artificial Potential Field Method," in 2021 33rd Chinese Control and Decision Conference (CCDC), 22-24 May 2021 2021, pp. 4922-4925, doi: 10.1109/CCDC52312.2021.9602174.

[23] R. Szczepanski, T. Tarczewski, and K. Erwinski, "Energy Efficient Local Path Planning Algorithm Based on Predictive Artificial Potential Field," IEEE Access, vol. 10, pp. 39729-39742, 2022, doi: 10.1109/ACCESS.2022.3166632.

[24] H. Wang, M. Gao, W. Gao, Y. Wang, and H. Zhou, "An Improved Artificial Potential Field Escape Method with Weight Adjustment," Journal of Physics: Conference Series, vol. 2095, no. 1, p. 012085, 2021/11/01 2021, doi: 10.1088/1742-6596/2095/1/012085.

[25] S. Xie, J. Hu, P. Bhowmick, Z. Ding, and F. Arvin, "Distributed Motion Planning for Safe Autonomous Vehicle Overtaking via Artificial Potential Field," IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 11, pp. 21531-21547, 2022, doi: 10.1109/TITS.2022.3189741.

[26] A. Lazarowska, "Discrete Artificial Potential Field Approach to Mobile Robot Path Planning," IFAC-PapersOnLine, vol. 52, no. 8,

pp. 277-282, 2019/01/01/ 2019, doi: https://doi.org/10.1016/j.ifacol.2019.08.083.

[27] H. Li, W. Liu, C. Yang, W. Wang, T. Qie, and C. Xiang, "An Optimization-Based Path Planning Approach for Autonomous Vehicles Using the DynEFWA-Artificial Potential Field," IEEE Transactions on Intelligent Vehicles, vol. 7, no. 2, pp. 263-272, 2022, doi: 10.1109/TIV.2021.3123341.

[28] C. Ju, Q. Luo, and X. Yan, "Path Planning Using Artificial Potential Field Method And A-star Fusion Algorithm," in 2020 Global Reliability and Prognostics and Health Management (PHM-Shanghai), 16-18 Oct. 2020 2020, pp. 1- 7, doi: 10.1109/PHM-Shanghai49105.2020.9280929.

[29] L. Liu, B. Wang, and H. Xu, "Research on Path-Planning Algorithm Integrating Optimization A-Star Algorithm and Artificial Potential Field Method," Electronics, vol. 11, no. 22, doi: 10.3390/electronics11223660.

[30] G. Du, Y. Zou, X. Zhang, Z. Li, and Q. Liu, "Hierarchical Motion Planning and Tracking for Autonomous Vehicles Using Global Heuristic Based Potential Field and Reinforcement Learning Based Predictive Control," IEEE Transactions on Intelligent Transportation Systems, vol. 24, no. 8, pp. 8304-8323, 2023, doi: 10.1109/TITS.2023.3266195.

[31] O. Montiel, U. Orozco-Rosas, and R. Sepúlveda, "Path planning for mobile robots using Bacterial Potential Field for avoiding static and dynamic obstacles," Expert Systems with Applications, vol. 42, no. 12, pp. 5177-5191, 2015/07/15/ 2015, doi: https://doi.org/10.1016/j.eswa.2015.02.033.

[32] F. Raheem and M. Abdulkareem, "DEVELOPMENT OF A\* ALGORITHM FOR ROBOT PATH PLANNING BASED ON MODIFIED PROBABILISTIC ROADMAP AND ARTIFICIAL POTENTIAL FIELD," Journal of Engineering Science and Technology, vol. Vol. 15, pp. 3034- 3054, 10/01 2020.

[33] C. Zhang, "Path Planning for Robot based on Chaotic Artificial Potential Field Method," IOP Conference Series: Materials Science and Engineering, vol. 317, no. 1, p. 012056, 2018/03/01 2018, doi: 10.1088/1757- 899X/317/1/012056.

[34] Y. Mingxin, W. Sun'an, W. Canyang, and L. Kunpeng, "Hybrid ant colony and immune network algorithm based on improved APF for

optimal motion planning," Robotica, vol. 28, no. 6, pp. 833-846, 2010, doi: 10.1017/S0263574709990567.

[35] F. Liu, H. He, Z. Li, Z. H. Guan, and H. O. Wang, "Improved potential field method path planning based on genetic algorithm," in 2020 39th Chinese Control Conference (CCC), 27-29 July 2020 2020, pp. 3725-3729, doi: 10.23919/CCC50068.2020.9189655.

[36] F. Raheem and M. Badr, "Development of Modified Path Planning Algorithm Using Artificial Potential Field (APF) Based on PSO for Factors Optimization," American Scientific Research Journal for Engineering, Technology, and Sciences, vol. 37, pp. 316-328, 11/01 2017.

[37] D. Wu, L. Wei, G. Wang, L. Tian, and G. Dai, "APF-IRRT\*: An Improved Informed Rapidly-Exploring Random Trees-Star Algorithm by Introducing Artificial Potential Field Method for Mobile Robot Path Planning," Applied Sciences, vol. 12, no. 21, doi: 10.3390/app122110905.

[38] C. Zheyi and X. Bing, "AGV Path Planning Based on Improved Artificial Potential Field Method," in 2021 IEEE International Conference on Power Electronics, Computer Applications (ICPECA), 22-24 Jan. 2021 2021, pp. 32-37, doi: 10.1109/ICPECA51329.2021.9362519.

[39] X. Gu, M. Han, W. Zhang, G. Xue, G. Zhang, and Y. Han, "Intelligent Vehicle Path Planning Based on Improved Artificial Potential Field Algorithm," in 2019 International Conference on High Performance Big Data and Intelligent Systems (HPBD&IS), 9-11 May 2019 2019, pp. 104-109, doi: 10.1109/HPBDIS.2019.8735451.

[40] N. He, Y. Su, G. j, X. Fan, Z. Liu, and B. Wang, "Dynamic path planning of mobile robot based on artificial potential field," in 2020 International Conference on Intelligent Computing and Human-Computer Interaction (ICHCI), 4-6 Dec. 2020 2020, pp. 259-264, doi: 10.1109/ICHCI51889.2020.00063.

[41] S. Wang, F. Lin, T. Wang, Y. Zhao, L. Zang, and Y. Deng, "Autonomous Vehicle Path Planning Based on Driver Characteristics Identification and Improved Artificial Potential Field," Actuators, vol. 11, no. 2, doi: 10.3390/act11020052.

[42] M. Akarsu and O. Cetin, "Effective Solutions for Common Problems of Artificial Potential Field Based Path Planning Algorithms for Mobile Robots," Beykent Üniversitesi Fen ve Mühendislik Bilimleri Dergisi, 12/24 2022.