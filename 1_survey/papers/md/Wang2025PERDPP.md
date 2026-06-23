---
citation_key: Wang2025PERDPP
arxiv_id: 2503.07411
arxiv_url: "https://arxiv.org/abs/2503.07411"
title: "PER-DPP Sampling Framework and Its Application in Path Planning"
authors_short: "Junzhe Wang"
year: 2025
direction_tag: Q_informed_sampling
source: pymupdf4llm
converted_at: 2026-06-23T18:11:09Z
origin: ai+web
reviewed: false
---

PER-DPP Sampling Framework and Its Application in Path Planning 

# **PER-DPP Sampling Framework and Its Application in Path Planning** 

## Junzhe Wang 

## **1. Abstract** 

Autonomous navigation in intelligent mobile systems represents a core research focus within artificial intelligence-driven robotics. Contemporary path planning approaches face constraints in dynamic environmental responsiveness and multi-objective task scalability, limiting their capacity to address growing intelligent operation requirements. Decision-centric reinforcement learning frameworks, capitalizing on their unique strengths in adaptive environmental interaction and selfoptimization, have gained prominence in advanced control system research. 

This investigation introduces methodological improvements to address sample homogeneity challenges in reinforcement learning experience replay mechanisms. By incorporating determinant point processes (DPP) for diversity assessment, we develop a dual-criteria sampling framework with adaptive selection protocols. This approach resolves representation bias in conventional prioritized experience replay (PER) systems while preserving algorithmic interoperability, offering improved decision optimization for dynamic operational scenarios. Key contributions comprise: 

Develop a hybrid sampling paradigm (PER-DPP) combining priority sequencing with diversity maximization.Based on this,create an integrated optimization scheme (PER-DPP-Elastic DQN) merging diversity-aware sampling with adaptive step-size regulation. Comparative simulations in 2D navigation scenarios demonstrate that the elastic step-size component temporarily delays initial convergence speed but synergistically enhances final-stage optimization with PER-DPP integration. The synthesized method generates navigation paths with optimized length efficiency and directional stability. 

1 

PER-DPP Sampling Framework and Its Application in Path Planning 

## **2. Preliminaries** 

## **2.1 Reinforcement Learning[[1]]** 

Reinforcement Learning is a learning paradigm where agents autonomously learn to make decision by interacting with an environment, with the goal of maximizing expected rewards. The system is formalized as a Markov Decision Process (MDP), which is defined by a tuple ⟨S,A,P,R,γ⟩, where S represents the state space, A represents the action space, P defines the state transition probabilities, R denotes the reward function, and γ is the discount factor. At each step t, the environment is in a state _[s] t_[, and ] the agent selects an action at according to a policy π. The environment then transitions to a new state based on the transition probability _P_ ( _st_ + 1 | _st_ , _at_ ) , and the agent receives a * reward. The agent’s objective is to learn an optimal policy  that maximizes the expected cumulative discounted reward starting from any initial state _st_ : 

2 _V_  ( _s_ ) = _E_ [ _Gt_ | _St_ = _s_ ]= _E_ [ _Rt_ + _Rt_ + 1 + _Rt_ + 2 + ....| _St_ = _s_ ] （2.1） where _V_  ( _s_ ) is the value function that estimates the expected return when following policy π from state _st_ 

## **2.2 Experience Replay** 

In deep reinforcement learning, experience replay plays a critical role by allowing agents to store and reuse historical interactions through a replay buffer. This approach addresses the problem of data correlation inherent in online training processes while enhancing the utilization efficiency of samples. A notable advancement in optimizing experience replay is Prioritized Experience Replay[[2]] (PER), which strategically weights past experiences to improve learning effectiveness. PER enhances the effectiveness of experience replay mechanisms by selectively emphasizing transitions with higher learning significance, as determined through temporal difference (TD) error measurements, as (2.2). 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0002-07.png)


In PER, an experience is assigned a priority _p j_ = |  _j_ | +  where  ensures nonzero priority. The probability P(j) of sampling an experience is proportional to its priority: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0002-09.png)


By focusing on experiences with higher TD errors, PER enhances learning efficiency and accelerates convergence. 

2 

PER-DPP Sampling Framework and Its Application in Path Planning 

## **2.3 Determinantal Point Processes[[3]]** 

