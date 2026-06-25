---
citation_key: Kim2021Neural
arxiv_id: 2111.06739
arxiv_url: "https://arxiv.org/abs/2111.06739"
title: "Neural Motion Planning for Autonomous Parking"
authors_short: "Dongchan Kim et al."
year: 2021
direction_tag: F_hybrid_astar
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:43:32Z
origin: ai+web
reviewed: false
---

# Neural Motion Planning for Autonomous Parking

Dongchan Kim and Kunsoo Huh

Abstract— This paper presents a hybrid motion planning strategy that combines a deep generative network with a conventional motion planning method. Existing planning methods such as $\mathbf { A } ^ { * }$ and Hybrid $\mathbf { A } ^ { * }$ are widely used in path planning tasks because of their ability to determine feasible paths even in complex environments; however, they have limitations in terms of efficiency. To overcome these limitations, a path planning algorithm based on a neural network, namely the neural Hybrid $\mathbf { A } ^ { * } ,$ is introduced. This paper proposes using a conditional variational autoencoder (CVAE) to guide the search algorithm by exploiting the ability of CVAE to learn information about the planning space given the information of the parking environment. An efficient expansion strategy is utilized based on a distribution of feasible trajectories learned in the demonstrations. The proposed method effectively learns the representations of a given state, and shows improvement in terms of algorithm performance.

## I. INTRODUCTION

Recently, autonomous driving technology has gained popularity. Parking is an essential task in autonomous driving. The autonomous vehicle should recognize the surrounding environment, including the obstacles and free space, and reach the desired goal state while avoiding collisions. Presently, autonomous parking systems are commercially available. In addition, autonomous valet parking that allows an autonomous vehicle to park the car is also available [1].

To date, many path planning algorithms have been developed, such as the artificial potential field (APF) [2], the rapidly exploring random tree (RRT) algorithm [3], the RRT\* algorithm [4], the partial motion planning (PMP) algorithm [5], the $\mathbf { A } ^ { * }$ algorithm [6] and the Hybrid $\mathbf { A } ^ { * }$ algorithm [7]. The potential field method uses the APF-based collision-free holonomic path first and then uses the generated path for further optimization.

Then, the remainder algorithms can be divided into two approaches [8]: sampling based methods and searching based methods. The sampling based methods include two approaches which consist of random sampling based methods and deterministic sampling based methods. First, RRT and $\mathrm { R R T ^ { * } }$ algorithms exist in the random sampling based methods. The RRT-based method constructs trees to connect the nodes obtained from the given sampling distributions. A feasible path is obtained by traversing the tree through nodes. The $\mathrm { R R T ^ { * } }$ algorithm is used to accelerate the computational time by utilizing the rewiring procedure. Then, the PMP method represents for the deterministic sampling based method [5]. This method performs local searching rather than searching entire space to reduce computational burden.

The searching based methods include heuristic based planning and state lattice based planning methods. First, $\mathbf { A } ^ { * }$ and Hybrid $\mathbf { A } ^ { * }$ algorithms are included in heuristic based methods. The $\mathbf { A } ^ { * } .$ -based method uses the $\mathbf { A } ^ { * }$ algorithm to efficiently search for parking spots and serves as a large parking guidance system. It adopts a heuristic function to obtain the optimal path. The Hybrid A\*-based method is used to search for a continuous state, and thereby it mitigates the limitation of classical $\mathbf { A } ^ { * } ,$ , where only the centers of the grid can be visited. The lattice based planning methods utilize the discretization of configuration space into a set of states [9], [10]. The lattice provides a solution as graph search in the motion planning problem.

Among the aforementioned algorithms, we focus on the application of the $\mathbf { A } ^ { * }$ and Hybrid $\mathbf { A } ^ { * }$ algorithms which are widely used for autonomous driving tasks. In particular, the Hybrid $\mathbf { A } ^ { * }$ can generate kinodynamic paths in clustered environments using a simplified vehicle model [7], and the designed paths are close to the human driving style. Therefore, the Hybrid $\mathbf { A } ^ { * }$ algorithm is applied in our study. However, the Hybrid $\mathbf { A } ^ { * }$ algorithm tends to become highly time and memory-intensive as the size of the configuration space grows.

To overcome the limitations of the Hybrid $\mathbf { A } ^ { * }$ algorithm, the strategy in searching which is a state expansion procedure should be improved. Inspired by existing studies on applying deep neural networks in planning problems [11], [12], a path planning algorithm with the help of a guidance map, which is a learned distribution of feasible trajectories, is utilized in this study.

