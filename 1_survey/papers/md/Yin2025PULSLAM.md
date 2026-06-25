---
citation_key: Yin2025PULSLAM
arxiv_id: 2511.04180
arxiv_url: "https://arxiv.org/abs/2511.04180"
title: "PUL-SLAM: Path-Uncertainty Co-Optimization with Lightweight Stagnation Detection for Efficient Robotic Exploration"
authors_short: "Yizhen Yin et al."
year: 2025
direction_tag: A_path_smoothing
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:21:06Z
origin: ai+web
reviewed: false
---

Journal Name

Crossmark

ARTICLE TYPE

RECEIVED dd Month yyyy REVISED dd Month yyyy

# PUL-SLAM: Path-Uncertainty Co-Optimization with Lightweight Stagnation Detection for Eficient Robotic Exploration

Yizhen Yin<sup>1</sup>, Dapeng Feng<sup>1</sup>,Hongbo Chen<sup>1,∗</sup> and Yuhua Qi<sup>1</sup>

<sup>1</sup>School of Systems Science and Engineering, Sun Yat-sen University, Guangzhou510220, People’s Republic of China <sup>∗</sup>Author to whom any correspondence should be addressed.

E-mail: chenhongbo@mail.sysu.edu.cn

Keywords: Active SLAM, Deep Reinforcement Learning, Autonomous Exploration, Intelligent Robotics

## Abstract

Existing Active SLAM methodologies face issues such as slow exploration speed and suboptimal paths. To address these limitations, we propose a hybrid framework combining a Path-Uncertainty Co-Optimization Deep Reinforcement Learning framework and a Lightweight Stagnation Detection mechanism. The Path-Uncertainty Co-Optimization framework jointly optimizes path length and pose uncertainty through a dual-objective reward function, balancing exploration and exploitation. The Lightweight Stagnation Detection reduces redundant exploration through Lidar Static Anomaly Detection and Map Update Stagnation Detection, terminating episodes on low expansion rates. Experimental results show that compared with the frontier-based method and RRT method, our approach shortens exploration time by up to 65% and reduces path distance by up to 42%, significantly improving exploration eficiency in complex environments while maintaining reliable map completeness. Ablation studies confirm that the collaborative mechanism accelerates training convergence. Empirical validation on a physical robotic platform demonstrates the algorithm’s practical applicability and its successful transferability from simulation to real-world environments.

## 1 Introduction

Active Simultaneous Localization and Mapping (Active SLAM) requires robots to simultaneously perform three critical tasks in unknown environments: environmental mapping, self-localization, and exploration path planning, thereby enabling eficient environmental exploration [1]. This technology has proven indispensable in critical application scenarios such as disaster rescue [2], planetary exploration [3], underground mine exploration [4, 5], and infrastructure inspection [6], particularly in environments that are inaccessible or hazardous to humans, where fully autonomous robotic exploration systems can substantially improve task execution eficiency while minimizing personnel risks [7]. The fundamental challenge of Active SLAM lies in achieving a dynamic equilibrium between exploration (discovering new areas) and exploitation (revisiting known regions to reduce localization and mapping uncertainty): robots must rapidly discover new areas while simultaneously conducting suficient exploration of known regions to minimize uncertainties in positioning and mapping. Unlike traditional SLAM approaches that focus exclusively on mapping and localization accuracy, Active SLAM introduces significant additional complexity through path planning and exploration strategy decision-making, thereby transforming the problem into a highly complex multi-objective optimization challenge.

Active SLAM methodologies exhibit significant diversity in exploration strategies. Traditional frontier-based methods [8–11], random sampling techniques like RRT [12–14], and information-theoretic approaches [15–18] have long dominated exploration strategies in unknown environments. These methods feature intuitive implementation architectures and are relatively easy to deploy. However, they employ static decision-making strategies that cannot adapt to dynamic environmental factors such as environmental complexity and exploration progress, resulting in unstable performance in varied environments. Furthermore, they typically optimize only a single objective (frontier-based methods focus on coverage ratio, RRT emphasizes path

feasibility, and information-theoretic approaches prioritize uncertainty reduction), while neglecting the multi-objective trade-ofs involving exploration eficiency, energy consumption, and other factors. This limitation, combined with their lack of global perspective, often leads to redundant backtracking paths in cluttered spaces. Recent deep reinforcement learning (DRL) methods [19–29] have demonstrated considerable potential in autonomous exploration domains. These approaches enable agents to interact with the environment and continuously refine their exploration strategies based on reward feedback, thereby optimizing the decision-making process. However, the performance of these methods is highly dependent on the design of the reward function. A well-designed reward function can steer the agent toward an optimal policy. Conversely, an improper design may result in the agent learning suboptimal strategies that significantly diverge from eficient exploration paths.

Despite these diverse paradigms, current systems still struggle to achieve an optimal balance between exploration eficiency and mapping accuracy, often sufering from slow exploration speeds and suboptimal trajectories. Additionally, existing systems lack mechanisms to dynamically detect and correct ineficient exploration behaviors, causing robots to become trapped in local oscillations or redundant exploration patterns when encountering complex obstacles. To address these limitations, we propose an innovative dual-layer collaborative optimization framework that jointl models path optimization and uncertainty reduction, while introducing a lightweight stagnation detection mechanism to enhance the system’s adaptability in complex environments. The main contributions of this study include:

• Path-Uncertainty Co-Optimization DRL Framework: We propose a novel deep reinforcement learning framework that jointly optimizes travel distance and pose uncertainty through a dual-objective reward function, balancing exploration and exploitation.

• Lightweight Stagnation Detection: A Lightweight Stagnation Detection module (LSD) mitigates redundant exploration via real-time LiDAR analysis. Simultaneously, map-update detection terminates episodes on low expansion rates. This dual strategy reduces ineficiencies and suppresses learning-hindering behaviors.

• Extensive simulation and real-world experiments: Experimental results show that compared with the frontier-based method and RRT method, the time is shortened by up to 65%, and the path is shortened by up to 42%, which significantly improves the exploration eficiency.

## 2 RELATED WORK

## 2.1 Traditional Active SLAM