There are various methods to measure sample heterogeneity. Many methods struggle to efficiently select highly diverse samples and often require substantial prior knowledge.The Determinantal Point Process (DPP) is a probabilistic model that defines correlations among samples via a kernel matrix, simplifying probability calculations through determinant computations. Elements in the kernel matrix represent pairwise similarities between samples, and the determinant value reflects the degree of heterogeneity within a subset. When a subset contains overly similar elements, the determinant decreases, thereby reducing the probability of their co-occurrence. DPP excels at modeling the balance between diversity and quality of elements in a set and is widely applied in recommendation systems, text summarization, image retrieval, and similar scenarios. Its core idea lies in measuring subset probabilities via matrix determinants, favoring subsets that are both high-quality and diverse. With its unique mathematical formulation and flexible design, DPP provides an efficient and powerful tool for addressing diversity and correlation challenges. A brief introduction is provided below. 

Given a predefined sample set Z  and its kernel function K , a probability measure space ( _Z_ ,2 _Z_ , _P_ ) can be mathematically defined. The definitions of Z and P are as follows: Let the candidate sample set Z = { _z_ 1, _z_ 2... _zN_ } contain N samples. The Determinantal Point Process (DPP) transforms complex probability calculations into simplified determinant computations, where the probability of sampling any subset _Y_  _Z_ is proportional to the determinant of its corresponding kernel submatrix _KY_ , as shown in Equation (2.4). Here, _KY_ denotes the Gaussian kernel matrix associated with the subset Y, which is a submatrix of the original kernel matrix K. 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0003-04.png)


The DPP algorithm can be formulated as the following determinant maximization problem: argmax _Y_  _R_ log(det( _KY_ )) .However, this constitutes an NP-Hard problem. Traditional MAP requires computing determinants over all possible subsets, resulting in exponential complexity ( O( _N_ 3 _M_ 3 ) , where N is the total number of elements and M is the target subset size), which becomes intractable for large-scale datasets. In practical implementations, greedy algorithms[[4]] are commonly employed to reduce computational complexity to O( _M_ 2 _N_ ) while guaranteeing near-optimal solutions. 

The greedy selection process iteratively selects a sample j from the candidate set that maximizes the marginal gain and adds it to the resulting subset Y until a stopping 

3 

PER-DPP Sampling Framework and Its Application in Path Planning 

criterion is met, as formalized in Equation (2.5). 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0004-02.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0004-03.png)


Then we get: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0004-05.png)


According to (2.10), we can simplify (2.5) as follows: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0004-07.png)


The advantage of this method lies in transforming the Cholesky decomposition process into an incremental computation rather than direct decomposition when adding new samples. After incorporating sample i , obtained through Equation (2.11), into the acquired subset Y , the updated Cholesky decomposition of the sub-kernel matrix can be derived according to Equation (2.7) as follows: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0004-09.png)


Similar to(2.8), _Ci_ and _di_ are updated and recorded, for every _j_  _R_ \ ( _Y_  { }) _i_ we can get a new decomposition as follows: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0004-11.png)


Then with (2.8) and (2.14),we can get: 

PER-DPP Sampling Framework and Its Application in Path Planning 

## **[5]** 

## **2.4 Elastic DQN** 

The Elastic DQN algorithm primarily integrates the concepts of Coarse Q- Learning and multi-step DQN learning, leveraging their distinctive properties to mitigate overestimation and enhance the overall performance of DQN. First, to incorporate Coarse Q-Learning principles, a memory bank is introduced before the experience replay buffer. This module employs unsupervised clustering analysis to evaluate the similarity between the current state and previous states. Meanwhile, multistep DQN exhibits sensitivity to the hyperparameter controlling the number of learning steps. The memory bank dynamically adjusts learning steps by aggregating updates for similar states into a single operation while processing dissimilar states independently, thereby enabling adaptive step-size updates. The algorithm workflow is illustrated in Figure 2.1. 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0005-04.png)


Figure 2.1 Elastic DQN workflow 

## **3. PER-DPP-Elastic DQN** 

## **3.1 PER-DPP sampling paradigm** 

Fujimoto et al[[6] ] demonstrated that prioritized sampling may excessively focus on a small subset of samples with high temporal-difference (TD) errors, leading to overreuse of specific samples and consequently reducing sample diversity. Fedus et al[[7] ] further noted that the prioritization mechanism in PER introduces distributional bias, causing models to overemphasize early high-error samples, which may not optimally benefit long-term learning. Li et al[[8]] improved algorithmic efficiency by filtering highsimilarity sequences duringexperience replay to reduce redundancy. Zhao et al[[9] ] proposed incorporating sample diversity into batch sampling, where higher heterogeneity 