Recently, deep generative networks have been actively studied. For example, a variational autoencoder (VAE), which is a popular method for learning a generative model of a set of data, was utilized [13]. The VAE enables the representation of high-dimensional movements in a lowdimensional latent space. In addition, an optimal movement is available to reproduce the movements. The conditional variational autoencoder (CVAE) incorporates additional conditional input to the VAE method [14]. The CVAE is a deep conditional generative model for structured output prediction that uses Gaussian latent variables. The input observations modulate the prior on the Gaussian latent variables that generate the output. There are several studies on trajectory prediction and multi-modal prediction using the CVAE network where the additional condition could enhance the performance [15], [16].

In this study, a CVAE network-based Hybrid $\mathbf { A } ^ { * }$ algorithm is proposed. The CVAE model is trained to provide the predicted distribution of feasible trajectories when the parking environment, along with the initial and goal states, is given. The contributions of this study can be summarized as follows:

• A neural Hybrid $\mathbf { A } ^ { * }$ algorithm for autonomous parking is proposed that combines a deep generative network and a conventional planning method.

• The CVAE architecture is utilized to learn the feasible trajectory distribution given the map information including the initial and goal states and obstacles.

• The proposed method significantly reduces the computational time and number of nodes in the test scenarios.

• The feasibility of the proposed method is demonstrated in various autonomous parking scenarios in the simulation.

The remainder of this paper proceeds as follows. In Section 2, the conventional Hybrid $\mathbf { A } ^ { * }$ algorithm is described in detail. In Section 3, the neural Hybrid $\mathbf { A } ^ { * }$ algorithm is described. The CVAE architecture is introduced and the proposed hybrid algorithm for autonomous parking is explained. Section 4 details the verification of the proposed algorithm via simulation. Finally, Section 5 summarizes the study and presents the conclusions drawn.

## II. PRELIMINARIES

## A. Hybrid A\* Algorithm

1) Transition Model: The state $\mathbf { x _ { k } } = ( x _ { k } , y _ { k } , \theta _ { k } ) ^ { T }$ represents a state in the planning step k, where $x _ { k } , y _ { k } ,$ , and $\theta _ { k }$ represent the x-axis position, y-axis position and heading angle, respectively. The state transition model in the discretized form is expressed as follows:

$$
\begin{array}{l} {x _ {k + 1} = x _ {k} + d \cos (\theta_ {k}) d i r} \\ {y _ {k + 1} = y _ {k} + d \sin (\theta_ {k}) d i r} \\ {\theta_ {k + 1} = \theta_ {k} + \frac {d}{L} \tan (\delta_ {k}) d i r} \end{array}\tag{1}
$$

where $\delta _ { k }$ is a steering angle candidate belonging to a discretized steering angle set D. dir represents the direction of the vehicle motion and d is the expansion amount during one searching step. The two control actions include the steering angle and direction. D includes a steering angle set between -40<sup>◦</sup> to 40 <sup>◦</sup> with an interval of 10<sup>◦</sup>, and dir has a value of either -1 or 1, each for backward and forward movement.

2) Hybrid $A ^ { * } { : }$ The Hybrid $\mathbf { A } ^ { * }$ algorithm generates a kinodynamic path using the transition model explained in (1). The Hybrid $\mathbf { A } ^ { * }$ implementation uses a resolution of 2 m in the X and Y dimensions, and $1 5 ^ { \circ } { }$ in the heading angle. This information is used to decide whether the candidate nodes are in a certain grid cell, where only the node with the lowest cost is retained.

Algorithm 1 shows the procedure that Hybrid $\mathbf { A } ^ { * }$ algorithm follows. The current state and zero cost are added to the open list. The state $\mathbf { \Pi } ( \mathbf { x } _ { \mathbf { k } } )$ , which has the lowest cost, is excluded from the open list and added to the closed list. The search ends if the goal state is reached. If not, the available actions (steering angle and direction) are used to obtain the next state via the transition model. If the searched state $\mathbf { \Gamma } ( \mathbf { x } _ { \mathbf { k } + 1 } )$ is collision-free and is in the open list, but the sum of the step cost and heuristic is lower than that of the state in the list, the corresponding state is replaced; the state $\mathbf { \Gamma } ( \mathbf { x } _ { \mathbf { k } + 1 } )$ is added to the open list if it is not in the open list. This process is repeated for the states in the open list, and if a selected state is the goal, the search is finished and the optimal trajectory is returned by backtracking via the closed list. The overall pseudocode is presented in Algorithm 1. N represents a node consisting of {state, action, path cost, heuristic, parent node}. <sup>O</sup> and <sup>C</sup> indicate the open list and closed list, respectively. Furthermore, the IsCollide procedure returns 0 when the vehicle is collision-free, and the transition procedure uses (1) to obtain the next state for the given control action.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Function Hybrid A*