Traditional Active SLAM methodologies can be broadly categorized into frontier-based exploration, random sampling techniques, and information-theoretic approaches, each with distinct characteristics and limitations that inform our current research direction.

Frontier-based exploration, pioneered by Yamauchi [8], represents one of the most influential paradigms in robotic exploration. This approach identifies boundary regions between known and unknown areas (frontiers) and directs robots toward these locations to maximize information gain. Enhanced variants like Wavefront Frontier Detection (WFD) [9] improved computational eficiency but still sufer from significant drawbacks in complex environments: the algorithm tends to generate suboptimal paths with excessive backtracking, struggles with large-scale environments due to growing computational overhead, and lacks mechanisms for global trajectory optimization. Despite these limitations, frontier-based methods remain widely adopted in recent works [10, 11] due to their intuitive implementation and reliable coverage performance.

Random sampling-based methods, particularly Rapidly-exploring Random Trees (RRT) [12], ofer an alternative exploration strategy by constructing search trees through random sampling of the configuration space. While RRT variants excel at finding feasible paths in high-dimensional spaces and complex obstacle arrangements, they exhibit critical shortcomings for exploration tasks: the resulting trajectories are often tortuous and energy-ineficient, coverage completeness is compromised due to undersampling in narrow passages, and the stochastic nature of sampling leads to inconsistent exploration patterns. These limitations become particularly pronounced in cluttered indoor environments where systematic coverage is essential.

Information-theoretic approaches employ metrics like Shannon entropy [16] and mutual information [17] to quantify and reduce mapping uncertainty through probabilistic modeling. Though theoretically sound, these methods face practical challenges including prohibitive computational costs for real-time information gain calculation, sensitivity to sensor noise, and frequent sacrifice of path eficiency for uncertainty reduction.

These traditional approaches establish important foundations but reveal significant gaps in handling the multi-objective nature of exploration. Their limitations in path optimality, computational eficiency, and adaptive decision-making motivate our development of a hybrid framework that preserves the strengths of systematic exploration while addressing these fundamental challenges through modern learning techniques.

## 2.2 DRL-based Active SLAM

In the field of DRL-based robotic autonomous exploration, the design of reward functions and termination conditions constitutes the core decision-making mechanism of Active SLAM systems, directly influencing exploration eficiency and map quality. The following sections systematically review the research progress in these two critical aspects.

2.2.1 Exploration Strategy Reward Function DRL-based exploration method has demonstrated significant potential in robotic autonomous exploration tasks, with the design of eficient reward functions being a core challenge to balance exploration eficiency and system robustness. Existing reward mechanisms can be categorized into three primary types:

Map-Completeness-Based Reward Mechanisms These methods motivate robots to achieve comprehensive environmental traversal through coverage increment incentives. For instance, Zhao et al. [21] decomposed rewards into map completeness, exploration rewards, and exploitation rewards to holistically incentivize exploration behaviors. Chaplot et al. [28] directly designed reward functions based on increases in covered area. These methods ofer intuitive interpretability and ensure systematic environmental traversal. However, they often lead to suboptimal path planning in complex environments, particularly in obstacle-dense regions where robots may become trapped in ineficient repetitive exploration due to excessive focus on local coverage.

Environment-Uncertainty-Based Reward Mechanisms These methods leverage information entropy reduction or feature metrics of SLAM covariance matrices to drive active exploration. Chen et al. [23] proposed a reward function integrating map information gain, control rewards, exploration completion rewards, and collision penalties. Alcalde et al. [24] and A. Placed et al. [26] adopted the D-optimality criterion to quantify localization and mapping uncertainties, embedding this metric into reward design. These approaches possess solid theoretical foundations and efectively reduce map uncertainty while improving localization accuracy. However, sensor noise can degrade performance, and path eficiency is often sacrificed to reduce uncertainty, resulting in excessive detours during exploration.

Other Reward Mechanisms Beyond the two primary mechanisms, several innovative reward designs have been proposed. For instance, Cao et al. [22] designed a composite reward function incorporating frontier point counts, path length penalties, and task completion incentives. In a related approach, Botteghi et al. [25] introduced an intrinsic curiosity-driven mechanism to encourage exploratory behavior. Similarly, Zhu et al. [27] employed negative penalties proportional to path length to promote shorter, more eficient trajectories.

Notably, path length, as a critical metric of exploration eficiency, has been rarely systematically incorporated into reward function design in existing literature. While Cao et al. [22] and Zhu et al. [27] introduced path length penalty terms in their respective works, no prior studies have proposed jointly optimizing path length and pose uncertainty as a dual-objective framework. The path-uncertainty co-optimization framework proposed in this study integrates both metrics into a unified reward function, dynamically balancing the trade-of between exploration and exploitation. This approach efectively addresses the suboptimal path planning issues resulting from existing methods’ excessive focus on single objectives such as coverage area or map entropy, thereby providing a more comprehensive and efective decision-making mechanism for autonomous robotic exploration.

2.2.2 Task Termination Mechanism The design of exploration task termination conditions is critical for ensuring both the completeness and computational eficiency of the exploration process. Existing methods primarily employ three termination mechanisms:

Environment-Triggered Termination Mechanisms Collision detection represents a typical example of this category, where tasks are terminated when the robot-obstacle distance falls below a predefined threshold (e.g., 0.2 meters) [21, 23–26]. This approach efectively prevents robots from continuing operation in hazardous environments, ensuring system safety. However, this mechanism lacks dynamic awareness of exploration progress, making it dificult to adapt to environments of varying complexity.

Task-Driven Termination Mechanisms Exploration completion thresholds (e.g., coverage ratio ≥ 93%) have been validated and applied across multiple studies [21–23, 25–28]. This mechanism ensures exploration tasks reach predefined objectives, but the threshold settings lack adaptability, making them unsuitable for environments of diferent scales and complexities. In simple environments, termination may occur too early; in complex environments, the threshold may never be reached, potentially resulting in indefinite task duration. Furthermore, this mechanism lacks dynamic awareness of exploration progress, making it dificult to adapt to environments of varying complexity.

Resource-Constrained Termination Mechanisms Fixed step limits or time ceilings ensure computational eficiency, as implemented in [23, 24, 28]. These methods prevent indefinite exploration through predefined resource constraints but lack dynamic awareness of exploration progress. This can result in critical regions remaining unexplored before resource exhaustion or premature termination when resources are still available.