5 

PER-DPP Sampling Framework and Its Application in Path Planning 

among samples accelerates agent learning. To address PER-induced diversity reduction caused by overemphasis on high-TD-error samples, this study introduces a two-stage hybrid algorithm. The first stage employs PER for importance calculation and ranking to select a larger batch of experiences, followed by the Fast Greedy MAP algorithm to extract a subset with enhanced diversity from this batch. 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0006-02.png)


Figure 3.1 PER-DPP workflow 

## **3.2 PER-DPP-Elastic DQN Algorithm** 

Similar to (2.2), we found that for multi-step DQN, TD error is as follow: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0006-06.png)


The Elastic DQN algorithm stores step-count information in the experience replay buffer and utilizes a multi-step DQN approach for agent network parameter updates. When integrated with the PER-DPP sampling framework, corresponding modifications to priority calculations are required. The associated pseudocode is provided as the following Table 3.1: 

Table 3.1 Pseudo code for PER-DPP- Elastic DQN 

**Initialization** ：step length d=0, replay buffer D, memory bank B, Setting the target network and main network with the same shape and initial parameters. While not finished： 

For every time step t： 

## **Experience sample clustering judgment or storage:** 

1.with  -greedy policy, get action _at_ from _[s] t_ 

2.get next state _st_ + _d_ + 1 and reward _[r] t_[  ,compute the Q value of ] _[s] t_[  and] 

_s t_ + _d_ + 1 

6 

PER-DPP Sampling Framework and Its Application in Path Planning 

3.store _Q_ ( _st_ ) and _Q_ ( _st_ + _d_ + 1) into memory bank B 

4.get samples from B to apply clustering,and add Q value into the samples 

5. Using the HDBSCAN, make the following judgments on the results： 

If _Q_ ( _st_ ) and _Q_ ( _st_ + _d_ + 1) have the same lable： 

store ( _st_ , _at_ , _Rt_ , _st_ + _d_ + 1, _d_ ) into D，with most priority _pt_ 

reset d=0 

else,compute accumulative reward： 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0007-08.png)


## **Sample and update network parameters:** 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0007-10.png)


8.update the priority _p j_ = |  _j_ | = | _Rj_ + _d_ + 1 max _a Q_ ( _s j_ + _d_ + 1, _a_ , _wT_ ) − _Q_ ( _s j_ , _a j_ , _w_ )| 

9.calculate the kernel matrix for measuring sample similarity 

10. Using the Fast Greedy MAP to select small batches of empirical samples 

11. Update network parameters based on experience and weights 

_st_  _st_ + 1 

## **Copy the main network parameters to the target network every T times** 

## **3.3 Experimental design** 

This section briefly introduces the two-dimensional maze environment for path planning (as shown in Figure 3.2), including the design of state space, action space, and reward function, and presents the experimental results of PER-DPP-Elastic DQN on three maps in the above environment. 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0007-19.png)


Figure 3.2 Two dimensional maze environment 

7 

PER-DPP Sampling Framework and Its Application in Path Planning 

in the exploration task of unknown environments, this study constructed three core state parameters as shown in Table 3.2: 

Table 3.2 State Space for Two Dimensional Maze Environment 

|Table 3.2 State|Space for Two Dimensional Maze Environment|
|---|---|
|Parameter|Parameter meaning|
|dx|horizontal distance from the target point|
|dy|vertical distance from the target point|
|ob|information on 8 nearbyobstacles|



Based on the actual situation, this study sets up an 8-dimensional action space, representing 8 directions on a two-dimensional plane: front, back, left, right, and left front, left back, right front, right back. The executed action moves one unit distance in the corresponding direction, as shown in Figure 3.3: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0008-05.png)


Figure 3.3 maze environment action space 

The design of the reward function r is shown in (3.2), which is relatively simple and easy to understand. If the agent remains stationary, a penalty of -200 will be given to encourage the agent to explore the environment; If the intelligent agent reaches its destination after performing an action, a large reward of 500 will be given; If the intelligent agent encounters an obstacle after performing an action, a large punishment of -500 will be given; If the intelligent agent is closer to the target after performing an action, a reward of 100 will be given; If the target point is far away, a penalty of -100 will be imposed. 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0008-08.png)


8 

PER-DPP Sampling Framework and Its Application in Path Planning 