Require:  $x_{s}$  : start state, g : goal state,  $h(x)$  : heuristic, O : obstacle

1:  $C \leftarrow \emptyset$ 

2:  $N = \{x_{s}, 0, 0, 0, \emptyset\}$ 

3:  $O \leftarrow N$ 

4: KeepSearching← 1

5: while KeepSearching is 1 do

6: if O is not empty then

7: N = Extract node with minimum  $c + h$  from O

8: Add N to C and Delete from O

9: if N is g then

10: trajectory = Backtracking(N)

11: KeepSearching← 0

12: else

13: foreach  $a \in Available$  action(N) do

14:  $\{x_{n}, c_{n}\} \leftarrow transition(N.x, a, N.c)$ 

15: if IsCollide( $x_{n}$ , O) is 0 then

16:  $N_{n} = \{x_{n}, c_{n}, h(x_{n}), a, N\}$ 

17: if  $N_{n} \in C$  then

18: continue

19: else if  $N_{n}$  has the same state with

20:  $n \in O$  with smaller cost then

21: Replace n with  $N_{n}$ 

22: else

23: Add  $N_{n}$  to O

24:

25: return trajectory
</div>

## III. NEURAL HYBRID A\* ALGORITHM

## A. CVAE Architecture

To learn the distribution of the feasible trajectories for autonomous parking, the CVAE architecture is used, which includes an encoder-decoder network with a conditional input. The conditional input utilized in this study represents the map information including the position and heading of the initial and goal points, the obstacles, and free space.

The overall architecture is shown in Fig. 1. A twodimensional (2-D) image is used to represent the map information, c. The width and height are 250 and 150, respectively, with a resolution of 0.1 m. Each pixel in the image has a specific value of 0 for free space, 1 for obstacle, 2 for start position with an arrow indicating heading information, 3 for goal position with an arrow indicating heading information. The true trajectory, $\xi ,$ is the planned trajectory obtained using the Hybrid $\mathbf { A } ^ { * }$ algorithm. A total of five trajectories are generated and the corresponding pixel in the 2-D image is assigned the value of 1. The true trajectory ξ, depicted with a dotted line, is used only during the training phase.

![](Kim2021Neural_figs/a92a444532c635d36ce2638e0c1462fd58a33174a2a1bbc01eacb3d72786fdc9.jpg)  
Fig. 1. Proposed CVAE architecture for neural motion planning.

The CVAE consists of a generative model $p _ { \rho } ( \xi | \tilde { c } , z )$ and an inference model $q _ { \phi } ( z | c , \xi )$ , and the latent variable z is expressed as follows using the reparameterization trick [17]:

$$
z = \mu_ {\phi} (c, \xi) + \sigma_ {\phi} (c, \xi) \times \epsilon\tag{2}
$$

where $\phi$ and $\rho$ are the parameters of the encoder and decoder networks, respectively. A normal distribution $\mathcal { N } ( 0 , I )$ is utilized to sample $\epsilon .$ To minimize the error between the predicted trajectory distribution $\hat { \xi }$ and the planned trajectory set $\xi ,$ the reconstruction loss is defined as the L2 loss. The CVAE architecture is trained by minimizing the loss function and is defined as follows:

$$
\begin{array}{r l} & {\mathcal {L} = L _ {R E C} + L _ {K L}} \\ & {\quad = \| \xi - \hat {\xi} \| ^ {2} + \beta D _ {K L} (q _ {\phi} (z | c, \xi) | | p (z))} \end{array}\tag{3}
$$

where the hyperparameter $\beta$ balances the two losses. The former loss represents the reconstruction loss, and the latter is the KL divergence loss between the multivariate normal distribution and the output distribution from the encoder.

