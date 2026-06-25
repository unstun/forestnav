---
citation_key: Xie2023JointSpace
arxiv_id: 2311.12385
arxiv_url: "https://arxiv.org/abs/2311.12385"
title: "Joint-Space Multi-Robot Motion Planning with Learned Decentralized Heuristics"
authors_short: "Fengze Xie et al."
year: 2023
direction_tag: D_asymptotically_optimal_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:34:14Z
origin: ai+web
reviewed: false
---

# Joint-Space Multi-Robot Motion Planning with Learned Decentralized Heuristics

Fengze Xie, Marcus Dominguez-Kuhne, Benjamin Riviere, Jialin Song, Wolfgang Honig,¨ Soon-Jo Chung, Yisong Yue, California Institute of Technology {fxxie, mddoming, briviere, jssong, whoenig, sjchung, yyue}@caltech.edu

## Abstract

In this paper, we present a method of multi-robot motion planning by biasing centralized, sampling-based tree search with decentralized, data-driven steer and distance heuristics. Over a range of robot and obstacle densities, we evaluate the plain Rapidly-expanding Random Trees (RRT), and variants of our method for double integrator dynamics. We show that whereas plain RRT fails in every instance to plan for 4 robots, our method can plan for up to 16 robots, corresponding to searching through a very large 65-dimensional space, which validates the effectiveness of data-driven heuristics at combating exponential search space growth. We also find that the heuristic information is complementary; using both heuristics produces search trees with lower failure rates, nodes, and path costs when compared to using each in isolation. These results illustrate the effective decomposition of highdimensional joint-space motion planning problems into local problems.

## 1 Introduction

Applications for autonomous teams of robots are rapidly expanding into domains of urban search and rescue, space and sea exploration, self-driving vehicles, and warehouse robotics. However, a critical mid-level component of the autonomy hierarchy, multi-robot motion planning, remains an active area of research because of the non-convexity of the underlying optimization problem and the exponential growth of the search space with the number of robots.

We are in particular interested in kinodynamic motionplanning, where robots obey dynamic constraints in a continuous state space; as opposed to path-planning, which usually ignores dynamics and plans in discrete space. A common kinodynamic motion planning technique is to use random sampling to grow a search tree, e.g., Rapidly-Exploring Random Tree (RRT) (Kuffner and LaValle 2000) and Expansive Space Tree (EST) (Hsu, Latombe, and Motwani 1997). Theoretical analysis of the RRT algorithm has shown it to be probabilistically complete (LaValle and Jr. 2001) and variants have been proposed with asymptotic optimality properties (Karaman and Frazzoli 2010; Hauser and Zhou 2016). However, sampling-based methods do not perform well for systems with complex dynamics or the large search dimension of robot teams (LaValle 2006). Other classical multirobot methods include (Zhou et al. 2017; Wang, Ames, and Egerstedt 2017; van den Berg et al. 2009) but these do not use a tree-structure and cannot guarantee the completeness property of the algorithm, i.e., if a feasible solution exists, the algorithm will find it.

![](Xie2023JointSpace_figs/dc90d038d01be464689a15fb33f57678e6dfc576841ed5f16ea09cb1763740a1.jpg)  
Figure 1: Schematic of our approach: Learned steer and distance heuristics guide the tree search, resulting in effective high-dimensional search and solutions with lower path cost, lower wall-clock time, fewer nodes, and lower failure rate.

Recently, machine learning techniques have been applied to robotic planning. Some single-agent methods tackle search complexity by biasing the tree search with datadriven heuristics (Silver et al. 2017; Ichter, Harrison, and Pavone 2018; Chiang et al. 2019; Chen et al. 2020). Our work extends this approach to multi-robot planning with decentralized heuristics compatible with variable team sizes. As decentralized heuristics compute control inputs for each robot with local information, the performance of these heuristics in a joint-space context illustrates the effective decomposition of high-dimensional joint-space motion planning problem into local motion planning problems.