## **3.4 Experimental result presentation** 

The experiment utilized the Tkinter library on the VSCode platform to create a 16 * 16 simulation grid environment, as shown in Figure 3.4. The white cells in the environment represent accessible areas, red squares represent agents, yellow ellipses represent destinations, and black squares represent obstacles. In order to ensure the universality of the algorithm under different difficulty levels, three maps with different characteristics of obstacle layouts were designed. 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0009-03.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0009-04.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0009-05.png)


Figure 3.4 three maps 

Among them, the obstacles in Map 1 are random distributed and have a high density; Obstacles are random distributed and relatively sparse in Map 2 ; The obstacle design in Map 3 has a certain degree of guidance, with obstacles concentrated in the lower left corner. In the early stages of exploration, there is only one feasible path that approaches the lower left corner. The agent needs to learn the path to transfer to the lower right corner in the middle and later stages in order to successfully reach the target. The presentation and analysis of the training results are as follows: 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0009-08.png)


Figure 3.5 Successful Rate Convergence Curve of Map 1 

9 

PER-DPP Sampling Framework and Its Application in Path Planning 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0010-01.png)


Figure 3.6 Successful Rate Convergence Curve of Map 2 

In the early stages of training, the convergence curves of the successful rate within the epoch of Map 1 and Map 2 are similar (where the successful rate within the epoch refers to the average successful rate of all complete rounds in the current epoch), as shown in Figure 3.5 and 3.6. During the experiment, it was observed that the elastic step mechanism of Elastic DQN adopted a large average number of steps in the early stages of training, and the data update of the experience pool was relatively slow. The speed of model training successful rate increase was not as fast as that of DQN. However, as the training data collected from the experience pool gradually increased, the number of elastic steps decreased, and the training process accelerated 

We define the average successful rate of the agent during the last 10 epochs as the final convergence successful rate of the algorithm. On Map 1, the final convergence successful rate of standard DQN is 51.9%, and the curve reaches for the first time in the 63rd epoch; The final convergence successful rate of Elastic DQN is 54.1%, and the curve reaches for the first time in the 62nd epoch; The final convergence successful rate of PER-DPP ElasticDQN is 56.7%, and the curve reaches for the first time in the 50th epoch. On Map 2, the final convergence successful rate of standard DQN is 66.2%, and the curve reaches for the first time in the 47th epoch; The final convergence successful rate of Elastic DQN is 69.1%, and the curve reaches for the first time in the 53rd epoch; The final convergence successful rate of PER-DPP ElasticDQN is 70.6%, and the curve reaches for the first time in the 46th epoch. The above results indicate that introducing the PER-DPP sampling framework based on the Elastic DQN algorithm can accelerate the convergence of the model to a certain extent and improve the successful rate of path planning. 

10 

PER-DPP Sampling Framework and Its Application in Path Planning 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0011-01.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0011-02.png)


Figure 3.7(a) DQN path in map1 

Figure 3.7(b) Elastic DQN path in map1 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0011-05.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0011-06.png)


Figure 3.7(c) PDE path in map1 

Figure 3.7(d) DQN path in map2 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0011-09.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0011-10.png)


Figure 3.7(e) Elastic DQN path in map2 Figure 3.7(f) PDED path in map2 The optimal path, path length, and number of turns planned by three algorithms 

11 

PER-DPP Sampling Framework and Its Application in Path Planning 

on two maps are shown in Figure 3.7 and Table 3.3(PER-DPP-Elastic DQN is abbreviated as PDED) 

Table 3.3 Three algorithms for optimal path information on Map 1 and Map 2 

|Algorithm|Map|Length|Number of turns|
|---|---|---|---|
|DQN|Map1|27|6|
|Elastic-DQN|Map1|25|10|
|PER-DPP-ElasticDQN|Map1|23|7|
|DQN|Map2|28|6|
|Elastic-DQN|Map2|28|11|
|PER-DPP-ElasticDQN|Map2|25|6|



On Map 1, although the optimal path length of Elastic DQN has been reduced compared to standard DQN, the number of turns has significantly increased; There is also a similar trend in the optimal path turning times between Elastic DQN and DQN on Map 2. After further introducing the PER-DPP sampling framework, Map 1 and Map 2 showed better performance in terms of optimal path length and number of turns. 

Compared to Map 1 and Map 2, the obstacle distribution in Map 3 is more unique, with the average successful rate curve and optimal path shown in Figures 3.8 and 3.9. The optimal path length and number of turns are shown in Table 3.4 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0012-06.png)