Although some termination conditions have been designed in the above-mentioned papers, no systematic approach has been developed to detect and correct abnormal exploration behaviors that lead to ineficient stagnation. The absence of such mechanisms can cause significant performance degradation, particularly in complex environments where robots may become trapped in local oscillations or ineficient wandering patterns. The lightweight stagnation detection mechanism proposed in this paper, through real-time LiDAR analysis and adaptive map-update monitoring, efectively identifies and corrects these problematic behaviors. This approach not only enhances the robustness of the exploration process but also provides a crucial missing component for comprehensive termination condition design in Active SLAM systems.

## 3 APPROACH

As illustrated in Fig. 1, the PUL-SLAM system features a dual-layer collaborative optimization architecture, integrating a high-level DRL-based decision-making framework with a low-level Lightweight Stagnation Detection mechanism. In the operational pipeline, the SLAM module first processes LiDAR inputs to generate a real-time occupancy grid map alongside robot pose estimation. Subsequently, the Lightweight Stagnation Detection module, which consists of LiDAR Static Anomaly Detection and Map Update Stagnation Detection, monitors for ineficient behaviors. The former identifies motion anomalies via consecutive frame similarity analysis, while the latter tracks map expansion rates. If any abnormal state is identified, the system promptly halts the current exploration episode and performs an environment reset to avoid reinforcing ineficient strategies. Simultaneously, the DRL framework leverages a path-uncertainty co-optimization strategy to dynamically trade of exploration eficiency with pose uncertainty, thereby producing optimal motion commands to drive the robot.

## 3.1 Path-Uncertainty Co-Optimization DRL Framework

3.1.1 Reward Function The reward function, as the core mechanism guiding agent learning in reinforcement learning, directly determines the performance of the algorithm. The proposed path-uncertainty co-optimization reward function aims to achieve a dynamic balance between exploration and exploitation through a dual-objective optimization mechanism, thereby avoiding the ineficiency problems caused by excessive focus on a single objective in traditional methods. Specifically, the reward function is formulated as:

$$
\mathcal {R} _ {t} = \left\{ \begin{array}{l l} 1 + \tanh \Big (\frac {\eta}{f (\Sigma)} \Big) + \mathcal {P} _ {t} & \text {if} \Delta c _ {t} > 0 \\ 0. 0 0 1 + \mathcal {P} _ {t} & \text {else if \neg done ,} \\ - 1 0 0 & \text {otherwise} \end{array} \right.\tag{1}
$$

![](Yin2025PULSLAM_figs/317a94cf8f65d8c46b4a4c06d36e28b40d0ea6f77944a5acd4d92c2f3ce0312e.jpg)  
Figure 1: The overall framework of the PUL-SLAM system.

where η is a task-dependent scale factor, $f \left( \Sigma \right)$ is the D-optimality criterion $[ 1 8 , 2 4 ] , \Delta c _ { t }$ represents the newly added map area at time $t ,$ and $\mathcal { P } _ { t }$ is the path penalty term, which is defined as follows:

$$
\mathcal {P} _ {t} = \left\{ \begin{array}{l l} - 0. 1 * d _ {t} & \text {if} \eta_ {t} <   0. 0 0 1 \text {and} d _ {t} > 0. 0 0 1 \\ 0 & \text {otherwise} \end{array} \right.,\tag{2}
$$

where the exploration eficiency $\eta _ { t }$ is defined as the ratio of the newly added map area $\Delta { c } _ { t }$ to the robot’s incremental distance $d _ { t } .$ , where $d _ { t }$ denotes the distance traversed by the robot from time t − 1 to t. A path penalty is imposed only when $\eta _ { t }$ falls below a predefined threshold.

3.1.2 Observation Space At time step t, we uniformly sample 360 laser measurements to obtain N ranging values, as illustrated in Fig. 2, yielding range values normalized to:

$$
\hat {\mathbf {s}} _ {t} = \left[ \hat {d} _ {t} ^ {(1)}, \hat {d} _ {t} ^ {(2)}, \dots , \hat {d} _ {t} ^ {(N)} \right] ^ {\intercal} \in [ 0, 1 ] ^ {N}.\tag{3}
$$

By reducing the number of sampling points N, computational complexity is efectively reduced while maintaining suficient environmental representational capacity, allowing the algorithm to run in real-time on resource-constrained mobile robot platforms.

The observation space $\mathbf { O } _ { t }$ for the reinforcement learning agent consists of two components: the normalized laser scan vector $\hat { \mathbf { s } } _ { t }$ and the current map coverage ratio $c _ { t } \colon$

$$
\mathbf {O} _ {t} = \left[ \hat {\mathbf {s}} _ {t}, c _ {t} \right].\tag{4}
$$

This design choice integrates local perception with global state awareness: the laser scan vector captures fine-grained geometric details of the immediate surroundings, furnishing the agent with real-time sensory input for decision-making, while the cumulative map coverage ratio serves as a global indicator of exploration progress, thereby enabling the agent to maintain a coherent understanding of its spatial context.

3.1.3 Action Space Based on the discrete action space strategy, the robot’s kinematic control parameters for three fundamental motion commands are defined as follows:

• Forward: Linear velocity is set at $v = 0 . 2 \mathrm { { m } / \mathrm { { s } } }$ with angular velocity $\omega = 0 \mathrm { r a d / s } _ { \mathrm { ; } }$ ensuring linear motion along the current heading direction.

• Turn left: Linear velocity $v = 0 . 2 \mathrm { { m } / \mathrm { { s } } }$ and angular velocity $\omega = 0 . 4 \mathrm { r a d / s } ,$ generating a smooth left-turning trajectory.

• Turn right: Linear velocity $v = 0 . 2 \mathrm { { m } / \mathrm { { s } } }$ and angular velocity $\omega = - 0 . 4 \mathrm { r a d / s }$ , producing a symmetric right-turning behavior.

3.1.4 Neural Networks We adopt the Proximal Policy Optimization (PPO) [30] algorithm for policy learning. The observation space is structured as a dictionary comprising N-dimensional normalized LiDAR readings and a 1-dimensional map coverage metric, resulting in a (N + 1)-dimensional joint input vector. This concatenated observation is processed by a shared backbone network consisting of two fully connected layers, each with 64 neurons and Tanh activation functions. The shared representation is then fed into two separate heads: a policy head that outputs logits over three discrete actions (forward, turn left, turn right), and a value head tha estimates the scalar state-value function. All network parameters are jointly optimized in an end-to-end manner via gradient-based updates.

## 3.2 Lightweight Stagnation Detection Module

3.2.1 Lidar Static Anomaly Detection Robotic exploration can exhibit intentional pausing (e.g., stationary behavior to maximize reward in RL) or motion failure (e.g., collisions or wheel slippage). Undetected motion failures degrade learning eficiency by slowing convergence and reinforcing suboptimal policies. To address this, we propose Lidar Static Anomaly Detection: a lightweight method that identifies motion failures via cosine similarity between consecutive LiDAR scans. Unlike odometry/IMU-based approaches, this method uses raw environmental perception data, maintaining reliability during motor idling or wheel slippage. By operating on normalized scan vectors, it inherently rejects localized environmental changes. Lidar Static Anomaly Detection achieves real-time stagnation detection, with negligible impact on exploration performance.

The similarity metric between two consecutive frames of processed LiDAR data at timestamps t and t − 1 is calculated as follows:

$$
\cos (t) = \frac {\left\langle \hat {\mathbf {s}} _ {t} , \hat {\mathbf {s}} _ {t - 1} \right\rangle}{\left\| \hat {\mathbf {s}} _ {t} \right\| \cdot \left\| \hat {\mathbf {s}} _ {t - 1} \right\|},\tag{5}
$$

where $\langle \cdot , \cdot \rangle$ denotes the vector inner product operation, and $\lVert \cdot \rVert$ represents the Euclidean norm. Consequently, the above expression expands to:

$$
\cos (t) = \frac {\sum_ {i = 1} ^ {N} \hat {d} _ {t} ^ {(i)} \hat {d} _ {t - 1} ^ {(i)}}{\sqrt {\sum_ {i = 1} ^ {N} (\hat {d} _ {t} ^ {(i)}) ^ {2}} \sqrt {\sum_ {i = 1} ^ {N} (\hat {d} _ {t - 1} ^ {(i)}) ^ {2}}}.\tag{6}
$$

A static indicator function is formally defined as:

$$
\mathbb {I} (t) = \left\{ \begin{array}{l l} 1 & \text {if} \cos (t) > \alpha \\ 0 & \text {otherwise} \end{array} \right.,\tag{7}
$$

where $\alpha \in ( 0 , 1 )$ is the similarity threshold. Consequently, the static state counter C updates according to the following rule:

$$
\mathcal {C} \left(t\right) = \left\{ \begin{array}{l l} \mathcal {C} \left(t - 1\right) + 1 & \text { if } \mathbb {I} \left(t\right) = 1 \\ 0 & \text { otherwise } \end{array} \right..\tag{8}
$$

The static status flag static F is a Boolean signal derived from the state counter, formalized as:

$$
\mathcal {F} (t) = \left\{ \begin{array}{l l} 1 & \text { if } \mathcal {C} (t) \geq \Omega \\ 0 & \text { otherwise } \end{array} \right.,\tag{9}
$$

where $\Omega \in \mathbb { Z } ^ { + }$ is the continuity threshold.

3.2.2 Map Update Stagnation Detection In autonomous exploration tasks, robots may fall into inefective exploration states due to various reasons, including but not limited to wheel slippage, sensor malfunctions, or lack of distinctive environmental features. These stagnation states not only significantly reduce exploration eficiency but may also lead to reward hacking, where the algorithm learns to maximize cumulative rewards by remaining stationary for extended periods rather than conducting genuine exploration. To address this issue, we propose an innovative Map Update Stagnation Detection mechanism that identifies and terminates inefective exploration behaviors through real-time monitoring of map expansion rate while ensuring legitimate low-speed exploration in sparse environments remains undisturbed.

![](Yin2025PULSLAM_figs/917c80be4da015abf2574de7fc1463ea94850cdfb7a4ba2b1ab0d6e7afe277f0.jpg)  
Figure 2: For the sampling of LiDAR data, the data volume changes from 360 to $N .$

The core concept of map update stagnation detection is to quantify the increment of newly explored area per unit time as an objective metric of exploration eficiency. Let $\Delta t$ denote the corresponding time interval. The map expansion rate can then be defined as:

$$
\dot {c} _ {t} = \Delta c _ {t} / \Delta t,\tag{10}
$$

This metric directly reflects the robot’s exploration eficiency: when the robot is in an efective exploration state, $\dot { c } _ { t }$ should remain within a certain positive range; when the robot enters a stagnation state, ${ \dot { c } } _ { t }$ will approach zero.

However, simply setting a fixed threshold cannot distinguish between genuine motion failures and legitimate low-speed exploration in sparse environments. To address this limitation, we designed a dynamic detection mechanism with time-cumulative efects. Let ϵ represent the environment-adaptive minimum efective exploration rate threshold, and T denote the continuous stagnation detection time window. The stagnation state can then be formally defined as:

$$
S (t) = \left\{ \begin{array}{l l} 1 & \text {if (\forall\tau\in[t - T,t], \hat {c} _{\tau} <  \epsilon)\wedge (\| \mathbf {v} \| > 0)} \\ 0 & \text {otherwise} \end{array} \right.,\tag{11}
$$

where $\| \mathbf { v } \|$ denotes the Euclidean norm of the velocity vector, representing the robot’s actual movement magnitude. When $S ( t ) = 1$ , the system determines that the robot has entered a stagnation state and triggers appropriate corrective measures. Notably, we specifically included the condition that velocity commands are active to ensure that stagnation detection only occurs when the robot is actively attempting to move, preventing legitimate boundary point pauses from being misclassified as stagnation.

For the design of threshold ϵ, we propose an environment-characteristic-based adaptive calculation method: 4

$$
\epsilon = \beta \cdot \frac {A _ {\mathrm{env}}}{T _ {\mathrm{max}}},\tag{12}
$$

where $A _ { \mathrm { e n v } }$ represents the estimated environment area, $T _ { \mathrm { m a x } }$ denotes the typical exploration time for the environment, and $\beta$ is an empirical coeficient. This design ensures the threshold can adap to environments of varying scales and complexities: in expansive environments, the threshold is higher to prevent premature termination of legitimate exploration; in narrow environments, the threshold is lower, enabling the system to more sensitively detect motion failures.

## 4 EXPERIMENTS AND RESULTS

## 4.1 Experimental Settings

To validate our algorithm, we established a ROS [31]-based simulation platform on an Ubuntu 20.04 system. This platform utilizes the Gazebo simulator to replicate realistic physical scenarios. Experiments were conducted using the TurtleBot3-Burger robot, equipped with a 360-degree LiDAR (maximum ranging distance of 3.5 meters) and wheel odometry for motion tracking. As shown in Fig. 3, the training scenario is a rectangular room with dimensions of 15 meters by 3 meters, filled with cylindrical obstacles. The density of these obstacles increases gradually from left to right, creating a gradient of complexity within the environment. The robot model initiates its learning and exploration process from the left side of the room. In the testing phase, three additional testing scenarios were introduced. These testing scenarios cover a range of areas from 56 to 128 square meters, representing environments of varying scales and complexities. Among them,

![](Yin2025PULSLAM_figs/1173973f40f6370efb62500b5dfcce79bee9e07f58899672505fa7597920845e.jpg)  
Figure 3: Env-1 for training.

Env-2 and Env-3 are standard scenarios commonly used for validating Active SLAM algorithms, and some studies [24, 26] have already conducted experiments in these environments. Env-4 is a complex suite designed by us, containing multiple obstacles with a more intricate layout. It is intended to further verify the robot’s adaptability and robustness in unknown and complex environments. By conducting tests in these diverse scenarios, we can comprehensively evaluate the performance of the proposed decision-making algorithm under diferent environmental conditions. The main parameters used in the experiment are shown in Table 1.

Table 1: Training and simulation main hyperparameters.

<table><tr><td>Hyperparameters</td><td>value</td></tr><tr><td>Batch size</td><td>64</td></tr><tr><td>Max episode steps</td><td>5000</td></tr><tr><td>Training iteration</td><td>350000</td></tr><tr><td>Discount factor γ</td><td>0.99</td></tr><tr><td>Learning rate</td><td>0.0003</td></tr><tr><td>Scale factor η</td><td>1</td></tr><tr><td>Number of LiDAR samples N</td><td>24</td></tr><tr><td>Similarity threshold α</td><td>0.98</td></tr><tr><td>Continuity threshold Ω</td><td>10</td></tr><tr><td>Time interval T</td><td>20</td></tr><tr><td>Stagnation threshold factor β</td><td>0.05</td></tr></table>

## 4.2 Testing Evaluation

To comprehensively evaluate the performance of the proposed algorithm, this study designed a systematic comparative experimental framework. In three simulation environments (Env-2, Env-3, and Env-4), the proposed algorithm was compared against Frontier-based [8], RRT-based [12] and DA-SLAM (DRL-based) [24]. Three core metrics were selected: exploration time (from algorithm initiation to automatic termination), robot traversal distance, and map coverage ratio at algorithm termination. Ten independent trials were conducted per scenario to mitigate stochastic efects, with arithmetic means adopted as baseline performance measures. Experimental results are

Table 2: Evaluation results in Env-2, Env-3, Env-4.

<table><tr><td>Env</td><td>Scenario</td><td>Method</td><td>Time(s)</td><td>Path Length(m)</td><td>Map Completeness (%)</td></tr><tr><td rowspan="4">Env-2</td><td rowspan="4"><img src="images/404c0c58d65f210f1dc322e8853faf5464fb4ce2d7e36c0a928f482b6953c1f4.jpg"/></td><td>Frontier</td><td>322.14</td><td>50.19</td><td>99.30</td></tr><tr><td>RRT</td><td>553.68</td><td>58.40</td><td>99.24</td></tr><tr><td>DA-SLAM</td><td>288.84</td><td>51.88</td><td>100</td></tr><tr><td>Ours</td><td>235.23</td><td>41.84</td><td>98.56</td></tr><tr><td rowspan="4">Env-3</td><td rowspan="4"><img src="images/fb9e523f82c2868507533be5173540301483ebfc68b7525317dbfd773f024e04.jpg"/></td><td>Frontier</td><td>334.98</td><td>34.10</td><td>99.68</td></tr><tr><td>RRT</td><td>268.89</td><td>37.29</td><td>98.45</td></tr><tr><td>DA-SLAM</td><td>199.59</td><td>36.12</td><td>89.23</td></tr><tr><td>Ours</td><td>167.07</td><td>29.26</td><td>94.13</td></tr><tr><td rowspan="4">Env-4</td><td rowspan="4"><img src="images/8532d0f3d30a712ae5a1b082b24900bc14475c93e441b5468ab2752ace3b61ef.jpg"/></td><td>Frontier</td><td>778.67</td><td>60.32</td><td>99.55</td></tr><tr><td>RRT</td><td>698.30</td><td>90.15</td><td>99.85</td></tr><tr><td>DA-SLAM</td><td>383.13</td><td>69.32</td><td>98.46</td></tr><tr><td>Ours</td><td>272.06</td><td>52.26</td><td>99.93</td></tr></table>

![](Yin2025PULSLAM_figs/0238cf02fe87faf9fef8a005678567b50c337cd4abb6b38ead14619d23714315.jpg)  
(a) Frontier

![](Yin2025PULSLAM_figs/3110923fbc14f443f6f17cd19cfbf930d2722b8de1340352a424fd2138b5d6e7.jpg)  
(b) RRT

![](Yin2025PULSLAM_figs/24c7b78e6f2411705438e429c2bfe56f381a0eb80d8d4c4d8a326e73f8f129c1.jpg)  
(c) DA-SLAM

![](Yin2025PULSLAM_figs/f47f05d061542822ebbdf72c40f714dd063812db6e328a1fce1aa7d8c473bf0a.jpg)  
(d) Ours  
Figure 4: Trajectory and mapping results in Env-2.

![](Yin2025PULSLAM_figs/c5ca7935f9cd729fb3553509fe2957e16875d68c5cd2cfc6ce6d2ab5b1cd0c0d.jpg)  
(a) Frontier

![](Yin2025PULSLAM_figs/dcb99369ee4f19838f13eb40e47f0a1e7695e9d7ba00fe32802377d266888184.jpg)  
(b) RRT

![](Yin2025PULSLAM_figs/3919105a81e9c9c013daf3c2d1d32d67c4690b4c597b31e8ee368588dbe0d4cd.jpg)  
(c) DA-SLAM

![](Yin2025PULSLAM_figs/4c778ac94b0557e837e653a9461314fe5bf1b706b560bdc1fa2a002fdadb8490.jpg)  
(d) Ours  
Figure 5: Trajectory and mapping results in Env-3.

![](Yin2025PULSLAM_figs/34968bde70969e0e5f2524fb166494932fb2680472cdab5ee46ceeed7c034d64.jpg)  
(a) Frontier

![](Yin2025PULSLAM_figs/f36d629527d454b3b9ad577f615994d2b14ce241fa97e90532d17e856691055a.jpg)  
(b) RRT

![](Yin2025PULSLAM_figs/77c1ef623b4cb4f5df157c380a1fa32031e380ce4bb256cfba44660e58066faa.jpg)  
(c) DA-SLAM

![](Yin2025PULSLAM_figs/ae1d0b874e6123b940947ee25b1f98e3a31d579daa87bbe877d8bafc5520b6b5.jpg)  
(d) Ours  
Figure 6: Trajectory and mapping results in Env-4.

aggregated in Table 2, while Figs. 4 to 6 illustrates the exploration paths and mapping outcomes from representative trials (closest to mean performance), and Fig. 7 presents the exploration progress dynamics of each algorithm across diferent environments.

The results in Table 2 show that the proposed algorithm achieves substantial improvements in both exploration time and path length across all test environments. In the most challenging Env-4, the proposed method completes exploration 65%, 60%, and 29% faster than Frontier, RRT, and DA-SLAM, respectively, while achieving a 42% shorter path than RRT and a 25% reduction compared to DA-SLAM. Consistent gains are observed in Env-2 and Env-3, with 25–30% time savings and approximately 20% shorter paths. While map completeness is slightly lower than baselines in Env-2 and Env-3, this reflects the algorithm’s deliberate trade-of: by suppressing redundant revisits and prioritizing unexplored regions, it optimizes the balance between eficiency and coverage.

## 4.3 Ablation Experiment

We conducted systematic ablation studies to quantitatively evaluate the contribution of each component in our proposed framework. The experiment was designed with three distinct configurations to isolate the efects of our key innovations:

1. Baseline Method: Uncertainty-based DRL approach [24] (blue curves)

2. LSD-Enhanced Method: Baseline + Lightweight Stagnation Detection (green curve)

3. Full Method: Path-Uncertainty Co-Optimization Reward (PUR) + Lightweight Stagnation Detection (red curve)

Figure 8 presents the average episode rewards over 2000 training episodes. The baseline method demonstrates extremely poor convergence characteristics throughout the entire training process. Despite 2000 episodes of training, its reward curve continues to exhibit severe oscillations, failing to achieve a stable policy. This instability stems from the algorithm’s inability to recognize and correct ineficient exploration patterns, allowing the agent to repeatedly learn destructive policies that result in environmental collisions or exploration stagnation. In contrast, both LSD-enhanced variants exhibit significantly stabilized training curves. This stability is attributed to the dual detection mechanism of the LSD module: LiDAR Static Anomaly Detection promptly identifies physical motion failures (such as wheel slippage or collisions), while Map Update Stagnation Detection terminates episodes where exploration progress stagnates despite active movement commands. By terminating these episodes characterized by motion failures or map update stagnation, the mechanism prevents the reinforcement learning agent from incorporating these detrimental experiences into its policy updates. The Full Method not only demonstrates superior stability but also achieves accelerated convergence. The path penalty term (Eq. 2) actively

![](Yin2025PULSLAM_figs/8eabc91ff74b6c5f54bb19657117cc0ac5479301b6fa5a124751f7178879192d.jpg)

![](Yin2025PULSLAM_figs/84d6ec924560444fd36cdcaa562c63190ec88fcabffb4ec3bfa41a201133f956.jpg)  
(a) test Env-2

![](Yin2025PULSLAM_figs/005396a7b9b6220bad0d31ccda9acc027685aa3c6e3473562416ebe3d531c883.jpg)

![](Yin2025PULSLAM_figs/8ffd0554bf63a40577f9613543d9d1e42486199aebb6dea13eed1a2bc7b01d00.jpg)  
(b) test Env-3

![](Yin2025PULSLAM_figs/254e79900ef34fead211cde32e92ec3803bcaea54002501f1f081bff19e3e895.jpg)

![](Yin2025PULSLAM_figs/fa3209916dca5b65f08e3291f2adbb0e283368b8e35f67758ecdb72af2b5e122.jpg)  
(c) test Env-4  
Figure 7: Exploration Progress: Coverage vs. Time (Left) and Coverage vs. Path Length (Right).

![](Yin2025PULSLAM_figs/e9a0c235e1f04aa3587a82a6120e5a1463be6ad53a57b396cbd5090f2abea97c.jpg)  
Figure 8: The average episode rewards during training.

discourages ineficient exploration behaviors, while the D-optimality criterion ensures suficient uncertainty reduction for reliable mapping.

Fig. 9 presents a comprehensive analysis of our ablation study across three critical performance metrics. Regarding exploration time, both the LSD-enhanced and the Full methods significantly outperform the baseline. Notably, the LSD-enhanced method exhibits shorter exploration time than the Full method. This apparent discrepancy is explained by analyzing map completeness (Fig. 9b) and movement distance (Fig. 9c): The Full method achieves faster convergence, attaining higher map completeness within the same training episodes (the red curve in Fig. 9b reaches high coverage earlier). This thorough exploration behavior increases exploration time and movement distance (higher distance values for the red curve in Fig. 9c). In contrast, while the LSD-enhanced method optimizes stagnation issues, its lack of dynamic reward guidance limits exploration scope within the same episodes, resulting in shorter time but incomplete map coverage. The baseline method performs worst across all metrics, exhibiting substantial time waste and redundant movement, underscoring the necessity of action correction and reward optimization.

This analysis validates the synergistic relationship between our two proposed mechanisms: the LSD module provides essential execution-level stability by filtering out catastrophic failures, while the DRL framework optimizes decision-making eficiency through a balanced reward structure. Their integration creates a learning environment where policy updates are derived from consistently productive exploration experiences, thereby ensuring training stability and accelerating convergence speed.

## 4.4 Real-world Experiment

To validate the efectiveness and adaptability of the proposed method in real-world scenarios, this study further conducted physical platform experiments. The experimental environment was set up within our laboratory, covering an area of approximately 60 square meters, with numerous randomly placed obstacles including chairs, tables, storage cabinets, and cardboard boxes. This environmental layout simulates the common cluttered obstacle distribution found in practical applications, presenting significant challenges to the robustness and adaptability of exploration algorithms. The experimental platform was equipped with an Intel N100 processor (1.8 GHz clock speed, 4 cores and 4 threads) running Ubuntu 20.04 operating system, and integrated with a Hokuyo UST-10LX LiDAR (ranging distance of 0.1-3.5 meters). To ensure experimental safety, the robot’s maximum linear velocity was set to 0.15 m/s, slightly lower than that used in the simulation environment.

Fig. 10 shows the laboratory environment, clearly displaying the densely distributed obstacles and complex spatial structures. Fig. 11 illustrates the experimental platform. Fig. 12 presents the robot’s final exploration trajectory (green path) along with the constructed complete environmental map. The experimental results indicate that the robot completed the entire environment exploration within 122.32 seconds, with a final path length of 15.96 meters, while successfully avoiding collisions with various obstacles in the environment. This result shows high consistency with the performance observed in the simulation environment, validating the transferability of the proposed algorithm from simulation to real-world settings. Notably, the robot’s exploration path during the process exhibited a highly concentrated characteristic, significantly reducing unnecessary backtracking and detouring behaviors.

![](Yin2025PULSLAM_figs/940597db03a49d5f851677a7468d3ef6278dba9fe031ab9542a8fa4ed5508590.jpg)

(a) Time vs. Episodes  
![](Yin2025PULSLAM_figs/f0de1cd66002ad758dc5d6c5910c8876a5df418f42787824c3aaf47393f35f9b.jpg)

(b) Coverage vs. Episodes  
![](Yin2025PULSLAM_figs/b32f76aea0767379d92d8ba1a3b27dee9623f9174366363f545a5ac66fb027e9.jpg)  
(c) Distance vs. Episodes  
Figure 9: Efectiveness of LSD and PUR during training.

![](Yin2025PULSLAM_figs/cc6745cc7aacc0fc93e33f6d2ebb1d0611d3e0c922f7ee7f2715cbbc88ea8efa.jpg)  
Figure 10: Laboratory environment.

The real-world experimental results verify the reliability of the simulation experiments and demonstrate the practical value of our proposed method, laying the foundation for future deployment in real-world applications such as disaster rescue and underground mine exploration. In our subsequent research, we will focus on validating the algorithm’s performance in larger-scale and more dynamic real environments.

## 5 CONCLUSIONS

This paper proposes a Path-Uncertainty Co-Optimization DRL framework with Lightweight Stagnation Detection mechanism, which significantly enhances robotic exploration eficiency. Experimental results show that the proposed method substantially outperforms the frontier-based method, the RRT-based approach and DA-SLAM in terms of exploration eficiency, while maintaining reliable map completeness. Specifically, it reduces exploration time by up to 65% relative to the frontier-based method and shortens path length by up to 42% compared to RRT, consistently outperforming all baselines across diverse and complex scenarios. Ablation studies further confirm the complementary roles of the Path-Uncertainty Co-Optimization Reward and the Lightweight Stagnation Detection mechanism: PUR enhances the eficient allocation of exploration resources at the decision-making level, while LSD suppresses inefective behaviors at the execution level. Their synergistic integration significantly accelerates training convergence. Moreover, real-world experiments on a physical robotic platform validate the successful sim-to-real transferability of the proposed approach, demonstrating its practical applicability and deployment potential. Future work will focus on further optimizing coverage uniformity and enhancing system robustness in large-scale environments.

![](Yin2025PULSLAM_figs/2a484af47487ee811807a89974e9e85c35545dee5cfd41e2bf1919ebb336ec29.jpg)  
Figure 11: Experimental platform

![](Yin2025PULSLAM_figs/fb024c17616821219ff29c3f1dc1786cc929e88dd294fbbaa49f74ac21127432.jpg)  
Figure 12: The constructed map

## References

[1] J. A. Placed, J. Strader, H. Carrillo, N. Atanasov, V. Indelman, L. Carlone, and J. A. Castellanos, “A survey on active simultaneous localization and mapping: State of the art and new frontiers,” IEEE Transactions on Robotics, vol. 39, no. 3, pp. 1686–1705, 2023.

[2] F. Niroui, K. Zhang, Z. Kashino, and G. Nejat, “Deep reinforcement learning robot for search and rescue applications: Exploration in unknown cluttered environments,” IEEE Robotics and Automation Letters, vol. 4, no. 2, pp. 610–617, 2019.

[3] S. Nahavandi, R. Alizadehsani, D. Nahavandi, S. Mohamed, N. Mohajer, M. Rokonuzzaman, and I. Hossain, “A comprehensive review on autonomous navigation,” ACM Computing Surveys, vol. 57, no. 9, pp. 1–67, 2025.

[4] C. Wang, C. Yu, X. Xu, Y. Gao, X. Yang, W. Tang, S. Yu, Y. Chen, F. Gao, Z. Jian et al., “Multi-robot system for cooperative exploration in unknown environments: A survey,” arXiv preprint arXiv:2503.07278, 2025.

[5] E. Ackerman, “Robots conquer the underground: What darpa’s subterranean challenge means for the future of autonomous robots,” IEEE Spectrum, vol. 59, no. 5, pp. 30–37, 2022.

[6] B. Zhou, H. Xu, and S. Shen, “Racer: Rapid collaborative exploration with a decentralized multi-uav system,” IEEE Transactions on Robotics, vol. 39, no. 3, pp. 1816–1835, 2023.

[7] H. Azp´urua, M. Saboia, G. M. Freitas, L. Clark, A.-a. Agha-mohammadi, G. Pessin, M. F. Campos, and D. G. Macharet, “A survey on the autonomous exploration of confined subterranean spaces: Perspectives from real-word and industrial robotic deployments,” Robotics and Autonomous Systems, vol. 160, p. 104304, 2023.

[8] B. Yamauchi, “A frontier-based approach for autonomous exploration,” in Proceedings 1997 IEEE International Symposium on Computational Intelligence in Robotics and Automation CIRA’97.’Towards New Computational Principles for Robotics and Automation’. IEEE, 1997, pp. 146–151.

[9] M. Keidar and G. A. Kaminka, “Eficient frontier detection for robot exploration,” The International Journal of Robotics Research, vol. 33, no. 2, pp. 215–236, 2014.

[10] M. Wang, B. Xin, M. Jing, and Y. Qu, “An exploration-enhanced search algorithm for robot indoor source searching,” IEEE Transactions on Robotics, 2024.

[11] S. Saravanan, C. Chaufaut, C. Chanel, and D. Vivet, “Fit-slam–fisher information and traversability estimation-based active slam for exploration in 3d environments,” arXiv preprint arXiv:2401.09322, 2024.

[12] H. Umari and S. Mukhopadhyay, “Autonomous robotic exploration based on multiple rapidly-exploring randomized trees,” in 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2017, pp. 1396–1402.

[13] A. Faust, K. Oslund, O. Ramirez, A. Francis, L. Tapia, M. Fiser, and J. Davidson, “Prm-rl: Long-range robotic navigation tasks by combining reinforcement learning and sampling-based planning,” in 2018 IEEE international conference on robotics and automation (ICRA). IEEE, 2018, pp. 5113–5120.

[14] C.-Y. Wu and H.-Y. Lin, “Autonomous mobile robot exploration in unknown indoor environments based on rapidly-exploring random tree,” in 2019 IEEE International Conference on Industrial Technology (ICIT). IEEE, 2019, pp. 1345–1350.

[15] P. Whaite and F. P. Ferrie, “Autonomous exploration: Driven by uncertainty,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 19, no. 3, pp. 193–205, 1997.

[16] A. Asgharivaskasi and N. Atanasov, “Semantic octree mapping and shannon mutual information computation for robot exploration,” IEEE Transactions on Robotics, vol. 39, no. 3, pp. 1910–1928, 2023.

[17] C. Stachniss, G. Grisetti, and W. Burgard, “Information gain-based exploration using rao-blackwellized particle filters.” in Robotics: Science and systems, vol. 2, no. 1, 2005, pp. 65–72.

[18] H. Carrillo, I. Reid, and J. A. Castellanos, “On the comparison of uncertainty criteria for active slam,” in 2012 IEEE International Conference on Robotics and Automation. IEEE, 2012, pp. 2080–2087.

[19] J. Zhao, W. Zhao, B. Deng, Z. Wang, F. Zhang, W. Zheng, W. Cao, J. Nan, Y. Lian, and A. F. Burke, “Autonomous driving system: A comprehensive survey,” Expert Systems with Applications, vol. 242, p. 122836, 2024.

[20] Y. Zhou, J. Yang, Z. Guo, Y. Shen, K. Yu, and J. C.-W. Lin, “An indoor blind area-oriented autonomous robotic path planning approach using deep reinforcement learning,” Expert Systems with Applications, vol. 254, p. 124277, 2024.

[21] S. Zhao and S.-H. Hwang, “Exploration-and exploitation-driven deep deterministic policy gradient for active slam in unknown indoor environments,” Electronics, vol. 13, no. 5, p. 999, 2024.

[22] Y. Cao, T. Hou, Y. Wang, X. Yi, and G. Sartoretti, “Ariadne: A reinforcement learning approach using attention-based deep networks for exploration,” arXiv preprint arXiv:2301.11575, 2023.

[23] J. Chen, K. Wu, M. Hu, P. N. Suganthan, and A. Makur, “Lidar-based end-to-end active slam using deep reinforcement learning in large-scale environments,” IEEE Transactions on Vehicular Technology, 2024.

[24] M. Alcalde, M. Ferreira, P. Gonz´alez, F. Andrade, and G. Tejera, “Da-slam: Deep active slam based on deep reinforcement learning,” in 2022 Latin American Robotics Symposium (LARS), 2022 Brazilian Symposium on Robotics (SBR), and 2022 Workshop on Robotics in Education (WRE). IEEE, 2022, pp. 282–287.

[25] N. Botteghi, B. Sirmacek, M. Poel, C. Brune, and R. Schulte, “Curiosity-driven reinforcement learning agent for mapping unknown indoor environments,” ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, vol. 5, no. 1, pp. 129–136, 2021.

[26] J. A. Placed and J. A. Castellanos, “A deep reinforcement learning approach for active slam,” Applied Sciences, vol. 10, no. 23, p. 8386, 2020.

[27] D. Zhu, T. Li, D. Ho, C. Wang, and M. Q.-H. Meng, “Deep reinforcement learning supervised autonomous exploration in ofice environments,” in 2018 IEEE international conference on robotics and automation (ICRA). IEEE, 2018, pp. 7548–7555.

[28] D. S. Chaplot, D. Gandhi, S. Gupta, A. Gupta, and R. Salakhutdinov, “Learning to explore using active neural slam,” arXiv preprint arXiv:2004.05155, 2020.

[29] H. Zhao, Y. Guo, Y. Liu, and J. Jin, “Multirobot unknown environment exploration and obstacle avoidance based on a voronoi diagram and reinforcement learning,” Expert Systems with Applications, vol. 264, p. 125900, 2025.

[30] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” arXiv preprint arXiv:1707.06347, 2017.

[31] M. Quigley, K. Conley, B. Gerkey, J. Faust, T. Foote, J. Leibs, R. Wheeler, A. Y. Ng et al., “Ros: an open-source robot operating system,” in ICRA workshop on open source software, vol. 3, no. 3.2. Kobe, 2009, p. 5.