---
citation_key: Zhao2025Industrial
arxiv_id: 2504.02492
arxiv_url: "https://arxiv.org/abs/2504.02492"
title: "Industrial Internet Robot Collaboration System and Edge Computing Optimization"
authors_short: "Haopeng Zhao et al."
year: 2025
direction_tag: P_nonholonomic_constraints
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:19:50Z
origin: ai+web
reviewed: false
---

# Industrial Internet Robot Collaboration System and Edge Computing Optimization

Haopeng Zhao¹ᵃ\*†, Dajun Tao²ᵇ†, Tian Qi³ᶜ, Jingyuan Xu⁴ᵈ, Zijie Zhou⁵ᵉ, and Lipeng Liu⁶ᶠ ¹ Independent Researcher, Mountain View, CA, USA

² School of Engineering, Carnegie Mellon University, Pittsburgh, PA, USA

³ College of Arts and Sciences, University of San Francisco, San Francisco, CA, USA

⁴ School of Computer and Information Science, University of the Cumberlands, Williamsburg, KY, USA

⁵ College of Engineering, Northeastern University, Boston, MA, USA

⁶ College of Engineering, Peking University, Beijing, China ᵃ\* haopeng.zhao1894@gmail.com, ᵇ dajunt@alumni.cmu.edu, ᶜ tqi51212@gmail.com, ᵈ jxu65428@ucumberlands.edu, ᵉ zhou.zijie@northeastern.edu, ᶠ lipeng.liu@pku.edu.cn

†These authors contributed equally to this work and are co-first authors.

Abstract—In industrial-Internet environments, mobile robots must generate collision-free global routes under stochastic obstacle layouts and random perturbations in commanded linear and angular velocities. This paper models a differential-drive robot with nonholonomic constraints, then decomposes motion into obstacle avoidance, target turning, and target approaching behaviors to parameterize the control variables. Global path planning is formulated as a constrained optimization problem and converted into a weighted energy function that balances path length and collision penalties. A three-layer neural network represents the planning model, while simulated annealing searches for near-global minima and mitigates local traps. During execution, a fuzzy controller uses heading and lateral-offset errors to output wheel-speed differentials for rapid correction; edge-side computation is discussed to reduce robot–server traffic and latency. Matlab 2024 simulations report deviation within ±5 cm, convergence within 10 ms, and shorter paths than two baseline methods. The approach improves robustness of global navigation in practice.

Keywords—Deep learning, Mobile robot, Global path, Control method, Fuzzy control algorithm

## I. INTRODUCTION

Industrial Internet scenarios such as warehousing, inspection, and flexible manufacturing increasingly rely on mobile robots. With advances in artificial intelligence and high-speed communications [1], robots can integrate sensing, planning, and control more tightly, yet cluttered environments and disturbances in commanded linear and angular velocities still cause tracking deviations and collision risk.

Path planning is therefore a core topic in mobile robotics. Many approaches optimize objectives such as minimum distance or minimum energy consumption [2], but highprecision navigation in complex environments remains difficult when local minima and execution disturbances are present. A practical solution must respect nonholonomic motion constraints while maintaining collision avoidance and stable tracking.

Edge computing can improve responsiveness by moving computation closer to the robot, reducing robot-server traffic and latency and enabling timely sharing of environmental information among collaborative robots. This paper studies global path planning and global path control by combining an energy-based planner with an error-correcting controller. Specifically, we establish a robot model and decompose motion into obstacle avoidance, target turning, and target approaching behaviors; simulated annealing is used to search low-energy paths, and a fuzzy controller outputs wheel-speed differentials from heading and lateral-offset errors. Matlab 2024 simulations compare the proposed method with two baselines..

## II. DYNAMIC ANALYSIS OF MOBILE ROBOT

## A. Dynamic Model

Set the wheel radius of the mobile robot as r and the distance between the drive shafts as l. The pose matrix is defined in (1), where (x, y) gives the robot position and θ gives the heading direction.