The true trajectory set $\xi$ is not available in the test phase. Therefore, z is directly sampled from $\mathcal { N } ( 0 , I )$ , and only the decoder part is utilized. Condition c is passed through an encoder to generate a latent vector ${ \tilde { c } } ,$ which is used in the decoder for inference.

Various predicted trajectory distributions can be generated by feeding different conditions such as map information. For example, by varying the start and goal positions along with the heading value, different trajectory distributions are generated. Fig. 2 shows the predicted trajectory distribution when the heading angle of the goal position is the opposite while the starting position and the target parking space are the same. The result indicates that the proposed CVAE network is successfully trained and can distinguish the difference in the map information.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Function Neural Hybrid A*

Require:  $x_{s}$  : start state, g : goal state,  $h(x)$  : heuristic, O : obstacle, Dmap : predicted trajectory distribution map
1:  $C \leftarrow \emptyset$ 
2:  $N = \{x_{s}, 0, 0, 0, \emptyset\}$ 
3:  $O \leftarrow N$ 
4: KeepSearching← 1
5: while KeepSearching is 1 do
6: if O is not empty then
7:    N = Extract node with minimum  $c + h$  from O
8:    Add N to C and Delete from O
9:    if N is g then
10:    trajectory = Backtracking(N)
11:    KeepSearching← 0
12:    else
13:    foreach  $a \in Available$  action(N) do
14:    $\{x_{n}, c_{n}\} \leftarrow transition(N.x, a, N.c)$ 
15:    if Rand() &gt; 0.2 then
16:    if CheckDistMap( $x_{n}$ , Dmap) then
17:    continue
18:    if IsCollide( $x_{n}$ , O) is 0 then
19:    $N_{n} = \{x_{n}, c_{n}, h(x_{n}), a, N\}$ 
20:    if  $N_{n} \in C$  then
21:    continue
22:    else if  $N_{n}$  has the same state with
23:    $n \in O$  with smaller cost then
24:    Replace n with  $N_{n}$ 
25:    else
26:    Add  $N_{n}$  to O
27:
28: return trajectory
</div>

## B. Neural Hybrid A\*

Neural Hybrid $\mathbf { A } ^ { * }$ uses trajectory distribution map information obtained from the CVAE network. The details are

![](Kim2021Neural_figs/b4d4248ede2614ad45db1cb35a66068632398c23936d13a127dc01bd26244f31.jpg)

![](Kim2021Neural_figs/af17d34898f16891774bef5128110bf8c412e464e0f46f1f433890f5ddc44c37.jpg)  
Fig. 2. Example of predicted trajectory distribution: Results (a) with the heading angle of $9 0 ^ { \circ }$ at goal position; (b) with the heading angle of ${ } _ { - 9 0 ^ { \circ } }$ a goal position.

![](Kim2021Neural_figs/14fb160bf7ea5a8ef7796608e51d763269d74cb0ef93865d0c26cc2463bc9001.jpg)  
Fig. 3. Example of the proposed planning strategy based on the predicted distribution.

presented in Algorithm 2 where the requirement includes new input, and Lines 15 to 17 are newly added. Dmap represents the distribution map of the predicted trajectory. The Line 15, a random number $R a n d ( ) \in ( 0 , 1 )$ is checked to determine whether Dmap is utilized. In this study, 80% of the node expansion proceeds with the help of a neural network model. The CheckDistM ap procedure returns 0 if the current state in the Dmap has a value greater than a certain threshold. As seen in Lines 16 and 17, if the Dmap has a value below the threshold in the position of state $\mathbf { x _ { n } } ,$ the action chosen in Line 13 is deemed unnecessary; otherwise, the next step is to proceed. Thus, with this state expansion strategy, the control action is chosen efficiently by performing the expansion mostly based on the learned trajectory distribution. Fig. 3 represents an example image of the aforementioned planning strategy. The expansion by the predefined action set is performed in the upper image which uses the conventional method. In the bottom image, an efficient expansion method is performed based on the predicted distribution from CVAE.

## IV. SIMULATION

In this section, the dataset acquisition, implementation details, evaluation of the CVAE model, and the results are discussed. The neural network model was designed and trained using PyTorch [18], an open source Python library. Hybrid $\mathbf { A } ^ { * } ,$ , a motion planning algorithm, is implemented in Python.

## A. Dataset

