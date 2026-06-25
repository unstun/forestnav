---
citation_key: Luo2023Reinforcement
arxiv_id: 2306.06754
arxiv_url: "https://arxiv.org/abs/2306.06754"
title: "Reinforcement Learning in Robotic Motion Planning by Combined Experience-based Planning and Self-Imitation Learning"
authors_short: "Sha Luo et al."
year: 2023
direction_tag: N_path_repair
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:29:40Z
origin: ai+web
reviewed: false
---

# Reinforcement Learning in Robotic Motion Planning by Combined Experience-based Planning and Self-Imitation Learning

Sha Luo<sup>a,∗</sup>, Lambert Schomaker<sup>a</sup>

<sup>a</sup>University of Groningen, Nijenborgh 9, Groningen, 9747 AG, The Netherlands

## Abstract

High-quality and representative data is essential for both Imitation Learning (IL)- and Reinforcement Learning (RL)-based motion planning tasks. For real robots, it is challenging to collect enough qualified data either as demonstrations for IL or experiences for RL due to safety consideration in environments with obstacles. We target this challenge by proposing the selfimitation learning by planning plus (SILP+) algorithm, which eficiently embeds experience-based planning into the learning architecture to mitigate the data-collection problem. The planner generates demonstrations based on successfully visited states from the current RL policy, and the policy improves by learning from these demonstrations. In this way, we relieve the demand for human expert operators to collect demonstrations required by IL and improve the RL performance as well. Various experimental results shows that SILP+ achieves better training eficiency, higher and more stable success rate in complex motion planning tasks compared to several other methods. Extensive tests on physical robots illustrate the efectiveness of SILP+ in a physical setting.

Keywords: self-imitation learning, reinforcement learning, robotics, motion planning, obstacle avoidance

## 1. Introduction

Motion planning is a fundamental module employed in many robotic platforms [1, 2, 3, 4, 5, 6]. For manipulators, sampling-based motion planning (SBMP) methods, including Rapidly-exploring Random Tree (RRT) [7], Probabilistic Roadmap (PRM) [8], are widely used in recent decades. These methods can be easily implemented on robots with high-dimensional degrees of freedom (DoF) as they approximate the collision-free space by sampling, instead of depending on the explicit geometry modeling of the collision and collision-free configuration spaces. In addition, they are probabilistically complete. However, the main disadvantage of SBMP is the slow adaptability in dynamic environments. In traditional trajectory planning, the assumption is that all necessary task-space information is available at the start of planning and that the world does not change when movement starts. Driven by the growing demand for intelligent autonomous robots that react instantly in changing environments, there is an increasing interest in neural motion planners (NMPs) [9, 10, 11] which approximate the planners with neural networks, such as imitation learning (IL) and reinforcement learning (RL). Instead of relying on a precise pre-planned path, such systems can use a more general policy for dealing with, e.g., unexpected obstacles, in order to adapt motion control, online.

Data collection is the primary barrier for training NMPs in high-DoF manipulation tasks due to the requirement of massive, diverse data in neuralbased IL and RL. However, for IL, the main challenge is the lack of representative data near the boundary of obstacles when the objective is to learn obstacles-avoiding behaviors [9]. For RL, exploring regions around obstacles to collect training data is unsafe and impractical in the real world. When there is inadequate or unbalanced data, it takes a long time for RL algorithms to gather enough informative experience for training the policy such that the algorithms perform well in a dynamic environment. The combination of IL and RL can potentially boost the performance in IL due to the improved exploration and it can accelerate the convergence in RL with the exploitation of ”expert” knowledge. However, a heavy data-preparation process still needs to be realized to bootstrap the approach. This can be realized using non-human examples from a simulated planner [12], via demonstrations by a human user [13, 14, 15] or by gathering data in parallel from multiple robots [16] in an ensemble.

Considering the advantages and disadvantages of traditional and learningbased motion planning algorithms, we explore the integration of planning and learning in motion planning tasks to tackle the data collection problem. On the learning side, RL makes decisions on selecting the next move in order to reach the goal configuration. As we know, RL is a process that balances exploration and exploitation. However, most experiences in the early training stage are not being exploited eficiently when they are not involved in successful trials. Still, such experiences could facilitate the obstacle-avoiding behaviors with collision-free biases. Therefore, we regard these episode-explored states as candidate collision-free nodes for the graph-based motion planning algorithms. In this work, we use a PRM-based method for supportive, online demonstration generation during training. By planning on the candidate collision-free nodes, this method generates up-to-date demonstrations, episode by episode, and saves them in the demonstration experience replay bufer. Since the demonstrations are generated based on the experience from the RL policy, we regard the planning module as a form of experience-based planning. We exploit those demonstrations for imitation learning, which is similar to the idea of learning from good past experiences. We categorize this method as a self-imitation learning algorithm and call it self-imitation learning by planning. The self-imitation learning scheme guides the RL to learn from demonstrations automatically and continuously without requiring a human expert for laborious data collection.

In this paper, we propose a new algorithm, called SILP+, which is an enhanced version of SILP [17]. Compared to SILP, SILP+:

1) proposes a Gaussian-process-guided exploration method to reduce undesirable collisions near obstacles. The reduced number of collisions improves the safety during exploration process and reduces the training time by 18%. The importance and details are explained in section 3.5, and experimental results can be check in section 4.4.

2) analyzes the extrapolation error in actor-critic neural networks and proposes a reward-based filter to stabilize the training process and helps increase the success rate. Motivations and diferences are explained section 3.4, and the experimental results can be check in section 4.5.

3) provides detailed and extensive analysis on diferent methods of dealing with collision failures during training. We discover that the RL agent learns better with positive feedback, but negative experience also helps. Details and discussions can refer to section 4.3.

Besides, we tested SILP+ in a pick-and-place task with the physical UR5e platform. The experimental results verify the robustness and adaptability of SILP+ in noisy and uncertain environments.

Although the current study mainly focuses on motion-planning tasks for manipulators, the empirical findings and analysis are of interest to the general study of motion planning and reinforcement learning due to the following reasons: First, SILP+ presented here is an algorithm that combines planning and learning to improve the performance of motion planning. It represents a new way of utilizing the advantages of planning in a learning scheme, while avoiding a high computation load; Second, the empirical results, the analysis of the collision failures and the analysis of the extrapolation error in actorcritic networks provide helpful inspiration for designing high-performance RL architectures for motion-planning tasks.

The remainder of this paper is organized as follows. Section 2 introduces the background and related work about neural motion planners and learning from demonstration, followed by the proposed methodology SILP+ in Section 3. In Section 4, experiments are conducted in both simulations and on the physical robot arm UR5e to analyze the eficiency and feasibility of the proposed SILP+ in motion planning tasks. Section 5 draws conclusions and envisions future work.

## 2. Related Work

## 2.1. Neural motion planning

Methods using neural networks to assist or approximate motion planners have attracted increasing attention because of recent advances in deep learning and the demand for adaptable motion planners in changing environments. Recent work includes biasing sampling to critic regions with machine learning techniques. For example, Zhang et al. [18] employed RL to learn the probability of rejecting a sampled state in order to bias the sampling to the less dangerous regions. Ichter et al. [19] predicted sampling nodes in critic regions on top of traditional SBMP methods using a conditional variational autoencoder. Francis et al. [20] proposed PRM-RL for longrange navigation, in which RL functions as a short-range local planner and also a collision-prediction module for the high-level PRM planner. A similar framework can be seen in [21] which uses a regular global planner (RRT or A\*) and an RL policy optimization method as the local planner. Besides, there are pure neural motion planners that approximate the motion planners with neural networks, mapping states directly to paths or actions. Qureshi et al. [10] proposed MPNet as the neural motion planner, and the MPNet showed less planning time compared with traditional motion planners. Jurgenson et al. [9] adapted DDPG and learned collision and reward models for visual motion planning tasks, which improved the accuracy and planning time compared with SBMP methods. The combination of planning with RL has also been investigated. Benjamin et al. [22] proposed a hierarchical framework for long-horizon reaching tasks: planning at the high level to find the subgoals in the replay bufer and learning at the low level to control the robot to reach the subgoals. It demonstrated how eficient it was when planning was embedded with learning. However, they focused on 2D reaching tasks; no obstacles existed in the environment and they planned on the whole replay bufer, which may involve heavy computation in a more complex task. Diferently, Xia et al. [23] used a SBMP planner at the low level, planning from the current state to subgoals and training the of-policy RL algorithm at the high level for subgoals generation.

## 2.2. Learning from Demonstrations

Learning a task from scratch without prior knowledge is a daunting process; even human beings and animals rarely try to learn from scratch [24]. They utilize previous experiences and demonstrations from instructors to derive strategies to approach a learning problem, which is called learning from demonstrations (LfD) or IL. LfD is widely used in learning-based robotic tasks, including helicopter maneuvering [25] [26], mobile robot navigation [27][28], surgery [29][30], manipulation [31] [32]. However, there are also limitations in LfD caused by sparse or poor datasets. Firstly, the controlling error will accumulate in behavior cloning when the agents encounter unfamiliar and unseen states in the demonstrations. Secondly, the policy’s performance depends heavily on the demonstrations’ quality; the agent cannot perform better than the supervisor without additional information to help improve. [33] [34].

One of the solutions is the combination of RL and LfD, called reinforcement learning from demonstrations (RLfD) [35] [36], which exploits the strengths of both sides and overcomes their shortcomings. The demonstrations are used to guide and improve RL policies, and then the RL provides feedback on the actions via the reward function and explores better policy than that of the supervisor [37, 38, 31] by exploration. Our SILP+ is similar to the work presented in [31], where demonstrations were stored in a demonstration replay bufer and embedded in an auxiliary behavior cloning loss to guide the learning. We modify the LfD framework by adding a planning module for demonstration generation, and these demonstrations are utilized for further self-imitation learning. Similar to SILP+, DAgger in [39] also adopts the idea of online supervision, which gives on-time evaluation feedback for the encountered states by relabelling actions. However, unlike DAgger, which retrieves expert guidance on every singe step, SILP+ plans on all states experienced within an episode, and therefore, it discovers the core steps in the episode through the global knowledge.

## 2.3. Self-Imitation Learning

The main idea of Self-Imitation Learning (SIL) [40] is to improve the sample eficiency in RL by utilizing good decisions in the past. However, the quality of the method depends heavily on the RL exploration strategies. It is dificult for the RL policy to obtain informative steps without direct supervision in complex robotic tasks. Besides, SIL was initially designed for the on-policy discrete settings, which is not straightforward to be used in ofpolicy, continuous action scenarios. Recent work [41] targeted at the robotics applications with continuous action space and proposed ESIL that combined hindsight with SIL such that the agent learned from good experience selected by Hindsight Experience Replay (HER) [42]. The major diference between ESIL and SILP+ is how they create good experiences. ESIL changed the goal based on HER to transform useless experience to positive feedback, while SILP+ uses rigid planners to convert ordinary trajectories into optimized successful paths. Therefore, SILP+ collects higher-quality experiences for SIL to learn.