$$
\mathbf {p} = \left[ \begin{array}{c} \mathrm{x}, \mathrm{y}, \theta \end{array} \right] ^ {\mathrm{T}}\tag{1}
$$

Based on the above pose, the dynamic equation of the mobile robot is established in (2) [3]. In (2), μ₁ and μ₂ are control inputs, c₁ and c₂ are inertia terms, $\Delta \mathrm { g } _ { \mathrm { x } } , \Delta \mathrm { g } _ { \mathrm { \ i } }$ and $\Delta \mathrm { g } \Theta$ are nonlinear functions, γ is the Lagrange multiplier, and n is the robot mass. The last line in (2) denotes the non-holonomic constraint. According to the above calculation results, the dynamic model is obtained and shown in Fig. 1.

$$
\left\{ \begin{array}{l} \ddot {\mathrm{x}} = \frac {\gamma}{\mathrm{n}} \sin \theta + c _ {1} \mu_ {1} \cos \theta + \Delta \mathrm{g} _ {\mathrm{x}} (\mathrm{p}, \dot {\mathrm{p}}) \\ \ddot {\mathrm{y}} = \frac {\gamma}{\mathrm{n}} \sin \theta + c _ {1} \mu_ {1} \cos \theta + \Delta \mathrm{g} _ {\gamma} (\mathrm{p}, \dot {\mathrm{p}}) \\ \ddot {\theta} = c _ {2} \mu_ {2} + \Delta \mathrm{g} _ {\theta} (\mathrm{p}, \dot {\mathrm{p}}) \\ \dot {\mathrm{x}} \sin \theta - \dot {\mathrm{y}} \sin \theta = 0 \end{array} \right.\tag{2}
$$

![](Zhao2025Industrial_figs/27d0230da368dc55a90eb752179d31cb48b285a3ec695edd4f0117950b456bc4.jpg)  
Fig. 1. Dynamics model of the mobile robot

Since the number of balance wheels does not affect the robot dynamics, the model is updated to the kinematic form in (3), where η denotes linear velocity and υ denotes angular velocity.

$$
\left\{ \begin{array}{l} \dot {\mathrm{x}} = \eta \cos \theta \\ \dot {\mathrm{y}} = \eta \sin \theta \\ \dot {\theta} = \mathrm{v} \end{array} \right.\tag{3}
$$

## B. Analysis of Robot Motion Behaviors

To improve controllability, robot motion is decomposed into three behaviors parameterized by linear velocity v and angular velocity $\dot { \xi } .$ Obstacle avoidance drives $\xi$ using the deviation angle $\mathbf { \bar { \beta } }$ and obstacle bearing φ, while v is adjusted by the minimum obstacle distance d\_obstacle, as in (4).

$$
\left\{ \begin{array}{l} \xi = - \beta \cdot \rho_ {\xi} (| \varphi | - \pi / 2) \\ \mathrm{v} = \rho_ {\mathrm{v}} / \mathrm{d} _ {\text { obstacle }} ^ {\mathrm{m}} + \varepsilon_ {\xi} \end{array} \right.\tag{4}
$$

Target approaching (positioning) limits v by the goal distance d\_goal and the maximum speed v\_max, while still considering obstacle-related terms, as in (5).

$$
\mathrm{v} = \min \left(\mathrm{o} _ {\text { goal }}, \mathrm{d} _ {\text { goal }}, \mathrm{v} _ {\max}, \rho_ {\mathrm{v}} / \mathrm{d} _ {\text { obstacle }} ^ {\mathrm{m}} + \varepsilon_ {\mathrm{v}}\right)\tag{5}
$$

Target turning sets $\xi$ from the difference between φ\_goal and φ\_obstacle, and bounds v by v\_tmax, as in (6).

$$
\left\{ \begin{array}{l} \xi = \beta \cdot \rho_ {\xi} \left(\left| \phi_ {\text { goal }} \right| - \varphi_ {\text { goal }}\right) \\ \mathrm{v} = \min \left(\mathrm{o} _ {\text { goal }} \mathrm{d} _ {\text { goal }}, \mathrm{v} _ {\text { tmax }}, \rho_ {\mathrm{v}} / \mathrm{d} _ {\text { obstacle }} ^ {\mathrm{m}} + \varepsilon_ {\mathrm{v}}\right) \end{array} \right.\tag{6}
$$

## III. GLOBAL PATH CONTROL METHOD OF ROBOT BASED ON FUZZY CONTROL

Based on the analysis results of the robot's motion behaviors, global path planning is carried out for the robot. The fuzzy control method [5] is introduced to promptly correct the path errors of the robot, thereby achieving the planning and control of the global path of the mobile robot.

## A. Global Path Planning

According to the analysis results of the robot's motion behaviors obtained in Section 2, artificial neural network principles are used to establish the global path planning model, and simulated annealing is applied to search an optimal path in a complex environment. The planning model is illustrated in Fig. 2.

![](Zhao2025Industrial_figs/80dcd51a5777a4355ea07575590e0dd83a80faf38d02ae0db9a1469e46ff358f.jpg)  
Fig. 2. Global path planning model of the mobile robot

The global path planning model is formulated as a constrained optimization problem, as shown in (7), where g(x) is the objective function and h\_i(x) are inequality constraints.

$$
\left\{ \begin{array}{l} \min g (x), x \in R ^ {n} \\ s \bullet t. h _ {i} (x) \leq 0 \end{array} \right.\tag{7}
$$

To improve solvability, the model is converted into an energy function F that includes a path-length term $\mathrm { ~ F ~ } _ { - } 1$ and a collision-penalty term $\mathrm { ~ F ~ } _ { Z } ,$ as defined in (8).

$$
\left\{ \begin{array}{l l} F _ {l} & = \sum_ {i = 1} ^ {M - 1} L _ {i} ^ {2} = \sum_ {i = 1} ^ {M - 1} \left[ (x _ {i + 1} - x _ {i}) ^ {2} - (y _ {i + 1} - y _ {i}) ^ {2} \right] \\ F _ {z} & = \sum_ {i = 1} ^ {M} \sum_ {k = 1} ^ {K} Z _ {i} ^ {k} \end{array} \right.\tag{8}
$$

A weighting coefficient δ\_l is introduced to obtain the final energy function and its minimum value, as shown in (9), where δ\_l balances F\_l and $\mathrm { ~ F ~ } _ { Z } .$ Here, M is the number of path points, K is the number of obstacles, and Z\_i^k represents the penalty between obstacle k and path point q(x\_i, y\_i).

$$
\left\{ \begin{array}{l} F = \delta_ {l} F _ {l} + (1 - \delta_ {l}) F _ {z} \\ \min F = \delta_ {l} F _ {l} + (1 - \delta_ {l}) F _ {z} \end{array} \right.\tag{9}
$$

To solve the established planning model, simulated annealing iteratively generates neighboring paths, evaluates the energy change ${ \bar { \Delta \mathrm { F } } } ,$ and accepts inferior solutions with a certain probability to avoid local minima. As the temperature decreases, the search converges to a low-energy global path.

## B. Global Path Control Method of the Robot

According to the detection range of the sensors on the mobile robot and the moving environment, the angle deviation is set $\mathrm { t o } \pm 1 0 ^ { \circ }$ and the central deviation does not exceed ±100 mm. When the deviation exceeds the threshold, the robot is judged to have deviated from the track, and the fuzzy controller is used to regulate the wheel-speed difference to keep the robot moving safely on the selected path.

When designing the controller, the input and output fuzzy sets are defined first (inputs: angle deviation and central deviation; output: left–right wheel-speed difference). A triangular membership function is used for error correction, as shown in (10).

$$
\rho_ {\square} (x) = \left\{ \begin{array}{l} \frac {x - d}{c - d}, c \geq x \geq d \\ \frac {e - x}{e - c}, e \geq x > c \\ 0, d > x / e > x \end{array} \right.\tag{10}
$$

Based on expert rules, fuzzy inference is performed, and the fuzzy output is defuzzified to obtain a crisp control action, as shown in (11).

$$
J _ {0} = \frac {\sum_ {i = 1} ^ {m} \left(\omega_ {c} \left(J _ {i}\right) \times J _ {i}\right)}{\sum_ {i = 1} ^ {m} \omega_ {c} \left(J _ {i}\right)}\tag{11}
$$

## IV. EXPERIMENT

Matlab 2024 was used to simulate global path control; the simulated robot and environment are shown in Fig. 3 and Fig. 4. Three methods were compared: the proposed deeplearning-based global path control, a visual-servo generalized-constraint planner, and a dynamic/static safetyfield planner.

![](Zhao2025Industrial_figs/8196e7c8121c51a570db6ed7a20abe875a50482c186547ff65b731c7f7e9a9e7.jpg)

Fig.3. A simulated mobile robot  
![](Zhao2025Industrial_figs/f2f462c03b8366a569e95c535d75c3fb5c51e3cf753508220015c7e782f5160b.jpg)  
Fig. 4. Simulation path map

## A. Comparison of the angular deviations of the robot paths

With increasing control time, all methods exhibited deviation, but the proposed method produced the smallest path deviation and stabilized the deviation convergence fastest, attributed to the prior motion-behavior analysis.

## B. Comparison of the lengths of the paths planned by the robot

As iterations increased (100–500), path lengths decreased for all methods (Table 1); the proposed method achieved the shortest mean path (114 m) and the best result at 500 iterations (106 m), compared with 132 m (visual-servo) and 130 m (safety-field) mean lengths.

Table 1. path planning length test results for different methods

<table><tr><td>Number of iterations / times</td><td>The proposed method</td><td>Ppath planning method for robots based on visual servo generalized constraint</td><td>Robot path planning method based on dynamic and static safety field</td></tr><tr><td>100</td><td>124</td><td>143</td><td>144</td></tr><tr><td>200</td><td>118</td><td>139</td><td>138</td></tr><tr><td>300</td><td>113</td><td>135</td><td>130</td></tr><tr><td>400</td><td>109</td><td>125</td><td>121</td></tr><tr><td>500</td><td>106</td><td>118</td><td>117</td></tr></table>

## V.CODE EXAMPLE OF GLOBAL PATH PLANNING USING NEURAL NETWORK ALGORITHM

The following is to present each part of the code separately, and add detailed explanations after each piece of code:

## A. Import necessary libraries

Import numpy, TensorFlow, and skfuzzy.control to support arrays, neural planning, and fuzzy correction.

## B. Modeling of the dynamic equation of the mobile robot

MobileRobotDynamics stores r, l, pose=[x,y,theta]; update\_pose(v,w,dt) updates pose using trigonometric relations.

## C. Global path planning model based on neural network

build\_path\_planning\_model builds Sequential Dense(64,relu), Dense(64,relu), Dense(2,linear) and compiles with Adam/MSE.

## D. Design of the fuzzy controller

Define angle\_deviation [-10,10], center\_deviation [- 100,100], output speed\_difference; use triangular membership and fuzzy rules.

## E. Main function, simulating the operation process of the robot

Initialize dynamics, model, and controller; set dt=0.1, num\_steps=100; loop predict, update pose, defuzzify, print.

## VI. CONCLUSION

This paper studied global path planning and global path control for a mobile robot in complex environments. A behavior-based dynamic analysis was used to parameterize obstacle avoidance, target turning, and target approaching; an energy-function planner combined neural-network modeling with simulated annealing to reduce collision risk and avoid local minima; and a fuzzy controller corrected heading and center deviations (±10° and ±100 mm) by regulating differential wheel speed.

Matlab 2024 simulations (Fig. 3–Fig. 4) show that the proposed method produces smaller path deviations (within ±5 cm) and faster deviation convergence (about 10 ms) than two baseline planners, while also generating shorter planned paths. Table 1 reports the best path length at 500 iterations (106 m) and the smallest mean length (114 m), compared with longer paths from the visual-servo and safety-field methods.

Limitations include dependence on modeling assumptions, hand-crafted fuzzy membership functions/rules, and sensitivity to sensor noise or abrupt environmental changes. Future work will incorporate uncertainty-aware sensing, adaptive tuning of fuzzy parameters, and real-robot experiments to validate robustness and real-time performance.

## REFERENCE

[1] Song Q, Li S, Yang J, et al. Intelligent Optimization Algorithm‐Based Path Planning for a Mobile Robot[J]. Computational intelligence and neuroscience, 2021, 2021(1): 8025730.

[2] Razzaq Abdul Wahhab O A, Al-Araji A S. Path Planning and Control Strategy Design for Mobile Robot Based on Hybrid Swarm Optimization Algorithm[J]. International Journal of Intelligen Engineering & Systems, 2021, 14(3).

[3] Singh M K, Parhi D R. Path optimisation of a mobile robot using an artificial neural network controller[J]. International Journal of Systems Science, 2011, 42(1): 107-120.

[4] Noguchi N, Terao H. Path planning of an agricultural mobile robot by neural network and genetic algorithm[J]. Computers and electronics in agriculture, 1997, 18(2-3): 187-204.

[5] Miao C, Chen G, Yan C, et al. Path planning optimization of indoor mobile robot based on adaptive ant colony algorithm[J]. Computers & Industrial Engineering, 2021, 156: 107230.

[6] Yu, D., Liu, L., Wu, S., Li, K., Wang, C., Xie, J., ... & Ji, R. (2024). Machine learning optimizes the efficiency of picking and packing in automated warehouse robot systems. In 2024 Internationa Conference on Computer Engineering, Network and Digital Communication (CENDC 2024).

[7] Mao, Y., Tao, D., Zhang, S., Qi, T., & Li, K. (2025). Research and Design on Intelligent Recognition of Unordered Targets for Robots Based on Reinforcement Learning. arXiv preprint arXiv:2503.07340.

[8] Li, K., Liu, L., Chen, J., Yu, D., Zhou, X., Li, M., ... & Li, Z. (2024, November). Research on reinforcement learning based warehouse robot navigation algorithm in complex warehouse layout. In 2024 6th International Conference on Artificial Intelligence and Computer Applications (ICAICA) (pp. 296-301). IEEE.

[9] Li, K., Wang, J., Wu, X., Peng, X., Chang, R., Deng, X., ... & Hong B. (2024). Optimizing automated picking systems in warehouse robots using machine learning. arXiv preprint arXiv:2408.16633.

[10] Lu, B., Dan, H. C., Zhang, Y., & Huang, Z. (2025). Journey into Automation: Image-Derived Pavement Texture Extraction and Evaluation. arXiv preprint arXiv:2501.02414.

[11] Lu, Z., Lu, B., & Wang, F. (2025). CausalSR: Structural Causal Model-Driven Super-Resolution with Counterfactual Inference. arXiv preprint arXiv:2501.15852.

[12] Dan, H. C., Lu, B., & Li, M. (2024). Evaluation of asphalt pavement texture using multiview stereo reconstruction based on deep learning. Construction and Building Materials, 412, 134837.

[13] Dan, H. C., Huang, Z., Lu, B., & Li, M. (2024). Image-driven prediction system: Automatic extraction of aggregate gradation of pavement core samples integrating deep learning and interactive image processing framework. Construction and Building Materials, 453, 139056.

[14] Tan, L., Liu, D., Liu, X., Wu, W., & Jiang, H. (2025). Efficient Grey Wolf Optimization: A High-Performance Optimizer with Reduced Memory Usage and Accelerated Convergence. Preprints. https://doi.org/10.20944/preprints202412.1974.v2

[15] Tan, L., Liu, X., Liu, D., Liu, S., Wu, W., & Jiang, H. (2024). An Improved Dung Beetle Optimizer for Random Forest Optimization. arXiv [Math.OC]. Retrieved from http://arxiv.org/abs/2411.17738

[16] Li, P., Yang, Q., Geng, X., Zhou, W., Ding, Z., & Nian, Y. (2024, May). Exploring diverse methods in visual question answering. In 2024 5th International Conference on Electronic Communication and Artificial Intelligence (ICECAI) (pp. 681-685). IEEE.

[17] Li, P., Abouelenien, M., Mihalcea, R., Ding, Z., Yang, Q., & Zhou, Y. (2024, May). Deception detection from linguistic and physiological data streams using bimodal convolutional neural networks. In 2024 5th International Conference on Information Science, Parallel and Distributed Systems (ISPDS) (pp. 263-267). IEEE.

[18] Tao, Y., Wang, Z., Zhang, H., & Wang, L. (2024). Nevlp: Noise-robust framework for efficient vision-language pre-training. arXiv preprint arXiv:2409.09582.

[19] Tao, Y., Shen, Y., Zhang, H., Shen, Y., Wang, L., Shi, C., & Du, S. (2024, December). Robustness of large language models against adversarial attacks. In 2024 4th International Conference on Artificial Intelligence, Robotics, and Communication (ICAIRC) (pp. 182-185). IEEE.

[20] Shi, C., Tao, Y., Zhang, H., Wang, L., Du, S., Shen, Y., & Shen, Y. (2025). Deep Semantic Graph Learning via LLM based Node Enhancement. arXiv preprint arXiv:2502.07982.

[21] Du, S., Tao, Y., Shen, Y., Zhang, H., Shen, Y., Qiu, X., & Shi, C. (2025). Zero-Shot End-to-End Relation Extraction in Chinese: A Comparative Study of Gemini, LLaMA and ChatGPT. arXiv preprint arXiv:2502.05694.

[22] Shen, Y., Zhang, H., Shen, Y., Wang, L., Shi, C., Du, S., & Tao, Y. (2024). AltGen: AI-Driven Alt Text Generation for Enhancing EPUB Accessibility. arXiv preprint arXiv:2501.00113.

[23] Liang, X., Tao, M., Xia, Y., Shi, T., Wang, J., & Yang, J. (2024). Cmat: A multi-agent collaboration tuning framework for enhancing small language models. arXiv preprint arXiv:2404.01663.

[24] Zhou, Z., Zhang, J., Zhang, J., He, Y., Wang, B., Shi, T., & Khamis, A. (2024). Human-centric Reward Optimization for Reinforcement Learning-based Automated Driving using Large Language Models. arXiv preprint arXiv:2405.04135.

[25] Yang, C., He, Y., Tian, A. X., Chen, D., Wang, J., Shi, T., ... & Liu, P. (2024). Wcdt: World-centric diffusion transformer for traffic scene generation. arXiv preprint arXiv:2404.02082.

[26] He, Y., Wang, X., & Shi, T. (2024, August). Ddpm-moco: Advancing industrial surface defect generation and detection with generative and contrastive learning. In International Joint Conference on Artificial Intelligence (pp. 34-49). Singapore: Springer Nature Singapore.

[27] He, Y., Li, S., Li, K., Wang, J., Li, B., Shi, T., ... & Wang, X. (2025). Enhancing Low-Cost Video Editing with Lightweight Adaptors and Temporal-Aware Inversion. arXiv preprint arXiv:2501.04606.

[28] Wang, J., He, Y., Li, K., Li, S., Zhao, L., Yin, J., ... & Wang, X. (2025). MDANet: A multi-stage domain adaptation framework for generalizable low-light image enhancement. Neurocomputing, 129572.