To train the model, expert trajectory sets are collected using the Hybrid $\mathbf { A } ^ { * }$ algorithm. Each scene has a combination of five trajectories. The hybrid $\mathbf { A } ^ { * }$ algorithm is a deterministic method, resulting in the same solution. Therefore, the order of action set D is randomly mixed to obtain different trajectories for the proposed network training. A total of 1,000 scenarios are simulated for the data collection. The start position is randomly sampled in free space, and the heading angle is sampled from either $0 ^ { \circ }$ or 180<sup>◦</sup>. The parking space is randomly selected, and the goal position is selected accordingly. The heading angle of the goal position is randomly sampled either from ${ } _ { - 9 0 ^ { \circ } }$ or 90<sup>◦</sup>. The collected dataset is utilized as a conditional input and label for training the proposed CVAE network.

## B. Implementation Details

The overall network is composed of an encoder and a decoder. There are two encoders, one for encoding the map information to be used in the decoder, and the other is for encoding the planned trajectories along with the map information to produce a latent vector.

![](Kim2021Neural_figs/8fdf2ab20e3f939c05f6afdc6b8882362a796db4c790807e2ac967362543f7fc.jpg)

![](Kim2021Neural_figs/07829e6cf2183d7a222e89b6d675aca9b9c4b1c4f382617cde39ccb43b2bd58b.jpg)

Fig. 4. Comparison between the proposed method and the conventional method in scenario 1. The blue distribution represents the predicted distribution of the feasible trajectory from the proposed CVAE network. The yellow points indicate the expanded nodes during the planning process.  
![](Kim2021Neural_figs/2d854aa365986b3ea667e00c9b6bd976c11b7bf2918421db00c67b1de8cafdc8.jpg)

![](Kim2021Neural_figs/5834f181cecef92318566b6f12ddd8b7d05d75964613ec34acda6f15c763b7c4.jpg)  
Fig. 5. Five trajectories generated in scenario 1: Results (a) with the proposed method; (b) with the conventional method.

The encoder is composed of a 2-D convolution, batch normalization, rectified linear unit (ReLU) activation function, and fully-connected layers. The convolutional neural network (CNN) model consists of three convolutional layers with output channels of 16, 32 and 64. The kernel size is [4,4], and the stride is 2. For the first encoder, the result is passed through a fully-connected layer with 32 hidden units, which is the dimension of the encoded condition. For the second encoder, the result is passed through two fully-connected layers with 32 hidden units, which is the dimension of the latent variable.

The decoder is composed of a fully-connected layer, 2- D deconvolution, batch normalization, and ReLU. The CNN model for the decoder consists of three convolutional layers with output channels of 32, 16 and 1. The kernel size and stride are the same as those of the encoder.

In the training process, the optimization was performed using a standard Adam optimizer with a learning rate of 0.001. In addition, parameter $\beta$ for the CVAE loss is set to

0.1.

## C. Evaluation of the CVAE Model

To evaluate the performance of the proposed method, a test dataset is generated. The map information with different initial positions or heading angles with those of the training set is selected for inference. The Figs. 5 to 10 show the results of the proposed neural Hybrid A\* algorithm compared with that of the conventional Hybrid A\* algorithm.

In Fig. 4, the results for the first scenario are compared. The blue distribution represents the predicted distribution of the feasible trajectory from the proposed CVAE network. The yellow circles represent the expanded nodes during this process. The left figure shows the results of the proposed method. As can be seen, along with the expanded nodes, the expansion is mostly done on the learned distribution. In contrast, the right figure shows the result without the help of the learned distribution. The nodes are scattered regardless of the distribution, resulting in high computation.

![](Kim2021Neural_figs/2e86cceef7c8412849764a757f5c9b465f1d05d727ee07db104ea6ce8274575e.jpg)

![](Kim2021Neural_figs/55877eba9c02d3dc447acf1e360cded67088c4bb77fec24acfff5c6b3e6f1287.jpg)

Fig. 6. Comparison between the proposed method and the conventional method in scenario 2.  
![](Kim2021Neural_figs/ed93b09cbea6b3673d53b32a246b79ee4cfa1c6cd53d20ad62b22d2337da5435.jpg)

![](Kim2021Neural_figs/89e9544cf7a7bf4f5b4c4a010f0ce76900ee35f845538a80963c53503dee666f.jpg)  
Fig. 7. Five trajectories generated in scenario 2: Results (a) with the proposed method; (b) with the conventional method.

Fig. 5 shows the planning result with the five trajectories generated. As shown in the figure on the left, the generated trajectories are mostly on the predicted distribution. The right figure shows that the planning results are more random regardless of the distribution, as no information on the CVAE network is used.

