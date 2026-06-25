---
citation_key: Wang2025PERDPP
arxiv_id: 2503.07411
arxiv_url: "https://arxiv.org/abs/2503.07411"
title: "PER-DPP Sampling Framework and Its Application in Path Planning"
authors_short: "Junzhe Wang"
year: 2025
direction_tag: Q_informed_sampling
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:12:12Z
origin: ai+web
reviewed: false
---

# PER-DPP Sampling Framework and Its Application in Path Planning

Junzhe Wang

## 1. Abstract

Autonomous navigation in intelligent mobile systems represents a core research focus within artificial intelligence-driven robotics. Contemporary path planning approaches face constraints in dynamic environmental responsiveness and multi-objective task scalability, limiting their capacity to address growing intelligent operation requirements. Decision-centric reinforcement learning frameworks, capitalizing on their unique strengths in adaptive environmental interaction and selfoptimization, have gained prominence in advanced control system research.

This investigation introduces methodological improvements to address sample homogeneity challenges in reinforcement learning experience replay mechanisms. By incorporating determinant point processes (DPP) for diversity assessment, we develop a dual-criteria sampling framework with adaptive selection protocols. This approach resolves representation bias in conventional prioritized experience replay (PER) systems while preserving algorithmic interoperability, offering improved decision optimization for dynamic operational scenarios. Key contributions comprise:

Develop a hybrid sampling paradigm (PER-DPP) combining priority sequencing with diversity maximization.Based on this,create an integrated optimization scheme (PER-DPP-Elastic DQN) merging diversity-aware sampling with adaptive step-size regulation. Comparative simulations in 2D navigation scenarios demonstrate that the elastic step-size component temporarily delays initial convergence speed but synergistically enhances final-stage optimization with PER-DPP integration. The synthesized method generates navigation paths with optimized length efficiency and directional stability.

## 2. Preliminaries

## 2.1 Reinforcement Learning<sup>[1]</sup>

Reinforcement Learning is a learning paradigm where agents autonomously learn to make decision by interacting with an environment, with the goal of maximizing expected rewards. The system is formalized as a Markov Decision Process (MDP), which is defined by a tuple $\langle \mathrm { S } , \mathrm { A } , \mathrm { P } , \mathrm { R } , \gamma \rangle$ , where S represents the state space, A represents the action space, P defines the state transition probabilities, R denotes the reward function, and $\gamma$ is the discount factor. At each step t, the environment is in a state $s _ { t }$ , and the agent selects an action at according to a policy π. The environment then transitions to a new state based on the transition probability $P ( s _ { t + 1 } \mid s _ { t } , a _ { t } )$ , and the agent receives a reward. The agent’s objective is to learn an optimal policy $\pi ^ { * }$ that maximizes the expected cumulative discounted reward starting from any initial state $s _ { t }$ :

$$
V _ {\pi} (s) = E \left[ G _ {t} \mid S _ {t} = s \right] = E \left[ R _ {t} + \gamma R _ {t + 1} + \gamma^ {2} R _ {t + 2} + \dots . \mid S _ {t} = s \right]\tag{2.1}
$$

where $V _ { \pi } ( s )$ is the value function that estimates the expected return when following policy π from state $s _ { t }$

## 2.2 Experience Replay

In deep reinforcement learning, experience replay plays a critical role by allowing agents to store and reuse historical interactions through a replay buffer. This approach addresses the problem of data correlation inherent in online training processes while enhancing the utilization efficiency of samples. A notable advancement in optimizing experience replay is Prioritized Experience Replay<sup>[2]</sup> (PER), which strategically weights past experiences to improve learning effectiveness. PER enhances the effectiveness of experience replay mechanisms by selectively emphasizing transitions with higher learning significance, as determined through temporal difference (TD) error measurements, as (2.2).

$$
\delta_ {j} = r _ {j} + \gamma \max _ {a} Q (s _ {j + 1}, a, w _ {T}) - Q (s _ {j}, a _ {j}, w)\tag{2.2}
$$

In PER, an experience is assigned a priority $p _ { j } = \mid \delta _ { j } \mid + \varepsilon$ where ensures nonzero priority. The probability P(j) of sampling an experience is proportional to its priority:

$$
P (j) = \frac {p _ {j} ^ {a}}{\sum_ {k} p _ {k} ^ {a}}\tag{2.3}
$$

By focusing on experiences with higher TD errors, PER enhances learning efficiency and accelerates convergence.

## 2.3 Determinantal Point Processes<sup>[3]</sup>

There are various methods to measure sample heterogeneity. Many methods struggle to efficiently select highly diverse samples and often require substantial prior knowledge.The Determinantal Point Process (DPP) is a probabilistic model that defines correlations among samples via a kernel matrix, simplifying probability calculations through determinant computations. Elements in the kernel matrix represent pairwise similarities between samples, and the determinant value reflects the degree of heterogeneity within a subset. When a subset contains overly similar elements, the determinant decreases, thereby reducing the probability of their co-occurrence. DPP excels at modeling the balance between diversity and quality of elements in a set and is widely applied in recommendation systems, text summarization, image retrieval, and similar scenarios. Its core idea lies in measuring subset probabilities via matrix determinants, favoring subsets that are both high-quality and diverse. With its unique mathematical formulation and flexible design, DPP provides an efficient and powerful tool for addressing diversity and correlation challenges. A brief introduction is provided below.

Given a predefined sample set Z and its kernel function K , a probability measure space $( Z , 2 ^ { Z } , P )$ can be mathematically defined. The definitions of Z and P are as follows: Let the candidate sample set $\textsf { Z } = \{ z _ { 1 } , z _ { 2 } . . . z _ { N } \}$ contain N samples. The Determinantal Point Process (DPP) transforms complex probability calculations into simplified determinant computations, where the probability of sampling any subset $Y \subseteq Z$ is proportional to the determinant of its corresponding kernel submatrix $K _ { Y }$ , as shown in Equation (2.4). Here, $K _ { \scriptscriptstyle { Y } }$ denotes the Gaussian kernel matrix associated with the subset Y, which is a submatrix of the original kernel matrix K.

$$
P (Y) \propto \det (K _ {Y})\tag{2.4}
$$

The DPP algorithm can be formulated as the following determinant maximization problem: $_ { Y \subseteq R } \log ( \operatorname* { d e t } ( K _ { Y } ) )$ .However, this constitutes an NP-Hard problem. Traditional MAP requires computing determinants over all possible subsets, resulting in exponential complexity $\left( \mathrm { O } ( N ^ { 3 } M ^ { 3 } ) \right)$ , where N is the total number of elements and M is the target subset size), which becomes intractable for large-scale datasets. In practical implementations, greedy algorithms<sup>[4]</sup> are commonly employed to reduce computational complexity to ${ \mathrm { O } } ( M ^ { 2 } N )$ while guaranteeing near-optimal solutions.

The greedy selection process iteratively selects a sample j from the candidate set that maximizes the marginal gain and adds it to the resulting subset Y until a stopping criterion is met, as formalized in Equation (2.5).

$$
j = \arg \max _ {j \in R \backslash Y} \log \det (K _ {Y \cup \{j \}}) - \log \det (K _ {Y})\tag{2.5}
$$

However, due to the high computational complexity of determinant calculations, the Cholesky decomposition of matrices is employed. The specific procedure is as follows: Assume a matrix with its Cholesky decomposition expressed as (2.6), where V is a non-invertible lower triangular matrix, and $( K _ { Y } ) > 0$

$$
K _ {Y} = V V ^ {T}\tag{2.6}
$$

For any $j \in R \backslash Y , K _ { Y \cup \{ j \} }$ has:

$$
\begin{array}{r l} K _ {Y \cup \{j \}} & = \left[ \begin{array}{c c} K _ {Y} & K _ {Y, j} \\ K _ {Y, j} ^ {T} & K _ {j j} \end{array} \right] = \left[ \begin{array}{c c} V & 0 \\ C _ {j} & d _ {j} \end{array} \right] \left[ \begin{array}{c c} V & 0 \\ C _ {j} & d _ {j} \end{array} \right] ^ {T} \\ & = \left[ \begin{array}{c c} V V ^ {T} & V C _ {j} ^ {T} \\ C _ {j} V ^ {T} & C _ {j} C _ {j} ^ {T} - d _ {j} ^ {2} \end{array} \right] \end{array}\tag{2.7}
$$