Existing data-driven methods either use reinforcement learning or imitation learning paradigms. Reinforcement learning methods (Chiang et al. 2019) are very general, but typically suffer from long training time. Instead, we use imitation learning from a centralized expert to effectively learn both heuristics with permutation-invariant neural network models based on Deep Sets (Zaheer et al. 2017). Our network encoding also permits a continuous state representation for dynamically coupled motion planning. Other multiagent planners are discrete (Sartoretti et al. 2019) and cannot handle dynamical constraints necessary for certain robotic applications. Riviere et al. (2020) also uses Deep Sets to\` study continuous multi-robot planning and learns the steering function from data but, without integrating the policy into a tree structure, it lacks interpretability and completeness guarantees. In this work, we address this limitation by integrating data-driven distance and steering heuristics into RRT and inheriting its probabilistic completeness property.

The overview of our method is as follows. First, we train a steer function that controls a single robot to a goal state using trajectory data from a centralized planner with a globalto-local imitation learning method. Next, we train a distance function with cost-to-go information from rolling out trajectories with the steer function. Then, both decentralized heuristics are integrated into a centralized RRT planner for joint-space planning. Our decentralized heuristics are compatible with arbitrary team sizes and enjoy computational efficiency and performance advantage in highdimensional joint-space. Integrating them with a centralized planner leads to improved interpretability, probabilistic completeness guarantee, and a higher-level safety guarantee. Both heuristics and their effect on RRT are visualized in Fig. 1. To the best of our knowledge, this work is the first to use decentralized heuristics to guide centralized multi-robot search in a continuous state with dynamical constraints. The success of our method demonstrates the effective decomposition of high-dimensional joint-space motion planning problems into local problems.

We empirically evaluate our method on a range of obstacle and robot density motion planning problems and show that equipping traditional planners with our heuristics is necessary to achieve a non-zero success rate for 4 robots, and permits planning for up to 16 robots. We also show that steer and distance heuristics each benefit the search independently by comparing variants of our method.

## 2 Approach

Problem Statement: We consider the classical kinodynamic motion planning problem (Hauser and Zhou 2016): given a state space, X , a feasible control space, U , a start state, $x _ { 0 } \in$ $x ,$ kinematic feasible set, $\mathcal F _ { t } \subset \mathcal X$ , dynamical constraints $x _ { t + 1 } = f ( x _ { t } , u _ { t } )$ , and goal set, $\chi _ { \mathrm { g o a l } } \subset \mathcal X$ , find a series of admissible control inputs $\{ u _ { t } \} _ { t \in [ 0 , T ] } , u _ { t } \in \mathcal { U } .$ , that result in a motion that starts at the initial condition, ends in the goal set, and remains in the free space for the entire trajectory, i. ${ \bf e . , } x _ { 0 } = x _ { 0 } \mathrm { ~ , ~ } x _ { t } \in \mathcal { F } _ { t } , x _ { T } \in \mathcal { X } _ { \mathrm { g o a l } }$ where $T$ is the last timestep in the motion plan.

The start state, $x _ { 0 }$ is constructed from composing the initial states of each robot, $x _ { 0 } ^ { i } , \mathbf { e . g . } , x _ { 0 } = [ x _ { 0 } ^ { 1 } ; \dots ; x _ { 0 } ^ { | \nu | } ]$ , where the set of all robot indices is denoted $\nu ,$ the robot index is denoted with a superscript, and the time index is denoted with a subscript. This joint-space representation couples the dimension of the state space, X , to the number of robots. In particular, we consider the double integrator system in a two-dimensional space where, for robot i at time $t ,$ the state, control, and dynamics are defined as:

$$
x _ {t} ^ {i} = \left[ \begin{array}{c} p _ {t} ^ {i} \\ v _ {t} ^ {i} \\ t \end{array} \right], \quad u _ {t} ^ {i} = a _ {t} ^ {i}, \quad x _ {t + \Delta_ {t}} ^ {i} = \left[ \begin{array}{c} p _ {t} ^ {i} \\ v _ {t} ^ {i} \\ t \end{array} \right] + \left[ \begin{array}{c} v _ {t} ^ {i} \\ a _ {t} ^ {i} \\ 1 \end{array} \right] \Delta_ {t},\tag{1}
$$

where $p , v , a$ are position, velocity, and acceleration vectors in $\mathbb { R } ^ { 2 } , \Delta _ { t }$ is the simulation timestep and t is the current time. The dynamics correspond to the Propagate function in line 15 of Algorithm 1. The kinematic feasibility space $\mathcal { F } _ { t }$ imposes two constraints: upper bound on velocity and collision avoidance with other agents and obstacles:

$$
\begin{array}{r} \mathcal {F} _ {t} = \{x _ {t} | \| v _ {t} ^ {i} \| _ {2} \leq \overline {{v}}, \| p _ {t} ^ {i} - p _ {t} ^ {j} \| _ {2} \geq 2 r _ {\mathrm{robot}}, \\ p _ {t} ^ {i} \not \in \Omega , \forall i, j \in \mathcal {V}, j \neq i \} \end{array}\tag{2}
$$

where Ω is the set union of all obstacle positions and $r _ { \mathrm { r o b o t } }$ is the robot radius. The admissible control space, U, imposes a bounded control input: ${ \mathcal { U } } = \{ u \ | \ \| u _ { t } ^ { i } \| _ { 2 } \leq \overline { { u } } , \ \forall i , t \}$ . Finally, the goal set $\mathcal { X } _ { \mathrm { g o a l } }$ is defined as the ball of radius $r _ { \mathrm { g o a l } }$ around each robot’s goal state, $g ^ { i } \colon$

$$
\mathcal {X} _ {\mathrm{goal}} = \{x \mid \sum_ {i \in \mathcal {V}} \| x ^ {i} - g ^ {i} \| _ {2} ^ {2} \leq r _ {\mathrm{goal}} \}.\tag{3}
$$

To empirically evaluate the proposed method, we consider the following metrics: success(/fail) rate, number of nodes, and path cost. Each motion planning problem is counted as a success unless the wall-clock time exceeds a time-out threshold value before reaching the goal set. The number of nodes is the size of the tree at problem termination. The path cost is calculated in an optimal control sense by integrating the norm of the control input across the entire trajectory:

$$
c = \sum_ {i} \sum_ {t} \| u _ {t} ^ {i} \| _ {2} ^ {2} \Delta_ {t}.\tag{4}
$$

Method: Our approach is to augment high-dimensional kinodynamic RRT with decentralized steer and distance heuristics, see Algorithm 1 where our changes from the traditional algorithm are on Lines $7 - 8$ and 12 – 13. First, we recap RRT, then we introduce the heuristics and their integration into Algorithm 1, and finally we discuss how they are trained.

Kinodynamic RRT typically works in four major steps: i) sample a random state from a distribution (line 3, where <sup>U</sup> denotes the uniform distribution), ii) find the closest state that is currently in the search tree (line 5), iii) steer towards the random state from the closest state in the tree (line 10), and iv) add the resulting motion to the tree if it is collisionfree (lines 14 – 19).

Before introducing the heuristics, we define a observation model to generate local inputs for the decentralized heuristics. Given a joint state x and a goal state $g ^ { i }$ , the local observation for the ith robot is:

$$
o ^ {i} = h ^ {i} (x, g ^ {i}) = \left[ g ^ {i} - x ^ {i}, \{x ^ {i j} \} _ {j \in \mathcal {N} _ {\nu} ^ {i}}, \{x ^ {i j} \} _ {j \in \mathcal {N} _ {\Omega} ^ {i}} \right],\tag{5}
$$

where $h ^ { i }$ is the observation function and the double superscript notation denotes a relative state or position, e.g., ${ \bf { \dot { x } } } ^ { i j } = { \bf { \dot { x } } } ^ { j } - x ^ { i }$ and $p ^ { i j } = p ^ { j } - p ^ { i }$ . In addition, $\mathcal { N } _ { \mathcal { V } } ^ { i } , \mathcal { N } _ { \Omega } ^ { i }$ , denote the neighboring set of robots and obstacles, respectively. These sets are defined by the observation radius, $r _ { \mathrm { s e n s e } } , \mathrm { e . g . }$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: RRT With Decentralized Heuristics
Input: $x_0, \mathcal{X}_{\text{goal}}, \mathcal{F}_t$ $T = \text{Tree}(x_0)$;
while True do
    $x_{\text{rand}} \leftarrow \mathbb{U}(\mathcal{X})$;
    if $\beta_d &lt; \mathbb{U}([0,1])$ then
    $x_{\text{nearest}} \leftarrow \text{KdTreeQuery}(x_{\text{rand}}, \mathcal{T}, 1)$;
    else
    $\mathcal{X}_{\text{near}} \leftarrow \text{KdTreeQuery}(x_{\text{rand}}, \mathcal{T}, K)$;
    $x_{\text{nearest}} \leftarrow \arg \min_{x \in \mathcal{X}_{\text{near}}} \sum_i \mathcal{H}_d(o^i(x^i, x_{\text{rand}}^i)) + \lambda_t |t - t_{\text{rand}}|$;
    if $\beta_s &lt; \mathbb{U}([0,1])$ then
    $u \leftarrow \text{ApproxSteer}(x_{\text{nearest}}, x_{\text{rand}})$;
    else
    for $i \in \mathcal{V}$ do
    $u^i \leftarrow \mathcal{H}_s(o^i(x_{\text{nearest}}^i, x_{\text{rand}}^i))$;
    $\Delta_t \leftarrow \mathbb{U}([\underline{\Delta_t}, \overline{\Delta_t}])$;
    $x_{\text{new}} \leftarrow \text{Propagate}(x_{\text{nearest}}, u, \Delta_t)$;
    if $x_{\text{new}} \in \mathcal{F}_t$ then
    $\mathcal{T}.insert(x_{\text{nearest}}, x_{\text{new}})$;
    if $x_{\text{new}} \in \mathcal{X}_{\text{goal}}$ then
    break;
    end
</div>

$$
\mathcal {N} _ {\mathcal {V}} ^ {i} = \{j \in \mathcal {V} \mid \| p ^ {i j} \| _ {2} \leq r _ {\text { sense }} \}.\tag{6}
$$

For obstacles, the relative state is constructed with a position to the center of the obstacle and zero velocity.

The first heuristic is a steer function that replaces the standard ApproxSteer function (line 10). Conventionally, $A p \mathrm { - }$ proxSteer samples many random control inputs, forward propagates the dynamics, and chooses the control resulting in the closest state to the desired state. Instead, our steer heuristic, ${ \mathcal { H } } _ { s } ,$ imitates the solution to a boundary value problem and maps observation to local robot control:

$$
u ^ {i} = \mathcal {H} _ {s} (o ^ {i} (x _ {\text { nearest }} ^ {i}, x _ {\text { rand }} ^ {i})).\tag{7}
$$

The joint-space, centralized RRT steer function is composed by calling our decentralized steer heuristic on all robots (lines 12 – 13). The result is that leaf node generation, x<sub>nearest</sub> is more consistent with the desired leaf generation.

The second heuristic is a distance, or cost-to-go function. For double integrator systems, a common RRT distance function is a hand-tuned weighted Euclidean distance. In contrast, our method is automatically tuned with a datadriven approach. In particular, the distance heuristic, $\mathcal { H } _ { d } ,$ inputs a local observation and outputs some value corresponding to cost-to-go, where $\lambda _ { t }$ is a scalar that balances the spatial and temporal costs:

$$
\tilde {c} ^ {i} = \mathcal {H} _ {d} (o ^ {i} (x _ {\mathrm{nearest}} ^ {i}, x _ {\mathrm{rand}} ^ {i})) + \lambda_ {t} | t _ {\mathrm{nearest}} - t _ {\mathrm{rand}} |\tag{8}
$$

As before, the RRT distance function is composed by summing the heuristic cost for each robot (lines $7 - 8 )$ . Thus, our distance metric accounts for obstacles and other robots. The effect on the tree growth is that the tree will choose the correct node to steer from; $\mathrm { e . g }$ . if a node is behind an obstacle wall, this distance function will correctly identify its large cost-to-go, even if the Euclidean distance is small. The heuristics are visualized in Fig. 1.

Both heuristics are integrated in a probabilistic manner via hyperparameters $0 \leq \beta _ { d } , \beta _ { s } \leq 1$ . We use the learned distance heuristic with probability $\beta _ { d }$ and the learned steering heuristic with probability $\beta _ { s }$ . In other cases, we use the conventional functions (lines 4 and 9). By adopting this scheme, similar to Ichter, Harrison, and Pavone (2018), we maintain the probabilistic completeness guarantee of RRT.

Implementations of RRT often utilize the KD-tree data structure for the distance function (S¸ ucan, Moll, and Kavraki 2012), which reduces the complexity of the nearest-neighbor computation from n to log $n ,$ where n is the size of the tree. However, KD-trees cannot operate on state-dependent distance metrics like $\mathcal { H } _ { d } .$ In order to maintain the same complexity as existing RRT methods, we use pre-filtering where we compute the closest K-neighbors with a KD-tree using a Euclidean distance, then we evaluate the distance heuristic only on the closest K nodes (line 7). In practice, this method improves the runtime of the search significantly. We apply another common implementation technique known as goal biasing. This method acts on the sample function (line 3) by using the goal state rather than $x _ { \mathrm { r a n d } }$ with probability $\mu .$ In practice, we found that the heuristics permitted setting the goal bias parameter to high values.

Training: To train the steer heuristic, $\mathcal { H } _ { s }$ , we use a similar training procedure to recent work in global-to-local learning (Riviere et al. 2020). First, we collect trajectory data,\` from an existing centralized planner (Honig et al. 2018a).¨ Then, we transform the joint-space state-action pairs to decentralized observation-action pairs by applying a local observation model (5) and considering the action of a single robot. Finally, we train a neural network policy with deep imitation learning on these observation-action pairs with a mean-squared loss function. We use Deep Sets (Zaheer et al. 2017) to encode variable observation sizes in a continuous state representation. The Deep Sets architecture leverages permutation invariance of observations, resulting in a compact learning representation and relatively small model, resulting in faster inference during the tree search. The steer heuristic has the following construction:

$$
\mathcal {H} _ {s} (o _ {t} ^ {i}) = \Psi ([ \rho_ {\Omega} (\sum_ {j \in \mathcal {N} _ {\Omega} ^ {i}} \phi_ {\Omega} (x ^ {i j})); \rho_ {\mathcal {V}} (\sum_ {j \in \mathcal {N} _ {\mathcal {V}} ^ {i}} \phi_ {\Omega} (x ^ {i j})) ])\tag{9}
$$

where the semicolon denotes a stacked vector and $\Psi , \rho _ { \Omega } , \phi _ { \Omega } , \rho _ { V } , \phi _ { V }$ are feed-forward networks.

To train the distance heuristic, $\mathcal { H } _ { d }$ , we collect trajectory data by rolling out trajectories with the steer heuristic. We transform each state to a set of local observations for each robot with (5). Then, we calculate the cost-to-go for each robot observation along the trajectory similar to (4) by summing the control effort from the current time to the terminal time. The distance heuristic is trained in a supervised learning manner with a similar architecture as steer with a single output dimension and using the cost-to-go target instead of the action.

![](Xie2023JointSpace_figs/89966a020d804533e1765386d7b5c8837021aa8fd5585117098dc21334e33d11.jpg)  
Figure 2: Four instances of joint-space planning

## 3 Experimental Results

Variants and Baseline: We consider 3 variants and a baseline algorithm corresponding to the combinations of heuristics. In all figures, we label each planning solution with either: 1) BOTH that uses both heuristics, 2) DISTANCE that uses only distance heuristic, 3) STEER that uses only steer heuristic, and 4) NONE corresponding to plain RRT baseline. These variants are equivalently constructed by setting the value of corresponding hyperparameter, $\beta _ { s , d } ,$ to zero.

Experimental Setup: We generate random 8m × 8m maps with 10% or 20% obstacles randomly placed in a grid pattern. We consider planning problems for 4, 8, and 16 robots. The expansion time step, $\Delta _ { t }$ is uniformly chosen from range $\Delta _ { t } = 0 . 1 , \overline { { \Delta _ { t } } } = 0 . 7 5$ . We apply a velocity bound $\overline { { v } } = 0 . 5$ and an acceleration bound $\overline { { a } } ~ = ~ 0 . 5$ . The robot’s have radius $r _ { \mathrm { r o b o t } } = 0 . 1 2 5$ and $r _ { \mathrm { g o a l } } = 0 . 2 | \nu |$ . For each different environment configuration (number of robots and obstacle density), we generate 100 random maps, with a total time threshold of 600 seconds for each map. The distance function uses $\lambda _ { t } ~ = ~ 0 . 0 5$ time bias, and, after the baseline distance function is tuned for performance, the velocities are weighed with a 0.3 coefficient. The pre-filter step is parameterized with $K = 1 0$ closest nodes. The hyperparameters determining the heuristic frequency are $\beta _ { s } = 0 . 5 , \beta _ { d } = 1 . 0$ We choose a goal bias $\mu = 0 . 3$ and a goal time $T = 6 0$

Results: We generate 600 random maps for a range of robot and obstacle densities and evaluate each variant for a total of 2,400 instances and plot the collective statistics in Fig. 3. First, we compare the average performance across all cases of the four algorithms. The planner with both heuristics consistently has the best performance on all three metrics, empirically validating the effectiveness of both heuristics. Over the 4 agents, 10% obstacle case, the BOTH variant has an 67.7% and 67.4% improvement over STEER and an 81.8% and 83.2% improvement over DISTANCE in number of nodes and path cost, respectively. The NONE variant is unable to solve any of the cases. Next, we compare the failure rate of each of methods over problem complexity, measured through agent and obstacle density. We find that although the STEER variant seems more robust than the DISTANCE, the DISTANCE heuristic provides complementary information as the BOTH variant far outperforms the STEER variant in success rate across agent densities.

![](Xie2023JointSpace_figs/8b45f764ad49b80adea3165009650ba3202dc28a48022396957fdab0a03b46fc.jpg)  
Figure 3: Joint-space planner results for each problem class where each bar represents 100 instances. Missing bars indicate that the respective algorithm did not solve any instance.

An instance of joint-space planner for our four variants is shown in Figure 2. In contrast to the NONE variant that samples many states in areas near the obstacles, the DIS-TANCE variant correctly interprets the distance near obstacles, resulting in even sampling throughout the space. The STEER variant and BOTH variant can bias to the goal while avoiding obstacles. Combining distance and steer heuristics, BOTH variant is the most robust solution and has the least control effort and smallest curvature of trajectories.

In our supplemental material, we include implementation details, a sequential planner variant, and a swapping corridor example to demonstrate the advantages of joint-space over sequential planning.

## 4 Conclusion

In this work we combine decentralized learned control policies with centralized informed search. Specifically, we present two novel decentralized data-driven heuristics that enable existing sampling-based kinodynamic motion planner to find better solutions quicker, even in high-dimensional search spaces, while retaining theoretical guarantees. Unlike traditional sampling-based planners, our method can effectively plan in joint-space for up to 16 doubleintegrator robots, corresponding to searching through a 65- dimensional state space. In future work, we will investigate more robot dynamics and learning generalization to different robot density regimes.

## References

Chen, B.; Dai, B.; Lin, Q.; Ye, G.; Liu, H.; and Song, L. 2020. Learning to Plan in High Dimensions via Neural Exploration-Exploitation Trees. In International Conference on Learning Representations.

Chiang, H. L.; Hsu, J.; Fiser, M.; Tapia, L.; and Faust, A. 2019. RL-RRT: Kinodynamic Motion Planning via Learning Reachability Estimators From RL Policies. IEEE Robotics Autom. Lett. 4(4): 4298–4305. doi:10.1109/LRA. 2019.2931199.

Hauser, K.; and Zhou, Y. 2016. Asymptotically Optimal Planning by Feasible Kinodynamic Planning in a State-Cost Space. IEEE Trans. Robotics 32(6): 1431–1443. doi: 10.1109/TRO.2016.2602363.

Hsu, D.; Latombe, J. .; and Motwani, R. 1997. Path planning in expansive configuration spaces. In International Conference on Robotics and Automation, 2719–2726 vol.3. doi: 10.1109/ROBOT.1997.619371.

Honig, W.; Preiss, J. A.; Kumar, T. K. S.; Sukhatme, G. S.; ¨ and Ayanian, N. 2018a. Trajectory Planning for Quadrotor Swarms. IEEE Transactions on Robotics 34(4): 856–869. doi:10.1109/TRO.2018.2853613.

Honig, W.; Preiss, J. A.; Kumar, T. K. S.; Sukhatme, G. S.; ¨ and Ayanian, N. 2018b. Trajectory Planning for Quadrotor Swarms. IEEE Transactions on Robotics 34(4): 856–869. doi:10.1109/TRO.2018.2853613.

Ichter, B.; Harrison, J.; and Pavone, M. 2018. Learning Sampling Distributions for Robot Motion Planning. In International Conference on Robotics and Automation, 7087–7094. IEEE. doi:10.1109/ICRA.2018.8460730.

Karaman, S.; and Frazzoli, E. 2010. Optimal kinodynamic motion planning using incremental sampling-based methods. In CDC, 7681–7687. IEEE.

Kuffner, J. J.; and LaValle, S. M. 2000. RRT-connect: An efficient approach to single-query path planning. In International Conference on Robotics and Automation, 995–1001 vol.2. doi:10.1109/ROBOT.2000.844730.

LaValle, S. M. 2006. Planning Algorithms. Cambridge University Press.

LaValle, S. M.; and Jr., J. J. K. 2001. Randomized Kinodynamic Planning. I. J. Robotics Res. 20(5): 378–400. doi: 10.1177/02783640122067453.

Riviere, B.; H\` onig, W.; Yue, Y.; and Chung, S. 2020. GLAS:¨ Global-to-Local Safe Autonomy Synthesis for Multi-Robot Motion Planning With End-to-End Learning. IEEE Robotics and Automation Letters 5(3): 4249–4256. doi:10.1109/LRA. 2020.2994035.

Sartoretti, G.; Kerr, J.; Shi, Y.; Wagner, G.; Kumar, T. K. S.; Koenig, S.; and Choset, H. 2019. PRIMAL: Pathfinding via Reinforcement and Imitation Multi-Agent Learning. IEEE Robotics and Automation Letters 4(3): 2378–2385. doi:10. 1109/LRA.2019.2903261.

Silver, D.; Schrittwieser, J.; Simonyan, K.; Antonoglou, I.; Huang, A.; Guez, A.; Hubert, T.; Baker, L.; Lai, M.; Bolton,

A.; Chen, Y.; Lillicrap, T. P.; Hui, F.; Sifre, L.; van den Driessche, G.; Graepel, T.; and Hassabis, D. 2017. Mastering the game of Go without human knowledge. Nature 550(7676): 354–359. doi:10.1038/nature24270.

S¸ ucan, I. A.; Moll, M.; and Kavraki, L. E. 2012. The Open Motion Planning Library. IEEE Robotics & Automation Magazine 19(4): 72–82. doi:10.1109/MRA.2012.2205651. https://ompl.kavrakilab.org.

van den Berg, J.; Guy, S. J.; Lin, M. C.; and Manocha, D. 2009. Reciprocal n-Body Collision Avoidance. In ISRR, volume 70 of Springer Tracts in Advanced Robotics, 3–19. Springer.

Wang, L.; Ames, A. D.; and Egerstedt, M. 2017. Safety Barrier Certificates for Collisions-Free Multirobot Systems. IEEE Trans. Robotics 33(3): 661–674.

Zaheer, M.; Kottur, S.; Ravanbakhsh, S.; Poczos, B.; Salakhutdinov, R. R.; and Smola, A. J. 2017. Deep Sets. In Advances in Neural Information Processing Systems, volume 30, 3391–3401.

Zhou, D.; Wang, Z.; Bandyopadhyay, S.; and Schwager, M. 2017. Fast, On-line Collision Avoidance for Dynamic Vehicles Using Buffered Voronoi Cells. IEEE Robotics Autom. Lett. 2(2): 1047–1054.

## A Sequential Planner

Sequential planners plan for one robot at a time while sequentially adding the completed robots’ motions to the environment as dynamic obstacles. This decomposition finds solutions in shorter times, but is not a complete search and its performance often suffers in dense environments. We use the same parameters as the joint-space method, except the goal radius is fixed to 0.2.

For our numerical validation of our method, we generate and evaluate 2,400 instances motion planning problems and plot the statistics in Fig. 4. The planner with both heuristics consistently has the best performance on all three metrics, empirically validating the effectiveness of both heuristics for a sequential planner. Our sequential planner with both heuristics improves traditional sequential samplingbased planners by producing solutions with 75% lower path cost, 69% lower wall-clock time, 88% fewer nodes, and 93% lower failure rate on average over all environments.

![](Xie2023JointSpace_figs/9c27dfc6ee77cbbf48d630fea8db3c50cb20a13e616679a41c0a47748d39f1a3.jpg)  
Figure 4: Sequential planner results for each problem class where each bar represents 100 instances. Missing bars indicate that the respective algorithm did not solve any instance.

Next, we analyze the performance gap of the methods across complexity of cases measured through robot density. Specifically, we compare the failure rate difference, which increases from 0.78 to 0.97 across robot density cases from 4-robot 10% obstacle density to 8-robot 10% obstacle density. Moreover, the path cost ratio of NONE variant over BOTH variant also increases from 3.4 to 4.8. This result implies the outlook that as we demand autonomy in more complex scenarios, we will need to rely more on heuristics to search because traditional uniform sampling methods will fail to search the high-dimensional space effectively.

## B Swapping Example

However, as sequential planning is not a complete search and its performance often suffers in dense environments, thus motivating our joint-space planning approach with better theoretical properties with respect to completeness. A classical example is the following ’swapping’ problem shown in Figure 5:

![](Xie2023JointSpace_figs/916e67541de95fad957d909e160cbd3ebabace37393652b19f54b37747a0d786.jpg)  
Figure 5: From right to left: The first example shows the joint-space planner correctly finding the swapping solution. The second two examples show the sequential planner failing to solve the problem because, after it has finalized the plan for the first robot, the second robot is trapped and cannot consider the possibility of the alcove solution.

In this example, the robots must swap positions through a narrow corridor, where their physical radius is such that both cannot pass at the same time. The only solution is for one robot to pass into the alcove and wait for the other to pass. We find the desired result: the joint-space planner finds the swapping solution while the sequential planner fails by nature: after it has finalized the plan for the first robot, the second robot is trapped and cannot consider the possibility of the alcove solution.

## C Implementation Details

Here we provide additional details of our learning implementation including problem and dataset generation, network architecture, and training. Our steer function is similar to the decentralized policy learned by deep imitation learning described in the GLAS (Riviere et al. 2020). This\` method is based on an observation-action pair dataset using expert demonstration and a deep learning architecture compatible with dynamic sensing network topologies. Our distance function has a similar neural architecture.

Problem Generation: For data generation of our network, we use an existing implementation of a centralized global trajectory planner (Honig et al. 2018b) and generate ¨ ≈ 2 × 10<sup>5</sup>(200k) random 8m×8m environments with 10% or 20% obstacles(1m × 1m) randomly placed in a grid pattern. We consider planning problems for 4, 8, and 16 robots. (Same as maps we used for experimental setup). The timestep for sample trajectories is set to 0.5s and there are $| D | = { \bar { 4 } } 0 \times$ $1 0 ^ { 6 }$ data points generated in total, evenly distributed over the 6 different environment kinds. The hyperparameters of $\rho _ { \mathcal { V } }$ and $\rho \Omega$ are described in the first paragraph of experimental results.

Dataset: As aforementioned, the expert demonstration used for our dataset is from an existing centralized planner (Honig et al. 2018b). This planner uses an optimization¨ framework to minimize control effort, so the policy imitates a solution with high performance. Specifically, we create our dataset by generating fixed-size static obstacles randomly placed in a grid pattern and random start/goal positions for a variable number of robots without any collision with obstacles and each other. We use the centralized planner to compute the trajectory. For each timestep and robot, we retrieve the local observation, $\mathbf { o } ^ { i }$ by masking the non-local information, and retrieve the action $\mathbf { u } ^ { i }$ through the second derivative of the robot i position. We repeat this process $n _ { \mathrm { c a s e } }$ times for each robot. Our dataset D, is:

$$
\mathcal {D} = \left\{\left(\mathbf {o} ^ {i}, \mathbf {u} ^ {i}\right) | \forall i \in \mathcal {V}, \forall k \in \{1... n _ {\text { case }} \}, \forall t \right\}.\tag{10}
$$

Network Architecture: The number of visible robots and obstacle for each robot greatly varies in each iteration, leading to a time-varying dimensionality of the observation. Leveraging the permutation invariance of the observation, we use Deep Set architecture (Zaheer et al. 2017) to model variable number of robots and obstacles. In the deep set paper (Zaheer et al. 2017), Theorem 7 establish the following property, which informs the neural architecture of our networks:

Theorem 1: Let $f : [ 0 , 1 ] ^ { l } \to \mathbb { R }$ be a permutation invariant continuous function iff it has the representation:

$$
f (x _ {1}, \dots , x _ {l}) = \rho \left(\sum_ {m = 1} ^ {l} \phi (x _ {m})\right),\tag{11}
$$

for some continuous outer and inner function $\rho : \mathbb { R } ^ { l + 1 }  \mathbb { R }$ and $\phi : \mathbb { R } \to \mathbb { R } ^ { l + 1 }$ respectively.

Intuitively, the $\rho$ function acts to combine the contributions of each element and the $\phi$ function acts as a contribution from each element in the set. Applying Deep Sets, our steer heuristic can learn the contribution of the neighboring set of robots and obstacles with the following network structure:

$$
\mathcal {H} _ {s} (o _ {t} ^ {i}) = \Psi ([ \rho_ {\Omega} (\sum_ {j \in \mathcal {N} _ {\Omega} ^ {i}} \phi_ {\Omega} (x ^ {i j})); \rho_ {\mathcal {V}} (\sum_ {j \in \mathcal {N} _ {\mathcal {V}} ^ {i}} \phi_ {\Omega} (x ^ {i j})) ]),\tag{12}
$$

where the semicolon denotes a stacked vector and $\Psi , \rho _ { \Omega } ,$ , ϕ<sub>Ω</sub>, $\rho _ { V } ,$ ϕ<sub>V</sub> are feed-forward networks of the form:

$$
F F (\mathbf {x}) = W ^ {l} \sigma (\dots W ^ {1} \sigma (\mathbf {x})),\tag{13}
$$

where $\mathrm { F F }$ is a feed-forward network on input $\mathbf { x } , W ^ { l }$ is the weight matrix of the $l ^ { \mathrm { t h } }$ layer and σ is the activation function.

The distance heuristic is trained in a supervised learning manner with similar architecture as steer with a single output dimension. The target for the distance heuristic is the costto-go: $c = \textstyle \sum _ { t } \| u _ { t } ^ { i } \| _ { 2 }$ summing from the time of the current state until the end of the trajectory.

For both networks, we use the mean squared loss function on the target:

$$
\mathcal {L} = \| f (x) - y \| _ {2} ^ {2},\tag{14}
$$

where $y$ is the learning target (either action from global planner or cost-to-go), and $f$ is our networks (either $\mathcal { H } _ { s } \ \mathrm { o r } \ \mathcal { H } _ { d } )$

Learning Implementation Details: We implement our algorithm in Python with Pytorch and our heuristics are constructed according to (12). Both heuristics have the same number of parameters, except in the final layer where the steer outputs a 2 dimensional control vector and the distance outputs a scalar value. The $\rho \Omega$ and $\rho _ { V }$ networks have an input layer with 2 neurons, one hidden layer with 64 neurons, and an output layer with 16 neurons. The $\rho \Omega$ and $\rho _ { V }$ networks have 16 neurons in their input and output layers and one hidden layer with 64 neurons. The Ψ network has an input layer with 34 neurons, one hidden layer with 64 neurons, and output layer with either one (for distance) or two (for steer) neurons. All networks use a fully connected feedforward structure with the ReLU activation function. We train our steer and distance heuristics with 3 and 5 million datapoints respectively, an initial learning rate of 0.001 with the PyTorch optimizer ReduceLROnPlateau function, a batch size of 32000, and train for 300 epochs.