Fig. 6 shows the results for the second scenario. The heading angle of the initial point is set to $1 7 0 ^ { \circ }$ , which is not included in the training dataset. The generated distribution seems to be utilized well as a guidance map as the expansion is nearly completed on the distribution map. However, as seen in the right figure, the expansion proceeds by covering a wider range when the distribution map is not utilized, resulting in a higher cost of node expansion.

Fig. 7 also shows the results with the five trajectories generated. As shown in the left figure, the generated trajectories are mostly on the predicted distribution using the neural Hybrid $\mathbf { A } ^ { * }$ method. However, it show more random results without the distribution map.

Figs. 8 to 11 show similar results to those of the aforementioned scenarios. In the third scenario shown in Fig. 9, the CVAE network provides a feasible distribution map even with an initial heading angle of $3 0 ^ { \circ }$ which varies significantly from the training dataset.

TABLE I  
COMPARISON OF METRICS.

<table><tr><td></td><td></td><td>Scen. 1</td><td>Scen. 2</td><td>Scen. 3</td><td>Scen. 4</td></tr><tr><td rowspan="2">Comparison (vs Hybrid A*)</td><td rowspan="2">Time Node</td><td>24.75%</td><td>30.33%</td><td>50.0%</td><td>10.86%</td></tr><tr><td>50.91%</td><td>53.30%</td><td>79.36%</td><td>35.35%</td></tr></table>

To evaluate the performance of the neural Hybrid $\mathbf { A } ^ { * }$ algorithm, two metrics, which comprise computational time and the number of nodes in the open list, are evaluated under the four test scenarios. Table. I shows the performance comparison in terms of the metrics. A statistical result is obtained by evaluating the scenarios five times and using a mean value for the two metrics. In all the test scenarios, the computational time and the number of nodes are significantly reduced with the proposed neural Hybrid $\mathbf { A } ^ { * }$ method compared with the conventional Hybrid $\mathbf { A } ^ { * }$ algorithm. In terms of the computational time, the results illustrate that the neural Hybrid $\mathbf { A } ^ { * }$ algorithm improves the state expansion efficiency of the planning problem for autonomous parking. In addition, in terms of the node, the results indicate that the proposed method is much less memory-intensive than the conventional method.

![](Kim2021Neural_figs/8f504302131a5d270c0052b6a494a8cc6b546dd9b559ead1dc36dcfd33f2dd70.jpg)

![](Kim2021Neural_figs/69e9fc86296ea93c2ed94b3798e5226d998a35ed1906c8527a9f1fdc4aa2b91f.jpg)

Fig. 8. Comparison between the proposed method and the conventional method in scenario 3.  
![](Kim2021Neural_figs/7e41c3fb6913ee7552b9ab8ace6e4913400f4473be721d555855c31dd1c9f55f.jpg)

![](Kim2021Neural_figs/45335954fcf985c91c163e269fe7d8c6f8066240061c84f088ddbc46491324fe.jpg)  
Fig. 9. Five trajectories generated in scenario 3: Results (a) with the proposed method; (b) with the conventional method.

## V. CONCLUSIONS

This paper presents a novel hybrid motion planning strategy for autonomous parking that integrates a deep generative network and a conventional searching based path planning algorithm. The CVAE network is constructed to learn the predicted distribution of the feasible trajectories, given the initial and goal positions along with the obstacle information. The proposed model learns several maps with feasible paths generated by the Hybrid $\mathbf { A } ^ { * }$ algorithm.

The simulation results with the neural Hybrid $\mathbf { A } ^ { * }$ algorithm shows that the neural Hybrid $\mathbf { A } ^ { * }$ algorithm reduces the computational time and number of nodes significantly. $\mathbf { A } \mathbf { s }$ the proposed method uses an expansion strategy based on the predicted distribution, other searching-based planning algorithms can also be applied. In future studies, simulations in more diverse parking scenarios will be conducted.

## REFERENCES

[1] M. Khalid, K. Wang, N. Aslam, Y. Cao, N. Ahmad, and M. K. Khan, “From smart parking towards autonomous valet parking: A survey, challenges and future works,” Journal of Network and Computer Applications, p. 102935, 2020.

[2] Y. Dong, Y. Zhang, and J. Ai, “Experimental test of artificial potential field-based automobiles automated perpendicular parking,” International Journal of Vehicular Technology, vol. 2016, 2016.