Then we get:

$$
V C _ {j} ^ {T} = K _ {Y, j}\tag{2.8}
$$

$$
d _ {j} ^ {2} = K _ {j j} - \left\| C _ {j} \right\| _ {2} ^ {2}\tag{2.9}
$$

$$
\det (K _ {Y \cup \{j \}}) = \det (V V ^ {T}) \bullet d _ {j} ^ {2}\tag{2.10}
$$

According to (2.10), we can simplify (2.5) as follows:

$$
i = \arg \max _ {j \in R \backslash Y} \log (d _ {j} ^ {2})\tag{2.11}
$$

The advantage of this method lies in transforming the Cholesky decomposition process into an incremental computation rather than direct decomposition when adding new samples. After incorporating sample i , obtained through Equation (2.11), into the acquired subset Y , the updated Cholesky decomposition of the sub-kernel matrix can be derived according to Equation (2.7) as follows:

$$
K _ {Y \cup \{i \}} = \left[ \begin{array}{l l} V & 0 \\ C _ {i} & d _ {i} \end{array} \right] \left[ \begin{array}{l l} V & 0 \\ C _ {i} & d _ {i} \end{array} \right] ^ {T} = V ^ {\prime} V ^ {\prime T}\tag{2.12}
$$

Similar $\mathrm { t o } ( 2 . 8 ) , C _ { i }$ and $d _ { i }$ are updated and recorded, for every $j \in R \backslash ( Y \cup \{ i \} )$ we can get a new decomposition as follows:

$$
V ^ {\prime} C _ {j} ^ {T} = \left[ \begin{array}{c c} V & 0 \\ C _ {i} & d _ {i} \end{array} \right] C _ {j} ^ {T} = K _ {Y \cup \{i \}, j} = \left[ \begin{array}{c} K _ {Y, j} \\ K _ {i j} \end{array} \right]\tag{2.13}
$$

$$
C _ {j} ^ {' T} = \left[ \begin{array}{c c} V & 0 \\ C _ {i} & d _ {i} \end{array} \right] ^ {- 1} \left[ \begin{array}{c} K _ {Y, j} \\ K _ {i j} \end{array} \right] = \left[ \begin{array}{c} V ^ {- 1} K _ {Y, j} \\ - (C _ {i} V ^ {- 1} K _ {Y, j} - K _ {i j}) / d _ {i} \end{array} \right]\tag{2.14}
$$

Then with (2.8) and (2.14),we can get:

$$
C _ {j} ^ {\prime} = \left[ \begin{array}{c c} C _ {j} & (K _ {i j} - C _ {i} ^ {T} C _ {j}) / d _ {i}) \end{array} \right] \triangleq [ C _ {j} \quad e _ {j} ]\tag{2.15}
$$

$$
d _ {j} ^ {\prime} = K _ {j j} - \left\| C _ {j} ^ {\prime} \right\| _ {2} ^ {2} = d _ {j} ^ {2} - e _ {j} ^ {2}
$$

（2.16）

## 2.4 Elastic DQN<sup>[5]</sup>

The Elastic DQN algorithm primarily integrates the concepts of Coarse Q-Learning and multi-step DQN learning, leveraging their distinctive properties to mitigate overestimation and enhance the overall performance of DQN. First, to incorporate Coarse Q-Learning principles, a memory bank is introduced before the experience replay buffer. This module employs unsupervised clustering analysis to evaluate the similarity between the current state and previous states. Meanwhile, multistep DQN exhibits sensitivity to the hyperparameter controlling the number of learning steps. The memory bank dynamically adjusts learning steps by aggregating updates for similar states into a single operation while processing dissimilar states independently, thereby enabling adaptive step-size updates. The algorithm workflow is illustrated in Figure 2.1.

![](Wang2025PERDPP_figs/dc66eeaba4481b6128a18a83f0fc228a3f6e511def9bf0bff031398133c82642.jpg)  
Figure 2.1 Elastic DQN workflow

## 3. PER-DPP-Elastic DQN