## 2.4. Leveraging Prior Experience

SILP+ can also be categorized as a data augmentation method, manipulating previous experience for better training. In this category, Weber et al. [43] learned the policy with data from imaginations, in which part of the training data was aggregated by rolling out the policy. The widely known HER [42] is also a method of utilizing prior experience. It generates informative data by regarding the experienced next state as the goal. However, the amount of useless data increases as more successful experiences are gained in HER, and thus impairs the sample eficiency. Nevertheless, Our method can select the most promising state as the next state, and those selected states in the episode could form a successful path to provide more informative data for RL training.

## 3. Methodology

The combination of RL and LfD has been used to tackle the problem of sample eficiency in RL. It is straightforward and eficient, but the preparation of expert demonstrations might not be easy in many situations. Therefore, a more practical approach is learning by utilizing the agent’s informative experiences. In the context of RL, SIL is a technique that takes advantage of this idea and encourages the agent to learn from actions with higher rewards. However, this technique was proposed for discrete control tasks and faced the problem of lacking informative, positive experiences in high-dimensional continuous tasks, such as robotics motion control.

Our SILP+ is a combination of the concepts of SIL and experience-based planning. Experience-based planning ensures qualified guidance by providing direct corrections on visited states using planning methods, while SIL guides the policy learning with good examples from the planning module. This section first formulates the motion planning task in an RL scheme, followed by the explanation of experience-based planning with PRM. Then, we introduce SIL in continuous control tasks and illustrate how planning is embedded with SIL to formulate SILP+. In addition, we propose a Gaussian-processguided exploration method near collision regions to improve the exploration eficiency. Finally, a model-based reward filter is employed to reduce the extrapolation error in actor-critic RL.

## 3.1. RL for Motion Planning

We formulate our motion planning task as follows. Let W represent the world space. The set of obstacles in the world space is denoted by O. The configuration space (i.e., the C-space) is denoted by C, in which a configuration of the robot is denoted by $q \in \mathcal { C }$ . The forward kinematics $\mathcal { F K } : \mathcal { C }  \mathcal { W }$ maps the robot configuration in C to the world space W. If $\mathcal F \mathcal K ( q )$ in W belongs to the obstacle set O, then q is in the collision configuration space $\mathcal { C } _ { o b s }$ . The collision-free configuration space then is defined by: $\mathcal { C } _ { f r e e } = \mathcal { C } \backslash \mathcal { C } _ { o b s }$ Given the collision-free starting configuration $q _ { 0 } \in \mathcal { C } _ { f r e e }$ and the goal configuration $q _ { g } \in \mathcal { C } _ { f r e e }$ , the motion planning task is to find a path that starts from $q _ { 0 }$ and ends at $q _ { g }$ , while avoiding the collision configuration space $\mathcal { C } _ { o b s } .$ This task can be formulated as a Markov Decision Process (MDP), which can be solved in the reinforcement learning framework.

We embed our motion planning task in an episodic of-policy RL framework, in which the environment and task are randomly sampled within the workspace at each episode [44]. The goal of the agent is to maximize the expected accumulated future returned reward $R _ { t } = \mathbb { E } [ \sum _ { i = t } ^ { \infty } \gamma ^ { i - t } r _ { i + 1 } ]$ from the current step t with a discounted factor $\gamma ~ \in ~ [ 0 , 1 ]$ weighting the future importance. Each policy π has a corresponding action-value function $Q ^ { \pi } ( s , a ) = \mathbb { E } [ R _ { t } | s _ { t } = s , a _ { t } = a ]$ , representing the expected return under policy π after taking action a in state s. Following policy $\pi , Q ^ { \pi }$ can be computed by the Bellman equation:

$$
Q ^ {\pi} (s _ {t}, a _ {t}) = \mathbb {E} _ {s _ {t + 1} \sim p} [ r (s _ {t}, a _ {t}) + \gamma \mathbb {E} _ {a _ {t + 1} \in A} [ Q ^ {\pi} (s _ {t + 1}, a _ {t + 1}) ] ],\tag{1}
$$

where A represents the action space and $p$ is the state distribution. Let $Q ^ { * } ( s , a )$ be the optimal action-value function. RL algorithms aim to find an optimal policy $\pi ^ { * }$ such that $Q ^ { \pi ^ { * } } ( s , a ) \ : = \ : Q ^ { * } ( s , a )$ for all states and actions. The learned policy should predict the action at every step, guiding the manipulator to reach the goal while avoiding collisions. The detailed formulation is described below.

• States: A feature vector is used to describe the continuous state, including the robot’s proprioception, the obstacle and goal information in the environment. We restrict the orientation of the gripper as orthogonal and downward to the table, so three joints out of six in our UR5e platform are active in the learning process. At each step t we record the i-th joint angles $j _ { i }$ for $i = { 1 , 2 , 3 }$ in radians and the end-efector’s position $( x ^ { e e } , y ^ { e e } , z ^ { e e } ) \in \mathbb { R } ^ { 3 }$ as the proprioception: proprio $= ( j _ { 1 } , j _ { 2 } , j _ { 3 } , x ^ { e e } , y ^ { e e } , z ^ { e e } ) \in \mathbb { R } ^ { 6 }$ . Then, we estimate the obstacle’s position in task space and use a bounding box to describe it: obs $= ( x _ { m i n } ^ { o } , x _ { m a x } ^ { o } , y _ { m i n } ^ { o } , y _ { m a x } ^ { o } , z _ { m i n } ^ { o } , z _ { m a x } ^ { o } ) \in \mathbb { R } ^ { 6 }$ . The goal is described as a point in the task space: goa $\mathsf { l } = ( x ^ { g } , y ^ { g } , z ^ { g } ) \in \mathbb { R } ^ { 3 }$ . Finally, the state feature vector can be represented as: $s = ( \mathrm { p r o p r i o } , \mathrm { o b s } , \mathrm { g o a l } ) \in \mathbb { R } ^ { 1 5 }$

• Actions: Each action is denoted by a vector $a \in ( [ - 1 , 1 ] ) ^ { 3 }$ , which represents the relative position change for the first three joints. The corresponding three joint angle changes are 0.125a rads.

• Rewards: A success is reached if the Euclidean distance between the end-efector and the goal $\mathrm { d i s } ( \mathrm { e e } , g ) < \mathrm { e r r }$ , where err controls the reach accuracy. Given the current state and the taken action, if the next state is not collision-free, then a severe punishment is given by a negative reward $r = - 1 0$ . If the next state results in a success, we encourage such a behavior by setting the reward $r = 1$ . In other cases, $r = - \mathrm { d i s } ( \mathrm { e e } , g )$ to penalize a long traveling distance. An episode is terminated when the predefined maximum steps or a success is reached.

Since the goal and obstacles are static in each episode, the state transition function $f _ { s }$ is defined by $\mathcal { F } \mathcal { K }$ . Given the state $s _ { i }$ and action $a _ { i } .$ , the next state $s _ { i + 1 }$ can be calculated by the function $f _ { s }$ under the position controller: $s _ { i + 1 } = f _ { s } ( s _ { i } , a _ { i } )$ . We make a natural assumption that the goal states are reachable.

Since the transition function is known, our of-policy reinforcement learning framework can also be regarded as model-based. However, unlike traditional model-based RL directly involving the model in policy optimization and decision-making, we mainly use the model to generate demonstrations to facilitate our “model-free” RL agent learning better from its own experience. Besides, most of the model-based RL heavily depends on the model accuracy to avoid suboptimal performance, our method focuses more on the model-free exploration process. Thus, we have a lighter dependence on the model accuracy. The model we used is mainly for demonstration generation, and the self-imitation learning module helps the robot learn only from good experiences.

## 3.2. Experience-based Planning with PRM

In motion planning, in order to respond to new requests eficiently, past solutions are stored in memory and can be retrieved and repaired for later usage to speed up the planning process. This strategy is called experience-based planning [5, 45, 46], where the experiences represent the previous solutions. However, in the context of RL, experiences refer to the past discrete decisions in the Markov Decision Process. It describes how the policy acts on a specific state and what the next state is under this action. Although most of these experiences are not part of the solutions, especially in the beginning exploration process, they still provide information to help understand the environment and the task. In this study, we generate demonstrations for SIL by planning on these experiences from the current policy.

Many graph-search-based planning approaches can be used in our SILP+ to plan paths; here, we propose a PRM-based path planning as the planner. PRM is a multi-query SBMP algorithm, which exploits the fact that in SBMP, it is cheap to check whether a single robot configuration is in free space or not. The roadmap contains nodes and edges, in which a node represents a specific location, and an edge corresponds to a path connecting two nodes. After the roadmap has been generated, planning queries can be answered by connecting the user-defined initial and goal configurations.

The basic PRM is designed for static path planning applications, and it can realize multi-query path planning by constructing a global roadmap. In our environment, the location of the obstacle is randomly selected within a defined workspace in each episode, making the basic PRM ineficient, as the roadmap needs to be constructed in every episode. Hence, we build a directed graph on the set of visited collision-free states denoted by $ { \boldsymbol { S } } _ { f }$ in each episode. Each node in $ { \boldsymbol { S } } _ { f }$ corresponds to a state in MDP. These states are already collision-checked as they are selected from the RL experience; therefore, the nodes collision-checking process can be omitted and the eficiency of the algorithm has thus been improved. We denote the edge between nodes $s _ { i }$ and $s _ { j }$ as $e _ { s _ { i } \to s _ { j } }$ . Edges which have lengths greater than d or intersect with obstacles are ignored. Finally, the graph $\mathcal { G }$ is formulated as follows:

$$
\mathcal {E} = \left\{ \begin{array}{l l} \emptyset & \text {if} d (s _ {i}, s _ {j}) > d \text {or} e _ {s _ {i} \to s _ {j}} \in \mathcal {C} _ {o}, \\ \{e _ {s _ {i} \to s _ {j}} \mid s _ {i}, s _ {j} \in \mathcal {S} _ {f} \} & \text {otherwise}, \end{array} \right.\tag{2}
$$

where $\mathcal { V } \in S _ { f }$ and E represent the nodes and edges in the graph, respectively, and $\scriptstyle { \mathcal { C } } _ { o }$ represents the edge collision space. We use A-star as the local planner to extract paths in each episode, in which the end efector’s positions in states are used to calculate the heuristic function. The adapted PRM-based path planning algorithm is illustrated in Fig. 1 and explained as follows:

1. Collision-free nodes construction: Instead of randomly generating configurations in the workspace and selecting collision-free ones as the candidate nodes, we directly select the collision-free states from the experiences as candidate nodes and each node corresponds to a state in the MDP. The selected nodes are shown in Fig. 1(1). This step is also explained in Alg. 1.

2. Start and goal configurations sampling: In the RL training process, the real goal probably cannot be reached, especially at the beginning of the training. Therefore, we randomly select N start and goal pairs from the filtered collision-free nodes $ { \boldsymbol { S } } _ { f }$ . Here, for the purpose of illustration, we use N = 1 and illustrate the start and goal nodes in Fig. 1(2). Then, we set the start node as the current node $s _ { i }$ and append it to the candidate path nodes $\nu _ { e }$

3. Candidate neighbors selection: To determine the candidate neighbors of node $s _ { i } ,$ we use the Euclidean distance as the metric to choose all the nodes not in $\nu _ { e }$ of which the distances to $s _ { i }$ are less than $d ,$ such as the nodes $n _ { 1 } , n _ { 2 } , n _ { 3 }$ in Fig. 1(3). The selection of the distance d is explained in Appendix A. We put them into a neighbors set. If no neighbors exist, we stop the planning process and continue with RL learning.

4. Collision-checking on edges: We check the edges between $s _ { i }$ and the candidate neighbors using our collision checking module, which is explained in Appendix B. Candidate neighbors with collision edges are removed. As shown in Fig. 1(4), the edge between $s _ { i }$ and $n _ { 3 }$ intersects with the obstacle and thus is removed from the neighbor set. The method for edge collision-checking is based on subdivision, in which the intermediate linear interpolations of configurations are sampled based on step size. The edge between two nodes is collision-free if all of the intermediate configurations are checked collision-free.

5. The local planner with A-star : We compute the cost of each candidate

![](Luo2023Reinforcement_figs/e104161a2f067ae6a25b54b1b1449c822668f402fe41d1ac9e165c6c1bd7c72e.jpg)  
Figure 1: PRM-based path planning: (1) collision-free nodes construction. (2) start and goal configurations sampling. (3) candidate neighbors selection. (4) collision-checking on edges. (5) the local planner with A-star. (6) select the next node.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Collision-free nodes construction
1 Input: on-training policy π, environment env; empty Collision-free nodes $S_f = \emptyset$;
2 Output: Collision-free nodes in $S_f$, experience {S, A, S', R, Done};
3 S, A, S', R, Done = [ ];
4 s = env.reset;
5 while episode not end do
6    a = π(s)
7    s', r, done, collision = env.step(a)
8    while collision do
9    a = random action
10    s', r, done, collision = env.step(a)
11    S.append(s); A.append(a); S'.append(s')
12    R.append(r); Done.append(done)
13    $S_f \leftarrow S_f \cup \{s'\}$
14    s = s'
</div>

neighbor in the task space using heuristic functions. The cost of a candidate neighbor nn is defined as: $f ( n n ) = h ( n n ) + g ( n n )$ , where functions $h$ and $g$ are the cost from $s _ { i }$ to nn and that from nn to the goal, respectively. Both functions use Euclidean distance as the cost value.

6. Select the next node: The node with the least cost will be selected as the next start node, as shown in Fig. 1(6) and be appended to the candidate path nodes $\nu _ { e }$ . The edge that connects the current node and the next node will be further processed when converting the path node $\nu _ { e }$ into demonstrations. Starting from the current node and repeating steps (3) to (6), the algorithm terminates when the final goal has been reached, the maximal running time has been used or no available neighbors can be found.

## 3.3. Online Generation of Demonstrations

In order to learn from demonstrations with RL, we need to convert the path node $V _ { e } = \{ s _ { 0 } , . . . , s _ { n } \}$ to MDP format for further imitation learning. Before proceeding, we make the following assumptions: (1) the forward kinematics function $f _ { s }$ is given and based on $f _ { s }$ , the end efector’s position is predictable using the robot’s joint values. (2) the inverse model $f _ { a }$ is given so that the action $a _ { i } = f _ { a } ( s _ { i } , s _ { i + 1 } )$ that controls the agent from one state to another state is accessible. Then, we illustrate the pseudo-code for online demonstrations generation in Alg. 2, in which the objective is to convert the state-based nodes $V _ { e }$ to $( s , a , s ^ { \prime } , r , d o n e )$ tuples and save them in a demonstration replay bufer $D _ { d e m o }$ . The conversion iterates the successive nodes s and $s ^ { \prime }$ and calculates the action a using the inverse model $f _ { a }$ . Based on $( s , a , s ^ { \prime } )$ R the reward r and the Boolean value done can be calculated. However, the predicted action may be out of the action space $A .$ . In this case, we insert an extra node between the states with a half value of $^ { a , }$ and the new next state is calculated by $f _ { s }$ . This process is repeated until the action is within action space A. We save the constructed demonstrations in $D _ { d e m o }$ for policy learning.

![](Luo2023Reinforcement_figs/fe517372dcfcef00e5048476634572424fe41281922b98f20e642b33dd851e34.jpg)  
Figure 2: Self-imitation learning by planning plus

The overall structure of SILP+ is depicted in Fig. 2. At the end of each training episode, we obtain the visited states, as shown in the left subfigure. These experiences are stored in the interaction experience replay bufer. Based on the visited states, we plan paths using PRM-based planner, and the result is shown as the directed-dotted lines in the right sub-figure. Then, these paths are converted as demonstration tuples saved in the demonstration replay bufer for further imitation learning.

## 3.4. Self-Imitation Learning

Self-imitation learning is an RL method that encourages actions whose returns were higher than the expectation [40]. It was proven to be able to improve the performance of actor-critic methods in several discrete control tasks. One of the challenges in SIL is the dificulty to perform the task if the exploration performs poorly. For instance, a random exploration never generates a good experience within a reasonable time. Therefore, the policy cannot benefit from imitating the good experience when there is no good experience. To this end, we propose to combine the SIL with experience-based planning, called $\mathrm { S I L P + }$ , in the context of motion planning. The planning module provides the demonstrations based on the visited experience, while SIL pushes the policy update toward the demonstrations.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Demonstrations Generation in SILP+
1 Input: Planned nodes $V_e = \{s_0, s_1, ..., s_n\}$ in episode e; environment env; action space A; action model function $f_a$ and forward kinematics function $f_s$;
2 Output: Updated demonstration replay buffer $D_{demo}$;
3 Demonstrations Generation:
4 for i in LENGTH($V_e$) do
5    $s = V_e[i]$ ;
6    $s' = V_e[i + 1]$ ;
7    $a = f_a(s, s')$ ;
8    while $a \notin A$ do
9    $(s'', a') = \text{INSERTNODES}(s, s', a)$ ;
10    $r' = \text{env.REWARD}(s, s'')$ ;
11    $D_{demo}.PUSH((s, a', s'', r'))$ ;
12    $s = s''$ ;
13    $a = f_a(s'', s')$ ;
14    $r = \text{env.REWARD}(s, s')$ ;
15    $D_{demo}.PUSH((s, a, s', r))$
16 Function InsertNodes($s, s', a$):
17    $a = a/2$ ;
18    $s' = f_s(s, a)$ ;
19    while $a \notin A$ do
20    $(s', a) = \text{INSERTNODES}(s, s', a)$
21    return $s', a$;
</div>

The method of embedding demonstration into SIL is adapted from [31], where demonstrations are stored in a separate replay bufer $D _ { d e m o }$ , along with an interaction experience replay bufer $D _ { \pi }$ that contains the interaction experiences. At each training step, we update the policy with $N _ { D }$ and $N _ { \pi }$ examples sampled from $D _ { d e m o }$ and $D _ { \pi }$ , respectively. The guidance from demonstrations is implemented with a behavior cloning loss as shown below:

$$
L _ {b c} = \sum_ {i = 1} ^ {N _ {D}} \left\| \pi (s _ {i} | \theta^ {\pi}) - a _ {i} \right\| ^ {2},\tag{3}
$$

where $a _ { i }$ and $s _ { i }$ are the action and state sampled from bufer $D _ { d e m o }$ . The $\theta ^ { \pi }$ represents the learning parameters in the policy. The policy imitates the good choices from the demonstrations by adding the behavior cloning loss to the objective J, which is weighted with hyperparameters $\lambda _ { 1 }$ and $\lambda _ { 2 }$ , as shown below:

$$
\lambda_ {1} \nabla_ {\theta_ {\pi}} J - \lambda_ {2} \nabla_ {\theta_ {\pi}} L _ {b c},\tag{4}
$$

In order to avoid learning from imperfect demonstrations, a $Q _ { f i l t e r }$ is employed in SILP [17] to prevent adding behavior cloning loss when the policy’s action is better than the action from the demonstrations. However, experience replay bufer-based of-policy RL methods, such as DDPG and SAC, prone to the extrapolation error in Q function approximation. They struggle to learn when the data is diferent from the current policy’s data distribution. For example, when updating the target Q values in DDPG and SAC, the next state $s ^ { \prime }$ and action $a ^ { \prime }$ from the target policy are involved. It risks to obtain unreliable Q value estimations as these state-action pairs are likely to be unfamiliar to the policy and not existed in the replay bufer. Fujimoto et al. [47] demonstrated that the actor-critic algorithms deteriorate when the data is uncorrelated, and the value estimation produced by the Q-network diverges. With these considerations, Q filter used in [31] could introduce the extrapolation error and lead to an incorrect filter for the action gap-guided RL training.

Since we use planning as the source of demonstrations, it is natural to utilize models to form a more reliable Q filter. To this end, we replace the Q filter with a predicted reward filter, in which instead of comparing the state-action values between the policy and demonstrations, we predict the rewards $f _ { r }$ based on the actions from the policy and demonstrations. The objective in (4) is changed to:

$$
\lambda_ {1} \nabla_ {\theta_ {\pi}} J - \lambda_ {2} R _ {f i l t e r} \nabla_ {\theta_ {\pi}} L _ {b c},\tag{5}
$$

where

$$
R _ {f i l t e r} = \left\{ \begin{array}{l l} 1 & \text { if } \quad R (s _ {i}, a _ {i}) > R (s _ {i}, \pi (s _ {i})), \\ 0 & \text { otherwise }. \end{array} \right.\tag{6}
$$

where

$$
R (s _ {i}, a _ {i}) = r _ {i} + \gamma f _ {r} (s _ {i + 1}, \pi (s _ {i + 1})) + \gamma^ {2} f _ {r} (s _ {i + 2}, \pi (s _ {i + 2})) + \dots + \gamma^ {k} f _ {r} (s _ {i + k}, \pi (s _ {i + k})),\tag{7}
$$

and $( s _ { i } , a _ { i } , s _ { i + 1 } , r _ { i } )$ is one of the MDP tuple batches in $D _ { d e m o }$ . For computing $R ( s _ { i } , \pi ( s _ { i } ) )$ in (6), we use (7) with $r _ { i }$ being replaced with $f _ { r } ( s _ { i } , \pi ( s _ { i } ) )$ . Correspondingly, next state $s _ { i + k }$ should be predicted based on $f _ { s }$ . While larger values of k can potentially yield better performance [48] by capturing longer-term dependencies, they often require more time during training due to the increased number of time steps to be considered. Given the complexity of our problem domain and the objectives of our study, we opted for the one-step return $k = 1$ to strike a balance between performance and training eficiency. However, it is straightforward to use $k > 1$

![](Luo2023Reinforcement_figs/1b1b6d43eed86e03f4065e6ee6d43f29e0419abf66ade6363188c3401572b26d.jpg)

![](Luo2023Reinforcement_figs/f7535e801e63ccae434ee3d7f437d0e6e4de06c3358a3cb166e30981b3a3b203.jpg)

![](Luo2023Reinforcement_figs/77cdc7022575a50a21ce6a271af03f6f8c32d4069d9c983236d76d531347e03e.jpg)  
Figure 3: An example of modeling the reward function with a Gaussian process in three views on the 3D joint space: The green points represent visited collision-free nodes and the black, crossed points represent the collision nodes. Diferent color levels represent the modeled reward values which increase from red (penalty) to blue (high reward). The units of the axes coordinates are radians. The modeled reward distribution can guide the RL policy to explore regions with higher rewards. Please note that the positions of the points are based on a 2D projection from the 3D joint space.

## 3.5. Gaussian Process-Guided Exploration

In SILP [17], when a collision happens during training, the agent would go one step back to the before-collision state and randomly select another action to continue. Under this strategy, we observed a scenario that the policy is likely to get stuck on selecting random collision-free actions near the obstacles until running out of the steps. This issue is due to the limitation of random sampling, which need to take an impractical amount of samples to cover the whole space. Therefore, the agent is easy to run out of the pre-defined steps before it encounters a valid action. To tackle this problem, we propose Gaussian-process-guided exploration to improve the exploration quality near the collision regions. The main idea is to model the reward landscape based on the collected experiences when the collision happens and select the action with the most promising reward.

We use the Gaussian process regression to approximate the function $f _ { m }$ which maps from the experienced states to rewards. First, we assume $f _ { m }$ is distributed as a Gaussian process: $f _ { m } \sim \mathcal { G P } ( 0 , k ( x , x ^ { \prime } ) )$ , with zero prior mean and the covariance function $k : \mathcal { X } \times \mathcal { X } \to \mathbb { R }$ . The output $y ( x )$ of the function $f _ { m }$ at input x can be written as $y ( x ) = f _ { m } ( x ) + \epsilon$ , with the Gaussian noise $\epsilon \sim \mathcal { N } ( \epsilon ; 0 , \sigma _ { n o } ^ { 2 } )$ . After having collected n observations, denoted by $D _ { n } = \{ { \pmb x } _ { n } , { \pmb y } _ { n } \} = \{ x _ { 1 } , . . . , x _ { n } , y _ { 1 } , . . . , y _ { n } \}$ , the predictive distribution at location x is given by

$$
p (f _ {m} \mid \mathcal {D} _ {n}, x) = \mathcal {N} (f _ {m} (x); \mu (x \mid \mathcal {D} _ {n}), \sigma^ {2} (x \mid \mathcal {D} _ {n})),
$$

with the predictive mean $\mu ( x \mid \mathcal { D } _ { n } ) = \pmb { k } _ { n } ^ { T } ( x ) [ K _ { n } + \sigma _ { n o } ^ { 2 } I ] ^ { - 1 } \pmb { y } _ { n }$ and the predictive variance $\sigma ^ { 2 } ( x \mid \mathcal { D } ) = k ( x , x ) - \pmb { k } _ { n } ^ { T } ( x ) [ K _ { n } + \sigma _ { n o } ^ { 2 } I ] ^ { - 1 } \pmb { k } _ { n } ( x ) \ [ 4 9 ]$ , where the entries of the vector $\pmb { k } _ { n } ( x ) \in \mathbb { R } ^ { n }$ are $[ \pmb { k } _ { n } ( x ) ] _ { i } = k ( x _ { i } , x )$ , the entries of the Gram matrix $K _ { n } \in \mathbb { R } ^ { n \times n }$ are $[ K _ { n } ] _ { i , j } = k ( x _ { i } , x _ { j } )$ , and the entries of the vector of observations $\ b { y } _ { n } \in \mathbb { R } ^ { n }$ are $[ { \pmb y } _ { n } ] _ { i } = y _ { i }$ . When there is a collision during training, we collect all of the states and rewards in the episode and fit the states and rewards as the input and output in $f _ { m }$ . Then we use the Monte Carlo planning to select the intended action: first, n random state configurations are sampled; then, the rewards are predicted for these configurations using the learned model $f _ { m } ;$ later, we scale the reward into a sampling probability within [0, 1] and make sure that the sum of those probabilities is 1; finally, we choose one of those configurations under the scaled probabilities as our desired next state and retrieve the corresponding action. The kernel in Gaussian process regression we used is: Matern $5 / 2 \ [ 5 0 ]$ . We depicted an example of fitted reward distributions in Fig. 3. From the figure, we can see that the experienced collision regions have lower rewards expectation and there are small probabilities to choose the next action in the vicinity of these regions.

## 4. Experiments

We conducted experiments in both simulations and real robot settings to answer the following questions: (1) Under the same environment and task settings, does SILP+ perform better than other baseline algorithms in terms of success rate and sample eficiency? (2) Will SILP+, which additionally includes an online demonstration generation step increases computation burden and leads to a slower training process? (3) How do collisions afect the learning performance? (4) How do the Gaussian-guided exploration and extrapolation errors afect the performance? (5) Can the policy learned in simulation transfers well to a physical robot where noise and uncertainty exist?

## 4.1. Task and Training Setup

We used Gazebo with an ODE physics engine as the simulator for training policies, in which a 6 DoF robot arm UR5e is equipped with a Robotiq-2f-140 gripper to accomplish long horizon motion planning tasks. The workspace for the end-efector is restricted to $x \in [ 0 , 0 . 8 ] \mathrm { m } , y \in [ - 0 . 3 , 0 . 8 ] \mathrm { m } , z \in [ 0 , 0 . 6 ] \mathrm { m }$ to simplify the tasks and avoid unnecessary collisions. A box with the width and height of 0.2m and 0.3m respectively is used as an obstacle in the task. The obstacle’s position (the center of the mass) is limited to $x \in [ 0 . 3 , 0 . 7 ] \mathrm { m }$ 2 $y \in [ 0 . 1 , 0 . 4 ] \mathrm { m } , z = 0 . 1 5 \mathrm { m }$ (see the purple region in Fig. 4a). The initial arm pose and the goal pose were restricted within the reachable workspace of the end-efector, as mentioned before. In order to balance the number of collision and non-collision interactions, we restrict the initial pose, goal pose and obstacle position to satisfy $d _ { 2 } > d _ { 1 } > d _ { 3 }$ , where $d _ { 1 }$ is the Euclidean distance between the initial end-efector’s position and the obstacle’s position, $d _ { 2 }$ is the Euclidean distance between the initial end-efector’s position and the goal position, and $d _ { 3 }$ is the Euclidean distance between the obstacle’s position and the goal position. This means that the robot needs to learn a generalized policy to reach the target from diferent directions while avoiding the obstacle. The relative positions are projected in 2D and depicted in Fig. 4b.

![](Luo2023Reinforcement_figs/f400b70cce94ad17a69bff545e079210253e6fafd390ce00127753384aab6241.jpg)  
(a) Task workspace

![](Luo2023Reinforcement_figs/9974fbda99e2fead19202c42310887b0717dddbd6fb160aa7a205e99a87bc885.jpg)  
(b) Position relationship in initialization  
Figure 4: (a) Task workspace: the transparent region bounded with dashed lines is the reachable workspace of the end efector and the goal; the purple region represents the region for the obstacle; (b) Position relationship in initialization: $d _ { 2 } > d _ { 1 } > d _ { 3 }$

## 4.2. Baseline Comparison

We employed two state-of-the-art of-policy RL algorithms as our basic baselines: deep deterministic policy gradient (DDPG) [51] and soft actorcritic (SAC) [52, 53] to evaluate SILP+. We call them DDPG-SILP+ and SAC-SILP+, respectively. The design of the neural networks and hyperparameters for DDPG and SAC, as well as the training details can be found in [17]. The procedure of SILP+ is described in detail in Section 3.2, above.

We compared the success rate (the number of successful task attempts divided by the total number of attempts) and training time for the following methods:

• DDPG: DDPG combined with a dense reward.

• DDPG-HER: DDPG combined with hindsight experience replay (HER) [42].

• DDPG-Demon: DDPG with experience replay bufer that contains demonstrations from online planning.

• DDPG-SILP+: DDPG combined with SILP+.

• SAC: SAC combined with a dense reward.

• SAC-HER: SAC combined with HER.

• SAC-Demon: SAC with experience replay bufer that contains demonstrations from online planning.

• SAC-SILP: SAC combined with SILP.

• SAC-SILP+: SAC combined with SILP+.

• PRM-0.1: PRM with planning time limited to 0.1 second.

• PRM-1: PRM with planning time limited to 1 second.

• BC-SAC-SILP+: Behavior cloning with demonstrations collected from SAC-SILP+ policy’s rollout.

• BC-PRM: Behavior cloning with demonstrations collected from PRM in Moveit under the planning time threshold of 1 second.

For HER, the number of imagined goals is four for each visited state. The DDPG-Demon and SAC-Demon methods impose demonstrations into the regular experience replay bufer. Similar to SILP+, those demonstrations come from online PRM planning. The diference between SILP+ and Demon is that Demon does not use a behavior cloning loss-based SIL to specifically learn from good experience. Instead, Demon is more of a data argumentation method. PRM-0.1 and PRM-1 were implemented in Moveit under the planning time limitation of 0.1 second and 1 second, respectively. We used 10k demonstrations to train the BC model. The demonstrations in BC-SAC-SILP+ were collected by the well-trained SAC-SILP+ policies, and the demonstrations in BC-PRM were collected by PRM through Moveit with planning time limited to 1 second.

For DDPG- and SAC-based methods, we set the training epoch to 1K. Here, the epoch represents certain iterations of updates in parameters. Each epoch contains ten episodes. The results are summarized in Table 1. The training time means the wall time for the defined 1K epochs, which is summarized from three trained policies with diferent seeds. The final success rates are measured under the three trained policies; each policy being tested 1K times. The planning time is the accumulated time for rolling out the learned policy, which is also summarized from the three trained policies, and each policy has been rolled out 1k times. Note that the PRM methods do not have training time as online planners do. The training time for BC-based methods comprises the data collection and policy training time.

From the success rate column, we observed that SAC-SILP+ achieved the highest success rate (0.973) and the lowest standard variance (0.002) compared with other methods. The success rates in the DDPG spectrum are lower than SAC spectrum methods, but SILP+ can boost DDPG’s performance to the same level of SACs, as we can see from the data in DDPG-SILP+ and SAC-SILP+. In addition, traditional PRM methods performed worse than our SILP+ methods, although the increased planning time could slightly improve the performance. Not surprisingly, BC methods depend heavily on the quality of the expert demonstrations. The demonstrations’ quality in SAC-SILP+ is better than in PRM’s. The reason is that the planned paths in PRM can be partly beyond the workspace or suboptimal because of singularities. As a result, BC with SAC-SILP+ demonstrations and PRM demonstrations achieved success rates of 0.967 and 0.464 respectively under the same test configurations.

Table 1: Success rate, training, and planning time of SILP+ compared with other methods. Results are collected in simulation and averaged: Each method was randomly initialized three times, trained and then tested on 1000 reaching trials.

<table><tr><td>Algorithms</td><td>Success Rate</td><td>Training Time (h:m:s)</td><td>Planning Time (s)</td></tr><tr><td>DDPG</td><td>0.763 (0.046)</td><td>08.17.53 (00.23.26)</td><td>0.110 (0.017)</td></tr><tr><td>DDPG-HER</td><td>0.532 (0.257)</td><td>11.15.01 (03.18.38)</td><td>0.126 (0.024)</td></tr><tr><td>DDPG-Demon</td><td>0.707 (0.039)</td><td>08.07.51 (00.13.21)</td><td>0.107 (0.007)</td></tr><tr><td>DDPG-SILP+</td><td>0.954 (0.021)</td><td>07.35.11 (00.13.50)</td><td>0.114 (0.009)</td></tr><tr><td>SAC</td><td>0.864 (0.066)</td><td>07.15.24 (00.48.00)</td><td>0.116 (0.010)</td></tr><tr><td>SAC-HER</td><td>0.902 (0.008)</td><td>07.25.42 (01.04.36)</td><td>0.113 (0.012)</td></tr><tr><td>SAC-Demon</td><td>0.925 (0.021)</td><td>05.19.24 (00.06.45)</td><td>0.121 (0.008)</td></tr><tr><td>SAC-SILP</td><td>0.944 (0.004)</td><td>06.35.07 (00.09.25)</td><td>0.118 (0.003)</td></tr><tr><td>SAC-SILP+</td><td>0.973 (0.002)</td><td>05.22.58 (00.04.26)</td><td>0.130 (0.008)</td></tr><tr><td>PRM-0.1</td><td>0.749 (0.038)</td><td>*</td><td>0.134 (0.004)</td></tr><tr><td>PRM-1</td><td>0.772 (0.067)</td><td>*</td><td>1.028 (0.005)</td></tr><tr><td>BC-SAC-SILP+</td><td>0.967 (0.003)</td><td>00.38.03 (00.02.25)</td><td>0.137 (0.008)</td></tr><tr><td>BC-PRM</td><td>0.464 (0.015)</td><td>01.32.56 (00.01.59)</td><td>0.144 (0.010)</td></tr></table>

From the training time column, we found that SAC-Demon took the least training time, but SAC-SILP+ used a similar amount of training time while the standard deviation is the lowest. SAC-SILP+ and DDPG-SILP+ have achieved 28% and 8% less on training time compared to SAC and DDPG methods. Although the planning module intertwines with the learning process, there is no additional substantial computation load on the main program. This is due to the following facts: (1) the planning process is based on the visited states and it has been accelerated with the elimination of collision-checking on the candidate nodes; (2) the most computationally expensive step is the interaction with the environment and the planner involves a small proportion of the total computation.

In addition, HER-related methods are more unstable than others in our task as they have the highest standard deviation variance among the compared algorithms. For BC-related methods, we calculated the training time as a sum of both data collection and BC model training time. The training time for BC methods is much lower than RL-based methods. However, we should notice the assumption that the expert was given before BC training. The access to the expert also takes time and efort. In terms of the planning time, learning-based methods take similar amounts of time for rolling out the policies. The situation for PRM methods is diferent as we can define the desired planning time for the planner. The longer time we allocate, the higher success rate we can expect. We found that if we limit the planning time in PRM to 0.1 second, the same level of planning time in our learning-based methods, the mean success rate is 0.749, which is much lower than the result in DDPG-SILP+ or SAC-SILP+. From this perspective, SILP+ is superior to the traditional PRM method.

We also compared the performance during the training in terms of success rate, as shown in Fig. 5. The curves indicate that our SILP+ related methods DDPG-SILP+ and SAC-SILP+ perform better than other methods in the very beginning of learning. The improvements slower down after 100 epochs, but the advantage of both methods remains significant until the end of training.

The above baseline comparisons verified higher success rates and better training eficiency of SILP+ than other algorithms, including SILP. The main contributions of SILP+ compared to SILP include the Gaussian processguided exploration near obstacles, the reward-based filter in the self-imitation learning framework, and the learning strategy in response to collisions. While the diference in success rates may appear small between SAC-SILP+ (0.973) and SAC-SILP (0.944), it is essential to consider the context. The success rate ceiling is 1, each incremental improvement becomes increasingly significant as we approach the maximum performance. Additionally, when we consider the eficiency aspect. We notice that the average training time for SILP+ has an improvement of 18.2% compared to SILP. This significant reduction in training time serves as a clear and easily understandable indicator of the superior performance of SILP+ over SILP.

![](Luo2023Reinforcement_figs/bcff98ee50e10a33d1420d0120c6804ecd114d0c360509c7124c3811badab6a2.jpg)  
Figure 5: Success rates during training, the data is recorded every 20 epochs. The solid line represents the mean value and the transparent region represents the standard deviation range under three randomly chosen seeds.

In the next subsections, we further investigate how each of these elements contributes to better performance and training eficiency in SILP+.

## 4.3. Collision Types Comparison

It is commonplace to encounter failures during the learning process in motion planning tasks. Herein we consider scenarios where failing is undesirable but not catastrophic, such as, avoiding touching, moving fragile objects or immobile obstacles. In such scenarios, failures still provide a valuable source of information, which have normally been handled by user-defined penalties in reward functions. Yet, designing efective reward functions to avoid failures is dificult and usually requires domain knowledge. Besides designing a suitable reward function, the way of dealing with collision states in the RL framework also plays a vital role in the learning performance. We consider the following three methods to deal with the collisions:

• type-0 (early-reset on collisions): The algorithm terminates the episode when a collision happens [54] [55] and gives the accident a punishment in the reward function [55] [56].

• type-1 (continue as if nothing happens): The algorithm continues the episode with another random but collision-free action; collision experiences are skipped and will not be added into the experience replay bufer for training.

![](Luo2023Reinforcement_figs/5b84a3ed4c1b6a1269976c4e0d82a8c050e2777165513f21ada17f9d19cdec63.jpg)  
Figure 6: The success rate of diferent ways of dealing with collisions during training; the data is recorded every 20 epochs. The solid curve is the mean value, and the transparent region is the standard deviation under three randomly chosen seeds. Type-0, type-1 and type-2 are diferent types of methods dealing with collisions. If we use these collision methods with SILP+, we have type-0-SILP+, type-1-SILP+ and type-2-SILP+.

• type-2 (learn from collisions and successes): The algorithm continues the episode with another random but collision-free action and adds all of the collision experiences into experience replay bufer for policy training.

We recorded the success rates during training with these three methods on pure SAC (type-0, type-1, type-2) and SAC-SILP+ (type-0-SILP+, type-1- SILP+, type-2-SILP+) and illustrated them in Fig. 6. The training time, the number of collisions, accumulated steps during training, and the success rates on trained policies (average with three seeds on 1K episodes) are summarized in Table 2.

The diference between type-0 and type-1 is that the latter will not terminate the episode when a collision happens. Instead, type-1 will randomly select collision-free actions to continue the episode. This results in a longer episode and training time, as shown in Table 2, the training time in type-1 has increased 70.3% and 78.5% in SAC and SAC-SILP+ compared to type-0. In addition, type-1 adds more experience and information near the obstacles, but the success rate of type-1 (0.423) in SAC is much lower than type-0 (0.819). The declined performance could attribute to the scarce random exploration near obstacles. In continuous space, these explorations are inadequate to help the policy gain a generalized understanding of the environment but confuse the policy. However, the situation is diferent when SILP+ gets involved; one can observe that all three types benefit from SILP+ in success rate and training time. Especially for the success rate of type-1, it is more than double that of SAC-SILP+, from 0.423 to 0.942. We interpret that the randomly explored states near the obstacle could enrich the nodes in PRM and help SILP+ plan better distributed demonstrations, thus alleviating the scarce experience problem near obstacles.

Table 2: Success rates and training time under diferent collision methods (simulation)

<table><tr><td colspan="2">Methods</td><td>Success Rate</td><td>Training Time (h.m.s)</td></tr><tr><td rowspan="3">SAC</td><td>type-0</td><td>0.819 (± 0.079)</td><td>06.18.07 (± 00.40.44)</td></tr><tr><td>type-1</td><td>0.423 (± 0.113)</td><td>10.43.53 (± 00.22.14)</td></tr><tr><td>type-2</td><td>0.865 (± 0.021)</td><td>07.12.06 (± 00.05.08)</td></tr><tr><td rowspan="3">SAC-SILP+</td><td>type-0</td><td>0.952 (± 0.027)</td><td>04.59.39 (± 00.06.08)</td></tr><tr><td>type-1</td><td>0.942 (± 0.015)</td><td>06.45.16 (± 00.32.18)</td></tr><tr><td>type-2</td><td>0.971 (± 0.010)</td><td>06.10.02 (± 00.14.13)</td></tr></table>

The diference between type-1 and type-2 is that type-2 uses the collision experiences to update its policy while type-1 does not. From the success rate in Table 2, we see that type-2 performs better than type-1 in both SAC and SAC-SILP+ settings. In accordance, the training time decreases, especially in SAC methods. We conclude that the failure experience can boost the performance, which is also reflected in the comparison between type-0 and type-2.

From the analysis above, one observes that the positive feedback from the planned path in SILP+ also helps with learning. However, which information has more impact on the results? Negative feedback from failures or positive feedback from the planned demonstrations? The answer can be found when one compares the success rates between type-0 and type-2 (from 0.819 to 0.865) and type-0 and type-0-SILP+ (from 0.819 to 0.925). The improvements from negative and positive feedback are 0.046 and 0.133, respectively. Therefore, we interpret that the positive feedback from LfD is more important than the negative feedback in training an NMP.

Here, we take the high success rate as our objective, so we selected type-2 to deal with collisions during the training process. However, if the eficiency has a higher priority, type-0 is also a good option as it can achieve comparable performance under the SILP+ algorithm but requires less training time.

## 4.4. Gaussian-Process-Guided Exploration

In this subsection, we did an ablation experiment to investigate the effect of the Gaussian-process-guided exploration. We compared SAC-SILP+, which was embeded with the Gaussian-process-guided exploration module, with another SAC-SILP+ that is without this module. We call them with-GP and without-GP, respectively. The success rate, training time and the number of collisions during training are summarized in Table 3. From the data, we can see that the final success rates are the same, but the number of collisions for with-GP has decreased to around 20% of without-GP. Accordingly, the training time has been shortened by more than 1 hour. The greatly decreased collision number can be beneficial for safety-sensitive applications, especially in the robotics field.

Table 3: Performance with Gaussian-Process-Guided Exploration (simulation)

<table><tr><td>Performance</td><td>without-GP</td><td>with-GP</td></tr><tr><td>SR</td><td>0.973</td><td>0.973</td></tr><tr><td>Time (h.m.s)</td><td>6.28.50</td><td>5.22.58</td></tr><tr><td>Collision Number</td><td>30844</td><td>6153</td></tr></table>

## 4.5. Extrapolation Error Reduction with Reward Filter

During the training process,if SILP+ is steadily improving, the number of actions in the demonstration bufer that perform better than the policy should decrease. The comparison between the demonstrations and policy was done with a Q filter as used in [31] and [17]. The results were embedded in a behavior cloning loss and contributed to update the RL gradients. However, Q filter can also trigger extrapolation error and result in unstable and unreliable training. In this part, we did an ablation experiment to investigate how extrapolation error occurred in the Q filter and afected the training performance, and how the proposed reward based filter can alleviate the impact.

![](Luo2023Reinforcement_figs/a6fc1112004cb5bac16abe40e189ead89d575b666b04a2cfc5714494a531ada0.jpg)  
Figure 7: Number of actions (#N) from demonstrations that perform better than the RL policy during training. In SAC-SILP+ (dark blue curve), the criterion for comparison is based on the rewards. In SAC-SILP+ with Q filter (ligh magenta curve) action-state values from the critic are used as the criterion. The curves are the mean values over three training sessions with diferent seeds and the semi-transparent band represents the variance.

In the experiments, we selected SAC-SILP+ as the algorithm with reward filter and replaced the reward filter with Q filter to form another comparison algorithm, called SAC-SILP+ with Q filter. First, we recorded the number of actions in the demonstration bufer that performed better than the actions from the policy during the training in Fig. 7. In the figure, the magenta curve and blue curve represent SAC-SILP+ with Q filter and SILP+ with our reward filter, respectively. From the curves, one can see that using the Q filter yields a large variance over the whole training process. In addition, the comparison was unstable before epoch 100, as one can observe from the downward and upward variations in the curve. In contrast, SILP+ with our reward filter (blue line) has a much more stable curve with lower variance. Furthermore, we notice that in our method, the number of actions in demonstrations that perform better than the policy is smaller than the one with Q filter after around epoch 50, which means the policy would need to imitate less from the expert while depending more on itself in SILP+. The results shown in Table 4 indicate that the extrapolation error in the Q value not only results in unstable training but also deteriorates the success rate and training eficiency.

Table 4: Sucesss rate and training time for two filter types (simulation)

<table><tr><td>Performance</td><td>SILP+-Qfilter</td><td>SILP+</td></tr><tr><td>SR</td><td>0.966</td><td>0.973</td></tr><tr><td>Time (h.m.s.)</td><td>06.07.47</td><td>5.22.58</td></tr></table>

## 4.6. Actual robot experiments

We designed several experiments on a physical UR5e robot mounted on a table (Universal Robots, S/N 20195501237). First, we compare the performance of the best-performing policy SAC-SILP+ in simulation and on the real robot. Then we perform an additional comparison between SAC-SILP+ and the next-best contender, SAC-Demon on the real robot. In the SAC-SILP+ test we used three diferent conditions in order to check the efectiveness of the simulation-trained policy being deployed on a pick-and place task in a physical context. The task is shown in Fig. 8, in which three objects are randomly put on the table with the considerations of not arranging them far away from the trained workspace. The big cardboard box (0.2m $\times \ 0 . 2 \mathrm { m } \times 0 . 3 \mathrm { m } )$ represents the obstacle that the robot should avoid during the movement; the small cube $( 0 . 0 7 \mathrm { { m } \times 0 . 0 7 { \mathrm { m } } \times 0 . 0 7 \mathrm { { m } ) } }$ is the object that needs to be picked and placed in the blue basket $( 0 . 1 5 \mathrm { m } \times 0 . 1 5 \mathrm { m } \times 0 . 1 \mathrm { m } )$ The blue basket is the goal, functioning as a container for the cube. The pick-and-place task consist of the following four steps:

• Objects recognition and localization: The perception system is supported by the Aruco marker method [57] [58], which recognizes the markers and calculates the pose of the markers relative to the camera. Based on the poses of these markers, we can compute the objects’ locations relative to the base of the robot arm

• Pick up: The robot goes to the position of the cube with the gripper’s center located 20cm higher than the center of the cube in the Z direction; then the robot goes 10cm down to prepare for the grasping action and locate the cube inside the gripper; finally, the gripper closes to half-way to grasp the cube and goes 10cm up to pick the cube up

• Goal reaching: The learned policy guides the robot to move towards the goal without colliding with the obstacle

![](Luo2023Reinforcement_figs/2e54eadca779a1aac8c78358722af95f2cdf33b1baa9856c5f5cca98610d504c.jpg)  
(a) Initial state

![](Luo2023Reinforcement_figs/073d8328c7315132d4a4e63afd5a87c0b8485511a96f3e794e3b87f0e977bb33.jpg)  
(b) Grasp the object

![](Luo2023Reinforcement_figs/8fb5bd6928cd0bc1c19bc4404f3123a58f9a5691eb0373940c81aec8701f9bdf.jpg)  
(c) Move towards the goal

![](Luo2023Reinforcement_figs/2551f3fcc7667c06a68acffcd82c614036365b125f236816f6413bfb71afe057.jpg)  
(d) Place the object  
Figure 8: Pick and place task with physical robot and objects. The black and white square makers attached to the robot, objects are being used for the perception system for localization.

• Place the object: Once the goal has been successfully reached, the gripper drops the cube into the basket. The process terminates if there is a collision or the policy runs out of pre-defined steps.

Note that in simulation training, the required positional accuracy for the successful reaching is 0.05m. Here, we use the reaching algorithm in a pickand-place task. Therefore, we choose a larger-than 0.05m basket as the goal indicator taking into account the cube’s size. Still, the required accuracy is nearly the same as in the simulation.

The initial states of the robot, obstacle, cube and basket will afect the task’s dificulty level and further afect the policy’s performance. To fully test the performance of the algorithm on the real robot, we categorized the test scenarios into three types: Free (easiest), Block (normal) and Change (dificult). In the Free task, the obstacle is not blocking the path from the tobe-grasped object to the basket and the robot can move straight to the goal without considering the obstacle. Block means the obstacle locates between the robot’s initial pose and the goal and the obstacle is a barrier for the robot’s motion. The dificult one is Change, in which instead of a fixed goal and a fixed obstacle, the goal and/or obstacle will move to other locations during the execution of the policy. The dificulty level increases from Free to Block and then to Change. We first tested each scenario for 50 trials in the real environment and saved the trajectories of the end-efector and the perceived poses of the goal, obstacle and objects. Then, we repeated the real-world experiments in Gazebo using the same trained policy.

![](Luo2023Reinforcement_figs/fa731a1a74a96b7325473bdaf8ddb5f9e5f1d8b75725700d594b24d157e6fac0.jpg)  
Figure 9: Success rates when SAC-SILP+ is applied on a real UR5e robot compared to the simulation environments. Please note that the origin of the Y-axis is not zero but 0.70.

For the comparison between SAC-SILP+ and the next-best contender (SAC-Demon), we used 10 diferent scenarios with diferent obstacles, goals, and initial robot poses. The experimental setting is mostly the same as in the first experiment, except that this experiment focus on a reaching task instead of a pick-and-place task. We run the two simulator-trained policies for ten trials in each scenario and record the successful times. At the end of the testing, each policy will be tested 100 times.

## 4.7. Actual UR5e robot - experimental results

For the first SILP+ experiment, the success rates in physical and simulated environments were compared in Fig. 9. The success rates decrease as the dificulty levels increase in simulation and physical environments, and the Sim2Real gap becomes more noticeable in more dificult scenarios. For the Free scenario, there were three and four failure trials in simulation and the real test, respectively. The three failures in both simulation and real trials were due to the fact that the obstacle’s position located out of the trained workspace. Another failure in the real environment was a collision with the basket, which is attributed to the diferent experimental settings in simulation and the actual robot experiment. The policy was trained to reach a point in the simulation, but we applied it in a pick-and-place application in the physical world. There were four and seven failure cases in simulation and the real test in the Block scenario, respectively. Among the four common failures, three of them are due to the fact that the obstacle and/or goal were put out of the trained workspace; another one could be the algorithm’s ability. There were three more failures in real experiments than in simulations. Two of them were due to collision and one was because of the out-of-basket dropping.

Possible reasons include the measure error from the perception system and the diferent task settings between the simulation and physical experiment. In the Change situation, five failures were found in both simulation and real experiments. Interestingly, there were two failures in simulation that were not the case in the real test due to the complexity of the dynamic environment. The simulation was designed to replicate the experiments in the real-robot test. However, the time and speed of the goal and/or obstacle’s change were hard to be replicated, which caused delays and collisions in simulation. In addition, there were seven failures in the physical experiments that did not happen in simulations; most of them were due to the measurement errors in the perception system. Generally, the causes of failure include locations out of familiar space, measurement errors, algorithm performance and time delay in the simulation. The external factors (e.g., environmental setting and sensor noises) played the most important role.

For the second experiment, we summarize the results in Table 5.

Table 5: Sim2Real success rate for SAC-SILP+ and SAC-Demon in a reaching task

<table><tr><td>Method</td><td>SAC-SILP+</td><td>SAC-Demon</td></tr><tr><td>Simulation</td><td>0.90</td><td>0.87</td></tr><tr><td>Real world</td><td>0.90</td><td>0.75</td></tr></table>

The comparison between our proposed method and the next-best contender on 100 additional trials in 10 scenarios yielded a success rate of 0.90 for SAC-SILP+ and 0.75 for SAC-Demon (significant at $p < 0 . 0 0 1 )$ on the real robot. In the simulated version of the test, the diference between SAC-

SILP+ and SAC-Demon is small (0.90 vs 0.87) when compare to the results in Table 1 which are based on 1000 trials. Failures, e.g., in ’scenario 5’ are characterized by a discrepancy between training and testing conditions.

Based on these extensive empirical analyses, we conclude that the results of SAC-SILP+ are good. The small Sim2Real performance diferences are expected to be solvable with better-matched experimental settings and improved perception systems.

The edited videos for the two actual robot experiments can be accessed through <sup>1</sup> <sup>2</sup>, respectively.

## 5. Conclusion

In this article, we have proposed SILP+ to relieve humans from collecting diverse demonstrations in goal-conditioned motion planning tasks. With the guidance of self-imitation learning that utilizes the demonstrations from planning on past experience, we train a neural motion planner that generalizes substantially better than those learned directly from of-policy RL, behavior cloning or hind-sight experience replay. The experimental results show that the methods of dealing with collision failures significantly determine the performance. Both positive and negative guidance can boost performance, especially the positive demonstrations. However, hesitating and/or cyclic moves around obstacles will deteriorate the training process by confusing the agent, since pertinent information is lacking. Besides, we verified that the proposed Gaussian-process-based exploration near obstacles could accelerate the training by reducing unnecessary collisions, resulting in shortened training time. Furthermore, we analyzed the extrapolation error in the actor-critic neural networks and found that the extrapolation error would lead to unstable training and afect the learning eficiency and success rate. This problem was solved by using a dedicated reward filter to obtain improved results.

We have explored a new way of embedding planning in the learning framework, while not adding much extra computation burden on the training process. The principle behind it may inspire the motion planning and reinforcement learning communities to design robust and eficient NMPs. In addition, the analysis and discussions on the collision solutions and extrapolation error reduction method could enhance studies related to safe and stable RL.

The beneficial efect of the SILP+ method was confirmed for two common RL frameworks in current use, i.e., SAC [52] and DDPG [51], with a clear advantage for the SAC-SILP+ combination.

Although we have tested SILP+ with a position controller on a UR5e robot arm, SILP+ can also be used with other controllers and other robotic platforms if an action model can be obtained to extract the MDP format demonstrations. Since the planning and learning modules in SILP+ are closely intertwined, there is a strong mutual influence. For example, a better exploration technique in RL will not only benefit RL but also generate better nodes for planning and further improve the quality of the behavior demonstrations. In future work, we will investigate how other planning techniques, such as MPCs [59] [60], could guide the exploration to critical regions in the RL training process and generate more informative experiences for further demonstration planning in SILP+.

## Appendix A. Planning Distance Selection

In PRM, the choice of the function that is used to select the neighbors for local planning can afect the planning performance and the path quality [61] [62]. As aforementioned, we use the Euclidean distance as the metric to choose the neighbors to expand the path, but how to define the distance threshold d is nontrivial. The best distance should be able to exclude unnecessary neighbor nodes that distant from the current node and discard neighbors that are too nearby to improve the planning eficiency by decrease the times of collision checking.

We did an empirical decision-making experiment to explore the suitable distance. The distance space is defined as a discrete set: {0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4}m. First, we compare the planning success rate, planned path steps, and the planning time for the successful paths. Then, we combine the selected distance with SILP+ to train the policy and test the final success rate. We summarize the results in Table. A.1, from which we can see that the planning success rate increases when the neighbor distance d increases. This trend is reasonable as the nodes in the roadmap are sparse since they are the explored states in one episode. So, a smaller distance will reduce the number of neighbor nodes within the distance, and the success rate decreases with fewer nodes within the defined d. The average planned path steps and planning time on each successfully planned path follow the decreasing trend with the distance increases. At last, we embed these diferent distances into

SILP+ to compare the final task success rates and illustrate the result in the last row in Table.A.1. We can see that the distance of 0.15m gained the highest task success rate. The PRM-based path planning algorithm is utilized to provide demonstrations for SILP+, in which the task success rate and training eficiency are the most important metrics. So we choose the final distance of 0.15m as the final distance threshold in the experience-based planning module.

Table A.1: The performance for diferent planning distance d

<table><tr><td>distance d (m)</td><td>0.1</td><td>0.15</td><td>0.2</td><td>0.25</td><td>0.3</td><td>0.35</td><td>0.4</td></tr><tr><td>SR(Planning)</td><td>0.8</td><td>0.8786</td><td>0.9028</td><td>0.9144</td><td>0.9214</td><td>0.9238</td><td>0.924</td></tr><tr><td>Avg Steps</td><td>6.39</td><td>5.614</td><td>5.064</td><td>4.676</td><td>4.402</td><td>4.152</td><td>3.920</td></tr><tr><td>Planning Time</td><td>0.242</td><td>0.218</td><td>0.202</td><td>0.191</td><td>0.184</td><td>0.177</td><td>0.171</td></tr><tr><td>SR(SILP+)</td><td>0.961</td><td>0.965</td><td>0.933</td><td>0.828</td><td>0.782</td><td>0.745</td><td>0.663</td></tr></table>

## Appendix B. Collision Model

Collision checking is one of the most computationally expensive modules in path planning [63]. Researchers tried to accelerate the collision checking process with neural networks. For instance, Kew et al. [64] proposed a neural network called ClearanceNet to predict the minimal distance between the robot and the workspace and use this prediction to infer the collisions. L¨utjens et al. [65] predicted collision probability based on a set of LSTM networks. Tuan et al. [66] utilized Contractive AutoEncoder (CAE) to learn the latent representation of the collision-free space in order to predict the validation of robot configurations.

In this work, we learned a neural network model M that predicts the collision probability given the robot’s joints configuration and obstacle’s information. The model has three hidden layers (512, 256 and 64 nodes each) and an output for the prediction of collision probability. The dataset contains 485k configurations and among them, 90% and 10% were used as the training and testing dataset. The evaluated accuracy, recall, precision and specificity are 0.991, 0.984, 0.989 and 0.995, respectively, under the discrimination threshold of 0.5. The ROC curve is illustrated in Fig. B.1. Ultimately, the output from M can be used to predict the collision probability between two states to improve the planning eficiency and the quality of the planned demonstrations.

![](Luo2023Reinforcement_figs/490d60dbd164e81e500560ae80ee1a53439aff9c5e55d97fab4bfc27d3194d08.jpg)  
Figure B.1: ROC curve of the collision checking model

## Acknowledgements

We want to thank the Reviewers for taking the time and efort necessary to review the manuscript. We sincerely appreciate all valuable comments and suggestions, which helped us improve the manuscript’s quality. In addition, we are grateful to Dr.Hamidreza Kasaei for his helpful discussions and experimental contributions. We are also thankful to Weijia Yao for the early discussions on problem formulation and article proofreading. Finally, we thank the Center for Information Technology of the University of Groningen for their support and for providing access to the Peregrine high-performance computing cluster.

## References

[1] P. Abbeel, D. Dolgov, A. Y. Ng, S. Thrun, Apprenticeship learning for motion planning with application to parking lot navigation, in: IEEE/RSJ International Conference on Intelligent Robots and Systems, 2008, pp. 1083–1090. doi:10.1109/IROS.2008.4651222.

[2] W. Yao, H. G. de Marina, B. Lin, M. Cao, Singularity-free guiding vector field for robot navigation, IEEE Transactions on Robotics 37 (4) (2021).

[3] H.-T. L. Chiang, A. Faust, M. Fiser, A. Francis, Learning navigation behaviors end-to-end with autorl, IEEE Robotics and Automation Letters 4 (2) (2019) 2007–2014. doi:10.1109/LRA.2019.2899918.

[4] D. A. Rosenbaum, R. J. Meulenbroek, J. Vaughan, C. Jansen, Posturebased motion planning: applications to grasping, Psychological review 108 (4) (2001) 709. doi:10.1037/0033-295X.108.4.709.

[5] C. Chamzas, A. Shrivastava, L. E. Kavraki, Using local experiences for global motion planning, in: IEEE International Conference on Robotics and Automation, 2019, pp. 8606–8612. doi:10.1109/ICRA. 2019.8794317.

[6] R. He, S. Prentice, N. Roy, Planning in information space for a quadrotor helicopter in a GPS-denied environment, in: IEEE International Conference on Robotics and Automation, 2008, pp. 1814–1820. doi: 10.1109/ROBOT.2008.4543471.

[7] S. M. LaValle, Rapidly-exploring random trees : a new tool for path planning, The annual research report (1998).

[8] L. Kavraki, P. Svestka, J.-C. Latombe, M. Overmars, Probabilistic roadmaps for path planning in high-dimensional configuration spaces, IEEE Transactions on Robotics and Automation 12 (4) (1996) 566–580. doi:10.1109/70.508439.

[9] T. Jurgenson, A. Tamar, Harnessing reinforcement learning for neural motion planning, in: Proceedings of Robotics: Science and Systems, FreiburgimBreisgau, Germany, 2019. doi:10.15607/RSS.2019.XV.026.

[10] A. H. Qureshi, A. Simeonov, M. J. Bency, M. C. Yip, Motion planning networks, in: IEEE International Conference on Robotics and Automation, 2019, pp. 2118–2124. doi:10.1109/ICRA.2019.8793889.

[11] H. Ravichandar, A. S. Polydoros, S. Chernova, A. Billard, Recent advances in robot learning from demonstration, Annual Review of Control, Robotics, and Autonomous Systems 3 (2020). doi:10.1146/ annurev-control-100819-063206.

[12] S. Chitta, I. Sucan, S. Cousins, Moveit! [ROS topics], IEEE Robotics Automation Magazine 19 (1) (2012) 18–19. doi:10.1109/MRA.2011. 2181749.

[13] A. Rajeswaran, V. Kumar, A. Gupta, G. Vezzani, J. Schulman, E. Todorov, S. Levine, Learning complex dexterous manipulation with

deep reinforcement learning and demonstrations, in: Proceedings of Robotics: Science and Systems, Pittsburgh, Pennsylvania, 2018. doi: 10.15607/RSS.2018.XIV.049.

[14] E. L. Sauser, B. D. Argall, G. Metta, A. G. Billard, Iterative learning of grasp adaptation through human corrections, Robotics and Autonomous Systems 60 (1) (2012) 55–71. doi:10.1016/j.robot.2011.08.012.

[15] J. Kober, J. Peters, Policy search for motor primitives in robotics, Machine learning 84 (1-2) (2011) 171–203. doi:10.1007/ s10994-010-5223-6.

[16] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke, et al., Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation, arXiv preprint arXiv:1806.10293 (2018).

[17] S. Luo, H. Kasaei, L. Schomaker, Self-imitation learning by planning, in: IEEE International Conference on Robotics and Automation, 2021, pp. 4823–4829. doi:10.1109/ICRA48506.2021.9561411.

[18] C. Zhang, J. Huh, D. D. Lee, Learning implicit sampling distributions for motion planning, in: IEEE/RSJ International Conference on Intelligent Robots and Systems, 2018, pp. 3654–3661. doi:10.1109/IROS.2018. 8594028.

[19] B. Ichter, J. Harrison, M. Pavone, Learning sampling distributions for robot motion planning, in: IEEE International Conference on Robotics and Automation, 2018, pp. 7087–7094. doi:10.1109/ICRA.2018. 8460730.

[20] A. Francis, A. Faust, H.-T. L. Chiang, J. Hsu, J. C. Kew, M. Fiser, T.-W. E. Lee, Long-range indoor navigation with prm-rl, IEEE Transactions on Robotics 36 (4) (2020) 1115–1134. doi:10.1109/TRO.2020. 2975428.

[21] B. Angulo, A. Panov, K. Yakovlev, Policy optimization to learn adaptive motion primitives in path planning with dynamic obstacles, IEEE Robotics and Automation Letters (2022).

[22] B. Eysenbach, R. R. Salakhutdinov, S. Levine, Search on the replay bufer: Bridging planning and reinforcement learning, in: Advances in Neural Information Processing Systems, 2019, pp. 15246–15257.

[23] F. Xia, C. Li, R. Mart´ın-Mart´ın, O. Litany, A. Toshev, S. Savarese, Relmogen: Integrating motion generation in reinforcement learning for mobile manipulation, in: IEEE International Conference on Robotics and Automation, 2021, pp. 4583–4590. doi:10.1109/ICRA48506.2021. 9561315.

[24] S. Schaal, Learning from demonstration, Advances in neural information processing systems 9 (1996).

[25] A. Y. Ng, H. J. Kim, M. I. Jordan, S. Sastry, S. Ballianda, Autonomous helicopter flight via reinforcement learning, in: Advances in Neural Information Processing Systems, Vol. 16, 2003.

[26] P. Abbeel, A. Coates, M. Quigley, A. Y. Ng, An application of reinforcement learning to aerobatic helicopter flight, in: Advances in Neural Information Processing Systems, 2007, pp. 1–8.

[27] M. Rigter, B. Lacerda, N. Hawes, A framework for learning from demonstration with minimal human efort, IEEE Robotics and Automation Letters 5 (2) (2020) 2023–2030. doi:10.1109/LRA.2020.2970619.

[28] X. Xiao, B. Liu, G. Warnell, J. Fink, P. Stone, Appld: Adaptive planner parameter learning from demonstration, IEEE Robotics and Automation Letters 5 (3) (2020) 4541–4547. doi:10.1109/LRA.2020.3002217.

[29] M. Laskey, S. Staszak, W. Y.-S. Hsieh, J. Mahler, F. T. Pokorny, A. D. Dragan, K. Goldberg, Shiv: Reducing supervisor burden in dagger using support vectors for eficient learning from demonstrations in high dimensional state spaces, in: IEEE International Conference on Robotics and Automation, 2016, pp. 462–469. doi:10.1109/ICRA.2016.7487167.

[30] H. Su, Y. Hu, Z. Li, A. Knoll, G. Ferrigno, E. De Momi, Reinforcement learning based manipulation skill transferring for robot-assisted minimally invasive surgery, in: IEEE International Conference on Robotics and Automation, 2020, pp. 2203–2208. doi:10.1109/ICRA40945.2020. 9196588.

[31] A. Nair, B. McGrew, M. Andrychowicz, W. Zaremba, P. Abbeel, Overcoming exploration in reinforcement learning with demonstrations, in: IEEE International Conference on Robotics and Automation, 2018, pp. 6292–6299. doi:10.1109/ICRA.2018.8463162.

[32] J. D. Sweeney, R. Grupen, A model of shared grasp afordances from demonstration, in: IEEE-RAS International Conference on Humanoid Robots, 2007, pp. 27–35. doi:10.1109/ICHR.2007.4813845.

[33] C. G. Atkeson, S. Schaal, Robot learning from demonstration, in: International Conference on Machine Learning, Vol. 97, PMLR, 1997, pp. 12–20.

[34] S. Ross, D. Bagnell, Eficient reductions for imitation learning, in: Proceedings of the thirteenth international conference on artificial intelligence and statistics, JMLR Workshop and Conference Proceedings, 2010, pp. 661–668.

[35] T. Brys, A. Harutyunyan, H. B. Suay, S. Chernova, M. E. Taylor, A. Now´e, Reinforcement learning from demonstration through shaping, in: Twenty-fourth international joint conference on artificial intelligence, 2015.

[36] M. Jing, X. Ma, W. Huang, F. Sun, C. Yang, B. Fang, H. Liu, Reinforcement learning from imperfect demonstrations under soft expert guidance, in: Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 34, 2020, pp. 5109–5116. doi:10.1609/aaai.v34i04.5953.

[37] M. Vecerik, T. Hester, J. Scholz, F. Wang, O. Pietquin, B. Piot, N. Heess, T. Roth¨orl, T. Lampe, M. Riedmiller, Leveraging demonstrations for deep reinforcement learning on robotics problems with sparse rewards, arXiv preprint arXiv:1707.08817 (2017).

[38] T. Hester, M. Vecerik, O. Pietquin, M. Lanctot, T. Schaul, B. Piot, D. Horgan, J. Quan, A. Sendonaris, I. Osband, et al., Deep Q-learning from demonstrations, in: Thirty-second AAAI conference on artificial intelligence, 2018.

[39] S. Ross, G. Gordon, D. Bagnell, A reduction of imitation learning and structured prediction to no-regret online learning, in: Proceedings of the

fourteenth international conference on artificial intelligence and statistics, JMLR Workshop and Conference Proceedings, 2011, pp. 627–635.

[40] J. Oh, Y. Guo, S. Singh, H. Lee, Self-imitation learning, in: International Conference on Machine Learning, PMLR, 2018, pp. 3878–3887.

[41] T. Dai, H. Liu, A. Anthony Bharath, Episodic self-imitation learning with hindsight, Electronics 9 (10) (2020) 1742. doi:10.3390/ electronics9101742.

[42] M. Andrychowicz, F. Wolski, A. Ray, J. Schneider, R. Fong, P. Welinder, B. McGrew, J. Tobin, O. P. Abbeel, W. Zaremba, Hindsight experience replay, in: Advances in Neural Information Processing Systems, 2017, pp. 5048–5058.

[43] S. Racani\`ere, T. Weber, D. Reichert, L. Buesing, A. Guez, D. J. Rezende, A. P. Badia, O. Vinyals, N. Heess, Y. Li, et al., Imagination-augmented agents for deep reinforcement learning, in: Advances in Neural Information Processing Systems, 2017, pp. 5690–5701.

[44] R. S. Sutton, A. G. Barto, Reinforcement learning: An introduction, MIT press, 2018.

[45] E. Pairet, C. Chamzas, Y. Petillot, L. E. Kavraki, Path planning for manipulation using experience-driven random trees, IEEE Robotics and Automation Letters 6 (2) (2021) 3295–3302. doi:10.1109/LRA.2021. 3063063.

[46] D. Coleman, I. A. S¸ucan, M. Moll, K. Okada, N. Correll, Experiencebased planning with sparse roadmap spanners, in: IEEE International Conference on Robotics and Automation, 2015, pp. 900–905. doi:10. 1109/ICRA.2015.7139284.

[47] S. Fujimoto, D. Meger, D. Precup, Of-policy deep reinforcement learning without exploration, in: International Conference on Machine Learning, PMLR, 2019, pp. 2052–2062.

[48] N. Heess, G. Wayne, D. Silver, T. Lillicrap, Y. Tassa, T. Erez, Learning continuous control policies by stochastic value gradients, Advances in Neural Information Processing Systems (2015) 2944–2952.

[49] C. E. Rasmussen, C. K. I. Williams, Gaussian Processes for Machine Learning, The MIT Press, 2005.

[50] C. E. Rasmussen, Gaussian processes in machine learning, in: Summer school on machine learning, Springer, 2003, pp. 63–71.

[51] T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, D. Wierstra, Continuous control with deep reinforcement learning, arXiv preprint arXiv:1509.02971 (2015).

[52] T. Haarnoja, A. Zhou, P. Abbeel, S. Levine, Soft actor-critic: Of-policy maximum entropy deep reinforcement learning with a stochastic actor, in: International Conference on Machine Learning, PMLR, 2018, pp. 1861–1870.

[53] T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, et al., Soft actor-critic algorithms and applications, arXiv preprint arXiv:1812.05905 (2018).

[54] J. Choi, G. Lee, C. Lee, Reinforcement learning-based dynamic obstacle avoidance and integration of path planning, Intelligent Service Robotics 14 (5) (2021) 663–677. doi:10.1007/s11370-021-00387-2.

[55] Y. Zhao, J. Guo, C. Bai, H. Zheng, Reinforcement learning-based collision avoidance guidance algorithm for fixed-wing uavs, Complexity 2021 (2021). doi:10.1155/2021/8818013.

[56] B. Sangiovanni, A. Rendiniello, G. P. Incremona, A. Ferrara, M. Piastra, Deep reinforcement learning for collision avoidance of robotic manipulators, in: European Control Conference (ECC), 2018, pp. 2063–2068. doi:10.23919/ECC.2018.8550363.

[57] F. J. Romero-Ramirez, R. Mu˜noz-Salinas, R. Medina-Carnicer, Speeded up detection of squared fiducial markers, Image and vision Computing 76 (2018) 38–47. doi:10.1016/j.imavis.2018.05.004.

[58] S. Garrido-Jurado, R. Munoz-Salinas, F. J. Madrid-Cuevas, R. Medina-Carnicer, Generation of fiducial marker dictionaries using mixed integer linear programming, Pattern Recognition 51 (2016) 481–491. doi:10. 1016/j.patcog.2015.09.023.

[59] B. Brito, M. Everett, J. P. How, J. Alonso-Mora, Where to go next: Learning a subgoal recommendation policy for navigation in dynamic environments, IEEE Robotics and Automation Letters 6 (3) (2021) 4616– 4623. doi:10.1109/LRA.2021.3068662.

[60] A. S. Morgan, D. Nandha, G. Chalvatzaki, C. D’Eramo, A. M. Dollar, J. Peters, Model predictive actor-critic: Accelerating robot skill acquisition with deep reinforcement learning, in: IEEE International Conference on Robotics and Automation, 2021, pp. 6672–6678. doi: 10.1109/ICRA48506.2021.9561298.

[61] N. M. Amato, O. B. Bayazit, L. K. Dale, C. Jones, D. Vallejo, Choosing good distance metrics and local planners for probabilistic roadmap methods, in: Proceedings. 1998 IEEE International Conference on Robotics and Automation (Cat. No. 98CH36146), Vol. 1, IEEE, 1998, pp. 630– 637. doi:10.1109/ROBOT.1998.677043.

[62] J. J. Kufner, Efective sampling and distance metrics for 3d rigid body path planning, in: IEEE International Conference on Robotics and Automation, 2004. Proceedings. ICRA’04. 2004, Vol. 4, IEEE, 2004, pp. 3993–3998. doi:10.1109/ROBOT.2004.1308895.

[63] J. Canny, The complexity of robot motion planning, MIT press, 1988.

[64] J. Chase Kew, B. Ichter, M. Bandari, T.-W. E. Lee, A. Faust, Neural Collision Clearance Estimator for Batched Motion Planning, in: International Workshop on the Algorithmic Foundations of Robotics, Springer, 2020, pp. 73–89.

[65] B. L¨utjens, M. Everett, J. P. How, Safe reinforcement learning with model uncertainty estimates, in: 2019 International Conference on Robotics and Automation, 2019, pp. 8662–8668. doi:10.1109/ICRA. 2019.8793611.

[66] T. Tran, J. Denny, C. Ekenna, Predicting Sample Collision with Neural Networks, arXiv preprint arXiv:2006.16868 (2020).