[3] Y. Kuwata, G. A. Fiore, J. Teo, E. Frazzoli, and J. P. How, “Motion planning for urban driving using rrt,” in 2008 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE, 2008, pp. 1681– 1686.

[4] J. Vlasak, M. Sojka, and Z. Hanzalek, “Accelerated rrt\* and its ´ evaluation on autonomous parking,” arXiv preprint arXiv:2002.04521, 2020.

![](Kim2021Neural_figs/e4718208c19d1f527cca8e7382e56f0ccbe973925fe229643a72678c50226310.jpg)

![](Kim2021Neural_figs/1fa7db467883599a5578913f8fc491f89536e77ce76e2bfa95e4a6640913ccab.jpg)

Fig. 10. Comparison between the proposed method and the conventional method in scenario 4.  
![](Kim2021Neural_figs/ad220e0ea56ebb1136068bd627ee3eae633c2f1bdcd0fd190b98c202158f5daa.jpg)

![](Kim2021Neural_figs/10abcdbc6fc74968c670837f6dd8406448ceecef672d2e7cb0aa90f3144b2ba0.jpg)  
Fig. 11. Five trajectories generated in scenario 4: Results (a) with the proposed method; (b) with the conventional method.

[5] R. Benenson, S. Petti, T. Fraichard, and M. Parent, “Integrating perception and planning for autonomous navigation of urban vehicles,” in 2006 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE, 2006, pp. 98–104.

[6] L. Cheng, C. Liu, and B. Yan, “Improved hierarchical a-star algorithm for optimal parking path planning of the large parking lot,” in 2014 IEEE International Conference on Information and Automation (ICIA). IEEE, 2014, pp. 695–698.

[7] D. Dolgov, S. Thrun, M. Montemerlo, and J. Diebel, “Path planning for autonomous vehicles in unknown semi-structured environments,” The international journal of robotics research, vol. 29, no. 5, pp. 485– 501, 2010.

[8] O. Sharma, N. C. Sahoo, and N. Puhan, “Recent advances in motion and behavior planning techniques for software architecture of autonomous vehicles: A state-of-the-art survey,” Engineering Applications of Artificial Intelligence, vol. 101, p. 104211, 2021.

[9] A. Bicchi, A. Marigo, and B. Piccoli, “On the reachability of quantized control systems,” IEEE Transactions on Automatic Control, vol. 47, no. 4, pp. 546–563, 2002.

[10] M. Pivtoraiko and A. Kelly, “Efficient constrained path planning via search in state lattices,” in International Symposium on Artificial Intelligence, Robotics, and Automation in Space. Munich Germany, 2005, pp. 1–7.

[11] B. Ichter, J. Harrison, and M. Pavone, “Learning sampling distributions for robot motion planning,” in 2018 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2018, pp. 7087–7094.

[12] J. Wang, W. Chi, C. Li, C. Wang, and M. Q.-H. Meng, “Neural rrt\*: Learning-based optimal path planning,” IEEE Transactions on Automation Science and Engineering, vol. 17, no. 4, pp. 1748–1758, 2020.

[13] N. Chen, M. Karl, and P. Van Der Smagt, “Dynamic movement primitives in latent space of time-dependent variational autoencoders,” in 2016 IEEE-RAS 16th international conference on humanoid robots (Humanoids). IEEE, 2016, pp. 629–636.

[14] K. Sohn, H. Lee, and X. Yan, “Learning structured output representation using deep conditional generative models,” Advances in neural information processing systems, vol. 28, pp. 3483–3491, 2015.

[15] X. Feng, Z. Cen, J. Hu, and Y. Zhang, “Vehicle trajectory prediction using intention-based conditional variational autoencoder,” in 2019 IEEE Intelligent Transportation Systems Conference (ITSC). IEEE, 2019, pp. 3514–3519.

[16] A. Bhattacharyya, M. Hanselmann, M. Fritz, B. Schiele, and C.-N. Straehle, “Conditional flow variational autoencoders for structured sequence prediction,” arXiv preprint arXiv:1908.09008, 2019.

[17] D. P. Kingma and M. Welling, “Auto-encoding variational bayes,” arXiv preprint arXiv:1312.6114, 2013.

[18] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, et al., “Pytorch: An imperative style, high-performance deep learning library,” Advances in neural information processing systems, vol. 32, pp. 8026–8037, 2019.