## 3.1 PER-DPP sampling paradigm

Fujimoto et al<sup>[6]</sup> demonstrated that prioritized sampling may excessively focus on a small subset of samples with high temporal-difference (TD) errors, leading to overreuse of specific samples and consequently reducing sample diversity. Fedus et al<sup>[7]</sup> further noted that the prioritization mechanism in PER introduces distributional bias, causing models to overemphasize early high-error samples, which may not optimally benefit long-term learning. Li et al<sup>[8]</sup> improved algorithmic efficiency by filtering highsimilarity sequences duringexperience replay to reduce redundancy. Zhao et al<sup>[9]</sup> proposed incorporating sample diversity into batch sampling, where higher heterogeneity among samples accelerates agent learning. To address PER-induced diversity reduction caused by overemphasis on high-TD-error samples, this study introduces a two-stage hybrid algorithm. The first stage employs PER for importance calculation and ranking to select a larger batch of experiences, followed by the Fast Greedy MAP algorithm to extract a subset with enhanced diversity from this batch.

![](Wang2025PERDPP_figs/031787e3984400731ec69f9d92a23cac13c0f8fb4b67e22e7c1205d11642a5b8.jpg)  
Figure 3.1 PER-DPP workflow

## 3.2 PER-DPP-Elastic DQN Algorithm

Similar to (2.2), we found that for multi-step DQN, TD error is as follow:

$$
\delta_ {j} = \sum_ {k = 0} ^ {n - 1} \gamma^ {k} r _ {t + k + 1} + \gamma^ {n} \max _ {a} Q (s _ {j + n}, a, w _ {T}) - Q (s _ {j}, a _ {j}, w)\tag{3.1}
$$

The Elastic DQN algorithm stores step-count information in the experience replay buffer and utilizes a multi-step DQN approach for agent network parameter updates. When integrated with the PER-DPP sampling framework, corresponding modifications to priority calculations are required. The associated pseudocode is provided as the following Table 3.1:

Table 3.1 Pseudo code for PER-DPP- Elastic DQN

<table><tr><td>Initialization: step length d=0, replay buffer D, memory bank B, Setting the target network and main network with the same shape and initial parameters.While not finished:For every time step t:Experience sample clustering judgment or storage:1.with ε -greedy policy, get action  $a_t$  from  $s_t$ 2.get next state  $s_{t+d+1}$  and reward  $r_t$ ,compute the Q value of  $s_t$  and $s_{t+d+1}$ </td></tr></table>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
3. store  $Q(s_{t})$  and  $Q(s_{t+d+1})$  into memory bank B
4. get samples from B to apply clustering, and add Q value into the samples
5. Using the HDBSCAN, make the following judgments on the results:
If  $Q(s_{t})$  and  $Q(s_{t+d+1})$  have the same lable:
store  $(s_{t}, a_{t}, R_{t}, s_{t+d+1}, d)$  into D, with most priority  $p_{t}$ 
reset d=0
else, compute accumulative reward:
 $R_{t} + = \gamma^{d} r_{t+d+1}$ , d+=1
Sample and update network parameters:
6. sample  $j \sim P(j) = \frac{p_{j}^{a}}{\Sigma_{k} p_{k}^{a}}$ 
7. compute weight  $w_{j} = (N \cdot P(j))^{-\beta} / \max_{k} w_{k}$ 
8. update the priority  $p_{j} = |\delta_{j}| = |R_{j} + \gamma^{d+1}| \max_{a} Q(s_{j+d+1}, a, w_{T}) - Q(s_{j}, a_{j}, w)|$ 
9. calculate the kernel matrix for measuring sample similarity
10. Using the Fast Greedy MAP to select small batches of empirical samples
11. Update network parameters based on experience and weights
 $s_{t} \leftarrow s_{t+1}$ 
Copy the main network parameters to the target network every T times
</div>

## 3.3 Experimental design

This section briefly introduces the two-dimensional maze environment for path planning (as shown in Figure 3.2), including the design of state space, action space, and reward function, and presents the experimental results of PER-DPP-Elastic DQN on three maps in the above environment.