Figure 3.8 Successful Rate Convergence Curve of Map 3 

On Map 3, the final convergence successful rate of DQN is 55%, and the curve reaches the final convergence success rate for the first time in epoch 78; The final convergence successful rate of Elastic DQN is 64.3%, and the curve reaches the final convergence success rate for the first time in the 76th epoch; The final convergence 

12 

PER-DPP Sampling Framework and Its Application in Path Planning 

success rate of PER-DPP-ElasticDQN is 64.2%, and the curve reaches the final convergence successful rate for the first time in the 58th epoch 


![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0013-02.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0013-03.png)



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0013-04.png)


**----- Start of picture text -----**<br>
Figure 3.9(a) DQN path in map3       Figure 3.9(b) Elastic DQN path in map3<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Wang2025PERDPP_figs/Wang2025PERDPP.pdf-0013-05.png)


Figure 3.9(c) PDED path in map3 

Table 3.4 Three algorithms for optimal path information on Map 3 

|Algorithm|Map|Length|Number of turns|
|---|---|---|---|
|DQN|Map3|23|16|
|Elastic-DQN|Map3|22|15|
|PER-DPP-ElasticDQN|Map3|19|8|



The optimal path lengths of the three algorithms on Map 3 decrease sequentially. The PER-DPP-ElasticDQN algorithm also significantly reduces the number of turns required for the optimal path compared to the other two algorithms. It is worth noting that unlike Map 1 and Map 2, the DQN algorithm did not show an early increase in success rate during the initial training stage. Observing the experimental process, it was found that in the early training stage, the agent tended to continuously take downward actions and enter the area with dense obstacles in the lower left corner. Therefore, the convergence curve of the success rate only showed signs of gradually increasing after 

13 

PER-DPP Sampling Framework and Its Application in Path Planning 

about 36 epochs. This may be because the PER-DPP mechanism can help the agent learn rich empirical information earlier. 

This chapter combines the PER-DPP sampling framework with the Elastic DQN algorithm to form the PER-DPP-Elastic DQN algorithm. Three maps with different characteristics were designed in a two-dimensional maze environment, and the training results of DQN, Elastic DQN, and PER-DPP Elastic DQN were compared on them. In Map 1 and Map 2, introducing the Elastic step mechanism during the initial training stage can result in a higher number of learning steps and a slower learning process compared to DQN. However, with the accumulation of empirical data, the PER-DPPElastic DQN algorithm can help agents learn paths with better performance in both path length and turning times at a faster speed. In addition, the experimental results in Map 3 indicate that PER-DPP ElasticDQN is more adaptable to environments with special information compared to DQN. 

## **References** 

- [1] Richard S. Sutton, Andrew G Barto. Reinforcement Learning: An Introduction, 2nd Edition [2nd ed][M].Bradford Books,2018. 

- [2] Schaul T,Quan J,Antonoglou I,et al.Prioritized Experience Replay[C].//4th International Con -ference on Learning Representations, ICLR 2016.2016. 

- [3] Kulesza A,Taskar B.Determinantal Point Processes for Machine Learning[J].Foundations and Trends in Machine Learning,2012,5,(2-3):123-286. 

- [4] Chen L M,Zhang G X,Zhou H N.Fast Greedy MAP Inference for Determinantal Point Process to Improve Recommendation Diversity[J].arXiv,2017. 

- [5] Ly A,Dazeley R,Vamplew P, et al.Elastic step DQN: A novel multi-step algorithm to alleviate overestimation in Deep Q-Networks[J].Neurocomputing,2024,576. 

- [6] Fujimoto S,van Hoof H,Meger D. Addressing Function Approximation Error in Actor- Critic Methods[C].//35th International Conference on Machine Learning (ICML).2018:2587-2601. 

- [7] Fedus W,Ramachandran P ,Agarwal R,et al. Revisiting Fundamentals of Experience Replay [C].//International Conference on Machine Learning (ICML).2020:3042-3052. 

- [8] Li J X,Chen Y T,Zhao X N,et al.An improved DQN Path Planning Algorithm[J].Journal of Supercomputing,2022,78,(1):616-639. 

- [9] Zhao K Y,Wang Y M,Chen Y Y, et al.Efficient Diversity-based Experience Replay For Deep Reinforcement Learning[J].arXiv,2024 

14 