![](Wang2025PERDPP_figs/6a977679d82adfca2b22bdb568101267a42bab99e8ca6747d7baf4c6202cc036.jpg)  
Figure 3.2 Two dimensional maze environment

in the exploration task of unknown environments, this study constructed three core state parameters as shown in Table 3.2:

Table 3.2 State Space for Two Dimensional Maze Environment

<table><tr><td>Parameter</td><td>Parameter meaning</td></tr><tr><td>dx</td><td>horizontal distance from the target point</td></tr><tr><td>dy</td><td>vertical distance from the target point</td></tr><tr><td>ob</td><td>information on 8 nearby obstacles</td></tr></table>

Based on the actual situation, this study sets up an 8-dimensional action space, representing 8 directions on a two-dimensional plane: front, back, left, right, and left front, left back, right front, right back. The executed action moves one unit distance in the corresponding direction, as shown in Figure 3.3:

![](Wang2025PERDPP_figs/05a44c5a9cdd2759d88fa2a8dbe1e5c8bef61f68f974ac7e4ad23bd0bb70ffac.jpg)  
Figure 3.3 maze environment action space

The design of the reward function r is shown in (3.2), which is relatively simple and easy to understand. If the agent remains stationary, a penalty of -200 will be given to encourage the agent to explore the environment; If the intelligent agent reaches its destination after performing an action, a large reward of 500 will be given; If the intelligent agent encounters an obstacle after performing an action, a large punishment of -500 will be given; If the intelligent agent is closer to the target after performing an action, a reward of 100 will be given; If the target point is far away, a penalty of -100 will be imposed.

$$
r = \left\{ \begin{array}{l l} - 5 0 0 & \text { encounter   obstacles } \\ - 2 0 0 & \text { remain   stationary } \\ - 1 0 0 & \text { move   further   away   from   the   target } \\ 1 0 0 & \text { get   closer   to   the   target } \\ 5 0 0 & \text { reaching   the   target } \end{array} \right.\tag{3.2}
$$

## 3.4 Experimental result presentation

The experiment utilized the Tkinter library on the VSCode platform to create a 16 \* 16 simulation grid environment, as shown in Figure 3.4. The white cells in the environment represent accessible areas, red squares represent agents, yellow ellipses represent destinations, and black squares represent obstacles. In order to ensure the universality of the algorithm under different difficulty levels, three maps with different characteristics of obstacle layouts were designed.

![](Wang2025PERDPP_figs/89e05d94a0bbf89b40b9bb0662c4e1b5ccb4e5046b8c91523ecedf4d7e0f63c7.jpg)  
Figure 3.4 three maps

Among them, the obstacles in Map 1 are random distributed and have a high density; Obstacles are random distributed and relatively sparse in Map 2 ; The obstacle design in Map 3 has a certain degree of guidance, with obstacles concentrated in the lower left corner. In the early stages of exploration, there is only one feasible path that approaches the lower left corner. The agent needs to learn the path to transfer to the lower right corner in the middle and later stages in order to successfully reach the target. The presentation and analysis of the training results are as follows:

![](Wang2025PERDPP_figs/eb0527ae80af6925ea260bcaaec0432fafa4934e7f6c6064c698c571f6a84272.jpg)  
Figure 3.5 Successful Rate Convergence Curve of Map 1

![](Wang2025PERDPP_figs/f964882cf66ad6c6994aefb15d58754201badd2627c7119bca15493c4d2cbab7.jpg)  
Figure 3.6 Successful Rate Convergence Curve of Map 2

In the early stages of training, the convergence curves of the successful rate within the epoch of Map 1 and Map 2 are similar (where the successful rate within the epoch refers to the average successful rate of all complete rounds in the current epoch), as shown in Figure 3.5 and 3.6. During the experiment, it was observed that the elastic step mechanism of Elastic DQN adopted a large average number of steps in the early stages of training, and the data update of the experience pool was relatively slow. The speed of model training successful rate increase was not as fast as that of DQN. However, as the training data collected from the experience pool gradually increased, the number of elastic steps decreased, and the training process accelerated

We define the average successful rate of the agent during the last 10 epochs as the final convergence successful rate of the algorithm. On Map 1, the final convergence successful rate of standard DQN is 51.9%, and the curve reaches for the first time in the 63rd epoch; The final convergence successful rate of Elastic DQN is 54.1%, and the curve reaches for the first time in the 62nd epoch; The final convergence successful rate of PER-DPP ElasticDQN is 56.7%, and the curve reaches for the first time in the 50th epoch. On Map 2, the final convergence successful rate of standard DQN is 66.2%, and the curve reaches for the first time in the 47th epoch; The final convergence successful rate of Elastic DQN is 69.1%, and the curve reaches for the first time in the 53rd epoch; The final convergence successful rate of PER-DPP ElasticDQN is 70.6%, and the curve reaches for the first time in the 46th epoch. The above results indicate that introducing the PER-DPP sampling framework based on the Elastic DQN algorithm can accelerate the convergence of the model to a certain extent and improve the successful rate of path planning.

![](Wang2025PERDPP_figs/78174bd7ea60180ad49d132cfc203569009f72f1fb14dd03a083dc8560304772.jpg)  
Figure 3.7(a) DQN path in map1

![](Wang2025PERDPP_figs/30bda6e903ac2abe81103a879ee58879368fae684d1693bedd181f5a666ee30c.jpg)  
Figure 3.7(b) Elastic DQN path in map1

![](Wang2025PERDPP_figs/d9e0ec00e954e83748af4f9de33010f550540d07ba9a7b2d1a61d883563417ae.jpg)  
Figure 3.7(c) PDE path in map1

![](Wang2025PERDPP_figs/6fe8a955f039d895149cc989e479bae48b464f2d6ca8908bee68cf564c694bda.jpg)

![](Wang2025PERDPP_figs/9d52be5a1a195e86c63c47f602c9b7e68e937d7a2c8e855da311079ff35f724b.jpg)  
Figure 3.7(e) Elastic DQN path in map2

Figure 3.7(d) DQN path in map2  
![](Wang2025PERDPP_figs/6d3915e90e2046645ea4269b1fe28684a9ed7680a06de2cf02b04db9009c9ea2.jpg)  
Figure 3.7(f) PDED path in map2  
The optimal path, path length, and number of turns planned by three algorithms

on two maps are shown in Figure 3.7 and Table 3.3(PER-DPP-Elastic DQN is abbreviated as PDED)

Table 3.3 Three algorithms for optimal path information on Map 1 and Map 2

<table><tr><td>Algorithm</td><td>Map</td><td>Length</td><td>Number of turns</td></tr><tr><td>DQN</td><td>Map1</td><td>27</td><td>6</td></tr><tr><td>Elastic-DQN</td><td>Map1</td><td>25</td><td>10</td></tr><tr><td>PER-DPP-ElasticDQN</td><td>Map1</td><td>23</td><td>7</td></tr><tr><td>DQN</td><td>Map2</td><td>28</td><td>6</td></tr><tr><td>Elastic-DQN</td><td>Map2</td><td>28</td><td>11</td></tr><tr><td>PER-DPP-ElasticDQN</td><td>Map2</td><td>25</td><td>6</td></tr></table>

On Map 1, although the optimal path length of Elastic DQN has been reduced compared to standard DQN, the number of turns has significantly increased; There is also a similar trend in the optimal path turning times between Elastic DQN and DQN on Map 2. After further introducing the PER-DPP sampling framework, Map 1 and Map 2 showed better performance in terms of optimal path length and number of turns.

Compared to Map 1 and Map 2, the obstacle distribution in Map 3 is more unique, with the average successful rate curve and optimal path shown in Figures 3.8 and 3.9. The optimal path length and number of turns are shown in Table 3.4

![](Wang2025PERDPP_figs/2f21d65fb8a1378827d8ef6ebfff7653b4de18178a7f0e4c49a9dceff4f36d49.jpg)  
Figure 3.8 Successful Rate Convergence Curve of Map 3

On Map 3, the final convergence successful rate of DQN is 55%, and the curve reaches the final convergence success rate for the first time in epoch 78; The final convergence successful rate of Elastic DQN is 64.3%, and the curve reaches the final convergence success rate for the first time in the 76th epoch; The final convergence success rate of PER-DPP-ElasticDQN is 64.2%, and the curve reaches the final convergence successful rate for the first time in the 58th epoch

![](Wang2025PERDPP_figs/1ac5cbb9ed2e69d81ab818bf59f5a10c083012965f79519d3fc3b3c4bb5659b7.jpg)  
Figure 3.9(a) DQN path in map3

![](Wang2025PERDPP_figs/24d08809ff829220e92b65266ff0c4b608743110b135803204bc35550d54dd41.jpg)

Figure 3.9(b) Elastic DQN path in map3  
![](Wang2025PERDPP_figs/9ca26f1643e1fdc0ddf809356554422c500d4375c24ecd1311cc932383d36965.jpg)  
Figure 3.9(c) PDED path in map3

Table 3.4 Three algorithms for optimal path information on Map 3

<table><tr><td>Algorithm</td><td>Map</td><td>Length</td><td>Number of turns</td></tr><tr><td>DQN</td><td>Map3</td><td>23</td><td>16</td></tr><tr><td>Elastic-DQN</td><td>Map3</td><td>22</td><td>15</td></tr><tr><td>PER-DPP-ElasticDQN</td><td>Map3</td><td>19</td><td>8</td></tr></table>

The optimal path lengths of the three algorithms on Map 3 decrease sequentially. The PER-DPP-ElasticDQN algorithm also significantly reduces the number of turns required for the optimal path compared to the other two algorithms. It is worth noting that unlike Map 1 and Map 2, the DQN algorithm did not show an early increase in success rate during the initial training stage. Observing the experimental process, it was found that in the early training stage, the agent tended to continuously take downward actions and enter the area with dense obstacles in the lower left corner. Therefore, the convergence curve of the success rate only showed signs of gradually increasing after about 36 epochs. This may be because the PER-DPP mechanism can help the agent learn rich empirical information earlier.

This chapter combines the PER-DPP sampling framework with the Elastic DQN algorithm to form the PER-DPP-Elastic DQN algorithm. Three maps with different characteristics were designed in a two-dimensional maze environment, and the training results of DQN, Elastic DQN, and PER-DPP Elastic DQN were compared on them. In Map 1 and Map 2, introducing the Elastic step mechanism during the initial training stage can result in a higher number of learning steps and a slower learning process compared to DQN. However, with the accumulation of empirical data, the PER-DPP-Elastic DQN algorithm can help agents learn paths with better performance in both path length and turning times at a faster speed. In addition, the experimental results in Map 3 indicate that PER-DPP ElasticDQN is more adaptable to environments with special information compared to DQN.

## References

[1] Richard S. Sutton, Andrew G Barto. Reinforcement Learning: An Introduction, 2nd Edition [2nd ed][M].Bradford Books,2018.

[2] Schaul T,Quan J,Antonoglou I,et al.Prioritized Experience Replay[C].//4th International Con -ference on Learning Representations, ICLR 2016.2016.

[3] Kulesza A,Taskar B.Determinantal Point Processes for Machine Learning[J].Foundations and Trends in Machine Learning,2012,5,(2-3):123-286.

[4] Chen L M,Zhang G X,Zhou H N.Fast Greedy MAP Inference for Determinantal Point Process to Improve Recommendation Diversity[J].arXiv,2017.

[5] Ly A,Dazeley R,Vamplew P, et al.Elastic step DQN: A novel multi-step algorithm to alleviate overestimation in Deep Q-Networks[J].Neurocomputing,2024,576.

[6] Fujimoto S,van Hoof H,Meger D. Addressing Function Approximation Error in Actor- Critic Methods[C].//35th International Conference on Machine Learning (ICML).2018:2587-2601.

[7] Fedus W,Ramachandran P ,Agarwal R,et al. Revisiting Fundamentals of Experience Replay [C].//International Conference on Machine Learning (ICML).2020:3042-3052.

[8] Li J X,Chen Y T,Zhao X N,et al.An improved DQN Path Planning Algorithm[J].Journal of Supercomputing,2022,78,(1):616-639.

[9] Zhao K Y,Wang Y M,Chen Y Y, et al.Efficient Diversity-based Experience Replay For Deep Reinforcement Learning[J].arXiv,2024